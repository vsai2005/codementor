"""Google sign-in account resolution with collision-safe usernames.

Identity is the Google subject (`sub`), with the Google-verified email as the link to an
existing account. The username is only a display/login handle, so it is derived from the
email local-part when free and otherwise suffixed deterministically from the identity:

    alex@gmail.com   -> "alex"
    alex@outlook.com -> "alex-3f9a"   (sha256 of the Google sub; longer on further collision)

Inserts run in a SAVEPOINT; a unique-constraint race either means the same person signed
in concurrently (return that account) or the handle was just taken (try the next one).
Nothing here ever updates another user's row.
"""

from __future__ import annotations

import hashlib
import logging
import re
import secrets
from typing import Iterator

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.models import User

log = logging.getLogger(__name__)

USERNAME_MAX_LEN = 30          # matches the register rule ^[a-zA-Z0-9._-]{3,30}$
_BASE_MAX_LEN = 17             # leaves room for "-" + up to 12 suffix characters
_SUFFIX_LENGTHS = (4, 6, 8, 12)
_RANDOM_FALLBACK_TRIES = 5


class GoogleAccountError(Exception):
    """The verified claims cannot be mapped to an account (message is safe to show)."""

    def __init__(self, message: str, status_code: int = 401) -> None:
        super().__init__(message)
        self.status_code = status_code


def username_base(email: str) -> str:
    local = email.split("@", 1)[0].lower()
    base = re.sub(r"[^a-z0-9._-]+", "", local).strip("._-")[:_BASE_MAX_LEN].strip("._-")
    if len(base) < 3:
        base = f"{base}-user" if base else "user"
    return base


def username_candidates(email: str, identity: str) -> Iterator[str]:
    """Readable first, then deterministic identity-derived suffixes, then random ones."""
    base = username_base(email)
    yield base
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    for n in _SUFFIX_LENGTHS:
        yield f"{base}-{digest[:n]}"
    for _ in range(_RANDOM_FALLBACK_TRIES):
        yield f"{base}-{secrets.token_hex(6)}"


def _find_existing(db: Session, sub: str, email: str) -> User | None:
    user = db.execute(select(User).where(User.google_sub == sub)).scalars().first()
    if user is not None:
        return user
    return db.execute(select(User).where(func.lower(User.email) == email)).scalars().first()


def resolve_google_user(db: Session, claims: dict) -> User:
    """Returns the account for verified Google claims, creating it if needed."""
    sub = str(claims.get("sub") or "").strip()
    email = str(claims.get("email") or "").strip().lower()
    if not sub or not email or "@" not in email:
        raise GoogleAccountError("Google sign-in did not provide a usable identity.")

    existing = _find_existing(db, sub, email)
    if existing is not None:
        if existing.google_sub and existing.google_sub != sub:
            # The email belongs to an account bound to a different Google identity.
            raise GoogleAccountError("This email is linked to a different Google account.", 409)
        if existing.google_sub is None:
            existing.google_sub = sub  # link the verified Google identity to this account
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                raise GoogleAccountError("This Google account is already linked to another user.", 409)
        return existing

    display_name = claims.get("name") or email.split("@", 1)[0]
    for candidate in username_candidates(email, sub):
        taken = db.execute(select(User.id).where(User.username == candidate)).first()
        if taken:
            continue
        try:
            with db.begin_nested():
                user = User(
                    email=email,
                    username=candidate,
                    name=display_name,
                    avatar_url=claims.get("picture"),
                    google_sub=sub,
                )
                db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            # Savepoint rolled back. Same identity created concurrently -> use it;
            # otherwise the handle was taken between the check and the insert.
            concurrent = _find_existing(db, sub, email)
            if concurrent is not None:
                return concurrent
            log.info("google sign-in: username %r taken concurrently, trying next", candidate)

    log.error("google sign-in: could not allocate a username for sub hash %s",
              hashlib.sha256(sub.encode()).hexdigest()[:12])
    raise GoogleAccountError("Could not create your account right now. Please try again.", 503)
