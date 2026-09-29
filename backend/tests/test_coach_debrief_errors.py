"""coach_debrief: LLM failures fall back to the static debrief, and are never silent."""

import logging
import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_current_user
from app.database import get_db
from app.main import app
from app.models.models import Problem, User
from app.services.llm import LLMError, LLMTimeout
from app.services.ratelimit import InMemoryRateLimiter

PAYLOAD = {
    "problem_id": "two-sum",
    "code": "def two_sum(nums, target): pass",
    "tests": {"passed": 1, "total": 1},
}
STATIC_PASS_MESSAGE = "Great execution! All test cases passed."


@pytest.fixture
def client():
    problem = Problem(
        id=uuid.uuid4(),
        slug="two-sum",
        title="Two Sum",
        statement_md="x",
        constraints_md="",
        difficulty_tier=1,
        entry_point="two_sum",
        test_cases=[],
        starter_code={},
    )
    session = MagicMock()
    session.get.return_value = problem
    session.execute.return_value.scalar_one_or_none.return_value = problem
    user = User(id=uuid.uuid4(), email="coach@example.com", username="coach", name="Coach")
    app.dependency_overrides[get_db] = lambda: session
    app.dependency_overrides[get_current_user] = lambda: user
    limiter = InMemoryRateLimiter(limit=100, window_s=60)
    with patch("app.api.routes.tutor.get_coach_rate_limiter", return_value=limiter):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()


class _Client:
    def __init__(self, reply=None, exc=None):
        self._reply, self._exc = reply, exc

    def complete(self, *args, **kwargs):
        if self._exc is not None:
            raise self._exc
        return self._reply


def test_successful_llm_reply_is_returned(client):
    with patch("app.api.routes.tutor.get_llm_client", return_value=_Client(reply=" Nice work. ")):
        res = client.post("/api/coach/debrief", json=PAYLOAD)
    assert res.status_code == 200
    assert res.json()["message"] == "Nice work."


@pytest.mark.parametrize("exc", [LLMError("no key configured"), LLMTimeout("slow")])
def test_llm_error_falls_back_and_logs_a_warning(client, capture_logs, exc):
    records = capture_logs("app.api.routes.tutor")
    with patch("app.api.routes.tutor.get_llm_client", return_value=_Client(exc=exc)):
        res = client.post("/api/coach/debrief", json=PAYLOAD)
    assert res.status_code == 200
    assert res.json()["message"].startswith(STATIC_PASS_MESSAGE)
    assert [r.levelno for r in records] == [logging.WARNING]
    assert records[0].exc_info is None


def test_unconfigured_provider_at_client_creation_falls_back(client, capture_logs):
    records = capture_logs("app.api.routes.tutor")
    with patch("app.api.routes.tutor.get_llm_client", side_effect=LLMError("NVIDIA key is not set")):
        res = client.post("/api/coach/debrief", json=PAYLOAD)
    assert res.status_code == 200
    assert res.json()["message"].startswith(STATIC_PASS_MESSAGE)
    assert [r.levelno for r in records] == [logging.WARNING]


def test_unexpected_error_falls_back_but_is_logged_with_traceback(client, capture_logs):
    records = capture_logs("app.api.routes.tutor")
    with patch("app.api.routes.tutor.get_llm_client", return_value=_Client(exc=KeyError("bug"))):
        res = client.post("/api/coach/debrief", json=PAYLOAD)
    assert res.status_code == 200
    assert res.json()["message"].startswith(STATIC_PASS_MESSAGE)
    assert [r.levelno for r in records] == [logging.ERROR]
    assert records[0].exc_info is not None and records[0].exc_info[0] is KeyError
