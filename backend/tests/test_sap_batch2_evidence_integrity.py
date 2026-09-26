"""Batch 2 adversarial suite: Practice evidence, Mission integrity, Mastery forgery.

Practice
- Self-attestation (day_number only) and client-supplied pass flags are rejected.
- Wrong, forged (unknown step / invalid option / missing step), cross-day, and locked-day
  submissions create zero state. A correct submission completes Practice idempotently.
- Graded practice steps never expose their answer key over the lesson API.

Missions
- Locked missions: 403 on start and attempt, zero state. Unlocked missions start.
- Unknown / fake step ids: 404, never fall back to another step, zero state.
- Wrong answers and malformed payloads never count and write nothing.
- Duplicate valid submissions are idempotent; completion requires every registered step.
- Completion side effects (state mutation, skill evidence, mastery) happen exactly once.

Mastery
- No user-callable endpoint writes mastery from a client score (any concept, any score).
- Internal writers reject non-finite / out-of-range / missing scores.
- Legitimate assessment and mission evidence still create mastery.
"""

from __future__ import annotations

import math
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
    SAPEnterpriseInstance,
    SAPMissionAttempt,
    SAPSkillEvidence,
    SAPUserConceptMastery,
    SAPUserDayState,
    SAPUserState,
)
from app.sap.services.mastery import SAPMasteryService
from app.sap.services.missions import SAPMissionRegistry
from app.sap.services.practice import practice_answer_key, practice_evidence_steps
from tests.sap_practice_helpers import correct_practice_answers, practice_payload

client = TestClient(app, raise_server_exceptions=False)

LOCKED_MISSION = "nova-plant-expansion"          # difficulty 2
ENTRY_MISSION = "nova-org-structure-design"      # difficulty 1; grants LOCKED_MISSION prereqs
OPTIONS_MISSION = "nova-sap-product-selection"   # difficulty 1; option steps only


# =============================================================================
# Fixtures & helpers
# =============================================================================

def _new_user(db) -> User:
    tag = uuid.uuid4().hex[:8]
    user = User(id=uuid.uuid4(), email=f"sap_b2_{tag}@example.com", username=f"sap_b2_{tag}", name="SAP B2")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def user(db):
    return _new_user(db)


@pytest.fixture
def as_user(db):
    """Authenticates the TestClient as the given user for the test's duration."""
    def _login(u: User):
        app.dependency_overrides[get_current_user] = lambda: u
        app.dependency_overrides[get_db] = lambda: db
    yield _login
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_db, None)


def snapshot(db, user_id: uuid.UUID) -> dict:
    """Every table a progression/mastery write could touch, for zero-mutation checks."""
    db.expire_all()

    def count(model):
        return db.execute(select(func.count()).select_from(model).where(model.user_id == user_id)).scalar_one()

    days = db.execute(select(SAPUserDayState).where(SAPUserDayState.user_id == user_id)).scalars().all()
    attempts = db.execute(select(SAPMissionAttempt).where(SAPMissionAttempt.user_id == user_id)).scalars().all()
    mastery = db.execute(select(SAPUserConceptMastery).where(SAPUserConceptMastery.user_id == user_id)).scalars().all()
    return {
        "days": sorted(
            (d.day_number, d.lesson_completed, d.practice_completed, d.practice_completed_at,
             d.assessment_passed, d.completed, d.status)
            for d in days
        ),
        "attempts": sorted(
            (str(a.id), a.status, a.score, a.passed, tuple(a.steps_completed or []))
            for a in attempts
        ),
        "mastery": sorted((str(m.concept_id), m.mastery_score, m.attempts) for m in mastery),
        "evidence": count(SAPSkillEvidence),
        "user_state": count(SAPUserState),
        "state_events": sorted(
            (i.state_version, len(i.audit_log or []))
            for i in db.execute(
                select(SAPEnterpriseInstance).where(SAPEnterpriseInstance.user_id == user_id)
            ).scalars().all()
        ),
    }


