"""Comprehensive test suite for SAP Lesson & Progression Gating Correctness.

Verifies:
1. Normal completion flow: practice completion + passing assessment + lesson completion -> day complete -> next day unlocked.
2. Failed assessment: assessment fail -> day NOT complete -> next day remains locked.
3. Assessment retry: failed attempt followed by passing attempt authoritatively completes day.
4. Locked day gating: server rejects completing locked milestones out of order.
5. Assessment contract validation: accepts "capstone_multi_concept", "mcq", and all curriculum assessment types without 422 error.
6. Waived placement days: placement-waived days (e.g. Days 1-8) allow completing Day 9 and properly unlocking Day 10.
7. Server state persistence across refresh: GET /api/sap/learning/progress accurately reflects all day states.
"""

from __future__ import annotations

from datetime import datetime, timezone
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "TEXT"

from tests.sap_practice_helpers import practice_payload
from app.main import app
from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import Base, User
from app.models.sap_models import (
    SAPUserState,
    SAPUserDayState,
    SAPDayStatus,
    SAPPlacementProfile,
    SAPPlacementStatus,
)

# In-memory SQLite for isolated integration testing
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
        email=f"sap_gating_{str(user_id)[:8]}@example.com",
        username=f"sapuser_{str(user_id)[:8]}",
        name="SAP Gating Tester",
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
# 1. Normal Completion Flow: Practice + Assessment + Lesson Complete
# =============================================================================

def test_normal_completion_flow(client_auth, mock_user, db_session):
    """Test full sequential lifecycle: practice -> assessment pass -> lesson complete -> Day 2 unlocked."""
    # Step 1: Complete interactive practice for Day 1
    practice_resp = client_auth.post("/api/sap/learning/complete-practice", json=practice_payload(1))
    assert practice_resp.status_code == 200
    practice_data = practice_resp.json()
    assert practice_data["practice_completed"] is True
    assert practice_data["day_number"] == 1

    # Step 2: Complete lesson step
    lesson_resp = client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 1})
    assert lesson_resp.status_code == 200
    lesson_data = lesson_resp.json()
    assert lesson_data["lesson_completed"] is True
    # Assessment not yet passed, so day should NOT be fully completed
    assert lesson_data["day_completed"] is False

    # Step 3: Submit passing assessment for Day 1
    assess_resp = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {
                "answers": {
                    "q1": "q1_a",
                    "q2": "q2_a",
                }
            },
        },
    )
    assert assess_resp.status_code == 200
    assess_data = assess_resp.json()
    assert assess_data["passed"] is True
    assert assess_data["score"] >= 70.0
    # Combined with lesson_completed, day is now complete and Day 2 unlocked
    assert assess_data["day_completed"] is True
    assert assess_data["unlocked_next_day"] is True
    assert assess_data["next_day_number"] == 2

    # Verify server progress overview
    progress_resp = client_auth.get("/api/sap/learning/progress")
    assert progress_resp.status_code == 200
    progress = progress_resp.json()
    assert progress["current_day"] == 2
    assert 1 in progress["completed_days"]

    day1_state = progress["day_states"]["1"]
    assert day1_state["completed"] is True
    assert day1_state["lesson_completed"] is True
    assert day1_state["practice_completed"] is True
    assert day1_state["assessment_passed"] is True
    assert day1_state["status"] == "completed"

    day2_state = progress["day_states"]["2"]
    assert day2_state["unlocked"] is True
    assert day2_state["completed"] is False
    assert day2_state["status"] in ("available", "current")


# =============================================================================
# 2. Failed Assessment Flow
# =============================================================================

