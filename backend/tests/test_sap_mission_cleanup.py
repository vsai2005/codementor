"""Batch 2 cleanup: mission reachability, answer-key leakage, ordering steps, concurrency.

1. Every prerequisite of every registered mission is a registered concept that a learner
   can actually earn (graded by an assessment, awarded by placement, or awarded by a mission
   that is itself reachable), so no mission is permanently locked.
2. Mission list/detail responses never contain answer keys or evaluator data, at any
   assistance level, and wrong-answer feedback never names the correct option.
3. Ordering steps accept only complete, duplicate-free permutations of their items; the
   entry mission is completable end-to-end through its ordering step.
4. PostgreSQL-backed races: concurrent valid submissions complete a mission exactly once.
"""

from __future__ import annotations

import threading
import uuid
from collections import Counter

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine
from app.data.sap_lessons import SAP_DAYS_CONTENT
from app.database import get_db
from app.main import app
from app.models.models import User
from app.models.sap_models import (
    SAPEnterpriseInstance,
    SAPMissionAttempt,
    SAPSkillEvidence,
    SAPUserConceptMastery,
)
from app.sap.data.placement_questions import EXPERIENCED_QUESTIONS, NOT_SURE_QUESTIONS
from app.sap.services.missions import SAPMissionRegistry, SAPMissionService

client = TestClient(app, raise_server_exceptions=False)

ORDER_MISSION = "nova-org-structure-design"
FORBIDDEN_KEYS = {
    "is_correct", "correct", "correct_order", "correct_option_id", "correct_answer",
    "explanation", "expected_state_patch", "success_criteria", "failure_conditions",
    "target_state_criteria", "initial_state_patch", "scoring_key", "rubric", "evaluator",
    "solution", "answer", "answers", "expected_output",
}


# =============================================================================
# Helpers
# =============================================================================

def assessment_evidence_concepts(day_number: int) -> set[str]:
    """Concepts SAPAssessmentService.evaluate credits for a day (mirrors its rules).

    Question-based assessments credit each question's concept_slug, falling back to the
    step's concept_slug, then the day's first atomic concept. Assessments without
    questions credit only the step's concept_slug.
    """
    lesson = SAP_DAYS_CONTENT[day_number]
    step = next(s for s in lesson["steps"] if s["step_type"] == "assessment")
    root = step.get("concept_slug") or (lesson.get("atomic_concepts") or [f"sap-day-{day_number}"])[0]
    questions = step.get("questions") or []
    if questions:
        return {q.get("concept_slug") or root for q in questions}
    return {step["concept_slug"]} if step.get("concept_slug") else set()


def earnable_concepts_and_reachable_missions() -> tuple[set[str], set[str]]:
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    earnable = set()
    for day in SAP_DAYS_CONTENT:
        earnable |= assessment_evidence_concepts(day)
    earnable |= {q["concept_slug"] for q in EXPERIENCED_QUESTIONS + NOT_SURE_QUESTIONS if q.get("concept_slug")}
    earnable = {c for c in earnable if engine.get_concept(c) is not None}

    reachable: set[str] = set()
    changed = True
    while changed:
        changed = False
        for m in SAPMissionRegistry.get_all():
            if m["slug"] in reachable:
                continue
            if m["difficulty"] <= 1 or all(p in earnable for p in m["prerequisite_concepts"]):
                reachable.add(m["slug"])
                earnable |= set(m["concept_slugs"])
                changed = True
    return earnable, reachable


def find_forbidden(obj, path="$") -> list[str]:
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in FORBIDDEN_KEYS or str(k).startswith("hidden_"):
                hits.append(f"{path}.{k}")
            hits += find_forbidden(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += find_forbidden(v, f"{path}[{i}]")
    return hits


def correct_payload(step: dict) -> dict:
    if step["step_type"] == "order_process":
        return {"ordered_items": list(step["correct_order"])}
    return {"selected_option_id": next(o["id"] for o in step["options"] if o.get("is_correct"))}


def _new_user(db) -> User:
    tag = uuid.uuid4().hex[:8]
    u = User(id=uuid.uuid4(), email=f"sap_cl_{tag}@example.com", username=f"sap_cl_{tag}", name="SAP Cleanup")
    db.add(u)
    db.commit()
    return u


@pytest.fixture
def user(db):
    return _new_user(db)


@pytest.fixture
def as_user(db):
    def _login(u):
        app.dependency_overrides[get_current_user] = lambda: u
        app.dependency_overrides[get_db] = lambda: db
    yield _login
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_db, None)


