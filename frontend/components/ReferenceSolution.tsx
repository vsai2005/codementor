"use client";

import { useState } from "react";

import { ApiError, api } from "@/lib/api";
import type { ReferenceSolution as ReferenceSolutionData } from "@/lib/types";

/**
 * Reference-solution reveal. Locked until the learner has passed every test —
 * you learn most from comparing an idiomatic model answer to a solution you
 * already produced, not from copying one before you've struggled.
 */
export function ReferenceSolution({
  problemId,
  unlocked,
}: {
  problemId: string;
  unlocked: boolean;
}) {
  const [data, setData] = useState<ReferenceSolutionData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const reveal = async () => {
    if (loading) return;
    setLoading(true);
    setError(null);
    try {
      setData(await api.referenceSolution(problemId));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Couldn't load the reference solution.");
    } finally {
      setLoading(false);
    }
  };

  if (!unlocked) {
    return (
      <div className="card-flat border-l-4 border-l-muted p-3">
        <p className="font-display text-sm font-bold">🔒 Reference solution</p>
        <p className="mt-1 font-body text-xs text-muted">
          Pass every test first — then compare your approach to an idiomatic model answer.
        </p>
      </div>
    );
  }

  return (
    <div className="card-flat border-l-4 border-l-accent-2 p-3">
      <div className="flex items-center justify-between gap-2">
        <p className="font-display text-sm font-bold">📖 Reference solution</p>
        {!data && (
          <button
            type="button"
            className="btn btn-primary px-2 py-1 text-xs"
            onClick={reveal}
            disabled={loading}
          >
            {loading ? "Loading…" : "Reveal"}
          </button>
        )}
      </div>

      {error && (
        <p className="mt-2 font-body text-xs text-accent" role="alert">
          {error}
        </p>
      )}

      {data && (
        <div className="mt-3 space-y-2">
          {data.commentary && (
            <p className="font-body text-sm leading-relaxed">{data.commentary}</p>
          )}
          {data.available && data.code ? (
            <pre className="overflow-x-auto border-2 border-ink bg-bg p-3 font-mono text-xs leading-relaxed">
              <code>{data.code}</code>
            </pre>
          ) : null}
        </div>
      )}
    </div>
  );
}
