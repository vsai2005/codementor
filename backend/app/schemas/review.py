"""Review schema + scoring (PRD 3.1). The LLM must match this exactly."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

Severity = Literal["minor", "major", "critical"]

# PRD 3.1 -- these must sum to 1.0
WEIGHTS: dict[str, float] = {
    "correctness": 0.40,
    "time_complexity": 0.25,
    "readability": 0.15,
    "edge_cases": 0.12,
    "space_complexity": 0.08,
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9

WRONG_ANSWER_CAP = 50


class Scores(BaseModel):
    correctness: int = Field(ge=0, le=100)
    time_complexity: int = Field(ge=0, le=100)
    space_complexity: int = Field(ge=0, le=100)
    readability: int = Field(ge=0, le=100)
    edge_cases: int = Field(ge=0, le=100)


class Complexity(BaseModel):
    time: str
    space: str


class Issue(BaseModel):
    severity: Severity
    title: str
    detail: str
    line: int | None = None


class Review(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    scores: Scores
    detected_complexity: Complexity
    optimal_complexity: Complexity
    summary: str
    issues: list[Issue] = Field(default_factory=list)
    improvement_hint: str
    weak_topics: list[str] = Field(default_factory=list)
    review_degraded: bool = False

    @field_validator("weak_topics")
    @classmethod
    def _normalise_topics(cls, v: list[str]) -> list[str]:
        seen, out = set(), []
        for t in v:
            slug = t.strip().lower().replace(" ", "-")
            if slug and slug not in seen:
                seen.add(slug)
                out.append(slug)
        return out


class LLMReviewDraft(BaseModel):
    """What the LLM is allowed to return.

    overall_score is deliberately absent -- the server computes it. Letting the
    model do its own arithmetic is how the weights silently stop being the
    weights, and it makes the wrong-answer cap unenforceable.
    """

    scores: Scores
    detected_complexity: Complexity
    optimal_complexity: Complexity
    summary: str
    issues: list[Issue] = Field(default_factory=list)
    improvement_hint: str
    weak_topics: list[str] = Field(default_factory=list)


def compute_overall_score(scores: Scores) -> int:
    """Weighted sum, then the wrong-answer cap. Order matters."""
    weighted = sum(WEIGHTS[field] * getattr(scores, field) for field in WEIGHTS)
    overall = int(round(weighted))
    if scores.correctness < 100:
        overall = min(overall, WRONG_ANSWER_CAP)
    return max(0, min(100, overall))
