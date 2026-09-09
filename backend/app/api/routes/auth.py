"""Authentication routes with HttpOnly cookie support (Phase 2)."""

from __future__ import annotations

import re
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.config import get_settings
from app.core.security import (
    AuthError,
    create_access_token,
    hash_password,
    verify_google_id_token,
    verify_password,
)
from app.database import get_db
from app.models.models import User
from app.schemas.api import (
    GoogleLoginRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserOut,
)

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
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    try:
        claims = verify_google_id_token(payload.id_token)
    except AuthError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(exc)) from exc

    email = claims["email"]
    user = db.execute(select(User).where(User.email == email)).scalars().first()
    if user is None:
        user = User(
            email=email,
            username=email.split("@")[0].lower(),
            name=claims.get("name") or email.split("@")[0],
            avatar_url=claims.get("picture"),
            google_sub=claims.get("sub"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(str(user.id), {"email": user.email})
    _set_auth_cookie(response, token)

    return TokenResponse(
        access_token=token,
        user=UserOut.model_validate(user),
    )


@router.post("/register", response_model=TokenResponse)
def register(
    payload: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
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
    db.commit()
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
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    ident = payload.identifier.strip().lower()
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
    )
    return {"detail": "Logged out successfully"}


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(user)