def complete_day(db, user_id: uuid.UUID, day_number: int) -> None:
    db.add(SAPUserDayState(
        user_id=user_id, day_number=day_number, status="completed", lesson_started=True,
        lesson_completed=True, practice_completed=True, assessment_passed=True, completed=True,
    ))
    db.commit()


def wrong_option(step: dict) -> str:
    key = practice_answer_key(step) if step.get("step_type") in ("interactive_practice", "practice", "challenge") \
        else next(o["id"] for o in step["options"] if o.get("is_correct"))
    return next(o["id"] for o in step["options"] if o["id"] != key)


def mission_step_payload(step: dict, correct: bool = True) -> dict:
    if step["step_type"] == "order_process":
        order = list(step["correct_order"])
        return {"ordered_items": order if correct else list(reversed(order))}
    if correct:
        return {"selected_option_id": next(o["id"] for o in step["options"] if o.get("is_correct"))}
    return {"selected_option_id": wrong_option(step)}


def mission_steps(slug: str) -> list[dict]:
    return SAPMissionRegistry.get(slug)["steps"]


def attempt_step(slug: str, step_id: str, payload: dict):
    return client.post(f"/api/sap/missions/{slug}/attempt", json={"step_id": step_id, "payload": payload})


def complete_mission(slug: str) -> None:
    for step in mission_steps(slug):
        res = attempt_step(slug, step["step_id"], mission_step_payload(step))
        assert res.status_code == 200, res.text
        assert res.json()["step_success"] is True


# =============================================================================
# 1. Practice evidence
# =============================================================================

def test_every_day_has_server_gradable_practice_evidence():
    for day in range(1, 101):
        steps = practice_evidence_steps(day)
        assert steps, f"Day {day} has no gradable practice evidence step"
        lesson_ids = {s["step_id"] for s in SAP_DAYS_CONTENT[day]["steps"]}
        assert all(s["step_id"] in lesson_ids for s in steps)


def test_direct_practice_self_completion_rejected(db, user, as_user):
    as_user(user)
    before = snapshot(db, user.id)

    res = client.post("/api/sap/learning/complete-practice", json={"day_number": 1})
    assert res.status_code == 422

    forged_flags = {"day_number": 1, "passed": True, "practice_completed": True, "score": 100}
    res = client.post("/api/sap/learning/complete-practice", json=forged_flags)
    assert res.status_code == 422

    res = client.post("/api/sap/learning/complete-practice", json={"day_number": 1, "answers": {}})
    assert res.status_code == 422

    assert snapshot(db, user.id) == before


def test_client_pass_flags_alongside_wrong_answers_are_ignored(db, user, as_user):
    as_user(user)
    before = snapshot(db, user.id)
    step = practice_evidence_steps(1)[0]
    res = client.post("/api/sap/learning/complete-practice", json={
        "day_number": 1,
        "answers": {step["step_id"]: wrong_option(step)},
        "passed": True, "practice_completed": True, "score": 100, "correct": True,
    })
    assert res.status_code == 200
    body = res.json()
    assert body["passed"] is False
    assert body["practice_completed"] is False
    assert snapshot(db, user.id) == before


def test_incorrect_practice_fails_with_zero_mutation_and_no_key_leak(db, user, as_user):
    as_user(user)
    before = snapshot(db, user.id)
    step = practice_evidence_steps(1)[0]
    res = client.post("/api/sap/learning/complete-practice", json={
        "day_number": 1, "answers": {step["step_id"]: wrong_option(step)},
    })
    assert res.status_code == 200
    body = res.json()
    assert body["passed"] is False
    assert body["practice_completed"] is False
    assert body["day_state"]["practice_completed"] is False
    assert [r["correct"] for r in body["results"]] == [False]
    assert practice_answer_key(step) not in res.text  # correct option id never revealed
    assert snapshot(db, user.id) == before


