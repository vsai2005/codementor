from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import Problem, Submission, Topic, User
from app.schemas.api import (
    GenerateProblemRequest,
    ProblemDetail,
    ProblemPage,
    ProblemSummary,
    ReferenceSolution,
)
from app.services.submissions import next_problem
from app.services.ratelimit import get_generate_rate_limiter

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
    user: User = Depends(get_current_user),
) -> ReferenceSolution:
    problem = None
    try:
        uid = uuid.UUID(problem_id)
        problem = db.get(Problem, uid)
    except (ValueError, TypeError):
        problem = db.execute(select(Problem).where(Problem.slug == problem_id)).scalar_one_or_none()

    if problem is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Problem not found")

    # Authoritative gating: user MUST have an accepted submission for this problem
    accepted = db.execute(
        select(Submission.id).where(
            Submission.user_id == user.id,
            Submission.problem_id == problem.id,
            Submission.tests_passed == Submission.tests_total,
            Submission.tests_total > 0,
        ).limit(1)
    ).scalar_one_or_none()

    if not accepted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reference solution is locked. You must solve the problem and pass all tests first.",
        )

    from app.core.reference_solutions import get_problem_reference_solution

    ref = getattr(problem, "reference_solution", None) or get_problem_reference_solution(problem.slug)

    if ref:
        return ReferenceSolution(
            available=True,
            language="python",
            code=str(ref).strip(),
            commentary=f"Optimal reference solution with {problem.optimal_time} time and {problem.optimal_space} space complexity."
        )

    return ReferenceSolution(
        available=False,
        language="python",
        code="",
        commentary="No reference solution available for this problem."
    )


@router.post("/recommend", response_model=ProblemDetail)
def recommend_problem(
    payload: GenerateProblemRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ProblemDetail:
    """Recommend an existing curated problem from the curriculum matching target criteria."""
    stmt = select(Problem)
    if payload.topic:
        stmt = stmt.join(Topic).where(Topic.slug == payload.topic)
    if payload.tier:
        stmt = stmt.where(Problem.difficulty_tier == payload.tier)
    problem = db.execute(stmt).scalars().first()
    if not problem:
        problem = db.execute(select(Problem)).scalars().first()
    if not problem:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No matching recommended problem found in curriculum.")

    detail = ProblemDetail.model_validate(problem)
    detail.is_generated = False
    detail.generation_source = "curated"
    return detail


@router.post("/generate", response_model=ProblemDetail)
async def generate_ai_problem(
    payload: GenerateProblemRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ProblemDetail:
    """Generate a validated problem using AI or return a curated recommendation."""
    verdict = get_generate_rate_limiter().check(f"generate:{user.id}")
    if not verdict.allowed:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Problem generation rate limit reached. Please wait {verdict.retry_after_s} seconds.",
            headers={"Retry-After": str(verdict.retry_after_s)},
        )

    if payload.mode == "recommend":
        return recommend_problem(payload, db, user)

    from app.services.problem_generator import generate_and_validate_problem
    return await generate_and_validate_problem(
        topic_slug=payload.topic,
        tier=payload.tier,
        db=db,
    )


