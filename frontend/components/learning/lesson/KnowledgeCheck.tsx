"use client";

import React, { useState } from "react";
import { CheckpointStep, CheckpointItem } from "@/lib/lessons/types";
import { LessonMarkdown, renderInlineText } from "./LessonMarkdown";

interface KnowledgeCheckProps {
  step: CheckpointStep;
  answers: Record<string, { selectedOptionId: string; isCorrect: boolean }>;
  onAnswer: (checkpointId: string, optionId: string, isCorrect: boolean) => void;
}

export function KnowledgeCheck({ step, answers, onAnswer }: KnowledgeCheckProps) {
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="card p-6 bg-surface">
        <div className="flex items-center gap-2">
          <span className="label text-accent font-bold">Step {String(step.stepNumber).padStart(2, "0")}</span>
          <span className="text-muted text-xs">•</span>
          <span className="font-mono text-xs font-bold uppercase text-accent">
            Checkpoint / Knowledge Check
          </span>
        </div>
        <h2 className="mt-1.5 font-display text-2xl sm:text-3xl font-bold text-ink leading-tight">
          {step.heading}
        </h2>
        {step.subheading && (
          <p className="mt-2 font-body text-sm sm:text-base text-ink/80 leading-relaxed">
            {step.subheading}
          </p>
        )}
      </div>

      {/* Checkpoint Questions List */}
      <div className="space-y-8">
        {step.checkpoints.map((checkpoint, idx) => (
          <SingleCheckpointCard
            key={checkpoint.id}
            index={idx + 1}
            total={step.checkpoints.length}
            checkpoint={checkpoint}
            savedAnswer={answers[checkpoint.id]}
            onAnswer={onAnswer}
          />
        ))}
      </div>

      {/* Key Takeaway */}
      {step.keyTakeaway && (
        <div className="card border-2 border-accent bg-accent/10 p-4 sm:p-5 shadow-hard-accent">
          <span className="label text-accent font-bold uppercase tracking-wider">
            Key Principle
          </span>
          <p className="mt-1 font-body text-sm sm:text-base font-semibold text-ink leading-relaxed">
            {renderInlineText(step.keyTakeaway)}
          </p>
        </div>
      )}
    </div>
  );
}

interface SingleCheckpointCardProps {
  index: number;
  total: number;
  checkpoint: CheckpointItem;
  savedAnswer?: { selectedOptionId: string; isCorrect: boolean };
  onAnswer: (checkpointId: string, optionId: string, isCorrect: boolean) => void;
}

