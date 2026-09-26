"""SAP placement lifecycle + waived-day concept continuity (Batch 3).

Lifecycle: placement is freely retakeable until the learner produces learning evidence
(day progress, assessment/mission attempts, skill evidence). After that, /submit and
/choose-start return 409 with zero writes, so history can never be waived, relocked,
reset, or moved backward. Identical retakes are no-ops; diagnostic mastery is awarded once.

Continuity: a waived day's concepts can be earned later through a graded waived-day
challenge (same server-side evaluator, lesson stays closed, day stays waived). A
machine-checked invariant proves every placement outcome keeps every mission reachable.
"""

from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app.api.deps import get_current_user
from app.data.sap_lessons import SAP_DAYS_CONTENT
from app.database import get_db
from app.main import app
from app.models.models import User
from app.models.sap_models import (
    SAPAssessmentAttempt,
    SAPConcept,
    SAPMissionAttempt,
    SAPPlacementProfile,
    SAPSkillEvidence,
    SAPUserConceptMastery,
    SAPUserDayState,
    SAPUserState,
)
from app.sap.data.placement_questions import EXPERIENCED_QUESTIONS, NOT_SURE_QUESTIONS
from app.sap.services.missions import SAPMissionRegistry
from app.sap.services.placement import SAPPlacementService
from app.sap.services.progression import SAPProgressionService
from tests.sap_concept_paths import (
    assessment_evidence_concepts,
    correct_assessment_answers,
    mission_fixpoint,
    unresolved_prerequisites,
    wrong_assessment_answers,
)
from tests.sap_practice_helpers import practice_payload

client = TestClient(app, raise_server_exceptions=False)

EXPERIENCED_ALL_CORRECT = {q["id"]: q["correct_option"] for q in EXPERIENCED_QUESTIONS}   # -> Day 77
NOT_SURE_ALL_CORRECT = {q["id"]: q["correct_option"] for q in NOT_SURE_QUESTIONS}         # -> Day 9


# =============================================================================
# Fixtures & helpers
# =============================================================================

@pytest.fixture
def user(db):
    tag = uuid.uuid4().hex[:8]
    u = User(id=uuid.uuid4(), email=f"plc_{tag}@example.com", username=f"plc_{tag}", name="Placement")
    db.add(u)
    db.commit()
    app.dependency_overrides[get_current_user] = lambda: u
    app.dependency_overrides[get_db] = lambda: db
    yield u
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_db, None)


def place(level: str, answers: dict | None = None):
    return client.post("/api/sap/placement/submit", json={"experience_level": level, "answers": answers or {}})


def snapshot(db, user_id) -> dict:
    """Everything placement or learning could touch, including timestamps."""
    db.expire_all()

    def count(model):
        return db.execute(select(func.count()).select_from(model).where(model.user_id == user_id)).scalar_one()

    profile = db.execute(select(SAPPlacementProfile).where(SAPPlacementProfile.user_id == user_id)).scalar_one_or_none()
    state = db.execute(select(SAPUserState).where(SAPUserState.user_id == user_id)).scalar_one_or_none()
    return {
        "profile": None if profile is None else (
            profile.persona, profile.recommended_start_day, profile.completed_at,
            repr(sorted((profile.diagnostic_results or {}).items())),
        ),
        "user_state": None if state is None else (
            state.current_recommended_day, state.placement_score, state.completed_days_count,
        ),
        "days": sorted(
            (d.day_number, d.status, d.waived, d.lesson_started, d.lesson_completed, d.lesson_completed_at,
             d.practice_completed, d.practice_completed_at, d.assessment_passed, d.assessment_passed_at,
             d.completed, d.completed_at)
            for d in db.execute(select(SAPUserDayState).where(SAPUserDayState.user_id == user_id)).scalars()
        ),
        "mastery": sorted(
            (slug, m.mastery_score, m.attempts, m.successful_attempts)
            for m, slug in db.execute(
                select(SAPUserConceptMastery, SAPConcept.slug)
                .join(SAPConcept, SAPConcept.id == SAPUserConceptMastery.concept_id)
                .where(SAPUserConceptMastery.user_id == user_id)
            ).all()
        ),
        "evidence": count(SAPSkillEvidence),
        "assessment_attempts": count(SAPAssessmentAttempt),
        "mission_attempts": count(SAPMissionAttempt),
    }


