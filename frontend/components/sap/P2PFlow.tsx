"use client";

import React, { useState } from "react";

export interface P2PStage {
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

const P2P_STAGES: P2PStage[] = [
  {
    stage_id: "pr",
    stage_number: 1,
    name: "Purchase Requisition",
    sap_transaction: "ME51N / Create Purchase Requisition (Fiori)",
    primary_table: "EBAN",
    responsible_role: "SAP_BR_EMPLOYEE_PROCUREMENT",
    document_example: "PR #10008412 (500x Optical Sensors RAW-01)",
    accounting_impact: "Zero FI posting (Statistical commitment if account assignment is Cost Center / WBS).",
    description: "Internal request from Plant PL01 assembly line supervisor requesting 500 units of RAW-01 for robotic controller assembly.",
  },
  {
    stage_id: "sourcing",
    stage_number: 2,
    name: "Operational Sourcing & RFQ",
    sap_transaction: "ME41 / Manage RFQs",
    primary_table: "EKKO / EKPO (Type AN)",
    responsible_role: "SAP_BR_PURCHASER",
    document_example: "RFQ #60000192 sent to Rheinland Optics (VEND-101)",
    accounting_impact: "Zero FI posting.",
    description: "Purchasing Org PO01 evaluates supplier quotes, confirms lead time (3 days), and selects Rheinland Precision Optics.",
  },
  {
    stage_id: "po",
    stage_number: 3,
    name: "Purchase Order",
    sap_transaction: "ME21N / Manage Purchase Orders",
    primary_table: "EKKO (Header) / EKPO (Item)",
    responsible_role: "SAP_BR_PURCHASER",
    document_example: "PO #4500019820 (500 EA @ €50.00 = €25,000)",
    accounting_impact: "Encumbrance / commitment created; zero General Ledger balance sheet posting.",
    description: "Legally binding commercial contract issued to VEND-101 specifying Plant PL01 delivery and Storage Location RAW1.",
  },
  {
    stage_id: "gr",
    stage_number: 4,
    name: "Goods Receipt (MIGO)",
    sap_transaction: "MIGO / Post Goods Movement (Movement 101)",
    primary_table: "MATDOC (Line Item) + MKPF",
    responsible_role: "SAP_BR_WAREHOUSE_CLERK",
    document_example: "Material Doc #5000018890 (500 EA received into RAW1)",
    accounting_impact: "Debit Inventory (131000) €25,000 | Credit GR/IR Clearing (211200) €25,000 in ACDOCA.",
    description: "Inbound delivery arrived at Plant PL01 dock. Warehouse clerk verified packing slip and accepted stock into unrestricted inventory.",
  },
  {
    stage_id: "invoice",
    stage_number: 5,
    name: "Invoice Verification (MIRO)",
    sap_transaction: "MIRO / Create Supplier Invoice",
    primary_table: "RBKP (Header) / RSEG (Item)",
    responsible_role: "SAP_BR_AP_CLERK_INVOICES",
    document_example: "Supplier Invoice #5105600112 (€25,000 + 19% VAT = €29,750)",
    accounting_impact: "Debit GR/IR Clearing (211200) €25,000 + Debit Input VAT (154000) €4,750 | Credit Vendor AP VEND-101 (211000) €29,750.",
    description: "3-way matching automated check verifies that PO price (€50/EA) matches GR quantity (500 EA) and vendor invoice total.",
  },
  {
    stage_id: "payment",
    stage_number: 6,
    name: "Automatic Payment (F110)",
    sap_transaction: "F110 / Manage Automatic Payments",
    primary_table: "REGUH / REGUP + ACDOCA",
    responsible_role: "SAP_BR_AP_ACCOUNTANT",
    document_example: "Payment Run #20260916-NM01 (SEPA Electronic Transfer)",
    accounting_impact: "Debit Vendor AP VEND-101 (211000) €29,750 | Credit Bank Clearing (113100) €29,750.",
    description: "Periodic payment proposal executes payment run, generating SEPA XML payment media and clearing vendor subledger open items.",
  },
];

interface P2PFlowProps {
  title?: string;
  instruction?: string;
}

export function P2PFlow({
  title = "Procure-to-Pay (P2P) End-to-End Flow Tracer",
  instruction = "Trace the complete transactional sequence from internal requisition to bank payment clearing. Click each stage to inspect underlying database tables, SAP transaction codes, and General Ledger postings.",
}: P2PFlowProps) {
  const [selectedStageId, setSelectedStageId] = useState<string>("po");
  const [quizAnswer, setQuizAnswer] = useState<string>("");
  const [quizEvaluated, setQuizEvaluated] = useState<boolean>(false);

  const activeStage = (P2P_STAGES.find((s) => s.stage_id === selectedStageId) || P2P_STAGES[2])!;

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
            <span className="border border-ink bg-emerald-200 text-emerald-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] P2P LIFECYCLE
            </span>
            <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-ink">
              Company Code: NM01 • Plant: PL01
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="text-xs font-mono font-bold bg-surface-raised border border-ink p-1.5">
          Material: <span className="text-emerald-700">RAW-01 (Optical Sensors)</span>
        </div>
      </div>

      {/* Horizontal Stage Pipeline */}
      <div
        role="tablist"
        aria-label="P2P Process Stages"
        className="flex items-center gap-2 overflow-x-auto pb-2 mb-5 scrollbar-thin"
      >
        {P2P_STAGES.map((stg) => {
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
              <span className="px-2 py-0.5 text-xs font-mono font-bold border bg-emerald-100 text-emerald-900 border-emerald-400">
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
              Simulated Enterprise Document
            </span>
            <span className="font-bold text-ink">{activeStage.document_example}</span>
          </div>

          <div className="p-3 border border-ink bg-surface">
            <span className="text-[10px] text-muted uppercase block font-bold mb-1">
              Financial Accounting (FI) Impact
            </span>
            <span className="font-bold text-emerald-950">{activeStage.accounting_impact}</span>
          </div>
        </div>
      </div>

      {/* Practice Challenge */}
      <div className="border-2 border-ink bg-surface p-4">
        <fieldset>
          <legend className="text-xs font-mono font-bold uppercase text-ink mb-2">
            Verification Challenge: P2P Integration & The GR/IR Invariant
          </legend>
          <p className="text-xs text-ink mb-3 font-medium">
            At Nova Manufacturing, why is the <strong>GR/IR Clearing Account</strong> credited during Goods Receipt (MIGO) rather than posting directly to Accounts Payable?
          </p>

          <div className="space-y-2 mb-3">
            {[
              {
                id: "ans_a",
                text: "Because at Goods Receipt the physical vendor invoice has not yet arrived or been verified. The GR/IR clearing account acts as an interim balance sheet accrual until 3-way matching in MIRO verifies the payable.",
                correct: true,
              },
              {
                id: "ans_b",
                text: "Because SAP S/4HANA automatically debits the company CEO's personal bank account until month-end.",
                correct: false,
              },
              {
                id: "ans_c",
                text: "Because the vendor will only be paid if the purchase order is deleted from table EKKO before midnight.",
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
                  name="p2p_flow_quiz"
                  value={opt.id}
                  checked={quizAnswer === opt.id}
                  disabled={quizEvaluated}
                  onChange={() => setQuizAnswer(opt.id)}
                  className="mt-0.5 accent-emerald-600"
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
                className="border-2 border-ink bg-emerald-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-300 disabled:opacity-50"
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
                  ? "✓ Correct! GR/IR clearing is a mandatory interim balance sheet liability ensuring accrual accounting consistency."
                  : "✗ Incorrect. Review the timing difference between physical goods delivery and vendor invoice receipt."}
              </div>
            )}
          </div>
        </fieldset>
      </div>
    </div>
  );
}
