"""Authoritative content definitions for SAP S/4HANA Guided Learning Days 45–54 (Phase 4).

Phase 4: HANA Engine & Data Semantics (HANA, VDM, CDS, Analytics, DCL).

Enterprise Continuous Model: Nova Manufacturing Corp (NM01)
- Plants: PL01 (Heidelberg Assembly), PL02 (Austin Tech Center)
- Purchasing Org: PO01, Sales Org: SO01
- Storage Locations: RAW1 (Raw Materials), FG01 (Finished Goods)
- Master Materials: RAW-01 (Optical Sensor Array), DXTR-1000 (Industrial Robotics Controller)
- Business Partners: VEND-101 (Rheinland Precision Optics), CUST-501 (Nordics Heavy Industrial AB)

Technical Truthfulness Invariants Enforced:
- HANA columnar engine uses secondary inverted indexes; it is false that "HANA needs no indexes".
- HANA pages data on-demand from persistence; it is false that "everything is always in RAM".
- Associations are lazy on-demand joins that save memory and CPU via join pruning.
- Pushdown is optimal for data-intensive set operations, not for procedural row-by-row logic.
- Modern S/4HANA uses RAP Service Definitions/Bindings, not legacy @OData.publish: true.
"""

from __future__ import annotations
from typing import Any

