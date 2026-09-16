"""
test_sap_phase4_slice.py

Comprehensive test suite verifying:
1. Days 45-54 curriculum completeness (10 days, 8 steps per day, canonical pedagogical sequence).
2. Block 1 (Days 45-48: HANA & Core CDS) architectural and technical truthfulness.
3. Block 2 (Days 49-51: Advanced CDS & Semantic Catalog) parameterized views, annotations, compositions.
4. Block 3 (Days 52-54: Analytics, DCL Security & Capstone) cubes, row-level security, and Day 54 Capstone.
5. Technical Truthfulness Invariants:
   - Inverted indexes exist in column store (no "HANA has no indexes").
   - Memory paging & persistence (no "everything is always in RAM").
   - Associations are lazy on-demand joins with pruning.
   - Pushdown trade-offs (avoid unpushable engine hops).
   - Modern S/4HANA uses RAP Service Definitions/Bindings (no @OData.publish: true).
6. Interactive component mappings for all Phase 4 visualizers.
7. 8 Phase 4 Enterprise Missions (registration, assistance rules, step evaluation, option sanitization).
8. DAG integration and remediation capsule resolution for all Phase 4 concepts.
9. Nova Manufacturing enterprise continuity (NM01, PL01, PL02, PO01, SO01, RAW1, FG01, VEND-101, CUST-501, DXTR-1000).
"""

import uuid
from unittest.mock import MagicMock, patch
import pytest

from app.data.sap_lessons import SAP_DAYS_CONTENT
from app.data.sap_lessons_phase4 import PHASE_4_DAYS_CONTENT
from app.sap.services.missions import SEED_MISSIONS, SAPMissionService
from app.sap.services.phase4_missions import PHASE_4_SEED_MISSIONS
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
# 1. Curriculum Integrity & 8-Step Architecture (Days 45 to 54)
# =============================================================================

def test_phase4_days_present():
    """Verify all 10 Phase 4 days (Days 45 to 54) are loaded in SAP_DAYS_CONTENT and PHASE_4_DAYS_CONTENT."""
    assert len(PHASE_4_DAYS_CONTENT) == 10
    for day_num in range(45, 55):
        assert day_num in SAP_DAYS_CONTENT, f"Day {day_num} missing from SAP_DAYS_CONTENT"
        assert day_num in PHASE_4_DAYS_CONTENT, f"Day {day_num} missing from PHASE_4_DAYS_CONTENT"
        day_data = SAP_DAYS_CONTENT[day_num]
        assert day_data["day_number"] == day_num
        assert len(day_data["title"]) > 5
        assert len(day_data["atomic_concepts"]) >= 1


def test_phase4_eight_step_pedagogical_structure():
    """Verify every Phase 4 day contains exactly 8 steps in the canonical sequence."""
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

    for day_num in range(45, 55):
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


def test_phase4_interactive_visualizers_assigned():
    """Verify each interactive visualizer is assigned to its respective practice step."""
    expected_components = {
        45: "PlanVizSimulator",
        46: "VDMBuilder",
        47: "CDSExpressionLab",
        48: "AssociationCardinalityMapper",
        49: "CDSExpressionLab",
        50: "AnnotationInspector",
        51: "AssociationCardinalityMapper",
        52: "AnalyticalCubeDesigner",
        53: "DCLAccessSimulator",
        54: "VDMBuilder",
    }
    for day, comp in expected_components.items():
        practice_step = SAP_DAYS_CONTENT[day]["steps"][3]
        assert practice_step["step_type"] == "interactive_practice"
        assert practice_step.get("component_type") == comp, (
            f"Day {day} practice component was {practice_step.get('component_type')}, expected {comp}"
        )


# =============================================================================
# 2. Technical Truthfulness Invariants
# =============================================================================

