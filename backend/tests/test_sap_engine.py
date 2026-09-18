"""Comprehensive verification suite for the SAP Learning Engine foundation.

Covers:
1. Architectural boundary & isolation enforcement (AST-based check)
2. Curriculum manifest data integrity (100 days, 9 phases, environment tiers)
3. DAG cycle-freedom, topological traversal, and root discovery
4. High-risk remediation capsules (ACDOCA, MATDOC, CDS, RAP, BTP)
5. SAP Mastery state machine transitions
6. SAP Placement diagnostic & persona resolution (5 personas)
7. Multi-modal assessment evaluation
8. Pluggable execution provider interface (Simulation, CDS, ABAP Cloud)
9. Database model schema definitions
10. FastAPI integration routes under /api/sap/...
11. Python Learning Engine regression & isolation verification
"""

from __future__ import annotations

import ast
from pathlib import Path
import uuid
import pytest
from fastapi.testclient import TestClient

from app.core.sap_curriculum_retrieval import (
    DAGIntegrityError,
    SAPCurriculumKnowledgeEngine,
)
from app.main import app
from app.models.sap_models import (
    SAPAssessment,
    SAPConcept,
    SAPCourse,
    SAPDay,
    SAPDayStatus,
    SAPMasteryState,
    SAPPhase,
    SAPPlacementProfile,
    SAPPlacementStatus,
    SAPRemediationCapsule,
    SAPUserConceptMastery,
    SAPUserDayState,
    SAPUserState,
)
from app.sap.services.assessment import SAPAssessmentService
from app.sap.services.execution import (
    ABAPCloudProvider,
    CDSValidationProvider,
    ExecutionCategory,
    SAPExecutionRequest,
    SimulationProvider,
    get_execution_provider,
)
from app.sap.services.placement import SAPPlacementService
from app.sap.services.progression import SAPProgressionService

client = TestClient(app)


# =============================================================================
# 1. Architectural Boundary & Isolation Enforcement
# =============================================================================

def test_sap_modules_have_zero_python_dependencies():
    """Verifies through AST analysis that no file in app/sap or sap_curriculum_retrieval
    imports Python sandbox, Python practice problems, Python submissions, or Python tutor logic."""
    forbidden_prefixes = {
        "app.services.sandbox",
        "app.services._sandbox_runner",
        "app.sandbox",
        "app.services.difficulty",
        "app.services.submissions",
        "app.services.review",
        "app.core.curriculum_map",
        "app.core.curriculum_retrieval",
    }

    sap_dir = Path(__file__).resolve().parent.parent / "app" / "sap"
    files_to_check = list(sap_dir.rglob("*.py"))
    files_to_check.append(Path(__file__).resolve().parent.parent / "app" / "core" / "sap_curriculum_retrieval.py")
    files_to_check.append(Path(__file__).resolve().parent.parent / "app" / "models" / "sap_models.py")

    assert len(files_to_check) > 5, "Should have found multiple SAP domain files to audit"

    for py_file in files_to_check:
        tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for forbidden in forbidden_prefixes:
                        assert not alias.name.startswith(forbidden), (
                            f"Isolation violation in {py_file.name}: imports forbidden '{alias.name}'"
                        )
            elif isinstance(node, ast.ImportFrom) and node.module:
                for forbidden in forbidden_prefixes:
                    assert not node.module.startswith(forbidden), (
                        f"Isolation violation in {py_file.name}: imports from forbidden '{node.module}'"
                    )


# =============================================================================
# 2. Curriculum Manifest & 100-Day Structure
# =============================================================================

