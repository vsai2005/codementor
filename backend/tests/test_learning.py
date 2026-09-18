"""Unit & regression tests for /api/learning/run execution endpoint."""

from __future__ import annotations

import uuid
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_current_user
from app.models.models import User
from app.services.ratelimit import get_run_rate_limiter


@pytest.fixture
def test_user():
    return User(
        id=uuid.uuid4(),
        email="learner@example.com",
        name="Test Learner",
    )


@pytest.fixture
def auth_client(test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    limiter = get_run_rate_limiter()
    limiter.reset()
    yield
    limiter.reset()


def test_learning_run_unauthenticated_rejected():
    """Anonymous calls to /api/learning/run must be rejected with 401 Unauthorized."""
    with TestClient(app) as anon_client:
        response = anon_client.post(
            "/api/learning/run",
            json={"code": "print('hello')", "day_number": 1},
        )
        assert response.status_code == 401


def test_learning_run_empty_code_rejected(auth_client):
    """Empty or whitespace-only code snippets must be rejected with 400 Bad Request."""
    response = auth_client.post(
        "/api/learning/run",
        json={"code": "   \n  \t  ", "day_number": 1},
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_learning_run_success(auth_client):
    payload = {
        "code": "x = 10\ny = 20\nprint(f'sum: {x + y}')",
        "day_number": 1,
    }
    response = auth_client.post("/api/learning/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "sum: 30" in data["stdout"]
    assert data["stderr"] == ""


def test_learning_run_memory_diagnostic(auth_client):
    payload = {
        "code": (
            "daily_coding_hours = 3.5\n"
            "initial_id = id(daily_coding_hours)\n"
            "daily_coding_hours = daily_coding_hours + 1\n"
            "new_id = id(daily_coding_hours)\n"
            "print(f'rebound: {initial_id != new_id}')"
        ),
        "day_number": 1,
    }
    response = auth_client.post("/api/learning/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "rebound: True" in data["stdout"]


def test_learning_run_syntax_error(auth_client):
    payload = {
        "code": "x = 10\nif x = 10:\n    print(x)",
        "day_number": 1,
    }
    response = auth_client.post("/api/learning/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "SyntaxError" in data["stderr"]


def test_learning_run_runtime_exception(auth_client):
    payload = {
        "code": "x = 10 / 0\nprint(x)",
        "day_number": 1,
    }
    response = auth_client.post("/api/learning/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "ZeroDivisionError" in data["stderr"]


def test_learning_run_blocked_operation(auth_client):
    payload = {
        "code": "import os\nos.system('echo dangerous')",
        "day_number": 1,
    }
    response = auth_client.post("/api/learning/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "blocked" in data["stderr"].lower() or "permission" in data["stderr"].lower()


def test_learning_run_rate_limiting(test_user, auth_client, monkeypatch):
    """Exceeding run_rate_limit triggers HTTP 429 Too Many Requests."""
    from app.config import get_settings
    from app.services import ratelimit

    # Temporarily set limit to 3 for testing
    monkeypatch.setattr(ratelimit, "_run_limiter", ratelimit.InMemoryRateLimiter(limit=3, window_s=60))

    payload = {"code": "print(1)", "day_number": 1}

    res1 = auth_client.post("/api/learning/run", json=payload)
    res2 = auth_client.post("/api/learning/run", json=payload)
    res3 = auth_client.post("/api/learning/run", json=payload)
    assert res1.status_code == 200
    assert res2.status_code == 200
    assert res3.status_code == 200

    # 4th request must be throttled
    res4 = auth_client.post("/api/learning/run", json=payload)
    assert res4.status_code == 429
    assert "too many code execution requests" in res4.json()["detail"].lower()
