"""Behaviour locks for the mypy clean-up: type-only edits must not change runtime results."""

import json
import sys
import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient

from app.api.deps import get_current_user
from app.database import get_db
from app.main import app
from app.models.models import User
from app.services import _sandbox_runner

# --- sandbox runner envelope ---------------------------------------------------------


def test_emit_writes_envelope_to_real_stdout(capfd):
    _sandbox_runner._emit({"status": "ok", "returned": [1, 2]})
    out, err = capfd.readouterr()
    assert json.loads(out) == {"status": "ok", "returned": [1, 2]}
    assert err == ""


def test_emit_falls_back_to_fd1_when_interpreter_stdout_is_missing(capfd, monkeypatch):
    monkeypatch.setattr(sys, "__stdout__", None)
    _sandbox_runner._emit({"status": "error", "stderr": "naïve ✓"})
    out, _ = capfd.readouterr()
    assert json.loads(out) == {"status": "error", "stderr": "naïve ✓"}


def test_emit_ignores_the_students_redirected_sys_stdout(capfd, monkeypatch):
    """sys.stdout holds captured student output in the runner; the envelope must not go there."""
    import io

    student_stream = io.StringIO()
    monkeypatch.setattr(sys, "stdout", student_stream)
    monkeypatch.setattr(sys, "__stdout__", None)
    _sandbox_runner._emit({"status": "ok"})
    out, _ = capfd.readouterr()
    assert json.loads(out) == {"status": "ok"}
    assert student_stream.getvalue() == ""


# --- /api/learning/dev-set-progress response handling -------------------------------

VALID_PROGRESS = {
    "current_day": 4,
    "completed_days": [1, 2, 3],
    "total_days": 160,
    "day_states": {
        "1": {
            "day_number": 1,
            "lesson_completed": True,
            "practice_passed": True,
            "completed": True,
            "unlocked": True,
            "status": "completed",
        }
    },
    "extra_field_not_in_schema": "dropped by response_model",
}


@pytest.fixture
def client():
    user = User(id=uuid.uuid4(), email="dev@example.com", username="dev", name="Dev")
    session = MagicMock()
    session.execute.return_value.scalar_one_or_none.return_value = None
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_db] = lambda: session
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_dev_set_progress_serializes_exactly_like_get_progress(client):
    with patch("app.services.learning.compute_user_progress", return_value=dict(VALID_PROGRESS)):
        via_dev = client.post("/api/learning/dev-set-progress", json={"completed_up_to": 3})
        via_get = client.get("/api/learning/progress")
    assert via_dev.status_code == via_get.status_code == 200
    assert via_dev.json() == via_get.json()
    assert "extra_field_not_in_schema" not in via_dev.json()
    assert via_dev.json()["day_states"]["1"]["lesson_completed_at"] is None


def test_dev_set_progress_invalid_payload_fails_in_response_validation(client):
    """An invalid service result still fails at FastAPI's response validation, as before."""
    bad = dict(VALID_PROGRESS, current_day="not-an-int")
    with patch("app.services.learning.compute_user_progress", return_value=bad):
        with pytest.raises(ResponseValidationError):
            client.post("/api/learning/dev-set-progress", json={"completed_up_to": 3})
        with pytest.raises(ResponseValidationError):
            client.get("/api/learning/progress")
