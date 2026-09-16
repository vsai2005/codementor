"use client";

import React, { useState } from "react";

export interface O2CStage {
  stage_id: string;
  stage_number: number;
  name: string;
  sap_transaction: string;
  primary_table: string;
  responsible_role: string;
  document_example: string;
  accounting_impact: string;
  description: string;
}

const O2C_STAGES: O2CStage[] = [
  {
    stage_id: "inquiry",
    stage_number: 1,
    name: "Customer Inquiry & Quotation",
    sap_transaction: "VA11 / VA21 (Manage Sales Quotations)",
    primary_table: "VBAK / VBAP (Doc Type QT)",
    responsible_role: "SAP_BR_INTERNAL_SALES_REP",
    document_example: "Quotation #20000412 (30x DXTR-1000 for CUST-501)",
    accounting_impact: "Zero FI posting.",
    description: "Commercial inquiry from Nordics Industrial AB (CUST-501). Pricing condition technique computes gross price, volume discount, and freight.",
  },
  {
    stage_id: "order",
    stage_number: 2,
    name: "Sales Order Processing",
    sap_transaction: "VA01 / Create Sales Orders",
    primary_table: "VBAK (Header) / VBAP (Item)",
    responsible_role: "SAP_BR_INTERNAL_SALES_REP",
    document_example: "Sales Order #10042 (Confirmed Delivery Date 2026-09-20)",
    accounting_impact: "Zero FI posting (Commitment on customer credit limit via SAP Credit Management).",
    description: "Customer accepts quotation. Sales order is created under Sales Org SO01. Automated aATP check confirms stock availability at Plant PL01.",
  },
  {
    stage_id: "delivery",
    stage_number: 3,
    name: "Outbound Delivery & Picking",
    sap_transaction: "VL01N / Manage Outbound Deliveries",
    primary_table: "LIKP (Header) / LIPS (Item)",
    responsible_role: "SAP_BR_SHIPPING_SPECIALIST",
    document_example: "Outbound Delivery #80019 (Shipping Point Heidelberg)",
    accounting_impact: "Zero FI posting.",
    description: "Delivery document generated based on shipping conditions. Warehouse picks 30 units of DXTR-1000 from Storage Location FG01 into handling units.",
  },
  {
    stage_id: "pgi",
    stage_number: 4,
    name: "Post Goods Issue (PGI)",
    sap_transaction: "VL02N / Post Goods Issue (Movement 601)",
    primary_table: "MATDOC + LIKP",
    responsible_role: "SAP_BR_WAREHOUSE_CLERK",
    document_example: "Material Doc #490001 (Stock balance reduced by 30 EA)",
    accounting_impact: "Debit Cost of Goods Sold COGS (500000) €25,500 | Credit Finished Goods Inventory (132000) €25,500 in ACDOCA.",
    description: "Freight carrier departs plant dock. Inventory title transfers to customer. Inventory decreases and COGS is recognized synchronously.",
  },
  {
    stage_id: "billing",
    stage_number: 5,
    name: "Customer Billing (VF01)",
    sap_transaction: "VF01 / Create Billing Documents",
    primary_table: "VBRK (Header) / VBRP (Item)",
    responsible_role: "SAP_BR_BILLING_CLERK",
    document_example: "Billing Document #900055 (€42,000 + 19% VAT = €49,980)",
    accounting_impact: "Debit Customer AR CUST-501 (121000) €49,980 | Credit Sales Revenue (410000) €42,000 + Credit Output Tax (217000) €7,980 in ACDOCA.",
    description: "Commercial invoice generated. Revenue account determination (VKOA key ERL) maps pricing condition PR00 directly to General Ledger revenue.",
  },
  {
    stage_id: "payment",
    stage_number: 6,
    name: "Incoming Payment & Clearing",
    sap_transaction: "F-28 / Post Incoming Payments",
    primary_table: "BSID (Open) -> BSAD (Cleared) via ACDOCA",
    responsible_role: "SAP_BR_AR_ACCOUNTANT",
    document_example: "Bank Payment #100021 (Bank Wire Transfer €49,980)",
    accounting_impact: "Debit Bank Account (113100) €49,980 | Credit Customer AR CUST-501 (121000) €49,980 in ACDOCA.",
    description: "Customer remittance received via electronic bank feed. Customer open item in ACDOCA is cleared with zero remaining balance.",
  },
];