def mastery_of(db, user_id, slug):
    db.expire_all()
    row = db.execute(
        select(SAPUserConceptMastery).join(SAPConcept, SAPConcept.id == SAPUserConceptMastery.concept_id)
        .where(SAPUserConceptMastery.user_id == user_id, SAPConcept.slug == slug)
    ).scalar_one_or_none()
    return row


def pass_day_1():
    assert client.post("/api/sap/learning/complete-practice", json=practice_payload(1)).json()["passed"]
    assert client.post("/api/sap/learning/complete-lesson", json={"day_number": 1}).status_code == 200
    res = client.post("/api/sap/assessments/submit", json={
        "day_number": 1, "assessment_id": "d1_s6_assessment", "assessment_type": "mcq",
        "submission_payload": {"answers": correct_assessment_answers(1)},
    })
    assert res.status_code == 200 and res.json()["day_completed"] is True


# =============================================================================
# 1. Retakes before learning
# =============================================================================

def test_rerun_before_learning_is_allowed_and_does_not_inflate_mastery(db, user):
    first = place("experienced", EXPERIENCED_ALL_CORRECT)
    assert first.status_code == 200 and first.json()["recommended_start_day"] == 77
    shared = set(first.json()["demonstrated_concepts"])
    assert first.json()["placement_locked"] is False

    second = place("not_sure", NOT_SURE_ALL_CORRECT)
    assert second.status_code == 200 and second.json()["recommended_start_day"] == 9
    assert SAPProgressionService.compute_user_progress(db, user.id)["waived_days"] == list(range(1, 9))

    # Mastery from the first diagnostic is kept (never erased) and a concept demonstrated
    # by both diagnostics is awarded once, not twice.
    both = shared & set(second.json()["demonstrated_concepts"])
    assert both, "fixture expects an overlapping concept"
    for slug in shared | set(second.json()["demonstrated_concepts"]):
        row = mastery_of(db, user.id, slug)
        assert row is not None and row.attempts == 1, slug


def test_identical_rerun_is_a_no_op(db, user):
    assert place("not_sure", NOT_SURE_ALL_CORRECT).status_code == 200
    snap = snapshot(db, user.id)
    for _ in range(3):
        res = place("not_sure", NOT_SURE_ALL_CORRECT)
        assert res.status_code == 200 and res.json()["recommended_start_day"] == 9
    assert snapshot(db, user.id) == snap


def test_choose_start_before_learning_is_allowed_and_idempotent(db, user):
    place("experienced", EXPERIENCED_ALL_CORRECT)
    assert client.post("/api/sap/placement/choose-start", json={"start_day": 1}).status_code == 200
    snap = snapshot(db, user.id)
    assert client.post("/api/sap/placement/choose-start", json={"start_day": 1}).status_code == 200
    assert snapshot(db, user.id) == snap


def test_invalid_rerun_payload_changes_nothing(db, user):
    place("not_sure", NOT_SURE_ALL_CORRECT)
    snap = snapshot(db, user.id)
    assert client.post("/api/sap/placement/submit", json={"experience_level": "not_sure",
                                                          "experience_years": -1}).status_code == 422
    assert client.post("/api/sap/placement/choose-start", json={"start_day": 50}).status_code == 400
    assert snapshot(db, user.id) == snap


# =============================================================================
# 2. Lock once learning starts
# =============================================================================

def _assert_locked(db, user_id, *, choose_days=(1,)):
    snap = snapshot(db, user_id)
    for level, answers in (("experienced", EXPERIENCED_ALL_CORRECT), ("not_sure", NOT_SURE_ALL_CORRECT),
                           ("fresher", {})):
        res = place(level, answers)
        assert res.status_code == 409, (level, res.text)
        assert "locked" in res.json()["detail"].lower()
    for day in choose_days:
        assert client.post("/api/sap/placement/choose-start", json={"start_day": day}).status_code == 409
    assert snapshot(db, user_id) == snap
    assert client.get("/api/sap/placement/profile").json()["placement_locked"] is True


def test_rerun_after_lesson_completion_is_locked(db, user):
    place("fresher")
    assert client.post("/api/sap/learning/complete-lesson", json={"day_number": 1}).status_code == 200
    _assert_locked(db, user.id)


def test_rerun_after_practice_is_locked_and_cannot_move_backward(db, user):
    place("not_sure", NOT_SURE_ALL_CORRECT)  # starts at Day 9
    assert client.post("/api/sap/learning/complete-practice", json=practice_payload(9)).json()["passed"]
    before = SAPProgressionService.compute_user_progress(db, user.id)
    _assert_locked(db, user.id, choose_days=(1, 9))
    after = SAPProgressionService.compute_user_progress(db, user.id)
    assert after["current_day"] == before["current_day"] == 9
    assert after["day_states"]["9"]["practice_completed"] is True


