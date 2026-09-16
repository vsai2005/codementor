"use client";

import React, { useState } from "react";

export interface MovementTypeDefinition {
  movement_code: string;
  name: string;
  category: "Receipt" | "Issue" | "Transfer" | "Reversal" | "Scrap";
  source: string;
  destination: string;
  fi_impact: string;
  valuation_impact: string;
  business_context: string;
}

const MOVEMENT_TYPES: MovementTypeDefinition[] = [
  {
    movement_code: "101",
    name: "Goods Receipt for Purchase / Production Order",
    category: "Receipt",
    source: "Vendor (VEND-101) or Production Shopfloor",
    destination: "Plant PL01 / SLoc RAW1 or FG01 (Unrestricted)",
    fi_impact: "Dr Inventory (131000) | Cr GR/IR Clearing (211200)",
    valuation_impact: "Increases total stock quantity and total valuation on inventory balance sheet.",
    business_context: "Material arrives at receiving dock against PO #45000108. Staged into warehouse inventory.",
  },
  {
    movement_code: "102",
    name: "Reversal of Goods Receipt (Cancellation)",
    category: "Reversal",
    source: "Plant PL01 / SLoc RAW1",
    destination: "Vendor / Transit (Reversal)",
    fi_impact: "Dr GR/IR Clearing (211200) | Cr Inventory (131000)",
    valuation_impact: "Exact reversal of 101 valuation and quantity before invoice posting.",
    business_context: "Clerk entered wrong quantity or incorrect delivery note number in MIGO and cancels the document.",
  },
  {
    movement_code: "122",
    name: "Return Delivery to Vendor (Quality Defect)",
    category: "Issue",
    source: "Plant PL01 / SLoc RAW1 (or Quality Inspection QI)",
    destination: "Vendor (VEND-101)",
    fi_impact: "Dr GR/IR Clearing (211200) | Cr Inventory (131000)",
    valuation_impact: "Reduces inventory valuation; reference PO quantity is reopened for replacement.",
    business_context: "Quality control inspection rejects defective optical sensors; parts shipped back to vendor.",
  },
  {
    movement_code: "261",
    name: "Goods Issue for Production Order (Consumption)",
    category: "Issue",
    source: "Plant PL01 / SLoc RAW1",
    destination: "Production Order #100888 (Shopfloor WIP)",
    fi_impact: "Dr Consumption Expense / Order WIP (510000) | Cr Raw Materials Inventory (131000)",
    valuation_impact: "Reduces raw materials inventory; capitalizes value into active production order WIP.",
    business_context: "Optical Sensor RAW-01 backflushed and consumed into assembly of DXTR-1000 controller.",
  },
  {
    movement_code: "311",
    name: "Transfer Posting: SLoc to SLoc (One-Step)",
    category: "Transfer",
    source: "Plant PL01 / SLoc RAW1",
    destination: "Plant PL01 / SLoc PROD1",
    fi_impact: "Zero FI posting (Valuation unchanged within the same plant and valuation area).",
    valuation_impact: "Quantities update in MATDOC; balance sheet inventory value is unaffected.",
    business_context: "Forklift moves 50 sensors from central raw storage to sub-assembly staging buffer.",
  },
  {
    movement_code: "301",
    name: "Transfer Posting: Plant to Plant (One-Step)",
    category: "Transfer",
    source: "Plant PL01 (Heidelberg Assembly)",
    destination: "Plant PL02 (Austin Tech Center)",
    fi_impact: "If standard costs differ: Dr/Cr Interplant Gain/Loss | Dr/Cr Plant Inventories.",
    valuation_impact: "Transfers stock across valuation areas. Triggers intercompany or interplant accounting.",
    business_context: "Emergency component replenishment transferred from European plant to North American assembly.",
  },
  {
    movement_code: "551",
    name: "Goods Issue for Scrap (Physical Damage)",
    category: "Scrap",
    source: "Plant PL01 / SLoc RAW1",
    destination: "Scrap Waste Disposal",
    fi_impact: "Dr Scrap Expense (590000) | Cr Raw Materials Inventory (131000)",
    valuation_impact: "Permanently writes off inventory value to Profit & Loss expense.",
    business_context: "Forklift collision crushes pallet of sensors; warehouse manager approves physical scrap write-off.",
  },
  {
    movement_code: "601",
    name: "Post Goods Issue for Outbound Delivery (PGI)",
    category: "Issue",
    source: "Plant PL01 / SLoc FG01",
    destination: "Customer CUST-501 (In-Transit)",
    fi_impact: "Dr Cost of Goods Sold COGS (500000) | Cr Finished Goods Inventory (132000)",
    valuation_impact: "Reduces finished goods asset; matches cost with commercial sales revenue.",
    business_context: "Truck departs plant with 30 units of DXTR-1000 for customer delivery.",
  },
];

interface InventoryMovementMapperProps {
  title?: string;
  instruction?: string;
}

