"""SAP Learning Progression Endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import User
from app.data.sap_lessons import SAP_DAYS_CONTENT
from app.sap.schemas.api import (
    SAPCompleteLessonRequest,
    SAPCompleteLessonResponse,
    SAPCompletePracticeRequest,
    SAPCompletePracticeResponse,
    SAPLessonDetail,
    SAPProgressResponse,
)
from app.sap.services.progression import SAPProgressionService

router = APIRouter()


@router.get("/progress", response_model=SAPProgressResponse)
def get_user_progress(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPProgressResponse:
    data = SAPProgressionService.compute_user_progress(db, user.id)
    return SAPProgressResponse(**data)


@router.get("/lessons/{day_number}", response_model=SAPLessonDetail)
def get_lesson_content(
    day_number: int,
) -> SAPLessonDetail:
    """Returns the full 8-step pedagogical lesson content and practice specs for a given day."""
    lesson = SAP_DAYS_CONTENT.get(day_number)
    if not lesson:
        raise HTTPException(
            status_code=404,
            detail=f"Lesson content for Day {day_number} is not authored yet (Days 1–54 available).",
        )
    return SAPLessonDetail(**lesson)


@router.post("/complete-lesson", response_model=SAPCompleteLessonResponse)
def complete_lesson(
    payload: SAPCompleteLessonRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPCompleteLessonResponse:
    try:
        result = SAPProgressionService.complete_lesson(db, user.id, payload.day_number)
        return SAPCompleteLessonResponse(**result)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.post("/complete-practice", response_model=SAPCompletePracticeResponse)
def complete_practice(
    payload: SAPCompletePracticeRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPCompletePracticeResponse:
    try:
        result = SAPProgressionService.record_practice_completed(db, user.id, payload.day_number)
        return SAPCompletePracticeResponse(**result)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

