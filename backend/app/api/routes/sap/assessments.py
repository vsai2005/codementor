"""SAP Assessment Evaluation Endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
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

router = APIRouter()


@router.post("/submit", response_model=SAPAssessmentSubmitResponse)
def submit_assessment(
    payload: SAPAssessmentSubmitRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPAssessmentSubmitResponse:
    result = SAPAssessmentService.evaluate(
        db=db,
        user_id=user.id,
        day_number=payload.day_number,
        assessment_id=payload.assessment_id,
        assessment_type=payload.assessment_type,
        rubric_spec=payload.rubric_spec,
        submission_payload=payload.submission_payload,
    )

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
