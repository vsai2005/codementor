"""JWT tests (PRD 5.3). Google verification is mocked -- no network in tests."""

import time
from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt

from app.config import get_settings
from app.core.security import AuthError, create_access_token, decode_access_token


def test_token_roundtrips_the_subject():
    token = create_access_token("user-123", {"email": "a@b.com"})
    claims = decode_access_token(token)
    assert claims["sub"] == "user-123"
    assert claims["email"] == "a@b.com"


def test_token_expiry_is_twenty_four_hours():
    claims = decode_access_token(create_access_token("u"))
    lifetime = claims["exp"] - claims["iat"]
    assert lifetime == 24 * 3600


def test_expired_token_is_rejected():
    settings = get_settings()
    past = datetime.now(timezone.utc) - timedelta(hours=1)
    expired = jwt.encode(
        {"sub": "u", "iat": int((past - timedelta(hours=25)).timestamp()),
         "exp": int(past.timestamp())},
        settings.jwt_secret, algorithm=settings.jwt_algorithm,
    )
    with pytest.raises(AuthError):
        decode_access_token(expired)


def test_token_signed_with_the_wrong_secret_is_rejected():
    forged = jwt.encode({"sub": "u", "exp": int(time.time()) + 3600},
                        "not-the-real-secret", algorithm="HS256")
    with pytest.raises(AuthError):
        decode_access_token(forged)


def test_garbage_token_is_rejected():
    with pytest.raises(AuthError):
        decode_access_token("not.a.jwt")


def test_alg_none_attack_is_rejected():
    """Classic JWT bypass: unsigned token claiming alg=none.

    Hand-assembled, because the library refuses to mint one -- which is the
    point. We still assert the decode side rejects it, since the attacker
    builds the token with base64 and a text editor, not with our library.
    """
    import base64
    import json

    def b64(data: dict) -> str:
        raw = json.dumps(data, separators=(",", ":")).encode()
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()

    forged = f'{b64({"alg": "none", "typ": "JWT"})}.{b64({"sub": "admin", "exp": int(time.time()) + 3600})}.'

    with pytest.raises(AuthError):
        decode_access_token(forged)
