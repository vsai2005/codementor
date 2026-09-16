"""Authoritative Phase 2 Enterprise Missions (Days 9–22).

8 cross-concept enterprise missions reflecting authentic operational challenges
at Nova Manufacturing Corp (NM01).
"""

from __future__ import annotations
from typing import Any
from app.models.sap_models import SAPMissionType

PHASE_2_SEED_MISSIONS: list[dict[str, Any]] = [
    # 1. S/4HANA Modernization Decision
    {
        "slug": "nova-s4hana-modernization-decision",
        "title": "S/4HANA Modernization & Simplification Architecture",
        "description": "Evaluate Nova Manufacturing's transition roadmap from legacy ECC to S/4HANA. Analyze deprecated tables, evaluate compatibility view impacts, and formulate the target data architecture.",
        "mission_type": SAPMissionType.CONFIGURATION.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [9, 10, 22],
        "concept_slugs": [
            "s4hana-value-drivers",
            "ecc-simplification-items",
            "compatibility-views-concept",
            "real-time-enterprise"
        ],
        "prerequisite_concepts": ["erp-foundations-synthesis"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "Nova Manufacturing is modernizing its Heidelberg assembly facility. You must advise the steering committee on table simplifications, compatibility views, and in-memory benefits."
        },
        "initial_state_patch": {},
        "target_state_criteria": {
            "modernization_blueprint": "S4HANA_SIMPLIFICATION_APPROVED",
            "table_simplification_validated": True
        },
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Remember that in S/4HANA, GLT0 and BSIS are replaced by the Universal Journal table ACDOCA.",
                    "Compatibility views provide read-redirection for SELECT queries, but direct SQL writes to deprecated tables will fail.",
                    "Real-time MRP Live runs directly on the database engine, eliminating overnight batch windows."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": [
                    "Evaluate custom code write operations versus read operations against deprecated tables."
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
                "step_id": "step_1_eval_aggregates",
                "title": "Audit Legacy Financial Aggregate Tables",
                "step_type": "decision",
                "instruction": "Nova Manufacturing's finance team asks why their custom report querying GLT0 (G/L Account Balances) will not need manual batch reconciliation after S/4HANA migration. Select the architectural explanation.",
                "options": [
                    {"id": "opt_a", "label": "GLT0 is retained as a physical database shadow table populated by asynchronous triggers.", "is_correct": False},
                    {"id": "opt_b", "label": "GLT0 is eliminated; balances are dynamically aggregated in RAM from ACDOCA line items in microseconds with zero batch delay.", "is_correct": True},
                    {"id": "opt_c", "label": "GLT0 is exported to an external sidecar database via nightly batch extraction.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_2_compat_view_guard",
                "step_type": "decision",
                "instruction": "A legacy interface job attempts to execute INSERT INTO bsik (Vendor Open Items). How should the development team remediate this code under S/4HANA simplification rules?",
                "options": [
                    {"id": "opt_a", "label": "Refactor the interface to post through standard financial accounting APIs (such as BAPI_ACC_DOCUMENT_POST) writing atomically to ACDOCA.", "is_correct": True},
                    {"id": "opt_b", "label": "Leave the SQL unchanged because Compatibility Views allow writing to legacy tables.", "is_correct": False},
                    {"id": "opt_c", "label": "Configure database triggers on BSIK to divert incoming rows into BSEG.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_3_mrp_live_decision",
                "step_type": "decision",
                "instruction": "The plant manager wants to know when production planning for optical sensors (RAW-01) should run. Formulate the operational strategy.",
                "options": [
                    {"id": "opt_a", "label": "Schedule classical MRP (MD01) to run as an overnight batch job to prevent database locks.", "is_correct": False},
                    {"id": "opt_b", "label": "Export bill of materials requirements to an external planning spreadsheet weekly.", "is_correct": False},
                    {"id": "opt_c", "label": "Execute MRP Live (MD01N) interactively during normal shift operations; in-memory pushdown computes material shortages in seconds without locking tables.", "is_correct": True}
                ]
            }
        ]
    },

    # 2. Universal Journal Investigation
    {
        "slug": "nova-universal-journal-investigation",
        "title": "Universal Journal & Multi-Ledger Discrepancy Investigation",
        "description": "Investigate financial balance discrepancies across parallel ledgers in table ACDOCA. Audit multi-dimension postings, verify multi-currency storage, and validate FI-CO unification.",
        "mission_type": SAPMissionType.INCIDENT.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [12],
        "concept_slugs": [
            "universal-journal-concept",
            "fi-co-unification",
            "acdoca-table-architecture",
            "parallel-ledgers"
        ],
        "prerequisite_concepts": ["module-interconnectivity", "columnar-database-engine"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01 (Heidelberg, EUR)",
            "scenario": "The European controller flagged a reporting difference between Leading Ledger 0L (IFRS) and Local Ledger 2L (German HGB) on fixed asset depreciation. Audit table ACDOCA to diagnose the variance."
        },
        "initial_state_patch": {},
        "target_state_criteria": {
            "universal_journal_audit": "PARALLEL_LEDGERS_RECONCILED",
            "acdoca_status": "MULTI_GAAP_BALANCED"
        },
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Remember that ACDOCA stores Ledger in field RLDNR (0L = Leading, 2L = Non-Leading).",
                    "Parallel accounting allows different depreciation methods (e.g. straight line vs accelerated) without creating reconciliation errors.",
                    "Secondary cost elements are now maintained directly as G/L accounts in ACDOCA."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": [
                    "Check the depreciation calculation rules per accounting principle."
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
                "step_id": "step_1_inspect_ledger_variance",
                "title": "Inspect Multi-Ledger Postings in ACDOCA",
                "step_type": "troubleshoot",
                "instruction": "Auditors find €1,000 depreciation posted to Ledger 0L and €1,500 posted to Ledger 2L for the same robotic stamping cell. What does this variance represent?",
                "options": [
                    {"id": "opt_a", "label": "Valid multi-GAAP parallel accounting: 0L follows IFRS 10-year depreciation, while 2L applies German statutory tax depreciation rules.", "is_correct": True},
                    {"id": "opt_b", "label": "A data corruption issue caused by incomplete ledger table replication.", "is_correct": False},
                    {"id": "opt_c", "label": "An unauthorized manual journal voucher adjustment in transaction FB01.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_2_verify_co_object",
                "step_type": "troubleshoot",
                "instruction": "The cost center manager asks whether internal management reporting requires running transaction KALC (FI-CO Reconciliation Ledger). What is the technical answer?",
                "options": [
                    {"id": "opt_a", "label": "KALC must be scheduled as an end-of-month batch job to sync secondary cost elements.", "is_correct": False},
                    {"id": "opt_b", "label": "Controlling postings must be reconciled through custom ABAP report extraction.", "is_correct": False},
                    {"id": "opt_c", "label": "KALC is obsolete. The depreciation posting in ACDOCA simultaneously updated Cost Center CC-1100 and G/L account in one atomic line item.", "is_correct": True}
                ]
            },
            {
                "step_id": "step_3_multi_currency_audit",
                "step_type": "troubleshoot",
                "instruction": "The transatlantic controller in Austin (PL02) wants to view this exact transaction in USD. How does ACDOCA handle the currency conversion?",
                "options": [
                    {"id": "opt_a", "label": "Amounts must be converted on-the-fly using external currency exchange web services.", "is_correct": False},
                    {"id": "opt_b", "label": "ACDOCA natively stores Document Currency (EUR), Local Currency (EUR), and Group Currency (USD) simultaneously on the line item.", "is_correct": True},
                    {"id": "opt_c", "label": "Group currency amounts are only calculated during annual balance sheet closing.", "is_correct": False}
                ]
            }
        ]
    },

    # 3. MATDOC Inventory Incident
    {
        "slug": "nova-matdoc-inventory-incident",
        "title": "MATDOC High-Throughput Inventory Bottleneck Incident",
        "description": "Troubleshoot concurrent goods movements and lock contention in warehouse operations. Transition legacy batch update logic to single-table MATDOC insert-only architecture.",
        "mission_type": SAPMissionType.INCIDENT.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [13],
        "concept_slugs": [
            "matdoc-table-architecture",
            "simplified-inventory-valuation"
        ],
        "prerequisite_concepts": ["acdoca-table-architecture"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "plant": "PL01 (Heidelberg) & PL02 (Austin)"
        },
        "initial_state_patch": {},
        "target_state_criteria": {
            "inventory_engine": "MATDOC_HIGH_THROUGHPUT_ACTIVE",
            "lock_contention_status": "ZERO_LOCKS"
        },
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "MATDOC replaces tables MKPF and MSEG for movement documents; master tables MARC and MBEW remain active master data with simplified dynamic aggregation.",
                    "HANA uses an insert-only ledger design to avoid row-level locks on material master records.",
                    "Current stock balances are aggregated dynamically from MATDOC in real-time."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": [
                    "Examine why concurrent transactions in legacy ECC caused table lock delays."
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
                "step_id": "step_1_diagnose_lock_bottleneck",
                "title": "Diagnose Warehouse Goods Receipt Freezes",
                "step_type": "troubleshoot",
                "instruction": "A legacy custom batch interface is attempting to update MARC stock totals directly, causing lock contention during high-speed inbound scanning. Identify the architectural fix.",
                "options": [
                    {"id": "opt_a", "label": "Increase the enqueue work process count in transaction RZ10 to absorb parallel update locks.", "is_correct": False},
                    {"id": "opt_b", "label": "Decommission the custom MARC update routine; post goods movements via standard BAPI into MATDOC, allowing HANA to aggregate stock dynamically.", "is_correct": True},
                    {"id": "opt_c", "label": "Serialize all goods movements through a single background batch queue.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_2_verify_matdoc_record",
                "step_type": "troubleshoot",
                "instruction": "Verify the resulting database commitment when Goods Receipt (Movement Type 101) for 500 units of RAW-01 is posted.",
                "options": [
                    {"id": "opt_a", "label": "A single atomic record is appended into MATDOC, synchronously creating an inventory valuation line in ACDOCA.", "is_correct": True},
                    {"id": "opt_b", "label": "Separate physical records are written to MKPF, MSEG, and MARC during an overnight update window.", "is_correct": False},
                    {"id": "opt_c", "label": "Inventory quantity is updated in memory only, without persistence to disk.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_3_validate_valuation",
                "step_type": "troubleshoot",
                "instruction": "How does S/4HANA ensure that stock valuation remains consistent during simultaneous goods issue and goods receipt transactions?",
                "options": [
                    {"id": "opt_a", "label": "By locking the entire plant inventory table during transaction execution.", "is_correct": False},
                    {"id": "opt_b", "label": "By postponing financial postings until physical inventory reconciliation at month-end.", "is_correct": False},
                    {"id": "opt_c", "label": "MATDOC maintains atomic inventory valuation records with microsecond timestamps, preventing balance drift without table locks.", "is_correct": True}
                ]
            }
        ]
    },

    # 4. Business Partner Migration
    {
        "slug": "nova-business-partner-migration",
        "title": "Central Business Partner & CVI Synchronization Project",
        "description": "Configure the central Business Partner entity for key partner Rheinland Precision Optics. Map FI Vendor, Purchasing Supplier, and Customer roles, and execute CVI synchronization.",
        "mission_type": SAPMissionType.CONFIGURATION.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [14],
        "concept_slugs": [
            "business-partner-cvi",
            "customer-vendor-synchronization"
        ],
        "prerequisite_concepts": ["master-data-concept"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "partner": "BP-101 (Rheinland Precision Optics)"
        },
        "initial_state_patch": {},
        "target_state_criteria": {
            "partner_cvi_status": "SYNCHRONIZED_ALL_ROLES"
        },
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Transaction BP is the mandatory single point of entry for all partner master data.",
                    "Purchasing requires role FLVN01 while invoice posting requires FLVN00. Customer sales require FLCU00/FLCU01.",
                    "Customer-Vendor Integration (CVI) synchronizes BUT000 real-time with legacy tables LFA1 and KNA1 upon save."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": [
                    "Ensure both supplier and customer role views are maintained for dual-relationship partners."
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
                "step_id": "step_1_create_central_bp",
                "title": "Establish Central Business Partner Identity",
                "step_type": "config",
                "instruction": "Rheinland Precision Optics operates both as a supplier of laser sensors and a buyer of CNC fixtures. How must their record be established in S/4HANA?",
                "options": [
                    {"id": "opt_a", "label": "Create two completely unrelated accounts in legacy transactions XK01 and XD01.", "is_correct": False},
                    {"id": "opt_b", "label": "Create a single central Business Partner (BP-101) in table BUT000 containing common legal, address, and tax information.", "is_correct": True},
                    {"id": "opt_c", "label": "Create an anonymous temporary guest vendor account in Financial Accounting.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_2_assign_supplier_roles",
                "step_type": "config",
                "instruction": "Nova Manufacturing needs to issue Purchase Orders, post incoming invoices, and sell finished fixtures to BP-101. Which roles must be assigned?",
                "options": [
                    {"id": "opt_a", "label": "Only role 000000 (General BP) with no organizational or company code assignments.", "is_correct": False},
                    {"id": "opt_b", "label": "Role BUP003 (Employee) with internal payroll banking details.", "is_correct": False},
                    {"id": "opt_c", "label": "Supplier roles FLVN00 (FI Vendor) and FLVN01 (Purchasing), plus Customer roles FLCU00 (FI Customer) and FLCU01 (Sales).", "is_correct": True}
                ]
            },
            {
                "step_id": "step_3_execute_cvi_sync",
                "step_type": "config",
                "instruction": "Verify Customer-Vendor Integration (CVI) synchronization so legacy reporting queries and operational transactions can access the partner.",
                "options": [
                    {"id": "opt_a", "label": "CVI links BUT000 synchronously to active tables LFA1/LFB1 and KNA1/KNB1 upon save, ensuring full compatibility.", "is_correct": True},
                    {"id": "opt_b", "label": "CVI converts all partner data into flat XML files stored in the application server directory.", "is_correct": False},
                    {"id": "opt_c", "label": "CVI drops legacy tables LFA1 and KNA1 from the database schema entirely.", "is_correct": False}
                ]
            }
        ]
    },

    # 5. CDS Reporting Requirement
    {
        "slug": "nova-cds-reporting-requirement",
        "title": "Operational Real-Time Reporting via ABAP CDS",
        "description": "Design and validate an operational reporting model using Core Data Services for Nova Manufacturing. Push calculations down to HANA and expose them via SAP Fiori.",
        "mission_type": SAPMissionType.PROCESS_TASK.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [15, 19],
        "concept_slugs": [
            "cds-fundamentals",
            "code-pushdown-philosophy",
            "embedded-analytics-foundations"
        ],
        "prerequisite_concepts": ["columnar-database-engine", "acdoca-table-architecture"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "plant": "PL01 (Heidelberg Assembly)"
        },
        "initial_state_patch": {},
        "target_state_criteria": {
            "cds_reporting_status": "CDS_VIEW_ENTITY_DEPLOYED"
        },
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "CDS View Entities push calculations down into the HANA in-memory database.",
                    "Associations provide on-demand lazy loading compared to eager SQL joins.",
                    "Modern RAP exposure uses Service Definitions and Service Bindings (OData V4 - UI)."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": [
                    "Compare application server looping vs database aggregation."
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
                "step_id": "step_1_choose_paradigm",
                "title": "Select the Data Access Architecture",
                "step_type": "decision",
                "instruction": "Plant operations requires a real-time monitor showing component scrap rates for robotics controller DXTR-1000 across 3,000,000 MATDOC rows. Choose the architectural paradigm.",
                "options": [
                    {"id": "opt_a", "label": "Write a legacy ABAP program that SELECTs 3,000,000 rows into internal tables and loops over them.", "is_correct": False},
                    {"id": "opt_b", "label": "Define a CDS View Entity with in-memory code pushdown (SUM, CASE) and partition filtering executing directly in HANA RAM.", "is_correct": True},
                    {"id": "opt_c", "label": "Extract the data into Microsoft Excel once a week via background batch job.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_2_structure_vdm",
                "step_type": "config",
                "instruction": "Structure the Virtual Data Model (VDM) according to SAP Best Practices.",
                "options": [
                    {"id": "opt_a", "label": "Create a Basic Interface View (I_MaterialBasic) on master data, a Composite Cube View (I_ProductionStockCube), and a Consumption View (C_NovaStockKPI).", "is_correct": True},
                    {"id": "opt_b", "label": "Create one single view that joins 85 unrelated database tables directly without associations.", "is_correct": False},
                    {"id": "opt_c", "label": "Bypass CDS entirely and query the database from client browser JavaScript directly.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_3_publish_fiori",
                "step_type": "config",
                "instruction": "Expose the consumption view to the plant manager's mobile SAP Fiori Launchpad.",
                "options": [
                    {"id": "opt_a", "label": "Export the CDS view metadata to a CSV file and upload to the SAP Fiori theme designer.", "is_correct": False},
                    {"id": "opt_b", "label": "Write a classical RFC function module that wraps the CDS view for SOAP web service integration.", "is_correct": False},
                    {"id": "opt_c", "label": "Define a RAP Business Service Definition and activate an OData V4 - UI Service Binding consumed by Fiori Elements.", "is_correct": True}
                ]
            }
        ]
    },

    # 6. Landscape Change Request
    {
        "slug": "nova-landscape-change-request",
        "title": "Landscape Release Management & Transport Governance",
        "description": "Formulate transport routes and enforce change management governance across DEV, QAS, and PRD systems for Nova Manufacturing's Austin plant expansion.",
        "mission_type": SAPMissionType.CONFIGURATION.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [16, 17],
        "concept_slugs": [
            "transport-management-cts",
            "system-landscapes-3tier"
        ],
        "prerequisite_concepts": ["three-tier-architecture"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "route": "DEV -> QAS -> PRD"
        },
        "initial_state_patch": {},
        "target_state_criteria": {
            "transport_governance_status": "CLEAN_CORE_DEPLOYED"
        },
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Direct changes in PRD are strictly disabled (SCC4 set to No Changes Allowed).",
                    "Customizing requests are client-dependent; Workbench requests apply system-wide.",
                    "Transport overtaking occurs when dependent transports are imported out of sequence."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": [
                    "Trace the change from DEV development through QAS testing before touching PRD."
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
                "step_id": "step_1_create_transport",
                "title": "Package Configuration in DEV Client 100",
                "step_type": "config",
                "instruction": "Configure Storage Location FG02 for Austin Plant PL02. Into which container must this change be saved?",
                "options": [
                    {"id": "opt_a", "label": "A Customizing Transport Request (e.g. DEVK900142) in DEV Client 100.", "is_correct": True},
                    {"id": "opt_b", "label": "Directly into Production Client 300 using emergency SAP_ALL privileges.", "is_correct": False},
                    {"id": "opt_c", "label": "A Workbench request that applies to all clients across the landscape simultaneously.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_2_verify_qas_uat",
                "step_type": "troubleshoot",
                "instruction": "Import the transport request into QAS Client 200 via STMS. What verification must be completed before PRD approval?",
                "options": [
                    {"id": "opt_a", "label": "Deploy directly to PRD without testing since unit tests were already executed in DEV 120.", "is_correct": False},
                    {"id": "opt_b", "label": "Perform a client copy of PRD over QAS to verify that test data matches live operations.", "is_correct": False},
                    {"id": "opt_c", "label": "Execute end-to-end user acceptance testing (UAT) in Plant PL02 and obtain formal business sign-off.", "is_correct": True}
                ]
            },
            {
                "step_id": "step_3_production_cutover",
                "step_type": "config",
                "instruction": "Deploy the verified change into Production (PRD Client 300). How is transport sequence integrity preserved?",
                "options": [
                    {"id": "opt_a", "label": "Import transports in reverse chronological order so the newest changes arrive first.", "is_correct": False},
                    {"id": "opt_b", "label": "Enforce strict transport queue ordering to ensure prerequisite configuration transports import before dependent CDS views (preventing overtaking).", "is_correct": True},
                    {"id": "opt_c", "label": "Import all pending transports in parallel using multi-threaded batch triggers.", "is_correct": False}
                ]
            }
        ]
    },

    # 7. Access Governance Incident
    {
        "slug": "nova-access-governance-incident",
        "title": "Fiori Access Governance & Segregation of Duties Audit",
        "description": "Audit user permissions, detect toxic authorization combinations, and resolve critical Segregation of Duties (SoD) violations on the Fiori Launchpad.",
        "mission_type": SAPMissionType.INCIDENT.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [18],
        "concept_slugs": [
            "identity-access-management",
            "pfcg-authorizations",
            "fiori-role-assignment"
        ],
        "prerequisite_concepts": ["fiori-launchpad-overview"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "user": "ANNA.MULLER (Plant PL01)"
        },
        "initial_state_patch": {},
        "target_state_criteria": {
            "sod_audit_status": "SOD_CLEARED_DUAL_CONTROL"
        },
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Business Roles in PFCG assign Business Catalogs, Spaces, and Pages.",
                    "Holding both PO creation and vendor payment release violates Segregation of Duties (SoD).",
                    "Remediate by reassigning the user to a restricted role without payment disbursement authorization."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": [
                    "Identify the conflicting business catalog and restore dual control."
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
                "step_id": "step_1_audit_user_roles",
                "title": "Identify Toxic Role Combinations",
                "step_type": "troubleshoot",
                "instruction": "Audit user ANNA.MULLER's profile. Why did external compliance auditors flag a high-risk Segregation of Duties (SoD) violation?",
                "options": [
                    {"id": "opt_a", "label": "She has been assigned authorization to view sales orders across both plant PL01 and PL02.", "is_correct": False},
                    {"id": "opt_b", "label": "Her user password has not been rotated within the standard 90-day window.", "is_correct": False},
                    {"id": "opt_c", "label": "She possesses both SAP_BR_PURCHASER (Create Purchase Orders) and SAP_BR_AP_ACCOUNTANT (Release Vendor Payments), enabling potential unauthorized disbursements.", "is_correct": True}
                ]
            },
            {
                "step_id": "step_2_remediate_catalogs",
                "title": "Remediate Segregation of Duties Violation",
                "step_type": "config",
                "instruction": "Formulate the correct access governance remediation to clear the audit finding while preserving Anna's logistics responsibilities.",
                "options": [
                    {"id": "opt_a", "label": "Grant Anna full administrative authorization (SAP_ALL) to override the compliance exception.", "is_correct": False},
                    {"id": "opt_b", "label": "Revoke role SAP_BR_AP_ACCOUNTANT and assign restricted role SAP_BR_AP_CLERK_INVOICES (retaining invoice verification but removing payment authorization F_REGU_BUK).", "is_correct": True},
                    {"id": "opt_c", "label": "Modify standard role template SAP_BR_AP_ACCOUNTANT in transaction PFCG directly in Production PRD.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_3_verify_fiori_launchpad",
                "title": "Verify Fiori Launchpad Dual Control",
                "step_type": "config",
                "instruction": "Verify Anna's Fiori Launchpad layout after remediation.",
                "options": [
                    {"id": "opt_a", "label": "The Purchasing Space remains active with Manage Purchase Orders, while the Payment Release tile is removed, restoring dual control.", "is_correct": True},
                    {"id": "opt_b", "label": "All Launchpad tiles are hidden until Anna completes annual compliance training.", "is_correct": False},
                    {"id": "opt_c", "label": "The user is forced to log into classical SAP GUI for all subsequent transactions.", "is_correct": False}
                ]
            }
        ]
    },

    # 8. Cross-Module Document Trace
    {
        "slug": "nova-cross-module-document-trace",
        "title": "Cross-Module Document Lineage & Financial Audit Trace",
        "description": "Follow a live business event across logistics, inventory, and finance. Audit document flow table VBFA, verify MATDOC goods issue, and validate ACDOCA journal postings.",
        "mission_type": SAPMissionType.PROCESS_TASK.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [20, 21],
        "concept_slugs": [
            "document-flow-continuity",
            "transactional-audit-trail",
            "s4hana-integrated-scenario"
        ],
        "prerequisite_concepts": ["acdoca-table-architecture", "matdoc-table-architecture"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "order": "Order #10042 (Customer CUST-501)"
        },
        "initial_state_patch": {},
        "target_state_criteria": {
            "audit_trail_status": "ORDER_10042_FULLY_TRACED_AND_CLEARED"
        },
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Table VBFA stores predecessor and successor relationships for sales orders.",
                    "Post Goods Issue (PGI) appends to MATDOC and recognizes COGS in ACDOCA with reference key AWTYP = 'MKPF'.",
                    "Billing release writes customer receivable, revenue, and tax into ACDOCA with reference key AWTYP = 'VBRK'."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": [
                    "Trace the document chain chronologically from Order to Payment."
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
                "step_id": "step_1_trace_vbfa_lineage",
                "title": "Audit Document Relationships in Table VBFA",
                "step_type": "troubleshoot",
                "instruction": "Audit customer order #10042 in table VBFA. Verify the chronological lineage connecting the commercial order to physical warehouse delivery.",
                "options": [
                    {"id": "opt_a", "label": "Sales orders and deliveries do not maintain relationships in S/4HANA; only billing documents are stored.", "is_correct": False},
                    {"id": "opt_b", "label": "Sales Order #10042 (Predecessor VBELV) links directly to Outbound Delivery #80019 (Successor VBELN) with Category 'J'.", "is_correct": True},
                    {"id": "opt_c", "label": "Table VBFA records only financial journal numbers and ignores SD documents.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_2_verify_pgi_and_cogs",
                "title": "Verify Goods Issue and Synchronous ACDOCA Commitment",
                "step_type": "troubleshoot",
                "instruction": "Inspect the dual commitments generated when warehouse operators posted Goods Issue (#490001) for the 30 robotics controllers.",
                "options": [
                    {"id": "opt_a", "label": "MATDOC reduced inventory by 30 units, while ACDOCA synchronously posted Dr COGS Expense €25,500 and Cr Inventory Asset €25,500 with AWTYP = 'MKPF'.", "is_correct": True},
                    {"id": "opt_b", "label": "Inventory was reduced in MATDOC, but financial accounting entries are deferred until month-end batch execution.", "is_correct": False},
                    {"id": "opt_c", "label": "Financial entries were posted to legacy table BSIS with zero updates to table ACDOCA.", "is_correct": False}
                ]
            },
            {
                "step_id": "step_3_validate_financial_clearing",
                "title": "Validate Commercial Billing and Bank Clearing",
                "step_type": "troubleshoot",
                "instruction": "Verify billing document #900055 and subsequent incoming bank payment #100021 in ACDOCA.",
                "options": [
                    {"id": "opt_a", "label": "Billing documents do not create accounting documents unless manual posting program SAPF048 is run.", "is_correct": False},
                    {"id": "opt_b", "label": "Incoming bank payments are posted exclusively to the Controlling ledger without affecting ACDOCA.", "is_correct": False},
                    {"id": "opt_c", "label": "Billing posted Dr Customer AR €49,980 (Gross) and Cr Revenue with AWTYP = 'VBRK'; subsequent bank payment cleared the open item with zero residual balance.", "is_correct": True}
                ]
            }
        ]
    }
]
