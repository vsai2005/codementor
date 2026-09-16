"use client";

import React, { useState } from "react";

interface CostSettlementVisualizerProps {
  title?: string;
  instruction?: string;
}

export function CostSettlementVisualizer({
  title = "Production Order Costing, Variance & Month-End Settlement (KO88)",
  instruction = "Analyze how actual manufacturing costs accumulate on Production Order #100888, how standard finished goods output credits the order, and how KO88 settles variances to ACDOCA.",
}: CostSettlementVisualizerProps) {
  const [scrapUnits, setScrapUnits] = useState<number>(5);
  const [laborOvertimeHours, setLaborOvertimeHours] = useState<number>(8);
  const [isSettled, setIsSettled] = useState<boolean>(false);
  const [quizAnswer, setQuizAnswer] = useState<string>("");
  const [quizSubmitted, setQuizSubmitted] = useState<boolean>(false);

  // Baseline standard costs
  const plannedOrderQty = 100;
  const standardCostPerUnit = 220; // €22,000 total planned credit on receipt
  const baseMaterialCost = 15000;
  const baseLaborCost = 4250;
  const baseMachineOverhead = 2750;

  // Variances based on user adjustments
  const scrapMaterialCost = scrapUnits * 150; // €150/unit raw material
  const overtimeLaborCost = laborOvertimeHours * 65; // €65/hr technician rate

  const actualTotalCost = baseMaterialCost + scrapMaterialCost + baseLaborCost + overtimeLaborCost + baseMachineOverhead;
  const standardDeliveredCredit = plannedOrderQty * standardCostPerUnit;
  const productionVariance = actualTotalCost - standardDeliveredCredit;

  const handleReset = () => {
    setScrapUnits(5);
    setLaborOvertimeHours(8);
    setIsSettled(false);
  };

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
            <span className="border border-ink bg-rose-200 text-rose-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] CO-PC ORDER SETTLEMENT
            </span>
            <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-ink">
              T-Code: KO88 • Order: #100888
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="text-xs font-mono bg-surface-raised border border-ink p-1.5">
          Standard Output: <strong className="text-emerald-700">€{standardDeliveredCredit.toLocaleString()}</strong> (100 EA @ €220)
        </div>
      </div>

      {/* Interactive Variance Sliders */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 border-2 border-ink bg-surface-raised p-4 mb-4">
        <div>
          <label htmlFor="scrap_input" className="block text-xs font-mono font-bold text-ink mb-1">
            Shopfloor Scrap Variance: {scrapUnits} defective sensor assemblies
          </label>
          <input
            id="scrap_input"
            type="range"
            min="0"
            max="15"
            step="1"
            value={scrapUnits}
            disabled={isSettled}
            onChange={(e) => setScrapUnits(parseInt(e.target.value, 10))}
            className="w-full accent-rose-600"
          />
          <span className="text-[11px] text-muted block mt-1 font-mono">
            Adds €{scrapMaterialCost.toLocaleString()} in unplanned raw material consumption (Mov 261).
          </span>
        </div>

        <div>
          <label htmlFor="overtime_input" className="block text-xs font-mono font-bold text-ink mb-1">
            Labor Overtime Variance: {laborOvertimeHours} additional technician hours
          </label>
          <input
            id="overtime_input"
            type="range"
            min="0"
            max="20"
            step="2"
            value={laborOvertimeHours}
            disabled={isSettled}
            onChange={(e) => setLaborOvertimeHours(parseInt(e.target.value, 10))}
            className="w-full accent-rose-600"
          />
          <span className="text-[11px] text-muted block mt-1 font-mono">
            Adds €{overtimeLaborCost.toLocaleString()} in secondary cost activity confirmations (CO11N).
          </span>
        </div>
      </div>

      {/* Production Order T-Account Balance Sheet */}
      <div className="border-2 border-ink bg-surface p-4 mb-4">
        <div className="text-xs font-mono font-bold uppercase text-ink border-b-2 border-ink pb-2 mb-3 flex items-center justify-between">
          <span>Production Order #100888 (Cost Object Ledger)</span>
          <span className="text-[11px] text-muted">Status: TECO (Technically Completed)</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
          {/* Debit Side */}
          <div className="p-3 border border-ink bg-surface-raised space-y-2">
            <div className="font-black text-rose-800 uppercase border-b border-ink/20 pb-1">
              Actual Cost Debits (Incurred)
            </div>
            <div className="flex justify-between">
              <span>Raw Materials (RAW-01 Sensors):</span>
              <span>€{(baseMaterialCost + scrapMaterialCost).toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span>Direct Shopfloor Labor:</span>
              <span>€{(baseLaborCost + overtimeLaborCost).toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span>Machine Depreciation Overhead:</span>
              <span>€{baseMachineOverhead.toLocaleString()}</span>
            </div>
            <div className="border-t border-ink/40 pt-1 font-black flex justify-between text-ink">
              <span>Total Debits:</span>
              <span>€{actualTotalCost.toLocaleString()}</span>
            </div>
          </div>

          {/* Credit Side */}
          <div className="p-3 border border-ink bg-surface-raised space-y-2">
            <div className="font-black text-emerald-800 uppercase border-b border-ink/20 pb-1">
              Output Credits & Settlements
            </div>
            <div className="flex justify-between">
              <span>Goods Receipt (100 EA @ €220 Std):</span>
              <span>-€{standardDeliveredCredit.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span>KO88 Settlement to ACDOCA:</span>
              <span className={isSettled ? "font-bold text-indigo-700" : "text-muted"}>
                {isSettled ? `-€${productionVariance.toLocaleString()}` : "Pending Settlement (€0.00)"}
              </span>
            </div>
            <div className="border-t border-ink/40 pt-1 font-black flex justify-between text-ink">
              <span>Net Order Balance:</span>
              <span className={isSettled ? "text-emerald-700 font-black" : "text-rose-700 font-black"}>
                {isSettled ? "€0.00 (Zero Balance ✓)" : `+€${productionVariance.toLocaleString()} (Debit Balance)`}
              </span>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="mt-4 flex flex-wrap items-center justify-between gap-2 pt-3 border-t border-ink/30">
          <div className="text-xs font-mono">
            Unsettled Order Variance:{" "}
            <strong className="text-rose-700">€{productionVariance.toLocaleString()}</strong> (Unfavorable Production Variance)
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setIsSettled(true)}
              disabled={isSettled}
              className="border-2 border-ink bg-rose-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-rose-300 disabled:opacity-50"
            >
              Execute Settlement (KO88)
            </button>
            <button
              type="button"
              onClick={handleReset}
              className="border border-ink bg-surface px-3 py-1.5 text-xs font-mono font-bold text-ink hover:bg-surface-raised"
            >
              Reset Simulation ↻
            </button>
          </div>
        </div>

        {isSettled && (
          <div className="mt-3 p-3 border border-emerald-500 bg-emerald-50 text-xs font-mono text-emerald-950">
            <strong>✓ Settlement Complete:</strong> Journal entry posted in ACDOCA:
            <br />
            <code>
              Debit Price Variance Expense (530000) €{productionVariance.toLocaleString()} | Credit Production Settlement / Factory Cost Clearing (520000) €{productionVariance.toLocaleString()}
            </code>
            <br />
            <span className="text-[11px] text-emerald-800">
              Order balance is now exactly €0.00. Variance details transferred to Profitability Analysis (CO-PA).
            </span>
          </div>
        )}
      </div>

      {/* Knowledge Check */}
      <div className="border-2 border-ink bg-surface p-4">
        <fieldset>
          <legend className="text-xs font-mono font-bold uppercase text-ink mb-2">
            Settlement Knowledge Check: Why Does S/4HANA Require Order Settlement?
          </legend>
          <p className="text-xs text-ink mb-3 font-medium">
            When a manufacturing order is technically completed (TECO), why must the financial controller run settlement transaction <strong>KO88</strong>?
          </p>

          <div className="space-y-2 mb-3">
            {[
              {
                id: "ans_settle",
                text: "Because actual incurred costs rarely match the standard cost exactly; KO88 transfers the remaining variance balance out of the order and posts it to General Ledger variance accounts and CO-PA, bringing the order balance to zero.",
                correct: true,
              },
              {
                id: "ans_delete",
                text: "Because KO88 deletes the production order from the database to save disk space.",
                correct: false,
              },
              {
                id: "ans_wire",
                text: "Because KO88 sends wire transfers to pay the factory workers' weekly wages.",
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
                  name="cost_settle_quiz"
                  value={opt.id}
                  checked={quizAnswer === opt.id}
                  disabled={quizSubmitted}
                  onChange={() => setQuizAnswer(opt.id)}
                  className="mt-0.5 accent-rose-600"
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
                className="border-2 border-ink bg-rose-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-rose-300 disabled:opacity-50"
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
                  quizAnswer === "ans_settle"
                    ? "bg-emerald-100 text-emerald-900 border-emerald-400"
                    : "bg-rose-100 text-rose-900 border-rose-400"
                }`}
              >
                {quizAnswer === "ans_settle"
                  ? "✓ Correct! KO88 ensures period costs and variances are credited from the order and posted into financial accounting and CO-PA."
                  : "✗ Incorrect. Settlement balances the manufacturing order by moving variance to financial accounting."}
              </div>
            )}
          </div>
        </fieldset>
      </div>
    </div>
  );
}
