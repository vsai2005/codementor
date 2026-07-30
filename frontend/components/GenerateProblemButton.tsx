"use client";

import { useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { ApiError, api } from "@/lib/api";

/**
 * Triggers AI problem generation. The model authors a fresh problem for the
 * learner's weakest topic; the backend validates its test cases by running the
 * reference solution before returning it. On success we seed the query cache and
 * navigate straight into the new problem.
 *
 * variant "card" — full dashboard call-to-action; "inline" — compact button.
 */
export function GenerateProblemButton({ variant = "card" }: { variant?: "card" | "inline" }) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generate = async () => {
    if (busy) return;
    setBusy(true);
    setError(null);
    try {
      const problem = await api.generateProblem();
      queryClient.setQueryData(["problem", problem.id], problem);
      router.push(`/practice/${problem.id}`);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : "Couldn't generate a problem right now. Please try again.",
      );
      setBusy(false);
    }
  };

  if (variant === "inline") {
    return (
      <div className="flex flex-col items-end gap-1">
        <button type="button" className="btn btn-primary px-3 py-1 text-xs" onClick={generate} disabled={busy}>
          {busy ? "Generating…" : "✨ Generate a problem"}
        </button>
        {error && <span className="font-body text-xs text-accent">{error}</span>}
      </div>
    );
  }

  return (
    <div className="card border-l-4 border-l-accent-2 p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="min-w-0">
          <p className="font-display text-base font-bold">✨ Generate a problem for me</p>
          <p className="mt-0.5 font-body text-sm text-muted">
            The AI writes a brand-new problem aimed at your weakest topic — with test cases it
            validates by running a reference solution. Never run out of targeted practice.
          </p>
        </div>
        <button type="button" className="btn btn-primary" onClick={generate} disabled={busy}>
          {busy ? "Crafting your problem…" : "Generate"}
        </button>
      </div>
      {busy && (
        <p className="mt-2 font-body text-xs text-muted">
          Authoring a problem and validating its tests — this takes a few seconds.
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