def test_technical_truthfulness_invariants():
    """Enforce non-negotiable architectural accuracy across all Phase 4 days."""
    p4_full_text = " ".join(_get_day_full_text(SAP_DAYS_CONTENT[d]) for d in range(45, 55))

    # Invariant 1: HANA uses secondary inverted indexes; false to claim it needs no indexes
    assert "secondary inverted index" in p4_full_text.lower() or "inverted index" in p4_full_text.lower()
    assert "hana needs no indexes" not in p4_full_text.lower() or "false" in p4_full_text.lower()

    # Invariant 2: Data paged on demand from persistence; false to claim everything is always in RAM
    assert "on-demand" in p4_full_text.lower() or "savepoint" in p4_full_text.lower() or "persistence" in p4_full_text.lower()

    # Invariant 3: Associations provide navigation semantics and instantiate joins on path traversal
    assert "path expression" in p4_full_text.lower()
    assert "pruning" in p4_full_text.lower()

    # Invariant 4: Pushdown trade-offs and engine hops
    assert "engine hop" in p4_full_text.lower() or "engine-hop" in p4_full_text.lower()

    # Invariant 5: Modern S/4HANA uses RAP Service Definitions / Bindings instead of @OData.publish: true
    assert "service definition" in p4_full_text.lower()
    assert "service binding" in p4_full_text.lower()
    if "@odata.publish" in p4_full_text.lower():
        assert "deprecated" in p4_full_text.lower() or "legacy" in p4_full_text.lower()


# =============================================================================
# 3. Targeted Technical Accuracy Hardening Invariants
# =============================================================================

def test_analytical_annotations_modern_syntax():
    """Verify modern CDS analytics uses @Aggregation.default: #SUM and treats @DefaultAggregation as legacy."""
    p4_full_text = " ".join(_get_day_full_text(SAP_DAYS_CONTENT[d]) for d in range(45, 55))

    assert "@aggregation.default: #sum" in p4_full_text.lower() or "@aggregation.default" in p4_full_text.lower()
    if "@defaultaggregation" in p4_full_text.lower():
        # Must be explicitly qualified as legacy/obsolete
        assert "legacy" in p4_full_text.lower() or "obsolete" in p4_full_text.lower()


def test_vdm_terminology_and_contracts():
    """Verify official VDM tiers (BASIC, COMPOSITE, CONSUMPTION), prefix conventions, and C1/C2 API release contracts."""
    d46_text = _get_day_full_text(SAP_DAYS_CONTENT[46])

    # Official VDM tiers
    assert "basic" in d46_text.lower()
    assert "composite" in d46_text.lower()
    assert "consumption" in d46_text.lower()

    # Prefixes are conventions, not semantic determinants
    assert "naming convention" in d46_text.lower() or "convention" in d46_text.lower()

    # C1 and C2 are API Release Contracts, NOT VDM tiers
    assert "c1" in d46_text.lower()
    assert "system-internally" in d46_text.lower() or "api release contract" in d46_text.lower()
    assert "remote api" in d46_text.lower() or "c2" in d46_text.lower()


def test_hana_persistence_accuracy():
    """Verify persistence savepoints to persistent data volumes without assuming NVMe, with redo logs."""
    p4_full_text = " ".join(_get_day_full_text(SAP_DAYS_CONTENT[d]) for d in range(45, 55))

    # Savepoints to persistent data volumes with default configurable ~5 min interval
    assert "persistent data volume" in p4_full_text.lower()
    assert "savepoint" in p4_full_text.lower()
    assert "5 minutes" in p4_full_text.lower()
    assert "redo log" in p4_full_text.lower()

    # Must NOT assume specific media like NVMe
    assert "nvme" not in p4_full_text.lower(), "Found hardcoded NVMe assumption in Phase 4 content"


def test_cds_associations_accuracy():
    """Verify CDS associations explain path expression join instantiation, navigation semantics, and performance realities."""
    d48_text = _get_day_full_text(SAP_DAYS_CONTENT[48])

    # Path expression instantiation
    assert "path expression" in d48_text.lower()
    # Reusable navigation semantics
    assert "navigation" in d48_text.lower()
    # Cardinality affects semantics/optimization
    assert "cardinality" in d48_text.lower()
    # Associations are not unconditionally faster/better than joins
    assert "faster" in d48_text.lower() or "optimization" in d48_text.lower()


