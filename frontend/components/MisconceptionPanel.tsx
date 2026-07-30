"use client";

import type { MisconceptionsResponse } from "@/lib/types";

/**
 * "Your common mistakes" — turns failed submissions into a visible pattern.
 * Each failure is classified (edge cases / efficiency / runtime error / logic)
 * and tallied, with a targeted tip, so the learner can see and attack their
 * recurring blind spots instead of just seeing a zero and moving on.
 */
export function MisconceptionPanel({ data }: { data?: MisconceptionsResponse }) {
  const items = data?.items ?? [];
  if (items.length === 0) return null; // nothing to show until a mistake happens

  return (
    <section className="card space-y-3 p-4">
      <div className="flex items-center justify-between">
        <p className="label">🧠 Your common mistakes</p>
        <span className="font-mono text-xs text-muted">{data?.total ?? 0} logged</span>
      </div>

      <ul className="space-y-2">
        {items.map((m) => (
          <li key={m.tag} className="card-flat border-l-4 border-l-accent p-3">
            <div className="flex items-center justify-between gap-2">
              <p className="font-body text-sm font-semibold">{m.label}</p>
              <span className="border-2 border-ink bg-surface px-2 py-0.5 font-mono text-xs font-bold">
                ×{m.count}
              </span>
            </div>
            <p className="mt-1 font-body text-xs text-muted">{m.tip}</p>
            {m.problems.length > 0 && (
              <p className="mt-1 font-body text-xs text-muted">
                Recent: {m.problems.join(", ")}
              </p>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}
