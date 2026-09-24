"""Adversarial and Security Verification Suite for SAP Batch 2.

Covers:
1. Waived-day consistency:
   - Direct lesson API access on waived day returns 403.
   - complete-lesson on waived day returns 400 with zero mutation.
   - complete-practice on waived day returns 400 with zero mutation.
   - assessment submit on waived day returns 403.
   - Waived vs completed vs current vs locked 5-state integrity.
2. Server-side assessment identity binding:
   - Arbitrary/forged assessment_id rejected with 400.
   - Cross-day assessment_id reuse rejected with 400.
   - Mismatched assessment_type rejected with 400.
   - Client rubric tampering ignored and evaluation strictly bound to authored day.
3. Execution API (/api/sap/execution/validate) security:
   - Anonymous requests rejected with 401.
   - Authenticated legitimate requests succeed with 200 and truthfulness metadata.
   - Oversized code payload (>64 KB) rejected with 413.
   - Oversized context parameters (>16 KB) rejected with 413.
   - User-aware rate-limit exhaustion returns 429 with Retry-After header.
   - Per-user rate-limit isolation (User A exhaustion does not block User B).
"""

from __future__ import annotations

import json
import uuid
import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_current_user
from app.database import get_db
from app.main import app
from app.models.models import User
from app.models.sap_models import (
    SAPAssessment,
    SAPAssessmentAttempt,
    SAPDayStatus,
    SAPPlacementProfile,
    SAPSkillEvidence,
    SAPUserDayState,
)
from app.sap.services.progression import SAPProgressionService
from app.services.ratelimit import InMemoryRateLimiter, get_sap_execution_rate_limiter


client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def test_user(db):
    user = User(
        id=uuid.uuid4(),
        email=f"sap_b2_{uuid.uuid4().hex[:8]}@example.com",
        username=f"sap_b2_{uuid.uuid4().hex[:8]}",
        name="SAP B2 Tester",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def second_user(db):
    user = User(
        id=uuid.uuid4(),
        email=f"sap_b2_sec_{uuid.uuid4().hex[:8]}@example.com",
        username=f"sap_b2_sec_{uuid.uuid4().hex[:8]}",
        name="SAP B2 Sec Tester",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def override_auth(user, session):
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_db] = lambda: session


def clear_auth():
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_db, None)


# =============================================================================
# 1. Waived-Day Consistency & Gating Tests
# =============================================================================

def test_waived_day_lesson_api_returns_403(test_user, db):
    """Direct GET /api/sap/learning/lessons/{day} for waived days must return 403."""
    override_auth(test_user, db)
    try:
        # Place user at Day 9 (Days 1–8 waived)
        beginner_answers = {
            "ns_fund_01": "b", "ns_org_02": "b", "ns_data_03": "a",
            "ns_p2p_04": "b", "ns_hana_05": "a", "ns_fiori_06": "b",
        }
        res = client.post("/api/sap/placement/submit", json={"experience_level": "not_sure", "answers": beginner_answers})
        assert res.status_code == 200
        assert res.json()["recommended_start_day"] == 9
        assert res.json()["waived_days"] == list(range(1, 9))

        # Check all waived days 1..8 return 403
        for waived_day in range(1, 9):
            resp = client.get(f"/api/sap/learning/lessons/{waived_day}")
            assert resp.status_code == 403
            assert "waived" in resp.json()["detail"].lower()

        # Day 9 (active) returns 200 with lesson content
        day9_resp = client.get("/api/sap/learning/lessons/9")
        assert day9_resp.status_code == 200
        assert day9_resp.json()["day_number"] == 9

        # Day 10 (locked) returns 403 with locked detail
        day10_resp = client.get("/api/sap/learning/lessons/10")
        assert day10_resp.status_code == 403
        assert "locked" in day10_resp.json()["detail"].lower()
    finally:
        clear_auth()


def test_waived_day_progression_mutation_blocked(test_user, db):
    """Attempting complete-lesson or complete-practice on waived day returns 400 with zero state change."""
    override_auth(test_user, db)
    try:
        beginner_answers = {
            "ns_fund_01": "b", "ns_org_02": "b", "ns_data_03": "a",
            "ns_p2p_04": "b", "ns_hana_05": "a", "ns_fiori_06": "b",
        }
        client.post("/api/sap/placement/submit", json={"experience_level": "not_sure", "answers": beginner_answers})

        # 1. complete-lesson on waived Day 1
        res_lesson = client.post("/api/sap/learning/complete-lesson", json={"day_number": 1})
        assert res_lesson.status_code == 400
        assert "waived" in res_lesson.json()["detail"].lower()

        # 2. complete-practice on waived Day 1
        res_practice = client.post("/api/sap/learning/complete-practice", json={"day_number": 1})
        assert res_practice.status_code == 400
        assert "waived" in res_practice.json()["detail"].lower()

        # 3. assessment submit on waived Day 1
        res_assess = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 1,
                "assessment_id": "d1_s6_assessment",
                "assessment_type": "mcq",
                "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
            },
        )
        assert res_assess.status_code == 403
        assert "waived" in res_assess.json()["detail"].lower()

        # Verify progression state remained unchanged: Day 1 still waived, completed_days empty
        prog = SAPProgressionService.compute_user_progress(db, test_user.id)
        assert prog["completed_days"] == []
        assert prog["current_day"] == 9
        assert prog["day_states"]["1"]["status"] == "waived_by_placement"
        assert prog["day_states"]["1"]["completed"] is False
    finally:
        clear_auth()


