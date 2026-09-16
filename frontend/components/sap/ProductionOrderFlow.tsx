"use client";

import React, { useState } from "react";

export interface ProdStage {
  stage_id: string;
  stage_number: number;
  title: string;
  tcode: string;
  sap_status: string;
  key_tables: string;
  shopfloor_action: string;
  accounting_impact: string;
  description: string;
}

const PRODUCTION_STAGES: ProdStage[] = [
  {
    stage_id: "creation",
    stage_number: 1,
    title: "1. Order Creation & Scheduling",
    tcode: "CO01 (Create Production Order)",
    sap_status: "CRTD (Created)",
    key_tables: "AFKO (Header) / AFPO (Item) / RESB (Reservations)",
    shopfloor_action: "Production order #100888 generated for 100 units of DXTR-1000 at Plant PL01.",
    accounting_impact: "Planned costs calculated via BOM CS01 and Routing CA01. Zero financial posting.",
    description: "System reads Bill of Materials (BOM) for component reservations and routing operations (Work Center WC-ROBOT-01). Preliminary planned cost matrix generated.",
  },
  {
    stage_id: "release",
    stage_number: 2,
    title: "2. Order Release & Dispatch",
    tcode: "CO02 (Release Order)",
    sap_status: "REL (Released) / PRC (Pre-Costed)",
    key_tables: "JEST (Status Object) / AFKO",
    shopfloor_action: "Material staging lists and shopfloor routing traveler cards printed for production supervisors.",
    accounting_impact: "Commitments activated for reserved components. Zero balance sheet posting.",
    description: "Order status transitions from CRTD to REL. Automatic material availability check confirms optical sensors RAW-01 and microcontrollers are present in warehouse RAW1.",
  },
  {
    stage_id: "goods_issue",
    stage_number: 3,
    title: "3. Material Goods Issue (Backflush)",
    tcode: "MIGO / Movement 261 (or Auto-Backflush)",
    sap_status: "REL / GMPS (Goods Movement Posted)",
    key_tables: "MATDOC + ACDOCA",
    shopfloor_action: "100x RAW-01 Optical Sensors physically transferred from SLoc RAW1 onto the assembly line.",
    accounting_impact: "Debit Order WIP / Consumption (510000) €15,000 | Credit Raw Materials Inventory (131000) €15,000 in ACDOCA.",
    description: "Raw materials are consumed into production order #100888. Inventory is deducted from stock and capitalized into the manufacturing order's Work-in-Process (WIP).",
  },
  {
    stage_id: "confirmation",
    stage_number: 4,
    title: "4. Operation Confirmation",
    tcode: "CO11N (Single Time Ticket Confirmation)",
    sap_status: "CNF (Confirmed)",
    key_tables: "AFRU (Order Confirmations)",
    shopfloor_action: "Technicians log 40 labor hours and 25 machine hours at Work Center WC-ROBOT-01.",
    accounting_impact: "Debit Order WIP (Direct Labor & Machine Overhead) €4,250 | Credit Cost Center CC-PROD-01 Activity Clearing (610000) €4,250.",
    description: "Internal activity allocation transfers cost from manufacturing cost center CC-PROD-01 to production order #100888 based on standard activity rates.",
  },
  {
    stage_id: "goods_receipt",
    stage_number: 5,
    title: "5. Finished Goods Receipt",
    tcode: "MIGO / Movement 101 (Into FG01)",
    sap_status: "DLV (Delivered)",
    key_tables: "MATDOC + ACDOCA + AFPO",
    shopfloor_action: "100 finished DXTR-1000 Robotics Controllers passed QA and placed into warehouse FG01.",
    accounting_impact: "Debit Finished Goods Inventory (132000) €22,000 | Credit Factory Cost Absorption / Order Output (520000) €22,000.",
    description: "Movement type 101 places finished products into unrestricted inventory at standard price (€220/EA). Order balance shows difference between accumulated debits and output credits.",
  },
  {
    stage_id: "teco",
    stage_number: 6,
    title: "6. Technical Completion (TECO)",
    tcode: "CO02 -> Restrict -> Technical Completion",
    sap_status: "TECO (Technically Completed)",
    key_tables: "JEST / AFKO",
    shopfloor_action: "Production execution is locked. Outstanding component reservations are purged.",
    accounting_impact: "Order is closed for shopfloor logistics; ready for Month-End Cost Settlement (KO88).",
    description: "TECO stops any further physical material staging. The cost controller can now run WIP calculation (KKA2), variance calculation (KKS2), and settlement to ACDOCA (KO88).",
  },
];

interface ProductionOrderFlowProps {
  title?: string;
  instruction?: string;
}

