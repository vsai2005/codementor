"""SAP Enterprise Mission Engine.

Manages authored business missions, DAG prerequisite enforcement, multi-step scenario evaluation,
and skill evidence generation.
"""

from __future__ import annotations

import copy
import uuid
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import select
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


class SAPMissionService:
    """Service managing authored missions, attempts, state consequences, and skill evidence."""

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
        mastered_concept_ids = {r.concept_id for r in mastery_rows if r.mastery_score >= 70.0}

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
            prereqs = list(m.prerequisite_concepts or [])
            is_unlocked = True
            missing_prereqs: list[str] = []

            for p_slug in prereqs:
                cid = slug_to_id.get(p_slug)
                if cid and cid not in mastered_concept_ids:
                    # If this is early mission 1 or learner is fresher, allow mission 1
                    if m.difficulty > 1:
                        is_unlocked = False
                        missing_prereqs.append(p_slug)

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
            "steps": mission.steps,
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
        """Starts or resumes a mission attempt."""
        cls.seed_missions_if_needed(db)
        mission = db.execute(
            select(SAPMission).where(SAPMission.slug == slug)
        ).scalar_one_or_none()
        if not mission:
            raise ValueError(f"Mission '{slug}' not found.")

        # Check existing active attempt
        attempt = db.execute(
            select(SAPMissionAttempt).where(
                SAPMissionAttempt.user_id == user_id,
                SAPMissionAttempt.mission_id == mission.id,
                SAPMissionAttempt.status.in_([SAPMissionAttemptStatus.STARTED.value, SAPMissionAttemptStatus.IN_PROGRESS.value]),
            )
        ).scalar_one_or_none()

        now = datetime.now(timezone.utc)
        if attempt is None:
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
                started_at=now,
            )
            db.add(attempt)
        else:
            attempt.assistance_level = assistance_level

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
        """Evaluates a mission step or complete mission, records skill evidence, and applies state mutations."""
        cls.seed_missions_if_needed(db)
        mission = db.execute(
            select(SAPMission).where(SAPMission.slug == slug)
        ).scalar_one_or_none()
        if not mission:
            raise ValueError(f"Mission '{slug}' not found.")

        attempt = cls.start_mission(db, user_id, slug, assistance_level)

        steps = list(mission.steps or [])
        target_step = next((s for s in steps if s.get("step_id") == step_id), None)
        if not target_step and steps:
            target_step = steps[0]

        step_type = target_step.get("step_type", "choose_action") if target_step else "choose_action"
        is_step_correct = True
        step_feedback = ""

        # Step validation logic
        if step_type in {"read_context", "choose_action", "make_decision"}:
            selected_id = payload.get("selected_option_id")
            options = target_step.get("options", []) if target_step else []
            correct_opt = next((o for o in options if o.get("is_correct")), None)
            if correct_opt and selected_id != correct_opt.get("id"):
                is_step_correct = False
                step_feedback = f"Incorrect choice. Best practice: {correct_opt.get('label')}"
            else:
                step_feedback = "Correct selection! Architectural requirement satisfied."

        elif step_type == "order_process":
            submitted_order = payload.get("ordered_items", [])
            expected_order = target_step.get("correct_order", []) if target_step else []
            if submitted_order != expected_order:
                is_step_correct = False
                step_feedback = "Order mismatch in organizational hierarchy."
            else:
                step_feedback = "Hierarchy ordering verified."

        now = datetime.now(timezone.utc)
        completed_steps = list(attempt.steps_completed or [])
        if step_id not in completed_steps:
            completed_steps.append(step_id)
        attempt.steps_completed = completed_steps

        # Update attempt score
        total_steps = max(1, len(steps))
        step_score = (100.0 / total_steps) if is_step_correct else 0.0
        attempt.score = round(min(100.0, float(attempt.score) + step_score), 1)

        # Check overall pass criteria
        min_pass = float((mission.success_criteria or {}).get("min_score", 70.0))
        attempt.passed = bool(attempt.score >= min_pass and len(completed_steps) >= total_steps)

        if attempt.passed:
            attempt.status = SAPMissionAttemptStatus.COMPLETED.value
            attempt.completed_at = now
            if attempt.started_at:
                attempt.duration_seconds = int((now - attempt.started_at).total_seconds())

            # 1. Apply deterministic enterprise state consequence
            mutation_patch = {}
            if mission.slug == "nova-org-structure-design":
                mutation_patch = {
                    "org_structure_status": "VALIDATED_ENTERPRISE_STRUCTURE",
                    "primary_company_code": "NM01",
                }
            elif mission.slug == "nova-plant-expansion":
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
            elif mission.slug == "nova-purchase-flow-trace":
                mutation_patch = {
                    "procurement_flow_audited": True,
                    "last_p2p_trace": "PR_PO_MIGO_MIRO_VALIDATED",
                }
            elif mission.slug == "nova-sap-product-selection":
                mutation_patch = {
                    "landscape_governance": "CLEAN_CORE_BTP_ALIGNED",
                }
            elif mission.slug == "nova-architecture-layer-incident":
                mutation_patch = {
                    "architecture_incident": "RESOLVED_BGD_BATCH_CONFIGURED",
                    "work_process_status": "STABLE_BALANCED",
                }
            elif mission.slug == "nova-p2p-workflow-incident":
                mutation_patch = {
                    "pending_incident": "RESOLVED",
                    "finance_state": {"gr_ir_clearing_status": "BALANCED_OK"},
                }

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
            for c_slug in (mission.concept_slugs or []):
                evidence_data = {
                    "source_type": SAPSkillEvidenceSourceType.MISSION.value,
                    "source_id": str(mission.id),
                    "mode": SAPLearningMode.MISSION.value,
                    "assistance_level": assistance_level,
                    "difficulty": mission.difficulty,
                    "score": attempt.score,
                    "result": "passed",
                    "evidence_summary": f"Completed enterprise mission: {mission.title}",
                    "details": {
                        "mission_slug": mission.slug,
                        "mission_type": mission.mission_type,
                        "steps_count": len(steps),
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
            "step_success": is_step_correct,
            "step_feedback": step_feedback,
            "mission_completed": attempt.passed,
            "mission_passed": attempt.passed,
            "current_score": attempt.score,
            "steps_completed_count": len(completed_steps),
            "total_steps": total_steps,
        }
