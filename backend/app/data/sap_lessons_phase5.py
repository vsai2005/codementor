"""Authoritative content definitions for SAP S/4HANA Guided Learning Days 55–64 (Phase 5).

Phase 5: SAP Fiori & Enterprise UX (Design, Spaces/Pages, UI5, OData, Elements, Floorplans, Capstone).
Enterprise Continuous Model: Nova Manufacturing Corp (NM01)
"""

from __future__ import annotations
from typing import Any

PHASE_5_DAYS_CONTENT: dict[int, dict[str, Any]] = {   55: {   'atomic_concepts': ['fiori-design-principles', 'fiori-app-types'],
            'day_number': 55,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'fiori-design-principles',
            'steps': [   {   'content_md': '### The Evolution of Enterprise User Experience in SAP\n'
                                           'SAP Fiori is the design system and user experience (UX) paradigm for SAP '
                                           'S/4HANA and the SAP Business Technology Platform (BTP). It replaces '
                                           'monolithic transaction codes (SAP GUI dynpros) with role-based, '
                                           'consumer-grade digital workplace experiences.\n'
                                           '\n'
                                           '#### The Five Core Fiori Design Principles:\n'
                                           '1. **Role-Based**: Applications are tailored to specific business roles '
                                           '(e.g., Accounts Payable Clerk, Plant Maintenance Engineer, Warehouse '
                                           'Supervisor), exposing only the exact tasks, fields, and actions needed '
                                           'rather than 50-field generic screens.\n'
                                           '2. **Adaptive**: UI layouts run seamlessly across devices (desktop, '
                                           'tablet, smartphone, rugged warehouse scanners) with responsive '
                                           'break-points and touch-optimized controls.\n'
                                           '3. **Coherent**: Consistent design language, navigation patterns, '
                                           'iconography, and color semantics (SAP Horizon, Quartz, Belize themes) '
                                           'across all business functions.\n'
                                           '4. **Simple**: 1-1-3 rule focus: 1 user, 1 task, up to 3 screens. '
                                           'Essential information is prioritized, while secondary attributes are '
                                           'tucked into progressive disclosure facets.\n'
                                           '5. **Delightful**: Rich micro-interactions, contextual drill-downs, '
                                           'proactive notifications, and embedded AI assistance (SAP Joule) elevate '
                                           'productivity and reduce cognitive fatigue.',
                             'key_terms': [   {   'definition': 'SAP standard enterprise UX design language unifying '
                                                                'visual design, interaction patterns, and ergonomics.',
                                                  'term': 'Fiori Design System'},
                                              {   'definition': 'Design approach providing dedicated, contextual '
                                                                'applications restricted to specific organizational '
                                                                'job roles.',
                                                  'term': 'Role-Based UX'},
                                              {   'definition': 'Interaction technique deferring complex or rarely '
                                                                'used features to secondary screens or accordion '
                                                                'facets.',
                                                  'term': 'Progressive Disclosure'}],
                             'step_id': 'd55_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'SAP Fiori decomposes massive legacy dynpro transactions into lightweight, '
                                         'role-tailored apps built on 5 fundamental design pillars.',
                             'title': 'SAP Fiori Design Principles & Enterprise UX Strategy'},
                         {   'content_md': '### Architectural Breakdown of Fiori App Types\n'
                                           'SAP S/4HANA categorizes frontend applications into three distinct '
                                           'architectural archetypes based on transactional state, database load, and '
                                           'visualization model:\n'
                                           '\n'
                                           '#### 1. Transactional Apps\n'
                                           '- **Purpose**: High-frequency operational tasks: creating purchase '
                                           'requisitions (`ME51N` equivalent), approving supplier invoices, entering '
                                           'goods receipts.\n'
                                           '- **Underlying Engine**: OData V2/V4 services with transactional write '
                                           'capabilities; modern implementations leverage the ABAP RESTful Application '
                                           'Programming Model (RAP) with draft handling.\n'
                                           '- **Database Interaction**: Read/write ACID transactions directly '
                                           'targeting transactional tables (`ACDOCA`, `MATDOC`, `EKKO`).\n'
                                           '\n'
                                           '#### 2. Analytical Apps\n'
                                           '- **Purpose**: Real-time operational monitoring, aggregation, variance '
                                           'analysis, and key performance indicators (KPIs).\n'
                                           '- **Underlying Engine**: SAP HANA Analytical Engine, Core Data Services '
                                           '(CDS) Analytical Queries with `@Analytics.query: true`.\n'
                                           '- **Database Interaction**: Real-time read-only columnar aggregations, '
                                           'slicing and dicing multidimensional cubes without pre-calculated batch '
                                           'cubes.\n'
                                           '\n'
                                           '#### 3. Fact Sheet Apps\n'
                                           '- **Purpose**: Contextual 360-degree object exploration, audit trails, and '
                                           'contextual navigation (e.g., displaying all sales orders, deliveries, and '
                                           'open invoices for Customer `CUST-501`).\n'
                                           '- **Underlying Engine**: Enterprise Search (Search Models based on CDS '
                                           'views) and semantic navigation links.\n'
                                           '- **Navigation Model**: Seamless cross-app navigation via Semantic Objects '
                                           'and Actions (`#BusinessPartner-displayFactSheet`).',
                             'key_terms': [   {   'definition': 'Interactive read/write application executing business '
                                                                'operations with ACID commit guarantees.',
                                                  'term': 'Transactional App'},
                                              {   'definition': 'Read-only multidimensional reporting application '
                                                                'powered by in-database HANA calculation engines.',
                                                  'term': 'Analytical App'},
                                              {   'definition': 'Contextual navigation cockpit providing 360-degree '
                                                                'visibility over a master data or transactional '
                                                                'business entity.',
                                                  'term': 'Fact Sheet App'}],
                             'step_id': 'd55_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Fiori applications are divided into Transactional (read/write operations), '
                                         'Analytical (real-time aggregation), and Fact Sheet (contextual 360-degree '
                                         'exploration).',
                             'title': 'The Three Canonical SAP Fiori Application Types'},
                         {   'company_context': {   'company_code': 'NM01',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'plants': ['PL01', 'PL02'],
                                                    'role_matrix': [   {   'app': 'Manage Purchase Orders',
                                                                           'role': 'Purchaser',
                                                                           'tech': 'RAP Draft OData V4',
                                                                           'type': 'Transactional'},
                                                                       {   'app': 'Production Cost Variance',
                                                                           'role': 'Plant Manager',
                                                                           'tech': 'CDS Analytical Cube',
                                                                           'type': 'Analytical'},
                                                                       {   'app': 'Material 360 (DXTR-1000)',
                                                                           'role': 'Quality Inspector',
                                                                           'tech': 'Enterprise Search + Object Page',
                                                                           'type': 'Fact Sheet'}]},
                             'content_md': '### Nova Enterprise App Deployment Matrix (Heidelberg PL01)\n'
                                           '1. **Transactional App: Manage Purchase Orders**\n'
                                           '   - **Target User**: Sourcing Specialist at Heidelberg (`PO01`).\n'
                                           '   - **Legacy GUI**: `ME21N` / `ME22N` (over 80 input fields).\n'
                                           '   - **Fiori Solution**: List Report with draft persistence. User enters '
                                           'vendor `VEND-101`, component `RAW-01`, and submits. Background validation '
                                           'checks budget automatically.\n'
                                           '2. **Analytical App: Production Variance Cockpit**\n'
                                           '   - **Target User**: Operations Director at Heidelberg (`PL01`).\n'
                                           '   - **Fiori Solution**: Analytical List Page (ALP) rendering real-time '
                                           'planned vs actual cost deviations for assembly line `DXTR-1000` directly '
                                           'from `ACDOCA`.\n'
                                           '3. **Fact Sheet: Supplier 360**\n'
                                           '   - **Target User**: Strategic Sourcing Lead.\n'
                                           '   - **Fiori Solution**: Contextual Fact Sheet launched via '
                                           '`#Supplier-displayFactSheet?Supplier=VEND-101`, displaying active '
                                           'contracts, on-time delivery rate (98.4%), and open defect notifications.',
                             'scenario': 'Nova Manufacturing is modernizing its plant floor and procurement office in '
                                         'Heidelberg. Rather than training operators on complex GUI t-codes, the IT '
                                         'team deploys a role-tailored Fiori portfolio.',
                             'step_id': 'd55_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing App Portfolio Breakdown: Heidelberg (PL01)'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "Evaluate the business requirement for Nova Manufacturing's Austin plant "
                                            'and select the correct application archetype.',
                             'options': [   {   'explanation': 'Custom freestyle UI5 with direct RFC calls violates '
                                                               'Clean Core and bypasses standard CDS analytical '
                                                               'engines.',
                                                'id': 'opt1',
                                                'is_correct': False,
                                                'text': 'Build a custom analytical freestyle UI5 application querying '
                                                        'raw BSEG and ACDOCA tables via custom RFCs.'},
                                            {   'explanation': 'Correct! CDS-based Analytical Apps push real-time '
                                                               'aggregation to the HANA engine while conforming to '
                                                               'Fiori role-based standards.',
                                                'id': 'opt2',
                                                'is_correct': True,
                                                'text': 'Deploy an Analytical Fiori App using a CDS Analytical '
                                                        'Projection on ACDOCA, integrated into Launchpad with '
                                                        'role-based tile KPIs.'},
                                            {   'explanation': 'Embedding legacy dynpros in iframes fails adaptive '
                                                               'mobile design and lacks role-tailored simplicity.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Re-enable WebGUI Dynpro ME21N inside an iframe on the '
                                                        'Launchpad.'}],
                             'step_id': 'd55_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Analytical apps leveraging CDS analytical engines provide zero-latency '
                                         'aggregation while maintaining Clean Core principles.',
                             'title': 'Enterprise Scenario: Selecting the Optimal Fiori App Architecture'},
                         {   'instruction': 'How should an enterprise SAP Solution Architect resolve this requirement '
                                            'while upholding Fiori principles?',
                             'options': [   {   'explanation': 'Violates Fiori simple and adaptive principles, causing '
                                                               'severe operational error rates in warehouse scanning.',
                                                'id': 'a',
                                                'is_correct': False,
                                                'text': 'Comply with the request by shrinking the font size and '
                                                        'disabling responsive CSS break-points on mobile devices.'},
                                            {   'explanation': 'Correct! Role-based UX separates operational order '
                                                               'fulfillment from sales order pricing, delivering a '
                                                               'streamlined, error-resilient mobile UI.',
                                                'id': 'b',
                                                'is_correct': True,
                                                'text': 'Apply the 1-1-3 rule: isolate the warehouse picker role, '
                                                        'display only picking status, bin location, and quantity, '
                                                        'deferring financial pricing fields.'},
                                            {   'explanation': 'Fails modern enterprise UX transformation and prevents '
                                                               'integration with real-time S/4HANA validation logic.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Migrate the picking team back to terminal telnet VT220 '
                                                        'emulation.'}],
                             'scenario': 'A legacy plant manager insists that their team needs all 110 fields from '
                                         'transaction VA01 displayed on a single smartphone screen for warehouse order '
                                         'picking.',
                             'step_id': 'd55_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Architectural Challenge: UX Harmonization Dilemma'},
                         {   'assessment_type': 'mcq',
                             'questions': [   {   'concept_slug': 'fiori-design-principles',
                                                  'explanation': 'Role-based design tailors applications specifically '
                                                                 'to the needs and permissions of a single enterprise '
                                                                 'job role.',
                                                  'id': 'd55_q1',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'Role-Based'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Monolithic Dynpro'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Database Centric'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Batch Oriented'}],
                                                  'prompt': 'Which core SAP Fiori design principle emphasizes '
                                                            'decomposing complex multi-purpose screens into '
                                                            'role-specific, focused task workflows?',
                                                  'question_id': 'd55_q1'},
                                              {   'concept_slug': 'fiori-app-types',
                                                  'explanation': 'Transactional apps handle operational read/write '
                                                                 'workflows that create or mutate business documents.',
                                                  'id': 'd55_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': False,
                                                                     'text': 'Analytical App'},
                                                                 {   'id': 'b',
                                                                     'is_correct': True,
                                                                     'text': 'Transactional App'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Fact Sheet App'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Overview Page Card'}],
                                                  'prompt': 'An enterprise application designed to allow warehouse '
                                                            'workers to confirm goods receipts and post inventory '
                                                            'updates to MATDOC belongs to which Fiori app type?',
                                                  'question_id': 'd55_q2'},
                                              {   'concept_slug': 'fiori-design-principles',
                                                  'explanation': 'Adaptive design guarantees responsive rendering '
                                                                 'across heterogeneous hardware, operating systems, '
                                                                 'and viewport sizes.',
                                                  'id': 'd55_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': False,
                                                                     'text': 'The application must run only on SAP GUI '
                                                                             '7.70 on Windows.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': True,
                                                                     'text': 'The application automatically adapts '
                                                                             'layouts and interaction controls to '
                                                                             'desktop, tablet, and smartphone form '
                                                                             'factors.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'The application must recompile its ABAP '
                                                                             'code when hardware changes.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'The user must manually resize browser '
                                                                             'windows to avoid horizontal scrolling.'}],
                                                  'prompt': "What does the 'Adaptive' principle in SAP Fiori UX "
                                                            'mandate for enterprise applications?',
                                                  'question_id': 'd55_q3'},
                                              {   'concept_slug': 'fiori-app-types',
                                                  'explanation': 'Fact Sheet apps display master data and '
                                                                 'transactional associations in a comprehensive '
                                                                 '360-degree overview.',
                                                  'id': 'd55_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Fact Sheet App'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Dynpro Screen'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Background Job Monitor'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Smart Multi-Edit Table'}],
                                                  'prompt': 'Which Fiori app type provides a contextual 360-degree '
                                                            'view of a business entity (such as Customer or Material) '
                                                            'and is typically launched via Semantic Object navigation?',
                                                  'question_id': 'd55_q4'}],
                             'step_id': 'd55_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 55 Verification Assessment'},
                         {   'step_id': 'd55_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Articulated the 5 Fiori design principles (Role-Based, Adaptive, '
                                           'Coherent, Simple, Delightful).\n'
                                           '- Mapped business operational requirements to Transactional, Analytical, '
                                           'and Fact Sheet archetypes.\n'
                                           '- Prevented UI anti-patterns (screen clutter, monolithic dynpro emulation) '
                                           'in favor of role-tailored workflows for Nova Manufacturing Corp.',
                             'title': 'Day 55 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd55_s8_completion',
                             'recommended_mission': {'slug': 'nova-fiori-design-audit', 'title': 'Fiori Design Principles & UX Audit', 'description': 'Evaluate Nova Manufacturing procurement UI against SAP Fiori design standards.'},
                             'step_type': 'completion',
                             'summary_md': 'Congratulations! You have mastered the foundational UX strategy and '
                                           'application taxonomy of SAP S/4HANA. Tomorrow, you will configure the '
                                           'central entry point for all Fiori apps: the **SAP Fiori Launchpad** using '
                                           'modern **Spaces and Pages**.',
                             'title': 'Day 55 Complete: Fiori Design Foundations Established'}],
            'subtitle': 'Role-based, adaptive, coherent, simple, and delightful UX; Transactional, Analytical, and '
                        'Factsheet apps.',
            'title': 'SAP Fiori Design Principles & App Types'},
    56: {   'atomic_concepts': ['flp-spaces-and-pages', 'business-catalogs-groups'],
            'day_number': 56,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'fiori-launchpad-spaces-pages',
            'steps': [   {   'content_md': '### The Central Access Portal: SAP Fiori Launchpad (FLP)\n'
                                           'The SAP Fiori Launchpad is the single role-based entry point for all '
                                           'S/4HANA applications, SAP GUI for HTML tiles, analytical dashboards, and '
                                           'third-party web apps.\n'
                                           '\n'
                                           '#### The Evolution from Legacy Groups to Spaces and Pages:\n'
                                           '1. **Legacy Classic FLP (Home Page & Groups)**:\n'
                                           '   - Apps were organized into flat "Groups" on a single endless scrolling '
                                           'homepage.\n'
                                           '   - As organizations scaled to hundreds of apps, user launchpads suffered '
                                           'severe performance degradation (DOM bloat) and overwhelming visual '
                                           'clutter.\n'
                                           '2. **Modern FLP Architecture (Spaces and Pages)**:\n'
                                           '   - **Space**: High-level organizational tab corresponding to a business '
                                           'role or functional area (e.g., *Procurement Overview*, *Production Control '
                                           'NM01*).\n'
                                           '   - **Page**: Structured layout assigned to a Space. A user can have one '
                                           'or more pages per space.\n'
                                           '   - **Section**: Visual grouping within a page (e.g., *Daily '
                                           'Requisitions*, *Supplier Approvals*, *Analytical Monitoring*).\n'
                                           '   - **Tile / Link**: Launchable app units within sections, displaying '
                                           'live KPI numbers or navigation targets.',
                             'key_terms': [   {   'definition': 'Single web-based entry point for enterprise '
                                                                'role-based navigation, search, and notifications.',
                                                  'term': 'Fiori Launchpad (FLP)'},
                                              {   'definition': 'Top-level navigation container representing a '
                                                                'business role area in modern FLP.',
                                                  'term': 'Space'},
                                              {   'definition': 'Structured visual hierarchy within a Space organizing '
                                                                'tiles and links into logical sub-tasks.',
                                                  'term': 'Page & Section'}],
                             'step_id': 'd56_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Spaces and Pages replace flat endless-scroll homepages with lean, '
                                         'hierarchical, role-aligned navigation containers.',
                             'title': 'SAP Fiori Launchpad Architecture: Spaces & Pages Paradigm'},
                         {   'content_md': '### Security & Content Delivery Mechanism\n'
                                           'Launchpad layout is strictly decoupled from authorization and application '
                                           'entitlement:\n'
                                           '\n'
                                           '#### 1. Business Catalogs (The Source of Truth for App Entitlements)\n'
                                           '- Created in the Fiori Launchpad Content Manager (`/UI2/FLPCM_CUST`).\n'
                                           '- Contains **Tile Definitions** (visual representation) and **Target '
                                           'Mappings** (intent-based routing configuration).\n'
                                           '- Example Intent: `SemanticObject: PurchaseOrder`, `Action: manage`.\n'
                                           '\n'
                                           '#### 2. PFCG Role Assignment\n'
                                           '- Business Catalogs are added to authorization roles via transaction '
                                           '`PFCG`.\n'
                                           '- When a user is assigned a PFCG role, they inherit:\n'
                                           '  1. Frontend authorization to execute the intent.\n'
                                           '  2. Backend OData service authorization (`IWSG` / `IWSV` or Gateway '
                                           'authorization objects).\n'
                                           '\n'
                                           '#### 3. Space and Page Assignment\n'
                                           '- Spaces and Pages are also assigned to PFCG roles.\n'
                                           '- When user `J_HEIDELBERG` logs in, FLP dynamically merges the Spaces '
                                           'assigned to their PFCG roles, populating sections with tiles granted by '
                                           'their Business Catalogs.',
                             'key_terms': [   {   'definition': 'Collection of apps, tiles, and target mappings '
                                                                'defining functional entitlement.',
                                                  'term': 'Business Catalog'},
                                              {   'definition': 'Rule resolving a Semantic Object and Action intent to '
                                                                'a concrete component, OData service, or URL.',
                                                  'term': 'Target Mapping'},
                                              {   'definition': 'ABAP authorization mechanism binding frontend '
                                                                'catalogs and backend authorizations to users.',
                                                  'term': 'PFCG Role Integration'}],
                             'step_id': 'd56_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Business Catalogs grant functional entitlement via PFCG roles, while Spaces '
                                         'and Pages organize layout presentation.',
                             'title': 'Business Catalogs, Target Mappings & PFCG Integration'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'page_id': 'ZPG_NM01_BUYER_DAILY',
                                                    'sections': [   {   'name': 'Urgent Approvals',
                                                                        'tiles': [   'Purchase Orders Pending Approval '
                                                                                     '(Count: 4)']},
                                                                    {   'name': 'Requisition Processing',
                                                                        'tiles': [   'Manage Requisitions (PL01)',
                                                                                     'Create PO (VEND-101)']},
                                                                    {   'name': 'Supplier Intelligence',
                                                                        'tiles': [   'Supplier Performance Monitor',
                                                                                     'Contract Expiry Radar']}],
                                                    'space_id': 'ZSP_NM01_PROCUREMENT'},
                             'content_md': "### Structure of Marcus Vance's Launchpad (NM01 Procurement)\n"
                                           '```\n'
                                           '[SPACE] Plant Procurement NM01\n'
                                           '  │\n'
                                           '  └── [PAGE] Buyer Daily Operations (PL01)\n'
                                           '        ├── [SECTION 1: Urgent Approvals]\n'
                                           '        │     ├── [Dynamic Tile] PO Approvals (> $50,000) [Count: 4]\n'
                                           '        │     └── [Dynamic Tile] Quality Holds (RAW-01)   [Count: 1]\n'
                                           '        │\n'
                                           '        ├── [SECTION 2: Operational Purchasing]\n'
                                           '        │     ├── [Static Tile] Manage Purchase Orders\n'
                                           '        │     └── [Static Tile] Sourcing Cockpit\n'
                                           '        │\n'
                                           '        └── [SECTION 3: Analytics & KPI Cards]\n'
                                           '              └── [Smart KPI Tile] On-Time Delivery: 94.2% [Target: '
                                           '95.0%]\n'
                                           '```',
                             'scenario': 'Nova Manufacturing configures a Space and Page for Plant Buyer Marcus Vance '
                                         'at Heidelberg (PL01). The launchpad structure maps directly to daily '
                                         'operational priorities.',
                             'step_id': 'd56_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing FLP Role Layout: Plant Procurement Lead'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "A junior buyer at Heidelberg cannot see the 'Manage Purchase Orders' tile "
                                            'on their assigned Page. Diagnose the cause.',
                             'options': [   {   'explanation': "Correct! If a page references a tile but the user's "
                                                               'PFCG role lacks the underlying Business Catalog, the '
                                                               'tile is suppressed for that user.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'The user was assigned the Page in PFCG, but the Business '
                                                        'Catalog containing the Target Mapping was omitted from their '
                                                        'PFCG role.'},
                                            {   'explanation': 'Modern Fiori Launchpad runs as pure HTML5/JavaScript; '
                                                               'ActiveX plugins are completely irrelevant.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': "The user's Windows laptop does not have the SAP GUI ActiveX "
                                                        'plugin installed.'},
                                            {   'explanation': 'Delta merge affects write storage consolidation, not '
                                                               'launchpad catalog authorization resolution.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'The HANA database delta merge process failed during the '
                                                        'night.'}],
                             'step_id': 'd56_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Tiles configured on a Page only appear if the user has an active PFCG '
                                         'authorization containing the corresponding Business Catalog.',
                             'title': 'FLP Configuration Simulation: Resolving Missing Tile Access'},
                         {   'instruction': 'What is the recommended SAP enterprise governance strategy for FLP '
                                            'personalization?',
                             'options': [   {   'explanation': 'Modifying global templates breaks standard governance, '
                                                               'overwrites peer roles, and prevents automated '
                                                               'transport updates.',
                                                'id': 'opt1',
                                                'is_correct': False,
                                                'text': 'Grant full administrator rights in `/UI2/FLP` to all 50 '
                                                        'managers so they can edit global templates.'},
                                            {   'explanation': 'Overly restrictive; prevents users from organizing '
                                                               'frequent shortcuts, degrading user adoption.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Lock all personalizations completely so users cannot even add '
                                                        'personal bookmarks.'},
                                            {   'explanation': 'Correct! Standard corporate sections remain centrally '
                                                               'governed while user personalization allows custom '
                                                               'personal sections.',
                                                'id': 'opt3',
                                                'is_correct': True,
                                                'text': 'Deliver standardized Corporate Spaces & Pages via PFCG, and '
                                                        'enable user personalization for personal sections and '
                                                        'bookmarks without altering corporate layouts.'}],
                             'scenario': 'Nova Manufacturing has 1,200 users across Germany and the US. 50 regional '
                                         'managers demand the ability to completely reorganize all company spaces and '
                                         'delete standard compliance sections.',
                             'step_id': 'd56_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Launchpad Architecture Challenge: Mass Customization Governance'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'flp-spaces-and-pages',
                                                  'explanation': 'Spaces serve as role-level navigation tabs grouping '
                                                                 'one or more sub-pages.',
                                                  'id': 'd56_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': False,
                                                                     'text': 'It acts as a physical disk volume on the '
                                                                             'HANA database.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': True,
                                                                     'text': 'It represents a high-level navigation '
                                                                             'tab corresponding to a business role or '
                                                                             'functional domain.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It compiles TypeScript code into browser '
                                                                             'bytecode.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It replaces the SAP NetWeaver '
                                                                             'application gateway.'}],
                                                  'prompt': 'In modern SAP Fiori Launchpad architecture, what is the '
                                                            "primary structural role of a 'Space'?",
                                                  'question_id': 'd56_q1'},
                                              {   'concept_slug': 'business-catalogs-groups',
                                                  'explanation': 'Target Mappings translate intent combinations '
                                                                 '(SemanticObject-action) into concrete UI component '
                                                                 'targets.',
                                                  'id': 'd56_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Target Mapping'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Delta Merge Queue'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'ACDOCA Secondary Index'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'RFC Destination'}],
                                                  'prompt': 'What core artifact in the Fiori Launchpad Content Manager '
                                                            'defines the Semantic Object and Action required to launch '
                                                            'an application?',
                                                  'question_id': 'd56_q2'},
                                              {   'concept_slug': 'flp-spaces-and-pages',
                                                  'explanation': 'Spaces and Pages provide structured pagination, '
                                                                 'eliminating endless-scroll browser performance '
                                                                 'issues.',
                                                  'id': 'd56_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Classic homepages suffered from endless '
                                                                             'scrolling, high DOM load times, and poor '
                                                                             'scalability as app counts grew.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Spaces and Pages require Adobe Flash '
                                                                             'Player to render.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Classic groups did not support ABAP '
                                                                             'programs.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Spaces and Pages eliminate the need for '
                                                                             'authorization checks.'}],
                                                  'prompt': 'Why did SAP introduce Spaces and Pages to replace the '
                                                            'legacy Fiori Home Page classic Groups model?',
                                                  'question_id': 'd56_q3'},
                                              {   'concept_slug': 'business-catalogs-groups',
                                                  'explanation': 'PFCG (Role Maintenance) links frontend Fiori '
                                                                 'Catalogs, Spaces, and backend authorizations to user '
                                                                 'accounts.',
                                                  'id': 'd56_q4',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'PFCG'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'SE38'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'SM59'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'AL11'}],
                                                  'prompt': 'Which ABAP transaction is used by security administrators '
                                                            'to assign Business Catalogs, Spaces, and Pages to '
                                                            'end-user authorization profiles?',
                                                  'question_id': 'd56_q4'}],
                             'step_id': 'd56_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 56 Verification Assessment'},
                         {   'step_id': 'd56_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Configured modern Fiori Launchpad Spaces, Pages, and Sections.\n'
                                           '- Decoupled functional authorization (Business Catalogs via PFCG) from '
                                           'visual presentation (Spaces/Pages).\n'
                                           '- Designed intent-based navigation target mappings '
                                           '(`SemanticObject-action`) for Nova Manufacturing Corp.',
                             'title': 'Day 56 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd56_s8_completion',
                             'recommended_mission': {'slug': 'nova-flp-spaces-pages-config', 'title': 'Configure FLP Spaces & Pages for Plant Ops', 'description': 'Organize production and procurement pages for Heidelberg plant managers.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You understand the operational entry point of S/4HANA. '
                                           'Tomorrow, you will dive into the underlying client-side engine: the '
                                           '**SAPUI5 Framework** (MVC architecture, two-way binding, and XML views).',
                             'title': 'Day 56 Complete: Enterprise Launchpad Configured'}],
            'subtitle': 'Configuring modern FLP Spaces, Pages, Sections, Business Catalogs, and Business Groups.',
            'title': 'Fiori Launchpad Configuration: Spaces & Pages'},
    57: {   'atomic_concepts': ['sapui5-mvc-architecture', 'ui5-data-binding'],
            'day_number': 57,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'sapui5-framework-basics',
            'steps': [   {   'content_md': '### The UI Framework Powering SAP Fiori\n'
                                           'SAPUI5 is an enterprise-grade HTML5/JavaScript framework featuring '
                                           'responsive UI controls, accessibility standards (WCAG 2.1), localization, '
                                           'and strict Model-View-Controller (MVC) separation.\n'
                                           '\n'
                                           '#### MVC Architectural Structure:\n'
                                           '1. **Model**: Manages application data, schema definitions, and '
                                           'communication with backend servers:\n'
                                           '   - **ODataModel (v2 / v4)**: Server-side model supporting server '
                                           'filtering, sorting, paging, and CRUD transactions.\n'
                                           '   - **JSONModel**: Client-side in-memory model for local UI states (e.g., '
                                           'toggling edit modes, wizard steps).\n'
                                           '   - **ResourceModel**: Manages translatable UI texts (`i18n.properties`) '
                                           'for internationalization.\n'
                                           '2. **View**: Declares the visual layout. In modern SAPUI5, **XML Views** '
                                           '(`*.view.xml`) are mandatory for performance, static validation, and clean '
                                           'design decoupling.\n'
                                           '3. **Controller**: JavaScript/TypeScript classes (`*.controller.js`) '
                                           'handling user events, custom formatting, and view lifecycle hooks '
                                           '(`onInit`, `onBeforeRendering`, `onAfterRendering`, `onExit`).\n'
                                           '4. **Component.js & manifest.json**: The application descriptor defining '
                                           'metadata, routing configuration, models, and dependencies.',
                             'key_terms': [   {   'definition': 'Enterprise client-side UI framework built on '
                                                                'JavaScript, HTML5, and CSS3 with built-in Fiori '
                                                                'controls.',
                                                  'term': 'SAPUI5'},
                                              {   'definition': 'Design pattern isolating data management (Model), '
                                                                'visual presentation (View), and logic (Controller).',
                                                  'term': 'MVC Architecture'},
                                              {   'definition': 'Central application descriptor declaring data '
                                                                'sources, routing targets, and runtime dependencies.',
                                                  'term': 'manifest.json'}],
                             'step_id': 'd57_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'SAPUI5 enforces strict separation of concerns via XML Views, JavaScript '
                                         'Controllers, and standardized OData/JSON/Resource Models.',
                             'title': 'SAPUI5 Framework Architecture & MVC Pattern'},
                         {   'content_md': '### Data Binding Mechanics in SAPUI5\n'
                                           'Data binding establishes a live link between UI control properties and '
                                           'model data structures:\n'
                                           '\n'
                                           '#### Binding Modes:\n'
                                           '- **One-Way Binding**: Data flows exclusively from Model to View. Ideal '
                                           'for read-only displays.\n'
                                           '- **Two-Way Binding**: User input in an input field automatically updates '
                                           'the client-side Model, and model changes immediately update the View. '
                                           'Supported natively by `JSONModel` and transactional `v2.ODataModel`.\n'
                                           '- **One-Time Binding**: Model data initializes the View once; subsequent '
                                           'model mutations do not trigger re-renders.\n'
                                           '\n'
                                           '#### Expression Binding Syntax:\n'
                                           'SAPUI5 allows embedded inline logic directly inside XML bindings without '
                                           'writing controller formatters:\n'
                                           '```xml\n'
                                           '<ObjectStatus\n'
                                           '    text="{statusText}"\n'
                                           '    state="{= ${totalAmount} > 50000 ? \'Error\' : \'Success\' }" />\n'
                                           '```\n'
                                           '\n'
                                           '#### Key Controller Lifecycle Hooks:\n'
                                           '- `onInit()`: Invoked once when the view is instantiated. Used to '
                                           'initialize local models and attach route pattern listeners.\n'
                                           '- `onBeforeRendering()` / `onAfterRendering()`: Executed before and after '
                                           'HTML DOM rendering.\n'
                                           '- `onExit()`: Cleanup hook invoked when the view is destroyed to free '
                                           'event listeners and memory.',
                             'key_terms': [   {   'definition': 'Automatic synchronization where view inputs update '
                                                                'model states and vice-versa.',
                                                  'term': 'Two-Way Data Binding'},
                                              {   'definition': 'Embedded JavaScript expressions in XML views '
                                                                'evaluating status or visibility dynamically.',
                                                  'term': 'Expression Binding'},
                                              {   'definition': 'Standard controller initialization hook invoked when '
                                                                'view metadata is compiled.',
                                                  'term': 'onInit Lifecycle'}],
                             'step_id': 'd57_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Data binding connects XML views dynamically to underlying models, with '
                                         'expression bindings enabling lean, declarative UI logic.',
                             'title': 'Two-Way Data Binding, Expressions & Lifecycle Hooks'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'component_name': 'RequisitionQuickCreate',
                                                    'material': 'RAW-01',
                                                    'plant': 'PL01'},
                             'content_md': '### Declarative XML View (`RequisitionQuickCreate.view.xml`)\n'
                                           '```xml\n'
                                           '<mvc:View\n'
                                           '    controllerName="nova.procurement.controller.RequisitionQuickCreate"\n'
                                           '    xmlns:mvc="sap.ui.core.mvc"\n'
                                           '    xmlns="sap.m">\n'
                                           '    <Page title="Nova Quick Requisition (PL01)">\n'
                                           '        <content>\n'
                                           '            <VBox class="sapUiMediumMargin">\n'
                                           '                <Label text="Material Number" labelFor="matInput" '
                                           'required="true"/>\n'
                                           '                <Input id="matInput" value="{reqModel>/material}" '
                                           'placeholder="e.g. RAW-01"/>\n'
                                           '                \n'
                                           '                <Label text="Required Quantity"/>\n'
                                           '                <StepInput value="{reqModel>/quantity}" min="1" '
                                           'max="500"/>\n'
                                           '                \n'
                                           '                <ObjectStatus\n'
                                           '                    text="{= ${reqModel>/quantity} > 100 ? \'Requires '
                                           'Plant Manager Approval\' : \'Standard Auto-Approval\'}"\n'
                                           '                    state="{= ${reqModel>/quantity} > 100 ? \'Warning\' : '
                                           '\'Success\'}"/>\n'
                                           '                \n'
                                           '                <Button text="Submit Requisition" '
                                           'press=".onSubmitRequisition" type="Emphasized"/>\n'
                                           '            </VBox>\n'
                                           '        </content>\n'
                                           '    </Page>\n'
                                           '</mvc:View>\n'
                                           '```',
                             'scenario': "Nova's UI5 developer creates an expedited material requisition view for "
                                         'Heidelberg maintenance technicians ordering sensor `RAW-01`.',
                             'step_id': 'd57_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Purchase Requisition Form: XML View & Controller'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'Determine the optimal SAPUI5 model type for managing temporary multi-step '
                                            'wizard button states.',
                             'options': [   {   'explanation': 'Correct! Client UI states (button enabled/disabled, '
                                                               'step flags) belong in a lightweight local JSONModel, '
                                                               'avoiding network overhead.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Instantiate a local client-side JSONModel (`new '
                                                        'sap.ui.model.json.JSONModel({ currentStep: 1, canProceed: '
                                                        'false })`).'},
                                            {   'explanation': 'Persisting transient UI hover states to the database '
                                                               'violates enterprise performance and latency standards.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': "Create an ABAP database table in S/4HANA to store the user's "
                                                        'current button hover state.'},
                                            {   'explanation': 'Global variables pollute the global namespace and '
                                                               'break component isolation in the Fiori Launchpad.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Hardcode global JavaScript variables on the `window` '
                                                        'object.'}],
                             'step_id': 'd57_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Client-side state belongs in a localized JSONModel; backend business '
                                         'entities belong in an ODataModel.',
                             'title': 'SAPUI5 Architectural Decision: Model Selection for Local UI State'},
                         {   'instruction': 'What architectural refactoring must be performed to bring the app up to '
                                            'SAP enterprise standards?',
                             'options': [   {   'explanation': 'Hardware display settings have zero impact on '
                                                               'JavaScript network loading and DOM parsing '
                                                               'bottlenecks.',
                                                'id': 'opt1',
                                                'is_correct': False,
                                                'text': "Upgrade the user's monitor refresh rate to 144Hz."},
                                            {   'explanation': 'Correct! SAPUI5 best practices mandate declarative XML '
                                                               'views, asynchronous component loading, and strict '
                                                               'model binding rather than raw DOM queries.',
                                                'id': 'opt2',
                                                'is_correct': True,
                                                'text': 'Convert the app to asynchronous module loading (AMD / '
                                                        '`sap.ui.define`), declare dependencies in `manifest.json`, '
                                                        'use standard XML views with two-way binding, and eliminate '
                                                        'raw DOM manipulation.'},
                                            {   'explanation': 'Web Dynpro is legacy technology; it fails modern Fiori '
                                                               'responsive design and mobile requirements.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Rewrite the app in legacy ABAP Web Dynpro.'}],
                             'scenario': 'A custom freestyle SAPUI5 app written by an offshore team takes 14 seconds '
                                         'to load. Inspection reveals 45 JavaScript script tags in the HTML header and '
                                         'DOM queries (`document.getElementById`) inside loops.',
                             'step_id': 'd57_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Performance Challenge: View Rendering Bottlenecks'},
                         {   'assessment_type': 'mcq',
                             'questions': [   {   'concept_slug': 'sapui5-mvc-architecture',
                                                  'explanation': 'XML Views are the SAP standard, offering '
                                                                 'compile-time checks, clean separation, and optimal '
                                                                 'rendering performance.',
                                                  'id': 'd57_q1',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'XML Views'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'HTML Script Tags'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'JSON Views'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Applet Views'}],
                                                  'prompt': 'What is the recommended view technology in modern SAPUI5 '
                                                            'applications for defining user interface structure?',
                                                  'question_id': 'd57_q1'},
                                              {   'concept_slug': 'ui5-data-binding',
                                                  'explanation': 'ResourceModels bind text properties to '
                                                                 '`i18n.properties` files, enabling effortless '
                                                                 'internationalization.',
                                                  'id': 'd57_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'ResourceModel (`i18n.properties`)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'ODataModel v4'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'JSONModel'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'XMLModel'}],
                                                  'prompt': 'Which SAPUI5 model type is best suited for managing '
                                                            'localized translations and multi-language UI labels?',
                                                  'question_id': 'd57_q2'},
                                              {   'concept_slug': 'sapui5-mvc-architecture',
                                                  'explanation': '`onInit()` is the initialization hook called once '
                                                                 'upon view creation.',
                                                  'id': 'd57_q3',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'onInit()'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'onExit()'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'onAfterRendering()'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'onSubmit()'}],
                                                  'prompt': 'In an SAPUI5 controller, which standard lifecycle method '
                                                            'is executed exactly once when the view is instantiated?',
                                                  'question_id': 'd57_q3'},
                                              {   'concept_slug': 'ui5-data-binding',
                                                  'explanation': 'Two-way binding synchronizes user inputs into the '
                                                                 'underlying model without requiring manual change '
                                                                 'listeners.',
                                                  'id': 'd57_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'The underlying model property is '
                                                                             'automatically updated in real-time '
                                                                             'without manual event handlers.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'The entire browser page reloads from '
                                                                             'scratch.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'The database commits an irreversible '
                                                                             'financial document immediately.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'The field is locked against further '
                                                                             'input.'}],
                                                  'prompt': 'What does two-way data binding accomplish when a user '
                                                            'types into an input field bound to a model property?',
                                                  'question_id': 'd57_q4'}],
                             'step_id': 'd57_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 57 Verification Assessment'},
                         {   'step_id': 'd57_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered SAPUI5 MVC structure (XML Views, JS Controllers, OData/JSON '
                                           'Models).\n'
                                           '- Applied two-way data binding and expression bindings to build dynamic '
                                           'form validations.\n'
                                           '- Eliminated performance anti-patterns (raw DOM manipulation, synchronous '
                                           'scripts) in favor of asynchronous Component loading.',
                             'title': 'Day 57 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd57_s8_completion',
                             'recommended_mission': {'slug': 'nova-ui5-controller-debugging', 'title': 'SAPUI5 Component & Controller Diagnostic', 'description': 'Trace two-way data binding and lifecycle events in custom manufacturing app.'},
                             'step_type': 'completion',
                             'summary_md': 'Superb work! You now understand the frontend runtime engine. Tomorrow, you '
                                           'will master the communication protocol that connects UI5 to the backend: '
                                           '**OData V2 and V4**.',
                             'title': 'Day 57 Complete: SAPUI5 Core Competency Achieved'}],
            'subtitle': 'Model-View-Controller (MVC) pattern, XML views, controllers, two-way data binding, and '
                        'Component.js.',
            'title': 'SAPUI5 Framework Architecture'},
    58: {   'atomic_concepts': ['odata-protocol-fundamentals', 'odata-v2-vs-v4'],
            'day_number': 58,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'odata-v2-v4-fundamentals',
            'steps': [   {   'content_md': '### What is OData?\n'
                                           'OData (Open Data Protocol) is an OASIS-standard RESTful protocol allowing '
                                           'the creation and consumption of queryable and interoperable APIs over '
                                           'HTTP. It is the mandatory communication standard between SAPUI5/Fiori '
                                           'frontends and S/4HANA backends.\n'
                                           '\n'
                                           '#### Core Protocol Capabilities:\n'
                                           '1. **Entity Data Model (EDM)**: OData exposes business data as strongly '
                                           'typed entities (e.g., `PurchaseOrder`, `PurchaseOrderItem`), entity sets, '
                                           'associations, and navigation properties.\n'
                                           '2. **Standard HTTP Verbs**:\n'
                                           '   - `GET`: Query entity sets or single entity records.\n'
                                           '   - `POST`: Create a new business entity or invoke an action.\n'
                                           '   - `PATCH` / `PUT`: Update attributes (PATCH updates delta fields; PUT '
                                           'replaces the entire entity).\n'
                                           '   - `DELETE`: Remove an entity.\n'
                                           '3. **Rich Query Options**: Client requests apply filtering, paging, and '
                                           'sorting directly via URL parameters:\n'
                                           "   - `$filter=CompanyCode eq 'NM01' and Plant eq 'PL01'`\n"
                                           '   - `$select=PurchaseOrder,Vendor,TotalAmount`\n'
                                           '   - `$expand=to_Items($select=ItemNumber,Material,NetPrice)`\n'
                                           '   - `$top=50&$skip=100` (Server-side pagination)\n'
                                           '   - `$orderby=CreatedAt desc`',
                             'key_terms': [   {   'definition': 'OASIS standard RESTful data access protocol providing '
                                                                'structured queries and entity relationships.',
                                                  'term': 'OData Protocol'},
                                              {   'definition': 'Abstract metadata schema defining entities, '
                                                                'properties, keys, and navigation links.',
                                                  'term': 'Entity Data Model (EDM)'},
                                              {   'definition': 'Standard URL parameters ($filter, $select, $expand, '
                                                                '$top) controlling server-side processing.',
                                                  'term': 'Query Options'}],
                             'step_id': 'd58_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'OData enables standard RESTful communication with database pushdown for '
                                         'filtering, sorting, and pagination via URL query options.',
                             'title': 'The Open Data Protocol (OData) in SAP S/4HANA'},
                         {   'content_md': '### Architectural Comparison: V2 vs V4\n'
                                           'While S/4HANA supports both versions, **OData V4** is the strategic '
                                           'standard for all modern SAP developments (including ABAP RAP and modern '
                                           'Fiori Elements):\n'
                                           '\n'
                                           '| Dimension | OData V2 (Legacy / Classic) | OData V4 (Strategic Standard) '
                                           '|\n'
                                           '|---|---|---|\n'
                                           '| **Payload Size** | Verbose XML/JSON with metadata wrappers (`d.results`) '
                                           '| Lean JSON format; up to 60% payload reduction |\n'
                                           '| **Data Types** | Legacy EDM primitive types | Strict, modernized EDM '
                                           'types (e.g., `Edm.Date`, `Edm.TimeOfDay`) |\n'
                                           '| **Expand Performance** | Nested expands can trigger un-optimized N+1 '
                                           'queries | Highly optimized `$expand` with sub-queries and filtering |\n'
                                           '| **Batch Processing** | `$batch` with MIME multipart payloads (complex '
                                           'parsing) | `$batch` supporting lean JSON batching and transactional groups '
                                           '|\n'
                                           '| **Side Effects** | Manual refresh calls or full entity re-reads | Native '
                                           'Side Effect annotations declare exact dependent re-fetches |\n'
                                           '| **RAP Alignment** | Requires legacy mapping layers | Direct native '
                                           'binding to RAP Behavior Definitions and Draft engine |',
                             'key_terms': [   {   'definition': 'Modernized OData protocol delivering lean JSON '
                                                                'payloads, advanced expands, and native RAP '
                                                                'integration.',
                                                  'term': 'OData V4'},
                                              {   'definition': 'OData V4 elimination of verbose wrapper objects to '
                                                                'maximize mobile throughput.',
                                                  'term': 'Payload Optimization'},
                                              {   'definition': 'Declarative protocol mechanism automatically '
                                                                'refreshing dependent fields when inputs change.',
                                                  'term': 'Side Effects'}],
                             'step_id': 'd58_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'OData V4 slashes payload size, provides powerful sub-expands, and is the '
                                         'native protocol for the ABAP RESTful Application Programming Model.',
                             'title': 'OData V2 vs OData V4: Enterprise Evolution & Differences'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'query': "?$filter=CompanyCode eq 'NM01' and Plant eq "
                                                             "'PL01'&$expand=to_Items($select=Material,OrderQuantity,NetPrice)&$top=2",
                                                    'service_endpoint': '/sap/opu/odata4/sap/zpo_buyer_v4/srvd/sap/zpo_service/0001/PurchaseOrder'},
                             'content_md': '### OData V4 Request & Lean JSON Response\n'
                                           '```http\n'
                                           'GET '
                                           '/sap/opu/odata4/sap/zpo_buyer_v4/srvd/sap/zpo_service/0001/PurchaseOrder?$filter=CompanyCode '
                                           "eq 'NM01' and Plant eq "
                                           "'PL01'&$expand=to_Items($select=Material,OrderQuantity,NetPrice)&$top=2 "
                                           'HTTP/1.1\n'
                                           'Host: s4h.novamfg.com\n'
                                           'Accept: application/json\n'
                                           '```\n'
                                           '\n'
                                           '```json\n'
                                           '{\n'
                                           '  "@odata.context": '
                                           '"$metadata#PurchaseOrder(to_Items(Material,OrderQuantity,NetPrice))",\n'
                                           '  "value": [\n'
                                           '    {\n'
                                           '      "PurchaseOrder": "4500001092",\n'
                                           '      "CompanyCode": "NM01",\n'
                                           '      "Plant": "PL01",\n'
                                           '      "Supplier": "VEND-101",\n'
                                           '      "TotalAmount": 84500.00,\n'
                                           '      "Currency": "EUR",\n'
                                           '      "to_Items": [\n'
                                           '        {\n'
                                           '          "Material": "RAW-01",\n'
                                           '          "OrderQuantity": 500,\n'
                                           '          "NetPrice": 169.00\n'
                                           '        }\n'
                                           '      ]\n'
                                           '    }\n'
                                           '  ]\n'
                                           '}\n'
                                           '```',
                             'scenario': 'Inspect an OData V4 query retrieving active purchase orders and associated '
                                         'line items for Heidelberg (PL01).',
                             'step_id': 'd58_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'OData V4 Payload Inspection: Nova Manufacturing Purchase Orders'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'A mobile warehouse app in Austin (PL02) is draining user data plans due '
                                            'to massive response payloads. Audit the query parameter configuration.',
                             'options': [   {   'explanation': 'Correct! Omitting `$select` and server-side paging '
                                                               '(`$top` / `$skip`) forces the backend to serialize '
                                                               'millions of unwanted attributes.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'The frontend request executes `GET /MaterialSet` without '
                                                        '`$select` or `$top`, fetching all 140 columns and 500,000 '
                                                        'records.'},
                                            {   'explanation': 'HTTPS encryption adds negligible protocol overhead and '
                                                               'is mandatory for enterprise security.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'The OData service is using HTTPS instead of plain unencrypted '
                                                        'HTTP.'},
                                            {   'explanation': 'Disk space issues cause HTTP 500 errors, not excessive '
                                                               'payload serialization.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'The SAP Gateway server is running out of disk space in '
                                                        '`/tmp`.'}],
                             'step_id': 'd58_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Always restrict OData payloads using `$select` for necessary attributes and '
                                         '`$top`/`$skip` for server-side paging.',
                             'title': 'OData Technical Audit: Diagnosing Payload Bloat & Inefficiencies'},
                         {   'instruction': 'What should the board mandate for new services?',
                             'options': [   {   'explanation': 'Correct! OData V4 is the strategic standard for RAP '
                                                               'and modern S/4HANA, offering superior performance and '
                                                               'native draft synchronization.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Mandate OData V4 for all new RAP applications, leveraging '
                                                        'lean JSON payloads, native draft side effects, and enhanced '
                                                        'sub-expands.'},
                                            {   'explanation': 'SOAP XML is heavy and legacy; it cannot power '
                                                               'responsive Fiori Elements frontends.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Mandate SOAP XML Web Services with WS-Security.'},
                                            {   'explanation': 'OData V2 is in maintenance mode for new development '
                                                               'and incurs higher payload and parsing overhead.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Mandate OData V2 because XML payloads are easier for human '
                                                        'developers to read.'}],
                             'scenario': "Nova's architecture board is establishing standards for all new S/4HANA 2023 "
                                         'applications built with the ABAP RESTful Application Programming Model '
                                         '(RAP).',
                             'step_id': 'd58_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Protocol Architecture Challenge: Choosing OData V2 vs V4 for New RAP App'},
                         {   'assessment_type': 'technical_audit',
                             'questions': [   {   'concept_slug': 'odata-protocol-fundamentals',
                                                  'explanation': '`$select` limits returned entity properties, '
                                                                 'minimizing network bandwidth and serialization time.',
                                                  'id': 'd58_q1',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': '$select'},
                                                                 {'id': 'b', 'is_correct': False, 'text': '$filter'},
                                                                 {'id': 'c', 'is_correct': False, 'text': '$orderby'},
                                                                 {'id': 'd', 'is_correct': False, 'text': '$expand'}],
                                                  'prompt': 'Which standard OData system query option instructs the '
                                                            'backend database to return only a specific subset of '
                                                            'entity fields rather than the entire table schema?',
                                                  'question_id': 'd58_q1'},
                                              {   'concept_slug': 'odata-v2-vs-v4',
                                                  'explanation': 'OData V4 eliminates verbose metadata wrappers, '
                                                                 'producing compact JSON responses ideal for web and '
                                                                 'mobile clients.',
                                                  'id': 'd58_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'OData V4 uses a lean JSON format without '
                                                                             'redundant `d.results` wrapper envelopes, '
                                                                             'significantly reducing payload size.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'OData V4 encodes all data inside ZIP '
                                                                             'archives.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'OData V4 replaces JSON with binary '
                                                                             'proprietary SAP formats.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'OData V4 only supports XML payloads.'}],
                                                  'prompt': 'What is a primary architectural advantage of OData V4 '
                                                            'over OData V2 regarding payload format?',
                                                  'question_id': 'd58_q2'},
                                              {   'concept_slug': 'odata-protocol-fundamentals',
                                                  'explanation': '`PATCH` submits delta field updates, leaving '
                                                                 'untouched entity attributes unmodified.',
                                                  'id': 'd58_q3',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'PATCH'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'GET'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'OPTIONS'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'HEAD'}],
                                                  'prompt': 'In an OData service, what HTTP request method is used to '
                                                            'execute a partial update mutating only specific modified '
                                                            'attributes of an entity?',
                                                  'question_id': 'd58_q3'},
                                              {   'concept_slug': 'odata-v2-vs-v4',
                                                  'explanation': 'OData V4 allows powerful nested options like '
                                                                 '`$expand=to_Items($filter=Active eq '
                                                                 'true;$select=Material)`.',
                                                  'id': 'd58_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'OData V4 supports full sub-queries, '
                                                                             'filtering, and paging within the '
                                                                             '`$expand` clause.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'OData V4 prohibits expanding '
                                                                             'associations completely.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'OData V4 requires separate manual HTTP '
                                                                             'calls for every child row.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'OData V4 converts child rows into raw '
                                                                             'CSV strings.'}],
                                                  'prompt': 'How does OData V4 handle nested association retrieval '
                                                            '(`$expand`) compared to OData V2?',
                                                  'question_id': 'd58_q4'}],
                             'step_id': 'd58_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 58 Verification Assessment'},
                         {   'step_id': 'd58_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Analyzed OData RESTful mechanics (EDM, query options `$filter`, '
                                           '`$select`, `$expand`, `$top`).\n'
                                           '- Evaluated architectural differences between OData V2 and V4 (payload '
                                           'compression, nested sub-queries, side-effect annotations).\n'
                                           '- Performed network efficiency audits to eliminate full-table '
                                           'serialization in favor of lean, projected OData requests.',
                             'title': 'Day 58 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd58_s8_completion',
                             'recommended_mission': {'slug': 'nova-odata-v4-optimization', 'title': 'OData V4 Batch Optimization', 'description': 'Refactor inventory queries into efficient OData V4 compound batch operations.'},
                             'step_type': 'completion',
                             'summary_md': 'Excellent progress! You understand the transport protocol between frontend '
                                           'and backend. Tomorrow, you will learn how to publish backend CDS views as '
                                           'live OData services using **SAP Gateway and RAP Service Bindings**.',
                             'title': 'Day 58 Complete: OData Protocol Mastery Achieved'}],
            'subtitle': 'Entity Data Model (EDM), service metadata documents ($metadata), CRUD-Q operations, and batch '
                        'requests.',
            'title': 'OData V2 & OData V4 Protocols'},
    59: {   'atomic_concepts': ['cds-odata-exposure', 'sap-gateway-registration'],
            'day_number': 59,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'exposing-cds-as-odata',
            'steps': [   {   'content_md': '### Methods of Exposing CDS as OData Services\n'
                                           'In SAP S/4HANA, there are three historical and modern methods to transform '
                                           'backend Core Data Services (CDS) view entities into consumable HTTP OData '
                                           'endpoints:\n'
                                           '\n'
                                           '#### 1. Legacy Auto-Exposure (`@OData.publish: true`)\n'
                                           '- Simple annotation added to the header of a CDS view.\n'
                                           '- SADL (Service Adaptation and Description Layer) automatically generates '
                                           'backend Gateway artifacts (`_CDS` service).\n'
                                           '- **Limitation**: Generates only OData V2, lacks transactional write '
                                           'support, and is considered legacy.\n'
                                           '\n'
                                           '#### 2. Classic SEGW (Gateway Service Builder) with SADL Reference\n'
                                           '- Developer creates a project in transaction `SEGW` and references the CDS '
                                           'entity as a data source.\n'
                                           '- Allows manual extension of ABAP model provider (`_MPC_EXT`) and data '
                                           'provider (`_DPC_EXT`) classes.\n'
                                           '- **Limitation**: High maintenance overhead; superseded by modern ABAP '
                                           'Cloud practices.\n'
                                           '\n'
                                           '#### 3. Modern RAP Service Definition & Service Binding (Strategic '
                                           'Standard)\n'
                                           '- **Service Definition**: ABAP repository object declaring which CDS '
                                           'entities and compositions are exposed (`DEFINE SERVICE ZUI_PURCHASEORDER { '
                                           'EXPOSE ZC_PurchaseOrder; EXPOSE ZC_PurchaseOrderItem; }`).\n'
                                           '- **Service Binding**: Binds the Service Definition to a specific protocol '
                                           'and scenario (e.g., `OData V4 - UI` or `OData V2 - Web API`).\n'
                                           '- Provides one-click local testing via the Fiori Elements Preview tool '
                                           'directly in Eclipse ADT.',
                             'key_terms': [   {   'definition': 'Declarative ABAP object specifying which CDS '
                                                                'projection views to expose in a service.',
                                                  'term': 'Service Definition'},
                                              {   'definition': 'Binding associating a Service Definition with an '
                                                                'OData protocol version (V2/V4) and runtime category.',
                                                  'term': 'Service Binding'},
                                              {   'definition': 'Built-in Eclipse ADT development server allowing '
                                                                'instant testing of generated Fiori apps.',
                                                  'term': 'Fiori Elements Preview'}],
                             'step_id': 'd59_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'RAP Service Definitions and Service Bindings represent the modern, Clean '
                                         'Core method for exposing CDS entities via OData V4.',
                             'title': 'Publishing CDS Entities to the Enterprise Gateway'},
                         {   'content_md': '### Runtime Architecture of SAP Gateway\n'
                                           'When an OData service is published in S/4HANA, several architectural '
                                           'layers collaborate:\n'
                                           '\n'
                                           '1. **ICF (Internet Communication Framework)**:\n'
                                           '   - System node path: `/sap/opu/odata/` (V2) or `/sap/opu/odata4/` (V4).\n'
                                           '   - Manages HTTP connection pooling, SSL/TLS negotiation, and '
                                           'authentication (SAML2, OAuth2, X.509, SPNEGO).\n'
                                           '2. **Gateway Service Registration (`/IWFND/MAINT_SERVICE`)**:\n'
                                           '   - In S/4HANA On-Premise/Private Cloud, services must be registered on '
                                           'the Gateway Hub/embedded system.\n'
                                           '   - Assigns a System Alias (directing requests to the local S/4HANA '
                                           'client or remote backend).\n'
                                           '3. **Gateway Error Log & Performance Monitor**:\n'
                                           '   - `/IWFND/ERROR_LOG`: Authoritative diagnostic transaction for '
                                           'analyzing failing HTTP payloads, authorization rejections, and runtime '
                                           'exceptions.\n'
                                           '   - `/IWFND/TRACES`: Measures request latency across network, Gateway '
                                           'framework, and backend database execution.',
                             'key_terms': [   {   'definition': 'Integration server providing secure OData consumption '
                                                                'of S/4HANA business logic.',
                                                  'term': 'SAP Gateway'},
                                              {   'definition': 'HTTP service tree endpoint managing web requests, '
                                                                'handlers, and security settings.',
                                                  'term': 'ICF Node'},
                                              {   'definition': 'Central administrative transaction for diagnosing '
                                                                'Gateway and OData runtime errors.',
                                                  'term': '/IWFND/ERROR_LOG'}],
                             'step_id': 'd59_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Published services map through ICF nodes and Gateway registration tables, '
                                         'monitored centrally via `/IWFND/ERROR_LOG`.',
                             'title': 'Gateway Registration, ICF Nodes & Service Maintenance'},
                         {   'company_context': {   'binding': 'ZUI_SUPPLIER_EVAL_O4',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'definition': 'ZUI_SUPPLIER_EVAL',
                                                    'service_url': '/sap/opu/odata4/sap/zui_supplier_eval_o4/srvd/sap/zui_supplier_eval/0001/'},
                             'content_md': '### Step 1: Define Service Definition (`ZUI_SUPPLIER_EVAL.srvd.srvdsrv`)\n'
                                           '```abap\n'
                                           "@EndUserText.label: 'Supplier Evaluation Service Definition'\n"
                                           'define service ZUI_SUPPLIER_EVAL {\n'
                                           '  expose ZC_SupplierPerformance as Supplier;\n'
                                           '  expose ZC_SupplierDefectItem   as DefectItems;\n'
                                           '}\n'
                                           '```\n'
                                           '\n'
                                           '### Step 2: Define Service Binding (`ZUI_SUPPLIER_EVAL_O4.srvb.binding`)\n'
                                           '- **Binding Type**: `OData V4 - UI`\n'
                                           '- **Service Name**: `ZUI_SUPPLIER_EVAL`\n'
                                           '- **Status**: Activated & Published\n'
                                           '- **Preview**: Clicking `Supplier` launches browser at '
                                           '`https://s4h.novamfg.com/sap/bc/adt/fiori/preview/...` displaying full '
                                           'List Report.',
                             'scenario': 'Nova Manufacturing publishes the Supplier Performance CDS entity for '
                                         'Heidelberg procurement analysts.',
                             'step_id': 'd59_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Exposing Nova Supplier CDS View via RAP Service Binding'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'A buyer reports HTTP 403 when launching the new Supplier Evaluation app. '
                                            'Determine the root cause.',
                             'options': [   {   'explanation': 'Correct! Gateway checks `S_SERVICE` / `S_START` before '
                                                               'allowing HTTP requests to reach the underlying CDS '
                                                               'view.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'The user lacks authorization object `S_SERVICE` (or '
                                                        '`S_START`) for the specific Gateway service name in their '
                                                        'PFCG role.'},
                                            {   'explanation': 'XML views run in the frontend browser; ABAP `COMMIT '
                                                               'WORK` does not exist in frontend client code.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'The developer forgot to run `COMMIT WORK` in the XML view.'},
                                            {   'explanation': 'Table space issues cause database crash or write '
                                                               'errors, not HTTP 403 Forbidden.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'The HANA columnar database run out of table space.'}],
                             'step_id': 'd59_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Gateway service security enforces authorization checks on `S_SERVICE` / '
                                         '`S_START` for every registered endpoint.',
                             'title': 'Gateway Incident Resolution: Resolving HTTP 403 Forbidden on OData Service'},
                         {   'instruction': 'Why is this an architectural violation, and what is the clean core '
                                            'remedy?',
                             'options': [   {   'explanation': 'False. Auto-exposure provides zero automatic '
                                                               'encryption and directly exposes internal data '
                                                               'structures.',
                                                'id': 'opt1',
                                                'is_correct': False,
                                                'text': 'Approve it because `@OData.publish: true` automatically '
                                                        'encrypts all tax identifiers.'},
                                            {   'explanation': 'Correct! Clean Core architecture requires dedicated '
                                                               'projection layers, access control (DCL), and explicit '
                                                               'RAP Service Definitions.',
                                                'id': 'opt2',
                                                'is_correct': True,
                                                'text': 'Reject it: auto-exposure is legacy V2. Build a dedicated '
                                                        'Consumption/Projection View (`ZC_`) excluding sensitive '
                                                        'fields, apply `@AccessControl`, and expose via RAP Service '
                                                        'Definition and Service Binding.'},
                                            {   'explanation': 'Violates corporate data security and regulatory '
                                                               'compliance.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Export the data to an unencrypted CSV file and upload to '
                                                        'Google Drive.'}],
                             'scenario': 'A legacy developer suggests using `@OData.publish: true` on an internal base '
                                         'CDS view containing raw unmasked employee tax identifiers.',
                             'step_id': 'd59_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Gateway Maintenance Challenge: Clean Core Service Exposure'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'cds-odata-exposure',
                                                  'explanation': 'Service Definitions group and expose CDS projection '
                                                                 'entities for service consumption.',
                                                  'id': 'd59_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Service Definition (`.srvd`)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'SE38 Report Program'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Function Module Pool'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Smart Form'}],
                                                  'prompt': 'What is the modern, Clean Core ABAP object used to '
                                                            'declare which CDS entities are exposed together as a '
                                                            'cohesive business service?',
                                                  'question_id': 'd59_q1'},
                                              {   'concept_slug': 'sap-gateway-registration',
                                                  'explanation': '`/IWFND/MAINT_SERVICE` is the core administration '
                                                                 'transaction for Gateway service registration.',
                                                  'id': 'd59_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': '/IWFND/MAINT_SERVICE'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'SE16N'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'SU01'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'SP01'}],
                                                  'prompt': 'Which central transaction in SAP Gateway is used to '
                                                            'register, activate, and monitor OData V2 services on the '
                                                            'NetWeaver hub?',
                                                  'question_id': 'd59_q2'},
                                              {   'concept_slug': 'cds-odata-exposure',
                                                  'explanation': 'Service Bindings configure the protocol (V2/V4), '
                                                                 'category (UI/Web API), and URL path.',
                                                  'id': 'd59_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Service Binding (`.srvb`)'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'Table Type'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Lock Object'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Message Class'}],
                                                  'prompt': 'In the ABAP RESTful Application Programming Model (RAP), '
                                                            'what artifact binds a Service Definition to a specific '
                                                            "runtime protocol such as 'OData V4 - UI'?",
                                                  'question_id': 'd59_q3'},
                                              {   'concept_slug': 'sap-gateway-registration',
                                                  'explanation': '`/IWFND/ERROR_LOG` logs full Gateway error details, '
                                                                 'context, and ABAP exception call stacks.',
                                                  'id': 'd59_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': '/IWFND/ERROR_LOG'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'SE11'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'SCC4'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'RZ10'}],
                                                  'prompt': 'When an HTTP 500 runtime error occurs during OData '
                                                            'execution, which SAP transaction provides the complete '
                                                            'ABAP call stack and diagnostic payload details?',
                                                  'question_id': 'd59_q4'}],
                             'step_id': 'd59_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 59 Verification Assessment'},
                         {   'step_id': 'd59_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Defined and published modern RAP Service Definitions and Service '
                                           'Bindings.\n'
                                           '- Differentiated between legacy `@OData.publish: true` and strategic OData '
                                           'V4 exposure.\n'
                                           '- Diagnosed Gateway authorization (`S_SERVICE`) and runtime errors using '
                                           '`/IWFND/ERROR_LOG`.',
                             'title': 'Day 59 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd59_s8_completion',
                             'recommended_mission': {'slug': 'nova-gateway-service-exposure', 'title': 'Publish Gateway Service for Sales Portal', 'description': 'Register and activate SAP Gateway service for external dealer portal.'},
                             'step_type': 'completion',
                             'summary_md': 'Well done! You can now publish any CDS view as a live OData V4 service. '
                                           'Tomorrow, you will unlock the superpower of modern SAP frontend '
                                           'engineering: **SAP Fiori Elements**.',
                             'title': 'Day 59 Complete: Service Exposure Mastered'}],
            'subtitle': 'Methods of exposure: auto-exposure (@OData.publish: true), SADL mapping, and RAP Service '
                        'Definitions.',
            'title': 'Exposing CDS Entities as OData Services'},
    60: {   'atomic_concepts': ['fiori-elements-paradigm', 'ui-annotations-framework'],
            'day_number': 60,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'fiori-elements-paradigm',
            'steps': [   {   'content_md': '### What is SAP Fiori Elements?\n'
                                           'SAP Fiori Elements provides pre-fabricated, standardized UI floorplans for '
                                           'common enterprise workflows. Instead of manually writing thousands of '
                                           'lines of HTML, CSS, and JavaScript, the frontend UI is **generated '
                                           'entirely at runtime** from OData metadata and **CDS UI annotations**.\n'
                                           '\n'
                                           '#### Why Fiori Elements Dominates S/4HANA Development:\n'
                                           '1. **High Development Velocity**: Up to 80% reduction in frontend '
                                           'development effort. Standard list pages and detail screens require zero '
                                           'JavaScript code.\n'
                                           '2. **Guaranteed Design Consistency**: 100% adherence to SAP Fiori UX '
                                           'guidelines. Whenever SAP updates its theme (e.g., from Quartz to Horizon), '
                                           'all Fiori Elements apps automatically inherit the new styling without code '
                                           'changes.\n'
                                           '3. **Enterprise Quality Out-of-the-Box**: Built-in accessibility '
                                           '(screen-readers, keyboard navigation), cross-device responsiveness, draft '
                                           'autosaving, multi-selection, and export to Excel.\n'
                                           '4. **Maintenance Resilience**: Upgrades to S/4HANA or UI5 framework '
                                           'versions do not break custom JavaScript DOM selectors, because there is no '
                                           'custom JavaScript.',
                             'key_terms': [   {   'definition': 'Framework providing metadata-driven standard UI '
                                                                'floorplans generated from CDS annotations.',
                                                  'term': 'Fiori Elements'},
                                              {   'definition': 'CDS annotations (`@UI.*`) directing the visual '
                                                                'layout, columns, filters, and actions of an '
                                                                'application.',
                                                  'term': 'UI Annotations'},
                                              {   'definition': 'Standardized interaction layout template (List '
                                                                'Report, Object Page, Overview Page, Worklist).',
                                                  'term': 'Floorplan'}],
                             'step_id': 'd60_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Fiori Elements generates responsive, accessible, consistent enterprise UIs '
                                         'at runtime directly from CDS UI annotations.',
                             'title': 'The Metadata-Driven Architecture: Zero Frontend Coding'},
                         {   'content_md': '### Core Annotations vs UI Annotations\n'
                                           'In clean SAP data modeling, annotations are organized into distinct '
                                           'layers:\n'
                                           '\n'
                                           '1. **Data Semantics**:\n'
                                           "   - `@Semantics.amount.currencyCode: 'Currency'`\n"
                                           "   - `@EndUserText.label: 'Total Net Value'`\n"
                                           '2. **UI Annotations (`@UI.*`)**:\n'
                                           '   - Control visual placement, sequence, visual hierarchy, and user '
                                           'interactions.\n'
                                           '   - Reside in the **Consumption / Projection View (`ZC_`)** or in a '
                                           'separate **Metadata Extension (`.ddlx`)**.\n'
                                           '\n'
                                           '#### Metadata Extensions (`.ddlx`): The Clean Core Best Practice\n'
                                           'To keep the primary CDS view clean and prevent accidental modification of '
                                           'data modeling logic, UI annotations should be placed in a **Metadata '
                                           'Extension** file:\n'
                                           '```abap\n'
                                           '@Metadata.layer: #CUSTOMER // or #CORE, #INDUSTRY, #PARTNER\n'
                                           'annotate view ZC_PurchaseOrder with {\n'
                                           '  @UI.lineItem: [{ position: 10, importance: #HIGH }]\n'
                                           '  PurchaseOrder;\n'
                                           '}\n'
                                           '```\n'
                                           'Metadata layers ensure that customer enhancements (`#CUSTOMER`) override '
                                           'core delivered annotations (`#CORE`) without modifying standard SAP code.',
                             'key_terms': [   {   'definition': 'Separate ABAP repository object holding UI '
                                                                'annotations to decouple data logic from presentation.',
                                                  'term': 'Metadata Extension (DDLX)'},
                                              {   'definition': 'Hierarchy (#CORE, #PARTNER, #CUSTOMER) governing '
                                                                'which annotations take precedence.',
                                                  'term': 'Annotation Layering'}],
                             'step_id': 'd60_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Metadata Extensions cleanly separate presentation annotations from CDS data '
                                         'logic and support upgrade-safe layering.',
                             'title': 'Separation of Concerns: CDS Annotation Architecture'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'ddlx_file': 'ZC_PurchaseOrder.ddlx',
                                                    'projection_view': 'ZC_PurchaseOrder'},
                             'content_md': '### Declarative Metadata Extension (`ZC_PurchaseOrder.ddlx`)\n'
                                           '```abap\n'
                                           '@Metadata.layer: #CUSTOMER\n'
                                           '@UI: {\n'
                                           '  headerInfo: {\n'
                                           "    typeName: 'Purchase Order',\n"
                                           "    typeNamePlural: 'Purchase Orders',\n"
                                           "    title: { type: #STANDARD, value: 'PurchaseOrder' }\n"
                                           '  }\n'
                                           '}\n'
                                           'annotate view ZC_PurchaseOrder with {\n'
                                           '  @UI.facet: [\n'
                                           "    { id: 'GeneralInfo', purpose: #STANDARD, type: "
                                           "#IDENTIFICATION_REFERENCE, label: 'General Information', position: 10 }\n"
                                           '  ]\n'
                                           '\n'
                                           '  @UI.lineItem: [{ position: 10, importance: #HIGH }]\n'
                                           '  @UI.selectionField: [{ position: 10 }]\n'
                                           '  PurchaseOrder;\n'
                                           '\n'
                                           '  @UI.lineItem: [{ position: 20, importance: #HIGH }]\n'
                                           '  @UI.selectionField: [{ position: 20 }]\n'
                                           '  Supplier;\n'
                                           '\n'
                                           '  @UI.lineItem: [{ position: 30 }]\n'
                                           '  TotalAmount;\n'
                                           '}\n'
                                           '```',
                             'scenario': 'Nova Manufacturing decorates the Purchase Order projection view with UI '
                                         'annotations to instantly produce an enterprise List Report.',
                             'step_id': 'd60_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Metadata Extension: Purchase Order Report'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "Nova's development team needs to build 40 standard master data and "
                                            'document management screens. Choose the development strategy.',
                             'options': [   {   'explanation': 'Correct! Fiori Elements handles standard search, '
                                                               'filter, detail, and edit operations with 80% lower '
                                                               'development and maintenance costs.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Adopt SAP Fiori Elements using CDS Views and Metadata '
                                                        'Extensions, reserving freestyle UI5 only for bespoke '
                                                        'non-standard visual layouts.'},
                                            {   'explanation': 'Massive maintenance overhead, high risk of '
                                                               'inconsistent UI patterns, and severe vulnerability to '
                                                               'framework upgrades.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Code all 40 applications as freestyle UI5 with custom '
                                                        'JavaScript controllers and CSS flexboxes.'},
                                            {   'explanation': 'Direct external SQL bypasses S/4HANA security, '
                                                               'business logic, authorization, and violates Clean '
                                                               'Core.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Write custom PHP pages connecting via direct SQL queries to '
                                                        'the HANA database.'}],
                             'step_id': 'd60_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Adopt Fiori Elements as the default enterprise standard; restrict freestyle '
                                         'UI5 to unique, non-standard visual requirements.',
                             'title': 'Architectural Evaluation: Freestyle UI5 vs Fiori Elements'},
                         {   'instruction': 'What is the Clean Core approach?',
                             'options': [   {   'explanation': 'Correct! CDS extensions and `#CUSTOMER` metadata '
                                                               'extensions provide upgrade-safe, non-destructive '
                                                               'customization.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Create a CDS View Extension extending the standard projection '
                                                        'view, and create a Metadata Extension at `@Metadata.layer: '
                                                        '#CUSTOMER`.'},
                                            {   'explanation': 'Modifying standard SAP core code directly destroys '
                                                               'upgrade safety and voids support warranties.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Directly modify the SAP standard CDS view in package `S_CORE` '
                                                        'using an emergency access key.'},
                                            {   'explanation': 'Browser injection scripts are fragile, insecure, and '
                                                               'completely unsupported in enterprise environments.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Inject raw JavaScript via browser monkey-patching scripts.'}],
                             'scenario': 'A business unit wants to add three custom fields to a standard SAP-delivered '
                                         'Fiori Elements List Report without modifying SAP standard code.',
                             'step_id': 'd60_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Clean Core Challenge: Modifying Standard Fiori Elements UI'},
                         {   'assessment_type': 'mcq',
                             'questions': [   {   'concept_slug': 'fiori-elements-paradigm',
                                                  'explanation': 'Fiori Elements reads OData service metadata and '
                                                                 '`@UI.*` annotations to instantiate standard UI '
                                                                 'controls dynamically.',
                                                  'id': 'd60_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'OData metadata and CDS UI annotations'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Hand-written jQuery plugins'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Windows registry configuration keys'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Static HTML table tags'}],
                                                  'prompt': 'In the SAP Fiori Elements paradigm, what primarily drives '
                                                            'the generation of the user interface layout and '
                                                            'interactive controls?',
                                                  'question_id': 'd60_q1'},
                                              {   'concept_slug': 'ui-annotations-framework',
                                                  'explanation': 'Metadata Extensions decouple presentation '
                                                                 'annotations from data modeling and support '
                                                                 'upgrade-safe layering.',
                                                  'id': 'd60_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To isolate UI annotations into a '
                                                                             'separate, layered artifact without '
                                                                             'cluttering the underlying data model '
                                                                             'view.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To compress disk space in the HANA '
                                                                             'indexserver.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To bypass user authorization checks.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To compile ABAP into Python scripts.'}],
                                                  'prompt': 'What is the primary architectural purpose of using a '
                                                            'Metadata Extension (`.ddlx`) in CDS?',
                                                  'question_id': 'd60_q2'},
                                              {   'concept_slug': 'fiori-elements-paradigm',
                                                  'explanation': 'The `#CUSTOMER` layer overrides `#PARTNER`, '
                                                                 '`#INDUSTRY`, and `#CORE` annotations.',
                                                  'id': 'd60_q3',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': '#CUSTOMER'},
                                                                 {'id': 'b', 'is_correct': False, 'text': '#CORE'},
                                                                 {'id': 'c', 'is_correct': False, 'text': '#INDUSTRY'},
                                                                 {'id': 'd', 'is_correct': False, 'text': '#LOCAL'}],
                                                  'prompt': 'Which metadata layer in a Metadata Extension has the '
                                                            'highest priority and overrides core SAP annotations?',
                                                  'question_id': 'd60_q3'},
                                              {   'concept_slug': 'ui-annotations-framework',
                                                  'explanation': 'Fiori Elements guarantees UX consistency and upgrade '
                                                                 'safety because the frontend template engine is '
                                                                 'maintained by SAP.',
                                                  'id': 'd60_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Automatic adherence to Fiori UX '
                                                                             'standards and zero-cost theme updates '
                                                                             'during S/4HANA upgrades.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Ability to write low-level C++ code '
                                                                             'inside the browser.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Exemption from user licensing '
                                                                             'requirements.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Direct access to non-SAP relational '
                                                                             'databases without APIs.'}],
                                                  'prompt': 'Which of the following is a major enterprise advantage of '
                                                            'Fiori Elements over Freestyle UI5 development?',
                                                  'question_id': 'd60_q4'}],
                             'step_id': 'd60_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 60 Verification Assessment'},
                         {   'step_id': 'd60_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered the Fiori Elements metadata-driven application model.\n'
                                           '- Decoupled presentation from data logic using CDS Metadata Extensions '
                                           '(`.ddlx`).\n'
                                           '- Applied annotation layers (`#CUSTOMER`, `#CORE`) to implement '
                                           'upgrade-resilient customizations.',
                             'title': 'Day 60 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd60_s8_completion',
                             'recommended_mission': {'slug': 'nova-fiori-elements-eval', 'title': 'Fiori Elements vs Freestyle Strategy', 'description': 'Conduct architectural appraisal for new shop floor tablet UI.'},
                             'step_type': 'completion',
                             'summary_md': 'Phenomenal achievement! You understand how annotations generate enterprise '
                                           'UIs. Tomorrow, you will master the specific annotations that govern tables '
                                           'and filters: **@UI.lineItem and @UI.selectionField**.',
                             'title': 'Day 60 Complete: Fiori Elements Paradigm Mastered'}],
            'subtitle': 'Eliminating custom UI coding: driving frontend application rendering entirely through CDS '
                        'annotations.',
            'title': 'Fiori Elements Paradigm: Metadata-Driven UIs'},
    61: {   'atomic_concepts': ['ui-lineitem-annotations', 'ui-selectionfields-annotations'],
            'day_number': 61,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'ui-annotations-lineitem-selection',
            'steps': [   {   'content_md': '### Constructing Standard List Pages via Annotations\n'
                                           'In an SAP Fiori Elements List Report, the two most fundamental visual '
                                           'structures are the **Smart Filter Bar** (top) and the **Responsive Table** '
                                           '(bottom).\n'
                                           '\n'
                                           '#### 1. `@UI.selectionField`: The Smart Filter Bar\n'
                                           '- Placing `@UI.selectionField: [{ position: 10 }]` on a CDS field '
                                           'instantly places an input filter control into the filter bar.\n'
                                           '- Value helps (search helps) bound to the field '
                                           '(`@Consumption.valueHelpDefinition`) automatically generate dropdown '
                                           'selection modals without frontend code.\n'
                                           '\n'
                                           '#### 2. `@UI.lineItem`: Table Columns and Actions\n'
                                           '- Placing `@UI.lineItem: [{ position: 10, importance: #HIGH }]` defines a '
                                           'visible column in the table.\n'
                                           '- **Attributes of `@UI.lineItem`**:\n'
                                           '  - `position`: Numeric ordering from left to right (e.g., 10, 20, 30).\n'
                                           '  - `importance`: `#HIGH`, `#MEDIUM`, `#LOW`. Governs responsive column '
                                           'hiding on smaller tablet/mobile viewports.\n'
                                           '  - `label`: Overrides default data element text.\n'
                                           '  - `type`: `#STANDARD`, `#FOR_ACTION` (buttons in table rows), '
                                           '`#WITH_URL` (hyperlinks).\n'
                                           '  - `criticality`: Binds the text/badge color to a status code '
                                           '(1=Red/Error, 2=Yellow/Warning, 3=Green/Success).',
                             'key_terms': [   {   'definition': 'CDS annotation configuring table columns, row '
                                                                'positions, priorities, and action buttons.',
                                                  'term': '@UI.lineItem'},
                                              {   'definition': 'CDS annotation placing a field into the top filter '
                                                                'bar of a List Report.',
                                                  'term': '@UI.selectionField'},
                                              {   'definition': 'Visual color coding (red, yellow, green, grey) bound '
                                                                'dynamically to numeric status fields.',
                                                  'term': 'Criticality'}],
                             'step_id': 'd61_s1_learn',
                             'step_type': 'learn',
                             'takeaway': '@UI.selectionField renders filter inputs, while @UI.lineItem configures '
                                         'columns, priority responsiveness, and row actions.',
                             'title': 'Core Table & Filter Annotations: LineItem & SelectionField'},
                         {   'content_md': '### Enriching the Metadata Model\n'
                                           'Beyond table columns and filters, advanced annotations provide vital '
                                           'enterprise polish:\n'
                                           '\n'
                                           '#### 1. `@UI.headerInfo`\n'
                                           'Placed at the entity level to declare singular and plural titles:\n'
                                           '```abap\n'
                                           '@UI.headerInfo: {\n'
                                           "  typeName: 'Sensor Requisition',\n"
                                           "  typeNamePlural: 'Sensor Requisitions',\n"
                                           "  title: { type: #STANDARD, value: 'RequisitionID' },\n"
                                           "  description: { value: 'MaterialDescription' }\n"
                                           '}\n'
                                           '```\n'
                                           '\n'
                                           '#### 2. Criticality Calculation Pushdown\n'
                                           'Rather than hardcoding colors in JavaScript, calculate criticality '
                                           'directly in the CDS View:\n'
                                           '```abap\n'
                                           'case \n'
                                           "  when ApprovalStatus = 'APPROVED' then 3 // Green\n"
                                           "  when ApprovalStatus = 'REJECTED' then 1 // Red\n"
                                           '  else 2                                  // Yellow (Pending)\n'
                                           'end as StatusCriticality\n'
                                           '```\n'
                                           "Then bind `@UI.lineItem: [{ position: 30, criticality: 'StatusCriticality' "
                                           '}]` to field `ApprovalStatus`.\n'
                                           '\n'
                                           '#### 3. Cross-App Intent-Based Navigation '
                                           '(`#WITH_INTENT_BASED_NAVIGATION`)\n'
                                           'Allows clicking a Supplier ID to navigate seamlessly to the standard '
                                           'Supplier Fact Sheet:\n'
                                           '```abap\n'
                                           "@Consumption.semanticObject: 'Supplier'\n"
                                           '@UI.lineItem: [{ position: 20, type: #WITH_INTENT_BASED_NAVIGATION, '
                                           "semanticObjectAction: 'manage' }]\n"
                                           'SupplierID;\n'
                                           '```',
                             'key_terms': [   {   'definition': 'Entity-level annotation defining object titles, '
                                                                'counts, and breadcrumbs.',
                                                  'term': '@UI.headerInfo'},
                                              {   'definition': 'Cross-application routing resolved dynamically via '
                                                                'Semantic Objects and Actions.',
                                                  'term': 'Intent-Based Navigation'},
                                              {   'definition': 'Data-driven UI color mapping evaluating business '
                                                                'health indicators directly in CDS.',
                                                  'term': 'Status Criticality'}],
                             'step_id': 'd61_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Criticality logic should be calculated in the CDS view, and semantic '
                                         'navigation enables seamless cross-app drill-downs.',
                             'title': 'HeaderInfo, Identification & Semantic Object Navigation'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'material': 'DXTR-1000',
                                                    'plant': 'PL02',
                                                    'view': 'ZC_InventoryMonitor'},
                             'content_md': '### Complete Annotations in `ZC_InventoryMonitor.ddlx`\n'
                                           '```abap\n'
                                           '@Metadata.layer: #CUSTOMER\n'
                                           '@UI.headerInfo: {\n'
                                           "  typeName: 'Stock Overview',\n"
                                           "  typeNamePlural: 'Stock Overviews'\n"
                                           '}\n'
                                           'annotate view ZC_InventoryMonitor with {\n'
                                           '  @UI.selectionField: [{ position: 10 }]\n'
                                           '  @UI.lineItem: [{ position: 10, importance: #HIGH }]\n'
                                           '  Plant;\n'
                                           '\n'
                                           '  @UI.selectionField: [{ position: 20 }]\n'
                                           '  @UI.lineItem: [{ position: 20, importance: #HIGH }]\n'
                                           '  Material;\n'
                                           '\n'
                                           '  @UI.lineItem: [{ position: 30, importance: #HIGH, criticality: '
                                           "'StockCriticality' }]\n"
                                           '  UnrestrictedStock;\n'
                                           '\n'
                                           '  @UI.lineItem: [{ position: 40, importance: #MEDIUM }]\n'
                                           '  SafetyStock;\n'
                                           '}\n'
                                           '```',
                             'scenario': "Nova's inventory manager at Austin (PL02) requires a real-time monitor for "
                                         'controller component DXTR-1000 with visual shortage alerts.',
                             'step_id': 'd61_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Inventory Monitor Metadata Definition'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "Design the annotation configuration so that 'Total Spend' remains visible "
                                            "on smartphones, while 'Created By' is hidden on small screens.",
                             'options': [   {   'explanation': 'Correct! Fiori Elements uses the `importance` property '
                                                               'to automatically drop `#LOW` and `#MEDIUM` columns on '
                                                               'mobile viewports.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': "Set `importance: #HIGH` on 'Total Spend' and `importance: "
                                                        "#LOW` on 'Created By' in `@UI.lineItem`."},
                                            {   'explanation': 'Violates Fiori Elements architecture and breaks '
                                                               'responsive table recalculation.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Write a CSS media query in a custom stylesheet hiding the '
                                                        'third `<td>` element.'},
                                            {   'explanation': 'Destroys underlying audit data required for '
                                                               'compliance.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': "Delete 'Created By' from the database table completely."}],
                             'step_id': 'd61_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Use `importance: #HIGH/#MEDIUM/#LOW` to govern responsive column disclosure '
                                         'without custom CSS.',
                             'title': 'CDS UI Annotation Modeling: Configuring Responsive Table Columns'},
                         {   'instruction': 'How do you correct the filter bar sequence in the Metadata Extension?',
                             'options': [   {   'explanation': 'Correct! The `position` value in `@UI.selectionField` '
                                                               'strictly dictates the left-to-right ordering of filter '
                                                               'controls.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Adjust the `position` integers inside `@UI.selectionField`: '
                                                        'assign CompanyCode position 10, Plant position 20, and '
                                                        'Document Notes position 100.'},
                                            {   'explanation': 'Database column names do not govern Fiori Elements '
                                                               'visual filter sequencing.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Rename the database columns alphabetically.'},
                                            {   'explanation': 'Personalization should not be used as a workaround for '
                                                               'flawed default metadata modeling.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Tell the user to drag and drop filters every time they open '
                                                        'their browser.'}],
                             'scenario': 'A user complains that the filter bar in their new Fiori app displays '
                                         "'Document Notes' before 'Company Code' and 'Plant', forcing them to scroll "
                                         'horizontally.',
                             'step_id': 'd61_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Annotation Modeling Challenge: Inverted Filter Ordering'},
                         {   'assessment_type': 'data_modeling',
                             'questions': [   {   'concept_slug': 'ui-lineitem-annotations',
                                                  'explanation': 'The `position` integer defines relative column order '
                                                                 'from left to right.',
                                                  'id': 'd61_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'position (e.g. `position: 10`)'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'sortOrder'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'columnID'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'indexKey'}],
                                                  'prompt': 'Which CDS annotation property determines the sequence '
                                                            'order of columns rendered in a Fiori Elements responsive '
                                                            'table?',
                                                  'question_id': 'd61_q1'},
                                              {   'concept_slug': 'ui-selectionfields-annotations',
                                                  'explanation': '`@UI.selectionField` automatically generates filter '
                                                                 'controls in the filter bar.',
                                                  'id': 'd61_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': '@UI.selectionField'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': '@UI.filterInput'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': '@UI.searchBar'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': '@UI.queryParameter'}],
                                                  'prompt': 'Which annotation is placed on a CDS view attribute to '
                                                            'expose it as an input filter field in the Fiori Elements '
                                                            'Smart Filter Bar?',
                                                  'question_id': 'd61_q2'},
                                              {   'concept_slug': 'ui-lineitem-annotations',
                                                  'explanation': 'Criticality binds visual state colors (1=Error/Red, '
                                                                 '2=Warning/Yellow, 3=Success/Green) to data '
                                                                 'attributes.',
                                                  'id': 'd61_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It colors table cell values or status '
                                                                             'badges (e.g., Red, Yellow, Green) based '
                                                                             'on the numeric value of the referenced '
                                                                             'field.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It marks the database row as read-only.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It alerts the SAP basis team via SMS.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It encrypts the column using AES-256.'}],
                                                  'prompt': "What does assigning `criticality: 'CriticalityField'` in "
                                                            '`@UI.lineItem` accomplish?',
                                                  'question_id': 'd61_q3'},
                                              {   'concept_slug': 'ui-lineitem-annotations',
                                                  'explanation': 'Lower importance columns are gracefully collapsed '
                                                                 'into pop-in rows on compact viewports.',
                                                  'id': 'd61_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'The column is hidden from the primary '
                                                                             'table view to preserve layout space, '
                                                                             'accessible via pop-in details.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'The column is permanently deleted from '
                                                                             'the database.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'The app crashes with an OutOfMemory '
                                                                             'exception.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'The font is reduced to 2 pixels.'}],
                                                  'prompt': 'In mobile responsive design, what occurs when a column '
                                                            'has `@UI.lineItem: [{ importance: #LOW }]` on a '
                                                            'smartphone?',
                                                  'question_id': 'd61_q4'}],
                             'step_id': 'd61_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 61 Verification Assessment'},
                         {   'step_id': 'd61_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Modeled `@UI.lineItem` columns with precise ordering, responsive '
                                           'priorities, and data-driven criticality.\n'
                                           '- Configured `@UI.selectionField` filter bars with search helps.\n'
                                           '- Embedded semantic object navigation for cross-application operational '
                                           'workflows.',
                             'title': 'Day 61 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd61_s8_completion',
                             'recommended_mission': {'slug': 'nova-cds-ui-annotations-refactor', 'title': 'CDS UI Annotation Refactoring', 'description': 'Enhance List Report metadata with dynamic line items and selection fields.'},
                             'step_type': 'completion',
                             'summary_md': 'Superb work! You can now generate production-grade list and filter views. '
                                           'Tomorrow, you will combine the List Report with its companion floorplan: '
                                           'the **Object Page**.',
                             'title': 'Day 61 Complete: Table & Filter Modeling Mastered'}],
            'subtitle': '@UI.lineItem, @UI.selectionField, @UI.headerInfo, and @UI.identification for standard list '
                        'pages.',
            'title': 'UI Annotations: LineItem & SelectionFields'},
    62: {   'atomic_concepts': ['list-report-floorplan', 'object-page-floorplan', 'facet-navigation'],
            'day_number': 62,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'fiori-elements-list-report-object-page',
            'steps': [   {   'content_md': '### The Workhorse Pattern of S/4HANA\n'
                                           'Over 70% of standard transactional and operational applications in S/4HANA '
                                           'follow the **List Report & Object Page (LR/OP)** floorplan combination.\n'
                                           '\n'
                                           '#### The Dual Floorplan Architecture:\n'
                                           '1. **List Report (Parent Level)**:\n'
                                           '   - **Purpose**: Search, filter, sort, and batch-evaluate collections of '
                                           'root business entities (e.g., all Purchase Orders for Company Code '
                                           '`NM01`).\n'
                                           '   - Key UI elements: Filter Bar, Table Toolbar (Create, Delete, Export to '
                                           'Excel), Responsive Table.\n'
                                           '2. **Object Page (Child Level)**:\n'
                                           '   - **Purpose**: Contextual 360-degree deep-dive into a single selected '
                                           'business object (e.g., Purchase Order `4500001092`).\n'
                                           '   - Displays header attributes, KPI micro-charts, editable form fields, '
                                           'and nested child tables (e.g., line items, delivery schedules, approval '
                                           'history).\n'
                                           '   - Serves as the primary canvas for transactional editing, draft state '
                                           'persistence, and business actions.',
                             'key_terms': [   {   'definition': 'Standard Fiori floorplan for querying, filtering, and '
                                                                'navigating large collections of business objects.',
                                                  'term': 'List Report'},
                                              {   'definition': 'Deep-dive detail floorplan displaying header KPIs, '
                                                                'form sections, and child compositions for a single '
                                                                'entity.',
                                                  'term': 'Object Page'},
                                              {   'definition': 'Split-screen layout allowing the List Report and '
                                                                'Object Page to display side-by-side.',
                                                  'term': 'Flexible Column Layout (FCL)'}],
                             'step_id': 'd62_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'The List Report filters and lists records; the Object Page provides '
                                         'comprehensive detail and transactional editing.',
                             'title': 'The List Report & Object Page (LR/OP) Floorplan Pattern'},
                         {   'content_md': '### Structuring the Object Page Layout\n'
                                           'The Object Page is divided into two major architectural regions governed '
                                           'entirely by CDS annotations:\n'
                                           '\n'
                                           '#### 1. Header Area (`@UI.headerFacets`)\n'
                                           '- Pinned at the top of the object page.\n'
                                           '- Contains key high-level status cards, KPI micro-charts, contact '
                                           'information, and primary document identifiers.\n'
                                           '- Types of header facets: DataPoints (`@UI.dataPoint`), FieldGroups, and '
                                           'Chart facets.\n'
                                           '\n'
                                           '#### 2. Body Sections & Facets (`@UI.facet`)\n'
                                           '- The main scrolling canvas organized into **Sections** and '
                                           '**Subsections** via facet trees.\n'
                                           '- Common Facet Types:\n'
                                           '  - `#COLLECTION`: Container facet grouping multiple sub-facets into an '
                                           'anchor tab.\n'
                                           '  - `#IDENTIFICATION_REFERENCE`: Form group displaying fields annotated '
                                           'with `@UI.identification`.\n'
                                           '  - `#FIELDGROUP_REFERENCE`: Custom named form group (e.g., *Shipping '
                                           'Details*, *Accounting Assignment*).\n'
                                           '  - `#LINEITEM_REFERENCE`: Child table rendering associated child entities '
                                           '(e.g., Purchase Order Items via association `to_Items`).',
                             'key_terms': [   {   'definition': 'Annotation constructing the hierarchical tabs, '
                                                                'sections, and tables of an Object Page.',
                                                  'term': '@UI.facet'},
                                              {   'definition': 'Pinned top region displaying key status DataPoints '
                                                                'and micro-charts.',
                                                  'term': '@UI.headerFacets'},
                                              {   'definition': 'Facet linking an association to render an embedded '
                                                                'child entity table.',
                                                  'term': '#LINEITEM_REFERENCE'}],
                             'step_id': 'd62_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Object Pages are structured into pinned Header Facets and scrolling Body '
                                         'Sections (@UI.facet) rendering child tables and form groups.',
                             'title': 'Object Page Facet Navigation & Header Facets'},
                         {   'company_context': {   'child_target': 'ZC_PurchaseOrderItem',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'object_page_target': 'ZC_PurchaseOrder'},
                             'content_md': '### Object Page Facet Tree Definition\n'
                                           '```abap\n'
                                           'annotate view ZC_PurchaseOrder with {\n'
                                           '  // HEADER FACET: Total Net Order Value\n'
                                           '  @UI.headerFacets: [\n'
                                           "    { id: 'NetValFacet', type: #DATAPOINT_REFERENCE, targetQualifier: "
                                           "'NetValDP', position: 10 }\n"
                                           '  ]\n'
                                           '\n'
                                           '  // BODY FACET 1: General Information Form\n'
                                           '  @UI.facet: [\n'
                                           "    { id: 'GeneralSection', purpose: #STANDARD, type: #COLLECTION, label: "
                                           "'General Info', position: 10 },\n"
                                           "    { id: 'GeneralGroup', parentId: 'GeneralSection', type: "
                                           '#IDENTIFICATION_REFERENCE, position: 10 },\n'
                                           '\n'
                                           '  // BODY FACET 2: Embedded Child Items Table\n'
                                           "    { id: 'ItemsSection', purpose: #STANDARD, type: #LINEITEM_REFERENCE, \n"
                                           "      targetElement: '_Items', label: 'Ordered Components', position: 20 "
                                           '}\n'
                                           '  ]\n'
                                           '\n'
                                           "  @UI.dataPoint: { qualifier: 'NetValDP', title: 'Total PO Value' }\n"
                                           '  TotalNetAmount;\n'
                                           '}\n'
                                           '```',
                             'scenario': 'Inspect the facet hierarchy configuring the Object Page for Purchase Order '
                                         '`4500001092` at Heidelberg (PL01).',
                             'step_id': 'd62_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Purchase Order Object Page Hierarchy'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'A developer needs to embed a table of delivery schedule lines inside the '
                                            'Purchase Order Item Object Page. Select the correct annotation pattern.',
                             'options': [   {   'explanation': 'Correct! `#LINEITEM_REFERENCE` combined with '
                                                               "`targetElement` renders the child entity's "
                                                               '`@UI.lineItem` annotations as an embedded table.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Add a facet of type `#LINEITEM_REFERENCE` with '
                                                        "`targetElement: '_ScheduleLines'` pointing to the child "
                                                        'association.'},
                                            {   'explanation': 'Raw jQuery breaks Fiori Elements lifecycle and OData '
                                                               'V4 batch synchronization.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Write a custom jQuery AJAX loop inside `index.html`.'},
                                            {   'explanation': 'Destroys relational modeling, sorting, and inline '
                                                               'editing capabilities.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Concatenate all schedule lines into a single comma-separated '
                                                        'string inside a text area.'}],
                             'step_id': 'd62_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Embed child collections using `#LINEITEM_REFERENCE` targeting the child '
                                         'association.',
                             'title': 'Object Page Architectural Decision: Embedding Child Entity Tables'},
                         {   'instruction': 'How can the frontend architect eliminate this friction without writing '
                                            'custom code?',
                             'options': [   {   'explanation': 'Correct! Flexible Column Layout (FCL) renders the List '
                                                               'Report in the left column and the Object Page in the '
                                                               'right column side-by-side.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': "Enable Flexible Column Layout (`fcl`) in the application's "
                                                        '`manifest.json` routing configuration.'},
                                            {   'explanation': 'Consumes excessive client memory and fails to provide '
                                                               'cohesive multi-document workflow.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Instruct users to open 50 separate browser tabs '
                                                        'simultaneously.'},
                                            {   'explanation': 'Violates Fiori design principles and makes the List '
                                                               'Report completely unreadable.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Remove the Object Page and force all 200 fields into the List '
                                                        'Report table.'}],
                             'scenario': 'Purchasers complain that clicking a row in the List Report causes a '
                                         'full-page transition to the Object Page, forcing them to lose their scroll '
                                         'position and filter context.',
                             'step_id': 'd62_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Floorplan Challenge: Flexible Column Layout (FCL) User Experience'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'list-report-floorplan',
                                                  'explanation': 'The List Report pairs a Smart Filter Bar for '
                                                                 'querying with a Responsive Table for results '
                                                                 'display.',
                                                  'id': 'd62_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Smart Filter Bar and Responsive Table'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Command Prompt and Hex Editor'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Chat Window and Video Player'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Static PDF Viewer and Excel Pivot '
                                                                             'Table'}],
                                                  'prompt': 'What are the two primary user interface regions that '
                                                            'compose a standard SAP Fiori Elements List Report?',
                                                  'question_id': 'd62_q1'},
                                              {   'concept_slug': 'object-page-floorplan',
                                                  'explanation': '`#LINEITEM_REFERENCE` embeds child table collections '
                                                                 'declared in the entity model.',
                                                  'id': 'd62_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': '#LINEITEM_REFERENCE'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': '#IDENTIFICATION_REFERENCE'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': '#DATAPOINT_REFERENCE'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': '#URL_REFERENCE'}],
                                                  'prompt': 'Which facet type in `@UI.facet` is used to embed an '
                                                            'editable table of child entities (such as invoice line '
                                                            'items) into an Object Page?',
                                                  'question_id': 'd62_q2'},
                                              {   'concept_slug': 'facet-navigation',
                                                  'explanation': 'Header facets display key status indicators and '
                                                                 'DataPoints in the pinned top summary region.',
                                                  'id': 'd62_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'In the pinned top header area above the '
                                                                             'main scrolling body content.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'In the browser URL bar.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'At the very bottom of the footer '
                                                                             'toolbar.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Inside a floating popup dialog.'}],
                                                  'prompt': 'Where are `@UI.headerFacets` visually displayed on a '
                                                            'Fiori Elements Object Page?',
                                                  'question_id': 'd62_q3'},
                                              {   'concept_slug': 'list-report-floorplan',
                                                  'explanation': 'FCL delivers split-screen master-detail '
                                                                 'productivity, keeping list context visible while '
                                                                 'inspecting details.',
                                                  'id': 'd62_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It displays the List Report and Object '
                                                                             'Page side-by-side in resizable '
                                                                             'master-detail columns.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It changes the database storage from '
                                                                             'column store to row store.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It translates English text into German '
                                                                             'automatically.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It compresses video streams.'}],
                                                  'prompt': 'What capability does the Flexible Column Layout (FCL) '
                                                            'provide in modern Fiori Elements applications?',
                                                  'question_id': 'd62_q4'}],
                             'step_id': 'd62_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 62 Verification Assessment'},
                         {   'step_id': 'd62_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Constructed complete List Report & Object Page floorplans using pure CDS '
                                           'metadata.\n'
                                           '- Organized multi-level facet trees (`#COLLECTION`, '
                                           '`#IDENTIFICATION_REFERENCE`, `#LINEITEM_REFERENCE`).\n'
                                           '- Implemented Flexible Column Layout (FCL) master-detail patterns for '
                                           'high-throughput enterprise users.',
                             'title': 'Day 62 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd62_s8_completion',
                             'recommended_mission': {'slug': 'nova-list-report-object-page-flow', 'title': 'List Report to Object Page Flow', 'description': 'Wire end-to-end drill-down navigation for DXTR-1000 manufacturing records.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You have mastered the core workhorse floorplan of S/4HANA. '
                                           'Tomorrow, you will learn how to build executive visual dashboards using '
                                           '**Overview Pages (OVP) and Analytical Cards**.',
                             'title': 'Day 62 Complete: LR/OP Floorplans Mastered'}],
            'subtitle': 'Constructing standard enterprise apps: List Report for searching/filtering + Object Page for '
                        'detail viewing.',
            'title': 'Fiori Elements Floorplans: List Report & Object Page'},
    63: {   'atomic_concepts': ['overview-page-ovp', 'analytical-cards-ovp'],
            'day_number': 63,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'overview-page-ovp',
            'steps': [   {   'content_md': '### The Strategic Role of Overview Pages\n'
                                           'While the List Report is designed for operational task execution, the '
                                           '**Overview Page (OVP)** serves as an interactive, role-based visual '
                                           'dashboard for managers, plant directors, and team leads.\n'
                                           '\n'
                                           '#### Key Architectural Characteristics of OVP:\n'
                                           '1. **Card-Based Dashboard**: The OVP surface is composed of responsive, '
                                           'resizable **Cards**. Each card focuses on a specific business domain '
                                           '(e.g., *Top 5 Overdue Suppliers*, *Scrap Rate by Work Center*, *Pending '
                                           'Requisitions*).\n'
                                           '2. **Global Filter Bar**: A unified Smart Filter Bar at the top filters '
                                           'all cards on the page simultaneously (e.g., selecting Plant `PL01` '
                                           'instantly updates all procurement, inventory, and cost cards).\n'
                                           '3. **Actionable Navigation**: Clicking an item or header on an OVP card '
                                           'triggers semantic navigation directly into a detailed List Report or '
                                           'Object Page with pre-filtered parameters.',
                             'key_terms': [   {   'definition': 'Card-based dashboard floorplan aggregating analytical '
                                                                'and transactional cards for a business role.',
                                                  'term': 'Overview Page (OVP)'},
                                              {   'definition': 'Top-level filter bar applying parameter filters '
                                                                'across all cards simultaneously on an OVP.',
                                                  'term': 'Global Filter'},
                                              {   'definition': 'Modular UI container rendering lists, tables, charts, '
                                                                'or KPIs linked to an underlying OData entity set.',
                                                  'term': 'Card'}],
                             'step_id': 'd63_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Overview Pages provide executive visual dashboards uniting analytical '
                                         'charts, lists, and KPI cards with global filtering.',
                             'title': 'Executive Dashboards: The Overview Page (OVP) Floorplan'},
                         {   'content_md': '### Taxonomy of OVP Cards\n'
                                           'An OVP dashboard supports five canonical card architectures configured in '
                                           '`manifest.json` and driven by CDS annotations:\n'
                                           '\n'
                                           '1. **Analytical Chart Card**:\n'
                                           '   - Renders interactive charts: Donut, Line, Bar, Bubble, Heatmap.\n'
                                           '   - Driven by `@UI.chart` annotations defining dimensions and measures.\n'
                                           '2. **List Card & Table Card**:\n'
                                           '   - Displays top-N records (e.g., *Top 5 Critical Backorders*).\n'
                                           '   - Driven by `@UI.lineItem` annotations.\n'
                                           '3. **KPI / Numeric Tag Card**:\n'
                                           '   - Large prominent header displaying a single headline metric (e.g., '
                                           '*Plant Scrap Rate: 2.1%*) with trend indicator arrows.\n'
                                           '   - Driven by `@UI.dataPoint` annotations.\n'
                                           '4. **Quick View Card**:\n'
                                           '   - Contact or vendor card displaying address, telephone, and direct '
                                           'action triggers.\n'
                                           '5. **Component Card**:\n'
                                           '   - Custom embedded UI5 control for non-standard visualizations.',
                             'key_terms': [   {   'definition': 'CDS annotation declaring chart type, category '
                                                                'dimensions, and measure aggregations for card '
                                                                'rendering.',
                                                  'term': '@UI.chart'},
                                              {   'definition': 'Prominent numerical card displaying high-level metric '
                                                                'trends and status color thresholds.',
                                                  'term': 'KPI Tag Card'},
                                              {   'definition': 'OVP card embedding visual data charts directly onto '
                                                                'the dashboard.',
                                                  'term': 'Analytical Card'}],
                             'step_id': 'd63_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'OVP cards range from analytical charts (@UI.chart) and lists (@UI.lineItem) '
                                         'to KPI DataPoints (@UI.dataPoint).',
                             'title': 'OVP Card Types & CDS Analytical Annotations'},
                         {   'company_context': {   'cards': [   {   'title': 'On-Time Assembly Rate (DXTR-1000)',
                                                                     'trend': 'Rising',
                                                                     'type': 'KPI Tag Card',
                                                                     'value': '98.4%'},
                                                                 {   'chart': 'Bar',
                                                                     'dim': 'WorkCenter',
                                                                     'measure': 'ScrapAmount',
                                                                     'title': 'Scrap Cost by Work Center',
                                                                     'type': 'Bar Chart Card'},
                                                                 {   'count': 3,
                                                                     'title': 'Critical Stock Shortages (RAW-01)',
                                                                     'type': 'Table Card'}],
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'ovp_name': 'Nova Plant Operations Dashboard'},
                             'content_md': '### OVP Manifest Configuration Snippet (`manifest.json`)\n'
                                           '```json\n'
                                           '"sap.ovp": {\n'
                                           '  "globalFilterModel": "mainModel",\n'
                                           '  "cards": {\n'
                                           '    "card_scrap_cost": {\n'
                                           '      "model": "mainModel",\n'
                                           '      "template": "sap.ovp.cards.charts.analytical",\n'
                                           '      "settings": {\n'
                                           '        "title": "Scrap Cost by Work Center",\n'
                                           '        "entitySet": "ScrapAnalytics",\n'
                                           '        "chartAnnotationPath": '
                                           '"com.sap.vocabularies.UI.v1.Chart#ScrapChart"\n'
                                           '      }\n'
                                           '    },\n'
                                           '    "card_shortages": {\n'
                                           '      "model": "mainModel",\n'
                                           '      "template": "sap.ovp.cards.table",\n'
                                           '      "settings": {\n'
                                           '        "title": "Critical Shortages",\n'
                                           '        "entitySet": "StockAlerts",\n'
                                           '        "annotationPath": '
                                           '"com.sap.vocabularies.UI.v1.LineItem#ShortagesTable"\n'
                                           '      }\n'
                                           '    }\n'
                                           '  }\n'
                                           '}\n'
                                           '```',
                             'scenario': "Nova's Plant Director in Heidelberg monitors real-time operations via a "
                                         'dedicated Plant Overview Page.',
                             'step_id': 'd63_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Executive Plant Dashboard: Heidelberg (PL01)'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'The Plant Director changes the global filter from Heidelberg (`PL01`) to '
                                            'Austin (`PL02`), but the Shortage Table card fails to update. Diagnose '
                                            'the configuration error.',
                             'options': [   {   'explanation': 'Correct! Global filters only cascade to cards whose '
                                                               'underlying entity set contains the filtered property.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'The entity set backing the Shortage Table card does not '
                                                        'expose `Plant` as a filterable property in its OData '
                                                        'metadata.'},
                                            {   'explanation': 'Reinstalling the operating system has zero relevance '
                                                               'to OData filter propagation.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'The user did not clear their browser cache and reinstall '
                                                        'Windows.'},
                                            {   'explanation': 'OVP supports global filtering on any valid property '
                                                               'exposed by the entity sets.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'OVP does not support filtering by Plant.'}],
                             'step_id': 'd63_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Ensure all card entity sets expose matching filter properties to participate '
                                         'in OVP global filtering.',
                             'title': 'OVP Configuration Simulation: Global Filter Integration'},
                         {   'instruction': 'Why is this an architectural violation, and what is the remediation?',
                             'options': [   {   'explanation': 'Correct! Fiori UX standards recommend 5 to 9 cards per '
                                                               'dashboard to maintain snappy performance and decision '
                                                               'clarity.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'It causes extreme browser DOM lag and cognitive overload. '
                                                        'Apply Fiori guidelines: limit the OVP to 5–9 high-priority '
                                                        'cards focused on the primary role persona.'},
                                            {   'explanation': 'Violates Fiori simple design principles and creates '
                                                               'unmaintainable performance bottlenecks.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Approve it because enterprise managers expect maximum visual '
                                                        'complexity.'},
                                            {   'explanation': 'Static images eliminate real-time interactivity, '
                                                               'filtering, and live enterprise data.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Convert all 28 cards into static JPEG screenshots.'}],
                             'scenario': 'A junior consultant configures an Overview Page with 28 analytical cards, 12 '
                                         'charts, and 14 tables on a single screen.',
                             'step_id': 'd63_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Dashboard Design Challenge: Avoiding Cognitive Overload'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'overview-page-ovp',
                                                  'explanation': 'The Global Filter synchronizes parameter filtering '
                                                                 'across all cards rendered on the OVP.',
                                                  'id': 'd63_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To apply filter criteria simultaneously '
                                                                             'across all cards on the dashboard '
                                                                             'sharing common entity properties.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To filter out spam emails from the '
                                                                             "user's inbox."},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To block unauthorized users from logging '
                                                                             'into the Launchpad.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To encrypt the database storage '
                                                                             'volume.'}],
                                                  'prompt': 'What is the primary role of the Global Filter Bar in an '
                                                            'SAP Fiori Overview Page (OVP)?',
                                                  'question_id': 'd63_q1'},
                                              {   'concept_slug': 'analytical-cards-ovp',
                                                  'explanation': '`@UI.chart` defines chart visualization semantics '
                                                                 'for analytical cards.',
                                                  'id': 'd63_q2',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': '@UI.chart'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': '@UI.lineItem'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': '@UI.selectionField'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': '@UI.identification'}],
                                                  'prompt': 'Which CDS annotation is primarily responsible for '
                                                            'defining the chart type, category dimensions, and '
                                                            'aggregation measures for an OVP Analytical Card?',
                                                  'question_id': 'd63_q2'},
                                              {   'concept_slug': 'overview-page-ovp',
                                                  'explanation': 'Clicking OVP cards navigates seamlessly to deep '
                                                                 'operational transactional apps via intent-based '
                                                                 'navigation.',
                                                  'id': 'd63_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It triggers semantic navigation, opening '
                                                                             'the detailed List Report or Object Page '
                                                                             'pre-filtered for that record.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It closes the browser window '
                                                                             'immediately.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It reboots the application server.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It converts the application into an '
                                                                             'Excel spreadsheet.'}],
                                                  'prompt': 'What user interaction occurs when clicking on an item '
                                                            'inside an OVP List Card?',
                                                  'question_id': 'd63_q3'},
                                              {   'concept_slug': 'analytical-cards-ovp',
                                                  'explanation': 'Fiori design guidelines advise 5 to 9 cards to '
                                                                 'maintain optimal performance and executive focus.',
                                                  'id': 'd63_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': '5 to 9 cards'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': '50 to 100 cards'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Exactly 1 card'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Unlimited cards'}],
                                                  'prompt': 'What is the recommended limit for the number of active '
                                                            'cards on an Overview Page to prevent performance '
                                                            'degradation and cognitive fatigue?',
                                                  'question_id': 'd63_q4'}],
                             'step_id': 'd63_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 63 Verification Assessment'},
                         {   'step_id': 'd63_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Architected role-based Overview Pages (OVP) uniting operational lists '
                                           'and analytical charts.\n'
                                           '- Configured `@UI.chart` and `@UI.dataPoint` annotations for card '
                                           'rendering.\n'
                                           '- Implemented global filtering and intent-based navigation linking '
                                           'executive dashboards to transactional drill-downs.',
                             'title': 'Day 63 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd63_s8_completion',
                             'recommended_mission': {'slug': 'nova-ovp-dashboard-assembly', 'title': 'Overview Page Cards Assembly', 'description': 'Design multi-card analytical dashboard for plant executive review.'},
                             'step_type': 'completion',
                             'summary_md': 'Brilliant work! You now understand the full suite of Fiori Elements '
                                           'floorplans. Tomorrow, you will tackle the comprehensive **Phase 5 Capstone '
                                           '& Security Audit**.',
                             'title': 'Day 63 Complete: Overview Pages Mastered'}],
            'subtitle': 'Configuring executive dashboards: List cards, Table cards, Bar chart cards, and KPI tag '
                        'cards.',
            'title': 'Overview Pages (OVP) & Analytical Cards'},
    64: {   'atomic_concepts': ['fiori-ux-synthesis'],
            'day_number': 64,
            'estimated_minutes': 90,
            'recommended_mission_slug': None,
            'slug': 'fiori-enterprise-ux-capstone',
            'steps': [   {   'content_md': '### Synthesizing the Modern Enterprise UX Stack\n'
                                           'In Phase 5, you have traversed the entire modern S/4HANA user experience '
                                           'architecture:\n'
                                           '1. **Design Strategy**: 5 Core Principles (Role-Based, Adaptive, Coherent, '
                                           'Simple, Delightful) and 3 App Types.\n'
                                           '2. **Central Portal**: Modern FLP Spaces & Pages decoupled from Business '
                                           'Catalog entitlements.\n'
                                           '3. **Frontend Runtime**: SAPUI5 MVC framework with two-way data binding '
                                           'and declarative XML views.\n'
                                           '4. **Transport Layer**: OData V2 and V4 RESTful protocols with database '
                                           'pushdown.\n'
                                           '5. **Service Exposure**: RAP Service Definitions, Service Bindings, and '
                                           'Gateway registration.\n'
                                           '6. **Metadata-Driven UX**: Fiori Elements List Reports, Object Pages, and '
                                           'Overview Pages driven by `@UI.*` annotations.\n'
                                           '\n'
                                           '#### The Capstone Challenge:\n'
                                           'Nova Manufacturing Corp is inaugurating its state-of-the-art Robotics '
                                           'Integration facility at Austin (Plant `PL02`). As Enterprise Lead '
                                           'Architect, you must conduct a rigorous architectural and security audit of '
                                           'the newly deployed Procurement & Production UX suite before global '
                                           'rollout.',
                             'key_terms': [   {   'definition': 'End-to-end alignment of business roles, Launchpad '
                                                                'spaces, OData protocols, and Fiori floorplans.',
                                                  'term': 'UX Synthesis'},
                                              {   'definition': 'Verification of authorization objects, ICF node '
                                                                'protections, and role segregation across UX layers.',
                                                  'term': 'Security Audit'}],
                             'step_id': 'd64_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Enterprise UX architecture unites frontend floorplans, OData protocol '
                                         'efficiency, and role-based security governance.',
                             'title': 'Phase 5 Capstone: End-to-End Enterprise UX Architecture'},
                         {   'content_md': '### The Architectural Audit Checklist\n'
                                           'Before signing off on an enterprise Fiori deployment, verify compliance '
                                           'across four critical architectural dimensions:\n'
                                           '\n'
                                           '1. **Authorization & RBAC**:\n'
                                           '   - Are Business Catalogs strictly aligned to Job Roles in PFCG?\n'
                                           '   - Is Gateway service authorization (`S_SERVICE` / `S_START`) restricted '
                                           'without wildcard (`*`) access?\n'
                                           '   - Do CDS views enforce row-level Data Control Language '
                                           '(`@AccessControl.authorizationCheck: #CHECK`)?\n'
                                           '2. **Performance & Payload Optimization**:\n'
                                           '   - Are OData requests leveraging `$select` and `$top` to prevent memory '
                                           'blowouts?\n'
                                           '   - Do analytical cards push down aggregations to HANA column engines '
                                           'rather than calculating in JavaScript?\n'
                                           '3. **Upgrade Safety (Clean Core)**:\n'
                                           '   - Are UI modifications encapsulated in Metadata Extensions (`.ddlx`) at '
                                           'layer `#CUSTOMER`?\n'
                                           '   - Are custom extensions using released C1 APIs rather than internal SAP '
                                           'structures?\n'
                                           '4. **Ergonomics & Accessibility**:\n'
                                           '   - Do List Reports configure `importance: #HIGH/#LOW` for responsive '
                                           'mobile behavior?\n'
                                           '   - Are all interactive elements accessible via standard keyboard tab '
                                           'navigation?',
                             'key_terms': [   {   'definition': 'Verification that extensions use released APIs and '
                                                                'layered metadata without core modification.',
                                                  'term': 'Clean Core Audit'},
                                              {   'definition': 'Mandatory CDS annotation enforcing DCL access rules '
                                                                'on database queries.',
                                                  'term': 'Authorization Check #CHECK'}],
                             'step_id': 'd64_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Enterprise sign-off demands strict verification of PFCG authorization, '
                                         'payload efficiency, DCL security, and Clean Core layering.',
                             'title': 'Security, Governance & Clean Core Audit Checklist'},
                         {   'company_context': {   'architecture_flow': 'Browser -> Fiori Launchpad (Spaces/Pages) -> '
                                                                         'OData V4 -> Gateway -> SADL -> CDS View '
                                                                         'Entity (DCL) -> HANA Column Store '
                                                                         '(ACDOCA/MATDOC)',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'plant': 'PL02',
                                                    'system': 'S/4HANA Cloud Private Edition 2023'},
                             'content_md': '### Complete End-to-End Request Pipeline\n'
                                           '```\n'
                                           '[User Browser: Buyer in Austin PL02]\n'
                                           '         │  HTTPS / OData V4 Request (Lean JSON)\n'
                                           '         ▼\n'
                                           '[SAP Web Dispatcher / Reverse Proxy]\n'
                                           '         │  SAML 2.0 / OAuth2 Authentication\n'
                                           '         ▼\n'
                                           '[Internet Communication Framework (ICF)]\n'
                                           '         │  /sap/opu/odata4/sap/zui_po_manage_o4/\n'
                                           '         ▼\n'
                                           '[SAP Gateway & Service Binding Layer]\n'
                                           '         │  Authorization Check: S_SERVICE, S_START\n'
                                           '         ▼\n'
                                           '[SADL & RAP Transactional Engine]\n'
                                           '         │  Evaluates Metadata Extension (@Metadata.layer: #CUSTOMER)\n'
                                           '         ▼\n'
                                           '[CDS View Entity & DCL Access Control]\n'
                                           "         │  DCL checks Plant = 'PL02' AND CompanyCode = 'NM01'\n"
                                           '         ▼\n'
                                           '[HANA Database Indexserver]\n'
                                           '         │  Columnar Inverted Index Scan & Join Pruning\n'
                                           '         ▼\n'
                                           '[Persistent Storage: ACDOCA / MATDOC]\n'
                                           '```',
                             'scenario': "Review the full-stack architectural blueprint connecting the buyer's browser "
                                         'in Austin to the S/4HANA core.',
                             'step_id': 'd64_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Full Stack Architecture Audit: Austin (PL02)'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'An external penetration test identifies that warehouse clerks in Austin '
                                            'can view confidential executive salaries by modifying URL parameters in '
                                            'their browser. Remediate the flaw.',
                             'options': [   {   'explanation': 'CSS hiding is cosmetic; the sensitive salary data is '
                                                               'still transmitted over the network in the OData JSON '
                                                               'response.',
                                                'id': 'a',
                                                'is_correct': False,
                                                'text': 'Hide the salary column in the XML view using CSS `display: '
                                                        'none`.'},
                                            {   'explanation': 'Correct! True enterprise security must be enforced in '
                                                               'the backend CDS/DCL layer; never rely on frontend UI '
                                                               'hiding for data protection.',
                                                'id': 'b',
                                                'is_correct': True,
                                                'text': 'Enforce backend Data Control Language (`DCL`) with '
                                                        '`@AccessControl.authorizationCheck: #CHECK`, and eliminate '
                                                        'the salary attribute from the operational CDS projection '
                                                        'view.'},
                                            {   'explanation': 'Administrative policies cannot substitute for robust '
                                                               'technical authorization controls.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Ask warehouse clerks to sign an NDA promising not to inspect '
                                                        'browser developer tools.'}],
                             'step_id': 'd64_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Security must be enforced at the backend CDS/DCL layer; frontend hiding does '
                                         'not prevent data interception.',
                             'title': 'Enterprise Security Audit: Remediating High-Risk UX Vulnerabilities'},
                         {   'instruction': 'How do you defend the SAP Fiori Elements / S/4HANA architecture?',
                             'options': [   {   'explanation': 'Correct! Fiori Elements provides deep S/4HANA '
                                                               'transactional and security alignment that bespoke '
                                                               'external frameworks cannot match without massive '
                                                               'custom code.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Fiori Elements delivers native S/4HANA integration, automatic '
                                                        'draft persistence, zero-effort theme upgrades, out-of-the-box '
                                                        'accessibility, and 80% lower lifecycle maintenance, while '
                                                        'external SPAs require building custom middleware, auth '
                                                        'synchronization, and manual re-implementation of SAP business '
                                                        'logic.'},
                                            {   'explanation': 'Inaccurate. Fiori Elements is technically superior for '
                                                               'standard ERP object workflows due to metadata-driven '
                                                               'runtime generation.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Admit that React.js would have been faster, but SAP contracts '
                                                        'require using only SAP products.'},
                                            {   'explanation': 'Unacceptable regression violating all modern '
                                                               'enterprise UX standards.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Propose abandoning web browsers and returning to terminal '
                                                        'screens.'}],
                             'scenario': 'The CIO challenges your decision to build the new Nova Manufacturing '
                                         'procurement portal using Fiori Elements and RAP OData V4 instead of hiring a '
                                         'third-party agency to build a React.js single-page application.',
                             'step_id': 'd64_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Phase 5 Capstone Defense: Architectural Sign-Off'},
                         {   'assessment_type': 'capstone_quiz',
                             'questions': [   {   'concept_slug': 'fiori-ux-synthesis',
                                                  'explanation': 'Backend DCL and authorization checks provide '
                                                                 'tamper-proof security regardless of client behavior.',
                                                  'id': 'd64_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'In backend CDS Access Control rules '
                                                                             '(DCL) and PFCG authorization objects.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Exclusively in the frontend XML view '
                                                                             'using CSS styles.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'In browser localStorage variables.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'In the client-side JavaScript '
                                                                             'controller.'}],
                                                  'prompt': 'In a production S/4HANA deployment, where must row-level '
                                                            'authorization and segregation of duties be '
                                                            'authoritatively enforced to prevent unauthorized data '
                                                            'exposure?',
                                                  'question_id': 'd64_q1'},
                                              {   'concept_slug': 'fiori-ux-synthesis',
                                                  'explanation': 'The List Report provides powerful filtering, '
                                                                 'sorting, multi-selection, and batch-action '
                                                                 'execution.',
                                                  'id': 'd64_q2',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'List Report'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Quick View Card'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Analytical Bubble Chart'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Fact Sheet'}],
                                                  'prompt': 'Which Fiori Elements floorplan is optimal for an '
                                                            'operational procurement specialist who needs to search, '
                                                            'filter, and batch-approve hundreds of purchase '
                                                            'requisitions daily?',
                                                  'question_id': 'd64_q2'},
                                              {   'concept_slug': 'fiori-ux-synthesis',
                                                  'explanation': 'Layered Metadata Extensions (`#CUSTOMER`) cleanly '
                                                                 'override core annotations without modifying base '
                                                                 'objects.',
                                                  'id': 'd64_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'CDS Metadata Extensions created at layer '
                                                                             '`#CUSTOMER`.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Editing core SAP code in transaction '
                                                                             'SE38.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Disabling S/4HANA quarterly release '
                                                                             'upgrades.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Storing UI code on an external FTP '
                                                                             'server.'}],
                                                  'prompt': 'What Clean Core mechanism guarantees that customer UI '
                                                            'enhancements survive standard S/4HANA upgrades without '
                                                            'modification conflicts?',
                                                  'question_id': 'd64_q3'},
                                              {   'concept_slug': 'fiori-ux-synthesis',
                                                  'explanation': 'OData V4 and RAP deliver lean payloads, native draft '
                                                                 'handling, and full Clean Core compliance.',
                                                  'id': 'd64_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'OData V4 paired with the ABAP RESTful '
                                                                             'Application Programming Model (RAP)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'SOAP XML paired with Function Modules'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'OData V2 paired with direct raw table '
                                                                             'updates'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'ODBC connections directly over the '
                                                                             'public internet'}],
                                                  'prompt': 'What modern protocol combination represents the strategic '
                                                            'standard for building high-performance, transactional '
                                                            'Fiori Elements applications in S/4HANA 2023?',
                                                  'question_id': 'd64_q4'}],
                             'step_id': 'd64_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Phase 5 Comprehensive Capstone Assessment'},
                         {   'step_id': 'd64_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Comprehensive Phase 5 Benchmark Achieved:\n'
                                           '- **Full UX Stack Synthesis**: Mastered design principles, FLP '
                                           'Spaces/Pages, SAPUI5 MVC, OData V2/V4, and Fiori Elements floorplans '
                                           '(LR/OP/OVP).\n'
                                           '- **Security & Authorization Audit**: Enforced strict PFCG catalog '
                                           'assignments, Gateway `S_SERVICE` boundaries, and backend CDS DCL data '
                                           'protection.\n'
                                           '- **Clean Core Governance**: Implemented layered Metadata Extensions '
                                           '(`#CUSTOMER`) and modern RAP Service Bindings.',
                             'title': 'Phase 5 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd64_s8_completion',
                             'recommended_mission': {'slug': 'nova-enterprise-ux-capstone', 'title': 'Enterprise UX & Fiori Capstone', 'description': 'Final validation and deployment defense of Nova UX suite.'},
                             'step_type': 'completion',
                             'summary_md': 'Congratulations! You have completed Phase 5: SAP Fiori & Enterprise UX. '
                                           'You now possess deep, end-to-end expertise in modern enterprise user '
                                           'experiences. In **Phase 6 (Days 65–76)**, you will master the principles '
                                           'of **S/4HANA Cloud & Clean Core** (SAP Activate, Key-User & Developer '
                                           'Extensibility, and Cloud Migration).',
                             'title': 'Phase 5 Complete: Enterprise UX & Fiori Elements Certified'}],
            'subtitle': 'Phase 5 benchmark: building and deploying a secure, responsive Fiori Elements app on custom '
                        'CDS entity.',
            'title': 'Enterprise UX Capstone & Security Audit'}}
