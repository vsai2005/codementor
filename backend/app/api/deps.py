"""Shared FastAPI dependencies."""

from __future__ import annotations

import uuid

from fastapi import Depends, Header, HTTPException, status
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
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise _UNAUTHORIZED

    try:
        claims = decode_access_token(authorization.split(" ", 1)[1].strip())
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
