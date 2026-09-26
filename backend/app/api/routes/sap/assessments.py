"""SAP Assessment Evaluation Endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import User
from app.sap.schemas.api import (
    SAPAssessmentSubmitRequest,
    SAPAssessmentSubmitResponse,
    SAPRemediationCapsuleDetail,
    SAPWaivedDayChallenge,
)
from app.sap.services.assessment import SAPAssessmentService
from app.sap.services.progression import SAPProgressionService

router = APIRouter()


def _submit_response(result: dict) -> SAPAssessmentSubmitResponse:
    remed_capsule = None
    if result.get("remediation_capsule"):
        remed_capsule = SAPRemediationCapsuleDetail(**result["remediation_capsule"])

    return SAPAssessmentSubmitResponse(
        submission_id=result["submission_id"],
        passed=result["passed"],
        score=result["score"],
        feedback=result["feedback"],
        evaluation_breakdown=result["evaluation_breakdown"],
        mastery_updated=result["mastery_updated"],
        concept_evaluations=result.get("concept_evaluations", []),
        remediation_required=result["remediation_required"],
        remediation_capsule=remed_capsule,
        all_remediations=result.get("all_remediations", []),
        day_completed=result.get("day_completed", False),
        unlocked_next_day=result.get("unlocked_next_day", False),
        current_day=result.get("current_day"),
        next_day_number=result.get("next_day_number"),
    )


def _bind_assessment_identity(payload: SAPAssessmentSubmitRequest) -> tuple[str, str]:
    """Binds a submission to the day's authoritative assessment id and type (else 400/404)."""
    from app.data.sap_lessons import SAP_DAYS_CONTENT

    day_data = SAP_DAYS_CONTENT.get(payload.day_number)
    if not day_data:
        raise HTTPException(
            status_code=404,
            detail=f"SAP Day {payload.day_number} content definition not found.",
        )

    assessment_step = next(
        (s for s in day_data.get("steps", []) if s.get("step_type") == "assessment"),
        None,
    )
    if not assessment_step:
        raise HTTPException(
            status_code=400,
            detail=f"No assessment defined for SAP Day {payload.day_number}.",
        )

    canonical_step_id = assessment_step.get("step_id")
    canonical_id = canonical_step_id or f"d{payload.day_number}_s6_assessment"
    valid_assessment_ids = {
        canonical_id,
        f"d{payload.day_number}_s6_assessment",
        f"day-{payload.day_number}-assessment",
    }
    if canonical_step_id:
        valid_assessment_ids.add(canonical_step_id)
    day_slug = day_data.get("slug", "")
    if day_slug:
        valid_assessment_ids.add(f"day-{payload.day_number}-{day_slug}")
    if payload.day_number == 8:
        valid_assessment_ids.add("day-8-foundations-capstone")
    elif payload.day_number == 22:
        valid_assessment_ids.add("day-22-s4hana-capstone")

    if not payload.assessment_id or not payload.assessment_id.strip():
        raise HTTPException(
            status_code=400,
            detail=(
                f"Assessment ID mismatch for Day {payload.day_number}. "
                f"Expected canonical ID '{canonical_id}', received empty or missing ID."
            ),
        )

    if payload.assessment_id not in valid_assessment_ids:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Assessment ID mismatch for Day {payload.day_number}. "
                f"Expected canonical ID '{canonical_id}', received '{payload.assessment_id}'."
            ),
        )

    raw_type = assessment_step.get("assessment_type")
    if raw_type:
        canonical_type = raw_type
    elif assessment_step.get("multi_concept_eval") or assessment_step.get("is_capstone"):
        canonical_type = "capstone_multi_concept"
    else:
        canonical_type = "mcq"

    valid_types = {canonical_type}
    if canonical_type in ("capstone_multi_concept", "capstone_quiz"):
        valid_types.update({"capstone_multi_concept", "capstone_quiz"})

    if payload.assessment_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Assessment type mismatch for Day {payload.day_number}. "
                f"Expected canonical type '{canonical_type}', received '{payload.assessment_type}'."
            ),
        )

    return canonical_id, canonical_type




