"""SAP Enterprise Mission Engine.

Manages authored business missions, DAG prerequisite enforcement, multi-step scenario evaluation,
and skill evidence generation.
"""

from __future__ import annotations

import copy
import uuid
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine
from app.models.sap_models import (
    SAPAssistanceLevel,
    SAPConcept,
    SAPLearningMode,
    SAPMission,
    SAPMissionAttempt,
    SAPMissionAttemptStatus,
    SAPMissionConcept,
    SAPMissionType,
    SAPSkillEvidenceSourceType,
    SAPUserConceptMastery,
)
from app.sap.services.enterprise import SAPEnterpriseService
from app.sap.services.mastery import SAPMasteryService
from app.sap.services.phase2_missions import PHASE_2_SEED_MISSIONS
from app.sap.services.phase3_missions import PHASE_3_SEED_MISSIONS
from app.sap.services.phase4_missions import PHASE_4_SEED_MISSIONS


# =============================================================================
# Seed Mission Definitions (3 Lightweight Architecture Missions)
# =============================================================================

SEED_MISSIONS: list[dict[str, Any]] = [
    {
        "slug": "nova-org-structure-design",
        "title": "Design Nova Manufacturing's Core Organizational Hierarchy",
        "description": "Nova Manufacturing is expanding its ERP footprint. Configure the organizational hierarchy linking Client, Company Code, Plants, and Procurement/Sales Organizations according to S/4HANA best practices.",
        "mission_type": SAPMissionType.CONFIGURATION.value,
        "difficulty": 1,
        "estimated_minutes": 15,
        "related_days": [4],
        "concept_slugs": [
            "org-structure-client",
            "org-structure-company-code",
            "org-structure-plant",
            "org-structure-logistics",
        ],
        "prerequisite_concepts": ["master-data-concept", "erp-evolution"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "The executive committee approved establishing the core SAP S/4HANA enterprise structure. You must assign the legal financial entity, primary manufacturing plant, and logistics organizations.",
        },
        "initial_state_patch": {},
        "target_state_criteria": {
            "primary_plant_assigned": "PL01",
            "purchasing_org_scope": "GLOBAL_CROSS_PLANT",
        },
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "In SAP S/4HANA, Company Code is the smallest organizational unit for which a complete, self-contained set of accounts can be drawn up.",
                    "Plant PL01 must belong directly to Company Code NM01 for financial valuation.",
                    "Purchasing Organization PO01 can be assigned to multiple plants for centralized global procurement.",
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": [
                    "Review the relationship between legal entities (Company Code) and logistical entities (Plants).",
                ],
                "show_prerequisite_primer": False,
            },
            "JOB": {
                "allow_hints": False,
                "hints": [],
                "show_prerequisite_primer": False,
            },
        },
        "steps": [
            {
                "step_id": "step_1_briefing",
                "title": "Analyze Enterprise Organizational Requirements",
                "step_type": "read_context",
                "instruction": "Review Nova Manufacturing's legal presence in Heidelberg (Germany) and select the primary legal entity code.",
                "options": [
                    {"id": "opt_client", "label": "Client 100", "is_correct": False},
                    {"id": "opt_nm01", "label": "Company Code NM01 (EUR)", "is_correct": True},
                    {"id": "opt_pl01", "label": "Plant PL01 (Heidelberg)", "is_correct": False},
                ],
            },
            {
                "step_id": "step_2_plant_assignment",
                "title": "Assign Manufacturing Facilities to Company Code",
                "step_type": "make_decision",
                "instruction": "Determine the structural assignment between Plant PL01 (Heidelberg) and legal entity NM01.",
                "options": [
                    {
                        "id": "opt_direct_assign",
                        "label": "Assign Plant PL01 to Company Code NM01 to enable direct balance sheet & P&L generation",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_standalone_plant",
                        "label": "Leave plants unassigned to company codes for cross-border tax evasion",
                        "is_correct": False,
                    },
                ],
            },
            {
                "step_id": "step_3_org_hierarchy",
                "title": "Establish Top-Down Structural Ordering",
                "step_type": "order_process",
                "instruction": "Order the organizational hierarchy from highest administrative level to granular storage location.",
                "correct_order": [
                    "Client (100)",
                    "Company Code (NM01)",
                    "Plant (PL01)",
                    "Storage Location (RM01)",
                ],
            },
        ],
        "success_criteria": {"min_score": 80.0},
        "failure_conditions": {"max_invalid_attempts": 3},
    },
    {
        "slug": "nova-plant-expansion",
        "title": "Nova Manufacturing Opens Plant PL02 in Austin",
        "description": "Nova Manufacturing has commissioned Plant PL02 in Austin for IoT sensor robotics. Configure the plant assignment, purchasing organization integration, and storage locations.",
        "mission_type": SAPMissionType.PROCESS_TASK.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [4, 5],
        "concept_slugs": [
            "org-structure-plant",
            "org-structure-logistics",
            "module-interconnectivity",
        ],
        "prerequisite_concepts": ["org-structure-company-code", "org-structure-plant"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "plant_code": "PL02",
            "scenario": "The new facility in Austin requires procurement connectivity with Global Purchasing Org PO01 and integration with automated material requirements planning (MRP).",
        },
        "initial_state_patch": {},
        "target_state_criteria": {"pl02_status": "INTEGRATED"},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "A plant can belong to only one Company Code in standard SAP.",
                    "A Purchasing Organization can procure for multiple plants if assigned appropriately.",
                    "Storage locations are always plant-specific.",
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": ["Check plant-to-purchasing-org assignment rules."],
                "show_prerequisite_primer": False,
            },
            "JOB": {
                "allow_hints": False,
                "hints": [],
                "show_prerequisite_primer": False,
            },
        },
        "steps": [
            {
                "step_id": "step_1_purchasing_link",
                "title": "Purchasing Organization Assignment",
                "step_type": "choose_action",
                "instruction": "How should Global Purchasing Org PO01 be integrated with the newly established Austin Plant PL02?",
                "options": [
                    {
                        "id": "opt_assign_po",
                        "label": "Assign Purchasing Org PO01 to Plant PL02 in Enterprise Structure Customizing",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_new_po_mandatory",
                        "label": "Create a completely separate SAP client for each plant",
                        "is_correct": False,
                    },
                ],
            },
            {
                "step_id": "step_2_storage_setup",
                "title": "Configure Storage Locations for Plant PL02",
                "step_type": "choose_action",
                "instruction": "Select the appropriate storage location setup for inbound component staging at Plant PL02.",
                "options": [
                    {
                        "id": "opt_loc_pl02",
                        "label": "Define Storage Location RM01 under Plant PL02 (Austin Inbound)",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_share_storage",
                        "label": "Assign Heidelberg's physical storage bins directly to Austin without network link",
                        "is_correct": False,
                    },
                ],
            },
            {
                "step_id": "step_3_valuation_ownership",
                "title": "Inventory Valuation Ownership",
                "step_type": "choose_action",
                "instruction": "Which legal entity reports inventory assets stored at Plant PL02?",
                "options": [
                    {
                        "id": "opt_val_nm01",
                        "label": "Company Code NM01 Balance Sheet (Plant PL02 is assigned to NM01)",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_val_vendor",
                        "label": "Supplier BP-101 Balance Sheet",
                        "is_correct": False,
                    },
                ],
            },
        ],
        "success_criteria": {"min_score": 80.0},
        "failure_conditions": {},
    },
    {
        "slug": "nova-purchase-flow-trace",
        "title": "Trace a Purchase Through the Enterprise",
        "description": "Follow a component procurement lifecycle for optical sensors from Purchase Requisition through Goods Receipt and Financial Settlement inside Nova Manufacturing.",
        "mission_type": SAPMissionType.PROCESS_TASK.value,
        "difficulty": 1,
        "estimated_minutes": 20,
        "related_days": [1, 3, 5],
        "concept_slugs": [
            "cross-functional-flows",
            "master-data-concept",
            "module-interconnectivity",
        ],
        "prerequisite_concepts": ["cross-functional-flows"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "material": "SENS-OPT-02 (Optical Sensor Module)",
            "scenario": "Assembly line PL01 requires 200 sensors. Trace the document sequence and identify which departments exchange data.",
        },
        "initial_state_patch": {},
        "target_state_criteria": {"procurement_traced": True},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Purchase Requisitions are internal requests; Purchase Orders are legally binding external contracts.",
                    "Goods Receipt (MIGO) touches both Materials Management and General Ledger via GR/IR.",
                    "Invoice Verification (MIRO) clears the GR/IR account and credits Vendor Accounts Payable.",
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": ["Review P2P document flow: PR → PO → MIGO → MIRO."],
                "show_prerequisite_primer": False,
            },
            "JOB": {
                "allow_hints": False,
                "hints": [],
                "show_prerequisite_primer": False,
            },
        },
        "steps": [
            {
                "step_id": "step_1_req_to_po",
                "title": "Internal Requisition to External Purchase Order",
                "step_type": "choose_action",
                "instruction": "Which organizational unit negotiates supplier pricing and converts an internal PR into a binding Purchase Order?",
                "options": [
                    {
                        "id": "opt_po_porg",
                        "label": "Purchasing Organization PO01 referencing Vendor Business Partner BP-101",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_po_sales",
                        "label": "Sales Organization SO01 referencing Customer BP-501",
                        "is_correct": False,
                    },
                ],
            },
            {
                "step_id": "step_2_gr_posting",
                "title": "Post Goods Receipt (MIGO)",
                "step_type": "choose_action",
                "instruction": "What dual posting occurs in General Ledger when 200 sensors are unloaded at Plant PL01 (MIGO)?",
                "options": [
                    {
                        "id": "opt_migo_gl",
                        "label": "Debit Inventory - Raw Materials (Asset) / Credit GR/IR Clearing Account (Liability)",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_migo_wrong",
                        "label": "Credit Bank Account / Debit CEO Personal Account",
                        "is_correct": False,
                    },
                ],
            },
            {
                "step_id": "step_3_invoice_clearing",
                "title": "Vendor Invoice Settlement (MIRO)",
                "step_type": "choose_action",
                "instruction": "How does Invoice Verification (MIRO) finalize the financial obligation to Supplier BP-101?",
                "options": [
                    {
                        "id": "opt_miro_gl",
                        "label": "Debit GR/IR Clearing Account (clearing to €0.00) / Credit Vendor Accounts Payable",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_miro_wrong",
                        "label": "Delete the purchase order from database history",
                        "is_correct": False,
                    },
                ],
            },
        ],
        "success_criteria": {"min_score": 80.0},
        "failure_conditions": {},
    },
    {
        "slug": "nova-sap-product-selection",
        "title": "Choose the Correct SAP Product & Architecture",
        "description": "Nova Manufacturing is evaluating digital transformation initiatives. Select the appropriate SAP product (S/4HANA, BTP, Signavio) and deployment model for each business requirement.",
        "mission_type": SAPMissionType.CONFIGURATION.value,
        "difficulty": 1,
        "estimated_minutes": 15,
        "related_days": [2],
        "concept_slugs": [
            "sap-portfolio-overview",
            "btp-positioning",
            "deployment-models-intro",
        ],
        "prerequisite_concepts": ["erp-evolution"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "scenario": "Nova's steering committee must allocate software licenses and cloud workloads adhering to Clean Core governance.",
        },
        "initial_state_patch": {},
        "target_state_criteria": {"portfolio_selected": True},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "S/4HANA is the digital core ERP.",
                    "BTP is for custom side-by-side apps, integration, and AI.",
                    "Signavio is for process mining and transformation modeling.",
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": ["Consider Clean Core: do custom extensions belong in the core or on BTP?"],
                "show_prerequisite_primer": False,
            },
            "JOB": {
                "allow_hints": False,
                "hints": [],
                "show_prerequisite_primer": False,
            },
        },
        "steps": [
            {
                "step_id": "step_1_side_by_side",
                "title": "Custom IoT Predictive Maintenance Application",
                "step_type": "choose_action",
                "instruction": "Where should Nova deploy a custom React/Node.js application that analyzes sensor telemetry and calls S/4HANA APIs?",
                "options": [
                    {
                        "id": "opt_btp",
                        "label": "SAP Business Technology Platform (BTP) using Cloud Foundry / Kyma runtime",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_core_mod",
                        "label": "Directly inside S/4HANA database by modifying standard SAP ABAP kernel",
                        "is_correct": False,
                    },
                ],
            },
            {
                "step_id": "step_2_core_choice",
                "title": "Core ERP Deployment Choice",
                "step_type": "choose_action",
                "instruction": "Nova has custom legacy assembly routines that require controlled upgrade cycles and dedicated cloud hosting. Which edition fits best?",
                "options": [
                    {
                        "id": "opt_private_cloud",
                        "label": "SAP S/4HANA Cloud Private Edition (Dedicated cloud infrastructure with upgrade flexibility)",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_excel",
                        "label": "Shared Google Sheets workbook",
                        "is_correct": False,
                    },
                ],
            },
            {
                "step_id": "step_3_process_mining",
                "title": "Process Mining & Bottleneck Analysis",
                "step_type": "choose_action",
                "instruction": "Which SAP product enables Nova to mine ERP event logs and visualize actual procurement bottlenecks?",
                "options": [
                    {
                        "id": "opt_signavio",
                        "label": "SAP Signavio Process Transformation Suite",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_gui",
                        "label": "Classic SAP GUI Notepad",
                        "is_correct": False,
                    },
                ],
            },
        ],
        "success_criteria": {"min_score": 80.0},
        "failure_conditions": {},
    },
    {
        "slug": "nova-architecture-layer-incident",
        "title": "Enterprise Architecture Incident: Diagnose the System Layer",
        "description": "Users in Heidelberg report application sluggishness and screen freezes during peak hours. Diagnose whether the issue originates in the Presentation, Application, or Database tier.",
        "mission_type": SAPMissionType.INCIDENT.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [6],
        "concept_slugs": [
            "three-tier-architecture",
            "abap-work-processes",
            "sap-gateway-concept",
        ],
        "prerequisite_concepts": ["three-tier-architecture"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "incident_severity": "HIGH",
            "scenario": "Order entry clerks report that transaction screens intermittently throw TIME_OUT errors, while background batches consume all server threads.",
        },
        "initial_state_patch": {"pending_incident": "WORK_PROCESS_STARVATION"},
        "target_state_criteria": {"incident_resolved": True},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Dialog (DIA) work processes have maximum runtime limits (e.g. 300s).",
                    "Long-running analytical or mass posting jobs must run in Background (BGD) work processes.",
                    "Web Dispatcher balances load across application servers.",
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": ["Review work process allocation: why would Dialog processes freeze?"],
                "show_prerequisite_primer": False,
            },
            "JOB": {
                "allow_hints": False,
                "hints": [],
                "show_prerequisite_primer": False,
            },
        },
        "steps": [
            {
                "step_id": "step_1_layer_isolation",
                "title": "Isolate the Architectural Layer",
                "step_type": "choose_action",
                "instruction": "Web browsers can reach SAP Web Dispatcher over HTTPS, and HANA Database CPU is at 8%. However, user requests hang. Which tier contains the bottleneck?",
                "options": [
                    {
                        "id": "opt_tier2_app",
                        "label": "Application Layer (AS ABAP) — Work process exhaustion in dialog pool",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_tier3_db",
                        "label": "Database Layer (SAP HANA) disk storage failure",
                        "is_correct": False,
                    },
                ],
            },
            {
                "step_id": "step_2_wp_remediation",
                "title": "Resolve Work Process Starvation",
                "step_type": "choose_action",
                "instruction": "Inspection reveals that a 4-hour material valuation report was triggered interactively in Dialog mode by accounting. What is the corrective action?",
                "options": [
                    {
                        "id": "opt_bgd_reschedule",
                        "label": "Cancel the interactive job and reschedule it as a Background Job (BGD work process) via SM36 during off-peak hours",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_kill_server",
                        "label": "Turn off power to the entire data center in Heidelberg",
                        "is_correct": False,
                    },
                ],
            },
        ],
        "success_criteria": {"min_score": 80.0},
        "failure_conditions": {},
    },
    {
        "slug": "nova-p2p-workflow-incident",
        "title": "Diagnose Purchase-to-Pay Accounting Posting Failure (Advanced)",
        "description": "A supplier invoice verification (MIRO) for 500 optical sensor modules failed at Plant PL01 due to an automatic account determination error. Diagnose the cross-module breakdown between MM and FI.",
        "mission_type": SAPMissionType.INCIDENT.value,
        "difficulty": 3,
        "estimated_minutes": 25,
        "related_days": [23],
        "concept_slugs": [
            "module-interconnectivity",
            "automatic-account-determination",
            "double-entry-accounting",
        ],
        "prerequisite_concepts": ["invoice-verification-miro", "goods-receipt-migo"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "tcode": "MIRO",
            "error_message": "Account determination for entry NM01 WRX not possible",
            "scenario": "Goods Receipt (MIGO) was posted successfully. However, when AP posted invoice verification (MIRO), the system failed to identify the GR/IR clearing account.",
        },
        "initial_state_patch": {"pending_incident": "GRIR_POSTING_LOCK"},
        "target_state_criteria": {"incident_resolved": True},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "WRX is the standard transaction key for the GR/IR clearing account.",
                    "Automatic account determination uses Chart of Accounts (YCOA), Valuation Class, and Transaction Key (WRX).",
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": ["Review transaction key WRX in OBYC settings."],
                "show_prerequisite_primer": False,
            },
            "JOB": {
                "allow_hints": False,
                "hints": [],
                "show_prerequisite_primer": False,
            },
        },
        "steps": [
            {
                "step_id": "step_1_error_diagnosis",
                "title": "Identify Failing Transaction Key",
                "step_type": "choose_action",
                "instruction": "Which SAP transaction key is responsible for determining the GR/IR clearing account during Goods Receipt and Invoice Verification?",
                "options": [
                    {"id": "opt_bsx", "label": "BSX (Inventory Balance Posting)", "is_correct": False},
                    {"id": "opt_wrx", "label": "WRX (GR/IR Clearing Account)", "is_correct": True},
                    {"id": "opt_prd", "label": "PRD (Price Differences)", "is_correct": False},
                ],
            },
            {
                "step_id": "step_2_remediation_action",
                "title": "Select Configuration Resolution in OBYC",
                "step_type": "make_decision",
                "instruction": "What customization action resolves the posting error for Chart of Accounts YCOA and Company Code NM01?",
                "options": [
                    {
                        "id": "opt_configure_wrx",
                        "label": "Maintain G/L account mapping for transaction key WRX in transaction OBYC for Chart of Accounts YCOA",
                        "is_correct": True,
                    },
                    {
                        "id": "opt_delete_po",
                        "label": "Delete the purchase order and pay the vendor in cash",
                        "is_correct": False,
                    },
                ],
            },
        ],
        "success_criteria": {"min_score": 80.0},
        "failure_conditions": {},
    },
]