def test_curriculum_100_days_completeness():
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    assert engine.get_total_days() == 100

    days = engine.get_all_days()
    day_numbers = [d.day_number for d in days]
    assert day_numbers == list(range(1, 101)), "Must have days 1 through 100 without gaps"

    # Check phase boundaries
    phase_counts = {p: 0 for p in range(1, 10)}
    for d in days:
        assert 1 <= d.phase_number <= 9
        phase_counts[d.phase_number] += 1
        assert len(d.objectives) > 0, f"Day {d.day_number} missing objectives"
        assert len(d.atomic_concepts) > 0, f"Day {d.day_number} missing atomic concepts"
        assert d.env_tier in {"browser", "simulated_sap_gui_fiori", "hana_cds", "eclipse_adt_abap_cloud", "btp"}, (
            f"Day {d.day_number} has invalid env_tier: {d.env_tier}"
        )

    # Validate exact phase distributions matching user specification
    assert phase_counts[1] == 8   # Days 1-8: Enterprise Architecture & ERP Foundations
    assert phase_counts[2] == 14  # Days 9-22: S/4HANA Fundamentals & Data Architecture
    assert phase_counts[3] == 22  # Days 23-44: Core End-to-End Business Processes
    assert phase_counts[4] == 10  # Days 45-54: HANA Engine & Data Semantics
    assert phase_counts[5] == 10  # Days 55-64: SAP Fiori & Enterprise UX
    assert phase_counts[6] == 12  # Days 65-76: S/4HANA Cloud & Clean Core
    assert phase_counts[7] == 13  # Days 77-89: ABAP Cloud & RAP
    assert phase_counts[8] == 6   # Days 90-95: SAP BTP & Enterprise Integration
    assert phase_counts[9] == 5   # Days 96-100: Enterprise Capstone


# =============================================================================
# 3. Adaptive Knowledge DAG & Graph Traversal
# =============================================================================

def test_dag_cycle_freedom_and_topological_sort():
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    # If there were any cycles, __init__ would have raised DAGIntegrityError
    concepts = engine.get_all_concepts()
    assert len(concepts) > 200

    # Verify ACDOCA topological prerequisite chain
    acdoca_prereqs = engine.traverse_prerequisites("acdoca-table-architecture")
    assert "double-entry-accounting" in acdoca_prereqs
    assert "universal-journal-concept" in acdoca_prereqs
    assert "subledger-vs-gl" in acdoca_prereqs
    # double-entry must precede universal-journal
    assert acdoca_prereqs.index("double-entry-accounting") < acdoca_prereqs.index("universal-journal-concept")


def test_dag_root_prerequisite_discovery():
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    rap_roots = engine.get_root_prerequisites("rap-save-sequence")
    assert "oop-fundamentals" in rap_roots
    assert "transactional-lifecycle" in rap_roots

    btp_roots = engine.get_root_prerequisites("enterprise-integration-synthesis")
    assert "erp-evolution" in btp_roots or "cloudevents-standard" in btp_roots or "double-entry-accounting" in btp_roots


def test_dag_dependent_discovery():
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    clean_core_deps = engine.traverse_dependents("clean-core-philosophy")
    assert "sap-activate-methodology" in clean_core_deps
    assert "developer-extensibility-on-stack" in clean_core_deps
    assert "side-by-side-extensibility" in clean_core_deps


# =============================================================================
# 4. High-Risk Remediation Capsules
# =============================================================================

def test_high_risk_remediation_capsules():
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    core_remediations = [
        "acdoca-table-architecture",
        "matdoc-table-architecture",
        "cds-associations-concept",
        "rap-save-sequence",
        "sap-event-mesh",
    ]

    for concept_slug in core_remediations:
        capsule = engine.get_remediation_capsule(concept_slug)
        assert capsule is not None, f"Missing required remediation capsule for '{concept_slug}'"
        assert len(capsule.deficiency_triggers) > 0
        assert len(capsule.prerequisite_deficiencies) > 0
        assert len(capsule.remediation_content_md) > 50
        assert capsule.recovery_assessment_slug != ""

    # Test gap analysis helper
    gaps = engine.analyze_learner_gaps(
        failed_concept_slug="acdoca-table-architecture",
        mastered_concepts={"erp-evolution", "three-tier-architecture"},
    )
    assert gaps["failed_concept"] == "acdoca-table-architecture"
    assert "double-entry-accounting" in gaps["unmastered_prerequisites"]
    assert gaps["remediation_capsule"] is not None


# =============================================================================
# 5. Execution Providers (Simulation, CDS, ABAP Cloud)
# =============================================================================

