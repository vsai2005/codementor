"""Authoritative content definitions for SAP S/4HANA Guided Learning Days 90–95 (Phase 8).

Phase 8: SAP BTP & Enterprise Integration (BTP, CPI, Groovy, Event Mesh, Cloud Connector, Capstone).
Enterprise Continuous Model: Nova Manufacturing Corp (NM01)
"""

from __future__ import annotations
from typing import Any

PHASE_8_DAYS_CONTENT: dict[int, dict[str, Any]] = {   90: {   'atomic_concepts': ['btp-architecture-overview', 'cloud-foundry-vs-kyma', 'btp-destinations'],
            'day_number': 90,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'btp-architecture-environments',
            'steps': [   {   'content_md': '### The Innovation & Integration Platform\n'
                                           'SAP Business Technology Platform (BTP) is the unified cloud platform '
                                           'enabling application development, process automation, integration, data '
                                           'management, and enterprise AI across hybrid multi-cloud landscapes.\n'
                                           '\n'
                                           '#### Account Model Architecture:\n'
                                           '1. **Global Account**: The top-level commercial agreement between the '
                                           'customer and SAP. Holds enterprise entitlement quotas and cost tracking.\n'
                                           '2. **Directories**: Optional organizational grouping structure dividing '
                                           'enterprise domains (e.g. *Manufacturing Hubs*, *Corporate Finance*).\n'
                                           '3. **Subaccounts**: The independent, isolated technical runtime tenants.\n'
                                           '   - Each Subaccount is bound to a specific geographic **Region** and '
                                           '**Hyperscaler Infrastructure Provider** (AWS Frankfurt, Azure US East, GCP '
                                           'Tokyo).\n'
                                           '   - Subaccounts maintain their own identity trust, destinations, service '
                                           'instances, and quotas.\n'
                                           '4. **Spaces**: Logical partitions within runtime environments (e.g., '
                                           '*Dev*, *QA*, *Prod* spaces in Cloud Foundry).',
                             'key_terms': [   {   'definition': 'Top-level commercial container managing enterprise '
                                                                'BTP entitlements and billing.',
                                                  'term': 'Global Account'},
                                              {   'definition': 'Isolated technical tenant bound to a specific region '
                                                                'and hyperscaler provider.',
                                                  'term': 'Subaccount'},
                                              {   'definition': 'BTP capability running workloads flexibly on AWS, '
                                                                'Azure, Google Cloud, or Alibaba Cloud.',
                                                  'term': 'Hyperscaler Choice'}],
                             'step_id': 'd90_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'BTP organizes cloud resources into Global Accounts, regional Subaccounts on '
                                         'major hyperscalers, and isolated Spaces.',
                             'title': 'SAP Business Technology Platform (BTP) Foundations'},
                         {   'content_md': '### The Three Execution Runtimes in BTP\n'
                                           'Developers can deploy applications across three distinct runtime '
                                           'environments within a subaccount:\n'
                                           '\n'
                                           '| Feature | Cloud Foundry Runtime | Kyma Runtime (Kubernetes) | ABAP '
                                           'Environment (Steampunk) |\n'
                                           '|---|---|---|---|\n'
                                           '| **Underlying Tech** | Cloud Foundry PaaS buildpacks | Open-source '
                                           'Kubernetes & Istio service mesh | Containerized SAP NetWeaver ABAP Kernel '
                                           '|\n'
                                           '| **Best For** | Standard 12-factor apps, SAP CAP (Node/Java) | Complex '
                                           'containerized microservices, Python, AI, custom Docker | Running modern '
                                           'ABAP Cloud code decoupled from ERP core |\n'
                                           '| **Scaling** | Application instance scaling | Native Kubernetes Pod '
                                           'Autoscaling (HPA) | Elastic cloud tenant compute units |\n'
                                           '| **Networking** | Standard route mapping | Kubernetes Ingress, Istio '
                                           'VirtualServices | HTTP OData services & RFC destinations |\n'
                                           '\n'
                                           '#### BTP Destinations Service:\n'
                                           '- Centralized configuration storing target system URLs, proxy types '
                                           '(`OnPremise` vs `Internet`), and authentication methods (OAuth2, SAML2 '
                                           'Bearer, Basic).\n'
                                           '- Enables applications to consume S/4HANA APIs using logical aliases '
                                           '(`Destination: S4H_HEIDELBERG_PL01`) without hardcoding endpoints or '
                                           'credentials.',
                             'key_terms': [   {   'definition': 'Cloud-native Kubernetes runtime for building modular '
                                                                'containerized microservices with Istio.',
                                                  'term': 'Kyma Environment'},
                                              {   'definition': 'Platform-as-a-Service runtime executing 12-factor '
                                                                'apps via polyglot buildpacks.',
                                                  'term': 'Cloud Foundry Environment'},
                                              {   'definition': 'Secure credential and URL configuration decoupling '
                                                                'app code from remote backend endpoints.',
                                                  'term': 'BTP Destination'}],
                             'step_id': 'd90_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Choose Cloud Foundry for standard CAP apps, Kyma for containerized '
                                         'Kubernetes workloads, and BTP Destinations for secure decoupled '
                                         'connectivity.',
                             'title': 'Runtime Environments: Cloud Foundry vs Kyma vs ABAP'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'global_account': 'Nova-Corp-Global (GA-9821)',
                                                    'subaccount_eu': 'NM01-Europe-Prod (AWS eu-central-1 Frankfurt)',
                                                    'subaccount_us': 'NM02-Americas-Prod (Azure us-east-1 Virginia)'},
                             'content_md': '### BTP Enterprise Topology Diagram\n'
                                           '```\n'
                                           '[Global Account: Nova-Corp-Global]\n'
                                           '  │\n'
                                           '  ├── [Directory: Production Operations]\n'
                                           '  │     ├── [Subaccount: NM01-Europe-Prod (AWS Frankfurt)]\n'
                                           '  │     │     ├── Kyma Cluster (Robotics IoT Ingestion)\n'
                                           '  │     │     └── Destination: S4H_PL01_HEIDELBERG (via Cloud Connector)\n'
                                           '  │     │\n'
                                           '  │     └── [Subaccount: NM02-Americas-Prod (Azure US East)]\n'
                                           '  │           ├── Cloud Foundry Space: PROD (Supplier Collaboration CAP '
                                           'App)\n'
                                           '  │           └── Destination: S4H_PL02_AUSTIN (Direct Public Cloud '
                                           'OData)\n'
                                           '```',
                             'scenario': 'Nova Manufacturing deploys subaccounts across AWS Frankfurt (serving '
                                         'Heidelberg) and Azure US East (serving Austin).',
                             'step_id': 'd90_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Multi-Region BTP Topology'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "Nova's data science team wants to deploy a Python machine-learning model "
                                            'packaged in a custom Docker container with GPU acceleration. Select the '
                                            'optimal BTP environment.',
                             'options': [   {   'explanation': 'Correct! Kyma provides full Kubernetes container '
                                                               'flexibility, ideal for custom Dockerized Python '
                                                               'microservices.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Deploy to BTP Kyma Runtime: it provides native Kubernetes '
                                                        'container orchestration, custom Docker image support, and '
                                                        'granular resource limits.'},
                                            {   'explanation': 'Impossible; the ABAP runtime cannot execute Docker '
                                                               'container images.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Attempt to compile the Python Docker container into an ABAP '
                                                        'report in SE38.'},
                                            {   'explanation': 'Mobile phones lack enterprise scalability and '
                                                               'security.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': "Run the machine learning script on a user's smartphone."}],
                             'step_id': 'd90_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Use Kyma Kubernetes runtime for custom Docker containers, Python AI models, '
                                         'and polyglot microservices.',
                             'title': 'BTP Environment Selection Simulation'},
                         {   'instruction': 'What is the enterprise security remediation?',
                             'options': [   {   'explanation': 'Correct! Hardcoded credentials violate enterprise '
                                                               'security; BTP Destinations manage secrets securely '
                                                               'with credential rotation.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Reject the code. Mandate using the BTP Destinations Service: '
                                                        'store credentials securely in the BTP Subaccount destination '
                                                        'with Principal Propagation (or OAuth2), and consume the '
                                                        'destination programmatically via '
                                                        '`@sap-cloud-sdk/connectivity`.'},
                                            {   'explanation': 'Severe security breach that will expose enterprise '
                                                               'systems to public hacking.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Commit the password to a public GitHub repository.'},
                                            {   'explanation': 'Disabling authentication destroys security.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Delete the S/4HANA password so nobody needs to enter it.'}],
                             'scenario': 'A contractor writes a Node.js microservice that stores the S/4HANA admin '
                                         'username and password hardcoded in a plain text `.env` file.',
                             'step_id': 'd90_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Security Challenge: Hardcoded Credentials vs BTP Destinations'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'btp-architecture-overview',
                                                  'explanation': 'Subaccounts represent regional deployments on chosen '
                                                                 'hyperscaler providers.',
                                                  'id': 'd90_q1',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'Subaccount'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Global Account'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'User Profile'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Browser Cookie'}],
                                                  'prompt': 'In the SAP BTP account model, what is the primary '
                                                            'architectural boundary that is bound to a specific region '
                                                            'and hyperscaler provider?',
                                                  'question_id': 'd90_q1'},
                                              {   'concept_slug': 'cloud-foundry-vs-kyma',
                                                  'explanation': 'Kyma delivers standard Kubernetes and Istio '
                                                                 'container management on BTP.',
                                                  'id': 'd90_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Kyma Environment'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Classic Dynpro Environment'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'DOS Prompt'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Windows 95 Virtual Machine'}],
                                                  'prompt': 'Which BTP runtime environment is built on open-source '
                                                            'Kubernetes and is optimal for deploying custom Dockerized '
                                                            'microservices and AI workloads?',
                                                  'question_id': 'd90_q2'},
                                              {   'concept_slug': 'btp-destinations',
                                                  'explanation': 'Destinations decouple application code from remote '
                                                                 'backend credentials and endpoints.',
                                                  'id': 'd90_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To securely store connection URLs, proxy '
                                                                             'settings, and authentication credentials '
                                                                             'outside application code.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To book airplane tickets for enterprise '
                                                                             'consultants.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To download video game updates.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To format XML files into PDF '
                                                                             'documents.'}],
                                                  'prompt': 'What is the primary operational purpose of the BTP '
                                                            'Destinations service?',
                                                  'question_id': 'd90_q3'},
                                              {   'concept_slug': 'btp-architecture-overview',
                                                  'explanation': 'BTP ABAP Environment hosts containerized ABAP Cloud '
                                                                 'applications directly on BTP.',
                                                  'id': 'd90_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'SAP BTP ABAP Environment'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'SAP GUI for Windows 3.11'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Eclipse ADT without internet'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Local Notepad editor'}],
                                                  'prompt': 'Which SAP service provides modern ABAP developers with a '
                                                            'cloud-managed ABAP environment directly on BTP '
                                                            '(Steampunk)?',
                                                  'question_id': 'd90_q4'}],
                             'step_id': 'd90_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 90 Verification Assessment'},
                         {   'step_id': 'd90_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered SAP BTP account hierarchy (Global Accounts, Directories, '
                                           'regional Subaccounts).\n'
                                           '- Evaluated runtime environments: Cloud Foundry (12-factor apps), Kyma '
                                           '(Kubernetes), and BTP ABAP.\n'
                                           '- Implemented secure backend connectivity using the BTP Destinations '
                                           'service.',
                             'title': 'Day 90 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd90_s8_completion',
                             
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You understand the BTP foundation. Tomorrow, you will master '
                                           'the enterprise integration engine: **SAP Integration Suite & Cloud '
                                           'Integration (CPI)**.',
                             'title': 'Day 90 Complete: BTP Architecture Mastered'}],
            'subtitle': 'Global accounts, subaccounts, Cloud Foundry, Kyma (Kubernetes), BTP Destinations, and '
                        'multi-cloud hyperscalers.',
            'title': 'SAP BTP Architecture & Runtimes'},
    91: {   'atomic_concepts': [   'sap-integration-suite',
                                   'cloud-integration-cpi',
                                   'iflow-design',
                                   'sync-vs-async-integration'],
            'day_number': 91,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'integration-suite-cpi-overview',
            'steps': [   {   'content_md': '### The Bridge Across Heterogeneous Landscapes\n'
                                           'In complex enterprise IT architectures, S/4HANA must integrate seamlessly '
                                           'with non-SAP systems (Salesforce, Workday, EDI supplier networks, banking '
                                           "gateways). **SAP Integration Suite** is SAP's leading Integration "
                                           'Platform-as-a-Service (iPaaS).\n'
                                           '\n'
                                           '#### Core Capabilities of SAP Integration Suite:\n'
                                           '1. **Cloud Integration (formerly CPI)**: Core message broker executing '
                                           '**Integration Flows (iFlows)** for message mediation, transformation, '
                                           'routing, and protocol conversion.\n'
                                           '2. **API Management**: Exposes, secures, throttles, and analyzes '
                                           'enterprise APIs.\n'
                                           '3. **Open Connectors**: Pre-built connectors to 160+ non-SAP cloud '
                                           'applications.\n'
                                           '4. **Integration Advisor**: AI-assisted B2B/EDI mapping assistant '
                                           '(generating EDIFACT, X12, and IDoc mappings).\n'
                                           '5. **Trading Partner Management**: B2B partner profile management and '
                                           'agreement tracking.',
                             'key_terms': [   {   'definition': 'Enterprise iPaaS providing message processing, API '
                                                                'management, and B2B integration.',
                                                  'term': 'SAP Integration Suite'},
                                              {   'definition': 'Core integration capability orchestrating message '
                                                                'transformation and iFlow routing.',
                                                  'term': 'Cloud Integration (CPI)'},
                                              {   'definition': 'Visual BPMN-style integration model defining message '
                                                                'reception, transformation, and dispatch.',
                                                  'term': 'Integration Flow (iFlow)'}],
                             'step_id': 'd91_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'SAP Integration Suite provides enterprise iPaaS capabilities, with Cloud '
                                         'Integration (CPI) executing visual iFlow message pipelines.',
                             'title': 'The Strategic Enterprise Middleware: SAP Integration Suite'},
                         {   'content_md': '### Choosing the Right Integration Pattern\n'
                                           'Architects must strictly classify integrations into synchronous or '
                                           'asynchronous patterns:\n'
                                           '\n'
                                           '| Dimension | Synchronous Integration (Request-Reply) | Asynchronous '
                                           'Integration (Fire-and-Forget) |\n'
                                           '|---|---|---|\n'
                                           '| **Mechanism** | Sender halts and waits for receiver response | Sender '
                                           'dispatches message and continues immediately |\n'
                                           '| **Protocol Example** | HTTP/REST, OData, SOAP Request-Response | JMS '
                                           'Queue, AMQP, Event Mesh, SFTP |\n'
                                           '| **Coupling** | Tight coupling; sender fails if receiver is down | '
                                           'Decoupled; queues buffer messages during receiver downtime |\n'
                                           '| **Latency** | Sub-second real-time | Near-real-time to minutes |\n'
                                           '| **Best For** | Credit card validation, real-time stock ATP check | '
                                           'Purchase orders, invoices, batch telemetry, journal entries |\n'
                                           '\n'
                                           '#### Adapters in Cloud Integration:\n'
                                           '- Inbound/Outbound adapters connect to diverse endpoints: **OData V2/V4**, '
                                           '**REST/HTTP**, **SOAP**, **AMQP**, **JMS**, **Kafka**, **SFTP**, and '
                                           '**Process Integration (XI)**.',
                             'key_terms': [   {   'definition': 'Request-reply communication where sender blocks '
                                                                'execution until a response is received.',
                                                  'term': 'Synchronous Pattern'},
                                              {   'definition': 'Decoupled message dispatch via persistent queues '
                                                                'without blocking sender execution.',
                                                  'term': 'Asynchronous Pattern'},
                                              {   'definition': 'Protocol connector translating external wire '
                                                                'protocols (SOAP, REST, JMS) into internal iFlow '
                                                                'messages.',
                                                  'term': 'Adapter'}],
                             'step_id': 'd91_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Use synchronous for immediate query lookups; use asynchronous with queue '
                                         'buffering for high-volume transactions.',
                             'title': 'Message Exchange Patterns: Synchronous vs Asynchronous Integration'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'iflow_name': 'Nova_EDI855_To_S4HANA_Confirmation',
                                                    'receiver_protocol': 'OData V4 (S/4HANA SupplierConfirmation API)',
                                                    'sender_protocol': 'SFTP (Inbound XML / EDIFACT)'},
                             'content_md': '### iFlow Pipeline Architecture\n'
                                           '```\n'
                                           '[External Supplier: VEND-101] \n'
                                           '         │  SFTP Polling (Every 15 min)\n'
                                           '         ▼\n'
                                           '[Inbound SFTP Adapter: reads XML Payload]\n'
                                           '         │\n'
                                           '         ▼  [Content Modifier: Extracts PO Number into Camel Header]\n'
                                           '         │\n'
                                           '         ▼  [Message Mapping: Maps EDI 855 fields -> S/4HANA OData V4 '
                                           'Schema]\n'
                                           '         │\n'
                                           '         ▼  [Groovy Script: Validates Plant PL01 ISO-9001 compliance]\n'
                                           '         │\n'
                                           '         ▼  [Outbound OData V4 Adapter: POST '
                                           '/sap/opu/odata4/.../SupplierConfirmation]\n'
                                           '         │\n'
                                           '[S/4HANA Private Cloud: Heidelberg NM01]\n'
                                           '         └── Purchase Order Item updated with confirmed delivery date!\n'
                                           '```',
                             'scenario': 'Nova connects external German suppliers sending ANSI X12/EDIFACT order '
                                         'confirmations to S/4HANA Cloud in Heidelberg.',
                             'step_id': 'd91_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing EDI Supplier Integration iFlow'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'A third-party logistics billing system experiences frequent 4-hour '
                                            'network outages. Real-time delivery confirmations from S/4HANA are '
                                            'failing and being lost. Redesign the integration.',
                             'options': [   {   'explanation': 'Correct! Asynchronous queuing buffers messages during '
                                                               'receiver downtime, retrying automatically until the '
                                                               'target system recovers.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Switch from synchronous HTTP to Asynchronous Queue-Based '
                                                        'Integration: place an internal JMS queue in Cloud Integration '
                                                        'between S/4HANA and the logistics provider, with retry '
                                                        'policies.'},
                                            {   'explanation': 'Manual re-entry causes massive human error and delayed '
                                                               'customer shipments.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Keep synchronous HTTP and have employees re-type lost '
                                                        'deliveries manually.'},
                                            {   'explanation': 'Halting business operations violates service-level '
                                                               'agreements.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Cancel shipments whenever the network is down.'}],
                             'step_id': 'd91_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Decouple fragile receiver endpoints using asynchronous JMS queues and '
                                         'automated retry policies.',
                             'title': 'iFlow Architecture Simulation: Resolving Receiver Outages'},
                         {   'instruction': 'As Chief Enterprise Architect, what is your ruling?',
                             'options': [   {   'explanation': 'Correct! Point-to-point integration creates '
                                                               "unmaintainable 'spaghetti architecture' and severe "
                                                               'security vulnerabilities.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Reject point-to-point connections. Enforce enterprise iPaaS '
                                                        'governance: mandate routing all integrations through SAP '
                                                        'Integration Suite, leveraging centralized security, message '
                                                        'monitoring, rate limiting, and Clean Core API decoupling.'},
                                            {   'explanation': 'Creates massive technical debt and unmanageable '
                                                               'security risks.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Approve the point-to-point connections to save a few days of '
                                                        'configuration.'},
                                            {   'explanation': 'Modern enterprises cannot operate without external '
                                                               'digital connectivity.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Disable all external integrations permanently.'}],
                             'scenario': 'A legacy team proposes connecting 45 non-SAP cloud applications directly to '
                                         'S/4HANA using custom point-to-point database scripts and custom open '
                                         'firewall ports.',
                             'step_id': 'd91_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Integration Governance Challenge: Point-to-Point Spaghetti vs iPaaS'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'sap-integration-suite',
                                                  'explanation': 'SAP Integration Suite is the strategic enterprise '
                                                                 'iPaaS.',
                                                  'id': 'd91_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'SAP Integration Suite'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'SAP WinWord'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Windows Media Player'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Adobe Photoshop'}],
                                                  'prompt': 'What is the comprehensive SAP Integration '
                                                            'Platform-as-a-Service (iPaaS) used for orchestrating '
                                                            'hybrid, multi-cloud, and non-SAP enterprise integrations?',
                                                  'question_id': 'd91_q1'},
                                              {   'concept_slug': 'cloud-integration-cpi',
                                                  'explanation': 'An iFlow defines the end-to-end processing pipeline '
                                                                 'for messages in Cloud Integration.',
                                                  'id': 'd91_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'A visual model defining message routing, '
                                                                             'transformations, splitters, aggregators, '
                                                                             'and adapter endpoints.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'A water pipe diagram for plant '
                                                                             'plumbing.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'A user timesheet report.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'An audio recording of an executive '
                                                                             'speech.'}],
                                                  'prompt': "What is an 'Integration Flow' (iFlow) in SAP Cloud "
                                                            'Integration?',
                                                  'question_id': 'd91_q2'},
                                              {   'concept_slug': 'sync-vs-async-integration',
                                                  'explanation': 'Asynchronous decoupling protects system reliability '
                                                                 'and prevents cascading timeouts.',
                                                  'id': 'd91_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It decouples sender and receiver, '
                                                                             'buffering messages in queues during '
                                                                             'target system downtime and preventing '
                                                                             'timeout cascading.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It deletes messages if the server is '
                                                                             'busy.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It requires no internet connection.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It converts XML into paper printouts.'}],
                                                  'prompt': 'Why is asynchronous integration preferred over '
                                                            'synchronous integration for high-volume, cross-system '
                                                            'document exchanges (like purchase orders)?',
                                                  'question_id': 'd91_q3'},
                                              {   'concept_slug': 'iflow-design',
                                                  'explanation': 'Adapters handle protocol mediation between external '
                                                                 'systems and the iFlow pipeline.',
                                                  'id': 'd91_q4',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'Adapter'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Font Picker'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'Sound Card'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Mouse Driver'}],
                                                  'prompt': 'Which component inside an iFlow is responsible for '
                                                            'translating external network protocols (such as SFTP, '
                                                            'SOAP, or OData) into the internal message format?',
                                                  'question_id': 'd91_q4'}],
                             'step_id': 'd91_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 91 Verification Assessment'},
                         {   'step_id': 'd91_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered SAP Integration Suite capabilities (Cloud Integration, API '
                                           'Management, Open Connectors).\n'
                                           '- Architected resilient iFlow pipelines connecting non-SAP systems to '
                                           'S/4HANA OData APIs.\n'
                                           '- Selected appropriate message exchange patterns (Synchronous vs '
                                           'Asynchronous Queues).',
                             'title': 'Day 91 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd91_s8_completion',
                             
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You understand message orchestration. Tomorrow, you will dive '
                                           'into message payload transformations: **CPI Message Transformations & '
                                           'Groovy Scripting**.',
                             'title': 'Day 91 Complete: Integration Suite & CPI Mastered'}],
            'subtitle': 'Integration flows (iFlows), adapter configurations (OData, REST, SOAP, SFTP), message '
                        'exchange patterns, and sync vs async.',
            'title': 'Integration Patterns & SAP Integration Suite'},
    92: {   'atomic_concepts': ['iflow-groovy-scripting', 'content-enricher-pattern'],
            'day_number': 92,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'iflow-transformations-groovy',
            'steps': [   {   'content_md': '### Transforming Heterogeneous Data Schemas\n'
                                           'Sender payloads rarely match the exact schema required by S/4HANA. Cloud '
                                           'Integration provides specialized transformation steps:\n'
                                           '\n'
                                           '#### Transformation Building Blocks:\n'
                                           '1. **Message Mapping**: Graphical drag-and-drop tool mapping source '
                                           'schemas (XSD/WSDL/JSON) to target schemas with built-in functions.\n'
                                           '2. **Content Modifier**: Creates, updates, or extracts message headers, '
                                           'properties, and body payloads using XPath, JSONPath, or static '
                                           'expressions.\n'
                                           '3. **Converter Steps**: XML-to-JSON and JSON-to-XML converters.\n'
                                           '4. **Content Enricher Pattern**: Lookups data from an auxiliary system '
                                           '(e.g. looking up a customer tax ID) and merges it into the active message '
                                           'payload without losing original data.',
                             'key_terms': [   {   'definition': 'iFlow step setting or extracting message headers, '
                                                                'properties, and body content.',
                                                  'term': 'Content Modifier'},
                                              {   'definition': 'Enterprise integration pattern combining secondary '
                                                                'lookup data into a primary message payload.',
                                                  'term': 'Content Enricher Pattern'},
                                              {   'definition': 'Visual structural transformation mapping source '
                                                                'fields to target fields.',
                                                  'term': 'Message Mapping'}],
                             'step_id': 'd92_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Transformations use Message Mappings, Content Modifiers, and Content '
                                         'Enrichers to harmonize disparate schemas.',
                             'title': 'Message Transformation in Cloud Integration'},
                         {   'content_md': '### Writing Custom Logic in Apache Groovy\n'
                                           'When graphical mappings cannot solve complex dynamic requirements (e.g. '
                                           'hashing, base64 encoding, dynamic token parsing), developers use **Groovy '
                                           'Scripts**:\n'
                                           '\n'
                                           '#### Anatomy of a Cloud Integration Groovy Script:\n'
                                           '```groovy\n'
                                           'import com.sap.gateway.ip.core.customdev.util.Message\n'
                                           '\n'
                                           'def Message processData(Message message) {\n'
                                           '    // 1. Read message body\n'
                                           '    def body = message.getBody(String)\n'
                                           '    \n'
                                           '    // 2. Read headers and exchange properties\n'
                                           '    def headers = message.getHeaders()\n'
                                           '    def plant = headers.get("Plant")\n'
                                           '    \n'
                                           '    // 3. Perform dynamic transformation\n'
                                           '    def jsonSlurper = new groovy.json.JsonSlurper()\n'
                                           '    def payload = jsonSlurper.parseText(body)\n'
                                           '    \n'
                                           '    if (plant == "PL01") {\n'
                                           '        payload.Currency = "EUR"\n'
                                           '    } else {\n'
                                           '        payload.Currency = "USD"\n'
                                           '    }\n'
                                           '    \n'
                                           '    // 4. Update message body and header\n'
                                           '    message.setBody(groovy.json.JsonOutput.toJson(payload))\n'
                                           '    message.setHeader("ProcessedBy", "NovaGroovyTransformer")\n'
                                           '    \n'
                                           '    return message\n'
                                           '}\n'
                                           '```',
                             'key_terms': [   {   'definition': 'Java-compatible scripting language executed within '
                                                                'iFlows for advanced payload manipulation.',
                                                  'term': 'Groovy Script'},
                                              {   'definition': 'Standard Apache Camel message instance providing '
                                                                'access to body, headers, and properties.',
                                                  'term': 'Message Object'}],
                             'step_id': 'd92_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Groovy scripts manipulate the Camel Message object (body, headers, '
                                         'properties) for advanced dynamic processing.',
                             'title': 'Dynamic Message Manipulation via Groovy Scripting'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'enrichment': 'Original Invoice + Looked-up Tax Code merged into '
                                                                  'single payload',
                                                    'pattern': 'Content Enricher (Lookup on Company Code NM01)'},
                             'content_md': '### Content Enricher Execution Model\n'
                                           '```\n'
                                           '[Original Inbound Invoice: Vendor VEND-101]\n'
                                           '               │\n'
                                           '               ▼\n'
                                           '[Content Enricher Step] ──(Queries S/4HANA OData)──► [Lookup: '
                                           'TaxJurisdiction]\n'
                                           '               │                                            │\n'
                                           '               └──────────── Combined Payload ◄─────────────┘\n'
                                           '                                    │\n'
                                           '                                    ▼\n'
                                           '[Groovy Script: Validates Tax Code format & formats JSON payload]\n'
                                           '                                    │\n'
                                           '                                    ▼\n'
                                           '                 [Final S/4HANA MIRO Invoice Post]\n'
                                           '```',
                             'scenario': 'Nova enriches an inbound supplier invoice with real-time tax jurisdiction '
                                         'codes looked up from S/4HANA via the Content Enricher.',
                             'step_id': 'd92_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Content Enricher & Groovy Token Validator'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'German umlauts (ä, ö, ü) in supplier names from Heidelberg are arriving '
                                            "corrupted as '?' in S/4HANA. Diagnose the Groovy script error.",
                             'options': [   {   'explanation': 'Correct! Character set corruption is resolved by '
                                                               'strictly enforcing UTF-8 reader decoding.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'The Groovy script reads `message.getBody(String)` without '
                                                        'specifying UTF-8 encoding, defaulting to system ASCII. Fix: '
                                                        'read as `message.getBody(java.io.Reader)` or explicitly '
                                                        'decode as `UTF-8`.'},
                                            {   'explanation': 'Unacceptable and offensive.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Tell German suppliers to rename their companies without '
                                                        'vowels.'},
                                            {   'explanation': 'Nonsensical.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Switch from computers to telegrams.'}],
                             'step_id': 'd92_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Always enforce strict UTF-8 character encoding when reading and writing '
                                         'message streams in Groovy.',
                             'title': 'Groovy Scripting Simulation: Handling Character Encoding Errors'},
                         {   'instruction': 'What is the certified streaming integration pattern?',
                             'options': [   {   'explanation': 'Correct! Streaming splitters prevent loading '
                                                               'multi-gigabyte payloads into JVM memory '
                                                               'simultaneously.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Use the General Splitter step to stream and split the large '
                                                        '2GB XML file into chunks of 500 records, processing each '
                                                        'chunk in a memory-bounded sub-process.'},
                                            {   'explanation': 'Poor architecture cannot be solved simply by adding '
                                                               'expensive hardware.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Ask SAP to buy 500 terabytes of additional RAM for the '
                                                        'tenant.'},
                                            {   'explanation': 'Destroys business catalog information.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Delete the first 1.9 gigabytes of catalog data.'}],
                             'scenario': 'An integration developer loads a 2-gigabyte XML catalog file into an '
                                         'in-memory DOM Groovy parser (`XmlSlurper`), triggering an OutOfMemoryError '
                                         'in Cloud Integration.',
                             'step_id': 'd92_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Performance Challenge: Memory Exhaustion in Large File Mappings'},
                         {   'assessment_type': 'abap_challenge',
                             'questions': [   {   'concept_slug': 'iflow-groovy-scripting',
                                                  'explanation': 'The `Message` object encapsulates payload, headers, '
                                                                 'and properties.',
                                                  'id': 'd92_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'com.sap.gateway.ip.core.customdev.util.Message'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'java.sql.Connection'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'org.apache.hadoop.FileSystem'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'javax.swing.JFrame'}],
                                                  'prompt': 'What object is passed as the primary argument to the '
                                                            '`processData` method in an SAP Cloud Integration Groovy '
                                                            'script?',
                                                  'question_id': 'd92_q1'},
                                              {   'concept_slug': 'content-enricher-pattern',
                                                  'explanation': 'Content Enricher merges secondary lookup data into '
                                                                 'active payloads.',
                                                  'id': 'd92_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'To query an external lookup system and '
                                                                             'merge auxiliary data into the primary '
                                                                             'message without losing original fields.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'To compress the message into a ZIP '
                                                                             'archive.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'To delete sensitive customer data.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'To translate English words into '
                                                                             'French.'}],
                                                  'prompt': 'What is the primary function of the Content Enricher '
                                                            'pattern in an iFlow?',
                                                  'question_id': 'd92_q2'},
                                              {   'concept_slug': 'iflow-groovy-scripting',
                                                  'explanation': '`message.getHeaders().get(...)` accesses Camel '
                                                                 'message headers.',
                                                  'id': 'd92_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': "message.getHeaders().get('HeaderName')"},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': "System.getenv('HeaderName')"},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'SELECT HeaderName FROM DB'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'READ TABLE headers'}],
                                                  'prompt': 'How are custom header variables retrieved inside a Groovy '
                                                            'script in Cloud Integration?',
                                                  'question_id': 'd92_q3'},
                                              {   'concept_slug': 'content-enricher-pattern',
                                                  'explanation': 'Content Modifiers extract XPath values into headers '
                                                                 'and properties.',
                                                  'id': 'd92_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Content Modifier (XPath expression)'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'Router'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'Filter'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Aggregator'}],
                                                  'prompt': 'Which iFlow step is typically used to extract values from '
                                                            'an incoming XML payload and store them in message '
                                                            'exchange properties without writing code?',
                                                  'question_id': 'd92_q4'}],
                             'step_id': 'd92_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 92 Verification Assessment'},
                         {   'step_id': 'd92_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Implemented payload transformations using Message Mappings and Content '
                                           'Modifiers.\n'
                                           '- Authored dynamic Groovy scripts manipulating Camel Message bodies and '
                                           'headers.\n'
                                           '- Applied the Content Enricher pattern and streaming splitters for '
                                           'enterprise memory efficiency.',
                             'title': 'Day 92 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd92_s8_completion',
                             
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You know how to manipulate message payloads. Tomorrow, you '
                                           'will master real-time asynchronous notifications: **Event-Driven '
                                           'Architecture & SAP Event Mesh**.',
                             'title': 'Day 92 Complete: Transformations & Groovy Mastered'}],
            'subtitle': 'Message Mapping, Content Modifier, Content Enricher pattern, and dynamic message manipulation '
                        'with Groovy scripts.',
            'title': 'iFlow Mappings & Groovy Scripting'},
    93: {   'atomic_concepts': ['event-driven-architecture', 'sap-event-mesh', 'cloudevents-standard'],
            'day_number': 93,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 'sap-event-mesh-eda',
            'steps': [   {   'content_md': '### Moving from Polling to Real-Time Push\n'
                                           'In legacy integrations, external systems polled S/4HANA every 5 minutes: '
                                           '*"Are there any new purchase orders?"*. 99% of polling calls returned '
                                           'empty, wasting network bandwidth and database CPU.\n'
                                           '\n'
                                           '#### The Event-Driven Paradigm:\n'
                                           '- **Publish-Subscribe (Pub-Sub)**: S/4HANA publishes a lightweight '
                                           '**Business Event** immediately when a business milestone occurs (e.g. '
                                           '*PurchaseOrder.Created*).\n'
                                           '- **SAP Event Mesh**: A fully managed cloud messaging broker on SAP BTP '
                                           'routing events between publishers and subscribers via standard topics and '
                                           'queues.\n'
                                           '- **Extreme Decoupling**: S/4HANA has zero knowledge of who consumes the '
                                           'event. 1 subscriber, 10 subscribers, or zero subscribers can receive the '
                                           'message without impacting the ERP core.',
                             'key_terms': [   {   'definition': 'Software pattern where systems produce, detect, and '
                                                                'react to state changes in real time.',
                                                  'term': 'Event-Driven Architecture (EDA)'},
                                              {   'definition': 'Managed cloud messaging service on BTP routing events '
                                                                'via queues and topic subscriptions.',
                                                  'term': 'SAP Event Mesh'},
                                              {   'definition': 'Messaging model decoupling publishers from '
                                                                'subscribers via intermediary broker topics.',
                                                  'term': 'Pub-Sub Pattern'}],
                             'step_id': 'd93_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'EDA replaces wasteful polling with real-time Pub-Sub notifications via SAP '
                                         'Event Mesh on BTP.',
                             'title': 'The Event-Driven Architecture (EDA) Revolution'},
                         {   'content_md': '### Standardized Event Formatting\n'
                                           'To guarantee interoperability across cloud providers, SAP adheres to the '
                                           'CNCF (Cloud Native Computing Foundation) **CloudEvents** specification:\n'
                                           '\n'
                                           '#### Anatomy of an SAP CloudEvent:\n'
                                           '```json\n'
                                           '{\n'
                                           '  "specversion": "1.0",\n'
                                           '  "type": "sap.s4.beh.purchaseorder.v1.PurchaseOrder.Created.v1",\n'
                                           '  "source": "/default/sap.s4.beh/NM01",\n'
                                           '  "id": "e7b8c2f1-9821-4f11-a872-98421092a110",\n'
                                           '  "time": "2026-09-17T10:15:30Z",\n'
                                           '  "datacontenttype": "application/json",\n'
                                           '  "data": {\n'
                                           '    "PurchaseOrder": "4500001092"\n'
                                           '  }\n'
                                           '}\n'
                                           '```\n'
                                           'Notice that the event payload contains only the document key '
                                           '(`4500001092`), not the full order details. Consumers use this key to '
                                           'query S/4HANA via OData if they need deeper attributes (Notification '
                                           'Pattern).',
                             'key_terms': [   {   'definition': 'CNCF open industry standard describing event data in '
                                                                'a common, interoperable format.',
                                                  'term': 'CloudEvents'},
                                              {   'definition': 'Filter pattern allowing queues to subscribe to '
                                                                'specific event types (e.g. '
                                                                '`sap/s4/beh/purchaseorder/*`).',
                                                  'term': 'Topic Subscription'}],
                             'step_id': 'd93_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Events follow the CloudEvents specification, carrying event metadata and '
                                         'technical keys for downstream consumption.',
                             'title': 'The CloudEvents Standard & Topic Hierarchies'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'consumers': [   'Vendor Portal (BTP)',
                                                                     'Warehouse Mobile Notification',
                                                                     'CO2 Carbon Tracker Service'],
                                                    'event_type': 'sap.s4.beh.purchaseorder.v1.PurchaseOrder.Created.v1'},
                             'content_md': '### Event-Driven Fan-Out Topology\n'
                                           '```\n'
                                           '[S/4HANA Cloud: Heidelberg NM01]\n'
                                           '             │  Publishes: PurchaseOrder.Created\n'
                                           '             ▼\n'
                                           '    [SAP Event Mesh on BTP]\n'
                                           '             │  Fan-out to 3 independent queues:\n'
                                           '             ├───────────────────────┼───────────────────────┐\n'
                                           '             ▼                       ▼                       ▼\n'
                                           '    [Queue: VendorPortal]    [Queue: MobilePush]     [Queue: '
                                           'CarbonTracker]\n'
                                           '             │                       │                       │\n'
                                           '             ▼                       ▼                       ▼\n'
                                           '   [CAP Portal App]         [Push Notification]     [Sustainability API]\n'
                                           '   (Alerts VEND-101)        (Alerts Warehouse PL01) (Logs sensor RAW-01 '
                                           'CO2)\n'
                                           '```',
                             'scenario': 'When Purchase Order 4500001092 is created at Heidelberg (PL01), three '
                                         'independent consumers react simultaneously.',
                             'step_id': 'd93_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Event Mesh Multi-Consumer Architecture'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'A developer attempts to pack an entire 50-megabyte PDF attachment and '
                                            '1,000 line items directly inside the CloudEvent payload. Diagnose the '
                                            'architectural violation.',
                             'options': [   {   'explanation': 'Correct! Event-driven architecture uses lightweight '
                                                               'event notifications; transferring massive binary '
                                                               'attachments through event brokers breaks messaging '
                                                               'throughput.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Violation: Event payloads must be lean notifications (< 64 '
                                                        'KB) containing only event metadata and technical keys. '
                                                        'Downstream consumers should fetch heavy documents on-demand '
                                                        'via OData APIs.'},
                                            {   'explanation': 'Completely false.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Events should only contain audio recordings.'},
                                            {   'explanation': 'Absurd.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'The message broker will automatically delete S/4HANA.'}],
                             'step_id': 'd93_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Keep event payloads lightweight (< 64 KB); consumers query heavy details '
                                         'on-demand via OData APIs.',
                             'title': 'Event Mesh Simulation: Event Payload Anti-Pattern'},
                         {   'instruction': 'What architectural pattern remediates this bottleneck?',
                             'options': [   {   'explanation': 'Correct! Dead Letter Queues isolate poison messages to '
                                                               'prevent queue head-of-line blocking.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Configure a Dead Letter Queue (DLQ) with a maximum retry '
                                                        'limit (e.g. 5 retries): after 5 failed attempts, the poison '
                                                        'message is automatically moved to the DLQ for offline '
                                                        'analysis, allowing valid orders to flow uninterrupted.'},
                                            {   'explanation': 'Destroys enterprise integration.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Delete all queues and revert to paper mail.'},
                                            {   'explanation': 'Causes silent data corruption.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Turn off error handling so crashes are ignored.'}],
                             'scenario': 'A downstream consumer crashes repeatedly while processing a poisoned '
                                         'message, blocking the Event Mesh queue from processing subsequent valid '
                                         'orders.',
                             'step_id': 'd93_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Resilience Challenge: Dead Letter Queues (DLQ)'},
                         {   'assessment_type': 'simulation',
                             'questions': [   {   'concept_slug': 'event-driven-architecture',
                                                  'explanation': 'EDA provides real-time notifications with zero '
                                                                 'polling waste and decoupled publishers.',
                                                  'id': 'd93_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It enables real-time push notifications '
                                                                             'without polling overhead, achieving '
                                                                             'extreme decoupling between systems.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It turns off user computers when idle.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It replaces the database with text '
                                                                             'files.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It requires no authentication.'}],
                                                  'prompt': 'What is the primary architectural benefit of Event-Driven '
                                                            'Architecture (EDA) over polling-based integrations?',
                                                  'question_id': 'd93_q1'},
                                              {   'concept_slug': 'cloudevents-standard',
                                                  'explanation': 'SAP business events adhere strictly to the '
                                                                 'CloudEvents standard.',
                                                  'id': 'd93_q2',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'CloudEvents'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'HTML5'},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'POSIX'},
                                                                 {'id': 'd', 'is_correct': False, 'text': 'MP3'}],
                                                  'prompt': 'What industry specification governed by the CNCF is '
                                                            'adopted by SAP for structuring business event payloads?',
                                                  'question_id': 'd93_q2'},
                                              {   'concept_slug': 'sap-event-mesh',
                                                  'explanation': 'Queues buffer messages reliably for consumers.',
                                                  'id': 'd93_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Queue (with optional Dead Letter Queue)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Hard drive swap partition'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Desktop recycle bin'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Browser history'}],
                                                  'prompt': 'In SAP Event Mesh, what mechanism buffers messages for a '
                                                            'specific consumer application and isolates poison '
                                                            'messages via retries?',
                                                  'question_id': 'd93_q3'},
                                              {   'concept_slug': 'cloudevents-standard',
                                                  'explanation': 'Notification events carry technical keys for '
                                                                 'on-demand detailed API queries.',
                                                  'id': 'd93_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Lightweight technical keys (e.g. '
                                                                             'PurchaseOrder ID) and metadata, '
                                                                             'prompting consumers to query full '
                                                                             'details on-demand.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'The entire 500-megabyte database table.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'User credit card numbers and passwords.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Video stream recordings.'}],
                                                  'prompt': 'In the Notification Pattern for event-driven systems, '
                                                            'what information is typically carried inside the event '
                                                            'data payload?',
                                                  'question_id': 'd93_q4'}],
                             'step_id': 'd93_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 93 Verification Assessment'},
                         {   'step_id': 'd93_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Mastered Event-Driven Architecture (EDA) using SAP Event Mesh on BTP.\n'
                                           '- Formatted business event payloads conforming to the CloudEvents '
                                           'standard.\n'
                                           '- Designed resilient pub-sub fan-out topologies and Dead Letter Queue '
                                           '(DLQ) policies.',
                             'title': 'Day 93 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd93_s8_completion',
                             
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You know how to publish and route business events. Tomorrow, '
                                           'you will connect S/4HANA to Event Mesh and secure hybrid networks: '
                                           '**S/4HANA Business Events Integration & The SAP Cloud Connector**.',
                             'title': 'Day 93 Complete: Event-Driven Architecture Mastered'}],
            'subtitle': 'Pub-sub messaging, SAP Event Mesh, CloudEvents standard, topic hierarchies, and asynchronous '
                        'business decoupling.',
            'title': 'Event-Driven Architecture with SAP Event Mesh'},
    94: {   'atomic_concepts': ['s4hana-business-events', 'event-enablement-binding', 'cloud-connector'],
            'day_number': 94,
            'estimated_minutes': 60,
            'recommended_mission_slug': None,
            'slug': 's4hana-business-events-integration',
            'steps': [   {   'content_md': '### Emitting Events from the Core\n'
                                           'To publish business events from S/4HANA into SAP Event Mesh, S/4HANA uses '
                                           'the **Enterprise Event Enablement (EEE)** framework.\n'
                                           '\n'
                                           '#### Framework Architecture:\n'
                                           '1. **Event Binding**: Connects an RFC destination targeting the BTP Event '
                                           'Mesh broker.\n'
                                           '2. **Channel Configuration**: Defines the logical channel (e.g. `SAP_EM`) '
                                           'and assigns outbound event topics:\n'
                                           '   - Example: Subscribing channel to topic '
                                           '`sap/s4/beh/purchaseorder/v1/PurchaseOrder/Created/v1`.\n'
                                           '3. **RAP Event Definition**:\n'
                                           '   In modern ABAP Cloud, business events can be declared directly inside a '
                                           'RAP Behavior Definition:\n'
                                           '   ```abap\n'
                                           '   define behavior for ZI_NovaPOHeader\n'
                                           '   {\n'
                                           '     event OrderApproved parameter ZD_POApprovedEvent;\n'
                                           '   }\n'
                                           '   ```\n'
                                           '   When the event is raised in ABAP via `RAISE EVENT`, the framework '
                                           'automatically serializes it to CloudEvents format and dispatches it over '
                                           'the channel.',
                             'key_terms': [   {   'definition': 'S/4HANA framework managing event publishing and '
                                                                'channel bindings to Event Mesh.',
                                                  'term': 'Enterprise Event Enablement (EEE)'},
                                              {   'definition': 'ABAP RAP statement triggering a business event from '
                                                                'within business logic.',
                                                  'term': 'RAISE EVENT'},
                                              {   'definition': 'Configured connection path linking S/4HANA event '
                                                                'sources to an external messaging broker.',
                                                  'term': 'Channel'}],
                             'step_id': 'd94_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'Enterprise Event Enablement and RAP `RAISE EVENT` publish CloudEvents '
                                         'natively from S/4HANA to SAP Event Mesh.',
                             'title': 'Enterprise Event Enablement in S/4HANA'},
                         {   'content_md': '### Secure Hybrid Connectivity Without Inbound Ports\n'
                                           'When integrating SAP BTP with S/4HANA On-Premise or Private Cloud (like '
                                           'Heidelberg `PL01`), security policies strictly forbid opening inbound '
                                           'firewall ports.\n'
                                           '\n'
                                           '#### How the SAP Cloud Connector Works:\n'
                                           '1. **Outbound-Only Reverse Tunnel**:\n'
                                           "   - The Cloud Connector is installed inside the customer's on-premise "
                                           'DMZ.\n'
                                           '   - It establishes a persistent, outbound-only TLS tunnel over port 443 '
                                           "to the customer's BTP Subaccount.\n"
                                           '   - **Zero inbound firewall ports** are opened.\n'
                                           '2. **Virtual-to-Internal Mapping**:\n'
                                           '   - Exposes internal SAP hosts under virtual names (e.g., Virtual: '
                                           '`s4h-heidelberg.virtual:443` -> Internal: `10.140.22.81:44300`).\n'
                                           '3. **Granular URL Whitelisting**:\n'
                                           '   - Administrators strictly whitelist exact URL paths (e.g. only '
                                           '`/sap/opu/odata4/sap/zui_po_manage_o4/`). All other paths are blocked.\n'
                                           '4. **Principal Propagation**:\n'
                                           "   - Securely propagates the cloud user's identity (SAML token) down to "
                                           "the on-premise ABAP system, executing transactions under the user's real "
                                           'personal authorization profile.',
                             'key_terms': [   {   'definition': 'On-premise agent establishing secure outbound '
                                                                'reverse-tunnels to BTP subaccounts.',
                                                  'term': 'SAP Cloud Connector'},
                                              {   'definition': 'Security mechanism forwarding authenticated cloud '
                                                                'user identity to backend systems.',
                                                  'term': 'Principal Propagation'},
                                              {   'definition': 'Network connection initiated outbound from '
                                                                'on-premise, allowing controlled inbound requests.',
                                                  'term': 'Reverse Tunnel'}],
                             'step_id': 'd94_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'The Cloud Connector establishes secure outbound reverse-tunnels with URL '
                                         'whitelisting and Principal Propagation.',
                             'title': 'The SAP Cloud Connector: Secure Reverse Tunnel Architecture'},
                         {   'company_context': {   'cloud_connector_host': 'scc-dmz.novamfg.corp',
                                                    'company_name': 'Nova Manufacturing Corp',
                                                    'virtual_host': 's4h-heidelberg.internal:443',
                                                    'whitelisted_path': '/sap/opu/odata4/sap/zui_po_manage_o4/'},
                             'content_md': '### Complete Secure Tunnel Pipeline\n'
                                           '```\n'
                                           '[BTP Cloud Subaccount: Supplier Portal]\n'
                                           '               │  Destination URL: https://s4h-heidelberg.internal:443\n'
                                           '               ▼  Proxy Type: OnPremise\n'
                                           '[BTP Connectivity Service]\n'
                                           '               │  Mutual TLS over established reverse tunnel\n'
                                           '               ▼\n'
                                           '[Corporate Firewall: Outbound Port 443 ONLY - No Inbound Ports!]\n'
                                           '               │\n'
                                           '               ▼\n'
                                           '[SAP Cloud Connector (Inside Nova DMZ)]\n'
                                           '               │  1. Verifies URL matches whitelist\n'
                                           '               │  2. Translates virtual host -> real IP: '
                                           '10.140.22.81:44300\n'
                                           '               │  3. Converts BTP JWT token into X.509 Short-Lived '
                                           'Certificate\n'
                                           '               ▼\n'
                                           '[S/4HANA Private Cloud: Heidelberg NM01]\n'
                                           "               └── Executes OData V4 query under user 'M_VANCE' with PFCG "
                                           'checks!\n'
                                           '```',
                             'scenario': 'A buyer on the BTP Supplier Portal in the cloud queries purchase order '
                                         'details from the private S/4HANA system in Heidelberg.',
                             'step_id': 'd94_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Secure Hybrid Pipeline: BTP to Heidelberg PL01'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': "A new OData service called from BTP fails with: 'Service execution "
                                            "failed: Access to system denied by Cloud Connector'. Diagnose the issue.",
                             'options': [   {   'explanation': 'Correct! Cloud Connector operates on a zero-trust '
                                                               'model; every URL path must be explicitly whitelisted '
                                                               'before requests are forwarded.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'The new OData service URL path has not been added to the '
                                                        'Accessible Resources Whitelist in the Cloud Connector '
                                                        'administration console.'},
                                            {   'explanation': 'Hardware damage is not the cause of application access '
                                                               'denial.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'The corporate firewall was struck by lightning.'},
                                            {   'explanation': 'Incorrect.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'The database was deleted.'}],
                             'step_id': 'd94_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Cloud Connector denies all requests by default; target URL paths must be '
                                         'explicitly added to the Accessible Resources list.',
                             'title': 'Cloud Connector Technical Audit: Diagnosing HTTP 403 Access Denied'},
                         {   'instruction': 'Why is this a critical audit failure and how do you remediate it?',
                             'options': [   {   'explanation': 'Correct! Principal Propagation guarantees '
                                                               'accountability and enforces individual user '
                                                               'authorizations.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'Critical audit failure: technical users destroy audit '
                                                        'traceability and bypass individual user permissions. '
                                                        'Remediate: configure Principal Propagation in Cloud Connector '
                                                        "and BTP, ensuring transactions are executed under each user's "
                                                        'authenticated personal identity with individual PFCG checks.'},
                                            {   'explanation': 'Violates SAP licensing, fails compliance audits, and '
                                                               'introduces severe security risks.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Approve it because using a single user saves money on user '
                                                        'licenses.'},
                                            {   'explanation': 'Severe compliance violation.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Turn off S/4HANA audit logging so auditors cannot see '
                                                        'RFC_USER.'}],
                             'scenario': 'A junior consultant configures an integration using a hardcoded technical '
                                         'superuser (`RFC_USER` with `SAP_ALL`), so all cloud transactions appear in '
                                         'S/4HANA audit logs as executed by `RFC_USER`.',
                             'step_id': 'd94_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Security Architecture Challenge: Technical User vs Principal Propagation'},
                         {   'assessment_type': 'technical_audit',
                             'questions': [   {   'concept_slug': 'cloud-connector',
                                                  'explanation': 'Cloud Connector establishes an outbound-only TLS '
                                                                 'reverse tunnel over port 443.',
                                                  'id': 'd94_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'By establishing a secure, persistent '
                                                                             'outbound-only TLS reverse tunnel from '
                                                                             'the on-premise network to BTP.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'By turning off the corporate firewall.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'By broadcasting messages over FM radio '
                                                                             'waves.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'By mailing flash drives daily.'}],
                                                  'prompt': 'How does the SAP Cloud Connector establish communication '
                                                            'between SAP BTP and on-premise systems without opening '
                                                            'inbound firewall ports?',
                                                  'question_id': 'd94_q1'},
                                              {   'concept_slug': 's4hana-business-events',
                                                  'explanation': 'Enterprise Event Enablement manages event channel '
                                                                 'publishing in S/4HANA.',
                                                  'id': 'd94_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Enterprise Event Enablement (EEE)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Spool Administrator'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Screen Painter'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Database Backup Utility'}],
                                                  'prompt': 'Which S/4HANA framework is configured to emit standard '
                                                            'business events to external message brokers like SAP '
                                                            'Event Mesh?',
                                                  'question_id': 'd94_q2'},
                                              {   'concept_slug': 'cloud-connector',
                                                  'explanation': 'Principal Propagation forwards logged-in user '
                                                                 'identities for end-to-end auditability.',
                                                  'id': 'd94_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Forwarding the authenticated cloud '
                                                                             "user's identity to the backend system so "
                                                                             "transactions execute under the user's "
                                                                             'personal authorizations and audit '
                                                                             'trail.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Replacing passwords with fingerprints.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Sharing administrative passwords with '
                                                                             'all employees.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Converting user accounts into guest '
                                                                             'accounts.'}],
                                                  'prompt': 'What is Principal Propagation in hybrid SAP integrations?',
                                                  'question_id': 'd94_q3'},
                                              {   'concept_slug': 'event-enablement-binding',
                                                  'explanation': '`RAISE EVENT` triggers RAP business events declared '
                                                                 'in the BDEF.',
                                                  'id': 'd94_q4',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'RAISE EVENT <event_name>'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': "CALL FUNCTION 'POPUP_TO_CONFIRM'"},
                                                                 {'id': 'c', 'is_correct': False, 'text': 'SEND EMAIL'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'FIRE_MESSAGE_ALERT'}],
                                                  'prompt': 'Which ABAP statement in modern RAP behavior '
                                                            'implementations triggers an outbound business event?',
                                                  'question_id': 'd94_q4'}],
                             'step_id': 'd94_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Day 94 Verification Assessment'},
                         {   'step_id': 'd94_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Architectural Mastery Demonstrated:\n'
                                           '- Configured Enterprise Event Enablement and emitted RAP business events '
                                           'via `RAISE EVENT`.\n'
                                           '- Architected secure hybrid connectivity using the SAP Cloud Connector '
                                           'outbound reverse tunnel.\n'
                                           '- Enforced zero-trust security using Accessible Resource whitelists and '
                                           'Principal Propagation.',
                             'title': 'Day 94 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd94_s8_completion',
                             
                             'step_type': 'completion',
                             'summary_md': 'Outstanding! You understand secure hybrid connectivity. Tomorrow, you will '
                                           'synthesize all integration knowledge in the **Phase 8 BTP & Enterprise '
                                           'Integration Capstone**.',
                             'title': 'Day 94 Complete: Business Events & Cloud Connector Mastered'}],
            'subtitle': 'Enterprise event enablement, Cloud Connector reverse tunnels, subaccount binding, and '
                        'principal propagation.',
            'title': 'Secure Connectivity & S/4HANA Event Integration'},
    95: {   'atomic_concepts': ['enterprise-integration-synthesis'],
            'day_number': 95,
            'estimated_minutes': 90,
            'recommended_mission_slug': None,
            'slug': 'btp-integration-capstone',
            'steps': [   {   'content_md': '### Synthesizing the Hybrid Integration Fabric\n'
                                           'In Phase 8, you have mastered the enterprise connectivity foundation '
                                           'powering modern SAP digital landscapes:\n'
                                           '1. **BTP Architecture**: Multi-cloud Subaccounts (AWS, Azure, GCP), Cloud '
                                           'Foundry vs Kyma Kubernetes runtimes, and BTP Destinations.\n'
                                           '2. **Integration Suite & CPI**: Message mediation, adapter protocols '
                                           '(OData, REST, SOAP, SFTP, JMS), and Synchronous vs Asynchronous patterns.\n'
                                           '3. **Payload Transformations**: Message Mappings, Content Modifiers, '
                                           'Content Enricher lookups, and dynamic Apache Groovy scripting.\n'
                                           '4. **Event-Driven Architecture (EDA)**: Pub-sub messaging, SAP Event Mesh, '
                                           'and CloudEvents standard notifications.\n'
                                           '5. **Secure Hybrid Connectivity**: Enterprise Event Enablement (`RAISE '
                                           'EVENT`), Cloud Connector reverse-tunnels, URL whitelisting, and Principal '
                                           'Propagation.\n'
                                           '\n'
                                           '#### The Capstone Challenge:\n'
                                           'Nova Manufacturing Corp is connecting its global robotics supply chain: '
                                           'suppliers in Germany, assembly plants in Heidelberg and Austin, and '
                                           'automated cloud quality services. You must conduct the definitive '
                                           'architectural and security audit of the global hybrid integration fabric.',
                             'key_terms': [   {   'definition': 'Unified architectural fabric connecting on-premise, '
                                                                'private cloud, and SaaS systems via BTP.',
                                                  'term': 'Hybrid Integration Fabric'},
                                              {   'definition': 'Policies ensuring all cross-system communications '
                                                                'adhere to security, scalability, and Clean Core '
                                                                'standards.',
                                                  'term': 'Integration Governance'}],
                             'step_id': 'd95_s1_learn',
                             'step_type': 'learn',
                             'takeaway': 'The Integration Capstone synthesizes BTP runtimes, Cloud Integration iFlows, '
                                         'Event Mesh, and Cloud Connector security.',
                             'title': 'Phase 8 Capstone: Enterprise Integration Architecture'},
                         {   'content_md': '### Pre-Production Integration Audit Checklist\n'
                                           'Before approving an enterprise integration architecture for global '
                                           'go-live, certify four core pillars:\n'
                                           '\n'
                                           '1. **Decoupling & Resilience**:\n'
                                           '   - Are high-volume transactional flows asynchronous using persistent '
                                           'queues (JMS / AMQP)?\n'
                                           '   - Are Dead Letter Queues (DLQ) configured for poison message '
                                           'isolation?\n'
                                           '2. **Security & Zero Trust**:\n'
                                           '   - Are all S/4HANA connections mediated via BTP Destinations and the '
                                           'Cloud Connector?\n'
                                           '   - Is Principal Propagation active for user-driven workflows?\n'
                                           '   - Are zero inbound firewall ports opened to the public internet?\n'
                                           '3. **Clean Core Compliance**:\n'
                                           '   - Are integration flows consuming strictly released APIs (Contract C2 '
                                           'remote APIs / OData V4)?\n'
                                           '   - Are direct database connections (ODBC/JDBC) to core tables completely '
                                           'eliminated?\n'
                                           '4. **Performance & Observability**:\n'
                                           '   - Are event payloads lightweight notifications (< 64 KB)?\n'
                                           '   - Are large XML/CSV files streamed via General Splitters to prevent '
                                           'memory exhaustion?',
                             'key_terms': [   {   'definition': 'Security model assuming all networks are hostile, '
                                                                'requiring mutual TLS, whitelists, and identity '
                                                                'tokens.',
                                                  'term': 'Zero-Trust Integration'},
                                              {   'definition': 'Central oversight ensuring all APIs use released '
                                                                'contracts and standard authentication.',
                                                  'term': 'API Governance'}],
                             'step_id': 'd95_s2_understand',
                             'step_type': 'understand',
                             'takeaway': 'Certify integration readiness across Decoupling, Zero-Trust Security, Clean '
                                         'Core APIs, and Streaming Performance.',
                             'title': 'The Architectural Integration Audit Checklist'},
                         {   'company_context': {   'company_name': 'Nova Manufacturing Corp',
                                                    'landscape': 'S/4HANA Private Cloud (Heidelberg) + S/4HANA Public '
                                                                 'Cloud (Austin) + SAP BTP',
                                                    'status': 'Ready for Audit'},
                             'content_md': '### Master Hybrid Integration Blueprint\n'
                                           '```\n'
                                           '[External World: Vendors (VEND-101), Customers, EDI Networks]\n'
                                           '                     │  HTTPS / OAuth2\n'
                                           '                     ▼\n'
                                           '[SAP BTP: API Management & Cloud Integration (CPI)]\n'
                                           '  ├── iFlow: Inbound EDI855 Confirmation -> Groovy Validation\n'
                                           '  ├── Content Enricher: Resolves Tax Codes via S/4HANA API\n'
                                           '  └── Asynchronous JMS Buffer: Retries on downstream outages\n'
                                           '                     │\n'
                                           '         ┌───────────┴───────────┐\n'
                                           '         ▼                       ▼\n'
                                           '[Event Mesh on BTP]     [SAP Cloud Connector (DMZ)]\n'
                                           '  ├── CloudEvents:        ├── Outbound-only mTLS Reverse Tunnel\n'
                                           '  │   PO.Created          ├── URL Whitelist enforced\n'
                                           '  └── Multi-Consumer      └── Principal Propagation (X.509)\n'
                                           '      Fan-Out                    │\n'
                                           '                                 ▼\n'
                                           '                     [S/4HANA Core: Heidelberg PL01]\n'
                                           '                       ├── Releases C1/C2 OData V4 APIs\n'
                                           '                       └── Zero Inbound Firewall Ports!\n'
                                           '```',
                             'scenario': "Review the full-stack hybrid integration fabric uniting Nova's global supply "
                                         'chain.',
                             'step_id': 'd95_s3_visual_example',
                             'step_type': 'visual_example',
                             'title': 'Nova Manufacturing Master Integration Blueprint'},
                         {   'component_type': 'ScenarioDecision',
                             'instruction': 'During an architecture review, an offshore team presents an iFlow that '
                                            'makes 50,000 synchronous HTTP calls in a tight loop to S/4HANA to fetch '
                                            'customer records. Remediate this design.',
                             'options': [   {   'explanation': 'Correct! Looping 50,000 individual synchronous HTTP '
                                                               'requests creates massive latency, network saturation, '
                                                               'and risks gateway timeouts.',
                                                'id': 'a',
                                                'is_correct': True,
                                                'text': 'Replace the 50,000 individual synchronous calls: use an OData '
                                                        'batch request (`$batch`) or an asynchronous bulk delta '
                                                        'extraction, reducing 50,000 network round-trips to a few '
                                                        'optimized requests.'},
                                            {   'explanation': 'Severe design flaw that will crash the application '
                                                               'gateway under load.',
                                                'id': 'b',
                                                'is_correct': False,
                                                'text': 'Approve it and run the loop every 5 minutes.'},
                                            {   'explanation': 'Destructive and absurd.',
                                                'id': 'c',
                                                'is_correct': False,
                                                'text': 'Delete all customer records to make the loop faster.'}],
                             'step_id': 'd95_s4_interactive_practice',
                             'step_type': 'interactive_practice',
                             'takeaway': 'Never execute thousands of individual synchronous HTTP calls in loops; use '
                                         'batching (`$batch`) or bulk delta extraction.',
                             'title': 'Enterprise Integration Audit Simulation'},
                         {   'instruction': 'How do you defend the SAP Integration Suite & BTP architecture?',
                             'options': [   {   'explanation': 'Correct! Integration Suite delivers pre-packaged '
                                                               'content, API security, and Clean Core compliance that '
                                                               'legacy point-to-point tools cannot match.',
                                                'id': 'opt1',
                                                'is_correct': True,
                                                'text': 'SAP Integration Suite is a modern cloud iPaaS providing '
                                                        'pre-built SAP Best Practice integration packages, continuous '
                                                        'security updates, native CloudEvents support, and Clean Core '
                                                        'API integration. On-premise direct database links break on '
                                                        'every S/4HANA upgrade, violate Clean Core, and lack cloud '
                                                        'scalability.'},
                                            {   'explanation': 'Abandons digital transformation and locks the company '
                                                               'in technical debt.',
                                                'id': 'opt2',
                                                'is_correct': False,
                                                'text': 'Agree with the director and stop using the cloud.'},
                                            {   'explanation': 'False; enterprise systems require robust integration.',
                                                'id': 'opt3',
                                                'is_correct': False,
                                                'text': 'Tell the director that integration is no longer necessary.'}],
                             'scenario': "A legacy infrastructure director argues: 'We should keep using our "
                                         '20-year-old on-premise BizTalk server with direct database table links '
                                         "instead of moving to SAP Integration Suite.'",
                             'step_id': 'd95_s5_challenge',
                             'step_type': 'challenge',
                             'title': 'Phase 8 Capstone Defense: Cloud-First Integration Strategy'},
                         {   'assessment_type': 'capstone_quiz',
                             'questions': [   {   'concept_slug': 'enterprise-integration-synthesis',
                                                  'explanation': 'SAP Integration Suite is the strategic enterprise '
                                                                 'iPaaS.',
                                                  'id': 'd95_q1',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'SAP Integration Suite (Cloud '
                                                                             'Integration)'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Classic IDoc Subroutine Pool'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Windows Notepad'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'FTP Command Line'}],
                                                  'prompt': 'What is the premier SAP cloud middleware for '
                                                            'orchestrating end-to-end integration flows across hybrid '
                                                            'and non-SAP environments?',
                                                  'question_id': 'd95_q1'},
                                              {   'concept_slug': 'enterprise-integration-synthesis',
                                                  'explanation': 'Cloud Connector provides outbound-only reverse '
                                                                 'tunneling with strict whitelisting.',
                                                  'id': 'd95_q2',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'It uses an outbound-only TLS reverse '
                                                                             'tunnel, strict URL whitelisting, and '
                                                                             'Principal Propagation with zero inbound '
                                                                             'firewall ports opened.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'It deletes all firewall rules.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'It assigns public IP addresses to '
                                                                             'internal databases.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'It disables SSL encryption.'}],
                                                  'prompt': 'How does the SAP Cloud Connector protect on-premise '
                                                            'systems from external cyber threats while allowing BTP '
                                                            'cloud integration?',
                                                  'question_id': 'd95_q2'},
                                              {   'concept_slug': 'enterprise-integration-synthesis',
                                                  'explanation': 'Asynchronous queuing buffers messages during '
                                                                 'receiver downtime.',
                                                  'id': 'd95_q3',
                                                  'options': [   {   'id': 'a',
                                                                     'is_correct': True,
                                                                     'text': 'Asynchronous integration using '
                                                                             'persistent JMS queues with automated '
                                                                             'retry policies and Dead Letter Queues.'},
                                                                 {   'id': 'b',
                                                                     'is_correct': False,
                                                                     'text': 'Synchronous HTTP calls with zero '
                                                                             'retries.'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Printing transactions on paper.'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Deleting messages on failure.'}],
                                                  'prompt': 'What messaging pattern should be implemented in Cloud '
                                                            'Integration when the receiving system experiences '
                                                            'periodic downtime, to prevent lost business transactions?',
                                                  'question_id': 'd95_q3'},
                                              {   'concept_slug': 'enterprise-integration-synthesis',
                                                  'explanation': 'SAP business events conform to the CloudEvents '
                                                                 'specification.',
                                                  'id': 'd95_q4',
                                                  'options': [   {'id': 'a', 'is_correct': True, 'text': 'CloudEvents'},
                                                                 {'id': 'b', 'is_correct': False, 'text': 'CSV format'},
                                                                 {   'id': 'c',
                                                                     'is_correct': False,
                                                                     'text': 'Binary Core Dump'},
                                                                 {   'id': 'd',
                                                                     'is_correct': False,
                                                                     'text': 'Adobe PostScript'}],
                                                  'prompt': 'What open industry standard format is adopted by SAP '
                                                            'Event Mesh for publishing lightweight real-time business '
                                                            'events?',
                                                  'question_id': 'd95_q4'}],
                             'step_id': 'd95_s6_assessment',
                             'step_type': 'assessment',
                             'title': 'Phase 8 Comprehensive Capstone Assessment'},
                         {   'step_id': 'd95_s7_mastery_evidence',
                             'step_type': 'mastery_evidence',
                             'summary_md': '### Comprehensive Phase 8 Benchmark Achieved:\n'
                                           '- **Hybrid Integration Fabric**: Mastered BTP runtimes, Cloud Integration '
                                           'iFlows, Event Mesh, and Cloud Connector.\n'
                                           '- **Enterprise Decoupling**: Architected asynchronous queuing, Dead Letter '
                                           'Queues, and CloudEvents fan-out patterns.\n'
                                           '- **Zero-Trust Security**: Enforced reverse-tunnel mTLS, URL whitelists, '
                                           'and Principal Propagation.',
                             'title': 'Phase 8 Mastery Evidence & Enterprise Synthesis'},
                         {   'recommended_mission': None,
                             'step_id': 'd95_s8_completion',
                             
                             'step_type': 'completion',
                             'summary_md': 'Congratulations! You have completed Phase 8: SAP BTP & Enterprise '
                                           'Integration. You now possess world-class enterprise integration '
                                           'engineering skills. In **Phase 9 (Days 96–100)**, you will embark on the '
                                           'ultimate program milestone: **The Enterprise Capstone Project & '
                                           'Architectural Defense**.',
                             'title': 'Phase 8 Complete: BTP & Enterprise Integration Certified'}],
            'subtitle': 'Phase 8 benchmark: end-to-end hybrid architecture audit, API security, and integration '
                        'defense.',
            'title': 'Enterprise Integration Capstone & Challenge'}}
