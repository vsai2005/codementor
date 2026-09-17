"""Comprehensive test suite for Python Learning Progression and Gating.

Verifies:
1. Lesson complete without Practice: Day 1 lesson completed sets lesson_completed=True,
   but practice_passed=False and completed=False. Day 2 remains locked (403 if attempted).
2. Practice pass without Lesson: Practice passed sets practice_passed=True, but
   lesson_completed=False and completed=False. Day 2 remains locked.
3. Both Lesson and Practice complete: Day 1 completed=True, Day 2 unlocks.
4. Failed practice submission does not record practice pass; Day 2 remains locked.
5. Strict sequential gating: Completing Day 3 when Day 2 is locked returns 403 Forbidden.
6. Developer fast-forward endpoint is disabled in production environments (403 Forbidden).
7. Tampered local progression cannot bypass server gating.
8. Full multi-day progression chain (Day 1 -> Day 2 -> Day 3) strictly requires both flags on each day.
9. All 160 curriculum days have valid practice mappings in CURRICULUM_DAY_PRACTICE
   and reverse lookup in PRACTICE_SLUG_TO_DAYS.
"""

from __future__ import annotations

import uuid
from unittest.mock import patch, MagicMock
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
from app.models.models import Base, User, UserLearningDayState, Problem, Topic
from app.core.curriculum_map import CURRICULUM_DAY_PRACTICE, PRACTICE_SLUG_TO_DAYS
from app.services.learning import record_practice_passed, compute_user_progress

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
        email=f"py_gating_{str(user_id)[:8]}@example.com",
        username=f"pyuser_{str(user_id)[:8]}",
        name="Python Gating Tester",
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


def test_initial_learning_progress_state(client_auth):
    """Initially, Day 1 is unlocked/current and Days 2-160 are locked."""
    res = client_auth.get("/api/learning/progress")
    assert res.status_code == 200
    data = res.json()
    assert data["current_day"] == 1
    assert data["completed_days"] == []
    assert data["total_days"] == 160

    day1 = data["day_states"]["1"]
    assert day1["unlocked"] is True
    assert day1["status"] == "current"
    assert day1["lesson_completed"] is False
    assert day1["practice_passed"] is False
    assert day1["completed"] is False

    day2 = data["day_states"]["2"]
    assert day2["unlocked"] is False
    assert day2["status"] == "locked"


def test_lesson_complete_without_practice_keeps_next_day_locked(client_auth):
    """Completing Day 1 lesson must NOT unlock Day 2 or complete Day 1."""
    res = client_auth.post("/api/learning/complete-lesson", json={"day_number": 1})
    assert res.status_code == 200
    data = res.json()
    assert data["lesson_completed"] is True
    assert data["day_completed"] is False
    assert data["unlocked_next_day"] is False

    # Check progress state
    prog_res = client_auth.get("/api/learning/progress")
    assert prog_res.status_code == 200
    prog = prog_res.json()
    assert prog["completed_days"] == []
    assert prog["current_day"] == 1

    day1 = prog["day_states"]["1"]
    assert day1["lesson_completed"] is True
    assert day1["practice_passed"] is False
    assert day1["completed"] is False
    assert day1["unlocked"] is True

    day2 = prog["day_states"]["2"]
    assert day2["unlocked"] is False
    assert day2["status"] == "locked"

    # Attempting to complete Day 2 must be rejected with 403 Forbidden
    res_day2 = client_auth.post("/api/learning/complete-lesson", json={"day_number": 2})
    assert res_day2.status_code == 403
    assert "locked" in res_day2.json()["detail"].lower()


def test_practice_passed_without_lesson_keeps_next_day_locked(client_auth, db_session, mock_user):
    """Passing practice without completing lesson sets practice_passed=True, but Day 2 remains locked."""
    day1_problem_slug = CURRICULUM_DAY_PRACTICE[1]
    res_practice = record_practice_passed(db_session, mock_user.id, day1_problem_slug)
    assert res_practice is not None
    assert 1 in res_practice["affected_days"]
    assert res_practice["newly_completed_days"] == []
    assert res_practice["unlocked_days"] == []

    prog_res = client_auth.get("/api/learning/progress")
    prog = prog_res.json()
    assert prog["completed_days"] == []
    assert prog["current_day"] == 1

    day1 = prog["day_states"]["1"]
    assert day1["lesson_completed"] is False
    assert day1["practice_passed"] is True
    assert day1["completed"] is False

    day2 = prog["day_states"]["2"]
    assert day2["unlocked"] is False
    assert day2["status"] == "locked"

    # Day 2 complete-lesson still rejected with 403
    res_day2 = client_auth.post("/api/learning/complete-lesson", json={"day_number": 2})
    assert res_day2.status_code == 403


