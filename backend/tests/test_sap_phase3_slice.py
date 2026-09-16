"""
test_sap_phase3_slice.py

Comprehensive test suite verifying:
1. Days 23-44 curriculum completeness (22 days, 8 steps per day, canonical pedagogical sequence).
2. Block 1 (P2P: Days 23-28) accounting and logistics integrity.
3. Block 2 (O2C: Days 29-36) pricing, fulfillment, and revenue recognition integrity.
4. Block 3 (FI/Mfg: Days 37-44) G/L, subledgers, period-end, manufacturing order lifecycle, and Day 44 Capstone.
5. Interactive component mappings for all 9 Phase 3 visualizers.
6. 12 Phase 3 Enterprise Missions (registration, assistance rules, step evaluation, option sanitization).
7. DAG integration and remediation capsule resolution for all Phase 3 concepts.
8. Nova Manufacturing enterprise continuity (NM01, PL01, PL02, PO01, SO01, RAW1, FG01, VEND-101, CUST-501).
"""

import uuid
from unittest.mock import MagicMock, patch
import pytest

from app.data.sap_lessons import SAP_DAYS_CONTENT
from app.data.sap_lessons_phase3 import PHASE_3_DAYS_CONTENT
from app.sap.services.missions import SEED_MISSIONS, SAPMissionService
from app.sap.services.phase3_missions import PHASE_3_SEED_MISSIONS
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


# =============================================================================
# 1. Curriculum Integrity & 8-Step Architecture (Days 23 to 44)
# =============================================================================

def test_phase3_days_present():
    """Verify all 22 Phase 3 days (Days 23 to 44) are loaded in SAP_DAYS_CONTENT and PHASE_3_DAYS_CONTENT."""
    assert len(PHASE_3_DAYS_CONTENT) == 22
    for day_num in range(23, 45):
        assert day_num in SAP_DAYS_CONTENT, f"Day {day_num} missing from SAP_DAYS_CONTENT"
        assert day_num in PHASE_3_DAYS_CONTENT, f"Day {day_num} missing from PHASE_3_DAYS_CONTENT"
        day_data = SAP_DAYS_CONTENT[day_num]
        assert day_data["day_number"] == day_num
        assert len(day_data["title"]) > 5
        assert len(day_data["atomic_concepts"]) >= 1


def test_phase3_eight_step_pedagogical_structure():
    """Verify every Phase 3 day contains exactly 8 steps in the canonical sequence."""
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

    for day_num in range(23, 45):
        day_data = SAP_DAYS_CONTENT[day_num]
        steps = day_data["steps"]
        assert len(steps) == 8, f"Day {day_num} has {len(steps)} steps instead of 8"

        for idx, (step, exp_type) in enumerate(zip(steps, expected_types)):
            assert step["step_type"] == exp_type, (
                f"Day {day_num} step {idx + 1} type is '{step['step_type']}', expected '{exp_type}'"
            )
            assert len(step["title"]) > 3

            # Step-specific schema checks
            if exp_type in ("learn", "understand"):
                assert len(step.get("content_md", "")) > 10, f"Day {day_num} {exp_type} missing content_md"
            elif exp_type == "visual_example":
                assert "company_context" in step or "scenario" in step or len(step.get("content_md", "")) > 10
            elif exp_type == "interactive_practice":
                assert "component_type" in step, f"Day {day_num} interactive_practice missing 'component_type'"
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


def test_phase3_interactive_visualizers_assigned():
    """Verify each of the 9 interactive visualizers is assigned to its respective practice step."""
    expected_components = {
        23: "P2PFlow",
        26: "InventoryMovementMapper",
        27: "InvoiceMatchVisualizer",
        29: "O2CFlow",
        31: "ATPVisualizer",
        32: "DeliveryPGITracer",
        33: "BillingAccountingFlow",
        39: "InventoryMovementMapper",
        41: "ProductionOrderFlow",
        42: "CostSettlementVisualizer",
    }
    for day, comp in expected_components.items():
        practice_step = SAP_DAYS_CONTENT[day]["steps"][3]
        assert practice_step["step_type"] == "interactive_practice"
        assert practice_step.get("component_type") == comp, (
            f"Day {day} practice component was {practice_step.get('component_type')}, expected {comp}"
        )


# =============================================================================
# 2. Block 1 (P2P: Days 23–28) Technical & Accounting Integrity
# =============================================================================

