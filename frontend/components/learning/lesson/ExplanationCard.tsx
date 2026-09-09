"use client";

import React from "react";
import { ExplanationStep } from "@/lib/lessons/types";
import { LessonMarkdown, renderInlineText, CodeBlock } from "./LessonMarkdown";

interface ExplanationCardProps {
  step: ExplanationStep;
}

export function ExplanationCard({ step }: ExplanationCardProps) {
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="card p-6 bg-surface">
        <div className="flex items-center gap-2">
          <span className="label text-accent font-bold">Step {String(step.stepNumber).padStart(2, "0")}</span>
          <span className="text-muted text-xs">•</span>
          <span className="font-mono text-xs text-muted">Core Concept</span>
        </div>
        <h2 className="mt-1.5 font-display text-2xl sm:text-3xl font-bold text-ink leading-tight">
          {renderInlineText(step.heading)}
        </h2>
        {step.subheading && (
          <p className="mt-2 font-body text-sm sm:text-base text-ink/80 leading-relaxed">
            {renderInlineText(step.subheading)}
          </p>
        )}
      </div>

      {/* Narrative Prose */}
      <div className="card p-6 bg-surface font-body text-sm sm:text-base text-ink leading-relaxed">
        <LessonMarkdown content={step.markdownContent} />
      </div>

      {/* Code Snippets */}
      {step.snippets && step.snippets.length > 0 && (
        <div className="space-y-4">
          {step.snippets.map((snip, idx) => (
            <div key={idx}>
              <CodeBlock
                code={snip.code}
                language={snip.language || "python"}
                title={snip.title || `Python Example #${idx + 1}`}
              />
              {snip.caption && (
                <div className="border border-ink/20 px-3 py-1.5 bg-bg/40 text-xs font-body text-muted rounded -mt-2 mb-3">
                  💡 {renderInlineText(snip.caption)}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Callouts */}
      {step.callouts && step.callouts.length > 0 && (
        <div className="space-y-3">
          {step.callouts.map((callout, i) => {
            let toneBorder = "border-ink";
            let toneBg = "bg-surface";
            let badgeText = "NOTE";
            let badgeStyle = "bg-ink text-bg";

            if (callout.type === "tip") {
              toneBorder = "border-accent-2";
              toneBg = "bg-accent-2/10";
              badgeText = "💡 ARCHITECT TIP";
              badgeStyle = "bg-accent-2 text-white dark:text-bg";
            } else if (callout.type === "warning") {
              toneBorder = "border-accent";
              toneBg = "bg-accent/10";
              badgeText = "⚠️ PITFALL WARNING";
              badgeStyle = "bg-accent text-white dark:text-bg";
            } else if (callout.type === "deep-dive") {
              toneBorder = "border-ink";
              toneBg = "bg-amber-500/10";
              badgeText = "🔬 DEEP DIVE";
              badgeStyle = "bg-amber-500 text-slate-900 font-bold";
            }

            return (
              <div key={i} className={`border-2 ${toneBorder} ${toneBg} p-4 sm:p-5 shadow-hard-sm`}>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 font-mono text-[10px] uppercase font-bold border border-ink ${badgeStyle}`}>
                    {badgeText}
                  </span>
                  <span className="font-display font-bold text-ink text-sm sm:text-base">
                    {renderInlineText(callout.title)}
                  </span>
                </div>
                <p className="mt-2 font-body text-xs sm:text-sm text-ink/90 leading-relaxed">
                  {renderInlineText(callout.content)}
                </p>
              </div>
            );
          })}
        </div>
      )}

      {/* Key Takeaway */}
      {step.keyTakeaway && (
        <div className="card border-2 border-accent bg-accent/10 p-4 sm:p-5 shadow-hard-accent">
          <span className="label text-accent font-bold uppercase tracking-wider">
            Key Mental Takeaway
          </span>
          <p className="mt-1 font-body text-sm sm:text-base font-semibold text-ink leading-relaxed">
            {renderInlineText(step.keyTakeaway)}
          </p>
        </div>
      )}
    </div>
  );
}