def test_waived_vs_completed_state_lifecycle(test_user, db):
    """Waived days remain waived; active days can be completed and reviewed cleanly."""
    override_auth(test_user, db)
    try:
        # Start at Day 1 (no waivers)
        fresher_res = client.post("/api/sap/placement/submit", json={"experience_level": "not_sure", "answers": {}})
        assert fresher_res.json()["recommended_start_day"] == 1

        # Day 1 is available
        prog_init = SAPProgressionService.compute_user_progress(db, test_user.id)
        assert prog_init["day_states"]["1"]["status"] in ("available", "current")
        assert prog_init["day_states"]["1"]["completed"] is False

        # Complete practice & lesson for Day 1
        client.post("/api/sap/learning/complete-practice", json={"day_number": 1})
        client.post("/api/sap/learning/complete-lesson", json={"day_number": 1})

        # Submit passing assessment for Day 1
        pass_res = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 1,
                "assessment_id": "d1_s6_assessment",
                "assessment_type": "mcq",
                "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
            },
        )
        assert pass_res.status_code == 200
        assert pass_res.json()["day_completed"] is True

        # Day 1 is now authoritatively completed and reviewable
        prog_after = SAPProgressionService.compute_user_progress(db, test_user.id)
        assert 1 in prog_after["completed_days"]
        assert prog_after["day_states"]["1"]["status"] == "completed"
        assert prog_after["day_states"]["1"]["completed"] is True

        # Lesson for completed Day 1 is accessible for review (200 OK)
        rev_resp = client.get("/api/sap/learning/lessons/1")
        assert rev_resp.status_code == 200
    finally:
        clear_auth()


# =============================================================================
# 2. Server-Bound Assessment Identity Tests
# =============================================================================

def test_tightened_assessment_identity_adversarial(test_user, db):
    """Tightened assessment identity rejects d1_fake, day-1-anything, other day's valid ID,

    and missing ID with 400 and zero DB mutation, while accepting the exact canonical ID.
    """
    override_auth(test_user, db)
    try:
        # Complete practice first to satisfy Day 1 practice gating
        p_res = client.post("/api/sap/learning/complete-practice", json={"day_number": 1})
        assert p_res.status_code == 200

        # Snapshot DB state before invalid submissions
        initial_attempts = db.query(SAPAssessmentAttempt).filter_by(user_id=test_user.id).count()
        initial_evidence = db.query(SAPSkillEvidence).filter_by(user_id=test_user.id).count()
        day1_state_before = db.query(SAPUserDayState).filter_by(user_id=test_user.id, day_number=1).first()
        assert initial_attempts == 0
        assert initial_evidence == 0
        assert day1_state_before is not None
        assert day1_state_before.completed is False
        assert day1_state_before.assessment_passed is not True

        valid_answers = {"answers": {"q1": "q1_a", "q2": "q2_a"}}

        # 1. Test vector: "d1_fake"
        res_d1_fake = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 1,
                "assessment_id": "d1_fake",
                "assessment_type": "mcq",
                "submission_payload": valid_answers,
            },
        )
        assert res_d1_fake.status_code == 400
        assert "assessment id mismatch" in res_d1_fake.json()["detail"].lower()

        # 2. Test vector: "day-1-anything"
        res_day1_anything = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 1,
                "assessment_id": "day-1-anything",
                "assessment_type": "mcq",
                "submission_payload": valid_answers,
            },
        )
        assert res_day1_anything.status_code == 400
        assert "assessment id mismatch" in res_day1_anything.json()["detail"].lower()

        # 3. Test vector: another day's valid ID ("d2_s6_assessment" submitted for Day 1)
        res_other_day = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 1,
                "assessment_id": "d2_s6_assessment",
                "assessment_type": "mcq",
                "submission_payload": valid_answers,
            },
        )
        assert res_other_day.status_code == 400
        assert "assessment id mismatch" in res_other_day.json()["detail"].lower()

        # 4. Test vectors: missing ID (empty string, whitespace, None, and omitted)
        missing_cases = [
            {"assessment_id": ""},
            {"assessment_id": "   "},
            {"assessment_id": None},
            {},  # omitted completely
        ]
        for missing_payload in missing_cases:
            payload = {
                "day_number": 1,
                "assessment_type": "mcq",
                "submission_payload": valid_answers,
                **missing_payload,
            }
            res_missing = client.post("/api/sap/assessments/submit", json=payload)
            assert res_missing.status_code == 400, f"Expected 400 for payload {missing_payload}, got {res_missing.status_code}: {res_missing.text}"
            assert "assessment id mismatch" in res_missing.json()["detail"].lower()

        # Verify ZERO DB / Evidence mutation after all failed mismatch attempts
        db.expire_all()
        assert db.query(SAPAssessmentAttempt).filter_by(user_id=test_user.id).count() == 0
        assert db.query(SAPSkillEvidence).filter_by(user_id=test_user.id).count() == 0
        day1_state_check = db.query(SAPUserDayState).filter_by(user_id=test_user.id, day_number=1).first()
        assert day1_state_check.completed is False
        assert day1_state_check.assessment_passed is not True

        # 5. Test vector: exact canonical ID ("d1_s6_assessment")
        res_canonical = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 1,
                "assessment_id": "d1_s6_assessment",
                "assessment_type": "mcq",
                "submission_payload": valid_answers,
            },
        )
        assert res_canonical.status_code == 200
        canon_data = res_canonical.json()
        assert canon_data["passed"] is True

        # Verify DB / Evidence DID mutate for valid submission
        db.expire_all()
        assert db.query(SAPAssessmentAttempt).filter_by(user_id=test_user.id).count() == 1
        assert db.query(SAPSkillEvidence).filter_by(user_id=test_user.id).count() >= 1
        day1_state_after = db.query(SAPUserDayState).filter_by(user_id=test_user.id, day_number=1).first()
        assert day1_state_after.assessment_passed is True
    finally:
        clear_auth()