@pytest.mark.parametrize("answers_factory, reason", [
    (lambda: {"fake_step": "opt1"}, "unknown step"),
    (lambda: {**correct_practice_answers(1), "d1_s6_assessment": "q1_a"}, "non-practice step"),
    (lambda: {k: "opt_does_not_exist" for k in correct_practice_answers(1)}, "invalid option"),
])
def test_forged_practice_evidence_rejected(db, user, as_user, answers_factory, reason):
    as_user(user)
    before = snapshot(db, user.id)
    res = client.post("/api/sap/learning/complete-practice", json={"day_number": 1, "answers": answers_factory()})
    assert res.status_code == 400, reason
    assert snapshot(db, user.id) == before


def test_missing_required_practice_step_rejected(db, user, as_user):
    day = next(d for d in range(1, 101) if len(practice_evidence_steps(d)) >= 2)
    for d in range(1, day):
        complete_day(db, user.id, d)
    as_user(user)
    answers = correct_practice_answers(day)
    partial = dict([next(iter(answers.items()))])
    before = snapshot(db, user.id)
    res = client.post("/api/sap/learning/complete-practice", json={"day_number": day, "answers": partial})
    assert res.status_code == 400
    assert "required" in res.json()["detail"]
    assert snapshot(db, user.id) == before


def test_cross_day_and_locked_day_replay_rejected(db, user, as_user):
    complete_day(db, user.id, 1)  # Day 2 unlocked, Day 3 locked
    as_user(user)
    before = snapshot(db, user.id)

    # Day 1's valid evidence replayed as Day 2 evidence
    res = client.post("/api/sap/learning/complete-practice",
                      json={"day_number": 2, "answers": correct_practice_answers(1)})
    assert res.status_code == 400
    assert "not practice activities of SAP Day 2" in res.json()["detail"]

    # Valid Day 3 evidence while Day 3 is locked
    res = client.post("/api/sap/learning/complete-practice", json=practice_payload(3))
    assert res.status_code == 400
    assert "locked" in res.json()["detail"]

    assert snapshot(db, user.id) == before


def test_legitimate_practice_completes_idempotently_and_is_user_bound(db, user, as_user):
    other = _new_user(db)
    as_user(user)
    other_before = snapshot(db, other.id)

    res = client.post("/api/sap/learning/complete-practice", json=practice_payload(1))
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["passed"] is True
    assert body["practice_completed"] is True
    assert all(r["correct"] for r in body["results"])
    assert body["day_completed"] is False  # lesson + assessment still required
    first = snapshot(db, user.id)
    first_at = first["days"][0][3]
    assert first_at is not None

    # Retry / refresh: identical state, original timestamp preserved
    res = client.post("/api/sap/learning/complete-practice", json=practice_payload(1))
    assert res.status_code == 200 and res.json()["passed"] is True
    assert snapshot(db, user.id) == first

    # A later wrong attempt neither revokes nor mutates
    step = practice_evidence_steps(1)[0]
    res = client.post("/api/sap/learning/complete-practice",
                      json={"day_number": 1, "answers": {step["step_id"]: wrong_option(step)}})
    assert res.json()["passed"] is False
    assert res.json()["practice_completed"] is True
    assert snapshot(db, user.id) == first

    # Evidence is bound to the authenticated user only
    assert snapshot(db, other.id) == other_before


@pytest.mark.parametrize("practice_first", [True, False])
def test_practice_and_lesson_ordering_preserved(db, user, as_user, practice_first):
    as_user(user)
    calls = [
        lambda: client.post("/api/sap/learning/complete-practice", json=practice_payload(1)),
        lambda: client.post("/api/sap/learning/complete-lesson", json={"day_number": 1}),
    ]
    for call in (calls if practice_first else reversed(calls)):
        assert call().status_code == 200
    progress = client.get("/api/sap/learning/progress").json()
    assert progress["day_states"]["1"]["completed"] is False
    assert progress["day_states"]["2"]["unlocked"] is False

    res = client.post("/api/sap/assessments/submit", json={
        "day_number": 1, "assessment_id": "d1_s6_assessment", "assessment_type": "mcq",
        "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
    })
    assert res.status_code == 200 and res.json()["passed"] is True
    progress = client.get("/api/sap/learning/progress").json()
    assert progress["day_states"]["1"]["completed"] is True
    assert progress["day_states"]["2"]["unlocked"] is True


