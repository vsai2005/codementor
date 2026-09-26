"""Shared model of how SAP concepts can be earned, for reachability invariants.

Mirrors the evidence rules of the services:
- SAPAssessmentService.evaluate credits each question's concept_slug, falling back to the
  step's concept_slug, then the day's first atomic concept (question-less assessments
  credit only the step's concept_slug). Waived-day challenges use the same evaluator.
- Placement awards only concepts the diagnostic demonstrated.
- A mission awards its concept_slugs once its prerequisites are met (difficulty 1: always).
"""

from __future__ import annotations

from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine
from app.data.sap_lessons import SAP_DAYS_CONTENT
from app.sap.data.placement_questions import EXPERIENCED_QUESTIONS, NOT_SURE_QUESTIONS
from app.sap.services.missions import SAPMissionRegistry


def assessment_evidence_concepts(day_number: int) -> set[str]:
    lesson = SAP_DAYS_CONTENT[day_number]
    step = next(s for s in lesson["steps"] if s["step_type"] == "assessment")
    root = step.get("concept_slug") or (lesson.get("atomic_concepts") or [f"sap-day-{day_number}"])[0]
    questions = step.get("questions") or []
    if questions:
        return {q.get("concept_slug") or root for q in questions}
    return {step["concept_slug"]} if step.get("concept_slug") else set()


def placement_concepts() -> set[str]:
    return {q["concept_slug"] for q in EXPERIENCED_QUESTIONS + NOT_SURE_QUESTIONS if q.get("concept_slug")}


def mission_fixpoint(seed_concepts: set[str]) -> tuple[set[str], set[str]]:
    """Returns (earnable concepts, reachable mission slugs) starting from seed_concepts."""
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    earnable = {c for c in seed_concepts if engine.get_concept(c) is not None}
    reachable: set[str] = set()
    changed = True
    while changed:
        changed = False
        for m in SAPMissionRegistry.get_all():
            if m["slug"] in reachable:
                continue
            if m["difficulty"] <= 1 or all(p in earnable for p in m["prerequisite_concepts"]):
                reachable.add(m["slug"])
                earnable |= set(m["concept_slugs"])
                changed = True
    return earnable, reachable


def unresolved_prerequisites(earnable: set[str], enforced_only: bool = False) -> list[tuple[str, str]]:
    """Prerequisites not in `earnable`. enforced_only: skip difficulty-1 missions, whose
    prerequisites are advisory (entry missions are open to every learner)."""
    return [
        (m["slug"], p)
        for m in SAPMissionRegistry.get_all()
        if not (enforced_only and m["difficulty"] <= 1)
        for p in m["prerequisite_concepts"]
        if p not in earnable
    ]


def correct_assessment_answers(day_number: int) -> dict[str, str]:
    step = next(s for s in SAP_DAYS_CONTENT[day_number]["steps"] if s["step_type"] == "assessment")
    return {
        (q.get("id") or q.get("question_id")): next(o["id"] for o in q["options"] if o.get("is_correct"))
        for q in step["questions"]
    }


def wrong_assessment_answers(day_number: int) -> dict[str, str]:
    step = next(s for s in SAP_DAYS_CONTENT[day_number]["steps"] if s["step_type"] == "assessment")
    return {
        (q.get("id") or q.get("question_id")): next(o["id"] for o in q["options"] if not o.get("is_correct"))
        for q in step["questions"]
    }
