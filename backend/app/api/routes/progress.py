from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import Problem, Submission, Topic, User, UserTopicState
from app.schemas.api import (
    AccountSummary,
    Badge,
    MisconceptionItem,
    MisconceptionsResponse,
    MomentumSummary,
    ProgressResponse,
    RecentSolvedItem,
    RecentSolvedResponse,
    ReviewQueueItem,
    ReviewQueueResponse,
    TopicOut,
    TopicProgress,
    TrendPoint,
    TrendResponse,
)

router = APIRouter(tags=["progress"])


@router.get("/api/progress/topics", response_model=ProgressResponse)
def topic_progress(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> ProgressResponse:
    rows = db.execute(
        select(UserTopicState, Topic)
        .join(Topic, Topic.id == UserTopicState.topic_id)
        .where(UserTopicState.user_id == user.id)
        .order_by(Topic.name)
    ).all()

    return ProgressResponse(
        topics=[
            TopicProgress(
                topic=TopicOut.model_validate(topic),
                current_tier=state.current_tier,
                attempts=state.attempts,
                avg_score=state.avg_score,
                mastery=state.mastery.value,
                last_practiced_at=state.last_practiced_at,
            )
            for state, topic in rows
        ]
    )


@router.get("/api/progress/trend", response_model=TrendResponse)
def score_trend(
    n: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TrendResponse:
    rows = db.execute(
        select(Submission)
        .where(Submission.user_id == user.id)
        .order_by(desc(Submission.created_at))
        .limit(n)
    ).scalars().all()

    return TrendResponse(
        points=[
            TrendPoint(
                submission_id=s.id,
                overall_score=s.overall_score,
                created_at=s.created_at,
            )
            for s in reversed(rows)
        ]
    )


@router.get("/api/account/summary", response_model=AccountSummary)
def account_summary(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AccountSummary:
    total_problems = db.execute(select(func.count(Problem.id))).scalar_one() or 0
    submissions = db.execute(
        select(Submission).where(Submission.user_id == user.id)
    ).scalars().all()
    attempts = len(submissions)
    scores = [s.overall_score for s in submissions if s.overall_score is not None]
    avg_score = round(sum(scores) / len(scores)) if scores else 0
    solved_problem_ids = {s.problem_id for s in submissions if s.overall_score >= 80}
    return AccountSummary(
        solved_count=len(solved_problem_ids),
        total_problems=total_problems,
        avg_score=avg_score,
        attempts=attempts,
    )


@router.get("/api/recent-solved", response_model=RecentSolvedResponse)
def recent_solved(
    limit: int = Query(default=5, ge=1, le=50),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> RecentSolvedResponse:
    solved_subs = db.execute(
        select(Submission, Problem, Topic)
        .join(Problem, Problem.id == Submission.problem_id)
        .join(Topic, Topic.id == Problem.topic_id)
        .where(Submission.user_id == user.id, Submission.overall_score >= 80)
        .order_by(desc(Submission.created_at))
    ).all()

    seen = set()
    items = []
    for sub, prob, top in solved_subs:
        if prob.id not in seen:
            seen.add(prob.id)
            items.append(
                RecentSolvedItem(
                    id=str(prob.slug or prob.id),
                    title=prob.title,
                    topic=TopicOut.model_validate(top),
                )
            )
            if len(items) >= limit:
                break

    return RecentSolvedResponse(
        items=items,
        solved_count=len(seen),
    )


@router.get("/api/review/due", response_model=ReviewQueueResponse)
def review_due(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ReviewQueueResponse:
    submissions = db.execute(
        select(Submission, Problem, Topic)
        .join(Problem, Problem.id == Submission.problem_id)
        .join(Topic, Topic.id == Problem.topic_id)
        .where(Submission.user_id == user.id)
        .order_by(desc(Submission.created_at))
    ).all()

    due = []
    upcoming = []
    seen = set()
    now = datetime.now(timezone.utc)

    for sub, prob, top in submissions:
        if prob.id in seen:
            continue
        seen.add(prob.id)
        score = sub.overall_score or 0
        interval_days = 1 if score < 80 else (3 if score < 95 else 7)
        due_at = sub.created_at + timedelta(days=interval_days) if sub.created_at else now
        is_due = due_at <= now
        days_left = max(0, (due_at - now).days) if not is_due else 0

        item = ReviewQueueItem(
            id=str(prob.slug or prob.id),
            title=prob.title,
            topic=TopicOut.model_validate(top),
            due_at=due_at.isoformat(),
            last_score=score,
            reps=1,
            due_in_days=days_left,
        )
        if is_due:
            due.append(item)
        else:
            upcoming.append(item)

    return ReviewQueueResponse(
        due=due,
        upcoming=upcoming,
        due_count=len(due),
        tracked_count=len(due) + len(upcoming),
    )


@router.get("/api/insights/misconceptions", response_model=MisconceptionsResponse)
def misconceptions_summary(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MisconceptionsResponse:
    failed_subs = db.execute(
        select(Submission, Problem)
        .join(Problem, Problem.id == Submission.problem_id)
        .where(Submission.user_id == user.id, Submission.overall_score < 80)
        .order_by(desc(Submission.created_at))
        .limit(50)
    ).all()

    patterns_map = {
        "edge-cases": {
            "label": "Edge cases (empty / boundary inputs)",
            "tip": "Before submitting, dry-run code on empty input and single elements.",
            "count": 0,
            "problems": [],
        },
        "efficiency": {
            "label": "Efficiency (too slow / timed out)",
            "tip": "Replace nested loops with hash map lookups, two pointers, or binary search.",
            "count": 0,
            "problems": [],
        },
        "runtime-error": {
            "label": "Runtime errors (crashes)",
            "tip": "Guard against index-out-of-range and None before accessing values.",
            "count": 0,
            "problems": [],
        },
        "logic": {
            "label": "Core logic (wrong output)",
            "tip": "Re-read the problem statement carefully and trace failing examples on paper.",
            "count": 0,
            "problems": [],
        },
    }

    for sub, prob in failed_subs:
        scores = sub.scores or {}
        edge_score = scores.get("edge_cases", 100)
        time_score = scores.get("time_complexity", 100)
        p_name = prob.title
        if edge_score < 70:
            patterns_map["edge-cases"]["count"] += 1
            if p_name not in patterns_map["edge-cases"]["problems"]:
                patterns_map["edge-cases"]["problems"].append(p_name)
        elif time_score < 70:
            patterns_map["efficiency"]["count"] += 1
            if p_name not in patterns_map["efficiency"]["problems"]:
                patterns_map["efficiency"]["problems"].append(p_name)
        elif sub.tests_passed < sub.tests_total:
            patterns_map["logic"]["count"] += 1
            if p_name not in patterns_map["logic"]["problems"]:
                patterns_map["logic"]["problems"].append(p_name)

    items = [
        MisconceptionItem(
            tag=tag,
            label=info["label"],
            tip=info["tip"],
            count=info["count"],
            problems=info["problems"][:3],
        )
        for tag, info in patterns_map.items()
    ]
    return MisconceptionsResponse(items=items, total=len(failed_subs))


@router.get("/api/momentum", response_model=MomentumSummary)
def momentum_summary(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MomentumSummary:
    submissions = db.execute(
        select(Submission).where(Submission.user_id == user.id)
    ).scalars().all()

    now = datetime.now(timezone.utc).date()
    solved_today = 0
    solved_dates = set()
    total_xp = 0
    solved_ids = set()

    for s in submissions:
        if s.overall_score and s.overall_score >= 80:
            solved_ids.add(s.problem_id)
            total_xp += s.overall_score
            if s.created_at:
                s_date = s.created_at.date()
                solved_dates.add(s_date)
                if s_date == now:
                    solved_today += 1

    streak = 0
    cur_date = now
    while cur_date in solved_dates:
        streak += 1
        cur_date -= timedelta(days=1)

    badges = [
        Badge(
            id="first-solve",
            emoji="🎯",
            label="First Solve",
            desc="Solved your first coding problem",
            earned=len(solved_ids) >= 1,
        ),
        Badge(
            id="streak-3",
            emoji="🔥",
            label="Hot Streak",
            desc="Maintained a 3-day coding streak",
            earned=streak >= 3,
        ),
        Badge(
            id="master-5",
            emoji="🏆",
            label="High Five",
            desc="Mastered 5 distinct coding challenges",
            earned=len(solved_ids) >= 5,
        ),
    ]

    return MomentumSummary(
        xp=total_xp,
        level=max(1, total_xp // 250 + 1),
        level_progress=total_xp % 250,
        level_span=250,
        streak=streak,
        longest_streak=max(streak, 1) if solved_dates else 0,
        daily_goal=1,
        solved_today=solved_today,
        solved_count=len(solved_ids),
        badges=badges,
        earned_count=sum(1 for b in badges if b.earned),
    )

