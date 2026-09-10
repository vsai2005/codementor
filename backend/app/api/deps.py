"""Shared FastAPI dependencies (Phase 2)."""

from __future__ import annotations

import uuid

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.security import AuthError, decode_access_token
from app.database import get_db
from app.models.models import User

_UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    request: Request,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    token: str | None = None

    # 1. Dual-Strategy: Inspect HttpOnly cookie first
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        token = cookie_token.strip()
    # 2. Fall back to Authorization: Bearer <token> header
    elif authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()

    if not token:
        raise _UNAUTHORIZED

    try:
        claims = decode_access_token(token)
    except AuthError:
        raise _UNAUTHORIZED from None

    try:
        user_id = uuid.UUID(claims["sub"])
    except (KeyError, ValueError):
        raise _UNAUTHORIZED from None

    user = db.get(User, user_id)
    if user is None:
        raise _UNAUTHORIZED
    return user


def get_current_user_optional(
    request: Request,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User | None:
    token: str | None = None
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        token = cookie_token.strip()
    elif authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()

    if not token:
        return None

    try:
        claims = decode_access_token(token)
        user_id = uuid.UUID(claims["sub"])
        return db.get(User, user_id)
    except Exception:
        return None
