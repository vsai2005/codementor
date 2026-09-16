"use client";

import React, { useState } from "react";

export interface DecisionOption {
  id: string;
  label?: string;
  text?: string;
  is_correct: boolean;
  consequence?: string;
  explanation?: string;
}

interface ScenarioDecisionProps {
  title: string;
  scenarioMd: string;
  options: DecisionOption[];
  onDecisionMade?: (optionId: string, isCorrect: boolean) => void;
}

export function ScenarioDecision({
  title,
  scenarioMd,
  options,
  onDecisionMade,
}: ScenarioDecisionProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [revealed, setRevealed] = useState<boolean>(false);

  const selectedOption = options.find((opt) => opt.id === selectedId);

  const getOptionLabel = (opt: DecisionOption) => opt.label || opt.text || "Option";
  const getOptionConsequence = (opt: DecisionOption) =>
    opt.consequence || opt.explanation || "Architectural decision evaluated.";

  const handleChoose = (id: string) => {
    if (revealed) return; // Prevent overwriting without resetting
    setSelectedId(id);
    setRevealed(true);
    const chosen = options.find((opt) => opt.id === id);
    if (chosen && onDecisionMade) {
      onDecisionMade(chosen.id, chosen.is_correct);
    }
  };

  const handleReset = () => {
    setSelectedId(null);
    setRevealed(false);
  };

  return (
    <div className="border-3 border-ink bg-surface p-6 shadow-hard">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-[10px] font-mono font-bold uppercase bg-amber-300 border border-ink text-ink px-2.5 py-0.5">
          Executive Dilemma
        </span>
        <h3 className="text-lg font-black text-ink">{title}</h3>
      </div>

      {/* Scenario Briefing */}
      <div className="border-2 border-ink bg-surface-raised p-4 mb-6 text-sm text-ink leading-relaxed whitespace-pre-line font-medium">
        {scenarioMd}
      </div>

      {/* Options List */}
      <div role="radiogroup" aria-label="Decision Options" className="space-y-3 mb-6">
        <div className="text-xs font-mono font-bold uppercase text-muted">
          Select Your Architectural or Operational Course of Action:
        </div>

        {options.map((option) => {
          const isSelected = selectedId === option.id;
          let optionStyle = "border-2 border-ink bg-surface hover:bg-surface-raised text-ink";

          if (revealed && isSelected) {
            optionStyle = option.is_correct
              ? "border-3 border-emerald-600 bg-emerald-100 text-emerald-950 font-bold"
              : "border-3 border-red-600 bg-red-100 text-red-950 font-bold";
          } else if (revealed && option.is_correct) {
            optionStyle = "border-2 border-dashed border-emerald-600 bg-emerald-50 text-emerald-950";
          }

          return (
            <button
              key={option.id}
              role="radio"
              aria-checked={isSelected}
              disabled={revealed}
              type="button"
              onClick={() => handleChoose(option.id)}
              className={`w-full text-left p-4 transition-all flex items-start gap-3 focus-visible:ring-2 focus-visible:ring-amber-500 focus-visible:outline-none disabled:cursor-default ${optionStyle}`}
            >
              <span className="font-mono text-xs font-black px-2 py-1 bg-ink text-surface border border-ink shrink-0 uppercase">
                {option.id.split("_").pop()}
              </span>
              <div className="text-xs sm:text-sm leading-snug font-medium">
                {getOptionLabel(option)}
              </div>
            </button>
          );
        })}
      </div>

      {/* Consequence Reveal + Reset Option */}
      {revealed && selectedOption && (
        <div
          role="alert"
          className={`border-3 border-ink p-4 transition-all ${
            selectedOption.is_correct
              ? "bg-emerald-50 border-emerald-500 shadow-hard-sm"
              : "bg-red-50 border-red-500 shadow-hard-sm"
          }`}
        >
          <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
            <span className="font-mono text-xs font-black uppercase">
              {selectedOption.is_correct ? "✓ Optimal Enterprise Strategy" : "⚠️ Risky Architectural Consequence"}
            </span>
            <button
              type="button"
              onClick={handleReset}
              className="border-2 border-ink bg-surface px-3 py-1 text-xs font-bold text-ink shadow-hard-sm hover:bg-surface-raised focus-visible:ring-2 focus-visible:ring-ink"
            >
              Try Another Option ↻
            </button>
          </div>

          <p className="text-xs sm:text-sm text-ink leading-relaxed font-medium">
            {getOptionConsequence(selectedOption)}
          </p>

          {!selectedOption.is_correct && (
            <div className="mt-3 pt-2 border-t border-red-200 text-xs text-red-800 font-medium">
              Review the architectural invariants above and consider how this choice compromises system consistency, Clean Core governance, or statutory accounting.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
