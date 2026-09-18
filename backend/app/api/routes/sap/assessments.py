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
)
from app.sap.services.assessment import SAPAssessmentService
from app.sap.services.progression import SAPProgressionService

router = APIRouter()


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

    try:
        result = SAPAssessmentService.evaluate(
            db=db,
            user_id=user.id,
            day_number=payload.day_number,
            assessment_id=payload.assessment_id,
            assessment_type=payload.assessment_type,
            rubric_spec=payload.rubric_spec,
            submission_payload=payload.submission_payload,
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

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