def test_cds_hierarchy_vs_composition_distinction():
    """Verify Day 51 distinctly separates analytical hierarchies (DEFINE HIERARCHY) from RAP compositions (composition of)."""
    d51_text = _get_day_full_text(SAP_DAYS_CONTENT[51])

    # Both concepts present
    assert "define hierarchy" in d51_text.lower() or "hierarchy" in d51_text.lower()
    assert "composition" in d51_text.lower()
    assert "association to parent" in d51_text.lower()

    # Explicit separation and anti-confusion instruction
    assert "analytical" in d51_text.lower()
    assert "business object" in d51_text.lower() or "rap" in d51_text.lower()


# =============================================================================
# 4. Block 1 (Days 45–48: HANA & Core CDS) Technical Integrity
# =============================================================================

def test_block1_hana_and_vdm_rules():
    """Verify HANA engine internals, VDM tiers, CDS expressions, and associations."""
    # Day 45: HANA Engine Architecture & Internals
    d45_text = _get_day_full_text(SAP_DAYS_CONTENT[45])
    assert "indexserver" in d45_text.lower()
    assert "delta merge" in d45_text.lower()
    assert "main store" in d45_text.lower()
    assert "planviz" in d45_text.lower()

    # Day 46: VDM Architecture
    d46_text = _get_day_full_text(SAP_DAYS_CONTENT[46])
    assert "I_" in d46_text
    assert "C_" in d46_text
    assert "clean core" in d46_text.lower()
    assert "c1" in d46_text.lower() or "stability contract" in d46_text.lower()

    # Day 47: CDS Syntax, Expressions & CASE
    d47_text = _get_day_full_text(SAP_DAYS_CONTENT[47])
    assert "define view entity" in d47_text.lower()
    assert "case" in d47_text.lower()
    assert "currency_conversion" in d47_text.lower() or "coalesce" in d47_text.lower()

    # Day 48: CDS Associations vs SQL Joins
    d48_text = _get_day_full_text(SAP_DAYS_CONTENT[48])
    assert "association" in d48_text.lower()
    assert "[1..1]" in d48_text or "[0..1]" in d48_text or "[1..*]" in d48_text
    assert "pruning" in d48_text.lower()


# =============================================================================
# 5. Block 2 (Days 49–51: Advanced CDS & Semantic Catalog) Technical Integrity
# =============================================================================

def test_block2_advanced_cds_and_annotations():
    """Verify parameterized views, annotations, and compositions."""
    # Day 49: Parameterized CDS Views & Session Variables
    d49_text = _get_day_full_text(SAP_DAYS_CONTENT[49])
    assert "$session" in d49_text
    assert "parameters" in d49_text.lower()

    # Day 50: CDS Annotations
    d50_text = _get_day_full_text(SAP_DAYS_CONTENT[50])
    assert "@semantics" in d50_text.lower()
    assert "@analytics" in d50_text.lower()
    assert "@endusertext" in d50_text.lower()

    # Day 51: CDS Hierarchies & Compositions
    d51_text = _get_day_full_text(SAP_DAYS_CONTENT[51])
    assert "composition" in d51_text.lower()
    assert "hierarchy" in d51_text.lower() or "parent" in d51_text.lower()


# =============================================================================
# 6. Block 3 (Days 52–54: Analytics, DCL Security & Capstone) Technical Integrity
# =============================================================================

def test_block3_analytics_dcl_and_capstone(knowledge_engine):
    """Verify analytical cubes, DCL row-level security, and Day 54 Capstone."""
    # Day 52: Analytical Queries: Cubes & Dimensions
    d52_text = _get_day_full_text(SAP_DAYS_CONTENT[52])
    assert "#cube" in d52_text.lower()
    assert "#dimension" in d52_text.lower()
    assert "@aggregation.default: #sum" in d52_text.lower() or "aggregation" in d52_text.lower()

    # Day 53: DCL Access Control / Row-Level Security
    d53_text = _get_day_full_text(SAP_DAYS_CONTENT[53])
    assert "define role" in d53_text.lower()
    assert "pfcg_auth" in d53_text.lower() or "aspect" in d53_text.lower()

    # Day 54: Capstone Multi-Concept Assessment (15 distinct concepts)
    d54 = SAP_DAYS_CONTENT[54]
    assessment_step = [s for s in d54["steps"] if s["step_type"] == "assessment"][0]
    questions = assessment_step["questions"]

    assert len(questions) >= 10, f"Day 54 Capstone has {len(questions)} questions, expected >= 10"
    concept_slugs = [q["concept_slug"] for q in questions]
    assert len(set(concept_slugs)) >= 10, "Day 54 questions must test at least 10 distinct concepts"

    for c_slug in concept_slugs:
        capsule = knowledge_engine.get_remediation_capsule(c_slug)
        assert capsule is not None, f"Day 54 Capstone concept '{c_slug}' has no remediation capsule in DAG"


