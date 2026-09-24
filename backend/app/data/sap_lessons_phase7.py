"""Authoritative content definitions for SAP S/4HANA Guided Learning Days 77–89 (Phase 7).

Phase 7: ABAP Cloud & RAP (Rules, Syntax, RAP BO Modeling, BDEF, Determinations, Validations, Draft, Capstone).
Enterprise Continuous Model: Nova Manufacturing Corp (NM01)
"""

from __future__ import annotations
from typing import Any

PHASE_7_DAYS_CONTENT: dict[int, dict[str, Any]] = {   77: {   'atomic_concepts': ['abap-cloud-paradigm', 'released-apis-c1', 'forbidden-legacy-abap'],
            'day_number': 77,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'abap-cloud-paradigm',
            'steps': [   {   'content_md': '### What is ABAP Cloud?\n'
                                           'ABAP Cloud is the modern, state-of-the-art development model for building '
                                           'cloud-ready business applications, services, and extensions across all SAP '
                                           'S/4HANA editions (Public, Private, On-Premise) and the SAP BTP ABAP '
                                           'Environment.\n'
                                           '\n'
                                           '#### Core Tenets of the ABAP Cloud Paradigm:\n'
                                           '1. **Language Version**: Packages must be configured with `ABAP for Cloud '
                                           'Development`.\n'
                                           '2. **Strict Object-Oriented Architecture**: Only ABAP Objects (classes, '
                                           'interfaces) are permitted. Procedural legacy artifacts (`FORM` routines, '
                                           'Function Modules, classical dynpro screens, reports with '
                                           '`SELECTION-SCREEN`) are forbidden.\n'
                                           '3. **No Direct Database Access to SAP Tables**: Custom code cannot perform '
                                           'direct `SELECT`, `INSERT`, or `UPDATE` on unreleased SAP database tables '
                                           '(like `BSEG`, `EKKO`, `MARA`). Data access occurs exclusively via '
                                           '**Released C1 CDS View Entities**.\n'
                                           '4. **RAP as the Transactional Engine**: All business logic and '
                                           'transactional flows are orchestrated through the ABAP RESTful Application '
                                           'Programming Model (RAP).',
                             'key_terms': [   {   'definition': 'Modern development model enforcing object-oriented, '
                                                                'cloud-ready programming with released APIs.',
                                                  'term': 'ABAP Cloud'},
                                              {   'definition': 'Obsolete syntax constructs (header lines, TABLES, '
                                                                'FORM routines) rejected by the ABAP Cloud compiler.',
                                                  'term': 'Forbidden Legacy ABAP'},
                                              {   'definition': 'Official SAP guarantee of API backwards-compatibility '
                                                                'for internal consumption.',
                                                  'term': 'Released C1 Contract'}],
                             'step_id': 'd77_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'ABAP Cloud strictly enforces pure ABAP Objects, released C1 APIs, and RAP '
                                         'transactional engines while banning legacy procedural constructs.',
                             'title': 'The ABAP Cloud Paradigm: Clean, Cloud-Native ABAP'},
                         {   'content_md': '### What the ABAP Cloud Compiler Rejects\n'
                                           'When a package is set to `ABAP for Cloud Development`, the compiler in '
                                           'Eclipse ADT actively blocks legacy ABAP patterns:\n'
                                           '\n'
                                           '| Forbidden Legacy Syntax | Why It Is Forbidden | Modern ABAP Cloud '
                                           'Replacement |\n'
                                           '|---|---|---|\n'
                                           '| `TABLES: ekko.` | Obsolete header-line memory allocation | Explicit '
                                           'structure declarations (`DATA ls_po TYPE ...`) |\n'
                                           '| `SELECT * FROM ekko` | Direct access to unreleased core database tables '
                                           '| `SELECT FROM I_PurchaseOrderAPI01` (Released C1 View) |\n'
                                           '| `COMMIT WORK` / `ROLLBACK` | Bypasses framework transactional lifecycle '
                                           'and locks | Handled automatically by the RAP Transactional Buffer |\n'
                                           "| `CALL FUNCTION 'BAPI_...'` | Legacy non-contractual RFC function modules "
                                           '| RAP Behavior Definitions or released C1 APIs |\n'
                                           "| `CALL TRANSACTION 'VA01'` | GUI dynpro screen execution | Fiori intent "
                                           'navigation (`#SalesOrder-create`) |\n'
                                           '| `MOVE-CORRESPONDING` without exact types | Runtime truncation and type '
                                           'mismatch errors | Strict `CORRESPONDING #( ... )` constructor expressions '
                                           '|',
                             'key_terms': [   {   'definition': 'Integrated development compiler validating ABAP Cloud '
                                                                'syntax and API contracts in real-time.',
                                                  'term': 'Eclipse ADT Compiler'},
                                              {   'definition': 'Modern type-safe constructor transferring matching '
                                                                'components between structures.',
                                                  'term': 'CORRESPONDING Operator'}],
                             'step_id': 'd77_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'ABAP Cloud bans direct table access, manual commits, function modules, and '
                                         'dynpros in favor of released CDS views and RAP.',
                             'title': 'Catalogue of Forbidden Legacy Syntax in ABAP Cloud'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'plant': 'PL01',
                                                    'refactoring_target': 'ZCL_NOVA_PO_INSPECT'},
                             'content_md': '### Legacy Code (FAILS in ABAP Cloud)\n'
                                           '```abap\n'
                                           '// FORBIDDEN IN ABAP CLOUD:\n'
                                           'TABLES: ekko, ekpo.\n'
                                           "SELECT * FROM ekko WHERE ebeln = '4500001092'.\n"
                                           '  WRITE: / ekko-lifnr.\n'
                                           'ENDSELECT.\n'
                                           '```\n'
                                           '\n'
                                           '### Modern ABAP Cloud Equivalent (PASSES)\n'
                                           '```abap\n'
                                           'CLASS zcl_nova_po_inspect DEFINITION PUBLIC FINAL CREATE PUBLIC.\n'
                                           '  PUBLIC SECTION.\n'
                                           '    INTERFACES if_oo_adt_classrun.\n'
                                           'ENDCLASS.\n'
                                           '\n'
                                           'CLASS zcl_nova_po_inspect IMPLEMENTATION.\n'
                                           '  METHOD if_oo_adt_classrun~main.\n'
                                           '    SELECT SINGLE FROM I_PurchaseOrderAPI01\n'
                                           '      FIELDS PurchaseOrder, Supplier, TotalNetAmount, DocumentCurrency\n'
                                           "      WHERE PurchaseOrder = '4500001092'\n"
                                           '      INTO @DATA(ls_po).\n'
                                           '\n'
                                           '    IF sy-subrc = 0.\n'
                                           '      out->write( |PO { ls_po-PurchaseOrder } Supplier: { ls_po-Supplier } '
                                           'Amount: { ls_po-TotalNetAmount } { ls_po-DocumentCurrency }| ).\n'
                                           '    ENDIF.\n'
                                           '  ENDMETHOD.\n'
                                           'ENDCLASS.\n'
                                           '```',
                             'scenario': 'Nova refactors a legacy purchase order inspection tool in Heidelberg to '
                                         'strict ABAP Cloud.',
                             'step_id': 'd77_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Code Refactoring: Legacy vs ABAP Cloud'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "A developer wrote `UPDATE vbak SET netwr = 5000 WHERE vbeln = '1000'`. "
                                            'Refactor this to compliant ABAP Cloud.',
                             'options': [   {   'explanation': 'Correct! Mutating business documents in ABAP Cloud '
                                                               'must be executed via EML on released RAP entities.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Execute an EML (Entity Manipulation Language) statement '
                                                        'targeting the released Sales Order RAP business object: '
                                                        '`MODIFY ENTITIES OF I_SalesOrderTP ENTITY SalesOrder UPDATE '
                                                        'FIELDS ( TotalNetAmount ) WITH VALUE #( ... )`.'},
                                            {   'explanation': 'Unreleased classic BAPIs cannot be invoked in ABAP for '
                                                               'Cloud Development packages.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': "Use `CALL FUNCTION 'BAPI_SALESORDER_CHANGE'` with classic "
                                                        'RFC.'},
                                            {   'explanation': 'Case sensitivity does not change the fact that direct '
                                                               'table writes are strictly forbidden.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Change `UPDATE vbak` to lowercase `update vbak`.'}],
                             'step_id': 'd77_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Mutate business documents via RAP Entity Manipulation Language (EML) on '
                                         'released entities, never via direct SQL updates.',
                             'title': 'ABAP Cloud Challenge: Refactoring Forbidden Database Operations'},
                         {   'instruction': 'What should the lead architect do during code review?',
                             'options': [   {   'explanation': 'Correct! In ABAP Cloud, manual COMMIT WORK statements '
                                                               'violate framework lifecycle governance.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Reject the code. In ABAP Cloud, transactional commit '
                                                        'boundaries are governed exclusively by the RAP framework. '
                                                        'Explicit COMMIT WORK corrupts the transactional buffer and '
                                                        'triggers runtime dumps.'},
                                            {   'explanation': 'Completely false in ABAP Cloud; manual commits cause '
                                                               'fatal runtime short dumps.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Approve it because waiting for commit is good practice.'},
                                            {   'explanation': '`WAIT` statements are also restricted and do not '
                                                               'substitute for framework commit orchestration.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Replace it with a 10-second `WAIT UP TO 10 SECONDS` loop.'}],
                             'scenario': 'A contractor submits an ABAP class containing `COMMIT WORK AND WAIT` inside '
                                         'a custom method.',
                             'step_id': 'd77_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Code Review Challenge: Detecting ABAP Cloud Anti-Patterns'},
                         {   'assessment_type': 'abap_challenge',
                             'questions': [   {   'concept_slug': 'abap-cloud-paradigm',
                                                  'explanation': '`ABAP for Cloud Development` enforces the strict '
                                                                 'cloud ruleset.',
                                                  'id': 'd77_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'ABAP for Cloud Development'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Standard ABAP 7.40'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Classic Dynpro ABAP'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Unrestricted Kernel Mode'}],
                                                  'prompt': 'What is the required Package Language Version setting in '
                                                            'Eclipse ADT for developing cloud-compliant ABAP?',
                                                  'question_id': 'd77_q1'},
                                              {   'concept_slug': 'forbidden-legacy-abap',
                                                  'explanation': 'RAP controls the transactional commit phase; manual '
                                                                 'commits corrupt the interaction phase buffer.',
                                                  'id': 'd77_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Transactional commits are managed '
                                                                             'centrally by the RAP runtime engine to '
                                                                             'guarantee LUW consistency.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Because the database does not have an '
                                                                             'undo log.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Because commits consume too much '
                                                                             'electricity.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Because SAP replaced commits with manual '
                                                                             'file saves.'}],
                                                  'prompt': 'Why is the classical `COMMIT WORK` statement forbidden in '
                                                            'ABAP Cloud business applications?',
                                                  'question_id': 'd77_q2'},
                                              {   'concept_slug': 'released-apis-c1',
                                                  'explanation': 'Released C1 CDS View Entities provide stable, '
                                                                 'contractual data access.',
                                                  'id': 'd77_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'By querying released C1 Core Data '
                                                                             'Services (CDS) View Entities (e.g. '
                                                                             '`I_PurchaseOrderAPI01`).'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'By downloading raw text files over FTP.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'By scanning printed barcodes.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'By reading the browser DOM.'}],
                                                  'prompt': 'How do custom ABAP Cloud programs query standard S/4HANA '
                                                            'business data without accessing internal tables directly?',
                                                  'question_id': 'd77_q3'},
                                              {   'concept_slug': 'abap-cloud-paradigm',
                                                  'explanation': 'ABAP Cloud mandates pure object-oriented design '
                                                                 'using classes and interfaces.',
                                                  'id': 'd77_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Pure Object-Oriented ABAP (ABAP '
                                                                             'Objects)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Procedural FORM routines'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Macro pools and subroutines'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Screen Dynpro logic (PBO/PAI)'}],
                                                  'prompt': 'Which programming paradigm is the exclusive foundation '
                                                            'for ABAP Cloud development?',
                                                  'question_id': 'd77_q4'}],
                             'step_id': 'd77_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 77 Verification Assessment'},
                         {   'step_id': 'd77_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered the ABAP Cloud paradigm and package governance in Eclipse ADT.\n'
                                           '- Refactored forbidden legacy constructs (header lines, manual commits, '
                                           'direct SQL writes).\n'
                                           '- Consumed contractual released C1 CDS entities for stable data access.',
                             'title': 'Day 77 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd77_s8_completion',
                             'recommended_mission': {'slug': 'nova-abap-cloud-syntax-guard', 'title': 'ABAP Cloud Syntax & Governance Guard', 'description': 'Refactor legacy ABAP constructs into released Tier 1 ABAP Cloud syntax.'},
                             'step_type': 'completion',
                             'summary_md': 'Superb work! You understand the foundational rules of ABAP Cloud. '
                                           'Tomorrow, you will master modern clean coding techniques: **Modern ABAP '
                                           'Objects Syntax & Automated ABAP Unit Testing**.',
                             'title': 'Day 77 Complete: ABAP Cloud Paradigm Mastered'}],
            'subtitle': 'Restricted ABAP syntax, forbidden legacy statements, released C1 APIs, and the clean ABAP '
                        'model.',
            'title': 'ABAP Cloud Paradigm & Rules'},
    78: {   'atomic_concepts': ['modern-abap-syntax', 'abap-unit-testing'],
            'day_number': 78,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'modern-abap-oo-unit-test',
            'steps': [   {   'content_md': '### Clean Coding in Modern ABAP\n'
                                           'Modern ABAP (7.40+) eliminated thousands of lines of boilerplate '
                                           'procedural code with expressive constructor expressions:\n'
                                           '\n'
                                           '#### 1. Constructor Expressions:\n'
                                           '- **`VALUE #( ... )`**: Instantiates structures and internal tables '
                                           'inline:\n'
                                           "  `DATA(lt_items) = VALUE zpo_item_t( ( item = '10' mat = 'RAW-01' ) ( "
                                           "item = '20' mat = 'RAW-02' ) ).`\n"
                                           '- **`CORRESPONDING #( ... )`**: Transfers identically named components '
                                           'between structures safely:\n'
                                           '  `DATA(ls_target) = CORRESPONDING ztarget_s( ls_source MAPPING custom_id '
                                           '= legacy_id ).`\n'
                                           '- **`COND #( ... )` / `SWITCH #( ... )`**: Conditional expressions inline '
                                           'without nested `IF` blocks.\n'
                                           '\n'
                                           '#### 2. Table Expressions:\n'
                                           '- Replace verbose `READ TABLE ... INTO ... WITH KEY`:\n'
                                           "  `DATA(ls_line) = lt_items[ item = '10' ].`\n"
                                           '  With optional default fallback: `DATA(ls_line) = VALUE #( lt_items[ item '
                                           "= '99' ] OPTIONAL ).`\n"
                                           '\n'
                                           '#### 3. String Templates:\n'
                                           '- String interpolation with pipes: `|Material: { ls_mat-id ALPHA = OUT } '
                                           'Plant: { ls_mat-plant }|`.',
                             'key_terms': [   {   'definition': 'Inline operators (VALUE, CORRESPONDING, COND) '
                                                                'creating and transforming typed data instances.',
                                                  'term': 'Constructor Expression'},
                                              {   'definition': 'Direct square-bracket table lookup syntax (`lt[ key = '
                                                                'val ]`) replacing classic READ TABLE.',
                                                  'term': 'Table Expression'},
                                              {   'definition': 'Embedded string interpolation syntax (`|Text { var '
                                                                '}|`) formatting values dynamically.',
                                                  'term': 'String Template'}],
                             'step_id': 'd78_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Modern ABAP replaces procedural boilerplate with inline constructor '
                                         'expressions, table expressions, and string templates.',
                             'title': 'Modern ABAP Syntax: Declarative, Functional & Concise'},
                         {   'content_md': '### Automated Unit Testing Framework (AUnit)\n'
                                           'Clean Core engineering requires automated regression testing directly on '
                                           'the backend via **ABAP Unit**:\n'
                                           '\n'
                                           '#### Architecture of an ABAP Unit Test Class:\n'
                                           '```abap\n'
                                           'CLASS ltc_po_calculator DEFINITION FINAL FOR TESTING\n'
                                           '  DURATION SHORT\n'
                                           '  RISK LEVEL HARMLESS.\n'
                                           '\n'
                                           '  PRIVATE SECTION.\n'
                                           '    DATA mo_cut TYPE REF TO zcl_po_calculator. // Class Under Test (CUT)\n'
                                           '    METHODS setup.\n'
                                           '    METHODS teardown.\n'
                                           '    METHODS test_volume_discount FOR TESTING.\n'
                                           'ENDCLASS.\n'
                                           '```\n'
                                           '\n'
                                           '#### Test Isolation via Test Doubles:\n'
                                           '- Tests must be **isolated** and **repeatable**: they must not depend on '
                                           'database states or modify real production data.\n'
                                           '- Modern ABAP provides standard double frameworks:\n'
                                           '  - **ABAP SQL Test Double Framework**: Intercepts `SELECT` statements on '
                                           'CDS views, returning mock in-memory data tables.\n'
                                           '  - **ABAP Function/Class Test Doubles**: Mocking method calls on external '
                                           'dependencies.',
                             'key_terms': [   {   'definition': 'Built-in automated unit testing framework integrated '
                                                                'into Eclipse ADT and ATC.',
                                                  'term': 'ABAP Unit'},
                                              {   'definition': 'The business logic class being validated in an '
                                                                'isolated unit test fixture.',
                                                  'term': 'Class Under Test (CUT)'},
                                              {   'definition': 'Framework intercepting database queries to return '
                                                                'mock test records during testing.',
                                                  'term': 'SQL Test Double Framework'}],
                             'step_id': 'd78_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'ABAP Unit provides fast, isolated regression testing using setup/teardown '
                                         'fixtures and the SQL Test Double Framework.',
                             'title': 'Automated Testing with ABAP Unit & Test Isolation'},
                         {   'company_context': {   'class_under_test': 'ZCL_NOVA_PRICING',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'test_class': 'LTC_NOVA_PRICING'},
                             'content_md': '### Test Implementation in Eclipse ADT\n'
                                           '```abap\n'
                                           'CLASS ltc_nova_pricing IMPLEMENTATION.\n'
                                           '  METHOD setup.\n'
                                           '    mo_cut = NEW zcl_nova_pricing( ).\n'
                                           '  ENDMETHOD.\n'
                                           '\n'
                                           '  METHOD test_volume_discount.\n'
                                           '    // Given: 500 units of component RAW-01 at base price 100 EUR\n'
                                           '    DATA(lv_discounted_price) = mo_cut->calculate_price(\n'
                                           "      iv_material = 'RAW-01'\n"
                                           '      iv_quantity = 500\n'
                                           '      iv_base_price = 100 ).\n'
                                           '\n'
                                           '    // Then: Expect 15% volume discount -> 85 EUR\n'
                                           '    cl_abap_unit_assert=>assert_equals(\n'
                                           '      act = lv_discounted_price\n'
                                           '      exp = 85\n'
                                           "      msg = 'Volume discount for 500+ units failed' ).\n"
                                           '  ENDMETHOD.\n'
                                           'ENDCLASS.\n'
                                           '```',
                             'scenario': "Nova's developer writes an automated ABAP Unit test validating volume "
                                         'pricing discounts for sensor RAW-01 in Heidelberg.',
                             'step_id': 'd78_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Pricing Calculator & Unit Test Fixture'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'Refactor a 10-line legacy loop checking if a record exists in an internal '
                                            'table into a single modern ABAP statement.',
                             'options': [   {   'explanation': 'Correct! `line_exists( ... )` returns a boolean in a '
                                                               'single readable expression without modifying internal '
                                                               'work areas.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Use the predicate function `line_exists( lt_items[ material = '
                                                        "'RAW-01' ] )`."},
                                            {   'explanation': 'Legacy imperative loop; modern ABAP provides '
                                                               'functional predicate expressions.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Write a `LOOP AT lt_items ... EXIT ... ENDLOOP` construct '
                                                        'with temporary flags.'},
                                            {   'explanation': 'Severe performance overhead and violates in-memory '
                                                               'execution principles.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Export the table to a flat file and search it using Python '
                                                        'grep.'}],
                             'step_id': 'd78_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Use `line_exists( ... )` to check table membership concisely.',
                             'title': 'Modern ABAP Refactoring Simulation: Eliminating Legacy Boilerplate'},
                         {   'instruction': 'What is the architectural violation and how do you remediate it?',
                             'options': [   {   'explanation': 'Correct! True unit tests are harmless and isolated '
                                                               'from persistent database storage.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Violation: Unit tests must have `RISK LEVEL HARMLESS` and '
                                                        'never pollute database tables. Remediate: use dependency '
                                                        'injection and the ABAP SQL Test Double Framework to mock '
                                                        'database reads/writes in memory.'},
                                            {   'explanation': 'Fragile and error-prone; risks deleting real '
                                                               'development customizing.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Approve it and run a manual script every Sunday to delete the '
                                                        'dummy records.'},
                                            {   'explanation': 'Destroys quality engineering and violates Clean Core '
                                                               'standards.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Disable ABAP Unit testing across the company.'}],
                             'scenario': 'A junior developer writes an ABAP Unit test that executes `INSERT INTO '
                                         'zpo_headers` on the database during test execution, leaving 500 dummy '
                                         'records in the development system.',
                             'step_id': 'd78_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Testing Governance Challenge: Database Modification in Unit Tests'},
                         {   'assessment_type': 'abap_challenge',
                             'questions': [   {   'concept_slug': 'modern-abap-syntax',
                                                  'explanation': '`VALUE #( table[ key = val ] OPTIONAL )` performs '
                                                                 'safe table reads without raising exceptions.',
                                                  'id': 'd78_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'DATA(ls_order) = VALUE #( lt_orders[ id '
                                                                             "= '100' ] OPTIONAL )."},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': "DATA(ls_order) = lt_orders->get('100')."},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'READ TABLE lt_orders WITH KEY id = 100 '
                                                                             'GOTO LABEL.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'FETCH FIRST ROW FROM lt_orders.'}],
                                                  'prompt': 'Which modern ABAP table expression retrieves a row from '
                                                            "internal table `lt_orders` where `id = '100'`, returning "
                                                            'an initial structure if no record is found?',
                                                  'question_id': 'd78_q1'},
                                              {   'concept_slug': 'abap-unit-testing',
                                                  'explanation': '`cl_abap_unit_assert=>assert_equals` is the standard '
                                                                 'assertion method in ABAP Unit.',
                                                  'id': 'd78_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'cl_abap_unit_assert=>assert_equals( act '
                                                                             '= lv_act exp = lv_exp )'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'IF lv_act == lv_exp THEN EXIT.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': "PRINT('Test Passed')"},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'ASSERT_TRUE_OR_DIE'}],
                                                  'prompt': 'What standard static method is used in ABAP Unit to '
                                                            'verify that an actual calculated value matches the '
                                                            'expected test result?',
                                                  'question_id': 'd78_q2'},
                                              {   'concept_slug': 'modern-abap-syntax',
                                                  'explanation': 'String templates provide clean, expressive string '
                                                                 'interpolation.',
                                                  'id': 'd78_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To perform inline string interpolation '
                                                                             'and dynamic formatting without manual '
                                                                             'CONCATENATE statements.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To execute shell commands in Linux.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To compress audio files.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To encrypt passwords.'}],
                                                  'prompt': 'What is the purpose of string templates wrapped in '
                                                            'vertical pipes (`|Text { variable }|`) in modern ABAP?',
                                                  'question_id': 'd78_q3'},
                                              {   'concept_slug': 'abap-unit-testing',
                                                  'explanation': '`RISK LEVEL HARMLESS` confirms that the test fixture '
                                                                 'creates no persistent side effects.',
                                                  'id': 'd78_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To declare that the test executes in '
                                                                             'memory without modifying persistent '
                                                                             'database tables or external system '
                                                                             'states.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To tell the operating system not to scan '
                                                                             'for viruses.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To allow the test to run without a CPU.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To disable all security firewalls.'}],
                                                  'prompt': 'Why should an ABAP Unit test class specify `RISK LEVEL '
                                                            'HARMLESS`?',
                                                  'question_id': 'd78_q4'}],
                             'step_id': 'd78_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 78 Verification Assessment'},
                         {   'step_id': 'd78_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered modern declarative ABAP syntax (constructor expressions, table '
                                           'expressions, string templates).\n'
                                           '- Architected automated ABAP Unit test fixtures using '
                                           '`cl_abap_unit_assert`.\n'
                                           '- Applied test isolation principles using the ABAP SQL Test Double '
                                           'Framework.',
                             'title': 'Day 78 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd78_s8_completion',
                             'recommended_mission': {'slug': 'nova-abap-unit-test-double', 'title': 'ABAP Unit & Test Double Framework', 'description': 'Write isolated unit tests with test doubles for business logic.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You have modern clean-coding techniques down. Tomorrow, you '
                                           'will step into the core architectural pillar of modern SAP engineering: '
                                           '**The ABAP RESTful Application Programming Model (RAP)**.',
                             'title': 'Day 78 Complete: Modern ABAP & Unit Testing Mastered'}],
            'subtitle': 'Constructor expressions, string templates, table expressions, ABAP Unit, and test isolation '
                        'with test doubles.',
            'title': 'Modern ABAP Objects & ABAP Unit'},
    79: {   'atomic_concepts': ['rap-architecture-overview', 'bdef-and-behavior-implementation'],
            'day_number': 79,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'rap-architecture-big-picture',
            'steps': [   {   'content_md': '### The Architectural Framework of Modern ABAP\n'
                                           'The **ABAP RESTful Application Programming Model (RAP)** is the '
                                           'evolutionary pinnacle of SAP transactional architecture, replacing legacy '
                                           'BOPF, classic dynpros, and unmanaged SEGW Gateway services.\n'
                                           '\n'
                                           '#### The 3 Core Architectural Pillars:\n'
                                           '1. **Data Model & Queries (CDS)**:\n'
                                           '   - Built on Core Data Services (CDS) View Entities.\n'
                                           '   - Defines relational structures, calculated fields, value helps, and '
                                           'semantic compositions (e.g. Header to Items).\n'
                                           '2. **Behavior Definition & Implementation (BDEF & ABAP)**:\n'
                                           '   - **Behavior Definition (`.bdef`)**: Declarative contract specifying '
                                           'CRUD capabilities, validations, determinations, actions, draft handling, '
                                           'and locks.\n'
                                           '   - **Behavior Pool (`BP_`)**: Object-oriented ABAP class implementing '
                                           'the business logic using local handler classes (`lhc_`) and local saver '
                                           'classes (`lsc_`).\n'
                                           '3. **Business Service Provisioning**:\n'
                                           '   - **Service Definition (`.srvd`)**: Exposes the CDS projection views.\n'
                                           '   - **Service Binding (`.srvb`)**: Binds the service to OData V4 UI, '
                                           'OData V2 UI, or Web API protocols.',
                             'key_terms': [   {   'definition': 'Standard ABAP programming model uniting CDS data '
                                                                'models, declarative behavior definitions, and OData '
                                                                'services.',
                                                  'term': 'RAP Architecture'},
                                              {   'definition': 'Declarative specification of transactional '
                                                                'operations, validations, and determinations for a '
                                                                'business object.',
                                                  'term': 'Behavior Definition (BDEF)'},
                                              {   'definition': 'ABAP class containing implementation methods for '
                                                                'determinations, validations, and actions.',
                                                  'term': 'Behavior Pool'}],
                             'step_id': 'd79_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'RAP is built on 3 pillars: Data Model (CDS), Behavior Definition (BDEF & '
                                         'Behavior Pool), and Service Provisioning (SRVD/SRVB).',
                             'title': 'The Three Pillars of RAP Architecture'},
                         {   'content_md': '### The RAP Transactional Engine\n'
                                           'RAP provides two primary implementation flavors governed by who owns the '
                                           'database commits:\n'
                                           '\n'
                                           '1. **Managed RAP Scenario**:\n'
                                           '   - The RAP framework automatically generates standard create, read, '
                                           'update, delete (CRUD) operations and handles database writes to the '
                                           'persistence table.\n'
                                           '   - Developers only write business logic for custom determinations, '
                                           'validations, and actions.\n'
                                           '   - **Ideal for**: Greenfield applications and new S/4HANA business '
                                           'tables.\n'
                                           '2. **Unmanaged RAP Scenario**:\n'
                                           '   - The developer writes all read and write logic, typically delegating '
                                           'to existing legacy APIs, BAPIs, or custom update task function modules.\n'
                                           '   - **Ideal for**: Wrapping legacy brownfield business objects without '
                                           'modifying core database structures.\n'
                                           '3. **Strict Mode (`strict(2)`)**:\n'
                                           '   - Modern BDEFs mandate `strict(2)` mode, enforcing strict naming '
                                           'conventions, mandatory ETag definitions, authorization checks, and '
                                           'preventing obsolete syntax.',
                             'key_terms': [   {   'definition': 'Framework-managed CRUD persistence where the runtime '
                                                                'handles database inserts/updates automatically.',
                                                  'term': 'Managed RAP'},
                                              {   'definition': 'Developer-managed persistence where custom logic '
                                                                'delegates to legacy BAPIs or existing update '
                                                                'routines.',
                                                  'term': 'Unmanaged RAP'},
                                              {   'definition': 'Compiler directive enforcing modern RAP best '
                                                                'practices and safety checks.',
                                                  'term': 'strict(2)'}],
                             'step_id': 'd79_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Managed RAP automates CRUD persistence for greenfield applications; '
                                         'Unmanaged RAP allows custom delegation to existing legacy APIs.',
                             'title': 'Runtime Engines: Managed vs Unmanaged Orchestration'},
                         {   'company_context': {   'behavior_pool': 'ZBP_I_NOVAPURCHASEREQUISITION',
                                                    'bo_name': 'ZI_NovaPurchaseRequisition',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'service_binding': 'ZUI_NOVAPURCHASEREQUISITION_O4'},
                             'content_md': '### Complete RAP Layer Diagram\n'
                                           '```\n'
                                           '[Frontend: Fiori Elements List Report & Object Page]\n'
                                           '                        │  OData V4 Request\n'
                                           '                        ▼\n'
                                           '[Service Binding: ZUI_NOVAPURCHASEREQUISITION_O4]\n'
                                           '                        │  Protocol: OData V4 - UI\n'
                                           '                        ▼\n'
                                           '[Service Definition: ZUI_NOVAPURCHASEREQUISITION]\n'
                                           '                        │  Exposes Projections\n'
                                           '                        ▼\n'
                                           '[Projection Layer: ZC_NovaPurchaseRequisition]\n'
                                           '                        │  Consumption CDS View Entity + UI Annotations\n'
                                           '                        ▼\n'
                                           '[Core Data Model: ZI_NovaPurchaseRequisition] ◄───► [Behavior Definition: '
                                           'ZI_NovaPurchaseRequisition.bdef]\n'
                                           '                        │                                          │\n'
                                           '                        ▼                                          ▼\n'
                                           '   [HANA Persistence: ZNOVA_REQ_TBL]             [Behavior Pool: '
                                           'ZBP_I_NOVAPURCHASEREQUISITION]\n'
                                           '                                                   ├── LHC_HEADER '
                                           '(Determinations, Validations, Actions)\n'
                                           '                                                   └── LSC_SAVER '
                                           '(Finalize, Save Sequence)\n'
                                           '```',
                             'scenario': "Inspect the architectural layer stack for Nova Manufacturing's Purchase "
                                         'Requisition business object.',
                             'step_id': 'd79_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing RAP Business Object Stack'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'Nova Manufacturing is building two applications: 1) A new greenfield '
                                            'calibration log on custom tables, and 2) A tool that creates standard '
                                            'S/4HANA Sales Orders wrapped around legacy pricing logic. Select the '
                                            'implementation models.',
                             'options': [   {   'explanation': 'Correct! Greenfield tables leverage framework-managed '
                                                               'persistence; legacy API orchestration requires '
                                                               'unmanaged persistence.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': '1. Calibration log -> Managed RAP. 2. Sales Order wrapper -> '
                                                        'Unmanaged RAP (delegating to released sales order APIs).'},
                                            {   'explanation': 'Direct SQL on standard tables violates Clean Core and '
                                                               'bypasses sales order integrity.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Build both using direct SQL `INSERT INTO vbak` in a classic '
                                                        'report.'},
                                            {   'explanation': 'Managed RAP cannot directly mutate standard unreleased '
                                                               'SAP tables.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Build both as managed scenarios attempting to write directly '
                                                        'to standard SAP tables.'}],
                             'step_id': 'd79_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Managed RAP for greenfield custom tables; Unmanaged RAP for legacy API and '
                                         'standard document orchestration.',
                             'title': 'RAP Architectural Decision: Managed vs Unmanaged Selection'},
                         {   'instruction': 'As Lead Solution Architect, how do you handle this code review?',
                             'options': [   {   'explanation': 'Correct! Strict mode ensures that critical security '
                                                               'and concurrency protections are not bypassed.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Reject the pull request. Re-enable `strict(2)`: modern '
                                                        'S/4HANA developments must enforce strict mode to guarantee '
                                                        'mandatory authorization definitions, ETag concurrency, and '
                                                        'Clean Core compatibility.'},
                                            {   'explanation': 'Dangerous anti-pattern that introduces severe security '
                                                               'and concurrency vulnerabilities.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Approve the removal because compiler warnings slow down '
                                                        'delivery.'},
                                            {   'explanation': 'Unnecessary; the correct action is to fix the missing '
                                                               'authorization rules.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Delete the entire business object.'}],
                             'scenario': 'A legacy developer removes `strict(2)` from the Behavior Definition because '
                                         'the compiler complained about missing authorization definitions.',
                             'step_id': 'd79_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'BDEF Governance Challenge: Enforcing strict(2) Quality Standards'},
                         {   'assessment_type': 'mcq',
                             'questions': [   {   'concept_slug': 'rap-architecture-overview',
                                                  'explanation': 'RAP integrates CDS data models, BDEF transactional '
                                                                 'behavior, and Service Provisioning.',
                                                  'id': 'd79_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Data Model (CDS), Behavior Definition & '
                                                                             'Implementation (BDEF), and Service '
                                                                             'Provisioning (SRVD/SRVB)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Word, Excel, and PowerPoint'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'FTP, Telnet, and Gopher'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'HTML, CSS, and Flash'}],
                                                  'prompt': 'What are the three fundamental architectural pillars of '
                                                            'the ABAP RESTful Application Programming Model (RAP)?',
                                                  'question_id': 'd79_q1'},
                                              {   'concept_slug': 'bdef-and-behavior-implementation',
                                                  'explanation': 'The BDEF acts as the transactional contract for the '
                                                                 'RAP entity.',
                                                  'id': 'd79_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To declaratively define transactional '
                                                                             'capabilities (CRUD), determinations, '
                                                                             'validations, actions, draft handling, '
                                                                             'and locks.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To store user passwords in plain text.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To format HTML print templates.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To configure database backup '
                                                                             'schedules.'}],
                                                  'prompt': 'What is the primary role of a Behavior Definition '
                                                            '(`.bdef`) in a RAP business object?',
                                                  'question_id': 'd79_q2'},
                                              {   'concept_slug': 'rap-architecture-overview',
                                                  'explanation': 'Managed RAP automates persistence and standard '
                                                                 'transactional buffering.',
                                                  'id': 'd79_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Managed RAP Scenario'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Unmanaged RAP Scenario'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Manual Dynpro Scenario'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'External ODBC Scenario'}],
                                                  'prompt': 'In which RAP scenario does the framework automatically '
                                                            'generate standard CRUD database operations to the '
                                                            'persistence table?',
                                                  'question_id': 'd79_q3'},
                                              {   'concept_slug': 'bdef-and-behavior-implementation',
                                                  'explanation': '`strict(2)` enforces robust security, naming, and '
                                                                 'concurrency best practices.',
                                                  'id': 'd79_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It enforces modern RAP standards, '
                                                                             'requiring explicit authorization checks, '
                                                                             'ETags, and clean syntax.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It limits the table to 2 rows of data.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It restricts execution to 2 users '
                                                                             'simultaneously.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It requires 2 passwords to log in.'}],
                                                  'prompt': 'What does the compiler directive `strict(2)` mandate in '
                                                            'modern Behavior Definitions?',
                                                  'question_id': 'd79_q4'}],
                             'step_id': 'd79_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 79 Verification Assessment'},
                         {   'step_id': 'd79_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered the three pillars of RAP: Data Modeling, Behavior Definition, '
                                           'and Service Provisioning.\n'
                                           '- Differentiated Managed vs Unmanaged RAP persistence models.\n'
                                           '- Enforced `strict(2)` compile-time governance for enterprise application '
                                           'safety.',
                             'title': 'Day 79 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd79_s8_completion',
                             'recommended_mission': {'slug': 'nova-rap-bo-modeling-scaffold', 'title': 'RAP Business Object Architecture Scaffold', 'description': 'Design root and child entity compositions for production tracking.'},
                             'step_type': 'completion',
                             'summary_md': 'Superb work! You understand the RAP architectural foundation. Tomorrow, '
                                           'you will build the relational foundation: **RAP Business Object Modeling, '
                                           'Root Entities, and Composition Hierarchies**.',
                             'title': 'Day 79 Complete: RAP Architecture Big Picture Mastered'}],
            'subtitle': 'The three pillars: Data Modeling (CDS), Behavior Definition (BDEF), and Service Provisioning '
                        '(SRVD/SRVB).',
            'title': 'RAP Architecture: The Big Picture'},
    80: {   'atomic_concepts': ['rap-business-object-modeling', 'composition-hierarchies'],
            'day_number': 80,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'rap-bo-modeling-composition',
            'steps': [   {   'content_md': '### Root Entities & Tree Structures\n'
                                           'Enterprise business documents are rarely flat single-table structures. An '
                                           'order consists of a header and multiple line items; an invoice contains '
                                           'items and tax breakdowns.\n'
                                           '\n'
                                           '#### The Composition Tree Architecture:\n'
                                           '1. **Root Entity (`root view entity`)**:\n'
                                           '   - The top of the business object hierarchy (e.g., `ZI_PurchaseOrder`).\n'
                                           '   - Represents the complete business document; controls the transactional '
                                           'lifecycle, locking, and authorization for all child entities.\n'
                                           '2. **Composition of Child (`composition of [0..*] ZI_Child`)**:\n'
                                           '   - A specialized, tightly coupled association where the child entity '
                                           'cannot exist independently of the parent root.\n'
                                           '   - If the root is deleted, all composed child entities are automatically '
                                           'deleted (cascade delete).\n'
                                           '3. **Association to Parent (`association to parent ZI_Root`)**:\n'
                                           '   - The reverse link defined in the child entity referencing its '
                                           'immediate parent.\n'
                                           '   - Guarantees referential integrity and foreign key relationship.',
                             'key_terms': [   {   'definition': 'The top-level CDS view entity acting as the root node '
                                                                'of a RAP composition hierarchy.',
                                                  'term': 'Root View Entity'},
                                              {   'definition': 'Strict parent-child association where child lifecycle '
                                                                'is bound entirely to the parent.',
                                                  'term': 'Composition (`composition of`)'},
                                              {   'definition': 'Mandatory reverse association in child entities '
                                                                'pointing to their immediate parent node.',
                                                  'term': 'Association to Parent'}],
                             'step_id': 'd80_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'RAP business objects are modeled as composition trees with a single Root '
                                         'View Entity governing composed child entities.',
                             'title': 'Modeling RAP Business Object Hierarchies'},
                         {   'content_md': '### Defining Compositions in CDS View Entities\n'
                                           'Here is the exact syntax for defining parent and child CDS view entities:\n'
                                           '\n'
                                           '#### Root Entity Definition:\n'
                                           '```abap\n'
                                           '@AccessControl.authorizationCheck: #CHECK\n'
                                           "@EndUserText.label: 'Purchase Order Header Root'\n"
                                           'define root view entity ZI_NovaPOHeader\n'
                                           '  as select from znova_po_h\n'
                                           '  composition [0..*] of ZI_NovaPOItem as _Items\n'
                                           '{\n'
                                           '  key po_uuid        as POUUID,\n'
                                           '      po_number      as PurchaseOrderNumber,\n'
                                           '      company_code   as CompanyCode,\n'
                                           '      plant          as Plant,\n'
                                           '      _Items\n'
                                           '}\n'
                                           '```\n'
                                           '\n'
                                           '#### Child Entity Definition:\n'
                                           '```abap\n'
                                           '@AccessControl.authorizationCheck: #CHECK\n'
                                           "@EndUserText.label: 'Purchase Order Line Item'\n"
                                           'define view entity ZI_NovaPOItem\n'
                                           '  as select from znova_po_i\n'
                                           '  association to parent ZI_NovaPOHeader as _POHeader\n'
                                           '    on $projection.POUUID = _POHeader.POUUID\n'
                                           '{\n'
                                           '  key item_uuid      as ItemUUID,\n'
                                           '      po_uuid        as POUUID,\n'
                                           '      item_number    as ItemNumber,\n'
                                           '      material       as Material,\n'
                                           '      order_quantity as OrderQuantity,\n'
                                           '      _POHeader\n'
                                           '}\n'
                                           '```',
                             'key_terms': [   {   'definition': 'CDS keyword establishing a child entity composition '
                                                                'in the root entity.',
                                                  'term': 'composition [0..*] of'},
                                              {   'definition': 'CDS keyword establishing the parent link inside the '
                                                                'child entity.',
                                                  'term': 'association to parent'}],
                             'step_id': 'd80_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Parent uses `composition [0..*] of Child`, and Child uses `association to '
                                         'parent Parent` with matching foreign keys.',
                             'title': 'Syntax & Semantics of Composition in CDS'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'root_entity': 'ZI_NovaMfgOrder (Root)',
                                                    'tier_2': 'ZI_NovaMfgOperation (Child of Root)',
                                                    'tier_3': 'ZI_NovaMfgComponent (Child of Operation)'},
                             'content_md': '### 3-Tier Composition Tree\n'
                                           '```\n'
                                           '[ROOT: ZI_NovaMfgOrder] (Order 10000045, Plant PL01)\n'
                                           '  │\n'
                                           '  ├── composition [1..*] of ZI_NovaMfgOperation as _Operations\n'
                                           '        │\n'
                                           '        └── [CHILD: ZI_NovaMfgOperation] (Op 0010: Surface Mount '
                                           'Assembly)\n'
                                           '              │\n'
                                           '              ├── association to parent ZI_NovaMfgOrder as _Order\n'
                                           '              │\n'
                                           '              └── composition [0..*] of ZI_NovaMfgComponent as '
                                           '_Components\n'
                                           '                    │\n'
                                           '                    └── [GRANDCHILD: ZI_NovaMfgComponent] (RAW-01 Sensor '
                                           'Array)\n'
                                           '                          └── association to parent ZI_NovaMfgOperation as '
                                           '_Operation\n'
                                           '```',
                             'scenario': 'Nova models a 3-tier composition hierarchy for Heidelberg (PL01): Production '
                                         'Order Header -> Operations -> Component Allocations.',
                             'step_id': 'd80_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Production Order Composition Tree'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "A child CDS entity fails to activate with error: 'Association _Order is "
                                            "not defined as association to parent'. What is the fix?",
                             'options': [   {   'explanation': 'Correct! RAP requires the explicit keyword '
                                                               '`association to parent` in child entities to establish '
                                                               'tree composition.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Change `association [1..1] to ZI_Order` to `association to '
                                                        'parent ZI_Order as _Order on $projection.OrderUUID = '
                                                        '_Order.OrderUUID`.'},
                                            {   'explanation': 'Deleting the entity does not solve the composition '
                                                               'requirement.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Delete the child entity completely.'},
                                            {   'explanation': 'Unmanaged reports do not provide modern CDS '
                                                               'composition semantics.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Change the root entity to an unmanaged report.'}],
                             'step_id': 'd80_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Always declare child-to-parent associations using the exact syntax '
                                         '`association to parent`.',
                             'title': 'Composition Modeling Simulation: Fixing Broken Parent References'},
                         {   'instruction': 'What is the correct architectural modeling choice?',
                             'options': [   {   'explanation': 'Correct! Compositions are exclusively for '
                                                               'lifecycle-bound child entities (like PO Items). '
                                                               'Independent master data entities must be regular '
                                                               'associations.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Use a standard `association [0..1] to I_Product`. Material '
                                                        'Master is an independent business object that exists before '
                                                        'and after the purchase order; it must NOT be composed (which '
                                                        'would delete the material if the PO is deleted).'},
                                            {   'explanation': 'Catastrophic error that would destroy master data.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Use `composition of I_Product` so every purchase order '
                                                        'deletes the material master when closed.'},
                                            {   'explanation': 'Fails dynamic data modeling.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Hardcode the material description as a comment in the code.'}],
                             'scenario': "Nova's developer wants to model the relationship between Purchase Order Item "
                                         'and Material Master (`I_Product`). Should this be a `composition of` or a '
                                         'standard `association [0..1] to`?',
                             'step_id': 'd80_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Data Modeling Challenge: Cross-BO Association vs Composition'},
                         {   'assessment_type': 'rap_challenge',
                             'questions': [   {   'concept_slug': 'rap-business-object-modeling',
                                                  'explanation': 'The Root View Entity is the primary anchor of the '
                                                                 'RAP business object.',
                                                  'id': 'd80_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Root View Entity (`define root view '
                                                                             'entity`)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Leaf View Entity'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Shadow View'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Sub-routine Pool'}],
                                                  'prompt': 'What is the top-level entity called that controls the '
                                                            'transactional lifecycle, locks, and authorization for a '
                                                            'RAP business object tree?',
                                                  'question_id': 'd80_q1'},
                                              {   'concept_slug': 'composition-hierarchies',
                                                  'explanation': '`composition of` binds the child entity lifecycle to '
                                                                 'the parent.',
                                                  'id': 'd80_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'composition [0..*] of ChildEntity'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'external join to ChildEntity'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'copy table ChildEntity'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'import ChildEntity'}],
                                                  'prompt': 'Which CDS keyword defines a lifecycle-dependent child '
                                                            'relationship from a root entity to its line items?',
                                                  'question_id': 'd80_q2'},
                                              {   'concept_slug': 'composition-hierarchies',
                                                  'explanation': '`association to parent` defines the reverse '
                                                                 'composition relationship.',
                                                  'id': 'd80_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'association to parent ParentEntity'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'goto ParentEntity'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'foreign key ParentEntity'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'extends ParentEntity'}],
                                                  'prompt': 'What mandatory keyword must be used inside a child CDS '
                                                            'entity to declare the reverse foreign-key link to its '
                                                            'parent node?',
                                                  'question_id': 'd80_q3'},
                                              {   'concept_slug': 'rap-business-object-modeling',
                                                  'explanation': 'Compositions enforce cascade deletion, ensuring zero '
                                                                 'orphaned child records.',
                                                  'id': 'd80_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'All composed child line items are '
                                                                             'automatically deleted in a cascade '
                                                                             'delete.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Child items remain orphaned in the '
                                                                             'database forever.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'The database crashes with a fatal '
                                                                             'error.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'The user is forced to re-type the line '
                                                                             'items.'}],
                                                  'prompt': 'What happens to composed child line items when the parent '
                                                            'root entity is deleted in a Managed RAP scenario?',
                                                  'question_id': 'd80_q4'}],
                             'step_id': 'd80_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 80 Verification Assessment'},
                         {   'step_id': 'd80_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Modeled multi-tier RAP composition trees using `define root view '
                                           'entity`.\n'
                                           '- Declared strict parent-child compositions (`composition of`) and reverse '
                                           'links (`association to parent`).\n'
                                           '- Differentiated lifecycle compositions from cross-BO master data '
                                           'associations.',
                             'title': 'Day 80 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd80_s8_completion',
                             'recommended_mission': {'slug': 'nova-rap-composition-binding', 'title': 'RAP BO Composition & Child Navigation', 'description': 'Define compositions of child items with associations to parent.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You know how to model multi-tier entities. Tomorrow, you will '
                                           'define their transactional behavior: **Behavior Definitions (BDEF) - '
                                           'Managed vs Unmanaged**.',
                             'title': 'Day 80 Complete: Composition Hierarchies Mastered'}],
            'subtitle': 'Root view entities, child entities, composition trees (`composition of`), and association to '
                        'parent.',
            'title': 'RAP Business Object Modeling & Composition'},
    81: {   'atomic_concepts': ['bdef-syntax', 'managed-vs-unmanaged-rap'],
            'day_number': 81,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'rap-bdef-managed-vs-unmanaged',
            'steps': [   {   'content_md': '### Declarative Transactional Contracts in RAP\n'
                                           'The Behavior Definition (`.bdef`) is the definitive contract specifying '
                                           'all transactional capabilities of a business object tree.\n'
                                           '\n'
                                           '#### Essential Header Syntax of a Managed BDEF:\n'
                                           '```abap\n'
                                           'managed implementation in class zbp_i_novapoheader unique;\n'
                                           'strict(2);\n'
                                           'with draft;\n'
                                           '\n'
                                           'define behavior for ZI_NovaPOHeader alias PurchaseOrder\n'
                                           'persistent table znova_po_h\n'
                                           'draft table znova_po_h_d\n'
                                           'lock master total etag LastChangedAt\n'
                                           'authorization master ( instance )\n'
                                           'etag master LocalLastChangedAt\n'
                                           '{\n'
                                           '  create; update; delete;\n'
                                           '  association _Items { create; with draft; }\n'
                                           '\n'
                                           '  field ( readonly, numbering : managed ) POUUID;\n'
                                           '  field ( mandatory ) CompanyCode, Plant, Supplier;\n'
                                           '}\n'
                                           '```',
                             'key_terms': [   {   'definition': 'The underlying active database table storing '
                                                                'committed business records.',
                                                  'term': 'persistent table'},
                                              {   'definition': 'Shadow database table buffering uncommitted user '
                                                                'modifications.',
                                                  'term': 'draft table'},
                                              {   'definition': 'Declares that the root entity controls the '
                                                                'transactional lock for the entire entity tree.',
                                                  'term': 'lock master'}],
                             'step_id': 'd81_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'The BDEF declaratively binds CDS entities to persistent tables, draft '
                                         'tables, lock masters, and CRUD operations.',
                             'title': 'The Behavior Definition (BDEF) Specification'},
                         {   'content_md': '### Architectural Differences in Execution\n'
                                           '| Dimension | Managed RAP | Unmanaged RAP |\n'
                                           '|---|---|---|\n'
                                           '| **CRUD Handlers** | Automatically provided by RAP runtime | Developer '
                                           'implements `create`, `update`, `delete` in LHC |\n'
                                           '| **Transactional Buffer** | Built-in in-memory transactional buffer | '
                                           'Developer manages local internal tables as buffer |\n'
                                           '| **Save Logic** | Framework automatically executes SQL `INSERT/UPDATE` | '
                                           'Developer implements `save` method in LSC (e.g. calling BAPIs) |\n'
                                           '| **Draft Support** | Turnkey draft enablement (`with draft`) | Manual '
                                           'draft implementation or unmanaged draft |\n'
                                           '| **Best Use Case** | Greenfield custom tables | Wrapping standard legacy '
                                           'APIs and existing update modules |',
                             'key_terms': [   {   'definition': 'In-memory state holding pending creates, updates, and '
                                                                'deletes during the interaction phase.',
                                                  'term': 'Transactional Buffer'},
                                              {   'definition': 'Local class inside the behavior pool implementing '
                                                                'business logic methods.',
                                                  'term': 'LHC (Local Handler Class)'}],
                             'step_id': 'd81_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Managed RAP automates buffering and SQL persistence; Unmanaged RAP delegates '
                                         'save execution to custom developer code.',
                             'title': 'Deep Comparison: Managed vs Unmanaged Execution'},
                         {   'company_context': {   'child': 'ZI_NovaPOItem',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'root': 'ZI_NovaPOHeader'},
                             'content_md': '### Full Composition BDEF Snippet\n'
                                           '```abap\n'
                                           'managed implementation in class zbp_i_novapoheader unique;\n'
                                           'strict(2);\n'
                                           '\n'
                                           'define behavior for ZI_NovaPOHeader alias PurchaseOrder\n'
                                           'persistent table znova_po_h\n'
                                           'lock master\n'
                                           'authorization master ( instance )\n'
                                           'etag master LocalLastChangedAt\n'
                                           '{\n'
                                           '  create; update; delete;\n'
                                           '  association _Items { create; }\n'
                                           '\n'
                                           '  mapping for znova_po_h {\n'
                                           '    POUUID = po_uuid;\n'
                                           '    CompanyCode = company_code;\n'
                                           '    Plant = plant;\n'
                                           '  }\n'
                                           '}\n'
                                           '\n'
                                           'define behavior for ZI_NovaPOItem alias Item\n'
                                           'persistent table znova_po_i\n'
                                           'lock dependent by _POHeader\n'
                                           'authorization dependent by _POHeader\n'
                                           'etag master LocalLastChangedAt\n'
                                           '{\n'
                                           '  update; delete;\n'
                                           '  association _POHeader;\n'
                                           '\n'
                                           '  field ( readonly ) POUUID;\n'
                                           '  mapping for znova_po_i {\n'
                                           '    ItemUUID = item_uuid;\n'
                                           '    POUUID = po_uuid;\n'
                                           '    Material = material;\n'
                                           '  }\n'
                                           '}\n'
                                           '```',
                             'scenario': 'Review the full BDEF binding the Purchase Order Header and its composed '
                                         'Items.',
                             'step_id': 'd81_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing BDEF with Child Composition'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "A child entity in a managed BDEF fails syntax checks with error: 'Child "
                                            "entity must declare lock dependent'. How do you resolve this?",
                             'options': [   {   'explanation': 'Correct! Composed child entities in RAP must declare '
                                                               '`lock dependent by _ParentAssociation`.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Add `lock dependent by _POHeader` to the child entity '
                                                        'definition, linking locking to the parent association.'},
                                            {   'explanation': 'A business object tree can have only ONE lock master '
                                                               '(the root entity).',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Declare the child entity as a second independent `lock '
                                                        'master`.'},
                                            {   'explanation': 'Disabling locks leads to fatal data corruption from '
                                                               'concurrent writes.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Disable locking completely across the system.'}],
                             'step_id': 'd81_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Composed child entities must declare `lock dependent by _ParentAssociation`.',
                             'title': 'BDEF Configuration Simulation: Resolving Child Lock Dependency'},
                         {   'instruction': 'Why does this trigger a critical runtime error in RAP?',
                             'options': [   {   'explanation': 'Correct! The RAP runtime orchestrates the global LUW '
                                                               'commit; manual commits break the transactional '
                                                               'integrity.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'In RAP, explicit `COMMIT WORK` inside the save method is '
                                                        'strictly forbidden; the RAP framework executes the single '
                                                        'authoritative COMMIT WORK after all saver classes complete '
                                                        'successfully.'},
                                            {   'explanation': 'Unmanaged scenarios do save data, but the framework '
                                                               'controls the commit boundary.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Because unmanaged scenarios do not save data to the '
                                                        'database.'},
                                            {   'explanation': 'Nonsensical; S/4HANA runs natively on SAP HANA with '
                                                               'ABAP.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Because the database does not support ABAP.'}],
                             'scenario': 'In an Unmanaged RAP scenario, a developer places a `COMMIT WORK` inside the '
                                         '`save` method of the Local Saver Class.',
                             'step_id': 'd81_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Architecture Challenge: Unmanaged Save with Commit Work'},
                         {   'assessment_type': 'rap_challenge',
                             'questions': [   {   'concept_slug': 'bdef-syntax',
                                                  'explanation': '`persistent table` specifies the active database '
                                                                 'table.',
                                                  'id': 'd81_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'persistent table <table_name>'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'database storage <table_name>'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'disk volume <table_name>'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'ram cache <table_name>'}],
                                                  'prompt': 'Which keyword in a RAP Behavior Definition designates the '
                                                            'database table where active committed business records '
                                                            'are persisted?',
                                                  'question_id': 'd81_q1'},
                                              {   'concept_slug': 'managed-vs-unmanaged-rap',
                                                  'explanation': 'Managed RAP automates database persistence; '
                                                                 'Unmanaged RAP gives developers manual save control.',
                                                  'id': 'd81_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'In Managed RAP, the framework '
                                                                             'automatically handles standard CRUD '
                                                                             'database persistence, whereas in '
                                                                             'Unmanaged RAP, the developer writes '
                                                                             'custom save logic.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Managed RAP only runs on mobile phones.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Unmanaged RAP does not support CDS '
                                                                             'views.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Managed RAP does not require user '
                                                                             'authentication.'}],
                                                  'prompt': 'What is the primary architectural difference between a '
                                                            'Managed RAP and an Unmanaged RAP scenario?',
                                                  'question_id': 'd81_q2'},
                                              {   'concept_slug': 'bdef-syntax',
                                                  'explanation': 'Child entities delegate locking to the root via '
                                                                 '`lock dependent by _ParentAssociation`.',
                                                  'id': 'd81_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'lock dependent by _ParentAssociation'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'lock master independent'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'no locking required'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'disable lock'}],
                                                  'prompt': 'How must concurrency locking be declared in a child '
                                                            'entity composed under a root entity in a RAP Behavior '
                                                            'Definition?',
                                                  'question_id': 'd81_q3'},
                                              {   'concept_slug': 'managed-vs-unmanaged-rap',
                                                  'explanation': 'Manual commits in RAP trigger fatal runtime dumps '
                                                                 'because RAP manages the LUW.',
                                                  'id': 'd81_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'The RAP transactional runtime terminates '
                                                                             'with a short dump because the framework '
                                                                             'controls the commit boundary.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'The operation executes 10 times faster.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'The database automatically creates a '
                                                                             'backup.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'The statement is silently ignored.'}],
                                                  'prompt': 'What occurs if a developer writes an explicit `COMMIT '
                                                            'WORK` statement inside an Unmanaged RAP saver method?',
                                                  'question_id': 'd81_q4'}],
                             'step_id': 'd81_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 81 Verification Assessment'},
                         {   'step_id': 'd81_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Authored declarative Behavior Definitions (BDEF) for managed and '
                                           'unmanaged entities.\n'
                                           '- Configured persistent tables, lock masters, and child lock '
                                           'dependencies.\n'
                                           '- Enforced framework-controlled transactional commit boundaries.',
                             'title': 'Day 81 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd81_s8_completion',
                             'recommended_mission': {'slug': 'nova-rap-managed-bdef-setup', 'title': 'Managed RAP Behavior Definition Setup', 'description': 'Configure transactional characteristics in managed BDEF.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You know how to define transactional contracts. Tomorrow, you '
                                           'will master the lifecycle that governs commits: **The RAP Transactional '
                                           'Save Sequence**.',
                             'title': 'Day 81 Complete: BDEF Syntax & Scenarios Mastered'}],
            'subtitle': 'BDEF syntax, persistent tables, draft tables, lock master/dependent, and implementation '
                        'classes.',
            'title': 'Behavior Definition (BDEF): Managed vs Unmanaged'},
    82: {   'atomic_concepts': ['rap-save-sequence', 'interaction-vs-save-phase'],
            'day_number': 82,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'rap-transactional-save-sequence',
            'steps': [   {   'content_md': '### Interaction Phase vs Save Phase\n'
                                           'The RAP transactional engine strictly partitions document processing into '
                                           'two sequential, decoupled phases:\n'
                                           '\n'
                                           '#### 1. The Interaction Phase\n'
                                           '- **What Happens**: User enters values, modifies fields, navigates '
                                           'screens, and clicks action buttons.\n'
                                           '- **Transactional State**: All changes exist exclusively in the '
                                           '**In-Memory Transactional Buffer** (or draft table). No permanent database '
                                           'commit occurs.\n'
                                           '- **Allowed Logic**: Determinations on modify, field calculations, '
                                           'temporary validations.\n'
                                           '- **Safe from Corruption**: If the user cancels, the buffer is simply '
                                           'discarded with zero database rollback overhead.\n'
                                           '\n'
                                           '#### 2. The Save Phase\n'
                                           "- **What Happens**: The user clicks 'Save' (or an action triggers `COMMIT "
                                           'ENTITIES`).\n'
                                           '- **Transactional State**: Strict, multi-step orchestration moving buffer '
                                           'data safely into persistent database tables with ACID guarantees.',
                             'key_terms': [   {   'definition': 'State where user inputs mutate in-memory '
                                                                'transactional buffers without database commits.',
                                                  'term': 'Interaction Phase'},
                                              {   'definition': 'Orchestrated sequence executing final validations, '
                                                                'late numbering, and database persistence.',
                                                  'term': 'Save Phase'}],
                             'step_id': 'd82_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'RAP decouples the user interaction phase (in-memory buffer) from the save '
                                         'phase (ACID database commit).',
                             'title': 'The Two Phases of the RAP Transactional Model'},
                         {   'content_md': '### Step-by-Step Execution of the Save Phase\n'
                                           'When a save is triggered, the RAP Local Saver Class (`lsc_`) executes 5 '
                                           'distinct methods in strict order:\n'
                                           '\n'
                                           '```\n'
                                           '[Save Triggered] ──► FINALIZE ──► CHECK_BEFORE_SAVE ──► ADJUST_NUMBERS ──► '
                                           'SAVE ──► CLEANUP\n'
                                           '```\n'
                                           '\n'
                                           '1. **`FINALIZE`**:\n'
                                           '   - Executes determinations `on save`. Last chance to calculate derived '
                                           'values before final validation.\n'
                                           '2. **`CHECK_BEFORE_SAVE`**:\n'
                                           '   - Executes validations `on save`. If any validation fails (records '
                                           'added to `failed` structure), the save sequence **aborts immediately**, '
                                           'rolling back to the interaction phase.\n'
                                           '3. **`ADJUST_NUMBERS`**:\n'
                                           '   - Assigns final enterprise numbers from standard number ranges (Late '
                                           'Numbering) to replace temporary IDs.\n'
                                           '4. **`SAVE`**:\n'
                                           '   - Data is written to persistent database tables.\n'
                                           '5. **`CLEANUP`**:\n'
                                           '   - Clears in-memory buffers after save (or after rollback if a failure '
                                           'occurred).',
                             'key_terms': [   {   'definition': 'Save phase stage running final determinations on '
                                                                'save.',
                                                  'term': 'FINALIZE'},
                                              {   'definition': 'Save phase stage executing final validations before '
                                                                'database modification.',
                                                  'term': 'CHECK_BEFORE_SAVE'},
                                              {   'definition': 'Stage drawing authoritative numbers from number '
                                                                'ranges for late numbering.',
                                                  'term': 'ADJUST_NUMBERS'}],
                             'step_id': 'd82_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'The save sequence executes: FINALIZE -> CHECK_BEFORE_SAVE -> ADJUST_NUMBERS '
                                         '-> SAVE -> CLEANUP.',
                             'title': 'The 5 Stages of the RAP Save Sequence'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'order_id': 'PO 4500001092',
                                                    'saver_class': 'LSC_ZI_NOVAPOHEADER'},
                             'content_md': '### Execution Log Trace in Eclipse ADT Console\n'
                                           '```\n'
                                           '[10:14:02] INTERACTION: User modified OrderQuantity = 500 on component '
                                           'RAW-01.\n'
                                           "[10:14:03] USER ACTION: User clicked 'Save'. Entering Save Phase.\n"
                                           '[10:14:03.1] STAGE 1: FINALIZE -> Calculated TotalNetAmount = 84,500.00 '
                                           'EUR.\n'
                                           '[10:14:03.2] STAGE 2: CHECK_BEFORE_SAVE -> Budget check passed. Supplier '
                                           'VEND-101 verified. FAILED is empty.\n'
                                           '[10:14:03.3] STAGE 3: ADJUST_NUMBERS -> Drew final number 4500001092 from '
                                           'Number Range Object ZNOVA_PO.\n'
                                           '[10:14:03.4] STAGE 4: SAVE -> Persistent table znova_po_h updated. Draft '
                                           'record cleared.\n'
                                           '[10:14:03.5] STAGE 5: CLEANUP -> Transactional buffer reset. Commit '
                                           'complete.\n'
                                           '```',
                             'scenario': 'Trace the execution log when a buyer saves Purchase Order 4500001092 in '
                                         'Heidelberg (PL01).',
                             'step_id': 'd82_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Save Sequence Execution Trace'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'A budget validation fails during the Save Phase because order amount '
                                            'exceeds credit limit. At which stage does the save abort?',
                             'options': [   {   'explanation': 'Correct! If `failed` is populated during '
                                                               '`CHECK_BEFORE_SAVE`, the sequence aborts before '
                                                               'numbers are drawn or data is written.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'At `CHECK_BEFORE_SAVE`: the validation adds the entity key to '
                                                        'the `failed` structure, causing RAP to abort the save and '
                                                        'return to the user with state error messages.'},
                                            {   'explanation': 'Completely false; invalid records are never saved to '
                                                               'persistent storage.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'At `CLEANUP`: the system saves anyway and then deletes the '
                                                        'record afterwards.'},
                                            {   'explanation': 'Save failures are standard business exceptions managed '
                                                               'by the framework.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'The system reboots automatically.'}],
                             'step_id': 'd82_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Validations failing in `CHECK_BEFORE_SAVE` immediately abort the save '
                                         'sequence.',
                             'title': 'Save Sequence Diagnostic Simulation: Aborting an Invalid Save'},
                         {   'instruction': 'How does the RAP save sequence prevent number gaps?',
                             'options': [   {   'explanation': 'Correct! Late Numbering draws numbers in stage 3 '
                                                               '(`ADJUST_NUMBERS`) strictly after validation has '
                                                               'passed.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Use Late Numbering in `ADJUST_NUMBERS`: numbers are drawn '
                                                        'only after `CHECK_BEFORE_SAVE` has confirmed zero errors, '
                                                        'guaranteeing that numbers are never drawn for aborted '
                                                        'documents.'},
                                            {   'explanation': 'Drawing numbers early causes massive gaps if the user '
                                                               'cancels.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Draw numbers during the initial mouse hover in the '
                                                        'interaction phase.'},
                                            {   'explanation': 'Unacceptable; enterprise documents require legal '
                                                               'tracking numbers.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Eliminate purchase order numbers entirely.'}],
                             'scenario': 'A financial auditor complains that failed purchase orders are consuming '
                                         'legal sequential numbers from the official number range, leaving audit gaps.',
                             'step_id': 'd82_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Architecture Challenge: Preventing Gap Numbers in Number Ranges'},
                         {   'assessment_type': 'technical_audit',
                             'questions': [   {   'concept_slug': 'rap-save-sequence',
                                                  'explanation': 'The standard save sequence is FINALIZE -> '
                                                                 'CHECK_BEFORE_SAVE -> ADJUST_NUMBERS -> SAVE -> '
                                                                 'CLEANUP.',
                                                  'id': 'd82_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'FINALIZE -> CHECK_BEFORE_SAVE -> '
                                                                             'ADJUST_NUMBERS -> SAVE -> CLEANUP'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'SAVE -> CLEANUP -> FINALIZE -> CHECK -> '
                                                                             'ADJUST'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'CLEANUP -> ADJUST -> SAVE -> CHECK -> '
                                                                             'FINALIZE'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'CHECK -> SAVE -> FINALIZE -> ADJUST -> '
                                                                             'CLEANUP'}],
                                                  'prompt': 'What is the exact chronological sequence of the five '
                                                            'stages in the RAP Save Phase?',
                                                  'question_id': 'd82_q1'},
                                              {   'concept_slug': 'interaction-vs-save-phase',
                                                  'explanation': 'The interaction phase buffers modifications in '
                                                                 'memory/draft.',
                                                  'id': 'd82_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'In the in-memory transactional buffer or '
                                                                             'draft table, without persistent database '
                                                                             'commit.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Permanently committed to table ACDOCA.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'On an external USB thumb drive.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'In the browser URL bar.'}],
                                                  'prompt': 'Where does data reside during the RAP Interaction Phase '
                                                            'before a save is triggered?',
                                                  'question_id': 'd82_q2'},
                                              {   'concept_slug': 'rap-save-sequence',
                                                  'explanation': '`ADJUST_NUMBERS` assigns final numbers after '
                                                                 'validation checks pass.',
                                                  'id': 'd82_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'ADJUST_NUMBERS'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'FINALIZE'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'CLEANUP'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'INTERACTION'}],
                                                  'prompt': 'Which stage of the save sequence is responsible for '
                                                            'assigning final sequential numbers from number range '
                                                            'intervals (Late Numbering)?',
                                                  'question_id': 'd82_q3'},
                                              {   'concept_slug': 'interaction-vs-save-phase',
                                                  'explanation': 'Populating `failed` in `CHECK_BEFORE_SAVE` cleanly '
                                                                 'aborts the save process.',
                                                  'id': 'd82_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'The save sequence terminates '
                                                                             'immediately, persistent tables remain '
                                                                             'untouched, and the user receives error '
                                                                             'messages.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'The system corrupts the hard drive.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'The document is saved anyway with status '
                                                                             "'CORRUPT'."},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'All database tables are deleted.'}],
                                                  'prompt': 'What happens during the save sequence if a business '
                                                            'validation in `CHECK_BEFORE_SAVE` reports a failure by '
                                                            'populating the `failed` structure?',
                                                  'question_id': 'd82_q4'}],
                             'step_id': 'd82_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 82 Verification Assessment'},
                         {   'step_id': 'd82_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Differentiated the Interaction Phase (buffer) from the Save Phase (ACID '
                                           'commit).\n'
                                           '- Mastered the 5 stages of the RAP save sequence (Finalize, Check, Adjust, '
                                           'Save, Cleanup).\n'
                                           '- Implemented Late Numbering in `ADJUST_NUMBERS` to prevent number range '
                                           'gaps.',
                             'title': 'Day 82 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd82_s8_completion',
                             'recommended_mission': {'slug': 'nova-rap-unmanaged-bdef-handler', 'title': 'Unmanaged RAP Save Handler', 'description': 'Implement custom transactional save sequence in unmanaged BDEF.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You understand the transactional save engine. Tomorrow, you '
                                           'will master automated business calculations: **RAP Determinations**.',
                             'title': 'Day 82 Complete: RAP Save Sequence Mastered'}],
            'subtitle': 'Interaction phase vs save phase: finalize, check_before_save, adjust_numbers, save, and '
                        'cleanup.',
            'title': 'RAP Transactional Buffer & Save Sequence'},
    83: {   'atomic_concepts': ['rap-determinations', 'determination-triggers'],
            'day_number': 83,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'rap-determinations',
            'steps': [   {   'content_md': '### Automatic Business Derivations\n'
                                           'A **Determination** is an automated calculation or derivation executed by '
                                           'the RAP framework when specific trigger conditions occur.\n'
                                           '\n'
                                           '#### Execution Timing:\n'
                                           '1. **`on modify`**:\n'
                                           '   - Triggered immediately during the interaction phase when a user '
                                           'modifies specific fields.\n'
                                           '   - Example: User changes `OrderQuantity` -> determination immediately '
                                           'recalculates `TotalNetAmount` and refreshes the UI.\n'
                                           '2. **`on save`**:\n'
                                           '   - Triggered during the `FINALIZE` stage of the save phase.\n'
                                           '   - Example: Calculating final tax rates or carbon footprint scores right '
                                           'before document commit.',
                             'key_terms': [   {   'definition': 'Automated business logic calculation triggered by '
                                                                'entity state changes.',
                                                  'term': 'Determination'},
                                              {   'definition': 'Determination executed immediately upon field '
                                                                'modification during user interaction.',
                                                  'term': 'on modify trigger'},
                                              {   'definition': 'Determination executed during the Finalize stage '
                                                                'before document commit.',
                                                  'term': 'on save trigger'}],
                             'step_id': 'd83_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Determinations automate derivations either immediately (`on modify`) or at '
                                         'final commit (`on save`).',
                             'title': 'What are RAP Determinations?'},
                         {   'content_md': '### Declaring and Implementing Determinations\n'
                                           '#### BDEF Declaration:\n'
                                           '```abap\n'
                                           'determination calculateTotalAmount on modify { field OrderQuantity, '
                                           'NetPrice; }\n'
                                           '```\n'
                                           '\n'
                                           '#### Behavior Pool Implementation Method:\n'
                                           '```abap\n'
                                           'METHOD calculateTotalAmount.\n'
                                           '  READ ENTITIES OF ZI_NovaPOHeader IN LOCAL MODE\n'
                                           '    ENTITY PurchaseOrder\n'
                                           '    FIELDS ( OrderQuantity NetPrice )\n'
                                           '    WITH CORRESPONDING #( keys )\n'
                                           '    RESULT DATA(lt_orders).\n'
                                           '\n'
                                           '  LOOP AT lt_orders ASSIGNING FIELD-SYMBOL(<order>).\n'
                                           '    DATA(lv_total) = <order>-OrderQuantity * <order>-NetPrice.\n'
                                           '    MODIFY ENTITIES OF ZI_NovaPOHeader IN LOCAL MODE\n'
                                           '      ENTITY PurchaseOrder\n'
                                           '      UPDATE FIELDS ( TotalNetAmount )\n'
                                           '      WITH VALUE #( ( %tky = <order>-%tky TotalNetAmount = lv_total ) ).\n'
                                           '  ENDLOOP.\n'
                                           'ENDMETHOD.\n'
                                           '```\n'
                                           'Notice `IN LOCAL MODE`: this special EML addition bypasses authorization '
                                           'checks and circular trigger loops inside the determination handler.',
                             'key_terms': [   {   'definition': 'EML addition allowing internal handler logic to '
                                                                'update entities without triggering redundant loops.',
                                                  'term': 'IN LOCAL MODE'},
                                              {   'definition': 'Technical key identifying the active or draft record '
                                                                'in the transactional buffer.',
                                                  'term': '%tky (Transactional Key)'}],
                             'step_id': 'd83_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Determinations read data using EML `READ ENTITIES IN LOCAL MODE` and update '
                                         'derivations using `MODIFY ENTITIES IN LOCAL MODE`.',
                             'title': 'BDEF Declaration & Local Handler Implementation'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'derived_fields': ['DiscountPercentage', 'TotalNetAmount'],
                                                    'trigger_fields': ['OrderQuantity', 'Plant']},
                             'content_md': '### Live Interaction Flow in Fiori Elements\n'
                                           '```\n'
                                           '[User Action: Enters OrderQuantity = 500 at Plant PL01]\n'
                                           '               │\n'
                                           '               ▼  OData PATCH request\n'
                                           "[RAP Runtime detects trigger on 'OrderQuantity']\n"
                                           '               │\n'
                                           '               ▼  Invokes LHC method: calculateTotalAmount\n'
                                           '[EML MODIFY ENTITIES: Sets Discount = 15%, NetAmount = 84,500.00 EUR]\n'
                                           '               │\n'
                                           '               ▼  Side Effects response updates browser view\n'
                                           '[Fiori UI updates Total Net Amount instantly on screen]\n'
                                           '```',
                             'scenario': 'When buyer changes quantity for sensor RAW-01 at Heidelberg, the system '
                                         'automatically applies plant-specific discount tables.',
                             'step_id': 'd83_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Price Calculation Determination'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'A determination on field `TotalAmount` executes an update on '
                                            '`TotalAmount`, triggering an infinite recursive loop. How do you prevent '
                                            'this?',
                             'options': [   {   'explanation': 'Correct! Explicit trigger fields and `IN LOCAL MODE` '
                                                               'prevent self-triggering recursive determination '
                                                               'cascades.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Always specify explicit `field { ... }` trigger conditions in '
                                                        'the BDEF, and use `IN LOCAL MODE` during EML updates.'},
                                            {   'explanation': 'Sleeping does not prevent infinite recursion; it '
                                                               'merely delays the inevitable stack overflow dump.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Add a 5-second sleep statement inside the loop.'},
                                            {   'explanation': 'Fails modern enterprise automation requirements.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Delete the determination and make the user calculate math on '
                                                        'paper.'}],
                             'step_id': 'd83_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Specify precise trigger fields and execute updates `IN LOCAL MODE` to '
                                         'prevent recursive loops.',
                             'title': 'Determination Trigger Simulation: Preventing Infinite Recursion'},
                         {   'instruction': 'What is the architectural remediation?',
                             'options': [   {   'explanation': 'Correct! `on modify` determinations must be sub-second '
                                                               "to prevent freezing the user's interactive Fiori "
                                                               'screen.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Move the expensive calculation to `on save` (in the Finalize '
                                                        'stage), or trigger it via an asynchronous BTP event or '
                                                        'explicit user Action, keeping `on modify` lean and snappy.'},
                                            {   'explanation': 'Unacceptable UX degradation violating Fiori '
                                                               'responsiveness standards.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Keep it in `on modify` and tell users to wait patiently.'},
                                            {   'explanation': 'Bypasses core business logic and security.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': "Run the calculation on the user's mobile phone CPU."}],
                             'scenario': 'A developer places a 20-second external machine learning API call inside a '
                                         'determination `on modify` that runs on every keystroke.',
                             'step_id': 'd83_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Performance Challenge: Heavy Calculations in on modify'},
                         {   'assessment_type': 'rap_challenge',
                             'questions': [   {   'concept_slug': 'rap-determinations',
                                                  'explanation': 'Determinations automate calculations and state '
                                                                 'derivations.',
                                                  'id': 'd83_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To automatically derive or calculate '
                                                                             'field values when defined trigger events '
                                                                             'occur on an entity.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To delete historical audit logs.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To lock user accounts after password '
                                                                             'failure.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To encrypt hard disk volumes.'}],
                                                  'prompt': 'What is the primary architectural purpose of a RAP '
                                                            'Determination?',
                                                  'question_id': 'd83_q1'},
                                              {   'concept_slug': 'determination-triggers',
                                                  'explanation': '`on modify` determinations execute immediately upon '
                                                                 'trigger field modification.',
                                                  'id': 'd83_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Immediately during the interaction phase '
                                                                             'whenever field A is modified by user '
                                                                             'input or EML.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Only at midnight during background '
                                                                             'jobs.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Only when the system is uninstalled.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Once per year during tax filing.'}],
                                                  'prompt': 'When is a determination defined with `on modify { field '
                                                            'A; }` executed?',
                                                  'question_id': 'd83_q2'},
                                              {   'concept_slug': 'rap-determinations',
                                                  'explanation': '`IN LOCAL MODE` executes internal framework '
                                                                 'operations cleanly without authorization re-checks.',
                                                  'id': 'd83_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It bypasses external authorization '
                                                                             'checks and suppresses redundant trigger '
                                                                             'cascades within internal business '
                                                                             'logic.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It disconnects the server from the '
                                                                             'internet.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It translates ABAP into German.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It converts the database to SQLite.'}],
                                                  'prompt': 'What is the purpose of using the `IN LOCAL MODE` addition '
                                                            'in EML statements inside a behavior handler?',
                                                  'question_id': 'd83_q3'},
                                              {   'concept_slug': 'determination-triggers',
                                                  'explanation': '`on save` determinations run in `FINALIZE` before '
                                                                 'validation checks.',
                                                  'id': 'd83_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'FINALIZE stage'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'CLEANUP stage'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'ADJUST_NUMBERS stage'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'SAVE stage'}],
                                                  'prompt': 'In which stage of the RAP Save Sequence do determinations '
                                                            'defined with `on save` execute?',
                                                  'question_id': 'd83_q4'}],
                             'step_id': 'd83_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 83 Verification Assessment'},
                         {   'step_id': 'd83_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Declared RAP Determinations with precise trigger fields and timing (`on '
                                           'modify` vs `on save`).\n'
                                           '- Implemented determination logic in Local Handler Classes using EML `IN '
                                           'LOCAL MODE`.\n'
                                           '- Prevented performance bottlenecks and infinite recursion in derivation '
                                           'cascades.',
                             'title': 'Day 83 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd83_s8_completion',
                             'recommended_mission': {'slug': 'nova-rap-save-sequence-trace', 'title': 'RAP Save Sequence Execution Trace', 'description': 'Trace finalize, check_before_save, and adjust_numbers stages.'},
                             'step_type': 'completion',
                             'summary_md': 'Superb work! You know how to automate calculations. Tomorrow, you will '
                                           'master business validation and error messaging: **RAP Validations & State '
                                           'Messages**.',
                             'title': 'Day 83 Complete: RAP Determinations Mastered'}],
            'subtitle': 'Trigger operations, trigger fields, determine on modify vs on save, and implementation in '
                        'local handlers.',
            'title': 'RAP Determinations: on modify vs on save'},
    84: {   'atomic_concepts': ['rap-validations', 'failed-reported-structures'],
            'day_number': 84,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'rap-validations-error-handling',
            'steps': [   {   'content_md': '### Guarding Data Integrity\n'
                                           'A **Validation** is a business check executed automatically to ensure that '
                                           "an entity's data satisfies regulatory, accounting, or operational rules.\n"
                                           '\n'
                                           '#### Key Validation Principles:\n'
                                           '1. **Read-Only Operation**: A validation must **never** modify business '
                                           'data. It only inspects values and reports errors.\n'
                                           '2. **Execution Timing**:\n'
                                           '   - `validation validateDate on save { field DeliveryDate; }`\n'
                                           '   - Executes during the `CHECK_BEFORE_SAVE` stage.\n'
                                           '3. **The Twin Response Structures: `FAILED` and `REPORTED`**:\n'
                                           '   - **`failed`**: Tells the framework *which entity keys failed '
                                           'validation*. This triggers save abort.\n'
                                           '   - **`reported`**: Carries the *user-facing error message* (`T100` '
                                           'message text) displayed on the UI.',
                             'key_terms': [   {   'definition': 'Read-only business rule verification executing during '
                                                                'save or interaction to prevent corrupt states.',
                                                  'term': 'Validation'},
                                              {   'definition': 'Output table listing technical keys of entities that '
                                                                'violated business rules.',
                                                  'term': 'failed structure'},
                                              {   'definition': 'Output table containing user-facing T100 diagnostic '
                                                                'error messages.',
                                                  'term': 'reported structure'}],
                             'step_id': 'd84_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Validations inspect data without mutating it, reporting failures via the '
                                         '`failed` (abort trigger) and `reported` (messages) structures.',
                             'title': 'Business Validations in RAP'},
                         {   'content_md': '### Lifecycle of User Messages in Fiori Elements\n'
                                           'In modern Fiori Elements apps, error messages are classified into two '
                                           'architectural categories:\n'
                                           '\n'
                                           '#### 1. State Messages (Field-Bound)\n'
                                           '- Bound to a specific entity instance and field (e.g. "Order Quantity '
                                           'cannot be zero" bound to field `OrderQuantity`).\n'
                                           '- Displays an inline red border on the input field in the browser.\n'
                                           '- Persists until the user fixes the value and re-triggers validation.\n'
                                           '- Instantiated using `state_area` parameter in the message constructor.\n'
                                           '\n'
                                           '#### 2. Transition Messages (Global / Toast)\n'
                                           '- Unbound system notifications (e.g. "Network timeout occurred" or "Order '
                                           '4500001092 approved successfully").\n'
                                           '- Transient; disappears after navigation or timeout.\n'
                                           '\n'
                                           '#### Message Instantiation Syntax:\n'
                                           '```abap\n'
                                           'APPEND VALUE #(\n'
                                           '  %tky = <order>-%tky\n'
                                           '  %msg = new_message_with_text(\n'
                                           '    severity = if_abap_behv_message=>severity-error\n'
                                           "    text = 'Delivery date must be in the future' )\n"
                                           '  %element-deliverydate = if_abap_behv=>mk-on\n'
                                           ') TO reported-purchaseorder.\n'
                                           '```',
                             'key_terms': [   {   'definition': 'Field-bound error message that highlights the input '
                                                                'control until corrected.',
                                                  'term': 'State Message'},
                                              {   'definition': 'Transient notification toast displayed upon action '
                                                                'execution or global failure.',
                                                  'term': 'Transition Message'}],
                             'step_id': 'd84_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'State messages highlight invalid input fields until corrected; transition '
                                         'messages provide transient operational feedback.',
                             'title': 'State Messages vs Transition Messages'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'rule': 'If Plant = PL01 and Supplier is not certified, abort save '
                                                            'with E042(ZNOVA_MSG)',
                                                    'validation_name': 'validateSupplierCertification'},
                             'content_md': '### Validation Method Implementation\n'
                                           '```abap\n'
                                           'METHOD validateSupplierCertification.\n'
                                           '  READ ENTITIES OF ZI_NovaPOHeader IN LOCAL MODE\n'
                                           '    ENTITY PurchaseOrder\n'
                                           '    FIELDS ( Plant Supplier )\n'
                                           '    WITH CORRESPONDING #( keys )\n'
                                           '    RESULT DATA(lt_orders).\n'
                                           '\n'
                                           '  LOOP AT lt_orders ASSIGNING FIELD-SYMBOL(<po>).\n'
                                           "    IF <po>-Plant = 'PL01' AND <po>-Supplier <> 'VEND-101'.\n"
                                           '      // 1. Mark entity as failed (aborts save)\n'
                                           '      APPEND VALUE #( %tky = <po>-%tky ) TO failed-purchaseorder.\n'
                                           '\n'
                                           '      // 2. Report user-facing error message bound to Supplier field\n'
                                           '      APPEND VALUE #(\n'
                                           '        %tky = <po>-%tky\n'
                                           '        %msg = new_message(\n'
                                           "          id = 'ZNOVA_MSG'\n"
                                           "          number = '042'\n"
                                           '          severity = if_abap_behv_message=>severity-error\n'
                                           '          v1 = <po>-Supplier )\n'
                                           '        %element-supplier = if_abap_behv=>mk-on\n'
                                           '      ) TO reported-purchaseorder.\n'
                                           '    ENDIF.\n'
                                           '  ENDLOOP.\n'
                                           'ENDMETHOD.\n'
                                           '```',
                             'scenario': 'Nova enforces that components for assembly line PL01 can only be ordered '
                                         'from certified ISO-9001 vendors.',
                             'step_id': 'd84_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Plant Validation Implementation'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'A developer writes a validation that appends an error message to '
                                            '`reported`, but forgets to append the key to `failed`. What happens when '
                                            'the user clicks save?',
                             'options': [   {   'explanation': 'Correct! The save sequence checks `failed` to '
                                                               'determine whether to abort. Omitting `failed` allows '
                                                               'invalid records to commit.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'The document is saved and committed to the database anyway, '
                                                        'even though the error message is displayed on screen, because '
                                                        '`failed` was empty.'},
                                            {   'explanation': 'RAP relies strictly on the `failed` structure; '
                                                               'messages alone do not block persistence.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'The system automatically knows to abort.'},
                                            {   'explanation': 'Incorrect; it commits the invalid record.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'The database deletes all data.'}],
                             'step_id': 'd84_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Always populate both `failed` (to block persistence) and `reported` (to '
                                         'inform the user).',
                             'title': 'Validation Diagnostic Simulation: Forgetting the failed Structure'},
                         {   'instruction': 'Why is this an architectural violation?',
                             'options': [   {   'explanation': 'Correct! Validations verify states; Determinations '
                                                               'modify states. Mixing them corrupts the transactional '
                                                               'sequence.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Validations must be strictly read-only side-effect-free '
                                                        'checks. If data needs to be derived or auto-fixed, it belongs '
                                                        'in a Determination, never in a Validation.'},
                                            {   'explanation': 'Addresses can be updated, but not inside validation '
                                                               'methods.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Because address tables do not support updates.'},
                                            {   'explanation': 'Completely false.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Because ABAP does not allow modifying strings.'}],
                             'scenario': 'A legacy programmer attempts to write an `UPDATE` statement inside a RAP '
                                         'validation to auto-fix an invalid customer address.',
                             'step_id': 'd84_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Clean Code Challenge: Database Updates Inside Validations'},
                         {   'assessment_type': 'rap_challenge',
                             'questions': [   {   'concept_slug': 'rap-validations',
                                                  'explanation': 'Validations are read-only inspections; derivations '
                                                                 'belong in Determinations.',
                                                  'id': 'd84_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Validations must be strictly read-only '
                                                                             'and must never modify entity states or '
                                                                             'database tables.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Validations must delete all records.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Validations must execute COMMIT WORK.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Validations must modify at least 5 '
                                                                             'fields.'}],
                                                  'prompt': 'What is the strict architectural rule regarding data '
                                                            'modification inside a RAP Validation method?',
                                                  'question_id': 'd84_q1'},
                                              {   'concept_slug': 'failed-reported-structures',
                                                  'explanation': 'The `failed` structure triggers the transactional '
                                                                 'save abort.',
                                                  'id': 'd84_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'failed structure'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'reported structure'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'mapped structure'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'keys structure'}],
                                                  'prompt': 'In RAP error handling, which structure informs the '
                                                            'runtime engine that a save must be aborted due to a '
                                                            'business rule violation?',
                                                  'question_id': 'd84_q2'},
                                              {   'concept_slug': 'failed-reported-structures',
                                                  'explanation': 'Binding the element highlights the exact erroneous '
                                                                 'field on the frontend.',
                                                  'id': 'd84_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It binds the error message directly to '
                                                                             'the specific input field on the Fiori '
                                                                             'UI, highlighting it in red.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It turns off the computer monitor.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It hides the field from view.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It makes the field mandatory on the '
                                                                             'database.'}],
                                                  'prompt': 'What is the purpose of setting `%element-fieldname = '
                                                            'if_abap_behv=>mk-on` in the `reported` structure?',
                                                  'question_id': 'd84_q3'},
                                              {   'concept_slug': 'rap-validations',
                                                  'explanation': 'Validations execute in `CHECK_BEFORE_SAVE`.',
                                                  'id': 'd84_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'CHECK_BEFORE_SAVE stage'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'ADJUST_NUMBERS stage'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'SAVE stage'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'CLEANUP stage'}],
                                                  'prompt': 'During which stage of the RAP Save Sequence do '
                                                            'validations defined with `on save` execute?',
                                                  'question_id': 'd84_q4'}],
                             'step_id': 'd84_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 84 Verification Assessment'},
                         {   'step_id': 'd84_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Authored read-only RAP Validations protecting business invariants.\n'
                                           '- Coordinated the twin response structures (`failed` to abort, `reported` '
                                           'for T100 diagnostics).\n'
                                           '- Implemented field-bound State Messages for intuitive Fiori Elements '
                                           'error highlighting.',
                             'title': 'Day 84 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd84_s8_completion',
                             'recommended_mission': {'slug': 'nova-rap-determinations-validations', 'title': 'RAP Determinations & Validations Implementation', 'description': 'Enforce business validations and auto-determinations with state messages.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You know how to validate and protect data. Tomorrow, you will '
                                           'master custom business operations: **RAP Actions & Entity Manipulation '
                                           'Language (EML)**.',
                             'title': 'Day 84 Complete: RAP Validations Mastered'}],
            'subtitle': 'Validation triggers, failed and reported structures, transition messages, and state messages.',
            'title': 'RAP Validations & Message Handling'},
    85: {   'atomic_concepts': ['rap-actions', 'entity-manipulation-language-eml'],
            'day_number': 85,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'rap-actions-instance-static',
            'steps': [   {   'content_md': '### Extending Beyond Standard CRUD\n'
                                           'Standard CRUD (Create, Read, Update, Delete) is insufficient for '
                                           'enterprise business objects. Businesses execute distinct operational '
                                           'decisions: *Approve Purchase Order*, *Reject Invoice*, *Release Production '
                                           'Order*, *Copy Document*.\n'
                                           '\n'
                                           '#### Categories of RAP Actions:\n'
                                           '1. **Instance Actions**:\n'
                                           '   - Executed on a specific existing entity instance (e.g. `#approve` '
                                           'called on Purchase Order `4500001092`).\n'
                                           '   - Requires entity key; can alter status, send notifications, and return '
                                           'updated entity results.\n'
                                           '2. **Static Actions**:\n'
                                           '   - Executed at the entity level without referencing a specific instance '
                                           '(e.g. `calculateGlobalCurrencyRates`).\n'
                                           '3. **Factory Actions**:\n'
                                           '   - Creates and returns a new entity instance (e.g. '
                                           '`copyPurchaseOrder`).\n'
                                           '4. **Internal Actions**:\n'
                                           '   - Declared with keyword `internal`: callable only by other business '
                                           'logic inside the behavior pool, hidden from external OData consumers.',
                             'key_terms': [   {   'definition': 'Custom business operation executed on a specific '
                                                                'entity record.',
                                                  'term': 'Instance Action'},
                                              {   'definition': 'Specialized action that instantiates and returns a '
                                                                'new business entity.',
                                                  'term': 'Factory Action'},
                                              {   'definition': 'Action restricted to internal implementation methods, '
                                                                'shielded from API exposure.',
                                                  'term': 'Internal Action'}],
                             'step_id': 'd85_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'RAP Actions provide custom business operations (instance, static, factory) '
                                         'extending standard CRUD capabilities.',
                             'title': 'Custom Business Operations: RAP Actions'},
                         {   'content_md': '### Programmatic Control of RAP Entities\n'
                                           '**Entity Manipulation Language (EML)** is the native ABAP language '
                                           'extension for interacting with RAP business objects programmatically:\n'
                                           '\n'
                                           '#### Core EML Syntax:\n'
                                           '1. **`READ ENTITIES`**:\n'
                                           '   `READ ENTITIES OF ZI_NovaPOHeader ENTITY PurchaseOrder FIELDS ( Status '
                                           ') WITH keys RESULT lt_result.`\n'
                                           '2. **`MODIFY ENTITIES`**:\n'
                                           '   `MODIFY ENTITIES OF ZI_NovaPOHeader ENTITY PurchaseOrder EXECUTE '
                                           'approvePo FROM keys.`\n'
                                           '3. **`COMMIT ENTITIES`**:\n'
                                           '   Orchestrates the save sequence for programmatic EML modifications '
                                           'outside a Fiori UI context (e.g. in background jobs or test classes).\n'
                                           '\n'
                                           '#### Why EML Supersedes Direct SQL:\n'
                                           'EML guarantees that all determinations, validations, locks, and '
                                           'authorization checks are executed exactly as if a human user performed the '
                                           'action on a Fiori screen.',
                             'key_terms': [   {   'definition': 'Native ABAP syntax for consuming, modifying, and '
                                                                'executing actions on RAP business objects.',
                                                  'term': 'Entity Manipulation Language (EML)'},
                                              {   'definition': 'EML command executing the transactional save sequence '
                                                                'in non-UI environments.',
                                                  'term': 'COMMIT ENTITIES'}],
                             'step_id': 'd85_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'EML is the mandatory ABAP syntax for reading, updating, and executing '
                                         'actions on RAP entities with full business logic enforcement.',
                             'title': 'Entity Manipulation Language (EML) Mechanics'},
                         {   'company_context': {   'action_name': 'approvePurchaseOrder',
                                                    'bdef_syntax': 'action ( features : instance ) '
                                                                   'approvePurchaseOrder result [1] $self;',
                                                    'company_name': 'Nova Manufacturing Corp'},
                             'content_md': '### Action Implementation in Behavior Pool\n'
                                           '```abap\n'
                                           'METHOD approvePurchaseOrder.\n'
                                           '  // 1. Read current order status via EML\n'
                                           '  READ ENTITIES OF ZI_NovaPOHeader IN LOCAL MODE\n'
                                           '    ENTITY PurchaseOrder\n'
                                           '    FIELDS ( ApprovalStatus )\n'
                                           '    WITH CORRESPONDING #( keys )\n'
                                           '    RESULT DATA(lt_orders).\n'
                                           '\n'
                                           "  // 2. Modify status to 'APPROVED'\n"
                                           '  MODIFY ENTITIES OF ZI_NovaPOHeader IN LOCAL MODE\n'
                                           '    ENTITY PurchaseOrder\n'
                                           '    UPDATE FIELDS ( ApprovalStatus )\n'
                                           '    WITH VALUE #( FOR order IN lt_orders (\n'
                                           '      %tky = order-%tky\n'
                                           "      ApprovalStatus = 'APPROVED'\n"
                                           '    ) ).\n'
                                           '\n'
                                           '  // 3. Return updated instance to refresh Fiori screen\n'
                                           '  READ ENTITIES OF ZI_NovaPOHeader IN LOCAL MODE\n'
                                           '    ENTITY PurchaseOrder\n'
                                           '    ALL FIELDS WITH CORRESPONDING #( keys )\n'
                                           '    RESULT DATA(lt_updated).\n'
                                           '\n'
                                           '  result = VALUE #( FOR updated IN lt_updated (\n'
                                           '    %tky = updated-%tky\n'
                                           '    %param = updated\n'
                                           '  ) ).\n'
                                           'ENDMETHOD.\n'
                                           '```',
                             'scenario': 'Nova defines an instance action `approvePurchaseOrder` in Heidelberg that '
                                         'verifies buyer budget and sets status to APPROVED.',
                             'step_id': 'd85_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Approve Purchase Order Action'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'Write an EML statement to execute the custom action `releaseOrder` across '
                                            'a list of 50 production orders.',
                             'options': [   {   'explanation': 'Correct! EML supports set-based execution of actions '
                                                               'across collections of keys in a single call.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': '`MODIFY ENTITIES OF ZI_MfgOrder ENTITY MfgOrder EXECUTE '
                                                        'releaseOrder FROM CORRESPONDING #( lt_keys ) FAILED '
                                                        'DATA(lt_failed) REPORTED DATA(lt_reported).`'},
                                            {   'explanation': 'Direct SQL bypasses all release validations, capacity '
                                                               'checks, and audit trails.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': "Execute `UPDATE zmfgorder SET status = 'RELEASED' WHERE id IN "
                                                        '(...)`.'},
                                            {   'explanation': 'Obsolete legacy technology that fails in ABAP Cloud.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Call transaction CO02 using batch input screen recording.'}],
                             'step_id': 'd85_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Execute batch actions via EML `MODIFY ENTITIES ... EXECUTE action_name FROM '
                                         'keys`.',
                             'title': 'EML Operation Simulation: Programmatic Batch Updates'},
                         {   'instruction': 'How is this implemented in RAP?',
                             'options': [   {   'explanation': 'Correct! Instance feature control '
                                                               '(`get_instance_features`) dynamically enables or '
                                                               'disables actions and fields based on entity state.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Declare `action ( features : instance ) approvePurchaseOrder` '
                                                        'in the BDEF, and implement the `get_instance_features` method '
                                                        'in the Local Handler Class to set '
                                                        '`%action-approvePurchaseOrder = if_abap_behv=>fc-o-disabled` '
                                                        'when status is not PENDING.'},
                                            {   'explanation': 'Violates Fiori Elements architecture and bypasses '
                                                               'backend authorization.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Write custom JavaScript in the browser to hide the button.'},
                                            {   'explanation': 'Completely absurd.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': "Delete the user's login account when they click approve "
                                                        'twice.'}],
                             'scenario': "The 'Approve' button in the Fiori UI must be dynamically disabled (greyed "
                                         'out) if the purchase order has already been approved or rejected.',
                             'step_id': 'd85_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Action Design Challenge: Dynamic Feature Control'},
                         {   'assessment_type': 'rap_challenge',
                             'questions': [   {   'concept_slug': 'rap-actions',
                                                  'explanation': 'Instance actions operate on a specific existing '
                                                                 'entity key.',
                                                  'id': 'd85_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Instance Action'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Static Action'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Database Action'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Operating System Action'}],
                                                  'prompt': 'What type of RAP Action is executed on a specific '
                                                            'existing entity instance (such as approving an existing '
                                                            'purchase order)?',
                                                  'question_id': 'd85_q1'},
                                              {   'concept_slug': 'entity-manipulation-language-eml',
                                                  'explanation': 'EML provides native ABAP syntax for consuming RAP '
                                                                 'entities.',
                                                  'id': 'd85_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Native ABAP language extension for '
                                                                             'reading, modifying, and triggering '
                                                                             'actions on RAP business objects with '
                                                                             'full business logic.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'An email formatting script.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'A 3D modeling language.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'A video codec.'}],
                                                  'prompt': 'What is Entity Manipulation Language (EML) in the ABAP '
                                                            'environment?',
                                                  'question_id': 'd85_q2'},
                                              {   'concept_slug': 'rap-actions',
                                                  'explanation': '`get_instance_features` evaluates instance state to '
                                                                 'govern action availability.',
                                                  'id': 'd85_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'get_instance_features'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'onInit'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'check_password'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'cleanup'}],
                                                  'prompt': 'Which method in the Local Handler Class dynamically '
                                                            'enables or disables action buttons (feature control) '
                                                            "based on the record's current status?",
                                                  'question_id': 'd85_q3'},
                                              {   'concept_slug': 'entity-manipulation-language-eml',
                                                  'explanation': '`COMMIT ENTITIES` orchestrates the save sequence for '
                                                                 'EML operations.',
                                                  'id': 'd85_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'COMMIT ENTITIES'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'COMMIT WORK'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'SAVE TO DISK'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'WRITE MEMORY'}],
                                                  'prompt': 'Which EML statement is used in non-UI environments (such '
                                                            'as background jobs or console classes) to trigger the '
                                                            'transactional save sequence?',
                                                  'question_id': 'd85_q4'}],
                             'step_id': 'd85_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 85 Verification Assessment'},
                         {   'step_id': 'd85_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Authored custom RAP Instance and Factory Actions.\n'
                                           '- Manipulated RAP business objects programmatically using Entity '
                                           'Manipulation Language (EML).\n'
                                           '- Implemented dynamic instance feature control (`get_instance_features`) '
                                           'to govern UI button states.',
                             'title': 'Day 85 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd85_s8_completion',
                             'recommended_mission': {'slug': 'nova-rap-custom-actions-eml', 'title': 'RAP Custom Actions & EML Operations', 'description': 'Implement custom business action invoked via EML MODIFY ENTITY.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You know how to implement custom business logic. Tomorrow, '
                                           'you will master the technology that enables enterprise autosaving: **RAP '
                                           'Draft Handling**.',
                             'title': 'Day 85 Complete: RAP Actions & EML Mastered'}],
            'subtitle': 'Instance vs static actions, factory actions, and calling RAP entities programmatically via '
                        'EML.',
            'title': 'RAP Actions: Instance, Static & Factory'},
    86: {   'atomic_concepts': ['rap-draft-handling', 'draft-activation-lifecycle'],
            'day_number': 86,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'rap-draft-handling',
            'steps': [   {   'content_md': '### Eliminating User Data Loss\n'
                                           'In legacy SAP GUI applications, if a user spent 45 minutes entering a '
                                           '200-line sales order and their network connection dropped, all data was '
                                           'permanently lost. Furthermore, long-running exclusive database locks '
                                           '(`ENQUEUE`) blocked other users.\n'
                                           '\n'
                                           '#### How RAP Draft Handling Solves This:\n'
                                           '1. **Dual-Table Architecture**:\n'
                                           '   - **Active Table (`znova_po_h`)**: Stores finalized, committed business '
                                           'documents.\n'
                                           '   - **Draft Table (`znova_po_h_d`)**: Automatically generated shadow '
                                           'table storing incomplete, unvalidated user edits.\n'
                                           '2. **Seamless Autosave**:\n'
                                           '   - Every keystroke and field modification is saved to the draft table '
                                           'automatically in the background.\n'
                                           '3. **Cross-Device Continuity**:\n'
                                           '   - A buyer can start a draft on their office desktop in Heidelberg, walk '
                                           'onto the shop floor, and resume editing the exact same draft on their '
                                           'mobile tablet.',
                             'key_terms': [   {   'definition': 'Shadow database table buffering work-in-progress '
                                                                'modifications without affecting active records.',
                                                  'term': 'Draft Table'},
                                              {   'definition': 'Production database table holding committed, '
                                                                'validated business data.',
                                                  'term': 'Active Table'},
                                              {   'definition': 'BDEF keyword activating automatic draft '
                                                                'infrastructure and actions.',
                                                  'term': 'Draft Enablement (`with draft`)'}],
                             'step_id': 'd86_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Draft handling uses shadow tables to autosave incomplete work-in-progress, '
                                         'eliminating user data loss and long-running locks.',
                             'title': 'The Draft Paradigm: Consumer-Grade Autosave'},
                         {   'content_md': '### The Draft Lifecycle\n'
                                           'Enabling `with draft` in a BDEF automatically equips the business object '
                                           'with four standardized draft actions:\n'
                                           '\n'
                                           '```\n'
                                           '[Active Record] ──(Edit Action)──► [Draft Created] ──(User Edits / '
                                           'Autosave)──► [Draft Updated]\n'
                                           '                                         │\n'
                                           '                 ┌───────────────────────┴───────────────────────┐\n'
                                           '                 ▼                                               ▼\n'
                                           '          (Activate Action)                              (Discard Action)\n'
                                           '                 │                                               │\n'
                                           '   [Validations Pass -> Active Updated]                [Draft Table Record '
                                           'Deleted]\n'
                                           '```\n'
                                           '\n'
                                           '1. **`Edit`**: Copies active record to draft table and marks draft as '
                                           'locked by current user.\n'
                                           '2. **`Activate`**: Triggers full validations. If valid, copies draft data '
                                           'to active table and deletes the draft record.\n'
                                           '3. **`Discard`**: Cancels editing and deletes the draft record, leaving '
                                           'the active record untouched.\n'
                                           '4. **`Resume`**: Allows the lock owner to resume editing an existing '
                                           'draft.',
                             'key_terms': [   {   'definition': 'Standard draft action promoting valid draft data into '
                                                                'active persistence.',
                                                  'term': 'Activate Action'},
                                              {   'definition': 'Standard draft action deleting work-in-progress '
                                                                'drafts without modifying active data.',
                                                  'term': 'Discard Action'},
                                              {   'definition': 'Timestamp field on active table detecting concurrent '
                                                                'changes while a draft was open.',
                                                  'term': 'Total ETag'}],
                             'step_id': 'd86_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Standard draft actions (Edit, Activate, Discard, Resume) govern the '
                                         'transition between active and draft tables.',
                             'title': 'The Draft Activation Lifecycle & Built-In Draft Actions'},
                         {   'company_context': {   'active_table': 'znova_po_h',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'draft_table': 'znova_po_h_d',
                                                    'total_etag': 'last_changed_at'},
                             'content_md': '### Draft BDEF Syntax\n'
                                           '```abap\n'
                                           'managed implementation in class zbp_i_novapoheader unique;\n'
                                           'strict(2);\n'
                                           'with draft;\n'
                                           '\n'
                                           'define behavior for ZI_NovaPOHeader alias PurchaseOrder\n'
                                           'persistent table znova_po_h\n'
                                           'draft table znova_po_h_d\n'
                                           'lock master total etag LastChangedAt\n'
                                           'etag master LocalLastChangedAt\n'
                                           '{\n'
                                           '  create; update; delete;\n'
                                           '  draft action Edit;\n'
                                           '  draft action Activate;\n'
                                           '  draft action Discard;\n'
                                           '  draft action Resume;\n'
                                           '  draft determine action Prepare;\n'
                                           '\n'
                                           '  association _Items { create; with draft; }\n'
                                           '}\n'
                                           '```',
                             'scenario': 'Nova draft-enables the Purchase Order business object to support '
                                         'multi-device mobile procurement in Heidelberg.',
                             'step_id': 'd86_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Purchase Order Draft BDEF'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "A user clicks 'Save' (Activate) on a draft purchase order, but a "
                                            'mandatory delivery date is missing. What does the draft framework do?',
                             'options': [   {   'explanation': 'Correct! Draft activation only promotes data if '
                                                               'validations pass. If validations fail, the draft is '
                                                               'preserved so the user can fix it.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Activation fails: the draft record remains safely preserved '
                                                        'in the draft table, the active table remains unmodified, and '
                                                        'the user sees the field error message.'},
                                            {   'explanation': 'Deleting drafts on validation failure would destroy '
                                                               'the entire purpose of draft handling.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'The draft is deleted and all user inputs are lost.'},
                                            {   'explanation': 'The framework does not fabricate business dates.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': "The invalid date is replaced with yesterday's date "
                                                        'automatically.'}],
                             'step_id': 'd86_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Failed activation preserves the draft in the draft table, allowing the user '
                                         'to correct errors without losing work.',
                             'title': 'Draft Lifecycle Simulation: Handling Validation Failures During Activation'},
                         {   'instruction': "How does the Total ETag protect against overwriting User B's changes?",
                             'options': [   {   'explanation': 'Correct! Total ETag protects active records from stale '
                                                               'draft overwrites (optimistic concurrency control).',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'The Total ETag comparison detects that the active record was '
                                                        'modified after User A opened their draft. Activation is '
                                                        'rejected with HTTP 412 (Precondition Failed), preventing User '
                                                        "A from silently overwriting User B's changes."},
                                            {   'explanation': 'Silent overwrites cause severe data loss and violate '
                                                               'ACID principles.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': "User A silently overwrites User B's changes without warning."},
                                            {   'explanation': 'Completely false.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Both orders are combined into a random third order.'}],
                             'scenario': 'User A opens a draft on Purchase Order 100. While User A is editing, User B '
                                         'modifies and commits an emergency change directly to the active record. User '
                                         'A now clicks Activate.',
                             'step_id': 'd86_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Concurrency Challenge: Total ETag Conflict on Activation'},
                         {   'assessment_type': 'rap_challenge',
                             'questions': [   {   'concept_slug': 'rap-draft-handling',
                                                  'explanation': 'Draft handling buffers uncommitted work in shadow '
                                                                 'tables with autosave capabilities.',
                                                  'id': 'd86_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To provide automatic background '
                                                                             'autosaving into shadow draft tables, '
                                                                             'eliminating user data loss and '
                                                                             'long-running locks.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To print physical drafts on paper '
                                                                             'printers.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To turn on air conditioning in the '
                                                                             'office.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To disable database security checks.'}],
                                                  'prompt': 'What is the primary architectural purpose of enabling '
                                                            'Draft Handling (`with draft`) in a RAP business object?',
                                                  'question_id': 'd86_q1'},
                                              {   'concept_slug': 'draft-activation-lifecycle',
                                                  'explanation': 'The `Activate` action promotes draft data to active '
                                                                 'tables.',
                                                  'id': 'd86_q2',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'Activate'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'Discard'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'Resume'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'Edit'}],
                                                  'prompt': 'Which standard draft action copies validated draft data '
                                                            'into the active persistent table and clears the draft '
                                                            'record?',
                                                  'question_id': 'd86_q2'},
                                              {   'concept_slug': 'draft-activation-lifecycle',
                                                  'explanation': '`Discard` clears temporary work-in-progress without '
                                                                 'altering active data.',
                                                  'id': 'd86_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'The draft record in the draft table is '
                                                                             'deleted, leaving the active production '
                                                                             'record untouched.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'The active production record is '
                                                                             'permanently deleted.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'The entire system reboots.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': "The user's password expires."}],
                                                  'prompt': "What happens when a user clicks the standard 'Discard' "
                                                            'draft action?',
                                                  'question_id': 'd86_q3'},
                                              {   'concept_slug': 'rap-draft-handling',
                                                  'explanation': 'Total ETag protects against concurrent active '
                                                                 'updates while drafts are being edited.',
                                                  'id': 'd86_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It detects whether the active record was '
                                                                             'modified by another transaction while a '
                                                                             'draft was open, preventing stale '
                                                                             'overwrites.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It counts the total number of lines of '
                                                                             'code.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It calculates invoice tax totals.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It encrypts network packets.'}],
                                                  'prompt': 'What is the role of the `total etag` declaration on the '
                                                            'lock master in a draft-enabled BDEF?',
                                                  'question_id': 'd86_q4'}],
                             'step_id': 'd86_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 86 Verification Assessment'},
                         {   'step_id': 'd86_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Architected dual-table draft persistence (Active table vs Draft table).\n'
                                           '- Implemented standard draft lifecycle actions (Edit, Activate, Discard, '
                                           'Resume).\n'
                                           '- Applied Total ETags to guarantee optimistic concurrency control during '
                                           'draft activation.',
                             'title': 'Day 86 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd86_s8_completion',
                             'recommended_mission': {'slug': 'nova-rap-draft-handling-setup', 'title': 'Draft Handling & Auto-Save Configuration', 'description': 'Configure draft table and optimistic locking on RAP business object.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You know how to implement enterprise autosaving. Tomorrow, '
                                           'you will master concurrency and locking: **Optimistic Locking via ETags & '
                                           'Pessimistic Locks**.',
                             'title': 'Day 86 Complete: RAP Draft Handling Mastered'}],
            'subtitle': 'Active tables vs draft tables, draft administrative data, draft actions (Edit, Activate, '
                        'Discard), and total ETags.',
            'title': 'Draft Handling in RAP'},
    87: {   'atomic_concepts': ['rap-concurrency-control', 'optimistic-locking-etag'],
            'day_number': 87,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'rap-concurrency-etags',
            'steps': [   {   'content_md': '### Preventing Conflicting Concurrent Updates\n'
                                           'In high-volume enterprise systems, multiple users or APIs frequently '
                                           'attempt to modify the same document simultaneously.\n'
                                           '\n'
                                           '#### The Two Concurrency Strategies:\n'
                                           '1. **Optimistic Locking (ETag-Based - Standard for Web & OData)**:\n'
                                           '   - Records are **not locked** while a user is viewing or editing them.\n'
                                           '   - Instead, the entity maintains an **Entity Tag (ETag)** timestamp or '
                                           'hash (e.g. `LocalLastChangedAt`).\n'
                                           '   - When updating, the client sends the ETag in the HTTP header: '
                                           '`If-Match: "20260917101500"`.\n'
                                           '   - The server compares ETags. If matching, the update commits and '
                                           'updates the timestamp. If mismatched, the server rejects the update with '
                                           '**HTTP 412 (Precondition Failed)**.\n'
                                           '2. **Pessimistic Locking (Enqueue-Based)**:\n'
                                           '   - The first user acquires an exclusive lock via standard SAP lock '
                                           'objects (`ENQUEUE`).\n'
                                           '   - Other users are blocked immediately from entering edit mode until the '
                                           'lock is released.',
                             'key_terms': [   {   'definition': 'Concurrency model verifying that data was not '
                                                                'modified between read and write using ETags.',
                                                  'term': 'Optimistic Locking'},
                                              {   'definition': 'Timestamp or hash field tracking the latest '
                                                                'modification of an entity instance.',
                                                  'term': 'ETag (Entity Tag)'},
                                              {   'definition': 'OData error response indicating an ETag mismatch '
                                                                'caused by concurrent modification.',
                                                  'term': 'HTTP 412 Precondition Failed'}],
                             'step_id': 'd87_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Optimistic locking uses ETags (If-Match headers) to detect concurrent '
                                         'modifications without holding long-lived database locks.',
                             'title': 'Concurrency Control: Optimistic vs Pessimistic Locking'},
                         {   'content_md': '### Local ETag vs Total ETag\n'
                                           'RAP differentiates between instance-level change tracking and cross-draft '
                                           'change tracking:\n'
                                           '\n'
                                           '1. **`etag master <field>` (Local ETag)**:\n'
                                           '   - Declared on each entity (root or child).\n'
                                           '   - Typically bound to a high-precision UTC timestamp: '
                                           '`locallastchangedat`.\n'
                                           "   - Evaluated during direct updates: compares the client's `If-Match` "
                                           'header against the current instance value.\n'
                                           '2. **`total etag <field>` (Total ETag)**:\n'
                                           '   - Declared on the `lock master` (root entity).\n'
                                           '   - Typically bound to `lastchangedat`.\n'
                                           '   - Evaluated during draft activation: detects if the active record was '
                                           'modified by another process while a draft was open.',
                             'key_terms': [   {   'definition': 'BDEF keyword declaring the local ETag field for '
                                                                'instance-level concurrency checks.',
                                                  'term': 'etag master'},
                                              {   'definition': 'BDEF keyword declaring the root-level timestamp '
                                                                'protecting draft activation.',
                                                  'term': 'total etag'}],
                             'step_id': 'd87_s2_understand',
                             'step_type': 'understand',
                             'takeaway': '`etag master` governs individual entity instance updates; `total etag` '
                                         'protects draft activation.',
                             'title': 'Configuring Local ETag vs Total ETag in BDEF'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'initial_etag': '2026-09-17T09:00:00Z',
                                                    'user_a_action': 'Updates delivery date -> ETag advances to '
                                                                     '09:02:15Z (COMMITTED)',
                                                    'user_b_action': 'Submits update using stale ETag 09:00:00Z -> '
                                                                     'HTTP 412 Rejected'},
                             'content_md': '### Concurrency Timeline\n'
                                           '```\n'
                                           '[Time 09:00] User A and User B both read PO 4500001092. ETag = '
                                           "'09:00:00Z'.\n"
                                           '[Time 09:02] User A clicks Save.\n'
                                           "             - Header: If-Match: '09:00:00Z'\n"
                                           '             - Server check: ETag matches! Commit successful.\n'
                                           "             - New server ETag updated to '09:02:15Z'.\n"
                                           '[Time 09:03] User B clicks Save.\n'
                                           "             - Header: If-Match: '09:00:00Z' (Stale ETag)\n"
                                           "             - Server check: '09:00:00Z' <> '09:02:15Z' -> MISMATCH!\n"
                                           '             - Server returns: HTTP 412 Precondition Failed.\n'
                                           "             - Fiori UI prompts User B: 'Record was modified by another "
                                           "user. Reload to see latest data.'\n"
                                           '```',
                             'scenario': 'Two procurement clerks in Heidelberg attempt to update Purchase Order '
                                         '4500001092 simultaneously.',
                             'step_id': 'd87_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Optimistic Concurrency Collision Scenario: Heidelberg (PL01)'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'An automated integration interface in Austin encounters HTTP 412 when '
                                            'submitting goods receipt updates. How should the API client handle this?',
                             'options': [   {   'explanation': 'Correct! Standard optimistic retry logic: re-read '
                                                               'fresh ETag, verify business consistency, and '
                                                               're-submit.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Catch HTTP 412, re-read the latest entity record to obtain '
                                                        'the new ETag and updated data state, re-apply the business '
                                                        'delta, and submit with the fresh ETag.'},
                                            {   'explanation': 'Using wildcard `*` bypasses concurrency protection, '
                                                               'causing data loss.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Submit the request with `If-Match: *` to forcibly overwrite '
                                                        "all other users' changes."},
                                            {   'explanation': 'Unacceptable; APIs must implement resilient retry '
                                                               'logic.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Crash the application and stop ordering goods.'}],
                             'step_id': 'd87_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Handle HTTP 412 by re-fetching the latest record and ETag, evaluating '
                                         'differences, and retrying.',
                             'title': 'Troubleshooting Simulation: Resolving HTTP 412 Precondition Failed'},
                         {   'instruction': 'What is the architectural remediation?',
                             'options': [   {   'explanation': 'Correct! Declaring an explicit ETag master enables '
                                                               'automatic framework-managed optimistic locking.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Add a UTC timestamp field (`LocalLastChangedAt`) to the '
                                                        'database table with annotation '
                                                        '`@Semantics.systemDateTime.localInstanceLastChangedAt: true`, '
                                                        'and declare `etag master LocalLastChangedAt` in the BDEF.'},
                                            {   'explanation': 'Completely absurd in an enterprise environment.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Tell users only one person can work in the company per hour.'},
                                            {   'explanation': 'Destructive and irrelevant.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Delete the database table.'}],
                             'scenario': 'A developer omits `etag master` from a high-frequency transactional BDEF, '
                                         'allowing concurrent updates to silently overwrite each other.',
                             'step_id': 'd87_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Concurrency Challenge: Missing ETag Declaration in BDEF'},
                         {   'assessment_type': 'troubleshooting',
                             'questions': [   {   'concept_slug': 'rap-concurrency-control',
                                                  'explanation': "HTTP 412 indicates that the client's ETag in the "
                                                                 "`If-Match` header does not match the server's "
                                                                 'current version.',
                                                  'id': 'd87_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'HTTP 412 Precondition Failed'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'HTTP 200 OK'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'HTTP 404 Not Found'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'HTTP 502 Bad Gateway'}],
                                                  'prompt': 'Which HTTP status code is returned by an OData service '
                                                            'when an update is rejected due to an ETag concurrency '
                                                            'mismatch?',
                                                  'question_id': 'd87_q1'},
                                              {   'concept_slug': 'optimistic-locking-etag',
                                                  'explanation': 'Optimistic locking avoids holding open lock table '
                                                                 'entries during idle user browsing.',
                                                  'id': 'd87_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It does not hold exclusive database '
                                                                             'locks while users browse screens, '
                                                                             'maximizing system scalability.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It eliminates the need for user '
                                                                             'passwords.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It guarantees that no data is ever '
                                                                             'written to the database.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It allows unauthenticated users to '
                                                                             'modify data.'}],
                                                  'prompt': 'What is the primary operational benefit of optimistic '
                                                            'locking over pessimistic locking in web applications?',
                                                  'question_id': 'd87_q2'},
                                              {   'concept_slug': 'optimistic-locking-etag',
                                                  'explanation': '`etag master` declares the optimistic concurrency '
                                                                 'timestamp field.',
                                                  'id': 'd87_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'etag master <field_name>'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'lock exclusive <field_name>'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'freeze table <field_name>'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'version code <field_name>'}],
                                                  'prompt': 'Which BDEF clause designates the field used for '
                                                            'instance-level optimistic locking checks?',
                                                  'question_id': 'd87_q3'},
                                              {   'concept_slug': 'rap-concurrency-control',
                                                  'explanation': 'Re-fetching fresh data and ETag allows safe '
                                                                 'reconciliation and re-submission.',
                                                  'id': 'd87_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Re-read the latest entity data and ETag '
                                                                             'from the server, verify business '
                                                                             'consistency, and re-submit.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Delete the database.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Resubmit the same stale request in a '
                                                                             'tight infinite loop.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Disconnect the server power cord.'}],
                                                  'prompt': 'How should an automated client interface recover when '
                                                            'receiving an HTTP 412 error?',
                                                  'question_id': 'd87_q4'}],
                             'step_id': 'd87_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 87 Verification Assessment'},
                         {   'step_id': 'd87_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered optimistic concurrency control using ETags and `If-Match` '
                                           'headers.\n'
                                           '- Differentiated `etag master` (instance updates) from `total etag` (draft '
                                           'activation).\n'
                                           '- Diagnosed and resolved HTTP 412 Precondition Failed collisions.',
                             'title': 'Day 87 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd87_s8_completion',
                             'recommended_mission': {'slug': 'nova-rap-etag-concurrency-control', 'title': 'ETag Optimistic Concurrency Control', 'description': 'Validate total ETag checks preventing lost updates during editing.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You understand concurrency control. Tomorrow, you will master '
                                           'document numbering and security: **Numbering Strategies & Authorization '
                                           'Control**.',
                             'title': 'Day 87 Complete: Concurrency & Locking Mastered'}],
            'subtitle': 'Optimistic locking via ETags (`etag master`), pessimistic enqueue locking, and resolving 412 '
                        'Precondition Failed.',
            'title': 'Concurrency Control & Optimistic Locking'},
    88: {   'atomic_concepts': ['rap-numbering-strategies', 'rap-authorization-control'],
            'day_number': 88,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'rap-numbering-authorization',
            'steps': [   {   'content_md': '### Assigning Enterprise Primary Keys\n'
                                           'Every business record requires an unambiguous primary key. RAP provides '
                                           'two distinct architectural strategies:\n'
                                           '\n'
                                           '#### 1. Early Numbering:\n'
                                           '- Key is generated **immediately upon record creation** during the '
                                           'interaction phase.\n'
                                           '- **Managed Numbering (`numbering : managed`)**: The framework '
                                           'automatically generates 16-byte raw UUIDs (`sysuuid_x16`).\n'
                                           '  - *Best for*: Internal technical keys, draft-enabled entities, '
                                           'multi-user parallel editing.\n'
                                           '\n'
                                           '#### 2. Late Numbering:\n'
                                           '- Key is assigned **at the very end of the save phase** in the '
                                           '`ADJUST_NUMBERS` stage.\n'
                                           '- Uses traditional sequential **SAP Number Range Objects** (e.g. Purchase '
                                           'Order `4500001092`).\n'
                                           '  - *Best for*: Legal, human-readable, gap-free document identifiers (Tax '
                                           'Invoices, Purchase Orders).\n'
                                           '  - *Benefit*: Zero wasted numbers if a user cancels creation midway.',
                             'key_terms': [   {   'definition': 'Key assignment occurring immediately at creation '
                                                                '(e.g. framework-managed UUIDs).',
                                                  'term': 'Early Numbering'},
                                              {   'definition': 'Key assignment occurring in the adjust_numbers stage '
                                                                'of the save phase from number ranges.',
                                                  'term': 'Late Numbering'},
                                              {   'definition': 'Standard SAP database sequence generator providing '
                                                                'gap-free legal numbering.',
                                                  'term': 'Number Range Object'}],
                             'step_id': 'd88_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Use Early Numbering (UUIDs) for technical keys and draft support; use Late '
                                         'Numbering for legal, gap-free human-readable document IDs.',
                             'title': 'Numbering Strategies in RAP: Early vs Late'},
                         {   'content_md': '### Security Governance in RAP\n'
                                           'RAP enforces two tiers of authorization checks declared in the BDEF:\n'
                                           '\n'
                                           '#### 1. Global Authorization (`authorization : global`)\n'
                                           '- Evaluated **before any specific instance is accessed or created**.\n'
                                           '- Checks generic operational permissions based on user PFCG roles.\n'
                                           '- *Example*: Does user Marcus have permission to create purchase orders '
                                           'for Company Code `NM01`?\n'
                                           '- Implemented in `get_global_authorizations`.\n'
                                           '\n'
                                           '#### 2. Instance Authorization (`authorization : instance`)\n'
                                           '- Evaluated on **a specific existing record based on its current data '
                                           'attributes**.\n'
                                           '- *Example*: Can user Marcus approve Purchase Order 4500001092 with total '
                                           'amount exceeding $100,000 in Plant `PL01`?\n'
                                           '- Implemented in `get_instance_authorizations`.\n'
                                           '- If denied, specific operations (Update, Delete, Custom Actions) are '
                                           'blocked.',
                             'key_terms': [   {   'definition': 'Check evaluating generic operational permissions '
                                                                'before instance creation or access.',
                                                  'term': 'Global Authorization'},
                                              {   'definition': 'Check evaluating field-dependent permissions on a '
                                                                'specific business object instance.',
                                                  'term': 'Instance Authorization'}],
                             'step_id': 'd88_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Global authorization checks generic create/access permissions; Instance '
                                         'authorization checks record-specific field attributes.',
                             'title': 'Authorization Control: Global vs Instance Authorization'},
                         {   'company_context': {   'auth_rule': 'Users can only edit orders for their assigned Plant '
                                                                 'in PFCG object M_BEST_WRK',
                                                    'business_key': 'PurchaseOrderNumber (Late Numbering via '
                                                                    'ADJUST_NUMBERS)',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'technical_key': 'POUUID (Early Managed UUID)'},
                             'content_md': '### BDEF Syntax\n'
                                           '```abap\n'
                                           'managed implementation in class zbp_i_novapoheader unique;\n'
                                           'strict(2);\n'
                                           '\n'
                                           'define behavior for ZI_NovaPOHeader alias PurchaseOrder\n'
                                           'persistent table znova_po_h\n'
                                           'lock master\n'
                                           'authorization master ( global, instance )\n'
                                           'late numbering\n'
                                           '{\n'
                                           '  field ( readonly, numbering : managed ) POUUID;\n'
                                           '  field ( readonly ) PurchaseOrderNumber;\n'
                                           '\n'
                                           '  create; update; delete;\n'
                                           '}\n'
                                           '```',
                             'scenario': 'Nova combines managed UUID technical keys with late legal numbering and '
                                         'plant-level instance authorization.',
                             'step_id': 'd88_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Dual-Numbering & Authorization Architecture'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'Buyer Marcus Vance (assigned to Plant PL01) attempts to edit a purchase '
                                            'order created in Plant PL02. Where and how does RAP block this?',
                             'options': [   {   'explanation': "Correct! Instance authorization inspects the record's "
                                                               'Plant value and denies update permissions.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Inside `get_instance_authorizations`: the method checks '
                                                        "`AUTHORITY-CHECK OBJECT 'M_BEST_WRK' FIELD 'WERKS' VALUE "
                                                        '<po>-Plant`. Authorization fails, setting `%update = '
                                                        'if_abap_behv=>auth-unauthorized`.'},
                                            {   'explanation': 'Security checks block access; they never delete '
                                                               'business records.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'By deleting the purchase order from the database.'},
                                            {   'explanation': 'Violates corporate security and compliance rules.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'By letting Marcus edit the order and sending an apology '
                                                        'email.'}],
                             'step_id': 'd88_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Implement instance security in `get_instance_authorizations` using standard '
                                         '`AUTHORITY-CHECK`.',
                             'title': 'Authorization Simulation: Enforcing Plant-Level Instance Security'},
                         {   'instruction': 'How should this EML update be executed?',
                             'options': [   {   'explanation': 'Correct! `IN LOCAL MODE` is specifically designed for '
                                                               'internal framework and background operations.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Execute the EML statement with the `IN LOCAL MODE` addition: '
                                                        '`MODIFY ENTITIES OF ZI_NovaPOHeader IN LOCAL MODE ...`. This '
                                                        'signals to the framework that the call is internal and '
                                                        'bypasses user-facing authorization checks.'},
                                            {   'explanation': 'Granting SAP_ALL violates the principle of least '
                                                               'privilege and fails security audits.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Give the background job temporary SAP_ALL administrative '
                                                        'superuser privileges.'},
                                            {   'explanation': 'Catastrophic security violation.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Disable authorization checks globally across the entire SAP '
                                                        'system.'}],
                             'scenario': 'A background automated system process needs to update purchase order status '
                                         'without being blocked by interactive user authorization checks.',
                             'step_id': 'd88_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Security Architecture Challenge: Bypassing Authorization in Internal Methods'},
                         {   'assessment_type': 'rap_challenge',
                             'questions': [   {   'concept_slug': 'rap-numbering-strategies',
                                                  'explanation': 'Late Numbering prevents number gaps by drawing '
                                                                 'numbers strictly after validations pass.',
                                                  'id': 'd88_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It draws sequential numbers from number '
                                                                             'ranges at the very end of the save '
                                                                             'phase, guaranteeing zero gaps from '
                                                                             'aborted documents.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It makes document numbers completely '
                                                                             'random.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It eliminates the need for primary '
                                                                             'keys.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It allows duplicate document numbers.'}],
                                                  'prompt': 'What is the primary advantage of Late Numbering over '
                                                            'Early Numbering for legal business documents like '
                                                            'invoices or purchase orders?',
                                                  'question_id': 'd88_q1'},
                                              {   'concept_slug': 'rap-authorization-control',
                                                  'explanation': 'Global checks general operation rights; Instance '
                                                                 'checks record-specific field attributes.',
                                                  'id': 'd88_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Global checks general permissions before '
                                                                             'accessing any record; Instance checks '
                                                                             'permissions against specific field '
                                                                             'attributes of an existing record.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Global is for English; Instance is for '
                                                                             'German.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Global runs on mobile phones; Instance '
                                                                             'runs on desktops.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Global requires internet access; '
                                                                             'Instance runs offline.'}],
                                                  'prompt': 'What is the fundamental difference between Global '
                                                            'Authorization and Instance Authorization in RAP?',
                                                  'question_id': 'd88_q2'},
                                              {   'concept_slug': 'rap-numbering-strategies',
                                                  'explanation': '`field ( numbering : managed )` generates 16-byte '
                                                                 'raw UUIDs automatically.',
                                                  'id': 'd88_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'field ( numbering : managed ) '
                                                                             '<field_name>'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'field ( random : true ) <field_name>'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'field ( key_generator ) <field_name>'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'field ( sequential : auto ) '
                                                                             '<field_name>'}],
                                                  'prompt': 'Which BDEF clause enables automatic, framework-generated '
                                                            'UUID primary keys on an entity field?',
                                                  'question_id': 'd88_q3'},
                                              {   'concept_slug': 'rap-authorization-control',
                                                  'explanation': '`get_instance_authorizations` enforces '
                                                                 'record-specific authorization rules.',
                                                  'id': 'd88_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'get_instance_authorizations'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'onInit'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'validate_password'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'teardown'}],
                                                  'prompt': 'Which method in the Local Handler Class is implemented to '
                                                            'enforce instance-level authorization rules?',
                                                  'question_id': 'd88_q4'}],
                             'step_id': 'd88_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 88 Verification Assessment'},
                         {   'step_id': 'd88_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Architected Early Numbering (UUIDs) and Late Numbering (sequential '
                                           'number ranges).\n'
                                           '- Implemented dual-tier security governance (Global vs Instance '
                                           'Authorization).\n'
                                           '- Enforced least privilege using `IN LOCAL MODE` for internal operations.',
                             'title': 'Day 88 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd88_s8_completion',
                             'recommended_mission': {'slug': 'nova-rap-early-late-numbering', 'title': 'Early vs Late Numbering Strategies', 'description': 'Implement adjust_numbers logic for legal document sequence generation.'},
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You have mastered all core building blocks of RAP. Tomorrow, '
                                           'you will synthesize everything in the comprehensive **Phase 7 ABAP Cloud & '
                                           'RAP Capstone**.',
                             'title': 'Day 88 Complete: Numbering & Authorization Mastered'}],
            'subtitle': 'Early numbering with UUIDs vs late numbering with number ranges; global vs instance '
                        'authorization.',
            'title': 'Number Ranges & Authorization Control'},
    89: {   'atomic_concepts': ['rap-full-stack-synthesis'],
            'day_number': 89,
            'estimated_minutes': 90,
            'recommended_mission_slug': None,
            'slug': 'abap-cloud-rap-capstone',
            'steps': [   {   'content_md': '### The Benchmark of Cloud-Native ABAP Engineering\n'
                                           'In Phase 7, you have mastered the complete architectural spectrum of '
                                           'modern ABAP Cloud:\n'
                                           '1. **ABAP Cloud Rules**: Banned legacy constructs (`TABLES`, direct SQL '
                                           'updates, manual commits), contractual released C1 APIs.\n'
                                           '2. **Clean Coding & AUnit**: Constructor expressions (`VALUE`, '
                                           '`CORRESPONDING`), string templates, isolated unit test fixtures.\n'
                                           '3. **RAP Three Pillars**: CDS Data Models, Behavior Definitions (BDEF), '
                                           'and Service Provisioning (OData V4).\n'
                                           '4. **Composition Trees**: Root view entities, child compositions, and '
                                           'cascade deletion.\n'
                                           '5. **Transactional Mechanics**: Managed vs unmanaged persistence, 5-stage '
                                           'save sequence (Finalize, Check, Adjust, Save, Cleanup).\n'
                                           '6. **Business Logic**: Determinations (`on modify`/`on save`), Validations '
                                           '(`failed` and `reported` state messages), Actions (instance/factory).\n'
                                           '7. **Enterprise Quality**: Draft handling (`with draft`), Optimistic '
                                           'concurrency via ETags, and Dual-Tier Authorization (Global & Instance).\n'
                                           '\n'
                                           '#### The Capstone Challenge:\n'
                                           'Nova Manufacturing Corp requires a mission-critical **Robotics Equipment '
                                           'Maintenance & Defect Management** application deployed on S/4HANA Cloud in '
                                           'Austin (Plant `PL02`). You must architect, review, and defend the '
                                           'full-stack RAP implementation.',
                             'key_terms': [   {   'definition': 'Complete end-to-end implementation uniting CDS, BDEF, '
                                                                'Draft, Determinations, and OData V4.',
                                                  'term': 'RAP Full-Stack Synthesis'},
                                              {   'definition': 'Rigorous architectural audit verifying Clean Core '
                                                                'compliance, concurrency safety, and test coverage.',
                                                  'term': 'Enterprise Review'}],
                             'step_id': 'd89_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'The RAP Capstone synthesizes data modeling, behavior contracts, draft '
                                         'handling, derivations, validations, and security.',
                             'title': 'Phase 7 Capstone: Full-Stack RAP Architecture Synthesis'},
                         {   'content_md': '### Blueprint of the Nova Robotics RAP Business Object\n'
                                           'Review the architectural blueprint for `ZI_NovaRoboticsIncident`:\n'
                                           '\n'
                                           '1. **CDS Root Entity (`ZI_NovaRoboticsIncident`)**:\n'
                                           '   - Composed of `ZI_NovaRoboticsActionItem` (1..*).\n'
                                           '   - Joins released C1 CDS views `I_Plant` and `I_Product` for description '
                                           'resolution.\n'
                                           '2. **Behavior Definition (`ZI_NovaRoboticsIncident.bdef`)**:\n'
                                           '   - `managed implementation in class zbp_i_novaroboticsincident unique;`\n'
                                           '   - `strict(2); with draft;`\n'
                                           '   - `lock master total etag LastChangedAt`\n'
                                           '   - `etag master LocalLastChangedAt`\n'
                                           '   - Determinations: `calculateRepairCost on modify { field LaborHours, '
                                           'SparePartQuantity; }`\n'
                                           '   - Validations: `validateSeverityOnSave on save { field '
                                           'IncidentSeverity; }`\n'
                                           '   - Actions: `action ( features : instance ) resolveIncident result [1] '
                                           '$self;`\n'
                                           '3. **Service Layer**:\n'
                                           '   - Service Definition `ZUI_ROBOTICS_INCIDENT` exposing projection '
                                           'views.\n'
                                           '   - Service Binding `ZUI_ROBOTICS_INCIDENT_O4` published as `OData V4 - '
                                           'UI`.',
                             'key_terms': [   {   'definition': 'Consumption CDS views tailoring the core data model '
                                                                'specifically for UI consumption.',
                                                  'term': 'Projection Layer'},
                                              {   'definition': 'Certification that the BDEF adheres strictly to all '
                                                                'modern compile-time rules.',
                                                  'term': 'strict(2) Compliance'}],
                             'step_id': 'd89_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'The complete stack links CDS compositions to managed draft BDEFs, local '
                                         'handlers, and OData V4 service bindings.',
                             'title': 'The Full-Stack Architectural Blueprint'},
                         {   'company_context': {   'bo_root': 'ZI_NovaRoboticsIncident',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'plant': 'PL02',
                                                    'status': 'Production Ready'},
                             'content_md': '### Architecture Trace: From UI to Database\n'
                                           '```\n'
                                           '[Fiori Elements Object Page: Resolve Incident Button Clicked]\n'
                                           '                     │\n'
                                           '                     ▼  OData V4: POST .../resolveIncident\n'
                                           '[Service Binding: ZUI_ROBOTICS_INCIDENT_O4]\n'
                                           '                     │\n'
                                           '                     ▼\n'
                                           '[BDEF & LHC: zbp_i_novaroboticsincident]\n'
                                           '  ├── get_instance_features -> Verifies incident is OPEN\n'
                                           "  ├── resolveIncident -> Sets Status = 'RESOLVED', records resolution "
                                           'timestamp\n'
                                           '  ├── calculateRepairCost -> Auto-calculates total parts and labor\n'
                                           "  └── validateSeverityOnSave -> Verifies sign-off if severity = 'HIGH'\n"
                                           '                     │\n'
                                           '                     ▼\n'
                                           '[Save Sequence (LSC)]\n'
                                           '  ├── FINALIZE -> Check complete\n'
                                           '  ├── CHECK_BEFORE_SAVE -> failed is empty\n'
                                           '  ├── ADJUST_NUMBERS -> Assigns INC-2026-0045 from Number Range\n'
                                           '  ├── SAVE -> Writes active table znova_inc_h; deletes draft record\n'
                                           '  └── CLEANUP -> Buffer reset\n'
                                           '```',
                             'scenario': "Review the full-stack code artifacts for Nova's Robotics Incident RAP "
                                         'implementation.',
                             'step_id': 'd89_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Full Stack RAP Code Architecture'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'Audit the following proposed RAP design. Which element violates Clean '
                                            'Core principles?',
                             'options': [   {   'explanation': 'Correct! In managed RAP, developers must NEVER bypass '
                                                               'the framework with direct SQL updates; always use EML '
                                                               '`MODIFY ENTITIES IN LOCAL MODE`.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'A developer placed an explicit `UPDATE znova_inc_h` direct '
                                                        'SQL statement inside the action method instead of using EML '
                                                        '`MODIFY ENTITIES IN LOCAL MODE`.'},
                                            {   'explanation': '`strict(2)` is mandatory best practice.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'The BDEF includes `strict(2)`.'},
                                            {   'explanation': 'OData V4 is the strategic standard.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'The service is exposed as OData V4.'}],
                             'step_id': 'd89_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Never use direct SQL updates in RAP behavior pools; always mutate data via '
                                         'EML `MODIFY ENTITIES IN LOCAL MODE`.',
                             'title': 'Full-Stack RAP Audit Simulation: Identifying Architectural Violations'},
                         {   'instruction': 'As Chief Enterprise Architect, how do you defend the ABAP Cloud & RAP '
                                            'architecture?',
                             'options': [   {   'explanation': 'Correct! RAP is the unified standard across all '
                                                               'S/4HANA editions and BTP.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'RAP is the single strategic programming model for all modern '
                                                        'SAP products (S/4HANA Public, Private, and BTP). Unlike '
                                                        'SEGW/BOPF, RAP delivers native draft handling, '
                                                        'compiler-enforced Clean Core compliance, OData V4 efficiency, '
                                                        'in-memory pushdown, and 100% upgrade safety. SEGW and BOPF '
                                                        'are legacy technologies with no future innovation.'},
                                            {   'explanation': 'Unacceptable surrender to technical debt.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Agree with the tech lead and cancel all cloud migrations.'},
                                            {   'explanation': 'Impossible and absurd.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Rewrite the entire S/4HANA core in JavaScript.'}],
                             'scenario': "A legacy tech lead argues: 'We should stick to classic SEGW OData V2 and "
                                         "BOPF because RAP is just another passing fad.'",
                             'step_id': 'd89_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Phase 7 Capstone Defense: RAP vs Legacy BOPF / SEGW'},
                         {   'assessment_type': 'capstone_quiz',
                             'questions': [   {   'concept_slug': 'rap-full-stack-synthesis',
                                                  'explanation': 'RAP is the unified strategic standard for modern '
                                                                 'ABAP development.',
                                                  'id': 'd89_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'ABAP RESTful Application Programming '
                                                                             'Model (RAP)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Classic Screen Painter (SE51)'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Business Object Processing Framework '
                                                                             '(BOPF)'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Visual Basic for Applications'}],
                                                  'prompt': 'What is the single strategic programming model for '
                                                            'building transactional enterprise business applications '
                                                            'in modern SAP S/4HANA and SAP BTP?',
                                                  'question_id': 'd89_q1'},
                                              {   'concept_slug': 'rap-full-stack-synthesis',
                                                  'explanation': 'EML `IN LOCAL MODE` safely mutates data within '
                                                                 'framework transactional boundaries.',
                                                  'id': 'd89_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Using Entity Manipulation Language (EML) '
                                                                             'with `MODIFY ENTITIES IN LOCAL MODE`'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Using direct SQL `UPDATE` statements'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Writing raw bytes directly to disk'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Calling legacy transaction codes via '
                                                                             'batch input'}],
                                                  'prompt': 'How does a developer mutate business data inside a RAP '
                                                            'behavior implementation method while remaining compliant '
                                                            'with framework lifecycle rules?',
                                                  'question_id': 'd89_q2'},
                                              {   'concept_slug': 'rap-full-stack-synthesis',
                                                  'explanation': 'RAP compositions enforce automatic cascade deletion.',
                                                  'id': 'd89_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'All composed child line items are '
                                                                             'automatically deleted via cascade '
                                                                             'deletion.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Child items remain orphaned in the '
                                                                             'database forever.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'The database crashes with a fatal '
                                                                             'error.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'The user is forced to re-type the line '
                                                                             'items.'}],
                                                  'prompt': 'What happens to composed child line items when a parent '
                                                            'root entity is deleted in a Managed RAP scenario?',
                                                  'question_id': 'd89_q3'},
                                              {   'concept_slug': 'rap-full-stack-synthesis',
                                                  'explanation': '`CHECK_BEFORE_SAVE` verifies business rules and '
                                                                 'aborts persistence on failure.',
                                                  'id': 'd89_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It executes final business validations, '
                                                                             'aborting the save immediately if the '
                                                                             '`failed` structure is populated.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It deletes all records from the draft '
                                                                             'table.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It downloads user emails.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It turns off database logging.'}],
                                                  'prompt': 'What is the role of the `CHECK_BEFORE_SAVE` stage in the '
                                                            'RAP Save Sequence?',
                                                  'question_id': 'd89_q4'}],
                             'step_id': 'd89_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Phase 7 Comprehensive Capstone Assessment'},
                         {   'step_id': 'd89_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Comprehensive Phase 7 Benchmark Achieved:\n'
                                           '- **Full-Stack RAP Mastery**: Mastered CDS view entities, managed BDEFs, '
                                           'draft handling, determinations, validations, actions, and service '
                                           'bindings.\n'
                                           '- **Clean Core Engineering**: Enforced ABAP Cloud language version rules, '
                                           'released C1 APIs, and eliminated forbidden legacy syntax.\n'
                                           '- **Transactional Rigor**: Orchestrated the 5-stage save sequence, '
                                           'optimistic locking via ETags, and dual-tier authorization.',
                             'title': 'Phase 7 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd89_s8_completion',
                             'recommended_mission': {'slug': 'nova-abap-cloud-rap-capstone', 'title': 'ABAP Cloud & RAP Enterprise Capstone', 'description': 'Architect, test, and activate end-to-end RAP BO for Nova manufacturing.'},
                             'step_type': 'completion',
                             'summary_md': 'Congratulations! You have completed Phase 7: ABAP Cloud & RAP. You possess '
                                           'deep, state-of-the-art pro-code engineering skills. In **Phase 8 (Days '
                                           '90–95)**, you will master enterprise connectivity: **SAP BTP & Enterprise '
                                           'Integration (Integration Suite, CPI, Event Mesh, Cloud Connector)**.',
                             'title': 'Phase 7 Complete: ABAP Cloud & RAP Certified'}],
            'subtitle': 'Full-stack RAP synthesis: CDS entities, managed BDEF with draft, determinations, validations, '
                        'actions, and review.',
            'title': 'ABAP Cloud & RAP Capstone Assessment'}}
