"use client";

import React, { useState } from "react";

export interface ProductScenario {
  business_need: string;
  best_product: string;
  reasoning: string;
}

interface SAPProductSelectorProps {
  scenarios?: ProductScenario[];
  title?: string;
  instruction?: string;
}

const DEFAULT_PORTFOLIO_PRODUCTS = [
  "SAP S/4HANA Finance (Cloud or Private)",
  "SAP BTP AI Core & Document Information Extraction",
  "SAP Signavio Process Insights & Intelligence",
  "SAP Fiori / SAP Mobile Services on BTP",
];

export function SAPProductSelector({
  scenarios = [],
  title = "SAP Product Portfolio Solution Matrix",
  instruction = "Match each enterprise business problem to the optimal modern SAP portfolio solution according to Clean Core principles.",
}: SAPProductSelectorProps) {
  const [selectedMatches, setSelectedMatches] = useState<Record<number, string>>({});
  const [activeScenarioIdx, setActiveScenarioIdx] = useState<number>(0);
  const [submitted, setSubmitted] = useState<boolean>(false);

  // Dynamically include any custom best_product from authored scenarios
  const availableProducts = Array.from(
    new Set([
      ...DEFAULT_PORTFOLIO_PRODUCTS,
      ...scenarios.map((s) => s.best_product).filter(Boolean),
    ])
  );

  const activeScenario = scenarios[activeScenarioIdx] || scenarios[0];

  const handleSelectProduct = (scenarioIdx: number, product: string) => {
    if (submitted) return; // Prevent mutating answers after evaluation
    setSelectedMatches((prev) => ({ ...prev, [scenarioIdx]: product }));
    if (scenarioIdx < scenarios.length - 1) {
      setActiveScenarioIdx(scenarioIdx + 1);
    }
  };

  const allSelected =
    scenarios.length > 0 && Object.keys(selectedMatches).length === scenarios.length;

  const correctCount = scenarios.filter(
    (sc, idx) => selectedMatches[idx] === sc.best_product
  ).length;

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      <div className="mb-4">
        <h3 className="text-base font-black text-ink">{title}</h3>
        <p className="text-xs text-muted mt-0.5">{instruction}</p>
      </div>

      {/* Header Tracker */}
      <div className="flex items-center justify-between border-b-2 border-ink pb-3 mb-4 text-xs font-mono">
        <div>
          Matched: <span className="font-bold">{Object.keys(selectedMatches).length}</span> /{" "}
          {scenarios.length}
        </div>
        {submitted && (
          <div
            className={`font-bold px-2.5 py-1 border-2 ${
              correctCount === scenarios.length
                ? "bg-emerald-100 text-emerald-950 border-emerald-500 font-black"
                : "bg-amber-100 text-amber-950 border-amber-500 font-black"
            }`}
          >
            {correctCount} / {scenarios.length} Correct Architectural Alignments
          </div>
        )}
      </div>

      {/* Scenario Tabs */}
      <div role="tablist" aria-label="Business Problems" className="flex flex-wrap gap-2 mb-4">
        {scenarios.map((item, idx) => {
          const isSelected = idx === activeScenarioIdx;
          const userChoice = selectedMatches[idx];
          const isCorrect = submitted && userChoice === item.best_product;
          const isWrong = submitted && userChoice && !isCorrect;

          let tabStyle = "bg-surface hover:bg-surface-raised border-ink text-ink";
          if (isSelected) {
            tabStyle = "bg-ink text-surface border-ink shadow-hard-sm";
          } else if (submitted) {
            tabStyle = isCorrect
              ? "bg-emerald-100 border-emerald-500 text-emerald-950 font-bold"
              : isWrong
              ? "bg-red-100 border-red-500 text-red-950 font-bold"
              : tabStyle;
          } else if (userChoice) {
            tabStyle = "bg-blue-50 border-blue-400 text-blue-900";
          }

          return (
            <button
              key={idx}
              role="tab"
              aria-selected={isSelected}
              type="button"
              onClick={() => setActiveScenarioIdx(idx)}
              className={`border-2 px-3 py-1.5 text-xs font-mono font-bold transition-all focus-visible:ring-2 focus-visible:ring-ink focus-visible:outline-none ${tabStyle}`}
            >
              Problem #{idx + 1}
            </button>
          );
        })}
      </div>

      {/* Active Business Problem */}
      {activeScenario && (
        <div className="border-2 border-ink bg-surface-raised p-4 mb-4">
          <div className="text-[10px] font-mono font-bold uppercase text-muted mb-1">
            Enterprise Business Need #{activeScenarioIdx + 1}
          </div>
          <div className="text-sm font-black text-ink mb-4">
            &ldquo;{activeScenario.business_need}&rdquo;
          </div>

          <div className="text-xs font-bold text-ink uppercase tracking-wider mb-2">
            Select Recommended Portfolio Offering:
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
            {availableProducts.map((prod) => {
              const isPicked = selectedMatches[activeScenarioIdx] === prod;
              return (
                <button
                  key={prod}
                  type="button"
                  disabled={submitted}
                  onClick={() => handleSelectProduct(activeScenarioIdx, prod)}
                  className={`text-left p-3 border-2 border-ink text-xs font-bold transition-all focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:outline-none ${
                    isPicked
                      ? "bg-blue-600 text-white shadow-hard-sm"
                      : "bg-surface hover:bg-blue-50 text-ink"
                  } ${submitted ? "cursor-not-allowed opacity-90" : ""}`}
                >
                  {prod}
                </button>
              );
            })}
          </div>

          {submitted && (
            <div role="alert" className="mt-4 pt-3 border-t-2 border-ink text-xs">
              <div
                className={`p-3 border-2 ${
                  selectedMatches[activeScenarioIdx] === activeScenario.best_product
                    ? "bg-emerald-50 border-emerald-500 text-emerald-950"
                    : "bg-red-50 border-red-500 text-red-950"
                }`}
              >
                <div className="font-bold mb-1">
                  Optimal Target: {activeScenario.best_product}
                </div>
                <p className="leading-relaxed font-medium">{activeScenario.reasoning}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center justify-between">
        <button
          type="button"
          onClick={() => setActiveScenarioIdx((prev) => Math.max(0, prev - 1))}
          disabled={activeScenarioIdx === 0}
          className="border border-ink bg-surface px-3 py-1.5 text-xs font-bold disabled:opacity-40 focus-visible:ring-2 focus-visible:ring-ink"
        >
          ← Previous
        </button>

        {!submitted ? (
          <button
            type="button"
            onClick={() => setSubmitted(true)}
            disabled={!allSelected}
            className="border-2 border-ink bg-emerald-400 px-5 py-2 text-xs font-black uppercase text-ink shadow-hard-sm hover:bg-emerald-300 disabled:opacity-40 focus-visible:ring-2 focus-visible:ring-ink"
          >
            Evaluate Portfolio Strategy →
          </button>
        ) : (
          <button
            type="button"
            onClick={() => {
              setSubmitted(false);
              setSelectedMatches({});
              setActiveScenarioIdx(0);
            }}
            className="border-2 border-ink bg-surface px-4 py-1.5 text-xs font-bold text-ink shadow-hard-sm hover:bg-surface-raised focus-visible:ring-2 focus-visible:ring-ink"
          >
            Reset Practice ↻
          </button>
        )}

        <button
          type="button"
          onClick={() =>
            setActiveScenarioIdx((prev) => Math.min(scenarios.length - 1, prev + 1))
          }
          disabled={activeScenarioIdx === scenarios.length - 1}
          className="border border-ink bg-surface px-3 py-1.5 text-xs font-bold disabled:opacity-40 focus-visible:ring-2 focus-visible:ring-ink"
        >
          Next →
        </button>
      </div>
    </div>
  );
}