def test_cross_day_assessment_reuse_rejected(test_user, db):
    """Submitting Day 2 with Day 1's assessment ID (or vice versa) is strictly rejected."""
    override_auth(test_user, db)
    try:
        # User advances to Day 2
        client.post("/api/sap/learning/complete-practice", json={"day_number": 1})
        client.post("/api/sap/learning/complete-lesson", json={"day_number": 1})
        client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 1,
                "assessment_id": "d1_s6_assessment",
                "assessment_type": "mcq",
                "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
            },
        )
        client.post("/api/sap/learning/complete-practice", json={"day_number": 2})

        # Attempt to submit Day 2 using Day 1's assessment ID
        bad_cross_day = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 2,
                "assessment_id": "d1_s6_assessment",  # Reused from Day 1!
                "assessment_type": "mcq",
                "submission_payload": {"answers": {"q1": "a", "q2": "a"}},
            },
        )
        assert bad_cross_day.status_code == 400
        assert "assessment id mismatch" in bad_cross_day.json()["detail"].lower()

        # Attempt to submit Day 1 using Day 2's assessment ID
        bad_cross_day_2 = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 1,
                "assessment_id": "d2_s6_assessment",  # Reused from Day 2!
                "assessment_type": "mcq",
                "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
            },
        )
        assert bad_cross_day_2.status_code == 400
        assert "assessment id mismatch" in bad_cross_day_2.json()["detail"].lower()
    finally:
        clear_auth()


def test_forged_assessment_type_rejected(test_user, db):
    """Submitting an assessment with an incompatible or forged assessment_type returns 400."""
    override_auth(test_user, db)
    try:
        client.post("/api/sap/learning/complete-practice", json={"day_number": 1})

        for invalid_type in ("rap_challenge", "abap_challenge", "simulation", "exploit_type"):
            resp = client.post(
                "/api/sap/assessments/submit",
                json={
                    "day_number": 1,
                    "assessment_id": "d1_s6_assessment",
                    "assessment_type": invalid_type,
                    "submission_payload": {"answers": {"q1": "q1_a", "q2": "q2_a"}},
                },
            )
            # Either 400 (type mismatch) or 422 (not in enum) is acceptable security rejection
            assert resp.status_code in (400, 422)
            if resp.status_code == 400:
                assert "assessment type mismatch" in resp.json()["detail"].lower()
    finally:
        clear_auth()