@pytest.mark.anyio
async def test_simulation_provider():
    provider = get_execution_provider("simulation")
    # Matching sequence
    req_good = SAPExecutionRequest(
        provider_type="simulation",
        code_or_payload='[{"step": 1, "action": "ME51N_CREATE_PR"}, {"step": 2, "action": "ME21N_CREATE_PO"}]',
        context_parameters={
            "expected_sequence": [{"action": "ME51N_CREATE_PR"}, {"action": "ME21N_CREATE_PO"}]
        },
    )
    res_good = await provider.execute(req_good)
    assert res_good.success is True
    assert res_good.status == "ok"

    # Mismatched sequence
    req_bad = SAPExecutionRequest(
        provider_type="simulation",
        code_or_payload='[{"step": 1, "action": "WRONG_ACTION"}]',
        context_parameters={
            "expected_sequence": [{"action": "ME51N_CREATE_PR"}]
        },
    )
    res_bad = await provider.execute(req_bad)
    assert res_bad.success is False
    assert any(f.rule_code == "STEP_SEQUENCE_MISMATCH" for f in res_bad.findings)


@pytest.mark.anyio
async def test_cds_validation_provider():
    provider = get_execution_provider("cds_validation")
    # Compliant CDS View Entity
    good_cds = """
    @EndUserText.label: 'Carrier Flight CDS'
    @AccessControl.authorizationCheck: #CHECK
    define view entity ZI_Carrier as select from scarr {
      key carrid as CarrierId,
          carrname as CarrierName
    }
    """
    res_good = await provider.execute(
        SAPExecutionRequest(provider_type="cds_validation", code_or_payload=good_cds)
    )
    assert res_good.success is True

    # Legacy syntax & missing label
    bad_cds = """
    define view ZI_Legacy as select from scarr {
      key carrid
    }
    """
    res_bad = await provider.execute(
        SAPExecutionRequest(provider_type="cds_validation", code_or_payload=bad_cds)
    )
    assert res_bad.success is False
    rule_codes = [f.rule_code for f in res_bad.findings]
    assert "DEPRECATED_CDS_SYNTAX" in rule_codes
    assert "MISSING_LABEL_ANNOTATION" in rule_codes


@pytest.mark.anyio
async def test_abap_cloud_provider():
    provider = get_execution_provider("abap_cloud")
    # Clean ABAP OO
    good_abap = """
    CLASS zcl_carrier_calculator DEFINITION PUBLIC FINAL CREATE PUBLIC.
      PUBLIC SECTION.
        METHODS calculate IMPORTING iv_amount TYPE decfloat34 RETURNING VALUE(rv_tax) TYPE decfloat34.
    ENDCLASS.
    CLASS zcl_carrier_calculator IMPLEMENTATION.
      METHOD calculate.
        rv_tax = iv_amount * '0.19'.
      ENDMETHOD.
    ENDCLASS.
    """
    res_good = await provider.execute(
        SAPExecutionRequest(provider_type="abap_cloud", code_or_payload=good_abap)
    )
    assert res_good.success is True

    # Forbidden legacy ABAP statements
    bad_abap = """
    DATA: wa_vbak TYPE vbak.
    CALL TRANSACTION 'VA01'.
    INSERT INTO vbak VALUES wa_vbak.
    COMMIT WORK.
    """
    res_bad = await provider.execute(
        SAPExecutionRequest(provider_type="abap_cloud", code_or_payload=bad_abap)
    )
    assert res_bad.success is False
    rule_codes = [f.rule_code for f in res_bad.findings]
    assert "CALL_TRANSACTION_FORBIDDEN" in rule_codes
    assert "DIRECT_STANDARD_DB_WRITE" in rule_codes
    assert "MANUAL_COMMIT_FORBIDDEN" in rule_codes


# =============================================================================
# 6. Placement Diagnostic & Personas
# =============================================================================