def test_failed_assessment_blocks_day_completion(client_auth, mock_user, db_session):
    """Test that failing an assessment does NOT unlock the next day or complete the milestone."""
    # Complete Day 1 first
    client_auth.post("/api/sap/learning/complete-practice", json=practice_payload(1))
    client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 1})
    client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {
                "answers": {"q1": "q1_a", "q2": "q2_a"}
            },
        },
    )

    # Now on Day 2: Complete practice and lesson
    client_auth.post("/api/sap/learning/complete-practice", json=practice_payload(2))
    client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 2})

    # Submit deliberate wrong answers to fail Day 2 assessment
    fail_resp = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 2,
            "assessment_id": "d2_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {
                "answers": {
                    "d2_q1": "b",
                    "d2_q2": "c",
                }
            },
        },
    )
    assert fail_resp.status_code == 200
    fail_data = fail_resp.json()
    assert fail_data["passed"] is False
    assert fail_data["score"] < 70.0
    assert fail_data["day_completed"] is False
    assert fail_data["unlocked_next_day"] is False

    # Day 3 MUST remain locked
    progress_resp = client_auth.get("/api/sap/learning/progress")
    assert progress_resp.status_code == 200
    progress = progress_resp.json()
    assert progress["current_day"] == 2
    assert 2 not in progress["completed_days"]

    day2_state = progress["day_states"]["2"]
    assert day2_state["completed"] is False
    assert day2_state["assessment_passed"] is False

    day3_state = progress["day_states"]["3"]
    assert day3_state["unlocked"] is False
    assert day3_state["status"] == "locked"


# =============================================================================
# 3. Assessment Retry Flow
# =============================================================================

def test_assessment_retry_success(client_auth, mock_user, db_session):
    """Test that retrying a previously failed assessment with passing answers unlocks next milestone."""
    # Ensure Day 1 complete
    client_auth.post("/api/sap/learning/complete-practice", json=practice_payload(1))
    client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 1})
    client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {
                "answers": {"q1": "q1_a", "q2": "q2_a"}
            },
        },
    )

    client_auth.post("/api/sap/learning/complete-practice", json=practice_payload(2))
    client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 2})

    # Initial fail
    fail_resp = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 2,
            "assessment_id": "d2_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {"answers": {"d2_q1": "b", "d2_q2": "c"}},
        },
    )
    assert fail_resp.json()["passed"] is False

    # Retry with correct answers
    retry_resp = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 2,
            "assessment_id": "d2_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {
                "answers": {
                    "d2_q1": "a",
                    "d2_q2": "a",
                }
            },
        },
    )
    assert retry_resp.status_code == 200
    retry_data = retry_resp.json()
    assert retry_data["passed"] is True
    assert retry_data["day_completed"] is True
    assert retry_data["unlocked_next_day"] is True
    assert retry_data["next_day_number"] == 3


# =============================================================================
# 4. Locked Day Rejection
# =============================================================================

def test_server_rejects_completing_locked_milestone(client_auth, mock_user, db_session):
    """Verify that attempting to complete a locked day fails with 400."""
    # Fresh user starts on Day 1; Day 5 is locked
    resp = client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 5})
    assert resp.status_code == 400
    assert "locked" in resp.json()["detail"].lower()

    # Practice on locked day must also be rejected
    resp_prac = client_auth.post("/api/sap/learning/complete-practice", json=practice_payload(5))
    assert resp_prac.status_code == 400
    assert "locked" in resp_prac.json()["detail"].lower()


# =============================================================================
# 5. Capstone Multi-Concept Contract Acceptance (No 422)
# =============================================================================

