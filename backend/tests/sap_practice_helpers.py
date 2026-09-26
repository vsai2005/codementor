"""Builds genuine SAP Practice evidence for tests that need a day's Practice completed.

Answers are derived from the authoritative lesson content, exactly as a learner who chose
the correct option on every graded practice step would submit them.
"""

from __future__ import annotations

from app.sap.services.practice import practice_answer_key, practice_evidence_steps


def correct_practice_answers(day_number: int) -> dict[str, str]:
    return {s["step_id"]: practice_answer_key(s) for s in practice_evidence_steps(day_number)}


def practice_payload(day_number: int) -> dict:
    return {"day_number": day_number, "answers": correct_practice_answers(day_number)}
