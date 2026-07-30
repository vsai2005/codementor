from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import Problem, Topic, User
from app.schemas.api import ProblemDetail, ProblemPage, ProblemSummary
from app.services.submissions import next_problem

router = APIRouter(prefix="/api/problems", tags=["problems"])


@router.get("", response_model=ProblemPage)
def list_problems(
    topic: str | None = None,
    tier: int | None = Query(default=None, ge=1, le=5),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ProblemPage:
    stmt = select(Problem)
    count_stmt = select(func.count()).select_from(Problem)

    if topic:
        stmt = stmt.join(Topic).where(Topic.slug == topic)
        count_stmt = count_stmt.join(Topic, Topic.id == Problem.topic_id).where(Topic.slug == topic)
    if tier is not None:
        stmt = stmt.where(Problem.difficulty_tier == tier)
        count_stmt = count_stmt.where(Problem.difficulty_tier == tier)

    total = db.execute(count_stmt).scalar_one()
    rows = db.execute(
        stmt.order_by(Problem.difficulty_tier, Problem.title)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).scalars().unique().all()

    return ProblemPage(
        items=[ProblemSummary.model_validate(p) for p in rows],
        page=page, page_size=page_size, total=total,
    )


@router.get("/next", response_model=ProblemDetail)
def recommended(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> ProblemDetail:
    problem = next_problem(db, user.id)
    if problem is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No unsolved problems available")
    return ProblemDetail.model_validate(problem)


@router.get("/{problem_id}", response_model=ProblemDetail)
def get_problem(
    problem_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ProblemDetail:
    problem = db.get(Problem, problem_id)
    if problem is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Problem not found")
    return ProblemDetail.model_validate(problem)
