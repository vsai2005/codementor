"""Authoritative objective questions and answer keys for SAP placement diagnostic.

Provides two distinct assessment tracks:
1. 'experienced': 10 in-depth architectural and technical questions spanning
   ERP architecture, S/4HANA tables (ACDOCA/MATDOC), CVI, P2P/O2C, CDS/VDM, and RAP.
2. 'not_sure': 6 foundational conceptual questions verifying basic enterprise
   intuitions and computing principles.
"""

from __future__ import annotations
from typing import Any

EXPERIENCED_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "exp_arch_01",
        "topic": "enterprise_architecture",
        "topic_label": "Enterprise Architecture",
        "concept_slug": "three-tier-architecture",
        "question": "In SAP NetWeaver / S/4HANA application server architecture, which statement accurately differentiates the role of Dialog (DIA) and Update (UPD) work processes?",
        "options": [
            {
                "id": "a",
                "text": "DIA work processes execute long-running background jobs, while UPD processes handle interactive user screen requests."
            },
            {
                "id": "b",
                "text": "DIA work processes handle interactive user interaction under time-slicing rules, while asynchronous database writes (V1/V2) are offloaded to UPD work processes."
            },
            {
                "id": "c",
                "text": "UPD work processes are located exclusively on the database host and communicate directly with the storage layer without application server coordination."
            },
            {
                "id": "d",
                "text": "DIA work processes commit transactional data synchronously to disk, rendering UPD processes obsolete in modern systems."
            }
        ],
        "correct_option": "b",
        "difficulty": 2,
    },
    {
        "id": "exp_org_02",
        "topic": "org_structure",
        "topic_label": "Organizational Structures",
        "concept_slug": "org-structure-company-code",
        "question": "When configuring enterprise organizational structures in SAP, what is the highest organizational unit for which a complete, self-contained set of financial accounts (Balance Sheet and P&L) can be drawn?",
        "options": [
            {
                "id": "a",
                "text": "Plant (Werks)"
            },
            {
                "id": "b",
                "text": "Controlling Area (KOKRS)"
            },
            {
                "id": "c",
                "text": "Company Code (Bukrs)"
            },
            {
                "id": "d",
                "text": "Sales Organization (VKORG)"
            }
        ],
        "correct_option": "c",
        "difficulty": 2,
    },
    {
        "id": "exp_acdoca_03",
        "topic": "s4hana_inmemory",
        "topic_label": "S/4HANA Data Architecture",
        "concept_slug": "acdoca-table-architecture",
        "question": "How does the S/4HANA Universal Journal (table ACDOCA) unify financial accounting and controlling compared to legacy SAP ECC 6.0?",
        "options": [
            {
                "id": "a",
                "text": "ACDOCA completely replaces all sales order and purchase order operational tables (VBAK, EKKO) with a single document table."
            },
            {
                "id": "b",
                "text": "ACDOCA unifies General Ledger (FI-GL), Asset Accounting (FI-AA), and Controlling (CO) line items into a single non-aggregated line-item table, while legacy total and index tables are replaced by compatibility views."
            },
            {
                "id": "c",
                "text": "ACDOCA stores pre-calculated totals and period-end aggregate summaries while raw line items continue to reside in BSEG only."
            },
            {
                "id": "d",
                "text": "ACDOCA operates strictly in the application server cache and flushes line items back to BSIS, BSAS, and GLT0 upon nightly batch cycles."
            }
        ],
        "correct_option": "b",
        "difficulty": 3,
    },
    {
        "id": "exp_matdoc_04",
        "topic": "s4hana_inmemory",
        "topic_label": "S/4HANA Data Architecture",
        "concept_slug": "matdoc-table-architecture",
        "question": "In S/4HANA Inventory Management simplification, which statement accurately describes table MATDOC?",
        "options": [
            {
                "id": "a",
                "text": "MATDOC records all inventory movements as discrete line items, eliminating the need for classic hybrid inventory tables (such as MKPF and MSEG) and removing historical table locks on stock tables."
            },
            {
                "id": "b",
                "text": "MATDOC completely deletes the Material Master tables (MARA, MARC, MARD) and replaces them with an unstructured JSON store."
            },
            {
                "id": "c",
                "text": "MATDOC is an optional reporting view built on top of MKPF and MSEG that requires manual batch reconciliation."
            },
            {
                "id": "d",
                "text": "MATDOC only stores physical inventory counts, while standard goods movements still write exclusively to MSEG."
            }
        ],
        "correct_option": "a",
        "difficulty": 3,
    },
    {
        "id": "exp_cvi_05",
        "topic": "master_data",
        "topic_label": "Master Data & CVI",
        "concept_slug": "business-partner-cvi",
        "question": "In S/4HANA Customer-Vendor Integration (CVI), what is the architectural relationship between the central Business Partner (BUT000) and legacy Customer/Supplier tables (KNA1/LFA1)?",
        "options": [
            {
                "id": "a",
                "text": "KNA1 and LFA1 are entirely deleted from the database schema; applications only ever query BUT000."
            },
            {
                "id": "b",
                "text": "Business Partner (BUT000) is the mandatory leading master data object; CVI synchronization components maintain subledger projection tables KNA1 and LFA1 automatically."
            },
            {
                "id": "c",
                "text": "Users maintain KNA1 and LFA1 directly in SAP GUI, which then triggers a background batch job to create a Business Partner."
            },
            {
                "id": "d",
                "text": "Business Partner is only used in S/4HANA Cloud Public Edition; On-Premise S/4HANA still uses traditional customer/vendor transactions (XD01/XK01)."
            }
        ],
        "correct_option": "b",
        "difficulty": 3,
    },
    {
        "id": "exp_proc_06",
        "topic": "business_processes",
        "topic_label": "End-to-End Business Processes",
        "concept_slug": "p2p-goods-receipt-migo",
        "question": "During a standard valuated Procure-to-Pay (P2P) Goods Receipt (transaction MIGO) against a Purchase Order, what double-entry general ledger posting occurs before invoice verification?",
        "options": [
            {
                "id": "a",
                "text": "Debit: Accounts Payable (Vendor) | Credit: Bank Clearing"
            },
            {
                "id": "b",
                "text": "Debit: Inventory Asset Account | Credit: GR/IR (Goods Receipt / Invoice Receipt) Clearing Account"
            },
            {
                "id": "c",
                "text": "Debit: Consumption Expense Account | Credit: Accounts Payable (Vendor)"
            },
            {
                "id": "d",
                "text": "No financial document or posting is generated until invoice receipt (MIRO) is completed."
            }
        ],
        "correct_option": "b",
        "difficulty": 3,
    },
    {
        "id": "exp_vdm_07",
        "topic": "cds_data_semantics",
        "topic_label": "CDS & VDM Architecture",
        "concept_slug": "vdm-architecture-tiers",
        "question": "In the SAP Virtual Data Model (VDM) architecture, what is the specific semantic role of a Basic (Interface) View?",
        "options": [
            {
                "id": "a",
                "text": "It serves as the user-facing analytical query consumed directly by Fiori Elements, containing UI annotations and parameters."
            },
            {
                "id": "b",
                "text": "It defines a core business entity directly on top of database tables (e.g., I_JournalEntry), providing clean data types and associations without enterprise business logic or UI annotations."
            },
            {
                "id": "c",
                "text": "It combines multiple basic views into a multidimensional cube with default aggregations."
            },
            {
                "id": "d",
                "text": "It is an internal temporary table generated during delta merge execution."
            }
        ],
        "correct_option": "b",
        "difficulty": 4,
    },
    {
        "id": "exp_assoc_08",
        "topic": "cds_data_semantics",
        "topic_label": "CDS & VDM Architecture",
        "concept_slug": "cds-associations-concept",
        "question": "What is the primary operational and performance distinction between a CDS Association and a traditional SQL JOIN in Core Data Services?",
        "options": [
            {
                "id": "a",
                "text": "Associations are executed exclusively in the ABAP application layer, whereas SQL JOINs execute in the database kernel."
            },
            {
                "id": "b",
                "text": "Associations define 'join-on-demand' relationships: the HANA database only executes the join if attributes from the associated entity are explicitly requested in the projection list or WHERE clause."
            },
            {
                "id": "c",
                "text": "Associations can only link tables within the same database schema, whereas SQL JOINs can cross remote BTP destinations."
            },
            {
                "id": "d",
                "text": "SQL JOINs require secondary indexes, whereas CDS Associations prohibit the use of indexes."
            }
        ],
        "correct_option": "b",
        "difficulty": 4,
    },
    {
        "id": "exp_rap_09",
        "topic": "abap_cloud_rap",
        "topic_label": "ABAP Cloud & RAP Architecture",
        "concept_slug": "abap-cloud-paradigm",
        "question": "Under the modern SAP Clean Core and ABAP Cloud paradigm, which rule governs database writes and custom transactional developments?",
        "options": [
            {
                "id": "a",
                "text": "Developers are encouraged to execute direct SQL statements (INSERT, UPDATE, DELETE) against standard SAP tables in custom function modules."
            },
            {
                "id": "b",
                "text": "Transactional writes must be encapsulated via RAP Behavior Definitions (BDEF) using Managed or Unmanaged implementations, consuming only Released APIs (C1 contract) and strictly avoiding direct modifications to standard SAP tables."
            },
            {
                "id": "c",
                "text": "ABAP Cloud eliminates custom database tables entirely, requiring all custom data to be stored on external AWS S3 buckets."
            },
            {
                "id": "d",
                "text": "BAPIs and classic IDocs are the mandatory transport layer for all new transactional entities."
            }
        ],
        "correct_option": "b",
        "difficulty": 4,
    },
    {
        "id": "exp_bdef_10",
        "topic": "abap_cloud_rap",
        "topic_label": "ABAP Cloud & RAP Architecture",
        "concept_slug": "rap-save-sequence",
        "question": "In the SAP RESTful Application Programming Model (RAP), what is the key functional difference between a Validation and a Determination?",
        "options": [
            {
                "id": "a",
                "text": "A Validation calculates and modifies field values, while a Determination issues error messages to the message pool."
            },
            {
                "id": "b",
                "text": "A Validation checks transactional consistency and reports messages without altering entity state; a Determination computes, defaults, or derives field values automatically in response to state triggers."
            },
            {
                "id": "c",
                "text": "A Determination executes only during batch jobs, while a Validation executes only on mobile Fiori clients."
            },
            {
                "id": "d",
                "text": "Validations are only supported in Unmanaged RAP scenarios, whereas Determinations are restricted to Managed RAP."
            }
        ],
        "correct_option": "b",
        "difficulty": 5,
    },
]