def test_lesson_api_hides_graded_practice_answer_keys(db, user, as_user):
    for d in range(1, 100):
        complete_day(db, user.id, d)
    as_user(user)
    for day in range(1, 101):
        res = client.get(f"/api/sap/learning/lessons/{day}")
        assert res.status_code == 200, res.text
        graded_ids = {s["step_id"] for s in practice_evidence_steps(day)}
        flagged = {s["step_id"] for s in res.json()["steps"] if s.get("practice_evidence")}
        assert flagged == graded_ids, f"Day {day}"
        for s in res.json()["steps"]:
            if s["step_id"] in graded_ids:
                for opt in s["options"]:
                    leaked = {"is_correct", "correct", "explanation", "consequence"} & opt.keys()
                    assert not leaked, f"Day {day} {s['step_id']} leaks {leaked}"


# =============================================================================
# 2. Mission prerequisites & step integrity
# =============================================================================

def test_locked_mission_start_and_attempt_return_403_with_zero_mutation(db, user, as_user):
    as_user(user)
    before = snapshot(db, user.id)

    res = client.post(f"/api/sap/missions/{LOCKED_MISSION}/start")
    assert res.status_code == 403
    assert "locked" in res.json()["detail"].lower()

    step = mission_steps(LOCKED_MISSION)[0]
    res = attempt_step(LOCKED_MISSION, step["step_id"], mission_step_payload(step))
    assert res.status_code == 403

    listed = {m["slug"]: m for m in client.get("/api/sap/missions").json()}
    assert listed[LOCKED_MISSION]["is_unlocked"] is False
    assert snapshot(db, user.id) == before


def test_unlocked_mission_starts_and_earned_mastery_unlocks_next(db, user, as_user):
    as_user(user)
    res = client.post(f"/api/sap/missions/{ENTRY_MISSION}/start")
    assert res.status_code == 200
    assert res.json()["status"] == "in_progress"

    # Earn the prerequisites legitimately by completing the entry mission
    complete_mission(ENTRY_MISSION)
    listed = {m["slug"]: m for m in client.get("/api/sap/missions").json()}
    assert listed[LOCKED_MISSION]["is_unlocked"] is True

    res = client.post(f"/api/sap/missions/{LOCKED_MISSION}/start")
    assert res.status_code == 200
    assert res.json()["status"] == "in_progress"


def test_invalid_assistance_level_rejected(db, user, as_user):
    as_user(user)
    before = snapshot(db, user.id)
    res = client.post(f"/api/sap/missions/{ENTRY_MISSION}/start?assistance_level=GODMODE")
    assert res.status_code == 400
    assert snapshot(db, user.id) == before


def test_unknown_step_ids_rejected_without_fallback(db, user, as_user):
    as_user(user)
    before = snapshot(db, user.id)
    first = mission_steps(OPTIONS_MISSION)[0]
    good_payload = mission_step_payload(first)  # a correct answer to the FIRST step
    for fake in ["", "step_999", "STEP_1_SIDE_BY_SIDE", f"{first['step_id']} ", "../step_1", "null"]:
        res = attempt_step(OPTIONS_MISSION, fake, good_payload)
        assert res.status_code == 404, fake
    assert snapshot(db, user.id) == before


