from datetime import datetime, timezone
import logging
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.api.deps import get_current_user, get_current_user_optional
from app.database import get_db
from app.models.models import User, UserLearningDayState
from app.schemas.api import (
    CompleteLessonRequest,
    CompleteLessonResponse,
    DevSetProgressRequest,
    LearningProgressResponse,
    LearningTutorChatRequest,
    LearningTutorQuickActionRequest,
    LearningTutorResponse,
)
from app.services import learning as learning_svc
from app.services.ratelimit import get_tutor_rate_limiter
from app.services.sandbox import execute_script_async
from app.services.teacher import AITeacherService, get_teacher_service
from app.services.tutor_security import sanitize_tutor_input

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/learning", tags=["learning"])


class RunLessonSnippetRequest(BaseModel):
    code: str = Field(..., max_length=25000, description="Python code snippet to execute")
    day_number: int = Field(default=1, ge=1, le=160, description="Curriculum day number")


class RunLessonSnippetResponse(BaseModel):
    status: str
    stdout: str
    stderr: str
    runtime_ms: int


@router.post("/run", response_model=RunLessonSnippetResponse)
async def run_lesson_snippet(payload: RunLessonSnippetRequest) -> RunLessonSnippetResponse:
    """Execute a student code snippet in the zero-trust sandbox for interactive curriculum days."""
    try:
        result = await execute_script_async(payload.code)
        return RunLessonSnippetResponse(
            status=result.get("status", "ok"),
            stdout=result.get("stdout", ""),
            stderr=result.get("stderr", ""),
            runtime_ms=result.get("runtime_ms", 0),
        )
    except Exception as exc:
        log.exception("learning snippet execution failure")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Execution engine error: {str(exc)}",
        ) from exc


@router.get("/progress", response_model=LearningProgressResponse)
def get_progress(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Retrieve full authoritative curriculum progression for current user."""
    return learning_svc.compute_user_progress(db, user.id)


@router.post("/complete-lesson", response_model=CompleteLessonResponse)
def complete_lesson(
    payload: CompleteLessonRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Marks day lesson completed after verifying day is unlocked."""
    try:
        return learning_svc.complete_lesson(db, user.id, payload.day_number)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))


@router.post("/tutor/chat", response_model=LearningTutorResponse)
async def tutor_chat(
    payload: LearningTutorChatRequest,
    request: Request,
    user: User | None = Depends(get_current_user_optional),
    teacher_svc: AITeacherService = Depends(get_teacher_service),
) -> LearningTutorResponse:
    """Chat with the Socratic AI Teacher for a specific curriculum day and step."""
    limiter = get_tutor_rate_limiter()
    ratelimit_key = str(user.id) if user else (request.client.host if request.client else "anonymous")
    verdict = limiter.check(ratelimit_key)
    if not verdict.allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many tutor requests. Please wait {verdict.retry_after_s} seconds.",
        )

    val_res = sanitize_tutor_input(payload.message, payload.user_code)
    if not val_res.is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=val_res.error_message or "Invalid input.",
        )

    result = teacher_svc.generate_response(
        day_number=payload.day_number,
        step_number=payload.step_number,
        query=val_res.sanitized_message,
        history=payload.history,
        user_code=val_res.sanitized_code,
        step_context=payload.step_context,
        quick_action=payload.quick_action,
    )
    return LearningTutorResponse(**result)


@router.post("/tutor/quick-action", response_model=LearningTutorResponse)
async def tutor_quick_action(
    payload: LearningTutorQuickActionRequest,
    request: Request,
    user: User | None = Depends(get_current_user_optional),
    teacher_svc: AITeacherService = Depends(get_teacher_service),
) -> LearningTutorResponse:
    """Execute a pedagogical quick action (e.g. explain simply, give hint, find mistake)."""
    limiter = get_tutor_rate_limiter()
    ratelimit_key = str(user.id) if user else (request.client.host if request.client else "anonymous")
    verdict = limiter.check(ratelimit_key)
    if not verdict.allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many tutor requests. Please wait {verdict.retry_after_s} seconds.",
        )

    val_res = sanitize_tutor_input(f"Action: {payload.action}", payload.user_code)
    result = teacher_svc.generate_response(
        day_number=payload.day_number,
        step_number=payload.step_number,
        query="",
        history=payload.history,
        user_code=val_res.sanitized_code,
        step_context=payload.step_context,
        quick_action=payload.action,
    )
    return LearningTutorResponse(**result)


@router.post("/dev-set-progress", response_model=LearningProgressResponse)
def dev_set_progress(
    payload: DevSetProgressRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> LearningProgressResponse:
    """Developer helper: fast-forward user progress up to day N."""
    settings = get_settings()
    if settings.is_production:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Developer fast-forward endpoint is disabled in production environments.",
        )

    now = datetime.now(timezone.utc)
    for d in range(1, payload.completed_up_to + 1):
        st = db.execute(
            select(UserLearningDayState).where(
                UserLearningDayState.user_id == user.id,
                UserLearningDayState.day_number == d,
            )
        ).scalar_one_or_none()
        if not st:
            st = UserLearningDayState(
                user_id=user.id,
                day_number=d,
                lesson_completed=True,
                lesson_completed_at=now,
                practice_passed=True,
                practice_passed_at=now,
                completed=True,
                completed_at=now,
            )
            db.add(st)
        else:
            st.lesson_completed = True
            st.practice_passed = True
            st.completed = True
            st.completed_at = now
    db.commit()
    return learning_svc.compute_user_progress(db, user.id)


