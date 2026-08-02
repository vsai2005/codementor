"use client";

import { useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { ApiError, api } from "@/lib/api";
import type { ProblemDetail } from "@/lib/types";
import { TIER_LABELS } from "@/lib/types";

/**
 * "Recommended next" on the dashboard. The primary action generates a BRAND-NEW
 * AI problem on every click (same as the Problems page) rather than re-opening
 * the last generated one. The current recommendation is still shown and can be
 * opened directly via the secondary button, so no practice is lost.
 */
export function NextProblemCard({ problem }: { problem: ProblemDetail | null }) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generate = async () => {
    if (busy) return;
    setBusy(true);
    setError(null);
    try {
      const fresh = await api.generateProblem();
      queryClient.setQueryData(["problem", fresh.id], fresh);
      // Refresh the recommendation so the next visit doesn't surface a stale one.
      queryClient.invalidateQueries({ queryKey: ["next-problem"] });
      router.push(`/practice/${fresh.id}`);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : "Couldn't generate a problem right now. Please try again.",
      );
      setBusy(false);
    }
  };

  return (
    <div className="card p-4">
      <p className="label mb-1">Recommended next</p>

      {problem ? (
        <>
          <h3 className="font-display text-xl font-bold leading-tight">{problem.title}</h3>
          <p className="mt-1 font-mono text-xs text-muted">
            {problem.topic.name} ·{" "}
            {TIER_LABELS[problem.difficulty_tier] ?? `T${problem.difficulty_tier}`}
          </p>
        </>
      ) : (
        <p className="font-body text-sm text-muted">
          Generate a fresh AI problem aimed at your weakest topic.
        </p>
      )}

      <div className="mt-3 flex flex-wrap items-center gap-2">
        <button type="button" className="btn btn-primary" onClick={generate} disabled={busy}>
          {busy ? "Generating…" : "✨ Generate new problem"}
        </button>
        {problem && (
          <Link href={`/practice/${problem.id}`} className="btn">
            Open this one
          </Link>
        )}
      </div>

      {busy && (
        <p className="mt-2 font-body text-xs text-muted">
          Authoring a fresh problem and validating its tests — a few seconds.
        </p>
      )}
      {error && (
        <p className="mt-2 font-body text-xs text-accent" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
