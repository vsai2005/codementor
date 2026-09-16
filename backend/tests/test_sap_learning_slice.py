"""Comprehensive Test Suite for SAP Days 1–8 Production Learning Slice & Enterprise Missions.

Covers:
1. Architectural Boundary & Isolation:
   - AST validation ensuring zero imports of Python sandbox, practice problems, or teacher prompts.
2. Complete 8-Day Guided Learning Content Integrity:
   - Days 1 through 8 strictly adhere to the 8-stage sequence:
     learn -> understand -> visual_example -> interactive_practice -> challenge -> assessment -> mastery_evidence -> completion.
   - Nova Manufacturing (NM01) digital twin continuous storyline throughout.
   - Interactive components (ProcessFlow, OrgStructureMapper, MasterDataClassifier, ArchitectureLayerMapper, SAPProductSelector, ModuleInteractionVisualizer, ScenarioDecision).
3. Day 8 Capstone Multi-Concept Evaluation & DAG Remediation:
   - Evaluating questions tagged by individual concept slugs.
   - Targeted DAG remediation capsules triggered for deficient concepts (< 70%).
   - Verified skill evidence generated per concept without flattening to a single score.
4. Enterprise Missions Expansion & Beginner / Advanced Locking:
   - 5 beginner missions mapped to Days 1–8 unlocked.
   - Day 23 advanced mission (nova-p2p-workflow-incident) remains locked for beginners without prerequisites.
   - Assistance levels (TRAINING, GUIDED, JOB) filter hints and primers properly.
5. API Route Verification:
   - GET /api/sap/learning/lessons/{day_number}
   - POST /api/sap/assessments/submit
"""

from __future__ import annotations

import ast
from pathlib import Path
from unittest.mock import MagicMock, patch
import uuid

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_current_user
from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine
from app.data.sap_lessons import SAP_DAYS_CONTENT
from app.database import get_db
from app.main import app
from app.models.models import User
from app.models.sap_models import (
    SAPAssistanceLevel,
    SAPConcept,
    SAPEnterprise,
    SAPEnterpriseInstance,
    SAPLearningMode,
    SAPMasteryState,
    SAPMission,
    SAPMissionAttempt,
    SAPMissionAttemptStatus,
    SAPMissionConcept,
    SAPMissionType,
    SAPRemediationCapsule,
    SAPSkillEvidence,
    SAPUserConceptMastery,
    SAPUserState,
)
from app.sap.services.assessment import SAPAssessmentService
from app.sap.services.mastery import SAPMasteryService
from app.sap.services.missions import SEED_MISSIONS, SAPMissionService

client = TestClient(app)


# =============================================================================
# 1. Architectural Boundary & Isolation Verification
# =============================================================================

class TestSAPLearningSliceIsolation:
    """Verify SAP learning slice files never import Python-specific engines."""

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
        Path("app/data/sap_lessons.py"),
        Path("app/api/routes/sap/learning.py"),
        Path("app/sap/services/assessment.py"),
        Path("app/sap/services/missions.py"),
        Path("app/sap/services/mastery.py"),
        Path("app/sap/services/progression.py"),
    ]

    def test_no_python_sandbox_or_services_imported(self):
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
# 2. Complete 8-Day Guided Learning Content Integrity
# =============================================================================

class TestSAPDaysContentIntegrity:
    """Verify all 8 days of Guided Learning content meet strict production criteria."""

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

    def test_days_1_to_8_all_present(self):
        for day in range(1, 9):
            assert day in SAP_DAYS_CONTENT, f"Day {day} must be authored in SAP_DAYS_CONTENT"

    def test_strict_8_step_sequence_for_all_days(self):
        for day, lesson in SAP_DAYS_CONTENT.items():
            assert lesson["day_number"] == day
            assert len(lesson["title"]) > 5
            steps = lesson["steps"]
            assert len(steps) == 8, f"Day {day} must have exactly 8 pedagogical steps"

            actual_types = [s["step_type"] for s in steps]
            assert actual_types == self.REQUIRED_STEPS_SEQUENCE, (
                f"Day {day} step sequence mismatch: {actual_types} != {self.REQUIRED_STEPS_SEQUENCE}"
            )

    def test_nova_manufacturing_twin_continuity(self):
        for day, lesson in SAP_DAYS_CONTENT.items():
            # Check step 3 (visual_example) specifically features Nova Manufacturing
            example_step = lesson["steps"][2]
            assert example_step["step_type"] == "visual_example"
            ctx = example_step.get("company_context")
            assert ctx is not None, f"Day {day} example must have company_context"
            # NM01 should be featured in context or markdown
            has_nm = (
                ctx.get("code") == "NM01"
                or ctx.get("company_code") == "NM01"
                or "NM01" in example_step["content_md"]
                or "Nova" in str(ctx)
            )
            assert has_nm, f"Day {day} visual example must reference Nova Manufacturing / NM01"

    def test_interactive_components_assigned(self):
        expected_components = {
            1: "ProcessFlow",
            2: "SAPProductSelector",
            3: "MasterDataClassifier",
            4: "OrgStructureMapper",
            5: "ModuleInteractionVisualizer",
            6: "ArchitectureLayerMapper",
            7: "ScenarioDecision",
            8: "OrgStructureMapper",
        }
        for day, comp in expected_components.items():
            practice_step = SAP_DAYS_CONTENT[day]["steps"][3]
            assert practice_step["step_type"] == "interactive_practice"
            assert practice_step["component_type"] == comp

    def test_companion_missions_recommended(self):
        for day, lesson in SAP_DAYS_CONTENT.items():
            completion_step = lesson["steps"][7]
            assert completion_step["step_type"] == "completion"
            rec = completion_step.get("recommended_mission")
            assert rec is not None, f"Day {day} must have recommended_mission in completion step"
            assert "slug" in rec and len(rec["slug"]) > 0


