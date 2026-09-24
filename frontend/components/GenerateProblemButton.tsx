"use client";

import { useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { ApiError, api } from "@/lib/api";

/**
 * Triggers truthful AI problem generation or curated catalog recommendation.
 *
 * Mode "generate": Authors a fresh problem via AI and strictly validates its test
 * cases by executing the reference solution in the sandbox before returning it.
 * Mode "recommend": Selects a curated curriculum problem matching the learner's
 * current level without falsely claiming generation.
 *
 * variant "card" — full dashboard call-to-action; "inline" — compact buttons.
 */
export function GenerateProblemButton({ variant = "card" }: { variant?: "card" | "inline" }) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [busyAction, setBusyAction] = useState<"generate" | "recommend" | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAction = async (mode: "generate" | "recommend") => {
    if (busyAction) return;
    setBusyAction(mode);
    setError(null);
    try {
      const problem =
        mode === "generate"
          ? await api.generateProblem({ mode: "generate" })
          : await api.recommendProblem();

      queryClient.setQueryData(["problem", problem.id], problem);
      router.push(`/practice/${problem.id}`);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : mode === "generate"
          ? "Couldn't generate a validated problem right now. Please try again or choose a curated recommendation."
          : "Couldn't retrieve a recommended problem right now. Please try again.",
      );
      setBusyAction(null);
    }
  };

  if (variant === "inline") {
    return (
      <div className="flex flex-col items-end gap-1">
        <div className="flex items-center gap-2">
          <button
            type="button"
            className="btn btn-secondary px-2.5 py-1 text-xs"
            onClick={() => handleAction("recommend")}
            disabled={busyAction !== null}
          >
            {busyAction === "recommend" ? "Recommending…" : "🎯 Recommend problem"}
          </button>
          <button
            type="button"
            className="btn btn-primary px-2.5 py-1 text-xs"
            onClick={() => handleAction("generate")}
            disabled={busyAction !== null}
          >
            {busyAction === "generate" ? "Generating & validating…" : "✨ Generate AI problem"}
          </button>
        </div>
        {error && <span className="font-body text-xs text-accent">{error}</span>}
      </div>
    );
  }

  return (
    <div className="card border-l-4 border-l-accent-2 p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="min-w-0">
          <p className="font-display text-base font-bold">✨ Targeted Practice &amp; Generation</p>
          <p className="mt-0.5 font-body text-sm text-muted">
            Choose genuine AI generation (fully verified against test cases in our sandbox)
            or get a recommended curated problem matched to your curriculum progress.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2 shrink-0">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => handleAction("recommend")}
            disabled={busyAction !== null}
          >
            {busyAction === "recommend" ? "Finding recommendation…" : "🎯 Recommended problem"}
          </button>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => handleAction("generate")}
            disabled={busyAction !== null}
          >
            {busyAction === "generate" ? "Authoring &amp; validating…" : "✨ Generate AI problem"}
          </button>
        </div>
      </div>
      {busyAction === "generate" && (
        <p className="mt-2 font-body text-xs text-muted">
          Authoring code problem and executing reference solution in sandbox — this takes a few seconds.
        </p>
      )}
      {busyAction === "recommend" && (
        <p className="mt-2 font-body text-xs text-muted">
          Selecting optimal curated problem from curriculum matching your mastery level.
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