def test_client_rubric_tampering_ignored(test_user, db):
    """Client cannot tamper with pass_score or inject questions; evaluation binds strictly to server questions."""
    override_auth(test_user, db)
    try:
        client.post("/api/sap/learning/complete-practice", json={"day_number": 1})

        # Client attempts to inject a pass_score of 0.0 and a fake single question
        tampered_payload = {
            "day_number": 1,
            "assessment_id": "d1_s6_assessment",
            "assessment_type": "mcq",
            "rubric_spec": {
                "pass_score": 0.0,
                "questions": [{"id": "injected_q", "options": [{"id": "opt_x", "is_correct": True}]}],
            },
            "submission_payload": {
                "answers": {"injected_q": "opt_x"},  # Missing real questions q1 and q2!
            },
        }
        res = client.post("/api/sap/assessments/submit", json=tampered_payload)
        assert res.status_code == 200
        data = res.json()
        # Must fail because real server questions q1 and q2 were not answered correctly
        assert data["passed"] is False
        assert data["score"] == 0.0
        assert data["day_completed"] is False

        # Verify DB assessment entity was created with server-defined pass_score (70), not 0
        db_assess = db.query(SAPAssessment).filter_by(day_number=1, slug="d1_s6_assessment").first()
        assert db_assess is not None
        assert db_assess.pass_score == 70
    finally:
        clear_auth()


# =============================================================================
# 3. Execution API (/api/sap/execution/validate) Security Tests
# =============================================================================

def test_anonymous_execution_validate_returns_401():
    """Calling /api/sap/execution/validate without authentication MUST return 401."""
    clear_auth()
    resp = client.post(
        "/api/sap/execution/validate",
        json={
            "provider_type": "abap_cloud",
            "code_or_payload": "DATA: x TYPE i.",
            "context_parameters": {},
        },
    )
    assert resp.status_code == 401


def test_authenticated_execution_validate_succeeds(test_user, db):
    """Authenticated request with valid code returns 200 and truthful simulation metadata."""
    override_auth(test_user, db)
    try:
        resp = client.post(
            "/api/sap/execution/validate",
            json={
                "provider_type": "abap_cloud",
                "code_or_payload": "DATA: lv_count TYPE i VALUE 1.",
                "context_parameters": {},
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["provider_category"] == "STATIC_VALIDATION"
        assert data["is_live_sap_system"] is False
        assert data["is_sandboxed_simulation"] is False
    finally:
        clear_auth()


def test_oversized_code_payload_returns_413(test_user, db):
    """Submitting code payload exceeding 64 KB must return 413 Payload Too Large."""
    override_auth(test_user, db)
    try:
        oversized_code = "DATA: x TYPE i. " * 5000  # ~80 KB > 64 KB
        resp = client.post(
            "/api/sap/execution/validate",
            json={
                "provider_type": "abap_cloud",
                "code_or_payload": oversized_code,
                "context_parameters": {},
            },
        )
        assert resp.status_code == 413
        assert "exceeds maximum permitted code size" in resp.json()["detail"].lower()
    finally:
        clear_auth()


def test_oversized_context_parameters_returns_413(test_user, db):
    """Submitting context_parameters exceeding 16 KB must return 413."""
    override_auth(test_user, db)
    try:
        oversized_params = {"data": "X" * (20 * 1024)}  # 20 KB > 16 KB
        resp = client.post(
            "/api/sap/execution/validate",
            json={
                "provider_type": "simulation",
                "code_or_payload": '{"step": 1}',
                "context_parameters": oversized_params,
            },
        )
        assert resp.status_code == 413
        assert "exceed maximum permitted size" in resp.json()["detail"].lower()
    finally:
        clear_auth()


def test_execution_rate_limit_exhaustion_and_per_user_isolation(test_user, second_user, db):
    """Rate limit exhausts at configured boundary and is strictly isolated per user."""
    from app.services import ratelimit

    # Configure a tiny in-memory rate limiter for this test: 3 requests per 60 seconds
    test_limiter = InMemoryRateLimiter(limit=3, window_s=60)
    original_limiter = ratelimit._sap_execution_limiter
    ratelimit._sap_execution_limiter = test_limiter

    try:
        # 1. User 1 sends 3 successful requests
        override_auth(test_user, db)
        for i in range(3):
            r = client.post(
                "/api/sap/execution/validate",
                json={"provider_type": "abap_cloud", "code_or_payload": f"DATA: val{i} TYPE i."},
            )
            assert r.status_code == 200

        # 4th request from User 1 MUST be rate-limited (429)
        r_blocked = client.post(
            "/api/sap/execution/validate",
            json={"provider_type": "abap_cloud", "code_or_payload": "DATA: val_blocked TYPE i."},
        )
        assert r_blocked.status_code == 429
        assert "rate limit exceeded" in r_blocked.json()["detail"].lower()
        assert "retry-after" in r_blocked.headers

        # 2. Per-user isolation: User 2 is NOT affected by User 1's rate limit exhaustion
        override_auth(second_user, db)
        r_user2 = client.post(
            "/api/sap/execution/validate",
            json={"provider_type": "abap_cloud", "code_or_payload": "DATA: val_user2 TYPE i."},
        )
        assert r_user2.status_code == 200
        assert r_user2.json()["provider_category"] == "STATIC_VALIDATION"
    finally:
        ratelimit._sap_execution_limiter = original_limiter
        clear_auth()