def test_replaying_first_step_answer_under_fake_ids_cannot_inflate(db, user, as_user):
    as_user(user)
    first = mission_steps(OPTIONS_MISSION)[0]
    res = attempt_step(OPTIONS_MISSION, first["step_id"], mission_step_payload(first))
    assert res.status_code == 200 and res.json()["steps_completed_count"] == 1
    after_first = snapshot(db, user.id)

    for i in range(25):
        res = attempt_step(OPTIONS_MISSION, f"fake_step_{i}", mission_step_payload(first))
        assert res.status_code == 404

    # Other real steps answered with the first step's option id are invalid, not passed
    for step in mission_steps(OPTIONS_MISSION)[1:]:
        res = attempt_step(OPTIONS_MISSION, step["step_id"], mission_step_payload(first))
        assert res.status_code == 400

    assert snapshot(db, user.id) == after_first
    attempt = after_first["attempts"][0]
    assert attempt[2] == pytest.approx(33.3) and attempt[3] is False


def test_incorrect_step_answer_never_counts(db, user, as_user):
    as_user(user)
    before = snapshot(db, user.id)
    for step in mission_steps(ENTRY_MISSION):  # covers option and order_process steps
        res = attempt_step(ENTRY_MISSION, step["step_id"], mission_step_payload(step, correct=False))
        assert res.status_code == 200
        body = res.json()
        assert body["step_success"] is False
        assert body["steps_completed_count"] == 0
        assert body["current_score"] == 0.0
        assert body["mission_completed"] is False
    assert snapshot(db, user.id) == before


@pytest.mark.parametrize("payload", [
    {},
    {"selected_option_id": None},
    {"selected_option_id": 1},
    {"selected_option_id": "opt_that_does_not_exist"},
    {"ordered_items": ["x"]},
])
def test_malformed_step_payload_rejected(db, user, as_user, payload):
    as_user(user)
    before = snapshot(db, user.id)
    step = mission_steps(OPTIONS_MISSION)[0]
    res = attempt_step(OPTIONS_MISSION, step["step_id"], payload)
    assert res.status_code == 400
    assert snapshot(db, user.id) == before


def test_duplicate_valid_step_submission_is_idempotent(db, user, as_user):
    as_user(user)
    first = mission_steps(OPTIONS_MISSION)[0]
    res = attempt_step(OPTIONS_MISSION, first["step_id"], mission_step_payload(first))
    snap = snapshot(db, user.id)
    for _ in range(5):
        res = attempt_step(OPTIONS_MISSION, first["step_id"], mission_step_payload(first))
        assert res.status_code == 200
        assert res.json()["steps_completed_count"] == 1
        assert res.json()["current_score"] == pytest.approx(33.3)
        assert res.json()["mission_completed"] is False
    assert snapshot(db, user.id) == snap


def test_premature_completion_impossible(db, user, as_user):
    as_user(user)
    steps = mission_steps(OPTIONS_MISSION)
    for step in steps[:-1]:
        payload = {**mission_step_payload(step), "mission_completed": True, "score": 100,
                   "steps_completed": [s["step_id"] for s in steps]}
        res = client.post(f"/api/sap/missions/{OPTIONS_MISSION}/attempt", json={
            "step_id": step["step_id"], "payload": payload,
            "mission_completed": True, "current_score": 100, "total_steps": 1,
        })
        assert res.status_code == 200
        assert res.json()["mission_completed"] is False
    snap = snapshot(db, user.id)
    assert snap["evidence"] == 0 and snap["mastery"] == [] and snap["state_events"] == []
    assert snap["attempts"][0][1] == "in_progress" and snap["attempts"][0][3] is False

    # Wrong answer to the last step still does not complete
    res = attempt_step(OPTIONS_MISSION, steps[-1]["step_id"], mission_step_payload(steps[-1], correct=False))
    assert res.json()["mission_completed"] is False
    assert snapshot(db, user.id) == snap