export function ProductionOrderFlow({
  title = "S/4HANA Discrete Production Execution Lifecycle",
  instruction = "Follow Production Order #100888 from creation through release, material backflushing (Mov 261), operation confirmation, finished goods receipt (Mov 101), and technical completion (TECO).",
}: ProductionOrderFlowProps) {
  const [activeStageId, setActiveStageId] = useState<string>("goods_issue");
  const [quizAnswer, setQuizAnswer] = useState<string>("");
  const [quizSubmitted, setQuizSubmitted] = useState<boolean>(false);

  const activeStage = (PRODUCTION_STAGES.find((s) => s.stage_id === activeStageId) || PRODUCTION_STAGES[2])!;

  const handleResetQuiz = () => {
    setQuizSubmitted(false);
    setQuizAnswer("");
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-purple-200 text-purple-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] PP-SFC SHOPFLOOR
            </span>
            <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-ink">
              Order: #100888 • Product: DXTR-1000
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="text-xs font-mono bg-surface-raised border border-ink p-1.5">
          Plant: <strong className="text-indigo-700">PL01 (Heidelberg)</strong> | Qty: <strong className="text-ink">100 EA</strong>
        </div>
      </div>

      {/* Stage Flow Navigation */}
      <div
        role="tablist"
        aria-label="Production Stages"
        className="flex items-center gap-2 overflow-x-auto pb-2 mb-4 scrollbar-thin"
      >
        {PRODUCTION_STAGES.map((stg) => {
          const isSelected = stg.stage_id === activeStageId;
          return (
            <button
              key={stg.stage_id}
              type="button"
              role="tab"
              aria-selected={isSelected}
              onClick={() => setActiveStageId(stg.stage_id)}
              className={`min-w-[150px] p-2.5 text-left border-2 border-ink shrink-0 transition-all focus-visible:ring-2 focus-visible:ring-ink ${
                isSelected
                  ? "bg-purple-100 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] border-purple-900 scale-[1.02] font-bold"
                  : "bg-surface hover:bg-surface-raised text-ink"
              }`}
            >
              <div className="flex items-center justify-between text-[10px] font-mono mb-1">
                <span>Stage {stg.stage_number}</span>
                <span className="px-1 border text-[9px] bg-surface font-bold text-ink">{stg.sap_status.split(" ")[0]}</span>
              </div>
              <div className="text-xs font-black truncate">{stg.title.split(". ")[1]}</div>
              <div className="text-[10px] text-muted font-mono truncate">{stg.tcode.split(" ")[0]}</div>
            </button>
          );
        })}
      </div>

      {/* Stage Detail Card */}
      <div className="border-2 border-ink bg-surface-raised p-4 mb-5 space-y-3">
        <div className="flex flex-wrap items-center justify-between border-b border-ink/30 pb-2 gap-2">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 text-xs font-mono font-bold border bg-purple-100 text-purple-950 border-purple-300">
                System Status: {activeStage.sap_status}
              </span>
              <h4 className="text-sm font-black text-ink">{activeStage.title}</h4>
            </div>
            <div className="text-xs font-mono text-muted mt-1">
              Transaction: <strong>{activeStage.tcode}</strong> • Tables: <strong>{activeStage.key_tables}</strong>
            </div>
          </div>
        </div>

        <p className="text-xs text-ink leading-relaxed font-medium">{activeStage.description}</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
          <div className="p-2.5 border border-ink bg-surface">
            <span className="text-[10px] text-muted uppercase block font-bold mb-1">Shopfloor Physical Action</span>
            <div className="text-ink font-bold">{activeStage.shopfloor_action}</div>
          </div>
          <div className="p-2.5 border border-ink bg-surface">
            <span className="text-[10px] text-muted uppercase block font-bold mb-1">Accounting & WIP Impact (ACDOCA)</span>
            <div className="text-indigo-950 font-bold">{activeStage.accounting_impact}</div>
          </div>
        </div>
      </div>

      {/* Practice Challenge */}
      <div className="border-2 border-ink bg-surface p-4">
        <fieldset>
          <legend className="text-xs font-mono font-bold uppercase text-ink mb-2">
            Production Execution Check: Movement 261 vs Movement 101
          </legend>
          <p className="text-xs text-ink mb-3 font-medium">
            In SAP Discrete Manufacturing, what is the accounting difference between <strong>Movement 261 (Goods Issue to Order)</strong> and <strong>Movement 101 (Goods Receipt from Order)</strong>?
          </p>

          <div className="space-y-2 mb-3">
            {[
              {
                id: "ans_wip",
                text: "Movement 261 issues raw materials and charges cost into the order (increasing Order WIP debits), while Movement 101 receives finished goods into inventory (crediting order output at standard cost).",
                correct: true,
              },
              {
                id: "ans_reverse",
                text: "Movement 261 is used to refund money to the customer, while Movement 101 pays supplier invoices.",
                correct: false,
              },
              {
                id: "ans_identical",
                text: "Movement 261 and 101 are identical numbers that do the exact same thing.",
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
                  name="prod_order_quiz"
                  value={opt.id}
                  checked={quizAnswer === opt.id}
                  disabled={quizSubmitted}
                  onChange={() => setQuizAnswer(opt.id)}
                  className="mt-0.5 accent-purple-600"
                />
                <span>{opt.text}</span>
              </label>
            ))}
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setQuizSubmitted(true)}
                disabled={!quizAnswer || quizSubmitted}
                className="border-2 border-ink bg-purple-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-purple-300 disabled:opacity-50"
              >
                Check Answer
              </button>
              {quizSubmitted && (
                <button
                  type="button"
                  onClick={handleResetQuiz}
                  className="border border-ink bg-surface px-3 py-1.5 text-xs font-mono font-bold text-ink hover:bg-surface-raised"
                >
                  Reset ↻
                </button>
              )}
            </div>

            {quizSubmitted && (
              <div
                role="alert"
                className={`text-xs font-bold px-3 py-1 border ${
                  quizAnswer === "ans_wip"
                    ? "bg-emerald-100 text-emerald-900 border-emerald-400"
                    : "bg-rose-100 text-rose-900 border-rose-400"
                }`}
              >
                {quizAnswer === "ans_wip"
                  ? "✓ Correct! Mov 261 debits order costs; Mov 101 credits order output and capitalizes finished inventory."
                  : "✗ Incorrect. Mov 261 is input consumption; Mov 101 is output finished goods receipt."}
              </div>
            )}
          </div>
        </fieldset>
      </div>
    </div>
  );
}
