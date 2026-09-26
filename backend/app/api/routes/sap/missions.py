"""SAP Enterprise Missions Endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import User
from app.models.sap_models import SAPUserState
from app.sap.schemas.api import (
    SAPMissionDetail,
    SAPMissionStartResponse,
    SAPMissionStepAttemptRequest,
    SAPMissionStepAttemptResponse,
    SAPMissionSummary,
)
from app.sap.services.missions import (
    SAPMissionLockedError,
    SAPMissionNotFoundError,
    SAPMissionService,
    SAPMissionStepNotFoundError,
)

router = APIRouter()


def _mission_http_error(err: ValueError) -> HTTPException:
    """Maps mission service errors: unknown mission/step 404, locked 403, otherwise 400."""
    if isinstance(err, (SAPMissionNotFoundError, SAPMissionStepNotFoundError)):
        return HTTPException(status_code=404, detail=str(err))
    if isinstance(err, SAPMissionLockedError):
        return HTTPException(status_code=403, detail=str(err))
    return HTTPException(status_code=400, detail=str(err))


@router.get("", response_model=list[SAPMissionSummary])
def list_missions(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[SAPMissionSummary]:
    """Lists all enterprise missions with unlock eligibility and attempt status."""
    missions = SAPMissionService.list_missions_for_user(db, user_id=user.id)
    return [SAPMissionSummary(**m) for m in missions]


@router.get("/{slug}", response_model=SAPMissionDetail)
def get_mission_detail(
    slug: str,
    assistance_level: str | None = Query(None, description="Override assistance level: TRAINING | GUIDED | JOB"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPMissionDetail:
    """Retrieves full mission details, digital twin context, and assistance rules."""
    # If not provided, fetch user's configured assistance level
    if not assistance_level:
        user_state = db.execute(
            select(SAPUserState).where(SAPUserState.user_id == user.id)
        ).scalar_one_or_none()
        assistance_level = user_state.assistance_level if user_state else "TRAINING"

    try:
        detail = SAPMissionService.get_mission_detail(
            db, user_id=user.id, slug=slug, assistance_level=assistance_level
        )
        return SAPMissionDetail(**detail)
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.post("/{slug}/start", response_model=SAPMissionStartResponse)
def start_mission(
    slug: str,
    assistance_level: str = Query("TRAINING", description="Assistance level: TRAINING | GUIDED | JOB"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPMissionStartResponse:
    """Starts or resumes a mission attempt. Locked missions return 403 with no state change."""
    try:
        attempt = SAPMissionService.start_mission(
            db, user_id=user.id, slug=slug, assistance_level=assistance_level
        )
        return SAPMissionStartResponse(
            mission_slug=slug,
            attempt_id=str(attempt.id),
            status=attempt.status,
            assistance_level=attempt.assistance_level,
            current_step_index=attempt.current_step_index,
        )
    except ValueError as err:
        raise _mission_http_error(err)


@router.post("/{slug}/attempt", response_model=SAPMissionStepAttemptResponse)
def submit_step_attempt(
    slug: str,
    payload: SAPMissionStepAttemptRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPMissionStepAttemptResponse:
    """Evaluates a mission step, records skill evidence, and applies deterministic enterprise consequences."""
    try:
        result = SAPMissionService.submit_step_attempt(
            db=db,
            user_id=user.id,
            slug=slug,
            step_id=payload.step_id,
            payload=payload.payload,
            assistance_level=payload.assistance_level,
        )
        return SAPMissionStepAttemptResponse(**result)
    except ValueError as err:
        raise _mission_http_error(err)
