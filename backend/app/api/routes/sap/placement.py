"""SAP Placement and Diagnostic Endpoints."""

from __future__ import annotations

from typing import Any, Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import User
from app.models.sap_models import SAPPlacementProfile
from app.sap.data.placement_questions import get_public_questions_for_track
from app.sap.schemas.api import (
    PlacementQuestionOut,
    SAPPlacementChooseStartRequest,
    SAPPlacementDiagnosticRequest,
    SAPPlacementProfileResponse,
)
from app.sap.services.placement import SAPPlacementLockedError, SAPPlacementService

router = APIRouter()


def _profile_response(db: Session, user_id, profile: SAPPlacementProfile) -> SAPPlacementProfileResponse:
    diag_res = profile.diagnostic_results or {}
    return SAPPlacementProfileResponse(
        persona=profile.persona,
        diagnostic_score=diag_res.get("overall_score", 0.0),
        recommended_start_day=profile.recommended_start_day,
        unlocked_days=diag_res.get("unlocked_days", [profile.recommended_start_day]),
        waived_days=diag_res.get("waived_days", []),
        rationale=profile.rationale or "",
        domain_scores=profile.concept_benchmarks or {},
        topic_breakdown=diag_res.get("topic_breakdown", []),
        demonstrated_concepts=diag_res.get("demonstrated_concepts", []),
        gap_concepts=diag_res.get("gap_concepts", []),
        placement_locked=bool(SAPPlacementService.learning_evidence(db, user_id)),
    )


@router.get("/questions", response_model=list[PlacementQuestionOut])
def get_placement_questions(
    track: Literal["experienced", "not_sure"] = Query(
        default="experienced",
        description="Assessment track to retrieve: 'experienced' (10 technical questions) or 'not_sure' (6 fundamental questions)."
    )
) -> list[PlacementQuestionOut]:
    """Retrieves objective questions and options for real diagnostic placement without answers."""
    return [
        PlacementQuestionOut(**q) for q in get_public_questions_for_track(track)
    ]


@router.post("/submit", response_model=SAPPlacementProfileResponse)
def submit_diagnostic(
    payload: SAPPlacementDiagnosticRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPPlacementProfileResponse:
    """Takes or retakes the diagnostic. 409 with no writes once SAP learning has started."""
    try:
        profile = SAPPlacementService.evaluate_diagnostic(
            db=db,
            user_id=user.id,
            experience_level=payload.experience_level,
            answers=payload.answers,
            domain_scores=payload.domain_scores,
            experience_years=payload.experience_years,
            persona_self_select=payload.persona_self_select,
        )
    except SAPPlacementLockedError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return _profile_response(db, user.id, profile)


@router.post("/choose-start", response_model=SAPPlacementProfileResponse)
def choose_starting_day(
    payload: SAPPlacementChooseStartRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPPlacementProfileResponse:
    """Switches between Day 1 and the assessed day. 409 with no writes once learning has started."""
    try:
        profile = SAPPlacementService.choose_start_day(
            db=db,
            user_id=user.id,
            start_day=payload.start_day,
        )
    except SAPPlacementLockedError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return _profile_response(db, user.id, profile)


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

    return _profile_response(db, user.id, profile)