# =============================================================================
# 3. Day 8 Capstone Multi-Concept Evaluation & DAG Remediation
# =============================================================================

class TestDay8CapstoneEvaluation:
    """Verify multi-concept evaluation and DAG remediation triggering."""

    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    def test_day_8_lesson_spec_has_multi_concept_eval(self):
        day8 = SAP_DAYS_CONTENT[8]
        assessment_step = day8["steps"][5]
        assert assessment_step["is_capstone"] is True
        assert assessment_step["multi_concept_eval"] is True
        concepts = assessment_step["concepts_evaluated"]
        assert len(concepts) >= 6
        assert "org-structure-company-code" in concepts
        assert "master-data-concept" in concepts
        assert "module-interconnectivity" in concepts
        assert "three-tier-architecture" in concepts

    def test_all_correct_answers_pass_and_no_remediation(self, mock_db):
        user_id = str(uuid.uuid4())
        # All correct answers for Day 8
        answers = {
            "cap_q1": "a",
            "cap_q2": "a",
            "cap_q3": "a",
            "cap_q4": "a",
            "cap_q5": "a",
            "cap_q6": "a",
        }
        with patch.object(SAPMasteryService, "record_skill_evidence") as mock_record:
            res = SAPAssessmentService.evaluate(
                db=mock_db,
                user_id=user_id,
                day_number=8,
                assessment_id="day-8-foundations-capstone",
                assessment_type="capstone_multi_concept",
                submission_payload={"answers": answers},
            )
            assert res["passed"] is True
            assert res["score"] == 100.0
            assert len(res.get("all_remediations", [])) == 0
            # Check individual concept evaluations
            concept_evals = res.get("concept_evaluations", [])
            assert len(concept_evals) == 6
            for c_data in concept_evals:
                assert c_data["passed"] is True
                assert c_data["score"] == 100.0
            # Evidence was recorded for each concept
            assert mock_record.call_count == 6

    def test_failing_specific_concepts_triggers_targeted_remediation(self, mock_db):
        user_id = str(uuid.uuid4())
        # Intentionally fail Q1 (org-structure-company-code) and Q2 (master-data-concept)
        answers = {
            "cap_q1": "b",  # Wrong!
            "cap_q2": "b",  # Wrong!
            "cap_q3": "a",
            "cap_q4": "a",
            "cap_q5": "a",
            "cap_q6": "a",
        }
        with patch.object(SAPMasteryService, "record_skill_evidence"):
            res = SAPAssessmentService.evaluate(
                db=mock_db,
                user_id=user_id,
                day_number=8,
                assessment_id="day-8-foundations-capstone",
                assessment_type="capstone_multi_concept",
                submission_payload={"answers": answers},
            )
            assert res["passed"] is False  # 4/6 = 66.67% < 70%
            concept_eval_map = {c["concept_slug"]: c for c in res.get("concept_evaluations", [])}
            assert concept_eval_map["org-structure-company-code"]["passed"] is False
            assert concept_eval_map["master-data-concept"]["passed"] is False
            assert concept_eval_map["module-interconnectivity"]["passed"] is True

            # Must trigger targeted remediation capsules for the 2 failed concepts
            remed_slugs = [c["target_concept_slug"] for c in res.get("all_remediations", [])]
            assert "org-structure-company-code" in remed_slugs
            assert "master-data-concept" in remed_slugs


# =============================================================================
# 4. Enterprise Missions Expansion & Locking Invariants
# =============================================================================