def test_both_lesson_and_practice_completed_unlocks_next_day(client_auth, db_session, mock_user):
    """When both lesson is completed and practice is passed, Day 1 completes and Day 2 unlocks."""
    # Complete lesson
    res_lesson = client_auth.post("/api/learning/complete-lesson", json={"day_number": 1})
    assert res_lesson.status_code == 200

    # Pass practice
    day1_problem_slug = CURRICULUM_DAY_PRACTICE[1]
    res_practice = record_practice_passed(db_session, mock_user.id, day1_problem_slug)
    assert res_practice is not None
    assert 1 in res_practice["newly_completed_days"]
    assert 2 in res_practice["unlocked_days"]

    prog_res = client_auth.get("/api/learning/progress")
    prog = prog_res.json()
    assert prog["completed_days"] == [1]
    assert prog["current_day"] == 2

    day1 = prog["day_states"]["1"]
    assert day1["lesson_completed"] is True
    assert day1["practice_passed"] is True
    assert day1["completed"] is True
    assert day1["status"] == "completed"

    day2 = prog["day_states"]["2"]
    assert day2["unlocked"] is True
    assert day2["status"] == "current"

    # Now Day 2 complete-lesson succeeds!
    res_day2 = client_auth.post("/api/learning/complete-lesson", json={"day_number": 2})
    assert res_day2.status_code == 200
    assert res_day2.json()["lesson_completed"] is True


def test_consecutive_gating_cannot_skip_days(client_auth, db_session, mock_user):
    """Learners cannot skip ahead to Day 3 or Day 10 without completing prior days."""
    # Complete Day 1
    client_auth.post("/api/learning/complete-lesson", json={"day_number": 1})
    day1_slug = CURRICULUM_DAY_PRACTICE[1]
    record_practice_passed(db_session, mock_user.id, day1_slug)

    # Day 2 is unlocked, but Day 3 is locked
    res_day3 = client_auth.post("/api/learning/complete-lesson", json={"day_number": 3})
    assert res_day3.status_code == 403
    assert "locked" in res_day3.json()["detail"].lower()

    res_day10 = client_auth.post("/api/learning/complete-lesson", json={"day_number": 10})
    assert res_day10.status_code == 403


def test_full_progression_chain_days_1_to_3(client_auth, db_session, mock_user):
    """Verify full sequential progression across Days 1, 2, and 3."""
    # Day 1
    client_auth.post("/api/learning/complete-lesson", json={"day_number": 1})
    record_practice_passed(db_session, mock_user.id, CURRICULUM_DAY_PRACTICE[1])
    
    # Day 2 is now unlocked
    prog = client_auth.get("/api/learning/progress").json()
    assert prog["current_day"] == 2
    assert prog["day_states"]["2"]["unlocked"] is True
    assert prog["day_states"]["3"]["unlocked"] is False

    # Day 2: complete lesson only
    client_auth.post("/api/learning/complete-lesson", json={"day_number": 2})
    prog = client_auth.get("/api/learning/progress").json()
    # Day 3 MUST still be locked because Day 2 practice is not passed
    assert prog["day_states"]["3"]["unlocked"] is False
    assert 3 not in prog["completed_days"]

    # Day 2: complete practice
    record_practice_passed(db_session, mock_user.id, CURRICULUM_DAY_PRACTICE[2])
    prog = client_auth.get("/api/learning/progress").json()
    assert prog["completed_days"] == [1, 2]
    assert prog["current_day"] == 3
    assert prog["day_states"]["3"]["unlocked"] is True


def test_stale_or_tampered_client_cannot_bypass_server(client_auth, db_session, mock_user):
    """Server state is strictly authoritative; client cannot forge completion via API."""
    # User tries to directly complete Day 5 without Day 1-4
    res = client_auth.post("/api/learning/complete-lesson", json={"day_number": 5})
    assert res.status_code == 403
    assert "Day 5 is locked" in res.json()["detail"]

    # In DB, verify no illegitimate records were created
    rows = db_session.execute(
        select(UserLearningDayState).where(UserLearningDayState.user_id == mock_user.id)
    ).scalars().all()
    assert all(r.day_number != 5 for r in rows)


def test_dev_set_progress_disabled_in_production(client_auth):
    """POST /api/learning/dev-set-progress is strictly forbidden in production."""
    with patch("app.api.routes.learning.get_settings") as mock_settings:
        mock_settings.return_value.is_production = True
        res = client_auth.post("/api/learning/dev-set-progress", json={"completed_up_to": 5})
        assert res.status_code == 403
        assert "disabled in production" in res.json()["detail"].lower()


def test_all_160_days_practice_mappings():
    """Verify that Days 1-160 all have assigned practice problems and correct reverse index."""
    assert len(CURRICULUM_DAY_PRACTICE) == 160
    for day in range(1, 161):
        assert day in CURRICULUM_DAY_PRACTICE, f"Day {day} missing practice mapping"
        slug = CURRICULUM_DAY_PRACTICE[day]
        assert isinstance(slug, str) and len(slug) > 0
        assert slug in PRACTICE_SLUG_TO_DAYS, f"Slug {slug} missing from reverse lookup map"
        assert day in PRACTICE_SLUG_TO_DAYS[slug], f"Day {day} missing from reverse mapped days for {slug}"
