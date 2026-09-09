"""JWT issuing/verification, password hashing, and Google ID-token validation (Phase 2)."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.config import get_settings

PBKDF2_ROUNDS = 100_000


class AuthError(Exception):
    pass


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    """Generate or use salt and compute PBKDF2-HMAC-SHA256 password hash."""
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), PBKDF2_ROUNDS
    ).hex()
    return salt, digest


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    """Constant-time password hash verification."""
    _, digest = hash_password(password, salt)
    return secrets.compare_digest(digest, expected_hash)


def create_access_token(subject: str, extra: dict | None = None) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=settings.jwt_expiry_hours)).timestamp()),
        **(extra or {}),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise AuthError(str(exc)) from exc


def verify_google_id_token(token: str) -> dict:
    """Server-side verification. Never trust a client-decoded token."""
    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token as google_id_token

    settings = get_settings()
    try:
        claims = google_id_token.verify_oauth2_token(
            token, google_requests.Request(), settings.google_client_id
        )
    except ValueError as exc:
        raise AuthError(f"invalid Google ID token: {exc}") from exc

    if claims.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
        raise AuthError("unexpected token issuer")
    if not claims.get("email_verified"):
        raise AuthError("Google account email is not verified")
    return claims
