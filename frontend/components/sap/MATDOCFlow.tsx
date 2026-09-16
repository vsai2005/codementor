"use client";

import React, { useState } from "react";

export interface MatdocRecord {
  mblnr: string; // Material Document Number
  mjahr: string; // Year
  bwart: string; // Movement Type (101, 261, 311)
  movement_name: string;
  matnr: string; // Material Number
  werks: string; // Plant
  lgort: string; // Storage Location
  menge: number; // Quantity
  meins: string; // Unit of Measure
  dmbtr: number; // Value in Local Currency
  waers: string; // Currency
  sobkz?: string; // Special stock indicator
  lock_status: string;
}

interface MATDOCFlowProps {
  records?: MatdocRecord[];
  title?: string;
  instruction?: string;
}

const DEFAULT_RECORDS: MatdocRecord[] = [
  {
    mblnr: "5000010912",
    mjahr: "2026",
    bwart: "101",
    movement_name: "Goods Receipt for PO",
    matnr: "RAW-01 (Optical Sensor Array)",
    werks: "PL01 (Heidelberg)",
    lgort: "RAW1",
    menge: 500,
    meins: "EA",
    dmbtr: 25000.0,
    waers: "EUR",
    lock_status: "No Table Lock (Insert-Only)",
  },
  {
    mblnr: "5000010913",
    mjahr: "2026",
    bwart: "261",
    movement_name: "Goods Issue for Production Order",
    matnr: "RAW-01 (Optical Sensor Array)",
    werks: "PL01 (Heidelberg)",
    lgort: "RAW1",
    menge: -150,
    meins: "EA",
    dmbtr: -7500.0,
    waers: "EUR",
    lock_status: "No Table Lock (Insert-Only)",
  },
  {
    mblnr: "5000010914",
    mjahr: "2026",
    bwart: "311",
    movement_name: "Transfer Posting Storage Location to Storage Location (within Plant)",
    matnr: "DXTR-1000 (Robotics Controller)",
    werks: "PL02 (Austin)",
    lgort: "FG01",
    menge: 80,
    meins: "EA",
    dmbtr: 112000.0,
    waers: "EUR",
    lock_status: "No Table Lock (Insert-Only)",
  },
];

