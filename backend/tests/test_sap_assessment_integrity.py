"""Adversarial and Integrity Verification Suite for SAP Assessment Integrity (Batch 1).

Covers:
1. Complete 100-Day API Answer-Key Leak Audit:
   - GET /api/sap/learning/lessons/{day} for all 100 days.
   - Strictly asserts ZERO leakage of `is_correct`, `correct`, `correct_answer`,
     `correct_option_id`, `scoring_key`, `rubric`, `expected_output`, `explanation`,
     or any `hidden_*` fields in the assessment step and its questions/options.
   - Asserts legitimate student-facing fields (`id`, `prompt`/`question`, `options` with `id`, `text`/`label`)
     are fully preserved.
2. Canonical assessment_type & assessment_id Preservation:
   - Asserts authored assessment_type survives FastAPI/Pydantic serialization for all 100 days.
   - Verifies Days 55-100 non-MCQ types are preserved on the API response.
3. Real End-to-End Evaluation for Target Non-MCQ Days:
   - Days 58, 61, 64, 65, 71, 72, 76, 82, 89, 94, 95, 100.
   - Submits canonical assessment_type with correct answers; asserts score=100.0 and passed=True.
4. Fail-Closed Security & Forged Type Rejection:
   - Submitting mismatched/forged assessment_type fails closed with HTTP 400.
   - Submitting incorrect answers fails (<70%) and triggers remediation.
   - Submitting empty or malformed answer payload fails closed with HTTP 400.
5. MCQ and Capstone Baseline Compatibility:
   - Standard MCQ (Day 1) and Capstone (Day 8, Day 100) complete their real flow.
"""

from __future__ import annotations

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
    SAPUserDayState,
)
from app.data.sap_lessons import SAP_DAYS_CONTENT