PHASE_4_DAYS_CONTENT: dict[int, dict[str, Any]] = {
    45: {   'atomic_concepts': ['hana-calc-engine', 'planviz-analysis', 'sql-optimizer-pushdown', 'delta-merge-architecture'],
    'day_number': 45,
    'estimated_minutes': 90,
    'recommended_mission_slug': 'nova-hana-performance-incident',
    'slug': 'hana-engine-internals',
    'steps': [   {   'content_md': '### The SAP HANA Indexserver Architecture\n'
                                   'In SAP S/4HANA, the **Indexserver** is the primary engine process responsible for '
                                   'in-memory data processing, transaction management, query optimization, and '
                                   'persistence.\n'
                                   '\n'
                                   'Key Architectural Foundations:\n'
                                   '1. **Column Store vs Row Store**: In standard S/4HANA transactional and analytical '
                                   'workloads, virtually all business tables (`ACDOCA`, `MATDOC`, `VBAK`, `EKKO`) '
                                   'reside in the **Column Store**. Data is partitioned vertically by column, enabling '
                                   'extreme SIMD compression (dictionary encoding, run-length encoding, bit-vector '
                                   'packing).\n'
                                   '2. **Main Store & Delta Store**:\n'
                                   '   - **Main Store**: Highly compressed, read-optimized, dictionary-encoded, and '
                                   'read-only.\n'
                                   '   - **Delta Store**: Write-optimized buffer receiving all real-time `INSERT`, '
                                   '`UPDATE`, and `DELETE` operations.\n'
                                   '   - **Delta Merge**: Periodic consolidation process that merges Main 1 + Delta 1 '
                                   'into a newly compressed Main 2 while routing concurrent writes into Delta 2.\n'
                                   '3. **Dual Persistence Layer**:\n'
                                   '   - **Persistent Data Volumes**: SAP HANA creates savepoints to persistent data '
                                   'volumes; the default interval is approximately 5 minutes and is configurable.\n'
                                   '   - **Redo Log Volumes**: Synchronous logging of all committed transactions '
                                   'protects committed changes between savepoints, ensuring ACID compliance and crash '
                                   'recovery.',
                     'key_terms': [   {   'definition': 'Core HANA database engine process hosting SQL engines, '
                                                        'execution plans, and data stores.',
                                          'term': 'Indexserver'},
                                      {   'definition': 'In-memory maintenance process merging write-optimized delta '
                                                        'buffers into read-optimized main columnar storage.',
                                          'term': 'Delta Merge'},
                                      {   'definition': 'Technique replacing variable-length cell values with compact '
                                                        'integer bit-vectors mapped to sorted distinct dictionaries.',
                                          'term': 'Dictionary Encoding'}],
                     'step_id': 'd45_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'HANA decouples fast transactional writes (Delta Store) from ultra-compressed SIMD '
                                 'reads (Main Store) with asynchronous persistence savepoints.',
                     'title': 'SAP HANA Indexserver & In-Memory Storage Architecture'},
                 {   'content_md': '### Dispelling Common HANA Architecture Myths\n'
                                   '> **CRITICAL ARCHITECTURAL SAFEGUARDS**:\n'
                                   '> 1. **"HANA needs no indexes" (FALSE)**: HANA column store extensively utilizes '
                                   '**secondary inverted indexes** to optimize point lookups, foreign key constraints, '
                                   'and partition pruning.\n'
                                   '> 2. **"Everything is always in RAM" (FALSE)**: Tables and partitions are loaded '
                                   'into memory on-demand. Infrequently accessed cold/warm data is aged out or managed '
                                   'via Native Storage Extension (NSE) on non-volatile SSDs.\n'
                                   '> 3. **"Pushdown is always faster" (FALSE)**: Pushing down complex row-by-row '
                                   'procedural logic or non-pushable calculations into the database can cause '
                                   'expensive engine-hops between the SQL engine and the Calculation Engine. Pushdown '
                                   'is optimal for data-intensive set operations, aggregations, and joins.\n'
                                   '\n'
                                   '### Plan Visualizer (PlanViz) Execution Analysis\n'
                                   'Database administrators and architects use **PlanViz** in SAP HANA Studio or '
                                   'Eclipse ADT to inspect the compiled physical execution plan:\n'
                                   '- **Inclusive Time**: Total time spent in an operator node including all child '
                                   'sub-tree operations.\n'
                                   '- **Exclusive Time**: CPU and memory time consumed directly by the specific '
                                   'operator node.\n'
                                   '- **Engine Breakdown**: Identifies whether execution ran in the optimized **Column '
                                   'Engine**, transitioned to the **Calculation Engine**, or fell back to the row '
                                   'engine.',
                     'key_terms': [   {   'definition': 'HANA graphical performance tracer displaying operator '
                                                        'execution trees, cardinalities, and engine assignments.',
                                          'term': 'PlanViz'},
                                      {   'definition': 'Auxiliary column store structure providing fast reverse '
                                                        'value-to-row lookup vectors.',
                                          'term': 'Secondary Inverted Index'},
                                      {   'definition': 'Costly context-switch between HANA SQL Engine and Calculation '
                                                        'Engine during query execution.',
                                          'term': 'Engine Hop'}],
                     'step_id': 'd45_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Secondary indexes and memory paging remain foundational to HANA performance; PlanViz '
                                 'provides the authoritative ground truth for execution efficiency.',
                     'title': 'Code Pushdown, PlanViz & Technical Truthfulness'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'plants': ['PL01', 'PL02'],
                                            'pushed_result_rows': 4,
                                            'rows_scanned': 150000,
                                            'runtime_reduction': '380ms -> 8.2ms',
                                            'table_analyzed': 'ACDOCA'},
                     'content_md': '### Execution Comparison: Un-Pushed Loop vs Column Pushdown\n'
                                   '1. **Un-Pushed Legacy Execution**:\n'
                                   '   - `TABLE SCAN (ACDOCA)`: 150,000 rows read into row buffer.\n'
                                   '   - Network payload: 86.4 MB transmitted across network interface.\n'
                                   '   - ABAP Application Server: Looped over 150,000 internal table records to '
                                   'aggregate margins. Runtime: 380 ms.\n'
                                   '2. **Optimized CDS Pushdown Execution**:\n'
                                   '   - `INVERTED INDEX RANGE SCAN`: Pruned partitions outside Company Code NM01 and '
                                   'Fiscal Period 009.\n'
                                   '   - `COLUMN SEARCH (Aggregation Pushdown)`: Grouped by Product Hierarchy and '
                                   'Plant directly in column vectors.\n'
                                   '   - Result payload: Only 4 aggregated rows transmitted across network interface. '
                                   'Runtime: 8.2 ms (46x speedup).',
                     'scenario': "Nova's BI team runs month-end product line profitability for Heidelberg (PL01). An "
                                 'un-pushed ABAP loop fetched 150,000 raw ACDOCA line items into application memory. '
                                 'Switching to an in-database CDS View Entity eliminated 86 MB of memory '
                                 'materialization.',
                     'step_id': 'd45_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Month-End PlanViz Audit: Heidelberg (PL01)'},
                 {   'component_type': 'PlanVizSimulator',
                     'instruction': 'Toggle between Optimized Pushdown and Un-Pushed ABAP Loop. Inspect operator '
                                    'inclusive time, memory consumption, and network transfer rows.',
                     'step_id': 'd45_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Pushing aggregations into the HANA column engine eliminates network payload and '
                                 'memory materialization.',
                     'title': '[SIMULATION MODEL] PlanViz Execution & Pushdown Simulator'},
                 {   'instruction': 'Select the correct technical refutation based on real SAP HANA architecture.',
                     'options': [   {   'explanation': 'Correct! Secondary indexes are critical in column store for '
                                                       'selective queries, and data aggregation must be pushed down to '
                                                       'the database tier.',
                                        'id': 'opt_d45_correct',
                                        'is_correct': True,
                                        'text': 'Reject both assertions. HANA uses secondary inverted indexes to '
                                                'accelerate point lookups and partition pruning, and performing data '
                                                'aggregation in ABAP loops defeats in-memory SIMD pushdown, creating '
                                                'network and memory bottlenecks.'},
                                    {   'explanation': 'Incorrect. Bypassing database optimization creates severe '
                                                       'performance degradation.',
                                        'id': 'opt_d45_err1',
                                        'is_correct': False,
                                        'text': 'Accept the suggestion because HANA in-memory databases eliminate the '
                                                'need for all database-tier optimization.'},
                                    {   'explanation': 'Incorrect. HANA is an in-memory database utilizing persistent '
                                                       'data volumes and redo logs for durability.',
                                        'id': 'opt_d45_err2',
                                        'is_correct': False,
                                        'text': 'Reject because HANA only runs on mechanical spinning hard disk '
                                                'drives.'}],
                     'scenario': 'During a technical architecture review for Nova Manufacturing, a developer suggests: '
                                 "'Since SAP HANA stores everything in RAM and needs no indexes, we should remove all "
                                 'secondary indexes from custom Z-tables and perform all data formatting in ABAP '
                                 "loops.' How do you respond?",
                     'step_id': 'd45_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'HANA Architecture Truthfulness Challenge'},
                 {   'questions': [   {   'concept_slug': 'delta-merge-architecture',
                                          'explanation': 'Delta store absorbs fast transactional writes, which are '
                                                         'periodically merged into compressed Main store.',
                                          'id': 'd45_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'To allow fast write operations in the Delta '
                                                                     'buffer without immediately re-compressing the '
                                                                     'large, read-optimized Main column dictionaries.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'To store confidential user passwords in Delta '
                                                                     'and public data in Main.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'To ensure row-store tables can be converted into '
                                                                     'Microsoft Excel files.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'To avoid writing any changes to non-volatile '
                                                                     'disk persistence.'}],
                                          'prompt': 'In SAP HANA Column Store architecture, what is the primary '
                                                    'purpose of separating data into Main Storage and Delta Storage?',
                                          'question_id': 'd45_q1'},
                                      {   'concept_slug': 'sql-optimizer-pushdown',
                                          'explanation': 'Un-pushed queries fetch massive raw record sets across the '
                                                         'network rather than aggregating in-engine.',
                                          'id': 'd45_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Massive row materialization and table scans '
                                                                     'transferring thousands of un-aggregated rows to '
                                                                     'the application server.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Sub-second execution times in the Column Store '
                                                                     'engine.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Inverted index pruning evaluating point filters '
                                                                     'directly in memory.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Zero network traffic between the database and '
                                                                     'application tier.'}],
                                          'prompt': 'When analyzing a slow query in SAP HANA Plan Visualizer '
                                                    '(PlanViz), which symptom indicates an architectural lack of code '
                                                    'pushdown?',
                                          'question_id': 'd45_q2'}],
                     'step_id': 'd45_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 45 Mastery Assessment: HANA Engine Internals'},
                 {   'step_id': 'd45_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Interpreted HANA Indexserver memory structures (Main Store vs Delta Store, Delta '
                                   'Merge).\n'
                                   '- Evaluated PlanViz execution trees, distinguishing pushdown aggregation from '
                                   'application-tier loops.\n'
                                   '- Refuted common HANA misconceptions regarding secondary inverted indexes and '
                                   'memory paging.',
                     'title': 'Mastery Verification: HANA Engine Internals'},
                 {   'recommended_mission': {   'description': 'Diagnose an indexserver memory exhaustion alert during '
                                                               'month-end profitability reporting and optimize '
                                                               'pushdown in PlanViz.',
                                                'slug': 'nova-hana-performance-incident',
                                                'title': 'HANA Indexserver Performance & Pushdown Incident'},
                     'step_id': 'd45_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered the physical and operational architecture of the SAP HANA '
                                   'Indexserver. Next, you will explore how the Virtual Data Model (VDM) structures '
                                   'enterprise CDS entities.',
                     'title': 'Day 45 Complete: HANA Internals Mastered'}],
    'subtitle': 'Indexserver, columnar main/delta store, delta merge, secondary inverted indexes, and PlanViz pushdown '
                'analysis',
    'title': 'HANA Engine Architecture & Internals'},
    46: {   'atomic_concepts': ['vdm-architecture-tiers', 'interface-vs-consumption-views'],
    'day_number': 46,
    'estimated_minutes': 75,
    'recommended_mission_slug': 'nova-vdm-architecture-request',
    'slug': 'vdm-architecture',
    'steps': [   {   'content_md': '### Enterprise Virtual Data Model (VDM) Foundations\n'
                                   'The **SAP Virtual Data Model (VDM)** is the authoritative architectural framework '
                                   'structuring all Core Data Services (CDS) view entities in SAP S/4HANA.\n'
                                   '\n'
                                   'The official VDM architecture establishes three strictly governed tiers defined by '
                                   'the `@VDM.viewType` annotation:\n'
                                   '1. **BASIC (`@VDM.viewType: #BASIC`)**:\n'
                                   '   - 1-to-1 projection on transparent database tables (`MARA`, `T001W`, `KNA1`, '
                                   '`ACDOCA`).\n'
                                   '   - Cleanses and standardizes technical field names into clear business semantics '
                                   '(e.g. `WERKS` -> `Plant`). Zero joins or business logic.\n'
                                   '2. **COMPOSITE (`@VDM.viewType: #COMPOSITE`)**:\n'
                                   '   - Combines multiple views via associations and joins to model core enterprise '
                                   'business entities (e.g. Sales Order with Items and Plant).\n'
                                   '   - Agnostic to UI frameworks; acts as the reusable building block for '
                                   'transactional applications and analytical fact cubes.\n'
                                   '3. **CONSUMPTION (`@VDM.viewType: #CONSUMPTION`)**:\n'
                                   '   - Top-level entities tailored specifically for application screens, analytical '
                                   'KPI queries, or OData services.\n'
                                   '   - **Crucial Invariant**: Consumption views are strictly endpoints and are NEVER '
                                   'referenced by other CDS views.\n'
                                   '\n'
                                   '### Dispelling the Prefix Myth\n'
                                   '> **IMPORTANT ARCHITECTURAL RULE**:\n'
                                   '> Naming prefixes (`I_`, `R_`, `C_`) are standard SAP conventions, but the view '
                                   'type derives from **actual semantics and annotations (`@VDM.viewType`)**:\n'
                                   '> - `I_` does NOT always equal Basic! Many foundational composite views also use '
                                   '`I_` (e.g., `I_SalesOrderItem` is Basic, but `I_SalesOrderWithItemsCube` is '
                                   'Composite).\n'
                                   '> - `R_` does NOT always equal Composite (`R_` is a reuse view convention).\n'
                                   '> - `C_` does NOT automatically make a view Consumption without `@VDM.viewType: '
                                   '#CONSUMPTION`.\n'
                                   '> Always verify the `@VDM.viewType` annotation rather than relying solely on the '
                                   'prefix.',
                     'key_terms': [   {   'definition': 'Authoritative multi-tier semantic data architecture defined '
                                                        'by @VDM.viewType: #BASIC, #COMPOSITE, and #CONSUMPTION.',
                                          'term': 'Virtual Data Model (VDM)'},
                                      {   'definition': 'Foundational CDS view projecting a single database table with '
                                                        'standardized business terminology.',
                                          'term': 'Basic View (#BASIC)'},
                                      {   'definition': 'Core enterprise business entity view combining basic views '
                                                        'with associations, joins, or aggregations.',
                                          'term': 'Composite View (#COMPOSITE)'},
                                      {   'definition': 'Top-tier CDS view designed specifically for an application UI '
                                                        'or analytical query; never referenced by other views.',
                                          'term': 'Consumption View (#CONSUMPTION)'}],
                     'step_id': 'd46_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Official VDM tiers are BASIC, COMPOSITE, and CONSUMPTION; view types derive from '
                                 '@VDM.viewType annotations rather than prefixes alone.',
                     'title': 'The SAP Virtual Data Model (VDM) Architecture'},
                 {   'content_md': '### Separating VDM Layering from API Release Contracts\n'
                                   'A common misconception is confusing VDM tiers with SAP API release contracts. They '
                                   'serve two entirely different purposes:\n'
                                   '- **VDM Layering (`BASIC`, `COMPOSITE`, `CONSUMPTION`)**: Governs semantic '
                                   'modeling, reusability, and data dependencies.\n'
                                   '- **API Release Contracts (`C1`, `C2`)**: Orthogonal governance classifications '
                                   'for public APIs ensuring upgrade stability in SAP Clean Core.\n'
                                   '\n'
                                   '### SAP API Release Contracts\n'
                                   'Custom side-by-side or on-stack developer extensions in Clean Core must only '
                                   'consume CDS views released under formal release contracts:\n'
                                   '- **Contract C1 (Use System-Internally)**: Guarantees that SAP will not introduce '
                                   'breaking changes (removed fields, altered technical types) to the view entity '
                                   'across release upgrades for custom ABAP development.\n'
                                   '- **Contract C2 (Use as Remote API)**: Released for remote consumption outside the '
                                   'core stack via OData, REST APIs, or SAP BTP.\n'
                                   '\n'
                                   '> **CRITICAL RULE**: Do NOT describe C1 or C2 as VDM tiers! VDM tiers are BASIC, '
                                   'COMPOSITE, and CONSUMPTION. C1 and C2 are API release governance contracts.\n'
                                   '\n'
                                   '### The Prohibition Against Direct Table Access\n'
                                   'Why is creating custom queries directly against transparent tables like `ACDOCA` '
                                   'or `MATDOC` forbidden in Clean Core?\n'
                                   '- Underlying physical table structures, internal lock engines, and partition '
                                   'layouts can evolve between SAP versions.\n'
                                   '- Released VDM Interface Views (`I_JournalEntryItem`, `I_MaterialDocumentItem`) '
                                   'provide a permanent, stable semantic abstraction layer protected by Contract C1, '
                                   'insulating custom code from database schema evolution.',
                     'key_terms': [   {   'definition': 'API release contract guaranteeing stability across upgrades '
                                                        'for system-internal ABAP consumption.',
                                          'term': 'Contract C1 (Use System-Internally)'},
                                      {   'definition': 'API release contract releasing a CDS entity or service for '
                                                        'remote consumption outside the core system.',
                                          'term': 'Contract C2 (Use as Remote API)'},
                                      {   'definition': 'Implementation methodology decoupling custom extensions from '
                                                        'core ERP code to ensure seamless continuous upgrades.',
                                          'term': 'Clean Core'}],
                     'step_id': 'd46_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'C1 (Use System-Internally) and C2 (Use as Remote API) are API release contracts, NOT '
                                 'VDM tiers; VDM tiers are BASIC, COMPOSITE, and CONSUMPTION.',
                     'title': 'API Release Contracts (C1, C2) vs VDM Layering'},
                 {   'company_context': {   'basic_views': [   'I_Plant',
                                                               'I_Product',
                                                               'I_SalesOrderItem',
                                                               'I_PurchaseOrderItem'],
                                            'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'composite_view': 'I_SalesOrderWithItemsCube',
                                            'consumption_view': 'C_RoboticsSalesMarginQuery',
                                            'customer': 'CUST-501',
                                            'materials': ['RAW-01', 'DXTR-1000'],
                                            'plants': ['PL01', 'PL02'],
                                            'purchasing_org': 'PO01',
                                            'sales_org': 'SO01',
                                            'storage_locations': ['RAW1', 'FG01'],
                                            'vendor': 'VEND-101'},
                     'content_md': '### VDM Lineage Architecture\n'
                                   '1. **Tier 1 (Basic)**:\n'
                                   '   - `I_Plant` selects from `T001W` (`werks` as `Plant`) covering Heidelberg '
                                   '(`PL01`) and Austin (`PL02`).\n'
                                   '   - `I_Product` selects from `MARA` (`matnr` as `Product`) modeling `RAW-01` and '
                                   '`DXTR-1000`.\n'
                                   '   - `I_PurchaseOrderItem` models inbound procurement for Purchasing Org `PO01` '
                                   'from supplier `VEND-101` into Storage Location `RAW1`.\n'
                                   '2. **Tier 2 (Composite Cube)**:\n'
                                   '   - `I_SalesOrderWithItemsCube` selects from `I_SalesOrderItem` under Sales Org '
                                   '`SO01` fulfilled from Storage Location `FG01` for customer `CUST-501`. Defines '
                                   'associations to `I_Plant` and `I_Product`. Aggregates measures with '
                                   '`@Aggregation.default: #SUM`.\n'
                                   '3. **Tier 3 (Consumption Query)**:\n'
                                   '   - `C_RoboticsSalesMarginQuery` projects dimensions (`Plant`, `Product`, '
                                   '`StorageLocation`) on `#ROWS` and measures (`NetAmount`) on `#COLUMNS` with '
                                   '`@Analytics.query: true`.',
                     'scenario': "Nova's development team designs an analytical margin model for Robotics Controller "
                                 'DXTR-1000 across plants PL01 and PL02. They organize the solution into three Clean '
                                 'Core VDM layers connecting procurement (PO01, VEND-101, RAW1) and sales distribution '
                                 '(SO01, CUST-501, FG01).',
                     'step_id': 'd46_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Robotics Inventory VDM: Heidelberg & Austin'},
                 {   'component_type': 'VDMBuilder',
                     'instruction': 'Filter views by tier (Basic, Composite, Consumption). Inspect the DDL source '
                                    'code, stability contracts, and Clean Core governance rules.',
                     'step_id': 'd46_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Each VDM tier serves a specific purpose: Basic wraps tables, Composite models '
                                 'business entities, and Consumption serves UI apps.',
                     'title': '[SIMULATION MODEL] VDM Architecture & Layering Studio'},
                 {   'instruction': 'Select the correct architectural verdict.',
                     'options': [   {   'explanation': 'Correct! Reusing consumption views creates tight UI coupling '
                                                       'and violates VDM layering rules.',
                                        'id': 'opt_d46_correct',
                                        'is_correct': True,
                                        'text': 'Reject the request. Consumption Views (C_) represent final UI '
                                                'endpoints and must NEVER be referenced by other CDS views; the second '
                                                'team must consume the underlying Composite View (I_).'},
                                    {   'explanation': 'Incorrect. Violates S/4HANA VDM layering principles.',
                                        'id': 'opt_d46_err1',
                                        'is_correct': False,
                                        'text': 'Approve the request because referencing any CDS view from any other '
                                                'CDS view is considered best practice.'},
                                    {   'explanation': 'Incorrect. Bypassing CDS violates Clean Core guidelines.',
                                        'id': 'opt_d46_err2',
                                        'is_correct': False,
                                        'text': 'Tell both teams to bypass CDS entirely and write native SQL against '
                                                'transparent table VBAK.'}],
                     'scenario': 'A development team created Consumption View `C_RoboticsSalesMarginQuery` for a Fiori '
                                 'KPI card. A second team building an automated logistics dispatch workflow wants to '
                                 'use `C_RoboticsSalesMarginQuery` as a data source. How should the enterprise '
                                 'architect rule?',
                     'step_id': 'd46_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'VDM Consumption Reusability Challenge'},
                 {   'questions': [   {   'concept_slug': 'vdm-architecture-tiers',
                                          'explanation': 'Basic Interface Views (I_) wrap transparent tables and '
                                                         'provide stable building blocks.',
                                          'id': 'd46_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Basic / Interface Views (prefixed with I_)'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Consumption Views (prefixed with C_)'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Analytical Query Views'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Classical ABAP Database Views'}],
                                          'prompt': 'In the SAP S/4HANA Virtual Data Model (VDM), which view tier is '
                                                    'directly mapped 1-to-1 against raw database tables and released '
                                                    'under stability contract C1?',
                                          'question_id': 'd46_q1'},
                                      {   'concept_slug': 'interface-vs-consumption-views',
                                          'explanation': 'Consumption views are top-level endpoints tailored for '
                                                         'UI/queries and must not become dependencies for other '
                                                         'models.',
                                          'id': 'd46_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Because Consumption views contain '
                                                                     'application-specific projections and UI metadata '
                                                                     'that lack stability guarantees for downstream '
                                                                     'core data modeling.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Because HANA does not allow more than one CDS '
                                                                     'view in a database instance.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Because Consumption views can only be compiled '
                                                                     'in the ABAP development client 000.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Because Consumption views are permanently '
                                                                     'deleted after each user session terminates.'}],
                                          'prompt': 'Why are Consumption Views (C_) prohibited from being referenced '
                                                    'as data sources by other CDS views?',
                                          'question_id': 'd46_q2'}],
                     'step_id': 'd46_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 46 Mastery Assessment: VDM Architecture'},
                 {   'step_id': 'd46_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Structured enterprise CDS entities into Basic (`I_`), Composite (`R_`/`I_`), and '
                                   'Consumption (`C_`) tiers.\n'
                                   '- Enforced SAP Clean Core stability contracts (Contract C1) and prohibited direct '
                                   'raw table querying.\n'
                                   '- Validated that Consumption views remain isolated architectural endpoints.',
                     'title': 'Mastery Verification: VDM Architecture'},
                 {   'recommended_mission': {   'description': 'Architect a multi-tier Virtual Data Model decoupling '
                                                               'custom apps from raw tables via released Interface '
                                                               'Views.',
                                                'slug': 'nova-vdm-architecture-request',
                                                'title': 'Nova VDM Architecture & Clean Core Extensibility'},
                     'step_id': 'd46_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered the architectural principles of the SAP Virtual Data Model. '
                                   'Next, you will master advanced CDS syntax, expressions, and in-database CASE '
                                   'logic.',
                     'title': 'Day 46 Complete: VDM Architecture Mastered'}],
    'subtitle': 'Basic views (I_), composite views (R_/I_), consumption views (C_), Clean Core stability contracts, '
                'and layering rules',
    'title': 'Virtual Data Model (VDM) Architecture'},
    47: {   'atomic_concepts': ['cds-advanced-expressions', 'cds-case-statements'],
    'day_number': 47,
    'estimated_minutes': 75,
    'recommended_mission_slug': 'nova-parameterized-reporting-service',
    'slug': 'cds-syntax-expressions',
    'steps': [   {   'content_md': '### The Modern ABAP CDS View Entity\n'
                                   'In modern S/4HANA (since SAP release 2020), **`DEFINE VIEW ENTITY`** is the '
                                   'standard for defining CDS views, completely replacing legacy DDIC-based views '
                                   '(`DEFINE VIEW`):\n'
                                   '- Eliminates dual-generation overhead (no classical SQL DDIC view in `SE11`).\n'
                                   '- Provides stricter syntax checks, better buffer synchronization, and native '
                                   'execution in the HANA SQL engine.\n'
                                   '\n'
                                   '### Built-in Scalar Expressions & Functions\n'
                                   'CDS View Entities execute rich arithmetic and string expressions directly in the '
                                   'database kernel:\n'
                                   "1. **String Manipulation**: `concat(FirstName, concat(' ', LastName))`, "
                                   '`substring(Material, 1, 4)`, `length(PostalCode)`.\n'
                                   '2. **Arithmetic & Coalesce**: `coalesce(DiscountRate, 0.00)` protects mathematical '
                                   'calculations from propagating `NULL` values.\n'
                                   '3. **Unit & Currency Conversions**:\n'
                                   '   - `currency_conversion(amount => NetAmount, source_currency => Currency, '
                                   "target_currency => 'USD', exchange_rate_date => $session.system_date)`\n"
                                   '   - Performs standard S/4HANA currency translation in the database using exchange '
                                   'rate table `TCURR`.',
                     'key_terms': [   {   'definition': 'Modern ABAP CDS artifact (define view entity) compiled '
                                                        'directly into HANA without classical SE11 DDIC views.',
                                          'term': 'CDS View Entity'},
                                      {   'definition': 'Built-in function returning the first non-null argument, '
                                                        'essential for protecting calculated fields from null poison.',
                                          'term': 'Coalesce'},
                                      {   'definition': 'HANA kernel function calculating foreign exchange conversions '
                                                        'referencing table TCURR in-database.',
                                          'term': 'Currency Conversion Pushdown'}],
                     'step_id': 'd47_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'CDS View Entities replace legacy DDIC views and execute complex string, arithmetic, '
                                 'and conversion functions directly in the database tier.',
                     'title': 'CDS View Entity Syntax & Modern Expressions'},
                 {   'content_md': '### The CDS CASE Expression\n'
                                   'CDS View Entities support declarative conditional classification through the '
                                   '`CASE` statement:\n'
                                   '\n'
                                   '```sql\n'
                                   'case\n'
                                   "  when DaysOpen > 30 then 'CRITICAL_OVERDUE'\n"
                                   "  when DaysOpen > 14 then 'IN_REVIEW'\n"
                                   "  else 'ON_TRACK'\n"
                                   'end as FulfillmentUrgency\n'
                                   '```\n'
                                   '\n'
                                   '### Architectural Execution Properties\n'
                                   '1. **Pure Columnar Evaluation**: During execution, the HANA SQL optimizer '
                                   'evaluates `CASE` expressions using parallel vector scans across column '
                                   'bit-vectors, avoiding procedural row-by-row looping.\n'
                                   '2. **Type Uniformity**: All `THEN` and `ELSE` branches must yield compatible data '
                                   'types and lengths; mismatched literals produce compiler errors.\n'
                                   '3. **Default Handling**: If the `ELSE` branch is omitted and no `WHEN` condition '
                                   'matches, the result evaluates to `NULL`. Always specify an explicit `ELSE` '
                                   'fallback.',
                     'key_terms': [   {   'definition': 'Declarative conditional operator in CDS evaluating conditions '
                                                        'sequentially and returning a typed result value.',
                                          'term': 'CASE Expression'}],
                     'step_id': 'd47_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'CASE expressions classify data directly within in-memory columnar scans with zero '
                                 'application-server procedural overhead.',
                     'title': 'Conditional CASE Expressions in In-Memory Processing'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'currency': 'EUR',
                                            'orders_evaluated': ['100045', '100046', '100047'],
                                            'target_currency': 'USD'},
                     'content_md': '### In-Database Calculation Results\n'
                                   '1. **Order #100045 (18 days open)**: Evaluates `WHEN DaysOpen > 14` $\to$ Marked '
                                   "`'IN_REVIEW'`. Discount rate coalesced to `0.05`.\n"
                                   '2. **Order #100046 (42 days open)**: Evaluates `WHEN DaysOpen > 30` $\to$ Marked '
                                   "`'CRITICAL_OVERDUE'`. Discount rate coalesced from `NULL` to `0.00`.\n"
                                   "3. **Order #100047 (5 days open)**: Evaluates `ELSE` $\to$ Marked `'ON_TRACK'`.",
                     'scenario': "Nova's sales operations team at Heidelberg (PL01) needs to classify customer sales "
                                 'orders into priority fulfillment buckets based on aging days open.',
                     'step_id': 'd47_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Order Urgency Classification'},
                 {   'component_type': 'CDSExpressionLab',
                     'instruction': 'Adjust the urgency threshold slider and switch target currencies. Observe the '
                                    'live evaluated output table.',
                     'step_id': 'd47_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Conditional CASE statements and currency conversions execute in-engine before '
                                 'transmitting data to the client.',
                     'title': '[SIMULATION MODEL] CDS Expression & CASE Logic Workbench'},
                 {   'instruction': 'Select the correct CDS expression to guarantee mathematical null safety.',
                     'options': [   {   'explanation': 'Correct! coalesce ensures that NULL values are converted to '
                                                       '0.00, preventing null propagation.',
                                        'id': 'opt_d47_correct',
                                        'is_correct': True,
                                        'text': 'GrossAmount - coalesce(DiscountAmount, 0.00) as NetAmount'},
                                    {   'explanation': 'Incorrect. In SQL, adding zero to NULL still results in NULL.',
                                        'id': 'opt_d47_err1',
                                        'is_correct': False,
                                        'text': 'GrossAmount - DiscountAmount + 0 as NetAmount'},
                                    {   'explanation': 'Incorrect.',
                                        'id': 'opt_d47_err2',
                                        'is_correct': False,
                                        'text': 'Convert the entire table to Microsoft Word documents.'}],
                     'scenario': 'A junior developer writes a CDS calculation: `GrossAmount - DiscountAmount as '
                                 'NetAmount`. In production, when `DiscountAmount` is NULL, `NetAmount` evaluates to '
                                 'NULL, causing total invoice values to disappear from financial reports. What is the '
                                 'correct fix?',
                     'step_id': 'd47_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'CDS Null-Safety & Expression Challenge'},
                 {   'questions': [   {   'concept_slug': 'cds-case-statements',
                                          'explanation': 'HANA executes CASE expressions using parallel SIMD column '
                                                         'scans directly in the database engine.',
                                          'id': 'd47_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Using parallel columnar bit-vector evaluations '
                                                                     'directly in the in-memory database tier without '
                                                                     'row-by-row procedural looping.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'By downloading all rows to the browser and '
                                                                     'running JavaScript switch statements.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'By writing temporary text files to the operating '
                                                                     'system file system.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'By requesting manual approval from the database '
                                                                     'administrator.'}],
                                          'prompt': 'In an ABAP CDS View Entity, how does the SAP HANA engine '
                                                    'physically execute a CASE expression across thousands of records?',
                                          'question_id': 'd47_q1'},
                                      {   'concept_slug': 'cds-advanced-expressions',
                                          'explanation': 'currency_conversion executes in-database foreign exchange '
                                                         'translations.',
                                          'id': 'd47_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'currency_conversion(...)'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'unit_conversion(...)'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'cast_to_currency(...)'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'convert_to_fiat(...)'}],
                                          'prompt': 'Which built-in CDS function is used to convert monetary values '
                                                    'into a target currency using authoritative exchange rates stored '
                                                    'in table TCURR?',
                                          'question_id': 'd47_q2'}],
                     'step_id': 'd47_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 47 Mastery Assessment: CDS Expressions & CASE'},
                 {   'step_id': 'd47_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Authored modern CDS View Entity (`define view entity`) syntax with zero legacy '
                                   'DDIC artifacts.\n'
                                   '- Implemented declarative conditional `CASE` statements with explicit fallback '
                                   'logic.\n'
                                   '- Applied `coalesce` and in-database `currency_conversion` functions for robust '
                                   'financial computing.',
                     'title': 'Mastery Verification: CDS Expressions & CASE'},
                 {   'recommended_mission': {   'description': 'Develop a parameterized CDS view entity supporting '
                                                               'dynamic currency translation and key-date valuation.',
                                                'slug': 'nova-parameterized-reporting-service',
                                                'title': 'Multi-Currency Parameterized Reporting Service'},
                     'step_id': 'd47_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered advanced expressions and conditional logic in CDS View Entities. '
                                   'Next, you will explore the critical architectural differences between CDS '
                                   'Associations and SQL Joins.',
                     'title': 'Day 47 Complete: CDS Expressions Mastered'}],
    'subtitle': 'Modern CDS view entities, conditional CASE statements, coalesce null-safety, and currency conversion '
                'pushdown',
    'title': 'CDS Syntax, Expressions & Case Statements'},
    48: {   'atomic_concepts': ['cds-associations-concept', 'cardinality-rules', 'path-expressions'],
    'day_number': 48,
    'estimated_minutes': 90,
    'recommended_mission_slug': 'nova-association-cardinality-defect',
    'slug': 'cds-associations-vs-joins',
    'steps': [   {   'content_md': '### Understanding CDS Associations vs SQL Joins\n'
                                   'In relational database systems, a standard SQL `LEFT OUTER JOIN` binds tables '
                                   'eagerly: every table in the join clause is evaluated by the database optimizer.\n'
                                   '\n'
                                   'An **ABAP CDS Association** fundamentally differs by providing **reusable '
                                   'navigation semantics**:\n'
                                   '1. **Navigation Semantics Without Immediate Joining**:\n'
                                   '   - Declaring an association (`association [1..1] to I_Customer as _Customer`) '
                                   'defines the relationship metadata and ON-condition, but declaring an association '
                                   'does NOT itself mean every target is joined.\n'
                                   '2. **Join Instantiation via Path Expressions**:\n'
                                   '   - Only when a consumer query accesses target fields through a **path '
                                   'expression** (e.g. `_Customer.Country`) is a physical SQL join instantiated in the '
                                   'execution plan.\n'
                                   '3. **Automatic Join Pruning**:\n'
                                   '   - If a query requests only fields from the root entity, the unreferenced '
                                   'association is pruned, sparing database memory reads.\n'
                                   '4. **Associations Are NOT Automatically Faster Than Joins**:\n'
                                   '   - Associations are NOT automatically faster or superior to joins! When path '
                                   'expressions are traversed, real database joins are executed. If path expressions '
                                   'traverse deep association chains or involve unindexed cardinalities, performance '
                                   'requires the same careful indexing and PlanViz profiling as classical joins.',
                     'key_terms': [   {   'definition': 'Reusable navigation relationship defining target metadata; '
                                                        'does not execute a join until consumed via path expression.',
                                          'term': 'CDS Association'},
                                      {   'definition': 'Syntax navigating an association (e.g. _Customer.Country) '
                                                        'that instantiates a database join on-demand.',
                                          'term': 'Path Expression'},
                                      {   'definition': 'Optimizer behavior omitting unreferenced associated tables '
                                                        'from the physical SQL execution plan.',
                                          'term': 'Join Pruning'}],
                     'step_id': 'd48_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Declaring an association defines reusable navigation without joining; path '
                                 'expressions instantiate joins on-demand. Associations are not automatically faster '
                                 'than joins.',
                     'title': 'CDS Associations vs Classical SQL Joins'},
                 {   'content_md': '### Explicit Cardinality Declarations in CDS\n'
                                   'Every association must declare an explicit cardinality specifying the min..max '
                                   'occurrences of matching target records:\n'
                                   '- `[1..1]`: Exactly one matching target record (e.g. Sales Order $\to$ Sold-To '
                                   'Customer).\n'
                                   '- `[0..1]`: Zero or one matching target record (e.g. Sales Order Item $\to$ '
                                   'Outbound Delivery Item before shipping).\n'
                                   '- `[1..*]`: At least one matching target record (e.g. Sales Order $\to$ Sales '
                                   'Order Items).\n'
                                   '- `[0..*]`: Zero, one, or multiple matching target records.\n'
                                   '\n'
                                   '### The Cardinality Defect Trap\n'
                                   '> **ARCHITECTURAL WARNING**: Declaring `[1..1]` when the underlying data is '
                                   'actually `[1..*]` causes catastrophic financial reporting errors!\n'
                                   '>\n'
                                   '> If a developer declares `[1..1]` on an association to delivery items, but an '
                                   'order item was split into multiple deliveries, the query produces duplicate rows '
                                   'for the parent order item. In an un-aggregated query, total revenue is multiplied! '
                                   'Always verify business data cardinality before declaring `[1..1]`.',
                     'key_terms': [   {   'definition': 'Declaration of minimum and maximum relationship multiplicity '
                                                        '([min..max]) guiding the SQL optimizer.',
                                          'term': 'Cardinality'},
                                      {   'definition': 'Erroneous numerical inflation caused by declaring [1..1] on '
                                                        'one-to-many business relationships.',
                                          'term': 'Multi-Count Trap'}],
                     'step_id': 'd48_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Accurate cardinality declarations are mandatory; misdeclaring [1..1] on one-to-many '
                                 'relationships causes duplicate row inflation.',
                     'title': 'Cardinality Rules & The Multi-Count Aggregation Trap'},
                 {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                            'customer': 'CUST-501',
                                            'deliveries': ['800021 (PL01)', '800022 (PL02)'],
                                            'net_amount': '€45,000',
                                            'sales_order': '100045'},
                     'content_md': '### Execution Analysis\n'
                                   '1. **Query 1 (Root Fields Only)**: `SELECT SalesOrder, NetAmount FROM '
                                   'I_SalesOrder`.\n'
                                   '   - HANA generated SQL: Reads only table `VBAK`. Zero joins to `KNA1` or `LIPS`.\n'
                                   '2. **Query 2 (With Path Expression)**: `SELECT SalesOrder, NetAmount, '
                                   '_Customer.Country FROM I_SalesOrder`.\n'
                                   '   - HANA generated SQL: Injects `LEFT OUTER MANY TO ONE JOIN KNA1` on demand.',
                     'scenario': 'Sales order #100045 for customer CUST-501 (€45,000) defines associations to '
                                 '_Customer [1..1] and _DeliveryItems [0..*].',
                     'step_id': 'd48_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Sales Order Association: CUST-501'},
                 {   'component_type': 'AssociationCardinalityMapper',
                     'instruction': 'Toggle Path Expression Traversal to inspect the runtime generated HANA SQL '
                                    'statement. Compare [1..1] vs [0..*] cardinalities.',
                     'step_id': 'd48_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Path expressions dynamically trigger SQL joins; unaccessed associations are pruned '
                                 'from the execution plan.',
                     'title': '[SIMULATION MODEL] Association vs Join & Cardinality Workbench'},
                 {   'instruction': 'Identify the root architectural defect.',
                     'options': [   {   'explanation': 'Correct! [1..1] tells the optimizer to treat the relationship '
                                                       'as single-valued, which duplicates header lines when multiple '
                                                       'deliveries exist.',
                                        'id': 'opt_d48_correct',
                                        'is_correct': True,
                                        'text': 'The developer declared cardinality [1..1] on the delivery '
                                                'association, but the order had two delivery lines. Joining the '
                                                'delivery items without aggregation duplicated the sales order header '
                                                'row.'},
                                    {   'explanation': 'Incorrect. Delta merge does not alter relationship '
                                                       'multiplicity.',
                                        'id': 'opt_d48_err1',
                                        'is_correct': False,
                                        'text': 'The HANA in-memory delta merge failed to execute.'},
                                    {   'explanation': 'Incorrect.',
                                        'id': 'opt_d48_err2',
                                        'is_correct': False,
                                        'text': 'The customer ordered two different companies.'}],
                     'scenario': 'An analytical billing report displays customer revenue as €90,000 for a sales order '
                                 'that was only billed for €45,000. Investigation shows the order was delivered in two '
                                 'separate shipments from Heidelberg and Austin. What caused the report defect?',
                     'step_id': 'd48_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Association Cardinality Defect Challenge'},
                 {   'questions': [   {   'concept_slug': 'cds-associations-concept',
                                          'explanation': 'Associations are join-on-demand, enabling the database '
                                                         'engine to prune unneeded joins.',
                                          'id': 'd48_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Associations are lazy and evaluated on-demand; '
                                                                     'if the query caller does not reference fields '
                                                                     'from the associated entity, the join is pruned '
                                                                     'from the physical execution plan.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Associations permanently delete the joined table '
                                                                     'to save disk space.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Associations force all queries to run in '
                                                                     'single-user mode.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Associations can only be created on Microsoft '
                                                                     'Access databases.'}],
                                          'prompt': 'What is the primary operational performance advantage of a CDS '
                                                    'Association over a classical SQL LEFT OUTER JOIN?',
                                          'question_id': 'd48_q1'},
                                      {   'concept_slug': 'cardinality-rules',
                                          'explanation': '0..1 correctly models that a newly created order item has '
                                                         'zero deliveries until shipping occurs.',
                                          'id': 'd48_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Because an order item that has just been placed '
                                                                     'has not yet been shipped, meaning an outbound '
                                                                     'delivery document does not yet exist.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Because delivery documents are not allowed to '
                                                                     'have item numbers.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Because SAP S/4HANA no longer uses outbound '
                                                                     'delivery documents.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Because [1..1] is prohibited on all logistics '
                                                                     'tables.'}],
                                          'prompt': 'In SAP CDS modeling, when linking a Sales Order Item to its '
                                                    'associated Outbound Delivery Document Item, why is [0..1] the '
                                                    'architecturally correct cardinality rather than [1..1]?',
                                          'question_id': 'd48_q2'}],
                     'step_id': 'd48_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 48 Mastery Assessment: Associations vs Joins'},
                 {   'step_id': 'd48_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Distinguished lazy join-on-demand CDS associations from eager SQL joins.\n'
                                   '- Demonstrated join pruning when path expressions are omitted from projection '
                                   'lists.\n'
                                   '- Enforced accurate cardinality rules ([1..1], [0..1], [1..*]), preventing '
                                   'duplicate row aggregation defects.',
                     'title': 'Mastery Verification: Associations vs Joins'},
                 {   'recommended_mission': {   'description': 'Diagnose and resolve an enterprise revenue multi-count '
                                                               'defect caused by an inaccurate association cardinality '
                                                               'declaration.',
                                                'slug': 'nova-association-cardinality-defect',
                                                'title': 'CDS Association Cardinality & Revenue Multi-Count Defect'},
                     'step_id': 'd48_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered CDS associations, path expressions, and cardinality modeling. '
                                   'Next, you will learn how to design parameterized CDS views and consume environment '
                                   'session variables.',
                     'title': 'Day 48 Complete: Associations Mastered'}],
    'subtitle': 'Lazy evaluation, join pruning, path expressions, and cardinality rules ([1..1], [0..1], [1..*])',
    'title': 'CDS Associations vs SQL Joins'},
    49: {   'atomic_concepts': ['cds-parameters', 'cds-session-variables'],
    'day_number': 49,
    'estimated_minutes': 75,
    'recommended_mission_slug': 'nova-parameterized-reporting-service',
    'slug': 'cds-parameters-session-vars',
    'steps': [   {   'content_md': '### Runtime Dynamic Inputs via CDS Parameters\n'
                                   'Standard CDS views provide static projection lists. However, enterprise financial '
                                   'and logistics calculations often depend on runtime inputs—such as a target '
                                   'currency for multi-GAAP reporting, a key evaluation date for inventory aging, or a '
                                   'simulation exchange rate.\n'
                                   '\n'
                                   'CDS View Entities support **typed input parameters**:\n'
                                   '```sql\n'
                                   'define view entity I_NovaSalesValuation\n'
                                   '  with parameters\n'
                                   '    p_target_curr : waers,\n'
                                   '    p_eval_date   : abap.dats\n'
                                   '  as select from I_SalesOrderItem as Item\n'
                                   '{\n'
                                   '  key Item.SalesOrder,\n'
                                   '  key Item.SalesOrderItem,\n'
                                   '      currency_conversion(\n'
                                   '        amount             => Item.NetAmount,\n'
                                   '        source_currency    => Item.Currency,\n'
                                   '        target_currency    => $parameters.p_target_curr,\n'
                                   '        exchange_rate_date => $parameters.p_eval_date\n'
                                   '      ) as ConvertedAmount\n'
                                   '}\n'
                                   '```\n'
                                   '\n'
                                   'Key Architectural Principles:\n'
                                   '1. **Strong Typing**: Parameters declare formal ABAP Dictionary data types (e.g. '
                                   '`waers` for currency codes, `abap.dats` for calendar dates).\n'
                                   '2. **Pushdown Binding**: Parameters are compiled directly into the underlying HANA '
                                   'database view definition, allowing the database engine to push parameter values '
                                   'into SIMD vector operations.',
                     'key_terms': [   {   'definition': 'Typed dynamic input variable passed to a CDS view entity at '
                                                        'execution time.',
                                          'term': 'CDS Parameter'},
                                      {   'definition': 'Standard ABAP Dictionary data element for 5-character '
                                                        'currency keys (e.g. EUR, USD).',
                                          'term': 'waers'},
                                      {   'definition': 'Built-in ABAP Dictionary calendar date type (YYYYMMDD).',
                                          'term': 'abap.dats'}],
                     'step_id': 'd49_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Typed parameters enable dynamic runtime calculations like currency translation to '
                                 'execute in-database.',
                     'title': 'Parameterized CDS Views in S/4HANA'},
                 {   'content_md': '### Built-in System Session Variables ($session)\n'
                                   'The ABAP CDS environment provides standardized **session variables** that inject '
                                   'runtime application context without requiring manual parameter passing:\n'
                                   "- **`$session.user`**: The current logon SAP user ID (e.g. `'NOVA_ARCHITECT'`).\n"
                                   "- **`$session.client`**: The active system client tenant (e.g. `'100'`).\n"
                                   '- **`$session.system_date`**: The current server date (`sy-datum`).\n'
                                   '- **`$session.system_language`**: The active logon language code (`sy-langu`).\n'
                                   '\n'
                                   '### Parameter Propagation Along Associations\n'
                                   'When a parameterized CDS view defines an association to another parameterized '
                                   'entity, parameters must be explicitly propagated across the relationship path:\n'
                                   '\n'
                                   '```sql\n'
                                   'association [1..1] to I_ProductValuation(\n'
                                   '  p_target_curr: $parameters.p_target_curr,\n'
                                   '  p_eval_date:   $parameters.p_eval_date\n'
                                   ') as _Valuation on $projection.Product = _Valuation.Product\n'
                                   '```\n'
                                   'If parameter binding is omitted along the path expression, the ABAP compiler '
                                   'rejects the view definition.',
                     'key_terms': [   {   'definition': 'System session variable exposing the authenticated user ID in '
                                                        'CDS.',
                                          'term': '$session.user'},
                                      {   'definition': 'Explicit binding of parameter values when traversing '
                                                        'associated parameterized CDS views.',
                                          'term': 'Parameter Propagation'}],
                     'step_id': 'd49_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Session variables provide automatic runtime context; parameterized associations '
                                 'require explicit parameter binding.',
                     'title': 'Session Variables ($session) & Parameter Propagation'},
                 {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                            'eval_date': '2026-09-25',
                                            'plants': ['PL01 (Heidelberg)', 'PL02 (Austin)'],
                                            'session_user': 'KLAUS_SCHMIDT',
                                            'target_currency': 'USD'},
                     'content_md': '### Parameterized Query Execution Trace\n'
                                   "1. **Parameter Binding**: User supplies `p_target_curr: 'USD'` and `p_eval_date: "
                                   "'20260925'`.\n"
                                   "2. **Session Injection**: System binds `$session.user` $\to$ `'KLAUS_SCHMIDT'`, "
                                   "`$session.client` $\to$ `'100'`.\n"
                                   '3. **Database Execution**:\n'
                                   '   - Heidelberg EUR line items (€45,000) converted to $48,600.00 using 2026-09-25 '
                                   'rate (1.08).\n'
                                   '   - Austin USD line items ($30,000) evaluate with identity conversion '
                                   '($30,000.00).\n'
                                   '   - Consolidated global inventory returned in uniform USD currency.',
                     'scenario': "Nova's corporate controller in Heidelberg evaluates cross-plant inventory for "
                                 'Robotics Controller DXTR-1000. Heidelberg books in EUR while Austin books in USD. '
                                 "The controller executes a parameterized query passing p_target_curr = 'USD' and "
                                 "p_eval_date = '20260925'.",
                     'step_id': 'd49_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Multi-Currency Valuation: PL01 & PL02'},
                 {   'component_type': 'CDSExpressionLab',
                     'instruction': 'Select target currency USD or GBP. Observe how input parameters alter in-database '
                                    'currency conversion results.',
                     'step_id': 'd49_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Parameters provide flexible dynamic inputs while keeping calculation pushdown '
                                 'entirely within the database tier.',
                     'title': '[SIMULATION MODEL] Parameterized View & Currency Workbench'},
                 {   'instruction': 'Select the correct compiler and architectural consequence.',
                     'options': [   {   'explanation': 'Correct! When an associated entity requires input parameters, '
                                                       'the path expression must explicitly pass parameter bindings.',
                                        'id': 'opt_d49_correct',
                                        'is_correct': True,
                                        'text': 'The ABAP compiler raises a syntax error because parameterized target '
                                                'views require explicit parameter binding along the association path: '
                                                '`_Valuation( p_key_date: $parameters.p_key_date ).StandardCost`.'},
                                    {   'explanation': 'Incorrect. Strongly typed compilers do not guess or generate '
                                                       'random parameters.',
                                        'id': 'opt_d49_err1',
                                        'is_correct': False,
                                        'text': 'The view compiles cleanly and automatically fills the missing '
                                                'parameter with a random number.'},
                                    {   'explanation': 'Incorrect.',
                                        'id': 'opt_d49_err2',
                                        'is_correct': False,
                                        'text': 'HANA database converts the parameter into an unencrypted network '
                                                'cookie.'}],
                     'scenario': 'A developer creates a parameterized CDS view `I_InventorySnapshot` with parameter '
                                 '`p_key_date`. The view references an associated view `I_MaterialValuation` that also '
                                 'requires an evaluation date. The developer leaves the association path expression as '
                                 '`_Valuation.StandardCost` without arguments. What happens when compiling the CDS '
                                 'view entity?',
                     'step_id': 'd49_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Session Variable & Propagation Challenge'},
                 {   'questions': [   {   'concept_slug': 'cds-parameters',
                                          'explanation': 'Parameters are declared using `with parameters` in the view '
                                                         'entity signature.',
                                          'id': 'd49_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Using the `with parameters` clause immediately '
                                                                     'preceding the `as select from` statement.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'By writing global JavaScript functions in the '
                                                                     'browser window.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Inside a separate text file located in the SAP '
                                                                     'GUI installation directory.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Inside classical SE38 executable programs '
                                                                     'only.'}],
                                          'prompt': 'In SAP CDS View Entity definition, how are dynamic input '
                                                    'parameters declared in the view header?',
                                          'question_id': 'd49_q1'},
                                      {   'concept_slug': 'cds-session-variables',
                                          'explanation': '$session.user returns the current logon user ID.',
                                          'id': 'd49_q2',
                                          'options': [   {'id': 'a', 'is_correct': True, 'text': '$session.user'},
                                                         {'id': 'b', 'is_correct': False, 'text': '$session.client'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': '$session.system_date'},
                                                         {'id': 'd', 'is_correct': False, 'text': '$session.password'}],
                                          'prompt': 'Which built-in CDS session variable provides the authenticated '
                                                    'SAP user ID executing the query at runtime?',
                                          'question_id': 'd49_q2'}],
                     'step_id': 'd49_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 49 Mastery Assessment: Parameters & Session Variables'},
                 {   'step_id': 'd49_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Declared strongly typed CDS input parameters (`with parameters`) for dynamic '
                                   'calculation pushdown.\n'
                                   '- Consumed built-in session variables (`$session.user`, `$session.system_date`, '
                                   '`$session.client`).\n'
                                   '- Propagated parameters across associated parameterized view path expressions.',
                     'title': 'Mastery Verification: Parameters & Session Variables'},
                 {   'recommended_mission': {   'description': 'Develop a parameterized CDS view entity supporting '
                                                               'dynamic currency translation and key-date valuation.',
                                                'slug': 'nova-parameterized-reporting-service',
                                                'title': 'Multi-Currency Parameterized Reporting Service'},
                     'step_id': 'd49_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered parameterized CDS views and environment session variables. Next, '
                                   'you will explore the CDS Annotations Framework and metadata governance.',
                     'title': 'Day 49 Complete: Parameters Mastered'}],
    'subtitle': 'Input parameters, $session environment variables, parameter propagation across associations, and '
                'multi-currency valuation',
    'title': 'Parameterized CDS Views & Session Variables'},
    50: {   'atomic_concepts': ['cds-annotations-framework', 'semantics-annotations'],
    'day_number': 50,
    'estimated_minutes': 75,
    'recommended_mission_slug': 'nova-cds-semantic-annotation-audit',
    'slug': 'cds-annotations-catalog',
    'steps': [   {   'content_md': '### What Are CDS Annotations?\n'
                                   'In ABAP Core Data Services, **Annotations** are metadata decorators prefixed with '
                                   '`@` that enrich database entities with semantic meaning.\n'
                                   '\n'
                                   'Annotations do NOT alter basic SQL query logic directly; instead, they instruct '
                                   '**downstream consumer frameworks** on how to compile, format, aggregate, secure, '
                                   'and render data:\n'
                                   '- **HANA Database Engine**: Directs in-engine analytical indexing and join '
                                   'pruning.\n'
                                   '- **Analytical Engine (SADL)**: Interprets measures, aggregations, and dimensional '
                                   'hierarchies.\n'
                                   '- **SAP Fiori Elements**: Automatically generates UI smart tables, charts, object '
                                   'pages, and filter bars without manual JavaScript coding.\n'
                                   '- **ABAP Runtime & Security**: Enforces Data Control Language (DCL) authorization '
                                   'checks.',
                     'key_terms': [   {   'definition': 'A declarative metadata tag (@) enriching CDS elements with '
                                                        'semantics consumed by compilers and frameworks.',
                                          'term': 'CDS Annotation'},
                                      {   'definition': 'Service Adaptation and Description Layer mapping CDS entities '
                                                        'to OData and analytical runtimes.',
                                          'term': 'SADL'},
                                      {   'definition': 'Architecture where SAP Fiori Elements dynamically renders '
                                                        'screens driven strictly by CDS annotations.',
                                          'term': 'Metadata-Driven UI'}],
                     'step_id': 'd50_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Annotations enrich CDS entities with metadata consumed by analytical engines, '
                                 'security layers, and UI generators.',
                     'title': 'The CDS Annotations Framework & Metadata Governance'},
                 {   'content_md': '### Core Annotation Categories in S/4HANA\n'
                                   '1. **Domain Semantics (`@Semantics`)**:\n'
                                   "   - `@Semantics.amount.currencyCode: 'CurrencyField'`: Binds a numerical decimal "
                                   'to its currency code, preventing currency aggregation errors.\n'
                                   "   - `@Semantics.quantity.unitOfMeasure: 'UnitField'`: Binds quantities to units "
                                   '(e.g. KG, EA).\n'
                                   '2. **Analytical Metadata (`@Analytics`)**:\n'
                                   '   - `@Analytics.dataCategory: #CUBE`: Marks view as fact cube.\n'
                                   '   - `@Analytics.dataCategory: #DIMENSION`: Marks view as master data dimension.\n'
                                   '   - `@Analytics.query: true`: Marks view as transient analytical query.\n'
                                   '   - `@Aggregation.default: #SUM`: Specifies automatic measure aggregation rule '
                                   '(modern standard; `@DefaultAggregation` is legacy/obsolete).\n'
                                   '3. **User Interface & Text (`@EndUserText`, `@UI`)**:\n'
                                   '   - `@EndUserText.label`: Provides human-readable, translatable labels.\n'
                                   '   - `@UI.lineItem`: Defines column display order in Fiori Elements tables.\n'
                                   '4. **Security (`@AccessControl`)**:\n'
                                   '   - `@AccessControl.authorizationCheck: #CHECK`: Mandates DCL authorization check '
                                   'at runtime.\n'
                                   '\n'
                                   '### Modern OData Exposure Standard\n'
                                   '> **CRITICAL ARCHITECTURAL SAFEGUARD**: Do NOT teach `@OData.publish: true` as '
                                   'modern standard!\n'
                                   '>\n'
                                   '> `@OData.publish: true` was a legacy DDIC-era shortcut. Modern SAP S/4HANA (since '
                                   '2020) exposes CDS views via **RAP Service Definitions** and **Service Bindings** '
                                   'supporting OData V4 and OData V2.',
                     'key_terms': [   {   'definition': 'Annotation domain defining business units, currency '
                                                        'references, and communication types.',
                                          'term': '@Semantics'},
                                      {   'definition': 'Modern ABAP CDS annotation defining default measure '
                                                        'aggregation (#SUM, #MAX, #MIN, #AVG); replaces obsolete '
                                                        '@DefaultAggregation.',
                                          'term': '@Aggregation.default'},
                                      {   'definition': 'Modern RAP artifact defining which CDS entities are exposed '
                                                        'in a business service.',
                                          'term': 'Service Definition'}],
                     'step_id': 'd50_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Annotations define data typing and semantics; modern OData exposure uses RAP Service '
                                 'Definitions, not @OData.publish.',
                     'title': 'Core Annotation Domains: @Semantics, @Analytics, @EndUserText'},
                 {   'company_context': {   'annotations_applied': [   '@Semantics.amount.currencyCode',
                                                                       '@Semantics.quantity.unitOfMeasure',
                                                                       '@Aggregation.default: #SUM'],
                                            'company_name': 'Nova Manufacturing Corp',
                                            'fields_fixed': ['NetAmount', 'OrderQuantity'],
                                            'view_audited': 'I_SalesOrderItem'},
                     'content_md': '### Before & After Annotation Comparison\n'
                                   '1. **Unannotated (Defective)**:\n'
                                   '   - `NetAmount : abap.curr(15,2);` $\to$ Fiori displays raw number, analytical '
                                   'engine sums across EUR and USD without conversion!\n'
                                   '2. **Corrected Modern CDS Definition**:\n'
                                   '   ```sql\n'
                                   "   @Semantics.amount.currencyCode: 'TransactionCurrency'\n"
                                   '   @Aggregation.default: #SUM\n'
                                   '   NetAmount,\n'
                                   '   TransactionCurrency,\n'
                                   '\n'
                                   "   @Semantics.quantity.unitOfMeasure: 'OrderQuantityUnit'\n"
                                   '   @Aggregation.default: #SUM\n'
                                   '   OrderQuantity,\n'
                                   '   OrderQuantityUnit\n'
                                   '   ```',
                     'scenario': "Nova's CDS view I_SalesOrderItem had unannotated monetary and quantity fields. Fiori "
                                 'displayed raw numbers like 45000.000 without currency signs. Adding @Semantics '
                                 'annotations resolved UI formatting and analytical rollups.',
                     'step_id': 'd50_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Sales Entity Annotation Audit'},
                 {   'component_type': 'AnnotationInspector',
                     'instruction': 'Click through annotation categories (@Semantics, @Analytics, @AccessControl). '
                                    'Inspect consumer frameworks and risks if omitted.',
                     'step_id': 'd50_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Annotations are essential contracts ensuring data integrity across analytical '
                                 'engines and UI applications.',
                     'title': '[SIMULATION MODEL] CDS Annotations Catalog Inspector'},
                 {   'instruction': 'Select the correct architectural recommendation.',
                     'options': [   {   'explanation': 'Correct! RAP Service Definitions and Bindings are the '
                                                       'authoritative standard for modern S/4HANA OData service '
                                                       'exposure.',
                                        'id': 'opt_d50_correct',
                                        'is_correct': True,
                                        'text': '`@OData.publish: true` is a legacy DDIC-based exposure mechanism. In '
                                                'modern S/4HANA, CDS View Entities must be exposed using ABAP RESTful '
                                                'Application Programming Model (RAP) Service Definitions and Service '
                                                'Bindings supporting OData V4.'},
                                    {   'explanation': 'Incorrect. Modern S/4HANA uses RAP Service Definitions.',
                                        'id': 'opt_d50_err1',
                                        'is_correct': False,
                                        'text': '`@OData.publish: true` is the only way to expose any service in '
                                                'S/4HANA forever.'},
                                    {   'explanation': 'Incorrect. OData is the standard protocol for all Fiori and '
                                                       'modern integrations.',
                                        'id': 'opt_d50_err2',
                                        'is_correct': False,
                                        'text': 'OData services are strictly prohibited in SAP systems.'}],
                     'scenario': 'A junior consultant suggests adding `@OData.publish: true` to a new CDS view entity '
                                 'to generate an OData service for an enterprise web application. What is the '
                                 'authoritative modern S/4HANA guidance?',
                     'step_id': 'd50_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'CDS OData Exposure Standard Challenge'},
                 {   'questions': [   {   'concept_slug': 'semantics-annotations',
                                          'explanation': '@Semantics.amount.currencyCode binds currency amounts to '
                                                         'their currency reference element.',
                                          'id': 'd50_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': "@Semantics.amount.currencyCode: 'CurrencyField'"},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': '@UI.currencyFormat: true'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': '@Analytics.currencyType: #ISO'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': '@Format.fiatCurrency'}],
                                          'prompt': 'Which annotation must decorate a numerical currency amount field '
                                                    'to link it with its corresponding 3-character ISO currency code '
                                                    'in the same CDS entity?',
                                          'question_id': 'd50_q1'},
                                      {   'concept_slug': 'cds-annotations-framework',
                                          'explanation': '#NOT_REQUIRED completely disables DCL security checks on the '
                                                         'entity.',
                                          'id': 'd50_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Because it instructs the runtime to bypass all '
                                                                     'DCL access control policies, allowing any '
                                                                     'authenticated user to read restricted row-level '
                                                                     'data.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Because it permanently locks the database table '
                                                                     'against updates.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Because it deletes user accounts automatically.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Because it converts the CDS view into a flat '
                                                                     'file.'}],
                                          'prompt': 'Why is setting `@AccessControl.authorizationCheck: #NOT_REQUIRED` '
                                                    'considered a potential risk on business-critical CDS view '
                                                    'entities?',
                                          'question_id': 'd50_q2'}],
                     'step_id': 'd50_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 50 Mastery Assessment: CDS Annotations'},
                 {   'step_id': 'd50_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Governed domain semantics using `@Semantics.amount` and `@Semantics.quantity`.\n'
                                   '- Configured analytical metadata (`@Analytics.dataCategory`, '
                                   '`@Aggregation.default: #SUM`).\n'
                                   '- Avoided deprecated `@OData.publish: true`, standardizing on RAP Service '
                                   'Definitions.',
                     'title': 'Mastery Verification: CDS Annotations'},
                 {   'recommended_mission': {   'description': 'Audit and remediate CDS entities missing @Semantics '
                                                               'annotations causing broken Fiori smart controls.',
                                                'slug': 'nova-cds-semantic-annotation-audit',
                                                'title': 'CDS Semantic Annotation & Fiori Contract Audit'},
                     'step_id': 'd50_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered the CDS Annotations Framework and metadata governance. Next, you '
                                   'will learn how to build hierarchical data models and entity compositions.',
                     'title': 'Day 50 Complete: Annotations Mastered'}],
    'subtitle': '@Semantics, @Analytics, @EndUserText, @AccessControl, metadata governance, and modern RAP service '
                'exposure',
    'title': 'CDS Annotations Catalog'},
    51: {   'atomic_concepts': ['cds-hierarchies', 'cds-compositions'],
    'day_number': 51,
    'estimated_minutes': 90,
    'recommended_mission_slug': 'nova-vdm-architecture-request',
    'slug': 'cds-hierarchy-composition',
    'steps': [   {   'content_md': '### CDS Hierarchies: Analytical Tree Traversal\n'
                                   'Enterprise business reporting frequently requires navigating recursive, '
                                   'multi-level structures:\n'
                                   '- **Cost Center & Profit Center Hierarchies**: Rollups of operational units into '
                                   'divisions and corporate entities.\n'
                                   '- **Manufacturing Bills of Material (BOMs)**: Multi-level assembly trees '
                                   '(DXTR-1000 controller -> Optical Array -> Micro-lenses).\n'
                                   '- **Organizational Trees**: Management reporting lines and approval escalation '
                                   'paths.\n'
                                   '\n'
                                   '### Native In-Database Hierarchies (`DEFINE HIERARCHY`)\n'
                                   'SAP S/4HANA provides native database-tier hierarchy processing via the **`DEFINE '
                                   'HIERARCHY`** statement:\n'
                                   '1. **Analytical Navigation Structure**: Built over self-referential parent-child '
                                   'associations within an entity to represent recursive trees.\n'
                                   '2. **HANA Kernel Execution**: Executed directly by graph processing engines in the '
                                   'HANA kernel, avoiding procedural loops in ABAP.\n'
                                   '3. **Generated Hierarchy Attributes**: Automatically computes navigational fields: '
                                   '`hierarchy_rank`, `hierarchy_level`, `hierarchy_is_cycle`, and '
                                   '`hierarchy_parent_rank` for multidimensional analytical slicing.',
                     'key_terms': [   {   'definition': 'Native database-tier analytical/navigational structure '
                                                        '(DEFINE HIERARCHY) executing recursive tree traversal in '
                                                        'HANA.',
                                          'term': 'CDS Hierarchy'},
                                      {   'definition': 'Calculated integer attribute indicating tree depth (root = '
                                                        'level 1, direct child = level 2).',
                                          'term': 'hierarchy_level'},
                                      {   'definition': 'Self-referential association linking child node IDs to parent '
                                                        'node IDs in the same entity.',
                                          'term': 'Parent-Child Relationship'}],
                     'step_id': 'd51_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'A CDS Hierarchy is an analytical/navigational structure providing native recursive '
                                 'tree traversal in the HANA kernel.',
                     'title': 'CDS Hierarchies: Analytical & Navigational Structures'},
                 {   'content_md': '### Fundamentally Distinguishing Hierarchy from Composition\n'
                                   '> **CRITICAL ARCHITECTURAL DISTINCTION**:\n'
                                   '> Do NOT present a composition as simply another hierarchy syntax!\n'
                                   '> - **CDS Hierarchy (`DEFINE HIERARCHY`)**: An analytical/navigational '
                                   'parent-child structure for recursive tree rollups and graph reporting.\n'
                                   '> - **CDS Composition (`composition of`)**: A specialized to-child association '
                                   'used for structured **business-object modeling** in the ABAP RESTful Application '
                                   'Programming Model (RAP).\n'
                                   '\n'
                                   '### Structured Business Object Modeling via Compositions\n'
                                   'In RAP, a business object consists of a root entity and composed sub-nodes:\n'
                                   '```sql\n'
                                   'define root view entity I_SalesOrder\n'
                                   '  as select from vbak\n'
                                   '  composition [0..*] of I_SalesOrderItem as _Items\n'
                                   '```\n'
                                   '\n'
                                   '### Key Composition Invariants:\n'
                                   '1. **Lifecycle Ownership**: Child entities cannot exist independently of their '
                                   'root entity. When the root sales order is deleted, the RAP framework automatically '
                                   'cascade-deletes all composed items.\n'
                                   '2. **Transactional Locking Boundary**: In RAP transactional processing, locking '
                                   'the root entity automatically locks the entire composition tree.\n'
                                   '3. **Bidirectional Parent Contract**: Every child entity in a composition must '
                                   'declare a matching `association to parent` referencing the root node.',
                     'key_terms': [   {   'definition': 'Specialized to-child association in RAP defining business '
                                                        'object lifecycle ownership and transactional locking.',
                                          'term': 'Composition'},
                                      {   'definition': 'The top-level anchor entity of a business object composition '
                                                        'tree (define root view entity).',
                                          'term': 'Root Entity'},
                                      {   'definition': 'Mandatory reverse association in composed child entities '
                                                        'referencing their parent node.',
                                          'term': 'association to parent'}],
                     'step_id': 'd51_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'A CDS composition is a specialized to-child association for transactional business '
                                 'object modeling, NOT an analytical hierarchy.',
                     'title': 'CDS Compositions: Transactional Business Object Modeling'},
                 {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                            'max_depth': 3,
                                            'raw_component': 'RAW-01',
                                            'root_product': 'DXTR-1000',
                                            'sub_assembly': 'BOARD-SUB-01'},
                     'content_md': '### Hierarchy Traversal Trace\n'
                                   '1. **Level 1 (Root)**: DXTR-1000 (Finished Assembly) $\to$ `hierarchy_level: 1`, '
                                   '`hierarchy_rank: 1`.\n'
                                   '2. **Level 2 (Sub-Assembly)**: BOARD-SUB-01 (Sensor PCB) $\to$ `hierarchy_level: '
                                   '2`, `hierarchy_parent_rank: 1`.\n'
                                   '3. **Level 3 (Raw Material)**: RAW-01 (Optical Sensor Array) $\to$ '
                                   '`hierarchy_level: 3`, `hierarchy_parent_rank: 2`.',
                     'scenario': "Nova's plant PL01 models the engineering bill-of-materials for Robotics Controller "
                                 'DXTR-1000. The assembly includes sub-assemblies (Sensor Board) and raw parts (RAW-01 '
                                 'Optical Array).',
                     'step_id': 'd51_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Multi-Level Robotics BOM Hierarchy'},
                 {   'component_type': 'AssociationCardinalityMapper',
                     'instruction': 'Inspect cardinality relationships and verify how composition trees enforce '
                                    'referential integrity.',
                     'step_id': 'd51_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Compositions guarantee atomic transactional consistency across multi-level document '
                                 'trees.',
                     'title': '[SIMULATION MODEL] Association & Composition Relationship Mapper'},
                 {   'instruction': 'Select the correct RAP/CDS modeling correction.',
                     'options': [   {   'explanation': 'Correct! Compositions enforce parent-child lifecycle ownership '
                                                       'and automatic cascade deletion.',
                                        'id': 'opt_d51_correct',
                                        'is_correct': True,
                                        'text': 'Model the relationship as a composition (`composition [0..*] of '
                                                'I_SalesOrderItem as _Items`) with `association to parent` on the '
                                                'child, enabling the framework to cascade delete items when the header '
                                                'is deleted.'},
                                    {   'explanation': 'Incorrect. Wiping all items deletes active valid orders.',
                                        'id': 'opt_d51_err1',
                                        'is_correct': False,
                                        'text': 'Write a nightly background job that deletes all records in table '
                                                'VBAP.'},
                                    {   'explanation': 'Incorrect.',
                                        'id': 'opt_d51_err2',
                                        'is_correct': False,
                                        'text': 'Tell customers they are never allowed to delete sales orders.'}],
                     'scenario': 'A developer models a Sales Order Header and Sales Order Items as loose unmanaged '
                                 'associations rather than compositions. When a sales order is deleted in the RAP '
                                 'transactional runtime, orphaned sales order items remain in the database. What '
                                 'architectural change is required?',
                     'step_id': 'd51_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Composition Lifecycle Challenge'},
                 {   'questions': [   {   'concept_slug': 'cds-hierarchies',
                                          'explanation': 'DEFINE HIERARCHY compiles recursive graph traversal directly '
                                                         'into in-engine execution.',
                                          'id': 'd51_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'It enables recursive parent-child traversal '
                                                                     'directly in the HANA database kernel, avoiding '
                                                                     'multi-step procedural ABAP looping.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'It converts database tables into graphical PNG '
                                                                     'image files.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'It restricts database access to senior '
                                                                     'management only.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'It requires all hierarchy nodes to have '
                                                                     'identical names.'}],
                                          'prompt': 'What is the primary operational benefit of using the `DEFINE '
                                                    'HIERARCHY` syntax in ABAP Core Data Services?',
                                          'question_id': 'd51_q1'},
                                      {   'concept_slug': 'cds-compositions',
                                          'explanation': 'Compositions establish strict lifecycle dependence and '
                                                         'transactional locking boundaries.',
                                          'id': 'd51_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'A composition defines tight lifecycle ownership '
                                                                     'where child entities cannot exist independently '
                                                                     'of the root parent entity.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Compositions can only be used on non-SAP '
                                                                     'databases.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Compositions do not support line items.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Compositions require manual database triggers.'}],
                                          'prompt': 'In the ABAP RESTful Application Programming Model (RAP), how does '
                                                    'a composition differ from a standard association?',
                                          'question_id': 'd51_q2'}],
                     'step_id': 'd51_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 51 Mastery Assessment: Hierarchies & Compositions'},
                 {   'step_id': 'd51_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Modelled parent-child recursive structures using native CDS `DEFINE HIERARCHY` '
                                   'syntax.\n'
                                   '- Established lifecycle boundaries using RAP transactional compositions '
                                   '(`composition of`).\n'
                                   '- Enforced cascade deletion and transactional locking across document trees.',
                     'title': 'Mastery Verification: Hierarchies & Compositions'},
                 {   'recommended_mission': {   'description': 'Architect a multi-tier Virtual Data Model decoupling '
                                                               'custom apps from raw tables via released Interface '
                                                               'Views.',
                                                'slug': 'nova-vdm-architecture-request',
                                                'title': 'Nova VDM Architecture & Clean Core Extensibility'},
                     'step_id': 'd51_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered CDS hierarchies and entity compositions. Next, you will design '
                                   'multidimensional Analytical Cubes and Query Views.',
                     'title': 'Day 51 Complete: Hierarchies Mastered'}],
    'subtitle': 'Parent-child hierarchies (define hierarchy), BOM trees, transactional compositions, and root entity '
                'lifecycle boundaries',
    'title': 'CDS View Hierarchies & Compositions'},
    52: {   'atomic_concepts': ['cds-analytical-cubes', 'multidimensional-queries'],
    'day_number': 52,
    'estimated_minutes': 90,
    'recommended_mission_slug': 'nova-executive-analytics-cube',
    'slug': 'cds-embedded-analytics-cubes',
    'steps': [   {   'content_md': '### Embedded Analytics Architecture in S/4HANA\n'
                                   'In SAP S/4HANA Embedded Analytics, operational analytical reporting follows a '
                                   'standardized **Star / Snowflake Schema** built entirely from CDS View Entities:\n'
                                   '1. **Analytical Cubes (`@Analytics.dataCategory: #CUBE`)**:\n'
                                   '   - Serve as fact repositories holding high-volume transactional metrics (e.g. '
                                   'Sales Invoiced Amount, Production Cost, Inventory Movements).\n'
                                   '   - Must belong to the **Composite View tier** (`I_` or `R_`).\n'
                                   '   - Every numerical metric must be formally annotated as a measure with an '
                                   'automated aggregation rule (e.g. `@Aggregation.default: #SUM` — note: '
                                   '`@DefaultAggregation` is legacy/obsolete syntax).\n'
                                   '2. **Dimension Views (`@Analytics.dataCategory: #DIMENSION`)**:\n'
                                   '   - Provide textual descriptions and master data attributes (Customer, Plant, '
                                   'Material, Cost Center).\n'
                                   '   - Linked to the fact cube via CDS associations (`association [1..1] to '
                                   'I_Customer as _Customer`).',
                     'key_terms': [   {   'definition': 'Composite CDS view holding transactional fact records and '
                                                        'measures with default aggregation rules.',
                                          'term': 'Analytical Cube (#CUBE)'},
                                      {   'definition': 'Master data CDS view providing contextual attributes, '
                                                        'hierarchies, and texts for analytical slicing.',
                                          'term': 'Dimension View (#DIMENSION)'},
                                      {   'definition': 'Modern ABAP CDS annotation specifying default measure '
                                                        'aggregation (#SUM, #MAX, #MIN, #AVG); replaces obsolete '
                                                        '@DefaultAggregation.',
                                          'term': '@Aggregation.default'}],
                     'step_id': 'd52_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'Analytical Cubes hold fact measures while Dimension views supply master data '
                                 'attributes for multidimensional slicing.',
                     'title': 'Multidimensional Modeling: Cubes & Dimensions'},
                 {   'content_md': '### The Analytical Query Tier\n'
                                   'An **Analytical Query** is a specialized Consumption View that exposes the Cube to '
                                   'front-end reporting tools (SAP Analytics Cloud, Fiori multidimensional grids, '
                                   'Analysis for Office):\n'
                                   '- Header Annotation: `@Analytics.query: true`.\n'
                                   '- Axis Allocations:\n'
                                   '  - `@AnalyticsDetails.query.axis: #ROWS`: Projects dimensions onto the row axis '
                                   '(e.g. `Plant`, `Product`).\n'
                                   '  - `@AnalyticsDetails.query.axis: #COLUMNS`: Projects measures onto the column '
                                   'axis (e.g. `NetAmount`, `CostOfGoodsSold`).\n'
                                   '\n'
                                   '### The Transient Execution Model\n'
                                   'Analytical query views are **transient**: they are NOT physical database tables. '
                                   'When executed, the **SADL Analytical Engine** translates user slice-and-dice '
                                   'requests into optimized HANA columnar aggregation queries with sub-second response '
                                   'times.',
                     'key_terms': [   {   'definition': 'Annotation converting a consumption CDS view into an '
                                                        'executable analytical query.',
                                          'term': '@Analytics.query: true'},
                                      {   'definition': 'Axis layout annotations configuring default multidimensional '
                                                        'pivot table presentation.',
                                          'term': '#ROWS / #COLUMNS'}],
                     'step_id': 'd52_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'Analytical Query views project measures and dimensions on row and column axes, '
                                 'evaluated in-memory by the analytical engine.',
                     'title': 'Analytical Queries (@Analytics.query: true) & Slicing'},
                 {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                            'cube_view': 'I_NovaSalesMarginCube',
                                            'gross_margin': '€29,500 (34.3%)',
                                            'query_view': 'C_NovaSalesMarginQuery',
                                            'total_cogs': '€56,500',
                                            'total_net': '€86,000'},
                     'content_md': '### Multidimensional Slicing Pivot\n'
                                   '- **Heidelberg (PL01)**: Net €56,000 | COGS €37,000 | Margin €19,000 (33.9%).\n'
                                   '- **Austin (PL02)**: Net €30,000 | COGS €19,500 | Margin €10,500 (35.0%).\n'
                                   '- **Consolidated Group**: Net €86,000 | COGS €56,500 | Margin €29,500 (34.3%).',
                     'scenario': "Nova's CFO requests an executive multidimensional query analyzing gross profit "
                                 'margins across Heidelberg (PL01) and Austin (PL02) for Robotics Controller '
                                 'DXTR-1000.',
                     'step_id': 'd52_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Executive Margin Cube: Heidelberg & Austin'},
                 {   'component_type': 'AnalyticalCubeDesigner',
                     'instruction': 'Slice the analytical cube by Plant, Product, or Customer. Compare Gross Profit '
                                    'Margins across dimensions.',
                     'step_id': 'd52_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'In-memory analytical cubes perform instant multidimensional aggregation without '
                                 'pre-calculated batch cubes.',
                     'title': '[SIMULATION MODEL] Analytical Cube & Multidimensional Slicing Studio'},
                 {   'instruction': 'Identify the cause of the missing measure.',
                     'options': [   {   'explanation': 'Correct! @Aggregation.default is mandatory to classify a field '
                                                       'as a measurable analytical metric (@DefaultAggregation is '
                                                       'legacy/obsolete).',
                                        'id': 'opt_d52_correct',
                                        'is_correct': True,
                                        'text': 'The Analytical Engine only classifies numerical fields as measures if '
                                                'they declare `@Aggregation.default: #SUM` (or #MAX, #MIN, #AVG); note '
                                                'that `@DefaultAggregation` is legacy syntax. Without this annotation, '
                                                'the field is treated as an unaggregatable attribute.'},
                                    {   'explanation': 'Incorrect.',
                                        'id': 'opt_d52_err1',
                                        'is_correct': False,
                                        'text': 'Because numerical amounts can only be displayed in Microsoft Paint.'},
                                    {   'explanation': 'Incorrect.',
                                        'id': 'opt_d52_err2',
                                        'is_correct': False,
                                        'text': 'Because the table must be converted to an un-indexed flat file.'}],
                     'scenario': 'A developer creates a CDS view annotated with `@Analytics.dataCategory: #CUBE` but '
                                 'omits `@Aggregation.default: #SUM` on numerical field `InvoicedAmount`. When testing '
                                 'the view in the Analytical Query preview, the column does not appear in the measure '
                                 'catalog. Why?',
                     'step_id': 'd52_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Analytical Measure Declaration Challenge'},
                 {   'questions': [   {   'concept_slug': 'cds-analytical-cubes',
                                          'explanation': '@Analytics.dataCategory: #CUBE designates the entity as an '
                                                         'analytical fact cube.',
                                          'id': 'd52_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': '@Analytics.dataCategory: #CUBE'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': '@Analytics.dataCategory: #DIMENSION'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': '@Analytics.query: true'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': '@VDM.viewType: #BASIC'}],
                                          'prompt': 'In SAP S/4HANA Embedded Analytics, which view annotation '
                                                    'registers a composite CDS view as a multidimensional fact cube?',
                                          'question_id': 'd52_q1'},
                                      {   'concept_slug': 'multidimensional-queries',
                                          'explanation': '@Analytics.query: true converts the consumption view into an '
                                                         'executable analytical query.',
                                          'id': 'd52_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': '@Analytics.query: true'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': '@OData.publish: true'},
                                                         {'id': 'c', 'is_correct': False, 'text': '@UI.chart: []'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': '@Search.searchable: true'}],
                                          'prompt': 'Which annotation is placed on a consumption CDS view entity to '
                                                    'enable it to be executed as an analytical query by SADL runtimes?',
                                          'question_id': 'd52_q2'}],
                     'step_id': 'd52_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 52 Mastery Assessment: Analytical Cubes'},
                 {   'step_id': 'd52_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Structured multidimensional models into `#CUBE` fact views and `#DIMENSION` '
                                   'master views.\n'
                                   '- Annotated numerical measures with `@Aggregation.default: #SUM`.\n'
                                   '- Created transient analytical query consumption views with `@Analytics.query: '
                                   'true`.',
                     'title': 'Mastery Verification: Analytical Cubes'},
                 {   'recommended_mission': {   'description': 'Construct an enterprise Analytical Cube on ACDOCA and '
                                                               'MATDOC providing real-time margin slicing.',
                                                'slug': 'nova-executive-analytics-cube',
                                                'title': 'Executive Analytics Cube & Multidimensional Slicing'},
                     'step_id': 'd52_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered multidimensional analytical modeling with CDS Cubes and Queries. '
                                   'Next, you will learn how to enforce row-level security using Data Control Language '
                                   '(DCL).',
                     'title': 'Day 52 Complete: Analytical Cubes Mastered'}],
    'subtitle': 'Multidimensional modeling, @Analytics.dataCategory: #CUBE, measure aggregations, and transient query '
                'views',
    'title': 'Analytical Queries: Cubes & Dimensions'},
    53: {   'atomic_concepts': ['dcl-access-control', 'row-level-security', 'pfcg-authorization-aspects'],
    'day_number': 53,
    'estimated_minutes': 90,
    'recommended_mission_slug': 'nova-dcl-data-leak-incident',
    'slug': 'cds-access-control-dcl',
    'steps': [   {   'content_md': '### Declarative Database-Tier Security\n'
                                   'In classical ERP, row-level authorization was enforced imperatively inside ABAP '
                                   'programs using `AUTHORITY-CHECK OBJECT ...` statements. If a developer forgot to '
                                   'code the check, unauthorized users could read sensitive data.\n'
                                   '\n'
                                   'In SAP S/4HANA, **Data Control Language (DCL)** provides **declarative, '
                                   'database-tier row-level security**:\n'
                                   '1. **View-Level Prerequisite**: The CDS View Entity must specify:\n'
                                   '   `@AccessControl.authorizationCheck: #CHECK`\n'
                                   '2. **DCL Definition Artifact (`DEFINE ROLE`)**:\n'
                                   '   Written in Eclipse ADT as an independent access control artifact:\n'
                                   '   ```sql\n'
                                   "   @EndUserText.label: 'Plant Security Role'\n"
                                   '   @MappingRole: true\n'
                                   '   define role Z_Nova_Plant_Access {\n'
                                   '     grant select on I_NovaPlantInventory\n'
                                   '     where (Plant) = aspect pfcg_auth(\n'
                                   '       M_MATE_WRK,\n'
                                   '       WERKS,\n'
                                   "       ACTVT = '03'\n"
                                   '     );\n'
                                   '   }\n'
                                   '   ```\n'
                                   '3. **Transparent Execution**: When any user queries `I_NovaPlantInventory`, the '
                                   'HANA SQL optimizer transparently injects an authorization filter (e.g. `WHERE '
                                   "Plant = 'PL01'`) based on the user's PFCG authorization profile.",
                     'key_terms': [   {   'definition': 'Declarative syntax (DEFINE ROLE) enforcing row-level database '
                                                        'filtering based on user authorizations.',
                                          'term': 'Data Control Language (DCL)'},
                                      {   'definition': 'DCL operator mapping view fields to SAP classical PFCG '
                                                        'authorization objects and activities.',
                                          'term': 'aspect pfcg_auth'},
                                      {   'definition': 'CDS view annotation mandating (#CHECK) or bypassing '
                                                        '(#NOT_REQUIRED) DCL security.',
                                          'term': '@AccessControl.authorizationCheck'}],
                     'step_id': 'd53_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'DCL enforces declarative row-level security in the database kernel, preventing '
                                 'unauthorized record disclosure across all consumers.',
                     'title': 'Data Control Language (DCL) & Row-Level Authorization'},
                 {   'content_md': '### How aspect pfcg_auth Operates at Runtime\n'
                                   'When user `KLAUS_SCHMIDT` queries a secured CDS view:\n'
                                   "1. **User Authorization Extraction**: The ABAP kernel reads user `KLAUS_SCHMIDT`'s "
                                   'assigned PFCG authorizations for object `M_MATE_WRK` (Plant Authorization).\n'
                                   "2. **Value Derivation**: Klaus is authorized for `WERKS = 'PL01'` and Activity "
                                   "`ACTVT = '03'` (Display).\n"
                                   "3. **Kernel SQL Injection**: HANA injects `WHERE (Plant = 'PL01')` directly into "
                                   'the database SQL plan.\n'
                                   '4. **Zero Data Leakage**: Records for Plant `PL02` (Austin) are completely '
                                   'filtered out in the database tier; they never cross the network or consume '
                                   'application server memory.\n'
                                   '\n'
                                   '### Handling Users with Zero Authorizations\n'
                                   'If an unauthorized guest user queries the view, `aspect pfcg_auth` evaluates to '
                                   '`WHERE (1 = 0)`. Zero rows are returned without raising an unhandled exception.',
                     'key_terms': [   {   'definition': 'Classical SAP security object defining fields and permissible '
                                                        'activities (e.g. M_MATE_WRK for plants).',
                                          'term': 'PFCG Authorization Object'},
                                      {   'definition': 'Automatic injection of security predicates into database '
                                                        'queries by the HANA SQL compiler.',
                                          'term': 'Kernel Injection'}],
                     'step_id': 'd53_s2_understand',
                     'step_type': 'understand',
                     'takeaway': 'DCL maps PFCG profiles into in-database WHERE clauses; unauthorized users receive '
                                 'zero rows directly from the database kernel.',
                     'title': 'Aspect Mapping, PFCG Objects & Zero-Leakage Architecture'},
                 {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                            'elena_user': 'PL01 + PL02 Authorized (VP)',
                                            'klaus_user': 'PL01 Authorized (Heidelberg)',
                                            'sarah_user': 'PL02 Authorized (Austin)',
                                            'table_secured': 'I_NovaPlantInventory'},
                     'content_md': '### DCL Filter Verification\n'
                                   '1. **Klaus Schmidt (PL01)**: Query returns 2 rows (45 EA DXTR-1000, 250 EA '
                                   'RAW-01). Austin records invisible.\n'
                                   '2. **Sarah Miller (PL02)**: Query returns 2 rows (28 EA DXTR-1000, 110 EA RAW-01). '
                                   'Heidelberg records invisible.\n'
                                   '3. **Temp Auditor**: Query returns 0 rows (Access Denied at database tier).',
                     'scenario': 'Nova audits inventory visibility for Robotics Controller DXTR-1000. Klaus (PL01 '
                                 'Manager) queries I_NovaPlantInventory and sees only PL01 rows. Sarah (PL02 Manager) '
                                 'sees only PL02 rows. Elena (VP) sees both plants.',
                     'step_id': 'd53_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Plant Isolation Audit: Heidelberg vs Austin'},
                 {   'component_type': 'DCLAccessSimulator',
                     'instruction': 'Switch between Klaus (PL01), Sarah (PL02), Elena (VP), and Temp Auditor. Observe '
                                    'the injected WHERE clause and visible records.',
                     'step_id': 'd53_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'DCL guarantees row-level data isolation without requiring procedural code in '
                                 'application programs.',
                     'title': '[SIMULATION MODEL] DCL Access Control & Row-Level Security Simulator'},
                 {   'instruction': 'Select the correct security remediation.',
                     'options': [   {   'explanation': 'Correct! #CHECK activates DCL enforcement and DEFINE ROLE '
                                                       'binds the entity to user PFCG plant profiles.',
                                        'id': 'opt_d53_correct',
                                        'is_correct': True,
                                        'text': 'Change view annotation to `@AccessControl.authorizationCheck: #CHECK` '
                                                'and create an active DCL role (`DEFINE ROLE`) mapping field Plant to '
                                                'authorization object `M_MATE_WRK` via `aspect pfcg_auth`.'},
                                    {   'explanation': 'Incorrect. Destroying data is not a security solution.',
                                        'id': 'opt_d53_err1',
                                        'is_correct': False,
                                        'text': 'Delete all data in the Heidelberg plant to ensure no records can be '
                                                'read.'},
                                    {   'explanation': 'Incorrect.',
                                        'id': 'opt_d53_err2',
                                        'is_correct': False,
                                        'text': 'Ask Austin users to close their eyes when viewing Heidelberg '
                                                'balances.'}],
                     'scenario': 'During an internal audit, Austin operators are found viewing confidential Heidelberg '
                                 'cost center balances in a custom CDS view. The view header has '
                                 '`@AccessControl.authorizationCheck: #NOT_REQUIRED`. What is the required '
                                 'architectural fix?',
                     'step_id': 'd53_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'DCL Data Leakage Investigation Challenge'},
                 {   'questions': [   {   'concept_slug': 'dcl-access-control',
                                          'explanation': 'DEFINE ROLE defines declarative DCL row-level security '
                                                         'policies.',
                                          'id': 'd53_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'DEFINE ROLE RoleName { grant select on ViewName '
                                                                     'where ...; }'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'CREATE USER UserName WITH PASSWORD ...;'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'ALTER TABLE TableName ADD SECURITY CONSTRAINT '
                                                                     '...;'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'GRANT ALL PRIVILEGES TO PUBLIC;'}],
                                          'prompt': 'In SAP S/4HANA, which declarative statement is used to author '
                                                    'row-level access control policies for CDS View Entities?',
                                          'question_id': 'd53_q1'},
                                      {   'concept_slug': 'row-level-security',
                                          'explanation': 'HANA automatically injects DCL authorization filters into '
                                                         'the SQL WHERE clause.',
                                          'id': 'd53_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'The HANA SQL compiler automatically injects the '
                                                                     "user's PFCG authorization filter into the "
                                                                     "query's WHERE clause at the database level."},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': "The user's computer downloads all rows and hides "
                                                                     'unauthorized data using client-side JavaScript.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'An email is sent to the system administrator '
                                                                     'requesting approval for every query.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'DCL rules are only enforced during weekend batch '
                                                                     'jobs.'}],
                                          'prompt': 'How does SAP S/4HANA enforce DCL access control rules when a user '
                                                    'runs a query against a protected CDS view?',
                                          'question_id': 'd53_q2'}],
                     'step_id': 'd53_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 53 Mastery Assessment: DCL Security'},
                 {   'step_id': 'd53_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Configured view entities for authorization checking '
                                   '(`@AccessControl.authorizationCheck: #CHECK`).\n'
                                   '- Authored declarative DCL roles (`DEFINE ROLE`) using `aspect pfcg_auth`.\n'
                                   '- Validated database-tier kernel filter injection, ensuring zero cross-plant row '
                                   'leakage.',
                     'title': 'Mastery Verification: DCL Security'},
                 {   'recommended_mission': {   'description': 'Investigate an urgent compliance incident where Austin '
                                                               'operators accessed confidential Heidelberg costs and '
                                                               'deploy DCL roles.',
                                                'slug': 'nova-dcl-data-leak-incident',
                                                'title': 'DCL Authorization Leak & Row-Level Security Incident'},
                     'step_id': 'd53_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'You have mastered Data Control Language and declarative row-level security. Next, '
                                   'you will enter the comprehensive Day 54 Practical Capstone.',
                     'title': 'Day 53 Complete: DCL Security Mastered'}],
    'subtitle': 'Row-level security, DEFINE ROLE statements, aspect pfcg_auth mappings, and database-tier filter '
                'injection',
    'title': 'Access Control: Data Control Language (DCL)'},
    54: {   'atomic_concepts': ['cds-vdm-synthesis'],
    'day_number': 54,
    'estimated_minutes': 90,
    'recommended_mission_slug': 'nova-secure-vdm-architecture-challenge',
    'slug': 'hana-data-semantics-assessment',
    'steps': [   {   'content_md': '### The Architectural Culmination of Phase 4\n'
                                   'Over Days 45–53, you have mastered the foundational layers of the SAP HANA engine '
                                   'and Core Data Services:\n'
                                   '1. **HANA Physical Engine**: In-memory columnar storage, Main vs Delta store, '
                                   'Delta Merge, PlanViz execution tracing, and code pushdown.\n'
                                   '2. **Virtual Data Model**: Basic (`I_`), Composite (`R_`/`I_`), and Consumption '
                                   '(`C_`) architectural layering enforcing Clean Core decoupling.\n'
                                   '3. **CDS Expressions & Syntax**: Modern `define view entity` standards, '
                                   'conditional `CASE` logic, `coalesce` null safety, and in-database '
                                   '`currency_conversion`.\n'
                                   '4. **Associations & Cardinality**: Lazy on-demand joins, path expression '
                                   'traversal, join pruning, and avoiding multi-count cardinality traps.\n'
                                   '5. **Parameters & Annotations**: Strong typing with `with parameters`, `$session` '
                                   'variables, `@Semantics` domain typing, and `@Analytics` multidimensional cubes.\n'
                                   '6. **Data Control Language**: Declarative row-level security via `DEFINE ROLE` and '
                                   '`aspect pfcg_auth`.\n'
                                   '\n'
                                   '### Capstone Objectives\n'
                                   'In this capstone, you will evaluate and synthesize a unified, secure analytical '
                                   'architecture for Nova Manufacturing Corp (`NM01`), testing all Phase 4 concepts '
                                   'across 10 distinct competency dimensions.',
                     'key_terms': [   {   'definition': 'Unified architectural integration of VDM layering, CDS '
                                                        'associations, analytical cubes, and DCL security.',
                                          'term': 'Data Semantics Synthesis'},
                                      {   'definition': 'Multi-dimensional practical assessment testing 10 core HANA '
                                                        'and CDS concepts independently.',
                                          'term': 'Phase 4 Capstone'}],
                     'step_id': 'd54_s1_learn',
                     'step_type': 'learn',
                     'takeaway': 'A production-grade S/4HANA analytical solution harmonizes VDM layering, lazy '
                                 'associations, analytical cubes, and DCL security.',
                     'title': 'Phase 4 Capstone: Enterprise Data Semantics Synthesis'},
                 {   'content_md': '### Nova Manufacturing Analytical Blueprint\n'
                                   "Nova's executive dashboard unifies transactional data across the entire "
                                   'enterprise:\n'
                                   '- **Raw Tables**: `ACDOCA` (Universal Journal), `MATDOC` (Material Movements), '
                                   '`VBAK`/`VBRP` (Sales Billing).\n'
                                   '- **Basic Views**: `I_JournalEntryItem`, `I_MaterialDocumentItem`, `I_Plant`, '
                                   '`I_Product`.\n'
                                   '- **Composite Cube**: `I_NovaEnterpriseMarginCube` (@Analytics.dataCategory: '
                                   '#CUBE) combining billed revenue, inventory movement costs, and manufacturing '
                                   'variances.\n'
                                   '- **Consumption Query**: `C_ExecutiveCockpitQuery` (@Analytics.query: true) '
                                   'providing multidimensional slicing for executives.\n'
                                   '- **Security Policy**: DCL role `Z_Nova_Global_Access` enforcing row-level access '
                                   'control based on user plant authorizations (`M_MATE_WRK`).',
                     'key_terms': [   {   'definition': 'End-to-end lineage mapping raw tables through VDM tiers to '
                                                        'executive dashboards.',
                                          'term': 'Analytical Blueprint'}],
                     'step_id': 'd54_s2_understand',
                     'step_type': 'understand',
                     'takeaway': "Nova's architecture decouples raw tables via VDM tiers and guarantees row-level "
                                 'security at the database kernel.',
                     'title': 'The Nova Manufacturing End-to-End Analytics Architecture'},
                 {   'company_context': {   'company_code': 'NM01',
                                            'company_name': 'Nova Manufacturing Corp',
                                            'data_volume': '150,000 journal records',
                                            'plants': ['PL01', 'PL02'],
                                            'query_response_time': '12 ms',
                                            'row_leakage': '0 records'},
                     'content_md': '### Architecture Evaluation Checklist\n'
                                   '- [x] **HANA Engine**: 100% Column Store execution; PlanViz confirms zero '
                                   'row-engine fallback.\n'
                                   '- [x] **VDM Layering**: Direct table access eliminated; all models build on '
                                   'released Interface Views.\n'
                                   '- [x] **Association Multiplicity**: Explicit cardinalities [1..1] and [0..*] '
                                   'validated against business rules.\n'
                                   '- [x] **Metadata Typing**: All currency fields annotated with '
                                   '`@Semantics.amount.currencyCode`.\n'
                                   '- [x] **DCL Enforcement**: Multi-tenant plant isolation verified with zero '
                                   'cross-plant row disclosure.',
                     'scenario': "Nova's Architecture Review Board evaluates the complete data lineage from ACDOCA "
                                 'line items through VDM layers into the Executive Cockpit.',
                     'step_id': 'd54_s3_visual_example',
                     'step_type': 'visual_example',
                     'title': 'Nova Manufacturing Executive Cockpit Lineage Audit'},
                 {   'component_type': 'VDMBuilder',
                     'instruction': 'Review the complete three-tier VDM hierarchy. Verify clean core stability '
                                    'contracts and DCL role integration.',
                     'step_id': 'd54_s4_interactive_practice',
                     'step_type': 'interactive_practice',
                     'takeaway': 'Strict adherence to VDM and DCL standards produces maintainable, high-performance '
                                 'S/4HANA solutions.',
                     'title': '[SIMULATION MODEL] VDM Architecture & Capstone Studio'},
                 {   'instruction': 'Select the authoritative enterprise architectural resolution.',
                     'options': [   {   'explanation': 'Correct! Reusing VDM entities and declarative DCL roles scales '
                                                       'seamlessly across new organizational units while maintaining '
                                                       'Clean Core integrity.',
                                        'id': 'opt_d54_correct',
                                        'is_correct': True,
                                        'text': 'Reject the proposal. Integrate Plant PL02 directly into the existing '
                                                'Company Code NM01 VDM architecture: extend basic interface views, '
                                                'assign PFCG plant authorizations to Austin staff, and enforce '
                                                'existing DCL roles and analytical cubes without code duplication or '
                                                'Clean Core violations.'},
                                    {   'explanation': 'Incorrect. Fragmenting the database destroys real-time '
                                                       'enterprise consolidation.',
                                        'id': 'opt_d54_err1',
                                        'is_correct': False,
                                        'text': 'Approve cloning the database because every plant must run on an '
                                                'independent physical server.'},
                                    {   'explanation': 'Incorrect.',
                                        'id': 'opt_d54_err2',
                                        'is_correct': False,
                                        'text': 'Delete table ACDOCA and conduct all business using paper ledgers.'}],
                     'scenario': 'Nova Manufacturing acquires a new subsidiary plant in Austin (PL02). An external '
                                 'contractor submits a proposal to clone the entire database and write standalone PHP '
                                 'reporting scripts querying table ACDOCA directly. As Chief SAP Enterprise Architect, '
                                 'how do you resolve this?',
                     'step_id': 'd54_s5_challenge',
                     'step_type': 'challenge',
                     'title': 'Comprehensive Data Semantics Architectural Decision'},
                 {   'questions': [   {   'concept_slug': 'sql-optimizer-pushdown',
                                          'explanation': 'Code pushdown delegates data-intensive work to the in-memory '
                                                         'database tier.',
                                          'id': 'd54_q1',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Data-intensive calculations, aggregations, and '
                                                                     'filters execute directly in the in-memory '
                                                                     'columnar database tier, minimizing network '
                                                                     'transport payload and application server memory '
                                                                     'consumption.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'It converts all database tables into '
                                                                     'uncompressed flat text files.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'It eliminates the need for user passwords.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'It forces all queries to run during scheduled '
                                                                     'weekend downtime.'}],
                                          'prompt': 'In SAP HANA architecture, what is the primary performance benefit '
                                                    'of Code Pushdown compared to classical application-server '
                                                    'processing?',
                                          'question_id': 'd54_q1'},
                                      {   'concept_slug': 'planviz-analysis',
                                          'explanation': 'Engine hops represent expensive context switches between '
                                                         'HANA execution engines.',
                                          'id': 'd54_q2',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'A costly context switch during query execution, '
                                                                     'typically caused by un-pushable procedural '
                                                                     'constructs or non-optimized calculation views.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'That the server cooling fans have switched to '
                                                                     'maximum speed.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'That the query executed with 100% optimal vector '
                                                                     'efficiency.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'That the database disk is completely full.'}],
                                          'prompt': 'When analyzing a compiled execution plan in SAP HANA Plan '
                                                    "Visualizer (PlanViz), what does an 'Engine Hop' between the SQL "
                                                    'engine and Calculation Engine signify?',
                                          'question_id': 'd54_q2'},
                                      {   'concept_slug': 'delta-merge-architecture',
                                          'explanation': 'Delta merge moves write-buffer records into compressed '
                                                         'columnar main storage.',
                                          'id': 'd54_q3',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'It consolidates transactional modifications from '
                                                                     'the write-optimized Delta Store into the '
                                                                     'read-optimized, dictionary-compressed Main '
                                                                     'Store.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'It deletes historical backup archives from tape '
                                                                     'storage.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'It merges multiple user email accounts into a '
                                                                     'single inbox.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'It converts column store tables into classical '
                                                                     'row store tables.'}],
                                          'prompt': 'What operational role does the SAP HANA Delta Merge mechanism '
                                                    'perform?',
                                          'question_id': 'd54_q3'},
                                      {   'concept_slug': 'vdm-architecture-tiers',
                                          'explanation': 'VDM tiers are BASIC, COMPOSITE, and CONSUMPTION; C1 and C2 '
                                                         'are API release contracts.',
                                          'id': 'd54_q4',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Official VDM tiers are BASIC, COMPOSITE, and '
                                                                     'CONSUMPTION governed by @VDM.viewType; release '
                                                                     'contracts C1 (Use System-Internally) and C2 (Use '
                                                                     'as Remote API) are orthogonal API governance '
                                                                     'contracts, not VDM tiers.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'C1 and C2 are the only two VDM tiers in '
                                                                     'S/4HANA.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Prefix I_ always guarantees a view is Basic.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'VDM tiers are defined by the physical disk size '
                                                                     'of database tables.'}],
                                          'prompt': 'In the SAP Virtual Data Model (VDM), how are official '
                                                    'architectural tiers defined and distinguished from API release '
                                                    'contracts?',
                                          'question_id': 'd54_q4'},
                                      {   'concept_slug': 'interface-vs-consumption-views',
                                          'explanation': 'Consumption views represent top-level UI endpoints and must '
                                                         'not become dependencies.',
                                          'id': 'd54_q5',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Because Consumption Views are tailored '
                                                                     'specifically for application screens and UI '
                                                                     'requirements, lacking the architectural '
                                                                     'stability contracts required for reusable data '
                                                                     'modeling.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Because HANA does not allow more than one CDS '
                                                                     'view in a database schema.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Because Consumption views automatically expire '
                                                                     'after 24 hours.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Because Consumption views only run in client '
                                                                     '000.'}],
                                          'prompt': 'According to authoritative SAP VDM layering rules, why are '
                                                    'Consumption Views (C_) strictly prohibited from being referenced '
                                                    'by other CDS views?',
                                          'question_id': 'd54_q5'},
                                      {   'concept_slug': 'cds-case-statements',
                                          'explanation': 'CDS View Entities use declarative SQL CASE statements.',
                                          'id': 'd54_q6',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Using declarative `case when Condition then '
                                                                     'Value else Fallback end` syntax.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Using procedural IF ... ELSEIF ... ENDIF '
                                                                     'statements.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Using JavaScript switch statements embedded in '
                                                                     'HTML comments.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Using operating system shell scripts.'}],
                                          'prompt': 'In an ABAP CDS View Entity, how must conditional classification '
                                                    'logic be declared for in-memory column engine execution?',
                                          'question_id': 'd54_q6'},
                                      {   'concept_slug': 'cds-associations-concept',
                                          'explanation': 'Declaring an association defines reusable navigation '
                                                         'semantics without joining; consuming target fields '
                                                         'instantiates joins on demand.',
                                          'id': 'd54_q7',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Declaring an association defines reusable '
                                                                     'navigation semantics without joining; consuming '
                                                                     'target fields via path expressions instantiates '
                                                                     'joins on-demand, allowing unreferenced targets '
                                                                     'to be pruned by the optimizer.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Associations are always faster than joins under '
                                                                     'every circumstance without exceptions.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Associations permanently delete unreferenced '
                                                                     'records to free up RAM.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Associations force all queries to run in '
                                                                     'single-user mode.'}],
                                          'prompt': 'How does a CDS Association differ architecturally from an eager '
                                                    'SQL LEFT OUTER JOIN in enterprise data models?',
                                          'question_id': 'd54_q7'},
                                      {   'concept_slug': 'cardinality-rules',
                                          'explanation': 'Inaccurate [1..1] cardinality results in Cartesian '
                                                         'duplication of parent rows.',
                                          'id': 'd54_q8',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'The database join produces duplicate rows for '
                                                                     'the parent entity, causing numerical measures '
                                                                     '(e.g. revenue, cost) to be multiplied and '
                                                                     'distorted in un-aggregated queries.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'The computer monitor turns off immediately.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'The database automatically corrects the error '
                                                                     'without consequence.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'All data in the system is converted into '
                                                                     'Japanese text.'}],
                                          'prompt': 'What catastrophic defect occurs if a developer declares '
                                                    'cardinality `[1..1]` on an association where the target entity '
                                                    'actually contains multiple matching rows (e.g. split deliveries)?',
                                          'question_id': 'd54_q8'},
                                      {   'concept_slug': 'cds-parameters',
                                          'explanation': 'ABAP SQL passes parameters via parentheses syntax `I_View( '
                                                         'param = val )`.',
                                          'id': 'd54_q9',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Using parenthesis syntax: `SELECT * FROM I_View( '
                                                                     "p_target_curr = 'USD', p_eval_date = '20260925' "
                                                                     ')`.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'By modifying global server environment variables '
                                                                     'in Windows Registry.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'By writing parameter values into a flat file on '
                                                                     'drive C:.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Parameters cannot be passed to CDS views.'}],
                                          'prompt': 'How are typed input parameters passed to a parameterized CDS view '
                                                    'entity at execution time in ABAP SQL?',
                                          'question_id': 'd54_q9'},
                                      {   'concept_slug': 'semantics-annotations',
                                          'explanation': '@Semantics.amount.currencyCode binds numerical amounts to '
                                                         'their currency key.',
                                          'id': 'd54_q10',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': "@Semantics.amount.currencyCode: 'CurrencyField'"},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': "@UI.currencySymbol: 'EUR'"},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': '@Analytics.currencyBinding: true'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': '@Format.currencyNumber'}],
                                          'prompt': 'Which CDS annotation must be applied to an amount field to bind '
                                                    'it to a currency code field in the projection list?',
                                          'question_id': 'd54_q10'},
                                      {   'concept_slug': 'cds-hierarchies',
                                          'explanation': 'Hierarchies provide analytical tree traversal; compositions '
                                                         'model business-object lifecycle and locking.',
                                          'id': 'd54_q11',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'A CDS Hierarchy provides recursive parent-child '
                                                                     'tree navigation and analytical rollups, whereas '
                                                                     'a CDS Composition is a specialized to-child '
                                                                     'association defining business-object lifecycle '
                                                                     'ownership and locking in RAP.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'They are identical syntaxes with different '
                                                                     'spelling.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Compositions are used only for drawing charts in '
                                                                     'web browsers.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Hierarchies can only have one single row.'}],
                                          'prompt': 'How does a native CDS Hierarchy (DEFINE HIERARCHY) fundamentally '
                                                    'differ from a CDS Composition (composition of)?',
                                          'question_id': 'd54_q11'},
                                      {   'concept_slug': 'cds-analytical-cubes',
                                          'explanation': '@Aggregation.default defines how measures roll up in '
                                                         'analytical multidimensional queries; @DefaultAggregation is '
                                                         'legacy.',
                                          'id': 'd54_q12',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': '@Aggregation.default: #SUM (or #MAX, #MIN, #AVG) '
                                                                     '— Note: @DefaultAggregation is legacy/obsolete'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': '@UI.chartType: #BAR'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': '@Analytics.isMeasure: true'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': '@Search.defaultSearchElement: true'}],
                                          'prompt': 'In SAP S/4HANA Embedded Analytics, what modern annotation must be '
                                                    'declared on every numerical measure in an analytical cube?',
                                          'question_id': 'd54_q12'},
                                      {   'concept_slug': 'dcl-access-control',
                                          'explanation': 'DCL enforces declarative row-level security directly at the '
                                                         'database tier.',
                                          'id': 'd54_q13',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'To declare database-tier row-level access '
                                                                     'control policies that automatically inject PFCG '
                                                                     'authorization filters into CDS queries.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'To design graphical user interface layouts.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'To manage printer spool jobs.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'To encrypt hard disk drives.'}],
                                          'prompt': 'What is the primary role of Data Control Language (DCL) in the '
                                                    'SAP S/4HANA architecture?',
                                          'question_id': 'd54_q13'},
                                      {   'concept_slug': 'row-level-security',
                                          'explanation': 'HANA database kernel injects the authorization predicate '
                                                         'directly into the SQL WHERE clause.',
                                          'id': 'd54_q14',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Directly in the SAP HANA database engine kernel '
                                                                     'during SQL query execution.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': "In the user's web browser using client-side "
                                                                     'JavaScript.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'In the network router between the client and '
                                                                     'server.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'In an external email gateway.'}],
                                          'prompt': 'When a user queries a CDS view protected by an active DCL role '
                                                    'using `aspect pfcg_auth`, where is the authorization filter '
                                                    'physically enforced?',
                                          'question_id': 'd54_q14'},
                                      {   'concept_slug': 'cds-vdm-synthesis',
                                          'explanation': 'A unified modern data semantics architecture combines VDM '
                                                         'layering, lazy associations, analytical cubes, and DCL '
                                                         'security.',
                                          'id': 'd54_q15',
                                          'options': [   {   'id': 'a',
                                                             'is_correct': True,
                                                             'text': 'Decoupling raw tables via released VDM Basic '
                                                                     'Views, modeling analytical facts as #CUBE with '
                                                                     'lazy associations, and enforcing declarative DCL '
                                                                     'row-level security at the database tier.'},
                                                         {   'id': 'b',
                                                             'is_correct': False,
                                                             'text': 'Writing all queries as direct SQL selects in '
                                                                     'user interface components.'},
                                                         {   'id': 'c',
                                                             'is_correct': False,
                                                             'text': 'Disabling all security checks to maximize CPU '
                                                                     'speed.'},
                                                         {   'id': 'd',
                                                             'is_correct': False,
                                                             'text': 'Exporting all data to unsecured desktop '
                                                                     'spreadsheets.'}],
                                          'prompt': 'What architectural principle unifies high performance, Clean Core '
                                                    'stability, and enterprise compliance across the S/4HANA data '
                                                    'model?',
                                          'question_id': 'd54_q15'}],
                     'step_id': 'd54_s6_assessment',
                     'step_type': 'assessment',
                     'title': 'Day 54 Capstone Benchmark: 10-Concept Multi-Dimensional Evaluation'},
                 {   'step_id': 'd54_s7_mastery_evidence',
                     'step_type': 'mastery_evidence',
                     'summary_md': '### Demonstrated Competencies\n'
                                   '- Evaluated all 10 core Phase 4 concept dimensions independently across physical '
                                   'engine, VDM, CDS, Analytics, and DCL.\n'
                                   '- Synthesized an enterprise-grade Virtual Data Model on ACDOCA and MATDOC for Nova '
                                   'Manufacturing.\n'
                                   '- Verified in-memory pushdown performance, Clean Core stability contracts, and '
                                   'database-tier row-level security.',
                     'title': 'Mastery Verification: Phase 4 Capstone Benchmark'},
                 {   'recommended_mission': {   'description': 'Architect a unified, high-performance, row-level '
                                                               'secured Virtual Data Model delivering real-time '
                                                               'operational analytics for Nova Manufacturing.',
                                                'slug': 'nova-secure-vdm-architecture-challenge',
                                                'title': 'Enterprise Secure VDM & Analytical Synthesis Challenge'},
                     'step_id': 'd54_s8_completion',
                     'step_type': 'completion',
                     'summary_md': 'Congratulations! You have successfully mastered SAP HANA Engine Architecture, the '
                                   'Virtual Data Model, advanced CDS modeling, Embedded Analytics, and DCL Security. '
                                   'You have completed Phase 4.',
                     'title': 'Day 54 Complete: Phase 4 Capstone Mastered'}],
    'subtitle': 'Phase 4 benchmark: developing a complete, secure, analytical VDM layer on ACDOCA and MATDOC',
    'title': 'HANA Engine & Data Semantics Assessment'},
}
