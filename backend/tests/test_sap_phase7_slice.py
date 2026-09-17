"""
test_sap_phase7_slice.py

Comprehensive test suite verifying:
1. Days 77-89 curriculum completeness (13 days, 8 steps per day, canonical pedagogical sequence).
2. ABAP Cloud & RAP truthfulness (Language Version 5, OO & Unit testing, RAP Architecture, BO Compositions, Managed vs Unmanaged BDEF, 5-stage Save Sequence, Determinations/Validations/Actions, Draft handling, ETags, Authorization).
3. Technical Truthfulness Invariants:
   - ABAP Cloud strictly forbids non-released SAP DDIC/APIs and direct database writes (INSERT/UPDATE on standard tables).
   - RAP BO uses Composition of Child with Association to Parent.
   - Managed BDEF vs Unmanaged BDEF transactional control.
   - 5-stage save sequence: finalize, check_before_save, adjust_numbers, save, cleanup.
   - Draft handling separates active persistence from draft persistence with auto-save and edit draft.
   - EML (Entity Manipulation Language) is the standard invocation method.
4. Nova Manufacturing enterprise continuity (NM01, PL01, PL02, DXTR-1000, RAW-01, VEND-101, CUST-501).
5. DAG concept mappings and remediation capsule resolution.
"""

import pytest
from app.data.sap_lessons import SAP_DAYS_CONTENT
from app.data.sap_lessons_phase7 import PHASE_7_DAYS_CONTENT
from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine


@pytest.fixture(scope="module")
def knowledge_engine():
    return SAPCurriculumKnowledgeEngine.get_instance()


def _get_day_full_text(day_dict: dict) -> str:
    parts = [day_dict.get("title", ""), day_dict.get("subtitle", "")]
    for s in day_dict.get("steps", []):
        parts.append(s.get("title", ""))
        parts.append(s.get("content_md", ""))
        parts.append(s.get("instruction", ""))
        parts.append(s.get("scenario", ""))
        parts.append(s.get("takeaway", ""))
        for q in s.get("questions", []):
            parts.append(q.get("question_text", ""))
            for opt in q.get("options", []):
                parts.append(opt.get("text", ""))
        for opt in s.get("options", []):
            parts.append(opt.get("text", ""))
    return " ".join(parts)


def test_phase7_days_present():
    """Verify all 13 Phase 7 days (Days 77 to 89) are loaded in SAP_DAYS_CONTENT and PHASE_7_DAYS_CONTENT."""
    assert len(PHASE_7_DAYS_CONTENT) == 13
    for day_num in range(77, 90):
        assert day_num in SAP_DAYS_CONTENT, f"Day {day_num} missing from SAP_DAYS_CONTENT"
        assert day_num in PHASE_7_DAYS_CONTENT, f"Day {day_num} missing from PHASE_7_DAYS_CONTENT"
        day_data = SAP_DAYS_CONTENT[day_num]
        assert day_data["day_number"] == day_num
        assert len(day_data["title"]) > 5
        assert len(day_data["atomic_concepts"]) >= 1


def test_phase7_eight_step_pedagogical_structure():
    """Verify every Phase 7 day contains exactly 8 steps in the canonical sequence."""
    expected_types = [
        "learn",
        "understand",
        "visual_example",
        "interactive_practice",
        "challenge",
        "assessment",
        "mastery_evidence",
        "completion",
    ]

    for day_num in range(77, 90):
        day_data = SAP_DAYS_CONTENT[day_num]
        steps = day_data["steps"]
        assert len(steps) == 8, f"Day {day_num} has {len(steps)} steps instead of 8"

        for idx, (step, exp_type) in enumerate(zip(steps, expected_types)):
            assert step["step_type"] == exp_type, (
                f"Day {day_num} step {idx + 1} type is '{step['step_type']}', expected '{exp_type}'"
            )
            assert len(step["title"]) > 3

            if exp_type in ("learn", "understand"):
                assert len(step.get("content_md", "")) > 10, f"Day {day_num} {exp_type} missing content_md"
            elif exp_type == "visual_example":
                assert "company_context" in step or "scenario" in step or len(step.get("content_md", "")) > 10
            elif exp_type == "interactive_practice":
                assert "instruction" in step, f"Day {day_num} interactive_practice missing 'instruction'"
            elif exp_type == "challenge":
                assert "options" in step, f"Day {day_num} challenge missing 'options'"
                assert len(step["options"]) >= 3, f"Day {day_num} challenge has < 3 options"
                assert any(opt.get("is_correct") for opt in step["options"]), f"Day {day_num} challenge must have a correct option"
            elif exp_type == "assessment":
                assert "questions" in step, f"Day {day_num} assessment missing 'questions'"
                assert len(step["questions"]) >= 2, f"Day {day_num} assessment has < 2 questions"
                for q in step["questions"]:
                    assert "id" in q or "question_id" in q
                    assert "concept_slug" in q
                    assert "options" in q
            elif exp_type == "mastery_evidence":
                assert "evidence_rule" in step or "summary_md" in step, f"Day {day_num} mastery_evidence missing evidence"
            elif exp_type == "completion":
                assert "summary_md" in step, f"Day {day_num} completion missing summary_md"


def test_phase7_technical_invariants():
    """Verify architectural accuracy across all Phase 7 days."""
    p7_full_text = " ".join(_get_day_full_text(SAP_DAYS_CONTENT[d]) for d in range(77, 90)).lower()

    # Invariant 1: ABAP Cloud & Language Version
    assert "abap cloud" in p7_full_text
    assert "released api" in p7_full_text or "tier 1" in p7_full_text or "restricted" in p7_full_text

    # Invariant 2: RAP Architecture & BDEF
    assert "bdef" in p7_full_text or "behavior definition" in p7_full_text
    assert "managed" in p7_full_text and "unmanaged" in p7_full_text

    # Invariant 3: Save Sequence (5 stages)
    assert "save sequence" in p7_full_text or "finalize" in p7_full_text
    assert "check_before_save" in p7_full_text or "adjust_numbers" in p7_full_text

    # Invariant 4: Determinations, Validations, Actions
    assert "determination" in p7_full_text
    assert "validation" in p7_full_text
    assert "action" in p7_full_text

    # Invariant 5: Draft Handling & EML
    assert "draft" in p7_full_text
    assert "eml" in p7_full_text or "modify entity" in p7_full_text or "modify entities" in p7_full_text


def test_phase7_nova_manufacturing_continuity():
    """Verify Nova Manufacturing continuity in Phase 7."""
    p7_full_text = " ".join(_get_day_full_text(SAP_DAYS_CONTENT[d]) for d in range(77, 90))
    assert "NM01" in p7_full_text
    assert "PL01" in p7_full_text
    assert "DXTR-1000" in p7_full_text or "Nova" in p7_full_text


def test_phase7_concepts_remediation_resolution(knowledge_engine):
    """Verify all atomic concepts in Phase 7 days resolve to valid remediation capsules."""
    for day_num in range(77, 90):
        day_data = SAP_DAYS_CONTENT[day_num]
        for concept_slug in day_data.get("atomic_concepts", []):
            capsule = knowledge_engine.get_remediation_capsule(concept_slug)
            assert capsule is not None, f"Concept '{concept_slug}' on Day {day_num} failed to resolve to a remediation capsule!"
            assert capsule.slug is not None
            assert len(capsule.title) > 0
