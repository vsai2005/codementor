import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models.models import Base
from app.config import Settings, get_settings

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "TEXT"

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def db_isolation():
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    get_settings.cache_clear()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user(client):
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com",
        "name": "Test User",
    })
    assert response.status_code == 200
    return response.json()


def test_login_sets_httponly_cookie_with_correct_attributes(client, test_user):
    # Default settings (development)
    response = client.post("/api/auth/login", json={
        "identifier": "testuser",
        "password": "testpassword",
    })
    assert response.status_code == 200
    
    set_cookie = response.headers.get("set-cookie")
    assert set_cookie is not None
    assert "access_token=" in set_cookie
    assert "HttpOnly" in set_cookie
    assert "Path=/" in set_cookie
    assert "Secure" not in set_cookie  # Not in dev

    # Patch settings to production mode using a dedicated Settings instance (never mutate singleton)
    prod_settings = Settings(environment="production", cookie_secure=None)
    with patch("app.api.routes.auth.get_settings", return_value=prod_settings):
        response = client.post("/api/auth/login", json={
            "identifier": "testuser",
            "password": "testpassword",
        })
        assert response.status_code == 200
        
        set_cookie = response.headers.get("set-cookie")
        assert set_cookie is not None
        assert "access_token=" in set_cookie
        assert "HttpOnly" in set_cookie
        assert "Path=/" in set_cookie
        assert "Secure" in set_cookie  # Should be present in prod


def test_logout_clears_cookie_with_secure_flag(client, test_user):
    # Login first
    client.post("/api/auth/login", json={
        "identifier": "testuser",
        "password": "testpassword",
    })
    
    # Logout default settings
    response = client.post("/api/auth/logout")
    assert response.status_code == 200
    set_cookie = response.headers.get("set-cookie")
    assert set_cookie is not None
    assert 'access_token=""' in set_cookie or "access_token=;" in set_cookie or "Max-Age=0" in set_cookie or "expires=" in set_cookie.lower()
    
    # Patch settings to production mode for logout
    prod_settings = Settings(environment="production", cookie_secure=None)
    with patch("app.api.routes.auth.get_settings", return_value=prod_settings):
        response = client.post("/api/auth/logout")
        assert response.status_code == 200
        set_cookie = response.headers.get("set-cookie")
        assert set_cookie is not None
        assert "Secure" in set_cookie


def test_cors_allows_configured_origin(client):
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET",
    }
    response = client.options("/api/auth/me", headers=headers)
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
    assert response.headers.get("access-control-allow-credentials") == "true"


def test_cors_rejects_unconfigured_origin(client):
    headers = {
        "Origin": "https://evil.com",
        "Access-Control-Request-Method": "GET",
    }
    response = client.options("/api/auth/me", headers=headers)
    assert response.headers.get("access-control-allow-origin") != "https://evil.com"
    if response.headers.get("access-control-allow-origin"):
        assert "evil.com" not in response.headers.get("access-control-allow-origin")


def test_unauthenticated_request_returns_401(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
