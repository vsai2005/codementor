"use client";

import React, { useState } from "react";

interface HANAStorageVisualizerProps {
  title?: string;
  instruction?: string;
}

export function HANAStorageVisualizer({
  title = "HANA Column-Store & Delta Merge Engine",
  instruction = "Understand why SAP HANA achieves dramatic performance gains. Explore columnar dictionary compression and simulate the Delta Merge lifecycle connecting write-optimized Delta Storage with read-optimized Main Storage.",
}: HANAStorageVisualizerProps) {
  const [activeStorageMode, setActiveStorageMode] = useState<"COLUMN" | "ROW">("COLUMN");
  const [deltaRowCount, setDeltaRowCount] = useState<number>(4);
  const [mainRowCount, setMainRowCount] = useState<number>(120);
  const [isMerging, setIsMerging] = useState<boolean>(false);
  const [mergeCount, setMergeCount] = useState<number>(0);
  const [quizAnswer, setQuizAnswer] = useState<string>("");
  const [quizEvaluated, setQuizEvaluated] = useState<boolean>(false);

  const handleAddDelta = () => {
    setDeltaRowCount((prev) => prev + 2);
  };

  const handleDeltaMerge = () => {
    setIsMerging(true);
    setTimeout(() => {
      setMainRowCount((prev) => prev + deltaRowCount);
      setDeltaRowCount(0);
      setMergeCount((prev) => prev + 1);
      setIsMerging(false);
    }, 600);
  };

  const handleReset = () => {
    setDeltaRowCount(4);
    setMainRowCount(120);
    setMergeCount(0);
    setQuizEvaluated(false);
    setQuizAnswer("");
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-purple-200 text-purple-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] SAP HANA
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        {/* Storage Format Toggle */}
        <div
          role="radiogroup"
          aria-label="Storage Mode"
          className="flex items-center border-2 border-ink bg-surface-raised p-1 gap-1"
        >
          <span className="text-[10px] font-mono font-bold uppercase text-muted px-1.5">
            Format:
          </span>
          {(["COLUMN", "ROW"] as const).map((fmt) => (
            <button
              key={fmt}
              type="button"
              role="radio"
              aria-checked={activeStorageMode === fmt}
              onClick={() => setActiveStorageMode(fmt)}
              className={`px-2.5 py-1 text-xs font-mono font-bold border border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink focus-visible:outline-none ${
                activeStorageMode === fmt
                  ? "bg-ink text-surface shadow-[1px_1px_0px_0px_rgba(0,0,0,1)]"
                  : "bg-surface hover:bg-surface-raised text-ink"
              }`}
            >
              {fmt === "COLUMN" ? "Columnar (S/4HANA Default)" : "Row-Store (Legacy)"}
            </button>
          ))}
        </div>
      </div>

      {activeStorageMode === "COLUMN" ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 mb-5">
          {/* Main Storage (Read Optimized) */}
          <div className="lg:col-span-6 border-2 border-ink bg-emerald-50/70 p-4">
            <div className="flex items-center justify-between border-b-2 border-ink pb-2 mb-3">
              <span className="text-xs font-mono font-bold uppercase text-emerald-950">
                1. Main Storage (Compressed)
              </span>
              <span className="text-[11px] font-mono font-bold bg-emerald-200 text-emerald-900 border border-emerald-500 px-2 py-0.5">
                {mainRowCount} Records • 5:1 Compression
              </span>
            </div>

            <div className="space-y-2 text-xs font-mono">
              <p className="text-ink text-[11px] leading-relaxed">
                Read-optimized. Highly compressed using dictionary encoding and bit-packing. Data is kept purely in RAM.
              </p>

              <div className="border border-ink/40 bg-surface p-2.5">
                <div className="text-[10px] uppercase text-muted mb-1">Dictionary Vector (Column: Plant)</div>
                <div className="grid grid-cols-3 gap-1 text-[11px]">
                  <span className="p-1 bg-surface-raised border border-ink/20">0: PL01</span>
                  <span className="p-1 bg-surface-raised border border-ink/20">1: PL02</span>
                  <span className="p-1 bg-surface-raised border border-ink/20">2: PL03</span>
                </div>
              </div>

              <div className="border border-ink/40 bg-surface p-2.5">
                <div className="text-[10px] uppercase text-muted mb-1">Index Vector (Referencing Dictionary)</div>
                <div className="text-[11px] text-ink font-mono truncate">
                  [0, 0, 1, 0, 1, 0, 0, 2, 1, 0, 0, 1, ...]
                </div>
              </div>

              <div className="text-[11px] text-emerald-900 font-bold mt-2">
                ✓ Scans perform at millions of rows/second using CPU vector SIMD instructions.
              </div>
            </div>
          </div>

          {/* Delta Storage & Merge Engine */}
          <div className="lg:col-span-6 border-2 border-ink bg-amber-50/70 p-4">
            <div className="flex items-center justify-between border-b-2 border-ink pb-2 mb-3">
              <span className="text-xs font-mono font-bold uppercase text-amber-950">
                2. Delta Storage (Write Optimized)
              </span>
              <span className="text-[11px] font-mono font-bold bg-amber-200 text-amber-900 border border-amber-500 px-2 py-0.5">
                {deltaRowCount} Unmerged Inserts
              </span>
            </div>

            <div className="space-y-2 text-xs font-mono">
              <p className="text-ink text-[11px] leading-relaxed">
                Write-optimized. Incoming INSERTs and UPDATEs write here without recompressing the entire massive Main memory dictionary.
              </p>

              <div className="border border-ink/40 bg-surface p-2.5 space-y-1">
                <div className="text-[10px] uppercase text-muted">Recent Transaction Buffer</div>
                {deltaRowCount > 0 ? (
                  <div className="text-[11px] text-amber-900 font-bold">
                    {deltaRowCount} new sales orders & inventory updates pending merge.
                  </div>
                ) : (
                  <div className="text-[11px] text-emerald-800 font-bold">
                    Delta buffer is empty. All rows successfully merged into Main storage!
                  </div>
                )}
              </div>

              {/* Simulation Controls */}
              <div className="pt-2 flex flex-wrap items-center gap-2">
                <button
                  type="button"
                  onClick={handleAddDelta}
                  className="border border-ink bg-surface px-2.5 py-1.5 text-xs font-bold text-ink hover:bg-surface-raised focus-visible:ring-2 focus-visible:ring-ink"
                >
                  + Simulate 2 New Transactions
                </button>
                <button
                  type="button"
                  onClick={handleDeltaMerge}
                  disabled={isMerging || deltaRowCount === 0}
                  className="border-2 border-ink bg-amber-400 px-3 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-amber-300 disabled:opacity-50 focus-visible:ring-2 focus-visible:ring-ink"
                >
                  {isMerging ? "Merging Delta into Main…" : "⚡ Execute Delta Merge"}
                </button>
              </div>

              <div className="text-[10px] text-muted mt-2">
                Merges completed in session: {mergeCount}
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* Row-Store View */
        <div className="border-2 border-ink bg-surface-raised p-4 mb-5 space-y-3">
          <div className="flex items-center gap-2">
            <span className="bg-gray-300 text-ink border border-ink px-2 py-0.5 text-xs font-mono font-bold">
              ROW-ORIENTED STORAGE (LEGACY RDBMS)
            </span>
            <span className="text-xs text-muted font-bold">1:1 Compression • Cache Misses on Analytics</span>
          </div>

          <p className="text-xs text-ink leading-relaxed">
            In traditional row-store databases, entire records are stored contiguously: <code>[ID, Customer, Date, Item, Quantity, Price, Tax, SLoc]</code>. If a reporting query asks for <code>SUM(Quantity)</code> across 10 million rows, the CPU must drag every other column (Customer, Date, Tax, etc.) through memory caches, wasting 90% of memory bandwidth.
          </p>
        </div>
      )}

      {/* Conceptual Practice Question */}
      <div className="border-2 border-ink bg-surface-raised p-4">
        <fieldset>
          <legend className="text-xs font-mono font-bold uppercase text-ink mb-2">
            Verification Challenge: The Delta Merge Invariant
          </legend>
          <p className="text-xs text-ink mb-3 font-medium">
            Why does SAP HANA maintain separate Main Storage and Delta Storage rather than writing directly into Main Storage?
          </p>

          <div className="space-y-2 mb-3">
            {[
              {
                id: "ans_a",
                text: "Because recompressing dictionary vectors on every single row write would destroy transactional write performance. Delta Storage accepts writes instantly, and Delta Merge asynchronously incorporates them into Main Storage.",
                correct: true,
              },
              {
                id: "ans_b",
                text: "Because SAP HANA permanently stores all transactional writes only in the application server memory buffer before writing to disk once daily.",
                correct: false,
              },
              {
                id: "ans_c",
                text: "Because Main Storage is an external read-only data warehouse (SAP BW) located on a separate network cluster.",
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
                  name="hana_storage_quiz"
                  value={opt.id}
                  checked={quizAnswer === opt.id}
                  disabled={quizEvaluated}
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
                onClick={() => setQuizEvaluated(true)}
                disabled={!quizAnswer || quizEvaluated}
                className="border-2 border-ink bg-purple-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-purple-300 disabled:opacity-50"
              >
                Check Answer
              </button>
              {quizEvaluated && (
                <button
                  type="button"
                  onClick={handleReset}
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
                  ? "✓ Correct! Delta storage provides low-latency writes while Main provides extreme read compression."
                  : "✗ Incorrect. Review why dictionary compression requires asynchronous batch merges."}
              </div>
            )}
          </div>
        </fieldset>
      </div>
    </div>
  );
}
