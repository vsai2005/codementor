"""Authoritative content definitions for SAP S/4HANA Guided Learning Days 9–22 (Phase 2).

S/4HANA Technical Accuracy & Architectural Invariants (Audited):
1. Universal Journal Scope: ACDOCA combines GL (BKPF/BSEG), CO (COEP), AA (ANEP), and ML (MLIT)
   into an atomic multi-dimension record. Operational documents (VBAK, EKKO) and document headers (BKPF) remain active.
2. Inventory Ledger: MATDOC records material movement line items in append-only columnar format.
   Master and valuation tables (MARC, MARD, MBEW) are preserved via generated CDS compatibility views (NSDM_V_*).
3. Central Business Partner: BUT000 is the mandatory single point of entry. Synchronization writes into
   traditional projection tables (KNA1, LFA1, KNVV, LFM1) via Customer-Vendor Integration (CVI / MDS_LOAD_COCKPIT).
4. Modern CDS Standards: Standardizes on DEFINE VIEW ENTITY (2020+). Deprecated @OData.publish: true is removed
   in favor of RAP Business Service Definitions and Service Bindings (OData V4 - UI).
5. Landscape Architecture: Central Business Configuration (CBC) is restricted to Public Cloud 3SL.
   Private Cloud and On-Premise use standard SPRO customizing with CTS/STMS transport pipelines.
6. Identity & Access Governance: Resolves SoD conflicts by reassigning to restricted roles (SAP_BR_AP_CLERK_INVOICES)
   without modifying delivered SAP template catalogs or granting direct payment release (F_REGU_BUK).

Strict 8-step pedagogical sequence for every day:
1. learn: Core concepts, definitions, and business rationale.
2. understand: Deep-dive architecture, invariants, and anti-patterns.
3. visual_example: Concrete implementation inside Nova Manufacturing Corp (NM01).
4. interactive_practice: Specification for reusable UI practice components.
5. challenge: Real-world enterprise scenario decision.
6. assessment: Multi-question concept test mapped directly to DAG concepts.
7. mastery_evidence: Explicit concept scoring and skill evidence metadata.
8. completion: Key takeaways, review, and companion Enterprise Mission links.
"""

from __future__ import annotations
from typing import Any

