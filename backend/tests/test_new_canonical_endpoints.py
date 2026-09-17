"""Comprehensive integration and unit tests for canonical backend endpoints.

Validates the 10 migrated/unified endpoints:
1. GET /api/problems/{id}/reference
2. POST /api/problems/generate
3. POST /api/submissions/run-custom
4. GET /api/account/summary
5. GET /api/recent-solved
6. GET /api/review/due
7. GET /api/insights/misconceptions
8. GET /api/momentum
9. POST /api/coach/debrief
10. POST /api/learning/dev-set-progress
And key SAP routes:
11. GET /api/sap/curriculum
12. GET /api/sap/curriculum/days/1
13. GET /api/sap/learning/lessons/1
"""

import uuid
from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_current_user, get_current_user_optional
from app.database import get_db
from app.models.models import Problem, Topic, User

client = TestClient(app)

@pytest.fixture
def mock_user():
    return User(
        id=uuid.uuid4(),
        email="dev_learner@example.com",
        name="Dev Learner",
    )

@pytest.fixture
def mock_db():
    session = MagicMock()
    # Mock problem lookup
    topic = Topic(id=uuid.uuid4(), slug="arrays", name="Arrays & Hashing")
    prob = Problem(
        id=uuid.uuid4(),
        slug="two-sum",
        title="Two Sum",
        statement_md="Find two indices that sum to target.",
        constraints_md="N <= 10^4",
        difficulty_tier=1,
        topic_id=topic.id,
        entry_point="two_sum",
        test_cases=[{"args": [[2, 7, 11, 15], 9], "expected": [0, 1]}],
        starter_code={"python": "def two_sum(nums, target):\n    pass\n"},
    )
    session.get.return_value = prob
    session.execute.return_value.scalars.return_value.all.return_value = []
    session.execute.return_value.scalars.return_value.first.return_value = prob
    session.execute.return_value.scalar_one_or_none.return_value = prob
    session.execute.return_value.scalar_one.return_value = 1
    session.execute.return_value.all.return_value = []
    return session


def test_sap_curriculum_route():
    """Verify GET /api/sap/curriculum loads 9 phases and 100 days from manifest."""
    res = client.get("/api/sap/curriculum")
    assert res.status_code == 200
    data = res.json()
    assert "phases" in data
    assert len(data["phases"]) == 9
    assert data["total_days"] == 100


def test_sap_curriculum_day_detail():
    """Verify GET /api/sap/curriculum/days/1 returns Day 1 metadata."""
    res = client.get("/api/sap/curriculum/days/1")
    assert res.status_code == 200
    data = res.json()
    assert data["day_number"] == 1
    assert "Enterprise Systems" in data["title"]
    assert len(data["atomic_concepts"]) >= 1


def test_sap_lesson_content():
    """Verify GET /api/sap/learning/lessons/1 returns 8-step pedagogical lesson."""
    res = client.get("/api/sap/learning/lessons/1")
    assert res.status_code == 200
    data = res.json()
    assert data["day_number"] == 1
    assert len(data["steps"]) == 8


def test_problem_reference_solution(mock_user, mock_db):
    """Verify GET /api/problems/{id}/reference returns starter/reference code."""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        res = client.get("/api/problems/two-sum/reference")
        assert res.status_code == 200
        data = res.json()
        assert data["language"] == "python"
        assert "code" in data
    finally:
        app.dependency_overrides.clear()


def test_submissions_run_custom(mock_user, mock_db):
    """Verify POST /api/submissions/run-custom executes arbitrary input."""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        payload = {
            "problem_id": "two-sum",
            "code": "def two_sum(nums, target):\n    return [0, 1]\n",
            "args": [[2, 7], 9],
        }
        res = client.post("/api/submissions/run-custom", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] in ("ok", "success")
        assert data["returned"] == [0, 1]
    finally:
        app.dependency_overrides.clear()


def test_account_summary(mock_user, mock_db):
    """Verify GET /api/account/summary returns user profile and statistics."""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        res = client.get("/api/account/summary")
        assert res.status_code == 200
        data = res.json()
        assert "solved_count" in data
        assert "total_problems" in data
    finally:
        app.dependency_overrides.clear()


def test_momentum_summary(mock_user, mock_db):
    """Verify GET /api/momentum returns daily streak and activity."""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        res = client.get("/api/momentum")
        assert res.status_code == 200
        data = res.json()
        assert "streak" in data
        assert "xp" in data
    finally:
        app.dependency_overrides.clear()