def test_rerun_after_assessment_and_mastery_is_locked_and_completed_day_survives(db, user):
    place("fresher")
    pass_day_1()
    _assert_locked(db, user.id)
    prog = SAPProgressionService.compute_user_progress(db, user.id)
    assert 1 in prog["completed_days"]
    assert prog["day_states"]["1"]["waived"] is False
    assert prog["day_states"]["1"]["status"] == "completed"


def test_rerun_after_mission_attempt_is_locked(db, user):
    place("fresher")
    step = SAPMissionRegistry.get("nova-sap-product-selection")["steps"][0]
    correct = next(o["id"] for o in step["options"] if o.get("is_correct"))
    res = client.post("/api/sap/missions/nova-sap-product-selection/attempt",
                      json={"step_id": step["step_id"], "payload": {"selected_option_id": correct}})
    assert res.status_code == 200
    _assert_locked(db, user.id)


def test_learning_evidence_is_empty_right_after_placement(db, user):
    place("experienced", EXPERIENCED_ALL_CORRECT)
    assert SAPPlacementService.learning_evidence(db, user.id) == []
    assert client.get("/api/sap/placement/profile").json()["placement_locked"] is False


# =============================================================================
# 3. Completed history can never be downgraded
# =============================================================================

def test_completed_day_is_never_reported_waived_even_if_rows_were_corrupted(db, user):
    """Legacy corruption (old reruns waived completed days) is repaired on read."""
    place("fresher")
    pass_day_1()
    profile = db.execute(select(SAPPlacementProfile).where(SAPPlacementProfile.user_id == user.id)).scalar_one()
    diag = dict(profile.diagnostic_results)
    diag["waived_days"] = list(range(1, 9))
    profile.diagnostic_results = diag
    day1 = db.execute(select(SAPUserDayState).where(SAPUserDayState.user_id == user.id,
                                                    SAPUserDayState.day_number == 1)).scalar_one()
    day1.waived = True
    day1.status = "waived_by_placement"
    db.commit()

    prog = SAPProgressionService.compute_user_progress(db, user.id)
    assert 1 in prog["completed_days"]
    assert 1 not in prog["waived_days"]
    assert prog["day_states"]["1"]["completed"] is True and prog["day_states"]["1"]["waived"] is False
    assert prog["day_states"]["1"]["assessment_passed_at"] is not None


# =============================================================================
# 4. Waived-day concept continuity
# =============================================================================

@pytest.mark.parametrize("persona", sorted(SAPPlacementService.PERSONA_CONFIG))
def test_every_placement_outcome_keeps_every_mission_reachable(persona):
    """Machine-checked invariant, worst case: placement demonstrated NOTHING.

    Earnable = lessons on non-waived days + challenges on waived days (+ mission awards).
    Every registered mission must stay reachable and no enforced prerequisite may be
    unresolved.
    """
    cfg = SAPPlacementService.PERSONA_CONFIG[persona]
    start = cfg["default_start_day"]
    waived = set(cfg["max_waivable_days"])
    assert waived == set(range(1, start))

    seed: set[str] = set()
    for day in SAP_DAYS_CONTENT:
        seed |= assessment_evidence_concepts(day)  # lesson if day >= start, challenge if waived
    earnable, reachable = mission_fixpoint(seed)
    assert unresolved_prerequisites(earnable, enforced_only=True) == []
    assert reachable == SAPMissionRegistry.get_slugs()
    # Anything unearnable without placement evidence may only be an advisory prerequisite
    # of an entry (difficulty-1) mission, which never locks.
    for slug, _ in unresolved_prerequisites(earnable):
        assert SAPMissionRegistry.get(slug)["difficulty"] <= 1, slug


def test_without_challenges_deep_placement_would_strand_missions():
    """Documents why the challenge path is required: lessons alone cannot reach them."""
    seed: set[str] = set()
    for day in SAP_DAYS_CONTENT:
        if day >= 77:
            seed |= assessment_evidence_concepts(day)
    _, reachable = mission_fixpoint(seed)
    assert SAPMissionRegistry.get_slugs() - reachable