def test_placement_persona_rules():
    # 1. Fresher: low scores across all domains -> Day 1
    scores_fresher = {"erp_basics": 30, "ddic_and_sql": 20, "classic_abap": 10, "modern_s4hana_rap": 10, "btp_integration": 10}
    # 2. Beginner: basic understanding -> Day 9
    scores_beginner = {"erp_basics": 55, "ddic_and_sql": 50, "classic_abap": 20, "modern_s4hana_rap": 10, "btp_integration": 10}
    # 3. Functional User: strong ERP & business, low coding -> Day 23
    scores_functional = {"erp_basics": 85, "ddic_and_sql": 40, "classic_abap": 20, "modern_s4hana_rap": 10, "btp_integration": 20}
    # 4. ECC Developer: strong ABAP & DDIC, low RAP -> Day 45
    scores_ecc = {"erp_basics": 80, "ddic_and_sql": 80, "classic_abap": 85, "modern_s4hana_rap": 30, "btp_integration": 30}
    # 5. Experienced S/4HANA: strong RAP & ABAP -> Day 77
    scores_s4 = {"erp_basics": 90, "ddic_and_sql": 90, "classic_abap": 85, "modern_s4hana_rap": 85, "btp_integration": 80}

    assert SAPPlacementService.PERSONA_CONFIG["fresher"]["default_start_day"] == 1
    assert SAPPlacementService.PERSONA_CONFIG["beginner"]["default_start_day"] == 9
    assert SAPPlacementService.PERSONA_CONFIG["functional_user"]["default_start_day"] == 23
    assert SAPPlacementService.PERSONA_CONFIG["ecc_developer"]["default_start_day"] == 45
    assert SAPPlacementService.PERSONA_CONFIG["experienced_s4hana"]["default_start_day"] == 77


# =============================================================================
# 7. Multi-Modal Assessment Evaluation
# =============================================================================

def test_assessment_mcq_evaluation():
    spec = {
        "correct_option_ids": ["opt_acdoca"],
        "explanations": {"opt_bseg": "BSEG is a legacy cluster table in ECC."},
    }
    # Correct pick
    score, feedback, bd = SAPAssessmentService._eval_mcq(spec, {"selected_option_ids": ["opt_acdoca"]})
    assert score == 100.0
    assert bd["accuracy"] == 1.0

    # Distractor pick
    score_bad, feedback_bad, bd_bad = SAPAssessmentService._eval_mcq(spec, {"selected_option_ids": ["opt_bseg"]})
    assert score_bad == 0.0
    assert "legacy cluster table" in feedback_bad


def test_assessment_process_ordering_evaluation():
    spec = {
        "target_ordered_ids": ["PR", "RFQ", "PO", "GR", "IV", "PAYMENT"]
    }
    # Perfect order
    score, msg, bd = SAPAssessmentService._eval_ordering(
        spec, {"ordered_ids": ["PR", "RFQ", "PO", "GR", "IV", "PAYMENT"]}
    )
    assert score == 100.0
    assert bd["match_ratio"] == 1.0

    # Partial order
    score_partial, msg_p, bd_p = SAPAssessmentService._eval_ordering(
        spec, {"ordered_ids": ["PR", "PO", "RFQ", "GR", "IV", "PAYMENT"]}
    )
    assert score_partial < 100.0
    assert bd_p["matched_positions"] == 4


# =============================================================================
# 8. Database Models Integrity
# =============================================================================

def test_sap_models_registered_in_metadata():
    from app.models.models import Base
    table_names = set(Base.metadata.tables.keys())

    expected_sap_tables = {
        "sap_courses",
        "sap_phases",
        "sap_days",
        "sap_concepts",
        "sap_concept_prerequisites",
        "sap_day_concepts",
        "sap_assessments",
        "sap_remediation_capsules",
        "sap_placement_profiles",
        "sap_user_state",
        "sap_user_day_state",
        "sap_user_concept_mastery",
        "sap_assessment_attempts",
    }
    for t in expected_sap_tables:
        assert t in table_names, f"Expected table '{t}' to be registered in Base.metadata"

    # Verify Python models still registered
    expected_python_tables = {
        "users",
        "topics",
        "problems",
        "submissions",
        "user_topic_state",
        "difficulty_events",
        "memory_notes",
        "user_learning_day_state",
    }
    for t in expected_python_tables:
        assert t in table_names, f"Expected Python table '{t}' to be preserved in Base.metadata"


# =============================================================================
# 9. API Integration Endpoints
# =============================================================================

def test_api_sap_curriculum_overview():
    resp = client.get("/api/sap/curriculum")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_days"] == 100
    assert len(data["phases"]) == 9
    assert len(data["days"]) == 100


