"use client";

import React, { useState } from "react";

export interface UniversalJournalEntry {
  line_item: number;
  ledger: "0L" | "2L";
  ledger_name: string;
  gl_account: string;
  account_name: string;
  amount: number;
  currency: string;
  debit_credit: "D" | "C";
  cost_center?: string;
  profit_center?: string;
  segment?: string;
  co_object_type?: "CostCenter" | "InternalOrder" | "WBS";
  origin_module: "FI" | "CO" | "MM" | "SD";
}

interface UniversalJournalVisualizerProps {
  entries?: UniversalJournalEntry[];
  title?: string;
  instruction?: string;
}

const DEFAULT_ENTRIES: UniversalJournalEntry[] = [
  {
    line_item: 1,
    ledger: "0L",
    ledger_name: "Leading Ledger (IFRS)",
    gl_account: "510000",
    account_name: "Raw Material Consumption",
    amount: 14500.0,
    currency: "EUR",
    debit_credit: "D",
    cost_center: "CC-1100 (Assembly Ops)",
    profit_center: "PC-1000 (Robotics)",
    segment: "SEG_INDUSTRIAL",
    co_object_type: "CostCenter",
    origin_module: "MM",
  },
  {
    line_item: 2,
    ledger: "0L",
    ledger_name: "Leading Ledger (IFRS)",
    gl_account: "131000",
    account_name: "Inventory Stock Raw Materials",
    amount: 14500.0,
    currency: "EUR",
    debit_credit: "C",
    profit_center: "PC-1000 (Robotics)",
    segment: "SEG_INDUSTRIAL",
    origin_module: "MM",
  },
  {
    line_item: 3,
    ledger: "2L",
    ledger_name: "Non-Leading Ledger (Local GAAP)",
    gl_account: "510000",
    account_name: "Raw Material Consumption",
    amount: 14100.0,
    currency: "EUR",
    debit_credit: "D",
    cost_center: "CC-1100 (Assembly Ops)",
    profit_center: "PC-1000 (Robotics)",
    segment: "SEG_INDUSTRIAL",
    co_object_type: "CostCenter",
    origin_module: "MM",
  },
  {
    line_item: 4,
    ledger: "2L",
    ledger_name: "Non-Leading Ledger (Local GAAP)",
    gl_account: "131000",
    account_name: "Inventory Stock Raw Materials",
    amount: 14100.0,
    currency: "EUR",
    debit_credit: "C",
    profit_center: "PC-1000 (Robotics)",
    segment: "SEG_INDUSTRIAL",
    origin_module: "MM",
  },
];

