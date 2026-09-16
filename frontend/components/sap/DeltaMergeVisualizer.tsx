"use client";

import React, { useState } from "react";

interface RowItem {
  id: number;
  doc_num: string;
  plant: string;
  material: string;
  amount: number;
  status: "MAIN" | "DELTA";
}

const INITIAL_MAIN_ROWS: RowItem[] = [
  { id: 1, doc_num: "50001001", plant: "PL01", material: "DXTR-1000", amount: 45000, status: "MAIN" },
  { id: 2, doc_num: "50001002", plant: "PL01", material: "RAW-01", amount: 12000, status: "MAIN" },
  { id: 3, doc_num: "50001003", plant: "PL02", material: "DXTR-1000", amount: 30000, status: "MAIN" },
  { id: 4, doc_num: "50001004", plant: "PL02", material: "RAW-01", amount: 8500, status: "MAIN" },
];

interface DeltaMergeVisualizerProps {
  title?: string;
  instruction?: string;
}

export const DeltaMergeVisualizer: React.FC<DeltaMergeVisualizerProps> = ({
  title = "HANA Column Store: Main/Delta Architecture & Delta Merge",
  instruction = "Insert transactional updates into the Delta store, then trigger a Delta Merge to consolidate into the read-optimized Main store.",
}) => {
  const [mainRows, setMainRows] = useState<RowItem[]>(INITIAL_MAIN_ROWS);
  const [deltaRows, setDeltaRows] = useState<RowItem[]>([
    { id: 101, doc_num: "50001005", plant: "PL01", material: "DXTR-1000", amount: 15000, status: "DELTA" },
  ]);
  const [mergePhase, setMergePhase] = useState<"IDLE" | "PREPARING" | "MERGING" | "COMMITTING">("IDLE");
  const [isMerging, setIsMerging] = useState<boolean>(false);
  const [mergeCount, setMergeCount] = useState<number>(0);

  const handleInsertTransaction = () => {
    if (isMerging) return;
    const nextId = 100 + deltaRows.length + 1;
    const plants = ["PL01", "PL02"];
    const materials = ["DXTR-1000", "RAW-01"];
    const randomPlant = plants[Math.floor(Math.random() * plants.length)] || "PL01";
    const randomMat = materials[Math.floor(Math.random() * materials.length)] || "DXTR-1000";
    const randomAmount = Math.floor(Math.random() * 25 + 5) * 1000;

    const newRow: RowItem = {
      id: nextId,
      doc_num: `5000${1000 + mainRows.length + deltaRows.length + 1}`,
      plant: randomPlant,
      material: randomMat,
      amount: randomAmount,
      status: "DELTA",
    };
    setDeltaRows((prev) => [...prev, newRow]);
  };

  const handleTriggerDeltaMerge = () => {
    if (isMerging || deltaRows.length === 0) return;
    setIsMerging(true);
    setMergePhase("PREPARING");

    setTimeout(() => {
      setMergePhase("MERGING");
      setTimeout(() => {
        setMergePhase("COMMITTING");
        setTimeout(() => {
          setMainRows((prev) => [
            ...prev,
            ...deltaRows.map((r) => ({ ...r, status: "MAIN" as const })),
          ]);
          setDeltaRows([]);
          setMergePhase("IDLE");
          setIsMerging(false);
          setMergeCount((c) => c + 1);
        }, 700);
      }, 700);
    }, 600);
  };

  const handleReset = () => {
    if (isMerging) return;
    setMainRows(INITIAL_MAIN_ROWS);
    setDeltaRows([
      { id: 101, doc_num: "50001005", plant: "PL01", material: "DXTR-1000", amount: 15000, status: "DELTA" },
    ]);
    setMergePhase("IDLE");
    setMergeCount(0);
  };

  const mainSizeKb = mainRows.length * 1.2;
  const deltaSizeKb = deltaRows.length * 8.4;

  return (
    <div className="border-4 border-ink bg-surface p-6 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-ink pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border-2 border-ink bg-accent text-surface px-2 py-0.5 text-xs font-mono font-black uppercase tracking-wider">
              [SIMULATION MODEL]
            </span>
            <span className="border-2 border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-muted">
              STATIC_VALIDATION / LOCAL_SIMULATION
            </span>
          </div>
          <h3 className="text-xl font-black font-mono tracking-tight mt-2">{title}</h3>
          <p className="text-xs font-mono text-muted mt-1">{instruction}</p>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={handleInsertTransaction}
            disabled={isMerging}
            className="border-2 border-ink bg-surface px-3 py-1.5 text-xs font-mono font-bold hover:bg-surface-raised transition-colors disabled:opacity-50"
          >
            + Post Transaction (Write to Delta)
          </button>
          <button
            type="button"
            onClick={handleTriggerDeltaMerge}
            disabled={isMerging || deltaRows.length === 0}
            className="border-2 border-ink bg-accent text-surface px-3 py-1.5 text-xs font-mono font-black hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {isMerging ? `Delta Merge: ${mergePhase}...` : "Trigger Delta Merge"}
          </button>
          <button
            type="button"
            onClick={handleReset}
            disabled={isMerging}
            className="border-2 border-ink bg-surface-raised px-2.5 py-1.5 text-xs font-mono font-bold hover:bg-surface transition-colors"
          >
            Reset
          </button>
        </div>
      </div>

      {/* Real-Time Storage Diagnostics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="border-2 border-ink bg-surface-raised p-3">
          <span className="text-[10px] font-mono text-muted uppercase font-bold">Main Store Rows (Read-Opt)</span>
          <p className="text-2xl font-mono font-black text-ink">{mainRows.length}</p>
          <span className="text-[10px] font-mono text-accent">90% Dict Compressed ({mainSizeKb.toFixed(1)} KB)</span>
        </div>
        <div className="border-2 border-ink bg-surface-raised p-3">
          <span className="text-[10px] font-mono text-muted uppercase font-bold">Delta Store Rows (Write-Opt)</span>
          <p className={`text-2xl font-mono font-black ${deltaRows.length > 3 ? "text-danger" : "text-ink"}`}>
            {deltaRows.length}
          </p>
          <span className="text-[10px] font-mono text-muted">Uncompressed Buffer ({deltaSizeKb.toFixed(1)} KB)</span>
        </div>
        <div className="border-2 border-ink bg-surface-raised p-3">
          <span className="text-[10px] font-mono text-muted uppercase font-bold">Delta Merge Phase</span>
          <p className={`text-xl font-mono font-black ${isMerging ? "text-accent animate-pulse" : "text-ink"}`}>
            {mergePhase}
          </p>
          <span className="text-[10px] font-mono text-muted">Successful Merges: {mergeCount}</span>
        </div>
        <div className="border-2 border-ink bg-surface-raised p-3">
          <span className="text-[10px] font-mono text-muted uppercase font-bold">Read Redirection Status</span>
          <p className="text-xl font-mono font-black text-ink">ACTIVE</p>
          <span className="text-[10px] font-mono text-muted">Queries read union: Main + Delta</span>
        </div>
      </div>

      {/* Main vs Delta Architecture Diagram */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Main Store Column */}
        <div className="border-2 border-ink bg-surface p-4 space-y-3">
          <div className="flex items-center justify-between border-b-2 border-ink pb-2">
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-accent inline-block border border-ink"></span>
              <h4 className="text-xs font-mono font-black uppercase tracking-wider">
                MAIN STORE (Read-Optimized, Compressed)
              </h4>
            </div>
            <span className="text-[10px] font-mono bg-accent/20 px-2 py-0.5 border border-ink font-bold">
              READ-ONLY
            </span>
          </div>

          <p className="text-[11px] font-mono text-muted leading-relaxed">
            Main storage stores dictionary-encoded column vectors. Read queries execute with high vector SIMD speed. Direct inserts are prohibited to avoid re-compressing entire column dictionaries on every transaction.
          </p>

          <div className="overflow-x-auto max-h-56 overflow-y-auto border border-ink">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-surface-raised border-b border-ink">
                <tr>
                  <th className="p-1.5">Doc #</th>
                  <th className="p-1.5">Plant</th>
                  <th className="p-1.5">Material</th>
                  <th className="p-1.5 text-right">Amount</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-ink/20">
                {mainRows.map((r) => (
                  <tr key={r.id} className="hover:bg-surface-raised">
                    <td className="p-1.5 font-bold">{r.doc_num}</td>
                    <td className="p-1.5">{r.plant}</td>
                    <td className="p-1.5">{r.material}</td>
                    <td className="p-1.5 text-right">€{r.amount.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Delta Store Column */}
        <div className="border-2 border-ink bg-surface p-4 space-y-3">
          <div className="flex items-center justify-between border-b-2 border-ink pb-2">
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-danger inline-block border border-ink"></span>
              <h4 className="text-xs font-mono font-black uppercase tracking-wider">
                DELTA STORE (Write-Optimized Buffer)
              </h4>
            </div>
            <span className="text-[10px] font-mono bg-danger/20 px-2 py-0.5 border border-ink font-bold">
              APPEND-ONLY
            </span>
          </div>

          <p className="text-[11px] font-mono text-muted leading-relaxed">
            All transactional writes (`INSERT`, `UPDATE`, `DELETE`) append immediately into the Delta store without heavy compression. During Delta Merge, Main 1 + Delta 1 are merged into a newly compressed Main 2.
          </p>

          <div className="overflow-x-auto max-h-56 overflow-y-auto border border-ink">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-surface-raised border-b border-ink">
                <tr>
                  <th className="p-1.5">Doc #</th>
                  <th className="p-1.5">Plant</th>
                  <th className="p-1.5">Material</th>
                  <th className="p-1.5 text-right">Amount</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-ink/20">
                {deltaRows.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="p-4 text-center text-muted italic">
                      Delta Store is empty (cleanly merged into Main Store).
                    </td>
                  </tr>
                ) : (
                  deltaRows.map((r) => (
                    <tr key={r.id} className="bg-danger/5 hover:bg-danger/10">
                      <td className="p-1.5 font-bold">{r.doc_num}</td>
                      <td className="p-1.5">{r.plant}</td>
                      <td className="p-1.5">{r.material}</td>
                      <td className="p-1.5 text-right">€{r.amount.toLocaleString()}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Truthfulness Notice */}
      <div className="p-3 bg-surface border-2 border-ink text-[11px] font-mono text-muted flex items-center justify-between">
        <span>* Educational simulation of SAP HANA indexserver main/delta columnar storage mechanics.</span>
        <span className="font-bold text-ink">[LOCAL SIMULATION ONLY]</span>
      </div>
    </div>
  );
};