def test_full_completion_side_effects_happen_exactly_once(db, user, as_user):
    as_user(user)
    complete_mission(OPTIONS_MISSION)
    concepts = SAPMissionRegistry.get(OPTIONS_MISSION)["concept_slugs"]
    done = snapshot(db, user.id)
    assert len(done["attempts"]) == 1
    assert done["attempts"][0][1] == "completed" and done["attempts"][0][2] == 100.0
    assert done["evidence"] == len(concepts)
    assert len(done["mastery"]) == len(concepts)

    # Replay every step, restart, and resubmit: no new attempt, evidence, mastery, or events
    complete_mission(OPTIONS_MISSION)
    res = client.post(f"/api/sap/missions/{OPTIONS_MISSION}/start")
    assert res.status_code == 200 and res.json()["status"] == "completed"
    step = mission_steps(OPTIONS_MISSION)[0]
    res = attempt_step(OPTIONS_MISSION, step["step_id"], mission_step_payload(step))
    assert res.json()["mission_completed"] is True
    assert snapshot(db, user.id) == done


# =============================================================================
# 3. Mastery forgery
# =============================================================================

@pytest.mark.parametrize("body", [
    {"concept_slug": "org-structure-plant", "score": 100},
    {"concept_slug": "definitely-not-a-concept", "score": 100},
    {"concept_slug": "org-structure-plant", "score": 100, "mastery_state": "MASTERED", "passed": True},
])
def test_direct_mastery_record_is_not_user_callable(db, user, as_user, body):
    as_user(user)
    before = snapshot(db, user.id)
    res = client.post("/api/sap/mastery/record", json=body)
    assert res.status_code in (404, 405)
    assert snapshot(db, user.id) == before
    assert client.get("/api/sap/mastery").json()["total_tracked"] == 0


def test_no_sap_route_accepts_client_mastery_writes():
    writes = [
        (r.path, sorted(r.methods)) for r in app.routes
        if getattr(r, "path", "").startswith("/api/sap/mastery") and (r.methods or set()) - {"GET", "HEAD"}
    ]
    assert writes == []


@pytest.mark.parametrize("score", [math.nan, math.inf, -1.0, 100.01, 1e9, True])
def test_mastery_service_rejects_invalid_scores(db, user, score):
    with pytest.raises(ValueError):
        SAPMasteryService.record_concept_attempt(db, user.id, "org-structure-plant", score)
    with pytest.raises(ValueError):
        SAPMasteryService.record_skill_evidence(db, user.id, "org-structure-plant", {"score": score})
    assert snapshot(db, user.id)["mastery"] == []


def test_mastery_service_requires_score_and_registered_concept(db, user):
    with pytest.raises(ValueError):
        SAPMasteryService.record_skill_evidence(db, user.id, "org-structure-plant", {"result": "passed"})
    with pytest.raises(ValueError):
        SAPMasteryService.record_concept_attempt(db, user.id, "definitely-not-a-concept", 90.0)
    assert snapshot(db, user.id)["mastery"] == []


def test_legitimate_assessment_evidence_still_creates_mastery(db, user, as_user):
    as_user(user)
    assert client.post("/api/sap/learning/complete-practice", json=practice_payload(1)).json()["passed"]
    res = client.post("/api/sap/assessments/submit", json={
        "day_number": 1, "assessment_id": "d1_s6_assessment", "assessment_type": "mcq",
        "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
    })
    assert res.status_code == 200 and res.json()["passed"] is True
    summary = client.get("/api/sap/mastery").json()
    assert summary["total_tracked"] >= 1
    assert all(c["mastery_score"] > 0 for c in summary["concepts"])


def test_legitimate_mission_evidence_still_creates_mastery(db, user, as_user):
    as_user(user)
    complete_mission(ENTRY_MISSION)
    tracked = {c["concept_slug"] for c in client.get("/api/sap/mastery").json()["concepts"]}
    assert set(SAPMissionRegistry.get(ENTRY_MISSION)["concept_slugs"]) <= tracked
