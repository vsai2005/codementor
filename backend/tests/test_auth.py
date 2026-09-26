"""JWT tests (PRD 5.3). Google verification is mocked -- no network in tests."""

import base64
import json
import time
from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt
from pydantic import ValidationError

from app.config import Settings, get_settings
from app.core.security import AuthError, create_access_token, decode_access_token, verify_google_id_token


def _b64(data: dict) -> str:
    raw = json.dumps(data, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


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


def test_tampered_signature_is_rejected():
    token = create_access_token("u")
    header, payload, signature = token.split(".")
    tampered = f"{header}.{payload}.{'A' if signature[0] != 'A' else 'B'}{signature[1:]}"
    with pytest.raises(AuthError):
        decode_access_token(tampered)


def test_unexpected_hmac_algorithm_is_rejected():
    settings = get_settings()
    unexpected = "HS512" if settings.jwt_algorithm != "HS512" else "HS256"
    token = jwt.encode(
        {"sub": "u", "exp": int(time.time()) + 3600},
        settings.jwt_secret,
        algorithm=unexpected,
    )
    with pytest.raises(AuthError):
        decode_access_token(token)


@pytest.mark.parametrize("algorithm", ["RS256", "ES256"])
def test_unexpected_asymmetric_algorithm_is_rejected(algorithm):
    token = create_access_token("u")
    _, payload, signature = token.split(".")
    forged = f'{_b64({"alg": algorithm, "typ": "JWT"})}.{payload}.{signature}'
    with pytest.raises(AuthError):
        decode_access_token(forged)


@pytest.mark.parametrize("algorithm", ["ES256", "RS256", "HS512"])
def test_session_algorithm_cannot_be_overridden(algorithm, monkeypatch):
    with pytest.raises(ValidationError):
        Settings(jwt_algorithm=algorithm)
    monkeypatch.setenv("JWT_ALGORITHM", algorithm)
    with pytest.raises(ValidationError):
        Settings()


def test_google_token_uses_google_verifier_and_checks_claims(monkeypatch):
    from google.oauth2 import id_token as google_id_token

    calls = []

    def verify(token, request, audience):
        calls.append((token, audience))
        return {"iss": "https://accounts.google.com", "email_verified": True, "sub": "google-user"}

    monkeypatch.setattr(google_id_token, "verify_oauth2_token", verify)
    monkeypatch.setattr("app.core.security.get_settings", lambda: Settings(google_client_id="test-client-id"))
    assert verify_google_id_token("signed-google-token")["sub"] == "google-user"
    assert calls == [("signed-google-token", "test-client-id")]

    for claims in (
        {"iss": "https://attacker.example", "email_verified": True},
        {"iss": "accounts.google.com", "email_verified": False},
    ):
        monkeypatch.setattr(google_id_token, "verify_oauth2_token", lambda *_: claims)
        with pytest.raises(AuthError):
            verify_google_id_token("signed-google-token")


def test_garbage_token_is_rejected():
    with pytest.raises(AuthError):
        decode_access_token("not.a.jwt")


def test_alg_none_attack_is_rejected():
    """Classic JWT bypass: unsigned token claiming alg=none.

    Hand-assembled, because the library refuses to mint one -- which is the
    point. We still assert the decode side rejects it, since the attacker
    builds the token with base64 and a text editor, not with our library.
    """
    forged = f'{_b64({"alg": "none", "typ": "JWT"})}.{_b64({"sub": "admin", "exp": int(time.time()) + 3600})}.'

    with pytest.raises(AuthError):
        decode_access_token(forged)