def user_rows(db, user_id) -> dict:
    db.expire_all()
    attempts = db.execute(select(SAPMissionAttempt).where(SAPMissionAttempt.user_id == user_id)).scalars().all()
    return {
        "attempts": sorted((a.status, a.score, tuple(a.steps_completed or [])) for a in attempts),
        "evidence": db.execute(select(func.count()).select_from(SAPSkillEvidence)
                               .where(SAPSkillEvidence.user_id == user_id)).scalar_one(),
        "mastery": sorted(
            (str(m.concept_id), m.attempts, m.mastery_score)
            for m in db.execute(select(SAPUserConceptMastery)
                                .where(SAPUserConceptMastery.user_id == user_id)).scalars().all()
        ),
    }


# =============================================================================
# 1. Reachability
# =============================================================================

def test_every_mission_concept_is_registered():
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    unresolved = [
        (m["slug"], c)
        for m in SAPMissionRegistry.get_all()
        for c in list(m["prerequisite_concepts"]) + list(m["concept_slugs"])
        if engine.get_concept(c) is None
    ]
    assert unresolved == []


def test_zero_unearnable_prerequisites_and_every_mission_reachable():
    earnable, reachable = earnable_concepts_and_reachable_missions()
    unresolved = [
        (m["slug"], p)
        for m in SAPMissionRegistry.get_all()
        for p in m["prerequisite_concepts"]
        if p not in earnable
    ]
    assert unresolved == []
    assert reachable == SAPMissionRegistry.get_slugs()


@pytest.mark.parametrize("slug", ["nova-p2p-workflow-incident", "nova-e2e-enterprise-cross-module-recovery"])
def test_previously_locked_missions_unlock_with_earned_mastery(db, user, as_user, slug):
    """Seed mastery exactly as graded evidence would, then start succeeds (was permanent 403)."""
    from app.sap.services.mastery import SAPMasteryService
    as_user(user)
    assert client.post(f"/api/sap/missions/{slug}/start").status_code == 403
    for concept in SAPMissionRegistry.get(slug)["prerequisite_concepts"]:
        SAPMasteryService.record_concept_attempt(db, user.id, concept, 100.0)
    res = client.post(f"/api/sap/missions/{slug}/start")
    assert res.status_code == 200, res.text


# =============================================================================
# 2. Answer-key leakage
# =============================================================================

def test_mission_detail_and_list_never_leak_answer_keys(db, user, as_user):
    as_user(user)
    listing = client.get("/api/sap/missions")
    assert listing.status_code == 200
    assert find_forbidden(listing.json()) == []

    for m in SAPMissionRegistry.get_all():
        for level in ("TRAINING", "GUIDED", "JOB"):
            res = client.get(f"/api/sap/missions/{m['slug']}?assistance_level={level}")
            assert res.status_code == 200, res.text
            body = res.json()
            assert find_forbidden(body) == [], (m["slug"], level)
            for view, step in zip(body["steps"], m["steps"]):
                assert set(view) <= {"step_id", "title", "step_type", "instruction", "options", "items"}
                for opt in view.get("options", []):
                    assert set(opt) == {"id", "label"}
                    # no rationale text that would reveal correctness
                    src = next(o for o in step["options"] if o["id"] == opt["id"])
                    if src.get("explanation"):
                        assert src["explanation"] not in res.text
                if step["step_type"] == "order_process":
                    assert sorted(view["items"]) == sorted(step["correct_order"])


