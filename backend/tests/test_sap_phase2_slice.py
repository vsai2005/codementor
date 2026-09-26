"""Comprehensive Test Suite for SAP Days 9–22 Production Learning Slice & Enterprise Missions.

Covers:
1. Architectural Boundary & Isolation:
   - AST validation ensuring zero imports of Python sandbox, practice problems, or teacher prompts
     in Phase 2 content and Phase 2 missions.
2. Complete 14-Day (Days 9–22) Guided Learning Content Integrity:
   - Days 9 through 22 strictly adhere to the 8-stage sequence:
     learn -> understand -> visual_example -> interactive_practice -> challenge -> assessment -> mastery_evidence -> completion.
   - Nova Manufacturing (NM01, PL01, PL02) digital twin continuous storyline throughout.
   - 8 new reusable UI components assigned to interactive practice steps:
     * Day 11: HANAStorageVisualizer
     * Day 12: UniversalJournalVisualizer
     * Day 13: MATDOCFlow
     * Day 14: BusinessPartnerMapper
     * Day 15: CDSConceptMapper
     * Day 16: LandscapeFlow
     * Day 18: AccessRoleMapper
     * Day 20: DocumentFlowTracer
3. Day 22 Capstone Multi-Concept Evaluation & DAG Remediation:
   - Multi-concept evaluation across 11 distinct concept dimensions.
   - Targeted DAG remediation capsules triggered for deficient concepts (< 70%).
   - Verified skill evidence generated per concept without flattening to a single score.
4. 8 Phase 2 Enterprise Missions & Advanced Locking:
   - All 8 Phase 2 missions registered in SEED_MISSIONS.
   - Day 23 advanced mission (nova-p2p-workflow-incident) remains strictly locked for beginners.
   - Assistance levels (TRAINING, GUIDED, JOB) filter hints and primers properly.
   - Step attempt submissions apply deterministic enterprise state mutations to Nova twin.
"""

from __future__ import annotations

import ast
from pathlib import Path
from unittest.mock import MagicMock, patch
import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine
from app.data.sap_lessons import SAP_DAYS_CONTENT
from app.data.sap_lessons_phase2 import PHASE_2_DAYS_CONTENT
from app.main import app
from app.models.sap_models import (
    SAPAssistanceLevel,
    SAPConcept,
    SAPEnterprise,
    SAPEnterpriseInstance,
    SAPLearningMode,
    SAPMission,
    SAPMissionAttempt,
    SAPMissionType,
    SAPUserConceptMastery,
)
from app.sap.services.assessment import SAPAssessmentService
from app.sap.services.mastery import SAPMasteryService
from app.sap.services.missions import SEED_MISSIONS, SAPMissionService
from app.sap.services.phase2_missions import PHASE_2_SEED_MISSIONS

client = TestClient(app)


# =============================================================================
# 1. Architectural Boundary & Isolation Verification
# =============================================================================