export function MATDOCFlow({
  records = DEFAULT_RECORDS,
  title = "MATDOC Single-Table Inventory Architecture",
  instruction = "Analyze how S/4HANA records material movement line items in append-only table MATDOC while preserving master and valuation tables (MARC, MARD, MBEW) via fast CDS compatibility views. Observe how goods movements insert columnar records with reduced lock contention.",
}: MATDOCFlowProps) {
  const data = records.length > 0 ? records : DEFAULT_RECORDS;
  const [selectedMblnr, setSelectedMblnr] = useState<string>(data[0]?.mblnr || "");
  const [activeTab, setActiveTab] = useState<"MATDOC" | "ECC_LEGACY">("MATDOC");
  const [selectedAnswer, setSelectedAnswer] = useState<string>("");
  const [evaluated, setEvaluated] = useState<boolean>(false);

  const activeRecord = data.find((r) => r.mblnr === selectedMblnr) || data[0];

  const handleEvaluate = () => {
    setEvaluated(true);
  };

  const handleReset = () => {
    setEvaluated(false);
    setSelectedAnswer("");
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-sky-200 text-sky-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] MATDOC
            </span>
            <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-ink">
              Plants: PL01 / PL02
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        {/* View Mode Toggle */}
        <div className="flex items-center border-2 border-ink bg-surface-raised p-1 gap-1">
          <button
            type="button"
            onClick={() => setActiveTab("MATDOC")}
            className={`px-3 py-1 text-xs font-mono font-bold border border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink focus-visible:outline-none ${
              activeTab === "MATDOC"
                ? "bg-ink text-surface shadow-[1px_1px_0px_0px_rgba(0,0,0,1)]"
                : "bg-surface hover:bg-surface-raised text-ink"
            }`}
          >
            S/4HANA MATDOC
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("ECC_LEGACY")}
            className={`px-3 py-1 text-xs font-mono font-bold border border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink focus-visible:outline-none ${
              activeTab === "ECC_LEGACY"
                ? "bg-ink text-surface shadow-[1px_1px_0px_0px_rgba(0,0,0,1)]"
                : "bg-surface hover:bg-surface-raised text-ink"
            }`}
          >
            Legacy ECC Comparison
          </button>
        </div>
      </div>

      {activeTab === "MATDOC" ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 mb-5">
          {/* Movement Records List */}
          <div className="lg:col-span-7 border-2 border-ink bg-surface-raised p-3">
            <div className="flex items-center justify-between text-xs font-mono font-bold text-muted mb-2">
              <span>Universal Inventory Records ({data.length})</span>
              <span>Insert-Only Columnar Ledger</span>
            </div>

            <div className="space-y-2">
              {data.map((rec) => {
                const isSelected = rec.mblnr === activeRecord?.mblnr;
                return (
                  <button
                    key={rec.mblnr}
                    type="button"
                    onClick={() => setSelectedMblnr(rec.mblnr)}
                    className={`w-full text-left p-3 border-2 border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink ${
                      isSelected
                        ? "bg-amber-100 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] translate-x-[2px]"
                        : "bg-surface hover:bg-surface-raised"
                    }`}
                  >
                    <div className="flex items-center justify-between font-mono text-xs font-bold mb-1">
                      <span className="text-ink">Doc #{rec.mblnr} ({rec.mjahr})</span>
                      <span className="bg-sky-100 text-sky-950 border border-sky-300 px-1.5 py-0.5 text-[10px]">
                        Movement: {rec.bwart}
                      </span>
                    </div>
                    <div className="text-xs font-semibold text-ink">{rec.movement_name}</div>
                    <div className="text-[11px] text-muted font-mono mt-1 flex justify-between">
                      <span>{rec.matnr}</span>
                      <span className="font-bold text-ink">
                        {rec.menge > 0 ? `+${rec.menge}` : rec.menge} {rec.meins} ({rec.dmbtr.toLocaleString()} {rec.waers})
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Record Details & Lock Elimination Analysis */}
          <div className="lg:col-span-5 border-2 border-ink bg-surface p-4">
            <div className="flex items-center justify-between border-b border-ink pb-2 mb-3">
              <span className="text-xs font-mono font-bold uppercase text-ink">
                MATDOC Entry Inspection
              </span>
              <span className="text-[10px] font-mono bg-emerald-100 text-emerald-950 border border-emerald-400 px-2 py-0.5 font-bold">
                {activeRecord?.lock_status}
              </span>
            </div>

            <div className="space-y-2 text-xs font-mono">
              <div className="p-2 border border-ink/40 bg-surface-raised">
                <span className="text-[10px] text-muted uppercase block">Material & Plant</span>
                <span className="font-bold text-ink">{activeRecord?.matnr}</span>
                <span className="text-muted block text-[11px]">{activeRecord?.werks} / {activeRecord?.lgort}</span>
              </div>

              <div className="p-2 border border-ink/40 bg-surface-raised">
                <span className="text-[10px] text-muted uppercase block">Quantity & Financial Valuation</span>
                <span className="font-bold text-ink">
                  {activeRecord?.menge} {activeRecord?.meins} = {activeRecord?.dmbtr.toLocaleString()} {activeRecord?.waers}
                </span>
              </div>

              <div className="p-3 border border-ink/40 bg-sky-50 text-sky-950 space-y-1">
                <span className="text-[10px] font-bold uppercase block text-sky-900">
                  ⚡ Eliminating the Stock-Table Bottleneck
                </span>
                <p className="text-[11px] leading-relaxed">
                  In legacy ERP, whenever two users posted receipts for the same material simultaneously, one transaction hung waiting on the <strong>MARC</strong> and <strong>MBEW</strong> record locks. In S/4HANA, MATDOC simply appends a new document row. Current stock is dynamically computed in-memory in microseconds.
                </p>
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* Legacy ECC View */
        <div className="border-2 border-ink bg-surface-raised p-4 mb-5 space-y-4">
          <div className="flex items-center gap-2">
            <span className="bg-rose-200 text-rose-950 border border-rose-400 px-2 py-0.5 text-xs font-mono font-bold">
              LEGACY ECC HYBRID MODEL
            </span>
            <span className="text-xs font-bold text-muted">26+ Aggregates & History Tables Deprecated</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
            <div className="p-3 border border-ink bg-surface">
              <div className="font-bold text-rose-900 mb-1">MKPF & MSEG</div>
              <div className="text-muted text-[11px]">
                Separate header and item tables. Every goods movement required writing 2 separate tables with distinct commit phases.
              </div>
            </div>
            <div className="p-3 border border-ink bg-surface">
              <div className="font-bold text-rose-900 mb-1">MBEW & MARC</div>
              <div className="text-muted text-[11px]">
                Stock master balance tables updated on every transaction with destructive row-level locks, causing warehouse bottlenecks.
              </div>
            </div>
            <div className="p-3 border border-ink bg-surface">
              <div className="font-bold text-rose-900 mb-1">MARDH & MBEWH</div>
              <div className="text-muted text-[11px]">
                Historical monthly snapshots requiring end-of-period batch jobs (MMPV) to advance posting periods.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Practice Question */}
      <div className="border-2 border-ink bg-surface-raised p-4">
        <fieldset>
          <legend className="text-xs font-mono font-bold uppercase text-ink mb-2">
            Verification Challenge: Inventory Table Simplification
          </legend>
          <p className="text-xs text-ink mb-3 font-medium">
            How does SAP S/4HANA determine current warehouse stock for Material DXTR-1000 dynamically while eliminating legacy stock total lock contention?
          </p>

          <div className="space-y-2 mb-3">
            {[
              {
                id: "ans_a",
                text: "The HANA columnar in-memory engine aggregates all historical movements in MATDOC on-the-fly in microseconds, eliminating the need to persist and lock static stock total rows.",
                correct: true,
              },
              {
                id: "ans_b",
                text: "Stock balances are pre-calculated every night by a batch background job that locks all plant tables during execution.",
                correct: false,
              },
              {
                id: "ans_c",
                text: "Current stock totals are retrieved directly by executing full-table scans across legacy disk files without using in-memory acceleration.",
                correct: false,
              },
            ].map((opt) => (
              <label
                key={opt.id}
                className={`flex items-start gap-2.5 p-2.5 border border-ink cursor-pointer text-xs font-medium transition-all focus-within:ring-2 focus-within:ring-ink ${
                  selectedAnswer === opt.id
                    ? "bg-ink text-surface font-bold"
                    : "bg-surface hover:bg-surface-raised text-ink"
                }`}
              >
                <input
                  type="radio"
                  name="matdoc_practice_quiz"
                  value={opt.id}
                  checked={selectedAnswer === opt.id}
                  disabled={evaluated}
                  onChange={() => setSelectedAnswer(opt.id)}
                  className="mt-0.5 accent-sky-600"
                />
                <span>{opt.text}</span>
              </label>
            ))}
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={handleEvaluate}
                disabled={!selectedAnswer || evaluated}
                className="border-2 border-ink bg-sky-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-sky-300 disabled:opacity-50"
              >
                Check Answer
              </button>
              {evaluated && (
                <button
                  type="button"
                  onClick={handleReset}
                  className="border border-ink bg-surface px-3 py-1.5 text-xs font-mono font-bold text-ink hover:bg-surface-raised"
                >
                  Reset ↻
                </button>
              )}
            </div>

            {evaluated && (
              <div
                role="alert"
                className={`text-xs font-bold px-3 py-1 border ${
                  selectedAnswer === "ans_a"
                    ? "bg-emerald-100 text-emerald-900 border-emerald-400"
                    : "bg-rose-100 text-rose-900 border-rose-400"
                }`}
              >
                {selectedAnswer === "ans_a"
                  ? "✓ Correct! Columnar in-memory aggregation replaces locked balance totals with dynamic speed."
                  : "✗ Incorrect. Review how HANA columnar speed replaces physical aggregate maintenance."}
              </div>
            )}
          </div>
        </fieldset>
      </div>
    </div>
  );
}