interface O2CFlowProps {
  title?: string;
  instruction?: string;
}

export function O2CFlow({
  title = "Order-to-Cash (O2C) End-to-End Flow Tracer",
  instruction = "Follow the complete commercial lifecycle of a customer order at Nova Manufacturing. Inspect how Sales, Shipping, Inventory, and Financial Accounting integrate seamlessly through table VBFA and ACDOCA.",
}: O2CFlowProps) {
  const [selectedStageId, setSelectedStageId] = useState<string>("order");
  const [quizAnswer, setQuizAnswer] = useState<string>("");
  const [quizEvaluated, setQuizEvaluated] = useState<boolean>(false);

  const activeStage = (O2C_STAGES.find((s) => s.stage_id === selectedStageId) || O2C_STAGES[1])!;

  const handleResetQuiz = () => {
    setQuizEvaluated(false);
    setQuizAnswer("");
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-indigo-200 text-indigo-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] O2C LIFECYCLE
            </span>
            <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-ink">
              Company: NM01 • Sales Org: SO01
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="text-xs font-mono font-bold bg-surface-raised border border-ink p-1.5">
          Customer: <span className="text-indigo-700">CUST-501 (Nordics Industrial AB)</span>
        </div>
      </div>

      {/* Horizontal Stage Pipeline */}
      <div
        role="tablist"
        aria-label="O2C Process Stages"
        className="flex items-center gap-2 overflow-x-auto pb-2 mb-5 scrollbar-thin"
      >
        {O2C_STAGES.map((stg) => {
          const isSelected = stg.stage_id === selectedStageId;
          return (
            <button
              key={stg.stage_id}
              type="button"
              role="tab"
              aria-selected={isSelected}
              onClick={() => setSelectedStageId(stg.stage_id)}
              className={`min-w-[150px] p-3 text-left border-2 border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink shrink-0 ${
                isSelected
                  ? "bg-amber-100 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] border-amber-900 scale-[1.02]"
                  : "bg-surface hover:bg-surface-raised"
              }`}
            >
              <div className="flex items-center justify-between text-[10px] font-mono font-bold mb-1">
                <span>Stage {stg.stage_number}</span>
                <span className="px-1 py-0.2 border bg-surface-raised text-ink text-[9px]">
                  {stg.stage_id.toUpperCase()}
                </span>
              </div>
              <div className="text-xs font-black text-ink truncate">{stg.name}</div>
              <div className="text-[10px] text-muted font-mono mt-1 truncate">
                T-Code: {stg.sap_transaction.split("/")[0]}
              </div>
            </button>
          );
        })}
      </div>

      {/* Stage Detail Inspector */}
      <div className="border-2 border-ink bg-surface-raised p-4 mb-5 space-y-3">
        <div className="flex flex-wrap items-center justify-between border-b border-ink/30 pb-3 gap-2">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 text-xs font-mono font-bold border bg-indigo-100 text-indigo-900 border-indigo-400">
                Stage {activeStage.stage_number} of 6
              </span>
              <h4 className="text-base font-black text-ink">{activeStage.name}</h4>
            </div>
            <div className="text-xs text-muted font-mono mt-1">
              Fiori App / T-Code: <strong>{activeStage.sap_transaction}</strong> • Table: <strong>{activeStage.primary_table}</strong>
            </div>
          </div>

          <div className="font-mono text-xs text-right">
            <span className="text-[10px] text-muted uppercase block">Responsible Role</span>
            <span className="font-bold text-indigo-900 bg-indigo-50 border border-indigo-200 px-1.5 py-0.5">
              {activeStage.responsible_role}
            </span>
          </div>
        </div>

        <p className="text-xs text-ink leading-relaxed font-medium">
          {activeStage.description}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
          <div className="p-3 border border-ink bg-surface">
            <span className="text-[10px] text-muted uppercase block font-bold mb-1">
              Simulated Commercial Document
            </span>
            <span className="font-bold text-ink">{activeStage.document_example}</span>
          </div>

          <div className="p-3 border border-ink bg-surface">
            <span className="text-[10px] text-muted uppercase block font-bold mb-1">
              Financial & Valuation Posting (ACDOCA)
            </span>
            <span className="font-bold text-indigo-950">{activeStage.accounting_impact}</span>
          </div>
        </div>
      </div>

      {/* Practice Challenge */}
      <div className="border-2 border-ink bg-surface p-4">
        <fieldset>
          <legend className="text-xs font-mono font-bold uppercase text-ink mb-2">
            Verification Challenge: PGI vs Billing Accounting Decoupling
          </legend>
          <p className="text-xs text-ink mb-3 font-medium">
            In SAP S/4HANA Order-to-Cash, why does <strong>Post Goods Issue (PGI)</strong> trigger a financial posting to Cost of Goods Sold (COGS), while revenue is recognized later during <strong>Billing (VF01)</strong>?
          </p>

          <div className="space-y-2 mb-3">
            {[
              {
                id: "ans_a",
                text: "Because PGI reflects the physical reduction of company inventory assets (matching principle for cost), while billing creates the legal claim on the customer (accounts receivable and sales revenue recognition).",
                correct: true,
              },
              {
                id: "ans_b",
                text: "Because the billing clerk forgets to press the 'Post' button until the customer calls customer support.",
                correct: false,
              },
              {
                id: "ans_c",
                text: "Because revenue cannot be recognized until the company pays all of its supplier invoices.",
                correct: false,
              },
            ].map((opt) => (
              <label
                key={opt.id}
                className={`flex items-start gap-2.5 p-2.5 border border-ink cursor-pointer text-xs font-medium transition-all focus-within:ring-2 focus-within:ring-ink ${
                  quizAnswer === opt.id
                    ? "bg-ink text-surface font-bold"
                    : "bg-surface-raised hover:bg-surface text-ink"
                }`}
              >
                <input
                  type="radio"
                  name="o2c_flow_quiz"
                  value={opt.id}
                  checked={quizAnswer === opt.id}
                  disabled={quizEvaluated}
                  onChange={() => setQuizAnswer(opt.id)}
                  className="mt-0.5 accent-indigo-600"
                />
                <span>{opt.text}</span>
              </label>
            ))}
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setQuizEvaluated(true)}
                disabled={!quizAnswer || quizEvaluated}
                className="border-2 border-ink bg-indigo-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-indigo-300 disabled:opacity-50"
              >
                Check Answer
              </button>
              {quizEvaluated && (
                <button
                  type="button"
                  onClick={handleResetQuiz}
                  className="border border-ink bg-surface px-3 py-1.5 text-xs font-mono font-bold text-ink hover:bg-surface-raised"
                >
                  Reset ↻
                </button>
              )}
            </div>

            {quizEvaluated && (
              <div
                role="alert"
                className={`text-xs font-bold px-3 py-1 border ${
                  quizAnswer === "ans_a"
                    ? "bg-emerald-100 text-emerald-900 border-emerald-400"
                    : "bg-rose-100 text-rose-900 border-rose-400"
                }`}
              >
                {quizAnswer === "ans_a"
                  ? "✓ Correct! PGI records inventory expense, while Billing establishes customer receivable."
                  : "✗ Incorrect. Review the accounting matching principle governing delivery vs invoicing."}
              </div>
            )}
          </div>
        </fieldset>
      </div>
    </div>
  );
}
