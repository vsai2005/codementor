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
from app.sap.services.assessment import SAPAssessmentService
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
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPLessonDetail:
    """Returns the full 8-step pedagogical lesson content for a day the learner may access.

    Access rules (server-side, authoritative):
    - 404 if lesson content is not yet authored.
    - 403 if the day is locked (learner has not unlocked it via prior progression).
    - 403 if the day was waived by diagnostic placement (lesson is not required).
    - 200 with full lesson for current, available, in-progress, or completed days.
    """
    lesson = SAP_DAYS_CONTENT.get(day_number)
    if not lesson:
        raise HTTPException(
            status_code=404,
            detail=f"Lesson content for Day {day_number} does not exist. Valid days are 1–{max(SAP_DAYS_CONTENT.keys())}.",
        )

    # Authoritative server-side access check
    progress = SAPProgressionService.compute_user_progress(db, user.id)
    day_info = progress["day_states"].get(str(day_number))

    if not day_info:
        raise HTTPException(
            status_code=404,
            detail=f"SAP Day {day_number} does not exist.",
        )
    if day_info.get("waived"):
        raise HTTPException(
            status_code=403,
            detail=f"Day {day_number} was waived by diagnostic placement. Its lesson content is not required.",
        )
    if not day_info["unlocked"]:
        raise HTTPException(
            status_code=403,
            detail=f"Day {day_number} is locked. Complete prior days or take the diagnostic placement first.",
        )

    sanitized = SAPAssessmentService.sanitize_lesson_content(day_number, lesson)
    return SAPLessonDetail(**sanitized)


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
    """Grades Practice evidence server-side; Practice is marked complete only on a pass.

    - 400: day locked/waived, or evidence that does not belong to this day's Practice
      (unknown step, missing step, or invalid option). Zero state mutation.
    - 200 with passed=False: well-formed but incorrect answers. Zero state mutation.
    - 200 with passed=True: Practice recorded (idempotent on repeat).
    """
    try:
        result = SAPProgressionService.submit_practice(
            db, user.id, payload.day_number, payload.answers
        )
        return SAPCompletePracticeResponse(**result)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