def test_p2p_procurement_accounting_rules():
    """Verify P2P teaching content and assessments reflect exact SAP accounting rules."""
    # Day 26: Goods Receipt (MIGO / Mov 101)
    day26_text = _get_day_full_text(SAP_DAYS_CONTENT[26])
    assert "101" in day26_text
    assert "GR/IR" in day26_text or "211200" in day26_text
    assert "131000" in day26_text or "Inventory" in day26_text

    # Day 27: Invoice Verification (MIRO)
    day27_text = _get_day_full_text(SAP_DAYS_CONTENT[27])
    assert "MIRO" in day27_text
    assert "211200" in day27_text or "GR/IR" in day27_text
    assert "211000" in day27_text or "Vendor" in day27_text or "AP" in day27_text
    assert "MRBR" in day27_text or "tolerance" in day27_text.lower() or "price variance" in day27_text.lower()

    # Day 28: P2P Exceptions & F110
    day28_text = _get_day_full_text(SAP_DAYS_CONTENT[28])
    assert "F110" in day28_text
    assert "Proposal" in day28_text or "Payment" in day28_text


# =============================================================================
# 3. Block 2 (O2C: Days 29–36) Order-to-Cash Technical Integrity
# =============================================================================

def test_o2c_order_to_cash_accounting_rules():
    """Verify O2C teaching content and assessments reflect exact SAP pricing and accounting rules."""
    # Day 29: Condition Technique & Pricing
    day29_text = _get_day_full_text(SAP_DAYS_CONTENT[29])
    assert "PR00" in day29_text
    assert "Condition" in day29_text

    # Day 30: Sales Order Creation
    day30_text = _get_day_full_text(SAP_DAYS_CONTENT[30])
    assert "VA01" in day30_text
    assert "VBAK" in day30_text and "VBAP" in day30_text

    # Day 31: aATP & Allocation
    day31_text = _get_day_full_text(SAP_DAYS_CONTENT[31])
    assert "ATP" in day31_text
    assert "ABC" in day31_text or "PAL" in day31_text or "Alternative" in day31_text

    # Day 32: Delivery, Picking & PGI (VL01N, KOSTA, Mov 601, COGS)
    day32_text = _get_day_full_text(SAP_DAYS_CONTENT[32])
    assert "VL01N" in day32_text
    assert "Shipping Point" in day32_text or "KOSTA" in day32_text
    assert "601" in day32_text
    assert "COGS" in day32_text or "500000" in day32_text

    # Day 33: Billing + FI Integration (VF01)
    day33_text = _get_day_full_text(SAP_DAYS_CONTENT[33])
    assert "VF01" in day33_text
    assert "ERL" in day33_text or "410000" in day33_text


# =============================================================================
# 4. Block 3 (FI/Mfg: Days 35–44) Finance & Production Technical Integrity
# =============================================================================

def test_fi_and_mfg_rules_and_settlement():
    """Verify Finance and Manufacturing order lifecycle, confirmations, and KO88 settlement."""
    # Day 35: G/L Journals & Posting Keys
    day35_text = _get_day_full_text(SAP_DAYS_CONTENT[35])
    assert "FB50" in day35_text
    assert "40" in day35_text and "50" in day35_text

    # Day 38: Period End Closing
    day38_text = _get_day_full_text(SAP_DAYS_CONTENT[38])
    assert "AFAB" in day38_text
    assert "OB52" in day38_text

    # Day 41: Production Orders & Backflushing (Mov 261)
    day41_text = _get_day_full_text(SAP_DAYS_CONTENT[41])
    assert "261" in day41_text
    assert "CO01" in day41_text
    assert "CO11N" in day41_text or "AFRU" in day41_text

    # Day 42: WIP, Variance & Settlement (KO88)
    day42_text = _get_day_full_text(SAP_DAYS_CONTENT[42])
    assert "KO88" in day42_text
    assert "530000" in day42_text or "Price Difference" in day42_text or "Variance" in day42_text


def test_day44_capstone_nineteen_concept_evaluation(knowledge_engine):
    """Verify Day 44 Capstone assessment contains exactly 19 distinct concept evaluations."""
    day44 = SAP_DAYS_CONTENT[44]
    assessment_step = [s for s in day44["steps"] if s["step_type"] == "assessment"][0]
    questions = assessment_step["questions"]

    assert len(questions) == 19, f"Day 44 Capstone has {len(questions)} questions instead of 19"

    concept_slugs = [q["concept_slug"] for q in questions]
    assert len(set(concept_slugs)) == 19, "Day 44 questions must test 19 distinct concepts"

    for c_slug in concept_slugs:
        capsule = knowledge_engine.get_remediation_capsule(c_slug)
        assert capsule is not None, f"Day 44 Capstone concept '{c_slug}' has no remediation capsule in DAG"


# =============================================================================
# 5. Phase 3 Enterprise Missions (12 Missions)
# =============================================================================

PHASE_3_MISSION_SLUGS = [
    "nova-p2p-workflow-incident",
    "nova-sourcing-rfq-decision",
    "nova-invoice-3way-match-investigation",
    "nova-f110-payment-exception-run",
    "nova-o2c-order-fulfillment-crisis",
    "nova-atp-allocation-conflict",
    "nova-o2c-billing-fi-reconciliation",
    "nova-gl-period-end-closing",
    "nova-inventory-discrepancy-audit",
    "nova-mfg-shopfloor-dispatch-incident",
    "nova-mfg-production-variance-investigation",
    "nova-e2e-enterprise-cross-module-recovery",
]


