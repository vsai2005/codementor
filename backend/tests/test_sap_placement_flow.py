"""Comprehensive tests for SAP Real Objective Placement Diagnostic Flow.

Tests:
1. GET /api/sap/placement/questions (experienced: 10 questions, not_sure: 6 questions, no answers leaked)
2. POST /api/sap/placement/submit (Fresher -> Day 1, no assessment)
3. POST /api/sap/placement/submit (Experienced high score -> Day 77 + demonstrated concepts)
4. POST /api/sap/placement/submit (Experienced mid score -> Day 45 or Day 23)
5. POST /api/sap/placement/submit (Prerequisite conflict -> fails fundamental architecture -> Day 1)
6. POST /api/sap/placement/submit (Not Sure high score -> Day 9, low score -> Day 1)
7. POST /api/sap/placement/choose-start (Switch starting day to Day 1)
8. GET /api/sap/placement/profile (Restores placement on refresh)
9. Progress isolation (Waived days never count as completed)
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.deps import get_current_user
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "TEXT"

from app.database import get_db
from app.models.models import Base, User
from app.models.sap_models import (
    SAPPlacementProfile,
    SAPUserState,
    SAPUserDayState,
    SAPUserConceptMastery,
)
from app.sap.services.progression import SAPProgressionService

# In-memory SQLite for isolated integration testing
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(test_db):
    user = User(
        id=uuid.uuid4(),
        email="sap_tester@example.com",
        name="SAP Tester",
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


def override_deps(user, db):
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_db] = lambda: db


def clear_deps():
    app.dependency_overrides.clear()


def test_get_placement_questions_experienced():
    """Verify GET /api/sap/placement/questions returns 10 questions without leaking answers."""
    res = client.get("/api/sap/placement/questions?track=experienced")
    assert res.status_code == 200
    questions = res.json()
    assert len(questions) == 10

    for q in questions:
        assert "id" in q
        assert "topic" in q
        assert "topic_label" in q
        assert "concept_slug" in q
        assert "question" in q
        assert "options" in q
        assert len(q["options"]) == 4
        # CRITICAL: ensure no answer key leaked
        assert "correct_option" not in q
        assert "is_correct" not in q
        for opt in q["options"]:
            assert "is_correct" not in opt
            assert "id" in opt
            assert "text" in opt


def test_get_placement_questions_not_sure():
    """Verify GET /api/sap/placement/questions returns 6 questions for not_sure track."""
    res = client.get("/api/sap/placement/questions?track=not_sure")
    assert res.status_code == 200
    questions = res.json()
    assert len(questions) == 6

    for q in questions:
        assert "correct_option" not in q
        assert len(q["options"]) == 4


def test_submit_fresher_placement(test_user, test_db):
    """Fresher -> NO assessment -> placed at Day 1 -> score 0.0, waived_days []."""
    override_deps(test_user, test_db)
    try:
        payload = {"experience_level": "fresher"}
        res = client.post("/api/sap/placement/submit", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["persona"] == "fresher"
        assert data["recommended_start_day"] == 1
        assert data["diagnostic_score"] == 0.0
        assert data["waived_days"] == []
        assert "fresher" in data["rationale"].lower() or "day 1" in data["rationale"].lower()
    finally:
        clear_deps()


def test_submit_experienced_high_score(test_user, test_db):
    """Experienced with 100% correct answers -> Tier 4 (Day 77 - ABAP Cloud & RAP)."""
    override_deps(test_user, test_db)
    try:
        # All 10 correct answers from placement_questions.py
        all_correct_answers = {
            "exp_arch_01": "b",
            "exp_org_02": "c",
            "exp_acdoca_03": "b",
            "exp_matdoc_04": "a",
            "exp_cvi_05": "b",
            "exp_proc_06": "b",
            "exp_vdm_07": "b",
            "exp_assoc_08": "b",
            "exp_rap_09": "b",
            "exp_bdef_10": "b",
        }
        payload = {
            "experience_level": "experienced",
            "answers": all_correct_answers,
        }
        res = client.post("/api/sap/placement/submit", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["persona"] == "experienced_s4hana"
        assert data["recommended_start_day"] == 77
        assert data["diagnostic_score"] == 100.0
        assert len(data["waived_days"]) == 76  # Days 1-76 waived
        assert len(data["demonstrated_concepts"]) >= 8
        assert len(data["topic_breakdown"]) >= 5
    finally:
        clear_deps()


def test_submit_experienced_mid_score(test_user, test_db):
    """Experienced with architecture + ACDOCA + P2P correct (60%) -> Tier 3 (Day 45)."""
    override_deps(test_user, test_db)
    try:
        mid_answers = {
            "exp_arch_01": "b",  # correct
            "exp_org_02": "c",   # correct
            "exp_acdoca_03": "b", # correct
            "exp_matdoc_04": "a", # correct
            "exp_cvi_05": "b",   # correct
            "exp_proc_06": "b",  # correct
            "exp_vdm_07": "a",   # wrong
            "exp_assoc_08": "a", # wrong
            "exp_rap_09": "a",   # wrong
            "exp_bdef_10": "a",  # wrong
        }
        payload = {
            "experience_level": "experienced",
            "answers": mid_answers,
        }
        res = client.post("/api/sap/placement/submit", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["persona"] == "ecc_developer"
        assert data["recommended_start_day"] == 45
        assert data["diagnostic_score"] == 60.0
        assert len(data["waived_days"]) == 44
    finally:
        clear_deps()


def test_submit_prerequisite_conflict(test_user, test_db):
    """Prerequisite conflict: user got RAP/CDS right but failed fundamental architecture.
    System must detect prerequisite conflict and route back to Day 1."""
    override_deps(test_user, test_db)
    try:
        conflict_answers = {
            "exp_arch_01": "a",  # WRONG on fundamental 3-tier architecture!
            "exp_org_02": "a",   # WRONG
            "exp_acdoca_03": "a", # WRONG
            "exp_matdoc_04": "b", # WRONG
            "exp_cvi_05": "a",   # WRONG
            "exp_proc_06": "a",  # WRONG
            "exp_vdm_07": "b",   # correct
            "exp_assoc_08": "b", # correct
            "exp_rap_09": "b",   # correct
            "exp_bdef_10": "b",  # correct
        }
        payload = {
            "experience_level": "experienced",
            "answers": conflict_answers,
        }
        res = client.post("/api/sap/placement/submit", json=payload)
        assert res.status_code == 200
        data = res.json()
        # Even with 40% score, fundamental architecture failed!
        assert data["recommended_start_day"] == 1
        assert "prerequisite" in data["rationale"].lower() or "architecture" in data["rationale"].lower()
    finally:
        clear_deps()


def test_submit_not_sure_high_and_low_score(test_user, test_db):
    """Not Sure track:
    - High score (>=80%) -> Day 9
    - Low score (<80%) -> Day 1"""
    override_deps(test_user, test_db)
    try:
        # 1. High score
        all_correct = {
            "ns_fund_01": "b",
            "ns_org_02": "b",
            "ns_data_03": "a",
            "ns_p2p_04": "b",
            "ns_hana_05": "a",
            "ns_fiori_06": "b",
        }
        res = client.post("/api/sap/placement/submit", json={"experience_level": "not_sure", "answers": all_correct})
        assert res.status_code == 200
        data = res.json()
        assert data["persona"] == "beginner"
        assert data["recommended_start_day"] == 9
        assert data["diagnostic_score"] == 100.0

        # 2. Low score
        poor_answers = {
            "ns_fund_01": "a",
            "ns_org_02": "a",
            "ns_data_03": "b",
            "ns_p2p_04": "a",
            "ns_hana_05": "b",
            "ns_fiori_06": "a",
        }
        res = client.post("/api/sap/placement/submit", json={"experience_level": "not_sure", "answers": poor_answers})
        assert res.status_code == 200
        data = res.json()
        assert data["recommended_start_day"] == 1
        assert data["diagnostic_score"] == 0.0
    finally:
        clear_deps()


def test_choose_start_day_override(test_user, test_db):
    """User placed at Day 77 can opt to start from Day 1."""
    override_deps(test_user, test_db)
    try:
        # Place at Day 77 first
        all_correct = {
            "exp_arch_01": "b", "exp_org_02": "c", "exp_acdoca_03": "b",
            "exp_matdoc_04": "a", "exp_cvi_05": "b", "exp_proc_06": "b",
            "exp_vdm_07": "b", "exp_assoc_08": "b", "exp_rap_09": "b",
            "exp_bdef_10": "b",
        }
        res = client.post("/api/sap/placement/submit", json={"experience_level": "experienced", "answers": all_correct})
        assert res.status_code == 200
        assert res.json()["recommended_start_day"] == 77

        # User chooses Day 1
        choose_res = client.post("/api/sap/placement/choose-start", json={"start_day": 1})
        assert choose_res.status_code == 200
        choose_data = choose_res.json()
        assert choose_data["recommended_start_day"] == 1
        # Diagnostic score & answers are still preserved
        assert choose_data["diagnostic_score"] == 100.0

        # Profile fetch also reflects Day 1
        prof_res = client.get("/api/sap/placement/profile")
        assert prof_res.status_code == 200
        assert prof_res.json()["recommended_start_day"] == 1
    finally:
        clear_deps()


def test_progress_isolation_and_waived_days(test_user, test_db):
    """Waived days must NOT be marked completed, and completed_days_count must be 0."""
    override_deps(test_user, test_db)
    try:
        all_correct = {
            "exp_arch_01": "b", "exp_org_02": "c", "exp_acdoca_03": "b",
            "exp_matdoc_04": "a", "exp_cvi_05": "b", "exp_proc_06": "b",
            "exp_vdm_07": "b", "exp_assoc_08": "b", "exp_rap_09": "b",
            "exp_bdef_10": "b",
        }
        client.post("/api/sap/placement/submit", json={"experience_level": "experienced", "answers": all_correct})

        # Check progression service
        progress = SAPProgressionService.compute_user_progress(test_db, test_user.id)
        assert progress["current_day"] == 77
        assert len(progress["completed_days"]) == 0  # CRITICAL: 0 completed days!
        assert len(progress["waived_days"]) == 76

        # Check day states
        day_1_state = progress["day_states"]["1"]
        assert day_1_state["status"] == "waived_by_placement"
        assert day_1_state["waived"] is True
        assert day_1_state["completed"] is False  # Must NOT be completed

        day_77_state = progress["day_states"]["77"]
        assert day_77_state["status"] in ("available", "current")
        assert day_77_state["unlocked"] is True
        assert day_77_state["completed"] is False

        day_78_state = progress["day_states"]["78"]
        assert day_78_state["status"] == "locked"
        assert day_78_state["unlocked"] is False
    finally:
        clear_deps()