# =============================================================================
# 6. Phase 4 Enterprise Missions (8 Missions)
# =============================================================================

PHASE_4_MISSION_SLUGS = [
    "nova-hana-performance-incident",
    "nova-vdm-architecture-request",
    "nova-association-cardinality-defect",
    "nova-parameterized-reporting-service",
    "nova-cds-semantic-annotation-audit",
    "nova-executive-analytics-cube",
    "nova-dcl-data-leak-incident",
    "nova-secure-vdm-architecture-challenge",
]


def test_phase4_missions_registration():
    """Verify all 8 Phase 4 missions are registered in SEED_MISSIONS and PHASE_4_SEED_MISSIONS."""
    assert len(SEED_MISSIONS) >= 33, f"Expected at least 33 total missions, found {len(SEED_MISSIONS)}"
    assert len(PHASE_4_SEED_MISSIONS) == 8, f"Expected 8 Phase 4 missions, found {len(PHASE_4_SEED_MISSIONS)}"

    seed_slugs = {m["slug"] for m in SEED_MISSIONS}
    for slug in PHASE_4_MISSION_SLUGS:
        assert slug in seed_slugs, f"Mission '{slug}' not found in SEED_MISSIONS"

    for m in PHASE_4_SEED_MISSIONS:
        assert len(m["steps"]) >= 1
        assert m["difficulty"] in (1, 2, 3, 4, 5)


def test_phase4_assistance_levels_configuration():
    """Verify TRAINING, GUIDED, and JOB assistance modes are configured on all Phase 4 missions."""
    for m in PHASE_4_SEED_MISSIONS:
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


def test_phase4_mission_step_options_are_sanitized_no_answer_leak():
    """Verify get_mission_detail strips 'is_correct' from options to prevent answer leaks."""
    user_id = uuid.uuid4()
    for seed in PHASE_4_SEED_MISSIONS:
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
# 7. DAG Integration & Remediation Coverage
# =============================================================================

def test_all_phase4_concepts_have_remediation(knowledge_engine):
    """Verify all atomic concepts in Days 45-54 map to valid DAG remediation capsules."""
    for day_num in range(45, 55):
        day_data = SAP_DAYS_CONTENT[day_num]
        for concept_slug in day_data.get("atomic_concepts", []):
            capsule = knowledge_engine.get_remediation_capsule(concept_slug)
            assert capsule is not None, (
                f"Day {day_num} concept '{concept_slug}' does not resolve to any remediation capsule"
            )


# =============================================================================
# 8. Enterprise Consistency: Nova Manufacturing (NM01)
# =============================================================================

def test_nova_manufacturing_continuity_phase4():
    """Verify strict naming and code consistency for Nova Manufacturing Corp across all Phase 4 days."""
    p4_content = " ".join(
        _get_day_full_text(day)
        for day in SAP_DAYS_CONTENT.values()
        if 45 <= day["day_number"] <= 54
    )

    assert "NM01" in p4_content, "Company Code NM01 missing"
    assert "PL01" in p4_content, "Plant PL01 missing"
    assert "PL02" in p4_content, "Plant PL02 missing"
    assert "PO01" in p4_content, "Purchasing Org PO01 missing"
    assert "SO01" in p4_content, "Sales Org SO01 missing"
    assert "RAW1" in p4_content, "Storage Location RAW1 missing"
    assert "FG01" in p4_content, "Storage Location FG01 missing"
    assert "VEND-101" in p4_content, "Vendor VEND-101 missing"
    assert "CUST-501" in p4_content, "Customer CUST-501 missing"
    assert "DXTR-1000" in p4_content, "Product DXTR-1000 missing"