function SingleCheckpointCard({
  index,
  total,
  checkpoint,
  savedAnswer,
  onAnswer,
}: SingleCheckpointCardProps) {
  const [selectedId, setSelectedId] = useState<string>(savedAnswer?.selectedOptionId || "");
  const [submitted, setSubmitted] = useState<boolean>(Boolean(savedAnswer));

  const isAnsweredCorrectly = savedAnswer?.isCorrect || false;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedId) return;

    const isCorrect = selectedId === checkpoint.correctOptionId;
    setSubmitted(true);
    onAnswer(checkpoint.id, selectedId, isCorrect);
  };

  const handleTryAgain = () => {
    setSubmitted(false);
    setSelectedId("");
  };

  return (
    <div className="card p-6 bg-surface space-y-5">
      <div className="flex items-center justify-between border-b-2 border-ink/10 pb-3">
        <span className="font-mono text-xs font-bold text-accent">
          Scenario {index} of {total}
        </span>
        {savedAnswer?.isCorrect && (
          <span className="font-mono text-xs font-bold text-accent-2 flex items-center gap-1">
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
            Mastered
          </span>
        )}
      </div>

      {/* Question Statement */}
      <div className="font-body text-base text-ink font-medium leading-relaxed">
        <LessonMarkdown content={checkpoint.question} className="space-y-3" />
      </div>

      {/* Code Snippet if present */}
      {checkpoint.codeSnippet && (
        <pre className="p-4 border-2 border-ink bg-[#141d2b] dark:bg-[#121110] text-[#f2ede3] font-mono text-xs sm:text-sm overflow-x-auto leading-relaxed">
          <code>{checkpoint.codeSnippet}</code>
        </pre>
      )}

      {/* Options Form with Semantic Fieldset & Keyboard Accessible Radios */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <fieldset className="space-y-2.5">
          <legend className="sr-only">{checkpoint.question}</legend>
          <div role="radiogroup" aria-label={checkpoint.question} className="space-y-2.5">
            {checkpoint.options.map((option) => {
              const isSelected = selectedId === option.id;
              const isDisabled = submitted && isAnsweredCorrectly;

              let cardClasses =
                "flex items-start gap-3 p-4 border-2 transition-all cursor-pointer select-none text-left w-full min-h-[52px] focus-within:ring-2 focus-within:ring-accent focus-within:ring-offset-2 ";

              if (submitted && isAnsweredCorrectly) {
                if (isSelected) {
                  cardClasses += "border-accent-2 bg-accent-2/15 shadow-hard-sm";
                } else {
                  cardClasses += "border-ink/20 bg-surface/60 opacity-60";
                }
              } else if (submitted && !isAnsweredCorrectly) {
                if (isSelected) {
                  cardClasses += "border-accent bg-accent/15 shadow-hard-sm";
                } else {
                  cardClasses += "border-ink/30 bg-surface opacity-80";
                }
              } else {
                if (isSelected) {
                  cardClasses += "border-accent bg-bg shadow-hard translate-x-0.5 translate-y-0.5";
                } else {
                  cardClasses += "border-ink bg-surface shadow-hard-sm hover:shadow-hard hover:-translate-y-0.5";
                }
              }

              return (
                <label key={option.id} className={cardClasses}>
                  {/* Native accessible radio input for full keyboard/SR support */}
                  <input
                    type="radio"
                    name={`checkpoint-${checkpoint.id}`}
                    value={option.id}
                    checked={isSelected}
                    disabled={isDisabled}
                    onChange={() => setSelectedId(option.id)}
                    className="sr-only"
                    aria-label={`Option ${option.id}: ${option.label}`}
                  />

                  {/* Custom styled indicator */}
                  <div
                    aria-hidden="true"
                    className={`h-5 w-5 rounded-none border-2 border-ink flex items-center justify-center shrink-0 mt-0.5 transition-colors ${
                      isSelected ? "bg-accent" : "bg-surface"
                    }`}
                  >
                    {isSelected && <span className="h-2 w-2 bg-white" />}
                  </div>

                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold px-1.5 py-0.5 border border-ink/30 bg-bg">
                        {option.id}
                      </span>
                      {option.subtext && (
                        <span className="font-mono text-[11px] text-muted uppercase">
                          {option.subtext}
                        </span>
                      )}
                    </div>
                    <div className="mt-1.5 font-body text-sm text-ink leading-relaxed">
                      {renderInlineText(option.label)}
                    </div>
                  </div>
                </label>
              );
            })}
          </div>
        </fieldset>

        {/* Submit Action */}
        {!submitted && (
          <div className="pt-2">
            <button
              type="submit"
              disabled={!selectedId}
              className="btn btn-primary min-h-[44px] px-6 font-bold shadow-hard-sm hover:shadow-hard focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Submit Answer
            </button>
          </div>
        )}
      </form>

      {/* Explanatory Feedback Banners with aria-live */}
      <div aria-live="polite" aria-atomic="true" className="space-y-3 pt-2">
        {submitted && (
          savedAnswer?.isCorrect ? (
            <div role="status" className="border-2 border-ink bg-accent-2/15 p-5 shadow-hard animate-in fade-in duration-200">
              <div className="flex items-center gap-2">
                <span className="bg-accent-2 text-white dark:text-bg font-mono text-xs font-bold uppercase tracking-wider px-2 py-0.5 border border-ink">
                  ✓ CONCEPT MASTERED
                </span>
                <span className="font-display font-bold text-ink text-base">
                  Spot on! Correct execution model.
                </span>
              </div>
              <div className="mt-2.5 font-body text-sm text-ink leading-relaxed">
                {renderInlineText(
                  checkpoint.explanations[selectedId] ||
                    checkpoint.explanations[checkpoint.correctOptionId] ||
                    ""
                )}
              </div>
            </div>
          ) : (
            <div role="alert" className="border-2 border-ink bg-amber-500/15 p-5 shadow-hard animate-in fade-in duration-200 space-y-3">
              <div className="flex items-center gap-2">
                <span className="bg-amber-500 text-slate-900 font-mono text-xs font-bold uppercase tracking-wider px-2 py-0.5 border border-ink">
                  ⚡ MENTAL MODEL CHECK
                </span>
                <span className="font-display font-bold text-ink text-base">
                  Not quite — here is what Python did behind the scenes:
                </span>
              </div>
              <div className="font-body text-sm text-ink leading-relaxed">
                {renderInlineText(
                  checkpoint.explanations[selectedId] ||
                    "Review the reference model to see how Python evaluates objects independently from name tags."
                )}
              </div>
              <div>
                <button
                  type="button"
                  onClick={handleTryAgain}
                  className="btn bg-surface min-h-[44px] px-4 font-semibold text-xs border-2 border-ink shadow-hard-sm hover:shadow-hard focus-visible:ring-2 focus-visible:ring-accent"
                >
                  ↺ Try Again
                </button>
              </div>
            </div>
          )
        )}
      </div>
    </div>
  );
}