NOT_SURE_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "ns_fund_01",
        "topic": "enterprise_architecture",
        "topic_label": "Enterprise Fundamentals",
        "concept_slug": "erp-evolution",
        "question": "What is the primary business purpose of an Enterprise Resource Planning (ERP) system like SAP S/4HANA?",
        "options": [
            {
                "id": "a",
                "text": "To serve as an email server and personal calendar application for company staff."
            },
            {
                "id": "b",
                "text": "To integrate core business operations (purchasing, manufacturing, sales, finance) into a single unified data model and transactional system."
            },
            {
                "id": "c",
                "text": "To replace client operating systems with a proprietary Linux kernel."
            },
            {
                "id": "d",
                "text": "To function solely as a public marketing website for consumer visitors."
            }
        ],
        "correct_option": "b",
        "difficulty": 1,
    },
    {
        "id": "ns_org_02",
        "topic": "org_structure",
        "topic_label": "Organizational Units",
        "concept_slug": "org-structure-company-code",
        "question": "If an international enterprise has legal corporate entities registered in Germany and the United States, which SAP organizational unit represents each distinct legal entity?",
        "options": [
            {
                "id": "a",
                "text": "Storage Location"
            },
            {
                "id": "b",
                "text": "Company Code"
            },
            {
                "id": "c",
                "text": "Purchasing Group"
            },
            {
                "id": "d",
                "text": "Distribution Channel"
            }
        ],
        "correct_option": "b",
        "difficulty": 1,
    },
    {
        "id": "ns_data_03",
        "topic": "master_data",
        "topic_label": "Data Architecture",
        "concept_slug": "master-data-concept",
        "question": "Which of the following represents Master Data rather than Transactional Data in an enterprise system?",
        "options": [
            {
                "id": "a",
                "text": "A Customer Account Record containing registered business address, tax ID, and payment terms."
            },
            {
                "id": "b",
                "text": "A Sales Order document placed on Tuesday afternoon for 10 units."
            },
            {
                "id": "c",
                "text": "A Goods Receipt material document recorded when a truck arrives."
            },
            {
                "id": "d",
                "text": "An Outbound Delivery packing slip printed for a warehouse picker."
            }
        ],
        "correct_option": "a",
        "difficulty": 1,
    },
    {
        "id": "ns_p2p_04",
        "topic": "business_processes",
        "topic_label": "Procurement Flow",
        "concept_slug": "p2p-pr-creation",
        "question": "In a standard corporate procurement process, which document is created first by an internal department to request goods before a vendor is engaged?",
        "options": [
            {
                "id": "a",
                "text": "Billing Document / Invoice"
            },
            {
                "id": "b",
                "text": "Purchase Requisition (PR)"
            },
            {
                "id": "c",
                "text": "Goods Issue Slip"
            },
            {
                "id": "d",
                "text": "Vendor Payment Remittance"
            }
        ],
        "correct_option": "b",
        "difficulty": 1,
    },
    {
        "id": "ns_hana_05",
        "topic": "s4hana_inmemory",
        "topic_label": "S/4HANA Innovation",
        "concept_slug": "s4hana-value-drivers",
        "question": "What is the primary technological breakthrough of SAP HANA compared to traditional relational database systems?",
        "options": [
            {
                "id": "a",
                "text": "HANA keeps active operational data in high-speed RAM with columnar storage and dictionary encoding, enabling real-time analytics directly on live transactional tables without batch aggregate tables."
            },
            {
                "id": "b",
                "text": "HANA eliminates all database backups and operates entirely without hard drives."
            },
            {
                "id": "c",
                "text": "HANA removes SQL and requires programs to write binary machine instructions directly to CPU registers."
            },
            {
                "id": "d",
                "text": "HANA can only store up to 10,000 records total."
            }
        ],
        "correct_option": "a",
        "difficulty": 2,
    },
    {
        "id": "ns_fiori_06",
        "topic": "enterprise_ux",
        "topic_label": "Modern User Experience",
        "concept_slug": "sap-gui-navigation",
        "question": "What is the role of SAP Fiori in modern S/4HANA systems?",
        "options": [
            {
                "id": "a",
                "text": "It is an internal database compression engine."
            },
            {
                "id": "b",
                "text": "It provides a responsive, web-based, role-driven user experience (UX) based on modern design guidelines, replacing the need for classic transaction codes (T-codes) for business users."
            },
            {
                "id": "c",
                "text": "It is an automated email marketing plugin."
            },
            {
                "id": "d",
                "text": "It is an on-premise hardware server rack."
            }
        ],
        "correct_option": "b",
        "difficulty": 1,
    },
]