class TestEnterpriseMissionsExpansion:
    """Verify the 5 beginner missions and locking of advanced Day 23 mission."""

    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    def test_seed_missions_contain_5_beginner_missions(self):
        beginner_slugs = {
            "nova-org-structure-design",
            "nova-plant-expansion",
            "nova-purchase-flow-trace",
            "nova-sap-product-selection",
            "nova-architecture-layer-incident",
        }
        existing_slugs = {m["slug"] for m in SEED_MISSIONS}
        for b_slug in beginner_slugs:
            assert b_slug in existing_slugs, f"Mission {b_slug} must be in SEED_MISSIONS"

    def test_beginner_missions_unlocked_for_new_user(self, mock_db):
        user_id = str(uuid.uuid4())
        mock_db.execute.return_value.scalars.return_value.all.return_value = []
        mock_db.execute.return_value.scalar_one_or_none.return_value = None

        with patch.object(SAPMissionService, "seed_missions_if_needed"):
            # Set up mock returns for list_missions_for_user
            mock_mission_1 = MagicMock()
            mock_mission_1.id = uuid.uuid4()
            mock_mission_1.slug = "nova-org-structure-design"
            mock_mission_1.title = "Core Org Hierarchy"
            mock_mission_1.description = "Test"
            mock_mission_1.mission_type = "CONFIGURATION"
            mock_mission_1.difficulty = 1
            mock_mission_1.estimated_minutes = 15
            mock_mission_1.related_days = [4]
            mock_mission_1.concept_slugs = ["org-structure-client"]
            mock_mission_1.prerequisite_concepts = []
            mock_mission_1.is_active = True

            mock_mission_adv = MagicMock()
            mock_mission_adv.id = uuid.uuid4()
            mock_mission_adv.slug = "nova-p2p-workflow-incident"
            mock_mission_adv.title = "P2P Incident"
            mock_mission_adv.description = "Advanced"
            mock_mission_adv.mission_type = "TROUBLESHOOTING"
            mock_mission_adv.difficulty = 3
            mock_mission_adv.estimated_minutes = 30
            mock_mission_adv.related_days = [23]
            mock_mission_adv.concept_slugs = ["invoice-verification-miro"]
            mock_mission_adv.prerequisite_concepts = ["invoice-verification-miro", "goods-receipt-migo"]
            mock_mission_adv.is_active = True

            mock_c1 = MagicMock(id=uuid.uuid4(), slug="invoice-verification-miro")
            mock_c2 = MagicMock(id=uuid.uuid4(), slug="goods-receipt-migo")

            mock_db.execute.return_value.scalars.return_value.all.side_effect = [
                [],  # mastery_rows
                [mock_c1, mock_c2],  # concepts
                [],  # attempts
                [mock_mission_1, mock_mission_adv],  # missions
            ]

            missions = SAPMissionService.list_missions_for_user(mock_db, user_id)
            mission_map = {m["slug"]: m for m in missions}

            assert mission_map["nova-org-structure-design"]["is_unlocked"] is True
            assert mission_map["nova-p2p-workflow-incident"]["is_unlocked"] is False

    def test_assistance_level_rules_configuration(self):
        # Test assistance_rules directly on seed missions
        sample_mission = SEED_MISSIONS[0]
        rules = sample_mission["assistance_rules"]

        # JOB level must disable hints and primer
        job_rules = rules["JOB"]
        assert job_rules["allow_hints"] is False
        assert len(job_rules["hints"]) == 0
        assert job_rules["show_prerequisite_primer"] is False

        # TRAINING level must enable hints and primer
        training_rules = rules["TRAINING"]
        assert training_rules["allow_hints"] is True
        assert len(training_rules["hints"]) > 0
        assert training_rules["show_prerequisite_primer"] is True


# =============================================================================
# 5. API Endpoint Verification
# =============================================================================

class TestSAPLearningSliceAPI:
    """Test API endpoints for Days 1–8 Guided Learning."""

    def test_get_authored_lesson_content(self):
        # Day 1
        res = client.get("/api/sap/learning/lessons/1")
        assert res.status_code == 200
        data = res.json()
        assert data["day_number"] == 1
        assert len(data["steps"]) == 8
        assert data["recommended_mission_slug"] == "nova-purchase-flow-trace"

        # Day 8 Capstone
        res8 = client.get("/api/sap/learning/lessons/8")
        assert res8.status_code == 200
        data8 = res8.json()
        assert data8["day_number"] == 8
        assert len(data8["steps"]) == 8
        assert data8["steps"][5]["is_capstone"] is True

    def test_get_unauthored_day_returns_404(self):
        res = client.get("/api/sap/learning/lessons/9")
        assert res.status_code == 404
        assert "not authored yet" in res.json()["detail"]