@router.post("/submit", response_model=SAPAssessmentSubmitResponse)
def submit_assessment(
    payload: SAPAssessmentSubmitRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPAssessmentSubmitResponse:
    # 1. Authoritative access and gating check
    progress = SAPProgressionService.compute_user_progress(db, user.id)
    day_info = progress["day_states"].get(str(payload.day_number))
    if not day_info:
        raise HTTPException(
            status_code=404,
            detail=f"SAP Day {payload.day_number} does not exist.",
        )

    if day_info.get("waived"):
        raise HTTPException(
            status_code=403,
            detail=f"SAP Day {payload.day_number} was waived by diagnostic placement and cannot be submitted.",
        )

    if not day_info.get("unlocked") or day_info.get("status") == "locked":
        raise HTTPException(
            status_code=403,
            detail=f"SAP Day {payload.day_number} is locked. Complete prerequisite days first.",
        )

    # 2. Mandatory practice requirement before assessment attempt
    if not day_info.get("practice_completed") and not day_info.get("completed"):
        raise HTTPException(
            status_code=400,
            detail=f"Interactive practice is mandatory. Complete Day {payload.day_number} practice before attempting assessment.",
        )

    # 3. Authoritative server-side assessment identity binding
    canonical_id, canonical_type = _bind_assessment_identity(payload)

    try:
        result = SAPAssessmentService.evaluate(
            db=db,
            user_id=user.id,
            day_number=payload.day_number,
            assessment_id=canonical_id,
            assessment_type=canonical_type,
            rubric_spec=payload.rubric_spec,
            submission_payload=payload.submission_payload,
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

    return _submit_response(result)


# =============================================================================
# Waived-day challenges
# =============================================================================

def _require_waived_day(db: Session, user_id, day_number: int) -> None:
    progress = SAPProgressionService.compute_user_progress(db, user_id)
    day_info = progress["day_states"].get(str(day_number))
    if not day_info:
        raise HTTPException(status_code=404, detail=f"SAP Day {day_number} does not exist.")
    if not day_info.get("waived"):
        raise HTTPException(
            status_code=403,
            detail=(
                f"SAP Day {day_number} was not waived by placement. Challenges are only for waived "
                "days; take this day's assessment through its lesson."
            ),
        )


@router.get("/challenge/{day_number}", response_model=SAPWaivedDayChallenge)
def get_waived_day_challenge(
    day_number: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPWaivedDayChallenge:
    """Returns ONLY the (answer-key-free) assessment of a day the learner's placement waived.

    The waived lesson itself stays closed (GET /learning/lessons/{day} remains 403); this is
    the path to earn that day's concepts from real graded evidence.
    """
    from app.data.sap_lessons import SAP_DAYS_CONTENT

    _require_waived_day(db, user.id, day_number)
    lesson = SAP_DAYS_CONTENT.get(day_number)
    if not lesson:
        raise HTTPException(status_code=404, detail=f"SAP Day {day_number} content definition not found.")
    sanitized = SAPAssessmentService.sanitize_lesson_content(day_number, lesson)
    step = next((s for s in sanitized["steps"] if s.get("step_type") == "assessment"), None)
    if step is None:
        raise HTTPException(status_code=404, detail=f"No assessment defined for SAP Day {day_number}.")
    return SAPWaivedDayChallenge(
        day_number=day_number,
        day_title=lesson.get("title", f"Day {day_number}"),
        title=step.get("title") or f"Day {day_number} Challenge",
        assessment_id=step["assessment_id"],
        assessment_type=step["assessment_type"],
        questions=step.get("questions") or [],
    )


@router.post("/challenge", response_model=SAPAssessmentSubmitResponse)
def submit_waived_day_challenge(
    payload: SAPAssessmentSubmitRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPAssessmentSubmitResponse:
    """Grades a waived day's assessment server-side and records the demonstrated concepts.

    Mastery changes only from the graded answers. The day stays waived: no lesson, practice,
    completion, unlock, or current-day change.
    """
    _require_waived_day(db, user.id, payload.day_number)
    canonical_id, canonical_type = _bind_assessment_identity(payload)
    try:
        result = SAPAssessmentService.evaluate(
            db=db,
            user_id=user.id,
            day_number=payload.day_number,
            assessment_id=canonical_id,
            assessment_type=canonical_type,
            submission_payload=payload.submission_payload,
            waived_day_challenge=True,
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    return _submit_response(result)
