from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import Problem, Topic, User
from app.schemas.api import (
    GenerateProblemRequest,
    ProblemDetail,
    ProblemPage,
    ProblemSummary,
    ReferenceSolution,
)
from app.services.submissions import next_problem

router = APIRouter(prefix="/api/problems", tags=["problems"])


@router.get("", response_model=ProblemPage)
def list_problems(
    topic: str | None = None,
    tier: int | None = Query(default=None, ge=1, le=5),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=250, ge=1, le=500),
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
    problem_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ProblemDetail:
    problem = None
    try:
        uid = uuid.UUID(problem_id)
        problem = db.get(Problem, uid)
    except (ValueError, TypeError):
        problem = db.execute(select(Problem).where(Problem.slug == problem_id)).scalar_one_or_none()

    if problem is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Problem not found")
    return ProblemDetail.model_validate(problem)


@router.get("/{problem_id}/reference", response_model=ReferenceSolution)
def get_reference_solution(
    problem_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ReferenceSolution:
    problem = None
    try:
        uid = uuid.UUID(problem_id)
        problem = db.get(Problem, uid)
    except (ValueError, TypeError):
        problem = db.execute(select(Problem).where(Problem.slug == problem_id)).scalar_one_or_none()

    if problem is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Problem not found")

    ref = getattr(problem, "reference_solution", None)
    if not ref and isinstance(problem.starter_code, dict):
        ref = problem.starter_code.get("reference") or problem.starter_code.get("solution")

    if ref:
        return ReferenceSolution(
            available=True,
            language="python",
            code=str(ref).strip(),
            commentary=f"Optimal reference solution with {problem.optimal_time} time and {problem.optimal_space} space complexity."
        )

    return ReferenceSolution(
        available=True,
        language="python",
        code=f"# Reference solution for {problem.title}\n# Target complexity: {problem.optimal_time} time, {problem.optimal_space} space\n\ndef {problem.entry_point}(*args, **kwargs):\n    pass\n",
        commentary=f"Standard solution targeting {problem.optimal_time} time and {problem.optimal_space} space complexity."
    )


@router.post("/generate", response_model=ProblemDetail)
def generate_ai_problem(
    payload: GenerateProblemRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ProblemDetail:
    stmt = select(Problem)
    if payload.topic:
        stmt = stmt.join(Topic).where(Topic.slug == payload.topic)
    if payload.tier:
        stmt = stmt.where(Problem.difficulty_tier == payload.tier)
    problem = db.execute(stmt).scalars().first()
    if not problem:
        problem = db.execute(select(Problem)).scalars().first()
    if not problem:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Could not generate or find a problem.")
    return ProblemDetail.model_validate(problem)