def test_ordering_items_are_randomized_not_the_answer(db, user, as_user):
    as_user(user)
    step = next(s for s in SAPMissionRegistry.get(ORDER_MISSION)["steps"] if s["step_type"] == "order_process")
    seen = Counter()
    for _ in range(60):
        view = next(s for s in client.get(f"/api/sap/missions/{ORDER_MISSION}").json()["steps"]
                    if s["step_id"] == step["step_id"])
        seen[tuple(view["items"])] += 1
    # A static order (sorted, authored, or reversed) would repeat every time.
    assert len(seen) > 5
    assert seen[tuple(step["correct_order"])] < 60 * 0.25


def test_wrong_answer_feedback_never_names_the_correct_option(db, user, as_user):
    as_user(user)
    for m in SAPMissionRegistry.get_all():
        if m["difficulty"] > 1:
            continue
        for step in m["steps"]:
            if step["step_type"] == "order_process":
                continue
            correct = next(o for o in step["options"] if o.get("is_correct"))
            wrong = next(o for o in step["options"] if not o.get("is_correct"))
            res = client.post(f"/api/sap/missions/{m['slug']}/attempt",
                              json={"step_id": step["step_id"], "payload": {"selected_option_id": wrong["id"]}})
            assert res.status_code == 200
            assert res.json()["step_success"] is False
            assert correct["label"] not in res.text and correct["id"] not in res.text
            if correct.get("explanation"):
                assert correct["explanation"] not in res.text


# =============================================================================
# 3. Ordering steps
# =============================================================================

def _order_step():
    return next(s for s in SAPMissionRegistry.get(ORDER_MISSION)["steps"] if s["step_type"] == "order_process")


@pytest.mark.parametrize("make_payload", [
    lambda order: {},
    lambda order: {"selected_option_id": "opt_nm01"},
    lambda order: {"ordered_items": "Client (100)"},
    lambda order: {"ordered_items": order[:-1]},                       # incomplete
    lambda order: {"ordered_items": order + [order[0]]},               # extra duplicate
    lambda order: {"ordered_items": [order[0]] + order[:-1]},          # duplicate, missing one
    lambda order: {"ordered_items": order[:-1] + ["Sales Org (S001)"]},  # foreign item
    lambda order: {"ordered_items": [1, 2, 3, 4]},
    lambda order: {"ordered_items": []},
])
def test_malformed_ordering_submissions_fail_closed(db, user, as_user, make_payload):
    as_user(user)
    step = _order_step()
    before = user_rows(db, user.id)
    res = client.post(f"/api/sap/missions/{ORDER_MISSION}/attempt",
                      json={"step_id": step["step_id"], "payload": make_payload(list(step["correct_order"]))})
    assert res.status_code == 400
    assert user_rows(db, user.id) == before


def test_wrong_permutation_is_incorrect_not_malformed(db, user, as_user):
    as_user(user)
    step = _order_step()
    before = user_rows(db, user.id)
    res = client.post(f"/api/sap/missions/{ORDER_MISSION}/attempt",
                      json={"step_id": step["step_id"], "payload": {"ordered_items": list(reversed(step["correct_order"]))}})
    assert res.status_code == 200
    assert res.json()["step_success"] is False
    assert user_rows(db, user.id) == before


def test_entry_mission_completes_through_its_ordering_step(db, user, as_user):
    as_user(user)
    detail = client.get(f"/api/sap/missions/{ORDER_MISSION}").json()
    registered = SAPMissionRegistry.get(ORDER_MISSION)["steps"]
    for view, step in zip(detail["steps"], registered):
        if step["step_type"] == "order_process":
            # A learner reorders the presented items; only the arrangement is submitted.
            rank = {item: i for i, item in enumerate(step["correct_order"])}
            payload = {"ordered_items": sorted(view["items"], key=rank.__getitem__)}
        else:
            payload = correct_payload(step)
        res = client.post(f"/api/sap/missions/{ORDER_MISSION}/attempt",
                          json={"step_id": view["step_id"], "payload": payload})
        assert res.status_code == 200 and res.json()["step_success"] is True, res.text
    assert res.json()["mission_completed"] is True
    assert res.json()["current_score"] == 100.0


# =============================================================================
# 4. PostgreSQL concurrency
# =============================================================================