def test_waived_lesson_stays_closed_and_non_waived_days_have_no_challenge(db, user):
    place("not_sure", NOT_SURE_ALL_CORRECT)  # waives 1..8
    assert client.get("/api/sap/learning/lessons/6").status_code == 403
    assert client.get("/api/sap/assessments/challenge/9").status_code == 403
    before = snapshot(db, user.id)
    res = client.post("/api/sap/assessments/challenge", json={
        "day_number": 9, "assessment_id": "d9_s6_assessment", "assessment_type": "mcq",
        "submission_payload": {"answers": {"q1": "a"}}})
    assert res.status_code == 403
    assert snapshot(db, user.id) == before


def test_challenge_payload_has_no_answer_keys(db, user):
    place("not_sure", NOT_SURE_ALL_CORRECT)
    res = client.get("/api/sap/assessments/challenge/6")
    assert res.status_code == 200
    body = res.json()
    assert body["questions"]
    for key in ("is_correct", "correct_option_id", "correct_answer", "explanation", "rubric", "scoring_key"):
        assert f'"{key}"' not in res.text, key
    assert set(body) == {"day_number", "day_title", "title", "assessment_id", "assessment_type", "questions"}


def _challenge(day, answers, **overrides):
    view = client.get(f"/api/sap/assessments/challenge/{day}").json()
    body = {"day_number": day, "assessment_id": view["assessment_id"],
            "assessment_type": view["assessment_type"], "submission_payload": {"answers": answers}}
    body.update(overrides)
    return client.post("/api/sap/assessments/challenge", json=body)


def test_passing_a_challenge_earns_only_demonstrated_concepts_and_unlocks_missions(db, user):
    place("not_sure", NOT_SURE_ALL_CORRECT)
    mission = "nova-architecture-layer-incident"  # difficulty 2, needs three-tier-architecture (Day 6)
    assert "three-tier-architecture" in SAPMissionRegistry.get(mission)["prerequisite_concepts"]
    assert mastery_of(db, user.id, "three-tier-architecture") is None  # not demonstrated by placement
    assert client.post(f"/api/sap/missions/{mission}/start").status_code == 403

    before = SAPProgressionService.compute_user_progress(db, user.id)
    rows_before = snapshot(db, user.id)
    res = _challenge(6, correct_assessment_answers(6))
    assert res.status_code == 200, res.text
    assert res.json()["passed"] is True and res.json()["day_completed"] is False

    # No day-state or macro-progress write at all (not even assessment_passed on Day 6).
    rows_after = snapshot(db, user.id)
    assert rows_after["days"] == rows_before["days"]
    assert rows_after["user_state"] == rows_before["user_state"]
    assert rows_after["profile"] == rows_before["profile"]

    after = SAPProgressionService.compute_user_progress(db, user.id)
    assert after["day_states"]["6"]["waived"] is True
    assert after["completed_days"] == before["completed_days"]
    assert after["current_day"] == before["current_day"] == 9
    assert client.get("/api/sap/learning/lessons/6").status_code == 403

    for slug in assessment_evidence_concepts(6):
        assert mastery_of(db, user.id, slug).mastery_score >= 70.0, slug
    evidence = db.execute(select(SAPSkillEvidence).where(SAPSkillEvidence.user_id == user.id)).scalars().all()
    assert evidence and {e.source_type for e in evidence} == {"placement_challenge"}
    assert client.post(f"/api/sap/missions/{mission}/start").status_code == 200


def test_failed_challenge_earns_no_mastery_and_keeps_day_waived(db, user):
    place("not_sure", NOT_SURE_ALL_CORRECT)
    res = _challenge(6, wrong_assessment_answers(6))
    assert res.status_code == 200 and res.json()["passed"] is False
    for slug in assessment_evidence_concepts(6):
        row = mastery_of(db, user.id, slug)
        assert row is None or row.mastery_score < 70.0, slug
    prog = SAPProgressionService.compute_user_progress(db, user.id)
    assert prog["day_states"]["6"]["waived"] is True and prog["current_day"] == 9


@pytest.mark.parametrize("override", [
    {"assessment_id": "d7_s6_assessment"},
    {"assessment_id": "fake"},
    {"assessment_type": "rubric_based"},
])
def test_forged_challenge_identity_rejected_with_zero_mutation(db, user, override):
    place("not_sure", NOT_SURE_ALL_CORRECT)
    before = snapshot(db, user.id)
    assert _challenge(6, correct_assessment_answers(6), **override).status_code == 400
    assert snapshot(db, user.id) == before
