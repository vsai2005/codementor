"use client";

import React, { useState } from "react";

export interface DeliveryStep {
  step_id: string;
  step_number: number;
  title: string;
  tcode: string;
  table: string;
  action_summary: string;
  logistics_status: string;
  fi_status: string;
  details: string;
}

const DELIVERY_STEPS: DeliveryStep[] = [
  {
    step_id: "delivery_creation",
    step_number: 1,
    title: "1. Create Outbound Delivery",
    tcode: "VL01N (Shipping Point Heidelberg)",
    table: "LIKP (Header) / LIPS (Item)",
    action_summary: "Sales Order #10042 lines transferred to Outbound Delivery #80019.",
    logistics_status: "Open for Picking",
    fi_status: "No Financial Posting",
    details: "System determines Shipping Point 1000 (Heidelberg) based on shipping condition 01 (Standard), loading group 0001 (Mechanical Crane), and Plant PL01. Calculates route determination and material availability dates.",
  },
  {
    step_id: "picking",
    step_number: 2,
    title: "2. Warehouse Picking & Transfer",
    tcode: "VL02N / Warehouse Management Task",
    table: "LIPS (Picked Qty: PIKMG)",
    action_summary: "Forklift driver picks 30x DXTR-1000 from Storage Location FG01.",
    logistics_status: "Picking Completed (30/30)",
    fi_status: "No Financial Posting",
    details: "Picking status KOSTA changes from 'A' (Not yet processed) to 'C' (Completely processed). Physical serial numbers DXTR-S-101 through DXTR-S-130 are scanned and verified against handling units.",
  },
  {
    step_id: "packing",
    step_number: 3,
    title: "3. Packing & Handling Units (HU)",
    tcode: "VL02N / Packing Cockpit",
    table: "VEKP (HU Header) / VEPO (HU Items)",
    action_summary: "30 controllers packed into 5 industrial wooden shipping crates.",
    logistics_status: "Packed & Staged at Dock 4",
    fi_status: "No Financial Posting",
    details: "Shipping labels (SSCC-18 barcodes) printed and attached to outer wooden containers. Gross weight 450 kg confirmed for freight forwarder bill of lading.",
  },
  {
    step_id: "pgi",
    step_number: 4,
    title: "4. Post Goods Issue (PGI)",
    tcode: "VL02N -> Post Goods Issue (Mov 601)",
    table: "MATDOC + ACDOCA + VBFA",
    action_summary: "Truck departs Heidelberg facility. Ownership passes to customer.",
    logistics_status: "Goods Issue Posted",
    fi_status: "Dr COGS (500000) €25,500 | Cr FG Inventory (132000) €25,500",
    details: "Movement type 601 creates Material Document #490001 in MATDOC. Inventory balance in Storage Location FG01 is reduced by 30 EA. Accounting document #1000042 is synchronously posted to ACDOCA debiting Cost of Goods Sold and crediting Inventory. Table VBFA links Sales Order -> Delivery -> Goods Issue.",
  },
];

interface DeliveryPGITracerProps {
  title?: string;
  instruction?: string;
}

