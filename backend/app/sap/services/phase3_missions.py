"""Authoritative Phase 3 Enterprise Missions (Days 23–44).

12 cross-concept enterprise missions covering Procure-to-Pay, Order-to-Cash,
Financial Accounting, and Discrete Manufacturing at Nova Manufacturing Corp (NM01).
"""

from __future__ import annotations
from typing import Any
from app.models.sap_models import SAPMissionType

PHASE_3_SEED_MISSIONS: list[dict[str, Any]] = [

    # 1. P2P Workflow Incident
    {
        "slug": "nova-p2p-workflow-incident",
        "title": "Procure-to-Pay Workflow & Account Assignment Incident",
        "description": "Resolve a high-priority procurement block for factory maintenance tools at Plant PL01. Fix an Account Assignment Category mismatch and clear a managerial approval deadlock.",
        "mission_type": SAPMissionType.TROUBLESHOOTING.value,
        "difficulty": 3,
        "estimated_minutes": 25,
        "related_days": [23, 24, 25, 28],
        "concept_slugs": ["p2p-pr-creation", "account-assignment-categories", "flexible-workflow"],
        "prerequisite_concepts": [
            "p2p-invoice-verification-miro",
            "p2p-goods-receipt-migo",
            "three-tier-architecture",
            "module-interconnectivity",
        ],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "A critical assembly line calibration sensor broke at Plant PL01. Maintenance submitted an emergency PR, but it is blocked in workflow due to an incorrect account assignment category."
        },
        "initial_state_patch": {"pr_workflow_status": "BLOCKED_ON_AAC", "plant": "PL01"},
        "target_state_criteria": {
            "pr_workflow_status": "APPROVED_TRANSMITTED",
            "aac_corrected": True
        },
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Consumable non-stock items require Account Assignment Category 'K' (Cost Center).",
                    "A blank AAC causes the system to treat the item as inventory asset, requiring storage location stock tracking.",
                    "Flexible Workflow evaluates the total net value and triggers approval based on purchasing group."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {
                "allow_hints": True,
                "hints": ["Check why the maintenance tool was rejected by warehouse stock valuation."],
                "show_prerequisite_primer": False,
            },
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "p2p_inc_step1",
                "title": "1. Diagnose Requisition Rejection",
                "step_type": "decision",
                "instruction": "Inspect rejected PR #10004599. The warehouse clerk rejected the requisition stating 'We do not hold non-standard maintenance tools in balance sheet stock'. What is the error?",
                "options": [
                    {
                        "id": "opt_a",
                        "label": "The PR was created with a blank Account Assignment Category, incorrectly forcing warehouse inventory capitalization instead of AAC 'K' (Cost Center).",
                        "is_correct": True,
                        "explanation": "Correct! AAC 'K' expenses the tool directly to Cost Center CC-MAINT-01 upon receipt."
                    },
                    {
                        "id": "opt_b",
                        "label": "The maintenance engineer entered their home address.",
                        "is_correct": False,
                        "explanation": "Incorrect."
                    }
                ],
                "expected_state_patch": {"aac_identified": True}
            },
            {
                "step_id": "p2p_inc_step2",
                "title": "2. Correct Account Assignment & Re-route Workflow",
                "step_type": "decision",
                "instruction": "Re-configure PR #10004599 with Account Assignment Category 'K'. Which cost object and G/L account must be assigned?",
                "options": [
                    {
                        "id": "opt_k_assign",
                        "label": "Assign Cost Center CC-MAINT-01 and G/L Account 541000 (Maintenance Tools Expense).",
                        "is_correct": True,
                        "explanation": "Correct! Consumables require cost center and expense account assignments."
                    },
                    {
                        "id": "opt_bad_assign",
                        "label": "Assign Customer AR reconciliation account 121000.",
                        "is_correct": False,
                        "explanation": "Incorrect. 121000 is for customer sales receivables."
                    }
                ],
                "expected_state_patch": {"pr_workflow_status": "APPROVED_TRANSMITTED", "aac_corrected": True}
            }
        ]
    },

    # 2. Sourcing RFQ Decision
    {
        "slug": "nova-sourcing-rfq-decision",
        "title": "Operational Sourcing & Landed Cost Optimization",
        "description": "Compare competing supplier quotations for precision lenses. Evaluate effective price factoring in Incoterms, freight surcharges, and customs duties.",
        "mission_type": SAPMissionType.ARCHITECTURE_DECISION.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [24],
        "concept_slugs": ["p2p-sourcing-rfq", "source-determination"],
        "prerequisite_concepts": ["p2p-pr-creation"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "Nova requires 500 optical lenses for DXTR-1000. Two certified vendors submitted bids with differing freight terms and payment discounts."
        },
        "initial_state_patch": {"sourcing_status": "QUOTES_RECEIVED"},
        "target_state_criteria": {"awarded_vendor": "VEND-101", "contract_established": True},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Evaluate Effective Price = Gross Price - Discounts + Freight + Duties.",
                    "Incoterm DDP means seller pays freight and duty; EXW means buyer pays freight and duty."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {"allow_hints": True, "hints": ["Calculate total landed cost per unit."], "show_prerequisite_primer": False},
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "rfq_step1",
                "title": "1. Landed Cost Calculation",
                "step_type": "decision",
                "instruction": "Vendor A bids €100/EA EXW (+€15 freight + 5% duty). Vendor B (VEND-101) bids €110/EA DDP (delivered, zero freight, zero duty) with 2% cash discount. Which vendor has the lower effective price?",
                "options": [
                    {
                        "id": "opt_vend_b",
                        "label": "Vendor B (VEND-101) has an effective unit cost of €107.80 vs Vendor A's €120.00 landed cost.",
                        "is_correct": True,
                        "explanation": "Correct! Vendor B's DDP terms and cash discount yield a lower total landed cost."
                    },
                    {
                        "id": "opt_vend_a",
                        "label": "Vendor A because €100 gross is lower than €110.",
                        "is_correct": False,
                        "explanation": "Incorrect. Ignores €15 freight and 5% customs duties."
                    }
                ],
                "expected_state_patch": {"awarded_vendor": "VEND-101", "contract_established": True}
            }
        ]
    },

    # 3. 3-Way Match Investigation
    {
        "slug": "nova-invoice-3way-match-investigation",
        "title": "Logistics Invoice 3-Way Match & Variance Release",
        "description": "Investigate a blocked supplier invoice with Payment Block 'R'. Audit PO contracted price vs GR received quantity vs vendor bill in transaction MRBR.",
        "mission_type": SAPMissionType.TROUBLESHOOTING.value,
        "difficulty": 2,
        "estimated_minutes": 25,
        "related_days": [26, 27],
        "concept_slugs": ["three-way-matching", "p2p-invoice-verification-miro", "gr-ir-clearing-account"],
        "prerequisite_concepts": ["p2p-goods-receipt-migo"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "Invoice #5105600114 from VEND-101 is blocked from payment. Finance cannot disburse cash until the price discrepancy is resolved."
        },
        "initial_state_patch": {"invoice_block_status": "BLOCKED_R", "tolerance_key": "PP"},
        "target_state_criteria": {"invoice_block_status": "RELEASED_FREE", "mrbr_executed": True},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Check Tolerance Key PP (Price Variance) vs Tolerance Key DQ (Quantity Variance).",
                    "Transaction MRBR is used to release blocked invoices after buyer approval."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {"allow_hints": True, "hints": ["Inspect PO item history in EKBE."], "show_prerequisite_primer": False},
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "match_step1",
                "title": "1. Identify Tolerance Key Violation",
                "step_type": "decision",
                "instruction": "PO specified €150.00/EA. Invoice billed €175.00/EA (+16.7%). Company upper limit is 5%. Why is payment blocked?",
                "options": [
                    {
                        "id": "opt_pp_breached",
                        "label": "Tolerance Key PP (Price Variance) exceeded configured threshold; S/4HANA assigned Payment Block 'R'.",
                        "is_correct": True,
                        "explanation": "Correct! Price variance breached the 5% tolerance limit."
                    },
                    {
                        "id": "opt_dq_breached",
                        "label": "The vendor shipped zero items.",
                        "is_correct": False,
                        "explanation": "Incorrect. Goods were physically received."
                    }
                ],
                "expected_state_patch": {"variance_explained": True}
            },
            {
                "step_id": "match_step2",
                "title": "2. Resolve Variance and Release via MRBR",
                "step_type": "decision",
                "instruction": "Procurement confirms the vendor had contractual authorization for an emergency surcharge. How should AP release the invoice?",
                "options": [
                    {
                        "id": "opt_mrbr_release",
                        "label": "Execute transaction MRBR (Release Blocked Invoices), select Invoice #5105600114, and execute 'Release Manually'.",
                        "is_correct": True,
                        "explanation": "Correct! MRBR removes Block 'R' and allows payment."
                    },
                    {
                        "id": "opt_cancel_vendor",
                        "label": "Delete the vendor master record.",
                        "is_correct": False,
                        "explanation": "Absurd distractor."
                    }
                ],
                "expected_state_patch": {"invoice_block_status": "RELEASED_FREE", "mrbr_executed": True}
            }
        ]
    },

    # 4. F110 Payment Exception Run
    {
        "slug": "nova-f110-payment-exception-run",
        "title": "Automated Payment Program (F110) Exception Recovery",
        "description": "Execute a corporate treasury payment run. Investigate payment proposal exception list items and generate ISO 20022 XML bank clearing files.",
        "mission_type": SAPMissionType.PROCESS_TASK.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [28, 36],
        "concept_slugs": ["p2p-f110-payment-run", "payment-block-exceptions"],
        "prerequisite_concepts": ["three-way-matching"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "Weekly payment run 20260925-NM01 halted with 3 vendor invoices in the exception list due to missing bank information."
        },
        "initial_state_patch": {"f110_status": "PROPOSAL_EXCEPTIONS", "exceptions_count": 3},
        "target_state_criteria": {"f110_status": "PAYMENT_RUN_COMPLETED", "exceptions_cleared": True},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Check the Payment Proposal Exception List in F110.",
                    "Missing IBAN/SWIFT in Business Partner master prevents electronic payment file generation."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {"allow_hints": True, "hints": ["Maintain BP bank details and regenerate proposal."], "show_prerequisite_primer": False},
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "f110_step1",
                "title": "1. Resolve Exception List Error 006",
                "step_type": "decision",
                "instruction": "Invoice #190000441 for VEND-101 failed with Error 006 'No valid bank details'. What is the fix?",
                "options": [
                    {
                        "id": "opt_bp_fix",
                        "label": "Maintain the verified IBAN and SWIFT code in the Business Partner record (transaction BP) under Company Code NM01 vendor payment transactions, then delete and recreate the F110 proposal.",
                        "is_correct": True,
                        "explanation": "Correct! Maintaining BP bank details allows F110 to generate the payment medium."
                    },
                    {
                        "id": "opt_write_check",
                        "label": "Mail an envelope of cash.",
                        "is_correct": False,
                        "explanation": "Severe audit violation."
                    }
                ],
                "expected_state_patch": {"f110_status": "PAYMENT_RUN_COMPLETED", "exceptions_cleared": True}
            }
        ]
    },

    # 5. O2C Order Fulfillment Crisis
    {
        "slug": "nova-o2c-order-fulfillment-crisis",
        "title": "Order-to-Cash Fulfillment & Credit Limit Crisis",
        "description": "A rush order from key client Nordics Industrial AB (CUST-501) is blocked by FSCM Credit Management and an unassigned Shipping Point. Resolve blocks to dispatch goods.",
        "mission_type": SAPMissionType.TROUBLESHOOTING.value,
        "difficulty": 2,
        "estimated_minutes": 25,
        "related_days": [30, 32],
        "concept_slugs": ["o2c-sales-order-creation", "credit-management", "shipping-point-determination"],
        "prerequisite_concepts": ["o2c-pricing-procedure"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "Sales Order #10042 is blocked. Delivery trucks cannot be loaded until credit and shipping point blocks are cleared."
        },
        "initial_state_patch": {"order_status": "BLOCKED_CREDIT_AND_SHP"},
        "target_state_criteria": {"order_status": "RELEASED_DELIVERY_CREATED"},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "FSCM Credit Manager reviews credit exposure vs limit.",
                    "Shipping point determination requires Shipping Condition + Loading Group + Plant."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {"allow_hints": True, "hints": ["Check credit case release and table TVSTZ."], "show_prerequisite_primer": False},
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "o2c_fsm_step1",
                "title": "1. Release FSCM Credit Block",
                "step_type": "decision",
                "instruction": "Customer CUST-501 is €2,000 over their credit limit, but paid an earlier invoice that has not yet cleared in bank feeds. How should the Credit Manager proceed?",
                "options": [
                    {
                        "id": "opt_credit_release",
                        "label": "Verify the incoming bank remittance confirmation and approve a documented credit exception in Fiori app 'Manage Credit Cases' to release the delivery block.",
                        "is_correct": True,
                        "explanation": "Correct! Documented credit case approval adheres to financial governance."
                    },
                    {
                        "id": "opt_cancel_order",
                        "label": "Cancel the customer contract immediately.",
                        "is_correct": False,
                        "explanation": "Damages key customer relationship."
                    }
                ],
                "expected_state_patch": {"credit_released": True}
            },
            {
                "step_id": "o2c_fsm_step2",
                "title": "2. Resolve Shipping Point Determination",
                "step_type": "decision",
                "instruction": "Delivery creation fails because Shipping Point could not be determined. What configuration link is required?",
                "options": [
                    {
                        "id": "opt_tvstz_link",
                        "label": "Map Shipping Condition 01 + Loading Group 0001 + Plant PL01 to Shipping Point 1000 in configuration.",
                        "is_correct": True,
                        "explanation": "Correct! Standard shipping point determination rule."
                    },
                    {
                        "id": "opt_bad_shp",
                        "label": "Change customer address to Berlin.",
                        "is_correct": False,
                        "explanation": "Incorrect."
                    }
                ],
                "expected_state_patch": {"order_status": "RELEASED_DELIVERY_CREATED"}
            }
        ]
    },

    # 6. aATP Allocation Conflict
    {
        "slug": "nova-atp-allocation-conflict",
        "title": "Advanced ATP & Alternative-Based Sourcing Conflict",
        "description": "Heidelberg Plant PL01 has an unexpected stock shortage of DXTR-1000. Configure Alternative-Based Confirmation (ABC) to route fulfillment through Austin Plant PL02.",
        "mission_type": SAPMissionType.CONFIGURATION.value,
        "difficulty": 3,
        "estimated_minutes": 25,
        "related_days": [31],
        "concept_slugs": ["advanced-atp-s4", "product-allocation", "backorder-processing"],
        "prerequisite_concepts": ["o2c-sales-order-creation"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "Customer CUST-501 needs 40 controllers. PL01 has only 20 available. PL02 in Austin has 25 available."
        },
        "initial_state_patch": {"pl01_deficit": 20, "confirmation_rate": "50%"},
        "target_state_criteria": {"confirmation_rate": "100%", "abc_enabled": True},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Alternative-Based Confirmation (ABC) evaluates substitute delivering plants.",
                    "Split delivery creates separate delivery items across multiple plants."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {"allow_hints": True, "hints": ["Enable ABC plant substitution in sales order."], "show_prerequisite_primer": False},
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "atp_step1",
                "title": "1. Configure ABC Substitution",
                "step_type": "decision",
                "instruction": "How should aATP be configured to resolve the 20-unit shortage at Plant PL01?",
                "options": [
                    {
                        "id": "opt_abc_split",
                        "label": "Enable Alternative-Based Confirmation (ABC) with substitution strategy prioritizing Plant PL02 as secondary source, confirming 20 EA from PL01 and 20 EA from PL02.",
                        "is_correct": True,
                        "explanation": "Correct! ABC splits fulfillment across plants to achieve 100% on-time delivery."
                    },
                    {
                        "id": "opt_backorder_lose",
                        "label": "Mark customer as 'Lose' in BOP and cancel their order.",
                        "is_correct": False,
                        "explanation": "Incorrect! Loses a key enterprise customer."
                    }
                ],
                "expected_state_patch": {"confirmation_rate": "100%", "abc_enabled": True}
            }
        ]
    },

    # 7. O2C Billing & FI Reconciliation
    {
        "slug": "nova-o2c-billing-fi-reconciliation",
        "title": "Order-to-Cash Billing & VKOA Account Determination",
        "description": "A batch of customer billing documents is blocked from posting to ACDOCA with error VF051. Diagnose the VKOA account determination error and release the journals via VFX3.",
        "mission_type": SAPMissionType.TROUBLESHOOTING.value,
        "difficulty": 2,
        "estimated_minutes": 25,
        "related_days": [33, 34],
        "concept_slugs": ["o2c-billing-creation", "revenue-recognition-posting", "o2c-post-goods-issue"],
        "prerequisite_concepts": ["shipping-point-determination"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "Export billing documents for Nordics Industrial AB are blocked with status 'Error in Accounting Interface'."
        },
        "initial_state_patch": {"vfx3_blocked_docs": 1, "vkoa_error": "ERL_MISSING"},
        "target_state_criteria": {"vfx3_blocked_docs": 0, "acdoca_posted": True},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Table VKOA maps Account Key ERL to G/L revenue accounts.",
                    "Transaction VFX3 is used to release blocked billing documents."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {"allow_hints": True, "hints": ["Check Chart of Accounts NMCA and Account Key ERL in VKOA."], "show_prerequisite_primer": False},
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "vkoa_step1",
                "title": "1. Fix VKOA Revenue Mapping",
                "step_type": "decision",
                "instruction": "Table VKOA lacked an entry for Account Key ERL under Customer Account Group 'Foreign'. What G/L account should be mapped?",
                "options": [
                    {
                        "id": "opt_gl_revenue",
                        "label": "Map G/L 410000 (Domestic/Foreign Sales Revenue) to Account Key ERL for Sales Org SO01.",
                        "is_correct": True,
                        "explanation": "Correct! Mapping G/L 410000 enables revenue recognition in ACDOCA."
                    },
                    {
                        "id": "opt_gl_cash",
                        "label": "Map Bank Account 113100.",
                        "is_correct": False,
                        "explanation": "Incorrect. Billing credits revenue, not bank cash."
                    }
                ],
                "expected_state_patch": {"vkoa_fixed": True}
            },
            {
                "step_id": "vkoa_step2",
                "title": "2. Release Document in VFX3",
                "step_type": "decision",
                "instruction": "After maintaining VKOA, how does the billing administrator release the blocked invoice into ACDOCA?",
                "options": [
                    {
                        "id": "opt_vfx3_run",
                        "label": "Execute transaction VFX3 (Release Billing Documents for Accounting), select Document #900055, and execute 'Release to Accounting'.",
                        "is_correct": True,
                        "explanation": "Correct! VFX3 re-triggers account determination and posts to ACDOCA."
                    },
                    {
                        "id": "opt_delete_inv",
                        "label": "Delete the invoice and tell the customer it was free.",
                        "is_correct": False,
                        "explanation": "Severe business violation."
                    }
                ],
                "expected_state_patch": {"vfx3_blocked_docs": 0, "acdoca_posted": True}
            }
        ]
    },

    # 8. G/L Period-End Closing
    {
        "slug": "nova-gl-period-end-closing",
        "title": "Financial Closing Cockpit & Valuation Execution",
        "description": "Execute the monthly closing sequence for Company Code NM01: run Asset Depreciation (AFAB), Foreign Currency Valuation (FAGL_FCV), and lock the period in OB52.",
        "mission_type": SAPMissionType.PROCESS_TASK.value,
        "difficulty": 3,
        "estimated_minutes": 25,
        "related_days": [35, 38],
        "concept_slugs": ["period-end-closing", "foreign-currency-valuation", "asset-depreciation-afab"],
        "prerequisite_concepts": ["posting-keys"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "Month 09 is closing. Finance must post asset depreciation, revalue USD receivables, and close the posting period."
        },
        "initial_state_patch": {"closing_status": "PERIOD_OPEN_UNCLOSED"},
        "target_state_criteria": {"closing_status": "PERIOD_CLOSED_OB52", "afab_posted": True, "fcv_posted": True},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "AFAB runs asset depreciation across all plant assets.",
                    "FAGL_FCV revalues foreign currency open items with automated month-start reversal.",
                    "OB52 closes the posting period across all account types."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {"allow_hints": True, "hints": ["Follow the Closing Cockpit checklist in sequence."], "show_prerequisite_primer": False},
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "close_step1",
                "title": "1. Execute Valuation Runs (AFAB & FAGL_FCV)",
                "step_type": "decision",
                "instruction": "Which sequence correctly executes month-end valuations before locking the period?",
                "options": [
                    {
                        "id": "opt_seq_close",
                        "label": "Execute AFAB depreciation run, execute FAGL_FCV foreign exchange revaluation, review GR/IR clearing balances, and lock Period 09 in transaction OB52.",
                        "is_correct": True,
                        "explanation": "Correct! All valuation postings must be completed before locking posting periods in OB52."
                    },
                    {
                        "id": "opt_lock_first",
                        "label": "Lock Period 09 in OB52 first, then try to run AFAB.",
                        "is_correct": False,
                        "explanation": "AFAB will fail with 'Period Closed' error."
                    }
                ],
                "expected_state_patch": {"closing_status": "PERIOD_CLOSED_OB52", "afab_posted": True, "fcv_posted": True}
            }
        ]
    },

    # 9. Inventory Discrepancy Audit
    {
        "slug": "nova-inventory-discrepancy-audit",
        "title": "Inventory Movement Discrepancy & Scrap Audit",
        "description": "Audit physical inventory discrepancies between warehouse Storage Location RAW1 and FG01. Reconcile movement types 311, 301, 551, and 122 in table MATDOC.",
        "mission_type": SAPMissionType.INCIDENT.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [39],
        "concept_slugs": ["simplified-inventory-valuation", "matdoc-table-architecture"],
        "prerequisite_concepts": ["p2p-goods-receipt-migo"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "Physical cycle count reveals a 10-unit discrepancy in optical sensors. You must verify if goods were transferred (311), shipped cross-plant (301), or scrapped (551)."
        },
        "initial_state_patch": {"inventory_audit": "DISCREPANCY_DETECTED"},
        "target_state_criteria": {"inventory_audit": "RECONCILED_MATDOC"},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Movement 311 is storage location transfer (no FI entry).",
                    "Movement 551 writes off damaged stock to Scrap Expense (G/L 590000)."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {"allow_hints": True, "hints": ["Check MATDOC movement records for RAW-01."], "show_prerequisite_primer": False},
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "inv_audit_step1",
                "title": "1. Trace MATDOC Movement History",
                "step_type": "decision",
                "instruction": "Audit log shows 10 sensors were crushed by a forklift. What movement type should be posted to reflect physical reality and recognize the loss?",
                "options": [
                    {
                        "id": "opt_mov_551",
                        "label": "Post Movement Type 551 (Goods Issue for Scrap), debiting Scrap Expense (590000) and crediting Raw Materials Inventory (131000) in ACDOCA.",
                        "is_correct": True,
                        "explanation": "Correct! Movement 551 legally documents physical scrap write-offs."
                    },
                    {
                        "id": "opt_mov_311",
                        "label": "Post Movement 311 to pretend the crushed sensors are in Storage Location FG01.",
                        "is_correct": False,
                        "explanation": "Falsifies finished goods inventory."
                    }
                ],
                "expected_state_patch": {"inventory_audit": "RECONCILED_MATDOC"}
            }
        ]
    },

    # 10. Shopfloor Dispatch Incident
    {
        "slug": "nova-mfg-shopfloor-dispatch-incident",
        "title": "Production Routing & Work Center Capacity Leveling",
        "description": "Work Center WC-ROBOT-01 is overloaded at 145% capacity. Re-level capacity across alternative assembly work centers and release urgent production orders.",
        "mission_type": SAPMissionType.CONFIGURATION.value,
        "difficulty": 2,
        "estimated_minutes": 20,
        "related_days": [40, 41],
        "concept_slugs": ["mfg-work-centers-routing", "capacity-requirements-planning", "production-order-lifecycle"],
        "prerequisite_concepts": ["mfg-bom-master"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "Heidelberg robotic assembly is facing severe queue delays. Orders for DXTR-1000 cannot be released without capacity leveling."
        },
        "initial_state_patch": {"wc_overload": "145%", "orders_stuck": True},
        "target_state_criteria": {"wc_overload": "95%", "orders_stuck": False},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Capacity leveling (transaction CM01 / CM21) redistributes operations across work centers.",
                    "Secondary work center WC-ROBOT-02 has 40 hours of available capacity."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {"allow_hints": True, "hints": ["Reassign operation 0010 to alternative work center."], "show_prerequisite_primer": False},
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "dispatch_step1",
                "title": "1. Capacity Leveling Reassignment",
                "step_type": "decision",
                "instruction": "How should the production planner resolve the 145% overload on WC-ROBOT-01?",
                "options": [
                    {
                        "id": "opt_split_wc",
                        "label": "Use Capacity Leveling (CM01) to split operations and dispatch 30 orders to alternative Work Center WC-ROBOT-02, reducing primary load to 95%.",
                        "is_correct": True,
                        "explanation": "Correct! Dispatching to alternative work centers resolves capacity bottlenecks."
                    },
                    {
                        "id": "opt_ignore_cap",
                        "label": "Force all orders onto WC-ROBOT-01 and let the machine break.",
                        "is_correct": False,
                        "explanation": "Causes equipment breakdown."
                    }
                ],
                "expected_state_patch": {"wc_overload": "95%", "orders_stuck": False}
            }
        ]
    },

    # 11. Production Variance Investigation
    {
        "slug": "nova-mfg-production-variance-investigation",
        "title": "Manufacturing Yield, Scrap & Cost Settlement (KO88)",
        "description": "Investigate a high €3,400 unfavorable variance on Production Order #100888. Audit labor confirmations, component scrap, and execute order settlement to ACDOCA.",
        "mission_type": SAPMissionType.TROUBLESHOOTING.value,
        "difficulty": 3,
        "estimated_minutes": 25,
        "related_days": [41, 42],
        "concept_slugs": ["production-order-confirmation", "production-order-settlement", "wip-variance-calculation"],
        "prerequisite_concepts": ["production-order-lifecycle"],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "Order #100888 shows actual debits of €25,400 against standard credit of €22,000. Finance must settle the €3,400 variance."
        },
        "initial_state_patch": {"order_balance": 3400.0, "settlement_status": "UNSETTLED"},
        "target_state_criteria": {"order_balance": 0.0, "settlement_status": "SETTLED_ACDOCA"},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Order must be set to TECO before settlement can calculate closed manufacturing variances.",
                    "KO88 posts variance to G/L Price Variance (530000) and brings order balance to zero."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {"allow_hints": True, "hints": ["Set status TECO, run variance calculation, and settle via KO88."], "show_prerequisite_primer": False},
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "var_step1",
                "title": "1. Set TECO & Execute KO88 Settlement",
                "step_type": "decision",
                "instruction": "All 100 units are finished and delivered into FG01. How should the cost controller clear the €3,400 order balance?",
                "options": [
                    {
                        "id": "opt_teco_ko88",
                        "label": "Set order status to TECO (Technically Completed) and execute transaction KO88 to settle the €3,400 variance to Price Variance G/L 530000, bringing the order balance in ACDOCA to €0.00.",
                        "is_correct": True,
                        "explanation": "Correct! TECO and KO88 properly settle the variance and balance the order to zero."
                    },
                    {
                        "id": "opt_leave_open",
                        "label": "Leave the order balance open forever.",
                        "is_correct": False,
                        "explanation": "Violates monthly financial close rules."
                    }
                ],
                "expected_state_patch": {"order_balance": 0.0, "settlement_status": "SETTLED_ACDOCA"}
            }
        ]
    },

    # 12. E2E Enterprise Cross-Module Recovery
    {
        "slug": "nova-e2e-enterprise-cross-module-recovery",
        "title": "End-to-End Cross-Module Enterprise Recovery Case",
        "description": "Recover an enterprise client lifecycle spanning Sales, Production, Procurement, and Financial Settlement. Diagnose and resolve cross-functional integration errors.",
        "mission_type": SAPMissionType.CAPSTONE.value,
        "difficulty": 3,
        "estimated_minutes": 30,
        "related_days": [43, 44],
        "concept_slugs": [
            "e2e-process-integration-synthesis",
            "three-way-matching",
            "o2c-billing-creation",
            "production-order-settlement"
        ],
        "prerequisite_concepts": [
            "p2p-f110-payment-run",
            "revenue-recognition-posting",
            "production-order-settlement"
        ],
        "company_context": {
            "company_name": "Nova Manufacturing Corp",
            "company_code": "NM01",
            "scenario": "An integrated enterprise order for 50 robotics controllers is stuck across three modules: raw materials are held at receiving, the production order is blocked, and customer billing failed."
        },
        "initial_state_patch": {"e2e_recovery_status": "MULTIPLE_BLOCKS"},
        "target_state_criteria": {"e2e_recovery_status": "E2E_SYNTHESIS_RECOVERED"},
        "assistance_rules": {
            "TRAINING": {
                "allow_hints": True,
                "hints": [
                    "Follow document flow sequence: P2P Goods Receipt -> Manufacturing Backflush -> Finished Goods Receipt -> O2C PGI -> Customer Billing -> Cost Settlement.",
                    "Verify each invariant: GR/IR clears to zero, PGI books COGS, Billing books Revenue."
                ],
                "show_prerequisite_primer": True,
            },
            "GUIDED": {"allow_hints": True, "hints": ["Resolve upstream procurement before releasing downstream manufacturing and shipping."], "show_prerequisite_primer": False},
            "JOB": {"allow_hints": False, "hints": [], "show_prerequisite_primer": False},
        },
        "steps": [
            {
                "step_id": "e2e_step1",
                "title": "1. Orchestrate Cross-Module Recovery",
                "step_type": "decision",
                "instruction": "What is the mandatory operational sequence to recover the end-to-end customer fulfillment?",
                "options": [
                    {
                        "id": "opt_e2e_seq",
                        "label": "1) Post MIGO Mov 101 to receive raw materials into RAW1; 2) Release production order and confirm operations (Mov 261 & 101); 3) Post PGI Mov 601 to deliver finished goods; 4) Generate Billing Document VF01; 5) Execute KO88 settlement.",
                        "is_correct": True,
                        "explanation": "Correct! Upstream procurement must precede manufacturing consumption, which precedes outbound shipping, billing, and settlement."
                    },
                    {
                        "id": "opt_e2e_bad_seq",
                        "label": "1) Bill the customer; 2) Try to build goods without raw materials; 3) Settle order before release.",
                        "is_correct": False,
                        "explanation": "Completely broken operational sequence violating all enterprise invariants."
                    }
                ],
                "expected_state_patch": {"e2e_recovery_status": "E2E_SYNTHESIS_RECOVERED"}
            }
        ]
    }
]
