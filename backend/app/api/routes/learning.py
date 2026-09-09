from __future__ import annotations

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import User
from app.schemas.api import (
    CompleteLessonRequest,
    CompleteLessonResponse,
    LearningProgressResponse,
)
from app.services import learning as learning_svc
from app.services.sandbox import execute_script_async

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

