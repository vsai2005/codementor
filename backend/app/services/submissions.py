"""Submission pipeline orchestration (PRD 5.4).

No FastAPI imports — routes stay thin, logic lives here.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models.models import (
    DifficultyEvent,
    Mastery,
    Problem,
    Submission,
    UserTopicState,
)
from app.schemas.review import Review
from app.services.difficulty import TierDecision, compute_next_tier, topic_priority
from app.services.sandbox import ExecutionReport, run_test_cases

log = logging.getLogger(__name__)

RECENT_SOLVED_WINDOW_DAYS = 30


def execute(problem: Problem, code: str) -> ExecutionReport:
    return run_test_cases(code, problem.entry_point, problem.test_cases)


def _recent_scores(db: Session, user_id: uuid.UUID, topic_id: uuid.UUID,
                   limit: int = 3) -> list[float]:
    stmt = (
        select(Submission.overall_score)
        .join(Problem, Problem.id == Submission.problem_id)
        .where(Submission.user_id == user_id, Problem.topic_id == topic_id)
        .order_by(desc(Submission.created_at))
        .limit(limit)
    )
    return [float(s) for s in db.execute(stmt).scalars().all()]


def _last_event_was_demotion(db: Session, user_id: uuid.UUID,
                             topic_id: uuid.UUID) -> bool:
    stmt = (
        select(DifficultyEvent.tier_from, DifficultyEvent.tier_to)
        .where(DifficultyEvent.user_id == user_id, DifficultyEvent.topic_id == topic_id)
        .order_by(desc(DifficultyEvent.created_at))
        .limit(1)
    )
    row = db.execute(stmt).first()
    return bool(row and row.tier_to < row.tier_from)


def _mastery_for(avg_score: float, attempts: int) -> Mastery:
    if attempts < 3:
        return Mastery.learning if avg_score >= 50 else Mastery.weak
    if avg_score >= 80:
        return Mastery.strong
    if avg_score >= 50:
        return Mastery.learning
    return Mastery.weak


def apply_difficulty(db: Session, *, user_id: uuid.UUID, topic_id: uuid.UUID,
                     submission_id: uuid.UUID, new_score: int) -> TierDecision:
    """Update tier state and write a difficulty_events row for EVERY submission."""
    state = db.get(UserTopicState, (user_id, topic_id))
    if state is None:
        state = UserTopicState(user_id=user_id, topic_id=topic_id, current_tier=1)
        db.add(state)
        db.flush()

    # The just-persisted submission is already in the table, so this window
    # includes it as s1 — which is what "most recent" means.
    scores = _recent_scores(db, user_id, topic_id)
    decision = compute_next_tier(
        state.current_tier, scores, _last_event_was_demotion(db, user_id, topic_id)
    )

    total = state.avg_score * state.attempts + new_score
    state.attempts += 1
    state.avg_score = round(total / state.attempts, 2)
    state.current_tier = decision.tier_to
    state.mastery = _mastery_for(state.avg_score, state.attempts)
    state.last_practiced_at = datetime.now(timezone.utc)

    db.add(
        DifficultyEvent(
            user_id=user_id,
            topic_id=topic_id,
            submission_id=submission_id,
            rolling_score=decision.rolling_score,
            tier_from=decision.tier_from,
            tier_to=decision.tier_to,
            reason=decision.reason,
        )
    )
    db.commit()
    return decision


def persist_submission(db: Session, *, user_id: uuid.UUID, problem: Problem,
                       language: str, code: str, report: ExecutionReport,
                       review: Review) -> Submission:
    submission = Submission(
        user_id=user_id,
        problem_id=problem.id,
        language=language,
        code=code,
        tests_passed=report.passed_count,
        tests_total=report.total,
        overall_score=review.overall_score,
        scores=review.scores.model_dump(),
        review=review.model_dump(),
        review_degraded=review.review_degraded,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


def next_problem(db: Session, user_id: uuid.UUID) -> Problem | None:
    """Highest-priority topic, at that topic's tier, not solved in 30 days."""
    states = db.execute(
        select(UserTopicState).where(UserTopicState.user_id == user_id)
    ).scalars().all()

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=RECENT_SOLVED_WINDOW_DAYS)

    recently_solved = set(
        db.execute(
            select(Submission.problem_id).where(
                Submission.user_id == user_id,
                Submission.created_at >= cutoff,
                Submission.overall_score >= 80,
            )
        ).scalars().all()
    )

    if not states:
        stmt = select(Problem).where(Problem.difficulty_tier == 1)
        if recently_solved:
            stmt = stmt.where(Problem.id.notin_(recently_solved))
        return db.execute(stmt.order_by(func.random()).limit(1)).scalars().first()

    ranked = sorted(
        states,
        key=lambda s: topic_priority(
            s.avg_score,
            (now - s.last_practiced_at).days if s.last_practiced_at else None,
        ),
        reverse=True,
    )

    for state in ranked:
        # Widen outward from the target tier rather than returning nothing when
        # a tier happens to be empty — an inventory gap should not stall practice.
        for tier in _tier_search_order(state.current_tier):
            stmt = select(Problem).where(
                Problem.topic_id == state.topic_id,
                Problem.difficulty_tier == tier,
            )
            if recently_solved:
                stmt = stmt.where(Problem.id.notin_(recently_solved))
            found = db.execute(stmt.order_by(func.random()).limit(1)).scalars().first()
            if found:
                return found
    return None


def _tier_search_order(tier: int) -> list[int]:
    order, seen = [], set()
    for offset in (0, -1, 1, -2, 2, -3, 3, -4, 4):
        candidate = tier + offset
        if 1 <= candidate <= 5 and candidate not in seen:
            seen.add(candidate)
            order.append(candidate)
    return order
