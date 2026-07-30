from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import SessionLocal, get_db
from app.models.models import Problem, Submission, User
from app.schemas.api import (
    DifficultyChange,
    RunRequest,
    SubmissionHistoryItem,
    SubmissionResponse,
    TestCaseResult,
    TestsResponse,
)
from app.services import submissions as svc
from app.services.difficulty import banner_text
from app.services.embeddings import get_embedder
from app.services.llm import get_llm_client
from app.services.memory import MemoryService, build_note_prompt
from app.services.ratelimit import get_rate_limiter
from app.services.repositories import PgMemoryRepository
from app.services.review import ReviewService, degraded_review

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/submissions", tags=["submissions"])


def _tests_payload(report) -> TestsResponse:
    return TestsResponse(
        passed=report.passed_count,
        total=report.total,
        all_passed=report.all_passed,
        results=[
            TestCaseResult(
                index=r.index, passed=r.passed, status=r.status,
                runtime_ms=r.runtime_ms, stdout=r.stdout, stderr=r.stderr,
            )
            for r in report.results
        ],
    )


def _load_problem(db: Session, problem_id: uuid.UUID) -> Problem:
    problem = db.get(Problem, problem_id)
    if problem is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Problem not found")
    return problem


@router.post("/run", response_model=TestsResponse)
def run_only(
    payload: RunRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TestsResponse:
    """Tests only, no LLM. Target < 2s p95."""
    problem = _load_problem(db, payload.problem_id)
    return _tests_payload(svc.execute(problem, payload.code))


@router.post("", response_model=SubmissionResponse)
def submit(
    payload: RunRequest,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> SubmissionResponse:
    # PRD 5.4 step 1 — rate limit before doing any expensive work.
    verdict = get_rate_limiter().check(f"submissions:{user.id}")
    if not verdict.allowed:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Submission rate limit reached. Try again shortly.",
            headers={"Retry-After": str(verdict.retry_after_s)},
        )

    problem = _load_problem(db, payload.problem_id)
    report = svc.execute(problem, payload.code)

    try:
        reviewer = ReviewService(get_llm_client())
        review = reviewer.review(
            problem_title=problem.title,
            statement_md=problem.statement_md,
            optimal_time=problem.optimal_time,
            optimal_space=problem.optimal_space,
            language=payload.language,
            code=payload.code,
            report=report,
        )
    except Exception:
        # A misconfigured LLM must not cost the user their submission.
        log.exception("review pipeline failed outright; degrading")
        review = degraded_review(report, problem.optimal_time, problem.optimal_space,
                                 note="AI reviewer unavailable")

    submission = svc.persist_submission(
        db, user_id=user.id, problem=problem, language=payload.language,
        code=payload.code, report=report, review=review,
    )
    decision = svc.apply_difficulty(
        db, user_id=user.id, topic_id=problem.topic_id,
        submission_id=submission.id, new_score=review.overall_score,
    )

    # PRD 5.7 — embedding runs after the response; it must never block or fail
    # the submission.
    background.add_task(
        _write_memory_note,
        user_id=str(user.id),
        submission_id=str(submission.id),
        topic_id=str(problem.topic_id),
        problem_title=problem.title,
        score=review.overall_score,
        summary=review.summary,
        weak_topics=list(review.weak_topics),
    )

    return SubmissionResponse(
        submission_id=submission.id,
        tests=_tests_payload(report),
        review=review,
        difficulty=DifficultyChange(
            **{"from": decision.tier_from, "to": decision.tier_to},
            rolling_score=decision.rolling_score,
            banner=banner_text(decision),
        ),
    )


@router.get("", response_model=list[SubmissionHistoryItem])
def history(
    problem_id: uuid.UUID | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[SubmissionHistoryItem]:
    stmt = select(Submission).where(Submission.user_id == user.id)
    if problem_id:
        stmt = stmt.where(Submission.problem_id == problem_id)
    rows = db.execute(stmt.order_by(desc(Submission.created_at)).limit(limit)).scalars().all()
    return [SubmissionHistoryItem.model_validate(r) for r in rows]


def _write_memory_note(*, user_id: str, submission_id: str, topic_id: str,
                       problem_title: str, score: int, summary: str,
                       weak_topics: list[str]) -> None:
    """Background task. Swallows every error by design (PRD 5.7)."""
    db = SessionLocal()
    try:
        llm = get_llm_client()
        prompt = build_note_prompt(problem_title, score, summary, weak_topics)
        content = llm.complete(prompt, temperature=0.3, max_tokens=200, timeout=10.0).strip()
        memory = MemoryService(PgMemoryRepository(db), get_embedder())
        memory.store_note(
            user_id=user_id, content=content,
            topic_id=topic_id, submission_id=submission_id,
        )
    except Exception:
        log.exception("memory note generation failed for submission %s", submission_id)
    finally:
        db.close()