def _race(engine, fn, n=2):
    """Runs fn(session) in n threads that start together; returns results or exceptions."""
    barrier = threading.Barrier(n)
    results: list = [None] * n

    def worker(i):
        with Session(engine) as s:
            barrier.wait()
            try:
                results[i] = fn(s)
            except Exception as exc:  # surfaced to the assertion below
                s.rollback()
                results[i] = exc

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)
    return results


@pytest.fixture
def committed_user(engine, migrated):
    """A user whose rows are really committed (visible across connections)."""
    with Session(engine) as s:
        u = User(id=uuid.uuid4(), email=f"race_{uuid.uuid4().hex[:8]}@example.com",
                 username=f"race_{uuid.uuid4().hex[:8]}", name="Race")
        s.add(u)
        s.commit()
        uid = u.id
    yield uid
    with Session(engine) as s:
        s.execute(delete(User).where(User.id == uid))  # FKs cascade
        s.commit()


def _completion_snapshot(engine, user_id, mission_slug):
    concepts = SAPMissionRegistry.get(mission_slug)["concept_slugs"]
    with Session(engine) as s:
        attempts = s.execute(select(SAPMissionAttempt).where(SAPMissionAttempt.user_id == user_id)).scalars().all()
        evidence = s.execute(select(SAPSkillEvidence).where(SAPSkillEvidence.user_id == user_id)).scalars().all()
        mastery = s.execute(select(SAPUserConceptMastery).where(SAPUserConceptMastery.user_id == user_id)).scalars().all()
        instances = s.execute(select(SAPEnterpriseInstance).where(SAPEnterpriseInstance.user_id == user_id)).scalars().all()
        return {
            "concepts": concepts,
            "attempts": [(a.status, a.score, a.passed, list(a.steps_completed)) for a in attempts],
            "evidence": len(evidence),
            "mastery_attempts": sorted(m.attempts for m in mastery),
            "mutations": sum(
                1 for i in instances for e in (i.audit_log or [])
                if e.get("action") == f"MISSION_COMPLETED_{mission_slug}"
            ),
        }


@pytest.mark.parametrize("round_", range(3))
def test_concurrent_final_step_submissions_complete_exactly_once(engine, committed_user, round_):
    slug = ORDER_MISSION
    steps = SAPMissionRegistry.get(slug)["steps"]
    with Session(engine) as s:
        for step in steps[:-1]:
            SAPMissionService.submit_step_attempt(s, committed_user, slug, step["step_id"], correct_payload(step))

    final = steps[-1]
    results = _race(engine, lambda s: SAPMissionService.submit_step_attempt(
        s, committed_user, slug, final["step_id"], correct_payload(final)))

    assert not [r for r in results if isinstance(r, Exception)], results
    assert all(r["step_success"] and r["mission_completed"] for r in results)
    assert all(r["current_score"] == 100.0 for r in results)

    snap = _completion_snapshot(engine, committed_user, slug)
    assert snap["attempts"] == [("completed", 100.0, True, [s["step_id"] for s in steps])]
    assert snap["evidence"] == len(snap["concepts"])
    assert snap["mastery_attempts"] == [1] * len(snap["concepts"])
    assert snap["mutations"] == 1


def test_concurrent_first_submissions_create_one_attempt(engine, committed_user, monkeypatch):
    # Widen the check-then-create window so an unserialized implementation reliably races.
    import time
    original = SAPMissionService._find_latest_attempt

    def slow_find(db, user_id, mission_id):
        found = original(db, user_id, mission_id)
        time.sleep(0.3)
        return found

    monkeypatch.setattr(SAPMissionService, "_find_latest_attempt", staticmethod(slow_find))
    slug = "nova-sap-product-selection"
    first = SAPMissionRegistry.get(slug)["steps"][0]
    results = _race(engine, lambda s: SAPMissionService.submit_step_attempt(
        s, committed_user, slug, first["step_id"], correct_payload(first)), n=4)
    assert not [r for r in results if isinstance(r, Exception)], results
    assert all(r["steps_completed_count"] == 1 for r in results)
    snap = _completion_snapshot(engine, committed_user, slug)
    assert snap["attempts"] == [("in_progress", 33.3, False, [first["step_id"]])]
    assert snap["evidence"] == 0
