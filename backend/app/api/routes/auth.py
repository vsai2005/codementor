"""Authentication routes with HttpOnly cookie support (Phase 2)."""

from __future__ import annotations

import logging
import re
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.rate_limit import account_subject, client_ip, enforce_rate_limit
from app.config import get_settings
from app.core.security import (
    AuthError,
    create_access_token,
    hash_password,
    verify_google_id_token,
    verify_password,
)
from app.database import get_db
from app.services.google_accounts import GoogleAccountError, resolve_google_user
from app.models.models import User
from app.schemas.api import (
    GoogleLoginRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserOut,
)

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])
USERNAME_RE = re.compile(r"^[a-zA-Z0-9._-]{3,30}$")


def _set_auth_cookie(response: Response, token: str) -> None:
    """Sets an HttpOnly, SameSite=Lax session cookie."""
    settings = get_settings()
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=settings.secure_cookies,
        samesite=settings.cookie_samesite,
        max_age=settings.cookie_max_age,
        domain=settings.cookie_domain,
        path="/",
    )


@router.post("/google", response_model=TokenResponse)
def google_login(
    payload: GoogleLoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Google sign-in. Rate-limited per IP before token verification and per Google
    identity after it; identity is the Google `sub`, the username is only a handle."""
    enforce_rate_limit("auth_google_ip", client_ip(request))
    try:
        claims = verify_google_id_token(payload.id_token)
    except AuthError as exc:
        log.info("google sign-in rejected: %s", exc)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Google sign-in failed. Please try again.") from exc

    enforce_rate_limit("auth_google_identity", account_subject(str(claims.get("sub") or "")))
    try:
        user = resolve_google_user(db, claims)
    except GoogleAccountError as exc:
        raise HTTPException(exc.status_code, str(exc)) from exc

    token = create_access_token(str(user.id), {"email": user.email})
    _set_auth_cookie(response, token)

    return TokenResponse(
        access_token=token,
        user=UserOut.model_validate(user),
    )


@router.post("/register", response_model=TokenResponse)
def register(
    payload: RegisterRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    enforce_rate_limit("auth_register_ip", client_ip(request))
    username = payload.username.strip().lower()
    if not USERNAME_RE.match(username):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Username must be 3-30 alphanumeric characters or . _ -",
        )
    if len(payload.password) < 6:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Password must be at least 6 characters.",
        )

    email = payload.email.strip().lower() if payload.email else None

    # Check if username or email is already registered
    conditions = [User.username == username]
    if email:
        conditions.append(User.email == email)
    existing = db.execute(select(User).where(or_(*conditions))).scalars().first()
    if existing:
        if existing.username == username:
            raise HTTPException(status.HTTP_409_CONFLICT, "That username is already taken.")
        raise HTTPException(status.HTTP_409_CONFLICT, "That email is already registered.")

    salt, pwd_hash = hash_password(payload.password)
    user = User(
        username=username,
        email=email or f"{username}@local.dev",
        name=payload.name or username.title(),
        salt=salt,
        pwd_hash=pwd_hash,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        # A concurrent registration claimed the username or email first.
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "That username or email is already taken.")
    db.refresh(user)

    token = create_access_token(str(user.id), {"sub": str(user.id)})
    _set_auth_cookie(response, token)

    return TokenResponse(
        access_token=token,
        user=UserOut.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Password login. Every attempt is counted per IP and per normalized identifier
    (existing or not) before any lookup or hashing, so limits reveal nothing."""
    ident = payload.identifier.strip().lower()
    enforce_rate_limit("auth_login_ip", client_ip(request))
    enforce_rate_limit("auth_login_account", account_subject(ident))
    user = db.execute(
        select(User).where(or_(User.username == ident, User.email == ident))
    ).scalars().first()

    if not user or not user.pwd_hash or not user.salt:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect username/email or password.",
        )

    if not verify_password(payload.password, user.salt, user.pwd_hash):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect username/email or password.",
        )

    token = create_access_token(str(user.id), {"sub": str(user.id)})
    _set_auth_cookie(response, token)

    return TokenResponse(
        access_token=token,
        user=UserOut.model_validate(user),
    )


@router.post("/logout")
def logout(response: Response) -> dict:
    settings = get_settings()
    response.delete_cookie(
        key="access_token",
        path="/",
        domain=settings.cookie_domain,
        samesite=settings.cookie_samesite,
        secure=settings.secure_cookies,
    )
    return {"detail": "Logged out successfully"}


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(user)