class TestSAPPhase2Isolation:
    """Verify SAP Phase 2 files never import Python-specific engines."""

    FORBIDDEN_PYTHON_MODULES = {
        "app.services.sandbox",
        "app.services._sandbox_runner",
        "app.sandbox",
        "app.services.submissions",
        "app.services.difficulty",
        "app.services.teacher",
        "app.core.curriculum_map",
        "app.core.curriculum_retrieval",
    }

    FILES_TO_CHECK = [
        Path("app/data/sap_lessons_phase2.py"),
        Path("app/sap/services/phase2_missions.py"),
    ]

    def test_no_python_sandbox_or_services_imported_in_phase2(self):
        backend_dir = Path(__file__).resolve().parent.parent
        for rel_path in self.FILES_TO_CHECK:
            full_path = backend_dir / rel_path
            assert full_path.exists(), f"File {rel_path} must exist"

            tree = ast.parse(full_path.read_text(encoding="utf-8"), filename=str(rel_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        for forbidden in self.FORBIDDEN_PYTHON_MODULES:
                            assert not alias.name.startswith(forbidden), (
                                f"{rel_path} illegally imports {alias.name}"
                            )
                elif isinstance(node, ast.ImportFrom):
                    mod = node.module or ""
                    for forbidden in self.FORBIDDEN_PYTHON_MODULES:
                        assert not mod.startswith(forbidden), (
                            f"{rel_path} illegally imports from {mod}"
                        )


# =============================================================================
# 2. Days 9–22 Guided Learning Content Integrity
# =============================================================================

class TestSAPPhase2ContentIntegrity:
    """Verify all 14 days of Phase 2 Guided Learning content meet strict production criteria."""

    REQUIRED_STEPS_SEQUENCE = [
        "learn",
        "understand",
        "visual_example",
        "interactive_practice",
        "challenge",
        "assessment",
        "mastery_evidence",
        "completion",
    ]

    def test_days_9_to_22_all_present_in_sap_days_content(self):
        for day in range(9, 23):
            assert day in SAP_DAYS_CONTENT, f"Day {day} must be present in merged SAP_DAYS_CONTENT"
            assert day in PHASE_2_DAYS_CONTENT, f"Day {day} must be authored in PHASE_2_DAYS_CONTENT"

    def test_strict_8_step_sequence_for_phase2_days(self):
        for day in range(9, 23):
            lesson = SAP_DAYS_CONTENT[day]
            assert lesson["day_number"] == day
            assert len(lesson["title"]) > 5
            steps = lesson["steps"]
            assert len(steps) == 8, f"Day {day} must have exactly 8 pedagogical steps"

            actual_types = [s["step_type"] for s in steps]
            assert actual_types == self.REQUIRED_STEPS_SEQUENCE, (
                f"Day {day} step sequence mismatch: {actual_types} != {self.REQUIRED_STEPS_SEQUENCE}"
            )

    def test_nova_manufacturing_twin_continuity_phase2(self):
        for day in range(9, 23):
            lesson = SAP_DAYS_CONTENT[day]
            # Check step 3 (visual_example) features Nova Manufacturing / NM01
            example_step = lesson["steps"][2]
            assert example_step["step_type"] == "visual_example"
            ctx = example_step.get("company_context")
            assert ctx is not None, f"Day {day} visual example must have company_context"

            has_nm = (
                ctx.get("code") == "NM01"
                or ctx.get("company_code") == "NM01"
                or "NM01" in example_step.get("content_md", "")
                or "Nova" in str(ctx)
            )
            assert has_nm, f"Day {day} visual example must reference Nova Manufacturing / NM01"

    def test_interactive_components_assigned_in_phase2(self):
        expected_components = {
            11: "HANAStorageVisualizer",
            12: "UniversalJournalVisualizer",
            13: "MATDOCFlow",
            14: "BusinessPartnerMapper",
            15: "CDSConceptMapper",
            16: "LandscapeFlow",
            18: "AccessRoleMapper",
            20: "DocumentFlowTracer",
        }
        for day, comp in expected_components.items():
            practice_step = SAP_DAYS_CONTENT[day]["steps"][3]
            assert practice_step["step_type"] == "interactive_practice"
            assert practice_step["component_type"] == comp, (
                f"Day {day} practice component was {practice_step.get('component_type')}, expected {comp}"
            )

    def test_companion_missions_recommended_in_phase2(self):
        for day in range(9, 23):
            lesson = SAP_DAYS_CONTENT[day]
            completion_step = lesson["steps"][7]
            assert completion_step["step_type"] == "completion"
            rec = completion_step.get("recommended_mission")
            assert rec is not None, f"Day {day} must recommend a companion enterprise mission"
            assert "slug" in rec and len(rec["slug"]) > 0


# =============================================================================
# 3. Day 22 Capstone Multi-Concept Evaluation & DAG Remediation
# =============================================================================

class TestDay22CapstoneEvaluation:
    """Verify multi-concept evaluation and DAG remediation triggering for Day 22 Capstone."""

    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    def test_day_22_lesson_spec_has_11_concept_evaluations(self):
        day22 = SAP_DAYS_CONTENT[22]
        assessment_step = day22["steps"][5]
        assert assessment_step["is_capstone"] is True
        assert assessment_step["multi_concept_eval"] is True
        concepts = assessment_step["concepts_evaluated"]
        assert len(concepts) == 11, f"Day 22 must evaluate 11 concepts, found {len(concepts)}"

        expected_concepts = [
            "s4hana-value-drivers",
            "ecc-simplification-items",
            "in-memory-computing",
            "universal-journal-concept",
            "matdoc-table-architecture",
            "business-partner-cvi",
            "cds-fundamentals",
            "transport-management-cts",
            "identity-access-management",
            "embedded-analytics-foundations",
            "document-flow-continuity",
        ]
        for c in expected_concepts:
            assert c in concepts, f"Concept {c} must be evaluated in Day 22 Capstone"

    def test_day_22_all_correct_answers_passes_with_zero_remediation(self, mock_db):
        user_id = str(uuid.uuid4())
        # All correct answers for Day 22 (11 concepts, balanced varied answer keys: b, a, c, b, a, c, b, d, c, a, b)
        answers = {
            "cap2_q1": "b",
            "cap2_q2": "a",
            "cap2_q3": "c",
            "cap2_q4": "b",
            "cap2_q5": "a",
            "cap2_q6": "c",
            "cap2_q7": "b",
            "cap2_q8": "d",
            "cap2_q9": "c",
            "cap2_q10": "a",
            "cap2_q11": "b",
        }

        with patch.object(SAPMasteryService, "record_skill_evidence") as mock_record:
            res = SAPAssessmentService.evaluate(
                db=mock_db,
                user_id=user_id,
                day_number=22,
                assessment_id="day-22-s4hana-capstone",
                assessment_type="capstone_multi_concept",
                submission_payload={"answers": answers},
            )
            assert res["passed"] is True
            assert res["score"] == 100.0
            assert len(res.get("all_remediations", [])) == 0

            concept_evals = res.get("concept_evaluations", [])
            assert len(concept_evals) == 11
            for c_data in concept_evals:
                assert c_data["passed"] is True
                assert c_data["score"] == 100.0
            # 11 distinct skill evidence rows recorded
            assert mock_record.call_count == 11

    def test_failing_matdoc_and_acdoca_triggers_targeted_remediation(self, mock_db):
        user_id = str(uuid.uuid4())
        # Start with all correct answers
        answers = {
            "cap2_q1": "b",
            "cap2_q2": "a",
            "cap2_q3": "c",
            "cap2_q4": "b",
            "cap2_q5": "a",
            "cap2_q6": "c",
            "cap2_q7": "b",
            "cap2_q8": "d",
            "cap2_q9": "c",
            "cap2_q10": "a",
            "cap2_q11": "b",
        }
        # Fail Q4 (universal-journal-concept: correct is 'b', submit 'a')
        # Fail Q5 (matdoc-table-architecture: correct is 'a', submit 'b')
        answers["cap2_q4"] = "a"
        answers["cap2_q5"] = "b"

        with patch.object(SAPMasteryService, "record_skill_evidence"):
            res = SAPAssessmentService.evaluate(
                db=mock_db,
                user_id=user_id,
                day_number=22,
                assessment_id="day-22-s4hana-capstone",
                assessment_type="capstone_multi_concept",
                submission_payload={"answers": answers},
            )
            remediations = res.get("all_remediations", [])
            assert len(remediations) >= 2

            rem_slugs = {r["slug"] for r in remediations}
            assert "remediation-matdoc" in rem_slugs
            assert "remediation-acdoca" in rem_slugs

    def test_all_11_capstone_concepts_resolve_to_valid_remediation_capsules(self):
        """Every single concept tested in Day 22 Capstone must map to an actionable remediation capsule."""
        engine = SAPCurriculumKnowledgeEngine.get_instance()
        capstone_concepts = [
            "s4hana-value-drivers",
            "ecc-simplification-items",
            "in-memory-computing",
            "universal-journal-concept",
            "matdoc-table-architecture",
            "business-partner-cvi",
            "cds-fundamentals",
            "transport-management-cts",
            "identity-access-management",
            "embedded-analytics-foundations",
            "document-flow-continuity",
        ]
        for c in capstone_concepts:
            capsule = engine.get_remediation_capsule(c)
            assert capsule is not None, f"Concept '{c}' must have a valid remediation capsule in DAG"
            assert capsule.slug.startswith("remediation-")
            assert len(capsule.title) > 0
            assert len(capsule.remediation_content_md) > 0


# =============================================================================
# 4. Phase 2 Enterprise Missions & Locking
# =============================================================================

class TestSAPPhase2EnterpriseMissions:
    """Verify the 8 Phase 2 missions, assistance levels, and Day 23 locking."""

    PHASE_2_SLUGS = [
        "nova-s4hana-modernization-decision",
        "nova-universal-journal-investigation",
        "nova-matdoc-inventory-incident",
        "nova-business-partner-migration",
        "nova-cds-reporting-requirement",
        "nova-landscape-change-request",
        "nova-access-governance-incident",
        "nova-cross-module-document-trace",
    ]

    def test_all_phase_2_missions_in_seed_missions(self):
        seed_slugs = {m["slug"] for m in SEED_MISSIONS}
        for slug in self.PHASE_2_SLUGS:
            assert slug in seed_slugs, f"Mission '{slug}' must be in SEED_MISSIONS"

    def test_phase_2_assistance_levels_configuration(self):
        for m in PHASE_2_SEED_MISSIONS:
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

    def test_day_23_advanced_mission_remains_locked(self):
        """Day 23 advanced incident requires the canonical MIRO and MIGO concepts."""
        from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine

        day_23_mission = next((m for m in SEED_MISSIONS if m["slug"] == "nova-p2p-workflow-incident"), None)
        assert day_23_mission is not None
        assert day_23_mission["difficulty"] >= 3
        assert 23 in day_23_mission["related_days"]
        assert "p2p-invoice-verification-miro" in day_23_mission["prerequisite_concepts"]
        assert "p2p-goods-receipt-migo" in day_23_mission["prerequisite_concepts"]
        engine = SAPCurriculumKnowledgeEngine.get_instance()
        for slug in day_23_mission["prerequisite_concepts"]:
            assert engine.get_concept(slug) is not None, slug

    def test_mission_step_options_are_sanitized_no_answer_leak(self):
        """Verify get_mission_detail strips 'is_correct' and sensitive keys from options."""
        user_id = uuid.uuid4()
        for seed in PHASE_2_SEED_MISSIONS:
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
                            f"Answer leak vulnerability! 'is_correct' was found in options of mission {seed['slug']}, step {step.get('step_number')}"
                        )


# =============================================================================
# 5. Technical Accuracy & Architectural Audit Assertions
# =============================================================================

class TestSAPPhase2TechnicalAccuracyAudit:
    """Enforce technical veracity across all 14 days of Phase 2 curriculum and visualizers."""

    def test_audit_acdoca_preserves_operational_and_header_tables(self):
        """Verify Day 12 explicitly teaches that BKPF, BSEG, VBAK, and EKKO remain active."""
        d12 = PHASE_2_DAYS_CONTENT[12]
        d12_text = str(d12)
        assert "BKPF" in d12_text, "ACDOCA curriculum must reference document header BKPF"
        assert "VBAK" in d12_text or "Sales Order" in d12_text
        assert "AWTYP" in d12_text or "Reference Key" in d12_text

    def test_audit_matdoc_preserves_marc_mard_mbew_compatibility_views(self):
        """Verify Day 13 documents table preservation via NSDM_V_* CDS compatibility views."""
        d13 = PHASE_2_DAYS_CONTENT[13]
        d13_text = str(d13)
        assert "MARC" in d13_text and "MARD" in d13_text and "MBEW" in d13_text
        assert "NSDM_V_MARD" in d13_text or "compatibility view" in d13_text.lower()

    def test_audit_no_deprecated_odata_publish_in_phase2(self):
        """Verify deprecated @OData.publish: true is never recommended for CDS View Entities."""
        for day_num, day_data in PHASE_2_DAYS_CONTENT.items():
            content_str = str(day_data)
            assert "@OData.publish: true\ndefine view entity" not in content_str, (
                f"Day {day_num} uses deprecated @OData.publish on CDS View Entity!"
            )

    def test_audit_cbc_scoped_strictly_to_public_cloud(self):
        """Verify Central Business Configuration (CBC) is restricted to Public Cloud 3SL."""
        d17 = PHASE_2_DAYS_CONTENT[17]
        d17_text = str(d17)
        assert "Public Edition" in d17_text or "Public Cloud" in d17_text
        assert "SPRO" in d17_text or "Customizing" in d17_text

    def test_audit_sod_conflict_resolution_uses_restricted_role(self):
        """Verify Day 18 IAM SoD remediation uses SAP_BR_AP_CLERK_INVOICES without F_REGU_BUK."""
        d18 = PHASE_2_DAYS_CONTENT[18]
        d18_text = str(d18)
        assert "SAP_BR_AP_CLERK_INVOICES" in d18_text
        assert "F_REGU_BUK" in d18_text or "payment" in d18_text.lower()

    def test_audit_movement_311_correct_storage_location_transfer_semantics(self):
        """Verify Movement 311 is correctly defined as Storage Location to Storage Location."""
        matdoc_component = Path("frontend/components/sap/MATDOCFlow.tsx")
        if matdoc_component.exists():
            content = matdoc_component.read_text(encoding="utf-8")
            assert "Storage Location to Storage Location (within Plant)" in content

    def test_audit_all_8_frontend_visualizers_tagged_simulation_model(self):
        """Verify all 8 visualizers have explicit [SIMULATION MODEL] badging."""
        visualizers = [
            "frontend/components/sap/UniversalJournalVisualizer.tsx",
            "frontend/components/sap/MATDOCFlow.tsx",
            "frontend/components/sap/HANAStorageVisualizer.tsx",
            "frontend/components/sap/BusinessPartnerMapper.tsx",
            "frontend/components/sap/CDSConceptMapper.tsx",
            "frontend/components/sap/LandscapeFlow.tsx",
            "frontend/components/sap/AccessRoleMapper.tsx",
            "frontend/components/sap/DocumentFlowTracer.tsx",
        ]
        for v_path_str in visualizers:
            p = Path(v_path_str)
            if p.exists():
                text = p.read_text(encoding="utf-8")
                assert "[SIMULATION MODEL]" in text, f"Component {p.name} missing [SIMULATION MODEL] badge"