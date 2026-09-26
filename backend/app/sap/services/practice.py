"""SAP Practice Evidence Grading.

Practice completion is server-authoritative: a day's Practice counts as completed only
when the learner submits answers that the server grades as correct against the answer
keys authored in SAP_DAYS_CONTENT. The client never supplies a pass flag or score.

A day's *practice evidence steps* are its Practice-phase steps (interactive practice lab
and scenario challenge) that carry exactly one authored `is_correct` option. Every one of
the 100 days has at least one such step (its scenario challenge).
"""

from __future__ import annotations

from typing import Any

from app.data.sap_lessons import SAP_DAYS_CONTENT

PRACTICE_PHASE_STEP_TYPES = frozenset({"interactive_practice", "practice", "challenge"})

# Option fields that reveal the answer key or its rationale before grading.
PRACTICE_SENSITIVE_OPTION_KEYS = frozenset({
    "is_correct", "correct", "explanation", "consequence", "rationale",
})


class SAPPracticeEvidenceError(ValueError):
    """Submitted practice evidence is malformed or does not belong to this day's Practice."""


def practice_answer_key(step: dict[str, Any]) -> str | None:
    """Returns the single correct option id of a gradable Practice-phase step, else None."""
    if step.get("step_type") not in PRACTICE_PHASE_STEP_TYPES:
        return None
    options = step.get("options")
    if not isinstance(options, list):
        return None
    correct = [o.get("id") for o in options if isinstance(o, dict) and o.get("is_correct") is True]
    if len(correct) != 1 or not isinstance(correct[0], str):
        return None
    return correct[0]


def practice_evidence_steps(day_number: int) -> list[dict[str, Any]]:
    """Returns the canonical, server-gradable Practice steps for a day (authoritative data)."""
    lesson = SAP_DAYS_CONTENT.get(day_number)
    if not lesson:
        return []
    return [s for s in lesson.get("steps", []) if practice_answer_key(s) is not None]


def grade_practice_submission(day_number: int, answers: dict[str, Any]) -> list[dict[str, Any]]:
    """Grades a practice submission against the day's authoritative answer keys.

    Raises SAPPracticeEvidenceError (never grades) when the submission references a step
    that is not one of this day's practice evidence steps, omits a required step, or
    selects an option that does not exist on the step. Returns one result per required step.
    """
    steps = practice_evidence_steps(day_number)
    if not steps:
        raise SAPPracticeEvidenceError(
            f"SAP Day {day_number} has no server-gradable practice activity."
        )
    if not isinstance(answers, dict) or not answers:
        raise SAPPracticeEvidenceError("Practice answers are required.")

    by_id = {s["step_id"]: s for s in steps}
    unknown = sorted(k for k in answers if k not in by_id)
    if unknown:
        raise SAPPracticeEvidenceError(
            f"Step(s) {unknown} are not practice activities of SAP Day {day_number}."
        )
    missing = [sid for sid in by_id if sid not in answers]
    if missing:
        raise SAPPracticeEvidenceError(
            f"Practice answers for step(s) {missing} are required for SAP Day {day_number}."
        )

    results: list[dict[str, Any]] = []
    for step_id, step in by_id.items():
        selected = answers[step_id]
        options = {o.get("id"): o for o in step["options"] if isinstance(o, dict)}
        if not isinstance(selected, str) or selected not in options:
            raise SAPPracticeEvidenceError(
                f"Option '{selected}' is not a valid choice for practice step '{step_id}'."
            )
        chosen = options[selected]
        results.append({
            "step_id": step_id,
            "correct": selected == practice_answer_key(step),
            "feedback": chosen.get("explanation") or chosen.get("consequence"),
        })
    return results
