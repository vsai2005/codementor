"""SAP Learning Modes & Assistance Endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import User
from app.models.sap_models import (
    SAPAssistanceLevel,
    SAPLearningMode,
    SAPUserState,
)
from app.sap.schemas.api import (
    SAPModeStateResponse,
    SAPModeSwitchRequest,
)

router = APIRouter()


@router.get("", response_model=SAPModeStateResponse)
def get_user_mode(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPModeStateResponse:
    """Retrieves learner's current learning mode, last active mode, and assistance level."""
    user_state = db.execute(
        select(SAPUserState).where(SAPUserState.user_id == user.id)
    ).scalar_one_or_none()

    if user_state is None:
        user_state = SAPUserState(
            user_id=user.id,
            preferred_mode=SAPLearningMode.GUIDED.value,
            last_active_mode=SAPLearningMode.GUIDED.value,
            current_guided_day=1,
            assistance_level=SAPAssistanceLevel.TRAINING.value,
        )
        db.add(user_state)
        db.commit()
        db.refresh(user_state)

    return SAPModeStateResponse(
        preferred_mode=user_state.preferred_mode,
        last_active_mode=user_state.last_active_mode,
        current_guided_day=user_state.current_guided_day,
        current_mission_id=str(user_state.current_mission_id) if user_state.current_mission_id else None,
        assistance_level=user_state.assistance_level,
    )


@router.post("", response_model=SAPModeStateResponse)
def switch_mode(
    payload: SAPModeSwitchRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPModeStateResponse:
    """Switches learner's active mode (GUIDED <-> MISSION) and updates assistance level without resetting progress."""
    user_state = db.execute(
        select(SAPUserState).where(SAPUserState.user_id == user.id)
    ).scalar_one_or_none()

    if user_state is None:
        user_state = SAPUserState(
            user_id=user.id,
            preferred_mode=payload.mode,
            last_active_mode=payload.mode,
            current_guided_day=1,
            assistance_level=payload.assistance_level or SAPAssistanceLevel.TRAINING.value,
        )
        db.add(user_state)
    else:
        user_state.preferred_mode = payload.mode
        user_state.last_active_mode = payload.mode
        if payload.assistance_level:
            user_state.assistance_level = payload.assistance_level

    db.commit()
    db.refresh(user_state)

    return SAPModeStateResponse(
        preferred_mode=user_state.preferred_mode,
        last_active_mode=user_state.last_active_mode,
        current_guided_day=user_state.current_guided_day,
        current_mission_id=str(user_state.current_mission_id) if user_state.current_mission_id else None,
        assistance_level=user_state.assistance_level,
    )