# =============================================================================
# Authoritative Mission Registry Across All Supported Phases
# =============================================================================

class SAPMissionRegistry:
    """Authoritative mission registry across all supported curriculum phases.

    Enforces uniqueness of mission slugs, prevents duplicate definitions, and guarantees
    every registered mission is retrievable by canonical slug.
    """

    _missions: list[dict[str, Any]] = []
    _by_slug: dict[str, dict[str, Any]] = {}
    _initialized: bool = False

    @classmethod
    def initialize(cls) -> None:
        """Initializes the registry from all supported phases and validates uniqueness."""
        if cls._initialized:
            return
        raw_missions = (
            SEED_MISSIONS_PHASE_1
            + PHASE_2_SEED_MISSIONS
            + PHASE_3_SEED_MISSIONS
            + PHASE_4_SEED_MISSIONS
        )
        seen_slugs: set[str] = set()
        cls._missions = []
        cls._by_slug = {}
        for m in raw_missions:
            slug = m["slug"]
            if slug in seen_slugs:
                raise ValueError(f"Duplicate mission slug detected in registry: '{slug}'")
            seen_slugs.add(slug)
            cls._missions.append(m)
            cls._by_slug[slug] = m
        cls._initialized = True

    @classmethod
    def get_all(cls) -> list[dict[str, Any]]:
        cls.initialize()
        return list(cls._missions)

    @classmethod
    def get(cls, slug: str) -> dict[str, Any] | None:
        cls.initialize()
        return cls._by_slug.get(slug)

    @classmethod
    def contains(cls, slug: str) -> bool:
        cls.initialize()
        return slug in cls._by_slug

    @classmethod
    def count(cls) -> int:
        cls.initialize()
        return len(cls._missions)

    @classmethod
    def get_slugs(cls) -> set[str]:
        cls.initialize()
        return set(cls._by_slug.keys())


