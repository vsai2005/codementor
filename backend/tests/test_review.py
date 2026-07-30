"""Review pipeline tests. The LLM is always mocked -- no network in tests."""

import pytest

from app.schemas.review import WEIGHTS, Scores, compute_overall_score
from app.services.llm import LLMClient, LLMError, LLMTimeout, extract_json
from app.services.review import ReviewService, degraded_review
from app.services.sandbox import ExecutionReport, TestResult

VALID_JSON = """{
  "scores": {"correctness": 100, "time_complexity": 55, "space_complexity": 80,
             "readability": 92, "edge_cases": 73},
  "detected_complexity": {"time": "O(n^2)", "space": "O(1)"},
  "optimal_complexity": {"time": "O(n)", "space": "O(n)"},
  "summary": "Works, but a nested loop where a hashmap gives O(n).",
  "issues": [{"severity": "major", "title": "Nested loop", "detail": "...", "line": 4}],
  "improvement_hint": "Store seen values in a dict as you iterate.",
  "weak_topics": ["hashmaps", "Time Complexity Analysis"]
}"""


class FakeLLM(LLMClient):
    def __init__(self, *responses, raises=None):
        self.responses = list(responses)
        self.raises = raises
        self.calls = 0

    def complete(self, prompt, *, system="", temperature=0.2,
                 max_tokens=1500, timeout=6.0):
        self.calls += 1
        if self.raises:
            raise self.raises
        return self.responses.pop(0) if self.responses else "{}"


def report(passed: int, total: int, timed_out: bool = False) -> ExecutionReport:
    results = []
    for i in range(total):
        ok = i < passed
        status = "timeout" if (timed_out and not ok) else ("ok" if ok else "wrong_answer")
        results.append(TestResult(i, ok, status, 12))
    return ExecutionReport(results=results)


def run(service, rep):
    return service.review(
        problem_title="Two Sum", statement_md="Find two indices.",
        optimal_time="O(n)", optimal_space="O(n)",
        language="python", code="def two_sum(a, t): return []", report=rep,
    )


# --- scoring maths --------------------------------------------------------

def test_weights_sum_to_one():
    assert sum(WEIGHTS.values()) == pytest.approx(1.0)


def test_weight_math_against_hand_calculation():
    # 0.40*100 + 0.25*55 + 0.15*92 + 0.12*73 + 0.08*80
    # = 40 + 13.75 + 13.8 + 8.76 + 6.4 = 82.71 -> 83
    s = Scores(correctness=100, time_complexity=55, space_complexity=80,
               readability=92, edge_cases=73)
    assert compute_overall_score(s) == 83


def test_wrong_answer_is_capped_at_fifty():
    s = Scores(correctness=60, time_complexity=100, space_complexity=100,
               readability=100, edge_cases=100)
    assert compute_overall_score(s) <= 50


def test_cap_does_not_inflate_a_genuinely_low_score():
    s = Scores(correctness=0, time_complexity=0, space_complexity=0,
               readability=10, edge_cases=0)
    assert compute_overall_score(s) < 50


def test_perfect_solution_scores_one_hundred():
    s = Scores(correctness=100, time_complexity=100, space_complexity=100,
               readability=100, edge_cases=100)
    assert compute_overall_score(s) == 100


# --- happy path -----------------------------------------------------------

def test_valid_llm_json_is_parsed_and_scored():
    svc = ReviewService(FakeLLM(VALID_JSON))
    review = run(svc, report(5, 5))

    assert review.review_degraded is False
    assert review.scores.correctness == 100
    assert review.overall_score == 83
    assert review.detected_complexity.time == "O(n^2)"
    assert review.weak_topics == ["hashmaps", "time-complexity-analysis"]


def test_fenced_json_is_still_accepted():
    svc = ReviewService(FakeLLM(f"Here you go:\n```json\n{VALID_JSON}\n```\nHope that helps!"))
    review = run(svc, report(5, 5))
    assert review.review_degraded is False
    assert review.overall_score == 83


def test_test_results_override_llm_correctness_claim():
    # Model claims 100 but only 3 of 5 tests actually passed.
    svc = ReviewService(FakeLLM(VALID_JSON))
    review = run(svc, report(3, 5))
    assert review.scores.correctness == 60, "LLM must not get a vote on correctness"
    assert review.overall_score <= 50, "wrong answer must be capped"


# --- degradation ----------------------------------------------------------

def test_malformed_json_retries_once_then_degrades():
    llm = FakeLLM("not json at all", "still not json")
    review = run(ReviewService(llm), report(5, 5))

    assert llm.calls == 2, "must retry exactly once"
    assert review.review_degraded is True
    assert review.scores.correctness == 100


def test_malformed_then_valid_recovers_on_retry():
    llm = FakeLLM("{ broken", VALID_JSON)
    review = run(ReviewService(llm), report(5, 5))

    assert llm.calls == 2
    assert review.review_degraded is False
    assert review.overall_score == 83


def test_schema_violation_is_treated_as_failure():
    bad = '{"scores": {"correctness": 500}, "summary": "x"}'
    llm = FakeLLM(bad, bad)
    review = run(ReviewService(llm), report(5, 5))
    assert review.review_degraded is True


def test_llm_timeout_degrades_without_raising():
    llm = FakeLLM(raises=LLMTimeout("timed out"))
    review = run(ReviewService(llm), report(4, 5))

    assert review.review_degraded is True
    assert review.scores.correctness == 80
    assert llm.calls == 2


def test_llm_transport_error_degrades():
    review = run(ReviewService(FakeLLM(raises=LLMError("503"))), report(5, 5))
    assert review.review_degraded is True


def test_sandbox_timeout_skips_the_llm_entirely():
    llm = FakeLLM(VALID_JSON)
    review = run(ReviewService(llm), report(0, 3, timed_out=True))

    assert llm.calls == 0, "PRD 5.7: sandbox timeout means no LLM call"
    assert review.overall_score == 0
    assert review.review_degraded is True
    assert "Time Limit Exceeded" in review.summary


def test_degraded_review_is_still_a_valid_review_object():
    review = degraded_review(report(3, 5))
    assert 0 <= review.overall_score <= 100
    assert review.improvement_hint
    assert review.review_degraded is True


# --- json extraction ------------------------------------------------------

@pytest.mark.parametrize("raw", [
    '{"a": 1}',
    '```json\n{"a": 1}\n```',
    '```\n{"a": 1}\n```',
    'Sure! {"a": 1} Let me know if you need more.',
])
def test_extract_json_handles_common_model_wrappers(raw):
    assert extract_json(raw) == {"a": 1}


def test_extract_json_raises_on_garbage():
    with pytest.raises(ValueError):
        extract_json("there is no json here")