def test_phase3_missions_registration():
    """Verify all 12 Phase 3 missions are registered in SEED_MISSIONS and PHASE_3_SEED_MISSIONS."""
    assert len(SEED_MISSIONS) >= 25, f"Expected at least 25 total missions, found {len(SEED_MISSIONS)}"
    assert len(PHASE_3_SEED_MISSIONS) == 12, f"Expected 12 Phase 3 missions, found {len(PHASE_3_SEED_MISSIONS)}"

    seed_slugs = {m["slug"] for m in SEED_MISSIONS}
    for slug in PHASE_3_MISSION_SLUGS:
        assert slug in seed_slugs, f"Mission '{slug}' not found in SEED_MISSIONS"

    for m in PHASE_3_SEED_MISSIONS:
        assert len(m["steps"]) >= 1
        assert m["difficulty"] in (1, 2, 3, 4)


def test_phase3_assistance_levels_configuration():
    """Verify TRAINING, GUIDED, and JOB assistance modes are configured on all Phase 3 missions."""
    for m in PHASE_3_SEED_MISSIONS:
        rules = m.get("assistance_rules", {})
        assert "TRAINING" in rules, f"Mission {m['slug']} missing TRAINING rules"
        assert "GUIDED" in rules, f"Mission {m['slug']} missing GUIDED rules"
        assert "JOB" in rules, f"Mission {m['slug']} missing JOB rules"

        # JOB mode must strictly disable hints
        job_rules = rules["JOB"]
        assert job_rules["allow_hints"] is False
        assert len(job_rules.get("hints", [])) == 0
        assert job_rules.get("show_prerequisite_primer") is False

        # TRAINING mode must provide hints
        training_rules = rules["TRAINING"]
        assert training_rules["allow_hints"] is True
        assert len(training_rules.get("hints", [])) > 0


def test_mission_step_options_are_sanitized_no_answer_leak():
    """Verify get_mission_detail strips 'is_correct' from options to prevent answer leaks."""
    user_id = uuid.uuid4()
    for seed in PHASE_3_SEED_MISSIONS:
        mock_db = MagicMock()
        mock_mission = MagicMock()
        mock_mission.slug = seed["slug"]
        mock_mission.steps = seed.get("steps", [])
        mock_mission.assistance_rules = seed.get("assistance_rules", {})
        mock_mission.id = uuid.uuid4()
        mock_db.execute.return_value.scalar_one_or_none.return_value = mock_mission
        mock_db.execute.return_value.scalars.return_value.first.return_value = None

        with patch("app.sap.services.enterprise.SAPEnterpriseService.get_or_create_instance") as mock_inst:
            mock_inst.return_value = MagicMock(state_payload={})
            detail = SAPMissionService.get_mission_detail(mock_db, user_id=user_id, slug=seed["slug"])
            assert detail is not None
            steps = detail.get("steps", [])
            assert len(steps) > 0
            for step in steps:
                options = step.get("options", [])
                for opt in options:
                    assert "is_correct" not in opt, (
                        f"Answer leak vulnerability! 'is_correct' was found in options of mission {seed['slug']}"
                    )


# =============================================================================
# 6. DAG Integration & Remediation Coverage
# =============================================================================

def test_all_phase3_concepts_have_remediation(knowledge_engine):
    """Verify all atomic concepts in Days 23-44 map to valid DAG remediation capsules."""
    for day_num in range(23, 45):
        day_data = SAP_DAYS_CONTENT[day_num]
        for concept_slug in day_data.get("atomic_concepts", []):
            capsule = knowledge_engine.get_remediation_capsule(concept_slug)
            assert capsule is not None, (
                f"Day {day_num} concept '{concept_slug}' does not resolve to any remediation capsule"
            )


# =============================================================================
# 7. Enterprise Consistency: Nova Manufacturing (NM01)
# =============================================================================

def test_nova_manufacturing_continuity():
    """Verify strict naming and code consistency for Nova Manufacturing Corp across all Phase 3 days."""
    p3_content = " ".join(
        _get_day_full_text(day)
        for day in SAP_DAYS_CONTENT.values()
        if 23 <= day["day_number"] <= 44
    )

    assert "NM01" in p3_content, "Company Code NM01 missing"
    assert "PL01" in p3_content, "Plant PL01 missing"
    assert "PO01" in p3_content, "Purchasing Org PO01 missing"
    assert "SO01" in p3_content, "Sales Org SO01 missing"
    assert "RAW1" in p3_content, "Storage Location RAW1 missing"
    assert "FG01" in p3_content, "Storage Location FG01 missing"
    assert "VEND-101" in p3_content, "Vendor VEND-101 missing"
    assert "CUST-501" in p3_content, "Customer CUST-501 missing"
    assert "DXTR-1000" in p3_content, "Product DXTR-1000 missing"

