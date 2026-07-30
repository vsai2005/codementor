"""Request/response models. Every endpoint gets both — no bare dicts."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.schemas.review import Review


class GoogleLoginRequest(BaseModel):
    id_token: str


class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    avatar_url: str | None = None

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    user: UserOut


class TopicOut(BaseModel):
    id: uuid.UUID
    slug: str
    name: str

    model_config = {"from_attributes": True}


class ProblemSummary(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    difficulty_tier: int
    topic: TopicOut

    model_config = {"from_attributes": True}


class ProblemDetail(ProblemSummary):
    statement_md: str
    constraints_md: str
    optimal_time: str
    optimal_space: str
    entry_point: str
    starter_code: dict[str, str]


class ProblemPage(BaseModel):
    items: list[ProblemSummary]
    page: int
    page_size: int
    total: int


class RunRequest(BaseModel):
    problem_id: uuid.UUID
    language: Literal["python"] = "python"
    code: str = Field(min_length=1, max_length=50_000)


class TestCaseResult(BaseModel):
    index: int
    passed: bool
    status: str
    runtime_ms: int
    stdout: str = ""
    stderr: str = ""


class TestsResponse(BaseModel):
    passed: int
    total: int
    all_passed: bool
    results: list[TestCaseResult]


class DifficultyChange(BaseModel):
    from_tier: int = Field(alias="from")
    to_tier: int = Field(alias="to")
    rolling_score: float
    banner: str

    model_config = {"populate_by_name": True}


class SubmissionResponse(BaseModel):
    submission_id: uuid.UUID
    tests: TestsResponse
    review: Review
    difficulty: DifficultyChange


class SubmissionHistoryItem(BaseModel):
    id: uuid.UUID
    problem_id: uuid.UUID
    overall_score: int
    tests_passed: int
    tests_total: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TopicProgress(BaseModel):
    topic: TopicOut
    current_tier: int
    attempts: int
    avg_score: float
    mastery: str
    last_practiced_at: datetime | None


class ProgressResponse(BaseModel):
    topics: list[TopicProgress]


class TrendPoint(BaseModel):
    submission_id: uuid.UUID
    overall_score: int
    created_at: datetime


class TrendResponse(BaseModel):
    points: list[TrendPoint]


class MemoryNoteOut(BaseModel):
    id: str
    content: str
    similarity: float


class TutorRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    problem_id: uuid.UUID | None = None


class TutorResponse(BaseModel):
    reply: str
    retrieved_notes: list[MemoryNoteOut]


class HealthResponse(BaseModel):
    status: Literal["ok"]


class ErrorResponse(BaseModel):
    detail: str
    retry_after_s: int | None = None
