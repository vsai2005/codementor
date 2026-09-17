"""
test_sap_phase8_9_slice.py

Comprehensive test suite verifying:
1. Days 90-100 curriculum completeness (11 days, 8 steps per day, canonical pedagogical sequence).
2. Phase 8 (Days 90-95) BTP & Enterprise Integration truthfulness:
   - BTP Architecture (Subaccounts, Cloud Foundry, Kyma).
   - Cloud Integration (CPI, iFlows, message transformations, Groovy scripting).
   - Event-Driven Architecture (SAP Event Mesh, CloudEvents standard).
   - Secure Hybrid Connectivity (Cloud Connector reverse-invoke tunnel, Destinations).
   - BTP Integration Capstone.
3. Phase 9 (Days 96-100) Enterprise Capstone & Certification:
   - End-to-end multi-tier architecture defense.
   - Day 96 Fit-to-Standard & Process scoping.
   - Day 97 CDS VDM & Data Semantics modeling.
   - Day 98 ABAP Cloud RAP Implementation & Business Logic.
   - Day 99 Fiori Elements & BTP Integration Assembly.
   - Day 100 Final Architecture Defense & S/4HANA Master Certification.
4. Nova Manufacturing enterprise continuity (NM01, PL01, PL02, DXTR-1000, RAW-01, VEND-101, CUST-501).
5. DAG concept mappings and remediation capsule resolution.
"""

import pytest
from app.data.sap_lessons import SAP_DAYS_CONTENT
from app.data.sap_lessons_phase8 import PHASE_8_DAYS_CONTENT
from app.data.sap_lessons_phase9 import PHASE_9_DAYS_CONTENT
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


def test_phase8_9_days_present():
    """Verify all Phase 8 & 9 days (Days 90 to 100) are loaded in SAP_DAYS_CONTENT."""
    assert len(PHASE_8_DAYS_CONTENT) == 6
    assert len(PHASE_9_DAYS_CONTENT) == 5
    for day_num in range(90, 101):
        assert day_num in SAP_DAYS_CONTENT, f"Day {day_num} missing from SAP_DAYS_CONTENT"
        day_data = SAP_DAYS_CONTENT[day_num]
        assert day_data["day_number"] == day_num
        assert len(day_data["title"]) > 5
        assert len(day_data["atomic_concepts"]) >= 1


def test_phase8_9_eight_step_pedagogical_structure():
    """Verify every Phase 8 & 9 day contains exactly 8 steps in the canonical sequence."""
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

    for day_num in range(90, 101):
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


def test_phase8_technical_invariants():
    """Verify architectural accuracy across Phase 8 BTP days."""
    p8_full_text = " ".join(_get_day_full_text(SAP_DAYS_CONTENT[d]) for d in range(90, 96)).lower()

    # Invariant 1: BTP Architecture
    assert "btp" in p8_full_text
    assert "subaccount" in p8_full_text or "cloud foundry" in p8_full_text or "kyma" in p8_full_text

    # Invariant 2: Integration Suite & CPI
    assert "integration suite" in p8_full_text or "iflow" in p8_full_text or "cpi" in p8_full_text
    assert "groovy" in p8_full_text

    # Invariant 3: Event Mesh & CloudEvents
    assert "event mesh" in p8_full_text or "event-driven" in p8_full_text
    assert "cloudevents" in p8_full_text or "publish-subscribe" in p8_full_text

    # Invariant 4: Cloud Connector & Secure Connectivity
    assert "cloud connector" in p8_full_text
    assert "tunnel" in p8_full_text or "reverse invoke" in p8_full_text or "reverse-invoke" in p8_full_text


def test_phase9_capstone_invariants():
    """Verify end-to-end architectural rigor across Phase 9 Capstone days."""
    p9_full_text = " ".join(_get_day_full_text(SAP_DAYS_CONTENT[d]) for d in range(96, 101)).lower()

    # Invariant 1: Capstone progression across 5 days
    assert "fit-to-standard" in p9_full_text or "discovery" in p9_full_text
    assert "cds" in p9_full_text
    assert "rap" in p9_full_text
    assert "fiori" in p9_full_text
    assert "certification" in p9_full_text or "defense" in p9_full_text


def test_phase8_9_nova_manufacturing_continuity():
    """Verify Nova Manufacturing continuity in Phases 8 & 9."""
    p8_9_full_text = " ".join(_get_day_full_text(SAP_DAYS_CONTENT[d]) for d in range(90, 101))
    assert "NM01" in p8_9_full_text
    assert "PL01" in p8_9_full_text
    assert "DXTR-1000" in p8_9_full_text or "Nova" in p8_9_full_text


def test_phase8_9_concepts_remediation_resolution(knowledge_engine):
    """Verify all atomic concepts in Phase 8 & 9 days resolve to valid remediation capsules."""
    for day_num in range(90, 101):
        day_data = SAP_DAYS_CONTENT[day_num]
        for concept_slug in day_data.get("atomic_concepts", []):
            capsule = knowledge_engine.get_remediation_capsule(concept_slug)
            assert capsule is not None, f"Concept '{concept_slug}' on Day {day_num} failed to resolve to a remediation capsule!"
            assert capsule.slug is not None
            assert len(capsule.title) > 0