def get_public_questions_for_track(track: str) -> list[dict[str, Any]]:
    """Returns question metadata and options without revealing correct answers."""
    source = EXPERIENCED_QUESTIONS if track == "experienced" else NOT_SURE_QUESTIONS
    sanitized: list[dict[str, Any]] = []
    for q in source:
        sanitized.append({
            "id": q["id"],
            "topic": q["topic"],
            "topic_label": q["topic_label"],
            "concept_slug": q["concept_slug"],
            "question": q["question"],
            "options": q["options"],
            "difficulty": q.get("difficulty", 1),
        })
    return sanitized


def evaluate_assessment_answers(
    track: str,
    answers: dict[str, str],
) -> tuple[float, dict[str, float], list[str], list[str]]:
    """Grading function evaluated strictly against authoritative secret answer keys.

    Returns:
    - overall_score: 0.0 to 100.0
    - domain_scores: dict mapping topic slug to percentage
    - demonstrated_concepts: list of concept slugs answered correctly
    - gap_concepts: list of concept slugs answered incorrectly or missed
    """
    questions = EXPERIENCED_QUESTIONS if track == "experienced" else NOT_SURE_QUESTIONS
    if not questions:
        return 0.0, {}, [], []

    topic_totals: dict[str, int] = {}
    topic_correct: dict[str, int] = {}
    demonstrated: list[str] = []
    gaps: list[str] = []

    total_correct = 0
    for q in questions:
        q_id = q["id"]
        topic = q["topic"]
        concept = q["concept_slug"]
        correct_opt = q["correct_option"]

        topic_totals[topic] = topic_totals.get(topic, 0) + 1
        user_choice = answers.get(q_id, "").strip().lower()

        if user_choice and user_choice == correct_opt.lower():
            total_correct += 1
            topic_correct[topic] = topic_correct.get(topic, 0) + 1
            if concept not in demonstrated:
                demonstrated.append(concept)
        else:
            if concept not in gaps:
                gaps.append(concept)

    overall_score = round((total_correct / len(questions)) * 100.0, 1)

    domain_scores: dict[str, float] = {}
    for topic, count in topic_totals.items():
        corr = topic_correct.get(topic, 0)
        domain_scores[topic] = round((corr / count) * 100.0, 1)

    return overall_score, domain_scores, demonstrated, gaps
