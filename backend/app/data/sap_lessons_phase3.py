"""Authoritative content definitions for SAP S/4HANA Guided Learning Days 23–44 (Phase 3).

Phase 3: Core End-to-End Business Processes (P2P, O2C, Finance, Inventory & Manufacturing).

Curriculum Map:
23 Procure-to-Pay: P2P Overview
24 Procure-to-Pay: Purchase Requisition & Sourcing
25 Procure-to-Pay: Purchase Orders
26 Procure-to-Pay: Goods Receipt
27 Procure-to-Pay: Invoice Verification / 3-Way Match
28 Procure-to-Pay: P2P Exceptions & Troubleshooting
29 Order-to-Cash: O2C Overview
30 Order-to-Cash: Sales Orders
31 Order-to-Cash: ATP / aATP
32 Order-to-Cash: Delivery, Picking & PGI
33 Order-to-Cash: Billing + FI Integration
34 Order-to-Cash: O2C Exceptions & Troubleshooting
35 Finance: General Ledger
36 Finance: Accounts Payable
37 Finance: Accounts Receivable
38 Finance: Financial Close
39 Inventory Management
40 Manufacturing Fundamentals
41 Production Execution
42 WIP / Variance / Cost Settlement
43 Integrated Cross-Module Enterprise Case
44 Practical Multi-Concept Capstone (19 distinct concept evaluations)

Enterprise Continuous Model: Nova Manufacturing Corp (NM01)
- Plants: PL01 (Heidelberg Assembly), PL02 (Austin Tech Center)
- Purchasing Org: PO01, Sales Org: SO01
- Storage Locations: RAW1 (Raw Materials), FG01 (Finished Goods)
- Master Materials: RAW-01 (Optical Sensor Array), DXTR-1000 (Industrial Robotics Controller)
- Business Partners: VEND-101 (Rheinland Precision Optics), CUST-501 (Nordics Heavy Industrial AB)

Technical Truthfulness Invariants Enforced:
- PGI (Mov 601) records physical dispatch and Cost of Goods Sold; it does NOT record sales revenue.
- Billing (VF01) is the authoritative trigger for Revenue, Output Tax, and Accounts Receivable recognition.
- Accounts 131000, 211200, 211000, 500000, 410000, 530000 are simulation examples, not universal SAP standards.
- Movement 261 records component consumption against the production order cost collector, not simply termed "WIP".
"""

from __future__ import annotations
from typing import Any

