"""Review pipeline, PRD 5.4 steps 3-6 and the 5.7 failure table.

Timeout note: PRD 5.7 says degrade at 15s while PRD 4.4 gives the frontend an
8s budget -- as written the user sees an error while the backend is still
waiting. The whole request must fit in 8s p95, so the LLM call gets 6s and the
first retry gets 4s: worst case ~10s, and degradation is well inside the
frontend's patience. LLM_TIMEOUT_S is env-tunable if the budget changes.
"""

from __future__ import annotations

import logging
import os

from pydantic import ValidationError

from app.schemas.review import (
    Complexity,
    Issue,
    LLMReviewDraft,
    Review,
    Scores,
    compute_overall_score,
)
from app.services.llm import LLMClient, LLMError, extract_json
from app.services.sandbox import ExecutionReport

log = logging.getLogger(__name__)

LLM_TIMEOUT_S = float(os.getenv("LLM_TIMEOUT_S", "6.0"))
LLM_RETRY_TIMEOUT_S = float(os.getenv("LLM_RETRY_TIMEOUT_S", "4.0"))

SYSTEM_PROMPT = """You are a senior software engineer reviewing a candidate's \
solution. You are precise, specific and terse. You never praise code you would \
not merge.

Return ONLY a single JSON object. No prose, no markdown fences, no commentary.

Required shape:
{
  "scores": {"correctness": int, "time_complexity": int, "space_complexity": int,
             "readability": int, "edge_cases": int},
  "detected_complexity": {"time": str, "space": str},
  "optimal_complexity": {"time": str, "space": str},
  "summary": str,
  "issues": [{"severity": "minor"|"major"|"critical", "title": str,
              "detail": str, "line": int|null}],
  "improvement_hint": str,
  "weak_topics": [str]
}

All scores are 0-100. Do not output an overall score -- the server computes it.
The `correctness` score is dictated by the test results supplied to you; do not
guess it and do not override it."""


def build_prompt(problem_title: str, statement_md: str, optimal_time: str,
                 optimal_space: str, language: str, code: str,
                 report: ExecutionReport) -> str:
    lines = [
        f"# Problem: {problem_title}",
        statement_md.strip(),
        "",
        f"Optimal complexity: time {optimal_time}, space {optimal_space}",
        "",
        f"# Candidate submission ({language})",
        "```",
        code.strip(),
        "```",
        "",
        "# Test results (authoritative -- these are real executions, not guesses)",
        f"Passed {report.passed_count} of {report.total}.",
    ]
    for r in report.results:
        verdict = "PASS" if r.passed else f"FAIL ({r.status})"
        detail = f" -- {r.stderr[:200]}" if r.stderr else ""
        lines.append(f"  case {r.index}: {verdict} in {r.runtime_ms}ms{detail}")

    pct = int(100 * report.passed_count / report.total) if report.total else 0
    lines += [
        "",
        f"Set correctness to exactly {pct}.",
        "Review the code for complexity, readability and edge-case handling.",
    ]
    return "\n".join(lines)


def degraded_review(report: ExecutionReport, optimal_time: str = "unknown",
                    optimal_space: str = "unknown", note: str = "") -> Review:
    """Tests-only review, used whenever the LLM path fails (PRD 5.7).

    Still a real, useful answer: the user learns whether their code works. The
    non-correctness dimensions are left at 0 rather than guessed, and the
    degraded flag tells the UI to say so.
    """
    correctness = int(100 * report.passed_count / report.total) if report.total else 0
    scores = Scores(correctness=correctness, time_complexity=0, space_complexity=0,
                    readability=0, edge_cases=0)

    if report.timed_out:
        summary = "Time Limit Exceeded. Your solution did not finish within the limit."
        issues = [Issue(severity="critical", title="Time Limit Exceeded",
                        detail="At least one test case exceeded the 5s CPU budget.")]
        scores = Scores(correctness=0, time_complexity=0, space_complexity=0,
                        readability=0, edge_cases=0)
    elif correctness == 100:
        summary = "All tests passed. Detailed review is unavailable right now."
        issues = []
    else:
        summary = (f"{report.passed_count} of {report.total} tests passed. "
                   "Detailed review is unavailable right now.")
        issues = [Issue(severity="major", title="Failing tests",
                        detail="Some test cases did not produce the expected output.")]

    return Review(
        overall_score=compute_overall_score(scores),
        scores=scores,
        detected_complexity=Complexity(time="unknown", space="unknown"),
        optimal_complexity=Complexity(time=optimal_time, space=optimal_space),
        summary=summary + (f" ({note})" if note else ""),
        issues=issues,
        improvement_hint="Re-submit to get a full review.",
        weak_topics=[],
        review_degraded=True,
    )


class ReviewService:
    def __init__(self, client: LLMClient) -> None:
        self._client = client

    def review(self, *, problem_title: str, statement_md: str, optimal_time: str,
               optimal_space: str, language: str, code: str,
               report: ExecutionReport) -> Review:
        # PRD 5.7: sandbox timeout means no LLM call at all, score 0.
        if report.timed_out:
            return degraded_review(report, optimal_time, optimal_space)

        prompt = build_prompt(problem_title, statement_md, optimal_time,
                              optimal_space, language, code, report)

        draft = self._attempt(prompt, LLM_TIMEOUT_S)
        if draft is None:
            log.warning("LLM review failed, retrying once")
            draft = self._attempt(prompt, LLM_RETRY_TIMEOUT_S)
        if draft is None:
            log.warning("LLM review failed twice, degrading")
            return degraded_review(report, optimal_time, optimal_space,
                                   note="AI reviewer unavailable")

        # Test results are authoritative -- the model does not get a vote on
        # correctness, whatever it claimed.
        actual = int(100 * report.passed_count / report.total) if report.total else 0
        scores = draft.scores.model_copy(update={"correctness": actual})

        return Review(
            overall_score=compute_overall_score(scores),
            scores=scores,
            detected_complexity=draft.detected_complexity,
            optimal_complexity=draft.optimal_complexity,
            summary=draft.summary,
            issues=draft.issues,
            improvement_hint=draft.improvement_hint,
            weak_topics=draft.weak_topics,
            review_degraded=False,
        )

    def _attempt(self, prompt: str, timeout: float) -> LLMReviewDraft | None:
        try:
            raw = self._client.complete(prompt, system=SYSTEM_PROMPT,
                                        temperature=0.2, timeout=timeout)
            return LLMReviewDraft.model_validate(extract_json(raw))
        except (LLMError, ValidationError, ValueError, KeyError, TypeError) as exc:
            log.info("LLM attempt failed: %s: %s", type(exc).__name__, exc)
            return None
