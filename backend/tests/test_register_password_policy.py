"""Registration password policy (min 8 chars) and login compatibility for legacy accounts."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.routes.auth import MIN_PASSWORD_LENGTH
from app.core.security import hash_password
from app.database import get_db
from app.main import app
from app.models.models import Base, User


@compiles(JSONB, "sqlite")
def _compile_jsonb_sqlite(type_, compiler, **kw):
    return "TEXT"


_engine = create_engine(
    "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
_Session = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@pytest.fixture(autouse=True)
def _db():
    Base.metadata.create_all(bind=_engine)

    def override_get_db():
        db = _Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=_engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def _register(client, username, password):
    return client.post("/api/auth/register", json={"username": username, "password": password})


def test_minimum_length_is_eight():
    assert MIN_PASSWORD_LENGTH == 8


@pytest.mark.parametrize("password", ["", "a", "abcdef", "abcdefg"])
def test_register_rejects_passwords_shorter_than_eight(client, password):
    res = _register(client, "shortpw", password)
    assert res.status_code == 400
    assert res.json()["detail"] == "Password must be at least 8 characters."
    # Nothing was created: the same username is still free with a valid password.
    assert _register(client, "shortpw", "abcdefgh").status_code == 200


def test_register_accepts_exactly_eight_characters(client):
    res = _register(client, "eightchar", "abcdefgh")
    assert res.status_code == 200
    assert res.json()["user"]["username"] == "eightchar"


def test_register_accepts_a_long_passphrase(client):
    assert _register(client, "longpass", "correct horse battery staple").status_code == 200


def test_new_short_password_login_is_not_length_checked(client):
    """Login never enforces the registration minimum, so a wrong short password is a
    plain 401 credential failure, not a 400/422 validation error."""
    assert _register(client, "loginuser", "abcdefgh").status_code == 200
    res = client.post("/api/auth/login", json={"identifier": "loginuser", "password": "abc"})
    assert res.status_code == 401


def test_legacy_six_character_account_can_still_log_in(client):
    salt, pwd_hash = hash_password("legacy")  # 6 chars: valid under the old rule
    db = _Session()
    db.add(
        User(
            username="legacyuser",
            email="legacyuser@local.dev",
            name="Legacy User",
            salt=salt,
            pwd_hash=pwd_hash,
        )
    )
    db.commit()
    db.close()

    res = client.post("/api/auth/login", json={"identifier": "legacyuser", "password": "legacy"})
    assert res.status_code == 200
    assert res.json()["user"]["username"] == "legacyuser"