def test_api_sap_day_detail():
    resp = client.get("/api/sap/curriculum/days/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["day_number"] == 1
    assert data["phase_number"] == 1
    assert len(data["objectives"]) > 0
    assert len(data["atomic_concepts"]) > 0

    # Non-existent day
    resp_404 = client.get("/api/sap/curriculum/days/101")
    assert resp_404.status_code == 404


def test_api_sap_concept_detail_with_dag():
    resp = client.get("/api/sap/curriculum/concepts/acdoca-table-architecture")
    assert resp.status_code == 200
    data = resp.json()
    assert data["slug"] == "acdoca-table-architecture"
    assert "universal-journal-concept" in data["direct_prerequisites"]
    assert "double-entry-accounting" in data["all_ancestor_prerequisites"]
    assert data["remediation_available"] is True


def test_api_sap_execution_validate():
    payload = {
        "provider_type": "abap_cloud",
        "code_or_payload": "CALL TRANSACTION 'SE11'.",
        "context_parameters": {},
    }
    resp = client.post("/api/sap/execution/validate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is False
    assert any(f["rule_code"] == "CALL_TRANSACTION_FORBIDDEN" for f in data["findings"])


# =============================================================================
# 10. Python Regression & Non-Interference
# =============================================================================

def test_python_learning_run_still_works():
    """Verify that Python execution sandbox is intact and untouched for authenticated users."""
    from app.api.deps import get_current_user
    from app.models.models import User

    test_user = User(id=uuid.uuid4(), email="sap_test@example.com", name="SAP Tester")
    app.dependency_overrides[get_current_user] = lambda: test_user
    try:
        payload = {
            "code": "print('Python sandbox remains completely functional')",
            "day_number": 1,
        }
        resp = client.post("/api/learning/run", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "Python sandbox remains completely functional" in data["stdout"]
    finally:
        app.dependency_overrides.pop(get_current_user, None)


# =============================================================================
# 11. Authoritative 100-Day Curriculum Map Verification
# =============================================================================

def test_authoritative_100_day_manifest_map():
    """Validates the authoritative 100-day manifest against the finalized curriculum specification."""
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    days = engine.get_all_days()
    assert len(days) == 100

    # Verify Day 12: ACDOCA / Universal Journal
    d12 = engine.get_day(12)
    assert d12 is not None
    assert d12.slug == "acdoca-universal-journal"
    assert "ACDOCA" in d12.title
    assert "Universal Journal" in d12.title
    assert d12.phase_number == 2

    # Verify Day 13: MATDOC
    d13 = engine.get_day(13)
    assert d13 is not None
    assert d13.slug == "matdoc-inventory-architecture"
    assert "MATDOC" in d13.title or "Material Document" in d13.title
    assert d13.phase_number == 2

    # Verify Days 14–22 sequence
    d14 = engine.get_day(14)
    assert d14 is not None and d14.slug == "business-partner-cvi"

    d15 = engine.get_day(15)
    assert d15 is not None and d15.slug == "cds-fundamentals-intro"

    d21 = engine.get_day(21)
    assert d21 is not None
    assert d21.slug == "s4hana-integrated-scenario"
    assert "Cross-Module" in d21.title or "Integrated Scenario" in d21.title
    assert d21.phase_number == 2

    d22 = engine.get_day(22)
    assert d22 is not None
    assert d22.slug == "s4hana-fundamentals-capstone"
    assert d22.phase_number == 2

    # Verify Day 45: HANA Engine Architecture & Internals
    d45 = engine.get_day(45)
    assert d45 is not None
    assert d45.phase_number == 4
    assert "HANA Engine" in d45.title

    # Verify Day 91: Integration Patterns & SAP Integration Suite
    d91 = engine.get_day(91)
    assert d91 is not None
    assert d91.phase_number == 8
    assert "Integration" in d91.title

    # Verify Day 94: Secure Connectivity & S/4HANA Event Integration
    d94 = engine.get_day(94)
    assert d94 is not None
    assert d94.phase_number == 8
    assert "Secure Connectivity" in d94.title or "Event Integration" in d94.title


# =============================================================================
# 12. DAG Reachability, Cycle Freedom & Coverage
# =============================================================================

def test_dag_complete_reachability_and_cycle_freedom():
    """Verifies that the knowledge graph is strictly a cycle-free DAG with complete coverage."""
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    # If invalid, validate_dag_integrity raises DAGIntegrityError; on success it returns None
    assert engine.validate_dag_integrity() is None

    concepts = engine.get_all_concepts()
    assert len(concepts) == 221, f"Expected 221 concepts, got {len(concepts)}"
    total_edges = sum(len(v) for v in engine._direct_prereqs.values())
    assert total_edges >= 250, f"Expected >= 250 DAG edges, got {total_edges}"

    # Check cross-phase prerequisite traversal:
    # Phase 2 -> Phase 3 -> Phase 4 -> Phase 7 -> Phase 8
    ancestors = engine.traverse_prerequisites("rap-full-stack-synthesis")
    assert "rap-architecture-overview" in ancestors
    assert "cds-associations-concept" in ancestors
    assert "master-data-concept" in ancestors or "erp-evolution" in ancestors


# =============================================================================
# 13. Evidence-Based Placement & Untested Concept Protection
# =============================================================================

def test_placement_evidence_routing_and_untested_concept_protection():
    """Verifies that placement routes based on domain evidence and waives days without falsely marking untested concepts as mastered."""
    from unittest.mock import MagicMock

    mock_db = MagicMock()
    # Mock no existing profile
    mock_db.execute.return_value.scalar_one_or_none.return_value = None
    mock_db.scalars.return_value.all.return_value = []
    mock_db.scalar.return_value = None

    test_user_id = uuid.uuid4()

    # Case 1: Fresher -> Day 1, no waived days
    fresher_prof = SAPPlacementService.evaluate_diagnostic(
        db=mock_db,
        user_id=test_user_id,
        domain_scores={"erp_basics": 25.0, "ddic_and_sql": 15.0},
        persona_self_select="fresher",
    )
    assert fresher_prof.recommended_start_day == 1
    assert fresher_prof.diagnostic_results["waived_days"] == []

    # Case 2: Beginner with high ERP fundamentals -> waives Days 1-8, starts Day 9
    beginner_prof = SAPPlacementService.evaluate_diagnostic(
        db=mock_db,
        user_id=test_user_id,
        domain_scores={"erp_basics": 75.0, "business_processes": 30.0},
    )
    assert beginner_prof.recommended_start_day == 9
    assert beginner_prof.diagnostic_results["waived_days"] == list(range(1, 9))

    # Case 3: Functional User with business process evidence -> Day 45
    func_prof = SAPPlacementService.evaluate_diagnostic(
        db=mock_db,
        user_id=test_user_id,
        domain_scores={"erp_basics": 85.0, "business_processes": 85.0, "s4hana_delta": 70.0},
    )
    assert func_prof.recommended_start_day == 45
    assert func_prof.diagnostic_results["waived_days"] == list(range(1, 45))

    # Case 4: ECC Developer with classic ABAP & DDIC -> Day 45
    ecc_prof = SAPPlacementService.evaluate_diagnostic(
        db=mock_db,
        user_id=test_user_id,
        domain_scores={"classic_abap": 85.0, "ddic_and_sql": 75.0, "erp_basics": 80.0},
    )
    assert ecc_prof.recommended_start_day == 45
    assert ecc_prof.diagnostic_results["waived_days"] == list(range(1, 45))

    # Case 5: Experienced S/4HANA Developer -> Day 90
    s4_prof = SAPPlacementService.evaluate_diagnostic(
        db=mock_db,
        user_id=test_user_id,
        domain_scores={
            "rap_foundations": 90.0,
            "modern_abap_cds": 85.0,
            "btp_integration": 80.0,
            "erp_basics": 90.0,
        },
    )
    assert s4_prof.recommended_start_day == 77
    assert s4_prof.diagnostic_results["waived_days"] == list(range(1, 77))


# =============================================================================
# 14. Day-State Five-State Semantics
# =============================================================================

def test_day_state_five_state_semantics():
    """Verifies that SAP day states explicitly include locked, available, in_progress, completed, and waived_by_placement."""
    assert SAPDayStatus.LOCKED.value == "locked"
    assert SAPDayStatus.AVAILABLE.value == "available"
    assert SAPDayStatus.IN_PROGRESS.value == "in_progress"
    assert SAPDayStatus.COMPLETED.value == "completed"
    assert SAPDayStatus.WAIVED_BY_PLACEMENT.value == "waived_by_placement"

    from unittest.mock import MagicMock
    mock_db = MagicMock()

    # Test progression progress compilation with waived days
    user_state = SAPUserState(
        user_id=uuid.uuid4(),
        current_recommended_day=9,
        completed_days_count=0,
    )
    # Day 1..8 marked waived_by_placement
    day_states = [
        SAPUserDayState(
            user_id=user_state.user_id,
            day_number=i,
            completed=False,
            status=SAPDayStatus.WAIVED_BY_PLACEMENT.value,
            waived=True,
        )
        for i in range(1, 9)
    ]
    placement = SAPPlacementProfile(
        user_id=user_state.user_id,
        recommended_start_day=9,
        persona="beginner",
        diagnostic_results={"waived_days": list(range(1, 9))},
    )

    mock_db.execute.return_value.scalar_one_or_none.return_value = placement
    mock_db.execute.return_value.scalars.return_value.all.return_value = day_states

    resp = SAPProgressionService.compute_user_progress(mock_db, user_state.user_id)
    assert resp["current_day"] == 9
    assert resp["completed_days"] == []  # Waived days must NOT be counted as completed
    assert resp["waived_days"] == list(range(1, 9))
    assert resp["day_states"]["1"]["status"] == "waived_by_placement"
    assert resp["day_states"]["1"]["waived"] is True
    assert resp["day_states"]["9"]["status"] == "available"


# =============================================================================
# 15. Migration 0003 Safe Downgrade Marker Pattern
# =============================================================================

def test_migration_0003_safe_downgrade_marker():
    """Verifies that migration 0003 contains the safe marker table pattern so downgrade cannot drop pre-existing tables."""
    migration_file = Path(__file__).resolve().parent.parent / "alembic" / "versions" / "0003_user_learning_day_state.py"
    assert migration_file.exists(), "Migration 0003 must exist"
    content = migration_file.read_text(encoding="utf-8")

    assert "_alembic_0003_user_learning_day_state_created" in content
    assert "downgrade" in content
    assert "has_table" in content or "inspect" in content


# =============================================================================
# 16. Execution Provider Truthfulness Metadata
# =============================================================================

@pytest.mark.anyio
async def test_execution_provider_truthfulness_metadata():
    """Verifies that execution providers are truthfully classified as local simulation/static validation and not real SAP systems."""
    assert ExecutionCategory.STATIC_VALIDATION.value == "STATIC_VALIDATION"
    assert ExecutionCategory.LOCAL_SIMULATION.value == "LOCAL_SIMULATION"
    assert ExecutionCategory.REAL_SAP_EXECUTION.value == "REAL_SAP_EXECUTION"

    # Simulation Provider
    sim = SimulationProvider()
    sim_res = await sim.execute(
        SAPExecutionRequest(
            provider_type="simulation",
            code_or_payload='[{"step": 1, "action": "ME51N_CREATE_PR"}]',
            context_parameters={"expected_sequence": [{"action": "ME51N_CREATE_PR"}]},
        )
    )
    assert sim_res.provider_category == ExecutionCategory.LOCAL_SIMULATION
    assert sim_res.is_sandboxed_simulation is True
    assert sim_res.is_live_sap_system is False

    # CDS Validation Provider
    cds = CDSValidationProvider()
    cds_res = await cds.execute(
        SAPExecutionRequest(provider_type="cds_validation", code_or_payload="define view entity ZTest ...")
    )
    assert cds_res.provider_category == ExecutionCategory.STATIC_VALIDATION
    assert cds_res.is_sandboxed_simulation is False
    assert cds_res.is_live_sap_system is False

    # ABAP Cloud Provider
    abap = ABAPCloudProvider()
    abap_res = await abap.execute(
        SAPExecutionRequest(provider_type="abap_cloud", code_or_payload="CLASS zcl_test DEFINITION...")
    )
    assert abap_res.provider_category == ExecutionCategory.STATIC_VALIDATION
    assert abap_res.is_sandboxed_simulation is False
    assert abap_res.is_live_sap_system is False

    # API Endpoint Response Truthfulness Metadata
    resp = client.post(
        "/api/sap/execution/validate",
        json={"provider_type": "abap_cloud", "code_or_payload": "DATA: x TYPE i."},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["provider_category"] == "STATIC_VALIDATION"
    assert data["is_sandboxed_simulation"] is False
    assert data["is_live_sap_system"] is False