export function DeliveryPGITracer({
  title = "Outbound Delivery & Post Goods Issue (PGI) Tracer",
  instruction = "Step through the shipping lifecycle for Sales Order #10042 at Plant PL01. Inspect how picking, packing, and Post Goods Issue (Movement 601) alter logistics status, inventory, and General Ledger balances.",
}: DeliveryPGITracerProps) {
  const [activeStepIndex, setActiveStepIndex] = useState<number>(0);
  const [quizAnswer, setQuizAnswer] = useState<string>("");
  const [quizSubmitted, setQuizSubmitted] = useState<boolean>(false);

  const currentStep = (DELIVERY_STEPS[activeStepIndex] || DELIVERY_STEPS[0])!;

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
            <span className="border border-ink bg-cyan-200 text-cyan-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] SD-LE-SHP
            </span>
            <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-ink">
              Plant: PL01 • SLoc: FG01
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="text-xs font-mono bg-surface-raised border border-ink p-1.5">
          Order: <strong className="text-indigo-700">SO #10042</strong> | Customer: <strong className="text-ink">CUST-501</strong>
        </div>
      </div>

      {/* Stepper Buttons */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-4">
        {DELIVERY_STEPS.map((step, idx) => {
          const isActive = idx === activeStepIndex;
          const isDone = idx < activeStepIndex;
          return (
            <button
              key={step.step_id}
              type="button"
              onClick={() => setActiveStepIndex(idx)}
              className={`p-2.5 text-left border-2 border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink ${
                isActive
                  ? "bg-amber-100 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] border-amber-900 font-bold"
                  : isDone
                  ? "bg-emerald-50 border-emerald-700 text-ink hover:bg-emerald-100"
                  : "bg-surface text-ink hover:bg-surface-raised"
              }`}
            >
              <div className="flex items-center justify-between text-[10px] font-mono font-bold mb-1">
                <span>Step {step.step_number}</span>
                <span>{isDone ? "✓ DONE" : isActive ? "ACTIVE" : "PENDING"}</span>
              </div>
              <div className="text-xs font-black truncate">{step.title.split(". ")[1]}</div>
              <div className="text-[10px] text-muted font-mono truncate">{step.tcode.split(" ")[0]}</div>
            </button>
          );
        })}
      </div>

      {/* Active Step Deep-Dive */}
      <div className="border-2 border-ink bg-surface-raised p-4 mb-5 space-y-3">
        <div className="flex flex-wrap items-center justify-between border-b border-ink/30 pb-2 gap-2">
          <div>
            <h4 className="text-sm font-black text-ink">{currentStep.title}</h4>
            <div className="text-xs font-mono text-muted mt-0.5">
              SAP Transaction: <strong>{currentStep.tcode}</strong> • Primary Table: <strong>{currentStep.table}</strong>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs font-mono">
            <span className="border border-ink bg-surface px-2 py-0.5 font-bold text-ink">
              Logistics: {currentStep.logistics_status}
            </span>
          </div>
        </div>

        <p className="text-xs text-ink leading-relaxed font-medium">{currentStep.details}</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
          <div className="p-2.5 border border-ink bg-surface">
            <span className="text-[10px] text-muted uppercase block font-bold mb-1">Logistics Document State</span>
            <div className="text-ink font-bold">{currentStep.action_summary}</div>
          </div>
          <div className="p-2.5 border border-ink bg-surface">
            <span className="text-[10px] text-muted uppercase block font-bold mb-1">Accounting & Balance Sheet Impact</span>
            <div className="text-indigo-950 font-bold">{currentStep.fi_status}</div>
          </div>
        </div>
      </div>

      {/* Concept Verification Quiz */}
      <div className="border-2 border-ink bg-surface p-4">
        <fieldset>
          <legend className="text-xs font-mono font-bold uppercase text-ink mb-2">
            Logistics & FI Knowledge Check: PGI Timing & Movement Type
          </legend>
          <p className="text-xs text-ink mb-3 font-medium">
            If a shipping clerk completes picking and packing in VL02N but does <strong>NOT</strong> click &quot;Post Goods Issue&quot; (Movement 601), what is the state of inventory and accounting?
          </p>

          <div className="space-y-2 mb-3">
            {[
              {
                id: "q_opt1",
                text: "Inventory remains asset property of Nova Manufacturing in Storage Location FG01, and zero COGS expense is recorded in ACDOCA.",
                correct: true,
              },
              {
                id: "q_opt2",
                text: "The customer is automatically charged via credit card because packing was finished.",
                correct: false,
              },
              {
                id: "q_opt3",
                text: "The inventory is deleted from MATDOC and written off directly to company overhead.",
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
                  name="delivery_pgi_quiz"
                  value={opt.id}
                  checked={quizAnswer === opt.id}
                  disabled={quizSubmitted}
                  onChange={() => setQuizAnswer(opt.id)}
                  className="mt-0.5 accent-cyan-600"
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
                className="border-2 border-ink bg-cyan-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-cyan-300 disabled:opacity-50"
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
                  quizAnswer === "q_opt1"
                    ? "bg-emerald-100 text-emerald-900 border-emerald-400"
                    : "bg-rose-100 text-rose-900 border-rose-400"
                }`}
              >
                {quizAnswer === "q_opt1"
                  ? "✓ Correct! Only Post Goods Issue (Mov 601) reduces stock and records COGS expense."
                  : "✗ Incorrect. Until PGI is posted, stock is legally owned by the seller and no FI entry exists."}
              </div>
            )}
          </div>
        </fieldset>
      </div>
    </div>
  );
}