PHASE_3_DAYS_CONTENT: dict[int, dict[str, Any]] = {
    23: {   'atomic_concepts': ['p2p-pr-creation', 'account-assignment-categories'],
    'day_number': 23,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-p2p-workflow-incident',
    'slug': 'p2p-overview',
    'steps': [   {   'content_md': '### End-to-End Enterprise Procurement\n'
                                   'In SAP S/4HANA, the **Procure-to-Pay (P2P)** business cycle coordinates the '
                                   'end-to-end fulfillment of operational and strategic material demand across '
                                   'Materials Management (MM), Inventory Management, and Financial Accounting (FI).\n'
                                   '\n'
                                   'The standard P2P process spans six primary phases:\n'
                                   '1. **Demand Determination & Requisition**: Internal department or MRP identifies '
                                   'demand (`Purchase Requisition` in table `EBAN`).\n'
                                   '2. **Operational Sourcing**: Supplier identification, Requests for Quotation '
                                   '(RFQ), and quotation analysis.\n'
                                   '3. **Purchase Order Processing**: Creation of legal commitment to supplier '
                                   '(`EKKO`/`EKPO`).\n'
                                   '4. **Goods Receipt**: Physical receipt into warehouse with inventory and GR/IR '
                                   'postings (table `MATDOC`).\n'
                                   '5. **Logistics Invoice Verification**: 3-way matching of PO, GR, and supplier '
                                   'invoice in transaction `MIRO` (table `RBKP`).\n'
                                   '6. **Payment & Clearing**: Automated payment run in `F110` clearing vendor '
                                   'liability in `ACDOCA`.\n'
                                   '\n'
                                   '### Organizational Structure in Procurement\n'
                                   'Procurement activities execute across a defined organizational hierarchy:\n'
                                   '- **Client**: Enterprise group level.\n'
                                   '- **Company Code (e.g. NM01)**: Financial entity with independent balance sheet.\n'
                                   '- **Plant (e.g. PL01 Heidelberg, PL02 Austin)**: Operational facility where '
                                   'inventory is held.\n'
                                   '- **Purchasing Organization (e.g. PO01)**: Commercial unit negotiating vendor '
                                   'terms and pricing contracts.\n'
                                   '- **Purchasing Group**: Tactical buyer team responsible for operational day-to-day '
                                   'purchasing.',
                     'key_terms': [   {   'definition': 'End-to-end process from requisitioning goods to supplier '
                                                        'payment.',
                                          'term': 'Procure-to-Pay (P2P)'},
                                      {   'definition': 'Organizational unit responsible for procuring materials and '
                                                        'negotiating contracts.',
                                          'term': 'Purchasing Organization'},
                                      {   'definition': 'Audit trail linking Requisition -> PO -> GR -> Invoice -> '
                                                        'Payment in S/4HANA.',
                                          'term': 'Document Flow'}],
                     'step_id': 'd23_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'P2P connects operational demand to financial disbursement across MM and FI, '
                                 'enforcing cross-functional auditability.',
                     'title': 'The Procure-to-Pay (P2P) Lifecycle Overview'},
                 {   'content_md': '### Transactional Document Chain & Data Architecture\n'
                                   'Unlike fragmented legacy ERPs, SAP S/4HANA provides instantaneous visibility into '
                                   'the procurement chain:\n'
                                   '- Requisition (`EBAN`) creates internal commitment.\n'
                                   '- Purchase Order (`EKKO`/`EKPO`) establishes legal terms with Business Partner '
                                   '(`LFA1`/`BUT000`).\n'
                                   '- Goods Receipt generates a Material Document (`MATDOC`) and synchronously creates '
                                   'Universal Journal entries in `ACDOCA`.\n'
                                   '- Invoice Verification updates `RBKP`/`RSEG` and balances the GR/IR interim '
                                   'clearing account.\n'
                                   '\n'
                                   '### The GR/IR Interim Clearing Principle\n'
                                   'In enterprise procurement, goods receipt and invoice receipt rarely happen '
                                   'simultaneously:\n'
                                   '- **Goods Receipt (MIGO)**: The company receives physical inventory before '
                                   'receiving the bill.\n'
                                   '  - Debit: Inventory Asset (e.g. Account 131000 in Nova simulation model)\n'
                                   '  - Credit: GR/IR Interim Clearing (e.g. Account 211200 in Nova simulation model)\n'
                                   '- **Invoice Verification (MIRO)**: The supplier invoice arrives and is matched '
                                   'against the PO and GR.\n'
                                   '  - Debit: GR/IR Interim Clearing (e.g. Account 211200)\n'
                                   '  - Credit: Vendor Accounts Payable (e.g. Account 211000)\n'
                                   '\n'
                                   '*Note: Account numbers 131000, 211200, and 211000 are Nova Manufacturing Corp '
                                   'simulation chart of accounts examples, not universal SAP constants.*',
                     'key_terms': [   {   'definition': 'Provisional balance sheet clearing account bridging physical '
                                                        'receipt and financial invoice.',
                                          'term': 'GR/IR Clearing Account'},
                                      {   'definition': 'Universal material document table storing single-record '
                                                        'inventory movements in S/4HANA.',
                                          'term': 'MATDOC'}],
                     'step_id': 'd23_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'The GR/IR account ensures inventory is capitalized upon receipt without prematurely '
                                 'recording accounts payable.',
                     'title': 'Cross-Functional Architecture & Accounting Principles'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'material': 'RAW-01',
                                            'plant': 'PL01',
                                            'purchasing_org': 'PO01',
                                            'vendor': 'VEND-101'},
                     'content_md': '### Walkthrough: The 6-Stage P2P Trace\n'
                                   '1. **Demand**: Production engineer submits PR #10004500 for 200 EA RAW-01.\n'
                                   '2. **Sourcing**: Purchasing Org PO01 selects certified vendor VEND-101 (Rheinland '
                                   'Precision Optics) at €120.00/EA.\n'
                                   '3. **PO**: PO #4500018900 is approved via S/4HANA Flexible Workflow.\n'
                                   '4. **Goods Receipt**: Warehouse clerk posts MIGO Mov 101 into Storage Location '
                                   'RAW1. Inventory increases by 200 EA; GR/IR interim liability credited for '
                                   '€24,000.\n'
                                   '5. **Invoice**: AP receives Invoice #5105600100 for €24,000. MIRO 3-way match '
                                   'succeeds; GR/IR clears to €0; Vendor AP credited.\n'
                                   '6. **Payment**: Automatic Payment Program F110 clears Vendor AP via SEPA bank '
                                   'transfer.',
                     'scenario': 'Nova Manufacturing Corp (NM01) requires 200 units of Optical Sensor Array RAW-01 for '
                                 'robotic controller assembly at Plant PL01 (Heidelberg).',
                     'step_id': 'd23_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing P2P Scenario: Optical Sensor Procurement'},
                 {   'component_type': 'P2PFlow',
                     'instruction': 'Click each stage of the Procure-to-Pay lifecycle to trace documents, '
                                    'organizational owners, and financial impact.',
                     'step_id': 'd23_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Notice how every logistics action synchronously triggers or clears a financial '
                                 'accounting entry.',
                     'title': '[SIMULATION MODEL] Interactive P2P Process Flow Navigator'},
                 {   'instruction': 'Select the correct organizational configuration and governance strategy.',
                     'options': [   {   'explanation': 'Correct! A cross-plant purchasing organization can procure for '
                                                       'multiple plants within a company code, centralizing vendor '
                                                       'negotiations.',
                                        'id': 'opt_cross_plant_po',
                                        'is_correct': True,
                                        'text': 'Yes, configure PO01 as a cross-plant Purchasing Organization assigned '
                                                'to Company Code NM01 and both plants PL01 and PL02 to maximize volume '
                                                'discounts.'},
                                    {   'explanation': 'Incorrect. Purchasing Organizations are assigned at Plant or '
                                                       'Company Code levels, never at Storage Location level.',
                                        'id': 'opt_po_per_sloc',
                                        'is_correct': False,
                                        'text': 'No, SAP requires every storage location to have its own independent '
                                                'Purchasing Organization.'},
                                    {   'explanation': 'Incorrect. Plant-level assignment is standard SAP '
                                                       'architecture.',
                                        'id': 'opt_po_client_only',
                                        'is_correct': False,
                                        'text': 'No, Purchasing Organizations cannot be assigned to plants in '
                                                'S/4HANA.'}],
                     'scenario': 'Nova Manufacturing has two plants: PL01 (Heidelberg) and PL02 (Austin). Management '
                                 'asks whether Purchasing Organization PO01 can negotiate contracts for both plants.',
                     'step_id': 'd23_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Procurement Architecture & Governance Challenge'},
                 {   'questions': [   {   'concept_slug': 'p2p-pr-creation',
                                          'explanation': 'A PR is strictly an internal request; only a Purchase Order '
                                                         'creates an external legal commitment.',
                                          'id': 'd23_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'It is an internal demand document that '
                                                                     'communicates requirements to purchasing without '
                                                                     'creating external legal liability.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'It is an external legal contract signed by the '
                                                                     'vendor.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'It posts an immediate debit to Accounts Payable '
                                                                     'in ACDOCA.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'It triggers automatic bank payment execution.'}],
                                          'prompt': 'What is the primary architectural purpose of a Purchase '
                                                    'Requisition (PR) in SAP S/4HANA?',
                                          'question_id': 'd23_q1'},
                                      {   'concept_slug': 'account-assignment-categories',
                                          'explanation': "AAC 'K' directs the purchase to a cost center expense rather "
                                                         'than balance sheet inventory stock.',
                                          'id': 'd23_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': "Account Assignment Category 'K' (Cost Center), "
                                                                     'requiring a Cost Center and G/L expense '
                                                                     'account.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Blank AAC (Standard Warehouse Inventory).'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Customer Account Group 0001.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Sales Distribution Channel 10.'}],
                                          'prompt': 'When ordering consumable supplies directly for factory '
                                                    'maintenance overhead rather than warehouse stock, which Account '
                                                    'Assignment Category (AAC) is typically selected?',
                                          'question_id': 'd23_q2'}],
                     'step_id': 'd23_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 23 Mastery Assessment: P2P Architecture'},
                 {   'step_id': 'd23_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Understood the 6-stage P2P lifecycle from Requisition to Payment.\n'
                                   '- Mapped procurement organizational units (Client, Company Code, Plant, Purchasing '
                                   'Org, Purchasing Group).\n'
                                   '- Traced document and accounting linkages across EBAN, EKKO, MATDOC, RBKP, and '
                                   'ACDOCA.',
                     'title': 'Mastery Verification: P2P Process & Document Flow'},
                 {   'recommended_mission': {   'description': 'Resolve a high-priority procurement block for factory '
                                                               'maintenance tools at Plant PL01.',
                                                'slug': 'nova-p2p-workflow-incident',
                                                'title': 'Procure-to-Pay Workflow & Account Assignment Incident'},
                     'step_id': 'd23_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered the foundational architecture of Procure-to-Pay in SAP S/4HANA. '
                                   'Next, you will explore Purchase Requisitions and Operational Sourcing.',
                     'title': 'Day 23 Complete: P2P Overview Mastered'}],
    'subtitle': 'End-to-end procurement lifecycle from requisition to invoice clearing across MM, Inventory, and FI',
    'title': 'Procure-to-Pay: P2P Overview'},
    24: {   'atomic_concepts': ['p2p-sourcing-rfq', 'source-determination'],
    'day_number': 24,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-sourcing-rfq-decision',
    'slug': 'p2p-requisition-sourcing',
    'steps': [   {   'content_md': '### Operational Demand Capture\n'
                                   'In SAP S/4HANA, the **Purchase Requisition (PR)** records internal demand. '
                                   'Requisitions originate either automatically via **MRP Live** (Material '
                                   'Requirements Planning) when stock levels drop below safety thresholds, or manually '
                                   'via the Fiori app **Create Purchase Requisition**.\n'
                                   '\n'
                                   '### Account Assignment Categories (AAC)\n'
                                   'The Account Assignment Category dictates where the cost of the requested item is '
                                   'posted:\n'
                                   '- **Blank (Standard Stock)**: Materials with a master record (e.g. `RAW-01`) '
                                   'received into inventory stock (Storage Location `RAW1`) as a balance sheet asset.\n'
                                   '- **K (Cost Center)**: Consumable materials or operational expenses debited to a '
                                   'cost center (e.g., `CC-MAINT-01`) upon goods receipt.\n'
                                   '- **P (Project)**: Earmarked for a Work Breakdown Structure (WBS) element in '
                                   'project systems.\n'
                                   '- **A (Asset)**: Capital expenditures assigned to an Asset Accounting fixed asset '
                                   'record.\n'
                                   '- **F (Order)**: Assigned to an internal order or production order.',
                     'key_terms': [   {   'definition': 'Code specifying cost destination (Cost Center, Asset, '
                                                        'Project) for purchased items.',
                                          'term': 'Account Assignment Category (AAC)'},
                                      {   'definition': 'HANA-optimized in-memory material requirements planning '
                                                        'engine.',
                                          'term': 'MRP Live'}],
                     'step_id': 'd24_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'AAC determines whether a purchase capitalizes as inventory or expenses immediately '
                                 'to a cost object.',
                     'title': 'Purchase Requisitions & Account Assignment Categories'},
                 {   'content_md': '### Sourcing & Source Determination\n'
                                   'Once a requisition is approved, purchasing identifies the optimal supplier through '
                                   '**Source Determination**:\n'
                                   '1. **Source List**: Master record maintaining authorized suppliers for a material '
                                   'at a plant.\n'
                                   '2. **Purchasing Info Record (PIR)**: Master data establishing price, lead time, '
                                   'tax code, and tolerance limits between a specific supplier and material.\n'
                                   '3. **Outline Agreements**: Long-term contracts or scheduling agreements.\n'
                                   '\n'
                                   '### Requests for Quotation (RFQ) & Effective Landed Cost\n'
                                   'When no valid contract exists, buyers issue **Requests for Quotation (RFQ)** to '
                                   'multiple vendors.\n'
                                   'Comparing bids requires calculating the **Effective Landed Cost**:\n'
                                   '$$\\text{Effective Unit Cost} = \\text{Gross Price} - \\text{Discounts} + '
                                   '\\text{Freight Surcharges} + \\text{Customs Duties}$$\n'
                                   '\n'
                                   'Incoterms directly dictate cost responsibility:\n'
                                   '- **DDP (Delivered Duty Paid)**: Seller pays freight and customs duties.\n'
                                   '- **EXW (Ex Works)**: Buyer pays freight and customs clearance surcharges.',
                     'key_terms': [   {   'definition': 'Relationship master record storing agreed price, lead times, '
                                                        'and tolerances with a vendor.',
                                          'term': 'Purchasing Info Record (PIR)'},
                                      {   'definition': 'True landed cost per unit factoring in discounts, freight, '
                                                        'and duties.',
                                          'term': 'Effective Price'}],
                     'step_id': 'd24_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Effective landed cost accounts for Incoterms and freight; the lowest gross quotation '
                                 'is not always the cheapest.',
                     'title': 'Source Determination, RFQ & Landed Cost Analysis'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'material': 'RAW-01',
                                            'plant': 'PL01'},
                     'content_md': '### Landed Cost Comparison Analysis\n'
                                   '- **Vendor A**: €100.00 base + €15.00 freight + €5.00 duty = **€120.00 / EA**.\n'
                                   '- **Vendor B (VEND-101)**: €110.00 base - €2.20 (2% discount) + €0 freight + €0 '
                                   'duty = **€107.80 / EA**.\n'
                                   '\n'
                                   'Vendor B delivers a lower effective landed cost despite a higher initial headline '
                                   'bid.',
                     'scenario': 'Nova needs 500 units of precision lenses. Two suppliers bid: Vendor A offers €100 '
                                 'EXW (+€15 freight + 5% duty); Vendor B (VEND-101) offers €110 DDP with a 2% '
                                 'prompt-payment cash discount.',
                     'step_id': 'd24_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Sourcing Decision: Sensor Procurement'},
                 {   'component_type': 'ScenarioDecision',
                     'instruction': 'Evaluate the requisition requirements and supplier quotation parameters to '
                                    'determine the compliant operational action.',
                     'options': [   {   'explanation': 'Correct! Vendor B offers the lowest effective landed cost of '
                                                       '€107.80/EA.',
                                        'id': 'opt_d24_award',
                                        'is_correct': True,
                                        'text': 'Award contract to Vendor B (VEND-101) under Incoterms DDP, and create '
                                                'Purchasing Info Record with agreed terms.'},
                                    {   'explanation': 'Incorrect! Ignores freight and customs duties which drive '
                                                       'total cost to €120.00/EA.',
                                        'id': 'opt_d24_gross',
                                        'is_correct': False,
                                        'text': 'Award to Vendor A because €100.00 is numerically smaller than '
                                                '€110.00.'},
                                    {   'explanation': 'Increases administrative overhead and unit costs.',
                                        'id': 'opt_d24_split',
                                        'is_correct': False,
                                        'text': 'Split order equally between both vendors ignoring freight costs.'}],
                     'step_id': 'd24_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Always evaluate total landed cost including Incoterms and freight.',
                     'title': '[SIMULATION MODEL] Sourcing & Requisition Decision Drill'},
                 {   'instruction': 'Identify the architectural error and proper resolution.',
                     'options': [   {   'explanation': 'Correct! Non-stock maintenance consumables must be assigned to '
                                                       "AAC 'K' and expensed directly.",
                                        'id': 'opt_d24_c1',
                                        'is_correct': True,
                                        'text': "Change Account Assignment Category to 'K' (Cost Center), specify "
                                                'maintenance Cost Center CC-MAINT-01 and G/L 541000 (Maintenance '
                                                'Supplies Expense).'},
                                    {   'explanation': 'Incorrect. Account 121000 is for customer sales receivables.',
                                        'id': 'opt_d24_c2',
                                        'is_correct': False,
                                        'text': 'Assign Customer AR reconciliation account 121000.'},
                                    {   'explanation': 'Absurd choice.',
                                        'id': 'opt_d24_c3',
                                        'is_correct': False,
                                        'text': 'Delete the conveyor belt from the plant.'}],
                     'scenario': 'A factory supervisor submits a PR for replacement conveyor belts. They leave the '
                                 'Account Assignment Category blank, but the warehouse refuses to stock them as '
                                 'standard inventory.',
                     'step_id': 'd24_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Requisition Account Assignment Challenge'},
                 {   'questions': [   {   'concept_slug': 'p2p-sourcing-rfq',
                                          'explanation': 'Effective price accounts for all landed cost components: '
                                                         'freight, duties, and discounts.',
                                          'id': 'd24_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Gross Price minus discounts, plus freight '
                                                                     'surcharges and applicable customs duties.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Gross Price alone without considering '
                                                                     'transportation or import tariffs.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'The price stored in the material master standard '
                                                                     'price field.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'The historical invoice price from the prior '
                                                                     'fiscal year.'}],
                                          'prompt': 'When evaluating competing supplier quotations under different '
                                                    'Incoterms (e.g. EXW vs DDP), how is effective price determined?',
                                          'question_id': 'd24_q1'},
                                      {   'concept_slug': 'source-determination',
                                          'explanation': 'The Purchasing Info Record stores the specific commercial '
                                                         'relationship parameters between a vendor and a material.',
                                          'id': 'd24_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Purchasing Info Record (PIR).'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Customer Material Info Record.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Field Status Group.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Cost Center Master.'}],
                                          'prompt': 'Which master data record defines the vendor-material specific '
                                                    'conditions such as agreed price, minimum order quantity, and lead '
                                                    'time?',
                                          'question_id': 'd24_q2'}],
                     'step_id': 'd24_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 24 Mastery Assessment: Requisitions & Sourcing'},
                 {   'step_id': 'd24_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Configured Account Assignment Categories (Blank vs K vs P vs A).\n'
                                   '- Evaluated operational sourcing strategies using Purchasing Info Records and '
                                   'Source Lists.\n'
                                   '- Computed effective landed prices factoring in Incoterms and freight.',
                     'title': 'Mastery Verification: PRs & Sourcing Optimization'},
                 {   'recommended_mission': {   'description': 'Evaluate multi-vendor RFQ bids for precision optical '
                                                               'arrays DXTR-1000 under tight delivery deadlines.',
                                                'slug': 'nova-sourcing-rfq-decision',
                                                'title': 'Strategic Sourcing & RFQ Comparative Decision'},
                     'step_id': 'd24_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered internal demand capture and sourcing optimization. Next, you '
                                   'will study Purchase Order processing and Flexible Workflow.',
                     'title': 'Day 24 Complete: Requisitioning & Sourcing Mastered'}],
    'subtitle': 'Demand capture, account assignment categories, source determination, and RFQ quotation analysis',
    'title': 'Procure-to-Pay: Purchase Requisition & Sourcing'},
    25: {   'atomic_concepts': ['p2p-po-processing', 'flexible-workflow'],
    'day_number': 25,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-p2p-workflow-incident',
    'slug': 'p2p-purchase-orders',
    'steps': [   {   'content_md': '### Legal Commitment to External Suppliers\n'
                                   'A **Purchase Order (PO)** is a formal legal contract issued by Nova Manufacturing '
                                   'Corp (Purchasing Org PO01) instructing supplier `VEND-101` to deliver specified '
                                   'materials under agreed prices, quantities, and delivery dates.\n'
                                   '\n'
                                   '### Data Model: Header vs Item Tables\n'
                                   'In S/4HANA, purchase order data is segregated into relational tiers:\n'
                                   '- **Header Table (`EKKO`)**: Document-wide attributes applying to all items.\n'
                                   '  - Purchasing Org (`EKKO-EKORG`), Purchasing Group (`EKKO-EKGRP`), Vendor '
                                   'Business Partner (`EKKO-LIFNR`), Document Date, Payment Terms, Incoterms.\n'
                                   '- **Item Table (`EKPO`)**: Granular line-item specifications.\n'
                                   '  - Material Number (`EKPO-MATNR`), Plant (`EKPO-WERKS`), Storage Location '
                                   '(`EKPO-LGORT`), Order Quantity (`EKPO-MENGE`), Net Price (`EKPO-NETPR`), Delivery '
                                   'Date, Tax Code.\n'
                                   '- **Schedule Lines Table (`EKET`)**: Precise delivery dates and staged batch '
                                   'delivery quantities.',
                     'key_terms': [   {   'definition': 'Purchasing Document Header table storing vendor, purchasing '
                                                        'org, and currency.',
                                          'term': 'EKKO'},
                                      {   'definition': 'Purchasing Document Item table storing material, plant, '
                                                        'quantity, and net price.',
                                          'term': 'EKPO'},
                                      {   'definition': 'Split delivery dates and quantities under a single purchase '
                                                        'order line item.',
                                          'term': 'Delivery Schedule'}],
                     'step_id': 'd25_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'EKKO holds document-wide commercial terms; EKPO holds material, plant, quantity, and '
                                 'unit price lines.',
                     'title': 'The Commercial Contract: Purchase Order Structure'},
                 {   'content_md': '### Purchase Order Status Sequence\n'
                                   '1. **Saved / In Preparation**: PO created with reference to PR #10004520; '
                                   'validation checks pass.\n'
                                   '2. **In Approval (Workflow Active)**: System locks PO for transmission while '
                                   'routing through management approval.\n'
                                   '3. **Released / Approved**: All designated approvers sign off; PO status '
                                   'transitions to *Approved*.\n'
                                   '4. **Output Transmitted**: EDI, email PDF, or SAP Business Network message sent to '
                                   'vendor VEND-101.\n'
                                   '5. **Open for Delivery**: Awaiting physical receipt at plant receiving dock.\n'
                                   '\n'
                                   '### Financial Commitment Tracking\n'
                                   'Although PO creation does **not** create balance sheet debit/credit postings in '
                                   'ACDOCA, it generates **Financial Commitments** in Controlling:\n'
                                   '- Earmarks budget on the cost center or internal order.\n'
                                   '- Prevents budget overspending before actual Goods Receipt or Invoice posting '
                                   'occurs.',
                     'key_terms': [   {   'definition': 'Reserved budget earmark in Controlling preventing '
                                                        'unauthorized overspending.',
                                          'term': 'Commitment'},
                                      {   'definition': 'Automated B2B transmission of POs directly into supplier ERP '
                                                        'systems.',
                                          'term': 'EDI (Electronic Data Interchange)'}],
                     'step_id': 'd25_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'POs generate Controlling commitments without balance sheet entries, preventing '
                                 'budget overspend before physical delivery.',
                     'title': 'PO Status Lifecycles & Flexible Release Workflows'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'po_number': '45000108',
                                            'status': 'RELEASED_AND_TRANSMITTED',
                                            'total_net_value': 30000.0,
                                            'vendor': 'VEND-101'},
                     'content_md': '### Formal Purchase Order Details\n'
                                   '\n'
                                   '**Document Header (EKKO)**:\n'
                                   '- **PO Number**: `45000108`\n'
                                   '- **Vendor**: `VEND-101` (Rheinland Precision Optics)\n'
                                   '- **Purchasing Org**: `PO01` | Company Code: `NM01`\n'
                                   '- **Terms**: Net 30 Days | Currency: EUR\n'
                                   '\n'
                                   '**Line Item 10 (EKPO)**:\n'
                                   '- **Material**: `RAW-01` (Optical Sensor Array)\n'
                                   '- **Quantity**: 200 EA\n'
                                   '- **Net Unit Price**: €150.00 / EA\n'
                                   '- **Total Net Value**: €30,000.00\n'
                                   '- **Plant**: `PL01` (Heidelberg) | SLoc: `RAW1`\n'
                                   '- **Delivery Date**: 2026-09-25\n'
                                   '\n'
                                   '**Workflow State**: Approved by Purchasing Director; EDI 850 transmitted to '
                                   'vendor.',
                     'step_id': 'd25_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: PO #45000108 Issued to Rheinland Optics'},
                 {   'component_type': 'P2PFlow',
                     'instruction': 'Select Stage 3 (Purchase Order) to observe how tables EKKO and EKPO capture '
                                    'contractual commitments.',
                     'step_id': 'd25_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'title': 'Interactive P2P Lifecycle: Purchase Order'},
                 {   'options': [   {   'explanation': 'Correct! Any significant value or quantity change resets '
                                                       'approval to prevent unauthorized commitments.',
                                        'id': 'opt_retrigger_wf',
                                        'is_correct': True,
                                        'label': "The PO approval status is reset to 'In Approval' and a new approval "
                                                 'workflow is triggered because the modified value exceeds the '
                                                 'previous approval threshold.'},
                                    {   'explanation': 'Incorrect. S/4HANA governance strictly revokes approval on '
                                                       'material condition increases.',
                                        'id': 'opt_silent_update',
                                        'is_correct': False,
                                        'label': 'The system quietly updates the database without notifying managers '
                                                 'because the vendor was already approved once.'},
                                    {   'explanation': 'Absurd distractor.',
                                        'id': 'opt_auto_invoice',
                                        'is_correct': False,
                                        'label': "The system immediately charges Nova Manufacturing's corporate credit "
                                                 'card.'}],
                     'scenario_md': 'After PO #45000108 is approved and transmitted to vendor VEND-101, the '
                                    'manufacturing supervisor requests increasing the quantity from 200 EA to 500 EA '
                                    '(raising value from €30,000 to €75,000).\n'
                                    '\n'
                                    'What happens automatically in S/4HANA when the buyer edits the quantity in '
                                    'transaction ME22N / Fiori app *Manage Purchase Orders*?',
                     'step_id': 'd25_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'PO Modification Dilemma: Changing Quantity Post-Transmission'},
                 {   'questions': [   {   'concept_slug': 'p2p-po-processing',
                                          'id': 'd25_q1',
                                          'options': [   {   'explanation': 'EKKO is the purchasing document header '
                                                                            'table.',
                                                             'id': 'q1_a',
                                                             'is_correct': True,
                                                             'label': 'EKKO'},
                                                         {   'explanation': 'EKPO stores purchasing document line '
                                                                            'items, not header data.',
                                                             'id': 'q1_b',
                                                             'is_correct': False,
                                                             'label': 'EKPO'},
                                                         {   'explanation': 'VBAK stores SD Sales Order headers.',
                                                             'id': 'q1_c',
                                                             'is_correct': False,
                                                             'label': 'VBAK'}],
                                          'points': 10,
                                          'question': 'Which database table stores the Purchasing Document Header '
                                                      'information (Company Code, Vendor, Purchasing Org) in S/4HANA?',
                                          'question_id': 'd25_q1'},
                                      {   'concept_slug': 'flexible-workflow',
                                          'id': 'd25_q2',
                                          'options': [   {   'explanation': 'POs create commercial commitments, but no '
                                                                            'assets or liabilities are recognized on '
                                                                            'the balance sheet until delivery or '
                                                                            'invoice.',
                                                             'id': 'q2_a',
                                                             'is_correct': True,
                                                             'label': 'No. A PO represents a legal commitment and may '
                                                                      'create Controlling commitments, but zero '
                                                                      'general ledger journal entries are posted in '
                                                                      'ACDOCA until Goods Receipt or Invoice receipt.'},
                                                         {   'explanation': 'Cash is never credited at PO creation; '
                                                                            'payment occurs long after delivery.',
                                                             'id': 'q2_b',
                                                             'is_correct': False,
                                                             'label': 'Yes. It debits accounts payable and credits '
                                                                      'cash immediately.'},
                                                         {   'explanation': 'Plausible nonsense distractor.',
                                                             'id': 'q2_c',
                                                             'is_correct': False,
                                                             'label': 'Yes, but only if the PO is created on a '
                                                                      'Friday.'}],
                                          'points': 10,
                                          'question': 'Does the creation and release of a standard stock Purchase '
                                                      'Order post financial journal entries into ACDOCA?',
                                          'question_id': 'd25_q2'}],
                     'step_id': 'd25_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 25 Assessment: Purchase Order Architecture'},
                 {   'concept_slug': 'p2p-po-processing',
                     'evidence_rule': 'Demonstrates clear distinction between commercial commitments and financial '
                                      'ledger postings, mastery of EKKO/EKPO data models, and flexible workflow '
                                      're-triggering logic.',
                     'step_id': 'd25_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': 'Validated expertise in S/4HANA Purchase Order contracts and commitment management.',
                     'title': 'Skill Evidence: Purchase Order Architecture'},
                 {   'recommended_mission': {   'description': 'Resolve purchase order exceptions and managerial '
                                                               'approval workflows.',
                                                'slug': 'nova-p2p-workflow-incident',
                                                'title': 'Procure-to-Pay Workflow & Account Assignment Incident'},
                     'step_id': 'd25_s8_completion',
                     'step_type': 'completion',
                     'summary_md': '### Core Takeaways\n'
                                   '- POs establish the legal contract with external vendors, structured into EKKO '
                                   '(header) and EKPO (item) tables.\n'
                                   '- Commitments protect departmental budgets without posting balance sheet '
                                   'liabilities.\n'
                                   '- Significant modifications dynamically re-trigger approval workflows.\n'
                                   '\n'
                                   'Next: **Day 26 — Goods Receipt (MIGO)** brings physical parts into the warehouse '
                                   'and triggers the first financial posting!',
                     'title': 'Day 25 Complete: Purchase Orders Issued'}],
    'subtitle': 'Contractual commitments, flexible workflow release, header/item structures, and tables EKKO/EKPO',
    'title': 'Procure-to-Pay: Purchase Orders'},
    26: {   'atomic_concepts': ['p2p-goods-receipt-migo', 'gr-ir-clearing-account'],
    'day_number': 26,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-invoice-3way-match-investigation',
    'slug': 'p2p-goods-receipt',
    'steps': [   {   'content_md': '### The Crucial Pivot in P2P: Goods Receipt\n'
                                   'When supplier `VEND-101` delivers components to Plant PL01, warehouse staff '
                                   'execute a **Goods Receipt (GR)** using transaction **MIGO** (or Fiori app *Post '
                                   'Goods Receipt for Purchasing Document*).\n'
                                   '\n'
                                   'Goods Receipt achieves three synchronized operations in real-time:\n'
                                   '1. **Physical Logistics**: Stock quantity is verified against the vendor packing '
                                   'slip and received into warehouse Storage Location `RAW1`.\n'
                                   '2. **Inventory Ledger (MATDOC)**: An append-only material document is written, '
                                   'incrementing unrestricted inventory balance.\n'
                                   '3. **Financial Accounting (ACDOCA)**: An accounting document is posted '
                                   'synchronously.\n'
                                   '\n'
                                   '### Movement Type 101\n'
                                   'In SAP ERP and S/4HANA, every physical movement requires a **Movement Type**:\n'
                                   '- **Movement Type 101**: Goods receipt for purchase order into warehouse stock.\n'
                                   '- Updates purchase order history in table `EKBE` (delivered quantity increases, '
                                   'remaining open quantity decreases).',
                     'key_terms': [   {   'definition': 'Standard SAP movement code for Goods Receipt against a '
                                                        'Purchase Order.',
                                          'term': 'Movement Type 101'},
                                      {   'definition': 'Single unified inventory movement table in S/4HANA replacing '
                                                        'legacy MKPF and MSEG.',
                                          'term': 'MATDOC'},
                                      {   'definition': 'Chronological record tracking all GR and Invoice postings '
                                                        'against a PO line.',
                                          'term': 'PO History (EKBE)'}],
                     'step_id': 'd26_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Goods Receipt (Mov 101) increases physical stock in MATDOC and triggers the first '
                                 'financial entry in ACDOCA.',
                     'title': 'Physical Receiving & The First Financial Posting'},
                 {   'content_md': '### Why S/4HANA Uses the GR/IR Clearing Account\n'
                                   "At the moment goods arrive at the dock, the vendor's invoice has usually **not** "
                                   'arrived yet.\n'
                                   'However, because Nova Manufacturing has taken physical possession of the '
                                   'inventory, accounting rules require capitalizing the asset immediately.\n'
                                   '\n'
                                   'Because the final vendor invoice payable is unknown, S/4HANA uses a temporary '
                                   'liability account: **GR/IR Clearing Account (Goods Receipt / Invoice Receipt)**.\n'
                                   '\n'
                                   '### The Standard Goods Receipt Accounting Entry:\n'
                                   '$$\\begin{aligned}\n'
                                   '\\text{Debit: } & \\text{Raw Material Inventory (G/L 131000)} & €30,000.00 \\\\\n'
                                   '\\text{Credit: } & \\text{GR/IR Clearing Account (G/L 211200)} & €30,000.00\n'
                                   '\\end{aligned}$$\n'
                                   '\n'
                                   '- **Inventory Asset (131000)**: Increases balance sheet assets.\n'
                                   '- **GR/IR Clearing (211200)**: Accrued liability representing goods received for '
                                   'which no invoice has been processed.',
                     'key_terms': [   {   'definition': 'Interim liability account holding accrued inventory '
                                                        'liabilities until invoice receipt.',
                                          'term': 'GR/IR Clearing Account'},
                                      {   'definition': 'Accounting doctrine recognizing expenses and asset gains in '
                                                        'the period they occur.',
                                          'term': 'Matching Principle'}],
                     'step_id': 'd26_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'GR debits Inventory asset and credits GR/IR interim liability; the credit is only '
                                 'cleared when the supplier invoice is posted.',
                     'title': 'Financial Mechanics: The GR/IR Clearing Account (211200)'},
                 {   'company_context': {   'accounting_doc': '100003921',
                                            'company_code': 'NM01',
                                            'matdoc_number': '5000018890',
                                            'movement_type': '101',
                                            'qty_received': 200,
                                            'sloc': 'RAW1'},
                     'content_md': '### Receiving Optical Sensors at Heidelberg Receiving Dock\n'
                                   'Truck arrives with 200 units of `RAW-01`. Warehouse clerk logs MIGO:\n'
                                   '- **Purchase Order**: `45000108` | Line: `10`\n'
                                   '- **Movement Type**: `101`\n'
                                   '- **Received Qty**: 200 EA (Item OK checkbox checked)\n'
                                   '- **Plant / SLoc**: `PL01` / `RAW1`\n'
                                   '\n'
                                   '**System Impact**:\n'
                                   '1. **Material Document #5000018890** written to `MATDOC`.\n'
                                   '2. Stock of `RAW-01` in SLoc `RAW1` increases from 50 EA to 250 EA.\n'
                                   '3. **Accounting Document #100003921** posted in `ACDOCA`:\n'
                                   '   - Debit G/L `131000` (Raw Materials): €30,000.00\n'
                                   '   - Credit G/L `211200` (GR/IR Clearing): €30,000.00\n'
                                   '4. PO line item open quantity becomes 0 EA.',
                     'step_id': 'd26_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: MIGO Execution for PO #45000108'},
                 {   'component_type': 'InventoryMovementMapper',
                     'instruction': 'Select Movement 101 to trace how Goods Receipt updates MATDOC stock quantities '
                                    'and posts to GR/IR clearing in ACDOCA.',
                     'step_id': 'd26_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'title': 'Inventory Movement Simulator: Movement 101'},
                 {   'options': [   {   'explanation': 'Correct! Posting partial GR for 150 EA capitalizes only the '
                                                       'accepted stock and leaves the PO open for 50 replacement '
                                                       'units.',
                                        'id': 'opt_partial_gr',
                                        'is_correct': True,
                                        'label': 'Post a partial Goods Receipt of 150 EA with Movement 101. The '
                                                 'remaining 50 EA stays as an open balance on PO #45000108 for '
                                                 'replacement delivery.'},
                                    {   'explanation': "Incorrect! Scrapping defective vendor items at Nova's expense "
                                                       "unfairly forces Nova to pay for the supplier's damaged goods.",
                                        'id': 'opt_full_scrap',
                                        'is_correct': False,
                                        'label': 'Post 200 EA under Movement 101, then immediately post Movement 551 '
                                                 "to scrap the 50 units at Nova's expense."},
                                    {   'explanation': 'Incorrect. 150 good units are urgently required for '
                                                       'manufacturing assembly.',
                                        'id': 'opt_cancel_po',
                                        'is_correct': False,
                                        'label': 'Delete the purchase order and tell the truck driver to go home.'}],
                     'scenario_md': 'During receiving inspection for PO #45000108, the quality inspector discovers '
                                    'that 50 of the 200 sensors have cracked lenses caused by in-transit vibrations. '
                                    'The inspector instructs the warehouse clerk to accept only the 150 perfect units '
                                    "and immediately return the 50 defective units back onto the supplier's truck.\n"
                                    '\n'
                                    'How should this transaction be recorded in MIGO?',
                     'step_id': 'd26_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Receiving Dilemma: Defective Batch on Delivery Dock'},
                 {   'questions': [   {   'concept_slug': 'gr-ir-clearing-account',
                                          'id': 'd26_q1',
                                          'options': [   {   'explanation': 'Inventory increases (Debit) and interim '
                                                                            'un-invoiced receipt liability increases '
                                                                            '(Credit).',
                                                             'id': 'q1_a',
                                                             'is_correct': True,
                                                             'label': 'Debit Inventory Asset (131000) | Credit GR/IR '
                                                                      'Clearing Account (211200)'},
                                                         {   'explanation': 'Cash and AP are not touched at Goods '
                                                                            'Receipt.',
                                                             'id': 'q1_b',
                                                             'is_correct': False,
                                                             'label': 'Debit Cash in Bank (113100) | Credit Vendor '
                                                                      'Accounts Payable (211000)'},
                                                         {   'explanation': 'Completely unrelated to purchasing '
                                                                            'receipts.',
                                                             'id': 'q1_c',
                                                             'is_correct': False,
                                                             'label': 'Debit Sales Revenue (410000) | Credit Retained '
                                                                      'Earnings'}],
                                          'points': 10,
                                          'question': 'What is the standard General Ledger posting when a warehouse '
                                                      'clerk posts Movement Type 101 (Goods Receipt for PO) for '
                                                      'standard stock inventory?',
                                          'question_id': 'd26_q1'},
                                      {   'concept_slug': 'p2p-goods-receipt-migo',
                                          'id': 'd26_q2',
                                          'options': [   {   'explanation': 'MATDOC is the central inventory ledger in '
                                                                            'S/4HANA.',
                                                             'id': 'q2_a',
                                                             'is_correct': True,
                                                             'label': 'MATDOC'},
                                                         {   'explanation': 'VBRK is the SD billing document header '
                                                                            'table.',
                                                             'id': 'q2_b',
                                                             'is_correct': False,
                                                             'label': 'VBRK'},
                                                         {   'explanation': 'LFA1 is the vendor master general data '
                                                                            'table.',
                                                             'id': 'q2_c',
                                                             'is_correct': False,
                                                             'label': 'LFA1'}],
                                          'points': 10,
                                          'question': 'Which table in SAP S/4HANA records the unified material '
                                                      'document line items for all inventory movements?',
                                          'question_id': 'd26_q2'}],
                     'step_id': 'd26_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 26 Assessment: Goods Receipt & GR/IR Accounting'},
                 {   'concept_slug': 'p2p-goods-receipt-migo',
                     'evidence_rule': 'Demonstrates precision in Movement Type 101 execution, MATDOC ledger mechanics, '
                                      'and GR/IR interim clearing calculations.',
                     'step_id': 'd26_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': 'Certified mastery in S/4HANA Goods Receipt logistics and financial balance sheet '
                                   'capitalization.',
                     'title': 'Skill Evidence: Goods Receipt & Valuation'},
                 {   'recommended_mission': {   'description': 'Investigate a high-value invoice block involving price '
                                                               'and quantity variances.',
                                                'slug': 'nova-invoice-3way-match-investigation',
                                                'title': 'Invoice 3-Way Match Discrepancy Investigation'},
                     'step_id': 'd26_s8_completion',
                     'step_type': 'completion',
                     'summary_md': '### Core Takeaways\n'
                                   '- Goods Receipt (MIGO / Mov 101) synchronizes warehouse stock increases with '
                                   'balance sheet asset capitalization.\n'
                                   '- The GR/IR clearing account (211200) acts as an essential interim liability '
                                   'awaiting invoice verification.\n'
                                   '- Table MATDOC provides high-speed, append-only inventory auditing.\n'
                                   '\n'
                                   'Next: **Day 27 — Invoice Verification (MIRO)** clears the GR/IR account against '
                                   "the vendor's commercial invoice!",
                     'title': 'Day 26 Complete: Goods Received & Capitalized'}],
    'subtitle': 'Physical delivery, movement type 101, MATDOC ledger updates, and GR/IR clearing mechanics',
    'title': 'Procure-to-Pay: Goods Receipt'},
    27: {   'atomic_concepts': ['p2p-invoice-verification-miro', 'three-way-matching'],
    'day_number': 27,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-invoice-3way-match-investigation',
    'slug': 'p2p-invoice-verification',
    'steps': [   {   'content_md': '### The Principle of 3-Way Matching\n'
                                   'In SAP S/4HANA, Accounts Payable accounts do **not** blindly pay supplier bills. '
                                   'Every incoming invoice is verified via **Logistics Invoice Verification (LIV / '
                                   'transaction MIRO)** using the strict **3-Way Match**:\n'
                                   '1. **Purchase Order (PO)**: Validates what was contracted (price €150/EA, payment '
                                   'terms, tax codes).\n'
                                   '2. **Goods Receipt (GR)**: Validates what was physically delivered and accepted '
                                   'into stock (quantity 200 EA).\n'
                                   '3. **Vendor Invoice**: Validates what the supplier is billing.\n'
                                   '\n'
                                   '### Automated Reconciliation & Tolerance Limits\n'
                                   'When an AP clerk enters an invoice referencing PO #45000108, S/4HANA automatically '
                                   'pulls the delivered quantities and contracted prices.\n'
                                   'If the invoice matches within configured company tolerance thresholds, the invoice '
                                   'posts cleanly with payment status *Free for Payment*.',
                     'key_terms': [   {   'definition': 'Reconciliation framework comparing Purchase Order, Goods '
                                                        'Receipt, and Vendor Invoice.',
                                          'term': '3-Way Match'},
                                      {   'definition': 'Standard transaction code for Logistics Invoice Verification.',
                                          'term': 'MIRO'},
                                      {   'definition': 'Status flag on invoice preventing cash disbursement until '
                                                        'discrepancies are resolved.',
                                          'term': 'Payment Block'}],
                     'step_id': 'd27_s1_learn',
                     'step_type': 'learn',
                     'takeaway': '3-way match compares PO contracted terms, GR actual delivered quantities, and '
                                 'Invoice billed amounts.',
                     'title': 'Logistics Invoice Verification (LIV) & 3-Way Matching'},
                 {   'content_md': '### Automated Tolerance Keys\n'
                                   'When variances occur, S/4HANA checks standard tolerance keys:\n'
                                   '- **Tolerance Key PP (Price Variance)**: Checks percentage and absolute deviation '
                                   'between invoice unit price and PO unit price.\n'
                                   '- **Tolerance Key DQ (Quantity Variance)**: Checks if invoiced quantity exceeds '
                                   'delivered quantity.\n'
                                   '- If variance exceeds the upper tolerance limit, S/4HANA automatically applies '
                                   "**Payment Block 'R' (Invoice Verification Block)**.\n"
                                   '\n'
                                   '### The Standard MIRO Financial Posting:\n'
                                   '$$\\begin{aligned}\n'
                                   '\\text{Debit: } & \\text{GR/IR Clearing Account (G/L 211200)} & €30,000.00 \\\\\n'
                                   '\\text{Debit: } & \\text{Input Tax / VAT Receivable (G/L 154000)} & €5,700.00 '
                                   '\\\\\n'
                                   '\\text{Credit: } & \\text{Vendor Accounts Payable (VEND-101 / G/L 211000)} & '
                                   '€35,700.00\n'
                                   '\\end{aligned}$$\n'
                                   '\n'
                                   'Notice that the **GR/IR clearing account is debited**, reducing the interim '
                                   'liability created during Goods Receipt to **zero**! The net liability now sits '
                                   'cleanly in Vendor Accounts Payable.',
                     'key_terms': [   {   'definition': 'Price variance threshold check during invoice verification.',
                                          'term': 'Tolerance Key PP'},
                                      {   'definition': 'Quantity variance threshold check comparing invoiced vs '
                                                        'delivered goods.',
                                          'term': 'Tolerance Key DQ'},
                                      {   'definition': 'System block assigned when price or quantity tolerances are '
                                                        'breached.',
                                          'term': "Payment Block 'R'"}],
                     'step_id': 'd27_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'MIRO debits GR/IR clearing (zeroing out the interim liability), debits Input VAT, '
                                 'and credits Vendor Accounts Payable.',
                     'title': 'Tolerance Keys & Financial Clearing Postings'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'gross_amount': 35700.0,
                                            'invoice_doc': '190000441',
                                            'tolerance_status': 'CLEAN_MATCH',
                                            'vendor': 'VEND-101'},
                     'content_md': '### Clean 3-Way Match Execution\n'
                                   'Vendor Rheinland Precision Optics sends invoice `INV-2026-9912` for €35,700 '
                                   '(€30,000 net + 19% German VAT €5,700).\n'
                                   '\n'
                                   '**Reconciliation**:\n'
                                   '- PO Contracted: 200 EA @ €150.00 = €30,000.00\n'
                                   '- GR Accepted: 200 EA (Material Doc #5000018890)\n'
                                   '- Invoiced: 200 EA @ €150.00 = €30,000.00 + €5,700.00 tax\n'
                                   '\n'
                                   '**Result**: Zero variance. Tolerance keys PP and DQ are completely satisfied.\n'
                                   'Accounting Document #190000441 posts in ACDOCA:\n'
                                   '- Debit GR/IR `211200`: €30,000.00\n'
                                   '- Debit Input VAT `154000`: €5,700.00\n'
                                   '- Credit Vendor AP `VEND-101` (`211000`): €35,700.00\n'
                                   'Open item status on VEND-101: **Open, Due in 30 days**.',
                     'step_id': 'd27_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: MIRO Invoice Posting for PO #45000108'},
                 {   'component_type': 'InvoiceMatchVisualizer',
                     'instruction': 'Test Clean Match, Price Variance (Tolerance Key PP), and Quantity Mismatch '
                                    "(Tolerance Key DQ) to observe automated Payment Block 'R' behavior.",
                     'step_id': 'd27_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'title': '3-Way Match & Variance Simulator'},
                 {   'options': [   {   'explanation': 'Correct! S/4HANA posts the accounting document so the '
                                                       "liability is not lost, but locks payment with Block 'R' until "
                                                       'procurement investigates.',
                                        'id': 'opt_block_r',
                                        'is_correct': True,
                                        'label': 'The invoice is posted into ACDOCA to record the liability, but '
                                                 "S/4HANA automatically tags the vendor line with Payment Block 'R' "
                                                 '(Invoice Verification), preventing payment until released via '
                                                 'transaction MRBR.'},
                                    {   'explanation': 'Absurd distractor.',
                                        'id': 'opt_crash',
                                        'is_correct': False,
                                        'label': 'The SAP system crashes and wipes out the purchase order history.'},
                                    {   'explanation': 'Incorrect. S/4HANA strictly halts payments that exceed '
                                                       'tolerance limits.',
                                        'id': 'opt_pay_full',
                                        'is_correct': False,
                                        'label': 'The system automatically wires the extra €25/EA immediately.'}],
                     'scenario_md': 'Vendor VEND-101 submits an invoice billing €175.00/EA instead of the contracted '
                                    "PO price of €150.00/EA (+16.7% variance), claiming raw material inflation. Nova's "
                                    'configured upper tolerance limit for Key PP is 5.0%.\n'
                                    '\n'
                                    'What happens in S/4HANA when the clerk attempts to post the invoice in MIRO?',
                     'step_id': 'd27_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Discrepancy Challenge: Vendor Price Surcharge'},
                 {   'questions': [   {   'concept_slug': 'three-way-matching',
                                          'id': 'd27_q1',
                                          'options': [   {   'explanation': 'The GR/IR clearing account is an interim '
                                                                            'bridge that clears to zero once both GR '
                                                                            'and Invoice are posted.',
                                                             'id': 'q1_a',
                                                             'is_correct': True,
                                                             'label': 'The GR/IR account is debited by the invoice net '
                                                                      'amount, clearing the credit balance created '
                                                                      'during Goods Receipt to exactly zero.'},
                                                         {   'explanation': 'GR/IR is a liability clearing account, '
                                                                            'not revenue.',
                                                             'id': 'q1_b',
                                                             'is_correct': False,
                                                             'label': 'The GR/IR balance doubles and is transferred to '
                                                                      'sales revenue.'},
                                                         {   'explanation': 'Nonsense distractor.',
                                                             'id': 'q1_c',
                                                             'is_correct': False,
                                                             'label': 'The GR/IR balance is permanently locked and '
                                                                      'cannot be audited.'}],
                                          'points': 10,
                                          'question': 'What happens to the balance of the GR/IR Clearing Account '
                                                      '(211200) when a clean 3-way match invoice is posted in MIRO for '
                                                      'the exact quantity and price received?',
                                          'question_id': 'd27_q1'},
                                      {   'concept_slug': 'p2p-invoice-verification-miro',
                                          'id': 'd27_q2',
                                          'options': [   {   'explanation': 'MRBR is the standard transaction used to '
                                                                            'investigate and release blocked invoices.',
                                                             'id': 'q2_a',
                                                             'is_correct': True,
                                                             'label': 'MRBR (Release Blocked Invoices)'},
                                                         {   'explanation': 'VA01 is for SD sales order creation.',
                                                             'id': 'q2_b',
                                                             'is_correct': False,
                                                             'label': 'VA01 (Create Sales Order)'},
                                                         {   'explanation': 'CS01 is for production BOM engineering.',
                                                             'id': 'q2_c',
                                                             'is_correct': False,
                                                             'label': 'CS01 (Create Bill of Materials)'}],
                                          'points': 10,
                                          'question': 'Which SAP transaction code or Fiori app is used by accounts '
                                                      'payable supervisors to review and release invoices blocked with '
                                                      "Payment Block 'R'?",
                                          'question_id': 'd27_q2'}],
                     'step_id': 'd27_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 27 Assessment: Invoice Verification & Matching'},
                 {   'concept_slug': 'three-way-matching',
                     'evidence_rule': 'Certifies capability in 3-way matching mechanics, tolerance key enforcement '
                                      '(PP/DQ), and invoice release workflows (MRBR).',
                     'step_id': 'd27_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': 'Demonstrated mastery in S/4HANA Logistics Invoice Verification and automated AP '
                                   'controls.',
                     'title': 'Skill Evidence: Invoice Verification'},
                 {   'recommended_mission': {   'description': 'Investigate a high-value invoice block involving price '
                                                               'and quantity variances.',
                                                'slug': 'nova-invoice-3way-match-investigation',
                                                'title': 'Invoice 3-Way Match Discrepancy Investigation'},
                     'step_id': 'd27_s8_completion',
                     'step_type': 'completion',
                     'summary_md': '### Core Takeaways\n'
                                   '- The 3-way match reconciles PO contracted prices, GR delivered quantities, and '
                                   'Invoice billed sums.\n'
                                   '- MIRO debits GR/IR clearing (zeroing out accrued liabilities) and credits Vendor '
                                   'Accounts Payable.\n'
                                   "- Tolerances (PP, DQ) prevent payment leakage by assigning Block 'R' until "
                                   'investigated.\n'
                                   '\n'
                                   'Next: **Day 28 — Payment Run & P2P Exceptions** completes the Procure-to-Pay cycle '
                                   'with automated bank disbursements!',
                     'title': 'Day 27 Complete: Invoices Verified & Reconciled'}],
    'subtitle': 'Logistics Invoice Verification, 3-way matching, tolerance keys PP/DQ, and payment blocks',
    'title': 'Procure-to-Pay: Invoice Verification / 3-Way Match'},
    28: {   'atomic_concepts': ['payment-block-exceptions', 'p2p-f110-payment-run'],
    'day_number': 28,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-p2p-workflow-incident',
    'slug': 'p2p-exceptions-troubleshooting',
    'steps': [   {   'content_md': '### Automated Cash Disbursement at Scale\n'
                                   'Global enterprises process thousands of vendor invoices weekly. Manual wire '
                                   'transfers are error-prone and fail to capture cash discounts.\n'
                                   '\n'
                                   'In SAP S/4HANA, the **Automatic Payment Program (APP / transaction F110)** '
                                   'automates cash disbursements:\n'
                                   '1. **Selection (Parameters)**: AP accountant specifies Company Code (`NM01`), '
                                   'payment methods (Wire, SEPA, ACH), and next posting date.\n'
                                   '2. **Payment Proposal**: S/4HANA evaluates all open vendor line items in ACDOCA, '
                                   'calculates due dates, and selects invoices ready for payment.\n'
                                   '3. **Proposal Edit / Approval**: Treasury reviews exceptions, blocked items, and '
                                   'approves disbursements.\n'
                                   '4. **Payment Run Execution**: Generates financial clearing journal entries and '
                                   'produces payment media files (ISO 20022 XML files / MT103 via Payment Medium '
                                   'Workbench PMW).',
                     'key_terms': [   {   'definition': 'Automatic Payment Program processing mass supplier '
                                                        'disbursements.',
                                          'term': 'F110'},
                                      {   'definition': 'Preliminary simulation list of vendor items eligible for '
                                                        'payment.',
                                          'term': 'Payment Proposal'},
                                      {   'definition': 'Engine generating standardized electronic banking payment '
                                                        'files (e.g. ISO 20022).',
                                          'term': 'Payment Medium Workbench (PMW)'}],
                     'step_id': 'd28_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'F110 automates vendor disbursements in four stages: Parameters, Proposal, Approval, '
                                 'and Payment Execution.',
                     'title': 'The Automatic Payment Program: F110'},
                 {   'content_md': '### Optimizing Working Capital: Cash Discounts (SKTO)\n'
                                   'When payment terms specify cash discounts (e.g. *2% within 14 days, Net 30*), F110 '
                                   'prioritizes payment before day 14 to capture the discount:\n'
                                   '\n'
                                   'For vendor `VEND-101` invoice of €35,700:\n'
                                   '- Gross Payable: €35,700.00\n'
                                   '- 2% Cash Discount on Net €30,000: **-€600.00**\n'
                                   '- Net Bank Wire Disbursement: **€35,100.00**\n'
                                   '\n'
                                   '### The Final Payment Journal Entry in ACDOCA:\n'
                                   '$$\\begin{aligned}\n'
                                   '\\text{Debit: } & \\text{Vendor Accounts Payable (VEND-101)} & €35,700.00 \\\\\n'
                                   '\\text{Credit: } & \\text{Bank Outgoing Payment Clearing (113100)} & €35,100.00 '
                                   '\\\\\n'
                                   '\\text{Credit: } & \\text{Cash Discount Received Income (G/L 710000)} & €600.00\n'
                                   '\\end{aligned}$$\n'
                                   '\n'
                                   'The open vendor item in table `ACDOCA` transitions from **Open** to **Cleared** '
                                   '(`AUGBL` document number populated). The P2P cycle is 100% complete!',
                     'key_terms': [   {   'definition': 'Financial income recognized by paying supplier invoices '
                                                        'within prompt discount periods.',
                                          'term': 'Cash Discount Received'},
                                      {   'definition': 'Marking invoices as settled and recording clearing document '
                                                        'references in ACDOCA.',
                                          'term': 'Open Item Clearing'}],
                     'step_id': 'd28_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'F110 clears the vendor open item, recognizes cash discount income, and credits the '
                                 'bank outgoing account.',
                     'title': 'Cash Discounts & Financial Clearing Accounting'},
                 {   'company_context': {   'bank_wire_total': 35100.0,
                                            'company_code': 'NM01',
                                            'discount_captured': 600.0,
                                            'f110_run_id': '20260925-NM01',
                                            'vendor_cleared': 'VEND-101'},
                     'content_md': '### Weekly Treasury Disbursement Run\n'
                                   'Treasury Lead Markus Schmidt executes F110 run `20260925-NM01`:\n'
                                   '- **Company Code**: `NM01`\n'
                                   '- **Payment Method**: `T` (SEPA Corporate Wire Transfer)\n'
                                   '- **Target Vendor**: `VEND-101` (Rheinland Precision Optics)\n'
                                   '\n'
                                   '**Results**:\n'
                                   '- Invoice `190000441` (€35,700) cleared.\n'
                                   '- €600 cash discount captured.\n'
                                   '- Payment document `150000088` posted in ACDOCA.\n'
                                   '- Bank clearing file `SEPA_XML_NM01_0925.xml` transmitted to Deutsche Bank via '
                                   'secure host-to-host banking link.',
                     'step_id': 'd28_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: F110 Payment Run Execution'},
                 {   'component_type': 'P2PFlow',
                     'instruction': 'Select Stage 6 (Payment Clearing) to review how the complete audit trail links PR '
                                    '-> PO -> GR -> Invoice -> Bank Payment.',
                     'step_id': 'd28_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'title': 'Full P2P Flow: Bank Payment Clearing'},
                 {   'options': [   {   'explanation': 'Correct! Maintaining the verified IBAN on the BP master record '
                                                       'allows the proposal to select the vendor and format the bank '
                                                       'transfer file.',
                                        'id': 'opt_bp_bank',
                                        'is_correct': True,
                                        'label': "Maintain the vendor's verified IBAN and SWIFT/BIC in the Business "
                                                 'Partner master record (transaction BP / Manage Business Partner), '
                                                 'then regenerate the payment proposal in F110.'},
                                    {   'explanation': 'Absurd distractor violating enterprise audit and safety '
                                                       'policies.',
                                        'id': 'opt_cash',
                                        'is_correct': False,
                                        'label': "Send an employee to the vendor's headquarters with an envelope of "
                                                 'cash.'},
                                    {   'explanation': 'Incorrect. Deleting posted accounting documents is strictly '
                                                       'prohibited.',
                                        'id': 'opt_delete_inv',
                                        'is_correct': False,
                                        'label': 'Delete the vendor invoice from ACDOCA.'}],
                     'scenario_md': 'During the F110 payment proposal run, invoice #190000441 appears in the '
                                    "**Exception List** with error code 006: *'No valid bank details (IBAN/BIC) found "
                                    "for vendor VEND-101'*.\n"
                                    '\n'
                                    'How should the treasury accountant resolve this exception?',
                     'step_id': 'd28_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Exception Challenge: Missing Bank Details in Proposal'},
                 {   'questions': [   {   'concept_slug': 'p2p-f110-payment-run',
                                          'id': 'd28_q1',
                                          'options': [   {   'explanation': 'The proposal is an editable preview that '
                                                                            'prevents erroneous wire disbursements.',
                                                             'id': 'q1_a',
                                                             'is_correct': True,
                                                             'label': 'It allows treasury accountants to inspect all '
                                                                      'selected invoices, verify cash discounts, and '
                                                                      'resolve exception blocks before irreversible '
                                                                      'bank files are generated.'},
                                                         {   'explanation': 'Checks are only printed during payment '
                                                                            'execution, not proposal simulation.',
                                                             'id': 'q1_b',
                                                             'is_correct': False,
                                                             'label': 'It automatically prints paper checks on the '
                                                                      'nearest office printer.'},
                                                         {   'explanation': 'Plausible nonsense distractor.',
                                                             'id': 'q1_c',
                                                             'is_correct': False,
                                                             'label': 'It resets all employee email passwords.'}],
                                          'points': 10,
                                          'question': 'What is the primary benefit of reviewing the Payment Proposal '
                                                      'before executing the actual Payment Run in transaction F110?',
                                          'question_id': 'd28_q1'},
                                      {   'concept_slug': 'payment-block-exceptions',
                                          'id': 'd28_q2',
                                          'options': [   {   'explanation': 'Cash discounts received reduce the '
                                                                            'overall expense and are credited to P&L '
                                                                            'financial income.',
                                                             'id': 'q2_a',
                                                             'is_correct': True,
                                                             'label': 'Cash Discount Received Income (P&L account '
                                                                      '710000)'},
                                                         {   'explanation': 'Finished goods inventory is part of '
                                                                            'manufacturing and sales, not AP payment '
                                                                            'discounts.',
                                                             'id': 'q2_b',
                                                             'is_correct': False,
                                                             'label': 'Finished Goods Inventory (132000)'},
                                                         {   'explanation': 'Customer AR relates to incoming revenue '
                                                                            'from clients, not outgoing payments.',
                                                             'id': 'q2_c',
                                                             'is_correct': False,
                                                             'label': 'Customer Accounts Receivable'}],
                                          'points': 10,
                                          'question': 'When an invoice is successfully settled by F110 with a cash '
                                                      'discount, which account is credited for the discount portion?',
                                          'question_id': 'd28_q2'}],
                     'step_id': 'd28_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 28 Assessment: Payment Runs & Exceptions'},
                 {   'concept_slug': 'p2p-f110-payment-run',
                     'evidence_rule': 'Validates complete mastery across the 6-stage Procure-to-Pay lifecycle from '
                                      'Requisition to Bank Clearing.',
                     'step_id': 'd28_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': 'Certified operational proficiency in S/4HANA Procure-to-Pay execution and treasury '
                                   'clearing.',
                     'title': 'Skill Evidence: P2P Payment & Exception Management'},
                 {   'recommended_mission': {   'description': 'Troubleshoot end-to-end procurement bottlenecks, '
                                                               'blocks, and reconciliation errors.',
                                                'slug': 'nova-p2p-workflow-incident',
                                                'title': 'Procure-to-Pay Workflow & Account Assignment Incident'},
                     'step_id': 'd28_s8_completion',
                     'step_type': 'completion',
                     'summary_md': '### 🏆 Procure-to-Pay Milestone Achieved!\n'
                                   'You have successfully mastered the entire **P2P Business Process (Days 23–28)**:\n'
                                   '1. Purchase Requisitions & Account Assignments (Day 23)\n'
                                   '2. Operational Sourcing & Info Records (Day 24)\n'
                                   '3. Purchase Orders & Commitments (Day 25)\n'
                                   '4. Goods Receipt & GR/IR Accounting (Day 26)\n'
                                   '5. 3-Way Matching & Logistics Invoice Verification (Day 27)\n'
                                   '6. Automatic Payment Program & Exception Clearing (Day 28)\n'
                                   '\n'
                                   'Next Block: **Days 29–34 — Order-to-Cash (O2C)**!',
                     'title': 'Day 28 Complete: Procure-to-Pay Block Mastered!'}],
    'subtitle': 'Automatic Payment Program (F110), cash discounts, payment medium workbench, and bank clearing',
    'title': 'Procure-to-Pay: P2P Exceptions & Troubleshooting'},
    29: {   'atomic_concepts': ['o2c-pricing-procedure', 'condition-technique'],
    'day_number': 29,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-o2c-order-fulfillment-crisis',
    'slug': 'o2c-overview',
    'steps': [   {   'content_md': '### The Order-to-Cash Commercial Cycle\n'
                                   'The Order-to-Cash (O2C) business process encompasses the complete enterprise '
                                   'journey from customer request to cash collection:\n'
                                   '1. **Sales Inquiry (VA11)**: Non-binding customer interest record.\n'
                                   '2. **Sales Quotation (VA21)**: Legally binding commercial proposal with validity '
                                   'dates, agreed pricing, and delivery conditions.\n'
                                   '3. **Sales Order (VA01)**: Formal customer purchase contract.\n'
                                   '\n'
                                   '### The SAP Condition Technique\n'
                                   'Pricing in SAP S/4HANA is driven by the **Condition Technique**—a modular rules '
                                   'engine that calculates gross price, customer discounts, freight surcharges, and '
                                   'taxes:\n'
                                   '- **Condition Types**: Standard calculation elements:\n'
                                   '  - `PR00`: Base Gross Selling Price (e.g. €1,500.00 / EA for `DXTR-1000`).\n'
                                   '  - `K004` / `K007`: Customer-specific discount or rebate.\n'
                                   '  - `KF00`: Freight surcharge.\n'
                                   '  - `MWST`: Value Added Tax (VAT / Output tax).\n'
                                   '- **Access Sequence**: Search strategy querying pricing master records from '
                                   'specific (Customer + Material) to general (Material group).\n'
                                   '- **Pricing Procedure**: Calculation schema specifying the sequence of conditions, '
                                   'subtotals, and accounting Account Keys (`ERL`, `ERS`, `MWS`).',
                     'key_terms': [   {   'definition': 'SAP rule engine determining pricing, taxes, and output '
                                                        'determination through access sequences and schemas.',
                                          'term': 'Condition Technique'},
                                      {   'definition': 'Calculation schema defining the arithmetic sequence of '
                                                        'condition types and accounting account keys.',
                                          'term': 'Pricing Procedure'},
                                      {   'definition': 'Standard SAP condition type representing base gross product '
                                                        'price.',
                                          'term': 'PR00'}],
                     'step_id': 'd29_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Condition technique calculates net pricing dynamically; quotations create binding '
                                 'commitments for defined validity windows.',
                     'title': 'Commercial Inception: Inquiries, Quotations & Condition Technique'},
                 {   'content_md': '### From Commercial Conditions to Financial G/L Accounts\n'
                                   'A common architectural misconception is that SD condition records contain General '
                                   'Ledger account numbers. They do **not**.\n'
                                   '\n'
                                   'Instead, each relevant line in the Pricing Procedure is assigned an **Account '
                                   'Key**:\n'
                                   '- `PR00` (Gross Price) -> Account Key **`ERL`** (Revenue)\n'
                                   '- `K004` (Customer Discount) -> Account Key **`ERS`** (Sales Deductions)\n'
                                   '- `MWST` (Output VAT) -> Account Key **`MWS`** (Tax on Sales/Purchases)\n'
                                   '\n'
                                   'During billing, table **`VKOA`** (Revenue Account Determination) evaluates the '
                                   'Account Key, Chart of Accounts (`NMCA`), Sales Org (`SO01`), and Customer Account '
                                   'Assignment Group to resolve the exact G/L account (`410000` for revenue).',
                     'key_terms': [   {   'definition': '3-character code (e.g. ERL, ERS, MWS) linking pricing '
                                                        'conditions to G/L accounts in table VKOA.',
                                          'term': 'Account Key'},
                                      {   'definition': 'Central SD-FI account determination table routing commercial '
                                                        'conditions to ACDOCA.',
                                          'term': 'VKOA'}],
                     'step_id': 'd29_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Account Keys decouple commercial pricing conditions from General Ledger chart of '
                                 'accounts.',
                     'title': 'Architecture: Pricing Schema Execution & Account Determination Keys'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'customer': 'CUST-501',
                                            'gross_total': 49980.0,
                                            'net_value': 42000.0,
                                            'quotation_num': '20000412',
                                            'tax_value': 7980.0},
                     'content_md': '### Quotation #20000412 for CUST-501\n'
                                   'Customer **Nordics Heavy Industrial AB (CUST-501)** requests a binding quotation '
                                   'for 30 units of `DXTR-1000` Industrial Robotics Controllers:\n'
                                   '\n'
                                   '**Condition Breakdown**:\n'
                                   '- `PR00` Base Price: €1,500.00 x 30 EA = €45,000.00\n'
                                   '- `K004` Customer Volume Discount (6.67%): -€3,000.00\n'
                                   '- **Net Commercial Value**: **€42,000.00**\n'
                                   '- `MWST` Output Tax (19%): €7,980.00\n'
                                   '- **Total Gross Quotation**: **€49,980.00**\n'
                                   '\n'
                                   'Validity: Valid through end of current quarter. Delivered DAP Stockholm via Sales '
                                   'Org `SO01`.',
                     'step_id': 'd29_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: Quotation for Nordics Industrial AB'},
                 {   'component_type': 'O2CFlow',
                     'instruction': 'Click Stage 1 (Customer Inquiry & Quotation) to inspect how condition pricing '
                                    'feeds into downstream sales order processing.',
                     'step_id': 'd29_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'title': 'O2C Flow: Quotation & Pricing Analysis'},
                 {   'options': [   {   'explanation': 'Correct! Condition Exclusion Groups prevent unwanted discount '
                                                       'stacking by suppressing lesser conditions.',
                                        'id': 'opt_exclusion',
                                        'is_correct': True,
                                        'label': 'Configure Condition Exclusion Groups in SPRO (transaction VOK0), '
                                                 'specifying that if condition RB00 is present, condition types K007 '
                                                 'and K020 are deactivated.'},
                                    {   'explanation': 'Absurd distractor.',
                                        'id': 'opt_delete_all',
                                        'is_correct': False,
                                        'label': 'Delete condition type PR00 so the customer gets the goods for free.'},
                                    {   'explanation': 'Incorrect. Bypassing condition technique violates audit and '
                                                       'internal pricing governance.',
                                        'id': 'opt_excel',
                                        'is_correct': False,
                                        'label': 'Instruct sales reps to manually calculate totals on an external '
                                                 'pocket calculator and hardcode final amounts.'}],
                     'scenario_md': 'A sales representative offers CUST-501 a special manual promotion discount of 10% '
                                    '(condition type RB00). However, the standard pricing procedure already applied a '
                                    '5% customer group discount (K007) and a 3% material group discount (K020). The '
                                    "customer's quotation shows an unintended cumulative 18% price drop!\n"
                                    '\n'
                                    'How can an SD solution architect configure the Pricing Procedure to enforce that '
                                    'manual promotion discounts override group discounts rather than stacking?',
                     'step_id': 'd29_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Pricing Dilemma: Unintended Discount Stacking'},
                 {   'questions': [   {   'concept_slug': 'o2c-pricing-procedure',
                                          'id': 'd29_q1',
                                          'options': [   {   'explanation': 'Account Keys link pricing calculation '
                                                                            'results to chart of accounts G/L lines.',
                                                             'id': 'q1_a',
                                                             'is_correct': True,
                                                             'label': 'It acts as the integration link between '
                                                                      'commercial condition types and G/L accounts in '
                                                                      'table VKOA, allowing automatic revenue account '
                                                                      'determination during billing.'},
                                                         {   'explanation': 'Absurd security violation distractor.',
                                                             'id': 'q1_b',
                                                             'is_correct': False,
                                                             'label': "It stores the customer's bank login password."},
                                                         {   'explanation': 'Weights are stored in material master '
                                                                            'basic data, not account keys.',
                                                             'id': 'q1_c',
                                                             'is_correct': False,
                                                             'label': 'It specifies the physical dimensions and '
                                                                      'shipping weight of the pallet.'}],
                                          'points': 10,
                                          'question': "What role does an 'Account Key' (such as ERL or MWS) play in an "
                                                      'SAP SD Pricing Procedure?',
                                          'question_id': 'd29_q1'},
                                      {   'concept_slug': 'condition-technique',
                                          'id': 'd29_q2',
                                          'options': [   {   'explanation': 'Access sequences determine how the system '
                                                                            'searches condition tables for valid '
                                                                            'prices.',
                                                             'id': 'q2_a',
                                                             'is_correct': True,
                                                             'label': 'It defines the search hierarchy of condition '
                                                                      'tables, searching from specific condition '
                                                                      'records (e.g. Customer + Material) to general '
                                                                      'records (e.g. Material Group).'},
                                                         {   'explanation': 'Plausible nonsense distractor.',
                                                             'id': 'q2_b',
                                                             'is_correct': False,
                                                             'label': 'It controls the speed of the database CPU '
                                                                      'fans.'},
                                                         {   'explanation': 'Output determination handles printing, '
                                                                            'not pricing access sequences.',
                                                             'id': 'q2_c',
                                                             'is_correct': False,
                                                             'label': 'It prints shipping barcode labels on the '
                                                                      'packaging line.'}],
                                          'points': 10,
                                          'question': 'In the SAP Condition Technique, what is the primary purpose of '
                                                      "an 'Access Sequence'?",
                                          'question_id': 'd29_q2'}],
                     'step_id': 'd29_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 29 Assessment: Inquiries & Pricing Procedures'},
                 {   'concept_slug': 'o2c-pricing-procedure',
                     'evidence_rule': 'Validates proficiency in condition types, pricing procedure calculation '
                                      'sequences, and Account Key integration with table VKOA.',
                     'step_id': 'd29_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': 'Demonstrated mastery in S/4HANA Sales Pricing and Condition Technique '
                                   'architecture.',
                     'title': 'Skill Evidence: Condition Technique & Pricing Procedures'},
                 {   'recommended_mission': {   'description': 'Handle a sudden credit limit breach on a high-value '
                                                               'priority customer sales order.',
                                                'slug': 'nova-o2c-order-fulfillment-crisis',
                                                'title': 'Order-to-Cash Fulfillment & Credit Crisis'},
                     'step_id': 'd29_s8_completion',
                     'step_type': 'completion',
                     'summary_md': '### Core Takeaways\n'
                                   '- SD condition technique separates commercial pricing logic from financial chart '
                                   'of accounts.\n'
                                   '- Account Keys (ERL, ERS, MWS) route conditions to General Ledger accounts via '
                                   'table VKOA.\n'
                                   '- Condition exclusion rules prevent revenue leakage from stacked discounts.\n'
                                   '\n'
                                   'Next: **Day 30 — Sales Order Creation & Partner Determination**!',
                     'title': 'Day 29 Complete: Quotes & Pricing Mastered'}],
    'subtitle': 'Condition technique, pricing procedures, condition types PR00/K004/MWST, and quotation lifecycles',
    'title': 'Order-to-Cash: O2C Overview'},
    30: {   'atomic_concepts': ['o2c-sales-order-creation', 'partner-determination', 'credit-management'],
    'day_number': 30,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-o2c-order-fulfillment-crisis',
    'slug': 'o2c-sales-orders',
    'steps': [   {   'content_md': '### Formalizing the Customer Commitment\n'
                                   'When customer `CUST-501` accepts Quotation #20000412, the internal sales '
                                   'representative generates a **Sales Order (transaction VA01 / Fiori app Create '
                                   'Sales Orders)**.\n'
                                   '\n'
                                   'The sales order is the authoritative commercial contract governing delivery dates, '
                                   'shipping conditions, billing schedules, and legal terms.\n'
                                   '\n'
                                   '### Data Model: Header vs Item Tables\n'
                                   '- **`VBAK`**: Sales Document Header\n'
                                   '  - Sales Document Type (`VBAK-AUART`, e.g. `OR` for Standard Order)\n'
                                   '  - Sales Area: Sales Organization (`SO01`), Distribution Channel (`10` '
                                   'Wholesale), Division (`00` Cross-division)\n'
                                   '  - Customer Purchase Order Number, Requested Delivery Date.\n'
                                   '- **`VBAP`**: Sales Document Item\n'
                                   '  - Material Number (`VBAP-MATNR`, `DXTR-1000`), Delivering Plant (`VBAP-WERKS`, '
                                   '`PL01`), Order Quantity (`VBAP-KWMENG`), Net Price, Item Category (`TAN` Standard '
                                   'Item).\n'
                                   '- **`VBEP`**: Sales Document Schedule Lines\n'
                                   '  - Confirmed delivery dates and confirmed quantities produced by the ATP check.',
                     'key_terms': [   {   'definition': 'Sales Document Header table storing sales org, document type, '
                                                        'and customer reference.',
                                          'term': 'VBAK'},
                                      {   'definition': 'Sales Document Item table storing material, plant, quantity, '
                                                        'and item category.',
                                          'term': 'VBAP'},
                                      {   'definition': 'Triad of Sales Organization, Distribution Channel, and '
                                                        'Division defining market structure.',
                                          'term': 'Sales Area'}],
                     'step_id': 'd30_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'VBAK holds header terms; VBAP holds material items; VBEP holds confirmed schedule '
                                 'lines.',
                     'title': 'The Commercial Contract: Standard Sales Order (VA01)'},
                 {   'content_md': '### Partner Functions in Sales\n'
                                   'In global enterprises, a single company may place orders through one branch, '
                                   'receive shipments at multiple factories, and remit payments through a central '
                                   'corporate treasury.\n'
                                   'S/4HANA handles this via **Partner Determination**:\n'
                                   '- **Sold-to Party (`SP`)**: Commercial entity placing the order (`CUST-501`).\n'
                                   '- **Ship-to Party (`SH`)**: Physical delivery destination (e.g. `CUST-501-DOCK4` '
                                   'in Stockholm).\n'
                                   '- **Bill-to Party (`BP`)**: Entity receiving the invoice for accounting.\n'
                                   '- **Payer (`PY`)**: Financial legal entity paying the bill (responsible for credit '
                                   'limits).\n'
                                   '\n'
                                   '### S/4HANA Credit Management (FSCM Integration)\n'
                                   'In S/4HANA, legacy FI credit management (tables KNKK/KNKA) has been replaced by '
                                   '**FSCM Credit Management (Financial Supply Chain Management)**:\n'
                                   '- Real-time credit exposure calculated across open sales orders, open deliveries, '
                                   'and unpaid open receivables.\n'
                                   "- Automated credit checks at order entry: if exposure exceeds the customer's "
                                   'credit limit (€100,000 for CUST-501), the order is blocked with credit status '
                                   '*Credit Check Not OK*.',
                     'key_terms': [   {   'definition': 'Roles played by Business Partners in a sales transaction '
                                                        '(Sold-to, Ship-to, Bill-to, Payer).',
                                          'term': 'Partner Functions'},
                                      {   'definition': 'Modern S/4HANA centralized credit risk engine evaluating '
                                                        'dynamic exposure against credit limits.',
                                          'term': 'FSCM Credit Management'}],
                     'step_id': 'd30_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Partner functions decouple ordering, delivery, and payment roles; FSCM protects '
                                 'against bad-debt exposure.',
                     'title': 'Partner Determination & S/4HANA Credit Management'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'credit_exposure': 77980.0,
                                            'credit_limit': 100000.0,
                                            'customer': 'CUST-501',
                                            'sales_order': '10042',
                                            'status': 'APPROVED_OPEN'},
                     'content_md': '### Standard Sales Order Details\n'
                                   '- **Order Number**: `10042` | Type: `OR` (Standard Order)\n'
                                   '- **Sales Area**: `SO01` / `10` / `00`\n'
                                   '- **Customer**: `CUST-501` (Nordics Heavy Industrial AB)\n'
                                   '- **Line Item 10**: 30 EA `DXTR-1000` @ €1,400.00 Net = €42,000.00\n'
                                   '- **Delivering Plant**: `PL01` (Heidelberg)\n'
                                   '- **Credit Exposure**: Prior open AR €28,000 + New Order €49,980 gross = €77,980.\n'
                                   '- **Credit Limit**: €100,000 -> **Credit Check Passed (Status: Green)**.\n'
                                   '- Schedule line 1 confirmed for 30 EA on 2026-09-20.',
                     'step_id': 'd30_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: Sales Order #10042 Created'},
                 {   'component_type': 'O2CFlow',
                     'instruction': 'Select Stage 2 (Sales Order Processing) to inspect how table VBAK and VBAP store '
                                    'order terms without creating financial entries.',
                     'step_id': 'd30_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'title': 'O2C Flow: Sales Order Processing'},
                 {   'options': [   {   'explanation': 'Correct! FSCM governance requires formal credit assessment '
                                                       'before releasing high-risk orders.',
                                        'id': 'opt_fscm_review',
                                        'is_correct': True,
                                        'label': "The Credit Manager reviews the customer's payment history in the "
                                                 "Fiori app 'Manage Credit Cases' and either requests a partial cash "
                                                 'deposit or temporarily raises the credit limit based on financial '
                                                 'vetting.'},
                                    {   'explanation': 'Severe audit violation leading to inventory discrepancies and '
                                                       'uncollected debts.',
                                        'id': 'opt_ship_anyway',
                                        'is_correct': False,
                                        'label': 'Ship the goods anyway without recording it in SAP.'},
                                    {   'explanation': 'Unreasonable overreaction that destroys valuable enterprise '
                                                       'client relationships.',
                                        'id': 'opt_cancel_cust',
                                        'is_correct': False,
                                        'label': 'Permanently ban the customer and blacklist their domain name.'}],
                     'scenario_md': 'CUST-501 attempts to double their order to 60 units of DXTR-1000 (gross €99,960). '
                                    'Added to their existing open AR of €28,000, total exposure reaches €127,960, '
                                    'exceeding their €100,000 credit limit. The order is automatically tagged with '
                                    "Delivery Block '01' (Credit Limit Exceeded).\n"
                                    '\n'
                                    'How should the enterprise handle this credit block?',
                     'step_id': 'd30_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Credit Limit Block Dilemma'},
                 {   'questions': [   {   'concept_slug': 'partner-determination',
                                          'id': 'd30_q1',
                                          'options': [   {   'explanation': 'The Payer is the financial partner '
                                                                            'responsible for credit limits and invoice '
                                                                            'payment.',
                                                             'id': 'q1_a',
                                                             'is_correct': True,
                                                             'label': 'Payer (PY)'},
                                                         {   'explanation': 'Ship-to party is the physical delivery '
                                                                            'receiving dock.',
                                                             'id': 'q1_b',
                                                             'is_correct': False,
                                                             'label': 'Ship-to Party (SH)'},
                                                         {   'explanation': 'Forwarding agent is the third-party '
                                                                            'transportation carrier.',
                                                             'id': 'q1_c',
                                                             'is_correct': False,
                                                             'label': 'Forwarding Agent'}],
                                          'points': 10,
                                          'question': 'Which partner function represents the legal entity responsible '
                                                      'for settling invoices and whose credit limit is checked during '
                                                      'sales order entry?',
                                          'question_id': 'd30_q1'},
                                      {   'concept_slug': 'o2c-sales-order-creation',
                                          'id': 'd30_q2',
                                          'options': [   {   'explanation': 'Revenue and inventory accounting only '
                                                                            'occur during PGI and Billing, not at '
                                                                            'sales order creation.',
                                                             'id': 'q2_a',
                                                             'is_correct': True,
                                                             'label': 'No. A sales order is a commercial commitment '
                                                                      'that affects credit exposure and schedule line '
                                                                      'reservations, but zero balance sheet journal '
                                                                      'entries are posted in ACDOCA.'},
                                                         {   'explanation': 'Completely incorrect accounting direction '
                                                                            'and timing.',
                                                             'id': 'q2_b',
                                                             'is_correct': False,
                                                             'label': 'Yes, it debits revenue and credits cash.'},
                                                         {   'explanation': 'BUT000 is for Business Partner master '
                                                                            'data, not sales order postings.',
                                                             'id': 'q2_c',
                                                             'is_correct': False,
                                                             'label': 'Yes, it writes an audit log in table BUT000.'}],
                                          'points': 10,
                                          'question': 'Does saving a standard sales order in transaction VA01 generate '
                                                      'financial debit/credit postings in ACDOCA?',
                                          'question_id': 'd30_q2'}],
                     'step_id': 'd30_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 30 Assessment: Sales Orders & Credit Management'},
                 {   'concept_slug': 'o2c-sales-order-creation',
                     'evidence_rule': 'Demonstrates mastery of VBAK/VBAP structures, Partner Determination roles, and '
                                      'FSCM credit exposure checks.',
                     'step_id': 'd30_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': 'Certified operational proficiency in S/4HANA Sales Order processing and Credit '
                                   'Management.',
                     'title': 'Skill Evidence: Sales Order Architecture'},
                 {   'recommended_mission': {   'description': 'Handle a sudden credit limit breach on a high-value '
                                                               'priority customer sales order.',
                                                'slug': 'nova-o2c-order-fulfillment-crisis',
                                                'title': 'Order-to-Cash Fulfillment & Credit Crisis'},
                     'step_id': 'd30_s8_completion',
                     'step_type': 'completion',
                     'summary_md': '### Core Takeaways\n'
                                   '- Sales orders formalize commercial agreements, linking Sales Area, customer '
                                   'partner functions, and materials.\n'
                                   '- Partner functions separate physical delivery (SH) from legal payment (PY).\n'
                                   '- FSCM credit checks protect enterprise cash flow from unvetted credit expansion.\n'
                                   '\n'
                                   'Next: **Day 31 — Advanced ATP (aATP)** determines product availability and '
                                   'multi-plant fulfillment!',
                     'title': 'Day 30 Complete: Sales Orders Mastered'}],
    'subtitle': 'Order types (OR/TA), tables VBAK/VBAP, partner determination (SP/BP/PY/SH), and credit management',
    'title': 'Order-to-Cash: Sales Orders'},
    31: {   'atomic_concepts': ['advanced-atp-s4', 'product-allocation', 'backorder-processing'],
    'day_number': 31,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-atp-allocation-conflict',
    'slug': 'o2c-atp-check',
    'steps': [   {   'content_md': '### Beyond Simple Stock Checks\n'
                                   'When a customer orders 40 units of custom robotics controllers, the sales rep '
                                   'cannot merely check current warehouse stock. If 50 units exist in the warehouse '
                                   'but 30 are already committed to other customers, promising 40 will cause an '
                                   'embarrassing fulfillment failure.\n'
                                   '\n'
                                   'In SAP S/4HANA, **Available-to-Promise (ATP)** calculates exact net availability:\n'
                                   '$$\\text{ATP Quantity} = \\text{Physical Stock} + \\text{Planned Receipts (PO, '
                                   'Prod Order)} - \\text{Committed Issues (Sales Orders, Reservations)}$$\n'
                                   '\n'
                                   '### The Three Innovations of Advanced ATP (aATP)\n'
                                   '1. **Product Allocation (PAL)**: Allocates scarce inventory quotas to strategic '
                                   'customers or sales channels to prevent a single buyer from exhausting all global '
                                   'stock.\n'
                                   '2. **Alternative-Based Confirmation (ABC)**: If Plant PL01 has a stock shortage, '
                                   'the system automatically checks alternative plants (e.g. Plant PL02 in Austin) or '
                                   'substitute materials.\n'
                                   '3. **Backorder Processing (BOP)**: Re-evaluates confirmed orders when stock '
                                   'changes, redistributing stock using prioritized strategies (*Win, Gain, '
                                   'Redistribute, Fill, Lose*).',
                     'key_terms': [   {   'definition': 'Advanced Available-to-Promise engine in S/4HANA providing '
                                                        'multi-plant substitution and allocation management.',
                                          'term': 'aATP'},
                                      {   'definition': 'Mechanism rationing limited supply to specific customer tiers '
                                                        'or regions.',
                                          'term': 'Product Allocation (PAL)'},
                                      {   'definition': 'Automated substitution of plants or materials when primary '
                                                        'sources face shortages.',
                                          'term': 'Alternative-Based Confirmation (ABC)'}],
                     'step_id': 'd31_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'aATP calculates net uncommitted stock and uses PAL and ABC to resolve global supply '
                                 'shortages.',
                     'title': 'The Promise to the Customer: Available-to-Promise (ATP)'},
                 {   'content_md': '### Dynamic Re-Prioritization with BOP\n'
                                   'When supply disruptions occur (e.g. a delayed raw material shipment), orders must '
                                   'be re-prioritized based on strategic enterprise value:\n'
                                   '\n'
                                   '- **Win**: Top-tier strategic clients (e.g. global contract customers). They '
                                   '**always** receive 100% confirmation, even if stock must be confiscated from '
                                   'lower-priority orders.\n'
                                   '- **Gain**: High-priority clients who retain existing confirmations and may gain '
                                   'additional stock.\n'
                                   '- **Redistribute**: Standard customers who may lose confirmations if higher tiers '
                                   'need stock.\n'
                                   '- **Fill**: Low-priority orders that only receive stock if no other orders require '
                                   'it.\n'
                                   '- **Lose**: Definite de-confirmation (all reserved stock is revoked and '
                                   'reallocated).',
                     'key_terms': [   {   'definition': 'Mass rescheduling and reallocation of open sales order '
                                                        'confirmations based on business priority.',
                                          'term': 'Backorder Processing (BOP)'},
                                      {   'definition': 'BOP category (Win, Gain, Redistribute, Fill, Lose) governing '
                                                        'how order lines compete for inventory.',
                                          'term': 'Confirmation Strategy'}],
                     'step_id': 'd31_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'BOP dynamically re-allocates inventory during crises to safeguard critical customer '
                                 'relationships.',
                     'title': 'Backorder Processing (BOP) Prioritization Strategies'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'fulfillment_achieved': '100% via ABC',
                                            'pl01_available': 20,
                                            'pl02_available': 25,
                                            'requested_qty': 40},
                     'content_md': '### Rush Order from CUST-501 for 40x DXTR-1000\n'
                                   '- **Primary Delivering Plant**: `PL01` (Heidelberg Assembly)\n'
                                   '  - Unrestricted Stock: 50 EA\n'
                                   '  - Open Reservations: 30 EA\n'
                                   '  - **Available ATP**: **20 EA** (Shortage of 20 EA!)\n'
                                   '- **Without aATP**: Order confirms only 20 EA for immediate delivery, pushing 20 '
                                   'EA out 3 weeks.\n'
                                   '- **With aATP Alternative-Based Confirmation (ABC)**:\n'
                                   '  - System checks alternative plant `PL02` (Austin Tech Center).\n'
                                   '  - PL02 Available ATP: 25 EA.\n'
                                   '  - S/4HANA splits confirmation: Line 10 (20 EA from PL01), Line 20 (20 EA from '
                                   'PL02 via express air freight).\n'
                                   '  - **Result**: 100% on-time customer fulfillment achieved!',
                     'step_id': 'd31_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: aATP Multi-Plant Substitution'},
                 {   'component_type': 'ATPVisualizer',
                     'instruction': 'Toggle Alternative-Based Confirmation (ABC) on and adjust order quantity to '
                                    'simulate how S/4HANA dynamically resolves plant shortages.',
                     'step_id': 'd31_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'title': 'Advanced ATP & Multi-Plant Sourcing Simulator'},
                 {   'options': [   {   'explanation': 'Correct! Product Allocation (PAL) rations scarce supply '
                                                       'according to pre-configured regional or customer quotas.',
                                        'id': 'opt_pal',
                                        'is_correct': True,
                                        'label': "Product Allocation (PAL), which caps the distributor's monthly quota "
                                                 'to a maximum of 15 units, reserving the remaining 85 units for '
                                                 'strategic partner tiers.'},
                                    {   'explanation': 'Absurd distractor.',
                                        'id': 'opt_shut_down',
                                        'is_correct': False,
                                        'label': 'Shut down the ERP server so no orders can be placed.'},
                                    {   'explanation': 'Incorrect. Master data deletion violates data governance and '
                                                       'loses legitimate business.',
                                        'id': 'opt_delete_dist',
                                        'is_correct': False,
                                        'label': 'Delete the wholesale distributor from the Business Partner '
                                                 'database.'}],
                     'scenario_md': 'During a global semiconductor shortage, Nova Manufacturing has only 100 robotics '
                                    'controllers remaining. A discount wholesale distributor submits a single bulk '
                                    "sales order for all 100 units. If accepted, Nova's long-term key accounts in "
                                    'aerospace and medical robotics will face complete stockouts.\n'
                                    '\n'
                                    'Which S/4HANA aATP feature prevents this scenario?',
                     'step_id': 'd31_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Allocation Crisis: Wholesaler Depleting Supply'},
                 {   'questions': [   {   'concept_slug': 'backorder-processing',
                                          'id': 'd31_q1',
                                          'options': [   {   'explanation': "The 'Win' strategy guarantees full "
                                                                            'confirmation regardless of overall stock '
                                                                            'deficit.',
                                                             'id': 'q1_a',
                                                             'is_correct': True,
                                                             'label': 'Win'},
                                                         {   'explanation': "'Lose' completely de-confirms orders.",
                                                             'id': 'q1_b',
                                                             'is_correct': False,
                                                             'label': 'Lose'},
                                                         {   'explanation': "'Redistribute' allows orders to lose "
                                                                            'stock to higher tiers.',
                                                             'id': 'q1_c',
                                                             'is_correct': False,
                                                             'label': 'Redistribute'}],
                                          'points': 10,
                                          'question': 'Under S/4HANA Backorder Processing (BOP), which confirmation '
                                                      'strategy guarantees that an order line item will retain 100% of '
                                                      'its confirmed quantity, taking stock from other orders if '
                                                      'necessary?',
                                          'question_id': 'd31_q1'},
                                      {   'concept_slug': 'advanced-atp-s4',
                                          'id': 'd31_q2',
                                          'options': [   {   'explanation': 'ABC dynamically sources shortages from '
                                                                            'alternative enterprise network nodes.',
                                                             'id': 'q2_a',
                                                             'is_correct': True,
                                                             'label': 'It automatically identifies and substitutes '
                                                                      'alternative plants, storage locations, or '
                                                                      'substitute materials to fulfill the customer '
                                                                      'request on time.'},
                                                         {   'explanation': 'Absurd distractor.',
                                                             'id': 'q2_b',
                                                             'is_correct': False,
                                                             'label': 'It sends a letter of apology in Latin.'},
                                                         {   'explanation': 'Asset revaluation is part of Asset '
                                                                            'Accounting, unrelated to ATP checks.',
                                                             'id': 'q2_c',
                                                             'is_correct': False,
                                                             'label': "It revalues the company's fixed assets in "
                                                                      'ACDOCA.'}],
                                          'points': 10,
                                          'question': 'What business benefit does Alternative-Based Confirmation (ABC) '
                                                      'provide when the primary delivering plant experiences an '
                                                      'inventory deficit?',
                                          'question_id': 'd31_q2'}],
                     'step_id': 'd31_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 31 Assessment: aATP & Allocation Strategies'},
                 {   'concept_slug': 'advanced-atp-s4',
                     'evidence_rule': 'Validates deep understanding of net availability calculations, Product '
                                      'Allocation quotas, and multi-plant ABC substitutions.',
                     'step_id': 'd31_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': 'Demonstrated mastery in S/4HANA Advanced Available-to-Promise rules and '
                                   'fulfillment optimization.',
                     'title': 'Skill Evidence: Advanced ATP'},
                 {   'recommended_mission': {   'description': 'Resolve conflicting customer delivery dates using '
                                                               'advanced ATP product allocation and alternative plant '
                                                               'substitution.',
                                                'slug': 'nova-atp-allocation-conflict',
                                                'title': 'Global ATP & Production Allocation Conflict'},
                     'step_id': 'd31_s8_completion',
                     'step_type': 'completion',
                     'summary_md': '### Core Takeaways\n'
                                   '- aATP guarantees reliable customer delivery dates by verifying net uncommitted '
                                   'supply.\n'
                                   '- Product Allocation (PAL) protects strategic customer relationships from rogue '
                                   'supply depletion.\n'
                                   '- Alternative-Based Confirmation (ABC) enables multi-plant enterprise sourcing '
                                   'networks.\n'
                                   '\n'
                                   'Next: **Day 32 — Outbound Delivery, Picking & Handling Units**!',
                     'title': 'Day 31 Complete: aATP Mastered'}],
    'subtitle': 'Product Allocation (PAL), Alternative-Based Confirmation (ABC), Backorder Processing (BOP), and '
                'multi-plant sourcing',
    'title': 'Order-to-Cash: ATP / aATP'},
    32: {   'atomic_concepts': [   'o2c-outbound-delivery',
                           'shipping-point-determination',
                           'o2c-post-goods-issue',
                           'cogs-accounting-split'],
    'day_number': 32,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-o2c-order-fulfillment-crisis',
    'slug': 'o2c-delivery-picking-pgi',
    'steps': [   {   'content_md': '### From Sales Commitment to Physical Warehouse Execution\n'
                                   'Once a Sales Order is confirmed, logistics execution initiates with the creation '
                                   'of the **Outbound Delivery** (transaction `VL01N` or Fiori app *Create Outbound '
                                   'Deliveries*).\n'
                                   '\n'
                                   'The Outbound Delivery serves as the central operational document controlling:\n'
                                   '1. **Shipping Point Determination**: The system automatically determines the '
                                   'delivering shipping facility using the three-way configuration rule:\n'
                                   '   $$\\text{Shipping Point} = \\text{Shipping Conditions (Customer Master)} + '
                                   '\\text{Loading Group (Material Master)} + \\text{Delivering Plant}$$\n'
                                   '2. **Delivery Scheduling**: Backward and forward scheduling calculates the '
                                   'Material Availability Date, Loading Date, Goods Issue Date, and Customer Delivery '
                                   'Date.\n'
                                   '3. **Route Determination**: Identifies transit path and freight forwarder based on '
                                   'departure zone, shipping condition, and destination country.',
                     'key_terms': [   {   'definition': 'Logistical document orchestrating shipping, picking, packing, '
                                                        'and dispatch.',
                                          'term': 'Outbound Delivery'},
                                      {   'definition': 'Physical enterprise facility where goods are loaded and '
                                                        'dispatched.',
                                          'term': 'Shipping Point'}],
                     'step_id': 'd32_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Shipping Point determination automatically pairs customer shipping preferences with '
                                 'plant loading capabilities.',
                     'title': 'Outbound Delivery Creation & Shipping Point Determination'},
                 {   'content_md': '### Warehouse Picking & Status Progression\n'
                                   'Before goods leave the factory:\n'
                                   '- **Picking (KOSTA)**: Warehouse operators pick materials from storage bin or '
                                   'rack. The picking status transitions from *A (Not yet picked)* to *C (Completely '
                                   'picked)*.\n'
                                   '- **Packing**: Goods are loaded into shipping units or pallets.\n'
                                   '\n'
                                   '### Post Goods Issue (PGI): The Logistical & Financial Pivot\n'
                                   'When the delivery truck departs the dock, the shipping coordinator executes **Post '
                                   'Goods Issue (PGI)** (Movement Type 601):\n'
                                   '1. **Inventory Reduction**: Stock quantity of the finished product is decremented '
                                   'in table `MATDOC`.\n'
                                   '2. **COGS Accounting Recognition**: PGI creates an accounting document in '
                                   '`ACDOCA`:\n'
                                   '   - **Debit**: Cost of Goods Sold (COGS) (e.g. Account 500000 in Nova simulation '
                                   'model)\n'
                                   '   - **Credit**: Finished Goods Inventory Asset (e.g. Account 132000 in Nova '
                                   'simulation model)\n'
                                   '\n'
                                   '> [!IMPORTANT]\n'
                                   '> **Technical Truthfulness Invariant**:\n'
                                   '> Post Goods Issue (PGI) is **NOT** the revenue recognition trigger! PGI documents '
                                   'physical dispatch and posts COGS against inventory. Customer Billing (transaction '
                                   '`VF01`) is the subsequent trigger for Revenue recognition, Accounts Receivable, '
                                   'and Sales Tax.',
                     'key_terms': [   {   'definition': 'Logistical step posting Movement 601 to record physical '
                                                        'inventory departure and COGS.',
                                          'term': 'Post Goods Issue (PGI)'},
                                      {   'definition': 'Direct expense reflecting the standard inventory '
                                                        'manufacturing cost of dispatched goods.',
                                          'term': 'Cost of Goods Sold (COGS)'}],
                     'step_id': 'd32_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'PGI recognizes COGS and relieves inventory asset stock; billing separately '
                                 'recognizes revenue.',
                     'title': 'Warehouse Picking, Packing & Post Goods Issue (PGI / Mov 601)'},
                 {   'company_context': {   'cogs': '€12,000',
                                            'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'delivery_doc': '80010042',
                                            'plant': 'PL01'},
                     'content_md': '### Operational Fulfillment Sequence\n'
                                   '1. **Delivery Created**: Outbound Delivery #80010042 created from Sales Order '
                                   '#5000021000 with Shipping Point 1000.\n'
                                   '2. **Warehouse Picking**: Storage Location FG01 confirms picking of 10 EA '
                                   'DXTR-1000 (Status KOSTA = C).\n'
                                   '3. **PGI Posted**: Movement 601 posts:\n'
                                   '   - Debit: COGS (Account 500000): €12,000.00\n'
                                   '   - Credit: Finished Goods Inventory (Account 132000): €12,000.00',
                     'scenario': 'Customer CUST-501 ordered 10 units of Industrial Robotics Controller DXTR-1000 from '
                                 'Plant PL01 (Heidelberg). Standard manufacturing cost is €1,200/EA.',
                     'step_id': 'd32_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Delivery & PGI Trace'},
                 {   'component_type': 'DeliveryPGITracer',
                     'instruction': 'Step through delivery creation, warehouse picking verification, and PGI posting '
                                    'to observe inventory and COGS movements.',
                     'step_id': 'd32_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Observe that PGI debits COGS and credits inventory without recording any customer '
                                 'receivables or revenue.',
                     'title': '[SIMULATION MODEL] Delivery & PGI Fulfillment Tracer'},
                 {   'instruction': "Evaluate the intern's claim against S/4HANA financial accounting rules.",
                     'options': [   {   'explanation': 'Correct! PGI reflects inventory and COGS; Billing is the '
                                                       'revenue and receivables trigger.',
                                        'id': 'opt_d32_c1',
                                        'is_correct': True,
                                        'text': 'The intern is incorrect. PGI records only physical inventory '
                                                'reduction and Cost of Goods Sold (Dr COGS / Cr Inventory). Customer '
                                                'Receivables and Sales Revenue are recognized subsequently when the '
                                                'Billing Document is created in VF01.'},
                                    {   'explanation': 'Incorrect. Billing is a distinct subsequent process in SD/FI.',
                                        'id': 'opt_d32_c2',
                                        'is_correct': False,
                                        'text': 'The intern is correct. PGI triggers customer invoicing and tax '
                                                'reporting automatically.'},
                                    {   'explanation': 'Incorrect. PGI posts mandatory COGS and inventory reduction '
                                                       'entries in ACDOCA.',
                                        'id': 'opt_d32_c3',
                                        'is_correct': False,
                                        'text': 'PGI has no financial impact whatsoever.'}],
                     'scenario': "An inexperienced logistics intern claims: 'Now that PGI is posted, we have "
                                 "recognized €15,000 in customer sales revenue and debited customer receivables.'",
                     'step_id': 'd32_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Delivery & PGI Accounting Invariant Challenge'},
                 {   'questions': [   {   'concept_slug': 'shipping-point-determination',
                                          'explanation': 'Shipping point determination is configured in TVSTZ '
                                                         'combining Shipping Condition, Loading Group, and Plant.',
                                          'id': 'd32_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Shipping Conditions (Customer) + Loading Group '
                                                                     '(Material) + Delivering Plant.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Purchasing Organization + Vendor Account Group + '
                                                                     'Incoterms.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Profit Center + Cost Center + General Ledger '
                                                                     'Account.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Sales Organization + Distribution Channel + '
                                                                     'Division.'}],
                                          'prompt': 'Which three parameters determine the Shipping Point in an '
                                                    'Outbound Delivery?',
                                          'question_id': 'd32_q1'},
                                      {   'concept_slug': 'o2c-post-goods-issue',
                                          'explanation': 'PGI recognizes the cost of goods sold and relieves '
                                                         'inventory; it does not record revenue.',
                                          'id': 'd32_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Debit: Cost of Goods Sold (COGS) / Credit: '
                                                                     'Finished Goods Inventory.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Debit: Customer Accounts Receivable / Credit: '
                                                                     'Sales Revenue.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Debit: Bank Cash / Credit: Customer Accounts '
                                                                     'Receivable.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Debit: GR/IR Interim Clearing / Credit: Vendor '
                                                                     'Accounts Payable.'}],
                                          'prompt': 'What financial accounting entry is generated in table ACDOCA upon '
                                                    'posting Goods Issue (Movement Type 601)?',
                                          'question_id': 'd32_q2'}],
                     'step_id': 'd32_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 32 Mastery Assessment: Delivery, Picking & PGI'},
                 {   'step_id': 'd32_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Configured Shipping Point determination parameters.\n'
                                   '- Traced warehouse picking and packing status progression (KOSTA).\n'
                                   '- Validated Movement 601 financial posting (COGS vs Inventory asset) without '
                                   'confusing PGI with revenue recognition.',
                     'title': 'Mastery Verification: Delivery & PGI Execution'},
                 {   'recommended_mission': {   'description': 'Coordinate shipping point determination, picking, and '
                                                               'PGI execution.',
                                                'slug': 'nova-o2c-order-fulfillment-crisis',
                                                'title': 'Order-to-Cash Fulfillment & Credit Crisis'},
                     'step_id': 'd32_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered Outbound Delivery and Post Goods Issue. Next, you will study '
                                   'Billing Document creation and FI Integration.',
                     'title': 'Day 32 Complete: Delivery, Picking & PGI Mastered'}],
    'subtitle': 'Outbound Delivery (VL01N), shipping point determination, warehouse picking (KOSTA), and Post Goods '
                'Issue (Mov 601 / COGS)',
    'title': 'Order-to-Cash: Delivery, Picking & PGI'},
    33: {   'atomic_concepts': ['o2c-billing-creation', 'revenue-recognition-posting'],
    'day_number': 33,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-o2c-billing-fi-reconciliation',
    'slug': 'o2c-billing-fi-integration',
    'steps': [   {   'content_md': '### Customer Billing in Order-to-Cash\n'
                                   'In SAP S/4HANA Sales & Distribution (SD), the **Billing Document** is the final '
                                   'transactional stage of the logistics fulfillment cycle and the direct integration '
                                   'bridge to Financial Accounting (FI).\n'
                                   '\n'
                                   'Key Billing Characteristics:\n'
                                   '1. **Creation Trigger**: Executed via transaction `VF01` (Create Billing Document) '
                                   'or automated background billing runs (transaction `VF04` / Fiori app "Create '
                                   'Billing Documents"). Standard invoices reference preceding Outbound Deliveries.\n'
                                   '2. **Standard Billing Type (`F2`)**: Represents standard commercial customer '
                                   'invoices generated from delivery items that have completed picking and Post Goods '
                                   'Issue (PGI).\n'
                                   '3. **Core Database Tables**:\n'
                                   '   - `VBRK`: Billing document header data (Billing type, Sales Organization, Payer '
                                   'partner, Billing date, Total net value).\n'
                                   '   - `VBRP`: Billing document item data (Material DXTR-1000, Invoiced quantity, '
                                   'Net price, Item condition values, Tax codes).',
                     'key_terms': [   {   'definition': 'SD document generated from deliveries to formally bill '
                                                        'customers and trigger FI postings.',
                                          'term': 'Billing Document (VF01)'},
                                      {   'definition': 'Standard customer invoice type in SAP Sales and Distribution.',
                                          'term': 'Billing Type F2'},
                                      {   'definition': 'Authoritative header and item transparent tables for billing '
                                                        'documents in S/4HANA.',
                                          'term': 'Tables VBRK & VBRP'}],
                     'step_id': 'd33_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Customer billing in VF01 formalizes commercial invoices and triggers automated '
                                 'financial accounting integration.',
                     'title': 'Customer Billing (VF01) & Billing Types (F2)'},
                 {   'content_md': '### Revenue Account Determination (Condition Technique)\n'
                                   'When a billing document is saved in `VF01`, SAP S/4HANA does not require users to '
                                   'enter G/L accounts manually. Instead, the system automatically determines G/L '
                                   'accounts using table **`VKOA`** based on the Condition Technique:\n'
                                   '- Evaluates Application (`V` for SD), Condition Type (e.g. `KOFI`), Chart of '
                                   'Accounts (`YCOA`), Sales Organization (`SO01`), Customer Account Assignment Group, '
                                   'Material Account Assignment Group, and **Account Key**:\n'
                                   '  - **Account Key `ERL`**: Standard Gross Sales Revenue. Routes to Domestic Sales '
                                   'Revenue Account (Account 410000 in Nova simulation model).\n'
                                   '  - **Account Key `ERS`**: Sales Deductions (discounts, rebates, allowances).\n'
                                   '  - **Account Key `MWS`**: Output Sales Tax. Routes to Output Tax Payable Account '
                                   '(Account 217000 in Nova simulation model).\n'
                                   '\n'
                                   '### Universal Journal (`ACDOCA`) Postings\n'
                                   '> **CRITICAL SAP INVARIANT**: Post Goods Issue (PGI) records inventory reduction '
                                   'and COGS. Billing (`VF01`) is the authoritative trigger for Revenue, Accounts '
                                   'Receivable, and Sales Tax recognition in `ACDOCA`!\n'
                                   '>\n'
                                   '> *(Note: Account numbers 121000, 410000, and 217000 are Nova simulation model '
                                   'examples, not universal SAP standards).*\n'
                                   '\n'
                                   '$$\\begin{aligned}\n'
                                   '\\text{Debit: } & \\text{Customer Accounts Receivable (Account 121000)} & '
                                   '€3,570.00 \\\\\n'
                                   '\\text{Credit: } & \\text{Domestic Sales Revenue (Account 410000, Key ERL)} & '
                                   '€3,000.00 \\\\\n'
                                   '\\text{Credit: } & \\text{Output Sales Tax 19% (Account 217000, Key MWS)} & '
                                   '€570.00\n'
                                   '\\end{aligned}$$',
                     'key_terms': [   {   'definition': 'Customizing table driving automatic revenue and tax account '
                                                        'determination in SD.',
                                          'term': 'Table VKOA'},
                                      {   'definition': 'Key assigned to pricing conditions in the pricing procedure '
                                                        'routing gross revenue to G/L accounts.',
                                          'term': 'Account Key ERL'},
                                      {   'definition': 'In standard SAP S/4HANA O2C, saving the billing document in '
                                                        'VF01 triggers revenue and AR posting.',
                                          'term': 'Revenue Trigger'}],
                     'step_id': 'd33_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Table VKOA and Account Keys (ERL, MWS) seamlessly map SD pricing lines into balanced '
                                 'ACDOCA journal entries.',
                     'title': 'Revenue Account Determination (VKOA) & ACDOCA Posting'},
                 {   'company_context': {   'billing_doc': '900055',
                                            'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'delivery_doc': '800021',
                                            'gross_amount': '€3,570.00',
                                            'net_amount': '€3,000.00',
                                            'sales_org': 'SO01',
                                            'tax_amount': '€570.00'},
                     'content_md': '### Transaction Trace & ACDOCA Creation\n'
                                   '1. **Source Document**: Outbound Delivery #800021 confirmed with Picking Status '
                                   '`C` and Goods Movement Status `C`.\n'
                                   '2. **Billing Generation**: Transaction `VF01` creates Invoice #900055 (Type F2).\n'
                                   '3. **Account Determination**:\n'
                                   '   - Condition `PR00` (€3,000.00) maps via Account Key `ERL` to G/L Account '
                                   '410000.\n'
                                   '   - Condition `MWST` (€570.00) maps via Account Key `MWS` to G/L Account 217000.\n'
                                   '4. **Accounting Document**: Subledger Customer CUST-501 debited €3,570.00 '
                                   '(synchronously updating AR Reconciliation Account 121000 in `ACDOCA`).',
                     'scenario': 'Billing clerk executes VF01 for Outbound Delivery #800021 (2 EA Robotics Controller '
                                 'DXTR-1000 for customer CUST-501).',
                     'step_id': 'd33_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Billing Run: Order #100045 Fulfillment'},
                 {   'component_type': 'BillingAccountingFlow',
                     'instruction': 'Examine the billing document lines, verify condition types PR00 and MWST, and '
                                    'inspect the resulting debit and credit postings in table ACDOCA.',
                     'step_id': 'd33_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Billing document generation links logistics delivery confirmation with financial '
                                 'revenue recognition.',
                     'title': '[SIMULATION MODEL] Billing & Revenue Account Determination Simulator'},
                 {   'instruction': 'Select the correct SAP architectural explanation.',
                     'options': [   {   'explanation': 'Correct! PGI records physical goods dispatch and COGS, whereas '
                                                       'billing creation in VF01 is the authoritative trigger for '
                                                       'revenue and receivables recognition.',
                                        'id': 'opt_d33_correct',
                                        'is_correct': True,
                                        'text': 'No error. In standard SAP S/4HANA Order-to-Cash, Post Goods Issue '
                                                '(PGI) only posts inventory reduction and Cost of Goods Sold (Dr COGS '
                                                '/ Cr Inventory). Customer Accounts Receivable and Sales Revenue are '
                                                'only recognized when the Billing Document is created in VF01.'},
                                    {   'explanation': 'Incorrect. Conflating PGI with revenue recognition violates '
                                                       'standard SAP accounting principles.',
                                        'id': 'opt_d33_err1',
                                        'is_correct': False,
                                        'text': 'System error. PGI should have immediately debited Customer AR and '
                                                'credited Sales Revenue simultaneously with inventory reduction.'},
                                    {   'explanation': 'Incorrect. Sales orders create legal commitments, not '
                                                       'financial balance sheet postings.',
                                        'id': 'opt_d33_err2',
                                        'is_correct': False,
                                        'text': 'System error. Customer AR and Revenue are posted when the Sales Order '
                                                '(VA01) is initially saved, not during delivery or billing.'}],
                     'scenario': 'A junior billing specialist notices that after Post Goods Issue (PGI) is posted for '
                                 "a sales order, the Customer's Accounts Receivable subledger and Sales Revenue have "
                                 'not yet increased. The specialist asks if this is a system error. What is the '
                                 'correct explanation?',
                     'step_id': 'd33_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Revenue Recognition Timing Challenge'},
                 {   'questions': [   {   'concept_slug': 'o2c-billing-creation',
                                          'explanation': 'Transaction VF01 creates billing documents, and table VBRK '
                                                         'stores billing document header records.',
                                          'id': 'd33_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Transaction VF01 and table VBRK'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Transaction VA01 and table VBAK'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Transaction VL01N and table LIKP'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Transaction MIRO and table RBKP'}],
                                          'prompt': 'Which SAP transaction code and database table are used to create '
                                                    'standard customer billing documents and store billing document '
                                                    'headers?',
                                          'question_id': 'd33_q1'},
                                      {   'concept_slug': 'revenue-recognition-posting',
                                          'explanation': 'Account Key ERL routes standard gross sales revenue to the '
                                                         'designated G/L revenue account.',
                                          'id': 'd33_q2',
                                          'options': [   {'id': 'a', 'is_correct': True, 'text': 'Account Key ERL'},
                                                         {'id': 'b', 'is_correct': False, 'text': 'Account Key MWS'},
                                                         {'id': 'c', 'is_correct': False, 'text': 'Account Key WRX'},
                                                         {'id': 'd', 'is_correct': False, 'text': 'Account Key BSX'}],
                                          'prompt': 'In SAP SD automatic account determination (table VKOA), which '
                                                    'Account Key is configured to route standard gross product sales '
                                                    'revenue to the appropriate G/L revenue account (e.g. Account '
                                                    '410000)?',
                                          'question_id': 'd33_q2'}],
                     'step_id': 'd33_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 33 Mastery Assessment: Billing & FI Integration'},
                 {   'step_id': 'd33_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Created customer billing documents (VF01, Billing Type F2) from deliveries.\n'
                                   '- Configured and traced automatic revenue account determination via table VKOA.\n'
                                   '- Mapped pricing conditions via Account Keys (ERL, MWS) to financial postings in '
                                   'ACDOCA.\n'
                                   '- Distinguished logistical dispatch accounting (PGI / Mov 601) from commercial '
                                   'revenue recognition.',
                     'title': 'Mastery Verification: Billing & FI Integration'},
                 {   'recommended_mission': {   'description': 'Resolve billing document interface failures held in '
                                                               'transaction VFX3.',
                                                'slug': 'nova-o2c-billing-fi-reconciliation',
                                                'title': 'O2C Billing & Financial Accounting Reconciliation'},
                     'step_id': 'd33_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered customer billing and its seamless integration into Financial '
                                   'Accounting. Next, you will explore handling O2C exceptions, customer returns, and '
                                   'billing block recovery in VFX3.',
                     'title': 'Day 33 Complete: Billing & FI Integration Mastered'}],
    'subtitle': 'Customer billing (VF01), VKOA revenue account determination, output taxes, and Accounts Receivable '
                'updates',
    'title': 'Order-to-Cash: Billing + FI Integration'},
    34: {   'atomic_concepts': ['o2c-returns-processing', 'credit-memo-requests'],
    'day_number': 34,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-o2c-billing-fi-reconciliation',
    'slug': 'o2c-exceptions-troubleshooting',
    'steps': [   {   'content_md': '### Operational Sales Exceptions & Returns Lifecycle\n'
                                   'When a customer rejects delivered goods due to defect or shipping damage, the '
                                   'fulfillment exception is processed via the **Returns Order (Order Type RE)**.\n'
                                   '\n'
                                   'Returns Workflow:\n'
                                   '1. **Returns Order (`RE`)**: Created referencing the original sales order or '
                                   'billing document. Specifies reason for return (e.g., transit damage, wrong '
                                   'component).\n'
                                   '2. **Returns Delivery (transaction `VL01N`)**: Logistical document routing goods '
                                   'back to the plant warehouse.\n'
                                   '3. **Goods Receipt for Return Delivery**:\n'
                                   '   - **Movement Type 651**: Posts returned goods into **Returns Blocked Stock** '
                                   '(quarantine) without immediate valuation change.\n'
                                   '   - **Movement Type 653**: Posts returned goods directly into **Unrestricted-Use '
                                   'Stock** if items are in pristine resalable condition.',
                     'key_terms': [   {   'definition': 'Sales document type authorizing a customer to return shipped '
                                                        'goods.',
                                          'term': 'Returns Order (RE)'},
                                      {   'definition': 'Goods receipt for customer return into returns blocked stock.',
                                          'term': 'Movement Type 651'}],
                     'step_id': 'd34_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Customer returns route goods back into warehouse stock through controlled inspection '
                                 'movement types.',
                     'title': 'Customer Returns (RE) & Returns Delivery (Mov 651/653)'},
                 {   'content_md': '### Credit Memo Requests & Credit Memos\n'
                                   'Once the warehouse inspects and accepts returned goods:\n'
                                   '1. **Credit Memo Request (`CR`)**: Sales document created to authorize a financial '
                                   "refund or credit to the customer's account. Subject to managerial approval via a "
                                   'billing block.\n'
                                   '2. **Credit Memo (`VF01`)**: Once the billing block is removed, the credit memo '
                                   'generates a financial posting in `ACDOCA`:\n'
                                   '   $$\\begin{aligned}\n'
                                   '   \\text{Debit: } & \\text{Sales Revenue / Sales Deductions (Account 410000)} & '
                                   '€3,000.00 \\\\\n'
                                   '   \\text{Debit: } & \\text{Output Sales Tax (Account 217000)} & €570.00 \\\\\n'
                                   '   \\text{Credit: } & \\text{Customer Accounts Receivable (Account 121000)} & '
                                   '€3,570.00\n'
                                   '   \\end{aligned}$$\n'
                                   '\n'
                                   '### Troubleshooting Billing Blocks in Transaction VFX3\n'
                                   'When billing documents cannot post to financial accounting due to configuration '
                                   'errors (e.g. `VF051 Account determination error`), they are held in transaction '
                                   '**`VFX3`** (Release Billing Documents for Accounting):\n'
                                   '- The administrator identifies the missing Account Key or G/L mapping in table '
                                   '`VKOA`.\n'
                                   '- Maintains configuration and releases the document, triggering instantaneous '
                                   'Universal Journal generation in `ACDOCA`.',
                     'key_terms': [   {   'definition': 'Sales document authorizing a customer credit note with '
                                                        'optional billing block.',
                                          'term': 'Credit Memo Request (CR)'},
                                      {   'definition': 'Diagnostic monitor for analyzing and releasing billing '
                                                        'documents blocked from accounting.',
                                          'term': 'Transaction VFX3'}],
                     'step_id': 'd34_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Credit memos reduce customer receivables and reverse revenue; VFX3 resolves '
                                 'accounting interface blocks.',
                     'title': 'Credit Memo Requests (CR) & VFX3 Billing Release Troubleshooting'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'credit_memo': '€3,570',
                                            'order_type': 'RE'},
                     'content_md': '### Returns & Credit Memo Progression\n'
                                   '1. **Returns Order Created**: Order #60001020 (Type RE) created referencing '
                                   'Billing Doc #900055.\n'
                                   '2. **Returns Delivery Posted**: Movement Type 651 posts 2 EA into Storage Location '
                                   'FG01 (Returns Blocked Stock).\n'
                                   '3. **Credit Memo Issued**: Credit Memo Request approved; Billing Doc #950001 '
                                   'posts:\n'
                                   '   - Debit: Sales Revenue (410000): €3,000.00\n'
                                   '   - Debit: Output Tax (217000): €570.00\n'
                                   '   - Credit: Customer AR (121000): €3,570.00',
                     'scenario': 'Customer CUST-501 returns 2 damaged robotics controllers DXTR-1000 billed at '
                                 '€1,500/EA (€3,000 total + 19% VAT).',
                     'step_id': 'd34_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Returns Trace: Damaged Controller'},
                 {   'component_type': 'ScenarioDecision',
                     'instruction': 'Diagnose the billing document blocked in transaction VFX3 with error VF051 and '
                                    'execute the proper corrective procedure.',
                     'options': [   {   'explanation': 'Correct! VKOA provides the G/L mapping and VFX3 triggers '
                                                       'accounting document creation.',
                                        'id': 'opt_d34_vfx3',
                                        'is_correct': True,
                                        'text': 'Maintain missing revenue account mapping in table VKOA for Account '
                                                'Key ERL, then execute transaction VFX3 to release the document to '
                                                'ACDOCA.'},
                                    {   'explanation': 'Bypasses system audit controls and breaks document flow.',
                                        'id': 'opt_d34_delete_doc',
                                        'is_correct': False,
                                        'text': 'Delete the billing document and issue an invoice manually on paper.'},
                                    {   'explanation': 'Causes substantial enterprise financial loss.',
                                        'id': 'opt_d34_credit_all',
                                        'is_correct': False,
                                        'text': "Credit the customer's entire account balance."}],
                     'step_id': 'd34_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'VFX3 acts as the central clearinghouse for billing interface errors.',
                     'title': '[SIMULATION MODEL] O2C Exceptions & VFX3 Recovery Simulator'},
                 {   'instruction': 'Select the compliant SAP operational answer.',
                     'options': [   {   'explanation': 'Correct! Enforces physical inspection before financial '
                                                       'liability adjustment.',
                                        'id': 'opt_d34_compliant',
                                        'is_correct': True,
                                        'text': 'Create a Returns Order (type RE), generate a Returns Delivery with '
                                                'Movement Type 651 into returns blocked stock for quality inspection, '
                                                'and issue a Credit Memo Request (type CR) after warehouse inspection '
                                                'clearance.'},
                                    {   'explanation': 'Violates internal inventory and accounting control policies.',
                                        'id': 'opt_d34_cash',
                                        'is_correct': False,
                                        'text': 'Wire cash immediately to the customer without creating any return '
                                                'delivery or checking warehouse stock.'},
                                    {   'explanation': 'Breaks transactional audit trail in ACDOCA.',
                                        'id': 'opt_d34_delete',
                                        'is_correct': False,
                                        'text': 'Delete the original customer sales order and invoice from the '
                                                'database.'}],
                     'scenario': 'Customer CUST-501 returns 2 damaged controllers. The sales rep wants to issue a cash '
                                 'refund directly without inspecting the returned goods.',
                     'step_id': 'd34_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Customer Return & Credit Memo Processing Challenge'},
                 {   'questions': [   {   'concept_slug': 'o2c-returns-processing',
                                          'explanation': 'Movement 651 receives customer returns into returns blocked '
                                                         'stock for quality inspection.',
                                          'id': 'd34_q1',
                                          'options': [   {'id': 'a', 'is_correct': True, 'text': 'Movement Type 651'},
                                                         {'id': 'b', 'is_correct': False, 'text': 'Movement Type 601'},
                                                         {'id': 'c', 'is_correct': False, 'text': 'Movement Type 101'},
                                                         {'id': 'd', 'is_correct': False, 'text': 'Movement Type 261'}],
                                          'prompt': 'Which movement type is used when receiving customer returned '
                                                    'goods into warehouse returns blocked stock pending inspection?',
                                          'question_id': 'd34_q1'},
                                      {   'concept_slug': 'credit-memo-requests',
                                          'explanation': 'Transaction VFX3 displays and releases billing documents '
                                                         'held by accounting interface errors.',
                                          'id': 'd34_q2',
                                          'options': [   {'id': 'a', 'is_correct': True, 'text': 'VFX3'},
                                                         {'id': 'b', 'is_correct': False, 'text': 'VA01'},
                                                         {'id': 'c', 'is_correct': False, 'text': 'ME21N'},
                                                         {'id': 'd', 'is_correct': False, 'text': 'FB50'}],
                                          'prompt': 'In SAP S/4HANA, which transaction code is used by billing '
                                                    'administrators to diagnose and release billing documents blocked '
                                                    'from posting to accounting?',
                                          'question_id': 'd34_q2'}],
                     'step_id': 'd34_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 34 Mastery Assessment: O2C Exceptions & Troubleshooting'},
                 {   'step_id': 'd34_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Processed Customer Returns orders (RE) and returns deliveries (Mov 651).\n'
                                   '- Generated Credit Memo Requests (CR) and verified financial postings in ACDOCA.\n'
                                   '- Diagnosed and released blocked billing documents in transaction VFX3.',
                     'title': 'Mastery Verification: O2C Exceptions & Recovery'},
                 {   'recommended_mission': {   'description': 'Resolve billing document interface failures held in '
                                                               'transaction VFX3.',
                                                'slug': 'nova-o2c-billing-fi-reconciliation',
                                                'title': 'O2C Billing & Financial Accounting Reconciliation'},
                     'step_id': 'd34_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered Order-to-Cash exception resolution and credit memo processing. '
                                   'Next, you will advance to Financial Accounting.',
                     'title': 'Day 34 Complete: O2C Exceptions Mastered'}],
    'subtitle': 'Resolving sales fulfillment exceptions, customer returns (RE), credit memos (CR), and billing release '
                'blocks (VFX3)',
    'title': 'Order-to-Cash: O2C Exceptions & Troubleshooting'},
    35: {   'atomic_concepts': ['gl-journal-entry', 'field-status-groups', 'posting-keys'],
    'day_number': 35,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-gl-period-end-closing',
    'slug': 'finance-general-ledger',
    'steps': [   {   'content_md': '### The Authoritative Record of Financial Truth\n'
                                   'In SAP S/4HANA, all enterprise financial transactions—whether originated in '
                                   'Procurement, Sales, Manufacturing, or Payroll—culminate in the **General Ledger '
                                   '(G/L)** stored in the **Universal Journal (`ACDOCA`)**.\n'
                                   '\n'
                                   'Finance accountants also post direct manual adjustments, accruals, and transfers '
                                   'using **Enter G/L Account Document (transaction FB50 / Fiori app Post General '
                                   'Journal Entries)**.\n'
                                   '\n'
                                   '### Posting Keys and Document Types\n'
                                   'Traditional SAP FI relies on foundational control parameters:\n'
                                   '- **Document Type (`BKPF-BLART`)**: Two-character key classifying the transaction '
                                   'and governing number ranges:\n'
                                   '  - `SA`: Standard G/L Account Document.\n'
                                   '  - `KR`: Vendor Invoice | `KZ`: Vendor Payment.\n'
                                   '  - `DR`: Customer Invoice | `DZ`: Customer Payment.\n'
                                   '- **Posting Key (`BSEG-BSCHL`)**: Two-digit code governing the line item:\n'
                                   '  - **40**: G/L Account Debit.\n'
                                   '  - **50**: G/L Account Credit.\n'
                                   '  - **01**: Customer Debit | **11**: Customer Credit.\n'
                                   '  - **21**: Vendor Debit | **31**: Vendor Credit.',
                     'key_terms': [   {   'definition': 'Single-screen General Ledger journal entry transaction in SAP '
                                                        'GUI / Fiori.',
                                          'term': 'FB50'},
                                      {   'definition': 'Key classifying financial documents (e.g. SA for general '
                                                        'ledger, KR for vendor invoice).',
                                          'term': 'Document Type (BLART)'},
                                      {   'definition': 'Numeric key (e.g. 40 Debit, 50 Credit) determining account '
                                                        'type and debit/credit sign.',
                                          'term': 'Posting Key'}],
                     'step_id': 'd37_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Document types categorize transactions; posting keys (40 Debit / 50 Credit) control '
                                 'line-item behavior in ACDOCA.',
                     'title': 'The Core of Financial Accounting: General Ledger Journal Entries'},
                 {   'content_md': '### Field Status Groups (Transaction OBC4)\n'
                                   'When posting a journal entry, which fields are mandatory? Should the user enter a '
                                   'Cost Center, a Profit Center, a Value Date, or a Tax Code?\n'
                                   'This is controlled by the **Field Status Group (FSG)** assigned to each G/L '
                                   'account master record:\n'
                                   '- **Suppress**: Field is completely hidden.\n'
                                   '- **Required Entry**: System throws a hard error if the user leaves the field '
                                   'blank.\n'
                                   '- **Optional Entry**: User may enter data or leave it blank.\n'
                                   '\n'
                                   '*Example*: Expense accounts (e.g. G/L `540000` Travel Expense) are assigned FSG '
                                   '`G004` (Cost accounts), making **Cost Center** mandatory so expenses cannot bypass '
                                   'controlling!\n'
                                   '\n'
                                   '### The Balance Invariant\n'
                                   'Under double-entry accounting rules, S/4HANA strictly enforces:\n'
                                   '$$\\sum \\text{Debits} = \\sum \\text{Credits}$$\n'
                                   'If debits do not equal credits in company code currency, S/4HANA refuses to post '
                                   'the document, keeping status in *Parked* or throwing a balancing error.',
                     'key_terms': [   {   'definition': 'Configuration rule in OBC4 determining whether fields are '
                                                        'Suppressed, Required, or Optional.',
                                          'term': 'Field Status Group (FSG)'},
                                      {   'definition': 'Draft financial document saved without posting to General '
                                                        'Ledger balances.',
                                          'term': 'Parked Document'}],
                     'step_id': 'd37_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Field Status Groups enforce mandatory controlling fields; balance equality (Debit = '
                                 'Credit) is strictly enforced.',
                     'title': 'Field Status Groups (FSG) & Document Balance Invariants'},
                 {   'company_context': {   'amount': 12500.0,
                                            'company_code': 'NM01',
                                            'cost_center': 'CC-ENG-01',
                                            'credit_gl': '211300',
                                            'debit_gl': '540000',
                                            'doc_type': 'SA',
                                            'document_number': '100005510'},
                     'content_md': '### Accruing Consulting Expenses at Plant PL01\n'
                                   'Chief Accountant Elena Rostova posts month-end engineering consulting accrual:\n'
                                   '- **Document Type**: `SA` | Company Code: `NM01`\n'
                                   '- **Posting Date**: 2026-09-30 | Ledger: `0L` (Leading Ledger)\n'
                                   '\n'
                                   '**Journal Lines (ACDOCA)**:\n'
                                   '1. **PK 40 (Debit)**: G/L `540000` (Consulting Expense) €12,500.00\n'
                                   '   - Field Status Group G004 requires Cost Center: `CC-ENG-01`\n'
                                   '2. **PK 50 (Credit)**: G/L `211300` (Accrued Liabilities) €12,500.00\n'
                                   '   - Cost center suppressed on balance sheet liability.\n'
                                   '\n'
                                   '**Result**: Document `#100005510` posted cleanly. Debits (€12,500) = Credits '
                                   '(€12,500).',
                     'step_id': 'd37_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: Month-End Accrual Posting'},
                 {   'component_type': 'UniversalJournalVisualizer',
                     'instruction': 'Inspect how manual G/L journal entries populate multi-dimension records (Company '
                                    'Code, G/L, Cost Center, Profit Center) in table ACDOCA.',
                     'step_id': 'd37_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'title': 'Universal Journal ACDOCA Inspector'},
                 {   'options': [   {   'explanation': 'Correct! A conflict between Posting Key field status and G/L '
                                                       'Field Status Group causes fields to hide while remaining '
                                                       'mandatory.',
                                        'id': 'opt_fsg_conflict',
                                        'is_correct': True,
                                        'label': "The Field Status Group assigned to G/L 560000 has 'Cost Center' set "
                                                 "to 'Suppress' in OBC4, while the Posting Key 40 or G/L master record "
                                                 'marked it as mandatory. The conflict can be resolved by setting Cost '
                                                 "Center to 'Required' or 'Optional' in FSG OBC4."},
                                    {   'explanation': 'Absurd distractor.',
                                        'id': 'opt_buy_license',
                                        'is_correct': False,
                                        'label': 'Nova Manufacturing must purchase an extra database license from '
                                                 'SAP.'},
                                    {   'explanation': 'Catastrophic error destroying enterprise cost accounting.',
                                        'id': 'opt_delete_co',
                                        'is_correct': False,
                                        'label': 'Delete Controlling area NM01.'}],
                     'scenario_md': 'An accountant attempts to post an advertising expense entry in FB50 to G/L '
                                    "560000, but the system throws error F5165: *'Account 560000 requires an "
                                    "assignment to a CO object'*. The accountant complains that the Cost Center field "
                                    'is completely missing from the screen!\n'
                                    '\n'
                                    'Why is this error occurring?',
                     'step_id': 'd37_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Field Status Configuration Conflict'},
                 {   'questions': [   {   'concept_slug': 'posting-keys',
                                          'id': 'd37_q1',
                                          'options': [   {   'explanation': 'Posting Key 40 represents G/L Account '
                                                                            'Debit; Posting Key 50 represents G/L '
                                                                            'Account Credit.',
                                                             'id': 'q1_a',
                                                             'is_correct': True,
                                                             'label': 'Posting Key 40'},
                                                         {   'explanation': 'Posting Key 01 is Customer Debit '
                                                                            '(Invoice).',
                                                             'id': 'q1_b',
                                                             'is_correct': False,
                                                             'label': 'Posting Key 01'},
                                                         {   'explanation': 'Posting Key 31 is Vendor Credit '
                                                                            '(Invoice).',
                                                             'id': 'q1_c',
                                                             'is_correct': False,
                                                             'label': 'Posting Key 31'}],
                                          'points': 10,
                                          'question': 'What is the standard SAP posting key used to debit a General '
                                                      'Ledger account in a standard manual journal entry?',
                                          'question_id': 'd37_q1'},
                                      {   'concept_slug': 'field-status-groups',
                                          'id': 'd37_q2',
                                          'options': [   {   'explanation': 'Field Status Groups are maintained per '
                                                                            'company code in G/L account master '
                                                                            'records.',
                                                             'id': 'q2_a',
                                                             'is_correct': True,
                                                             'label': 'In the Company Code segment of the G/L Account '
                                                                      'Master Record (table SKB1 / transaction FS00).'},
                                                         {   'explanation': 'Nonsense distractor.',
                                                             'id': 'q2_b',
                                                             'is_correct': False,
                                                             'label': "In the user's browser cookie settings."},
                                                         {   'explanation': 'Shipping points belong to SD logistics, '
                                                                            'completely unrelated to FI field '
                                                                            'statuses.',
                                                             'id': 'q2_c',
                                                             'is_correct': False,
                                                             'label': 'In the shipping point configuration table.'}],
                                          'points': 10,
                                          'question': 'Where is the Field Status Group (FSG) assigned to control '
                                                      'whether fields like Cost Center or Business Area appear during '
                                                      'journal entry?',
                                          'question_id': 'd37_q2'}],
                     'step_id': 'd37_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 37 Assessment: G/L Journals & Field Status'},
                 {   'concept_slug': 'gl-journal-entry',
                     'evidence_rule': 'Validates proficiency in FB50 journal creation, Document Type and Posting Key '
                                      'rules, Field Status Group (OBC4) controls, and ACDOCA multi-dimension '
                                      'recording.',
                     'step_id': 'd37_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': 'Demonstrated mastery in S/4HANA General Ledger document posting and control '
                                   'configuration.',
                     'title': 'Skill Evidence: General Ledger Journal Entries'},
                 {   'recommended_mission': {   'description': 'Execute financial period closing operations and '
                                                               'balance sheet reconciliation.',
                                                'slug': 'nova-gl-period-end-closing',
                                                'title': 'Financial Period-End Closing & Variance Recovery'},
                     'step_id': 'd37_s8_completion',
                     'step_type': 'completion',
                     'summary_md': '### Core Takeaways\n'
                                   '- G/L journal entries record financial truth in ACDOCA under strict debit/credit '
                                   'balancing invariants.\n'
                                   '- Document types (SA) and Posting keys (40 Debit / 50 Credit) standardize line '
                                   'item behavior.\n'
                                   '- Field Status Groups (OBC4) enforce mandatory cost center and controlling '
                                   'allocations.\n'
                                   '\n'
                                   'Next: **Day 38 — AP & AR Subledger Operations & Special G/L Indicators**!',
                     'title': 'Day 37 Complete: General Ledger Mastered'}],
    'subtitle': 'S/4HANA Universal Journal (ACDOCA), journal entries (FB50), posting keys (40/50), and field status '
                'groups',
    'title': 'Finance: General Ledger'},
    36: {   'atomic_concepts': ['ap-ar-subledger-operations', 'special-gl-indicators'],
    'day_number': 36,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-f110-payment-exception-run',
    'slug': 'finance-accounts-payable',
    'steps': [   {   'content_md': '### The Accounts Payable (FI-AP) Subledger\n'
                                   'In SAP S/4HANA, Accounts Payable manages liabilities owed to external suppliers '
                                   '(Business Partner role Supplier).\n'
                                   '\n'
                                   'Key Architectural Invariants:\n'
                                   '1. **Subledger to General Ledger Link**: Suppliers are not maintained as '
                                   'individual G/L accounts. Instead, every vendor master record is assigned a '
                                   '**Reconciliation Account** (e.g. Account 211000 in Nova simulation model) in '
                                   'company code data.\n'
                                   '2. **Real-Time Integration**: Postings to a vendor account synchronously update '
                                   'the vendor subledger and the associated G/L reconciliation account in `ACDOCA`.\n'
                                   '3. **No Direct Postings**: Manual direct postings to reconciliation accounts are '
                                   'prohibited; all updates flow through subledger transactions (e.g. `MIRO`, `FB60`).',
                     'key_terms': [   {   'definition': 'G/L account automatically updated when postings are made to '
                                                        'customer or vendor subledgers.',
                                          'term': 'Reconciliation Account'},
                                      {   'definition': 'Accounting method where debit and credit line items remain '
                                                        'open until explicitly matched and cleared.',
                                          'term': 'Open Item Management'}],
                     'step_id': 'd36_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Reconciliation accounts guarantee automatic alignment between detailed vendor '
                                 'subledgers and the general ledger.',
                     'title': 'Vendor Subledger & Reconciliation Account Architecture'},
                 {   'content_md': '### Special G/L Indicators (e.g. Down Payments)\n'
                                   'Standard invoices update the default reconciliation account. However, certain '
                                   'transactions must post to alternative balance sheet lines:\n'
                                   "- **Special G/L Indicator 'A' (Down Payments)**: Reroutes postings to an "
                                   'alternative reconciliation account (e.g. Advances to Suppliers 133000) rather than '
                                   'standard AP.\n'
                                   '\n'
                                   '### Automatic Payment Program (F110)\n'
                                   'Corporate treasury uses transaction `F110` to disburse payments to hundreds of '
                                   'suppliers automatically:\n'
                                   '1. **Parameters**: Company Code, Payment Methods (SEPA, Check, Wire), Next Posting '
                                   'Date.\n'
                                   '2. **Proposal Run**: S/4HANA selects due invoices based on cash discount terms and '
                                   'baseline dates.\n'
                                   '3. **Exception List**: Displays blocked items (e.g. missing IBAN, payment block '
                                   "'R').\n"
                                   '4. **Payment Run**: Generates electronic bank payment files (ISO 20022 / pain.001 '
                                   'XML) and clears vendor open items in `ACDOCA`.',
                     'key_terms': [   {   'definition': 'Code directing postings to alternative reconciliation '
                                                        'accounts without changing master data.',
                                          'term': 'Special G/L Indicator'},
                                      {   'definition': 'Automated batch program for evaluating due invoices, '
                                                        'generating bank clearing files, and clearing AP.',
                                          'term': 'F110 Payment Run'}],
                     'step_id': 'd36_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'F110 automates treasury disbursements while Special G/L indicators correctly isolate '
                                 'down payments.',
                     'title': 'Special G/L Indicators & Automatic Payment Program (F110)'},
                 {   'company_context': {   'cleared_amount': '€24,000',
                                            'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'run_id': '20260925-NM01'},
                     'content_md': '### F110 Execution Flow\n'
                                   '1. **Parameters Entered**: Company Code NM01, Payment Method T (Bank Transfer).\n'
                                   '2. **Proposal Created**: Invoice #5105600100 for €24,000 selected. Zero '
                                   'exceptions.\n'
                                   '3. **Payment Run**: Vendor AP (Account 211000) debited for €24,000; Bank Outgoing '
                                   'Clearing (Account 113100) credited for €24,000. Open item status changes from red '
                                   'to green (cleared).',
                     'scenario': 'Treasury runs F110 for Company Code NM01. Supplier VEND-101 has an open invoice of '
                                 '€24,000 due for net payment.',
                     'step_id': 'd36_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing AP Operations: Payment Run 20260925-NM01'},
                 {   'component_type': 'ScenarioDecision',
                     'instruction': 'Review the payment proposal exception list where an invoice failed with Error 006 '
                                    "'No valid bank details'. Choose the correct resolution.",
                     'options': [   {   'explanation': "Correct! Maintaining the vendor's bank master allows "
                                                       'electronic payment file generation.',
                                        'id': 'opt_d36_fix',
                                        'is_correct': True,
                                        'text': 'Maintain the verified IBAN and SWIFT code in the Business Partner '
                                                'record under Company Code NM01, then recreate the F110 proposal.'},
                                    {   'explanation': 'Severe audit violation.',
                                        'id': 'opt_d36_cash',
                                        'is_correct': False,
                                        'text': "Send cash by postal mail to the vendor's office."},
                                    {   'explanation': 'Payment program will fail to generate DMEE file.',
                                        'id': 'opt_d36_ignore',
                                        'is_correct': False,
                                        'text': 'Ignore the error and run payment anyway.'}],
                     'step_id': 'd36_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'F110 exception handling requires maintaining master data integrity before '
                                 're-executing proposals.',
                     'title': '[SIMULATION MODEL] Accounts Payable & F110 Exception Drill'},
                 {   'instruction': 'Select the correct SAP accounting transaction.',
                     'options': [   {   'explanation': "Correct! Special G/L Indicator 'A' isolates advance payments "
                                                       'on the balance sheet.',
                                        'id': 'opt_d36_spgl',
                                        'is_correct': True,
                                        'text': 'Post vendor down payment request/payment using Special G/L Indicator '
                                                "'A', posting to alternative reconciliation account 133000 (Advances "
                                                'to Suppliers) rather than standard AP liability.'},
                                    {   'explanation': 'Incorrect. Falsely suggests goods have been received and '
                                                       'distorts liability reporting.',
                                        'id': 'opt_d36_std',
                                        'is_correct': False,
                                        'text': 'Post as a standard vendor invoice without special indicators.'},
                                    {   'explanation': 'Severe internal accounting violation.',
                                        'id': 'opt_d36_cancel',
                                        'is_correct': False,
                                        'text': 'Cancel the purchase order and pay cash without a documented '
                                                'invoice.'}],
                     'scenario': 'Nova agrees to pay a 30% advance deposit to vendor VEND-101 before specialized '
                                 'machinery fabrication begins. How must this deposit be recorded?',
                     'step_id': 'd36_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Special G/L Indicator Accounting Challenge'},
                 {   'questions': [   {   'concept_slug': 'ap-ar-subledger-operations',
                                          'explanation': 'Blocking direct postings ensures subledgers and general '
                                                         'ledger stay in 100% synchronized harmony.',
                                          'id': 'd36_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'To enforce strict data integrity and prevent '
                                                                     'reconciliation divergence between the subledger '
                                                                     'and general ledger.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Because reconciliation accounts have zero '
                                                                     'balance at all times.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Because reconciliation accounts can only be used '
                                                                     'by external auditors.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Because SAP S/4HANA no longer uses '
                                                                     'reconciliation accounts.'}],
                                          'prompt': 'Why are manual direct journal entries to G/L reconciliation '
                                                    'accounts blocked in SAP S/4HANA?',
                                          'question_id': 'd36_q1'},
                                      {   'concept_slug': 'special-gl-indicators',
                                          'explanation': 'Special G/L indicators route transactions to alternate '
                                                         'reconciliation accounts for down payments and guarantees.',
                                          'id': 'd36_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'It redirects the line item to an alternate '
                                                                     'reconciliation account configured in the '
                                                                     'system.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': "It permanently deletes the vendor's credit "
                                                                     'limit.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'It waives all future taxes on the purchase.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'It forces immediate cash payment without invoice '
                                                                     'receipt.'}],
                                          'prompt': "What is the function of a Special G/L Indicator (such as 'A') in "
                                                    'Accounts Payable transactions?',
                                          'question_id': 'd36_q2'}],
                     'step_id': 'd36_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 36 Mastery Assessment: Accounts Payable'},
                 {   'step_id': 'd36_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Mastered vendor subledger and reconciliation account mechanics.\n'
                                   '- Configured Special G/L indicators for advance down payments.\n'
                                   '- Executed F110 automated payment runs and resolved proposal exception items.',
                     'title': 'Mastery Verification: Accounts Payable Architecture'},
                 {   'recommended_mission': {   'description': 'Investigate payment proposal exceptions for blocked '
                                                               'suppliers before bank clearing execution.',
                                                'slug': 'nova-f110-payment-exception-run',
                                                'title': 'Treasury Payment Run (F110) Exception Handling'},
                     'step_id': 'd36_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered Accounts Payable subledger management and payment automation. '
                                   'Next, you will study Accounts Receivable.',
                     'title': 'Day 36 Complete: Accounts Payable Mastered'}],
    'subtitle': 'Vendor subledger management, line item display (FBL1N), Special G/L indicators, and Automatic Payment '
                'Program (F110)',
    'title': 'Finance: Accounts Payable'},
    37: {   'atomic_concepts': ['o2c-customer-incoming-payment', 'dunning-procedures'],
    'day_number': 37,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-o2c-billing-fi-reconciliation',
    'slug': 'finance-accounts-receivable',
    'steps': [   {   'content_md': '### Cash Collection: The Culmination of O2C\n'
                                   'A sale is never truly successful until cash is in the bank. When customer '
                                   '`CUST-501` remits payment for Invoice #900055, Accounts Receivable processes the '
                                   'receipt using **Incoming Payments (transaction F-28 / Fiori app Post Incoming '
                                   'Payments)**.\n'
                                   '\n'
                                   'Incoming payment processing achieves:\n'
                                   '1. **Bank Account Debit**: Records the cash inflow on the company bank balance '
                                   'sheet.\n'
                                   '2. **Customer AR Credit**: Clears the open customer receivable item in subledger '
                                   'accounting.\n'
                                   '3. **Audit Clearing**: Generates clearing document reference `AUGBL` linking the '
                                   'invoice to the payment in `ACDOCA`.',
                     'key_terms': [   {   'definition': 'Financial accounting transaction clearing customer open '
                                                        'receivables against bank deposits.',
                                          'term': 'Incoming Payment (F-28)'},
                                      {   'definition': 'Unique document number in ACDOCA marking open items as '
                                                        'settled.',
                                          'term': 'Clearing Document (AUGBL)'},
                                      {   'definition': 'Automated multi-tiered reminder and legal notice process for '
                                                        'overdue receivables.',
                                          'term': 'Dunning'}],
                     'step_id': 'd35_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'F-28 debits bank cash and credits customer AR, clearing open items in table ACDOCA.',
                     'title': 'Closing the Cash Loop: Customer Incoming Payment (F-28)'},
                 {   'content_md': '### Automated Collections with Dunning\n'
                                   'If a customer fails to pay within agreed payment terms (e.g. Net 30), S/4HANA '
                                   'automatically triggers the **Dunning Program (transaction F150)**:\n'
                                   '- **Dunning Area / Procedure**: Configured in customer Business Partner company '
                                   'code data.\n'
                                   '- **Dunning Levels**: Graduated reminder escalation:\n'
                                   '  - **Level 1 (Gentle Reminder)**: Friendly notification that invoice #900055 is 5 '
                                   'days overdue.\n'
                                   '  - **Level 2 (Formal Notice + Fees)**: Formal demand for payment; dunning fees '
                                   'and interest applied.\n'
                                   '  - **Level 3 (Legal Warning)**: Executive escalation and threat of credit limit '
                                   'revocation or legal collections.\n'
                                   '  - **Level 4 (Collections / Legal Action)**: Immediate delivery block across all '
                                   'sales areas.',
                     'key_terms': [   {   'definition': 'Escalation severity tier (1 to 4) tracking how long an '
                                                        'invoice remains past due.',
                                          'term': 'Dunning Level'},
                                      {   'definition': 'Automated Dunning Program generating mass customer overdue '
                                                        'letters and interest fees.',
                                          'term': 'F150'}],
                     'step_id': 'd35_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'F150 automates overdue invoice collection through graduated dunning notice levels.',
                     'title': 'Dunning Procedures (Transaction F150)'},
                 {   'company_context': {   'amount_cleared': 49980.0,
                                            'company_code': 'NM01',
                                            'customer': 'CUST-501',
                                            'payment_doc': '100021',
                                            'remaining_ar': 0.0},
                     'content_md': '### Cash Receipt Reconciliation in Heidelberg\n'
                                   'Bank statement feeds show wire transfer €49,980.00 from Nordics Industrial AB:\n'
                                   '- Reference: Invoice `#900055`\n'
                                   '- Cashier executes F-28:\n'
                                   '  - Debit Bank Account `113100`: €49,980.00\n'
                                   '  - Credit Customer AR `CUST-501` (`121000`): €49,980.00\n'
                                   '- Clearing Document `#100021` posted in `ACDOCA`.\n'
                                   '- Customer open item status transitions to **Cleared (Green Circle)**.\n'
                                   '- Customer credit exposure in FSCM decreases by €49,980.00, restoring available '
                                   'credit limit!',
                     'step_id': 'd35_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: Incoming Wire from CUST-501'},
                 {   'component_type': 'O2CFlow',
                     'instruction': 'Select Stage 6 (Incoming Payment & Clearing) to verify how cash receipt completes '
                                    'the commercial lifecycle and restores credit capacity.',
                     'step_id': 'd35_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'title': 'O2C Flow: Incoming Payment & Clearing'},
                 {   'options': [   {   'explanation': 'Correct! Creating an FSCM dispute case documents the '
                                                       "customer's claim while capitalizing the €48,980 cash received.",
                                        'id': 'opt_partial_dispute',
                                        'is_correct': True,
                                        'label': 'Post a Partial Payment or Residual Item for €48,980 and create an '
                                                 'FSCM Dispute Case for the €1,000 variance so logistics can '
                                                 'investigate the damaged crate claim.'},
                                    {   'explanation': 'Harmful business practice damaging enterprise liquidity.',
                                        'id': 'opt_reject_wire',
                                        'is_correct': False,
                                        'label': 'Refuse the €48,980 and send the entire wire transfer back to the '
                                                 'customer.'},
                                    {   'explanation': 'Fraudulent accounting practice.',
                                        'id': 'opt_write_off_quiet',
                                        'is_correct': False,
                                        'label': 'Write off the €1,000 directly to executive entertainment expenses.'}],
                     'scenario_md': 'Customer CUST-501 wires €48,980 instead of the full €49,980, deducting €1,000 '
                                    'claiming freight damages on one wooden crate. The invoice cannot be cleared with '
                                    'a clean zero balance.\n'
                                    '\n'
                                    'How should the AR accountant record this in S/4HANA?',
                     'step_id': 'd35_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Short Payment Dispute Dilemma'},
                 {   'questions': [   {   'concept_slug': 'o2c-customer-incoming-payment',
                                          'id': 'd35_q1',
                                          'options': [   {   'explanation': 'Payment clears the debt and frees up '
                                                                            'credit capacity for future orders.',
                                                             'id': 'q1_a',
                                                             'is_correct': True,
                                                             'label': 'It clears the open accounts receivable item in '
                                                                      "ACDOCA and immediately reduces the customer's "
                                                                      'credit exposure, restoring their available '
                                                                      'credit limit.'},
                                                         {   'explanation': 'Nonsense distractor.',
                                                             'id': 'q1_b',
                                                             'is_correct': False,
                                                             'label': "It deletes the customer's phone number."},
                                                         {   'explanation': 'Absurd distractor.',
                                                             'id': 'q1_c',
                                                             'is_correct': False,
                                                             'label': 'It locks the sales organization from accepting '
                                                                      'orders for 30 days.'}],
                                          'points': 10,
                                          'question': 'What is the primary effect of posting an incoming customer '
                                                      "payment in transaction F-28 on the customer's FSCM credit "
                                                      'exposure?',
                                          'question_id': 'd35_q1'},
                                      {   'concept_slug': 'dunning-procedures',
                                          'id': 'd35_q2',
                                          'options': [   {   'explanation': 'F150 is the standard automated dunning '
                                                                            'program in SAP ERP / S/4HANA.',
                                                             'id': 'q2_a',
                                                             'is_correct': True,
                                                             'label': 'F150 (Dunning Program)'},
                                                         {   'explanation': 'VL01N is for creating outbound '
                                                                            'deliveries.',
                                                             'id': 'q2_b',
                                                             'is_correct': False,
                                                             'label': 'VL01N (Outbound Delivery)'},
                                                         {   'explanation': 'MIGO is for inventory goods movements.',
                                                             'id': 'q2_c',
                                                             'is_correct': False,
                                                             'label': 'MIGO (Goods Movement)'}],
                                          'points': 10,
                                          'question': 'Which SAP transaction code or Fiori app is used to execute '
                                                      'automated mass customer dunning runs for overdue accounts '
                                                      'receivable?',
                                          'question_id': 'd35_q2'}],
                     'step_id': 'd35_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 35 Assessment: Payments & Dunning'},
                 {   'concept_slug': 'o2c-customer-incoming-payment',
                     'evidence_rule': 'Validates proficiency in customer open item clearing, cash journal entries in '
                                      'ACDOCA, dispute case handling, and automated dunning runs.',
                     'step_id': 'd35_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': 'Demonstrated mastery in S/4HANA Cash Collection and Accounts Receivable clearing.',
                     'title': 'Skill Evidence: Incoming Payments & Collections'},
                 {   'recommended_mission': {   'description': 'Reconcile customer incoming payments and resolve '
                                                               'payment deductions.',
                                                'slug': 'nova-o2c-billing-fi-reconciliation',
                                                'title': 'O2C Billing & Financial Accounting Reconciliation'},
                     'step_id': 'd35_s8_completion',
                     'step_type': 'completion',
                     'summary_md': '### Core Takeaways\n'
                                   '- Incoming payments (F-28) close the commercial loop by debiting bank cash and '
                                   'clearing customer AR.\n'
                                   '- Dunning programs (F150) automate collections for overdue customer accounts.\n'
                                   '- Dispute cases protect working capital while investigating short-payment '
                                   'deductions.\n'
                                   '\n'
                                   'Next: **Day 36 — Returns & Credit Memos** handles reverse logistics and billing '
                                   'adjustments!',
                     'title': 'Day 35 Complete: Cash Collected & Cleared'}],
    'subtitle': 'Customer subledger management, incoming payments (F-28), bank clearing, and automated dunning runs '
                '(F150)',
    'title': 'Finance: Accounts Receivable'},
    38: {   'atomic_concepts': ['period-end-closing', 'foreign-currency-valuation', 'asset-depreciation-afab'],
    'day_number': 38,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-gl-period-end-closing',
    'slug': 'finance-financial-close',
    'steps': [   {   'content_md': '### The Role of Movement Types in S/4HANA\n'
                                   'In SAP S/4HANA, every change in inventory quantity, location, or stock '
                                   'classification is governed by a 3-digit **Movement Type**.\n'
                                   '\n'
                                   'Core Movement Types:\n'
                                   '- **101**: Goods Receipt against Purchase Order or Production Order (Capitalizes '
                                   'inventory).\n'
                                   '- **102**: Reversal of Goods Receipt.\n'
                                   '- **122**: Return Delivery to Vendor (Reverses GR and credits inventory).\n'
                                   '- **261**: Goods Issue for Production Order (Records component consumption against '
                                   'the order).\n'
                                   '- **311**: Storage Location to Storage Location transfer within the same plant '
                                   '(Pure logistics, zero G/L posting).\n'
                                   '- **301**: Plant-to-Plant stock transfer (Can trigger cross-company or cross-plant '
                                   'valuation postings).\n'
                                   '- **551**: Goods Issue for Scrap (Debits Scrap Expense 590000, credits Inventory '
                                   'Asset 131000).\n'
                                   '- **601**: Post Goods Issue for Outbound Delivery (Debits COGS 500000, credits '
                                   'Inventory 132000).\n'
                                   '\n'
                                   '### High-Speed MATDOC Architecture\n'
                                   'In legacy ECC, goods movements generated headers in `MKPF` and line items in '
                                   '`MSEG`, while requiring locking on hybrid aggregate tables (`MARC`, `MARD`, '
                                   '`MBEW`).\n'
                                   'In S/4HANA, table **`MATDOC`** stores movement records in a single columnar '
                                   'architecture, eliminating aggregate locking and enabling parallel inventory '
                                   'postings.',
                     'key_terms': [   {   'definition': 'Three-digit key determining the operational and accounting '
                                                        'behavior of inventory transactions.',
                                          'term': 'Movement Type'},
                                      {   'definition': 'Universal material document table recording all inventory '
                                                        'transactions in S/4HANA.',
                                          'term': 'MATDOC'}],
                     'step_id': 'd39_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Movement types enforce strict rules on whether stock changes trigger accounting '
                                 'entries in ACDOCA.',
                     'title': 'Enterprise Inventory Movement Types & MATDOC'},
                 {   'content_md': '### Physical Inventory Lifecycle\n'
                                   'Enterprise governance mandates periodic cycle counts to verify physical stock '
                                   'against book records:\n'
                                   '1. **Create Physical Inventory Document (`MI01`)**: Blocks storage bin or '
                                   'materials from stock movements during counting.\n'
                                   '2. **Enter Count (`MI04`)**: Physical quantities recorded by warehouse staff.\n'
                                   '3. **Post Differences (`MI07`)**: Reconciles book inventory to actual count:\n'
                                   '   - **Surplus**: Credits Inventory Gain / Debits Inventory Asset.\n'
                                   '   - **Shortage / Damage**: Debits Inventory Loss/Scrap Expense (e.g. Account '
                                   '590000) / Credits Inventory Asset (e.g. Account 131000).\n'
                                   '\n'
                                   '### Stock Types in Storage Locations\n'
                                   'Materials within a storage location are categorized into distinct stock types:\n'
                                   '- **Unrestricted-Use Stock**: Available for immediate production or customer '
                                   'delivery.\n'
                                   '- **Quality Inspection Stock**: Held pending laboratory clearance.\n'
                                   '- **Blocked Stock**: Defective or quarantined inventory prohibited from use.',
                     'key_terms': [   {   'definition': 'Control document specifying materials and storage locations '
                                                        'scheduled for physical verification.',
                                          'term': 'Physical Inventory Document'},
                                      {   'definition': 'Operational classification of stock (Unrestricted, Quality '
                                                        'Inspection, Blocked).',
                                          'term': 'Stock Type'}],
                     'step_id': 'd39_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Physical inventory counting bridges physical reality with ledger valuation through '
                                 'controlled difference postings.',
                     'title': 'Physical Inventory Counting, Valuation & Differences'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'plant': 'PL01',
                                            'scrap_loss': '€1,200',
                                            'sloc': 'RAW1'},
                     'content_md': '### Incident Reconciliation Trace\n'
                                   '1. **Discrepancy**: Physical count = 190 EA; Book stock in MATDOC = 200 EA.\n'
                                   '2. **Investigation**: Warehouse manager confirms physical destruction of 10 '
                                   'sensors.\n'
                                   '3. **Scrap Posting**: Posting Movement Type 551 via MIGO:\n'
                                   '   - Debit: Scrap Loss Expense (Account 590000): €1,200.00\n'
                                   '   - Credit: Raw Material Inventory (Account 131000): €1,200.00\n'
                                   '4. **Result**: Book stock in MATDOC adjusted to 190 EA; financial loss recognized '
                                   'in period P&L.',
                     'scenario': 'A cycle count in Storage Location RAW1 discovers that 10 units of Optical Sensor '
                                 'RAW-01 were crushed by a forklift during transit.',
                     'step_id': 'd39_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Inventory Audit: Forklift Sensor Damage'},
                 {   'component_type': 'InventoryMovementMapper',
                     'instruction': 'Test and map movement types (101, 102, 122, 261, 311, 301, 551, 601) to their '
                                    'respective logistical actions and accounting impacts.',
                     'step_id': 'd39_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Observe which movement types generate accounting documents versus pure logistics '
                                 'movements like 311.',
                     'title': '[SIMULATION MODEL] Inventory Movement Type Mapper'},
                 {   'instruction': 'Select the correct SAP operational answer.',
                     'options': [   {   'explanation': 'Correct! Movement 311 within the same plant has no valuation '
                                                       'impact, hence zero FI posting.',
                                        'id': 'opt_d39_311',
                                        'is_correct': True,
                                        'text': 'Post Movement Type 311 (Storage Location Transfer). It generates a '
                                                'material document in MATDOC but produces ZERO financial journal '
                                                'postings because the material remains in the same plant and company '
                                                'code.'},
                                    {   'explanation': 'Incorrect! Movement 601 is for customer delivery dispatch, not '
                                                       'internal transfers.',
                                        'id': 'opt_d39_601',
                                        'is_correct': False,
                                        'text': 'Post Movement Type 601 and recognize revenue.'},
                                    {   'explanation': 'Incorrect! Movement 551 writes off goods as scrap.',
                                        'id': 'opt_d39_551',
                                        'is_correct': False,
                                        'text': 'Post Movement Type 551 to expense the goods.'}],
                     'scenario': 'A warehouse clerk wants to move 50 sensors from Storage Location RAW1 to Storage '
                                 'Location FG01 within the same plant PL01. They ask which movement type should be '
                                 'used and what journal will post to ACDOCA.',
                     'step_id': 'd39_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Movement Type Compliance Challenge'},
                 {   'questions': [   {   'concept_slug': 'p2p-goods-receipt-migo',
                                          'explanation': 'Movement 122 is the standard return delivery to vendor, '
                                                         'reversing the initial goods receipt.',
                                          'id': 'd39_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Movement Type 122 (Return Delivery to Vendor).'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Movement Type 101 (Goods Receipt).'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Movement Type 261 (Goods Issue to Order).'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Movement Type 311 (Transfer between SLocs).'}],
                                          'prompt': 'Which movement type is used in SAP S/4HANA to return defective '
                                                    'received goods back to an external supplier from the warehouse?',
                                          'question_id': 'd39_q1'},
                                      {   'concept_slug': 'gr-ir-clearing-account',
                                          'explanation': 'Movement 551 recognizes an operational loss by debiting '
                                                         'scrap expense and crediting the inventory asset.',
                                          'id': 'd39_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Debit: Scrap Loss Expense / Credit: Inventory '
                                                                     'Asset.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Debit: Accounts Receivable / Credit: Sales '
                                                                     'Revenue.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Debit: GR/IR Interim Clearing / Credit: Accounts '
                                                                     'Payable.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Debit: Customer Cash / Credit: Bank Clearing.'}],
                                          'prompt': 'When posting Movement Type 551 (Goods Issue for Scrap), what '
                                                    'financial accounting entry is generated in ACDOCA?',
                                          'question_id': 'd39_q2'}],
                     'step_id': 'd39_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 39 Mastery Assessment: Inventory Management'},
                 {   'step_id': 'd39_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Differentiated standard movement types (101, 102, 122, 261, 311, 301, 551, '
                                   '601).\n'
                                   '- Traced MATDOC single-table architecture and elimination of aggregate inventory '
                                   'locks.\n'
                                   '- Executed physical inventory counting and difference write-offs.',
                     'title': 'Mastery Verification: Inventory Movements & Valuation'},
                 {   'recommended_mission': {   'description': 'Execute financial period closing operations and '
                                                               'balance sheet reconciliation.',
                                                'slug': 'nova-gl-period-end-closing',
                                                'title': 'Financial Period-End Closing & Variance Recovery'},
                     'step_id': 'd39_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered inventory movement types and physical inventory controls. Next, '
                                   'you will explore Manufacturing Fundamentals.',
                     'title': 'Day 39 Complete: Inventory Management Mastered'}],
    'subtitle': 'Period-end financial close sequence: depreciation (AFAB), foreign currency valuation (FAGL_FCV), and '
                'period locks (OB52)',
    'title': 'Finance: Financial Close'},
    39: {   'atomic_concepts': ['p2p-goods-receipt-migo', 'gr-ir-clearing-account'],
    'day_number': 39,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-inventory-discrepancy-audit',
    'slug': 'inventory-management',
    'steps': [   {   'content_md': '### The Role of Movement Types in S/4HANA\n'
                                   'In SAP S/4HANA, every change in inventory quantity, location, or stock '
                                   'classification is governed by a 3-digit **Movement Type**.\n'
                                   '\n'
                                   'Core Movement Types:\n'
                                   '- **101**: Goods Receipt against Purchase Order or Production Order (Capitalizes '
                                   'inventory).\n'
                                   '- **102**: Reversal of Goods Receipt.\n'
                                   '- **122**: Return Delivery to Vendor (Reverses GR and credits inventory).\n'
                                   '- **261**: Goods Issue for Production Order (Records component consumption against '
                                   'the order).\n'
                                   '- **311**: Storage Location to Storage Location transfer within the same plant '
                                   '(Pure logistics, zero G/L posting).\n'
                                   '- **301**: Plant-to-Plant stock transfer (Can trigger cross-company or cross-plant '
                                   'valuation postings).\n'
                                   '- **551**: Goods Issue for Scrap (Debits Scrap Expense 590000, credits Inventory '
                                   'Asset 131000).\n'
                                   '- **601**: Post Goods Issue for Outbound Delivery (Debits COGS 500000, credits '
                                   'Inventory 132000).\n'
                                   '\n'
                                   '### High-Speed MATDOC Architecture\n'
                                   'In legacy ECC, goods movements generated headers in `MKPF` and line items in '
                                   '`MSEG`, while requiring locking on hybrid aggregate tables (`MARC`, `MARD`, '
                                   '`MBEW`).\n'
                                   'In S/4HANA, table **`MATDOC`** stores movement records in a single columnar '
                                   'architecture, eliminating aggregate locking and enabling parallel inventory '
                                   'postings.',
                     'key_terms': [   {   'definition': 'Three-digit key determining the operational and accounting '
                                                        'behavior of inventory transactions.',
                                          'term': 'Movement Type'},
                                      {   'definition': 'Universal material document table recording all inventory '
                                                        'transactions in S/4HANA.',
                                          'term': 'MATDOC'}],
                     'step_id': 'd39_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Movement types enforce strict rules on whether stock changes trigger accounting '
                                 'entries in ACDOCA.',
                     'title': 'Enterprise Inventory Movement Types & MATDOC'},
                 {   'content_md': '### Physical Inventory Lifecycle\n'
                                   'Enterprise governance mandates periodic cycle counts to verify physical stock '
                                   'against book records:\n'
                                   '1. **Create Physical Inventory Document (`MI01`)**: Blocks storage bin or '
                                   'materials from stock movements during counting.\n'
                                   '2. **Enter Count (`MI04`)**: Physical quantities recorded by warehouse staff.\n'
                                   '3. **Post Differences (`MI07`)**: Reconciles book inventory to actual count:\n'
                                   '   - **Surplus**: Credits Inventory Gain / Debits Inventory Asset.\n'
                                   '   - **Shortage / Damage**: Debits Inventory Loss/Scrap Expense (e.g. Account '
                                   '590000) / Credits Inventory Asset (e.g. Account 131000).\n'
                                   '\n'
                                   '### Stock Types in Storage Locations\n'
                                   'Materials within a storage location are categorized into distinct stock types:\n'
                                   '- **Unrestricted-Use Stock**: Available for immediate production or customer '
                                   'delivery.\n'
                                   '- **Quality Inspection Stock**: Held pending laboratory clearance.\n'
                                   '- **Blocked Stock**: Defective or quarantined inventory prohibited from use.',
                     'key_terms': [   {   'definition': 'Control document specifying materials and storage locations '
                                                        'scheduled for physical verification.',
                                          'term': 'Physical Inventory Document'},
                                      {   'definition': 'Operational classification of stock (Unrestricted, Quality '
                                                        'Inspection, Blocked).',
                                          'term': 'Stock Type'}],
                     'step_id': 'd39_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Physical inventory counting bridges physical reality with ledger valuation through '
                                 'controlled difference postings.',
                     'title': 'Physical Inventory Counting, Valuation & Differences'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'plant': 'PL01',
                                            'scrap_loss': '€1,200',
                                            'sloc': 'RAW1'},
                     'content_md': '### Incident Reconciliation Trace\n'
                                   '1. **Discrepancy**: Physical count = 190 EA; Book stock in MATDOC = 200 EA.\n'
                                   '2. **Investigation**: Warehouse manager confirms physical destruction of 10 '
                                   'sensors.\n'
                                   '3. **Scrap Posting**: Posting Movement Type 551 via MIGO:\n'
                                   '   - Debit: Scrap Loss Expense (Account 590000): €1,200.00\n'
                                   '   - Credit: Raw Material Inventory (Account 131000): €1,200.00\n'
                                   '4. **Result**: Book stock in MATDOC adjusted to 190 EA; financial loss recognized '
                                   'in period P&L.',
                     'scenario': 'A cycle count in Storage Location RAW1 discovers that 10 units of Optical Sensor '
                                 'RAW-01 were crushed by a forklift during transit.',
                     'step_id': 'd39_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Inventory Audit: Forklift Sensor Damage'},
                 {   'component_type': 'InventoryMovementMapper',
                     'instruction': 'Test and map movement types (101, 102, 122, 261, 311, 301, 551, 601) to their '
                                    'respective logistical actions and accounting impacts.',
                     'step_id': 'd39_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Observe which movement types generate accounting documents versus pure logistics '
                                 'movements like 311.',
                     'title': '[SIMULATION MODEL] Inventory Movement Type Mapper'},
                 {   'instruction': 'Select the correct SAP operational answer.',
                     'options': [   {   'explanation': 'Correct! Movement 311 within the same plant has no valuation '
                                                       'impact, hence zero FI posting.',
                                        'id': 'opt_d39_311',
                                        'is_correct': True,
                                        'text': 'Post Movement Type 311 (Storage Location Transfer). It generates a '
                                                'material document in MATDOC but produces ZERO financial journal '
                                                'postings because the material remains in the same plant and company '
                                                'code.'},
                                    {   'explanation': 'Incorrect! Movement 601 is for customer delivery dispatch, not '
                                                       'internal transfers.',
                                        'id': 'opt_d39_601',
                                        'is_correct': False,
                                        'text': 'Post Movement Type 601 and recognize revenue.'},
                                    {   'explanation': 'Incorrect! Movement 551 writes off goods as scrap.',
                                        'id': 'opt_d39_551',
                                        'is_correct': False,
                                        'text': 'Post Movement Type 551 to expense the goods.'}],
                     'scenario': 'A warehouse clerk wants to move 50 sensors from Storage Location RAW1 to Storage '
                                 'Location FG01 within the same plant PL01. They ask which movement type should be '
                                 'used and what journal will post to ACDOCA.',
                     'step_id': 'd39_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Movement Type Compliance Challenge'},
                 {   'questions': [   {   'concept_slug': 'p2p-goods-receipt-migo',
                                          'explanation': 'Movement 122 is the standard return delivery to vendor, '
                                                         'reversing the initial goods receipt.',
                                          'id': 'd39_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Movement Type 122 (Return Delivery to Vendor).'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Movement Type 101 (Goods Receipt).'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Movement Type 261 (Goods Issue to Order).'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Movement Type 311 (Transfer between SLocs).'}],
                                          'prompt': 'Which movement type is used in SAP S/4HANA to return defective '
                                                    'received goods back to an external supplier from the warehouse?',
                                          'question_id': 'd39_q1'},
                                      {   'concept_slug': 'gr-ir-clearing-account',
                                          'explanation': 'Movement 551 recognizes an operational loss by debiting '
                                                         'scrap expense and crediting the inventory asset.',
                                          'id': 'd39_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Debit: Scrap Loss Expense / Credit: Inventory '
                                                                     'Asset.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Debit: Accounts Receivable / Credit: Sales '
                                                                     'Revenue.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Debit: GR/IR Interim Clearing / Credit: Accounts '
                                                                     'Payable.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Debit: Customer Cash / Credit: Bank Clearing.'}],
                                          'prompt': 'When posting Movement Type 551 (Goods Issue for Scrap), what '
                                                    'financial accounting entry is generated in ACDOCA?',
                                          'question_id': 'd39_q2'}],
                     'step_id': 'd39_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 39 Mastery Assessment: Inventory Management'},
                 {   'step_id': 'd39_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Differentiated standard movement types (101, 102, 122, 261, 311, 301, 551, '
                                   '601).\n'
                                   '- Traced MATDOC single-table architecture and elimination of aggregate inventory '
                                   'locks.\n'
                                   '- Executed physical inventory counting and difference write-offs.',
                     'title': 'Mastery Verification: Inventory Movements & Valuation'},
                 {   'recommended_mission': {   'description': 'Conduct a physical inventory audit in storage location '
                                                               'RAW1 and resolve discrepancies via MATDOC adjustments.',
                                                'slug': 'nova-inventory-discrepancy-audit',
                                                'title': 'Inventory Valuation & Physical Discrepancy Audit'},
                     'step_id': 'd39_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered inventory movement types and physical inventory controls. Next, '
                                   'you will explore Manufacturing Fundamentals.',
                     'title': 'Day 39 Complete: Inventory Management Mastered'}],
    'subtitle': 'Warehouse movement types (101, 102, 122, 261, 311, 301, 551), single-table MATDOC architecture, and '
                'physical inventory',
    'title': 'Inventory Management'},
    40: {   'atomic_concepts': ['mfg-bom-master', 'mfg-work-centers-routing'],
    'day_number': 40,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-mfg-shopfloor-dispatch-incident',
    'slug': 'manufacturing-fundamentals',
    'steps': [   {   'content_md': '### Converting Raw Materials into Finished Goods\n'
                                   'Before an enterprise can execute manufacturing on the shopfloor, Production '
                                   'Planning (PP) requires three synchronized master data structures:\n'
                                   '\n'
                                   '1. **Bill of Materials (BOM / transaction CS01)**: The structural recipe of '
                                   'parts.\n'
                                   '   - For `DXTR-1000`: 2x `RAW-01` (Optical Sensor Arrays), 1x Aluminum Chassis, 1x '
                                   'Power Supply Module, 4x Servo Motors.\n'
                                   '   - Item Category: `L` (Stock Item), `N` (Non-stock item).\n'
                                   '2. **Work Center (transaction CR01)**: The physical manufacturing resource where '
                                   'operations occur (machines, assembly stations, technician teams).\n'
                                   '   - Linked to a Controlling **Cost Center** (e.g. `CC-PROD-01`).\n'
                                   '   - Defines standard available capacity (e.g. 16 hours/day, 2 shifts).\n'
                                   '3. **Routing (transaction CA01)**: The chronological sequence of operational '
                                   'steps.\n'
                                   '   - Op 0010: Surface-mount electronics assembly (Work Center `WC-PCB-01`).\n'
                                   '   - Op 0020: Optical alignment & calibration (Work Center `WC-OPTIC-01`).\n'
                                   '   - Op 0030: Final robotic functional testing (Work Center `WC-TEST-01`).',
                     'key_terms': [   {   'definition': 'Hierarchical product structure listing all components '
                                                        'required to manufacture an assembly.',
                                          'term': 'Bill of Materials (BOM)'},
                                      {   'definition': 'Shopfloor machine or labor station with defined capacity and '
                                                        'cost center activity rates.',
                                          'term': 'Work Center'},
                                      {   'definition': 'Step-by-step sequence of manufacturing operations, standard '
                                                        'run times, and work centers.',
                                          'term': 'Routing'}],
                     'step_id': 'd40_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'BOM defines what is built; Work Center defines where it is built; Routing defines '
                                 'how it is built.',
                     'title': 'The Trinity of Manufacturing Master Data'},
                 {   'content_md': '### How Manufacturing Data Calculates Product Cost\n'
                                   'How does S/4HANA know that a `DXTR-1000` controller costs €850 to manufacture?\n'
                                   'Through the automated link between **Routing standard run times** and '
                                   '**Controlling Activity Types (KP26)**:\n'
                                   '\n'
                                   '$$\\text{Standard Manufacturing Cost} = \\sum \\text{BOM Raw Materials} + \\sum '
                                   '(\\text{Routing Activity Hours} \\times \\text{Work Center Activity Rate})$$\n'
                                   '\n'
                                   'For Work Center `WC-ROBOT-01`:\n'
                                   '- Machine Activity Rate: €45.00 / Machine Hour\n'
                                   '- Direct Labor Activity Rate: €65.00 / Labor Hour\n'
                                   '- Routing Op 0010 specifies: 2.0 Machine Hours (€90.00) + 1.5 Labor Hours '
                                   '(€97.50).\n'
                                   '\n'
                                   'When product costing (**CK11N / CK24**) runs, the system rolls up component costs '
                                   "and operational labor into the material's **Standard Price (MBEW-STPRS)** on the "
                                   'balance sheet!',
                     'key_terms': [   {   'definition': 'Unit of operational work (e.g. Machine Hours, Labor Hours) '
                                                        'with configured standard hourly rates.',
                                          'term': 'Activity Type'},
                                      {   'definition': 'Automatic standard cost calculation rolling up BOM materials '
                                                        'and routing activities.',
                                          'term': 'Cost Rollup (CK11N)'}],
                     'step_id': 'd40_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Routings specify standard operation times; work center activity rates roll up into '
                                 'balance sheet standard product costs.',
                     'title': 'Costing Integration: Activity Types & Standard Cost Calculation'},
                 {   'company_context': {   'bom_components': 3,
                                            'company_code': 'NM01',
                                            'cost_center': 'CC-PROD-01',
                                            'finished_good': 'DXTR-1000',
                                            'primary_work_center': 'WC-ROBOT-01',
                                            'standard_cost': 850.0},
                     'content_md': '### Engineering Blueprint at Plant PL01\n'
                                   '- **Product**: `DXTR-1000` Industrial Robotics Controller\n'
                                   '- **BOM Structure (CS01)**:\n'
                                   '  - Line 0010: 2 EA `RAW-01` (Optical Sensor Arrays)\n'
                                   '  - Line 0020: 1 EA `PCB-MAIN-01` (Main Logic Motherboard)\n'
                                   '  - Line 0030: 4 EA `SERVO-500` (High-torque Actuators)\n'
                                   '- **Work Center (CR01)**: `WC-ROBOT-01`\n'
                                   '  - Cost Center: `CC-PROD-01` (Plant Assembly)\n'
                                   '  - Capacity: 80 hours/week (2 shifts x 5 days)\n'
                                   '- **Routing (CA01)**:\n'
                                   '  - Op 0010: Mechanical assembly (1.0 hr setup, 2.0 hr run)\n'
                                   '  - Op 0020: Optical calibration (0.5 hr setup, 1.5 hr run)\n'
                                   '- Standard Product Cost: €850.00 / EA.',
                     'step_id': 'd40_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: DXTR-1000 Master Data Architecture'},
                 {   'component_type': 'ProductionOrderFlow',
                     'instruction': 'Select Stage 1 (Order Creation & Scheduling) to inspect how BOM components and '
                                    'routing operations initialize production orders.',
                     'step_id': 'd40_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'title': 'Production Engineering Flow'},
                 {   'options': [   {   'explanation': 'Correct! Temporal validity dates in BOMs ensure smooth '
                                                       'component phase-in/phase-out without disrupting active orders.',
                                        'id': 'opt_ecm_validity',
                                        'is_correct': True,
                                        'label': "Use Engineering Change Management (ECM) or maintain 'Valid From' / "
                                                 "'Valid To' validity dates directly on the BOM item lines in CS02, "
                                                 'ensuring RAW-01A expires on Oct 31 and RAW-01B takes effect Nov 1.'},
                                    {   'explanation': 'Severe error breaking active October production runs.',
                                        'id': 'opt_delete_mara',
                                        'is_correct': False,
                                        'label': 'Delete material RAW-01A from the database immediately.'},
                                    {   'explanation': 'Manual sticky notes fail automated MRP and order reservation '
                                                       'systems.',
                                        'id': 'opt_manual_note',
                                        'is_correct': False,
                                        'label': 'Write a sticky note and stick it onto the shopfloor assembly line.'}],
                     'scenario_md': "Nova's engineering team redesigns the DXTR-1000 controller to replace defective "
                                    'optical sensor variant RAW-01A with new high-resolution sensor RAW-01B starting '
                                    'November 1st. Existing production orders scheduled for October must continue '
                                    'using RAW-01A.\n'
                                    '\n'
                                    'How should this engineering change be configured in SAP S/4HANA?',
                     'step_id': 'd40_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'BOM Component Obsolescence Challenge'},
                 {   'questions': [   {   'concept_slug': 'mfg-work-centers-routing',
                                          'id': 'd40_q1',
                                          'options': [   {   'explanation': 'Routings define operational sequences, '
                                                                            'setup times, and run times on work '
                                                                            'centers.',
                                                             'id': 'q1_a',
                                                             'is_correct': True,
                                                             'label': 'Routing (transaction CA01 / CA02)'},
                                                         {   'explanation': 'BOMs define component materials, not '
                                                                            'operational sequences.',
                                                             'id': 'q1_b',
                                                             'is_correct': False,
                                                             'label': 'Bill of Materials (BOM)'},
                                                         {   'explanation': 'Info records are for procurement vendor '
                                                                            'pricing.',
                                                             'id': 'q1_c',
                                                             'is_correct': False,
                                                             'label': 'Purchase Info Record'}],
                                          'points': 10,
                                          'question': 'Which SAP master data object defines the step-by-step sequence '
                                                      'of operations, required work centers, and standard planned '
                                                      'times for manufacturing a product?',
                                          'question_id': 'd40_q1'},
                                      {   'concept_slug': 'mfg-bom-master',
                                          'id': 'd40_q2',
                                          'options': [   {   'explanation': 'Work centers link to cost centers and '
                                                                            'activity types, enabling internal '
                                                                            'activity allocations.',
                                                             'id': 'q2_a',
                                                             'is_correct': True,
                                                             'label': 'By linking to a Controlling Cost Center (e.g. '
                                                                      'CC-PROD-01) and assigning standard Activity '
                                                                      'Types (e.g. Machine Hours, Labor Hours) with '
                                                                      'configured hourly rates.'},
                                                         {   'explanation': 'Absurd distractor.',
                                                             'id': 'q2_b',
                                                             'is_correct': False,
                                                             'label': 'By storing the bank account number of the '
                                                                      'machine manufacturer.'},
                                                         {   'explanation': 'Completely unrelated to SD customer '
                                                                            'billing.',
                                                             'id': 'q2_c',
                                                             'is_correct': False,
                                                             'label': 'By transmitting customer sales invoices via '
                                                                      'email.'}],
                                          'points': 10,
                                          'question': 'How does a Work Center link shopfloor physical machine '
                                                      'operations to Financial Controlling (CO)?',
                                          'question_id': 'd40_q2'}],
                     'step_id': 'd40_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 40 Assessment: Production Master Data'},
                 {   'concept_slug': 'mfg-bom-master',
                     'evidence_rule': 'Validates proficiency in BOM engineering structures (CS01), Work Center '
                                      'capacity definitions (CR01), Routing operations (CA01), and standard cost '
                                      'rollup integration.',
                     'step_id': 'd40_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': 'Demonstrated mastery in S/4HANA Manufacturing Master Data and standard product '
                                   'costing architecture.',
                     'title': 'Skill Evidence: Manufacturing Master Data'},
                 {   'recommended_mission': {   'description': 'Resolve a critical work center bottleneck and capacity '
                                                               'overload on the Heidelberg assembly line.',
                                                'slug': 'nova-mfg-shopfloor-dispatch-incident',
                                                'title': 'Manufacturing Shopfloor Dispatch & Resource Bottleneck'},
                     'step_id': 'd40_s8_completion',
                     'step_type': 'completion',
                     'summary_md': '### Core Takeaways\n'
                                   '- The manufacturing trinity (BOM, Work Center, Routing) defines product structure, '
                                   'physical resources, and assembly steps.\n'
                                   '- Work centers link operational activities to Controlling cost centers and '
                                   'standard activity rates.\n'
                                   '- Standard costing (CK11N) rolls up raw material costs and activity rates into '
                                   'balance sheet standard inventory values.\n'
                                   '\n'
                                   'Next: **Day 41 — Production Order Execution & Capacity Leveling**!',
                     'title': 'Day 40 Complete: Manufacturing Master Data Mastered'}],
    'subtitle': 'Bills of Material (CS01), Work Centers (CR01), standard activity rates, and Routings (CA01)',
    'title': 'Manufacturing Fundamentals'},
    41: {   'atomic_concepts': [   'production-order-lifecycle',
                           'capacity-requirements-planning',
                           'production-order-confirmation',
                           'component-backflushing'],
    'day_number': 41,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-mfg-shopfloor-dispatch-incident',
    'slug': 'manufacturing-production-execution',
    'steps': [   {   'content_md': '### The Shopfloor Contract: Production Order Lifecycle\n'
                                   'When MRP Live generates a Planned Order to fulfill sales demand, the production '
                                   'planner converts it into a formal **Production Order (transaction CO01 / Fiori app '
                                   'Manage Production Orders)**.\n'
                                   '\n'
                                   'The production order is both a **logistics execution document** and an **internal '
                                   'cost collector**:\n'
                                   '1. **Created (`CRTD`)**: System reads current BOM and Routing, reserves raw '
                                   'materials in table `RESB`, and calculates planned costs.\n'
                                   '2. **Capacity Availability Check**: Checks if Work Centers have sufficient free '
                                   'hours to complete the order without bottlenecks.\n'
                                   '3. **Released (`REL`)**: Authorizes the shopfloor to begin physical assembly. '
                                   'Staging lists and traveler route sheets are printed.\n'
                                   '4. **Material Staging & Component Consumption (Movement 261)**: Raw materials are '
                                   'withdrawn from warehouse Storage Location `RAW1` and consumed on the assembly '
                                   'line:\n'
                                   '   - Decrements component inventory quantity in `MATDOC`.\n'
                                   '   - Debits the production order cost collector in `ACDOCA` (e.g. Account 510000 '
                                   'in Nova simulation model) and credits Raw Material Inventory asset (Account '
                                   '131000).',
                     'key_terms': [   {   'definition': 'Shopfloor manufacturing contract governing components, '
                                                        'operations, and cost collection.',
                                          'term': 'Production Order (CO01)'},
                                      {   'definition': 'Goods issue movement recording raw material consumption '
                                                        'against a production order.',
                                          'term': 'Movement Type 261'}],
                     'step_id': 'd41_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Order release authorizes execution; Movement 261 debits component costs to the '
                                 'production order cost collector.',
                     'title': 'Production Order Lifecycle & Component Consumption (Mov 261)'},
                 {   'content_md': '### Operation Confirmations (transaction CO11N / table AFRU)\n'
                                   'As operators execute work center routing steps, they record actual operational '
                                   'results in transaction **`CO11N`** (or Fiori app *Confirm Production Operation*):\n'
                                   '- **Yield Quantity**: Finished assemblies produced.\n'
                                   '- **Scrap Quantity**: Defective parts rejected during operation.\n'
                                   '- **Actual Activity Times**: Setup time, machine hours, and direct labor hours.\n'
                                   '\n'
                                   'When confirmations are posted, table **`AFRU`** records operation details, and the '
                                   'system performs **Activity Allocation**:\n'
                                   '- Debits Production Order with actual labor/machine costs.\n'
                                   '- Credits Cost Centers (e.g. `CC-PROD-01`) based on cost center activity rates.\n'
                                   '\n'
                                   '### Finished Goods Receipt (Movement 101)\n'
                                   'Upon completion of the final operation, the finished product (e.g. `DXTR-1000`) is '
                                   'received into warehouse Storage Location `FG01` via **Movement Type 101**:\n'
                                   '$$\\begin{aligned}\n'
                                   '\\text{Debit: } & \\text{Finished Goods Inventory Asset (Account 132000)} & '
                                   '€22,000.00 \\\\\n'
                                   '\\text{Credit: } & \\text{Production Order Output Credit (Account 520000)} & '
                                   '€22,000.00\n'
                                   '\\end{aligned}$$\n'
                                   '\n'
                                   'The order status updates to **`DLV` (Delivered)** or **`TECO` (Technically '
                                   'Completed)**, readying the order for period-end cost settlement.',
                     'key_terms': [   {   'definition': 'Shopfloor feedback recording actual labor, machine time, and '
                                                        'yield into table AFRU.',
                                          'term': 'Confirmation (CO11N)'},
                                      {   'definition': 'Receiving manufactured finished goods into warehouse '
                                                        'inventory at standard cost.',
                                          'term': 'Goods Receipt (Mov 101)'}],
                     'step_id': 'd41_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'CO11N records actual activity labor/machine times; Movement 101 receives finished '
                                 'goods into inventory and credits the order.',
                     'title': 'Operation Confirmations (CO11N) & Finished Goods Receipt (Mov 101)'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'material': 'DXTR-1000',
                                            'order_id': '100888',
                                            'plant': 'PL01'},
                     'content_md': '### Complete Shopfloor Execution Sequence\n'
                                   '1. **Order Release**: Production Order #100888 created via CO01, capacity checked, '
                                   'and released (REL).\n'
                                   '2. **Component Consumption**: 200x RAW-01 sensors issued via Movement Type 261 '
                                   'from RAW1 (Dr Order 510000 / Cr Inventory 131000: €15,000).\n'
                                   '3. **Operation Confirmation (CO11N)**: Assembly operation confirmed with 100 EA '
                                   'yield, 40 machine hours, and 20 labor hours recorded in table AFRU.\n'
                                   '4. **Finished Goods Receipt (Mov 101)**: 100x DXTR-1000 received into Storage '
                                   'Location FG01 at standard cost of €220/EA (€22,000 total: Dr Inventory 132000 / Cr '
                                   'Order Credit 520000).',
                     'scenario': 'Plant PL01 (Heidelberg) executes Production Order #100888 for 100 units of '
                                 'DXTR-1000. Components consumed via Mov 261, operations confirmed in CO11N, and '
                                 'finished units received into FG01 via Mov 101.',
                     'step_id': 'd41_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: Order #100888 Execution & Confirmation'},
                 {   'component_type': 'ProductionOrderFlow',
                     'instruction': 'Step through Order Creation, Release, Component Issue (Mov 261), Operation '
                                    'Confirmation (CO11N), and Finished Receipt (Mov 101).',
                     'step_id': 'd41_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Observe how actual costs debit the order and finished goods receipts credit the '
                                 'order at standard cost.',
                     'title': '[SIMULATION MODEL] Production Order Flow Visualizer'},
                 {   'instruction': 'Select the correct SAP operational answer.',
                     'options': [   {   'explanation': 'Correct! Operation confirmation records activity time; '
                                                       'physical inventory capitalization requires Movement 101.',
                                        'id': 'opt_d41_c1',
                                        'is_correct': True,
                                        'text': 'No, CO11N confirms labor, machine time, and operational yield '
                                                '(recorded in table AFRU). Finished inventory capitalization requires '
                                                'a separate Goods Receipt posting (Movement Type 101) into warehouse '
                                                'storage location FG01.'},
                                    {   'explanation': 'Incorrect! Warehouse receiving and delivery creation are '
                                                       'distinct subsequent steps.',
                                        'id': 'opt_d41_c2',
                                        'is_correct': False,
                                        'text': 'Yes, confirming an operation immediately places the finished goods on '
                                                'delivery trucks to the customer.'},
                                    {   'explanation': 'Incorrect! Orders remain for cost variance analysis and '
                                                       'settlement.',
                                        'id': 'opt_d41_c3',
                                        'is_correct': False,
                                        'text': 'CO11N deletes the production order once operations are finished.'}],
                     'scenario': "A junior shopfloor supervisor asks: 'If we confirm operations in CO11N, does that "
                                 'automatically receive the finished goods into warehouse inventory without any goods '
                                 "receipt posting?'",
                     'step_id': 'd41_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Operation Confirmation vs Material Issue Challenge'},
                 {   'questions': [   {   'concept_slug': 'production-order-lifecycle',
                                          'explanation': 'CO01 is used to create production orders; VA01 is for sales '
                                                         'orders; ME21N is for purchase orders; FB50 is for G/L '
                                                         'journals.',
                                          'id': 'd41_q1',
                                          'options': [   {'id': 'a', 'is_correct': True, 'text': 'CO01'},
                                                         {'id': 'b', 'is_correct': False, 'text': 'VA01'},
                                                         {'id': 'c', 'is_correct': False, 'text': 'ME21N'},
                                                         {'id': 'd', 'is_correct': False, 'text': 'FB50'}],
                                          'prompt': 'Which transaction code in SAP GUI is used to create a standard '
                                                    'discrete manufacturing Production Order?',
                                          'question_id': 'd41_q1'},
                                      {   'concept_slug': 'component-backflushing',
                                          'explanation': 'Movement 261 deducts component stock from inventory and '
                                                         'debits the production order cost collector.',
                                          'id': 'd41_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Debit: Production Order Cost Collector / Credit: '
                                                                     'Raw Material Inventory Asset.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Debit: Customer Accounts Receivable / Credit: '
                                                                     'Sales Revenue.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Debit: Bank Cash / Credit: Accounts Payable.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Debit: Price Variance / Credit: GR/IR '
                                                                     'Clearing.'}],
                                          'prompt': 'When raw materials are issued to a production order using '
                                                    'Movement Type 261, what is the financial accounting effect in '
                                                    'ACDOCA?',
                                          'question_id': 'd41_q2'},
                                      {   'concept_slug': 'production-order-confirmation',
                                          'explanation': 'Table AFRU stores order confirmation records; EKKO is for '
                                                         'POs; VBAK is for sales orders; KNA1 is for customers.',
                                          'id': 'd41_q3',
                                          'options': [   {'id': 'a', 'is_correct': True, 'text': 'AFRU'},
                                                         {'id': 'b', 'is_correct': False, 'text': 'EKKO'},
                                                         {'id': 'c', 'is_correct': False, 'text': 'VBAK'},
                                                         {'id': 'd', 'is_correct': False, 'text': 'KNA1'}],
                                          'prompt': 'In which database table does SAP record operational confirmation '
                                                    'details (yield, scrap, machine time, labor time) entered via '
                                                    'transaction CO11N?',
                                          'question_id': 'd41_q3'}],
                     'step_id': 'd41_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 41 Mastery Assessment: Production Execution'},
                 {   'step_id': 'd41_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Executed production order lifecycle from CO01 creation to release.\n'
                                   '- Verified Movement 261 component consumption against order cost collectors.\n'
                                   '- Validated CO11N confirmations in table AFRU and Movement 101 finished goods '
                                   'receipts.',
                     'title': 'Mastery Verification: Production Execution'},
                 {   'recommended_mission': {   'description': 'Resolve a critical work center bottleneck and capacity '
                                                               'overload on the Heidelberg assembly line.',
                                                'slug': 'nova-mfg-shopfloor-dispatch-incident',
                                                'title': 'Manufacturing Shopfloor Dispatch & Resource Bottleneck'},
                     'step_id': 'd41_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered production order execution, operation confirmations, and '
                                   'finished goods receipt. Next, you will study WIP, variances, and KO88 cost '
                                   'settlement.',
                     'title': 'Day 41 Complete: Production Execution Mastered'}],
    'subtitle': 'Production order lifecycle (CO01), release, component backflushing (Mov 261), confirmations (CO11N), '
                'and FG receipt (Mov 101)',
    'title': 'Production Execution'},
    42: {   'atomic_concepts': ['production-order-settlement', 'wip-variance-calculation'],
    'day_number': 42,
    'estimated_minutes': 45,
    'recommended_mission_slug': 'nova-mfg-production-variance-investigation',
    'slug': 'manufacturing-cost-settlement',
    'steps': [   {   'content_md': '### Production Orders as Cost Collectors\n'
                                   'In discrete manufacturing, a Production Order is not only a manufacturing '
                                   'schedule—it is an **internal cost collector** that accumulates debits and credits '
                                   'throughout its lifecycle:\n'
                                   '- **Actual Debits**: Incurred during production via Movement 261 (raw materials '
                                   'issued) and CO11N confirmations (direct labor and machine overhead allocated from '
                                   'cost centers).\n'
                                   '- **Standard Credits**: Posted upon finished goods receipt (Movement Type 101) '
                                   'when completed units enter warehouse stock at their standard valuation price '
                                   '(`MBEW-STPRS`).\n'
                                   '\n'
                                   '### System Status Logic: WIP vs Closed Variances\n'
                                   'At period end, the cost controller must evaluate the order balance based on order '
                                   'status:\n'
                                   '1. **Work-in-Process (WIP) (Status `REL` - Released)**: The order is still in '
                                   'progress on the shopfloor. The incurred costs represent incomplete assemblies and '
                                   'are capitalized on the balance sheet as WIP asset.\n'
                                   '2. **Manufacturing Variances (Status `TECO` - Technically Completed or `DLV` - '
                                   'Delivered)**: Production is finished. The difference between actual debits and '
                                   'standard credits represents operational variance (price, quantity, or scrap) that '
                                   'must be expensed to P&L.',
                     'key_terms': [   {   'definition': 'Unfinished production order costs capitalized as balance '
                                                        'sheet assets at period close.',
                                          'term': 'Work-in-Process (WIP)'},
                                      {   'definition': 'Difference between actual incurred costs and standard output '
                                                        'credit for completed orders.',
                                          'term': 'Manufacturing Variance'}],
                     'step_id': 'd42_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Status REL calculates WIP on the balance sheet; status TECO or DLV calculates '
                                 'variances expensed to P&L.',
                     'title': 'Production Order Costing, WIP & Variances'},
                 {   'content_md': '### Order Settlement via Transaction KO88\n'
                                   'At the close of each fiscal period, transaction **`KO88`** executes cost '
                                   'settlement for individual orders (or `CO88` for collective batch settlement):\n'
                                   '- Evaluates order balance (Debits minus Credits).\n'
                                   '- Generates an accounting document in `ACDOCA` that clears the order balance to '
                                   'zero.\n'
                                   '\n'
                                   '### Accounting Entries for Settlement:\n'
                                   '1. **Uncompleted Order (Status REL - WIP Settlement)**:\n'
                                   '   $$\\begin{aligned}\n'
                                   '   \\text{Debit: } & \\text{Work-in-Process Balance Sheet Asset (Account 134000)} '
                                   '\\\\\n'
                                   '   \\text{Credit: } & \\text{WIP Inventory Change P&L Offset (Account 521000)}\n'
                                   '   \\end{aligned}$$\n'
                                   '2. **Completed Order with Unfavorable Variance (Status TECO/DLV)**:\n'
                                   '   $$\\begin{aligned}\n'
                                   '   \\text{Debit: } & \\text{Production Price Variance Expense (Account 530000)} & '
                                   '€3,400.00 \\\\\n'
                                   '   \\text{Credit: } & \\text{Production Order Settlement Credit (Account 520000)} '
                                   '& €3,400.00\n'
                                   '   \\end{aligned}$$\n'
                                   '\n'
                                   'After settlement, the production order cost collector in ACDOCA reflects an active '
                                   'balance of **€0.00**.',
                     'key_terms': [   {   'definition': 'Controlling procedure allocating order balance to financial '
                                                        'accounting and clearing order balance to zero.',
                                          'term': 'Order Settlement (KO88)'},
                                      {   'definition': 'P&L expense account capturing differences between actual '
                                                        'manufacturing costs and standard price.',
                                          'term': 'Price Variance Account (530000)'}],
                     'step_id': 'd42_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'KO88 settlement clears the production order balance to zero and reflects true '
                                 'manufacturing variances in ACDOCA.',
                     'title': 'Order Settlement (KO88) & Universal Journal Postings'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'order_id': '100888',
                                            'variance': '€3,400 unfavorable'},
                     'content_md': '### Settlement Walkthrough\n'
                                   '1. **Status Set to TECO**: Production planner sets order status to Technically '
                                   'Completed (TECO).\n'
                                   '2. **Variance Calculation**: Variance analysis identifies €2,000 material price '
                                   'variance and €1,400 machine overtime variance.\n'
                                   '3. **Settlement Executed (KO88)**:\n'
                                   '   - Debit: Production Price Variance (530000): €3,400.00\n'
                                   '   - Credit: Production Order Settlement (520000): €3,400.00\n'
                                   '4. **Result**: Order balance becomes €0.00; variance is recognized in NM01 period '
                                   'P&L.',
                     'scenario': 'Production Order #100888 completed 100 units of DXTR-1000. Incurred actual debits = '
                                 '€25,400. Standard goods receipt credit = €22,000. Net unfavorable variance = €3,400.',
                     'step_id': 'd42_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing: Order #100888 Month-End Settlement'},
                 {   'component_type': 'CostSettlementVisualizer',
                     'instruction': 'Simulate status transitions (REL vs TECO) and execute KO88 settlement to observe '
                                    'WIP vs variance postings in ACDOCA.',
                     'step_id': 'd42_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Notice how setting TECO shifts settlement from WIP capitalization to P&L variance '
                                 'recognition.',
                     'title': '[SIMULATION MODEL] Cost Settlement Visualizer'},
                 {   'instruction': 'Identify the system status prerequisite for variance calculation.',
                     'options': [   {   'explanation': 'Correct! Orders in status REL are considered in progress and '
                                                       'calculate WIP; status TECO or DLV enables closed variance '
                                                       'settlement.',
                                        'id': 'opt_d42_teco',
                                        'is_correct': True,
                                        'text': 'The order still has status REL (Released); the system requires status '
                                                'TECO (Technically Completed) or DLV (Delivered) before it will '
                                                'calculate closed variances instead of WIP.'},
                                    {   'explanation': 'Deleting the order would destroy costing records and audit '
                                                       'trails.',
                                        'id': 'opt_d42_delete',
                                        'is_correct': False,
                                        'text': 'The cost accountant must delete the production order from the '
                                                'system.'},
                                    {   'explanation': 'Manual journal entries violate production order subledger '
                                                       'integration rules.',
                                        'id': 'opt_d42_manual_gl',
                                        'is_correct': False,
                                        'text': 'The cost accountant should post a manual journal in FB50 to override '
                                                'the order.'}],
                     'scenario': 'A cost accountant attempts to execute KO88 settlement to recognize closed '
                                 'manufacturing variances on Order #100888, but the system calculates WIP instead of '
                                 'variance. What is the reason?',
                     'step_id': 'd42_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Premature Settlement & Status Logic Challenge'},
                 {   'questions': [   {   'concept_slug': 'production-order-settlement',
                                          'explanation': 'KO88 settles order balances to G/L variance accounts and '
                                                         'clears the order cost collector to zero.',
                                          'id': 'd42_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'To transfer the balance of debits and credits '
                                                                     'from the production order cost collector to '
                                                                     'financial accounting (ACDOCA), bringing the '
                                                                     'order balance to zero.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'To print shipping labels for the warehouse.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'To recalculate customer sales tax rates.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'To release blocked purchase requisitions.'}],
                                          'prompt': 'What is the primary architectural purpose of transaction KO88 '
                                                    '(Order Settlement)?',
                                          'question_id': 'd42_q1'},
                                      {   'concept_slug': 'wip-variance-calculation',
                                          'explanation': 'System status dictates settlement logic: REL triggers WIP; '
                                                         'TECO/DLV triggers variance calculation.',
                                          'id': 'd42_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Based on the system status of the order: Status '
                                                                     'REL calculates WIP; Status TECO or DLV '
                                                                     'calculates closed variances.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Based on whether the customer has paid their '
                                                                     'bill.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Based on the plant calendar days remaining.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Based on manual spreadsheet entry.'}],
                                          'prompt': 'How does SAP S/4HANA determine whether to calculate '
                                                    'Work-in-Process (WIP) or closed manufacturing variances for an '
                                                    'order at period end?',
                                          'question_id': 'd42_q2'}],
                     'step_id': 'd42_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 42 Mastery Assessment: WIP & Cost Settlement'},
                 {   'step_id': 'd42_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Differentiated WIP calculation (status REL) from variance calculation (status '
                                   'TECO/DLV).\n'
                                   '- Executed transaction KO88 order settlement and validated Price Variance postings '
                                   'in ACDOCA.\n'
                                   '- Verified that completed production orders balance to €0.00 upon period close.',
                     'title': 'Mastery Verification: WIP & Order Settlement'},
                 {   'recommended_mission': {   'description': 'Diagnose unfavorable manufacturing variances on '
                                                               'completed robotics orders and post KO88 settlements.',
                                                'slug': 'nova-mfg-production-variance-investigation',
                                                'title': 'Production Order Variance & WIP Settlement Investigation'},
                     'step_id': 'd42_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered WIP, variance analysis, and KO88 cost settlement. Next, you will '
                                   'synthesize all modules in the Integrated Cross-Module Enterprise Case.',
                     'title': 'Day 42 Complete: Cost Settlement Mastered'}],
    'subtitle': 'Period-end production cost accounting: Work-in-Process (WIP) calculation, variance analysis, and '
                'order settlement (KO88)',
    'title': 'WIP / Variance / Cost Settlement'},
    43: {   'atomic_concepts': ['e2e-process-integration-synthesis'],
    'day_number': 43,
    'estimated_minutes': 50,
    'recommended_mission_slug': 'nova-e2e-enterprise-cross-module-recovery',
    'slug': 'cross-module-enterprise-case',
    'steps': [   {   'content_md': '### Cross-Module Process Synergy\n'
                                   'In modern enterprise operations at Nova Manufacturing Corp (NM01), business '
                                   'departments do not operate in isolation. A single customer demand triggers a '
                                   'synchronized chain across all ERP functional modules:\n'
                                   '\n'
                                   '```\n'
                                   '[SD] Sales Order -> [PP] Production Order -> [MM] Procurement Requisition\n'
                                   '     |                    |                         |\n'
                                   '[SD] Outbound Delivery    |                    [MM] Purchase Order\n'
                                   '     |                    |                         |\n'
                                   '[SD] PGI (COGS)      <- [PP] Confirm & FG Receipt <- [MM] Goods Receipt (MIGO)\n'
                                   '     |                    |                         |\n'
                                   '[SD] Customer Billing     |                    [FI] Invoice Verification (MIRO)\n'
                                   '     |                    |                         |\n'
                                   '[FI] Cash Collection     [FI] Order Settlement (KO88) [FI] Payment Run (F110)\n'
                                   '```\n'
                                   '\n'
                                   '### Enterprise Invariants Across Modules\n'
                                   '1. **Supply-Driven Demand**: If raw materials are missing, manufacturing cannot '
                                   'confirm orders, delaying customer delivery.\n'
                                   '2. **Accounting Reconciliation Harmony**:\n'
                                   '   - Upstream: GR/IR clearing account (`211200`) balances between MIGO and MIRO.\n'
                                   '   - Manufacturing: Work-in-Process and Price Variances (`530000`) settle to zero '
                                   'via KO88.\n'
                                   '   - Downstream: Post Goods Issue books COGS (`500000`), and Customer Billing '
                                   'books Revenue (`410000`) and Tax (`217000`).',
                     'key_terms': [   {   'definition': 'Auditable chain linking commercial, logistical, and financial '
                                                        'documents across all modules.',
                                          'term': 'Document Flow'},
                                      {   'definition': 'System event where a logistical action automatically triggers '
                                                        'a financial accounting posting.',
                                          'term': 'Integration Touchpoint'}],
                     'step_id': 'd43_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Cross-module integration ensures that supply chain events synchronously generate '
                                 'auditable financial records.',
                     'title': 'The Unified Enterprise Chain: From Procurement to Customer Cash'},
                 {   'content_md': '### Trace of Enterprise Journal Postings\n'
                                   'During an integrated production cycle at Nova Manufacturing:\n'
                                   '1. **Raw Material Receipt (MIGO / Mov 101)**:\n'
                                   '   - Debit: Raw Material Inventory (`131000`)\n'
                                   '   - Credit: GR/IR Interim Clearing (`211200`)\n'
                                   '2. **Supplier Invoice Verification (MIRO)**:\n'
                                   '   - Debit: GR/IR Interim Clearing (`211200`)\n'
                                   '   - Credit: Vendor Accounts Payable (`211000`)\n'
                                   '3. **Component Issue to Production (CO01 / Mov 261)**:\n'
                                   '   - Debits Production Order cost collector (`510000`)\n'
                                   '   - Credit: Raw Material Inventory (`131000`)\n'
                                   '4. **Finished Product Receipt (CO11N / Mov 101)**:\n'
                                   '   - Debit: Finished Goods Inventory (`132000`)\n'
                                   '   - Credit: Production Order Output Credit (`520000`)\n'
                                   '5. **Customer Delivery Post Goods Issue (VL01N / Mov 601)**:\n'
                                   '   - Debit: Cost of Goods Sold (`500000`)\n'
                                   '   - Credit: Finished Goods Inventory (`132000`)\n'
                                   '6. **Customer Billing (VF01)**:\n'
                                   '   - Debit: Customer Accounts Receivable (`121000`)\n'
                                   '   - Credit: Sales Revenue (`410000`)\n'
                                   '   - Credit: Output Sales Tax (`217000`)\n'
                                   '7. **Period-End Order Settlement (KO88)**:\n'
                                   '   - Clears Production Order variance balance to Price Variance (`530000`).',
                     'key_terms': [   {   'definition': 'Single table recording all cross-module financial, '
                                                        'managerial, and inventory entries.',
                                          'term': 'Universal Journal (ACDOCA)'},
                                      {   'definition': 'Cost controlling procedure balancing order debits and credits '
                                                        'at period end.',
                                          'term': 'Order Settlement'}],
                     'step_id': 'd43_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Every stage of the continuous enterprise trace maintains accounting balance across '
                                 'balance sheet and P&L accounts.',
                     'title': 'The Complete Document & Financial Ledger Audit Trail'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'sales_order': '5000021000',
                                            'total_revenue': '€75,000'},
                     'content_md': '### End-to-End Enterprise Timeline\n'
                                   '- **T0**: Sales Order #5000021000 created; aATP identifies component shortage.\n'
                                   '- **T1**: PR #10004500 and PO #4500018900 issued to VEND-101 for 50 sensors.\n'
                                   '- **T2**: MIGO Mov 101 receives sensors into RAW1; MIRO matches supplier invoice '
                                   'for €6,000.\n'
                                   '- **T3**: Production Order #100888 consumes sensors (Mov 261), confirms assembly '
                                   '(CO11N), and receives 50 controllers into FG01 (Mov 101).\n'
                                   '- **T4**: Delivery #80010042 dispatched; PGI Mov 601 records COGS of €45,000.\n'
                                   '- **T5**: Billing Document #900055 created; records €75,000 Revenue and €14,250 '
                                   'Tax.\n'
                                   '- **T6**: Production order settled via KO88.',
                     'scenario': 'Customer CUST-501 places a rush order for 50 units of DXTR-1000 controllers at '
                                 '€1,500/EA (€75,000 total). Plant PL01 must procure raw sensors, manufacture '
                                 'assemblies, dispatch goods, and invoice the customer.',
                     'step_id': 'd43_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Integrated Case: Order #5000021000'},
                 {   'component_type': 'ScenarioDecision',
                     'instruction': 'Evaluate the handoff error where finished goods receipt (Mov 101) succeeded, but '
                                    'the customer delivery cannot be created because the shipping point is missing. '
                                    'Determine the required corrective action.',
                     'options': [   {   'explanation': 'Correct! Resolving shipping point determination allows '
                                                       'delivery creation.',
                                        'id': 'opt_d43_shp',
                                        'is_correct': True,
                                        'text': 'Check table TVSTZ configuration to ensure Shipping Condition 01 + '
                                                'Loading Group 0001 + Delivering Plant PL01 resolves to Shipping Point '
                                                '1000.'},
                                    {   'explanation': 'Absurd and highly destructive action.',
                                        'id': 'opt_d43_cancel',
                                        'is_correct': False,
                                        'text': 'Cancel the production order and scrap all 50 controllers.'},
                                    {   'explanation': 'Severe audit violation bypassing shipping governance.',
                                        'id': 'opt_d43_ignore',
                                        'is_correct': False,
                                        'text': 'Ship the goods without an outbound delivery document.'}],
                     'step_id': 'd43_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Supply chain execution requires resolving master data and configuration handoffs '
                                 'across modules.',
                     'title': '[SIMULATION MODEL] Cross-Module Enterprise Execution Drill'},
                 {   'instruction': 'Identify the proper operational recovery sequence.',
                     'options': [   {   'explanation': 'Correct! VKOA provides the missing revenue G/L mapping, and '
                                                       'VFX3 releases the document to ACDOCA.',
                                        'id': 'opt_d43_c1',
                                        'is_correct': True,
                                        'text': 'Maintain table VKOA to map Account Key ERL to G/L Revenue Account '
                                                '410000 for Sales Org SO01, then execute transaction VFX3 and choose '
                                                "'Release to Accounting'."},
                                    {   'explanation': 'Incorrect! Breaks document flow reconciliation between SD and '
                                                       'FI.',
                                        'id': 'opt_d43_c2',
                                        'is_correct': False,
                                        'text': 'Post a manual journal in FB50 to debit bank and credit revenue, '
                                                'leaving the billing document blocked in VFX3.'},
                                    {   'explanation': 'Does not resolve the missing revenue account determination '
                                                       'error.',
                                        'id': 'opt_d43_c3',
                                        'is_correct': False,
                                        'text': 'Change the customer currency to Japanese Yen to force the document '
                                                'through.'}],
                     'scenario': 'During financial close, the auditor discovers that Invoice #900055 was created in '
                                 'SD, but table ACDOCA has no corresponding revenue journal. Transaction VFX3 reports '
                                 "error VF051 'Account determination error for Account Key ERL'.",
                     'step_id': 'd43_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Cross-Functional Exception Recovery Challenge'},
                 {   'questions': [   {   'concept_slug': 'e2e-process-integration-synthesis',
                                          'explanation': 'Supply chain prerequisites dictate that raw materials must '
                                                         'be received before manufacturing, which precedes delivery, '
                                                         'billing, and settlement.',
                                          'id': 'd43_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': '1) Goods Receipt of raw materials -> 2) '
                                                                     'Production execution & confirmation -> 3) '
                                                                     'Outbound delivery & PGI -> 4) Customer Billing '
                                                                     '-> 5) Order Settlement.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': '1) Customer Billing -> 2) Post Goods Issue -> 3) '
                                                                     'Production execution -> 4) Goods Receipt.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': '1) Order Settlement -> 2) Customer Billing -> 3) '
                                                                     'Production execution -> 4) Sourcing.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': '1) Outbound Delivery -> 2) Raw Material '
                                                                     'Requisition -> 3) PGI -> 4) Customer Billing.'}],
                                          'prompt': 'What is the mandatory chronological operational sequence across '
                                                    'ERP modules to fulfill a make-to-order customer requirement?',
                                          'question_id': 'd43_q1'},
                                      {   'concept_slug': 'e2e-process-integration-synthesis',
                                          'explanation': 'ACDOCA provides real-time single-source-of-truth integration '
                                                         'across logistics and finance.',
                                          'id': 'd43_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'By synchronously posting Universal Journal line '
                                                                     'items for every inventory movement, billing '
                                                                     'document, and cost settlement with inherited '
                                                                     'organizational dimensions.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'By executing nightly manual batch reconciliation '
                                                                     'programs that compare paper receipts.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'By storing only summary totals without document '
                                                                     'references.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'By excluding logistics transactions from the '
                                                                     'general ledger.'}],
                                          'prompt': 'How does table ACDOCA maintain consistency between logistics '
                                                    'movements and financial reporting during an integrated order?',
                                          'question_id': 'd43_q2'}],
                     'step_id': 'd43_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 43 Mastery Assessment: Cross-Module Integration'},
                 {   'step_id': 'd43_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Traced end-to-end continuous flow across Procurement, Manufacturing, Sales, and '
                                   'Finance.\n'
                                   '- Audited cross-module journal postings across inventory, GR/IR, COGS, revenue, '
                                   'and variance accounts.\n'
                                   '- Resolved integration handoff bottlenecks and billing accounting release blocks '
                                   'in VFX3.',
                     'title': 'Mastery Verification: End-to-End Enterprise Flow'},
                 {   'recommended_mission': {   'description': 'Resolve a cascading cross-module supply chain failure '
                                                               'spanning PR, PO, GR, Production, Sales, PGI, and FI '
                                                               'settlement.',
                                                'slug': 'nova-e2e-enterprise-cross-module-recovery',
                                                'title': 'End-to-End Enterprise Process Recovery: Nova Crisis'},
                     'step_id': 'd43_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered the complete end-to-end enterprise integration flow. You are now '
                                   'prepared for the Practical Multi-Concept Capstone.',
                     'title': 'Day 43 Complete: Integrated Cross-Module Case Mastered'}],
    'subtitle': 'End-to-end continuous business case: Procurement -> Inventory -> Manufacturing -> Sales -> Finance '
                'for Nova Manufacturing',
    'title': 'Integrated Cross-Module Enterprise Case'},
    44: {   'atomic_concepts': ['e2e-process-integration-synthesis'],
    'day_number': 44,
    'estimated_minutes': 60,
    'recommended_mission_slug': 'nova-e2e-enterprise-cross-module-recovery',
    'slug': 'practical-multi-concept-capstone',
    'steps': [   {   'content_md': '### Core End-to-End Business Processes Architecture\n'
                                   'Phase 3 (Days 23–44) covered the foundational business execution loops that drive '
                                   'enterprise operations in SAP S/4HANA:\n'
                                   '1. **Procure-to-Pay (P2P)**: Requisitions, Sourcing, POs, Goods Receipt (Mov 101), '
                                   'Invoice Verification (MIRO), and GR/IR clearing.\n'
                                   '2. **Order-to-Cash (O2C)**: Condition pricing, Sales Orders, aATP, Delivery, Post '
                                   'Goods Issue (Mov 601 / COGS), and Billing (VF01 / Revenue).\n'
                                   '3. **Financial Accounting (FI)**: Universal Journal (ACDOCA), G/L (FB50), AP '
                                   'subledger (F110), AR subledger (F-28 / Dunning), and Month-End Close (AFAB / '
                                   'FAGL_FCV / OB52).\n'
                                   '4. **Discrete Manufacturing (PP/CO)**: BOMs, Work Centers, Routings, Production '
                                   'Orders (Mov 261 & 101), Confirmations (CO11N), and Cost Settlement (KO88).',
                     'key_terms': [   {   'definition': 'Unified understanding of logistics, manufacturing, and '
                                                        'financial integration.',
                                          'term': 'Cross-Functional Synthesis'},
                                      {   'definition': 'Non-negotiable accounting and logistical rules governing '
                                                        'S/4HANA execution.',
                                          'term': 'Enterprise Invariants'}],
                     'step_id': 'd44_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'True enterprise mastery requires understanding how operational transactions across '
                                 'MM, SD, and PP synchronously drive ACDOCA.',
                     'title': 'Phase 3 Comprehensive Benchmark Synthesis'},
                 {   'content_md': '### Benchmark Evaluation Architecture\n'
                                   'This Capstone evaluates **19 distinct core business process concepts** across P2P, '
                                   'O2C, Finance, and Manufacturing.\n'
                                   '\n'
                                   'Each evaluation item independently measures your operational diagnosis and '
                                   'configuration mastery. In the event of an incorrect answer, the knowledge engine '
                                   'immediately routes the specific deficit to a targeted DAG remediation capsule '
                                   'without failing unrelated modules.',
                     'key_terms': [   {   'definition': 'DAG-driven routing that isolates specific conceptual '
                                                        'deficiencies.',
                                          'term': 'Targeted Remediation'},
                                      {   'definition': 'Rigorous proof of operational competence across business '
                                                        'cycles.',
                                          'term': 'Mastery Evidence'}],
                     'step_id': 'd44_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Each question evaluates a specific concept node in the DAG, ensuring precise '
                                 'assessment without score masking.',
                     'title': 'Independent Multi-Dimensional Evaluation Framework'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'evaluation_concepts': '19 distinct concepts'},
                     'content_md': '### Evaluation Spectrum\n'
                                   '- **Procure-to-Pay**: PR demand, Account Assignment, Sourcing, Workflow, MIGO 101, '
                                   'GR/IR, 3-way match, F110.\n'
                                   '- **Order-to-Cash**: Pricing procedure, Partner determination, aATP, Shipping '
                                   'Point, PGI Mov 601, VF01 Billing.\n'
                                   '- **Finance & Controlling**: Posting Keys 40/50, Special G/L, Period-end close, '
                                   'Inventory scrap Mov 551.\n'
                                   '- **Manufacturing Execution**: BOM & Routing, Production Order confirmation, KO88 '
                                   'Settlement.',
                     'scenario': 'Nova Manufacturing Corp (NM01) evaluation suite covering all operational cycles '
                                 'across Heidelberg (PL01) and Austin (PL02).',
                     'step_id': 'd44_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Capstone Assessment Architecture Overview'},
                 {   'component_type': 'ScenarioDecision',
                     'instruction': 'Confirm readiness to begin the 19-concept comprehensive benchmark evaluation.',
                     'options': [   {   'explanation': 'Proceed to the assessment step to begin.',
                                        'id': 'opt_d44_ready',
                                        'is_correct': True,
                                        'text': 'I am ready to complete the 19-concept comprehensive benchmark '
                                                'evaluation across P2P, O2C, FI, and Manufacturing.'}],
                     'step_id': 'd44_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Approach each question with rigorous enterprise operational awareness.',
                     'title': '[SIMULATION MODEL] Capstone Readiness Self-Check'},
                 {   'instruction': 'Select the architectural explanation.',
                     'options': [   {   'explanation': 'Correct! Universal Journal single-table architecture '
                                                       'eliminates batch reconciliation overhead.',
                                        'id': 'opt_d44_synch',
                                        'is_correct': True,
                                        'text': 'Real-time posting eliminates reconciliation batch lags, guarantees '
                                                'immediate synchronization between logistics and financial accounting, '
                                                'and provides a single source of truth.'},
                                    {   'explanation': 'Incorrect! S/4HANA posts directly and synchronously.',
                                        'id': 'opt_d44_batch',
                                        'is_correct': False,
                                        'text': 'Batch reconciliation is still required because MM and SD cannot write '
                                                'to FI.'},
                                    {   'explanation': 'Incorrect! Real-time Universal Journal entries eliminate '
                                                       'manual reconciliation.',
                                        'id': 'opt_d44_opt3',
                                        'is_correct': False,
                                        'text': 'S/4HANA requires database administrators to manually reconcile '
                                                'subledgers at the end of each week.'}],
                     'scenario': 'Why does S/4HANA execute real-time postings to table ACDOCA from MIGO, VF01, and '
                                 'KO88 rather than relying on batch reconciliation interfaces?',
                     'step_id': 'd44_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Phase 3 Synthesis Architecture Challenge'},
                 {   'questions': [   {   'concept_slug': 'p2p-pr-creation',
                                          'explanation': 'A PR is strictly an internal demand request; external '
                                                         'liability arises only with a Purchase Order.',
                                          'id': 'd44_q1_p2p_pr',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'It captures internal material or service demand '
                                                                     'without creating external commercial liability '
                                                                     'or financial ledger entries.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'It creates a legally binding contract with the '
                                                                     'supplier.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'It debits Accounts Payable and credits Bank '
                                                                     'Cash.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'It records physical warehouse receiving in '
                                                                     'MATDOC.'}],
                                          'prompt': 'In the Procure-to-Pay process, what is the primary role of a '
                                                    'Purchase Requisition (PR) in table EBAN?',
                                          'question_id': 'd44_q1_p2p_pr'},
                                      {   'concept_slug': 'account-assignment-categories',
                                          'explanation': "AAC 'K' directs the purchase to an overhead cost center "
                                                         'rather than balance sheet inventory.',
                                          'id': 'd44_q2_aac',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': "Account Assignment Category 'K' (Cost Center), "
                                                                     'which expenses the item upon goods receipt.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Blank Account Assignment Category (Balance sheet '
                                                                     'inventory asset).'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Customer Account Group 0001.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Distribution Channel 10.'}],
                                          'prompt': 'When purchasing non-stock consumable supplies (e.g. factory '
                                                    'safety gear) for a cost center, which Account Assignment Category '
                                                    'is required?',
                                          'question_id': 'd44_q2_aac'},
                                      {   'concept_slug': 'p2p-sourcing-rfq',
                                          'explanation': 'Effective landed cost factors in all freight, duties, and '
                                                         'discount conditions.',
                                          'id': 'd44_q3_sourcing',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Gross Price minus prompt payment discounts, plus '
                                                                     'freight surcharges and import duties.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Gross quotation headline price only.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Historical prior-year invoice price.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Material standard cost from MBEW.'}],
                                          'prompt': 'When evaluating vendor bids under different Incoterms (e.g. EXW '
                                                    'vs DDP), how must effective landed cost be determined?',
                                          'question_id': 'd44_q3_sourcing'},
                                      {   'concept_slug': 'flexible-workflow',
                                          'explanation': 'Flexible Workflow provides low-code, rule-based approval '
                                                         'workflows natively in Fiori.',
                                          'id': 'd44_q4_workflow',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'By dynamically evaluating configured '
                                                                     'precondition rules (e.g. Net Value > €10,000, '
                                                                     'Purchasing Group) in Fiori.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'By requiring manual user exit ABAP code '
                                                                     'modifications for every threshold change.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'By bypassing all manager approvals '
                                                                     'automatically.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'By sending orders to external non-SAP email '
                                                                     'servers.'}],
                                          'prompt': 'How does S/4HANA Flexible Workflow determine approval routing for '
                                                    'Purchase Orders?',
                                          'question_id': 'd44_q4_workflow'},
                                      {   'concept_slug': 'p2p-goods-receipt-migo',
                                          'explanation': 'MIGO Mov 101 writes to MATDOC for inventory quantity and '
                                                         'ACDOCA for financial accounting.',
                                          'id': 'd44_q5_gr',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Table MATDOC is updated with the material '
                                                                     'movement, and ACDOCA is updated with inventory '
                                                                     'and GR/IR postings.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Only table VBAK is updated.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Only table KNA1 is updated.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Zero database tables are updated until invoice '
                                                                     'receipt.'}],
                                          'prompt': 'When a warehouse clerk executes transaction MIGO for Movement '
                                                    'Type 101, what primary tables are updated?',
                                          'question_id': 'd44_q5_gr'},
                                      {   'concept_slug': 'gr-ir-clearing-account',
                                          'explanation': 'GR/IR clearing holds provisional liability between goods '
                                                         'receipt and invoice receipt.',
                                          'id': 'd44_q6_grir',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'It serves as an interim balance sheet clearing '
                                                                     'account bridging the timing difference between '
                                                                     'physical goods receipt and invoice receipt.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'It records customer sales revenue.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'It accumulates corporate income tax '
                                                                     'liabilities.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'It records bank cash withdrawals.'}],
                                          'prompt': 'What is the accounting role of the GR/IR clearing account (e.g. '
                                                    'Account 211200 in the Nova simulation model)?',
                                          'question_id': 'd44_q6_grir'},
                                      {   'concept_slug': 'three-way-matching',
                                          'explanation': '3-way matching compares PO, GR, and supplier invoice to '
                                                         'verify quantity and price compliance.',
                                          'id': 'd44_q7_3way',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Purchase Order terms vs Goods Receipt delivered '
                                                                     'quantity vs Supplier Invoice billed '
                                                                     'amount/quantity.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Customer Inquiry vs Sales Quotation vs Sales '
                                                                     'Order.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Material Master vs BOM vs Routing.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Asset Master vs Depreciation Schedule vs Bank '
                                                                     'Statement.'}],
                                          'prompt': 'In Logistics Invoice Verification (MIRO), what three documents '
                                                    'are verified during a 3-way match?',
                                          'question_id': 'd44_q7_3way'},
                                      {   'concept_slug': 'p2p-f110-payment-run',
                                          'explanation': 'F110 automates batch vendor payments and clears Accounts '
                                                         'Payable open items.',
                                          'id': 'd44_q8_f110',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'It evaluates open vendor invoices based on due '
                                                                     'dates and cash discounts, generates electronic '
                                                                     'payment media, and clears vendor liabilities.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'It creates new purchase requisitions for '
                                                                     'low-stock materials.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'It calculates depreciation on production '
                                                                     'machinery.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'It issues customer credit memos.'}],
                                          'prompt': 'What is the primary function of the Automatic Payment Program '
                                                    '(transaction F110) in corporate treasury?',
                                          'question_id': 'd44_q8_f110'},
                                      {   'concept_slug': 'condition-technique',
                                          'explanation': 'The Condition Technique uses pricing procedures, condition '
                                                         'types, access sequences, and condition tables.',
                                          'id': 'd44_q9_pricing',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'It executes a configured Pricing Procedure '
                                                                     'evaluating Condition Types (PR00, K004, MWST) '
                                                                     'using Access Sequences linked to Condition '
                                                                     'Tables.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'It queries the purchasing info record directly.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': "It uses the vendor's wholesale catalog price."},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'It prompts the sales manager to enter a manual '
                                                                     'price for every order.'}],
                                          'prompt': 'In SD pricing, how does the Condition Technique determine the net '
                                                    'sales price of an item?',
                                          'question_id': 'd44_q9_pricing'},
                                      {   'concept_slug': 'partner-determination',
                                          'explanation': 'Standard partner functions in SD are Sold-to (SP), Ship-to '
                                                         '(SH), Bill-to (BP), and Payer (PY).',
                                          'id': 'd44_q10_partner',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Sold-to Party (SP), Ship-to Party (SH), Bill-to '
                                                                     'Party (BP), and Payer (PY).'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Vendor, Purchasing Org, Plant, and Buyer.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Company Code, Cost Center, Profit Center, and '
                                                                     'Segment.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Creator, Approver, Reviewer, and Auditor.'}],
                                          'prompt': 'What are the four mandatory standard SD partner functions '
                                                    'established during Sales Order creation?',
                                          'question_id': 'd44_q10_partner'},
                                      {   'concept_slug': 'advanced-atp-s4',
                                          'explanation': 'ABC in aATP dynamically substitutes delivering plants or '
                                                         'materials to satisfy demand.',
                                          'id': 'd44_q11_atp',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'It automatically evaluates and confirms stock '
                                                                     'from substitute delivering plants or alternative '
                                                                     'materials during shortages.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'It deletes customer backorders immediately.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'It prevents customer orders from being entered.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'It converts sales orders into purchase '
                                                                     'requisitions.'}],
                                          'prompt': 'What capability does Alternative-Based Confirmation (ABC) provide '
                                                    'in S/4HANA Advanced ATP?',
                                          'question_id': 'd44_q11_atp'},
                                      {   'concept_slug': 'shipping-point-determination',
                                          'explanation': 'Shipping point determination is configured combining '
                                                         'Shipping Condition, Loading Group, and Plant.',
                                          'id': 'd44_q12_shp',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Shipping Condition (Customer Master) + Loading '
                                                                     'Group (Material Master) + Delivering Plant.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Purchasing Org + Purchasing Group + Vendor.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Cost Center + Profit Center + Company Code.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Sales Org + Distribution Channel + Division.'}],
                                          'prompt': 'How is the Shipping Point determined in an Outbound Delivery?',
                                          'question_id': 'd44_q12_shp'},
                                      {   'concept_slug': 'o2c-post-goods-issue',
                                          'explanation': 'PGI documents inventory reduction and COGS recognition; it '
                                                         'does NOT record sales revenue.',
                                          'id': 'd44_q13_pgi',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Debit: Cost of Goods Sold (COGS) / Credit: '
                                                                     'Finished Goods Inventory.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Debit: Customer Accounts Receivable / Credit: '
                                                                     'Sales Revenue.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Debit: Bank Cash / Credit: Accounts Receivable.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Debit: Inventory / Credit: GR/IR Clearing.'}],
                                          'prompt': 'What financial accounting entry is posted in table ACDOCA when '
                                                    'Post Goods Issue (Movement Type 601) is executed?',
                                          'question_id': 'd44_q13_pgi'},
                                      {   'concept_slug': 'revenue-recognition-posting',
                                          'explanation': 'Billing (VF01) triggers revenue, output sales tax, and '
                                                         'customer receivables recognition in ACDOCA.',
                                          'id': 'd44_q14_billing',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Customer Billing Document created in transaction '
                                                                     'VF01 (table VBRK/VBRP).'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Sales Order confirmation in VA01.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Post Goods Issue in VL01N.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Incoming customer payment in F-28.'}],
                                          'prompt': 'In Order-to-Cash, which transaction and document is the '
                                                    'authoritative trigger for Sales Revenue and Accounts Receivable '
                                                    'recognition?',
                                          'question_id': 'd44_q14_billing'},
                                      {   'concept_slug': 'posting-keys',
                                          'explanation': 'In SAP standard accounting, Posting Key 40 indicates G/L '
                                                         'Debit, and Posting Key 50 indicates G/L Credit.',
                                          'id': 'd44_q15_gl',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Posting Key 40 = Debit G/L Account; Posting Key '
                                                                     '50 = Credit G/L Account.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Posting Key 40 = Vendor Invoice; Posting Key 50 '
                                                                     '= Customer Invoice.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Posting Key 40 = Asset Acquisition; Posting Key '
                                                                     '50 = Asset Retirement.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Posting Key 40 = Period Open; Posting Key 50 = '
                                                                     'Period Close.'}],
                                          'prompt': 'In SAP General Ledger journal entries (FB50 / ACDOCA), what do '
                                                    'Posting Keys 40 and 50 signify?',
                                          'question_id': 'd44_q15_gl'},
                                      {   'concept_slug': 'special-gl-indicators',
                                          'explanation': 'Special G/L indicators route items like down payments to '
                                                         'alternative reconciliation accounts.',
                                          'id': 'd44_q16_spgl',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'To post transactions to alternative balance '
                                                                     'sheet reconciliation accounts without altering '
                                                                     'master data.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'To bypass general ledger posting entirely.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'To hide payments from financial auditors.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'To eliminate the need for double-entry '
                                                                     'bookkeeping.'}],
                                          'prompt': "Why are Special G/L Indicators (such as 'A' for Down Payments) "
                                                    'used in subledger accounting?',
                                          'question_id': 'd44_q16_spgl'},
                                      {   'concept_slug': 'period-end-closing',
                                          'explanation': 'All valuation postings must complete before locking posting '
                                                         'periods in OB52.',
                                          'id': 'd44_q17_close',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Post valuation runs (Depreciation AFAB, Foreign '
                                                                     'Currency Valuation FAGL_FCV, Cost Settlement '
                                                                     'KO88), reconcile GR/IR, then lock periods in '
                                                                     'OB52.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Lock periods in OB52 first, then run AFAB and '
                                                                     'KO88.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Delete open sales orders, then lock periods.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Run OB52 at the beginning of the month and leave '
                                                                     'it locked.'}],
                                          'prompt': 'In what sequence should month-end closing tasks be executed '
                                                    'before locking posting periods in transaction OB52?',
                                          'question_id': 'd44_q17_close'},
                                      {   'concept_slug': 'mfg-bom-master',
                                          'explanation': "BOM defines 'what' parts are required; Routing defines 'how' "
                                                         "and 'where' operations execute.",
                                          'id': 'd44_q18_mfg_bom',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'The BOM defines the component ingredients/parts, '
                                                                     'while the Routing defines the operational '
                                                                     'sequence, work centers, and labor/machine run '
                                                                     'times.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'The BOM defines sales pricing, while the Routing '
                                                                     'defines vendor purchasing terms.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'The BOM and Routing are identical records in '
                                                                     'table CS01.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'BOMs are used only in Finance, while Routings '
                                                                     'are used only in SD.'}],
                                          'prompt': 'In discrete manufacturing, what is the architectural relationship '
                                                    'between a Bill of Materials (BOM) and a Routing?',
                                          'question_id': 'd44_q18_mfg_bom'},
                                      {   'concept_slug': 'production-order-settlement',
                                          'explanation': 'KO88 settles production variances to financial accounting, '
                                                         'bringing the order cost collector to zero balance.',
                                          'id': 'd44_q19_settle',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'The order balance (difference between actual '
                                                                     'debits and standard credits) is settled to Price '
                                                                     'Variance (G/L 530000) in ACDOCA, balancing the '
                                                                     'order to zero.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'The order is deleted from the database.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'The customer is automatically sent a cash '
                                                                     'refund.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Inventory quantities in warehouse storage bins '
                                                                     'are reset to zero.'}],
                                          'prompt': 'What occurs during period-end Production Order Settlement '
                                                    '(transaction KO88) for a completed order (status TECO/DLV)?',
                                          'question_id': 'd44_q19_settle'}],
                     'step_id': 'd44_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Phase 3 Comprehensive Benchmark Assessment (19 Concepts)'},
                 {   'step_id': 'd44_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Validated 19 distinct core business process concepts across P2P, O2C, FI, and '
                                   'Manufacturing.\n'
                                   '- Proved accounting integrity across GR/IR, inventory, COGS, revenue, and variance '
                                   'accounts.\n'
                                   '- Successfully achieved Phase 3 Core Business Processes certification.',
                     'title': 'Mastery Verification: Phase 3 Comprehensive Certification'},
                 {   'recommended_mission': {   'description': 'Resolve a cascading cross-module supply chain failure '
                                                               'spanning PR, PO, GR, Production, Sales, PGI, and FI '
                                                               'settlement.',
                                                'slug': 'nova-e2e-enterprise-cross-module-recovery',
                                                'title': 'End-to-End Enterprise Process Recovery: Nova Crisis'},
                     'step_id': 'd44_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'Congratulations! You have completed Phase 3 (Core End-to-End Business Processes). '
                                   'You are now prepared to advance to Phase 4 (HANA Engine & Data Semantics: CDS, '
                                   'VDM, Analytics).',
                     'title': 'Day 44 Complete: Phase 3 Capstone Achieved!'}],
    'subtitle': 'Multi-dimensional benchmark evaluation rigorously testing 19 distinct core business process concepts',
    'title': 'Practical Multi-Concept Capstone'},
}
