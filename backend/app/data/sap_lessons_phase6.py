"""Authoritative content definitions for SAP S/4HANA Guided Learning Days 65–76 (Phase 6).

Phase 6: S/4HANA Cloud & Clean Core (Activate, Extensibility, CBC, Migration, Testing, Cutover, Capstone).
Enterprise Continuous Model: Nova Manufacturing Corp (NM01)
"""

from __future__ import annotations
from typing import Any

PHASE_6_DAYS_CONTENT: dict[int, dict[str, Any]] = {   65: {   'atomic_concepts': ['s4hana-cloud-editions', 'cloud-governance-models'],
            'day_number': 65,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 's4hana-cloud-flavors',
            'steps': [   {   'content_md': '### The Spectrum of S/4HANA Cloud Deployments\n'
                                           'SAP S/4HANA is offered across distinct deployment editions tailored to '
                                           'organizational agility, customization requirements, and regulatory '
                                           'sovereignty:\n'
                                           '\n'
                                           '#### 1. SAP S/4HANA Cloud Public Edition (SaaS)\n'
                                           '- **Multi-Tenant SaaS**: Shared infrastructure and software stack managed '
                                           '100% by SAP.\n'
                                           '- **Release Cadence**: Semi-annual continuous innovation updates '
                                           'automatically applied by SAP.\n'
                                           '- **Configuration**: Exclusively via SAP Central Business Configuration '
                                           '(CBC) with standard SAP Best Practices scope items.\n'
                                           '- **Extensibility**: Strict Clean Core. Only Key-User extensibility and '
                                           'On-Stack Developer Extensibility (ABAP Cloud) using released C1 APIs. '
                                           '**Zero modifications to SAP core code.**\n'
                                           '- **Infrastructure**: Hyper-scaler cloud managed by SAP.\n'
                                           '\n'
                                           '#### 2. SAP S/4HANA Cloud Private Edition (IaaS / Managed Cloud)\n'
                                           '- **Single-Tenant Dedicated**: Dedicated virtual instance running in '
                                           'customer-selected hyperscaler (AWS, Azure, GCP) or SAP data center.\n'
                                           '- **Release Cadence**: Customer-managed annual upgrades with extended '
                                           'mainstream maintenance support.\n'
                                           '- **Configuration**: Complete access to classic SPRO (Implementation '
                                           'Guide) plus CBC support.\n'
                                           '- **Extensibility**: Supports the full Clean Core model, while still '
                                           'permitting classic ABAP and modifications where legally or technically '
                                           'necessary for brownfield transitions.\n'
                                           '\n'
                                           '#### 3. S/4HANA On-Premise\n'
                                           '- Customer-managed in private data centers; identical technical codebase '
                                           'to Private Cloud.',
                             'key_terms': [   {   'definition': 'Multi-tenant SaaS deployment with mandatory Clean '
                                                                'Core, automated upgrades, and standardized Best '
                                                                'Practices.',
                                                  'term': 'Public Cloud Edition'},
                                              {   'definition': 'Single-tenant managed cloud offering full ERP '
                                                                'functional scope with controlled upgrade timing.',
                                                  'term': 'Private Cloud Edition'},
                                              {   'definition': 'Architectural principle strictly decoupling standard '
                                                                'SAP code from customizations via released APIs.',
                                                  'term': 'Clean Core'}],
                             'step_id': 'd65_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Public Cloud provides maximum standardization with automatic updates; '
                                         'Private Cloud provides dedicated single-tenant flexibility.',
                             'title': 'SAP S/4HANA Deployment Models: Public Cloud vs Private Cloud'},
                         {   'content_md': '### Evaluating the Enterprise Decision Matrix\n'
                                           'Selecting between Public and Private Cloud fundamentally shapes an '
                                           "enterprise's operating model:\n"
                                           '\n'
                                           '| Governance Dimension | S/4HANA Cloud Public Edition | S/4HANA Cloud '
                                           'Private Edition |\n'
                                           '|---|---|---|\n'
                                           '| **Custom ABAP Code** | Only ABAP Cloud (restricted syntax, released '
                                           'APIs) | Full ABAP stack + ABAP Cloud support |\n'
                                           '| **IMG Configuration** | Central Business Configuration (CBC) | Full SPRO '
                                           '+ CBC |\n'
                                           '| **System Landscapes** | 3SL (Dev, Test, Prod tenants) | 3-tier, 4-tier, '
                                           'or multi-track landscapes |\n'
                                           '| **OS / DB Root Access** | Zero access (managed entirely by SAP) | '
                                           'Restricted basis access (SAP ECS managed) |\n'
                                           '| **Upgrade Ownership** | SAP-driven semi-annual upgrades | '
                                           'Customer-driven annual upgrade projects |\n'
                                           '| **TCO Profile** | Lowest operational TCO; predictable SaaS subscription '
                                           '| Balanced TCO with tailored modernization pace |',
                             'key_terms': [   {   'definition': 'Cloud deployment topology comprising Development, '
                                                                'Test, and Production tenants.',
                                                  'term': '3-System Landscape (3SL)'},
                                              {   'definition': 'Enterprise Cloud Services: SAP managed services team '
                                                                'responsible for private cloud infrastructure.',
                                                  'term': 'SAP ECS'}],
                             'step_id': 'd65_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Public Cloud maximizes SaaS standardization and low TCO; Private Cloud '
                                         'balances cloud agility with deep legacy process preservation.',
                             'title': 'Cloud Governance Models & Total Cost of Ownership (TCO)'},
                         {   'company_context': {   'austin_choice': 'S/4HANA Cloud Public Edition (100% standard best '
                                                                     'practices)',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'heidelberg_choice': 'S/4HANA Cloud Private Edition (preserving '
                                                                         'custom device protocols)',
                                                    'integration': 'Two-Tier ERP connected via SAP Integration Suite '
                                                                   '(BTP)'},
                             'content_md': '### Nova Manufacturing Two-Tier ERP Blueprint\n'
                                           '```\n'
                                           '[Corporate HQ & Heavy Assembly: Heidelberg PL01]\n'
                                           '         S/4HANA Cloud Private Edition\n'
                                           '  ├── Full manufacturing routings & custom sensor drivers\n'
                                           '  └── Classical subledger integrations\n'
                                           '         │\n'
                                           '         │  SAP Integration Suite (BTP) / Master Data Integration\n'
                                           '         ▼\n'
                                           '[Agile Innovation Hub: Austin Tech Center PL02]\n'
                                           '         S/4HANA Cloud Public Edition\n'
                                           '  ├── 100% SAP Best Practices standard scope items\n'
                                           '  ├── Automated semi-annual feature upgrades\n'
                                           '  └── Zero custom modifications (Clean Core)\n'
                                           '```',
                             'scenario': 'Nova Manufacturing evaluates its global landscape: Heidelberg (PL01) has 20 '
                                         'years of complex specialized machinery interfaces, while Austin (PL02) is a '
                                         'brand-new greenfield robotics facility.',
                             'step_id': 'd65_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Dual-Cloud Strategy: Heidelberg vs Austin'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'Evaluate the customer requirements and select the appropriate S/4HANA '
                                            'Cloud edition.',
                             'options': [   {   'explanation': 'Correct! Greenfield deployments with standardized '
                                                               'requirements achieve the highest ROI and lowest '
                                                               'maintenance on Public Cloud.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Choose S/4HANA Cloud Public Edition for a greenfield '
                                                        'subsidiary requiring rapid 12-week deployment and zero custom '
                                                        'ABAP modifications.'},
                                            {   'explanation': 'Impossible. Public Cloud strictly prohibits '
                                                               'un-refactored legacy dynpros and direct database '
                                                               'modifications.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Attempt to install 500 legacy un-refactored SAP GUI dynpro '
                                                        'screens onto S/4HANA Cloud Public Edition.'},
                                            {   'explanation': 'Obsolete legacy technology that violates all modern '
                                                               'corporate architecture strategies.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Revert to an on-premise mainframe running R/3 4.6C.'}],
                             'step_id': 'd65_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Public Cloud is the premier choice for greenfield standardization; legacy '
                                         'brownfield requirements require Private Cloud.',
                             'title': 'Deployment Decision Matrix: Evaluating Greenfield vs Brownfield Cloud'},
                         {   'instruction': 'As Cloud Architect, how do you explain the SaaS operating model?',
                             'options': [   {   'explanation': 'Correct! In true SaaS, tenant upgrades cannot be '
                                                               'deferred; organizations leverage automated test tools '
                                                               'to validate releases smoothly.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Explain that in Public Cloud SaaS, upgrades are mandatory and '
                                                        'automatic to guarantee security, continuous innovation, and '
                                                        'shared infrastructure stability. Automated regression tests '
                                                        'must be executed during the 2-week test window.'},
                                            {   'explanation': 'Violates SLAs and causes complete system downtime.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Agree to unplug the SAP datacenter network cables during the '
                                                        'upgrade weekend.'},
                                            {   'explanation': 'SAP does not freeze versions for individual tenants in '
                                                               'Public Cloud.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Promise that SAP will make an exception and freeze their '
                                                        'cloud version forever.'}],
                             'scenario': 'A business manager on S/4HANA Cloud Public Edition demands to delay a '
                                         'mandatory SAP semi-annual release upgrade by two years because the sales '
                                         'team is busy.',
                             'step_id': 'd65_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Cloud Governance Challenge: Mandated Semi-Annual Upgrades'},
                         {   'assessment_type': 'decision_matrix',
                             'questions': [   {   'concept_slug': 's4hana-cloud-editions',
                                                  'explanation': 'Public Edition is the fully managed multi-tenant '
                                                                 'SaaS offering.',
                                                  'id': 'd65_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'S/4HANA Cloud Public Edition'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'S/4HANA Cloud Private Edition'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'S/4HANA On-Premise'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'SAP ECC 6.0'}],
                                                  'prompt': 'Which S/4HANA deployment edition is a multi-tenant SaaS '
                                                            'solution with semi-annual upgrades managed entirely by '
                                                            'SAP and zero access to classic SPRO?',
                                                  'question_id': 'd65_q1'},
                                              {   'concept_slug': 'cloud-governance-models',
                                                  'explanation': 'Central Business Configuration (CBC) is the central '
                                                                 'configuration engine for Public Cloud.',
                                                  'id': 'd65_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'SAP Central Business Configuration '
                                                                             '(CBC)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Transaction SE11'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'MS Excel Macros'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'SAP Solution Manager'}],
                                                  'prompt': 'In S/4HANA Cloud Public Edition, which tool is used for '
                                                            'scoping, organizational structure setup, and business '
                                                            'configuration instead of classic SPRO?',
                                                  'question_id': 'd65_q2'},
                                              {   'concept_slug': 's4hana-cloud-editions',
                                                  'explanation': 'Private Edition offers full functional breadth and '
                                                                 'supports brownfield conversion of existing systems.',
                                                  'id': 'd65_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It supports gradual code modernization '
                                                                             'while permitting classic ABAP and '
                                                                             'modifications where necessary.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It does not require any user licenses.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It eliminates the need for database '
                                                                             'backups.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It runs inside a web browser without '
                                                                             'internet access.'}],
                                                  'prompt': 'What is an architectural benefit of S/4HANA Cloud Private '
                                                            'Edition over Public Edition for brownfield enterprise '
                                                            'transformations?',
                                                  'question_id': 'd65_q3'},
                                              {   'concept_slug': 'cloud-governance-models',
                                                  'explanation': 'Modern Public Cloud delivers a standardized 3-System '
                                                                 'Landscape (3SL).',
                                                  'id': 'd65_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': '3-System Landscape (Development, Test, '
                                                                             'and Production tenants)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Single all-in-one tenant without '
                                                                             'testing'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': '10 independent developer laptops'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Paper-based sandbox'}],
                                                  'prompt': 'What is the standard tenant landscape architecture '
                                                            'delivered for customers implementing S/4HANA Cloud Public '
                                                            'Edition?',
                                                  'question_id': 'd65_q4'}],
                             'step_id': 'd65_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 65 Verification Assessment'},
                         {   'step_id': 'd65_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Differentiated S/4HANA Cloud Public vs Private Edition across '
                                           'governance, upgrades, configuration, and TCO.\n'
                                           '- Designed a Two-Tier ERP architecture uniting standardized cloud '
                                           'subsidiaries with heavy industrial manufacturing plants.\n'
                                           '- Established cloud governance guidelines for automated release '
                                           'management.',
                             'title': 'Day 65 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd65_s8_completion',
                             'recommended_mission': {'slug': 'nova-cloud-edition-selection', 'title': 'Public vs Private Cloud Decision Matrix', 'description': 'Analyze regulatory and customization requirements for Nova expansion.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You understand the cloud deployment landscape. Tomorrow, you '
                                           'will master the cardinal architectural rule of modern SAP engineering: '
                                           '**The Clean Core Philosophy**.',
                             'title': 'Day 65 Complete: Cloud Deployment Architectures Mastered'}],
            'subtitle': 'Public vs Private Cloud, multi-tenant SaaS vs single-tenant IaaS, release cadences, and cloud '
                        'governance.',
            'title': 'S/4HANA Cloud: Public vs Private Architecture'},
    66: {   'atomic_concepts': ['clean-core-philosophy', 'upgrade-safety-principles'],
            'day_number': 66,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'clean-core-philosophy',
            'steps': [   {   'content_md': '### Why Legacy ERP Transformations Failed\n'
                                           'For decades, SAP ERP implementations suffered from the "customization '
                                           'trap":\n'
                                           '- Developers directly modified SAP standard code (user exits, repair '
                                           'modifications).\n'
                                           '- Custom ABAP programs performed direct `SELECT` and `UPDATE` operations '
                                           'on internal database tables (`VBAK`, `BKPF`, `MARA`).\n'
                                           '- **Result**: Upgrades took 18–36 months and cost millions because every '
                                           'upgrade broke custom modifications.\n'
                                           '\n'
                                           '#### The Clean Core Philosophy\n'
                                           'Clean Core is an architectural discipline that makes the ERP system '
                                           '**continuously upgrade-safe, cloud-compliant, and modular**:\n'
                                           '1. **Zero Modifications to Standard**: Core SAP code is treated as '
                                           'immutable.\n'
                                           '2. **Strict Use of Released APIs**: Custom code interacts with standard '
                                           'data only through officially released stable interfaces (**Contract C1** '
                                           'for system-internal calls, **Contract C2** for external integrations).\n'
                                           '3. **Decoupled Extensions**: Extensibility is segregated into Key-User '
                                           'apps, On-Stack ABAP Cloud, or Side-by-Side on SAP Business Technology '
                                           'Platform (BTP).\n'
                                           '4. **Data Model Integrity**: Custom fields and tables are defined via '
                                           'standard extension tools or RAP managed entities, never via direct '
                                           'dictionary hacks.',
                             'key_terms': [   {   'definition': 'Architectural standard ensuring ERP software remains '
                                                                'fully upgradable without regression risk.',
                                                  'term': 'Clean Core'},
                                              {   'definition': 'SAP guarantee that an interface (CDS view, method, '
                                                                'BAPI) will remain stable across future upgrades.',
                                                  'term': 'Contract C1 (Released API)'},
                                              {   'definition': 'Legacy practice of altering standard code, leading to '
                                                                'massive technical debt and upgrade paralysis.',
                                                  'term': 'Modification Trap'}],
                             'step_id': 'd66_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Clean Core enforces zero core modifications and strictly released APIs so '
                                         'systems can be upgraded continuously without breaking.',
                             'title': 'The Clean Core Imperative in SAP S/4HANA'},
                         {   'content_md': '### SAP API Release Contract Taxonomy\n'
                                           'To give enterprise developers clarity on what can be safely consumed, SAP '
                                           'publishes strict Release Contracts visible in Eclipse ADT and the SAP API '
                                           'Business Hub:\n'
                                           '\n'
                                           '1. **Contract C1 (System-Internal Use)**:\n'
                                           '   - Released for On-Stack developer extensibility.\n'
                                           '   - Includes released CDS views (`I_PurchaseOrderAPI01`), released ABAP '
                                           'classes (`cl_abap_context_info`), and RAP behavior definitions.\n'
                                           '   - Guaranteed backwards compatible across all future upgrades.\n'
                                           '2. **Contract C2 (External Integration / Remote APIs)**:\n'
                                           '   - Released for external consumption via OData, SOAP, or REST (e.g., '
                                           'from SAP BTP, Salesforce, or external portals).\n'
                                           '3. **Contract C3 (State-Sharing)**:\n'
                                           '   - For transactional coordination within the same LUW across '
                                           'components.\n'
                                           '4. **Contract C4 (Data Modeling & Extensibility)**:\n'
                                           '   - Extensibility points explicitly designed for CDS view extensions or '
                                           'custom fields.\n'
                                           '\n'
                                           '#### Unreleased Objects: The Forbidden Zone\n'
                                           'Any SAP object lacking a Release Contract is considered internal. '
                                           'Consuming unreleased objects in ABAP Cloud triggers syntax errors or ATC '
                                           '(ABAP Test Cockpit) check failures.',
                             'key_terms': [   {   'definition': 'Binding contract guaranteeing cross-release stability '
                                                                'for internal ABAP Cloud consumption.',
                                                  'term': 'Release Contract C1'},
                                              {   'definition': 'Automated code governance scanner checking compliance '
                                                                'with ABAP Cloud and Clean Core rules.',
                                                  'term': 'ABAP Test Cockpit (ATC)'}],
                             'step_id': 'd66_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Only objects with official Release Contracts (C1/C2/C4) may be consumed in a '
                                         'Clean Core architecture.',
                             'title': 'Release Contracts: C1, C2, C3, and C4'},
                         {   'company_context': {   'clean_core_fix': 'RAP Entity Manipulation Language (EML) update '
                                                                      'via released interface I_PurchaseOrderAPI01',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'legacy_defect': 'Direct UPDATE on EKKO table in custom program '
                                                                     'ZPO_MOD'},
                             'content_md': '### Architecture Comparison\n'
                                           '```\n'
                                           '[DIRTY CORE: Legacy ECC Style (BREAKS ON UPGRADE)]\n'
                                           'Custom Code ───> Direct SQL: UPDATE EKKO SET ... ───> Raw DB Table\n'
                                           '  * Bypasses business logic, commit locks, and authorization\n'
                                           '  * Fails completely in S/4HANA Cloud\n'
                                           '\n'
                                           '[CLEAN CORE: Modern S/4HANA Style (UPGRADE-SAFE)]\n'
                                           'Custom Code ───> EML: MODIFY ENTITIES OF I_PurchaseOrderAPI01 ───> RAP '
                                           'Engine ───> ACID Commit\n'
                                           '  * Validates business rules, budgets, and change history\n'
                                           '  * Backwards compatible across all S/4HANA releases\n'
                                           '```',
                             'scenario': 'Nova Manufacturing inspects a legacy modification in Heidelberg vs the '
                                         'refactored Clean Core solution.',
                             'step_id': 'd66_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Clean Core vs Dirty Core Architecture Comparison'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "An ATC scan on new custom code flags an error: 'Use of unreleased table "
                                            "VBAP is forbidden in ABAP Cloud'. Remediate the code.",
                             'options': [   {   'explanation': 'Correct! Consuming the released C1 CDS view '
                                                               '`I_SalesOrderItem` satisfies ATC Clean Core rules and '
                                                               'guarantees stability.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Replace the direct `SELECT * FROM vbap` with a query '
                                                        'targeting the released C1 CDS View Entity '
                                                        '`I_SalesOrderItem`.'},
                                            {   'explanation': 'Bypassing ATC breaks governance, violates Clean Core, '
                                                               'and fails transports in Public Cloud.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Disable ATC checks globally in transaction `SATC` so the code '
                                                        'can be transported.'},
                                            {   'explanation': 'Creating duplicate rogue shadow tables creates severe '
                                                               'data inconsistency.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Rename the table to `ZVBAP`.'}],
                             'step_id': 'd66_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Replace direct access to internal database tables with released C1 CDS view '
                                         'entities.',
                             'title': 'Clean Core Governance Simulation: Resolving ATC Release Violations'},
                         {   'instruction': 'What is the certified Clean Core remediation strategy?',
                             'options': [   {   'explanation': 'Correct! The Extensibility Wrapper pattern isolates '
                                                               'non-clean debt into an explicit layer, making future '
                                                               'migration to a released API effortless.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Use the Clean Core Extensibility Wrapper pattern: encapsulate '
                                                        'the unreleased call inside a classic ABAP wrapper in Private '
                                                        'Cloud, document the technical debt, and register an API '
                                                        'release request with SAP.'},
                                            {   'explanation': 'Destroys system integrity and voids all software '
                                                               'licenses.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Hack the system by changing the SAP kernel C++ code '
                                                        'directly.'},
                                            {   'explanation': 'Halting business operations is unacceptable when '
                                                               'standard isolation wrapper patterns exist.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Cancel the business requirement and halt company invoicing.'}],
                             'scenario': "Nova's developer needs to call a specialized taxation calculation function, "
                                         'but SAP has not yet released a C1 interface for it in the current release.',
                             'step_id': 'd66_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Clean Core Dilemma: Missing Released API for Specialized Function'},
                         {   'assessment_type': 'mcq',
                             'questions': [   {   'concept_slug': 'clean-core-philosophy',
                                                  'explanation': 'Clean Core guarantees frictionless, predictable '
                                                                 'system upgrades by eliminating standard code '
                                                                 'modifications.',
                                                  'id': 'd66_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To ensure the ERP system can be '
                                                                             'continuously upgraded without manual '
                                                                             'code refactoring or regression '
                                                                             'failures.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To delete all historical company records '
                                                                             'every evening.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To mandate that all employees use Linux '
                                                                             'laptops.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To eliminate the need for an internet '
                                                                             'connection.'}],
                                                  'prompt': 'What is the primary operational objective of adhering to '
                                                            'the Clean Core philosophy in SAP S/4HANA?',
                                                  'question_id': 'd66_q1'},
                                              {   'concept_slug': 'upgrade-safety-principles',
                                                  'explanation': 'Contract C1 provides official stability guarantees '
                                                                 'for internal ABAP Cloud consumption.',
                                                  'id': 'd66_q2',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'Contract C1'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Contract Z9'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Contract ISO-9001'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Contract GDPR'}],
                                                  'prompt': 'Which SAP Release Contract guarantees that an internal '
                                                            'CDS view or ABAP class is stable and will not have '
                                                            'breaking signature changes in future upgrades?',
                                                  'question_id': 'd66_q2'},
                                              {   'concept_slug': 'clean-core-philosophy',
                                                  'explanation': 'ATC enforces automated rules checking for ABAP Cloud '
                                                                 'language compliance and released API usage.',
                                                  'id': 'd66_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'ABAP Test Cockpit (ATC)'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'Notepad++'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Windows Defender'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'SAP Spooler'}],
                                                  'prompt': 'What automated SAP governance tool scans custom code in '
                                                            'Eclipse ADT to detect unreleased API usage and Clean Core '
                                                            'violations?',
                                                  'question_id': 'd66_q3'},
                                              {   'concept_slug': 'upgrade-safety-principles',
                                                  'explanation': 'Direct database updates bypass business logic and '
                                                                 'audit integrity, causing severe corruption.',
                                                  'id': 'd66_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It bypasses standard transactional '
                                                                             'validations, locks, change documents, '
                                                                             'and breaks on future schema changes.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It makes the database font size '
                                                                             'smaller.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Direct SQL execution is physically '
                                                                             'impossible on SSDs.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'SQL updates automatically disconnect the '
                                                                             'power supply.'}],
                                                  'prompt': 'Why is performing direct SQL `UPDATE` operations on '
                                                            'standard SAP tables (like `EKKO` or `ACDOCA`) strictly '
                                                            'forbidden in Clean Core?',
                                                  'question_id': 'd66_q4'}],
                             'step_id': 'd66_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 66 Verification Assessment'},
                         {   'step_id': 'd66_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered the Clean Core principles: zero core modifications, released '
                                           'APIs, and decoupled extensibility.\n'
                                           '- Analyzed API Release Contracts (C1 for internal, C2 for remote '
                                           'integration).\n'
                                           '- Applied ATC automated code governance and the Extensibility Wrapper '
                                           'pattern for legacy isolation.',
                             'title': 'Day 66 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd66_s8_completion',
                             'recommended_mission': {'slug': 'nova-clean-core-audit', 'title': 'Clean Core Governance & C1 API Audit', 'description': 'Audit custom Z-code portfolio against SAP Clean Core criteria.'},
                             'step_type': 'completion',
                             'summary_md': 'Superb work! Clean Core is the bedrock of modern SAP consulting. Tomorrow, '
                                           'you will master the delivery framework that executes Clean Core '
                                           'implementations: **SAP Activate Methodology and Quality Gates**.',
                             'title': 'Day 66 Complete: Clean Core Philosophy Internalized'}],
            'subtitle': 'Decoupling extensions from the core: released APIs (C1 contract), cloud-compliant ABAP, and '
                        'zero modifications.',
            'title': 'The Clean Core Philosophy & Principles'},
    67: {   'atomic_concepts': ['sap-activate-methodology', 'activate-quality-gates'],
            'day_number': 67,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'sap-activate-methodology',
            'steps': [   {   'content_md': '### The Modern Cloud Delivery Framework\n'
                                           'SAP Activate is the standard agile implementation methodology for S/4HANA '
                                           'Cloud and On-Premise. It replaces legacy waterfall approaches (such as '
                                           'ASAP) with iterative, pre-configured best-practice delivery.\n'
                                           '\n'
                                           '#### The 6 Sequential Phases of SAP Activate:\n'
                                           '1. **Discover**: Business explores S/4HANA capabilities, trials solution '
                                           'scope via trial systems, and formulates the high-level digital '
                                           'transformation business case.\n'
                                           '2. **Prepare**: Project kick-off, team onboarding, initial governance '
                                           'setup, and provisioning of the initial starter system landscape.\n'
                                           '3. **Explore**: Conduct **Fit-to-Standard workshops** comparing company '
                                           'processes to standard SAP Best Practices. Capture delta requirements and '
                                           'configuration backlog.\n'
                                           '4. **Realize**: Agile sprint cycles configuring CBC/SPRO, developing Clean '
                                           'Core extensions, migrating data batches, and conducting integration '
                                           'testing (SIT/UAT).\n'
                                           '5. **Deploy**: Final cutover activities, blackout periods, production data '
                                           'load validation, end-user training, and formal transition to the live '
                                           'system.\n'
                                           '6. **Run**: Hypercare support, steady-state operations, and continuous '
                                           'innovation adoption during semi-annual cloud upgrades.',
                             'key_terms': [   {   'definition': 'Standard agile implementation methodology combining '
                                                                'Best Practices, Guided Configuration, and iterative '
                                                                'sprints.',
                                                  'term': 'SAP Activate'},
                                              {   'definition': 'Workshops validating standard SAP processes against '
                                                                'business requirements to prevent custom '
                                                                'modifications.',
                                                  'term': 'Fit-to-Standard'},
                                              {   'definition': 'Pre-configured cloud tenant used in Prepare and '
                                                                'Explore phases to demonstrate live best practices.',
                                                  'term': 'Starter System'}],
                             'step_id': 'd67_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'SAP Activate guides projects across 6 phases: Discover, Prepare, Explore, '
                                         'Realize, Deploy, and Run.',
                             'title': 'The Six Phases of the SAP Activate Methodology'},
                         {   'content_md': '### Governance Through Strict Quality Gates\n'
                                           'To prevent unready implementations from advancing into costly failures, '
                                           'SAP Activate mandates formal **Quality Gates (Q-Gates)** between phases:\n'
                                           '\n'
                                           '#### The 4 Critical Quality Gates:\n'
                                           '1. **Q-Gate 1 (Prepare to Explore)**: Verifies project charter sign-off, '
                                           'starter system availability, and team readiness for Fit-to-Standard '
                                           'sessions.\n'
                                           '2. **Q-Gate 2 (Explore to Realize)**: Crucial gate. Confirms that all '
                                           'scope items are finalized, delta backlogs are strictly validated against '
                                           'Clean Core rules, and baseline architecture is locked.\n'
                                           '3. **Q-Gate 3 (Realize to Deploy)**: Validates that all integration tests '
                                           '(SIT), User Acceptance Tests (UAT), and data migration mock dry-runs have '
                                           'passed with zero high-severity defects.\n'
                                           '4. **Q-Gate 4 (Deploy to Run)**: Final executive go/no-go cutover sign-off '
                                           'confirming operational readiness, support team staffing, and hypercare '
                                           'SLAs.',
                             'key_terms': [   {   'definition': 'Formal stage-gate audit verifying mandatory '
                                                                'deliverables and risk criteria before phase exit.',
                                                  'term': 'Quality Gate (Q-Gate)'},
                                              {   'definition': 'Final executive evaluation at Q-Gate 4 authorizing '
                                                                'production system cutover.',
                                                  'term': 'Go/No-Go Decision'}],
                             'step_id': 'd67_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Quality Gates enforce mandatory risk checks, ensuring projects never advance '
                                         'to realization or cutover with unresolved gaps.',
                             'title': 'Quality Gates (Q-Gates) & Risk Governance'},
                         {   'company_context': {   'audit_findings': '14 Best Practice scope items accepted without '
                                                                      'change; 2 delta extensions approved for ABAP '
                                                                      'Cloud; 1 custom modification rejected for Clean '
                                                                      'Core violation.',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'gate': 'Q-Gate 2 (Explore -> Realize)',
                                                    'plant': 'PL02'},
                             'content_md': '### Q-Gate 2 Governance Dashboard (Austin PL02)\n'
                                           '```\n'
                                           '[Phase: Explore] ──────────────────────────► [Q-GATE 2 AUDIT] '
                                           '──────────────────────────► [Phase: Realize]\n'
                                           '                                                    │\n'
                                           '      '
                                           '┌─────────────────────────────────────────────┴─────────────────────────────────────────────┐\n'
                                           '      ▼                                             '
                                           '▼                                             ▼\n'
                                           '[14 Scope Items Confirmed]                 [2 Clean Core Ext. '
                                           'Approved]                  [1 Custom Mod REJECTED]\n'
                                           '* J45: Procurement                         * BTP Event Mesh '
                                           'notification                 * Attempt to modify EKKO table\n'
                                           '* BNZ: Sales Order Processing              * Custom Field for Sensor '
                                           'ID                  * Enforced: Use RAP EML instead\n'
                                           '* Status: 100% Fit-to-Standard             * Status: C1 API '
                                           'Compliant                    * Status: Remediated to Clean Core\n'
                                           '```',
                             'scenario': 'Nova Manufacturing conducts Q-Gate 2 at the conclusion of the Explore phase '
                                         'for Plant Austin (PL02).',
                             'step_id': 'd67_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Phase Road-map & Q-Gate 2 Audit'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'Arrange the implementation activities into the correct chronological SAP '
                                            'Activate sequence.',
                             'options': [   {   'explanation': 'Correct! This sequence precisely mirrors the '
                                                               'authoritative Activate methodology phases.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': '1. Project Charter (Prepare) -> 2. Fit-to-Standard Workshops '
                                                        '(Explore) -> 3. Sprint Configuration & SIT (Realize) -> 4. '
                                                        'Cutover Execution (Deploy) -> 5. Hypercare (Run).'},
                                            {   'explanation': 'Deploying to production before workshops or project '
                                                               'planning is disastrous.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': '1. Production Cutover -> 2. Fit-to-Standard -> 3. Project '
                                                        'Kick-off.'},
                                            {   'explanation': 'Configuring the system before scoping and requirements '
                                                               'discovery violates project fundamentals.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': '1. Realize configuration -> 2. Discover business case -> 3. '
                                                        'Prepare charter.'}],
                             'step_id': 'd67_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Activate rigorously sequences requirements discovery, Fit-to-Standard '
                                         'validation, sprint realization, and governed deployment.',
                             'title': 'Activate Process Ordering: Sequencing Implementation Stages'},
                         {   'instruction': 'How should the Project Director and Quality Manager respond?',
                             'options': [   {   'explanation': 'Correct! Q-Gates exist precisely to prevent disastrous '
                                                               'unready cutovers with critical data corruption risks.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Refuse to sign off on Q-Gate 3. Deploying with open Sev-1 '
                                                        'posting defects will corrupt the General Ledger (`ACDOCA`) '
                                                        'and halt billing operations. Remediate defects in an '
                                                        'emergency sprint before re-evaluating the gate.'},
                                            {   'explanation': 'Catastrophic failure; will corrupt financial reporting '
                                                               'and trigger regulatory investigations.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Sign off immediately and assume financial postings will fix '
                                                        'themselves in production.'},
                                            {   'explanation': 'Concealing critical defects violates governance and '
                                                               'professional ethics.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Delete the defect tickets from Jira.'}],
                             'scenario': 'A business sponsor demands to bypass Q-Gate 3 and proceed to production '
                                         'deployment despite 12 unresolved severity-1 financial posting defects in '
                                         'UAT.',
                             'step_id': 'd67_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Governance Challenge: Bypassing Q-Gate 3 Defect Thresholds'},
                         {   'assessment_type': 'process_ordering',
                             'questions': [   {   'concept_slug': 'sap-activate-methodology',
                                                  'explanation': 'Fit-to-Standard workshops are the central activity '
                                                                 'of the Explore phase.',
                                                  'id': 'd67_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Explore Phase'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'Run Phase'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Deploy Phase'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Discover Phase'}],
                                                  'prompt': 'In which SAP Activate phase are Fit-to-Standard workshops '
                                                            'conducted to evaluate standard Best Practice processes '
                                                            'against customer requirements?',
                                                  'question_id': 'd67_q1'},
                                              {   'concept_slug': 'activate-quality-gates',
                                                  'explanation': 'Quality Gates serve as mandatory risk and quality '
                                                                 'governance milestones.',
                                                  'id': 'd67_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To conduct a formal audit ensuring all '
                                                                             'phase exit criteria and quality '
                                                                             'standards are satisfied before '
                                                                             'advancing.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To charge credit cards for cloud '
                                                                             'software licenses.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To lock user accounts after office '
                                                                             'hours.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To reformat hard drives in the '
                                                                             'datacenter.'}],
                                                  'prompt': 'What is the primary function of a Quality Gate (Q-Gate) '
                                                            'in the SAP Activate governance framework?',
                                                  'question_id': 'd67_q2'},
                                              {   'concept_slug': 'sap-activate-methodology',
                                                  'explanation': 'The Realize phase builds, tests, and validates the '
                                                                 'configured solution.',
                                                  'id': 'd67_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Realize Phase'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Prepare Phase'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Discover Phase'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Deploy Phase'}],
                                                  'prompt': 'Which phase of SAP Activate focuses on agile '
                                                            'configuration sprints, developer extensibility, data '
                                                            'migration mock loads, and integration testing?',
                                                  'question_id': 'd67_q3'},
                                              {   'concept_slug': 'activate-quality-gates',
                                                  'explanation': 'Q-Gate 4 authorizes the live cutover from deployment '
                                                                 'to production run.',
                                                  'id': 'd67_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Q-Gate 4 (Deploy to Run)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Q-Gate 1 (Prepare to Explore)'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Q-Gate 2 (Explore to Realize)'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Q-Gate 0 (Discovery)'}],
                                                  'prompt': 'Which Quality Gate governs the formal Go/No-Go decision '
                                                            'authorizing production system cutover?',
                                                  'question_id': 'd67_q4'}],
                             'step_id': 'd67_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 67 Verification Assessment'},
                         {   'step_id': 'd67_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered the 6 phases of the SAP Activate methodology (Discover, '
                                           'Prepare, Explore, Realize, Deploy, Run).\n'
                                           '- Enforced Quality Gate (Q-Gate) governance criteria to protect production '
                                           'integrity.\n'
                                           '- Aligned implementation workflows with agile sprints and Clean Core delta '
                                           'evaluation.',
                             'title': 'Day 67 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd67_s8_completion',
                             'recommended_mission': {'slug': 'nova-activate-methodology-gate', 'title': 'SAP Activate Quality Gate Review', 'description': 'Lead Explore-to-Realize phase sign-off for manufacturing deployment.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You understand the delivery lifecycle. Tomorrow, you will '
                                           'master the cornerstone workshop of the Explore phase: **Fit-to-Standard '
                                           'Workshops and Scope Items**.',
                             'title': 'Day 67 Complete: SAP Activate Methodology Mastered'}],
            'subtitle': 'Discover, Prepare, Explore, Realize, Deploy, Run; Quality Gates, agile sprints, and '
                        'governance.',
            'title': 'SAP Activate Methodology & Quality Gates'},
    68: {   'atomic_concepts': ['fit-to-standard-approach', 'best-practices-scope-items'],
            'day_number': 68,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'fit-to-standard-workshops',
            'steps': [   {   'content_md': "### Replacing the 'Blank Sheet' with Best Practices\n"
                                           'In legacy ERP projects, consultants conducted "Business Blueprinting": '
                                           'asking business users how they wanted the software to work, leading to '
                                           'thousands of custom modifications mimicking obsolete legacy routines.\n'
                                           '\n'
                                           '#### The Fit-to-Standard Approach:\n'
                                           "- **Show, Don't Tell**: Consultants demonstrate standard, live **SAP Best "
                                           'Practice Scope Items** in a working pre-configured cloud system (Starter '
                                           'System).\n'
                                           '- **Validation**: Business users validate how standard processes fulfill '
                                           'their requirements.\n'
                                           '- **Delta Classification**: When a gap arises, it is strictly evaluated:\n'
                                           '  1. *Can the business adopt the standard process?* (Preferred).\n'
                                           '  2. *Can it be solved via standard configuration in CBC?*\n'
                                           '  3. *Can it be solved via Key-User extensibility (custom fields)?*\n'
                                           '  4. *Only if essential*: Captured in the delta backlog for developer '
                                           'extensibility using released APIs.',
                             'key_terms': [   {   'definition': 'Workshops demonstrating standard processes to align '
                                                                'business practices to standard software.',
                                                  'term': 'Fit-to-Standard'},
                                              {   'definition': 'Pre-packaged, end-to-end business process scenario '
                                                                'delivered by SAP with process flows and test scripts.',
                                                  'term': 'Best Practice Scope Item'},
                                              {   'definition': 'Prioritized inventory of valid process variations '
                                                                'requiring configuration or Clean Core extensions.',
                                                  'term': 'Delta Backlog'}],
                             'step_id': 'd68_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Fit-to-Standard demonstrates standard scope items in a live system to '
                                         'maximize standardization and eliminate unnecessary custom code.',
                             'title': 'The Fit-to-Standard Paradigm vs Legacy Blueprinting'},
                         {   'content_md': '### Standard Scope Items (e.g., J45, BNZ, BD9)\n'
                                           'Every SAP Best Practice scope item is published in the SAP Signavio '
                                           'Process Navigator with standard artifacts:\n'
                                           '\n'
                                           '1. **Scope Item Identifier**: 3-character code (e.g., `J45` = Procurement '
                                           'of Direct Materials, `BNZ` = Create Sales Orders, `BD9` = Sell from '
                                           'Stock).\n'
                                           '2. **Process Flow Diagram (BPMN 2.0)**: Visual step-by-step swimlane '
                                           'diagram showing role interactions (Purchaser, Warehouse Clerk, Accounts '
                                           'Payable).\n'
                                           '3. **Test Script**: Complete step-by-step procedural manual with sample '
                                           'master data (Company Code `1010`, Plant `1010`, Material `TG11`).\n'
                                           '4. **Prerequisites & Scope Dependencies**: Identifies upstream scope items '
                                           'required (e.g., `BNZ` requires master data scope item `BND`).',
                             'key_terms': [   {   'definition': 'Central SAP cloud repository providing process flows, '
                                                                'scope descriptions, and test scripts for Best '
                                                                'Practices.',
                                                  'term': 'Process Navigator'},
                                              {   'definition': 'Standard SAP Best Practice for direct materials '
                                                                'procurement from requisition to invoice.',
                                                  'term': 'Scope Item J45'}],
                             'step_id': 'd68_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Scope items provide pre-built process flows, test scripts, and role '
                                         'assignments that eliminate the need to design processes from scratch.',
                             'title': 'Anatomy of an SAP Best Practice Scope Item'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'delta_requirement': 'Custom inspection certificate tracking '
                                                                         'requirement resolved via standard Key-User '
                                                                         'field on Material Document.',
                                                    'scope_item': 'J45 (Direct Procurement)',
                                                    'standard_fit': 'Requisition -> PO Approval -> MIGO Goods Receipt '
                                                                    '-> MIRO Invoice Match (100% Fit)'},
                             'content_md': '### Scope Item J45 Swimlane Alignment (Nova Heidelberg)\n'
                                           '```\n'
                                           '[Role: Purchaser (Marcus)]       [Role: Warehouse (PL01)]       [Role: '
                                           'Accounts Payable]\n'
                                           '          │                                  '
                                           '│                               │\n'
                                           '  Create Purchase Order                      '
                                           '│                               │\n'
                                           '          │                                  '
                                           '│                               │\n'
                                           '          ▼                                  '
                                           '▼                               │\n'
                                           '  Vendor VEND-101 Confirmed ───────> Goods Receipt '
                                           '(MIGO)                    │\n'
                                           '                                     * Posts to '
                                           'MATDOC                       │\n'
                                           '                                             '
                                           '│                               ▼\n'
                                           '                                             └──────────────────────> '
                                           'Invoice Verification (MIRO)\n'
                                           '                                                                      * '
                                           '3-Way Match & Clear GR/IR\n'
                                           '```',
                             'scenario': "Nova's procurement team evaluates Scope Item J45 (Procurement of Direct "
                                         'Materials) for sensor RAW-01 at Heidelberg (PL01).',
                             'step_id': 'd68_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Fit-to-Standard Session: Scope Item J45'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'A department manager demands a custom 4-tier approval screen with custom '
                                            "email popups because 'that is how we did it in 2005'. Apply "
                                            'Fit-to-Standard discipline.',
                             'options': [   {   'explanation': 'Correct! Showing how standard Flexible Workflow '
                                                               'already fulfills the underlying business need '
                                                               'satisfies the requirement without custom code.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Demonstrate SAP standard Flexible Workflow for Purchase '
                                                        'Orders: it supports multi-tier rule-based approvals, mobile '
                                                        'Fiori notifications, and zero custom code.'},
                                            {   'explanation': 'Violates Fit-to-Standard and creates massive technical '
                                                               'debt.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Immediately agree to code a 5,000-line custom ABAP dynpro '
                                                        'program.'},
                                            {   'explanation': 'Unprofessional; consulting requires educating '
                                                               'stakeholders on modern standard capabilities.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Tell the manager their request is forbidden and cancel their '
                                                        'user account.'}],
                             'step_id': 'd68_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Address process delta demands by demonstrating standard capabilities (such '
                                         'as Flexible Workflow) that satisfy the business need.',
                             'title': 'Fit-to-Standard Simulation: Handling Process Delta Demands'},
                         {   'instruction': 'How should this requirement be classified during Fit-to-Standard?',
                             'options': [   {   'explanation': 'Correct! Truly differentiating competitive '
                                                               'intellectual property belongs in decoupled BTP '
                                                               'extensions, preserving Clean Core.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Classify as a Strategic Process Differentiator: build as a '
                                                        'decoupled Side-by-Side extension on SAP BTP using released '
                                                        'APIs, while keeping core procurement standard.'},
                                            {   'explanation': 'Destroys competitive advantage; ERP must support '
                                                               'genuine competitive differentiation via clean '
                                                               'extensibility.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Force Nova to abandon their patent and use generic manual '
                                                        'assembly.'},
                                            {   'explanation': 'Modifying financial tables for manufacturing '
                                                               'algorithms violates core architectural separation.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Modify core standard table ACDOCA to store calibration '
                                                        'data.'}],
                             'scenario': 'Nova Manufacturing has a proprietary patent-protected robotic calibration '
                                         'algorithm that creates real competitive market advantage.',
                             'step_id': 'd68_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Workshop Challenge: Classifying Genuine Process Differentiators'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'fit-to-standard-approach',
                                                  'explanation': 'Fit-to-Standard anchors discussions in working '
                                                                 'standard software rather than abstract custom '
                                                                 'blueprints.',
                                                  'id': 'd68_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Fit-to-Standard demonstrates live '
                                                                             'standard Best Practices to minimize '
                                                                             'customization, whereas Blueprinting '
                                                                             'designed custom processes from a blank '
                                                                             'sheet.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Fit-to-Standard is only conducted in '
                                                                             'German.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Fit-to-Standard requires no business '
                                                                             'users to participate.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Fit-to-Standard guarantees that zero '
                                                                             'configuration changes are permitted.'}],
                                                  'prompt': 'What is the fundamental difference between '
                                                            'Fit-to-Standard workshops and traditional legacy '
                                                            'Blueprinting?',
                                                  'question_id': 'd68_q1'},
                                              {   'concept_slug': 'best-practices-scope-items',
                                                  'explanation': 'Scope items represent standardized building blocks '
                                                                 'of ERP business functionality.',
                                                  'id': 'd68_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'A pre-packaged, documented, end-to-end '
                                                                             'business process delivered with standard '
                                                                             'process flows, role assignments, and '
                                                                             'test scripts.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'A hardware measurement tool for computer '
                                                                             'screens.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'An encrypted password string.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'A legal disclaimer on customer '
                                                                             'invoices.'}],
                                                  'prompt': "In SAP terminology, what is a 'Scope Item' (such as J45 "
                                                            'or BNZ)?',
                                                  'question_id': 'd68_q2'},
                                              {   'concept_slug': 'fit-to-standard-approach',
                                                  'explanation': 'Standard configuration is always exhausted before '
                                                                 'considering custom extensibility.',
                                                  'id': 'd68_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Standard configuration in Central '
                                                                             'Business Configuration (CBC) or SPRO.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Core modification of standard SAP ABAP '
                                                                             'kernel programs.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Abandoning the S/4HANA cloud migration '
                                                                             'entirely.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Purchasing an un-integrated third-party '
                                                                             'ERP system.'}],
                                                  'prompt': 'When a genuine business requirement cannot be satisfied '
                                                            'by standard SAP Best Practices, what is the first '
                                                            'architectural option evaluated?',
                                                  'question_id': 'd68_q3'},
                                              {   'concept_slug': 'best-practices-scope-items',
                                                  'explanation': 'Process Navigator is the official central repository '
                                                                 'for Best Practice documentation.',
                                                  'id': 'd68_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'SAP Signavio Process Navigator (formerly '
                                                                             'SAP Best Practices Explorer)'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'Wikipedia'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Local hard drive C:\\temp\\'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Stack Overflow'}],
                                                  'prompt': 'Where can enterprise architects find authoritative '
                                                            'process flows, test scripts, and dependency diagrams for '
                                                            'all SAP Best Practices scope items?',
                                                  'question_id': 'd68_q4'}],
                             'step_id': 'd68_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 68 Verification Assessment'},
                         {   'step_id': 'd68_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Executed Fit-to-Standard methodology to align business operations with '
                                           'SAP Best Practice scope items.\n'
                                           '- Managed delta backlogs prioritizing configuration over customization.\n'
                                           '- Isolated strategic competitive differentiators into decoupled Clean Core '
                                           'extensions.',
                             'title': 'Day 68 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd68_s8_completion',
                             'recommended_mission': {'slug': 'nova-fit-to-standard-scoping', 'title': 'Fit-to-Standard Workshop Scoping', 'description': 'Reconcile delta requirements against standard best practices.'},
                             'step_type': 'completion',
                             'summary_md': 'Superb work! You know how to scope standard processes. Tomorrow, you will '
                                           'configure those scope items in the cloud using **SAP Central Business '
                                           'Configuration (CBC)**.',
                             'title': 'Day 68 Complete: Fit-to-Standard Mastery Achieved'}],
            'subtitle': 'Executing Fit-to-Standard vs blueprinting; SAP Best Practices scope items (e.g., J45, BNZ), '
                        'and delta backlog management.',
            'title': 'Fit-to-Standard Workshops & Scope Items'},
    69: {   'atomic_concepts': ['cbc-configuration', 'scoping-and-fine-tuning'],
            'day_number': 69,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'central-business-configuration',
            'steps': [   {   'content_md': '### What is Central Business Configuration (CBC)?\n'
                                           'SAP Central Business Configuration (CBC) is the modern SaaS configuration '
                                           'engine for S/4HANA Cloud Public Edition. Instead of navigating thousands '
                                           'of nested folders in classic transaction SPRO on every individual system, '
                                           'CBC manages business configuration centrally across the entire cloud '
                                           'tenant landscape.\n'
                                           '\n'
                                           '#### Core Capabilities of CBC:\n'
                                           '1. **Scoping**: Select countries/regions (e.g., Germany, USA) and activate '
                                           'required Best Practice Scope Items (e.g., J45, BNZ).\n'
                                           '2. **Organizational Structure Management**: Visual drag-and-drop hierarchy '
                                           'builder to define Companies, Plants, Sales Orgs, and Purchasing Orgs.\n'
                                           '3. **Configuration Activities (Fine-Tuning)**: Contextual tasks guiding '
                                           'the configuration of payment terms, account determination, tax codes, and '
                                           'pricing rules.\n'
                                           '4. **Automated Deployment**: CBC automatically deploys configuration '
                                           'changes into the connected S/4HANA Development tenant (Customizing Client '
                                           '100).',
                             'key_terms': [   {   'definition': 'Central SaaS application managing scoping, org '
                                                                'structures, and fine-tuning across cloud tenants.',
                                                  'term': 'Central Business Configuration (CBC)'},
                                              {   'definition': 'CBC project phase where countries, industries, and '
                                                                'specific Best Practice scope items are activated.',
                                                  'term': 'Scoping Phase'},
                                              {   'definition': 'Visual organizational modeling tool in CBC that '
                                                                'automatically creates backend enterprise units.',
                                                  'term': 'Org Structure Management'}],
                             'step_id': 'd69_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'CBC replaces classic SPRO in Public Cloud, providing centralized scoping, '
                                         'visual org structure setup, and automated deployment.',
                             'title': 'The Central Configuration Engine: SAP CBC'},
                         {   'content_md': '### The CBC Project Governance Lifecycle\n'
                                           'CBC enforces structured project gates to prevent premature or conflicting '
                                           'configuration:\n'
                                           '\n'
                                           '1. **Scope Phase (Scope Confirmation)**:\n'
                                           '   - Select Primary Country and Additional Countries.\n'
                                           '   - Bundle scope items into the project. Once Scope Confirmation is '
                                           'locked, baseline database initialization begins.\n'
                                           '2. **Specify Phase (Org Structure)**:\n'
                                           '   - Define Company Code (e.g., `NM01`), Plant (e.g., `PL01`), Storage '
                                           'Locations, and Financial Year Variants.\n'
                                           '   - Confirm Org Structure. CBC deploys org units to the backend system.\n'
                                           '3. **Product-Specific Configuration Phase**:\n'
                                           '   - Complete mandatory pre-requisite configuration tasks before entering '
                                           'the Realize phase.\n'
                                           '4. **Realize Phase**:\n'
                                           '   - Continuous fine-tuning activities. Customizing changes are recorded '
                                           'on **Customizing Transport Requests** in the S/4HANA Development tenant '
                                           'for release to Test and Production.',
                             'key_terms': [   {   'definition': 'Milestone in CBC locking selected countries and scope '
                                                                'items to trigger tenant initialization.',
                                                  'term': 'Scope Confirmation'},
                                              {   'definition': 'Targeted configuration tasks tailoring standard rules '
                                                                'to specific enterprise parameters.',
                                                  'term': 'Fine-Tuning Activities'}],
                             'step_id': 'd69_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'CBC follows a structured lifecycle: Scope Confirmation -> Org Structure '
                                         'Confirmation -> Realize Fine-Tuning.',
                             'title': 'Project Lifecycle in CBC: Scoping, Product-Specific, and Realize'},
                         {   'company_context': {   'company_codes': ['NM01 (Germany)', 'NM02 (US)'],
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'countries': ['Germany (DE)', 'United States (US)'],
                                                    'plants': ['PL01 (Heidelberg Assembly)', 'PL02 (Austin Robotics)']},
                             'content_md': '### Visual Org Structure in CBC\n'
                                           '```\n'
                                           '[CBC Project: Nova Global Transformation]\n'
                                           '  ├── [Country: Germany]\n'
                                           '  │     └── [Company Code: NM01 (EUR)]\n'
                                           '  │           └── [Plant: PL01 (Heidelberg)]\n'
                                           '  │                 ├── [Storage Loc: RAW1 (Sensors)]\n'
                                           '  │                 └── [Storage Loc: FG01 (Finished Goods)]\n'
                                           '  │\n'
                                           '  └── [Country: United States]\n'
                                           '        └── [Company Code: NM02 (USD)]\n'
                                           '              └── [Plant: PL02 (Austin)]\n'
                                           '                    ├── [Storage Loc: RAW1 (Components)]\n'
                                           '                    └── [Storage Loc: FG01 (Robotics)]\n'
                                           '```',
                             'scenario': "Nova's lead configuration expert sets up the multi-country organizational "
                                         'structure in CBC.',
                             'step_id': 'd69_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing CBC Configuration: Heidelberg (PL01) & Austin (PL02)'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "Nova's project team attempts to start fine-tuning payment terms before "
                                            'completing Scope Confirmation in CBC. Diagnose the behavior.',
                             'options': [   {   'explanation': 'Correct! CBC enforces phased sequence governance; '
                                                               'fine-tuning tasks remain locked until scope and org '
                                                               'structure are confirmed.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'CBC blocks fine-tuning activities because Scope Confirmation '
                                                        'and Org Structure Confirmation must be formally completed '
                                                        'before Realize activities unlock.'},
                                            {   'explanation': 'CBC is a cloud web app; phase locking is governed by '
                                                               'application business logic.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'The browser crashed because the laptop lacks sufficient RAM.'},
                                            {   'explanation': 'Payment terms are standard configuration in the '
                                                               'Realize phase.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Payment terms cannot be configured in S/4HANA.'}],
                             'step_id': 'd69_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'CBC strictly enforces milestone gating: Scope Confirmation and Org Structure '
                                         'must be locked before Realize fine-tuning unlocks.',
                             'title': 'CBC Configuration Simulation: Scoping Milestone Lock'},
                         {   'instruction': 'How does CBC handle adding new country scope to an ongoing project?',
                             'options': [   {   'explanation': 'Correct! CBC Change Projects enable safe, modular '
                                                               'scope expansions to existing active tenants.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': "Initiate an 'Add New Scope' change project in CBC: select "
                                                        'Country Japan (JP), activate Japanese localization scope '
                                                        'items, confirm scope delta, and deploy to Dev client without '
                                                        'disrupting existing German and US configuration.'},
                                            {   'explanation': 'Catastrophic; destroying production systems for scope '
                                                               'additions is never done.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Delete the entire S/4HANA production system and start over '
                                                        'from scratch.'},
                                            {   'explanation': 'Violates Clean Core, destroys supportability, and is '
                                                               'impossible in Public Cloud.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Manually insert raw records into SAP kernel database tables '
                                                        'via SQL.'}],
                             'scenario': 'Nova decides to expand operations into Japan midway through the Realize '
                                         'phase of its initial deployment.',
                             'step_id': 'd69_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Configuration Challenge: Mid-Project Country Scope Addition'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'cbc-configuration',
                                                  'explanation': 'CBC is the central configuration solution for '
                                                                 'S/4HANA Cloud Public Edition.',
                                                  'id': 'd69_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Central SaaS engine for business '
                                                                             'scoping, organizational structure setup, '
                                                                             'and configuration fine-tuning across '
                                                                             'cloud tenants.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'A video conferencing tool for project '
                                                                             'status meetings.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'An email spam filter.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'A compiler for C++ code.'}],
                                                  'prompt': 'What is the primary role of SAP Central Business '
                                                            'Configuration (CBC) in S/4HANA Cloud Public Edition?',
                                                  'question_id': 'd69_q1'},
                                              {   'concept_slug': 'scoping-and-fine-tuning',
                                                  'explanation': 'Scope Confirmation locks selected countries and Best '
                                                                 'Practices to initiate tenant setup.',
                                                  'id': 'd69_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Scope Confirmation'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Hypercare Exit'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Final User Acceptance Sign-off'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Annual Tax Filing'}],
                                                  'prompt': 'What milestone in CBC must be confirmed before backend '
                                                            'tenant database initialization and organizational unit '
                                                            'deployment can proceed?',
                                                  'question_id': 'd69_q2'},
                                              {   'concept_slug': 'cbc-configuration',
                                                  'explanation': 'Configurations deploy to the Development customizing '
                                                                 'tenant and flow through standard transport '
                                                                 'mechanisms.',
                                                  'id': 'd69_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Directly to the Development system '
                                                                             'Customizing client (e.g. Client 100), '
                                                                             'recorded on Transport Requests.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Directly into the live Production system '
                                                                             'bypassing testing.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': "To the user's browser temporary cache."},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Into an external unencrypted Google '
                                                                             'Sheet.'}],
                                                  'prompt': 'Where does CBC deploy fine-tuning configuration changes '
                                                            "within the customer's 3-System Landscape (3SL)?",
                                                  'question_id': 'd69_q3'},
                                              {   'concept_slug': 'scoping-and-fine-tuning',
                                                  'explanation': 'CBC Change Projects allow continuous addition of '
                                                                 'countries and scope items post go-live.',
                                                  'id': 'd69_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'By initiating a Change Project in CBC to '
                                                                             'evaluate and deploy the delta scope.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'By re-installing Windows on all user '
                                                                             'laptops.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'By writing custom ABAP scripts in '
                                                                             'transaction SE38.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'New scope cannot be added once a system '
                                                                             'is live.'}],
                                                  'prompt': 'How can a customer add a new country or scope item to an '
                                                            'S/4HANA Cloud system after the initial go-live?',
                                                  'question_id': 'd69_q4'}],
                             'step_id': 'd69_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 69 Verification Assessment'},
                         {   'step_id': 'd69_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered Central Business Configuration (CBC) architecture and project '
                                           'governance.\n'
                                           '- Executed business scoping, country activations, and visual '
                                           'organizational structure modeling.\n'
                                           '- Managed configuration deployment and change projects across the 3-System '
                                           'Landscape.',
                             'title': 'Day 69 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd69_s8_completion',
                             'recommended_mission': {'slug': 'nova-cbc-org-setup', 'title': 'Central Business Configuration Org Setup', 'description': 'Provision global organizational entities in CBC.'},
                             'step_type': 'completion',
                             'summary_md': 'Phenomenal work! You now understand how cloud configuration is managed '
                                           'centrally. Tomorrow, you will unlock the first tier of the Clean Core '
                                           'extensibility model: **Key-User Extensibility**.',
                             'title': 'Day 69 Complete: Cloud Configuration (CBC) Mastered'}],
            'subtitle': 'Project setup, business scoping, organizational structure management, and configuration '
                        'fine-tuning.',
            'title': 'Central Business Configuration (CBC)'},
    70: {   'atomic_concepts': ['key-user-extensibility', 'custom-fields-and-logic', 'restricted-abap-cloud'],
            'day_number': 70,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'key-user-extensibility',
            'steps': [   {   'content_md': '### Low-Code Extensibility for Business Experts\n'
                                           'In the SAP Clean Core Extensibility Framework, **Key-User Extensibility** '
                                           '(also called In-App Extensibility) enables business analysts and key users '
                                           'to tailor standard applications without developer tools (Eclipse ADT) and '
                                           'without writing classical ABAP code.\n'
                                           '\n'
                                           '#### Key Capabilities of Key-User Extensibility:\n'
                                           '1. **Custom Fields**: Add business fields to standard entities (e.g., '
                                           'adding `InspectionCertificateID` to Purchase Order headers). The tool '
                                           'automatically updates database tables, CDS views, OData APIs, and Fiori UI '
                                           'screens.\n'
                                           '2. **UI Adaptation at Runtime**: Visually re-arrange fields, rename '
                                           'labels, group sections, or hide irrelevant inputs directly inside the '
                                           'running Fiori app.\n'
                                           '3. **Custom Logic (Restricted ABAP)**: Implement cloud Business Add-Ins '
                                           '(BAdIs) using a sandboxed web-based code editor with **Restricted ABAP '
                                           'Cloud syntax**.\n'
                                           '4. **Custom Business Objects (CBOs)**: Build standalone master data or '
                                           'lookup tables with auto-generated Fiori maintenance apps.\n'
                                           '5. **Custom Email & Form Templates**: Adapt Adobe Output Forms and '
                                           'notification emails.',
                             'key_terms': [   {   'definition': 'Low-code in-app toolset empowering authorized '
                                                                'business users to extend standard apps safely.',
                                                  'term': 'Key-User Extensibility'},
                                              {   'definition': 'Central Fiori app for creating custom fields and '
                                                                'implementing sandboxed Cloud BAdIs.',
                                                  'term': 'Custom Fields and Logic'},
                                              {   'definition': 'Fiori capability allowing visual drag-and-drop '
                                                                're-ordering and hiding of screen elements.',
                                                  'term': 'UI Adaptation at Runtime'}],
                             'step_id': 'd70_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Key-User Extensibility provides low-code customization (fields, UI '
                                         'adaptation, and sandboxed BAdIs) that is 100% upgrade-safe.',
                             'title': 'The Key-User Extensibility Tier (In-App Extensibility)'},
                         {   'content_md': '### Why Key-User Code Cannot Break the System\n'
                                           'Key-User logic is executed inside a hardened sandbox running **Restricted '
                                           'ABAP Cloud**:\n'
                                           '\n'
                                           '#### The Sandbox Security Rules:\n'
                                           '1. **Forbidden Statements**:\n'
                                           '   - No direct database writes (`INSERT`, `UPDATE`, `DELETE`).\n'
                                           '   - No transactional commit calls (`COMMIT WORK`, `ROLLBACK WORK`).\n'
                                           "   - No dynamic programming (`CALL 'SYSTEM'`, `ASSIGN`).\n"
                                           '   - No file system or operating system access.\n'
                                           '2. **Allowed Operations**:\n'
                                           '   - Safe control structures: `IF`, `CASE`, `LOOP AT`, `ASSIGN '
                                           'COMPONENT`.\n'
                                           '   - String, date, and math calculations.\n'
                                           '   - Read access exclusively through released C1 CDS views and APIs.\n'
                                           '3. **Automated Transport**:\n'
                                           '   - Key-User extensions are bundled into Software Collections and '
                                           'transported cleanly to Test and Production via the *Export / Import '
                                           'Software Collection* Fiori apps.',
                             'key_terms': [   {   'definition': 'Sandboxed subset of ABAP language preventing database '
                                                                'mutation and system-level operations.',
                                                  'term': 'Restricted ABAP Cloud'},
                                              {   'definition': 'Released enhancement hook executed in the key-user '
                                                                'sandbox for custom validation or derivation logic.',
                                                  'term': 'Cloud BAdI'}],
                             'step_id': 'd70_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Restricted ABAP Cloud enforces safety: no direct SQL writes, no commit work, '
                                         'and automatic lifecycle management via software collections.',
                             'title': 'Restricted ABAP Cloud Syntax & Sandboxed Execution'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'enabled_usage': [   'Fiori Manage Purchase Orders',
                                                                         'OData API',
                                                                         'PO Print Form'],
                                                    'entity': 'Purchasing Document Item',
                                                    'field_name': 'YY1_SensorCertID_PDI',
                                                    'type': 'Text (Length 20)'},
                             'content_md': '### Key-User Custom Logic Implementation (`Custom Fields and Logic` App)\n'
                                           '```abap\n'
                                           '// BAdI: Modify Purchase Order Item (MMPUR_PO_MODIFY_ITEM)\n'
                                           '// Business Rule: Sensor RAW-01 requires a valid Certification ID\n'
                                           "if purchaseorderitem-material = 'RAW-01' and "
                                           'purchaseorderitem-yy1_sensorcertid_pdi is initial.\n'
                                           "  purchaseorderitem-yy1_sensorcertid_pdi = 'PENDING-QC'.\n"
                                           'endif.\n'
                                           '```',
                             'scenario': "Nova's quality lead adds a mandatory inspection certificate field to "
                                         'component RAW-01 on purchase orders at Heidelberg (PL01).',
                             'step_id': 'd70_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Custom Field: Sensor Certification on PO Item'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'A key user attempts to write `COMMIT WORK` and `DELETE FROM ztable` '
                                            'inside a Cloud BAdI in the Custom Fields and Logic app. What happens?',
                             'options': [   {   'explanation': 'Correct! The Restricted ABAP sandbox blocks all direct '
                                                               'database mutation and transaction commit statements.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'The web-based editor syntax checker immediately flags compile '
                                                        'errors: `COMMIT WORK` and direct `DELETE` statements are '
                                                        'strictly forbidden in Restricted ABAP Cloud.'},
                                            {   'explanation': 'Impossible; the sandbox architecture is specifically '
                                                               'engineered to prevent unauthorized data corruption.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'The code runs and deletes the entire company database.'},
                                            {   'explanation': 'The ABAP Cloud sandbox compiles natively to ABAP '
                                                               'bytecode with restricted keywords.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'The browser converts the ABAP code into Python '
                                                        'automatically.'}],
                             'step_id': 'd70_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'The Restricted ABAP compiler rejects forbidden keywords (COMMIT, DELETE, '
                                         'direct SQL writes) before code can be activated.',
                             'title': 'Key-User Governance Simulation: Validating Allowed Statements'},
                         {   'instruction': 'As Enterprise Architect, how do you evaluate this request?',
                             'options': [   {   'explanation': 'Correct! Key-User Extensibility is the fastest, '
                                                               'lowest-cost Clean Core method for simple field and UI '
                                                               'extensions.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Reject the developer request. Use Key-User Extensibility '
                                                        '(Custom Fields app) to add the field and UI Adaptation to '
                                                        'place it on the screen in 15 minutes at zero development '
                                                        'cost.'},
                                            {   'explanation': 'Massive waste of budget and time when standard '
                                                               'low-code tools solve the requirement instantly.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Approve the $20,000 developer project because custom ABAP '
                                                        'code is always better.'},
                                            {   'explanation': 'Unacceptable; warranty tracking is a standard business '
                                                               'requirement.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Tell the business that warranty expiration dates cannot be '
                                                        'stored in ERP.'}],
                             'scenario': 'Nova Manufacturing needs to add a simple warranty expiration date field to '
                                         'the Customer Master Fiori screen. A developer requests 2 weeks and $20,000 '
                                         'to build a custom Eclipse ADT RAP project.',
                             'step_id': 'd70_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Extensibility Decision Challenge: Key-User vs Developer Extensibility'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'key-user-extensibility',
                                                  'explanation': '`Custom Fields and Logic` is the central Fiori app '
                                                                 'for Key-User in-app extensibility.',
                                                  'id': 'd70_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Custom Fields and Logic Fiori App'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Transaction SE11'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Transaction SE38'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'Notepad'}],
                                                  'prompt': 'What is the primary architectural tool in SAP S/4HANA '
                                                            'used by business experts to add custom fields to standard '
                                                            'entities without writing code?',
                                                  'question_id': 'd70_q1'},
                                              {   'concept_slug': 'restricted-abap-cloud',
                                                  'explanation': '`COMMIT WORK` is strictly forbidden because '
                                                                 'transactional commit boundaries are managed '
                                                                 'exclusively by the framework.',
                                                  'id': 'd70_q2',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'COMMIT WORK'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'IF ... ENDIF.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'CASE ... ENDCASE.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'LOOP AT ... ENDLOOP.'}],
                                                  'prompt': 'Which of the following statements is strictly forbidden '
                                                            'when writing custom logic in the Key-User Cloud BAdI '
                                                            'editor?',
                                                  'question_id': 'd70_q2'},
                                              {   'concept_slug': 'custom-fields-and-logic',
                                                  'explanation': 'UI Adaptation enables visual drag-and-drop screen '
                                                                 'customization directly inside the browser.',
                                                  'id': 'd70_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It allows authorized key users to '
                                                                             'visually move, hide, and rename fields '
                                                                             'on live screens without modifying '
                                                                             'frontend code.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': "It changes the user's desktop "
                                                                             'wallpaper.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It downloads MP3 files.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It converts the screen into an Excel '
                                                                             'spreadsheet.'}],
                                                  'prompt': "What capability does 'UI Adaptation at Runtime' provide "
                                                            'in modern SAP Fiori applications?',
                                                  'question_id': 'd70_q3'},
                                              {   'concept_slug': 'key-user-extensibility',
                                                  'explanation': 'Software Collections package and transport Key-User '
                                                                 'extensions across the 3SL landscape.',
                                                  'id': 'd70_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Export and Import Software Collection '
                                                                             'Fiori apps'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Copying and pasting files over FTP'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Emailing code snippets to SAP support'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Re-entering all fields manually in each '
                                                                             'system'}],
                                                  'prompt': 'How are Key-User extensions (custom fields, UI '
                                                            'adaptations) deployed from the Development tenant to Test '
                                                            'and Production in S/4HANA Cloud?',
                                                  'question_id': 'd70_q4'}],
                             'step_id': 'd70_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 70 Verification Assessment'},
                         {   'step_id': 'd70_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Applied Key-User Extensibility to create custom fields and adapt Fiori '
                                           'UI layouts at runtime.\n'
                                           '- Implemented sandboxed Cloud BAdIs using Restricted ABAP Cloud syntax.\n'
                                           '- Transported low-code extensions across the 3SL landscape via Software '
                                           'Collections.',
                             'title': 'Day 70 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd70_s8_completion',
                             'recommended_mission': {'slug': 'nova-key-user-custom-fields', 'title': 'Key-User Extensibility Custom Fields', 'description': 'Add regulated environmental tracking fields using Key-User tools.'},
                             'step_type': 'completion',
                             'summary_md': 'Superb work! You have mastered low-code in-app extensions. Tomorrow, you '
                                           'will step into professional cloud development: **Developer Extensibility '
                                           'On-Stack using the ABAP Cloud Language Version in Eclipse ADT**.',
                             'title': 'Day 70 Complete: Key-User Extensibility Mastered'}],
            'subtitle': 'Custom Fields and Logic app, UI adaptation at runtime, restricted ABAP Cloud, and business '
                        'user extensibility.',
            'title': 'Key-User Extensibility (In-App)'},
    71: {   'atomic_concepts': ['developer-extensibility-on-stack', 'abap-cloud-language-version', 'released-apis-c1'],
            'day_number': 71,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'developer-extensibility-on-stack',
            'steps': [   {   'content_md': '### Pro-Code Development Directly on the S/4HANA Stack\n'
                                           'When business requirements exceed Key-User low-code capabilities (e.g., '
                                           'complex data processing, custom business objects, multi-entity '
                                           'validations), developers use **Developer Extensibility (Tier 2)**.\n'
                                           '\n'
                                           '#### Core Foundations of On-Stack Developer Extensibility:\n'
                                           '1. **Development Environment**: Exclusively **Eclipse with ABAP '
                                           'Development Tools (ADT)**. Classic SAP GUI development tools (`SE38`, '
                                           '`SE80`, `SE11`) are disabled or unsupported for ABAP Cloud development.\n'
                                           "2. **Language Version: 'ABAP for Cloud Development'**:\n"
                                           '   - Packages are flagged with the *ABAP for Cloud Development* language '
                                           'version.\n'
                                           '   - The compiler strictly enforces ABAP Cloud rules: obsolete legacy '
                                           'syntax (e.g., header lines, `TABLES`, `FORM` routines, '
                                           '`MOVE-CORRESPONDING` without exact typing) triggers compilation errors.\n'
                                           '3. **Released APIs (Contract C1)**:\n'
                                           '   - Custom code can only access SAP objects that have an official **C1 '
                                           'Release Contract**.\n'
                                           '   - Direct access to internal database tables or unreleased function '
                                           'modules is completely blocked.\n'
                                           '4. **RAP as the Core Architecture**:\n'
                                           '   - Custom applications are built using the **ABAP RESTful Application '
                                           'Programming Model (RAP)** with CDS view entities, behavior definitions, '
                                           'and service bindings.',
                             'key_terms': [   {   'definition': 'Pro-code development directly on the S/4HANA stack '
                                                                'using restricted ABAP Cloud and Eclipse ADT.',
                                                  'term': 'Developer Extensibility (Tier 2)'},
                                              {   'definition': 'Strict ABAP language version enforcing modern '
                                                                'object-oriented principles and released API usage.',
                                                  'term': 'ABAP for Cloud Development'},
                                              {   'definition': 'Official modern IDE for ABAP development replacing '
                                                                'legacy SAP GUI SE80.',
                                                  'term': 'Eclipse ADT'}],
                             'step_id': 'd71_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'On-Stack Developer Extensibility runs pro-code ABAP Cloud in Eclipse ADT '
                                         'using released C1 APIs and RAP architecture.',
                             'title': 'The On-Stack Developer Extensibility Model'},
                         {   'content_md': '### Structuring Cloud-Compliant ABAP Artifacts\n'
                                           'To maintain Clean Core governance across large development teams, ABAP '
                                           'Cloud organizes artifacts into structured packages:\n'
                                           '\n'
                                           '#### 1. Software Component Assignment\n'
                                           '- Development artifacts belong to custom Software Components (e.g., '
                                           '`ZCUSTOM_APP`).\n'
                                           '- Software Components are decoupled from standard SAP software components '
                                           '(`SAP_BASIS`, `SAP_APPL`), ensuring clean separation.\n'
                                           '\n'
                                           '#### 2. Package-Level Language Enforcement\n'
                                           '- In Eclipse ADT, every package specifies `ABAP Language Version: ABAP for '
                                           'Cloud Development`.\n'
                                           '- Any attempt to create a program using classic dynpros or unreleased '
                                           'tables inside this package fails compile-time checks.\n'
                                           '\n'
                                           '#### 3. ABAP Test Cockpit (ATC) Enforcement\n'
                                           '- Transports cannot be released unless the code passes mandatory ATC check '
                                           'variants (`ABAP_CLOUD_READINESS`).\n'
                                           '- ATC checks verify: zero unreleased API calls, strict error handling, and '
                                           'unit test coverage (`AUnit`).',
                             'key_terms': [   {   'definition': 'Top-level delivery unit grouping custom ABAP packages '
                                                                'for lifecycle and transport management.',
                                                  'term': 'Software Component'},
                                              {   'definition': 'Standard ATC check variant verifying compliance with '
                                                                'ABAP Cloud rules.',
                                                  'term': 'ABAP_CLOUD_READINESS'}],
                             'step_id': 'd71_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Packages enforce the ABAP for Cloud Development version, and ATC gates '
                                         'prevent non-compliant code from being transported.',
                             'title': 'Package Architecture, Software Components & ATC Quality Gates'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'ide': 'Eclipse ADT 3.36',
                                                    'language_version': 'ABAP for Cloud Development',
                                                    'package': 'ZNOVA_ROBOTICS_CORE'},
                             'content_md': '### Cloud-Compliant ABAP Class in Eclipse ADT\n'
                                           '```abap\n'
                                           'CLASS zcl_nova_robotics_eval DEFINITION\n'
                                           '  PUBLIC\n'
                                           '  FINAL\n'
                                           '  CREATE PUBLIC.\n'
                                           '\n'
                                           '  PUBLIC SECTION.\n'
                                           '    INTERFACES if_oo_adt_classrun.\n'
                                           '    METHODS evaluate_sensor_health\n'
                                           '      IMPORTING iv_plant TYPE werks_d\n'
                                           '      RETURNING VALUE(rv_health_score) TYPE i.\n'
                                           'ENDCLASS.\n'
                                           '\n'
                                           'CLASS zcl_nova_robotics_eval IMPLEMENTATION.\n'
                                           '  METHOD evaluate_sensor_health.\n'
                                           '    // Consuming released C1 CDS View Entity\n'
                                           '    SELECT SINGLE FROM I_Plant\n'
                                           '      FIELDS PlantName\n'
                                           '      WHERE Plant = @iv_plant\n'
                                           '      INTO @DATA(lv_plant_name).\n'
                                           '\n'
                                           '    rv_health_score = 98.\n'
                                           '  ENDMETHOD.\n'
                                           'ENDCLASS.\n'
                                           '```',
                             'scenario': "Nova's developer builds an on-stack ABAP Cloud service in Eclipse ADT to "
                                         'track robotics calibration data for assembly line PL01.',
                             'step_id': 'd71_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing On-Stack Service: Predictive Tool Maintenance'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'Audit the following code snippet submitted by a legacy developer. Which '
                                            'line triggers an ABAP Cloud compile error?',
                             'options': [   {   'explanation': 'Correct! `TABLES` statements and querying unreleased '
                                                               'tables like `EKKO` directly are forbidden in ABAP '
                                                               'Cloud.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Line: `TABLES: ekko.` (Header-line dictionary declaration) '
                                                        'and `SELECT * FROM ekko WHERE ...` (Direct unreleased table '
                                                        'query).'},
                                            {   'explanation': 'Standard ABAP Objects class definition is fully '
                                                               'supported.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Line: `CLASS zcl_test DEFINITION PUBLIC.`'},
                                            {   'explanation': 'Inline data declarations are standard modern ABAP.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': "Line: `DATA(lv_name) = 'Nova'.`"}],
                             'step_id': 'd71_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'ABAP Cloud bans legacy constructs (`TABLES`, header lines, obsolete internal '
                                         'tables) and unreleased table queries.',
                             'title': 'ABAP Cloud Technical Audit: Identifying Forbidden Legacy Syntax'},
                         {   'instruction': 'What is the Clean Core on-stack alternative?',
                             'options': [   {   'explanation': 'Correct! OData V4 Web APIs built via RAP are the '
                                                               'strategic, cloud-compliant replacement for legacy '
                                                               'RFCs.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Build a modern RAP Business Object with a Service Definition, '
                                                        'bind it as an OData V4 Web API in Eclipse ADT, and protect it '
                                                        'with OAuth2 authentication.'},
                                            {   'explanation': 'Fails cloud security standards, lacks modern OData '
                                                               'semantics, and violates Clean Core.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Approve the RFC because RFCs have worked since 1992.'},
                                            {   'explanation': 'Severe security violation exposing the core database '
                                                               'to the internet.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Open port 3300 on the database firewall to allow direct ODBC '
                                                        'access.'}],
                             'scenario': 'A legacy team wants to expose customer data to a new web app by writing an '
                                         'un-typed RFC function module using `CALL FUNCTION ... DESTINATION`.',
                             'step_id': 'd71_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Architectural Challenge: Legacy RFC vs ABAP Cloud Service Exposure'},
                         {   'assessment_type': 'technical_audit',
                             'questions': [   {   'concept_slug': 'abap-cloud-language-version',
                                                  'explanation': '`ABAP for Cloud Development` is the language version '
                                                                 'enforcing cloud rules and released APIs.',
                                                  'id': 'd71_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'ABAP for Cloud Development'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Standard ABAP (Classic)'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'ABAP for Mainframe R/2'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Visual Basic for SAP'}],
                                                  'prompt': 'What is the official ABAP language version required for '
                                                            'packages implementing On-Stack Developer Extensibility in '
                                                            'S/4HANA Cloud?',
                                                  'question_id': 'd71_q1'},
                                              {   'concept_slug': 'released-apis-c1',
                                                  'explanation': 'Unreleased objects cannot be compiled in ABAP Cloud '
                                                                 'packages.',
                                                  'id': 'd71_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'The compiler throws a syntax error '
                                                                             'because table `EKKO` is an unreleased '
                                                                             'internal object without a C1 contract.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'The code executes normally without '
                                                                             'warning.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'The database automatically deletes the '
                                                                             'table.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'The user is logged out of Windows.'}],
                                                  'prompt': 'If a developer in an ABAP Cloud package attempts to '
                                                            'execute `SELECT * FROM ekko`, what happens during '
                                                            'compilation in Eclipse ADT?',
                                                  'question_id': 'd71_q2'},
                                              {   'concept_slug': 'developer-extensibility-on-stack',
                                                  'explanation': 'Eclipse ADT is the exclusive supported development '
                                                                 'tool for ABAP Cloud.',
                                                  'id': 'd71_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Eclipse with ABAP Development Tools '
                                                                             '(ADT)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'SAP GUI Transaction SE38'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Microsoft Visual Studio 2008'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Sublime Text'}],
                                                  'prompt': 'Which integrated development environment (IDE) is '
                                                            'mandatory for developing ABAP Cloud applications in '
                                                            'modern SAP S/4HANA?',
                                                  'question_id': 'd71_q3'},
                                              {   'concept_slug': 'abap-cloud-language-version',
                                                  'explanation': 'RAP is the strategic application framework for all '
                                                                 'on-stack development.',
                                                  'id': 'd71_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'ABAP RESTful Application Programming '
                                                                             'Model (RAP)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Classic Dynpro Screen Painter'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Web Dynpro ABAP'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Business Server Pages (BSP)'}],
                                                  'prompt': 'Which modern programming model is the foundation for '
                                                            'building transactional business applications in On-Stack '
                                                            'Developer Extensibility?',
                                                  'question_id': 'd71_q4'}],
                             'step_id': 'd71_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 71 Verification Assessment'},
                         {   'step_id': 'd71_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered On-Stack Developer Extensibility (Tier 2) in Eclipse ADT.\n'
                                           "- Enforced the 'ABAP for Cloud Development' language version and released "
                                           'C1 API compliance.\n'
                                           '- Audited code to eliminate legacy un-typed syntax and direct table access '
                                           'in favor of RAP services.',
                             'title': 'Day 71 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd71_s8_completion',
                             'recommended_mission': {'slug': 'nova-developer-extensibility-adt', 'title': 'On-Stack Developer Extensibility in ADT', 'description': 'Build Tier 1 ABAP Cloud extension on S/4HANA stack.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You understand on-stack cloud development. Tomorrow, you will '
                                           'master the third extensibility tier: **Side-by-Side Extensibility on SAP '
                                           'Business Technology Platform (BTP)**.',
                             'title': 'Day 71 Complete: On-Stack Developer Extensibility Mastered'}],
            'subtitle': 'ABAP Cloud language version in Eclipse ADT, released C1 APIs, RAP on-stack development, and '
                        'package governance.',
            'title': 'Developer Extensibility (On-Stack ABAP Cloud)'},
    72: {   'atomic_concepts': ['side-by-side-extensibility', 'btp-extension-architecture'],
            'day_number': 72,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'side-by-side-extensibility-btp',
            'steps': [   {   'content_md': '### Completely Decoupled Cloud Innovations\n'
                                           'While On-Stack extensibility runs directly inside the S/4HANA instance, '
                                           '**Side-by-Side Extensibility (Tier 3)** runs completely outside S/4HANA on '
                                           'the **SAP Business Technology Platform (BTP)**.\n'
                                           '\n'
                                           '#### Why Build Side-by-Side on BTP?\n'
                                           '1. **Zero Core Footprint**: Custom code runs in independent BTP containers '
                                           '(Cloud Foundry or Kyma/Kubernetes), consuming zero S/4HANA database or CPU '
                                           'resources.\n'
                                           '2. **Polyglot Technology Freedom**: Develop using the **SAP Cloud '
                                           'Application Programming Model (CAP)** in Node.js / TypeScript, Java, or '
                                           'Python, in addition to ABAP Cloud via BTP ABAP Environment.\n'
                                           '3. **External Audience Security**: Customer portals, supplier '
                                           'collaboration apps, or public consumer apps run safely on BTP without '
                                           'granting external users direct network access to the core ERP.\n'
                                           '4. **Independent Lifecycle**: BTP microservices can be updated, '
                                           'redeployed, and scaled multiple times per day without touching or testing '
                                           'the core ERP.',
                             'key_terms': [   {   'definition': 'Building decoupled applications on SAP BTP that '
                                                                'integrate with S/4HANA via remote APIs and events.',
                                                  'term': 'Side-by-Side Extensibility (Tier 3)'},
                                              {   'definition': 'Business Technology Platform: unified cloud platform '
                                                                'for integration, data, AI, and extensibility.',
                                                  'term': 'SAP BTP'},
                                              {   'definition': 'Cloud Application Programming Model: framework of '
                                                                'languages, libraries, and tools for building '
                                                                'enterprise services.',
                                                  'term': 'SAP CAP'}],
                             'step_id': 'd72_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Side-by-Side on BTP decouples extensions from S/4HANA, running polyglot apps '
                                         'with zero core resource consumption.',
                             'title': 'The Side-by-Side Extensibility Tier (Tier 3)'},
                         {   'content_md': '### Selecting the Right Extensibility Tier\n'
                                           'Architects use the official SAP Clean Core decision matrix to assign '
                                           'requirements to the optimal tier:\n'
                                           '\n'
                                           '| Criteria | Tier 1: Key-User (In-App) | Tier 2: Developer On-Stack | Tier '
                                           '3: Side-by-Side (BTP) |\n'
                                           '|---|---|---|---|\n'
                                           '| **Audience** | Business Analysts / Key Users | Professional ABAP '
                                           'Developers | Full-Stack / Polyglot Developers |\n'
                                           '| **Tooling** | Fiori Web Apps | Eclipse ADT | VS Code / Business '
                                           'Application Studio |\n'
                                           '| **Technology** | Low-code / Restricted ABAP | ABAP Cloud & RAP | CAP '
                                           '(Node/Java), Kyma, Python |\n'
                                           '| **Data Locality** | Tightly coupled to standard entities | Direct, '
                                           'high-speed on-database SQL | Remote REST/OData / Event Mesh |\n'
                                           '| **Best For** | Custom fields, UI layout, simple BAdIs | Core '
                                           'transactional logic, tight DB coupling | Portals, SaaS apps, AI, partner '
                                           'apps |',
                             'key_terms': [   {   'definition': 'Authoritative guide categorizing extensions into '
                                                                'Key-User, On-Stack, or Side-by-Side.',
                                                  'term': 'Tri-Tier Decision Matrix'},
                                              {   'definition': 'BTP cloud messaging service routing asynchronous '
                                                                'business events between S/4HANA and extensions.',
                                                  'term': 'SAP Event Mesh'}],
                             'step_id': 'd72_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Use Tier 1 for simple fields/UI, Tier 2 for tight transactional data logic, '
                                         'and Tier 3 for decoupled external apps.',
                             'title': 'The Tri-Tier Extensibility Decision Matrix'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'framework': 'SAP CAP (Node.js/TypeScript) + Fiori Elements',
                                                    'integration': 'SAP Event Mesh + S/4HANA OData V4 Purchase Order '
                                                                   'API',
                                                    'solution': 'Side-by-Side Extension on SAP BTP'},
                             'content_md': '### Architecture Diagram: Nova Supplier Portal (BTP Tier 3)\n'
                                           '```\n'
                                           '[External Vendors: VEND-101 in Germany]\n'
                                           '         │  HTTPS / Public Internet\n'
                                           '         ▼\n'
                                           '[SAP BTP: Custom Supplier Portal App (CAP / Node.js)]\n'
                                           '  ├── Authenticated via SAP Cloud Identity Services\n'
                                           '  ├── Scales elastically on Cloud Foundry\n'
                                           '  └── Zero access to internal corporate network\n'
                                           '         │\n'
                                           '         │  SAP Cloud Connector & Principal Propagation\n'
                                           '         ▼\n'
                                           '[S/4HANA Private Cloud: Heidelberg NM01]\n'
                                           '  ├── Releases PurchaseOrder.Created Business Event via Event Mesh\n'
                                           '  └── Receives confirmed delivery dates via OData V4 API\n'
                                           '```',
                             'scenario': 'Nova Manufacturing builds a public-facing Supplier Portal allowing 400 '
                                         'global vendors (including VEND-101) to confirm purchase orders and upload '
                                         'shipping manifests.',
                             'step_id': 'd72_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Global Supplier Portal Architecture'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'Evaluate the following three requirements and match them to the correct '
                                            'Clean Core Extensibility Tier.',
                             'options': [   {   'explanation': 'Correct! This perfectly aligns with data locality, '
                                                               'user audience, and architectural decoupling '
                                                               'principles.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': '1. Add a custom field to PO Header -> Tier 1 (Key-User). 2. '
                                                        'High-volume scrap calculation looping on MATDOC -> Tier 2 '
                                                        '(On-Stack). 3. Public vendor portal with mobile notifications '
                                                        '-> Tier 3 (BTP Side-by-Side).'},
                                            {   'explanation': 'Violates modern security, exposes the core to public '
                                                               'web traffic, and destroys Clean Core.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Build everything as a single monolithic ABAP dynpro in Tier '
                                                        '2.'},
                                            {   'explanation': 'Direct database hacking is strictly forbidden in Clean '
                                                               'Core.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Build all custom fields by modifying S/4HANA database tables '
                                                        'directly.'}],
                             'step_id': 'd72_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Key-User for fields, On-Stack for tight transactional loops, and '
                                         'Side-by-Side on BTP for external portals and innovation.',
                             'title': 'Extensibility Tier Selection Simulation'},
                         {   'instruction': 'As Chief Enterprise Architect, what is your ruling?',
                             'options': [   {   'explanation': 'Correct! S/4HANA core systems must never be exposed '
                                                               'directly to public internet traffic; the SAP Cloud '
                                                               'Connector establishes a secure reverse-tunnel.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Reject direct internet exposure. Mandate building a '
                                                        'Side-by-Side microservice on SAP BTP; connect BTP to S/4HANA '
                                                        'securely via the SAP Cloud Connector with mutual TLS and '
                                                        'strict API scoping.'},
                                            {   'explanation': 'Catastrophic security failure that invites ransomware '
                                                               'attacks.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Open the firewall and disable passwords for the marketing '
                                                        'agency.'},
                                            {   'explanation': 'Violates GDPR, CCPA, and enterprise confidentiality.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Email a copy of the entire customer database to the agency as '
                                                        'an unencrypted Excel file.'}],
                             'scenario': 'A marketing agency demands direct public internet access to port 443 of the '
                                         'production S/4HANA core to read customer data for a mobile promotion.',
                             'step_id': 'd72_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Integration Security Challenge: Exposing S/4HANA to the Internet'},
                         {   'assessment_type': 'decision_matrix',
                             'questions': [   {   'concept_slug': 'side-by-side-extensibility',
                                                  'explanation': 'SAP BTP is the strategic platform for decoupled '
                                                                 'Side-by-Side extensibility.',
                                                  'id': 'd72_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'SAP Business Technology Platform (BTP)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Local developer USB drives'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Windows Desktop Active Directory'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'SAP GUI Dynpro Painter'}],
                                                  'prompt': 'What is the primary architectural platform used for '
                                                            'building Tier 3 Side-by-Side extensions for SAP S/4HANA?',
                                                  'question_id': 'd72_q1'},
                                              {   'concept_slug': 'btp-extension-architecture',
                                                  'explanation': 'SAP CAP is the premier framework for building '
                                                                 'enterprise cloud services on BTP.',
                                                  'id': 'd72_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'SAP Cloud Application Programming Model '
                                                                             '(CAP)'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'COBOL 74'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Visual Basic 6.0'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Adobe Flash'}],
                                                  'prompt': 'Which enterprise development framework provides '
                                                            'languages, libraries, and best practices for building '
                                                            'microservices in Node.js or Java on SAP BTP?',
                                                  'question_id': 'd72_q2'},
                                              {   'concept_slug': 'side-by-side-extensibility',
                                                  'explanation': 'BTP provides a secure cloud DMZ isolating external '
                                                                 'web traffic from the internal ERP core.',
                                                  'id': 'd72_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It protects the core ERP by hosting the '
                                                                             'external application in a secure cloud '
                                                                             'perimeter without direct database '
                                                                             'exposure.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'BTP eliminates the need for any internet '
                                                                             'connection.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'BTP converts all data into paper '
                                                                             'documents.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'External vendors do not need user '
                                                                             'accounts.'}],
                                                  'prompt': 'Why is Side-by-Side extensibility on BTP preferred when '
                                                            'developing public-facing portals for external vendors or '
                                                            'consumers?',
                                                  'question_id': 'd72_q3'},
                                              {   'concept_slug': 'btp-extension-architecture',
                                                  'explanation': 'The SAP Cloud Connector creates an encrypted reverse '
                                                                 'tunnel connecting BTP to on-premise/private systems '
                                                                 'securely.',
                                                  'id': 'd72_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'SAP Cloud Connector'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'Telnet'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'FTP Server'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Remote Desktop Protocol (RDP)'}],
                                                  'prompt': 'What SAP component establishes a secure, outbound-only '
                                                            'reverse tunnel between SAP BTP and on-premise or private '
                                                            'cloud S/4HANA instances without opening inbound firewall '
                                                            'ports?',
                                                  'question_id': 'd72_q4'}],
                             'step_id': 'd72_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 72 Verification Assessment'},
                         {   'step_id': 'd72_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered Side-by-Side Extensibility (Tier 3) on SAP Business Technology '
                                           'Platform (BTP).\n'
                                           '- Applied the Tri-Tier Decision Matrix to match business requirements to '
                                           'Key-User, On-Stack, or Side-by-Side tiers.\n'
                                           '- Designed secure hybrid integration architectures using the SAP Cloud '
                                           'Connector and SAP CAP.',
                             'title': 'Day 72 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd72_s8_completion',
                             'recommended_mission': {'slug': 'nova-btp-side-by-side-extension', 'title': 'Side-by-Side BTP Extension Architecture', 'description': 'Decouple dealer portal logic onto BTP Kyma runtime.'},
                             'step_type': 'completion',
                             'summary_md': 'Brilliant work! You now understand all three tiers of the Clean Core '
                                           'Extensibility Framework. Tomorrow, you will master the critical data '
                                           'transition engine: **The SAP Data Migration Cockpit**.',
                             'title': 'Day 72 Complete: Side-by-Side Extensibility Mastered'}],
            'subtitle': 'Decoupled extensions on SAP BTP, Cloud Application Programming (CAP) model, event-driven '
                        'integration, and multi-cloud.',
            'title': 'Side-by-Side Extensibility on SAP BTP'},
    73: {   'atomic_concepts': ['data-migration-cockpit', 'migration-staging-tables'],
            'day_number': 73,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'data-migration-cockpit-ltmc',
            'steps': [   {   'content_md': '### Modernizing Data Transition to S/4HANA\n'
                                           'Data migration is historically the highest-risk workstream in ERP '
                                           'projects. In S/4HANA, the **SAP S/4HANA Migration Cockpit** is the '
                                           'mandatory, comprehensive tool for loading legacy master and transactional '
                                           'data into both Cloud and On-Premise environments.\n'
                                           '\n'
                                           '#### Migration Approaches Supported:\n'
                                           '1. **Migrate Data Using Staging Tables (Universal Standard)**:\n'
                                           '   - SAP provides pre-built **Migration Objects** (e.g., *Customer*, '
                                           '*Supplier*, *Material*, *G/L Open Items*, *Purchase Order*).\n'
                                           '   - Each migration object generates a dedicated set of relational '
                                           '**Staging Tables** in the SAP HANA database.\n'
                                           '   - Legacy data is populated into staging tables via XML file templates, '
                                           'CSV files, or direct database ETL extraction.\n'
                                           '2. **Direct Transfer from SAP System (On-Premise / Private Cloud)**:\n'
                                           '   - Connects directly to a source SAP ECC 6.0 system via RFC, reading '
                                           'data structures and mapping them automatically into S/4HANA.',
                             'key_terms': [   {   'definition': 'Authoritative S/4HANA tool for orchestrating, '
                                                                'validating, and executing data migration loads.',
                                                  'term': 'Migration Cockpit'},
                                              {   'definition': 'Pre-configured business entity containing staging '
                                                                'tables, mapping rules, and posting APIs.',
                                                  'term': 'Migration Object'},
                                              {   'definition': 'Temporary relational database tables in HANA '
                                                                'buffering legacy data prior to validation and '
                                                                'posting.',
                                                  'term': 'Staging Tables'}],
                             'step_id': 'd73_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Migration Cockpit uses pre-configured Migration Objects and HANA staging '
                                         'tables to validate and post legacy data.',
                             'title': 'The Central Migration Engine in S/4HANA'},
                         {   'content_md': '### Rigorous Data Validation & Loading Sequence\n'
                                           'The Migration Cockpit enforces a deterministic 4-step execution sequence '
                                           'to guarantee data integrity:\n'
                                           '\n'
                                           '1. **Extract / Populate Staging Tables**:\n'
                                           '   - Legacy records are extracted from source systems and inserted into '
                                           'the staging tables.\n'
                                           '2. **Step 1: Validate Data**:\n'
                                           '   - Syntax and format check. Verifies data types, mandatory fields, and '
                                           'field lengths without hitting business posting logic.\n'
                                           '3. **Step 2: Convert Values (Mapping Tasks)**:\n'
                                           '   - Resolves legacy codes to S/4HANA target customizing (e.g., mapping '
                                           'legacy vendor `V100` to S/4HANA Business Partner `VEND-101`, or legacy '
                                           'payment term `0001` to `NT30`).\n'
                                           '   - Mappings are stored centrally and re-used across subsequent '
                                           'simulation and migration runs.\n'
                                           '4. **Step 3: Simulate**:\n'
                                           '   - Executes standard S/4HANA posting APIs in test mode. Fully validates '
                                           'accounting rules, duplicate checks, and master data dependencies without '
                                           'committing records to the database.\n'
                                           '5. **Step 4: Execute Migration (Post)**:\n'
                                           '   - Commits records into official S/4HANA tables (`BUT000`, `MARA`, '
                                           '`ACDOCA`).',
                             'key_terms': [   {   'definition': 'Rules translating legacy source values into target '
                                                                'S/4HANA customizing codes.',
                                                  'term': 'Mapping Tasks'},
                                              {   'definition': 'Test run executing real posting APIs without database '
                                                                'commit to identify business errors early.',
                                                  'term': 'Simulation Phase'}],
                             'step_id': 'd73_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'The migration pipeline executes in 4 strict stages: Validate -> Convert '
                                         'Values -> Simulate -> Execute (Post).',
                             'title': 'The Four-Step Migration Execution Pipeline'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'mapping_sample': "Legacy Code 'DE_OPT_99' -> Target S/4HANA BP "
                                                                      "'VEND-101' (Rheinland Precision)",
                                                    'migration_object': 'Supplier (SI_MM_SUPPLIER)',
                                                    'staging_table': '/1LT/DS_NM01_001'},
                             'content_md': '### Execution Status in Migration Cockpit\n'
                                           '```\n'
                                           '[Migration Object: Supplier]\n'
                                           '  ├── Records in Staging: 5,000\n'
                                           '  ├── Step 1: Validate Data ──────> 5,000 Valid (0 Errors)\n'
                                           '  ├── Step 2: Convert Values ─────> 12 Mapping Tasks Confirmed (Payment '
                                           'terms, Tax codes, Reconciliation G/L)\n'
                                           '  ├── Step 3: Simulate ───────────> 4,998 Success, 2 Failed (Duplicate VAT '
                                           'Registration Number)\n'
                                           '  └── Step 4: Execute Migration ──> 4,998 Business Partners Created in '
                                           'BUT000 / LFA1\n'
                                           '```',
                             'scenario': 'Nova Manufacturing migrates 5,000 legacy suppliers into Business Partners '
                                         'for Company Code NM01 in Heidelberg.',
                             'step_id': 'd73_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Master Data Migration: Business Partners'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'During Step 3 (Simulate), 150 material master records fail with error: '
                                            "'Valuation Class 3000 not allowed for Material Type RAW'. How do you "
                                            'resolve this?',
                             'options': [   {   'explanation': 'Correct! Value conversion mappings translate source '
                                                               'codes to valid target customizing without '
                                                               're-extracting data.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Update the Value Conversion mapping task in Migration Cockpit '
                                                        'to map legacy valuation class to valid target class `3001` '
                                                        '(Raw Materials), then re-run simulation.'},
                                            {   'explanation': 'Direct database writes corrupt valuation tables and '
                                                               'violate S/4HANA financial integrity.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Bypass simulation and force-write the records directly to '
                                                        'table MARA using custom SQL.'},
                                            {   'explanation': 'Deleting active production materials prevents '
                                                               'manufacturing from ordering components.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Delete all 150 materials from the company product catalog.'}],
                             'step_id': 'd73_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Resolve business simulation errors by adjusting Mapping Tasks in the '
                                         'Migration Cockpit, then re-simulate.',
                             'title': 'Migration Cockpit Simulation: Resolving Simulation Failures'},
                         {   'instruction': 'How does an enterprise architect extend the Migration Object?',
                             'options': [   {   'explanation': 'Correct! `LTMOM` (Migration Object Modeler) is the '
                                                               'official tool for extending standard migration objects '
                                                               'with custom structures and rules.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Use the SAP Migration Object Modeler (transaction `LTMOM`) to '
                                                        'add the custom field to the source structure and map it to '
                                                        'the target BAPI/API parameter.'},
                                            {   'explanation': 'Screen recording scripts are slow, un-governed, '
                                                               'error-prone, and unmaintainable.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Abandon the Migration Cockpit and write a custom screen '
                                                        'recording script.'},
                                            {   'explanation': 'Inaccurate; LTMOM is designed specifically to support '
                                                               'custom field migration.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Tell the business that custom fields cannot be migrated.'}],
                             'scenario': 'Nova added a custom field `YY1_RoboticsCalib_MAT` to the Material Master. '
                                         'The standard Migration Cockpit object does not include this custom field in '
                                         'its default staging table.',
                             'step_id': 'd73_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Migration Architecture Challenge: Custom Fields in Migration Objects'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'data-migration-cockpit',
                                                  'explanation': 'Migration Cockpit is the modern, supported tool for '
                                                                 'S/4HANA data loading (LSMW is obsolete and '
                                                                 'unsupported).',
                                                  'id': 'd73_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'SAP S/4HANA Migration Cockpit'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'LSMW (Legacy System Migration '
                                                                             'Workbench)'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Microsoft Access'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'FileZilla FTP'}],
                                                  'prompt': 'What is the official SAP tool for loading legacy master '
                                                            'and transactional data into SAP S/4HANA?',
                                                  'question_id': 'd73_q1'},
                                              {   'concept_slug': 'migration-staging-tables',
                                                  'explanation': 'Staging tables buffer raw source data for validation '
                                                                 'and conversion before committing to production '
                                                                 'tables.',
                                                  'id': 'd73_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'They act as intermediate relational '
                                                                             'buffer tables in HANA where legacy data '
                                                                             'is staged, validated, and converted '
                                                                             'prior to posting.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'They store historical employee chat '
                                                                             'logs.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'They permanently replace the core '
                                                                             'database tables.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'They host temporary video recordings of '
                                                                             'training sessions.'}],
                                                  'prompt': "What is the function of 'Staging Tables' in the SAP "
                                                            'Migration Cockpit architecture?',
                                                  'question_id': 'd73_q2'},
                                              {   'concept_slug': 'data-migration-cockpit',
                                                  'explanation': 'Simulation verifies business rules, account '
                                                                 'determination, and master data references without '
                                                                 'database commits.',
                                                  'id': 'd73_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Standard business posting APIs execute '
                                                                             'all validation logic in test mode '
                                                                             'without committing changes to the '
                                                                             'database.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'The entire operating system reboots.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'All staging table data is deleted.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Real financial documents are posted '
                                                                             'permanently.'}],
                                                  'prompt': "What occurs during the 'Simulate' step of the Migration "
                                                            'Cockpit execution pipeline?',
                                                  'question_id': 'd73_q3'},
                                              {   'concept_slug': 'migration-staging-tables',
                                                  'explanation': '`LTMOM` (Migration Object Modeler) customizes '
                                                                 'migration structures, rules, and field mappings.',
                                                  'id': 'd73_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'LTMOM (Migration Object Modeler)'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'SE38'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'SM50'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'SU53'}],
                                                  'prompt': 'Which transaction is used by developers and consultants '
                                                            'to adjust mapping rules and add custom fields to '
                                                            'Migration Objects?',
                                                  'question_id': 'd73_q4'}],
                             'step_id': 'd73_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 73 Verification Assessment'},
                         {   'step_id': 'd73_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered SAP S/4HANA Migration Cockpit architecture (staging tables and '
                                           'direct transfer).\n'
                                           '- Orchestrated the 4-step execution pipeline (Validate, Convert Values, '
                                           'Simulate, Execute).\n'
                                           '- Extended migration structures with custom fields using the Migration '
                                           'Object Modeler (LTMOM).',
                             'title': 'Day 73 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd73_s8_completion',
                             'recommended_mission': {'slug': 'nova-migration-cockpit-staging', 'title': 'Data Migration Cockpit Staging Execution', 'description': 'Load supplier balances and material stocks via LTMC staging tables.'},
                             'step_type': 'completion',
                             'summary_md': 'Superb work! You know how to migrate enterprise data. Tomorrow, you will '
                                           'master quality assurance and regression protection: **Cloud Test '
                                           'Automation & Upgrade Regression Testing**.',
                             'title': 'Day 73 Complete: Data Migration Mastered'}],
            'subtitle': 'Data migration architecture: staging tables, direct transfer from SAP ECC, migration object '
                        'modeler (LTMOM), and validation.',
            'title': 'Data Migration Cockpit (Migrate Your Data)'},
    74: {   'atomic_concepts': ['cloud-test-automation', 'upgrade-regression-testing'],
            'day_number': 74,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'cloud-testing-quality-assurance',
            'steps': [   {   'content_md': '### Navigating Continuous Innovation Safely\n'
                                           'In traditional on-premise ERP, testing was performed once every 5 to 7 '
                                           'years during massive upgrade projects. In S/4HANA Cloud:\n'
                                           '- **Semi-annual major release upgrades** (e.g., 2402, 2408 in Public '
                                           'Cloud) are applied automatically by SAP.\n'
                                           '- **Bi-weekly continuous quality updates** deliver patches and security '
                                           'fixes.\n'
                                           '- **Manual testing is mathematically impossible**: Testing 200 business '
                                           'processes manually every two weeks would require full-time testing armies '
                                           'and still cause production outages.\n'
                                           '\n'
                                           '#### The Solution: The SAP Cloud Test Automation Tool\n'
                                           'S/4HANA Cloud includes a built-in, no-code **Test Automation Tool**:\n'
                                           '1. **Pre-Delivered Automated Test Scripts**: SAP delivers automated test '
                                           'scripts for all standard Best Practice Scope Items (e.g., automated '
                                           'execution of J45 procurement from PO to invoice).\n'
                                           '2. **Post-Upgrade Tests (PUT)**: During the mandatory 2-week upgrade '
                                           'window between Test tenant and Production upgrade, automated test suites '
                                           'execute automatically to certify release readiness.\n'
                                           '3. **Custom Test Plans**: Teams record, customize, and schedule automated '
                                           'test runs simulating daily operational workloads.',
                             'key_terms': [   {   'definition': 'Built-in S/4HANA Cloud tool for recording, '
                                                                'maintaining, and executing automated regression '
                                                                'tests.',
                                                  'term': 'Test Automation Tool'},
                                              {   'definition': 'Automated regression suite executed during cloud '
                                                                'upgrade windows to validate core processes.',
                                                  'term': 'Post-Upgrade Tests (PUT)'},
                                              {   'definition': 'Curated collection of automated test processes '
                                                                'scheduled for continuous regression execution.',
                                                  'term': 'Test Plan'}],
                             'step_id': 'd74_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Test automation is mandatory in the cloud; SAP delivers automated test '
                                         'scripts for Best Practices to execute Post-Upgrade Tests.',
                             'title': 'The Imperative of Test Automation in the Cloud'},
                         {   'content_md': '### Constructing Resilient Test Automations\n'
                                           'An automated test case in S/4HANA Cloud is composed of three architectural '
                                           'components:\n'
                                           '\n'
                                           '1. **Test Process**:\n'
                                           '   - Sequential steps mirroring human actions: Launch App -> Enter Vendor '
                                           '`VEND-101` -> Add Material `RAW-01` -> Click Save -> Read PO Number.\n'
                                           '2. **Test Data Container (TDC)**:\n'
                                           '   - Decouples test logic from hardcoded master data.\n'
                                           '   - Allows the same automated test script to run across Heidelberg '
                                           '(`Company NM01 / Plant PL01`) and Austin (`Company NM02 / Plant PL02`) '
                                           'simply by toggling data variants.\n'
                                           '3. **Verification & Assertion Steps**:\n'
                                           '   - The test does not just click buttons; it verifies outcome values '
                                           '(e.g., asserting that the generated Invoice status is `APPROVED` and the '
                                           'Net Value matches calculated tax).\n'
                                           '4. **Defect Auto-Logging**:\n'
                                           '   - When a step fails, the tool captures full DOM screenshots, network '
                                           'payload traces, and error logs for immediate developer remediation.',
                             'key_terms': [   {   'definition': 'Reusable data repository parameterizing test cases '
                                                                'across different organizational units.',
                                                  'term': 'Test Data Container (TDC)'},
                                              {   'definition': 'Automated check verifying that actual system output '
                                                                'matches expected business values.',
                                                  'term': 'Assertion'}],
                             'step_id': 'd74_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Test processes decouple from test data via Test Data Containers (TDCs) and '
                                         'use assertions to verify business results.',
                             'title': 'Anatomy of an Automated Test Case & Test Data Variants'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'execution_time': '1 hour 15 minutes (automated)',
                                                    'results': '41 Passed, 1 Failed (Custom field validation rule '
                                                               'mismatch on Sales Orders)',
                                                    'test_suite': 'Nova Global Core Regression (42 Processes)'},
                             'content_md': '### Automated Test Execution Summary\n'
                                           '```\n'
                                           '[Cloud Upgrade Window: 2408 Release applied to Test Tenant]\n'
                                           '  ├── Test Plan: ZNOVA_PUT_CORE_2408\n'
                                           '  │     ├── Process 1: J45 (Direct Procurement) ────────► PASSED (18.2s)\n'
                                           '  │     ├── Process 2: BNZ (Sales Order to Cash) ───────► FAILED '
                                           '(Assertion on Discount Field)\n'
                                           '  │     ├── Process 3: J58 (Accounting Period End) ─────► PASSED (42.1s)\n'
                                           '  │     └── Process 4-42: Production & Warehouse ───────► PASSED\n'
                                           '  │\n'
                                           '  └── Resolution: Remediate Cloud BAdI logic in Dev -> Transport to Test '
                                           '-> Re-run -> 100% Green\n'
                                           '```',
                             'scenario': 'During the semi-annual upgrade window, Nova executes its automated '
                                         'regression test suite on the Test tenant in Heidelberg.',
                             'step_id': 'd74_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Post-Upgrade Test Suite Execution'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'An automated regression test for Scope Item J45 fails post-upgrade '
                                            'because the sample plant `PL01` ran out of stock for test material '
                                            '`RAW-01`. Remediate the test data strategy.',
                             'options': [   {   'explanation': 'Correct! Robust test automation must ensure data '
                                                               'prerequisites (such as available stock) are fulfilled '
                                                               'prior to operational execution.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Add a pre-requisite test step to the Test Process that '
                                                        'automatically posts initial inventory via Goods Receipt '
                                                        '(MIGO), or configure dynamic test data generation in the '
                                                        'TDC.'},
                                            {   'explanation': 'Deleting tests removes regression safety and masks '
                                                               'production defects.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Delete the automated test so it stops failing.'},
                                            {   'explanation': "Test data maintenance is the customer's operational "
                                                               'responsibility.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'File a lawsuit against SAP.'}],
                             'step_id': 'd74_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Design automated test cases with self-sufficient test data prerequisites to '
                                         'prevent false-positive failures.',
                             'title': 'Quality Assurance Simulation: Resolving Upgrade Test Failures'},
                         {   'instruction': "How do you defend the 'Shift-Left' quality engineering approach?",
                             'options': [   {   'explanation': 'Correct! The Shift-Left testing paradigm catches '
                                                               'defects early in the lifecycle where they are cheapest '
                                                               'and safest to resolve.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Defects identified during cutover cost 100x more to fix, '
                                                        'cause catastrophic go-live delays, and risk data corruption. '
                                                        "Enforce 'Shift-Left': mandate ABAP Unit tests during "
                                                        'development, automated SIT during sprint realization, and '
                                                        'automated regression before cutover.'},
                                            {   'explanation': 'Violates professional engineering standards and leads '
                                                               'to project failure.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Agree with the manager because skipping tests lets developers '
                                                        'leave work early.'},
                                            {   'explanation': 'Testing in production destroys operational business '
                                                               'continuity.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Outsource all testing to end-users on production go-live '
                                                        'day.'}],
                             'scenario': 'A project manager suggests skipping unit testing during developer sprint '
                                         'realization and relying solely on the final cutover weekend to find bugs.',
                             'step_id': 'd74_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Testing Strategy Challenge: Shift-Left Testing Culture'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'cloud-test-automation',
                                                  'explanation': 'Frequent cloud releases demand automated regression '
                                                                 'to validate processes within tight upgrade windows.',
                                                  'id': 'd74_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Because frequent, automated cloud '
                                                                             'upgrades and quality patches make '
                                                                             'comprehensive manual testing impossible '
                                                                             'within release windows.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Because the cloud does not support human '
                                                                             'mouse clicks.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Because automated testing is required by '
                                                                             'browser copyright laws.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Because SAP deletes untested systems '
                                                                             'automatically.'}],
                                                  'prompt': 'Why is automated regression testing mandatory for '
                                                            'organizations running SAP S/4HANA Cloud?',
                                                  'question_id': 'd74_q1'},
                                              {   'concept_slug': 'upgrade-regression-testing',
                                                  'explanation': 'PUT validates standard and custom business processes '
                                                                 'following semi-annual cloud upgrades.',
                                                  'id': 'd74_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Automated test suites executed on the '
                                                                             'Test tenant following a cloud upgrade to '
                                                                             'certify that business processes continue '
                                                                             'functioning without regression.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Surveys sent to end-users asking how '
                                                                             'they like the new colors.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Physical hardware stress tests on server '
                                                                             'fans.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Manual pen-and-paper audit checklists.'}],
                                                  'prompt': 'What are Post-Upgrade Tests (PUT) in the context of '
                                                            'S/4HANA Cloud release management?',
                                                  'question_id': 'd74_q2'},
                                              {   'concept_slug': 'cloud-test-automation',
                                                  'explanation': 'TDCs parameterize test scripts with reusable data '
                                                                 'sets for multi-company and multi-plant execution.',
                                                  'id': 'd74_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It stores reusable parameter sets and '
                                                                             'data variants, allowing test logic to '
                                                                             'run across multiple companies or plants '
                                                                             'without modifying scripts.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It encrypts user credit card numbers.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It serves as a physical shipping '
                                                                             'container for servers.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It compresses video training files.'}],
                                                  'prompt': 'What is the role of a Test Data Container (TDC) in the '
                                                            'SAP Test Automation Tool?',
                                                  'question_id': 'd74_q3'},
                                              {   'concept_slug': 'upgrade-regression-testing',
                                                  'explanation': 'Shift-Left testing identifies and remediates defects '
                                                                 'early in sprint cycles.',
                                                  'id': 'd74_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Shift-Left Testing'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Shift-Right Testing'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Waterfall Testing'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Post-Go-Live Testing'}],
                                                  'prompt': 'What quality engineering concept advocates testing as '
                                                            'early as possible during the development cycle rather '
                                                            'than waiting for final deployment?',
                                                  'question_id': 'd74_q4'}],
                             'step_id': 'd74_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 74 Verification Assessment'},
                         {   'step_id': 'd74_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered the SAP Cloud Test Automation Tool architecture and test '
                                           'execution lifecycle.\n'
                                           '- Configured Post-Upgrade Tests (PUT) and Test Data Containers (TDCs) for '
                                           'continuous regression safety.\n'
                                           '- Implemented Shift-Left quality governance across agile development '
                                           'sprints.',
                             'title': 'Day 74 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd74_s8_completion',
                             'recommended_mission': {'slug': 'nova-cloud-automated-testing', 'title': 'Cloud Test Automation Suite Configuration', 'description': 'Create automated regression test plans for quarterly release upgrades.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You know how to validate and protect cloud systems against '
                                           'regressions. Tomorrow, you will master the final critical operational '
                                           'hurdle: **Cutover Execution, Hypercare & Operational Readiness**.',
                             'title': 'Day 74 Complete: Cloud Test Automation Mastered'}],
            'subtitle': 'Test automation in the cloud, SAP Cloud Test Automation Tool, Post-Upgrade Tests (PUT), and '
                        'regression management.',
            'title': 'Cloud Testing & Regression Automation'},
    75: {   'atomic_concepts': ['cutover-strategy', 'hypercare-operations'],
            'day_number': 75,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'cutover-operational-readiness',
            'steps': [   {   'content_md': '### Orchestrating the Final Go-Live\n'
                                           'Cutover is the mission-critical transition period where the organization '
                                           'shuts down legacy systems, transfers final data balances, executes '
                                           'technical validation, and opens the live S/4HANA production system for '
                                           'business operations.\n'
                                           '\n'
                                           '#### Core Elements of an Enterprise Cutover Strategy:\n'
                                           '1. **Cutover Runbook (Minute-by-Minute Schedule)**: A granular, highly '
                                           'synchronized task schedule documenting hundreds of steps, assigned owners, '
                                           'dependencies, planned start/end times, and rollback criteria.\n'
                                           '2. **Blackout Period (Business Freeze)**: Planned business downtime '
                                           '(typically over a weekend or holiday period) where legacy systems are set '
                                           'to read-only, physical inventory is counted, and transactional postings '
                                           'halt.\n'
                                           '3. **Mock Cutovers (Dress Rehearsals)**: At least two full mock cutover '
                                           'dry-runs executed in the Test/Pre-Production environment prior to real '
                                           'go-live to measure exact timings and eliminate execution bottlenecks.\n'
                                           '4. **Fallback / Rollback Strategy**: Clear, predefined triggers defining '
                                           "when an executive 'No-Go' decision must be called and how to revert safely "
                                           'to the legacy state.',
                             'key_terms': [   {   'definition': 'Minute-by-minute execution schedule specifying task '
                                                                'dependencies, owners, and duration estimates.',
                                                  'term': 'Cutover Runbook'},
                                              {   'definition': 'Agreed operational freeze window where legacy '
                                                                'postings halt to ensure clean data extraction.',
                                                  'term': 'Blackout Period'},
                                              {   'definition': 'Full-scale dry run rehearsing cutover timing, '
                                                                'technical steps, and validation under realistic '
                                                                'conditions.',
                                                  'term': 'Mock Cutover'}],
                             'step_id': 'd75_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Cutover executes via a minute-by-minute runbook during a planned blackout '
                                         'period, rehearsed through realistic mock dry-runs.',
                             'title': 'The Cutover Phase: Crossing the Enterprise Chasm'},
                         {   'content_md': '### Surviving Day 1 to Day 30: Hypercare\n'
                                           'The period immediately following Go-Live is **Hypercare** (typically '
                                           'lasting 30 to 60 days):\n'
                                           '\n'
                                           '#### Hypercare Operating Architecture:\n'
                                           '1. **War Room / Command Center**: Central physical and virtual triage desk '
                                           'uniting enterprise architects, functional leads, basis engineers, and '
                                           'business super-users.\n'
                                           '2. **Fast-Track Defect Resolution**: Emergency change management workflow '
                                           'allowing critical Sev-1 production fixes to be developed, tested, and '
                                           'transported within hours rather than weekly sprints.\n'
                                           '3. **Daily Business Checkpoints**: Daily executive standups monitoring '
                                           'critical operational KPIs:\n'
                                           '   - Order intake volume vs historical baseline.\n'
                                           '   - Warehouse shipping throughput (PL01 / PL02).\n'
                                           '   - Billing and financial posting error rate.\n'
                                           '4. **Formal Handover to Run**: Once defect volumes drop below threshold '
                                           'and the first month-end financial closing completes successfully, the '
                                           'project formally hands over to the permanent SAP Center of Excellence '
                                           '(CoE).',
                             'key_terms': [   {   'definition': 'Intensive post-go-live support period ensuring '
                                                                'operational stabilization and fast defect resolution.',
                                                  'term': 'Hypercare'},
                                              {   'definition': 'Centralized cross-functional operations room actively '
                                                                'managing real-time cutover incidents.',
                                                  'term': 'Command Center (War Room)'},
                                              {   'definition': 'The definitive operational milestone proving '
                                                                'accounting, billing, and inventory reconciliation '
                                                                'integrity.',
                                                  'term': 'First Month-End Close'}],
                             'step_id': 'd75_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Hypercare stabilizes operations via command center triage, fast-track defect '
                                         'fixes, and validation through the first month-end close.',
                             'title': 'Hypercare Operations & Incident Management'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'critical_path': 'Legacy Freeze -> Delta Financial Extraction -> '
                                                                     'S/4HANA Staging -> MIRO/ACDOCA Reconciliation',
                                                    'cutover_window': 'Friday 18:00 to Monday 06:00',
                                                    'total_tasks': 184},
                             'content_md': '### Minute-by-Minute Runbook Excerpt\n'
                                           '```\n'
                                           'Friday 18:00: [T-01] Legacy ECC set to READ-ONLY. SAP GUI lockouts active. '
                                           '(Owner: Basis Lead)\n'
                                           'Friday 20:00: [T-08] Physical stock counts finalized at PL01 & PL02. '
                                           '(Owner: Inventory Lead)\n'
                                           'Saturday 02:00: [T-24] Final delta extraction to Migration Cockpit staging '
                                           'tables completed.\n'
                                           'Saturday 08:00: [T-42] Migration Cockpit Step 4: Post Master Data '
                                           '(Business Partners, Materials).\n'
                                           'Saturday 16:00: [T-78] Post Open Inventory Balances to MATDOC.\n'
                                           'Sunday 04:00: [T-112] Post Open Accounts Payable & Accounts Receivable '
                                           'into ACDOCA.\n'
                                           'Sunday 12:00: [T-140] Financial Balance Reconciliation: Trial Balance '
                                           'Delta = 0.00 EUR.\n'
                                           'Sunday 18:00: [T-165] Q-Gate 4 Meeting: Executive GO Decision confirmed.\n'
                                           'Monday 06:00: [T-184] Production Fiori Launchpad opened to all 1,200 '
                                           'users. Go-Live Achieved!\n'
                                           '```',
                             'scenario': 'Nova Manufacturing executes Go-Live over Easter weekend for Heidelberg '
                                         '(PL01) and Austin (PL02).',
                             'step_id': 'd75_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Go-Live Cutover Runbook Snapshot'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'Arrange the cutover milestones into the correct logical and chronological '
                                            'execution sequence.',
                             'options': [   {   'explanation': 'Correct! Master data must precede transactional '
                                                               'balances, financial reconciliation must verify '
                                                               'numbers, and user access unlocks last.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': '1. Freeze legacy system transactions -> 2. Load open master '
                                                        'data -> 3. Post open transactional balances (GL/AP/AR) -> 4. '
                                                        'Financial trial balance reconciliation -> 5. Release Fiori '
                                                        'Launchpad to users.'},
                                            {   'explanation': 'Opening the system before loading master data will '
                                                               'trigger thousands of immediate user errors.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': '1. Open system to users -> 2. Freeze legacy system -> 3. Post '
                                                        'master data.'},
                                            {   'explanation': 'Reconciliation cannot occur before balances are '
                                                               'actually extracted and posted.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': '1. Financial reconciliation -> 2. Post balances -> 3. Freeze '
                                                        'legacy.'}],
                             'step_id': 'd75_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Legacy freeze -> Master data load -> Open balances post -> Financial '
                                         'reconciliation -> User access unlock.',
                             'title': 'Cutover Process Ordering: Sequencing Critical Cutover Milestones'},
                         {   'instruction': 'As Cutover Director, how do you handle this critical situation?',
                             'options': [   {   'explanation': 'Correct! Financial integrity is non-negotiable; going '
                                                               'live with an unreconciled multi-million EUR variance '
                                                               'will result in catastrophic financial reporting '
                                                               'failure.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Halt the cutover schedule immediately. Convene the Financial '
                                                        'Lead and Migration Architect in the War Room to trace the '
                                                        'variance. If the variance cannot be reconciled and corrected '
                                                        'before the agreed drop-dead decision deadline, invoke the '
                                                        'Rollback plan.'},
                                            {   'explanation': 'Catastrophic governance failure leading to immediate '
                                                               'financial audit failure and regulatory penalties.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Ignore the 4.2 million variance and go live anyway, hoping '
                                                        "accountants don't notice."},
                                            {   'explanation': 'Fraudulent accounting practice that violates corporate '
                                                               'criminal law.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Post a fake manual adjustment entry to a miscellaneous '
                                                        'expense account to make the numbers match.'}],
                             'scenario': 'At Sunday 14:00 (6 hours before the Go/No-Go decision), the financial '
                                         'reconciliation shows an unexplained variance of 4.2 million EUR between the '
                                         'legacy trial balance and S/4HANA ACDOCA.',
                             'step_id': 'd75_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Cutover Crisis Challenge: Financial Balance Variance at T-Minus 6 Hours'},
                         {   'assessment_type': 'process_ordering',
                             'questions': [   {   'concept_slug': 'cutover-strategy',
                                                  'explanation': 'The Cutover Runbook governs the detailed execution '
                                                                 'of the go-live sequence.',
                                                  'id': 'd75_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Cutover Runbook'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Marketing Brochure'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Weekly Lunch Menu'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Source Code Repository'}],
                                                  'prompt': 'What is the primary operational document used to '
                                                            'orchestrate minute-by-minute tasks, owners, and '
                                                            'dependencies during production cutover?',
                                                  'question_id': 'd75_q1'},
                                              {   'concept_slug': 'hypercare-operations',
                                                  'explanation': 'Hypercare provides high-touch support and rapid '
                                                                 'triage to stabilize new operations.',
                                                  'id': 'd75_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To provide intensive support, rapidly '
                                                                             'triage production defects, and stabilize '
                                                                             'business operations through the first '
                                                                             'month-end close.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To take a 4-week vacation.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To dismantle the computer network.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To redesign the company logo.'}],
                                                  'prompt': 'What is the primary operational objective of the '
                                                            'Hypercare period following an SAP go-live?',
                                                  'question_id': 'd75_q2'},
                                              {   'concept_slug': 'cutover-strategy',
                                                  'explanation': 'Mock cutovers rehearse and optimize the real '
                                                                 'sequence under realistic operational conditions.',
                                                  'id': 'd75_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To test execution duration, validate '
                                                                             'data conversion timing, and eliminate '
                                                                             'technical bottlenecks in a '
                                                                             'non-production environment.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To fill out human resources timesheets.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To consume excess computer electricity.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To delete historical backups.'}],
                                                  'prompt': "Why are 'Mock Cutovers' (dress rehearsals) executed prior "
                                                            'to the real production cutover?',
                                                  'question_id': 'd75_q3'},
                                              {   'concept_slug': 'hypercare-operations',
                                                  'explanation': 'The first month-end close proves full financial, '
                                                                 'operational, and billing reconciliation integrity.',
                                                  'id': 'd75_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Successful completion of the First '
                                                                             'Month-End Financial Closing'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Sending 1,000 marketing emails'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Purchasing new office furniture'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Reaching 100 days of project delay'}],
                                                  'prompt': 'Which key enterprise milestone typically marks the formal '
                                                            'conclusion of Hypercare and the transition to '
                                                            'steady-state operations?',
                                                  'question_id': 'd75_q4'}],
                             'step_id': 'd75_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 75 Verification Assessment'},
                         {   'step_id': 'd75_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Architected production Cutover strategies with granular runbooks, '
                                           'blackout windows, and rollback criteria.\n'
                                           '- Orchestrated Mock Cutover dress rehearsals to de-risk high-volume data '
                                           'transitions.\n'
                                           '- Established Hypercare command center operations and stabilized systems '
                                           'through the first month-end close.',
                             'title': 'Day 75 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd75_s8_completion',
                             'recommended_mission': {'slug': 'nova-cutover-hypercare-execution', 'title': 'Cutover & Hypercare Operational Execution', 'description': 'Execute dress rehearsal cutover sequence for production launch.'},
                             'step_type': 'completion',
                             'summary_md': 'Phenomenal work! You have traversed the complete deployment lifecycle. '
                                           'Tomorrow, you will synthesize all Phase 6 knowledge in the **Phase 6 Clean '
                                           'Core Capstone & Extensibility Roadmap**.',
                             'title': 'Day 75 Complete: Cutover & Hypercare Mastered'}],
            'subtitle': 'Cutover planning, blackout periods, mock cutovers, hypercare support, and transition to '
                        'operations.',
            'title': 'Cutover Strategy & Operational Readiness'},
    76: {   'atomic_concepts': ['clean-core-roadmap-synthesis'],
            'day_number': 76,
            'estimated_minutes': 90,
            'recommended_mission_slug': None,
            'slug': 'cloud-clean-core-capstone',
            'steps': [   {   'content_md': '### Synthesizing Cloud Modernization & Clean Core\n'
                                           'In Phase 6, you have mastered the complete architectural paradigm '
                                           'governing modern SAP cloud transformations:\n'
                                           '1. **Deployment Flavors**: Public Cloud (SaaS/3SL) vs Private Cloud '
                                           '(IaaS/managed) vs Two-Tier ERP.\n'
                                           '2. **Clean Core Philosophy**: Zero core modifications, release contracts '
                                           '(C1 internal / C2 external), and upgrade-safety.\n'
                                           '3. **Delivery Framework**: SAP Activate (6 phases, Q-Gates 1–4) and '
                                           'Fit-to-Standard workshops.\n'
                                           '4. **Configuration**: SAP Central Business Configuration (CBC) for '
                                           'centralized scoping and org structure.\n'
                                           '5. **The Tri-Tier Extensibility Model**:\n'
                                           '   - **Tier 1**: Key-User (Custom Fields & Logic, UI Adaptation, '
                                           'Restricted ABAP).\n'
                                           '   - **Tier 2**: Developer Extensibility On-Stack (ABAP Cloud, Eclipse '
                                           'ADT, RAP, C1 APIs).\n'
                                           '   - **Tier 3**: Side-by-Side Extensibility on SAP BTP (CAP, Kyma, '
                                           'decoupled microservices).\n'
                                           '6. **Data & Quality Operations**: Migration Cockpit (staging tables, '
                                           'LTMOM), Cloud Test Automation Tool (PUT regression), Cutover runbooks, and '
                                           'Hypercare stabilization.\n'
                                           '\n'
                                           '#### The Capstone Challenge:\n'
                                           'Nova Manufacturing Corp is completing its global transformation blueprint. '
                                           'As Chief Enterprise Architect, you must defend the comprehensive Clean '
                                           'Core Extensibility Roadmap and Governance Framework before the Executive '
                                           'Board.',
                             'key_terms': [   {   'definition': 'End-to-end alignment of deployment models, delivery '
                                                                'methodology, extensibility tiers, and upgrade '
                                                                'governance.',
                                                  'term': 'Clean Core Synthesis'},
                                              {   'definition': 'Strategic portfolio classification allocating '
                                                                'business customizations to the optimal Clean Core '
                                                                'tier.',
                                                  'term': 'Extensibility Roadmap'}],
                             'step_id': 'd76_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'The Clean Core Capstone synthesizes deployment models, Activate delivery, '
                                         'CBC scoping, the 3 extensibility tiers, and upgrade-safe operations.',
                             'title': 'Phase 6 Capstone: Enterprise Clean Core Architecture'},
                         {   'content_md': '### Defending the Clean Core Strategy Against Legacy Resistance\n'
                                           'Enterprise architects constantly face resistance from legacy practitioners '
                                           'demanding classical modifications. Here is the authoritative architectural '
                                           'defense:\n'
                                           '\n'
                                           '#### 1. Why Not Classic User Exits & Modifications?\n'
                                           '- *Legacy Argument*: "Modifying standard code directly is faster for '
                                           'developers."\n'
                                           '- *Clean Core Defense*: "Modifications incur massive hidden technical '
                                           'debt. A single direct modification can delay a critical upgrade by months '
                                           'and cost hundreds of thousands in regression testing. Clean Core '
                                           'extensions use released C1/C2 APIs that survive every upgrade '
                                           'automatically."\n'
                                           '\n'
                                           '#### 2. Why Not Put Everything on BTP?\n'
                                           '- *Legacy Argument*: "If BTP is decoupled, let\'s put 100% of all code on '
                                           'BTP."\n'
                                           '- *Clean Core Defense*: "Putting high-volume transactional calculations '
                                           '(e.g., looping over 100,000 inventory items) on BTP causes massive network '
                                           'latency and data serialization overhead. Tier 2 (On-Stack Developer '
                                           'Extensibility) executes directly in-memory next to the HANA database, '
                                           'providing optimal throughput while remaining Clean Core compliant."\n'
                                           '\n'
                                           '#### 3. The Golden Rule of Modern SAP Extensibility:\n'
                                           '*"Keep the core clean, build near the data when high throughput is '
                                           'required (Tier 2), and build on BTP when decoupling or external access is '
                                           'needed (Tier 3)."*',
                             'key_terms': [   {   'definition': 'Architectural justifications demonstrating the TCO, '
                                                                'speed, and agility benefits of Clean Core over legacy '
                                                                'modifications.',
                                                  'term': 'Clean Core Defense'},
                                              {   'definition': 'Principle dictating that high-volume transactional '
                                                                'data operations run on-stack (Tier 2) to eliminate '
                                                                'network latency.',
                                                  'term': 'Data Proximity'}],
                             'step_id': 'd76_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Balance data proximity (On-Stack Tier 2 for high-throughput loops) with '
                                         'decoupled agility (Side-by-Side Tier 3 for portals and SaaS).',
                             'title': 'The Clean Core Architectural Defense'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'erp_core': 'S/4HANA Cloud (Two-Tier Architecture)',
                                                    'plants': ['PL01 Heidelberg', 'PL02 Austin'],
                                                    'platform': 'SAP BTP Multi-Region'},
                             'content_md': '### Master Extensibility Matrix (Nova Manufacturing)\n'
                                           '```\n'
                                           '┌──────────────────────────────────────────────────────────────────────────────────────────────────┐\n'
                                           '│                               NOVA MANUFACTURING EXTENSIBILITY '
                                           'MATRIX                            │\n'
                                           '├───────────────────────┬───────────────────────────┬──────────────────────────────────────────────┤\n'
                                           '│ Extensibility Tier    │ Implemented Scenarios     │ Technology '
                                           'Stack                             │\n'
                                           '├───────────────────────┼───────────────────────────┼──────────────────────────────────────────────┤\n'
                                           '│ Tier 1: Key-User      │ * Custom Sensor Cert ID   │ * Custom Fields & '
                                           'Logic App                  │\n'
                                           '│ (In-App Low-Code)     │ * Runtime UI Adaptation   │ * Restricted ABAP '
                                           'Cloud BAdIs                │\n'
                                           '│                       │ * Custom Print Layouts    │ * Export / Import '
                                           'Software Collections       │\n'
                                           '├───────────────────────┼───────────────────────────┼──────────────────────────────────────────────┤\n'
                                           '│ Tier 2: Developer     │ * Complex Scrap Logic     │ * Eclipse ADT '
                                           '(Language: ABAP Cloud)         │\n'
                                           '│ (On-Stack Pro-Code)   │ * RAP Business Objects    │ * Released C1 APIs '
                                           '(I_PurchaseOrderAPI01)    │\n'
                                           '│                       │ * In-Memory Analytics     │ * ABAP Unit & ATC '
                                           'Governance                 │\n'
                                           '├───────────────────────┼───────────────────────────┼──────────────────────────────────────────────┤\n'
                                           '│ Tier 3: Side-by-Side  │ * Global Supplier Portal  │ * SAP BTP Cloud '
                                           'Foundry & Kyma               │\n'
                                           '│ (Decoupled BTP)       │ * IoT Telemetry Ingestion │ * SAP CAP '
                                           '(Node.js/TypeScript)               │\n'
                                           '│                       │ * Supplier Sustainability │ * Event Mesh & Cloud '
                                           'Connector (mTLS)        │\n'
                                           '└───────────────────────┴───────────────────────────┴──────────────────────────────────────────────┘\n'
                                           '```',
                             'scenario': "Review the master extensibility matrix approved for Nova Manufacturing's "
                                         'global enterprise architecture.',
                             'step_id': 'd76_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Global Clean Core Extensibility Blueprint'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "The Chief Financial Officer asks: 'Why did we spend budget implementing "
                                            'the SAP Cloud Test Automation Tool instead of relying on our annual audit '
                                            "team?' Provide the authoritative answer.",
                             'options': [   {   'explanation': 'Correct! Continuous cloud upgrades require automated '
                                                               'testing to maintain business continuity and agility.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Explain that the Cloud Test Automation Tool executes '
                                                        'continuous regression testing for every bi-weekly quality '
                                                        'update and semi-annual upgrade. Without automation, the ERP '
                                                        'core would either suffer severe business outages or be '
                                                        'blocked from adopting critical tax and security innovations.'},
                                            {   'explanation': 'Completely false; test automation is essential for '
                                                               'cloud survival.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Admit that the test tool was purchased by mistake and promise '
                                                        'to uninstall it.'},
                                            {   'explanation': 'Dangerous misconception; cloud systems require '
                                                               'rigorous regression validation.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Tell the CFO that testing is irrelevant in the cloud.'}],
                             'step_id': 'd76_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Automated regression testing is the foundational operational safeguard '
                                         'enabling continuous cloud innovation.',
                             'title': 'Executive Architectural Defense Simulation'},
                         {   'instruction': 'As Chief Enterprise Architect, what action do you take?',
                             'options': [   {   'explanation': 'Correct! Direct database connections bypass security, '
                                                               'audit logs, business validation, and completely '
                                                               'violate Clean Core.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Revoke database-level access immediately. Enforce Clean Core '
                                                        'governance: mandate that external billing data integrate via '
                                                        'official released OData V4 Web APIs or through SAP '
                                                        'Integration Suite on BTP with OAuth2 and auditing.'},
                                            {   'explanation': 'Extreme security vulnerability that invites data '
                                                               'corruption and audit failure.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Allow the direct database access as long as the third party '
                                                        'promises to be careful.'},
                                            {   'explanation': 'Completely irresponsible and violates compliance '
                                                               'standards.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Disable S/4HANA database security checks globally.'}],
                             'scenario': 'A rogue business unit attempted to connect an unapproved third-party billing '
                                         'database directly to S/4HANA via database-level ODBC root credentials.',
                             'step_id': 'd76_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Phase 6 Capstone Defense: Clean Core Audit Sign-Off'},
                         {   'assessment_type': 'capstone_quiz',
                             'questions': [   {   'concept_slug': 'clean-core-roadmap-synthesis',
                                                  'explanation': 'Clean Core enforces zero core modifications and '
                                                                 'strictly released stable APIs.',
                                                  'id': 'd76_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Zero modifications to standard SAP code, '
                                                                             'with all customizations decoupled and '
                                                                             'interacting exclusively via released '
                                                                             'APIs.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Writing all software code in raw '
                                                                             'assembly language.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Upgrading systems only once every twenty '
                                                                             'years.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Deleting all custom reports every '
                                                                             'weekend.'}],
                                                  'prompt': 'What is the cardinal rule of the SAP Clean Core '
                                                            'philosophy?',
                                                  'question_id': 'd76_q1'},
                                              {   'concept_slug': 'clean-core-roadmap-synthesis',
                                                  'explanation': 'Tier 2 executes directly on-stack next to the '
                                                                 'database, eliminating network serialization '
                                                                 'overhead.',
                                                  'id': 'd76_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Tier 2: On-Stack Developer Extensibility '
                                                                             '(ABAP Cloud & RAP)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Tier 3: Side-by-Side on external '
                                                                             'platforms'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Excel Macros'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Legacy Dynpro Screens'}],
                                                  'prompt': 'Which Clean Core extensibility tier is optimal for '
                                                            'high-throughput, data-intensive transactional business '
                                                            'logic that requires direct proximity to the HANA '
                                                            'database?',
                                                  'question_id': 'd76_q2'},
                                              {   'concept_slug': 'clean-core-roadmap-synthesis',
                                                  'explanation': 'Quality Gates enforce formal milestone audits '
                                                                 'ensuring quality standards before phase transitions.',
                                                  'id': 'd76_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Through mandatory Quality Gates (Q-Gates '
                                                                             '1 through 4) with strict phase-exit '
                                                                             'criteria.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'By locking computer keyboards.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'By shutting down the internet '
                                                                             'connection.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Through annual employee surveys.'}],
                                                  'prompt': 'How does SAP Activate prevent projects from proceeding '
                                                            'into realization or deployment with critical unaddressed '
                                                            'risks?',
                                                  'question_id': 'd76_q3'},
                                              {   'concept_slug': 'clean-core-roadmap-synthesis',
                                                  'explanation': 'Two-Tier ERP integrates subsidiaries and corporate '
                                                                 'HQ cleanly via Integration Suite and standard APIs.',
                                                  'id': 'd76_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Via SAP Integration Suite and released '
                                                                             'standard OData/Event APIs, maintaining '
                                                                             'Clean Core on both tiers.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Via raw database replication bypassing '
                                                                             'the application layer.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Via weekly paper mail printouts.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Two-tier systems must never be '
                                                                             'connected.'}],
                                                  'prompt': 'In an enterprise two-tier ERP landscape, how should a '
                                                            'standardized cloud subsidiary (e.g. S/4HANA Cloud Public '
                                                            'Edition) integrate with corporate headquarters?',
                                                  'question_id': 'd76_q4'}],
                             'step_id': 'd76_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Phase 6 Comprehensive Capstone Assessment'},
                         {   'step_id': 'd76_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Comprehensive Phase 6 Benchmark Achieved:\n'
                                           '- **Clean Core Architecture Synthesis**: Mastered cloud deployment models, '
                                           'Activate delivery, CBC configuration, and the Tri-Tier Extensibility '
                                           'Framework.\n'
                                           '- **Extensibility Roadmap Defense**: Defended on-stack (Tier 2) data '
                                           'proximity vs side-by-side (Tier 3) decoupling before executive '
                                           'stakeholders.\n'
                                           '- **Operational De-Risking**: Enforced automated regression testing (PUT), '
                                           'Migration Cockpit governance, and cutover runbook execution.',
                             'title': 'Phase 6 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd76_s8_completion',
                             'recommended_mission': {'slug': 'nova-clean-core-capstone', 'title': 'Clean Core & Cloud Architecture Capstone', 'description': 'Defend end-to-end cloud transformation architecture.'},
                             'step_type': 'completion',
                             'summary_md': 'Congratulations! You have completed Phase 6: S/4HANA Cloud & Clean Core. '
                                           'You possess the strategic and technical competence required to lead cloud '
                                           'transformations. In **Phase 7 (Days 77–89)**, you will dive into modern '
                                           'developer engineering: **ABAP Cloud & the RESTful Application Programming '
                                           'Model (RAP)**.',
                             'title': 'Phase 6 Complete: S/4HANA Cloud & Clean Core Certified'}],
            'subtitle': 'Phase 6 benchmark: Clean Core architecture defense, cloud governance, and multi-tier '
                        'extensibility roadmap.',
            'title': 'S/4HANA Cloud & Clean Core Assessment'}}