PHASE_2_DAYS_CONTENT: dict[int, dict[str, Any]] = {
    # =========================================================================
    # DAY 9: S/4HANA Core Value Drivers
    # =========================================================================
    9: {
        "day_number": 9,
        "slug": "s4hana-value-drivers",
        "title": "S/4HANA Value Drivers & Business Case",
        "subtitle": "Real-time enterprise execution, simplification, and total cost of ownership",
        "estimated_minutes": 45,
        "atomic_concepts": ["s4hana-value-drivers", "real-time-enterprise"],
        "recommended_mission_slug": "nova-s4hana-modernization-decision",
        "steps": [
            {
                "step_id": "d9_s1_learn",
                "step_type": "learn",
                "title": "Why Modern Enterprises Transition to S/4HANA",
                "content_md": """### Beyond Traditional Database Upgrades

SAP S/4HANA is not merely a database upgrade or an ECC release with a new user interface. It represents a fundamental redesign of enterprise resource planning for in-memory hardware architectures.

In legacy ECC architectures:
- **Massive Data Redundancy**: Relational databases could not aggregate millions of records instantaneously, requiring dozens of duplicate summary tables (e.g. GLT0 for account totals, BSIS/BSAS for open/cleared items).
- **Nightly Batch Processing**: Material Requirements Planning (MRP), financial closing, and inventory reconciliation were forced into overnight batches because running them during operating hours locked active transactional tables.
- **Latency in Decision Making**: Executive reports relied on stale data extracted into external data warehouses via ETL pipelines.

### The Three Pillars of S/4HANA Value
1. **Real-Time Execution**: With in-memory columnar computing, analytical calculations (such as real-time MRP or profit center balance sheets) execute directly on transactional records in seconds.
2. **Simplified Data Model**: Hundreds of redundant aggregate and secondary index tables have been replaced with central universal ledgers (ACDOCA for Financial/Controlling line items, MATDOC for Inventory goods movements), while core master data and operational documents remain properly segregated.
3. **User Productivity & Mobility**: Role-based SAP Fiori applications replace complex 4-character transaction codes with responsive, device-independent workflows.""",
                "key_terms": [
                    {"term": "S/4HANA", "definition": "SAP Suite 4 HANA: The next-generation in-memory ERP platform replacing SAP ECC."},
                    {"term": "Real-Time MRP", "definition": "MRP Live (MD01N): Material requirements planning executed directly on the HANA database via SQLScript/AMDP pushdown in minutes rather than hours."},
                    {"term": "Data Footprint Reduction", "definition": "The dramatic shrinkage of database size achieved by eliminating aggregate tables and applying columnar compression."}
                ],
            },
            {
                "step_id": "d9_s2_understand",
                "step_type": "understand",
                "title": "Batch Latency vs. Event-Driven Real-Time Processing",
                "content_md": """### The Architectural Bottleneck of Legacy ERP

In SAP ECC on legacy relational databases, calculating the financial impact of a plant shutdown required:
1. Extracting data from multiple isolated subledgers (AP, AR, Asset Accounting, Cost Center Accounting).
2. Waiting for scheduled batch jobs to execute background balance reconciliations.
3. Reconciling discrepancies caused by concurrent postings that occurred during the batch window.

### S/4HANA Event-Driven Architecture
Because SAP HANA stores columnar data in main memory and utilizes vector SIMD processing, every valuated business event (such as a warehouse goods receipt or customer billing document) immediately updates the universal ledgers (MATDOC/ACDOCA) in real time without batch latency.

- **Zero Reconciliation Overhead**: Controlling and Financial Accounting write to the exact same table row in ACDOCA.
- **Continuous Accounting**: Period-end closing becomes a continuous validation rather than a two-week post-month crisis.
- **Reduced Total Cost of Ownership (TCO)**: A smaller physical memory footprint and fewer batch servers drastically cut infrastructure maintenance costs.""",
            },
            {
                "step_id": "d9_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: From Overnight Batches to Real-Time MRP",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "plants": "PL01 (Heidelberg) & PL02 (Austin)"
                },
                "content_md": """### The Operational Crisis in Heidelberg (PL01)

Before modernizing to S/4HANA, Nova Manufacturing's Heidelberg plant ran its Material Requirements Planning (MRP) batch job every evening at 11:00 PM. 

On Tuesday at 2:00 PM, a key customer placed an urgent rush order for 50 units of the **DXTR-1000** Robotics Controller:
- In ECC, the production planner had to wait until Wednesday morning at 7:00 AM to discover that optical sensors (**RAW-01**) were out of stock. Sourcing was delayed by 17 hours.
- In S/4HANA, the planner executes **MRP Live (MD01N)** in 12 seconds directly on the active database. The missing optical sensors are identified instantaneously, triggering an automated Purchase Requisition to vendor Rheinland Precision Optics (**VEND-101**).""",
            },
            {
                "step_id": "d9_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Analyze S/4HANA Value Drivers & Business Case",
                "component_type": "ScenarioDecision",
                "instruction": "Evaluate the architectural tradeoffs and financial justifications for transitioning Nova Manufacturing from legacy batch ERP to S/4HANA real-time processing.",
                "options": [
                    {
                        "id": "opt_a",
                        "title": "Option A: Retain ECC Batch Infrastructure & Add External Data Warehouse",
                        "consequence": "Nightly batch locks persist. Operational reporting remains 24 hours out-of-date. Heavy ETL maintenance costs continue to escalate.",
                        "tradeoff": "Lowest immediate implementation cost, but severely cripples real-time supply chain agility.",
                        "is_recommended": False
                    },
                    {
                        "id": "opt_b",
                        "title": "Option B: Migrate to S/4HANA Private Cloud with Real-Time MRP & Universal Journal",
                        "consequence": "Batch windows eliminated. Inventory planning latency drops from 17 hours to seconds. Data footprint reduced by 65% via columnar compression.",
                        "tradeoff": "Requires one-time migration effort and Clean Core governance, but radically lowers long-term TCO.",
                        "is_recommended": True
                    }
                ]
            },
            {
                "step_id": "d9_s5_challenge",
                "step_type": "challenge",
                "title": "The CFO's S/4HANA Business Case Challenge",
                "scenario_md": """Nova Manufacturing's Chief Financial Officer questions the investment in S/4HANA:
*"Our IT budget is tight. If we only treat this as a technical database swap without changing our business processes, will we still capture the promised value drivers of S/4HANA?"*

How should the Chief Enterprise Architect respond?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "Yes, simply swapping the database automatically transforms legacy business operations without requiring any organizational or process adjustments.",
                        "is_correct": False,
                        "explanation": "A pure technical lift-and-shift ('technical migration') leaves legacy batch mentalities and redundant custom code in place, capturing only a fraction of S/4HANA value."
                    },
                    {
                        "id": "ch_b",
                        "text": "No. Maximum value requires adopting Clean Core, standard business processes, real-time MRP, and Fiori role-based workflows to eliminate operational latency.",
                        "is_correct": True,
                        "explanation": "True S/4HANA value comes from business process simplification and event-driven operational speed, not just in-memory database speed."
                    },
                    {
                        "id": "ch_c",
                        "text": "No, S/4HANA actually increases operational costs and requires quadrupling the night-shift batch operations team.",
                        "is_correct": False,
                        "explanation": "S/4HANA eliminates batch windows and reduces data footprints, lowering long-term operational overhead."
                    }
                ]
            },
            {
                "step_id": "d9_s6_assessment",
                "step_type": "assessment",
                "title": "Day 9 Concept Assessment: Value Drivers & Real-Time Enterprise",
                "questions": [
                    {
                        "id": "d9_q1",
                        "concept_slug": "s4hana-value-drivers",
                        "prompt": "Which of the following is a primary architectural driver behind the dramatic reduction in database footprint in S/4HANA compared to ECC?",
                        "options": [
                            {"id": "a", "text": "Elimination of redundant pre-aggregated summary and index tables in favor of single columnar ledgers", "is_correct": True},
                            {"id": "b", "text": "Deleting all historical financial data older than 6 months permanently", "is_correct": False},
                            {"id": "c", "text": "Compressing user photos and PDFs stored in the operating system spool", "is_correct": False}
                        ],
                        "explanation": "Eliminating duplicate summary tables (GLT0, BSIS, KNC1) and relying on in-memory aggregation shrinks the database by up to 70%."
                    },
                    {
                        "id": "d9_q2",
                        "concept_slug": "real-time-enterprise",
                        "prompt": "Why can Material Requirements Planning (MRP Live) run during normal business operating hours in S/4HANA without locking active production tables?",
                        "options": [
                            {"id": "a", "text": "Because it executes directly on the database engine via AMDP/SQLScript pushdown, reading inventory from MATDOC and requirements in-memory without legacy balance table locks", "is_correct": True},
                            {"id": "b", "text": "Because it creates static snapshot tables at the beginning of each hour and runs planning exclusively in application server memory", "is_correct": False},
                            {"id": "c", "text": "Because MRP Live only analyzes uncommitted draft simulation data rather than actual inventory", "is_correct": False}
                        ],
                        "explanation": "Database pushdown logic (MRP Live via AMDP) reads inventory movements and open requirements in-memory simultaneously without locking material master balance records."
                    }
                ]
            },
            {
                "step_id": "d9_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 9 Skill Evidence Verification",
                "concept_slug": "s4hana-value-drivers",
                "evidence_rule": "Demonstrated understanding of S/4HANA value drivers, TCO metrics, and real-time processing capabilities.",
            },
            {
                "step_id": "d9_s8_completion",
                "step_type": "completion",
                "title": "Day 9 Complete: S/4HANA Value Drivers Mastered",
                "summary_md": """### 🚀 Value Drivers Foundation Established!

You now understand the fundamental economic and technical imperatives driving S/4HANA adoption:
- The transition from batch-oriented information islands to real-time event processing.
- Elimination of aggregate tables and massive data compression.
- How MRP Live and continuous accounting transform operational velocity at Nova Manufacturing.

**Next Milestone**: Day 10 dives into **ECC → S/4HANA Structural Shifts**—analyzing exactly which tables were deprecated and how Compatibility Views preserve custom code.""",
                "recommended_mission": {
                    "slug": "nova-s4hana-modernization-decision",
                    "title": "Mission: S/4HANA Modernization Decision",
                    "description": "Evaluate Nova Manufacturing's transition roadmap and defend the technical business case to the executive board."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 10: ECC to S/4HANA Structural Shifts
    # =========================================================================
    10: {
        "day_number": 10,
        "slug": "ecc-to-s4hana-changes",
        "title": "ECC to S/4HANA Architectural Changes",
        "subtitle": "Simplification items, table elimination, and compatibility views",
        "estimated_minutes": 45,
        "atomic_concepts": ["ecc-simplification-items", "compatibility-views-concept"],
        "recommended_mission_slug": "nova-s4hana-modernization-decision",
        "steps": [
            {
                "step_id": "d10_s1_learn",
                "step_type": "learn",
                "title": "Deconstructing the Legacy ECC Data Schema",
                "content_md": """### The Proliferation of Redundant Tables in ECC

In classical SAP ECC, relational databases were too slow to calculate open items or account balances on the fly. To achieve acceptable reporting performance, SAP architects created multiple shadow tables for the exact same business transaction:

- **Financial Accounting**: When an invoice was posted, it wrote to the document header (`BKPF`), line items (`BSEG`), open items (`BSIS` for G/L, `BSIK` for vendors, `BSID` for customers), and period balances (`GLT0`).
- **Controlling**: The identical transaction wrote to cost elements (`COEP`), totals (`COSS`), and object headers (`COBK`).
- **Materials Management**: Movements wrote to header (`MKPF`), items (`MSEG`), updated balance counters in master/valuation tables (`MARC`, `MARD`, `MBEW`), and wrote period snapshots into history tables (`MARCH`, `MARDH`, `MBEWH`).

### The Simplification List
SAP published the **Simplification List**—a comprehensive catalog of data model and functional changes between ECC and S/4HANA. Over 40 classical aggregate and index tables were eliminated as physical storage structures and redirected to universal ledgers:
- G/L balances (`GLT0`), open item indexes (`BSIS`, `BSIK`, `BSID`), and CO totals (`COSP`, `COSS`) collapsed into **ACDOCA** (while document headers `BKPF` and open item table `BSEG` remain).
- Material document items (`MSEG`, `MKPF`) and stock history tables (`MARCH`, `MARDH`, `MBEWH`) collapsed into **MATDOC** (while master tables `MARC`, `MARD`, `MBEW` remain).""",
                "key_terms": [
                    {"term": "Simplification Item", "definition": "A documented functional or technical change describing deprecated tables, altered transactions, or new data structures in S/4HANA."},
                    {"term": "Compatibility View", "definition": "A non-materialized CDS database view with the exact schema of a deprecated ECC table, reading dynamically from ACDOCA/MATDOC."},
                    {"term": "De-clustering", "definition": "Converting legacy proprietary cluster tables into transparent tables (e.g. BSEG declustered on HANA; legacy pricing cluster table KONV replaced by transparent table PRCD_ELEMENTS)."}
                ],
            },
            {
                "step_id": "d10_s2_understand",
                "step_type": "understand",
                "title": "How Compatibility Views Protect Custom Legacy Code",
                "content_md": """### The Backward Compatibility Dilemma

Global enterprises run thousands of custom ABAP programs (Z-programs) containing queries like:
```abap
SELECT * FROM bsis WHERE hkont = '0000113100'.
```
If SAP physically deleted table `BSIS` (Open G/L Items), every single custom reporting program in the enterprise would instantly crash with database syntax errors during an upgrade.

### The Architectural Solution: Compatibility Views
SAP solved this using **Compatibility Views**:
1. The physical database table `BSIS` is dropped from database storage.
2. In its place, SAP creates a database view named `BSIS` pointing directly to `ACDOCA`.
3. When custom ABAP executes `SELECT * FROM bsis`, the database transparently redirects the query to `ACDOCA`, dynamically filtering where open item status is active.

### The Read vs. Write Invariant
- **READ Operations**: Fully supported via Compatibility Views without changing a single line of ABAP.
- **WRITE Operations**: Strictly prohibited! Any custom code attempting `INSERT INTO bsis` or `UPDATE bsis` will fail immediately. All transactional postings must use standard SAP S/4HANA APIs or BAPIs.""",
            },
            {
                "step_id": "d10_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: Resolving a Legacy Custom Report Incident",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "system": "S/4HANA Private Cloud (DEV 120 Unit Test)"
                },
                "content_md": """### The Incident in Heidelberg (PL01)

During technical unit testing in DEV Client 120 (after copying customizing from Golden Client 100 via SCC1), the finance team executed a legacy custom report `Z_VENDOR_AGING` that evaluated outstanding payables to suppliers like Rheinland Precision Optics (**VEND-101**):

- The report ran successfully and produced identical results to ECC because its `SELECT * FROM bsik` was automatically redirected by the database to table `ACDOCA`.
- However, a secondary custom routine `Z_UPDATE_STATUS` attempted a direct SQL `UPDATE bsik SET zstat = 'X'`.
- The update crashed with a database exception: **DBSQL_CANNOT_INSERT_TO_VIEW**.

The enterprise development team resolved the incident by replacing the direct SQL write with the standard accounting API `BAPI_ACC_DOCUMENT_POST`, preserving Clean Core integrity.""",
            },
            {
                "step_id": "d10_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Analyze Simplification Impact on Custom ABAP Code",
                "component_type": "ScenarioDecision",
                "instruction": "Examine legacy code patterns and determine the necessary remediation path under S/4HANA simplification rules.",
                "options": [
                    {
                        "id": "opt_read_redirect",
                        "title": "Scenario 1: Custom Report SELECTs from BSAS (Cleared G/L Items)",
                        "consequence": "Compatibility view redirects read query to ACDOCA in-memory. Zero code modification required.",
                        "tradeoff": "Zero migration effort for pure read operations.",
                        "is_recommended": True
                    },
                    {
                        "id": "opt_write_direct",
                        "title": "Scenario 2: Custom Interface Executes INSERT Directly Into MSEG",
                        "consequence": "Fatal database error. MSEG is a compatibility view over MATDOC; direct inserts into views are rejected.",
                        "tradeoff": "Mandatory remediation: must refactor interface to call BAPI_GOODSMVT_CREATE.",
                        "is_recommended": False
                    }
                ]
            },
            {
                "step_id": "d10_s5_challenge",
                "step_type": "challenge",
                "title": "The Legacy Code Modernization Dilemma",
                "scenario_md": """A senior ABAP developer proposes keeping 40 legacy custom Z-reports querying compatibility views forever:
*"Since Compatibility Views work transparently, there is no need to ever refactor our custom reports to use Core Data Services (CDS) or modern APIs."*

As the S/4HANA Technical Architect, what is your evaluation?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "The developer is correct. Compatibility views have zero performance overhead and will remain forever in future cloud releases.",
                        "is_correct": False,
                        "explanation": "Compatibility views are transitional bridges. They do not leverage modern CDS associations or pushdown annotations and cannot be exposed to Fiori."
                    },
                    {
                        "id": "ch_b",
                        "text": "Incorrect. Compatibility views are transitional bridges. New reporting must use CDS View Entities to leverage Fiori Elements and full analytical pushdown.",
                        "is_correct": True,
                        "explanation": "While compatibility views prevent runtime crashes, true architectural modernization requires native CDS View Entities."
                    },
                    {
                        "id": "ch_c",
                        "text": "Incorrect. The database will delete all compatibility views every 30 days automatically.",
                        "is_correct": False,
                        "explanation": "Compatibility views are managed database artifacts, not temporary caches."
                    }
                ]
            },
            {
                "step_id": "d10_s6_assessment",
                "step_type": "assessment",
                "title": "Day 10 Concept Assessment: Simplification Items & Compatibility Views",
                "questions": [
                    {
                        "id": "d10_q1",
                        "concept_slug": "ecc-simplification-items",
                        "prompt": "What happened to the physical database tables GLT0, KNC1, and LFC1 (period balance aggregates) during the transition to S/4HANA?",
                        "options": [
                            {"id": "a", "text": "They were eliminated as physical storage tables because balances are aggregated dynamically from ACDOCA in real-time", "is_correct": True},
                            {"id": "b", "text": "They were moved to an encrypted USB drive attached to the server", "is_correct": False},
                            {"id": "c", "text": "They were expanded to 1,000 columns each to store raw transactions", "is_correct": False}
                        ],
                        "explanation": "Aggregate tables were eliminated because HANA computes balances on-the-fly directly from Universal Journal line items."
                    },
                    {
                        "id": "d10_q2",
                        "concept_slug": "compatibility-views-concept",
                        "prompt": "What is the primary constraint when an ABAP program interacts with a legacy table that has been replaced by a Compatibility View?",
                        "options": [
                            {"id": "a", "text": "SELECT statements are redirected to ACDOCA/MATDOC, but direct INSERT/UPDATE/DELETE database modifications will fail", "is_correct": True},
                            {"id": "b", "text": "The program can only be executed between 8:00 AM and 5:00 PM", "is_correct": False},
                            {"id": "c", "text": "The program must be written in Python instead of ABAP", "is_correct": False}
                        ],
                        "explanation": "Compatibility views are read-only database projections; direct write operations are strictly disallowed."
                    }
                ]
            },
            {
                "step_id": "d10_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 10 Skill Evidence Verification",
                "concept_slug": "ecc-simplification-items",
                "evidence_rule": "Demonstrated understanding of database simplification lists and compatibility view mechanics.",
            },
            {
                "step_id": "d10_s8_completion",
                "step_type": "completion",
                "title": "Day 10 Complete: Structural Shifts Mastered",
                "summary_md": """### 🛡️ Legacy Simplifications Mastered!

You have mastered the architectural shifts between ECC and S/4HANA:
- Why redundant aggregate and index tables were decommissioned.
- How Compatibility Views protect legacy ABAP read operations.
- The strict prohibition against direct database writes to deprecated tables.

**Next Milestone**: Day 11 explores the **HANA In-Memory Engine**—uncovering column-store mechanics, dictionary encoding, and the critical Delta Merge lifecycle.""",
                "recommended_mission": {
                    "slug": "nova-s4hana-modernization-decision",
                    "title": "Mission: S/4HANA Modernization Decision",
                    "description": "Analyze Nova Manufacturing's ECC modernization roadmap and classify simplification impacts."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 11: HANA In-Memory Engine
    # =========================================================================
    11: {
        "day_number": 11,
        "slug": "hana-in-memory-architecture",
        "title": "HANA In-Memory Database Architecture",
        "subtitle": "Columnar data storage, dictionary compression, and the delta merge lifecycle",
        "estimated_minutes": 45,
        "atomic_concepts": ["in-memory-computing", "columnar-database-engine", "delta-merge-architecture"],
        "recommended_mission_slug": "nova-architecture-layer-incident",
        "steps": [
            {
                "step_id": "d11_s1_learn",
                "step_type": "learn",
                "title": "How SAP HANA Redefines Database Mechanics",
                "content_md": """### Memory as the Primary Persistence Tier

Classical relational database management systems (RDBMS) were architected when RAM was prohibitively expensive. They treated disk storage as the primary source of truth, loading small pages into memory buffers only when needed.

**SAP HANA inverts this paradigm**:
- **RAM as Primary Working Store**: Active columnar tables are loaded into memory for query processing. Column data is loaded on-demand (lazy loading) and can be dynamically unloaded or paged via Native Storage Extension (NSE) under memory thresholds.
- **ACID Persistence Layer**: Persistence is non-volatile and dual-tiered: Data Volumes record asynchronous dirty page savepoints (every 5 minutes by default), while Log Volumes record synchronous redo logs on transaction commit.
- **Secondary Indexes in Column Store**: While columnar layout inherently acts as a single-column scan index via dictionary encoding, SAP HANA actively utilizes secondary inverted indexes for multi-column criteria, unique constraints, and high-selectivity joins.
- **Column-Store by Default**: Tables are stored vertically column-by-column rather than row-by-row.
- **Massive Parallelism**: Modern multi-core CPUs scan columnar data arrays in parallel using SIMD (Single Instruction, Multiple Data) vector registers.

### Column-Store vs. Row-Store
| Feature | Row-Store (Legacy) | Column-Store (SAP HANA) |
|---|---|---|
| Contiguous Layout | Entire records: `[ID, Date, Mat, Qty, Val]` | Single attributes: `[Qty1, Qty2, Qty3...]` |
| Aggregation Performance | Slow (must read all unused columns) | Blazing fast (scans only the target column) |
| Compression Ratio | Low (diverse data types in each block) | Extreme (identical data types compress up to 10:1) |
| Best Used For | Configuration tables, single-record lookup | High-volume transactional & reporting tables |""",
                "key_terms": [
                    {"term": "Columnar Storage", "definition": "Storing database tables by attribute columns contiguously in memory rather than by complete rows."},
                    {"term": "Dictionary Encoding", "definition": "Replacing repetitive data values (e.g. Plant 'PL01') with small integer tokens and a distinct lookup dictionary."},
                    {"term": "Delta Merge", "definition": "The asynchronous background process that merges uncompressed writes from Delta Storage into compressed Main Storage."}
                ],
            },
            {
                "step_id": "d11_s2_understand",
                "step_type": "understand",
                "title": "The Delta Merge Architecture: Resolving the Write Penalty",
                "content_md": """### The Architectural Challenge of Columnar Compression

While columnar dictionary compression makes analytical SELECT queries ultra-fast, inserting a single row into a heavily compressed column requires:
1. Decompressing the entire column dictionary.
2. Inserting the new distinct value in sorted order.
3. Re-encoding all index vectors across millions of rows.

If every incoming sales order had to recompress Main Memory, write performance would drop to single-digit transactions per second!

### The Two-Tier Storage Architecture
SAP HANA solves this through the **Delta Storage Architecture**:

1. **Main Storage**:
   - Contains 99% of historical data.
   - Read-optimized and highly compressed via dictionary encoding.
   - Strictly **read-only**; never modified in-place during ordinary transactions.

2. **Delta Storage**:
   - Write-optimized with minimal compression.
   - Accepts all incoming `INSERT`, `UPDATE`, and `DELETE` operations instantaneously.

3. **The Delta Merge Process**:
   - When Delta storage reaches a threshold size, an asynchronous background thread triggers the **Delta Merge**.
   - A new Main Storage (Main 2) is created incorporating all Delta changes.
   - Once Main 2 is complete, active readers switch instantaneously to Main 2, and the old Delta storage is truncated.""",
            },
            {
                "step_id": "d11_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: High-Throughput Goods Movements",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "plant": "PL01 (Heidelberg Assembly)"
                },
                "content_md": """### Peak Shift Transaction Volume

At Nova Manufacturing's Heidelberg assembly plant, 45 automated robotic assembly lines produce robotics controllers (**DXTR-1000**), generating over 200 goods movements per minute during the morning shift:

- Every goods movement appends directly to the write-optimized **Delta Storage** of table `MATDOC`.
- Operators experience instantaneous response times under 5 milliseconds due to the elimination of database row-level counter locks on stock balance tables.
- Meanwhile, the plant manager runs real-time inventory queries across 8,000,000 historical records. The query reads compressed **Main Storage** and the small active **Delta Storage** simultaneously, returning exact stock counts in 0.04 seconds.
- At 1:00 PM, HANA automatically executes an asynchronous Delta Merge, incorporating the morning's 60,000 transactions into Main storage without blocking any active assembly line transactions.""",
            },
            {
                "step_id": "d11_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Interactive HANA Storage & Delta Merge Lab",
                "component_type": "HANAStorageVisualizer",
                "instruction": "Inspect the Main Storage dictionary vector compression and simulate transaction writes into Delta Storage. Execute a Delta Merge to observe memory re-balancing.",
            },
            {
                "step_id": "d11_s5_challenge",
                "step_type": "challenge",
                "title": "The Memory Explosion Operational Incident",
                "scenario_md": """During month-end close at Nova Manufacturing, an alert triggers on the SAP HANA database:
*Alert 43: High Memory Consumption in Delta Storage (Table ACDOCA > 40 GB).*

The junior DBA suggests rebooting the database server immediately. What is the correct architectural evaluation and remediation?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "Reboot the database server to clear all RAM instantly.",
                        "is_correct": False,
                        "explanation": "Rebooting interrupts active business operations and forces a lengthy database reload from disk savepoints."
                    },
                    {
                        "id": "ch_b",
                        "text": "Do not reboot. The alert indicates that automated delta merge was delayed by long-running transactions. Execute an explicit manual Delta Merge or inspect uncommitted open transactions.",
                        "is_correct": True,
                        "explanation": "Delta growth is resolved by executing a Delta Merge once blocking uncommitted transactions complete."
                    },
                    {
                        "id": "ch_c",
                        "text": "Convert table ACDOCA from Column-Store to Row-Store permanently.",
                        "is_correct": False,
                        "explanation": "ACDOCA must reside in Column-Store for S/4HANA to operate; row-store conversion is unsupported and fatal."
                    }
                ]
            },
            {
                "step_id": "d11_s6_assessment",
                "step_type": "assessment",
                "title": "Day 11 Concept Assessment: In-Memory & Columnar Mechanics",
                "questions": [
                    {
                        "id": "d11_q1",
                        "concept_slug": "columnar-database-engine",
                        "prompt": "Why does a reporting query executing SELECT SUM(menge) FROM matdoc run significantly faster on a columnar database than on a row-oriented database?",
                        "options": [
                            {"id": "a", "text": "Because the CPU only reads the contiguous memory addresses of the 'menge' column, skipping all other table attributes entirely", "is_correct": True},
                            {"id": "b", "text": "Because columnar databases convert all numbers into text before calculating", "is_correct": False},
                            {"id": "c", "text": "Because the operating system sends the calculation to an overseas cloud server", "is_correct": False}
                        ],
                        "explanation": "Columnar storage avoids dragging unnecessary columns into CPU memory caches during aggregations."
                    },
                    {
                        "id": "d11_q2",
                        "concept_slug": "delta-merge-architecture",
                        "prompt": "What occurs to active SELECT queries that are currently reading Main Storage when a Delta Merge begins?",
                        "options": [
                            {"id": "a", "text": "They continue reading the original Main Storage undisturbed; once the merge creates Main 2, subsequent queries switch seamlessly without interruption", "is_correct": True},
                            {"id": "b", "text": "All active queries are terminated with an error code", "is_correct": False},
                            {"id": "c", "text": "Queries are paused and frozen for up to 45 minutes", "is_correct": False}
                        ],
                        "explanation": "HANA utilizes Multi-Version Concurrency Control (MVCC) so active readers are never blocked by the merge process."
                    }
                ]
            },
            {
                "step_id": "d11_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 11 Skill Evidence Verification",
                "concept_slug": "columnar-database-engine",
                "evidence_rule": "Demonstrated understanding of columnar storage, dictionary encoding, and delta merge execution.",
            },
            {
                "step_id": "d11_s8_completion",
                "step_type": "completion",
                "title": "Day 11 Complete: HANA In-Memory Architecture Mastered",
                "summary_md": """### ⚡ In-Memory Architecture Validated!

You possess certified comprehension of the SAP HANA engine:
- Columnar vector scanning and dictionary compression ratios.
- How write-optimized Delta Storage eliminates row-level write contention.
- Multi-Version Concurrency Control (MVCC) and the Delta Merge lifecycle.

**Next Milestone**: Day 12 examines the crown jewel of S/4HANA Finance—**ACDOCA & The Universal Journal**!""",
                "recommended_mission": {
                    "slug": "nova-architecture-layer-incident",
                    "title": "Mission: Architecture Layer Incident",
                    "description": "Diagnose database bottlenecks and optimize work process allocation across Nova Manufacturing's 3-tier architecture."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 12: ACDOCA / Universal Journal
    # =========================================================================
    12: {
        "day_number": 12,
        "slug": "acdoca-universal-journal",
        "title": "ACDOCA & Universal Journal Architecture",
        "subtitle": "The universal accounting document table: 350+ dimensions, FI/CO unification, and parallel ledgers",
        "estimated_minutes": 45,
        "atomic_concepts": [
            "universal-journal-concept",
            "fi-co-unification",
            "acdoca-table-architecture",
            "parallel-ledgers",
            "multi-currency-accounting"
        ],
        "recommended_mission_slug": "nova-universal-journal-investigation",
        "steps": [
            {
                "step_id": "d12_s1_learn",
                "step_type": "learn",
                "title": "The Single Source of Truth in Financial Accounting",
                "content_md": """### The Fragmentation of Legacy Financials

In legacy SAP ECC, the Chief Financial Officer faced a structural dilemma: Financial Accounting (FI) and Controlling (CO) were two completely separate software modules with separate databases:
- **FI (External Reporting)** wrote balance sheet accounts to `BSEG`/`BKPF` for statutory tax authorities and investors.
- **CO (Internal Management)** wrote cost centers and internal orders to `COEP`/`COBK` for operational management profitability.
- At the end of every month, accounting teams spent hundreds of hours running the **FI-CO Reconciliation Ledger** (`KALC`) to balance contradictory totals.

### Table ACDOCA: The Universal Journal
SAP S/4HANA completely dismantled this division by introducing table **ACDOCA** (The Universal Accounting Document):
- **Unified Journal Line Items**: Every accounting document posts a header record in `BKPF` and balanced debit/credit line items in `ACDOCA` (with open-item-managed items also synchronized in `BSEG`).
- **350+ Unified Dimensions**: Each line item simultaneously stores G/L Account, Profit Center, Cost Center, Functional Area, Segment, Business Partner, and Fixed Asset subledger assignments.
- **FI and CO Unification**: Secondary cost elements are configured directly as G/L accounts (categories 42/43). FI and CO read from the exact same line item table, rendering the legacy reconciliation ledger obsolete.
- **Separation of Operational Documents**: ACDOCA stores accounting postings; operational source documents—such as Sales Orders (`VBAK`/`VBAP`), Purchase Orders (`EKKO`/`EKPO`), and Billing Invoices (`VBRK`/`VBRP`)—remain in their dedicated logistics tables. ACDOCA entries link back to these source documents via the Object Type (`AWTYP = 'MKPF'` for goods movements, `'VBRK'` for billing) and Reference Key (`AWKEY`/`AWREF`).""",
                "key_terms": [
                    {"term": "ACDOCA", "definition": "The central Universal Journal line item table in S/4HANA storing all financial, management, asset, and material valuation postings."},
                    {"term": "Parallel Ledgers", "definition": "Maintaining multiple distinct ledgers (e.g. 0L for IFRS and 2L for local tax GAAP) within ACDOCA simultaneously."},
                    {"term": "Secondary Cost Element", "definition": "In S/4HANA, an internal allocation cost object configured directly as a G/L Account (category 42/43)."}
                ],
            },
            {
                "step_id": "d12_s2_understand",
                "step_type": "understand",
                "title": "Multi-GAAP Parallel Accounting & Multi-Currency Dimensions",
                "content_md": """### Parallel Ledgers in Global Corporations

Global enterprises cannot operate under a single set of accounting rules:
- An enterprise headquartered in Germany with subsidiaries in the USA must report under **IFRS** for global consolidation, but must report under **US GAAP** or **German HGB** for local statutory tax authorities.

### The S/4HANA Ledger Architecture
Inside ACDOCA, every line item is tagged with a `RLDNR` (Ledger) identifier:
1. **Leading Ledger (0L)**:
   - Contains the primary accounting principle (e.g. IFRS).
   - Fully integrated with all subledgers (AP, AR, Fixed Assets, Inventory).
   - Used for global executive consolidation.
2. **Non-Leading Ledgers (e.g. 2L)**:
   - Contains local statutory principles (e.g. German HGB or US GAAP).
   - Only records transactions where local accounting rules differ (e.g. accelerated asset depreciation or inventory valuation variances).

### Multi-Currency Storage
In a single ACDOCA record, S/4HANA persists up to 10 parallel currency values simultaneously:
- `WSL`: Transaction / Document Currency (e.g. JPY).
- `TSL`: Company Code Local Currency (e.g. EUR).
- `KSL`: Global Group Currency (e.g. USD).""",
            },
            {
                "step_id": "d12_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: Parallel Depreciation & Multi-Ledger Entry",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01 (Heidelberg, EUR)",
                    "plant": "PL01 & PL02"
                },
                "content_md": """### Purchasing a €120,000 Robotic Stamping Cell

Nova Manufacturing acquired a heavy precision stamping machine for Plant `PL01`:

In SAP S/4HANA, when the monthly depreciation runs:
- **Leading Ledger 0L (IFRS)**: Depreciates over 10 years straight-line = **€1,000.00 / month**.
  - `Line 1 (0L)`: Dr Depreciation Expense `650000`, Cr Accumulated Depreciation `170000` (€1,000.00).
- **Non-Leading Ledger 2L (German HGB)**: Tax rules permit accelerated depreciation = **€1,500.00 / month**.
  - `Line 2 (2L)`: Dr Depreciation Expense `650000`, Cr Accumulated Depreciation `170000` (€1,500.00).

Both postings occur synchronously in table `ACDOCA` tagged with Cost Center `CC-1100` (Assembly Operations) and Profit Center `PC-1000` (Robotics). When the corporate controller runs group statements, 0L is queried; when German tax auditors inspect, 2L is queried. Zero data reconciliation is required!""",
            },
            {
                "step_id": "d12_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Interactive ACDOCA Universal Journal Inspector",
                "component_type": "UniversalJournalVisualizer",
                "instruction": "Filter line items between Leading Ledger 0L and Non-Leading Ledger 2L. Inspect how FI and CO dimensions coexist in a single atomic record.",
            },
            {
                "step_id": "d12_s5_challenge",
                "step_type": "challenge",
                "title": "The Period-End Intercompany Clearing Dilemma",
                "scenario_md": """Nova Manufacturing transfers 20 robotics components from Heidelberg (Plant PL01) to the Austin Tech Center (Plant PL02) under Company Code NM01.
The junior accountant asks:
*"Do we need to run a batch FI-CO reconciliation job at the end of the month to balance the cost allocations between our plants?"*

How should the Chief Enterprise Architect advise?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "Yes, cross-company cost allocations still require running transaction KALC on the last Friday of every month.",
                        "is_correct": False,
                        "explanation": "Transaction KALC and the FI-CO reconciliation ledger are completely obsolete in S/4HANA."
                    },
                    {
                        "id": "ch_b",
                        "text": "No. In S/4HANA, secondary cost allocations write directly to ACDOCA and automatically generate intercompany clearing entries in real-time.",
                        "is_correct": True,
                        "explanation": "Universal Journal integration immediately posts intercompany receivables and payables during internal activity allocation."
                    },
                    {
                        "id": "ch_c",
                        "text": "No, because S/4HANA prohibits doing business between two entities of the same parent company.",
                        "is_correct": False,
                        "explanation": "Intercompany business is fully supported and automated via Universal Journal cross-company postings."
                    }
                ]
            },
            {
                "step_id": "d12_s6_assessment",
                "step_type": "assessment",
                "title": "Day 12 Concept Assessment: Universal Journal & Parallel Ledgers",
                "questions": [
                    {
                        "id": "d12_q1",
                        "concept_slug": "universal-journal-concept",
                        "prompt": "Which statement accurately describes how Financial Accounting (FI) and Controlling (CO) are integrated in SAP S/4HANA?",
                        "options": [
                            {"id": "a", "text": "They write to the exact same table (ACDOCA), eliminating the need for period-end reconciliation runs between G/L and cost accounting", "is_correct": True},
                            {"id": "b", "text": "FI is stored on the HANA database while CO is stored in an Access database file", "is_correct": False},
                            {"id": "c", "text": "CO has been completely removed from SAP and replaced by a calculator widget", "is_correct": False}
                        ],
                        "explanation": "ACDOCA unifies FI and CO into a single transactional line-item table."
                    },
                    {
                        "id": "d12_q2",
                        "concept_slug": "parallel-ledgers",
                        "prompt": "In S/4HANA multi-GAAP accounting, what is the role of the Leading Ledger (0L)?",
                        "options": [
                            {"id": "a", "text": "It represents the corporate group's primary accounting standard (e.g. IFRS) and is integrated across all subledgers", "is_correct": True},
                            {"id": "b", "text": "It is a temporary ledger used only for testing new company codes before going live", "is_correct": False},
                            {"id": "c", "text": "It only stores foreign currency exchange rates and cannot hold accounting amounts", "is_correct": False}
                        ],
                        "explanation": "Leading ledger 0L is the primary source for group consolidation and mandatory subledger integration."
                    }
                ]
            },
            {
                "step_id": "d12_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 12 Skill Evidence Verification",
                "concept_slug": "universal-journal-concept",
                "evidence_rule": "Demonstrated mastery of ACDOCA schema, FI/CO single source of truth, and parallel ledger configuration.",
            },
            {
                "step_id": "d12_s8_completion",
                "step_type": "completion",
                "title": "Day 12 Complete: Universal Journal Mastered",
                "summary_md": """### 🏆 Universal Journal Verified!

You have conquered one of the most critical architecture innovations in enterprise ERP:
- Table `ACDOCA` as the 350+ dimension single source of truth.
- Elimination of the FI-CO reconciliation ledger.
- Parallel Ledgers (`0L` vs `2L`) and multi-currency accounting.

**Next Milestone**: Day 13 explores the logistics counterpart to ACDOCA—**MATDOC and Inventory Simplification**!""",
                "recommended_mission": {
                    "slug": "nova-universal-journal-investigation",
                    "title": "Mission: Universal Journal Investigation",
                    "description": "Investigate financial balance discrepancies across parallel ledgers and audit multi-dimension postings in ACDOCA."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 13: MATDOC / Inventory Simplification
    # =========================================================================
    13: {
        "day_number": 13,
        "slug": "matdoc-inventory-architecture",
        "title": "Material Document Architecture (MATDOC)",
        "subtitle": "Inventory management simplification: single-table ledger, lock reduction, and valuation",
        "estimated_minutes": 45,
        "atomic_concepts": ["matdoc-table-architecture", "simplified-inventory-valuation"],
        "recommended_mission_slug": "nova-matdoc-inventory-incident",
        "steps": [
            {
                "step_id": "d13_s1_learn",
                "step_type": "learn",
                "title": "The Logistics Bottleneck: Legacy Inventory Tables",
                "content_md": """### The Spaghetti Architecture of Legacy Inventory

In SAP ECC Materials Management (MM-IM), posting a simple goods movement (e.g. Goods Receipt for a Purchase Order) was one of the most database-intensive operations in the enterprise:
- **Header & Item Tables**: Wrote document metadata to `MKPF` and line items to `MSEG`.
- **Stock Total Tables**: Updated stock quantities in `MARC` (Plant stock), `MARD` (Storage location stock), `MSSQ` (Special stock), and `MCHB` (Batch stock).
- **Valuation Tables**: Updated inventory value in `MBEW`.
- **History Tables**: Updated monthly historical snapshots in `MARCH`, `MARDH`, and `MBEWH`.

### The Catastrophic Consequence: Table Locks
Because multiple transactions for the same material had to update the exact same balance row in `MARC` and `MBEW`, the database acquired exclusive **row-level locks**. If ten forklift operators attempted to scan goods receipts for the same raw material simultaneously, nine operators were blocked and experienced screen freezes!

### Table MATDOC: The Universal Inventory Ledger
SAP S/4HANA eliminated database balance locks by introducing table **MATDOC**:
- Consolidates goods movement document tables (`MKPF`, `MSEG`) and legacy periodic stock history tables (`MARCH`, `MARDH`, `MBEWH`, `MSSQH`) into a single insert-only columnar ledger.
- Material master tables (`MARA`, `MARC`, `MARD`) and valuation tables (`MBEW`) remain as physical master data anchors.
- Current stock balances and valuations are computed dynamically in-memory via Core Data Services (CDS) views (such as `NSDM_V_MARD`) that aggregate recent `MATDOC` postings with baseline inventory levels.""",
                "key_terms": [
                    {"term": "MATDOC", "definition": "The single universal material document table in S/4HANA storing all inventory goods movements and valuation updates."},
                    {"term": "Insert-Only Architecture", "definition": "An append-only database design where new transactions insert rows rather than updating locked total balance records."},
                    {"term": "Lock Contention Reduction", "definition": "The dramatic reduction of warehouse bottlenecks achieved by eliminating row-level locks on material master balance counters."}
                ],
            },
            {
                "step_id": "d13_s2_understand",
                "step_type": "understand",
                "title": "How Real-Time Columnar Aggregation Replaces Physical Totals",
                "content_md": """### The Myth of Physical Balance Storage

For four decades, software engineers assumed that calculating total inventory required maintaining a physical counter:
$$\\text{Total Stock} = \\text{Previous Stock} + \\text{Receipt} - \\text{Issue}$$

Updating this counter requires a database lock on the counter row.

### The In-Memory Revolution
In SAP HANA, column-store scans execute at billions of records per second. When an application asks: *"What is the current unrestricted stock of material DXTR-1000 in Plant PL01 Storage Location FG01?"*, S/4HANA does not read a static counter in `MARD`.

Instead, it executes dynamic in-memory aggregation through hybrid Core Data Services (CDS) views such as `NSDM_V_MARD`:
```sql
-- Hybrid aggregation model: baseline snapshot plus active MATDOC deltas
SELECT matnr, werks, lgort, SUM(menge) AS labst
FROM nsdm_v_mard
WHERE matnr = 'DXTR-1000' AND werks = 'PL01' AND lgort = 'FG01'
GROUP BY matnr, werks, lgort;
```
Because `MATDOC` is stored in contiguous columnar RAM and compressed via dictionary encoding, the HANA engine computes the current stock balance across millions of historical transactions in microseconds.

### Benefits
1. **Massive Lock Reduction**: Warehouse throughput increases dramatically because transactions append rows to `MATDOC` without competing for database row-level locks on balance counter tables. (Note: Application-level enqueue locks in `SM12`, such as moving average price valuation locks or negative stock checks, are still respected during the LUW).
2. **Infinite Historical Auditability**: Stock balances can be reconstructed for any second in history without running month-end snapshot jobs (`MMPV`).""",
            },
            {
                "step_id": "d13_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: High-Speed Warehouse Inbound at PL01",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "storage_locations": "RAW1 (Raw Materials) & FG01 (Finished Goods)"
                },
                "content_md": """### Receiving 500 Optical Sensor Arrays (RAW-01)

At Plant `PL01` in Heidelberg, three delivery trucks arrive simultaneously from Rheinland Precision Optics (**VEND-101**):

1. **Truck 1**: Dock 4 receives 200 units of `RAW-01` (PO #4500008101).
2. **Truck 2**: Dock 5 receives 200 units of `RAW-01` (PO #4500008102).
3. **Truck 3**: Dock 6 receives 100 units of `RAW-01` (PO #4500008103).

In legacy ECC, Dock 5 and Dock 6 would freeze while Dock 4 locked table `MBEW`.
In S/4HANA, three distinct rows (`MBLNR 5000010912`, `5000010913`, `5000010914`) are appended into `MATDOC` simultaneously. Within 4 milliseconds, total available inventory of `RAW-01` in Storage Location `RAW1` reflects **500 units**, immediately visible to production scheduling!""",
            },
            {
                "step_id": "d13_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Interactive MATDOC Single-Table Inventory Flow",
                "component_type": "MATDOCFlow",
                "instruction": "Explore real-time goods receipts and transfer postings in table MATDOC. Toggle the ECC Legacy view to contrast with deprecated table locks.",
            },
            {
                "step_id": "d13_s5_challenge",
                "step_type": "challenge",
                "title": "The High-Frequency Warehouse Lock Contention Incident",
                "scenario_md": """During the launch of Nova Manufacturing's Austin Tech Center (PL02), logistics engineers report that automated barcode scanners occasionally experience 30-second delays during high-volume goods issue.

The warehouse manager suspects table lock contention on table MSEG. What is the technical diagnosis?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "MSEG table locks cannot be the cause in S/4HANA because MSEG is a read-only compatibility view; the bottleneck must be external network latency or an application enqueue lock (e.g. SM12 moving average price lock or Z-code lock).",
                        "is_correct": True,
                        "explanation": "S/4HANA writes directly to MATDOC without database row-level counter locks on MARC/MSEG. Delays in S/4HANA typically stem from custom Z-code locks, RFC/network latency, or application enqueue locks in SM12 (e.g., late valuation lock contention on moving average price materials)."
                    },
                    {
                        "id": "ch_b",
                        "text": "The manager is correct: MSEG must be restarted every morning to release warehouse locks.",
                        "is_correct": False,
                        "explanation": "MSEG is not an active write table in S/4HANA."
                    },
                    {
                        "id": "ch_c",
                        "text": "The warehouse must stop scanning barcodes and record goods movements with pen and paper.",
                        "is_correct": False,
                        "explanation": "Manual recording eliminates enterprise traceability."
                    }
                ]
            },
            {
                "step_id": "d13_s6_assessment",
                "step_type": "assessment",
                "title": "Day 13 Concept Assessment: Material Document Architecture",
                "questions": [
                    {
                        "id": "d13_q1",
                        "concept_slug": "matdoc-table-architecture",
                        "prompt": "How does table MATDOC simplify the SAP S/4HANA Materials Management data model compared to SAP ECC?",
                        "options": [
                            {"id": "a", "text": "It consolidates header, item, and historical inventory balances into a single insert-only columnar table while retaining master tables MARC and MARD", "is_correct": True},
                            {"id": "b", "text": "It physically deletes all plant master data in MARC and forces all queries into unindexed text logs", "is_correct": False},
                            {"id": "c", "text": "It replaces relational tables with flat JSON files stored in client web browser local storage", "is_correct": False}
                        ],
                        "explanation": "MATDOC replaces document tables MKPF and MSEG as well as legacy stock history/aggregate tables (MARCH, MARDH, MBEWH), while master tables MARC, MARD, and valuation table MBEW remain as physical master structures."
                    },
                    {
                        "id": "d13_q2",
                        "concept_slug": "simplified-inventory-valuation",
                        "prompt": "Why can concurrent goods receipts for the exact same material occur simultaneously in S/4HANA without lock contention?",
                        "options": [
                            {"id": "a", "text": "Because goods movements insert new rows into MATDOC without locking a static balance row in MARC/MBEW", "is_correct": True},
                            {"id": "b", "text": "Because S/4HANA ignores inventory valuation completely", "is_correct": False},
                            {"id": "c", "text": "Because only one person in the entire world is allowed to use S/4HANA at a time", "is_correct": False}
                        ],
                        "explanation": "Insert-only architecture avoids row-level locks on material master balance totals."
                    }
                ]
            },
            {
                "step_id": "d13_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 13 Skill Evidence Verification",
                "concept_slug": "matdoc-table-architecture",
                "evidence_rule": "Demonstrated mastery of MATDOC architecture, inventory lock reduction, and columnar valuation.",
            },
            {
                "step_id": "d13_s8_completion",
                "step_type": "completion",
                "title": "Day 13 Complete: MATDOC Architecture Mastered",
                "summary_md": """### 📦 Inventory Architecture Validated!

You have mastered the mechanics of S/4HANA inventory management:
- Single-table inventory storage in table `MATDOC`.
- Real-time columnar stock balance aggregation replacing locked counters.
- Dramatic throughput acceleration across automated logistics facilities.

**Next Milestone**: Day 14 tackles master data modernization—**Business Partner & Customer-Vendor Integration (CVI)**!""",
                "recommended_mission": {
                    "slug": "nova-matdoc-inventory-incident",
                    "title": "Mission: MATDOC Inventory Incident",
                    "description": "Troubleshoot concurrent goods movements and audit inventory valuation integrity in MATDOC."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 14: Business Partner / CVI
    # =========================================================================
    14: {
        "day_number": 14,
        "slug": "business-partner-cvi",
        "title": "Business Partner & Customer-Vendor Integration (CVI)",
        "subtitle": "Mandatory Business Partner master data, CVI synchronization cockpit, and role architecture",
        "estimated_minutes": 45,
        "atomic_concepts": ["business-partner-cvi", "customer-vendor-synchronization"],
        "recommended_mission_slug": "nova-business-partner-migration",
        "steps": [
            {
                "step_id": "d14_s1_learn",
                "step_type": "learn",
                "title": "The Mandatory Single Point of Entry: Business Partner",
                "content_md": """### The Fragmented Master Data of Legacy ECC

In classical SAP ECC, customer and vendor master data were completely isolated:
- Vendors were created in transaction `XK01` and written to tables `LFA1` (General), `LFB1` (Company Code), and `LFM1` (Purchasing).
- Customers were created in transaction `XD01` and written to tables `KNA1` (General), `KNB1` (Company Code), and `KNVV` (Sales).

If an enterprise like Nova Manufacturing bought raw materials from a partner and also sold spare parts to that same partner:
- The partner had to be created twice with separate IDs.
- Two separate mailing addresses, tax numbers, and bank details had to be maintained manually.
- If the partner changed their bank account, updating the vendor record left the customer record dangerously out of sync!

### The S/4HANA Paradigm: Central Business Partner (BP)
In SAP S/4HANA, transactions `XK01`, `XD01`, `FK01`, and `FD01` are **completely obsolete**.
The **Business Partner (BP)** transaction is the single mandatory point of entry for all legal entities, individuals, and organizations.""",
                "key_terms": [
                    {"term": "Business Partner (BP)", "definition": "The central S/4HANA master data entity representing natural persons or legal organizations with multiple business roles."},
                    {"term": "Customer-Vendor Integration (CVI)", "definition": "The synchronization layer that automatically maps central BP data into underlying customer (KNA1) and vendor (LFA1) tables."},
                    {"term": "MDS_LOAD_COCKPIT", "definition": "The master data synchronization cockpit transaction used to migrate and synchronize legacy ECC customer/vendor records into BPs."}
                ],
            },
            {
                "step_id": "d14_s2_understand",
                "step_type": "understand",
                "title": "Role Architecture and CVI Synchronization Mechanics",
                "content_md": """### Single Identity, Multiple Business Roles

In S/4HANA, table `BUT000` stores the central identity (Legal Name, Address, Tax Numbers) once.
Specific functional capabilities are added by assigning **BP Roles**:

1. **General Role (`000000`)**:
   - Universal baseline identity. No company code or sales data required.
2. **Supplier Roles**:
   - `FLVN00` (FI Vendor): Adds Company Code accounting views (reconciliation accounts, payment terms). Required for Accounts Payable.
   - `FLVN01` (Purchasing Supplier): Adds Purchasing Organization views (order currency, Incoterms). Required for Purchase Orders.
3. **Customer Roles**:
   - `FLCU00` (FI Customer): Adds Company Code views for Accounts Receivable.
   - `FLCU01` (Sales Customer): Adds Sales Area views (shipping conditions, pricing). Required for Sales Orders.

### The CVI Synchronization Layer
When an administrator saves a Business Partner in transaction `BP`, the **Customer-Vendor Integration (CVI)** engine executes synchronously in the background:
- It transparently updates underlying supplier tables (`LFA1` general, `LFB1` company code, `LFM1` purchasing) and customer tables (`KNA1` general, `KNB1` company code, `KNVV` sales area).
- Legacy custom reports, interfaces, and EDI mappings that read `LFA1` or `KNA1` continue to function with 100% fidelity!

> [!IMPORTANT]
> **Subledger Tables Are NOT Deleted**: A widespread misconception is that S/4HANA eliminated tables `KNA1` and `LFA1`. In fact, they are retained as active projection tables. Financial subledgers and logistics transactions still depend on `KNA1`/`LFA1` records, which CVI automatically populates in the same database commit when saving a Business Partner.""",
            },
            {
                "step_id": "d14_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: Dual-Role Partner Rheinland Precision",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "partner": "BP-101 (Rheinland Precision Optics)"
                },
                "content_md": """### Sourcing Sensors While Selling Replacement Components

Rheinland Precision Optics, previously managed in legacy ECC as supplier **`VEND-101`**, is modernized in S/4HANA as central Business Partner **`BP-101`**. 
Under CVI synchronization, `BP-101` links the central identity to both supplier subledger `VEND-101` and customer subledger `CUST-101`:

In S/4HANA:
- **Central Record**: `BUT000` (ID: `BP-101`, Rheinland Precision Optics, Stuttgart).
- **As a Supplier (Legacy VEND-101)**:
  - Role `FLVN00`: Assigned to Company Code `NM01` (Reconciliation G/L `16000000` Accounts Payable).
  - Role `FLVN01`: Assigned to Purchasing Org `PO01` (Currency: EUR, Incoterms: DDP).
- **As a Customer (Subledger CUST-101)**:
  - Role `FLCU00`: Assigned to Company Code `NM01` (Reconciliation G/L `12100000` Accounts Receivable).
  - Role `FLCU01`: Assigned to Sales Org `SO01` (Shipping Point: Heidelberg).

When Rheinland updates its corporate banking details, a single edit in `BP-101` updates both payable disbursements and incoming customer payment matching!""",
            },
            {
                "step_id": "d14_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Interactive Business Partner Role & CVI Cockpit",
                "component_type": "BusinessPartnerMapper",
                "instruction": "Assign required roles (FLVN00 and FLVN01) to partner BP-101 and trigger CVI synchronization to validate underlying table creation.",
            },
            {
                "step_id": "d14_s5_challenge",
                "step_type": "challenge",
                "title": "The Procurement Block Incident",
                "scenario_md": """Nova Manufacturing's procurement team in Heidelberg attempts to create a Purchase Order for optical sensors with vendor Rheinland Precision (BP-101).
The transaction fails with error:
*ME013: Supplier BP-101 not maintained for Purchasing Organization PO01.*

The finance team confirms they can post invoices to BP-101 without issue. What is the root cause?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "The partner only has role FLVN00 (FI Vendor) assigned. Role FLVN01 (Purchasing Supplier) must be added and maintained for Purchasing Org PO01.",
                        "is_correct": True,
                        "explanation": "FLVN00 only maintains financial accounting views; PO creation strictly requires the logistics purchasing role FLVN01."
                    },
                    {
                        "id": "ch_b",
                        "text": "The supplier was blacklisted by the European Central Bank.",
                        "is_correct": False,
                        "explanation": "This is an internal role assignment omission, not an external banking block."
                    },
                    {
                        "id": "ch_c",
                        "text": "The purchasing agent must delete the Business Partner and recreate it in transaction XK01.",
                        "is_correct": False,
                        "explanation": "Transaction XK01 is obsolete in S/4HANA; all maintenance must happen in transaction BP."
                    }
                ]
            },
            {
                "step_id": "d14_s6_assessment",
                "step_type": "assessment",
                "title": "Day 14 Concept Assessment: Business Partner & CVI",
                "questions": [
                    {
                        "id": "d14_q1",
                        "concept_slug": "business-partner-cvi",
                        "prompt": "What is the mandatory transaction in SAP S/4HANA for creating and maintaining customer and supplier master records?",
                        "options": [
                            {"id": "a", "text": "Transaction BP", "is_correct": True},
                            {"id": "b", "text": "Transaction XK01", "is_correct": False},
                            {"id": "c", "text": "Transaction XD01", "is_correct": False}
                        ],
                        "explanation": "Transaction BP is the unified and mandatory transaction for all master data partners in S/4HANA."
                    },
                    {
                        "id": "d14_q2",
                        "concept_slug": "customer-vendor-synchronization",
                        "prompt": "What is the primary function of Customer-Vendor Integration (CVI) in an S/4HANA system?",
                        "options": [
                            {"id": "a", "text": "To synchronize central Business Partner records (BUT000) with legacy customer (KNA1) and vendor (LFA1) tables in real-time", "is_correct": True},
                            {"id": "b", "text": "To send automated WhatsApp messages to customer contacts", "is_correct": False},
                            {"id": "c", "text": "To convert paper checks into cryptocurrency", "is_correct": False}
                        ],
                        "explanation": "CVI bridges the central BP model with underlying legacy customer/vendor tables."
                    }
                ]
            },
            {
                "step_id": "d14_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 14 Skill Evidence Verification",
                "concept_slug": "business-partner-cvi",
                "evidence_rule": "Demonstrated mastery of central Business Partner architecture, CVI synchronization, and multi-role assignments.",
            },
            {
                "step_id": "d14_s8_completion",
                "step_type": "completion",
                "title": "Day 14 Complete: Business Partner & CVI Mastered",
                "summary_md": """### 🤝 Master Data Architecture Validated!

You have mastered the modern S/4HANA partner paradigm:
- Mandatory Business Partner model replacing legacy XK01/XD01 transactions.
- Multi-role extensibility across Financials (`FLVN00`/`FLCU00`) and Logistics (`FLVN01`/`FLCU01`).
- Customer-Vendor Integration (CVI) synchronization mechanics.

**Next Milestone**: Day 15 dives into declarative data modeling—**Core Data Services (CDS) Fundamentals**!""",
                "recommended_mission": {
                    "slug": "nova-business-partner-migration",
                    "title": "Mission: Business Partner Migration",
                    "description": "Migrate and synchronize legacy vendor records into unified Business Partners using CVI Cockpit."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 15: CDS Fundamentals
    # =========================================================================
    15: {
        "day_number": 15,
        "slug": "cds-fundamentals-intro",
        "title": "Core Data Services (CDS) Fundamentals",
        "subtitle": "ABAP Core Data Services, code-to-data pushdown, and view entity architecture",
        "estimated_minutes": 45,
        "atomic_concepts": ["cds-fundamentals", "code-pushdown-philosophy", "view-entity-syntax"],
        "recommended_mission_slug": "nova-cds-reporting-requirement",
        "steps": [
            {
                "step_id": "d15_s1_learn",
                "step_type": "learn",
                "title": "The Evolution to Declarative Data Modeling",
                "content_md": """### Moving Logic Down to the Database

For decades, SAP programming followed the **Data-to-Code** pattern:
1. ABAP programs used `SELECT` statements to drag raw table rows from the database into internal tables on the application server.
2. The application server executed heavy `LOOP AT ... ENDLOOP` statements to calculate sums, filter records, and format currencies.

While acceptable for modest data sets, dragging 5,000,000 lines of `ACDOCA` or `MATDOC` across the local network created immense network bottlenecks and overwhelmed application server memory.

### The Code-to-Data Paradigm
With SAP HANA, the database is vastly more powerful than the application server. **Core Data Services (CDS)** is SAP's declarative, SQL-based data definition language that pushes calculations, aggregations, and business logic directly down into the database engine:
- Only the final calculated result (e.g. 10 aggregated KPI rows) is returned to the application server.
- Built natively into ABAP using modern Eclipse ADT (ABAP Development Tools).""",
                "key_terms": [
                    {"term": "Core Data Services (CDS)", "definition": "An advanced SQL-based declarative data modeling infrastructure pushed down to the database engine."},
                    {"term": "Code Pushdown", "definition": "Executing complex calculations, aggregations, and filtering directly in the HANA database rather than in application server loops."},
                    {"term": "CDS View Entity", "definition": "The modern S/4HANA (2020+) CDS definition that generates no redundant classical DDIC SQL view artifact."}
                ],
            },
            {
                "step_id": "d15_s2_understand",
                "step_type": "understand",
                "title": "CDS View Entities, Annotations, and Associations",
                "content_md": """### Key Architectural Elements of ABAP CDS

1. **View Entities (`define view entity`)**:
   - Unlike legacy classical CDS views (`define view`) that generated a physical DDIC SQL view artifact in transaction `SE11`, modern **View Entities** exist purely in the database catalog with zero activation overhead, strict operand safety, and no classical view restrictions.

2. **Rich Semantic Annotations (`@...`)**:
   - Annotations enrich data models with UI metadata, analytics rules, and access control:
     - `@EndUserText.label`: Translatable human-readable title.
     - `@Analytics.dataCategory: #CUBE`: Designates an analytical data cube with aggregatable measures.
     - `@AccessControl.authorizationCheck: #CHECK`: Enforces CDS Data Control Language (DCL) access rules.
   - *RAP Service Exposure*: In modern S/4HANA (2020+), CDS View Entities are exposed as OData services through the **ABAP RESTful Application Programming Model (RAP)** using a **Service Definition** (`define service`) and **Service Binding** (`OData V4 - UI`), replacing the deprecated `@OData.publish: true` annotation.

3. **Associations vs. SQL Joins**:
   - Classical SQL `JOIN` immediately evaluates all joined tables, consuming memory and compute even if fields from joined tables are never requested.
   - CDS **Associations** define semantic relationships that are evaluated **on-demand (lazy-load)** only when a query explicitly navigates a path expression:
```sql
association [0..1] to I_Customer as _Customer on $projection.Kunnr = _Customer.Customer
```
   - If the consuming client only asks for Sales Order ID and net amount, the customer master table is never read!""",
            },
            {
                "step_id": "d15_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: Real-Time Scrap Rate Analytics View",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "plant": "PL01 (Heidelberg Assembly)"
                },
                "content_md": """### Building the Production KPI Engine

Nova Manufacturing's plant operations director required a real-time monitor showing component scrap rates for robotics controllers (**DXTR-1000**):

Instead of a 600-line ABAP program looping over table `MATDOC`:
- The enterprise developer wrote a CDS View Entity `C_ScrapAnalytics` that executes directly on `MATDOC`.
- It calculates scrap percentages in-memory using `sum(case when bwart = '551' then menge else 0 end)` pushed down to HANA.
- Selective partition filters (`werks = 'PL01'` and fiscal year boundary) are applied in the view to prevent unconstrained table scans and protect OLTP memory.
- The developer exposed the view entity via a RAP Service Definition and published an **OData V4 - UI** Service Binding. It renders on the director's mobile SAP Fiori Launchpad with sub-second response times!""",
            },
            {
                "step_id": "d15_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Interactive CDS View Entity & Code Pushdown Lab",
                "component_type": "CDSConceptMapper",
                "instruction": "Explore the three tiers of the Virtual Data Model (Basic, Composite, Consumption) and contrast code pushdown performance with legacy application loops.",
            },
            {
                "step_id": "d15_s5_challenge",
                "step_type": "challenge",
                "title": "The Legacy Query Refactoring Challenge",
                "scenario_md": """A developer at Nova Manufacturing has written a report that performs a SELECT on 1,500,000 ACDOCA records and loops through them in ABAP memory to calculate total revenue per product group.
The report takes 4 minutes to run and occasionally causes memory dump TSV_TNEW_PAGE_ALLOC_FAILED.

What is the recommended modern S/4HANA refactoring approach?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "Increase the server physical RAM quota in transaction RZ11 and keep the ABAP loop logic unchanged.",
                        "is_correct": False,
                        "explanation": "Expanding application server memory quotas masks the underlying architectural anti-pattern and does not eliminate heavy network data transfer."
                    },
                    {
                        "id": "ch_b",
                        "text": "Refactor the logic into a CDS View Entity with code pushdown aggregation (SUM, GROUP BY) on ACDOCA, returning only the small summarized result set.",
                        "is_correct": True,
                        "explanation": "Code pushdown executes aggregations directly in HANA in-memory engines and transmits only the final summarized KPI records across the network."
                    },
                    {
                        "id": "ch_c",
                        "text": "Create classical secondary database indexes on ACDOCA and export raw line items to an external flat file via nightly batch.",
                        "is_correct": False,
                        "explanation": "Adding custom indexes to ACDOCA increases write overhead and fails to deliver real-time operational reporting."
                    }
                ]
            },
            {
                "step_id": "d15_s6_assessment",
                "step_type": "assessment",
                "title": "Day 15 Concept Assessment: CDS Fundamentals & Code Pushdown",
                "questions": [
                    {
                        "id": "d15_q1",
                        "concept_slug": "code-pushdown-philosophy",
                        "prompt": "What is the core principle of the 'Code-to-Data' pushdown paradigm in SAP S/4HANA?",
                        "options": [
                            {"id": "a", "text": "Extracting raw table line items into ABAP internal tables and executing nested LOOP AT statements on the application server", "is_correct": False},
                            {"id": "b", "text": "Pushing data-intensive logic, calculations, and aggregations down to the database engine so only final results cross the network", "is_correct": True},
                            {"id": "c", "text": "Replicating database tables via ETL batches into external spreadsheet files for desktop computation", "is_correct": False}
                        ],
                        "explanation": "Code pushdown executes aggregations and filtering at the database layer in HANA RAM, returning only distilled results."
                    },
                    {
                        "id": "d15_q2",
                        "concept_slug": "view-entity-syntax",
                        "prompt": "What is a major advantage of CDS View Entities compared to traditional SQL joins?",
                        "options": [
                            {"id": "a", "text": "CDS Associations load joined data lazily on-demand only when specific path expressions are requested", "is_correct": True},
                            {"id": "b", "text": "CDS View Entities evaluate all related tables simultaneously in memory regardless of field selection", "is_correct": False},
                            {"id": "c", "text": "CDS View Entities generate a classical DDIC SQL view artifact in SE11 for backward compatibility", "is_correct": False}
                        ],
                        "explanation": "Associations provide on-demand lazy evaluation, preventing unnecessary database joins when related attributes are omitted from queries."
                    }
                ]
            },
            {
                "step_id": "d15_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 15 Skill Evidence Verification",
                "concept_slug": "cds-fundamentals",
                "evidence_rule": "Demonstrated mastery of ABAP Core Data Services, code pushdown architecture, and CDS View Entity syntax.",
            },
            {
                "step_id": "d15_s8_completion",
                "step_type": "completion",
                "title": "Day 15 Complete: CDS Fundamentals Mastered",
                "summary_md": """### 📊 Declarative Data Modeling Mastered!

You have acquired foundational proficiency in ABAP CDS:
- The code-to-data pushdown philosophy eliminating application memory dumps.
- Modern CDS View Entity architecture and semantic annotations.
- On-demand path expressions and lazy-loaded associations.

**Next Milestone**: Day 16 covers enterprise landscape governance—**DEV / QAS / PRD Landscapes & Transport Management**!""",
                "recommended_mission": {
                    "slug": "nova-cds-reporting-requirement",
                    "title": "Mission: CDS Reporting Requirement",
                    "description": "Design and validate an operational reporting model using Core Data Services for Nova Manufacturing."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 16: DEV / QAS / PRD Landscapes
    # =========================================================================
    16: {
        "day_number": 16,
        "slug": "system-landscapes-dev-qas-prd",
        "title": "DEV / QAS / PRD Landscape Architecture",
        "subtitle": "Three-system landscape governance, CTS transport requests, and release management",
        "estimated_minutes": 45,
        "atomic_concepts": ["transport-management-cts", "system-landscapes-3tier"],
        "recommended_mission_slug": "nova-landscape-change-request",
        "steps": [
            {
                "step_id": "d16_s1_learn",
                "step_type": "learn",
                "title": "The Enterprise Three-System Landscape",
                "content_md": """### Why Enterprise ERP Requires Physical Landscape Separation

No serious enterprise permits modifying production configuration or source code directly in the live operating system. A single erroneous configuration change in fiscal year variants or account determination could immediately halt invoicing, block shipments, or corrupt general ledger balances.

### The Classic 3-System Landscape
SAP mandates a minimum three-system landscape:
1. **DEV (Development System)**:
   - Where functional consultants configure business scope and developers write code.
   - Divided into dedicated clients:
     - **Client 100 (Golden Customizing)**: Clean client for business configuration only. Zero master data or transactional testing is executed here.
     - **Client 110 (ABAP Development / Workbench)**: Client where developers create and test ABAP classes, CDS views, and repository objects.
     - **Client 120 (Unit Test)**: Target client where customizing from Client 100 is copied locally via transaction `SCC1` / `SCC1N` for functional unit testing with sample master data.
2. **QAS (Quality Assurance System)**:
   - A mirror of production with realistic business transactional and master data.
   - Used for User Acceptance Testing (UAT), integration testing, authorization verification, and performance cutover rehearsals.
3. **PRD (Production System)**:
   - The live commercial environment executing active company operations.
   - System settings strictly prohibit direct configuration (`SCC4` client setting set to *No Changes Allowed* and `SE06` system change option locked).""",
                "key_terms": [
                    {"term": "Change and Transport System (CTS)", "definition": "The SAP infrastructure that tracks configuration and code changes and moves them safely between landscape systems."},
                    {"term": "Transport Request (TR)", "definition": "A packaged container with a unique ID (e.g. DEVK900142) recording changed repository objects or customizing entries."},
                    {"term": "STMS", "definition": "System Transport Management System: The central administrative transaction for managing transport routes and import queues."}
                ],
            },
            {
                "step_id": "d16_s2_understand",
                "step_type": "understand",
                "title": "Transport Lifecycle: Customizing vs. Workbench & Overtaking",
                "content_md": """### Types of Transport Requests

1. **Customizing Request (Client-Dependent)**:
   - Records business settings (e.g. creating Storage Location `RAW1`, payment terms, tax codes).
   - Only affects the specific client in which it is imported.
2. **Workbench Request (Client-Independent)**:
   - Records repository code changes (ABAP classes, CDS View Entities, dictionary tables) and cross-client customizing entries (e.g. factory calendar `TFACS`).
   - Automatically affects all clients across the target system upon import.

### The Transport Lifecycle
$$\\text{Create Task} \\rightarrow \\text{Release Task} \\rightarrow \\text{Release Transport Request} \\rightarrow \\text{Import to QAS} \\rightarrow \\text{UAT Approval} \\rightarrow \\text{Import to PRD}$$

### The Critical Overtaking Hazard
If Developer A creates a base Interface CDS View Entity `ZI_SalesOrderItem` in Transport 1, and Developer B builds a Consumption CDS View Entity `ZC_SalesOrderCube` in Transport 2 that references `ZI_SalesOrderItem`:
- If Transport 2 is imported into PRD before Transport 1, the import crashes with syntax and activation errors because the underlying interface view entity does not yet exist in PRD!
- Landscape governance strictly enforces sequential transport queue order to prevent **overtaking**.""",
            },
            {
                "step_id": "d16_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: Commissioning Austin Storage Location FG02",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "route": "DEV (Client 100) -> QAS (Client 200) -> PRD (Client 300)"
                },
                "content_md": """### Promoting a Logistical Change Across the Landscape

To prepare for high-volume finished goods shipping at the Austin Tech Center (**PL02**), Nova Manufacturing needed to configure Storage Location **FG02** (Robotics Buffer):

1. **In DEV (Client 100)**: The functional consultant configured FG02 under Plant PL02. Changes were saved into Customizing Request **DEVK900142**.
2. **Local Test Copy in DEV (Client 120)**: The consultant used transaction `SCC1` to copy DEVK900142 into unit test client 120, verifying material assignments before release.
3. **Release in DEV**: Individual tasks were released, followed by the main transport request, packaging data files into the operating system transport directory (`/usr/sap/trans/data` and `cofiles`).
4. **Import to QAS (Client 200)**: Basis administrators triggered import via transaction `STMS`. The Austin warehouse lead executed a test goods receipt confirming inventory landed in FG02.
5. **Production Deployment (PRD Client 300)**: With business sign-off, the change was imported during the Friday night release window. Zero disruption occurred to Heidelberg live manufacturing!""",
            },
            {
                "step_id": "d16_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Interactive 3-System Landscape & Transport Flow",
                "component_type": "LandscapeFlow",
                "instruction": "Follow Transport Request DEVK900142 through DEV, QAS, and PRD. Validate transport prerequisites and prevent production governance violations.",
            },
            {
                "step_id": "d16_s5_challenge",
                "step_type": "challenge",
                "title": "The Emergency Hotfix In Production Dilemma",
                "scenario_md": """A critical customer invoice posting in Production (PRD) fails due to an erroneous account determination rule.
The plant manager demands:
*"Open Production Client 300 immediately so we can fix the configuration table in PRD directly and save 2 hours!"*

How must the SAP Release Governance Lead respond?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "Agree and open PRD Client 300 using transaction SCC4 to allow direct edits in the live environment.",
                        "is_correct": False,
                        "explanation": "Direct changes in PRD violate corporate governance, bypass audit tracking, and lead to landscape divergence where DEV and PRD no longer match."
                    },
                    {
                        "id": "ch_b",
                        "text": "Refuse direct PRD modification. Maintain the fix in DEV, release an emergency transport request, test in QAS, and import via STMS.",
                        "is_correct": True,
                        "explanation": "Emergency fixes must always travel through the audited transport pipeline to prevent regression and landscape divergence."
                    },
                    {
                        "id": "ch_c",
                        "text": "Perform an unverified client copy of the entire QAS database directly over PRD during operating hours.",
                        "is_correct": False,
                        "explanation": "Overwriting production with test data would destroy live financial and transactional records."
                    }
                ]
            },
            {
                "step_id": "d16_s6_assessment",
                "step_type": "assessment",
                "title": "Day 16 Concept Assessment: Landscapes & Transport Management",
                "questions": [
                    {
                        "id": "d16_q1",
                        "concept_slug": "transport-management-cts",
                        "prompt": "What is the key difference between a Customizing Transport Request and a Workbench Transport Request?",
                        "options": [
                            {"id": "a", "text": "Customizing requests record client-dependent business configurations, while Workbench requests record client-independent repository code and data structures", "is_correct": True},
                            {"id": "b", "text": "Customizing requests modify database schemas permanently, while Workbench requests only modify temporary memory caches", "is_correct": False},
                            {"id": "c", "text": "Customizing requests apply across all systems simultaneously, while Workbench requests cannot be transported", "is_correct": False}
                        ],
                        "explanation": "Customizing is client-specific; Workbench repository objects apply system-wide across all clients."
                    },
                    {
                        "id": "d16_q2",
                        "concept_slug": "system-landscapes-3tier",
                        "prompt": "Why is direct configuration in the Production (PRD) system strictly disabled in enterprise governance?",
                        "options": [
                            {"id": "a", "text": "Because PRD database instances operate in read-only mode and do not support INSERT statements", "is_correct": False},
                            {"id": "b", "text": "To prevent untested changes from halting live operations and to maintain strict auditability via transport request lineage", "is_correct": True},
                            {"id": "c", "text": "Because SAP license keys expire whenever transaction SCC4 is accessed in a production system", "is_correct": False}
                        ],
                        "explanation": "Disabling direct edits guarantees audit integrity and prevents live operational crashes."
                    }
                ]
            },
            {
                "step_id": "d16_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 16 Skill Evidence Verification",
                "concept_slug": "transport-management-cts",
                "evidence_rule": "Demonstrated mastery of 3-system landscape architecture, CTS transport lifecycles, and release governance.",
            },
            {
                "step_id": "d16_s8_completion",
                "step_type": "completion",
                "title": "Day 16 Complete: System Landscapes Mastered",
                "summary_md": """### 🏛️ System Landscape Governance Validated!

You possess certified knowledge of enterprise landscape operations:
- The 3-system separation (DEV $\\to$ QAS $\\to$ PRD).
- Customizing vs. Workbench transport request mechanics.
- Transport sequence integrity and emergency change governance.

**Next Milestone**: Day 17 explores modern cloud delivery—**Cloud Implementation Landscapes & Central Business Configuration (CBC)**!""",
                "recommended_mission": {
                    "slug": "nova-landscape-change-request",
                    "title": "Mission: Landscape Change Request",
                    "description": "Formulate a transport route and guide a mission-critical change request through DEV, QAS, and PRD."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 17: Cloud Implementation Landscapes
    # =========================================================================
    17: {
        "day_number": 17,
        "slug": "cloud-implementation-landscapes",
        "title": "Cloud Implementation Landscapes & CBC",
        "subtitle": "Central Business Configuration (CBC), 2-system vs 3-system cloud landscapes, and provisioning",
        "estimated_minutes": 45,
        "atomic_concepts": ["central-business-configuration", "cloud-3-system-landscape"],
        "recommended_mission_slug": "nova-landscape-change-request",
        "steps": [
            {
                "step_id": "d17_s1_learn",
                "step_type": "learn",
                "title": "Modern Cloud Deployment Architecture",
                "content_md": """### From On-Premise IMG to Central Business Configuration

In classical on-premise and Private Cloud SAP implementations, consultants logged into transaction `SPRO` (SAP Reference Implementation Guide) to configure thousands of parameters directly within the development system.

In **SAP S/4HANA Cloud Public Edition**:
- Scoping and business configuration are orchestrated outside the ERP runtime using **SAP Central Business Configuration (CBC)**.
- CBC provides a centralized, guided SaaS cockpit where project teams define enterprise scope, activate SAP Best Practices scope items, and model organizational structures visually.
- Once completed in CBC, configuration is automatically deployed into the Public Cloud landscape systems via automated APIs.

*Architectural Distinction*: **S/4HANA Cloud Private Edition** and **On-Premise** deployments do **not** use CBC; they retain full access to the traditional `SPRO` Implementation Guide and standard CTS/STMS transport routes.""",
                "key_terms": [
                    {"term": "SAP Central Business Configuration (CBC)", "definition": "The central SaaS cockpit used to configure business processes and enterprise structure across S/4HANA Cloud Public Edition landscapes."},
                    {"term": "Cloud 3-System Landscape (3SL)", "definition": "Modern cloud architecture comprising Development System, Test System, and Production System with automated deployment pipelines."},
                    {"term": "Scope Bundle", "definition": "A pre-packaged set of standardized end-to-end business processes (e.g. Baseline Scope) activated via CBC."}
                ],
            },
            {
                "step_id": "d17_s2_understand",
                "step_type": "understand",
                "title": "2-System vs. 3-System Cloud Landscapes (2SL vs. 3SL)",
                "content_md": """### The Evolution of Cloud Landscapes

1. **Legacy 2-System Landscape (2SL - Deprecated)**:
   - Consisted of only **Quality (QAS)** and **Production (PRD)**.
   - Limited strictly to Key-User (No-Code/Low-Code) extensibility. Custom ABAP code was disallowed.
2. **Modern 3-System Landscape (3SL - Standard)**:
   - **Development System (DEV)**:
     - **Client 080 (Development Tenant)**: Where developers build custom ABAP Cloud objects, CDS view entities, and RAP business services using Eclipse ADT.
     - **Client 100 (Customizing Tenant)**: Where CBC configuration is received and key-user business settings are maintained.
   - **Test System (TEST)**: Validates configuration and custom code against semi-annual cloud upgrades (e.g. 2402, 2408) using realistic business data.
   - **Production System (PRD)**: Live productive operations.

### Software Transport in the Cloud
Instead of classic GUI transaction `STMS`:
- Key-user changes are transported using the **Export Software Collection** and **Import Collection** SAP Fiori apps.
- ABAP Cloud repository objects are version-controlled and deployed using **git-enabled CTS (gCTS)** and Manage Software Components!""",
            },
            {
                "step_id": "d17_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: Cloud Scoping for Austin Tech Center (PL02)",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "cloud_project": "Austin Expansion 3SL Project"
                },
                "content_md": """### Scoping in SAP Central Business Configuration (CBC)

When planning a cloud-first expansion for the Austin Tech Center (**PL02**), Nova Manufacturing evaluated S/4HANA Cloud Public Edition:

1. **CBC Project Scoping**: In the CBC portal, the project lead activated Scope Items `BD9` (Sell from Stock) and `J45` (Procurement of Direct Materials).
2. **Organizational Definition**: Plant `PL02` and Storage Location `RAW1` were defined visually in CBC's Org Structure app and assigned to Company Code `NM01`.
3. **Automated Deployment**: CBC validated structural consistency and automatically provisioned the configuration into the Development System (DEV Client 100) tenant.
4. **Developer Extensibility**: The development team logged into DEV Client 080 in Eclipse ADT to build custom CDS View Entities using ABAP Cloud, complying 100% with Clean Core governance!""",
            },
            {
                "step_id": "d17_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Interactive Cloud Landscape & Transport Pipeline",
                "component_type": "LandscapeFlow",
                "instruction": "Inspect cloud release governance and understand how CBC scope definitions deploy across a modern 3-System Cloud Landscape (DEV-TEST-PRD).",
            },
            {
                "step_id": "d17_s5_challenge",
                "step_type": "challenge",
                "title": "The Cloud Extensibility Governance Challenge",
                "scenario_md": """A developer on the Nova Manufacturing cloud expansion project wants to modify a core SAP standard database table directly using classical ABAP in S/4HANA Cloud 3SL.
The development lead rejects the transport.

What is the governing architectural principle?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "Clean Core: S/4HANA Cloud restricts developer extensibility to released APIs and objects. Direct modifications to SAP core tables are technically prohibited to ensure seamless automated cloud upgrades.",
                        "is_correct": True,
                        "explanation": "Cloud 3SL enforces restricted ABAP Cloud; only released APIs and extension points can be used."
                    },
                    {
                        "id": "ch_b",
                        "text": "The developer should bypass the transport pipeline and execute an SQL ALTER TABLE command directly via database administrator console in PRD.",
                        "is_correct": False,
                        "explanation": "Direct DDL commands in cloud databases are strictly blocked by cloud security and destroy upgrade stability."
                    },
                    {
                        "id": "ch_c",
                        "text": "Standard table modifications are allowed only if wrapped inside legacy unmanaged BAPIs from R/3.",
                        "is_correct": False,
                        "explanation": "Unreleased legacy BAPIs are not supported in ABAP Cloud."
                    }
                ]
            },
            {
                "step_id": "d17_s6_assessment",
                "step_type": "assessment",
                "title": "Day 17 Concept Assessment: Cloud Landscapes & CBC",
                "questions": [
                    {
                        "id": "d17_q1",
                        "concept_slug": "central-business-configuration",
                        "prompt": "What is the primary role of SAP Central Business Configuration (CBC) in S/4HANA Cloud implementations?",
                        "options": [
                            {"id": "a", "text": "A low-level ABAP debugger used to set execution breakpoints on background RFC jobs", "is_correct": False},
                            {"id": "b", "text": "The central SaaS application used to select business scope, define organizational structures, and deploy configurations across S/4HANA Cloud Public Edition systems", "is_correct": True},
                            {"id": "c", "text": "An external ETL tool used to copy operational transactional data into third-party relational data marts", "is_correct": False}
                        ],
                        "explanation": "CBC manages business scoping, Best Practice activation, and automated configuration deployment across cloud systems."
                    },
                    {
                        "id": "d17_q2",
                        "concept_slug": "cloud-3-system-landscape",
                        "prompt": "What key capability does a Cloud 3-System Landscape (3SL) provide that was missing in the legacy Cloud 2-System Landscape (2SL)?",
                        "options": [
                            {"id": "a", "text": "Developer Extensibility using ABAP Cloud in Eclipse ADT with released SAP APIs and dedicated development tenants", "is_correct": True},
                            {"id": "b", "text": "Unrestricted direct modifications to standard SAP table definitions in transaction SE11", "is_correct": False},
                            {"id": "c", "text": "Elimination of Quality Assurance testing so changes deploy directly from development into production", "is_correct": False}
                        ],
                        "explanation": "Cloud 3SL introduced full developer extensibility via ABAP Cloud alongside key-user extensibility."
                    }
                ]
            },
            {
                "step_id": "d17_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 17 Skill Evidence Verification",
                "concept_slug": "central-business-configuration",
                "evidence_rule": "Demonstrated understanding of Central Business Configuration, Cloud 3SL architecture, and Clean Core extensibility.",
            },
            {
                "step_id": "d17_s8_completion",
                "step_type": "completion",
                "title": "Day 17 Complete: Cloud Landscapes Mastered",
                "summary_md": """### ☁️ Cloud Implementation Validated!

You have mastered modern SAP cloud delivery architecture:
- Central Business Configuration (CBC) for scope and org structure deployment.
- The Cloud 3-System Landscape (DEV-TEST-PRD).
- Clean Core Developer Extensibility using released APIs.

**Next Milestone**: Day 18 tackles enterprise security—**Identity & Access Governance in S/4HANA**!""",
                "recommended_mission": {
                    "slug": "nova-landscape-change-request",
                    "title": "Mission: Landscape Change Request",
                    "description": "Evaluate cloud release transport routes and enforce governance rules across landscapes."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 18: Identity & Access Governance
    # =========================================================================
    18: {
        "day_number": 18,
        "slug": "identity-access-governance",
        "title": "Identity & Access Governance in S/4HANA",
        "subtitle": "PFCG authorization roles, catalogs, spaces, pages, and segregation of duties",
        "estimated_minutes": 45,
        "atomic_concepts": ["identity-access-management", "pfcg-authorizations", "fiori-role-assignment"],
        "recommended_mission_slug": "nova-access-governance-incident",
        "steps": [
            {
                "step_id": "d18_s1_learn",
                "step_type": "learn",
                "title": "Role-Based Access Control in S/4HANA",
                "content_md": """### Securing the Digital Enterprise

In modern ERP systems, security is not merely about logging into a server. It is about enforcing the **Principle of Least Privilege**: ensuring that every employee has access to exactly the data and business functions required for their job role—and nothing more.

### The Modern S/4HANA Access Hierarchy
S/4HANA connects classical backend authorization checks with the modern SAP Fiori Launchpad frontend:

1. **Business User**: The identity representing the employee (e.g. `ANNA.MULLER` maintained in transaction `SU01` or *Maintain Business Users* app).
2. **Business Role (PFCG)**: Standard single role templates delivered by SAP (e.g. `SAP_BR_PURCHASER`, `SAP_BR_AP_ACCOUNTANT`) or custom enterprise single roles (`Z_BR_*`) assigned to users.
3. **Business Spaces & Pages**: The modern visual layout on the Fiori Launchpad organizing applications into role-based workspaces and intuitive task sections.
4. **Business Catalogs**: The technical bundles containing specific apps, target mappings, and semantic objects (e.g. `SAP_MM_BC_PO_PROCESS_PC`).
5. **Authorization Objects**: The low-level ABAP kernel authorization checks (e.g. `M_BEST_WRK` for plant-specific purchase order activities, `F_REGU_BUK` for company code payment execution).""",
                "key_terms": [
                    {"term": "Role-Based Access Control (RBAC)", "definition": "A security model where access permissions are granted to job roles rather than to individual users."},
                    {"term": "Segregation of Duties (SoD)", "definition": "An internal control policy ensuring that critical conflicting tasks cannot be executed by the same individual (e.g. creating POs and paying vendors)."},
                    {"term": "Business Space & Page", "definition": "The modern SAP Fiori Launchpad layout paradigm organizing applications into role-based workspaces."}
                ],
            },
            {
                "step_id": "d18_s2_understand",
                "step_type": "understand",
                "title": "Segregation of Duties (SoD) & Audit Compliance",
                "content_md": """### The Threat of Toxic Role Combinations

A **Segregation of Duties (SoD) Conflict** occurs when a single user possesses two authorization profiles that bypass internal fraud controls.

### Classic Enterprise SoD Anti-Patterns:
1. **Procurement Fraud**:
   - `SAP_BR_PURCHASER` (Creates Purchase Orders) + `SAP_BR_AP_ACCOUNTANT` (Releases Vendor Payments).
   - *Risk*: A rogue employee could create a fictitious purchase order to a colluding vendor and immediately execute the electronic wire transfer (`F110` / `F_REGU_BUK`) to personal accounts.
2. **Inventory Theft**:
   - `SAP_BR_WAREHOUSE_CLERK` (Posts Goods Receipts) + `SAP_BR_INVENTORY_MANAGER` (Executes Physical Inventory Write-Offs).
   - *Risk*: An employee could divert physical components and write off the missing inventory as "scrap" without independent oversight.

### Resolving SoD Conflicts
Security administrators utilize **SAP Access Governance** and PFCG role redesign to identify conflicting business catalogs and split operational authorities across distinct individuals.""",
            },
            {
                "step_id": "d18_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: The Accounts Payable Audit Finding",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "user": "ANNA.MULLER (Plant PL01 Logistics Lead)"
                },
                "content_md": """### The Internal Audit Exception

During an external compliance audit of Nova Manufacturing Heidelberg (**NM01**), auditors flagged an immediate high-risk exception:

- Logistics specialist Anna Muller held role `SAP_BR_PURCHASER` to issue purchase orders for laser sensors (**RAW-01**).
- During a vacation coverage emergency, Anna was also assigned role `SAP_BR_AP_ACCOUNTANT`, granting payment catalog `SAP_FIN_BC_AP_PAYMENTS_PC` and authorization object `F_REGU_BUK`.
- **The Violation**: Anna held end-to-end authority to order materials and release disbursements to Rheinland Precision Optics (**VEND-101**).

The security lead resolved the audit finding by revoking role `SAP_BR_AP_ACCOUNTANT` from Anna's user profile and assigning the restricted role `SAP_BR_AP_CLERK_INVOICES`. This role grants invoice verification (`SAP_FIN_BC_AP_INVOICES_PC`) while strictly withholding payment run authorization (`F_REGU_BUK`), restoring dual-control governance.""",
            },
            {
                "step_id": "d18_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Interactive Fiori Role Architecture & SoD Remediation",
                "component_type": "AccessRoleMapper",
                "instruction": "Inspect business roles, assigned spaces, and catalogs. Resolve the toxic Segregation of Duties conflict on Anna Muller's account.",
            },
            {
                "step_id": "d18_s5_challenge",
                "step_type": "challenge",
                "title": "The Missing Tile Troubleshooting Challenge",
                "scenario_md": """A newly hired purchasing specialist in Austin (PL02) complains:
*"I was assigned role SAP_BR_PURCHASER, and I can see the Purchasing Space on my Fiori Launchpad. However, the 'Manage Purchase Orders' tile is completely missing!"*

What is the root cause and remediation?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "The business role is missing Business Catalog SAP_MM_BC_PO_PROCESS_PC, or the catalog is not assigned to the active Page layout.",
                        "is_correct": True,
                        "explanation": "Tiles only render when their underlying Business Catalog is both authorized in the PFCG role and assigned to a Page."
                    },
                    {
                        "id": "ch_b",
                        "text": "The user must clear their browser cookies and request SAP BASIS to restart the production database server.",
                        "is_correct": False,
                        "explanation": "Database restarts do not remediate missing Fiori catalog and page layout assignments."
                    },
                    {
                        "id": "ch_c",
                        "text": "The user must be assigned SAP_ALL composite profile to grant full system authorizations.",
                        "is_correct": False,
                        "explanation": "Assigning SAP_ALL is a catastrophic security violation that breaks all corporate compliance."
                    }
                ]
            },
            {
                "step_id": "d18_s6_assessment",
                "step_type": "assessment",
                "title": "Day 18 Concept Assessment: Identity & Access Governance",
                "questions": [
                    {
                        "id": "d18_q1",
                        "concept_slug": "identity-access-management",
                        "prompt": "What is the primary risk of allowing a single employee to hold both purchasing order creation and vendor payment release authorities?",
                        "options": [
                            {"id": "a", "text": "It causes high network latency during batch payment file transfers", "is_correct": False},
                            {"id": "b", "text": "It violates Segregation of Duties (SoD) by enabling unauthorized disbursements without independent dual-control verification", "is_correct": True},
                            {"id": "c", "text": "It locks the material valuation table MBEW during fiscal year closing", "is_correct": False}
                        ],
                        "explanation": "SoD prevents fraud by requiring separate individuals to order and disburse funds."
                    },
                    {
                        "id": "d18_q2",
                        "concept_slug": "fiori-role-assignment",
                        "prompt": "In the SAP Fiori Launchpad architecture, what component directly bundles applications, semantic target mappings, and authorization objects for assignment to PFCG roles?",
                        "options": [
                            {"id": "a", "text": "Fiori Theme Designer", "is_correct": False},
                            {"id": "b", "text": "Business Catalog", "is_correct": True},
                            {"id": "c", "text": "Local Browser Bookmark", "is_correct": False}
                        ],
                        "explanation": "Business Catalogs contain the technical tiles, target mappings, and authorization objects."
                    }
                ]
            },
            {
                "step_id": "d18_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 18 Skill Evidence Verification",
                "concept_slug": "identity-access-management",
                "evidence_rule": "Demonstrated mastery of S/4HANA role-based access control, Fiori catalogs/spaces, and Segregation of Duties.",
            },
            {
                "step_id": "d18_s8_completion",
                "step_type": "completion",
                "title": "Day 18 Complete: Identity & Access Governance Mastered",
                "summary_md": """### 🛡️ Enterprise Security Validated!

You have mastered the principles of S/4HANA access governance:
- Role-Based Access Control (RBAC) linking PFCG roles to Fiori Launchpads.
- Separation of Business Spaces, Pages, and technical Business Catalogs.
- Prevention and remediation of critical Segregation of Duties (SoD) conflicts.

**Next Milestone**: Day 19 explores real-time reporting—**Embedded Analytics Architecture**!""",
                "recommended_mission": {
                    "slug": "nova-access-governance-incident",
                    "title": "Mission: Access Governance Incident",
                    "description": "Audit user permissions, detect toxic authorization combinations, and resolve Segregation of Duties violations."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 19: Embedded Analytics
    # =========================================================================
    19: {
        "day_number": 19,
        "slug": "embedded-analytics-foundations",
        "title": "Embedded Analytics Architecture",
        "subtitle": "Operational reporting directly on transactional tables without ETL or separate data warehouses",
        "estimated_minutes": 45,
        "atomic_concepts": ["embedded-analytics-foundations", "operational-reporting-vdm"],
        "recommended_mission_slug": "nova-cds-reporting-requirement",
        "steps": [
            {
                "step_id": "d19_s1_learn",
                "step_type": "learn",
                "title": "The End of Operational ETL Pipelines",
                "content_md": """### The Latency of Traditional Data Warehouses

In classical enterprise architectures, transactional systems (OLTP) and analytical reporting systems (OLAP) were strictly segregated:
1. Business users executed day-to-day transactions in SAP ECC.
2. Every night, heavy ETL (Extract, Transform, Load) batch jobs extracted millions of records across the network into a separate data warehouse (e.g. SAP BW or Snowflake).
3. Executives could only analyze data that was **24 hours old**. If inventory ran out at 10:00 AM, the reporting dashboard remained blissfully unaware until the following morning.

### S/4HANA Embedded Analytics
Because SAP HANA stores transactional data in columnar in-memory RAM, S/4HANA achieves **Hybrid Transactional/Analytical Processing (HTAP)**:
- Operational reporting runs directly on live transactional tables (`ACDOCA`, `MATDOC`, `VBAK`).
- Zero data replication, zero ETL pipelines, and zero reporting latency!""",
                "key_terms": [
                    {"term": "Embedded Analytics", "definition": "Real-time reporting tools and analytical CDS views built directly into the S/4HANA transactional core."},
                    {"term": "Virtual Data Model (VDM)", "definition": "The structured hierarchy of CDS views providing consistent semantic access across all SAP modules."},
                    {"term": "Smart Business KPI", "definition": "A dynamic SAP Fiori tile displaying live metric thresholds (e.g. Days Sales Outstanding) with color-coded status."}
                ],
            },
            {
                "step_id": "d19_s2_understand",
                "step_type": "understand",
                "title": "Operational vs. Strategic Analytics & The VDM Hierarchy",
                "content_md": """### When to Use Embedded Analytics vs. Enterprise Data Warehousing

| Characteristic | Embedded Analytics (S/4HANA) | Enterprise Data Warehouse (SAP Datasphere / BW/4HANA) |
|---|---|---|
| Latency | **0 seconds (Real-Time)** | Minutes to hours (Batch/Replication/Federation) |
| Data Scope | Live S/4HANA transactional tables (`ACDOCA`, `MATDOC`) | Cross-enterprise (CRM, non-SAP, historical 10-year data) |
| Target Audience | Operational Managers, Plant Supervisors, Billing Clerks | Board of Directors, Strategic Planners, Data Scientists |
| Primary Tool | SAP Fiori Elements, Smart Business KPIs, SAC Live Connection | SAP Analytics Cloud (SAC), Snowflake, Power BI, Databricks |

### The Virtual Data Model (VDM) Hierarchy
1. **Basic / Interface Views (`P_` / `I_`)**:
   - `P_` (Private Views): Internal building blocks designed for single-purpose use, not released for customer extension.
   - `I_` (Interface Views): Public, stable core dimension and entity views (e.g. `I_Customer`, `I_Product`, `I_SalesOrder`).
2. **Composite Views (`I_`)**:
   - Combine multiple interface views with business logic and associations.
   - Annotated with `@Analytics.dataCategory: #CUBE` to define dimensions and aggregatable numeric measures (`@Aggregation.default: #SUM`).
3. **Consumption Views (`C_`)**:
   - Analytical queries annotated with `@Analytics.query: true`. Consumed directly by Fiori multidimensional reporting engines and SAC live connections via the InA (Information Access) analytical protocol.""",
            },
            {
                "step_id": "d19_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: Real-Time Plant PL01 Margin Dashboard",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "plant": "PL01 (Heidelberg Assembly)"
                },
                "content_md": """### Real-Time Margin Tracking for DXTR-1000

Nova Manufacturing's VP of Manufacturing monitors contribution margins across high-precision robotics controllers (**DXTR-1000**):

- In legacy ECC, calculating actual gross margins required waiting until post-month variance settlement.
- In S/4HANA Embedded Analytics, a Fiori KPI tile *"Live Production Margin"* evaluates table `ACDOCA` directly.
- The moment warehouse operators post goods issue for raw components, actual component cost is compared against sales order pricing in real-time.
- When optical sensor acquisition costs from Rheinland Precision (**VEND-101**) fluctuated by 4%, the Fiori KPI tile turned from Green to Yellow instantaneously on the VP's tablet!""",
            },
            {
                "step_id": "d19_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Interactive VDM & Embedded Analytics Lab",
                "component_type": "CDSConceptMapper",
                "instruction": "Examine how Consumption Views (C_ Views) format live transactional data for Fiori Smart Business KPIs and Multidimensional Analysis.",
            },
            {
                "step_id": "d19_s5_challenge",
                "step_type": "challenge",
                "title": "The Analytics Architecture Decision",
                "scenario_md": """Nova Manufacturing's sales director wants a real-time mobile dashboard showing overdue customer orders.
The IT project manager proposes building an ETL pipeline to replicate all sales tables every hour into an external MySQL database.

How should the Enterprise Architect evaluate this proposal?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "Approve the external MySQL pipeline because transactional ERP databases should never process analytical queries.",
                        "is_correct": False,
                        "explanation": "HANA was engineered specifically for Hybrid Transactional/Analytical Processing (HTAP), eliminating the need for operational sidecar databases."
                    },
                    {
                        "id": "ch_b",
                        "text": "Reject the external ETL pipeline. Deploy a standard S/4HANA Fiori Analytical App built on standard VDM Consumption views directly on live transactional data.",
                        "is_correct": True,
                        "explanation": "Embedded Analytics provides zero-latency operational reporting without redundant ETL pipelines or external database licenses."
                    },
                    {
                        "id": "ch_c",
                        "text": "Write a custom ABAP report scheduled as a 5-minute background job that appends flat CSV files to an FTP share.",
                        "is_correct": False,
                        "explanation": "Frequent background export jobs introduce severe file I/O overhead and fail to provide interactive drilldown analytics."
                    }
                ]
            },
            {
                "step_id": "d19_s6_assessment",
                "step_type": "assessment",
                "title": "Day 19 Concept Assessment: Embedded Analytics Architecture",
                "questions": [
                    {
                        "id": "d19_q1",
                        "concept_slug": "embedded-analytics-foundations",
                        "prompt": "What is the primary operational benefit of S/4HANA Embedded Analytics compared to traditional data warehousing?",
                        "options": [
                            {"id": "a", "text": "It executes directly on live transactional database tables without data replication or batch ETL latency", "is_correct": True},
                            {"id": "b", "text": "It replaces all primary database tables with flat external CSV files", "is_correct": False},
                            {"id": "c", "text": "It eliminates the need for user authorization and access control checks", "is_correct": False}
                        ],
                        "explanation": "Embedded Analytics eliminates ETL delay by querying live transactional tables directly."
                    },
                    {
                        "id": "d19_q2",
                        "concept_slug": "operational-reporting-vdm",
                        "prompt": "In the SAP Virtual Data Model (VDM), which layer is specifically designed for direct UI consumption and analytical queries?",
                        "options": [
                            {"id": "a", "text": "Private Views (P_ Views) used as unreleased internal building blocks", "is_correct": False},
                            {"id": "b", "text": "Raw Physical Database Tables stored on non-volatile disk", "is_correct": False},
                            {"id": "c", "text": "Consumption Views (C_ Views) annotated with @Analytics.query: true", "is_correct": True}
                        ],
                        "explanation": "Consumption views (prefixed with C_) are designed specifically for analytical UI exposure."
                    }
                ]
            },
            {
                "step_id": "d19_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 19 Skill Evidence Verification",
                "concept_slug": "embedded-analytics-foundations",
                "evidence_rule": "Demonstrated mastery of S/4HANA Embedded Analytics, Virtual Data Models, and real-time operational reporting.",
            },
            {
                "step_id": "d19_s8_completion",
                "step_type": "completion",
                "title": "Day 19 Complete: Embedded Analytics Mastered",
                "summary_md": """### 📈 Real-Time Intelligence Validated!

You have mastered the principles of S/4HANA Embedded Analytics:
- Elimination of operational ETL batch pipelines.
- Hybrid Transactional/Analytical Processing (HTAP) in main memory.
- Virtual Data Model (VDM) hierarchy from Basic to Consumption views.

**Next Milestone**: Day 20 explores end-to-end traceability—**Document Flow & Cross-Document Integration**!""",
                "recommended_mission": {
                    "slug": "nova-cds-reporting-requirement",
                    "title": "Mission: CDS Reporting Requirement",
                    "description": "Design an operational reporting architecture for Nova Manufacturing using CDS View Entities and Smart Business KPIs."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 20: S/4HANA Document Flow
    # =========================================================================
    20: {
        "day_number": 20,
        "slug": "document-flow-integration",
        "title": "Document Flow & Cross-Document Traceability",
        "subtitle": "Trace transactional continuity across sales, delivery, inventory, billing, and general ledgers",
        "estimated_minutes": 45,
        "atomic_concepts": ["document-flow-continuity", "transactional-audit-trail"],
        "recommended_mission_slug": "nova-cross-module-document-trace",
        "steps": [
            {
                "step_id": "d20_s1_learn",
                "step_type": "learn",
                "title": "The Thread of Transactional Continuity",
                "content_md": """### Connecting the Enterprise Chain

In an integrated enterprise system, no document exists in isolation. A single customer order initiates a chronological chain of commercial, physical, and financial commitments:

$$\\text{Quotation} \\rightarrow \\text{Sales Order} \\rightarrow \\text{Outbound Delivery} \\rightarrow \\text{Goods Issue (MATDOC)} \\rightarrow \\text{Billing Document} \\rightarrow \\text{Universal Journal (ACDOCA)}$$

### Table VBFA: The Relationship Nervous System
In SAP S/4HANA, the end-to-end relationship between commercial documents is tracked in table **VBFA** (Sales Document Flow):
- **Preceding Document (`VBELV`)**: The predecessor record number (e.g. Sales Order `#10042`).
- **Subsequent Document (`VBELN`)**: The successor record number (e.g. Outbound Delivery `#80019`).
- **Preceding Document Category (`VBTYP_V`)**: The category of predecessor (e.g. Order `C`, Delivery `J`).
- **Subsequent Document Category (`VBTYP_N`)**: The category of successor (e.g. Delivery `J`, Goods Issue `R`, Invoice `M`).

### The Technical Bridge to Financial Accounting
While table `VBFA` maintains relationships between Sales & Distribution documents, the link between logistics and Financial Accounting (`BKPF`/`ACDOCA`) is bridged via header Reference Transaction keys:
- For Goods Issue: `AWTYP = 'MKPF'` and `AWKEY = Material Document Number + Fiscal Year`.
- For Invoices: `AWTYP = 'VBRK'` and `AWKEY = Billing Document Number`.
This reference key bridge allows any accountant in Fiori to drill straight back from an ACDOCA journal entry to the originating packing slip or billing document!""",
                "key_terms": [
                    {"term": "Document Flow", "definition": "The chronological lineage linking all commercial, logistics, and financial documents generated by a business event."},
                    {"term": "Table VBFA", "definition": "The central sales document relationship table recording predecessor and successor links across the order lifecycle."},
                    {"term": "Reference Transaction (AWTYP/AWKEY)", "definition": "The header link fields in BKPF/ACDOCA storing the originating source application and document number."}
                ],
            },
            {
                "step_id": "d20_s2_understand",
                "step_type": "understand",
                "title": "How Logistics Integrates Synchronously with Finance",
                "content_md": """### The Crucial Handshakes in the Document Flow

Two pivotal milestones in the document flow trigger synchronous financial consequences:

1. **Post Goods Issue (PGI)**:
   - *Logistics Event*: Warehouse confirms that goods have physically left the loading dock.
   - *Material Ledger*: Generates document in table `MATDOC` reducing inventory quantity.
   - *Financial Ledger*: Generates synchronous journal entry in `ACDOCA`:
     - **Debit**: Cost of Goods Sold (COGS Expense Account).
     - **Credit**: Inventory Valuation Account (Balance Sheet Asset).

2. **Billing Document Release**:
   - *Commercial Event*: Invoice generated and transmitted to customer.
   - *Financial Ledger*: Generates synchronous journal entry in `ACDOCA`:
     - **Debit**: Customer Accounts Receivable Subledger.
     - **Credit**: Sales Revenue Account.
     - **Credit**: Output Tax Liability Account.

### The Integrity Guarantee
If an error occurs during the financial posting (e.g. account determination is missing), the logistics transaction is rolled back. Data inconsistency between logistics and finance is architecturally impossible!""",
            },
            {
                "step_id": "d20_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: Order #10042 End-to-End Lineage",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "order": "Sales Order #10042 (CUST-501)"
                },
                "content_md": """### Auditing a €42,000 Transatlantic Order

Nordics Heavy Industrial AB (**CUST-501**) ordered 30 units of the **DXTR-1000** Robotics Controller:

1. **Sales Order `#10042`**: Created in `SO01`, confirmed availability at Plant `PL01`.
2. **Outbound Delivery `#80019`**: Heidelberg warehouse picked 30 units from Storage Location `FG01`.
3. **Goods Issue `#490001`**: Appended to `MATDOC`. Synchronous ACDOCA entry recognized **€25,500.00** Cost of Goods Sold.
4. **Billing Document `#900055`**: Commercial invoice issued with 19% German VAT.
5. **Journal Entry `#100008`**: ACDOCA recognized **€49,980.00** gross receivable on customer `CUST-501` (`AWTYP = 'VBRK'`).
6. **Clearing `#100021`**: Electronic bank transfer cleared the customer account with zero residual variance!""",
            },
            {
                "step_id": "d20_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Interactive Document Flow Tracer",
                "component_type": "DocumentFlowTracer",
                "instruction": "Navigate the chronological document chain from Sales Order to Financial Clearing. Inspect table references and audit debit/credit postings.",
            },
            {
                "step_id": "d20_s5_challenge",
                "step_type": "challenge",
                "title": "The Unbilled Delivery Audit Investigation",
                "scenario_md": """An internal audit at Nova Manufacturing discovers an outbound delivery (LF #80019) that was picked 3 weeks ago, but no customer invoice was ever generated.
The sales team insists the customer was billed.

How should the enterprise analyst diagnose table VBFA to determine the exact point of breakdown?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "Inspect table VBFA for preceding document #80019. If no successor document with category 'R' (Goods Issue) exists, the warehouse omitted Post Goods Issue (PGI), blocking the billing queue.",
                        "is_correct": True,
                        "explanation": "Billing strictly requires confirmed Goods Issue; checking VBFA successor links reveals where the process halted."
                    },
                    {
                        "id": "ch_b",
                        "text": "Execute an immediate manual journal entry in ACDOCA directly debiting the customer without a reference billing document.",
                        "is_correct": False,
                        "explanation": "Manual entries without reference documents violate SD-FI audit reconciliation controls."
                    },
                    {
                        "id": "ch_c",
                        "text": "Delete outbound delivery #80019 from the database to remove the open item from audit reports.",
                        "is_correct": False,
                        "explanation": "Deleting operational transaction records destroys audit trails and creates inventory imbalances."
                    }
                ]
            },
            {
                "step_id": "d20_s6_assessment",
                "step_type": "assessment",
                "title": "Day 20 Concept Assessment: Document Flow & Traceability",
                "questions": [
                    {
                        "id": "d20_q1",
                        "concept_slug": "document-flow-continuity",
                        "prompt": "Which database table maintains predecessor and successor document linkages across the sales and distribution document flow in S/4HANA?",
                        "options": [
                            {"id": "a", "text": "Table VBFA", "is_correct": True},
                            {"id": "b", "text": "Table T001", "is_correct": False},
                            {"id": "c", "text": "Table SKA1", "is_correct": False}
                        ],
                        "explanation": "Table VBFA (Sales Document Flow) stores all predecessor/successor document relationships."
                    },
                    {
                        "id": "d20_q2",
                        "concept_slug": "transactional-audit-trail",
                        "prompt": "What financial accounting posting occurs in ACDOCA at the exact moment warehouse personnel execute Post Goods Issue (PGI) for an outbound sales delivery?",
                        "options": [
                            {"id": "a", "text": "Debit Cash at Bank, Credit Accounts Receivable Subledger", "is_correct": False},
                            {"id": "b", "text": "Debit Cost of Goods Sold (COGS) Expense, Credit Inventory Valuation Balance Sheet Account", "is_correct": True},
                            {"id": "c", "text": "Debit Accounts Payable, Credit Vendor Clearing Account", "is_correct": False}
                        ],
                        "explanation": "PGI immediately reduces balance sheet inventory and recognizes COGS expense in ACDOCA."
                    }
                ]
            },
            {
                "step_id": "d20_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 20 Skill Evidence Verification",
                "concept_slug": "document-flow-continuity",
                "evidence_rule": "Demonstrated mastery of cross-module document flow, VBFA lineage, and financial integration handshakes.",
            },
            {
                "step_id": "d20_s8_completion",
                "step_type": "completion",
                "title": "Day 20 Complete: Document Flow Traceability Mastered",
                "summary_md": """### 🔗 Cross-Document Traceability Validated!

You have mastered transactional lineage across S/4HANA:
- Chronological document flow from sales order to financial clearing.
- Relationship tracking via table `VBFA`.
- Synchronous financial commitments triggered by Post Goods Issue and Billing.

**Next Milestone**: Day 21 synthesizes everything in a **Cross-Module Integrated Scenario**!""",
                "recommended_mission": {
                    "slug": "nova-cross-module-document-trace",
                    "title": "Mission: Cross-Module Document Trace",
                    "description": "Follow a live business event across logistics, inventory, and finance to audit transactional continuity."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 21: Cross-Module Integrated Scenario
    # =========================================================================
    21: {
        "day_number": 21,
        "slug": "s4hana-integrated-scenario",
        "title": "Cross-Module Integrated Scenario",
        "subtitle": "End-to-end transactional integration: executing a complete customer order touching BP, Sales, MATDOC, and ACDOCA",
        "estimated_minutes": 45,
        "atomic_concepts": ["s4hana-integrated-scenario"],
        "recommended_mission_slug": "nova-cross-module-document-trace",
        "steps": [
            {
                "step_id": "d21_s1_learn",
                "step_type": "learn",
                "title": "The Master Symphony of Enterprise ERP",
                "content_md": """### Synthesizing the Complete S/4HANA Engine

Over the last 12 days, you have explored individual architectural components of SAP S/4HANA:
- The in-memory columnar engine of **SAP HANA** (Day 11).
- The universal financial ledger **ACDOCA** (Day 12).
- The single-table inventory ledger **MATDOC** (Day 13).
- The central master entity **Business Partner** (Day 14).
- Declarative view entities in **Core Data Services** (Day 15).
- Enterprise landscape deployment governance (Days 16–17).
- Identity & Access Governance (Day 18).
- Real-time **Embedded Analytics** (Day 19).
- Document lineage in **VBFA** (Day 20).

In today's integrated scenario, all these components execute simultaneously in a single, high-stakes operational workflow.""",
                "key_terms": [
                    {"term": "End-to-End Execution", "definition": "Executing a complete commercial process traversing master data, inventory, sales, and financial ledgers."},
                    {"term": "Synchronous Posting", "definition": "Immediate atomic updates across disparate functional tables within a single database commit."},
                    {"term": "Audit Trail Verification", "definition": "Validating that every operational document correctly references its predecessor and maintains financial balance."}
                ],
            },
            {
                "step_id": "d21_s2_understand",
                "step_type": "understand",
                "title": "The Anatomy of an Integrated Transactional Event",
                "content_md": """### What Actually Happens During Order Execution?

When customer **CUST-501** orders 50 units of **DXTR-1000**:
1. **Master Data Validation**:
   - The system checks `BUT000` / `FLCU01` for sales terms, currency, and credit limits.
2. **Inventory Availability Check (ATP)**:
   - HANA queries `MATDOC` in RAM to verify physical stock in Plant `PL01` Storage Location `FG01`.
3. **Outbound Delivery & Picking**:
   - Generates document in `LIKP`/`LIPS` and creates relationship record in `VBFA`.
4. **Post Goods Issue**:
   - Appends inventory decrease to `MATDOC`.
   - Simultaneously writes COGS expense and inventory asset reduction to `ACDOCA`.
5. **Commercial Invoicing**:
   - Generates billing document in `VBRK`/`VBRP`.
   - Writes revenue, accounts receivable, and VAT tax rows to `ACDOCA`.
6. **Embedded Analytics Update**:
   - Real-time CDS KPI tiles immediately reflect updated margin and inventory balances with zero delay!""",
            },
            {
                "step_id": "d21_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: Transatlantic Integrated Order Fulfillment",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "scenario": "Live Order Execution CUST-501"
                },
                "content_md": """### Execution Log: Order to Financial Settlement

- **09:00 AM**: Sales Order `#10055` created for customer `CUST-501` (Nordics Industrial AB) for 50x `DXTR-1000` at €1,400.00/unit = **€70,000.00**.
- **09:15 AM**: Outbound Delivery `#80032` created at Plant `PL01` Shipping Point Heidelberg.
- **10:30 AM**: Warehouse scans handling units and executes Post Goods Issue.
  - `MATDOC` record `#5000010990` posted: -50 EA.
  - `ACDOCA` record `#100045` posted: Dr COGS €42,500.00, Cr Inventory €42,500.00.
- **11:00 AM**: Billing Document `#900088` generated with 19% VAT = **€83,300.00** gross.
  - `ACDOCA` record `#100046` posted: Dr AR CUST-501 €83,300.00, Cr Revenue €70,000.00, Cr Tax €13,300.00.
- **11:01 AM**: Executive Fiori Dashboard shows updated gross profit of **€27,500.00** with zero batch jobs executed!""",
            },
            {
                "step_id": "d21_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Interactive End-to-End Document Flow & Ledger Tracer",
                "component_type": "DocumentFlowTracer",
                "instruction": "Follow the complete integrated fulfillment scenario across SD, MM, and FI. Validate the exact table commitments across VBFA, MATDOC, and ACDOCA.",
            },
            {
                "step_id": "d21_s5_challenge",
                "step_type": "challenge",
                "title": "The Cross-Module Discrepancy Investigation",
                "scenario_md": """During the integrated scenario, the billing document generates successfully, but the accounting document in ACDOCA is blocked with error:
*Account Determination Error: G/L account for Account Key ERL (Sales Revenues) not maintained for Chart of Accounts YCOA in transaction VKOA.*

What has occurred, and how is it remediated?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "The automatic account determination rules linking the billing condition type (PR00) and account key (ERL) to the general ledger revenue account are missing in configuration transaction VKOA.",
                        "is_correct": True,
                        "explanation": "Billing integration with ACDOCA requires configured G/L account determination (VKOA); maintaining the mapping allows the journal to post immediately."
                    },
                    {
                        "id": "ch_b",
                        "text": "The billing document has exceeded the customer's credit limit managed in SAP Credit Management (FSCM-CR).",
                        "is_correct": False,
                        "explanation": "Credit limit blocks occur during sales order confirmation or delivery creation, not as VKOA account determination errors."
                    },
                    {
                        "id": "ch_c",
                        "text": "The outbound delivery document was archived prematurely before billing generation.",
                        "is_correct": False,
                        "explanation": "Archiving does not trigger G/L account determination errors in active billing runs."
                    }
                ]
            },
            {
                "step_id": "d21_s6_assessment",
                "step_type": "assessment",
                "title": "Day 21 Concept Assessment: Integrated Scenario Synthesis",
                "questions": [
                    {
                        "id": "d21_q1",
                        "concept_slug": "s4hana-integrated-scenario",
                        "prompt": "When a sales billing document is released to accounting in SAP S/4HANA, which financial table immediately records the customer receivable, revenue, and tax line items in a single commit?",
                        "options": [
                            {"id": "a", "text": "Table VBAP (Sales Order Item data)", "is_correct": False},
                            {"id": "b", "text": "Table ACDOCA (Universal Journal)", "is_correct": True},
                            {"id": "c", "text": "Table MARA (General Material Data)", "is_correct": False}
                        ],
                        "explanation": "ACDOCA unifies customer subledger, general ledger, and revenue accounting into a single atomic record."
                    }
                ]
            },
            {
                "step_id": "d21_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Day 21 Skill Evidence Verification",
                "concept_slug": "s4hana-integrated-scenario",
                "evidence_rule": "Demonstrated full-lifecycle integration capability uniting Master Data, Logistics, Inventory, and Financial Accounting.",
            },
            {
                "step_id": "d21_s8_completion",
                "step_type": "completion",
                "title": "Day 21 Complete: Cross-Module Integration Validated",
                "summary_md": """### 🌐 Cross-Module Symphony Mastered!

You have validated full operational execution across the core modules of S/4HANA:
- Master data validation via central Business Partner.
- High-speed inventory movement in `MATDOC`.
- Document lineage auditability in `VBFA`.
- Real-time financial settlement in `ACDOCA`.

**Next Milestone**: Day 22 presents the **S/4HANA Fundamentals Capstone Exam**—evaluating 11 distinct architectural concepts!""",
                "recommended_mission": {
                    "slug": "nova-cross-module-document-trace",
                    "title": "Mission: Cross-Module Document Trace",
                    "description": "Execute an end-to-end enterprise audit trace across sales, inventory, and financials."
                }
            }
        ]
    },

    # =========================================================================
    # DAY 22: S/4HANA Fundamentals Capstone
    # =========================================================================
    22: {
        "day_number": 22,
        "slug": "s4hana-fundamentals-capstone",
        "title": "S/4HANA Fundamentals & Architecture Evaluation",
        "subtitle": "Comprehensive Phase 2 benchmark evaluation across 11 core architectural dimensions",
        "estimated_minutes": 60,
        "atomic_concepts": [
            "s4hana-architecture-synthesis",
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
            "document-flow-continuity"
        ],
        "recommended_mission_slug": "nova-s4hana-modernization-decision",
        "steps": [
            {
                "step_id": "d22_s1_learn",
                "step_type": "learn",
                "title": "Phase 2 Architectural Defense & Synthesis",
                "content_md": """### The Capstone Milestone of Phase 2

Welcome to the **S/4HANA Fundamentals & Architecture Capstone**. Over Days 9 through 21, you investigated the core technical shifts that distinguish modern S/4HANA from legacy ERP systems.

This Capstone benchmark evaluates your ability to make holistic architectural decisions for **Nova Manufacturing Corp (`NM01`)** as it scales its operations across Heidelberg (`PL01`) and the Austin Tech Center (`PL02`).

### 11 Architectural Dimensions Tested
1. **S/4HANA Core Value Drivers**: Business case, TCO, and elimination of batch latency.
2. **ECC Simplifications**: Deprecated aggregate tables and Compatibility View mechanics.
3. **In-Memory Computing**: Columnar storage, dictionary compression, and Delta Merge lifecycle.
4. **Universal Journal**: Table `ACDOCA`, single source of truth, and Parallel Ledgers (`0L` vs `2L`).
5. **MATDOC Inventory Architecture**: Lock contention elimination and insert-only logistics.
6. **Business Partner & CVI**: Role hierarchy (`FLVN00`/`FLVN01`, `FLCU00`/`FLCU01`) and synchronization.
7. **Core Data Services (CDS)**: View Entities, associations, and code pushdown philosophy.
8. **Landscape Governance**: 3-System Landscape (DEV $\to$ QAS $\to$ PRD) and transport request integrity.
9. **Identity & Access Management**: Fiori Launchpad RBAC, spaces, pages, and Segregation of Duties.
10. **Embedded Analytics**: Real-time HTAP reporting without external ETL pipelines.
11. **Document Flow**: End-to-end audit trails in table `VBFA` linking logistics to financials.

### Multi-Concept Evaluation Semantics
This Capstone does **not** flatten your score into a single vague percentage. Each of the 11 dimensions is scored individually. Any concept scoring below 70% immediately triggers targeted DAG remediation capsules!""",
                "key_terms": [
                    {"term": "Architecture Synthesis", "definition": "The holistic integration of data models, in-memory mechanics, and business processes to design resilient enterprise systems."},
                    {"term": "Multi-Concept Evaluation", "definition": "Evaluating each atomic DAG concept independently to isolate knowledge gaps without masking deficiencies."},
                    {"term": "Targeted Remediation", "definition": "Specific recovery tasks and concept reviews triggered automatically when individual concept mastery falls below threshold."}
                ],
            },
            {
                "step_id": "d22_s2_understand",
                "step_type": "understand",
                "title": "Designing for Clean Core, Resilience, and High Concurrency",
                "content_md": """### Architectural Invariants of Modern S/4HANA

Before beginning the benchmark evaluation, review the three non-negotiable enterprise invariants:

1. **The Clean Core Invariant**:
   - Standard SAP tables must never be modified directly.
   - All extensibility must use released APIs, Key-User tools, or SAP BTP side-by-side applications to ensure friction-free automated upgrades.

2. **The In-Memory Pushdown Invariant**:
   - Aggregations and filtering must happen at the database layer (via CDS View Entities) rather than in application server memory loops.
   - Analytical reporting must leverage live transactional tables (`ACDOCA`, `MATDOC`) before considering external data replication.

3. **The Audit Integrity Invariant**:
   - Logistics goods movements, billing releases, and ledger entries must maintain unbroken traceability via table `VBFA` and reference keys.
   - Direct database writes to compatibility views (e.g. inserting into `MSEG` or updating `BSIK`) are strictly prohibited.""",
            },
            {
                "step_id": "d22_s3_visual_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: Transatlantic Enterprise Architecture Review",
                "company_context": {
                    "name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "plants": "PL01 (Heidelberg) & PL02 (Austin)"
                },
                "content_md": """### The Boardroom Architecture Defense

Nova Manufacturing's Board of Directors has convened to approve the transatlantic commissioning of Plant `PL02` in Austin, Texas:

- **Financial Architecture**: Leading Ledger `0L` (IFRS in EUR) and Non-Leading Ledger `2L` (US GAAP in USD) operate in parallel inside table `ACDOCA`.
- **Logistics Architecture**: Austin storage locations `RAW1` and `FG01` post goods movements directly to `MATDOC` with zero row-lock contention.
- **Master Data**: Vendor Rheinland Precision (**BP-101**) is maintained via central Business Partner with synchronized purchasing and financial views.
- **Integration**: A transatlantic sales order for 100 units of `DXTR-1000` is traced end-to-end from Fiori Launchpad order creation to bank clearing in 0.8 seconds.

The Chief Enterprise Architect must now defend the technical architecture under rigorous cross-examination!""",
            },
            {
                "step_id": "d22_s4_interactive_practice",
                "step_type": "interactive_practice",
                "title": "Capstone Pre-Flight Architectural Decision Review",
                "component_type": "ScenarioDecision",
                "instruction": "Evaluate the architectural readiness of Nova Manufacturing's S/4HANA environment before taking the comprehensive benchmark exam.",
                "options": [
                    {
                        "id": "opt_clean_core",
                        "title": "Strategy 1: Enforce Clean Core, ACDOCA/MATDOC Single Ledgers, and CDS Pushdown",
                        "consequence": "Zero batch bottlenecks. Real-time MRP Live. Multi-GAAP compliance. Automated quarterly cloud upgrades supported.",
                        "tradeoff": "Requires disciplined adherence to standard SAP Best Practices and released APIs.",
                        "is_recommended": True
                    },
                    {
                        "id": "opt_legacy_hybrid",
                        "title": "Strategy 2: Reintroduce Legacy Aggregate Tables and Nightly Batch Closing",
                        "consequence": "Database footprint swells by 300%. Table locks stall automated assembly lines. High reconciliation overhead returns.",
                        "tradeoff": "Comfortable for legacy personnel, but fatal to enterprise scalability.",
                        "is_recommended": False
                    }
                ]
            },
            {
                "step_id": "d22_s5_challenge",
                "step_type": "challenge",
                "title": "The Transatlantic Expansion Architecture Dilemma",
                "scenario_md": """Nova Manufacturing's Austin plant (PL02) requires local US dollar reporting under US GAAP, while the Heidelberg headquarters (NM01) requires euro reporting under IFRS.
A consultant proposes installing a second, completely separate S/4HANA system in Austin to satisfy local US requirements.

How should the Chief Enterprise Architect evaluate this proposal?""",
                "options": [
                    {
                        "id": "ch_a",
                        "text": "Reject the second system. S/4HANA natively supports multi-GAAP and multi-currency reporting within a single system instance using Leading Ledger (0L) and Non-Leading Ledger (2L) in table ACDOCA.",
                        "is_correct": True,
                        "explanation": "Parallel ledgers in ACDOCA provide complete legal separation and consolidation within a single system instance."
                    },
                    {
                        "id": "ch_b",
                        "text": "Approve the second system because S/4HANA can only support one currency in the entire database.",
                        "is_correct": False,
                        "explanation": "ACDOCA natively supports up to 10 parallel currencies simultaneously in one record."
                    },
                    {
                        "id": "ch_c",
                        "text": "Implement manual monthly journal adjustments in external spreadsheets to convert euro balances into US dollars outside the ERP system.",
                        "is_correct": False,
                        "explanation": "Manual spreadsheet adjustments introduce high audit risks, eliminate real-time reporting, and defeat the purpose of an integrated ERP."
                    }
                ]
            },
            {
                "step_id": "d22_s6_assessment",
                "step_type": "assessment",
                "title": "Phase 2 S/4HANA Fundamentals Capstone Benchmark Exam",
                "is_capstone": True,
                "multi_concept_eval": True,
                "concepts_evaluated": [
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
                    "document-flow-continuity"
                ],
                "questions": [
                    {
                        "id": "cap2_q1",
                        "concept_slug": "s4hana-value-drivers",
                        "prompt": "Which operational benefit is directly enabled by S/4HANA's elimination of aggregate tables and adoption of in-memory computing?",
                        "options": [
                            {"id": "a", "text": "Executing traditional nightly batch closing runs across all general ledger accounts", "is_correct": False},
                            {"id": "b", "text": "Material Requirements Planning (MRP Live) can run during business hours in minutes rather than overnight batch windows", "is_correct": True},
                            {"id": "c", "text": "Complete elimination of disaster recovery data centers and backup retention policies", "is_correct": False},
                            {"id": "d", "text": "Mandatory replacement of all enterprise transactional documents with non-relational JSON files", "is_correct": False}
                        ],
                        "explanation": "MRP Live leverages in-memory pushdown (MD01N) directly in HANA RAM, enabling planners to evaluate component shortages on-demand during active shifts."
                    },
                    {
                        "id": "cap2_q2",
                        "concept_slug": "ecc-simplification-items",
                        "prompt": "How does an SAP S/4HANA Compatibility View handle custom ABAP programs that execute read SELECT queries against deprecated legacy tables like BSIS or MSEG?",
                        "options": [
                            {"id": "a", "text": "It transparently redirects the query in the database catalog to ACDOCA or MATDOC without requiring custom code modification", "is_correct": True},
                            {"id": "b", "text": "It blocks program execution and raises syntax error 'TABLE_NO_LONGER_EXISTS' in transaction SE38", "is_correct": False},
                            {"id": "c", "text": "It replicates historical records on-the-fly into physical shadow tables on application server disks", "is_correct": False},
                            {"id": "d", "text": "It converts the SQL SELECT query into an unmanaged RFC call to an external archive system", "is_correct": False}
                        ],
                        "explanation": "Compatibility views act as non-materialized CDS-based database views sharing the legacy table's name and structure, redirecting SELECT statements dynamically to Universal Ledgers."
                    },
                    {
                        "id": "cap2_q3",
                        "concept_slug": "in-memory-computing",
                        "prompt": "What is the primary architectural function of the Delta Merge process in the SAP HANA column store?",
                        "options": [
                            {"id": "a", "text": "To write dirty memory pages from RAM to the non-volatile disk data volume during regular savepoints", "is_correct": False},
                            {"id": "b", "text": "To delete soft-deleted client records permanently to free database storage space", "is_correct": False},
                            {"id": "c", "text": "To transfer write-optimized uncompressed transactional records from Delta Storage into read-optimized compressed Main Storage", "is_correct": True},
                            {"id": "d", "text": "To synchronize database replication between the primary host and secondary standby node in High Availability", "is_correct": False}
                        ],
                        "explanation": "HANA column tables write incoming transactions to write-optimized Delta storage; asynchronous Delta Merge operations sort, compress, and merge them into the columnar Main storage."
                    },
                    {
                        "id": "cap2_q4",
                        "concept_slug": "universal-journal-concept",
                        "prompt": "Why is the traditional FI-CO reconciliation ledger obsolete in SAP S/4HANA?",
                        "options": [
                            {"id": "a", "text": "Because Controlling (CO) module transactions have been deprecated and replaced entirely by external BI cubes", "is_correct": False},
                            {"id": "b", "text": "Because Financial Accounting and Controlling line items are written simultaneously to the Universal Journal (ACDOCA) as a single source of truth", "is_correct": True},
                            {"id": "c", "text": "Because period-end financial reconciliation is postponed until annual corporate audits", "is_correct": False},
                            {"id": "d", "text": "Because general ledger accounts can no longer be assigned to internal orders or cost centers", "is_correct": False}
                        ],
                        "explanation": "Table ACDOCA unifies GL balance sheet accounts, P&L expenses, cost centers, profit centers, and market segments in every single transaction line, guaranteeing zero variance between FI and CO."
                    },
                    {
                        "id": "cap2_q5",
                        "concept_slug": "matdoc-table-architecture",
                        "prompt": "How does table MATDOC eliminate warehouse inventory lock contention during high-volume goods receipts and goods issues?",
                        "options": [
                            {"id": "a", "text": "By adopting an insert-only ledger architecture that appends movement records rather than updating locked aggregate balance rows in MARC/MARD/MBEW", "is_correct": True},
                            {"id": "b", "text": "By serializing all warehouse goods movements through a single global background enqueue process", "is_correct": False},
                            {"id": "c", "text": "By caching inventory movements in web browser memory until end-of-shift batch submission", "is_correct": False},
                            {"id": "d", "text": "By disabling database transaction ACID rollback protection during peak delivery hours", "is_correct": False}
                        ],
                        "explanation": "MATDOC appends new rows for each movement. Current stock quantities are calculated on-the-fly via fast in-memory aggregation, eliminating exclusive row locks on material master balance records."
                    },
                    {
                        "id": "cap2_q6",
                        "concept_slug": "business-partner-cvi",
                        "prompt": "In S/4HANA master data architecture, how is an organization that acts as both a component supplier and a finished goods customer configured?",
                        "options": [
                            {"id": "a", "text": "By creating two independent master records with completely separate addresses and tax numbers in XD01 and XK01", "is_correct": False},
                            {"id": "b", "text": "By defining an anonymous guest account in Fiori and attaching invoice line items manually", "is_correct": False},
                            {"id": "c", "text": "As a single central Business Partner (BUT000) assigned both supplier roles (FLVN00/FLVN01) and customer roles (FLCU00/FLCU01)", "is_correct": True},
                            {"id": "d", "text": "By converting the supplier into an internal company code and billing via intercompany clearing", "is_correct": False}
                        ],
                        "explanation": "The Business Partner (BP) model maintains legal and general data centrally in BUT000, extending business relationships through specialized roles while Customer-Vendor Integration (CVI) synchronizes legacy KNA1/LFA1 tables."
                    },
                    {
                        "id": "cap2_q7",
                        "concept_slug": "cds-fundamentals",
                        "prompt": "What is the primary architectural advantage of using modern CDS View Entities compared to legacy application server processing loops?",
                        "options": [
                            {"id": "a", "text": "CDS View Entities generate classical ABAP transparent tables in SE11 for direct transactional writing", "is_correct": False},
                            {"id": "b", "text": "Calculations, filtering, and aggregations are pushed down directly into the HANA database engine, returning only aggregated KPI results across the network", "is_correct": True},
                            {"id": "c", "text": "CDS View Entities bypass enterprise role-based access control and PFCG authorization checks", "is_correct": False},
                            {"id": "d", "text": "CDS View Entities compile into client-side JavaScript executed exclusively within web browsers", "is_correct": False}
                        ],
                        "explanation": "Code pushdown executes intensive joins and mathematical aggregations directly in HANA in-memory RAM, preventing millions of raw records from traversing the application network."
                    },
                    {
                        "id": "cap2_q8",
                        "concept_slug": "transport-management-cts",
                        "prompt": "In enterprise landscape governance, why is direct configuration modifying (SCC4 / SE06) strictly locked in the Production (PRD) system?",
                        "options": [
                            {"id": "a", "text": "Because production database licenses do not support UPDATE or INSERT SQL operations", "is_correct": False},
                            {"id": "b", "text": "To force consultants to execute manual SQL ALTER TABLE scripts directly through the operating system shell", "is_correct": False},
                            {"id": "c", "text": "Because production client storage quota prevents creating transport log files", "is_correct": False},
                            {"id": "d", "text": "To prevent untested changes from disrupting active commercial operations and guarantee audit compliance through verified transport request lineage", "is_correct": True}
                        ],
                        "explanation": "Locking production clients ensures that every configuration or code change undergoes rigorous unit and integration testing across DEV and QAS, maintaining complete transport auditability."
                    },
                    {
                        "id": "cap2_q9",
                        "concept_slug": "identity-access-management",
                        "prompt": "What constitutes a critical Segregation of Duties (SoD) violation in S/4HANA enterprise access governance?",
                        "options": [
                            {"id": "a", "text": "Assigning a user multiple language packs on the SAP Fiori Launchpad", "is_correct": False},
                            {"id": "b", "text": "Granting a user authorization to display both sales order headers and delivery packing lists", "is_correct": False},
                            {"id": "c", "text": "Granting a single employee both purchase order release authority and automatic vendor payment disbursement authorization", "is_correct": True},
                            {"id": "d", "text": "Allowing an inventory manager to view standard cost estimates in Plant PL01", "is_correct": False}
                        ],
                        "explanation": "Dual control is required between procurement and disbursement. Combining PO release (M_BEST_WRK) with payment execution (F_REGU_BUK) enables fraudulent disbursements without secondary oversight."
                    },
                    {
                        "id": "cap2_q10",
                        "concept_slug": "embedded-analytics-foundations",
                        "prompt": "How does S/4HANA Embedded Analytics achieve real-time operational reporting without data latency?",
                        "options": [
                            {"id": "a", "text": "It executes analytical CDS queries directly on live transactional tables (ACDOCA, MATDOC) in memory without ETL replication delays", "is_correct": True},
                            {"id": "b", "text": "It replicates operational tables every 5 minutes into external flat CSV files on an FTP server", "is_correct": False},
                            {"id": "c", "text": "It caches static monthly report snapshots in the application server buffer during system reboot", "is_correct": False},
                            {"id": "d", "text": "It disables financial document postings whenever an executive opens a reporting dashboard", "is_correct": False}
                        ],
                        "explanation": "Embedded Analytics leverages HANA's HTAP capabilities, allowing analytical queries to aggregate live transactional records instantaneously without staging or ETL pipelines."
                    },
                    {
                        "id": "cap2_q11",
                        "concept_slug": "document-flow-continuity",
                        "prompt": "Which SAP database table maintains the chronological predecessor and successor linkages across sales orders, outbound deliveries, and customer invoices?",
                        "options": [
                            {"id": "a", "text": "Table T001 (Company Code Definitions)", "is_correct": False},
                            {"id": "b", "text": "Table VBFA (Sales Document Flow)", "is_correct": True},
                            {"id": "c", "text": "Table SKA1 (General Ledger Accounts in Chart of Accounts)", "is_correct": False},
                            {"id": "d", "text": "Table USR02 (Logon Data and Password Hashes)", "is_correct": False}
                        ],
                        "explanation": "Table VBFA tracks sales document relationships using predecessor/successor document numbers (VBELV/VBELN) and category codes (VBTYP_V/VBTYP_N), ensuring complete transaction traceability."
                    }
                ]
            },
            {
                "step_id": "d22_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Phase 2 Capstone Multi-Concept Skill Proof",
                "concept_slug": "s4hana-architecture-synthesis",
                "evidence_rule": "Evaluates 11 distinct concept dimensions independently. Records first-class SAPSkillEvidence for each verified concept and triggers targeted DAG remediation capsules for any failing score.",
            },
            {
                "step_id": "d22_s8_completion",
                "step_type": "completion",
                "title": "Phase 2 Complete: Certified S/4HANA Fundamentals Architect",
                "summary_md": """### 🎓 Phase 2 Benchmark Completed!

You have successfully completed **Phase 2: S/4HANA Fundamentals & Data Architecture (Days 9–22)**!

You possess validated proficiency across the 11 pillars of S/4HANA:
1. S/4HANA Core Value Drivers & Real-Time MRP
2. ECC Simplifications & Compatibility Views
3. In-Memory Computing & Delta Merge Lifecycle
4. ACDOCA Universal Journal & Parallel Ledgers
5. MATDOC Single-Table Inventory Architecture
6. Business Partner (BP) & Customer-Vendor Integration (CVI)
7. Core Data Services (CDS) & Code Pushdown
8. 3-System Landscape (DEV $\\\\to$ QAS $\\\\to$ PRD) & CTS Governance
9. Fiori Role Architecture & Segregation of Duties (SoD)
10. Embedded Analytics & Virtual Data Model (VDM)
11. End-to-End Document Flow & Transactional Traceability (VBFA)

**Coming Next**: Phase 3 (Days 23–44) explores **Core End-to-End Business Processes**—diving into the deep transactional execution of Procure-to-Pay (P2P), Order-to-Cash (O2C), Manufacturing, and Financial Settlement!""",
                "recommended_mission": {
                    "slug": "nova-s4hana-modernization-decision",
                    "title": "Final Phase 2 Mission: S/4HANA Modernization Decision",
                    "description": "Synthesize your architectural knowledge to formulate Nova Manufacturing's enterprise transition blueprint."
                }
            }
        ]
    }
}