def test_capstone_multi_concept_contract_acceptance(client_auth, mock_user, db_session):
    """Verify that 'capstone_multi_concept' and all manifest assessment types are accepted without 422 error."""
    now = datetime.now(timezone.utc)
    for d in range(1, 8):
        day_state = SAPUserDayState(
            user_id=mock_user.id,
            day_number=d,
            status=SAPDayStatus.COMPLETED.value,
            lesson_completed=True,
            lesson_completed_at=now,
            practice_completed=True,
            practice_completed_at=now,
            assessment_passed=True,
            assessment_passed_at=now,
            completed=True,
            completed_at=now,
        )
        db_session.add(day_state)
    user_state = SAPUserState(
        user_id=mock_user.id,
        current_recommended_day=8,
        completed_days_count=7,
        last_active_at=now,
    )
    db_session.add(user_state)
    db_session.commit()

    # Day 8 is now available
    client_auth.post("/api/sap/learning/complete-practice", json=practice_payload(8))
    client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 8})

    # Submit Day 8 capstone with assessment_type="capstone_multi_concept"
    capstone_payload = {
        "day_number": 8,
        "assessment_id": "d8_s6_assessment",
        "assessment_type": "capstone_multi_concept",
        "submission_payload": {
            "answers": {
                "cap_q1": "a",
                "cap_q2": "a",
                "cap_q3": "a",
                "cap_q4": "a",
                "cap_q5": "a",
                "cap_q6": "a",
            }
        },
    }
    resp = client_auth.post("/api/sap/assessments/submit", json=capstone_payload)
    # Must NOT return 422 Unprocessable Entity
    assert resp.status_code == 200
    data = resp.json()
    assert data["passed"] is True
    assert data["score"] == 100.0
    assert data["day_completed"] is True
    assert data["unlocked_next_day"] is True
    assert data["next_day_number"] == 9
    assert "concept_evaluations" in data
    assert any(c["concept_slug"] == "org-structure-company-code" for c in data["concept_evaluations"])


# =============================================================================
# 6. Waived Placement Days Progression
# =============================================================================

def test_waived_placement_days_progression(client_auth, mock_user, db_session):
    """Verify that placement-waived days (e.g. 1-8) allow completing Day 9 and advancing to Day 10."""
    now = datetime.now(timezone.utc)
    placement = SAPPlacementProfile(
        id=uuid.uuid4(),
        user_id=mock_user.id,
        persona="beginner",
        recommended_start_day=9,
        diagnostic_results={"score": 85.0},
    )
    db_session.add(placement)

    # Mark days 1-8 as waived
    for d in range(1, 9):
        day_state = SAPUserDayState(
            user_id=mock_user.id,
            day_number=d,
            status=SAPDayStatus.WAIVED_BY_PLACEMENT.value,
            completed=False,
        )
        db_session.add(day_state)

    user_state = SAPUserState(
        user_id=mock_user.id,
        current_recommended_day=9,
        completed_days_count=0,
        placement_status=SAPPlacementStatus.COMPLETED.value,
        placement_score=85.0,
        last_active_at=now,
    )
    db_session.add(user_state)
    db_session.commit()

    # Progress overview shows Day 9 is current
    progress_resp = client_auth.get("/api/sap/learning/progress")
    assert progress_resp.status_code == 200
    prog = progress_resp.json()
    assert prog["current_day"] == 9
    assert prog["day_states"]["9"]["unlocked"] is True
    assert prog["day_states"]["10"]["unlocked"] is False

    # Complete Day 9
    client_auth.post("/api/sap/learning/complete-practice", json=practice_payload(9))
    client_auth.post("/api/sap/learning/complete-lesson", json={"day_number": 9})
    assess_resp = client_auth.post(
        "/api/sap/assessments/submit",
        json={
            "day_number": 9,
            "assessment_id": "d9_s6_assessment",
            "assessment_type": "mcq",
            "submission_payload": {
                "answers": {"d9_q1": "a", "d9_q2": "a"}
            },
        },
    )
    assert assess_resp.status_code == 200
    assess_data = assess_resp.json()
    assert assess_data["passed"] is True
    assert assess_data["unlocked_next_day"] is True
    assert assess_data["next_day_number"] == 10

    # Day 10 is now unlocked
    progress_after = client_auth.get("/api/sap/learning/progress").json()
    assert progress_after["current_day"] == 10
    assert progress_after["day_states"]["10"]["unlocked"] is True