export function InventoryMovementMapper({
  title = "SAP Inventory Movement Types (MATDOC & Accounting Impact)",
  instruction = "Select standard SAP material movement types to analyze how physical warehouse stock transfers update table MATDOC and trigger synchronous financial postings in ACDOCA.",
}: InventoryMovementMapperProps) {
  const [selectedCode, setSelectedCode] = useState<string>("101");
  const [quizAnswer, setQuizAnswer] = useState<string>("");
  const [quizSubmitted, setQuizSubmitted] = useState<boolean>(false);

  const activeMovement = (MOVEMENT_TYPES.find((m) => m.movement_code === selectedCode) || MOVEMENT_TYPES[0])!;

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
            <span className="border border-ink bg-amber-200 text-amber-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] MM-IM INVENTORY
            </span>
            <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-ink">
              Table: MATDOC • MIGO
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="text-xs font-mono bg-surface-raised border border-ink p-1.5">
          Plant: <strong className="text-indigo-700">PL01</strong> | Material: <strong className="text-ink">RAW-01 / DXTR-1000</strong>
        </div>
      </div>

      {/* Movement Type Badges */}
      <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-8 gap-1.5 mb-4">
        {MOVEMENT_TYPES.map((mov) => {
          const isSelected = mov.movement_code === selectedCode;
          return (
            <button
              key={mov.movement_code}
              type="button"
              onClick={() => setSelectedCode(mov.movement_code)}
              className={`p-2 text-center border-2 border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink ${
                isSelected
                  ? "bg-amber-300 font-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] scale-[1.03]"
                  : "bg-surface hover:bg-surface-raised font-bold text-ink"
              }`}
            >
              <div className="text-sm font-mono">{mov.movement_code}</div>
              <div className="text-[9px] uppercase tracking-tight text-muted">{mov.category}</div>
            </button>
          );
        })}
      </div>

      {/* Active Movement Card */}
      <div className="border-2 border-ink bg-surface-raised p-4 mb-5 space-y-3">
        <div className="flex flex-wrap items-center justify-between border-b border-ink/30 pb-2 gap-2">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 text-xs font-mono font-black border bg-amber-100 text-amber-950 border-amber-400">
                Movement Type {activeMovement.movement_code}
              </span>
              <h4 className="text-sm font-black text-ink">{activeMovement.name}</h4>
            </div>
            <p className="text-xs text-muted font-mono mt-1">
              Category: <strong>{activeMovement.category}</strong>
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
          <div className="p-3 border border-ink bg-surface">
            <span className="text-[10px] text-muted uppercase block font-bold mb-1">Source / Issuing Point</span>
            <div className="text-ink font-bold">{activeMovement.source}</div>
          </div>
          <div className="p-3 border border-ink bg-surface">
            <span className="text-[10px] text-muted uppercase block font-bold mb-1">Destination / Receiving Point</span>
            <div className="text-ink font-bold">{activeMovement.destination}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
          <div className="p-3 border border-ink bg-surface">
            <span className="text-[10px] text-muted uppercase block font-bold mb-1">General Ledger Accounting (ACDOCA)</span>
            <div className="text-indigo-950 font-bold">{activeMovement.fi_impact}</div>
          </div>
          <div className="p-3 border border-ink bg-surface">
            <span className="text-[10px] text-muted uppercase block font-bold mb-1">Inventory Balance & Valuation Impact</span>
            <div className="text-ink font-medium">{activeMovement.valuation_impact}</div>
          </div>
        </div>

        <div className="p-2.5 border border-ink/40 bg-surface text-xs font-sans">
          <strong className="font-mono text-[11px] text-muted uppercase block">Enterprise Business Context:</strong>
          <span className="text-ink font-medium">{activeMovement.business_context}</span>
        </div>
      </div>

      {/* Verification Quiz */}
      <div className="border-2 border-ink bg-surface p-4">
        <fieldset>
          <legend className="text-xs font-mono font-bold uppercase text-ink mb-2">
            Storage Location Transfer Knowledge Check: Movement 311 vs 301
          </legend>
          <p className="text-xs text-ink mb-3 font-medium">
            Why does <strong>Movement Type 311</strong> (transfer between Storage Location RAW1 and FG01 within Plant PL01) create <strong>zero General Ledger postings</strong> in ACDOCA?
          </p>

          <div className="space-y-2 mb-3">
            {[
              {
                id: "ans_val_area",
                text: "Because in SAP ERP / S/4HANA, the Valuation Area is set at the Plant level. Moving goods within the same plant does not alter the total financial value or ownership of the plant's balance sheet inventory.",
                correct: true,
              },
              {
                id: "ans_bug",
                text: "Because SAP forgot to write an integration module between storage locations.",
                correct: false,
              },
              {
                id: "ans_vat",
                text: "Because transfers within a plant are automatically taxed at 100% and canceled out.",
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
                  name="inventory_mov_quiz"
                  value={opt.id}
                  checked={quizAnswer === opt.id}
                  disabled={quizSubmitted}
                  onChange={() => setQuizAnswer(opt.id)}
                  className="mt-0.5 accent-amber-600"
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
                className="border-2 border-ink bg-amber-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-amber-300 disabled:opacity-50"
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
                  quizAnswer === "ans_val_area"
                    ? "bg-emerald-100 text-emerald-900 border-emerald-400"
                    : "bg-rose-100 text-rose-900 border-rose-400"
                }`}
              >
                {quizAnswer === "ans_val_area"
                  ? "✓ Correct! Valuation area = Plant. SLoc transfers are purely logistical in table MATDOC."
                  : "✗ Incorrect. The valuation area is defined at the Plant level in standard S/4HANA."}
              </div>
            )}
          </div>
        </fieldset>
      </div>
    </div>
  );
}
