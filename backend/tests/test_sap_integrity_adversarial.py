"""Adversarial and Integrity Test Suite for SAP Assessments, Progression Gating and Lesson Access.

Verifies:
1. Forged Rubric Bypass Blocked: Client cannot pass forged questions, options, or pass scores to achieve 100%.
2. Malformed Payloads Rejected: Empty answers, non-dict payloads, empty dicts return 400 Bad Request.
3. Unknown Assessment Type Rejected: Unsupported assessment type returns 400 Bad Request (never returns 100%).
4. Locked-Day Assessment Bypass Blocked: Attempting assessment on locked future days returns 403 Forbidden with zero DB side-effects.
5. Waived-Day Assessment Bypass Blocked: Attempting assessment on waived days returns 403 Forbidden with zero DB side-effects.
6. Assessment Before Practice Blocked: Submitting assessment without completing mandatory practice returns 400 Bad Request.
7. Mandatory Practice Requirement: Day is NOT completed and next day is NOT unlocked without practice completion.
8. Assessment Retry Idempotency: Retrying an already passed assessment does not double-advance days or double-count completion.
9. Normal Full Progression: Lesson + Practice + Assessment unlocks Day 2 correctly.
10. Locked Lesson Access Blocked: GET /api/sap/learning/lessons/{day} requires auth and locked/waived days return 403.
11. Completed Day Lesson Accessible: Completed days still return 200 (review access).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "TEXT"

from app.main import app
from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import Base, User
from app.models.sap_models import (
    SAPAssessmentAttempt,
    SAPSkillEvidence,
    SAPUserConceptMastery,
    SAPUserDayState,
    SAPUserState,
    SAPDayStatus,
)

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def mock_user(db_session):
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        email=f"sap_integrity_{str(user_id)[:8]}@example.com",
        username=f"sapuser_{str(user_id)[:8]}",
        name="SAP Integrity Tester",
        pwd_hash="hashed_password",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def client_auth(mock_user, db_session):
    def override_get_db():
        yield db_session

    def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# =============================================================================
# 1. Assessment Bypass: Forged Rubrics, Pass Scores, & Options
# =============================================================================

def test_forged_rubric_questions_and_pass_score_ignored(client_auth, mock_user, db_session):
    """Client provides forged questions with trivial answers and pass_score=0.
    Server MUST ignore client questions and evaluate only against server definitions (Day 1).
    """
    # Complete practice first so assessment can be attempted
    client_auth.post("/api/sap/learning/complete-practice", json={"day_number": 1})

    forged_payload = {
        "day_number": 1,
        "assessment_id": "d1_s6_assessment",
        "assessment_type": "mcq",
        "rubric_spec": {
            "pass_score": 0.0,
            "questions": [
                {
                    "id": "hacked_question_id",
                    "options": [
                        {"id": "hacked_answer", "is_correct": True}
                    ]
                }
            ]
        },
        "submission_payload": {
            "answers": {
                "hacked_question_id": "hacked_answer"
            }
        }
    }

    resp = client_auth.post("/api/sap/assessments/submit", json=forged_payload)
    assert resp.status_code == 200
    data = resp.json()
    # Server should NOT have awarded 100% or passed using forged question
    assert data["passed"] is False
    assert data["score"] == 0.0
    assert data["day_completed"] is False


def test_malformed_and_empty_payloads_rejected(client_auth, mock_user, db_session):
    """Server must reject empty answers, whitespace answers, or non-dict payloads with 400."""
    client_auth.post("/api/sap/learning/complete-practice", json={"day_number": 1})

    # Empty answers dictionary
    resp_empty = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {"answers": {}},
        },
    )
    assert resp_empty.status_code == 400
    assert "answers" in resp_empty.json()["detail"].lower() or "malformed" in resp_empty.json()["detail"].lower()

    # Whitespace/None answers
    resp_ws = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {"answers": {"q1": "   ", "q2": ""}},
        },
    )
    assert resp_ws.status_code == 400
    assert "cannot be empty" in resp_ws.json()["detail"].lower()


def test_unknown_assessment_type_rejected(client_auth, mock_user, db_session):
    """Server must reject unknown or exploit assessment types with 400/422 instead of defaulting to 100%."""
    client_auth.post("/api/sap/learning/complete-practice", json={"day_number": 1})

    resp = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "exploit_auto_pass_type",
            "submission_payload": {"answers": {"any": "thing"}},
        },
    )
    # Both 400 Bad Request and 422 Unprocessable Entity properly reject malformed request
    assert resp.status_code in (400, 422)


# =============================================================================
# 2. Locked-Day Assessment Bypass Gating
# =============================================================================

def test_locked_future_day_assessment_returns_403_no_side_effects(client_auth, mock_user, db_session):
    """Submitting assessment on a locked day (e.g. Day 25 when user is on Day 1)
    MUST return HTTP 403 Forbidden and create ZERO DB records (attempts, mastery, evidence).
    """
    resp = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 25,
            "assessment_id": "d25_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {"answers": {"q1": "q1_a"}},
        },
    )
    assert resp.status_code == 403
    assert "locked" in resp.json()["detail"].lower()

    # Verify zero database side effects
    attempts = db_session.execute(
        select(SAPAssessmentAttempt).where(SAPAssessmentAttempt.user_id == mock_user.id)
    ).scalars().all()
    assert len(attempts) == 0

    evidence = db_session.execute(
        select(SAPSkillEvidence).where(SAPSkillEvidence.user_id == mock_user.id)
    ).scalars().all()
    assert len(evidence) == 0

    mastery = db_session.execute(
        select(SAPUserConceptMastery).where(SAPUserConceptMastery.user_id == mock_user.id)
    ).scalars().all()
    assert len(mastery) == 0


def test_waived_day_assessment_returns_403_no_side_effects(client_auth, mock_user, db_session):
    """Submitting assessment on a diagnostic-waived day MUST return 403 Forbidden."""
    # Mark Day 1 as waived by placement
    day_state = SAPUserDayState(
        user_id=mock_user.id,
        day_number=1,
        status=SAPDayStatus.WAIVED_BY_PLACEMENT.value,
        waived=True,
    )
    db_session.add(day_state)
    db_session.commit()

    resp = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
        },
    )
    assert resp.status_code == 403
    assert "waived" in resp.json()["detail"].lower()


# =============================================================================
# 3. Practice Must Be Mandatory
# =============================================================================

def test_assessment_before_practice_rejected_with_400(client_auth, mock_user, db_session):
    """Learner cannot submit assessment before completing interactive practice."""
    # Day 1 is unlocked, but practice is NOT completed
    resp = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
        },
    )
    assert resp.status_code == 400
    assert "practice is mandatory" in resp.json()["detail"].lower()


def test_missing_practice_blocks_day_completion(client_auth, mock_user, db_session):
    """Even if lesson is completed, missing practice must prevent day completion."""
    # Step 1: Complete lesson only
    lesson_resp = client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 1})
    assert lesson_resp.status_code == 200
    assert lesson_resp.json()["day_completed"] is False

    # Check progress: Day 1 should not be completed and Day 2 should remain locked
    progress_resp = client_auth.get("/api/sap/learning/progress")
    assert 1 not in progress_resp.json()["completed_days"]
    assert progress_resp.json()["day_states"]["2"]["unlocked"] is False


def test_sequential_practice_lesson_assessment_unlocks_day_2(client_auth, mock_user, db_session):
    """Full legitimate sequence (practice + lesson + assessment) completes Day 1 and unlocks Day 2."""
    # 1. Practice
    prac_resp = client_auth.post("/api/sap/learning/complete-practice", json={"day_number": 1})
    assert prac_resp.status_code == 200
    assert prac_resp.json()["practice_completed"] is True

    # 2. Lesson
    less_resp = client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 1})
    assert less_resp.status_code == 200
    assert less_resp.json()["lesson_completed"] is True
    assert less_resp.json()["day_completed"] is False

    # 3. Assessment
    assess_resp = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
        },
    )
    assert assess_resp.status_code == 200
    assess_data = assess_resp.json()
    assert assess_data["passed"] is True
    assert assess_data["day_completed"] is True
    assert assess_data["unlocked_next_day"] is True
    assert assess_data["next_day_number"] == 2

    # Verify overall progress
    prog = client_auth.get("/api/sap/learning/progress").json()
    assert prog["current_day"] == 2
    assert 1 in prog["completed_days"]
    assert prog["day_states"]["1"]["completed"] is True
    assert prog["day_states"]["2"]["unlocked"] is True


def test_assessment_retry_idempotency_does_not_double_advance(client_auth, mock_user, db_session):
    """Retrying an assessment on an already completed day must not increment
    completed_days_count or double-advance current_recommended_day.
    """
    # Complete Day 1 legitimately
    client_auth.post("/api/sap/learning/complete-practice", json={"day_number": 1})
    client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 1})
    client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
        },
    )

    user_state = db_session.execute(
        select(SAPUserState).where(SAPUserState.user_id == mock_user.id)
    ).scalar_one()
    assert user_state.completed_days_count == 1
    assert user_state.current_recommended_day == 2

    # Learner re-takes Day 1 assessment
    retry_resp = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
        },
    )
    assert retry_resp.status_code == 200
    assert retry_resp.json()["passed"] is True

    # User state must remain unchanged
    db_session.refresh(user_state)
    assert user_state.completed_days_count == 1
    assert user_state.current_recommended_day == 2


# =============================================================================
# 4. Server-Protected Lesson Content: GET /api/sap/learning/lessons/{day}
# =============================================================================


class TestLockedLessonAccess:
    """Verifies that GET /api/sap/learning/lessons/{day_number} enforces
    server-side authentication and progression-based access control."""

    def test_unauthenticated_lesson_access_is_rejected(self, db_session):
        """An unauthenticated request must be rejected (401 or 403), never 200."""
        # No auth override — raw TestClient with no user
        def override_get_db():
            yield db_session

        app.dependency_overrides[get_db] = override_get_db
        # Explicitly do NOT override get_current_user — it will try to read a real token
        app.dependency_overrides.pop(get_current_user, None)

        try:
            with TestClient(app, raise_server_exceptions=False) as anon_client:
                resp = anon_client.get("/api/sap/learning/lessons/1")
            # FastAPI's dependency will raise 401 or 403 without a valid session
            assert resp.status_code in (401, 403), (
                f"Expected 401 or 403 for unauthenticated access, got {resp.status_code}"
            )
        finally:
            app.dependency_overrides.clear()

    def test_locked_future_day_lesson_returns_403(self, client_auth):
        """An authenticated user on Day 1 cannot fetch lesson content for locked Day 25."""
        resp = client_auth.get("/api/sap/learning/lessons/25")
        assert resp.status_code == 403, (
            f"Expected 403 for locked Day 25, got {resp.status_code}: {resp.json()}"
        )
        assert "locked" in resp.json()["detail"].lower()

    def test_current_day_lesson_returns_200(self, client_auth):
        """An authenticated user can access the lesson for their current/unlocked Day 1."""
        resp = client_auth.get("/api/sap/learning/lessons/1")
        assert resp.status_code == 200, (
            f"Expected 200 for unlocked Day 1, got {resp.status_code}: {resp.json()}"
        )
        data = resp.json()
        assert data["day_number"] == 1
        assert "steps" in data
        assert len(data["steps"]) > 0

    def test_waived_day_lesson_returns_403(self, client_auth, mock_user, db_session):
        """A day waived by diagnostic placement must return 403 on lesson content access."""
        # Mark Day 1 as waived
        day_state = db_session.execute(
            select(SAPUserDayState).where(
                SAPUserDayState.user_id == mock_user.id,
                SAPUserDayState.day_number == 1,
            )
        ).scalar_one_or_none()

        if day_state is None:
            day_state = SAPUserDayState(
                user_id=mock_user.id,
                day_number=1,
                status=SAPDayStatus.WAIVED_BY_PLACEMENT.value,
                waived=True,
            )
            db_session.add(day_state)
        else:
            day_state.waived = True
            day_state.status = SAPDayStatus.WAIVED_BY_PLACEMENT.value
        db_session.commit()

        resp = client_auth.get("/api/sap/learning/lessons/1")
        assert resp.status_code == 403, (
            f"Expected 403 for waived Day 1, got {resp.status_code}: {resp.json()}"
        )
        assert "waived" in resp.json()["detail"].lower()

    def test_completed_day_lesson_remains_accessible(self, client_auth, mock_user, db_session):
        """A completed day's lesson content must still be accessible (for review)."""
        # Complete Day 1 fully: practice + lesson + assessment
        client_auth.post("/api/sap/learning/complete-practice", json={"day_number": 1})
        client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 1})
        client_auth.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 1,
                "assessment_id": "d1_s6_assessment",
                "assessment_type": "mcq",
                "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
            },
        )

        # Completed day lesson should still return 200 (review access)
        resp = client_auth.get("/api/sap/learning/lessons/1")
        assert resp.status_code == 200, (
            f"Expected 200 for completed Day 1 (review access), got {resp.status_code}"
        )
        data = resp.json()
        assert data["day_number"] == 1

    def test_nonexistent_lesson_day_returns_404(self, client_auth):
        """Requesting lesson content for a day beyond the authored range returns 404."""
        resp = client_auth.get("/api/sap/learning/lessons/999")
        # Day 999 is far beyond the authored range — must return 404 (not 403)
        assert resp.status_code == 404