SEED_MISSIONS_PHASE_1 = SEED_MISSIONS[:5]
SAPMissionRegistry.initialize()
SEED_MISSIONS = SAPMissionRegistry.get_all()


OPTION_STEP_TYPES = frozenset({
    "read_context", "choose_action", "make_decision", "decision", "troubleshoot", "config",
})


class SAPMissionNotFoundError(ValueError):
    """Mission slug is not in the authoritative registry (HTTP 404)."""


class SAPMissionLockedError(ValueError):
    """Learner has not satisfied the mission's prerequisites (HTTP 403)."""


class SAPMissionStepNotFoundError(ValueError):
    """step_id is not one of the mission's registered steps (HTTP 404)."""


class SAPMissionSubmissionError(ValueError):
    """Submission is malformed for the step, or the step is not gradable (HTTP 400)."""


class SAPMissionService:
    """Service managing authored missions, attempts, state consequences, and skill evidence."""

    PREREQUISITE_MASTERY_THRESHOLD = 70.0

    @classmethod
    def seed_missions_if_needed(cls, db: Session) -> list[SAPMission]:
        """Seeds default architecture missions and links them to concepts and enterprise."""
        template = SAPEnterpriseService.get_or_create_template(db)
        engine = SAPCurriculumKnowledgeEngine.get_instance()

        seeded: list[SAPMission] = []
        for m_data in SEED_MISSIONS:
            m = db.execute(
                select(SAPMission).where(SAPMission.slug == m_data["slug"])
            ).scalar_one_or_none()

            if m is None:
                m = SAPMission(
                    slug=m_data["slug"],
                    title=m_data["title"],
                    description=m_data["description"],
                    mission_type=m_data["mission_type"],
                    difficulty=m_data["difficulty"],
                    enterprise_id=template.id,
                    company_context=copy.deepcopy(m_data["company_context"]),
                    initial_state_patch=copy.deepcopy(m_data.get("initial_state_patch", {})),
                    target_state_criteria=copy.deepcopy(m_data.get("target_state_criteria", {})),
                    related_days=copy.deepcopy(m_data.get("related_days", [])),
                    concept_slugs=copy.deepcopy(m_data.get("concept_slugs", [])),
                    prerequisite_concepts=copy.deepcopy(m_data.get("prerequisite_concepts", [])),
                    assistance_rules=copy.deepcopy(m_data.get("assistance_rules", {})),
                    steps=copy.deepcopy(m_data.get("steps", [])),
                    success_criteria=copy.deepcopy(m_data.get("success_criteria", {})),
                    failure_conditions=copy.deepcopy(m_data.get("failure_conditions", {})),
                    estimated_minutes=m_data.get("estimated_minutes", 20),
                    is_active=True,
                )
                db.add(m)
                db.flush()

                # Link concepts relationally
                for c_slug in m_data.get("concept_slugs", []):
                    c = db.execute(select(SAPConcept).where(SAPConcept.slug == c_slug)).scalar_one_or_none()
                    if c is None:
                        c_meta = engine.get_concept(c_slug)
                        if c_meta:
                            c = SAPConcept(slug=c_meta.slug, name=c_meta.name, category=c_meta.category, difficulty=c_meta.difficulty)
                            db.add(c)
                            db.flush()
                    if c:
                        link = SAPMissionConcept(mission_id=m.id, concept_id=c.id, relevance="PRIMARY")
                        db.add(link)
            else:
                m.title = m_data["title"]
                m.description = m_data["description"]
                m.mission_type = m_data["mission_type"]
                m.difficulty = m_data["difficulty"]
                m.company_context = copy.deepcopy(m_data["company_context"])
                m.related_days = copy.deepcopy(m_data.get("related_days", []))
                m.concept_slugs = copy.deepcopy(m_data.get("concept_slugs", []))
                m.prerequisite_concepts = copy.deepcopy(m_data.get("prerequisite_concepts", []))
                m.assistance_rules = copy.deepcopy(m_data.get("assistance_rules", {}))
                m.steps = copy.deepcopy(m_data.get("steps", []))
                m.success_criteria = copy.deepcopy(m_data.get("success_criteria", {}))

            seeded.append(m)

        db.commit()
        return seeded

    @classmethod
    def list_missions_for_user(cls, db: Session, user_id: uuid.UUID) -> list[dict[str, Any]]:
        """Lists available missions for a learner, computing unlock status and attempt progress."""
        cls.seed_missions_if_needed(db)

        # Get learner mastered concepts
        mastery_rows = db.execute(
            select(SAPUserConceptMastery).where(SAPUserConceptMastery.user_id == user_id)
        ).scalars().all()
        mastered_concept_ids = {
            r.concept_id for r in mastery_rows
            if r.mastery_score >= cls.PREREQUISITE_MASTERY_THRESHOLD
        }

        # Get concepts mapping
        concepts = db.execute(select(SAPConcept)).scalars().all()
        slug_to_id = {c.slug: c.id for c in concepts}

        # Get learner mission attempts
        attempts = db.execute(
            select(SAPMissionAttempt).where(SAPMissionAttempt.user_id == user_id)
        ).scalars().all()
        attempt_map = {a.mission_id: a for a in attempts}

        missions = db.execute(
            select(SAPMission).where(SAPMission.is_active == True)  # noqa: E712
        ).scalars().all()

        results: list[dict[str, Any]] = []
        for m in missions:
            # Check DAG prerequisites: all required concepts must be mastered or introduced
            missing_prereqs = cls._missing_prerequisites(
                m.difficulty,
                m.prerequisite_concepts,
                slug_to_id=slug_to_id,
                mastered_concept_ids=mastered_concept_ids,
            )
            is_unlocked = not missing_prereqs

            att = attempt_map.get(m.id)
            results.append({
                "id": str(m.id),
                "slug": m.slug,
                "title": m.title,
                "description": m.description,
                "mission_type": m.mission_type,
                "difficulty": m.difficulty,
                "estimated_minutes": m.estimated_minutes,
                "related_days": list(m.related_days or []),
                "concept_slugs": list(m.concept_slugs or []),
                "is_unlocked": is_unlocked,
                "missing_prerequisites": missing_prereqs,
                "attempt_status": att.status if att else "not_started",
                "score": att.score if att else None,
                "passed": att.passed if att else False,
            })

        return results

    @classmethod
    def get_mission_detail(
        cls,
        db: Session,
        user_id: uuid.UUID,
        slug: str,
        assistance_level: str = SAPAssistanceLevel.TRAINING.value,
    ) -> dict[str, Any]:
        """Retrieves complete mission details with company context and assistance rules filtered by level."""
        mission = db.execute(
            select(SAPMission).where(SAPMission.slug == slug)
        ).scalar_one_or_none()
        if not mission:
            cls.seed_missions_if_needed(db)
            mission = db.execute(
                select(SAPMission).where(SAPMission.slug == slug)
            ).scalar_one_or_none()
        if not mission:
            raise ValueError(f"Mission '{slug}' not found.")

        # Ensure learner digital twin instance exists
        instance = SAPEnterpriseService.get_or_create_instance(db, user_id)

        # Filter assistance rules according to level
        level_key = assistance_level.upper()
        rules = (mission.assistance_rules or {}).get(level_key, {})

        # Fetch latest attempt if any
        attempt = db.execute(
            select(SAPMissionAttempt).where(
                SAPMissionAttempt.user_id == user_id,
                SAPMissionAttempt.mission_id == mission.id,
            ).order_by(SAPMissionAttempt.started_at.desc())
        ).scalars().first()

        # Sanitize steps so is_correct is not leaked to the frontend
        sanitized_steps = []
        for step in (mission.steps or []):
            s_copy = dict(step)
            if "options" in s_copy:
                s_copy["options"] = [
                    {k: v for k, v in opt.items() if k != "is_correct"}
                    for opt in s_copy["options"]
                ]
            sanitized_steps.append(s_copy)

        return {
            "id": str(mission.id),
            "slug": mission.slug,
            "title": mission.title,
            "description": mission.description,
            "mission_type": mission.mission_type,
            "difficulty": mission.difficulty,
            "estimated_minutes": mission.estimated_minutes,
            "company_context": mission.company_context,
            "enterprise_code": instance.enterprise.code if instance.enterprise else "NM01",
            "company_state": instance.company_state,
            "assistance_level": assistance_level,
            "assistance_rules": rules,
            "steps": sanitized_steps,
            "related_days": mission.related_days,
            "concept_slugs": mission.concept_slugs,
            "current_attempt": {
                "status": attempt.status,
                "score": attempt.score,
                "passed": attempt.passed,
                "current_step_index": attempt.current_step_index,
            } if attempt else None,
        }

    @classmethod
    def start_mission(
        cls,
        db: Session,
        user_id: uuid.UUID,
        slug: str,
        assistance_level: str = SAPAssistanceLevel.TRAINING.value,
    ) -> SAPMissionAttempt:
        """Starts or resumes a mission attempt after verifying prerequisites server-side.

        Raises SAPMissionNotFoundError for unregistered slugs and SAPMissionLockedError when
        the learner has not mastered the mission's prerequisite concepts; both leave state
        untouched. A mission that was already completed returns its completed attempt.
        """
        cls._validate_assistance_level(assistance_level)
        mission, definition = cls._resolve_mission(db, slug)
        cls._require_unlocked(db, user_id, definition)

        attempt = cls._get_or_create_attempt(db, user_id, mission, assistance_level)
        db.commit()
        db.refresh(attempt)
        return attempt

    @classmethod
    def submit_step_attempt(
        cls,
        db: Session,
        user_id: uuid.UUID,
        slug: str,
        step_id: str,
        payload: dict[str, Any],
        assistance_level: str = SAPAssistanceLevel.TRAINING.value,
    ) -> dict[str, Any]:
        """Grades one registered mission step; completion derives only from graded steps.

        - Unknown mission -> SAPMissionNotFoundError; locked -> SAPMissionLockedError;
          unknown step -> SAPMissionStepNotFoundError; malformed payload ->
          SAPMissionSubmissionError. All raise before any write.
        - A wrong answer returns step_success=False and writes nothing.
        - A correct answer marks that exact step passed once; repeats are idempotent.
        - The mission completes (state mutation + skill evidence, exactly once) when every
          registered step has been passed.
        """
        cls._validate_assistance_level(assistance_level)
        mission, definition = cls._resolve_mission(db, slug)
        cls._require_unlocked(db, user_id, definition)

        # The registered definition is authoritative for steps, answer keys, and pass criteria.
        steps = list(definition.get("steps") or [])
        canonical_ids = [s.get("step_id") for s in steps]
        total_steps = len(canonical_ids)
        target_step = next((s for s in steps if s.get("step_id") == step_id), None)
        if target_step is None:
            raise SAPMissionStepNotFoundError(f"Step '{step_id}' not found in mission '{slug}'.")

        is_step_correct, step_feedback = cls._grade_step(target_step, payload)

        if not is_step_correct:
            existing = cls._find_latest_attempt(db, user_id, mission.id)
            passed_ids = cls._passed_canonical_steps(existing, canonical_ids)
            completed = bool(existing is not None and existing.passed)
            return {
                "step_id": step_id,
                "step_success": False,
                "step_feedback": step_feedback,
                "mission_completed": completed,
                "mission_passed": completed,
                "current_score": cls._score(passed_ids, total_steps),
                "steps_completed_count": len(passed_ids),
                "total_steps": total_steps,
            }

        attempt = cls._get_or_create_attempt(db, user_id, mission, assistance_level, lock=True)

        if attempt.status == SAPMissionAttemptStatus.COMPLETED.value:
            # Already completed: idempotent, no new score, state mutation, or evidence.
            passed_ids = cls._passed_canonical_steps(attempt, canonical_ids)
            db.commit()
            return {
                "step_id": step_id,
                "step_success": True,
                "step_feedback": step_feedback,
                "mission_completed": True,
                "mission_passed": bool(attempt.passed),
                "current_score": float(attempt.score),
                "steps_completed_count": len(passed_ids),
                "total_steps": total_steps,
            }

        now = datetime.now(timezone.utc)
        passed_set = set(cls._passed_canonical_steps(attempt, canonical_ids)) | {step_id}
        passed_ids = [sid for sid in canonical_ids if sid in passed_set]
        attempt.steps_completed = passed_ids
        responses = dict(attempt.learner_responses or {})
        responses[step_id] = cls._recorded_response(target_step, payload)
        attempt.learner_responses = responses
        attempt.score = cls._score(passed_ids, total_steps)
        attempt.current_step_index = next(
            (i for i, sid in enumerate(canonical_ids) if sid not in passed_set),
            max(0, total_steps - 1),
        )

        min_pass = float((definition.get("success_criteria") or {}).get("min_score", 70.0))
        attempt.passed = bool(len(passed_ids) == total_steps and attempt.score >= min_pass)

        if attempt.passed:
            attempt.status = SAPMissionAttemptStatus.COMPLETED.value
            attempt.completed_at = now
            if attempt.started_at:
                attempt.duration_seconds = int((now - attempt.started_at).total_seconds())

            # 1. Apply deterministic enterprise state consequence
            mutation_patch = cls._completion_patch(mission.slug)
            if mutation_patch:
                SAPEnterpriseService.apply_state_mutation(
                    db=db,
                    user_id=user_id,
                    enterprise_slug="nova-manufacturing",
                    mutation_action=f"MISSION_COMPLETED_{mission.slug}",
                    patch=mutation_patch,
                    mission_slug=mission.slug,
                )

            # 2. Record Skill Evidence for all tested concepts in the mission
            for c_slug in (definition.get("concept_slugs") or []):
                evidence_data = {
                    "source_type": SAPSkillEvidenceSourceType.MISSION.value,
                    "source_id": str(mission.id),
                    "mode": SAPLearningMode.MISSION.value,
                    "assistance_level": attempt.assistance_level,
                    "difficulty": mission.difficulty,
                    "score": attempt.score,
                    "result": "passed",
                    "evidence_summary": f"Completed enterprise mission: {mission.title}",
                    "details": {
                        "mission_slug": mission.slug,
                        "mission_type": mission.mission_type,
                        "steps_count": total_steps,
                    },
                }
                SAPMasteryService.record_skill_evidence(
                    db=db,
                    user_id=user_id,
                    concept_slug=c_slug,
                    evidence=evidence_data,
                )

        db.commit()
        db.refresh(attempt)

        return {
            "step_id": step_id,
            "step_success": True,
            "step_feedback": step_feedback,
            "mission_completed": attempt.passed,
            "mission_passed": attempt.passed,
            "current_score": attempt.score,
            "steps_completed_count": len(passed_ids),
            "total_steps": total_steps,
        }

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _validate_assistance_level(assistance_level: str) -> None:
        if assistance_level not in {lvl.value for lvl in SAPAssistanceLevel}:
            raise SAPMissionSubmissionError(
                f"Invalid assistance level '{assistance_level}'. Use TRAINING, GUIDED, or JOB."
            )

    @classmethod
    def _resolve_mission(cls, db: Session, slug: str) -> tuple[SAPMission, dict[str, Any]]:
        """Resolves a registered mission: its DB row (attempt FK) and its registry definition."""
        definition = SAPMissionRegistry.get(slug)
        if definition is None:
            raise SAPMissionNotFoundError(f"Mission '{slug}' not found.")
        mission = db.execute(
            select(SAPMission).where(SAPMission.slug == slug)
        ).scalar_one_or_none()
        if not mission:
            cls.seed_missions_if_needed(db)
            mission = db.execute(
                select(SAPMission).where(SAPMission.slug == slug)
            ).scalar_one_or_none()
        if not mission:
            raise SAPMissionNotFoundError(f"Mission '{slug}' not found.")
        return mission, definition

    @classmethod
    def _missing_prerequisites(
        cls,
        difficulty: int,
        prerequisite_concepts: list[str] | None,
        slug_to_id: dict[str, uuid.UUID],
        mastered_concept_ids: set[uuid.UUID],
    ) -> list[str]:
        """Authoritative unlock rule shared by the listing and every write path.

        Entry-level (difficulty 1) missions are open to every learner. Any other mission
        requires every prerequisite concept to be mastered; a prerequisite with no mastery
        record (including one never materialized as a concept row) counts as missing.
        """
        if difficulty <= 1:
            return []
        return [
            p for p in (prerequisite_concepts or [])
            if slug_to_id.get(p) not in mastered_concept_ids
        ]

    @classmethod
    def _require_unlocked(cls, db: Session, user_id: uuid.UUID, definition: dict[str, Any]) -> None:
        prereqs = list(definition.get("prerequisite_concepts") or [])
        difficulty = int(definition.get("difficulty", 1))
        if difficulty <= 1 or not prereqs:
            return
        rows = db.execute(
            select(SAPConcept.slug, SAPConcept.id)
            .join(SAPUserConceptMastery, SAPUserConceptMastery.concept_id == SAPConcept.id)
            .where(
                SAPUserConceptMastery.user_id == user_id,
                SAPUserConceptMastery.mastery_score >= cls.PREREQUISITE_MASTERY_THRESHOLD,
                SAPConcept.slug.in_(prereqs),
            )
        ).all()
        slug_to_id = {slug: cid for slug, cid in rows}
        missing = cls._missing_prerequisites(
            difficulty, prereqs, slug_to_id=slug_to_id, mastered_concept_ids=set(slug_to_id.values())
        )
        if missing:
            raise SAPMissionLockedError(
                f"Mission '{definition['slug']}' is locked. Master prerequisite concepts first: "
                f"{', '.join(missing)}."
            )

    @staticmethod
    def _lock_user_mission(db: Session, user_id: uuid.UUID, mission_id: uuid.UUID) -> None:
        """Serializes concurrent attempt creation/completion for one learner and mission."""
        bind = db.get_bind()
        if getattr(getattr(bind, "dialect", None), "name", None) == "postgresql":
            db.execute(
                text("SELECT pg_advisory_xact_lock(hashtextextended(:k, 0))"),
                {"k": f"sap-mission:{user_id}:{mission_id}"},
            )

    @staticmethod
    def _find_latest_attempt(
        db: Session, user_id: uuid.UUID, mission_id: uuid.UUID
    ) -> SAPMissionAttempt | None:
        """The learner's completed attempt if one exists, else the newest active one. Read-only."""
        attempts = db.execute(
            select(SAPMissionAttempt).where(
                SAPMissionAttempt.user_id == user_id,
                SAPMissionAttempt.mission_id == mission_id,
                SAPMissionAttempt.status.in_([
                    SAPMissionAttemptStatus.STARTED.value,
                    SAPMissionAttemptStatus.IN_PROGRESS.value,
                    SAPMissionAttemptStatus.COMPLETED.value,
                ]),
            ).order_by(SAPMissionAttempt.started_at.desc())
        ).scalars().all()
        completed = next(
            (a for a in attempts if a.status == SAPMissionAttemptStatus.COMPLETED.value), None
        )
        return completed or (attempts[0] if attempts else None)

    @classmethod
    def _get_or_create_attempt(
        cls,
        db: Session,
        user_id: uuid.UUID,
        mission: SAPMission,
        assistance_level: str,
        lock: bool = False,
    ) -> SAPMissionAttempt:
        """Returns the learner's completed or active attempt, creating one only if neither exists.

        Does not commit. A completed mission never spawns a new attempt, so completion
        consequences and skill evidence are recorded at most once per learner and mission.
        """
        cls._lock_user_mission(db, user_id, mission.id)
        attempt = cls._find_latest_attempt(db, user_id, mission.id)
        if attempt is not None:
            if lock:
                db.refresh(attempt, with_for_update=True)
            if attempt.status != SAPMissionAttemptStatus.COMPLETED.value:
                attempt.assistance_level = assistance_level
            return attempt

        attempt = SAPMissionAttempt(
            user_id=user_id,
            mission_id=mission.id,
            status=SAPMissionAttemptStatus.IN_PROGRESS.value,
            assistance_level=assistance_level,
            current_step_index=0,
            steps_completed=[],
            learner_responses={},
            state_mutations=[],
            score=0.0,
            passed=False,
            feedback={"message": "Mission started"},
            started_at=datetime.now(timezone.utc),
        )
        db.add(attempt)
        db.flush()
        return attempt

    @staticmethod
    def _passed_canonical_steps(
        attempt: SAPMissionAttempt | None, canonical_ids: list[str]
    ) -> list[str]:
        """Registered step ids recorded as passed; ignores anything not in the registry."""
        if attempt is None:
            return []
        recorded = set(attempt.steps_completed or [])
        return [sid for sid in canonical_ids if sid in recorded]

    @staticmethod
    def _score(passed_ids: list[str], total_steps: int) -> float:
        if total_steps <= 0:
            return 0.0
        return round(100.0 * len(passed_ids) / total_steps, 1)

    @staticmethod
    def _grade_step(step: dict[str, Any], payload: dict[str, Any]) -> tuple[bool, str]:
        """Grades a submission against the step's authored key. Fails closed.

        Raises SAPMissionSubmissionError when the payload is malformed for the step type or
        the step has no gradable answer key; an ungradable step is never treated as passed.
        """
        payload = payload if isinstance(payload, dict) else {}
        step_type = step.get("step_type")
        step_ref = step.get("step_id")

        if step_type in OPTION_STEP_TYPES:
            options = [o for o in (step.get("options") or []) if isinstance(o, dict)]
            correct = [o for o in options if o.get("is_correct") is True]
            if len(correct) != 1:
                raise SAPMissionSubmissionError(f"Step '{step_ref}' has no gradable answer key.")
            selected_id = payload.get("selected_option_id")
            if not isinstance(selected_id, str) or selected_id not in {o.get("id") for o in options}:
                raise SAPMissionSubmissionError(
                    f"A valid selected_option_id is required for step '{step_ref}'."
                )
            if selected_id != correct[0].get("id"):
                return False, f"Incorrect choice. Best practice: {correct[0].get('label')}"
            return True, "Correct selection! Architectural requirement satisfied."

        if step_type == "order_process":
            expected_order = step.get("correct_order")
            if not isinstance(expected_order, list) or not expected_order:
                raise SAPMissionSubmissionError(f"Step '{step_ref}' has no gradable answer key.")
            submitted_order = payload.get("ordered_items")
            if not isinstance(submitted_order, list) or not all(isinstance(i, str) for i in submitted_order):
                raise SAPMissionSubmissionError(
                    f"ordered_items (list of strings) is required for step '{step_ref}'."
                )
            if submitted_order != expected_order:
                return False, "Order mismatch in organizational hierarchy."
            return True, "Hierarchy ordering verified."

        raise SAPMissionSubmissionError(f"Step '{step_ref}' has unsupported step type '{step_type}'.")

    @staticmethod
    def _recorded_response(step: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        if step.get("step_type") == "order_process":
            return {"ordered_items": list(payload.get("ordered_items") or [])}
        return {"selected_option_id": payload.get("selected_option_id")}

    @staticmethod
    def _completion_patch(slug: str) -> dict[str, Any]:
        """Deterministic enterprise state consequence applied when a mission completes."""
        mutation_patch = {}
        if slug == "nova-org-structure-design":
            mutation_patch = {
                "org_structure_status": "VALIDATED_ENTERPRISE_STRUCTURE",
                "primary_company_code": "NM01",
            }
        elif slug == "nova-plant-expansion":
            mutation_patch = {
                "plants": [
                    {
                        "id": "PL02",
                        "name": "Austin Tech Center",
                        "status": "ACTIVE_INTEGRATED",
                        "company_code": "NM01",
                    }
                ]
            }
        elif slug == "nova-purchase-flow-trace":
            mutation_patch = {
                "procurement_flow_audited": True,
                "last_p2p_trace": "PR_PO_MIGO_MIRO_VALIDATED",
            }
        elif slug == "nova-sap-product-selection":
            mutation_patch = {
                "landscape_governance": "CLEAN_CORE_BTP_ALIGNED",
            }
        elif slug == "nova-architecture-layer-incident":
            mutation_patch = {
                "architecture_incident": "RESOLVED_BGD_BATCH_CONFIGURED",
                "work_process_status": "STABLE_BALANCED",
            }
        elif slug == "nova-s4hana-modernization-decision":
            mutation_patch = {
                "modernization_blueprint": "S4HANA_SIMPLIFICATION_APPROVED",
                "table_simplification_validated": True,
            }
        elif slug == "nova-universal-journal-investigation":
            mutation_patch = {
                "acdoca_reconciliation_status": "VERIFIED_BALANCED",
                "parallel_ledgers_audited": True,
            }
        elif slug == "nova-matdoc-inventory-incident":
            mutation_patch = {
                "inventory_ledger_status": "MATDOC_HIGH_CONCURRENCY_ACTIVE",
                "table_lock_incident": "RESOLVED",
            }
        elif slug == "nova-business-partner-migration":
            mutation_patch = {
                "cvi_sync_status": "CVI_SYNCHRONIZED_ACTIVE",
                "legacy_customers_vendors_migrated": True,
            }
        elif slug == "nova-cds-reporting-requirement":
            mutation_patch = {
                "vdm_reporting_status": "BASIC_COMPOSITE_CONSUMPTION_DEPLOYED",
                "code_pushdown_active": True,
            }
        elif slug == "nova-landscape-change-request":
            mutation_patch = {
                "cts_transport_route_status": "DEV_QAS_PRD_RELEASED",
                "direct_prd_changes_blocked": True,
            }
        elif slug == "nova-access-governance-incident":
            mutation_patch = {
                "fiori_access_status": "SPACES_PAGES_RBAC_ENFORCED",
                "sod_conflict_resolved": True,
            }
        elif slug == "nova-cross-module-document-trace":
            mutation_patch = {
                "document_chain_trace": "VBFA_TRANSPARENT_AUDITED",
                "sales_to_finance_reconciliation": "BALANCED_CLEAR",
            }
        elif slug == "nova-p2p-workflow-incident":
            mutation_patch = {
                "pending_incident": "RESOLVED",
                "finance_state": {"gr_ir_clearing_status": "BALANCED_OK"},
            }

        return mutation_patch