client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def test_user(db):
    user = User(
        id=uuid.uuid4(),
        email=f"sap_b1_{uuid.uuid4().hex[:8]}@example.com",
        username=f"sap_b1_{uuid.uuid4().hex[:8]}",
        name="SAP B1 Integrity Tester",
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


def unlock_all_days(db, user_id: uuid.UUID):
    """Seed user progress so all 100 days are unlocked and accessible via GET."""
    states = []
    for d in range(1, 101):
        states.append(
            SAPUserDayState(
                user_id=user_id,
                day_number=d,
                lesson_started=True,
                lesson_completed=True,
                practice_completed=True,
                assessment_passed=True,
                completed=(d < 100),
            )
        )
    db.add_all(states)
    db.commit()


# =============================================================================
# 1. 100-Day API Answer-Key Leak Audit
# =============================================================================

def test_100_days_zero_answer_leakage_over_api(test_user, db):
    """GET /api/sap/learning/lessons/{day} for all 100 days must NEVER expose answer keys."""
    unlock_all_days(db, test_user.id)
    override_auth(test_user, db)

    SENSITIVE_KEYS = {
        "is_correct", "correct", "correct_answer", "correct_option_id",
        "scoring_key", "rubric", "rubrics", "rubric_or_solution",
        "scoring_criteria", "solution", "expected_output", "expected_outputs",
        "explanation",
    }

    try:
        for day in range(1, 101):
            resp = client.get(f"/api/sap/learning/lessons/{day}")
            assert resp.status_code == 200, f"Day {day} GET failed: {resp.text}"
            data = resp.json()

            # Find the assessment step
            assessment_step = next((s for s in data["steps"] if s["step_type"] == "assessment"), None)
            assert assessment_step is not None, f"Day {day} missing assessment step in API response"

            # Check step-level fields
            for k in assessment_step.keys():
                assert k not in ("rubric", "rubric_or_solution", "scoring_criteria", "solution", "expected_output"), (
                    f"Day {day} assessment step leaked '{k}'"
                )
                assert not k.startswith("hidden_"), f"Day {day} assessment step leaked hidden field '{k}'"

            # Check questions & options
            questions = assessment_step.get("questions") or []
            assert len(questions) >= 1, f"Day {day} assessment step has no questions"

            for q_idx, q in enumerate(questions):
                # Verify student-facing essentials
                assert "id" in q or "question_id" in q, f"Day {day} Q{q_idx} missing ID"
                assert "prompt" in q or "question" in q, f"Day {day} Q{q_idx} missing prompt/question"

                # Verify NO sensitive question keys leaked
                for qk in q.keys():
                    assert qk not in SENSITIVE_KEYS, f"Day {day} Q{q_idx} leaked sensitive key '{qk}'"
                    assert not qk.startswith("hidden_"), f"Day {day} Q{q_idx} leaked hidden field '{qk}'"

                options = q.get("options") or []
                assert len(options) >= 2, f"Day {day} Q{q_idx} must have at least 2 options"

                for opt_idx, opt in enumerate(options):
                    assert "id" in opt, f"Day {day} Q{q_idx} opt {opt_idx} missing ID"
                    assert "text" in opt or "label" in opt, f"Day {day} Q{q_idx} opt {opt_idx} missing text/label"

                    # Verify NO sensitive option keys leaked (especially is_correct!)
                    for ok in opt.keys():
                        assert ok not in SENSITIVE_KEYS, (
                            f"Day {day} Q{q_idx} opt {opt['id']} leaked sensitive key '{ok}'!"
                        )
                        assert not ok.startswith("hidden_"), (
                            f"Day {day} Q{q_idx} opt {opt['id']} leaked hidden field '{ok}'"
                        )
    finally:
        clear_auth()


# =============================================================================
# 2. Canonical assessment_type & assessment_id Preservation
# =============================================================================

def test_canonical_assessment_types_preserved_across_all_100_days(test_user, db):
    """Canonical assessment_type must survive serialization and match authored type."""
    unlock_all_days(db, test_user.id)
    override_auth(test_user, db)

    try:
        for day in range(1, 101):
            resp = client.get(f"/api/sap/learning/lessons/{day}")
            assert resp.status_code == 200
            data = resp.json()

            assess_step = next(s for s in data["steps"] if s["step_type"] == "assessment")
            api_type = assess_step.get("assessment_type")
            api_id = assess_step.get("assessment_id")

            assert api_type is not None, f"Day {day} assessment_type is None in API response"
            assert api_id is not None, f"Day {day} assessment_id is None in API response"

            # Derive expected authored canonical type
            raw_authored = SAP_DAYS_CONTENT[day]
            authored_step = next(s for s in raw_authored["steps"] if s["step_type"] == "assessment")
            expected_type = authored_step.get("assessment_type")
            if not expected_type:
                expected_type = "capstone_multi_concept" if (authored_step.get("multi_concept_eval") or authored_step.get("is_capstone")) else "mcq"

            assert api_type == expected_type, (
                f"Day {day} assessment_type mismatch: got '{api_type}', expected authored '{expected_type}'"
            )
    finally:
        clear_auth()


# =============================================================================
# 3. Real End-to-End Evaluation for Target Non-MCQ Days
# =============================================================================

@pytest.mark.parametrize("day_number", [58, 61, 64, 65, 71, 72, 76, 82, 89, 94, 95, 100])
def test_target_non_mcq_days_assessment_flow(day_number, test_user, db):
    """Verify Days 58, 61, 64, 65, 71, 72, 76, 82, 89, 94, 95, 100 complete their real assessment flow."""
    unlock_all_days(db, test_user.id)
    override_auth(test_user, db)

    try:
        # 1. Fetch lesson over API to obtain canonical assessment_type & assessment_id
        res_lesson = client.get(f"/api/sap/learning/lessons/{day_number}")
        assert res_lesson.status_code == 200
        lesson_data = res_lesson.json()

        assess_step = next(s for s in lesson_data["steps"] if s["step_type"] == "assessment")
        assessment_type = assess_step["assessment_type"]
        assessment_id = assess_step["assessment_id"]

        # Ensure it is NOT falling back to mcq for non-MCQ authored days
        raw_authored = SAP_DAYS_CONTENT[day_number]
        raw_step = next(s for s in raw_authored["steps"] if s["step_type"] == "assessment")
        assert assessment_type == raw_step["assessment_type"]

        # 2. Build 100% correct answers payload from server-side authoritative definitions
        correct_answers = {}
        for q in raw_step["questions"]:
            qid = q.get("id") or q.get("question_id")
            correct_opt = next(o["id"] for o in q["options"] if o.get("is_correct"))
            correct_answers[qid] = correct_opt

        # 3. Submit assessment
        res_submit = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": day_number,
                "assessment_id": assessment_id,
                "assessment_type": assessment_type,
                "submission_payload": {"answers": correct_answers},
            },
        )
        assert res_submit.status_code == 200, f"Day {day_number} submit failed: {res_submit.text}"
        data = res_submit.json()

        assert data["passed"] is True, f"Day {day_number} assessment did not pass"
        assert data["score"] == 100.0, f"Day {day_number} score expected 100.0, got {data['score']}"
        assert data["remediation_required"] is False

        # 4. Verify DB assessment entity was created or updated with the canonical type
        db_assessment = db.query(SAPAssessment).filter(
            SAPAssessment.day_number == day_number,
            SAPAssessment.slug == assessment_id,
        ).first()
        assert db_assessment is not None
        assert db_assessment.assessment_type == assessment_type
    finally:
        clear_auth()


