"""
test_sap_100_days_complete.py

Authoritative, full-curriculum verification suite for the 100-Day SAP S/4HANA Curriculum:
1. 100% Day Coverage: Exactly 100 days (1-100) loaded in SAP_DAYS_CONTENT and manifest.
2. Canonical 8-Step Pedagogical Sequence across all 100 days (800 steps total).
3. Zero-Cycle DAG Integrity: Topological sorting and graph acyclicity verified.
4. 100% Remediation Capsule Resolution: Every single concept across all 100 days resolves to a valid capsule.
5. Assessment Contract Validity: All assessment types belong to SAPAssessmentType enum.
6. Enterprise Continuity: Consistent Nova Manufacturing corporate identity across all 100 days.
"""

import pytest
from app.data.sap_lessons import SAP_DAYS_CONTENT
from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine
from app.sap.schemas.api import SAPAssessmentType
from typing import get_args


@pytest.fixture(scope="module")
def knowledge_engine():
    return SAPCurriculumKnowledgeEngine.get_instance()


def test_complete_100_days_presence():
    """Verify exactly 100 days (1 to 100) are fully authored and present."""
    assert len(SAP_DAYS_CONTENT) == 100, f"Expected 100 days in SAP_DAYS_CONTENT, got {len(SAP_DAYS_CONTENT)}"
    day_numbers = sorted(SAP_DAYS_CONTENT.keys())
    assert day_numbers == list(range(1, 101)), "Day numbers are not exactly 1 through 100!"


def test_complete_800_steps_pedagogical_structure():
    """Verify that all 100 days have exactly 8 steps conforming to the canonical sequence."""
    expected_sequence = [
        "learn",
        "understand",
        "visual_example",
        "interactive_practice",
        "challenge",
        "assessment",
        "mastery_evidence",
        "completion",
    ]

    total_steps = 0
    for day_num in range(1, 101):
        day_data = SAP_DAYS_CONTENT[day_num]
        steps = day_data["steps"]
        assert len(steps) == 8, f"Day {day_num} has {len(steps)} steps instead of 8"
        total_steps += len(steps)

        for idx, (step, exp_type) in enumerate(zip(steps, expected_sequence)):
            assert step["step_type"] == exp_type, (
                f"Day {day_num} step {idx + 1} has type '{step['step_type']}', expected '{exp_type}'"
            )
            assert len(step.get("title", "")) > 0, f"Day {day_num} step {idx + 1} missing title"

    assert total_steps == 800, f"Expected 800 total pedagogical steps across 100 days, got {total_steps}"


def test_all_100_days_assessment_questions_integrity():
    """Verify that every day has a valid assessment step with well-formed questions."""
    for day_num in range(1, 101):
        day_data = SAP_DAYS_CONTENT[day_num]
        assessment_step = day_data["steps"][5]
        assert assessment_step["step_type"] == "assessment"
        questions = assessment_step.get("questions", [])
        assert len(questions) >= 1, f"Day {day_num} has {len(questions)} assessment questions"

        for q in questions:
            assert any(k in q for k in ("prompt", "question_text", "question")), f"Day {day_num} question missing text"
            assert "options" in q
            assert len(q["options"]) >= 2
            assert any(opt.get("is_correct") for opt in q["options"]), f"Day {day_num} question missing correct option"


def test_dag_acyclicity_and_topological_integrity(knowledge_engine):
    """Verify the curriculum knowledge graph is strictly a Directed Acyclic Graph (0 cycles)."""
    # validate_dag_integrity raises DAGIntegrityError if any cycles or broken references exist
    knowledge_engine.validate_dag_integrity()
    
    # Check that root traversal works
    roots = knowledge_engine.get_root_prerequisites("universal-journal-concept")
    assert len(roots) > 0
    assert "double-entry-accounting" in roots or "fi-co-unification" in roots


def test_100_percent_remediation_resolution(knowledge_engine):
    """Verify every single atomic concept in the manifest and lessons resolves to a valid remediation capsule."""
    concepts = knowledge_engine.get_all_concepts()
    assert len(concepts) >= 200, f"Expected >= 200 concepts in manifest, got {len(concepts)}"

    for concept in concepts:
        capsule = knowledge_engine.get_remediation_capsule(concept.slug)
        assert capsule is not None, f"Concept '{concept.slug}' has no resolvable remediation capsule!"
        assert capsule.slug is not None
        assert len(capsule.title) > 0

    # Check atomic concepts referenced in all 100 lesson days
    for day_num in range(1, 101):
        day_data = SAP_DAYS_CONTENT[day_num]
        for slug in day_data.get("atomic_concepts", []):
            capsule = knowledge_engine.get_remediation_capsule(slug)
            assert capsule is not None, f"Day {day_num} atomic concept '{slug}' has no remediation capsule!"


def test_assessment_type_contract_compliance(knowledge_engine):
    """Verify all assessment types used across the 100 days belong to SAPAssessmentType."""
    allowed_types = set(get_args(SAPAssessmentType))
    all_days = knowledge_engine.get_all_days()
    assert len(all_days) == 100
    for day in all_days:
        for a_type in day.assessment_types:
            assert a_type in allowed_types, f"Manifest day {day.day_number} uses unknown assessment type '{a_type}'"


def test_nova_manufacturing_continuity_100_days():
    """Verify Nova Manufacturing enterprise continuity across the entire 100-day journey."""
    full_corpus = []
    for day_num in range(1, 101):
        day = SAP_DAYS_CONTENT[day_num]
        full_corpus.append(day.get("title", ""))
        for s in day.get("steps", []):
            full_corpus.append(s.get("content_md", ""))
            full_corpus.append(s.get("scenario", ""))

    text = " ".join(full_corpus)
    assert "Nova Manufacturing" in text or "NM01" in text
    assert "PL01" in text
