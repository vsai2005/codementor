from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import Submission, Topic, User, UserTopicState
from app.schemas.api import (
    ProgressResponse,
    TopicOut,
    TopicProgress,
    TrendPoint,
    TrendResponse,
)

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("/topics", response_model=ProgressResponse)
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


@router.get("/trend", response_model=TrendResponse)
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
            TrendPoint(submission_id=s.id, overall_score=s.overall_score,
                       created_at=s.created_at)
            for s in reversed(rows)
        ]
    )
