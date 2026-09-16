"""SAP Placement and Diagnostic Endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import User
from app.models.sap_models import SAPPlacementProfile
from app.sap.schemas.api import (
    SAPPlacementDiagnosticRequest,
    SAPPlacementProfileResponse,
)
from app.sap.services.placement import SAPPlacementService

router = APIRouter()


@router.post("/submit", response_model=SAPPlacementProfileResponse)
def submit_diagnostic(
    payload: SAPPlacementDiagnosticRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPPlacementProfileResponse:
    profile = SAPPlacementService.evaluate_diagnostic(
        db=db,
        user_id=user.id,
        domain_scores=payload.domain_scores,
        experience_years=payload.experience_years,
        persona_self_select=payload.persona_self_select,
    )
    return SAPPlacementProfileResponse(
        persona=profile.persona,
        diagnostic_score=profile.diagnostic_results.get("overall_score", 0.0),
        recommended_start_day=profile.recommended_start_day,
        unlocked_days=profile.diagnostic_results.get("unlocked_days", []),
        rationale=profile.rationale or "",
        domain_scores=profile.concept_benchmarks,
    )


@router.get("/profile", response_model=SAPPlacementProfileResponse)
def get_user_placement(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPPlacementProfileResponse:
    profile = db.execute(
        select(SAPPlacementProfile).where(SAPPlacementProfile.user_id == user.id)
    ).scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="No SAP placement diagnostic found for current user.")

    return SAPPlacementProfileResponse(
        persona=profile.persona,
        diagnostic_score=profile.diagnostic_results.get("overall_score", 0.0),
        recommended_start_day=profile.recommended_start_day,
        unlocked_days=profile.diagnostic_results.get("unlocked_days", []),
        rationale=profile.rationale or "",
        domain_scores=profile.concept_benchmarks,
    )
