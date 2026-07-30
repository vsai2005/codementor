"use client";

import { useState } from "react";

import type { ConceptLesson as ConceptLessonData } from "@/lib/types";

/**
 * Collapsible "pattern" mini-lesson shown beside a problem. It gives the
 * connective tissue — the underlying pattern, when to reach for it, and one
 * worked example — so solving builds transferable intuition, not just reps.
 * Collapsed by default so it never gets in the way of reading the problem.
 */
export function ConceptLesson({ concept }: { concept?: ConceptLessonData | null }) {
  const [open, setOpen] = useState(false);
  if (!concept) return null;

  return (
    <div className="card-flat border-l-4 border-l-accent-2 p-3">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-2 text-left"
      >
        <span className="font-display text-sm font-bold">📘 Pattern: {concept.pattern}</span>
        <span className="font-mono text-xs text-muted">{open ? "hide" : "learn"}</span>
      </button>

      {open && (
        <div className="mt-3 space-y-3">
          <div>
            <p className="label mb-1">The idea</p>
            <p className="font-body text-sm leading-relaxed">{concept.summary}</p>
          </div>
          <div>
            <p className="label mb-1">Reach for it when</p>
            <p className="font-body text-sm leading-relaxed">{concept.when_to_use}</p>
          </div>
          <div>
            <p className="label mb-1">Worked example</p>
            <p className="font-body text-sm leading-relaxed">{concept.worked_example}</p>
          </div>
        </div>
      )}
    </div>
  );
}