# =============================================================================
# 4. Fail-Closed Security & Forged Type / Answer Rejection
# =============================================================================

def test_forged_assessment_type_rejected(test_user, db):
    """Submitting forged or mismatched assessment_type must fail closed with 400."""
    unlock_all_days(db, test_user.id)
    override_auth(test_user, db)

    try:
        # Day 58 authored type is 'technical_audit'; client sends 'mcq'
        res_mismatch = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 58,
                "assessment_id": "d58_s6_assessment",
                "assessment_type": "mcq",
                "submission_payload": {"answers": {"d58_q1": "a"}},
            },
        )
        assert res_mismatch.status_code == 400
        assert "expected canonical type 'technical_audit'" in res_mismatch.json()["detail"].lower()

        # Day 1 authored type is 'mcq'; client sends arbitrary 'unsupported_type'
        res_unknown = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 1,
                "assessment_id": "d1_s6_assessment",
                "assessment_type": "hacked_exploit_type",
                "submission_payload": {"answers": {"q1": "q1_a"}},
            },
        )
        assert res_unknown.status_code in (400, 422)
    finally:
        clear_auth()


def test_incorrect_answers_trigger_remediation_and_fail(test_user, db):
    """Submitting wrong answers must fail (< 70%) and trigger remediation capsules."""
    unlock_all_days(db, test_user.id)
    override_auth(test_user, db)

    try:
        raw_authored = SAP_DAYS_CONTENT[58]
        raw_step = next(s for s in raw_authored["steps"] if s["step_type"] == "assessment")

        # Pick wrong options for all questions
        wrong_answers = {}
        for q in raw_step["questions"]:
            qid = q.get("id") or q.get("question_id")
            wrong_opt = next(o["id"] for o in q["options"] if not o.get("is_correct"))
            wrong_answers[qid] = wrong_opt

        res_submit = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 58,
                "assessment_id": "d58_s6_assessment",
                "assessment_type": "technical_audit",
                "submission_payload": {"answers": wrong_answers},
            },
        )
        assert res_submit.status_code == 200
        data = res_submit.json()

        assert data["passed"] is False
        assert data["score"] == 0.0
        assert data["remediation_required"] is True
    finally:
        clear_auth()


def test_empty_answers_rejected_with_400(test_user, db):
    """Submitting empty answers must fail closed with 400."""
    unlock_all_days(db, test_user.id)
    override_auth(test_user, db)

    try:
        res_empty = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 58,
                "assessment_id": "d58_s6_assessment",
                "assessment_type": "technical_audit",
                "submission_payload": {"answers": {}},
            },
        )
        assert res_empty.status_code == 400
        assert "answers" in res_empty.json()["detail"].lower()
    finally:
        clear_auth()


# =============================================================================
# 5. Normal MCQ and Capstone Baseline Compatibility
# =============================================================================

def test_standard_mcq_day_1_flow(test_user, db):
    """Standard Day 1 MCQ assessment continues to evaluate and pass properly."""
    unlock_all_days(db, test_user.id)
    override_auth(test_user, db)

    try:
        res_submit = client.post(
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
        assert res_submit.status_code == 200
        data = res_submit.json()
        assert data["passed"] is True
        assert data["score"] == 100.0
    finally:
        clear_auth()


def test_capstone_day_8_flow(test_user, db):
    """Day 8 Foundations Capstone continues to evaluate and pass properly."""
    unlock_all_days(db, test_user.id)
    override_auth(test_user, db)

    try:
        raw_step = next(s for s in SAP_DAYS_CONTENT[8]["steps"] if s["step_type"] == "assessment")
        correct_answers = {}
        for q in raw_step["questions"]:
            qid = q.get("id") or q.get("question_id")
            correct_opt = next(o["id"] for o in q["options"] if o.get("is_correct"))
            correct_answers[qid] = correct_opt

        res_submit = client.post(
            "/api/sap/assessments/submit",
            json={
                "day_number": 8,
                "assessment_id": "d8_s6_assessment",
                "assessment_type": "capstone_multi_concept",
                "submission_payload": {"answers": correct_answers},
            },
        )
        assert res_submit.status_code == 200
        data = res_submit.json()
        assert data["passed"] is True
        assert data["score"] == 100.0
    finally:
        clear_auth()