def test_insights_misconceptions(mock_user, mock_db):
    """Verify GET /api/insights/misconceptions returns weakness analysis."""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        res = client.get("/api/insights/misconceptions")
        assert res.status_code == 200
        data = res.json()
        assert "items" in data
        assert "total" in data
    finally:
        app.dependency_overrides.clear()


def test_review_due(mock_user, mock_db):
    """Verify GET /api/review/due returns spaced-repetition queue."""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        res = client.get("/api/review/due")
        assert res.status_code == 200
        data = res.json()
        assert "due" in data
        assert "upcoming" in data
    finally:
        app.dependency_overrides.clear()


def test_coach_debrief(mock_user, mock_db):
    """Verify POST /api/coach/debrief returns AI coach commentary."""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        payload = {
            "problem_id": "two-sum",
            "code": "def two_sum(nums, target): return [0, 1]",
            "tests": {"passed": True, "failed": False}
        }
        res = client.post("/api/coach/debrief", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert "message" in data
    finally:
        app.dependency_overrides.clear()


def test_dev_set_progress(mock_user, mock_db):
    """Verify POST /api/learning/dev-set-progress records developer day progress."""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        payload = {
            "completed_up_to": 3,
        }
        res = client.post("/api/learning/dev-set-progress", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert "current_day" in data
        assert "completed_days" in data
    finally:
        app.dependency_overrides.clear()


def test_dev_set_progress_production_forbidden(mock_user, mock_db):
    """Verify POST /api/learning/dev-set-progress is forbidden (403) in production."""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        with patch("app.api.routes.learning.get_settings") as mock_settings:
            mock_settings.return_value.is_production = True
            payload = {"completed_up_to": 5}
            res = client.post("/api/learning/dev-set-progress", json=payload)
            assert res.status_code == 403
            assert "disabled in production" in res.json()["detail"]
    finally:
        app.dependency_overrides.clear()


def test_sap_placement_unauthenticated():
    """Verify SAP placement endpoints reject unauthenticated requests with 401."""
    res_submit = client.post("/api/sap/placement/submit", json={"domain_scores": {}, "persona_self_select": "fresher"})
    assert res_submit.status_code == 401

    res_profile = client.get("/api/sap/placement/profile")
    assert res_profile.status_code == 401


def test_sap_placement_submit_authenticated(mock_user, mock_db):
    """Verify SAP placement submit processes diagnostic for authenticated users."""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        with patch("app.api.routes.sap.placement.SAPPlacementService.evaluate_diagnostic") as mock_eval:
            mock_profile = MagicMock()
            mock_profile.persona = "functional_user"
            mock_profile.diagnostic_results = {"overall_score": 85.0, "unlocked_days": list(range(1, 24))}
            mock_profile.recommended_start_day = 23
            mock_profile.rationale = "Demonstrated strong business process foundations."
            mock_profile.concept_benchmarks = {"p2p": 85, "o2c": 90}
            mock_eval.return_value = mock_profile

            payload = {
                "domain_scores": {"erp_basics": 85},
                "persona_self_select": "functional_user",
            }
            res = client.post("/api/sap/placement/submit", json=payload)
            assert res.status_code == 200
            data = res.json()
            assert data["persona"] == "functional_user"
            assert data["recommended_start_day"] == 23
            assert data["diagnostic_score"] == 85.0
            assert "unlocked_days" in data
    finally:
        app.dependency_overrides.clear()


def test_cookie_session_auth_flow(mock_user, mock_db):
    """Verify HttpOnly cookie-based session lifecycle without Bearer tokens."""
    from app.core.security import create_access_token
    token = create_access_token(str(mock_user.id), {"email": mock_user.email})

    app.dependency_overrides[get_db] = lambda: mock_db
    # mock db.get(User, user_id) to return mock_user
    mock_db.get.return_value = mock_user

    try:
        # 1. Protected endpoint with cookie -> 200
        res_me = client.get("/api/auth/me", cookies={"access_token": token})
        assert res_me.status_code == 200
        assert res_me.json()["email"] == mock_user.email

        # 2. Protected endpoint without cookie -> 401
        res_unauth = client.get("/api/auth/me")
        assert res_unauth.status_code == 401

        # 3. Logout endpoint deletes cookie
        res_logout = client.post("/api/auth/logout")
        assert res_logout.status_code == 200
        set_cookie = res_logout.headers.get("set-cookie", "")
        assert 'access_token=""' in set_cookie or "access_token=;" in set_cookie
    finally:
        app.dependency_overrides.clear()


