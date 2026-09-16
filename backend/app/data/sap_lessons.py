"""Authoritative content definitions for SAP S/4HANA Guided Learning Days 1–8.

Implements the strict 8-step pedagogical sequence for every day:
1. learn: Core concepts, definitions, and business rationale.
2. understand: Deep-dive architecture and design patterns.
3. visual_example: Concrete implementation inside Nova Manufacturing Corp (NM01).
4. interactive_practice: Specification for reusable UI practice components.
5. challenge: Real-world enterprise scenario decision.
6. assessment: Multi-question concept test mapped directly to DAG concepts.
7. mastery_evidence: Explicit concept scoring and skill evidence metadata.
8. completion: Key takeaways, review, and companion Enterprise Mission links.
"""

from __future__ import annotations

from typing import Any

SAP_DAYS_CONTENT: dict[int, dict[str, Any]] = {
    1: {
        "day_number": 1,
        "slug": "enterprise-systems-cross-functional",
        "title": "Enterprise Systems & Cross-Functional Flows",
        "subtitle": "How integrated ERP eliminates departmental silos",
        "estimated_minutes": 45,
        "atomic_concepts": ["erp-evolution", "cross-functional-flows"],
        "recommended_mission_slug": "nova-purchase-flow-trace",
        "steps": [
            {
                "step_id": "d1_s1_learn",
                "step_type": "learn",
                "title": "What is an Enterprise Resource Planning (ERP) System?",
                "content_md": """### The Core Mission of Modern ERP

An Enterprise Resource Planning (ERP) system serves as the single digital nervous system for an organization. Before ERP, companies operated in fragmented departmental silos: Sales used one database, Procurement used another, Manufacturing tracked inventory on local spreadsheets, and Finance spent weeks reconciling contradictory records.

In modern business, every operation is inherently cross-functional. When a sales order is accepted:
- **Materials Management (MM)** must verify inventory or trigger procurement.
- **Production Planning (PP)** must allocate factory capacity.
- **Warehouse Management (WM)** must stage components.
- **Financial Accounting (FI)** must recognize revenue, taxes, and accounts receivable.

SAP S/4HANA is designed around **in-memory, real-time integration**—meaning when a transaction occurs anywhere in the enterprise, all downstream documents and general ledger postings occur synchronously without batch delays.""",
                "key_terms": [
                    {"term": "ERP", "definition": "Enterprise Resource Planning: Integrated software architecture managing core business operations in real-time."},
                    {"term": "Cross-Functional Flow", "definition": "A business process that seamlessly spans multiple functional departments (e.g. Sales, Warehouse, Finance)."},
                    {"term": "Document Lineage", "definition": "The end-to-end audit trail connecting related business documents (Quotation → Order → Delivery → Invoice)."}
                ],
            },
            {
                "step_id": "d1_s2_understand",
                "step_type": "understand",
                "title": "Why Functional Silos Cripple Business Agility",
                "content_md": """### From Information Islands to Integrated Flows

When companies grow without an integrated enterprise architecture, they develop "information islands." A customer places an order for 200 units of custom equipment. Sales confirms delivery in 10 days because their local system shows stock. However:

1. **The Warehouse Reality**: The physical stock was already reserved for another customer yesterday.
2. **The Procurement Delay**: Purchasing has no visibility into the new reservation and does not order raw materials.
3. **The Financial Blindspot**: Accounting only discovers the problem when the customer cancels the order and refuses to pay invoices.

SAP solves this by replacing duplicate departmental databases with a **single source of truth**. Every document inherits data from its predecessor through document flow, creating a tamper-proof audit trail and guaranteeing inventory transparency.""",
                "takeaway": "Integrated ERP eliminates guesswork: inventory, commitments, and financial balance sheets are updated synchronously at the exact moment of transaction execution.",
            },
            {
                "step_id": "d1_s3_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: Meet Company Code NM01",
                "content_md": """### Welcome to Nova Manufacturing Corp

Throughout your SAP journey, you will engineer and optimize systems for **Nova Manufacturing Corp (Company Code: NM01)**.

- **Headquarters**: Heidelberg, Germany
- **Core Business**: High-precision robotics, automation controllers, and IoT sensor hubs.
- **Primary Plant**: Plant `PL01` (Heidelberg Assembly & Main Distribution)
- **High-Tech Facility**: Plant `PL02` (Austin Tech Center, Texas)
- **Primary Finished Good**: `DXTR-1000` (High-Torque Robotics Controller)

When Nova's customer, *Nordics Heavy Industrial AB (`CUST-501`)*, places an order for 50 `DXTR-1000` units, the transaction flows seamlessly across Sales, Plant `PL01`, Inventory, and General Ledger without manual re-keying.""",
                "company_context": {
                    "code": "NM01",
                    "plants": ["PL01 (Heidelberg)", "PL02 (Austin)"],
                    "flagship_material": "DXTR-1000 Robotics Controller",
                    "key_customer": "CUST-501 (Nordics Heavy Industrial AB)",
                },
            },
            {
                "step_id": "d1_s4_practice",
                "step_type": "interactive_practice",
                "title": "Trace the Order-to-Cash (O2C) Flow",
                "component_type": "ProcessFlow",
                "instruction": "Explore the chronological progression of an integrated Order-to-Cash document flow. Click each stage to observe how data and financial responsibility transition between departments.",
                "flow_data": [
                    {
                        "step_number": 1,
                        "name": "Sales Order Creation",
                        "department": "Sales & Distribution (SD)",
                        "document": "Sales Order #10042",
                        "impact": "Checks customer credit limit and triggers ATP (Available-to-Promise) inventory check at Plant PL01."
                    },
                    {
                        "step_number": 2,
                        "name": "Outbound Delivery & Picking",
                        "department": "Logistics / Warehouse (LE/WM)",
                        "document": "Outbound Delivery #80019",
                        "impact": "Generates transfer order to pick 50 units of DXTR-1000 from storage location FG01."
                    },
                    {
                        "step_number": 3,
                        "name": "Post Goods Issue (PGI)",
                        "department": "Warehouse & Finance (MM/FI)",
                        "document": "Material Document #490001",
                        "impact": "Physical stock decreases. System automatically debits Cost of Goods Sold (COGS) and credits Inventory."
                    },
                    {
                        "step_number": 4,
                        "name": "Customer Billing (Invoice)",
                        "department": "Billing & Finance (SD/FI)",
                        "document": "Billing Doc #900055",
                        "impact": "Generates official customer invoice, debits Customer Account (AR), and credits Sales Revenue."
                    },
                    {
                        "step_number": 5,
                        "name": "Incoming Payment Clearing",
                        "department": "Financial Accounting (FI)",
                        "document": "Accounting Doc #100008",
                        "impact": "Customer wire transfer clears Accounts Receivable and debits Bank Account."
                    }
                ],
            },
            {
                "step_id": "d1_s5_challenge",
                "step_type": "challenge",
                "title": "Enterprise Scenario: The Phantom Stock Conflict",
                "instruction": "Evaluate the situation and select the best architectural decision.",
                "scenario_md": """Nova Manufacturing's sales representative in Frankfurt wants to close a €250,000 deal with an automotive client. The client demands guaranteed delivery in 7 days. The sales rep claims: *"I can see 60 units of DXTR-1000 sitting in storage location FG01 on my report, so I will promise delivery immediately."*

However, Plant PL01's production manager points out that those 60 units are already earmarked for a scheduled warranty replacement batch.

What feature of an integrated SAP system prevents this conflict?""",
                "options": [
                    {
                        "id": "opt_a",
                        "text": "Available-to-Promise (ATP): The system dynamically calculates free stock after deducting active reservations and committed orders, preventing double-allocation.",
                        "is_correct": True,
                        "explanation": "Correct! ATP checks not just physical on-hand inventory, but unreserved, available stock across open order commitments."
                    },
                    {
                        "id": "opt_b",
                        "text": "Nightly batch synchronization between the sales spreadsheet and the plant database.",
                        "is_correct": False,
                        "explanation": "Batch updates cause information latency and are the primary cause of double-allocation conflicts."
                    },
                    {
                        "id": "opt_c",
                        "text": "Allowing the sales rep to override inventory locks since revenue takes priority over maintenance.",
                        "is_correct": False,
                        "explanation": "Overriding inventory controls leads to stockout penalties, production disruptions, and customer disputes."
                    }
                ],
            },
            {
                "step_id": "d1_s6_assessment",
                "step_type": "assessment",
                "title": "Day 1 Foundations Knowledge Check",
                "concept_slug": "cross-functional-flows",
                "questions": [
                    {
                        "id": "q1",
                        "prompt": "In an integrated SAP S/4HANA system, what triggers the initial financial accounting entry during the standard goods delivery process?",
                        "options": [
                            {"id": "q1_a", "text": "Post Goods Issue (PGI) in the warehouse", "is_correct": True},
                            {"id": "q1_b", "text": "Creating the initial sales inquiry", "is_correct": False},
                            {"id": "q1_c", "text": "Printing the packing slip label", "is_correct": False}
                        ],
                        "explanation": "Post Goods Issue (PGI) is the legal transfer of ownership and physical reduction of stock, generating automatic FI entries (Debit COGS, Credit Inventory)."
                    },
                    {
                        "id": "q2",
                        "prompt": "What is the primary operational consequence of operating with departmental 'silos' rather than an integrated ERP?",
                        "options": [
                            {"id": "q2_a", "text": "Inconsistent data, duplicated entry, and lack of real-time supply chain visibility", "is_correct": True},
                            {"id": "q2_b", "text": "Hardware servers consume less electrical power", "is_correct": False},
                            {"id": "q2_c", "text": "Invoices are always paid earlier by customers", "is_correct": False}
                        ],
                        "explanation": "Silos cause data discrepancies, conflicting inventory figures, and manual reconciliation overhead."
                    }
                ],
            },
            {
                "step_id": "d1_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Mastery Verification",
                "concept_slug": "cross-functional-flows",
                "evidence_rule": "Passing Day 1 assessment demonstrates understanding of cross-functional enterprise workflows and document lineage.",
            },
            {
                "step_id": "d1_s8_completion",
                "step_type": "completion",
                "title": "Day 1 Complete: Cross-Functional Mastery",
                "summary_md": """### Congratulations on Completing Day 1!

You now understand:
1. The difference between isolated departmental software and integrated enterprise computing.
2. How document lineage connects Sales, Logistics, Inventory, and General Ledger.
3. How Nova Manufacturing (`NM01`) structures cross-functional customer fulfillment.

**Next Milestone**: In Day 2, you will discover the modern SAP product portfolio, comparing S/4HANA Cloud, SAP Business Technology Platform (BTP), and Signavio.""",
                "recommended_mission": {
                    "slug": "nova-purchase-flow-trace",
                    "title": "Trace a Purchase Through Nova Manufacturing",
                    "description": "Ready to apply your knowledge? Follow a real component procurement from purchase requisition to inventory balance update.",
                },
            },
        ],
    },
    2: {
        "day_number": 2,
        "slug": "modern-sap-product-portfolio",
        "title": "Modern SAP Product Portfolio",
        "subtitle": "S/4HANA, BTP, Signavio, and Cloud Deployment Models",
        "estimated_minutes": 50,
        "atomic_concepts": ["sap-portfolio-overview", "btp-positioning", "deployment-models-intro"],
        "recommended_mission_slug": "nova-sap-product-selection",
        "steps": [
            {
                "step_id": "d2_s1_learn",
                "step_type": "learn",
                "title": "The Pillars of Modern SAP Architecture",
                "content_md": """### Beyond ERP: The Modern Enterprise Portfolio

SAP is no longer just a monolithic database application. In the modern cloud era, SAP provides a coordinated ecosystem anchored by three key pillars:

1. **SAP S/4HANA (The Digital Core)**:
   The enterprise transactional engine handling Finance, Procurement, Sales, Manufacturing, and Asset Management. Powered by the in-memory SAP HANA database.
2. **SAP Business Technology Platform (BTP)**:
   The cloud innovation and integration layer. BTP is where side-by-side extensions, integration flows (iFlows), machine learning services, and custom apps run **without modifying the ERP core**.
3. **SAP Signavio (Business Process Transformation)**:
   Process intelligence suite for process mining, modeling, simulation, and governance. Signavio analyzes real operational bottlenecks before and during ERP implementation.""",
                "key_terms": [
                    {"term": "Digital Core", "definition": "The standard ERP backbone (S/4HANA) handling core financial and logistical transactions."},
                    {"term": "BTP", "definition": "Business Technology Platform: SAP's PaaS offering for extensions, integration, analytics, and AI."},
                    {"term": "Clean Core", "definition": "The architectural discipline of keeping standard ERP code unmodified by moving custom development to BTP."}
                ],
            },
            {
                "step_id": "d2_s2_understand",
                "step_type": "understand",
                "title": "Deployment Models: Public Cloud vs Private Cloud vs On-Premise",
                "content_md": """### Choosing the Right Deployment Strategy

Organizations deploy S/4HANA under three distinct models depending on customization needs and governance:

- **S/4HANA Cloud Public Edition (SaaS)**:
  - Multi-tenant shared infrastructure managed entirely by SAP.
  - Strict standard processes; continuous automated bi-annual upgrades.
  - No traditional ABAP modification allowed; 100% Clean Core.
- **S/4HANA Cloud Private Edition (Managed Cloud)**:
  - Single-tenant dedicated cloud infrastructure (on AWS, Azure, GCP, or SAP DC).
  - Maximum flexibility to migrate legacy code and customize while adhering to Clean Core governance.
  - Customer controls upgrade scheduling (annual release cycle).
- **S/4HANA On-Premise**:
  - Customer manages or hosts hardware directly in their own data center. Full infrastructure control, but highest maintenance overhead.""",
                "takeaway": "Public Cloud maximizes standardization and low TCO; Private Cloud balances cloud infrastructure benefits with enterprise customization requirements.",
            },
            {
                "step_id": "d2_s3_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing's Architecture Strategy",
                "content_md": """### Nova Manufacturing's Cloud Decisions

When Nova Manufacturing (`NM01`) upgraded from legacy ECC, the executive board faced a critical decision:
- **Core ERP**: Nova selected **S/4HANA Cloud Private Edition** because they have specialized robotics assembly routines in Heidelberg (`PL01`) that require tailored shop-floor interfaces.
- **Side-by-Side Apps**: Rather than writing custom Z-tables inside the ERP database, Nova deploys their customer IoT portal on **SAP BTP**.
- **Process Optimization**: Nova utilizes **SAP Signavio** to mine their Purchase-to-Pay process and eliminate approval bottlenecks.""",
                "company_context": {
                    "core_system": "S/4HANA Cloud Private Edition 2023",
                    "extension_platform": "SAP BTP (Cloud Foundry & Kyma)",
                    "intelligence_tool": "SAP Signavio Process Manager",
                    "architectural_mandate": "Clean Core Tier-1 Compliance",
                },
            },
            {
                "step_id": "d2_s4_practice",
                "step_type": "interactive_practice",
                "title": "Product Fit Matrix",
                "component_type": "SAPProductSelector",
                "instruction": "Match each enterprise requirement to the correct SAP product or deployment model.",
                "scenarios": [
                    {
                        "requirement": "Build a custom mobile app for field technicians to view real-time IoT sensor telemetry without touching the ERP core database.",
                        "recommended": "SAP BTP",
                        "options": ["SAP S/4HANA Core", "SAP BTP", "SAP Signavio", "SAP GUI"]
                    },
                    {
                        "requirement": "Process €50M in daily financial ledger postings, vendor payments, and inventory goods receipts.",
                        "recommended": "SAP S/4HANA Core",
                        "options": ["SAP S/4HANA Core", "SAP BTP", "SAP Signavio", "Event Mesh"]
                    },
                    {
                        "requirement": "Analyze purchase order cycle times across 10 global branches to identify hidden approval delays.",
                        "recommended": "SAP Signavio",
                        "options": ["SAP S/4HANA Core", "SAP BTP", "SAP Signavio", "SAP GUI"]
                    }
                ],
            },
            {
                "step_id": "d2_s5_challenge",
                "step_type": "challenge",
                "title": "Enterprise Scenario: The Customization Dilemma",
                "instruction": "Select the architectural approach that preserves Clean Core.",
                "scenario_md": """Nova Manufacturing's engineering team wants to integrate custom Bluetooth torque-wrench calibrations directly with shop-floor assembly orders. An external consultant proposes:
*"Let's modify standard SAP database tables and write custom ABAP code directly inside the core ERP transaction."*

As Nova's lead SAP Solutions Architect, how should you respond?""",
                "options": [
                    {
                        "id": "opt_clean",
                        "text": "Reject direct core modification. Build the Bluetooth calibration service on SAP BTP and communicate with S/4HANA using standard released APIs (Clean Core).",
                        "is_correct": True,
                        "explanation": "Correct! Clean Core ensures ERP upgrades remain effortless without breaking custom IoT hardware integrations."
                    },
                    {
                        "id": "opt_modify",
                        "text": "Approve the modification because writing code inside the core database is always fastest.",
                        "is_correct": False,
                        "explanation": "Modifying core tables creates technical debt, breaks future SAP upgrade cycles, and violates Clean Core standards."
                    },
                    {
                        "id": "opt_signavio",
                        "text": "Deploy SAP Signavio to calibrate the Bluetooth wrenches.",
                        "is_correct": False,
                        "explanation": "Signavio is for process modeling and mining, not hardware device calibration."
                    }
                ],
            },
            {
                "step_id": "d2_s6_assessment",
                "step_type": "assessment",
                "title": "Day 2 Portfolio Knowledge Check",
                "concept_slug": "sap-portfolio-overview",
                "questions": [
                    {
                        "id": "d2_q1",
                        "prompt": "What is the primary role of SAP Business Technology Platform (BTP) in a modern enterprise landscape?",
                        "options": [
                            {"id": "a", "text": "To host side-by-side extensions, integrations, and innovation without modifying the S/4HANA core", "is_correct": True},
                            {"id": "b", "text": "To replace the General Ledger and perform bank reconciliations", "is_correct": False},
                            {"id": "c", "text": "To act as a physical desktop monitor driver for SAP GUI", "is_correct": False}
                        ],
                        "explanation": "BTP is the PaaS platform enabling clean side-by-side development and API integration."
                    },
                    {
                        "id": "d2_q2",
                        "prompt": "Which deployment model guarantees strict standardization with automated continuous upgrades and zero core modifications?",
                        "options": [
                            {"id": "a", "text": "S/4HANA Cloud Public Edition", "is_correct": True},
                            {"id": "b", "text": "S/4HANA On-Premise", "is_correct": False},
                            {"id": "c", "text": "Legacy SAP R/3 4.6C", "is_correct": False}
                        ],
                        "explanation": "Public Edition is a true multi-tenant SaaS ERP enforcing 100% standard processes and automatic upgrades."
                    }
                ],
            },
            {
                "step_id": "d2_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Portfolio Skill Evidence",
                "concept_slug": "sap-portfolio-overview",
                "evidence_rule": "Passing Day 2 confirms understanding of modern SAP products, BTP extensibility, and cloud deployment tradeoffs.",
            },
            {
                "step_id": "d2_s8_completion",
                "step_type": "completion",
                "title": "Day 2 Complete: Portfolio Architect",
                "summary_md": """### You Have Mastered the SAP Product Landscape!

Key takeaways:
1. **S/4HANA** is the core transactional engine.
2. **BTP** provides side-by-side innovation while keeping the core clean.
3. **Signavio** delivers business process intelligence and journey mapping.

**Next Milestone**: In Day 3, we dive into the data layer: **Master Data Architecture** (Business Partners, Material Masters, and Bills of Materials).""",
                "recommended_mission": {
                    "slug": "nova-sap-product-selection",
                    "title": "Mission: Choose the Correct SAP Product",
                    "description": "Put your portfolio expertise to work by resolving architectural solution requests for Nova Manufacturing.",
                },
            },
        ],
    },
    3: {
        "day_number": 3,
        "slug": "master-data-architecture",
        "title": "Master Data Architecture",
        "subtitle": "Business Partners, Material Masters, and Bills of Materials (BOM)",
        "estimated_minutes": 55,
        "atomic_concepts": ["master-data-concept", "business-partner-foundations", "material-master-basics"],
        "recommended_mission_slug": "nova-purchase-flow-trace",
        "steps": [
            {
                "step_id": "d3_s1_learn",
                "step_type": "learn",
                "title": "Master Data vs Transactional Data",
                "content_md": """### The Foundations of Enterprise Consistency

In SAP, all data is partitioned into two distinct categories:

1. **Master Data**:
   The static, persistent records representing key business entities that remain in the database for years.
   - *Examples*: Business Partners (Customers, Suppliers, Employees), Material Master records, Bills of Materials (BOMs), General Ledger accounts, Fixed Assets.
   - Master data is defined once and referenced millions of times.

2. **Transactional Data**:
   Event-driven, temporary records created as business activities occur.
   - *Examples*: Purchase Order #450001, Sales Order #10022, Material Document #500019, Accounting Document #100088.
   - Every transactional document references master data for addresses, tax rules, pricing, and accounting valuation.""",
                "key_terms": [
                    {"term": "Business Partner (BP)", "definition": "Single central object in S/4HANA representing any external party (Customer, Supplier, Contact)."},
                    {"term": "Material Master", "definition": "Central repository containing all data required to purchase, manufacture, store, and sell a material."},
                    {"term": "Bill of Materials (BOM)", "definition": "Hierarchical list of raw materials, components, and assemblies needed to manufacture a product."}
                ],
            },
            {
                "step_id": "d3_s2_understand",
                "step_type": "understand",
                "title": "The S/4HANA Business Partner Revolution & Material Views",
                "content_md": """### 1. The Unified Business Partner (BP) Approach
In legacy SAP ECC, Customers (`KNA1`) and Vendors (`LFA1`) were separate tables. If a partner was both a buyer and a supplier, their contact data had to be maintained redundantly in two places.

In **SAP S/4HANA**, the **Business Partner (`BUT000`)** is mandatory:
- One single BP number represents the organization.
- **Roles** define capabilities: Role `FLCU01` (Customer for Sales), Role `FLVN01` (Supplier for Purchasing), Role `BUP003` (Employee).

### 2. Multi-View Architecture of Material Master
A material is not just a name; different departments require different data:
- **Basic Data**: Weight, dimensions, base unit of measure (e.g. PC) — valid across entire enterprise.
- **Purchasing View**: Purchasing group, order unit, delivery tolerances — valid per plant.
- **MRP/Production View**: Reorder point, safety stock, lot size — valid per plant.
- **Accounting View**: Valuation class, price control (Standard S vs Moving Average V) — valid per valuation area.""",
                "takeaway": "Master data uses organizational views: engineering defines dimensions once, while purchasing and finance maintain plant-specific parameters.",
            },
            {
                "step_id": "d3_s3_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing's Master Records",
                "content_md": """### Core Master Data at Nova Manufacturing

Take a look at how Nova Manufacturing (`NM01`) structures master data:

- **Key Supplier**: `BP-101` (*Rheinland Precision Metal GmbH*)
  - Roles: `BUP000` (General Partner), `FLVN01` (Supplier - Purchasing Org PO01), `FLVN00` (Supplier - FI NM01).
- **Key Customer**: `BP-501` (*Nordics Heavy Industrial AB*)
  - Roles: `BUP000`, `FLCU01` (Customer - Sales Org SO01), `FLCU00` (Customer - FI NM01).
- **Flagship Material**: `DXTR-1000` (Robotics Controller Assembly)
  - Material Type: `FERT` (Finished Product)
  - Valuation Class: `7920` (Finished Goods)
  - Bill of Materials (`BOM-NM-01`):
    - 1x `PCB-CTRL-88` (Main Motherboard, Semifinished `HALB`)
    - 4x `SENS-OPT-02` (Optical Sensor Module, Raw `ROH` from Supplier `BP-101`)
    - 1x `ALUM-HOUS-01` (Anodized Enclosure, Raw `ROH`)""",
                "company_context": {
                    "material_code": "DXTR-1000",
                    "material_type": "FERT (Finished Product)",
                    "bom_components": ["PCB-CTRL-88 (HALB)", "SENS-OPT-02 (ROH)", "ALUM-HOUS-01 (ROH)"],
                    "primary_supplier": "BP-101 (Rheinland Precision Metal)",
                },
            },
            {
                "step_id": "d3_s4_practice",
                "step_type": "interactive_practice",
                "title": "Master vs Transactional Data Classifier",
                "component_type": "MasterDataClassifier",
                "instruction": "Classify each business record as either Master Data or Transactional Data.",
                "items": [
                    {"id": "i1", "name": "Customer Account: Nordics Heavy Industrial (BP-501)", "type": "master", "category": "Business Partner"},
                    {"id": "i2", "name": "Purchase Order #45000291 for 500 Sensor Chips", "type": "transactional", "category": "Purchasing Document"},
                    {"id": "i3", "name": "Finished Good Record: DXTR-1000 (Controller)", "type": "master", "category": "Material Master"},
                    {"id": "i4", "name": "Goods Receipt Slip #500018 from Truck Unloading", "type": "transactional", "category": "Material Document"},
                    {"id": "i5", "name": "Bill of Materials for Robotics Assembly (BOM-NM-01)", "type": "master", "category": "Manufacturing Spec"},
                    {"id": "i6", "name": "Vendor Invoice #90014 for Raw Aluminum Stock", "type": "transactional", "category": "Financial Document"}
                ],
            },
            {
                "step_id": "d3_s5_challenge",
                "step_type": "challenge",
                "title": "Enterprise Scenario: The Supplier Role Omission",
                "instruction": "Diagnose the master data issue and pick the correct resolution.",
                "scenario_md": """Nova Manufacturing's procurement team in Heidelberg creates a new Business Partner `BP-205` (*Bavaria Sensors AG*) using general role `BUP000`.

When the buyer attempts to create Purchase Order `PO #450008` in transaction `ME21N`, the system throws an error:
`Partner BP-205 not defined for Purchasing Organization PO01`.

What caused this error and how should it be fixed?""",
                "options": [
                    {
                        "id": "opt_role",
                        "text": "The partner only has General Partner data. You must extend BP-205 with the Supplier role (FLVN01) and maintain Purchasing Organization PO01 data.",
                        "is_correct": True,
                        "explanation": "Spot on! In S/4HANA, purchasing transactions require the Supplier role (FLVN01) with purchasing organization details."
                    },
                    {
                        "id": "opt_restart",
                        "text": "Delete the entire S/4HANA database and recreate the server.",
                        "is_correct": False,
                        "explanation": "Deleting the database is absurd. S/4HANA Business Partners are designed to be extended across roles incrementally."
                    },
                    {
                        "id": "opt_bypass",
                        "text": "Bypass the error by entering the supplier's bank account number into the Purchase Order header remarks.",
                        "is_correct": False,
                        "explanation": "Free text does not satisfy database referential integrity or legal tax compliance."
                    }
                ],
            },
            {
                "step_id": "d3_s6_assessment",
                "step_type": "assessment",
                "title": "Day 3 Master Data Knowledge Check",
                "concept_slug": "master-data-concept",
                "questions": [
                    {
                        "id": "d3_q1",
                        "prompt": "What is the single mandatory entity used in SAP S/4HANA to maintain Customers, Vendors, and Employees?",
                        "options": [
                            {"id": "a", "text": "Business Partner (BP)", "is_correct": True},
                            {"id": "b", "text": "Customer Master only (KNA1)", "is_correct": False},
                            {"id": "c", "text": "Vendor Master only (LFA1)", "is_correct": False}
                        ],
                        "explanation": "S/4HANA replaced separate customer and vendor masters with the unified Business Partner (BP) model."
                    },
                    {
                        "id": "d3_q2",
                        "prompt": "Why is the Material Master divided into distinct organizational views (e.g. Basic Data, Purchasing, Accounting)?",
                        "options": [
                            {"id": "a", "text": "To allow different departments and plants to maintain localized data while sharing common core attributes", "is_correct": True},
                            {"id": "b", "text": "Because computer monitors cannot display more than four fields per screen", "is_correct": False},
                            {"id": "c", "text": "To force employees to log in from separate desktop computers", "is_correct": False}
                        ],
                        "explanation": "Views allow multi-plant enterprises to define dimensions once while assigning local prices, suppliers, and reorder policies per plant."
                    }
                ],
            },
            {
                "step_id": "d3_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Master Data Mastery Evidence",
                "concept_slug": "master-data-concept",
                "evidence_rule": "Validates understanding of master vs transactional records, the Business Partner model, and material view partitioning.",
            },
            {
                "step_id": "d3_s8_completion",
                "step_type": "completion",
                "title": "Day 3 Complete: Data Architecture",
                "summary_md": """### Outstanding Work on Day 3!

You have mastered:
1. The structural distinction between Master Data and Transactional Data.
2. S/4HANA's centralized Business Partner (BP) framework.
3. Multi-view Material Master architecture and Bills of Materials (BOMs).

**Next Milestone**: In Day 4, you will construct **Organizational Structures** (Clients, Company Codes, Plants, Storage Locations, and Sales/Purchasing Orgs).""",
                "recommended_mission": {
                    "slug": "nova-purchase-flow-trace",
                    "title": "Trace a Purchase Through the Enterprise",
                    "description": "Inspect how Nova Manufacturing's master data items are pulled into real procurement transactions.",
                },
            },
        ],
    },
    4: {
        "day_number": 4,
        "slug": "organizational-structures",
        "title": "Organizational Structures in SAP",
        "subtitle": "Client, Company Code, Plant, Storage Location, Sales & Purchasing Organizations",
        "estimated_minutes": 60,
        "atomic_concepts": [
            "org-structure-client",
            "org-structure-company-code",
            "org-structure-plant",
            "org-structure-logistics",
        ],
        "recommended_mission_slug": "nova-org-structure-design",
        "steps": [
            {
                "step_id": "d4_s1_learn",
                "step_type": "learn",
                "title": "The Enterprise Hierarchy Blueprint",
                "content_md": """### Mapping the Physical & Legal World into SAP

An SAP enterprise structure is the foundational skeleton upon which all business processes operate. Every document created belongs to specific organizational units.

The hierarchy follows a strict parent-child logic:

1. **Client (Mandant)**:
   The highest organizational unit in the SAP system. It represents the entire corporate group (e.g. Client `100`). Master records and configuration can be client-wide.
2. **Company Code (Buchungskreis)**:
   The legal entity unit for financial accounting (e.g. `NM01`). It is the smallest organizational unit for which a legally required, complete set of financial statements (Balance Sheet, P&L) can be drawn up.
3. **Plant (Werk)**:
   An operational unit for manufacturing, central warehousing, assembly, or branch distribution (e.g. `PL01`). Every Plant must be assigned to exactly one Company Code.
4. **Storage Location (Lagerort)**:
   A physical subdivision of a Plant where inventory is held (e.g. `RM01` Raw Materials, `FG01` Finished Goods).""",
                "key_terms": [
                    {"term": "Client", "definition": "Highest commercial and technical unit in SAP (self-contained data and environment)."},
                    {"term": "Company Code", "definition": "Independent financial entity with complete Balance Sheet and Profit & Loss."},
                    {"term": "Plant", "definition": "Logistical location for manufacturing, storing, and distributing materials."},
                    {"term": "Purchasing Organization", "definition": "Legal purchasing unit negotiating contracts and pricing with suppliers."}
                ],
            },
            {
                "step_id": "d4_s2_understand",
                "step_type": "understand",
                "title": "Logistical vs Financial Organizational Units",
                "content_md": """### How Logistics Connects to Finance

A critical concept in SAP architecture is the relationship between **Logistics (MM/SD/PP)** and **Finance (FI/CO)**:

- **Financial Units**:
  - `Company Code`: Dictates currency (e.g. EUR), chart of accounts (e.g. YCOA), and fiscal year variant (e.g. K4).
  - A multi-national corporation will have multiple Company Codes (e.g. `NM01` Germany, `NM02` USA).
- **Logistical Units**:
  - `Plants` handle physical operations.
  - `Purchasing Organizations` can be **cross-company code**, **company-code-specific**, or **plant-specific**.
  - `Sales Organizations` belong directly to a Company Code and distribute goods through Distribution Channels and Divisions (Sales Area).

When a goods movement occurs at Plant `PL01`, SAP looks up which Company Code owns `PL01` and posts the financial debit/credit automatically to that Company Code's general ledger!""",
                "takeaway": "Plants are logistical; Company Codes are financial. Every physical plant MUST assign to a company code so goods movements can be valued financially.",
            },
            {
                "step_id": "d4_s3_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing's Org Chart",
                "content_md": """### The Real Architecture of Nova Manufacturing

Let us examine the complete organizational configuration for Nova Manufacturing:

- **Client**: `100` (Production Tenant)
- **Company Code**: `NM01` (*Nova Manufacturing AG*, Heidelberg, Currency: EUR)
- **Assigned Plants**:
  - `PL01`: *Heidelberg Main Assembly & R&D* (Germany)
    - Storage Locations: `RM01` (Raw Materials), `FG01` (Finished Goods), `SP01` (Spare Parts)
  - `PL02`: *Austin High-Tech Facility* (Texas, USA - owned by NM01)
    - Storage Locations: `RM01` (Inbound Staging), `FG01` (Distribution Bay)
- **Purchasing**:
  - `PO01`: *Global Purchasing Org* (Assigned to both `PL01` and `PL02` for global volume pricing)
- **Sales**:
  - `SO01`: *Direct Enterprise Sales* (Assigned to Company Code `NM01`)""",
                "company_context": {
                    "client": "100",
                    "company_code": "NM01",
                    "plants": ["PL01 (Heidelberg)", "PL02 (Austin)"],
                    "purchasing_org": "PO01 (Global)",
                    "sales_org": "SO01 (Enterprise)",
                },
            },
            {
                "step_id": "d4_s4_practice",
                "step_type": "interactive_practice",
                "title": "Build the Enterprise Hierarchy",
                "component_type": "OrgStructureMapper",
                "instruction": "Assemble the valid organizational hierarchy for Nova Manufacturing. Arrange the units in the proper parent-child relationship.",
                "units": [
                    {"id": "u1", "code": "Client 100", "type": "client", "level": 1, "description": "Corporate Group Level"},
                    {"id": "u2", "code": "Company Code NM01", "type": "company_code", "level": 2, "parent": "u1", "description": "Legal Financial Entity (EUR)"},
                    {"id": "u3", "code": "Plant PL01", "type": "plant", "level": 3, "parent": "u2", "description": "Heidelberg Manufacturing Plant"},
                    {"id": "u4", "code": "Plant PL02", "type": "plant", "level": 3, "parent": "u2", "description": "Austin High-Tech Facility"},
                    {"id": "u5", "code": "SLoc FG01", "type": "storage_location", "level": 4, "parent": "u3", "description": "Finished Goods Warehouse"},
                    {"id": "u6", "code": "Purchasing Org PO01", "type": "purchasing_org", "level": 3, "parent": "u2", "description": "Centralized Procurement Org"}
                ],
            },
            {
                "step_id": "d4_s5_challenge",
                "step_type": "challenge",
                "title": "Enterprise Scenario: The Plant Assignment Mistake",
                "instruction": "Identify the organizational violation in the proposed architecture.",
                "scenario_md": """A junior consultant submits a new Customizing proposal for Nova Manufacturing:
*"To simplify accounting for the new Austin facility, we will create Plant PL02 under Client 100, but leave it unassigned to Company Code NM01. We will link it directly to Purchasing Org PO01 only."*

Why will the SAP S/4HANA system reject this configuration during testing?""",
                "options": [
                    {
                        "id": "opt_cc_mandatory",
                        "text": "Every Plant must be assigned to exactly one Company Code. Without a Company Code assignment, SAP cannot determine the currency, chart of accounts, or valuation area for inventory accounting.",
                        "is_correct": True,
                        "explanation": "Spot on! Inventory has financial value. When a plant receives stock, SAP must know which Company Code ledger to post the asset to."
                    },
                    {
                        "id": "opt_color",
                        "text": "Plants cannot operate in North America if the company code is European.",
                        "is_correct": False,
                        "explanation": "False. A company code can own plants internationally, subject to tax and branch accounting configurations."
                    },
                    {
                        "id": "opt_limit",
                        "text": "SAP S/4HANA only supports one single plant per client.",
                        "is_correct": False,
                        "explanation": "False. An enterprise can have hundreds of plants across global company codes."
                    }
                ],
            },
            {
                "step_id": "d4_s6_assessment",
                "step_type": "assessment",
                "title": "Day 4 Org Structure Knowledge Check",
                "concept_slug": "org-structure-company-code",
                "questions": [
                    {
                        "id": "d4_q1",
                        "prompt": "What is the smallest organizational unit in SAP S/4HANA for which a complete, legal set of financial books (Balance Sheet and P&L) can be drawn up?",
                        "options": [
                            {"id": "a", "text": "Company Code", "is_correct": True},
                            {"id": "b", "text": "Plant", "is_correct": False},
                            {"id": "c", "text": "Storage Location", "is_correct": False}
                        ],
                        "explanation": "The Company Code is the primary legal reporting unit in Financial Accounting (FI)."
                    },
                    {
                        "id": "d4_q2",
                        "prompt": "How does a centralized Purchasing Organization (e.g. PO01) differ from a plant-specific purchasing organization?",
                        "options": [
                            {"id": "a", "text": "A centralized purchasing org can procure materials for multiple plants across the enterprise to negotiate volume discounts", "is_correct": True},
                            {"id": "b", "text": "A centralized purchasing org is only allowed to buy office stationery", "is_correct": False},
                            {"id": "c", "text": "A centralized purchasing org does not require any supplier master data", "is_correct": False}
                        ],
                        "explanation": "Centralized purchasing orgs assign to multiple plants to aggregate purchasing volume and secure better vendor pricing."
                    }
                ],
            },
            {
                "step_id": "d4_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Org Structure Skill Evidence",
                "concept_slug": "org-structure-company-code",
                "evidence_rule": "Validates understanding of SAP organizational modeling, entity relationships, and legal financial boundaries.",
            },
            {
                "step_id": "d4_s8_completion",
                "step_type": "completion",
                "title": "Day 4 Complete: Enterprise Org Architect",
                "summary_md": """### Masterful Work on Day 4!

You have mastered:
1. The organizational hierarchy: Client → Company Code → Plant → Storage Location.
2. The role of Purchasing and Sales Organizations.
3. How Nova Manufacturing (`NM01`) structures European and US operations.

**Companion Missions Unlocked!**
You are now fully prepared to tackle:
- **Mission 1**: *Design Nova Manufacturing's Organizational Structure*
- **Mission 2**: *Nova Manufacturing Opens Plant PL02*""",
                "recommended_mission": {
                    "slug": "nova-plant-expansion",
                    "title": "Mission: Nova Manufacturing Opens Plant PL02",
                    "description": "Configure the complete enterprise integration for Nova's Austin facility, assigning plants, storage locations, and purchasing orgs.",
                },
            },
        ],
    },
    5: {
        "day_number": 5,
        "slug": "module-interconnectivity",
        "title": "Module Interconnectivity",
        "subtitle": "Real-Time Integration across FI/CO, MM, SD, and PP",
        "estimated_minutes": 55,
        "atomic_concepts": ["module-interconnectivity", "automatic-account-determination"],
        "recommended_mission_slug": "nova-purchase-flow-trace",
        "steps": [
            {
                "step_id": "d5_s1_learn",
                "step_type": "learn",
                "title": "The Magic of Automatic Postings",
                "content_md": """### Cross-Module Touchpoints

In traditional non-ERP companies, when a warehouse clerk unloads a delivery of raw materials, accounting has no idea until a paper invoice arrives weeks later.

In SAP S/4HANA, modules communicate **synchronously via transactional events**:

- **MM (Materials Management)**: Manages procurement, purchase orders, and physical goods receipts.
- **FI (Financial Accounting)**: Manages statutory ledgers, accounts payable, accounts receivable, and balance sheets.
- **SD (Sales & Distribution)**: Manages quotations, sales orders, delivery picking, and customer billing.
- **PP (Production Planning)**: Manages bills of materials, work centers, and factory production orders.

When a warehouse worker confirms Goods Receipt (transaction `MIGO`) in MM, the system **automatically triggers financial accounting entries in FI** without human intervention!""",
                "key_terms": [
                    {"term": "Automatic Account Determination", "definition": "SAP configuration rules that determine which General Ledger accounts are debited/credited based on transaction keys."},
                    {"term": "GR/IR Clearing Account", "definition": "Goods Receipt / Invoice Receipt: A temporary clearing account balancing physical stock receipts against vendor invoices."},
                    {"term": "Synchronous Posting", "definition": "Simultaneous creation of material documents and accounting documents within the same database commit."}
                ],
            },
            {
                "step_id": "d5_s2_understand",
                "step_type": "understand",
                "title": "How the GR/IR Clearing Account Operates",
                "content_md": """### The P2P Two-Step Financial Balance

A classic interview and operational question is: **Why does SAP use a GR/IR account?**

In procurement, the physical goods and the supplier invoice almost never arrive at the same second:

1. **Step 1: Goods Receipt (MIGO)**
   - Physical components arrive at Plant `PL01`.
   - Inventory value increases: **Debit Inventory Account (Balance Sheet Asset)**.
   - But we haven't received or verified the invoice yet! Who do we owe?
   - SAP posts a liability offset: **Credit GR/IR Clearing Account (Liability)**.

2. **Step 2: Invoice Verification (MIRO)**
   - The invoice arrives from Supplier `BP-101`.
   - We verify the invoice matches the purchase order and goods receipt.
   - SAP clears the temporary liability: **Debit GR/IR Clearing Account**.
   - And recognizes the official debt: **Credit Vendor Accounts Payable (AP)**.

When both steps finish, the GR/IR balance is exactly **€0.00**, inventory is properly capitalized, and the vendor is paid on time!""",
                "takeaway": "The GR/IR clearing account guarantees that inventory is valued immediately upon arrival while tracking un-invoiced liabilities accurately.",
            },
            {
                "step_id": "d5_s3_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: A Live Component Receipt",
                "content_md": """### Inside Plant PL01: Receiving Optical Sensors

Watch what happens inside Nova Manufacturing (`NM01`) when shipment arrives:

1. **Purchasing**: Buyer issues `PO #450010` to *Rheinland Precision Metal (`BP-101`)* for 100 units of `SENS-OPT-02` at €50/unit (€5,000 total).
2. **Receiving (MM)**: Warehouse clerk at Heidelberg logs `MIGO` with movement type `101` (Goods Receipt into Plant `PL01`, SLoc `RM01`).
3. **Synchronous FI Commit**:
   - `Debit`: Inventory - Raw Materials (`BSX` account `140000`): **+€5,000**
   - `Credit`: GR/IR Clearing Account (`WRX` account `211000`): **-€5,000**
4. **Invoice (FI/MM)**: Accounting enters invoice in `MIRO`.
   - `Debit`: GR/IR Clearing Account (`WRX`): **+€5,000** (clearing line!)
   - `Credit`: Vendor `BP-101` Accounts Payable (`KBS`): **-€5,000**""",
                "company_context": {
                    "po_number": "PO #450010",
                    "material": "SENS-OPT-02 (Optical Sensor)",
                    "value": "€5,000.00",
                    "gl_inventory": "140000 (Raw Materials)",
                    "gl_grir": "211000 (GR/IR Clearing)",
                },
            },
            {
                "step_id": "d5_s4_practice",
                "step_type": "interactive_practice",
                "title": "Cross-Module Document Flow Visualizer",
                "component_type": "ModuleInteractionVisualizer",
                "instruction": "Click between Purchase-to-Pay (MM/FI) and Order-to-Cash (SD/FI) to see which documents and general ledger accounts are touched at each phase.",
                "scenarios": [
                    {
                        "module_pair": "MM → FI (Procurement)",
                        "events": [
                            {"event": "Purchase Order", "modules": ["MM"], "gl_impact": "None (Commitment only)"},
                            {"event": "Goods Receipt (MIGO)", "modules": ["MM", "FI"], "gl_impact": "Debit Inventory / Credit GR-IR"},
                            {"event": "Invoice Receipt (MIRO)", "modules": ["MM", "FI"], "gl_impact": "Debit GR-IR / Credit Accounts Payable"}
                        ]
                    },
                    {
                        "module_pair": "SD → FI (Sales)",
                        "events": [
                            {"event": "Sales Order", "modules": ["SD"], "gl_impact": "None (No financial transaction yet)"},
                            {"event": "Post Goods Issue (PGI)", "modules": ["SD", "MM", "FI"], "gl_impact": "Debit COGS / Credit Finished Goods"},
                            {"event": "Customer Billing (VF01)", "modules": ["SD", "FI"], "gl_impact": "Debit Customer AR / Credit Sales Revenue"}
                        ]
                    }
                ],
            },
            {
                "step_id": "d5_s5_challenge",
                "step_type": "challenge",
                "title": "Enterprise Scenario: The Price Variance Anomaly",
                "instruction": "Identify how SAP resolves price differences between PO and Invoice.",
                "scenario_md": """Nova Manufacturing creates a Purchase Order for specialized aluminum casings at €100/unit.
1. Goods Receipt (`MIGO`) is posted for 10 units:
   - Debit Inventory: €1,000
   - Credit GR/IR: €1,000
2. When the vendor's invoice arrives (`MIRO`), the vendor billed €110/unit (€1,100 total) due to unexpected shipping surcharges.

How does SAP S/4HANA reconcile this €100 discrepancy if the material uses standard price control?""",
                "options": [
                    {
                        "id": "opt_prv",
                        "text": "SAP clears the GR/IR account for €1,000, credits Vendor AP for €1,100, and automatically posts the €100 difference to a Price Variance (PRD) expense account.",
                        "is_correct": True,
                        "explanation": "Correct! Automatic account determination routes purchase price variances (PRD) to an expense account to keep standard inventory cost stable."
                    },
                    {
                        "id": "opt_fail",
                        "text": "The SAP system crashes and locks all database tables until the buyer writes a paper check.",
                        "is_correct": False,
                        "explanation": "False. Price variances are a normal part of business and handled cleanly by automatic account determination."
                    },
                    {
                        "id": "opt_delete",
                        "text": "The warehouse manager deletes the Goods Receipt document to match the invoice.",
                        "is_correct": False,
                        "explanation": "Never delete physical inventory records. Document flow preserves exact historical audit trails."
                    }
                ],
            },
            {
                "step_id": "d5_s6_assessment",
                "step_type": "assessment",
                "title": "Day 5 Module Integration Knowledge Check",
                "concept_slug": "module-interconnectivity",
                "questions": [
                    {
                        "id": "d5_q1",
                        "prompt": "Which temporary clearing account balances physical warehouse receipts against vendor invoices in the Purchase-to-Pay process?",
                        "options": [
                            {"id": "a", "text": "GR/IR (Goods Receipt / Invoice Receipt) Clearing Account", "is_correct": True},
                            {"id": "b", "text": "Petty Cash Account", "is_correct": False},
                            {"id": "c", "text": "Customer Bad Debt Reserve", "is_correct": False}
                        ],
                        "explanation": "The GR/IR account holds interim liability until the vendor invoice arrives and matches the receipt."
                    },
                    {
                        "id": "d5_q2",
                        "prompt": "What mechanism enables SAP to determine General Ledger debit and credit accounts automatically without manual entry by warehouse workers?",
                        "options": [
                            {"id": "a", "text": "Automatic Account Determination (configured via transaction keys like BSX, WRX, PRD)", "is_correct": True},
                            {"id": "b", "text": "Random coin toss in the application server", "is_correct": False},
                            {"id": "c", "text": "Warehouse workers typing GL account numbers by memory on every receipt", "is_correct": False}
                        ],
                        "explanation": "Automatic Account Determination uses Valuation Class, Chart of Accounts, and Movement Type to determine accounts automatically."
                    }
                ],
            },
            {
                "step_id": "d5_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Module Interconnectivity Evidence",
                "concept_slug": "module-interconnectivity",
                "evidence_rule": "Validates understanding of cross-module integration triggers, automatic accounting postings, and the GR/IR clearing cycle.",
            },
            {
                "step_id": "d5_s8_completion",
                "step_type": "completion",
                "title": "Day 5 Complete: Integration Specialist",
                "summary_md": """### Brilliant Progress! Day 5 is Complete!

You now understand:
1. How MM, SD, PP, and FI integrate in real-time.
2. The role and lifecycle of the GR/IR Clearing Account.
3. How Automatic Account Determination generates accounting lines seamlessly.

**Recommended Mission**: Test your procurement tracing skills in *Trace a Purchase Through Nova Manufacturing*!""",
                "recommended_mission": {
                    "slug": "nova-purchase-flow-trace",
                    "title": "Mission: Trace a Purchase Through the Enterprise",
                    "description": "Follow the complete information and document lineage from requisition to invoice settlement inside Nova Manufacturing.",
                },
            },
        ],
    },
    6: {
        "day_number": 6,
        "slug": "technical-architecture-foundations",
        "title": "Technical Architecture Foundations",
        "subtitle": "Three-Tier Client-Server Architecture, Work Processes, and SAP Gateway",
        "estimated_minutes": 60,
        "atomic_concepts": ["three-tier-architecture", "abap-work-processes", "sap-gateway-concept"],
        "recommended_mission_slug": "nova-architecture-layer-incident",
        "steps": [
            {
                "step_id": "d6_s1_learn",
                "step_type": "learn",
                "title": "The Classic Three-Tier Architecture",
                "content_md": """### Separation of Concerns at Scale

SAP S/4HANA is built on a proven **Three-Tier Client-Server Architecture** designed to support tens of thousands of concurrent users with zero data corruption:

1. **Presentation Layer (Tier 1)**:
   The user interface. In modern S/4HANA, this is the **SAP Fiori Launchpad** running in web browsers or mobile devices (HTML5/SAPUI5), alongside classical **SAP GUI** on Windows/macOS. It handles rendering and user input.
2. **Application Layer (Tier 2 - AS ABAP)**:
   The brains of the system. The Application Server ABAP executes business logic, runs authorization checks, orchestrates database transactions, and manages **Work Processes**.
3. **Database Layer (Tier 3 - SAP HANA)**:
   The persistence engine. SAP HANA stores all transactional tables, master data, and indexes entirely **in-memory** in columnar format, executing complex analytical aggregations in milliseconds.""",
                "key_terms": [
                    {"term": "Three-Tier Architecture", "definition": "Separation of Presentation, Application Logic, and Database persistence into distinct scalable layers."},
                    {"term": "Work Process (WP)", "definition": "An independent operating system process in AS ABAP dedicated to executing specific tasks (Dialog, Background, Update, Spool)."},
                    {"term": "SAP Gateway", "definition": "Component in AS ABAP exposing business data as standard OData/REST services for web and mobile frontends."}
                ],
            },
            {
                "step_id": "d6_s2_understand",
                "step_type": "understand",
                "title": "ABAP Work Process Types Demystified",
                "content_md": """### Inside the Application Server: The Work Process Dispatcher

When hundreds of employees in Heidelberg and Austin perform tasks simultaneously, how does the Application Server handle them without crashing?

The AS ABAP uses a **Dispatcher** that assigns user requests to a pool of specialized **Work Processes (WPs)**:

- **Dialog (DIA)**: Handles interactive user screen requests. To prevent system freezing, DIA processes enforce a strict timeout (e.g. 300 seconds).
- **Background (BGD)**: Executes long-running batch jobs (e.g. nightly depreciation runs, mass billing, MRP calculation). No screen timeouts.
- **Update (UPD/UPD2)**: Executes critical database commits asynchronously, ensuring that large financial writes don't block the user's interactive screen.
- **Spool (SPO)**: Manages output printing, barcode generation, and document formatting.
- **Enqueue (ENQ)**: Manages logical application lock table in memory, preventing two users from editing the same sales order simultaneously.""",
                "takeaway": "Work processes isolate tasks: fast interactive screens run in DIA; heavy data calculations run safely in BGD without impacting responsive users.",
            },
            {
                "step_id": "d6_s3_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing's Landscape Tiers",
                "content_md": """### A Request Flowing Through Nova's Infrastructure

Imagine Nova's plant manager in Austin (`PL02`) opening the "Monitor Stock" app:

1. **Tier 1 (Presentation)**: The iPad browser makes an HTTPS OData request to the SAP Fiori Launchpad.
2. **SAP Web Dispatcher**: Distributes the incoming HTTPS call to the fastest available ABAP application server.
3. **Tier 2 (Application Layer)**:
   - **SAP Gateway** receives the OData request.
   - Dispatcher assigns a **Dialog (DIA)** work process.
   - Business authorization checks confirm the user has access to Plant `PL02`.
4. **Tier 3 (Database Layer)**:
   - The application server sends a SQL query to the **SAP HANA Database**.
   - HANA reads columnar tables in memory and returns aggregated stock in 4 milliseconds.
5. **Response**: The DIA process formats the JSON OData payload, and Fiori updates the iPad screen.""",
                "company_context": {
                    "company_name": "Nova Manufacturing Corp",
                    "code": "NM01",
                    "presentation": "SAP Fiori on iOS & Chrome (HTTPS)",
                    "gateway": "SAP Gateway (OData V4)",
                    "app_server": "AS ABAP 2023 (Linux Cluster)",
                    "database": "SAP HANA 2.0 SPS07 In-Memory Engine",
                },
            },
            {
                "step_id": "d6_s4_practice",
                "step_type": "interactive_practice",
                "title": "Architecture Layer Diagnostics",
                "component_type": "ArchitectureLayerMapper",
                "instruction": "Diagnose each enterprise scenario and identify which architectural tier or work process is responsible.",
                "scenarios": [
                    {
                        "issue": "A user complains: 'When I click Save on a 500-line invoice, my browser says Connection Refused before anything displays.'",
                        "layer": "Presentation / Network Tier",
                        "options": ["Presentation / Network Tier", "Application Layer (AS ABAP)", "Database Layer (SAP HANA)"]
                    },
                    {
                        "issue": "A nightly MRP run calculates material requirements for 40,000 components across Heidelberg and Austin without any user logged in.",
                        "layer": "Application Layer (Background BGD Work Process)",
                        "options": ["Application Layer (Dialog DIA Work Process)", "Application Layer (Background BGD Work Process)", "Presentation Layer (SAP GUI)"]
                    },
                    {
                        "issue": "A custom analytical report running complex multi-table aggregations experiences high memory consumption and columnar index merges.",
                        "layer": "Database Layer (SAP HANA Engine)",
                        "options": ["Presentation Layer", "Application Layer", "Database Layer (SAP HANA Engine)"]
                    }
                ],
            },
            {
                "step_id": "d6_s5_challenge",
                "step_type": "challenge",
                "title": "Enterprise Scenario: The Freezing Dialog Process",
                "instruction": "Select the correct architectural fix for the long-running job.",
                "scenario_md": """A financial controller at Nova Manufacturing writes a complex ad-hoc report. They execute it interactively in transaction `SE38` during peak business hours.
After 300 seconds, their screen terminates with the runtime error:
`TIME_OUT: Maximum dialog runtime exceeded`.

The controller asks you to increase the Dialog timeout to 2 hours for all users.

How should you solve this problem properly?""",
                "options": [
                    {
                        "id": "opt_bgd",
                        "text": "Reject increasing Dialog timeout. Instruct the controller to schedule the heavy report as a Background Job (BGD work process in SM36/SM37), which has no dialog timeout.",
                        "is_correct": True,
                        "explanation": "Correct! Dialog processes are reserved for interactive user screens. Long-running reports must execute in Background work processes."
                    },
                    {
                        "id": "opt_infinite",
                        "text": "Set Dialog timeout to infinite, allowing interactive screens to freeze user workstations all day.",
                        "is_correct": False,
                        "explanation": "Infinite dialog timeouts cause thread starvation, locking up application servers for all other employees."
                    },
                    {
                        "id": "opt_browser",
                        "text": "Tell the user to upgrade their home Wi-Fi router.",
                        "is_correct": False,
                        "explanation": "The error was triggered by AS ABAP server safety limits, not home Wi-Fi."
                    }
                ],
            },
            {
                "step_id": "d6_s6_assessment",
                "step_type": "assessment",
                "title": "Day 6 Technical Architecture Knowledge Check",
                "concept_slug": "three-tier-architecture",
                "questions": [
                    {
                        "id": "d6_q1",
                        "prompt": "In the SAP Three-Tier Architecture, which layer is responsible for executing business logic and orchestrating work processes?",
                        "options": [
                            {"id": "a", "text": "Application Layer (AS ABAP)", "is_correct": True},
                            {"id": "b", "text": "Presentation Layer (SAP Fiori / GUI)", "is_correct": False},
                            {"id": "c", "text": "Database Layer (SAP HANA)", "is_correct": False}
                        ],
                        "explanation": "The Application Server ABAP executes business rules and program logic."
                    },
                    {
                        "id": "d6_q2",
                        "prompt": "Which ABAP work process type is specifically designated to execute long-running batch processing tasks without interactive timeouts?",
                        "options": [
                            {"id": "a", "text": "Background (BGD)", "is_correct": True},
                            {"id": "b", "text": "Dialog (DIA)", "is_correct": False},
                            {"id": "c", "text": "Spool (SPO)", "is_correct": False}
                        ],
                        "explanation": "Background (BGD) work processes execute asynchronous, scheduled jobs without screen runtime limits."
                    }
                ],
            },
            {
                "step_id": "d6_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Technical Architecture Evidence",
                "concept_slug": "three-tier-architecture",
                "evidence_rule": "Validates understanding of 3-tier architecture, work process allocation, and SAP Gateway communication.",
            },
            {
                "step_id": "d6_s8_completion",
                "step_type": "completion",
                "title": "Day 6 Complete: Systems Architect",
                "summary_md": """### Exceptional Work! Day 6 is Complete!

You have mastered:
1. The Three-Tier Architecture (Presentation, Application, Database).
2. Work Process Dispatching (DIA, BGD, UPD, SPO, ENQ).
3. How SAP Gateway and Web Dispatcher connect modern web clients to HANA.

**Recommended Mission**: Tackle *Mission 5: Enterprise Architecture Incident* to diagnose cross-tier incidents under simulated job conditions!""",
                "recommended_mission": {
                    "slug": "nova-architecture-layer-incident",
                    "title": "Mission: Enterprise Architecture Incident",
                    "description": "Step into the role of a systems engineer to diagnose whether a high-priority outage originates in UI, Application, or Database.",
                },
            },
        ],
    },
    7: {
        "day_number": 7,
        "slug": "sap-gui-vs-fiori-launchpad",
        "title": "SAP GUI vs Fiori Launchpad",
        "subtitle": "Comparing Classic Transaction Codes with Modern Role-Based Enterprise UX",
        "estimated_minutes": 50,
        "atomic_concepts": ["sap-gui-navigation", "fiori-launchpad-overview"],
        "recommended_mission_slug": "nova-architecture-layer-incident",
        "steps": [
            {
                "step_id": "d7_s1_learn",
                "step_type": "learn",
                "title": "The UX Evolution: Classic Dynpro to Modern Fiori",
                "content_md": """### Two Windows into the Same Enterprise Core

For over three decades, the primary interface to SAP was **SAP GUI** (Graphical User Interface). While immensely powerful for power users, classic SAP GUI was technical, intimidating, and required desktop software installation.

With **SAP S/4HANA**, the standard user interface is **SAP Fiori**:

- **SAP GUI (Classic)**:
  - Navigated via **Transaction Codes (T-Codes)** like `VA01` (Create Sales Order), `ME21N` (Create Purchase Order), `FB01` (Post Document).
  - Dense screens with hundreds of fields across dozens of tabs.
  - Desktop-only protocol (DIAG / RFC).
- **SAP Fiori (Modern)**:
  - Navigated via role-based **Fiori Launchpad** in any web browser or mobile device.
  - Role-based: a warehouse worker only sees tiles relevant to receiving and picking.
  - Built on open web standards: HTML5, CSS3, JavaScript (**SAPUI5**), and RESTful **OData** services.""",
                "key_terms": [
                    {"term": "Transaction Code (T-Code)", "definition": "A 4-20 character shortcut in SAP GUI that directly launches an ABAP dynpro program (e.g. MIGO, ME21N)."},
                    {"term": "Fiori Launchpad", "definition": "The browser-based shell organizing business apps into spaces, pages, and dynamic tiles based on the user's role."},
                    {"term": "SAPUI5", "definition": "SAP's enterprise JavaScript framework for building responsive, cross-device HTML5 web applications."}
                ],
            },
            {
                "step_id": "d7_s2_understand",
                "step_type": "understand",
                "title": "The Three Fiori Application Types",
                "content_md": """### Fiori Application Archetypes

Not all Fiori applications are identical. In modern S/4HANA, Fiori apps are organized into three primary architectural types:

1. **Transactional Apps**:
   - Designed for task execution (e.g. "Create Purchase Order", "Approve Leave Request").
   - Emphasize simple, guided forms, barcode scanning, and direct CRUD operations.
2. **Analytical Apps**:
   - Provide real-time operational insights (e.g. "Days Sales Outstanding", "Net Working Capital Overview").
   - Driven directly by HANA Core Data Services (CDS) analytical queries with visual charts and drilldown.
3. **Fact Sheets / Object Pages**:
   - Display a 360-degree overview of a central business entity (e.g. "Customer 360", "Material DXTR-1000 Overview").
   - Enable users to navigate contextual links between related documents effortlessly.""",
                "takeaway": "Fiori replaces massive multi-purpose screens with contextual, role-tailored apps that work seamlessly across phones, tablets, and laptops.",
            },
            {
                "step_id": "d7_s3_example",
                "step_type": "visual_example",
                "title": "Nova Manufacturing: A Tale of Two Personas",
                "content_md": """### Who Uses What at Nova Manufacturing?

At Nova Manufacturing (`NM01`), different personas utilize the interface best suited for their job:

- **Persona 1: Marcus (Senior Cost Controller, Heidelberg)**
  - *Primary Interface*: **SAP GUI**
  - *Why*: Marcus runs heavy period-end closing transactions (`CKMLCP` Material Ledger Costing Cockpit, `F.01` Balance Sheet). He prefers high keyboard shortcut density and sub-second multi-window Dynpro switching.
- **Persona 2: Sarah (Warehouse Team Lead, Austin PL02)**
  - *Primary Interface*: **SAP Fiori Launchpad on Rugged Android Tablet**
  - *Why*: Sarah walks the warehouse floor inspecting deliveries. She uses the Fiori "Post Goods Receipt for Inbound Delivery" app with camera barcode scanning and large touch buttons.""",
                "company_context": {
                    "power_user_interface": "SAP GUI 8.0 (Windows/Mac)",
                    "mobile_workforce_interface": "SAP Fiori Launchpad (SAPUI5 / HTTPS)",
                    "design_philosophy": "Role-based productivity matching the user's daily environment",
                },
            },
            {
                "step_id": "d7_s4_practice",
                "step_type": "interactive_practice",
                "title": "UX Recommendation Matrix",
                "component_type": "ScenarioDecision",
                "instruction": "Evaluate the user persona and select whether SAP GUI or SAP Fiori is the optimal recommendation.",
                "scenarios": [
                    {
                        "persona": "Executive VP of Supply Chain traveling between European branches wanting real-time KPI dashboards on an iPad.",
                        "recommendation": "SAP Fiori Launchpad (Analytical Dashboard App)",
                        "reasoning": "Fiori is browser-based, touch-responsive, and leverages real-time HANA analytical queries directly."
                    },
                    {
                        "persona": "Senior Basis Administrator configuring low-level background job schedules and SAP transport routes.",
                        "recommendation": "SAP GUI (Transaction STMS, SM37, SM50)",
                        "reasoning": "Technical administration requires deep system dynpros that remain native to classic GUI tools."
                    },
                    {
                        "persona": "Shop floor assembler confirming finished assembly of DXTR-1000 with a quick barcode scan at Plant PL01.",
                        "recommendation": "SAP Fiori Launchpad (Transactional Touch App)",
                        "reasoning": "Simple, focused task screen that eliminates distracting accounting fields and works on tablet touchscreens."
                    }
                ],
            },
            {
                "step_id": "d7_s5_challenge",
                "step_type": "challenge",
                "title": "Enterprise Scenario: The T-Code Dilemma",
                "instruction": "Explain the architectural evolution from T-Codes to Fiori Semantic Objects.",
                "scenario_md": """A veteran procurement clerk at Nova Manufacturing protests against the Fiori rollout:
*"I have memorized transaction code ME21N for 20 years. Fiori has no transaction codes! How can I possibly be as fast?"*

How do you explain the Fiori navigation concept to reassure the clerk?""",
                "options": [
                    {
                        "id": "opt_semantic",
                        "text": "In Fiori, users navigate by intent (Semantic Object + Action, like 'PurchaseOrder-create'), but the Launchpad search bar STILL allows typing classic T-codes like ME21N to launch the exact app immediately.",
                        "is_correct": True,
                        "explanation": "Correct! Fiori Launchpad search supports classic T-codes directly, allowing veterans to use shortcuts while modernizing UX."
                    },
                    {
                        "id": "opt_force",
                        "text": "Tell the clerk that memory is obsolete and they must click through 50 folders each morning.",
                        "is_correct": False,
                        "explanation": "Fiori is designed to improve speed, not degrade it. The global search bar provides instant app launching."
                    },
                    {
                        "id": "opt_cancel",
                        "text": "Cancel the entire S/4HANA rollout and revert the company to paper ledgers.",
                        "is_correct": False,
                        "explanation": "Reverting to paper is not an enterprise strategy."
                    }
                ],
            },
            {
                "step_id": "d7_s6_assessment",
                "step_type": "assessment",
                "title": "Day 7 UX Knowledge Check",
                "concept_slug": "sap-gui-navigation",
                "questions": [
                    {
                        "id": "d7_q1",
                        "prompt": "What design principle distinguishes SAP Fiori from classic SAP GUI?",
                        "options": [
                            {"id": "a", "text": "Fiori is role-based, responsive across devices, and built on open web standards (SAPUI5/OData)", "is_correct": True},
                            {"id": "b", "text": "Fiori requires users to install heavy C++ desktop client executables on every laptop", "is_correct": False},
                            {"id": "c", "text": "Fiori only works if the computer has a floppy disk drive", "is_correct": False}
                        ],
                        "explanation": "Fiori is role-based, responsive, and runs in modern browsers using SAPUI5 and OData."
                    },
                    {
                        "id": "d7_q2",
                        "prompt": "Which type of Fiori application leverages in-memory HANA queries to provide real-time KPI charts and operational drilldowns?",
                        "options": [
                            {"id": "a", "text": "Analytical Apps", "is_correct": True},
                            {"id": "b", "text": "Transactional Dynpros", "is_correct": False},
                            {"id": "c", "text": "Legacy Spool Files", "is_correct": False}
                        ],
                        "explanation": "Analytical apps run directly on HANA CDS views to render interactive charts and business KPIs."
                    }
                ],
            },
            {
                "step_id": "d7_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "UX Evaluation Evidence",
                "concept_slug": "sap-gui-navigation",
                "evidence_rule": "Validates understanding of SAP GUI transaction shortcuts, Fiori design principles, and role-based UX selection.",
            },
            {
                "step_id": "d7_s8_completion",
                "step_type": "completion",
                "title": "Day 7 Complete: Enterprise UX Specialist",
                "summary_md": """### Phenomenal Achievement!

You have mastered:
1. The architectural differences between classic SAP GUI and modern SAP Fiori.
2. The three Fiori application archetypes (Transactional, Analytical, Fact Sheet).
3. How to position UX tools effectively based on user roles and task requirements.

**Next Milestone**: Day 8 is the **Foundations Capstone & Assessment**! You will solve an integrated enterprise challenge for Nova Manufacturing synthesizing all 7 days!""",
                "recommended_mission": {
                    "slug": "nova-architecture-layer-incident",
                    "title": "Mission: Enterprise Architecture Incident",
                    "description": "Diagnose presentation vs application vs database tier incidents before stepping into the Day 8 Capstone!",
                },
            },
        ],
    },
    8: {
        "day_number": 8,
        "slug": "foundation-capstone-assessment",
        "title": "Foundation Capstone & Comprehensive Assessment",
        "subtitle": "Synthesizing Architecture, Master Data, Org Structure & Integration for Nova Manufacturing",
        "estimated_minutes": 75,
        "atomic_concepts": [
            "erp-foundations-synthesis",
            "org-structure-company-code",
            "master-data-concept",
            "module-interconnectivity",
            "three-tier-architecture",
            "sap-portfolio-overview",
            "sap-gui-navigation",
        ],
        "recommended_mission_slug": "nova-plant-expansion",
        "steps": [
            {
                "step_id": "d8_s1_learn",
                "step_type": "learn",
                "title": "The Phase 1 Capstone Challenge",
                "content_md": """### Synthesizing Phase 1: Enterprise Architecture & ERP Foundations

Over the last 7 days, you have explored the foundational pillars of enterprise computing:
1. **Day 1**: Enterprise Systems & Cross-Functional Workflows
2. **Day 2**: Modern SAP Product Portfolio (S/4HANA, BTP, Signavio, Cloud Models)
3. **Day 3**: Master Data Architecture (Business Partners, Materials, BOMs)
4. **Day 4**: Organizational Structures (Client, Company Code, Plants, SLocs, POrgs)
5. **Day 5**: Module Interconnectivity & Automatic Postings (MM, SD, PP, FI)
6. **Day 6**: Technical Three-Tier Architecture (Presentation, App Server, HANA)
7. **Day 7**: Enterprise UX (SAP GUI vs Fiori Launchpad)

In this Capstone, you step in as **Lead SAP Enterprise Architect** for Nova Manufacturing Corp (`NM01`) during their transatlantic expansion. You will evaluate end-to-end integration scenarios, make architectural decisions, and sit for the Phase 1 benchmark evaluation.""",
                "key_terms": [
                    {"term": "Enterprise Synthesis", "definition": "Connecting organizational hierarchy, master data, cross-module integration, and technical tiers into a unified operational solution."},
                    {"term": "Clean Core Extensibility", "definition": "Ensuring business adaptations run side-by-side on BTP to keep the S/4HANA core upgradable."},
                    {"term": "Multi-Dimensional Evaluation", "definition": "Scoring distinct architectural competencies individually to detect targeted knowledge gaps."}
                ],
            },
            {
                "step_id": "d8_s2_understand",
                "step_type": "understand",
                "title": "Capstone Business Scenario: The Transatlantic Expansion",
                "content_md": """### Nova Manufacturing's High-Stakes Project

Nova Manufacturing (`NM01`) has approved a major initiative:
- **Operational Goal**: Open Plant `PL02` in Austin, Texas to assemble the new `IOT-GATEWAY-200` product line for the North American market.
- **Supply Chain**: Raw sensors (`SENS-OPT-02`) will be sourced centrally using global supplier agreements.
- **Logistics**: Completed gateways will be warehoused locally in Austin and shipped to US robotics integrators.
- **Architecture Mandate**: All shop-floor workers will use mobile tablets. No custom code may be written inside the S/4HANA core. Financial closing must consolidate seamlessly into the Heidelberg General Ledger.

As the architect, every decision you make touches Org Structure, Master Data, Module Integration, UX, and Technical Infrastructure simultaneously.""",
                "takeaway": "Real enterprise architecture is holistic: changing an organizational assignment impacts master data views, document flows, and financial balance sheets.",
            },
            {
                "step_id": "d8_s3_example",
                "step_type": "visual_example",
                "title": "The End-to-End Solution Blueprint",
                "content_md": """### The Architectural Blueprint

Review the validated architecture blueprint for Nova's expansion:

```
[ Corporate Client 100 ]
           │
  [ Company Code NM01 ] (Heidelberg, EUR)
     ┌─────┴────────────────────────────────┐
     ▼                                      ▼
[ Plant PL01 ] (Heidelberg)           [ Plant PL02 ] (Austin, TX)
  ├── SLoc RM01 (Raw)                   ├── SLoc RM01 (Inbound)
  ├── SLoc FG01 (Finished)              └── SLoc FG01 (Distribution)
  └── SLoc SP01 (Spares)
     ▲                                      ▲
     └──────────────┬───────────────────────┘
                    │
       [ Purchasing Org PO01 ] (Global Centralized)
                    │
         [ Vendor BP-101 ] (Rheinland Precision)
```

- **Document Flow**:
  1. PO created in `PO01` for Plant `PL02`.
  2. Supplier ships components; Plant `PL02` posts `MIGO`.
  3. System automatically debits Inventory and credits GR/IR in Company Code `NM01`.
  4. Austin warehouse confirms dispatch on Fiori touch tablet.""",
                "company_context": {
                    "project": "Nova Transatlantic Expansion",
                    "target_plant": "PL02 (Austin)",
                    "company_code": "NM01",
                    "core_material": "IOT-GATEWAY-200",
                },
            },
            {
                "step_id": "d8_s4_practice",
                "step_type": "interactive_practice",
                "title": "Multi-Tier Architecture & Process Synthesis",
                "component_type": "OrgStructureMapper",
                "instruction": "Review the full Nova Manufacturing model before taking the Phase 1 Capstone Exam.",
                "units": [
                    {"id": "u1", "code": "Client 100", "type": "client", "level": 1, "description": "Global Enterprise Group"},
                    {"id": "u2", "code": "Company Code NM01", "type": "company_code", "level": 2, "parent": "u1", "description": "Nova Manufacturing AG (EUR)"},
                    {"id": "u3", "code": "Plant PL01", "type": "plant", "level": 3, "parent": "u2", "description": "Heidelberg Main Assembly"},
                    {"id": "u4", "code": "Plant PL02", "type": "plant", "level": 3, "parent": "u2", "description": "Austin High-Tech Facility"},
                    {"id": "u5", "code": "Purchasing Org PO01", "type": "purchasing_org", "level": 3, "parent": "u2", "description": "Centralized Cross-Plant Procurement"},
                    {"id": "u6", "code": "Sales Org SO01", "type": "sales_org", "level": 3, "parent": "u2", "description": "Direct Enterprise Sales"}
                ],
            },
            {
                "step_id": "d8_s5_challenge",
                "step_type": "challenge",
                "title": "Capstone Synthesis Decision",
                "instruction": "Evaluate the architectural conflict and make the executive recommendation.",
                "scenario_md": """During the final go-live review of Plant PL02, three department heads disagree on how to handle custom IoT assembly diagnostics:

- **Factory Supervisor**: *"Let's build it directly into SAP GUI so our engineers in Austin can run classic transactions."*
- **External Contractor**: *"Let's write direct SQL scripts against the SAP HANA database tables."*
- **Enterprise Architect (You)**: *"What is the correct S/4HANA Clean Core strategy?"*""",
                "options": [
                    {
                        "id": "opt_capstone_clean",
                        "text": "Build a responsive SAP Fiori app deployed on SAP BTP that communicates with S/4HANA via standard OData APIs. This keeps the core clean and supports shop-floor mobile tablets.",
                        "is_correct": True,
                        "explanation": "Correct! This combines Clean Core BTP extensibility, modern Fiori mobile UX, and safe API integration."
                    },
                    {
                        "id": "opt_capstone_db",
                        "text": "Write direct SQL scripts into the HANA database, bypassing the Application Server completely.",
                        "is_correct": False,
                        "explanation": "Direct database updates bypass business authorizations, enqueue locks, and audit trails, corrupting database consistency."
                    },
                    {
                        "id": "opt_capstone_manual",
                        "text": "Have workers record assembly parameters on paper clipboards and mail them to Heidelberg monthly.",
                        "is_correct": False,
                        "explanation": "Paper mailings eliminate real-time supply chain transparency."
                    }
                ],
            },
            {
                "step_id": "d8_s6_assessment",
                "step_type": "assessment",
                "title": "Phase 1 Foundations Capstone Benchmark Exam",
                "is_capstone": True,
                "multi_concept_eval": True,
                "concepts_evaluated": [
                    "org-structure-company-code",
                    "master-data-concept",
                    "module-interconnectivity",
                    "three-tier-architecture",
                    "sap-portfolio-overview",
                    "sap-gui-navigation",
                ],
                "questions": [
                    {
                        "id": "cap_q1",
                        "concept_slug": "org-structure-company-code",
                        "prompt": "Which statement correctly describes the relationship between Company Codes and Plants in SAP S/4HANA?",
                        "options": [
                            {"id": "a", "text": "Every Plant must be assigned to exactly one Company Code to ensure all physical goods movements have legal financial valuation.", "is_correct": True},
                            {"id": "b", "text": "A Plant can exist independently without assigning to any Company Code.", "is_correct": False},
                            {"id": "c", "text": "A single Plant can belong to four different Company Codes simultaneously without any intercompany configuration.", "is_correct": False}
                        ],
                        "explanation": "Every logistical plant must be owned by a financial company code for inventory accounting."
                    },
                    {
                        "id": "cap_q2",
                        "concept_slug": "master-data-concept",
                        "prompt": "In S/4HANA, how is an entity that acts as both a parts supplier and an equipment customer modeled?",
                        "options": [
                            {"id": "a", "text": "As a single central Business Partner (BP) assigned both Customer (FLCU01) and Supplier (FLVN01) roles", "is_correct": True},
                            {"id": "b", "text": "By duplicating their profile across two completely different SAP server instances", "is_correct": False},
                            {"id": "c", "text": "By deleting their record and creating an ad-hoc purchase order each time", "is_correct": False}
                        ],
                        "explanation": "The unified Business Partner object maintains one master record with multiple functional roles."
                    },
                    {
                        "id": "cap_q3",
                        "concept_slug": "module-interconnectivity",
                        "prompt": "When a warehouse team posts Goods Receipt (MIGO) for purchased stock, which account temporarily balances the inventory increase before the invoice arrives?",
                        "options": [
                            {"id": "a", "text": "GR/IR (Goods Receipt / Invoice Receipt) Clearing Account", "is_correct": True},
                            {"id": "b", "text": "Sales Revenue Account", "is_correct": False},
                            {"id": "c", "text": "Customer Accounts Receivable", "is_correct": False}
                        ],
                        "explanation": "GR/IR clearing accounts maintain interim liability until invoice verification (MIRO)."
                    },
                    {
                        "id": "cap_q4",
                        "concept_slug": "three-tier-architecture",
                        "prompt": "Why are long-running analytical calculations or mass batch jobs assigned to Background (BGD) work processes instead of Dialog (DIA)?",
                        "options": [
                            {"id": "a", "text": "To prevent interactive Dialog work processes from exceeding screen runtime limits (e.g. 300s timeout) and blocking interactive users", "is_correct": True},
                            {"id": "b", "text": "Because Dialog processes only work when the computer monitor is turned off", "is_correct": False},
                            {"id": "c", "text": "Because Background jobs delete the database after running", "is_correct": False}
                        ],
                        "explanation": "Dialog processes enforce timeouts to protect interactive responsiveness; batch jobs run safely in BGD processes."
                    },
                    {
                        "id": "cap_q5",
                        "concept_slug": "sap-portfolio-overview",
                        "prompt": "What is the primary architectural benefit of developing custom applications on SAP BTP rather than modifying S/4HANA core tables?",
                        "options": [
                            {"id": "a", "text": "Clean Core: S/4HANA upgrades can be performed seamlessly without breaking side-by-side custom applications", "is_correct": True},
                            {"id": "b", "text": "It guarantees that the company will never need an internet connection", "is_correct": False},
                            {"id": "c", "text": "It allows employees to bypass corporate cybersecurity firewalls", "is_correct": False}
                        ],
                        "explanation": "Side-by-side development on BTP guarantees Clean Core compliance and friction-free ERP upgrades."
                    },
                    {
                        "id": "cap_q6",
                        "concept_slug": "sap-gui-navigation",
                        "prompt": "Which SAP user interface archetype provides role-based, responsive mobile access and is built on SAPUI5 and OData services?",
                        "options": [
                            {"id": "a", "text": "SAP Fiori Launchpad", "is_correct": True},
                            {"id": "b", "text": "Classic SAP GUI for Windows Dynpro", "is_correct": False},
                            {"id": "c", "text": "MS-DOS Command Prompt", "is_correct": False}
                        ],
                        "explanation": "SAP Fiori is the modern role-based web/mobile UX for S/4HANA."
                    }
                ],
            },
            {
                "step_id": "d8_s7_evidence",
                "step_type": "mastery_evidence",
                "title": "Phase 1 Capstone Multi-Concept Evidence",
                "concept_slug": "erp-foundations-synthesis",
                "evidence_rule": "Each concept evaluated in the Capstone updates its respective SAPUserConceptMastery moving average and records first-class SAPSkillEvidence.",
            },
            {
                "step_id": "d8_s8_completion",
                "step_type": "completion",
                "title": "Phase 1 Complete: Certified Foundations Enterprise Engineer",
                "summary_md": """### 🏆 Phase 1 Milestone Accomplished!

You have successfully completed **Enterprise Architecture & ERP Foundations (Days 1–8)**!

You possess validated proficiency in:
- Cross-Functional Document Lineage (Order-to-Cash & Purchase-to-Pay)
- Modern SAP Product Portfolio (S/4HANA, BTP, Signavio, Cloud Editions)
- Master Data Architecture (Business Partners, Material Masters, BOMs)
- Organizational Modeling (Client, Company Code, Plant, SLoc, POrg, SOrg)
- Module Interconnectivity & Automatic Account Determination (GR/IR)
- Three-Tier Client-Server Architecture & Work Processes
- SAP Fiori vs Classic SAP GUI

**Coming Next**: Phase 2 (Days 9–22) introduces **S/4HANA Fundamentals & Data Architecture**—diving deep into the in-memory columnar HANA engine, the Universal Journal (`ACDOCA`), `MATDOC`, and Core Data Services (CDS)!""",
                "recommended_mission": {
                    "slug": "nova-plant-expansion",
                    "title": "Final Phase 1 Challenge: Nova Plant Expansion",
                    "description": "Solidify your Phase 1 credentials by completing the multi-step Austin Plant PL02 enterprise integration mission!",
                },
            },
        ],
    },
}

# Merge Phase 2 (Days 9–22)
try:
    from app.data.sap_lessons_phase2 import PHASE_2_DAYS_CONTENT
    SAP_DAYS_CONTENT.update(PHASE_2_DAYS_CONTENT)
except ImportError:
    pass

# Merge Phase 3 (Days 23–44)
try:
    from app.data.sap_lessons_phase3 import PHASE_3_DAYS_CONTENT
    SAP_DAYS_CONTENT.update(PHASE_3_DAYS_CONTENT)
except ImportError:
    pass

# Merge Phase 4 (Days 45–54)
try:
    from app.data.sap_lessons_phase4 import PHASE_4_DAYS_CONTENT
    SAP_DAYS_CONTENT.update(PHASE_4_DAYS_CONTENT)
except ImportError:
    pass