export function UniversalJournalVisualizer({
  entries = DEFAULT_ENTRIES,
  title = "ACDOCA Universal Journal Inspector",
  instruction = "Explore the unified single source of truth in SAP S/4HANA table ACDOCA. Toggle parallel ledgers to analyze how Financial Accounting (FI) and Controlling (CO) coexist in a single table without reconciliation batches.",
}: UniversalJournalVisualizerProps) {
  const data = entries.length > 0 ? entries : DEFAULT_ENTRIES;
  const [activeLedger, setActiveLedger] = useState<"ALL" | "0L" | "2L">("0L");
  const [selectedLine, setSelectedLine] = useState<number>(1);
  const [verified, setVerified] = useState<boolean>(false);
  const [quizAnswer, setQuizAnswer] = useState<string>("");

  const filteredEntries =
    activeLedger === "ALL"
      ? data
      : data.filter((e) => e.ledger === activeLedger);

  const currentEntry =
    filteredEntries.find((e) => e.line_item === selectedLine) ||
    filteredEntries[0] ||
    data[0];

  const handleVerify = () => {
    setVerified(true);
  };

  const handleReset = () => {
    setVerified(false);
    setQuizAnswer("");
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-emerald-200 text-emerald-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] ACDOCA
            </span>
            <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-ink">
              Company Code: NM01
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        {/* Ledger Filter Radiogroup */}
        <div
          role="radiogroup"
          aria-label="Filter by Ledger"
          className="flex items-center border-2 border-ink bg-surface-raised p-1 gap-1"
        >
          <span className="text-[10px] font-mono font-bold uppercase text-muted px-1.5">
            Ledger:
          </span>
          {(["0L", "2L", "ALL"] as const).map((led) => (
            <button
              key={led}
              type="button"
              role="radio"
              aria-checked={activeLedger === led}
              onClick={() => setActiveLedger(led)}
              className={`px-2.5 py-1 text-xs font-mono font-bold border border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink focus-visible:outline-none ${
                activeLedger === led
                  ? "bg-ink text-surface shadow-[1px_1px_0px_0px_rgba(0,0,0,1)]"
                  : "bg-surface hover:bg-surface-raised text-ink"
              }`}
            >
              {led === "0L" ? "0L (Leading)" : led === "2L" ? "2L (Local)" : "All Ledgers"}
            </button>
          ))}
        </div>
      </div>

      {/* Main Grid: Entries Table + Single Record Deep Dive */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 mb-5">
        {/* Left: Table of Line Items (7 cols) */}
        <div className="lg:col-span-7 border-2 border-ink bg-surface-raised p-3">
          <div className="flex items-center justify-between text-xs font-mono font-bold text-muted mb-2">
            <span>Journal Lines (Total: {filteredEntries.length})</span>
            <span>Single Source of Truth</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono border-collapse">
              <thead>
                <tr className="border-b-2 border-ink bg-surface text-ink">
                  <th className="p-2">Item</th>
                  <th className="p-2">Ledger</th>
                  <th className="p-2">G/L Account</th>
                  <th className="p-2">D/C</th>
                  <th className="p-2 text-right">Amount</th>
                  <th className="p-2">Module</th>
                </tr>
              </thead>
              <tbody>
                {filteredEntries.map((row) => {
                  const isSelected = row.line_item === currentEntry?.line_item;
                  const shCode = row.debit_credit === "D" ? "S" : "H";
                  const shLabel = row.debit_credit === "D" ? "S (Dr)" : "H (Cr)";
                  return (
                    <tr
                      key={row.line_item}
                      tabIndex={0}
                      role="button"
                      aria-label={`Select line item ${row.line_item}, account ${row.gl_account}`}
                      onClick={() => setSelectedLine(row.line_item)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" || e.key === " ") {
                          e.preventDefault();
                          setSelectedLine(row.line_item);
                        }
                      }}
                      className={`border-b border-ink/20 cursor-pointer transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ink ${
                        isSelected
                          ? "bg-amber-200 text-ink font-bold"
                          : "hover:bg-surface"
                      }`}
                    >
                      <td className="p-2 font-bold">#{row.line_item}</td>
                      <td className="p-2">{row.ledger}</td>
                      <td className="p-2">
                        {row.gl_account}
                        <span className="text-[10px] text-muted block truncate max-w-[120px]">
                          {row.account_name}
                        </span>
                      </td>
                      <td className="p-2">
                        <span
                          title={shCode === "S" ? "Soll (Debit)" : "Haben (Credit)"}
                          className={`px-1.5 py-0.5 text-[10px] font-bold border ${
                            shCode === "S"
                              ? "bg-blue-100 text-blue-900 border-blue-400"
                              : "bg-emerald-100 text-emerald-900 border-emerald-400"
                          }`}
                        >
                          {shLabel}
                        </span>
                      </td>
                      <td className="p-2 text-right font-bold">
                        {row.amount.toLocaleString()} {row.currency}
                      </td>
                      <td className="p-2">
                        <span className="bg-purple-100 text-purple-900 border border-purple-300 px-1 py-0.5 text-[10px] font-bold">
                          {row.origin_module}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right: Selected Line Item 350+ Dimensions Inspector (5 cols) */}
        <div className="lg:col-span-5 border-2 border-ink bg-surface p-4">
          <div className="flex items-center justify-between border-b border-ink pb-2 mb-3">
            <span className="text-xs font-mono font-bold uppercase text-ink">
              Line #{currentEntry?.line_item} Dimensions
            </span>
            <span className="text-[11px] font-mono bg-amber-100 border border-ink text-ink px-1.5 py-0.5 font-bold">
              {currentEntry?.ledger_name}
            </span>
          </div>

          <div className="space-y-2 text-xs font-mono">
            <div className="p-2 border border-ink/40 bg-surface-raised">
              <span className="text-[10px] text-muted uppercase block">Financial Account (FI)</span>
              <span className="font-bold text-ink">{currentEntry?.gl_account} — {currentEntry?.account_name}</span>
            </div>

            <div className="p-2 border border-ink/40 bg-surface-raised">
              <span className="text-[10px] text-muted uppercase block">Management Object (CO)</span>
              <span className="font-bold text-ink">
                {currentEntry?.cost_center ? `Cost Center: ${currentEntry.cost_center}` : "Balance Sheet Account (No Cost Object)"}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div className="p-2 border border-ink/40 bg-surface-raised">
                <span className="text-[10px] text-muted uppercase block">Profit Center</span>
                <span className="font-bold text-ink">{currentEntry?.profit_center || "N/A"}</span>
              </div>
              <div className="p-2 border border-ink/40 bg-surface-raised">
                <span className="text-[10px] text-muted uppercase block">Segment</span>
                <span className="font-bold text-ink">{currentEntry?.segment || "N/A"}</span>
              </div>
            </div>

            <div className="p-2 border border-ink/40 bg-emerald-50 text-emerald-950">
              <span className="text-[10px] font-bold uppercase block text-emerald-800">
                Architectural Invariant
              </span>
              In ECC, this transaction required separate entries in BSEG (FI) and COEP (CO), requiring period-end reconciliation. In S/4HANA ACDOCA, both FI and CO dimensions are committed in this single atomic row.
            </div>
          </div>
        </div>
      </div>

      {/* Mechanical Practice Question */}
      <div className="border-2 border-ink bg-surface-raised p-4">
        <fieldset>
          <legend className="text-xs font-mono font-bold uppercase text-ink mb-2">
            Verification Challenge: Multi-Ledger & Single-Source Accounting
          </legend>
          <p className="text-xs text-ink mb-3 font-medium">
            Nova Manufacturing operates Plant PL01 in Germany. Why can the amounts or postings differ between Leading Ledger 0L (IFRS) and Non-Leading Ledger 2L (Local GAAP) inside the exact same ACDOCA table?
          </p>

          <div className="space-y-2 mb-3">
            {[
              {
                id: "ans_a",
                text: "Because S/4HANA supports parallel accounting principles (multi-GAAP) where depreciation and inventory valuation rules can differ per ledger without redundant subledger tables.",
                correct: true,
              },
              {
                id: "ans_b",
                text: "Because Ledger 2L is a temporary draft table that must be manually batch-reconciled into 0L every Friday night.",
                correct: false,
              },
              {
                id: "ans_c",
                text: "Because Ledger 0L only stores Materials Management records while 2L stores Sales records.",
                correct: false,
              },
            ].map((opt) => (
              <label
                key={opt.id}
                className={`flex items-start gap-2.5 p-2.5 border border-ink cursor-pointer text-xs font-medium transition-all focus-within:ring-2 focus-within:ring-ink ${
                  quizAnswer === opt.id
                    ? "bg-ink text-surface font-bold"
                    : "bg-surface hover:bg-surface-raised text-ink"
                }`}
              >
                <input
                  type="radio"
                  name="acdoca_practice_quiz"
                  value={opt.id}
                  checked={quizAnswer === opt.id}
                  disabled={verified}
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
                onClick={handleVerify}
                disabled={!quizAnswer || verified}
                className="border-2 border-ink bg-emerald-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-300 disabled:opacity-50"
              >
                Check Answer
              </button>
              {verified && (
                <button
                  type="button"
                  onClick={handleReset}
                  className="border border-ink bg-surface px-3 py-1.5 text-xs font-mono font-bold text-ink hover:bg-surface-raised"
                >
                  Reset ↻
                </button>
              )}
            </div>

            {verified && (
              <div
                role="alert"
                className={`text-xs font-bold px-3 py-1 border ${
                  quizAnswer === "ans_a"
                    ? "bg-emerald-100 text-emerald-900 border-emerald-400"
                    : "bg-rose-100 text-rose-900 border-rose-400"
                }`}
              >
                {quizAnswer === "ans_a"
                  ? "✓ Correct! S/4HANA Universal Journal natively persists parallel accounting standards in one single table."
                  : "✗ Incorrect. Review the parallel ledger architecture: 0L and 2L exist simultaneously without batch runs."}
              </div>
            )}
          </div>
        </fieldset>
      </div>
    </div>
  );
}
