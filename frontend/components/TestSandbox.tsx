"use client";

import { useState } from "react";

import { ApiError, api } from "@/lib/api";
import type { CustomRunResponse } from "@/lib/types";

/**
 * "Try your own input" sandbox. Runs the learner's current code against an
 * arbitrary argument list — the fastest way to build edge-case intuition (the
 * exact skill the misconception tracker flags). No grading, just the output.
 */
export function TestSandbox({
  problemId,
  code,
  entryPoint,
}: {
  problemId: string;
  code: string;
  entryPoint: string;
}) {
  const [open, setOpen] = useState(false);
  const [argsText, setArgsText] = useState("[]");
  const [result, setResult] = useState<CustomRunResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const run = async () => {
    if (busy) return;
    setError(null);
    let args: unknown[];
    try {
      const parsed = JSON.parse(argsText);
      if (!Array.isArray(parsed)) throw new Error("not an array");
      args = parsed;
    } catch {
      setError("Enter arguments as a JSON array, e.g. [[1, 2, 3, 1]] for one list argument.");
      return;
    }
    setBusy(true);
    try {
      setResult(await api.runCustom({ problem_id: problemId, code, args }));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Couldn't run your input.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="card-flat p-3">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-2 text-left"
      >
        <span className="font-display text-sm font-bold">🧪 Try your own input</span>
        <span className="font-mono text-xs text-muted">{open ? "hide" : "open"}</span>
      </button>

      {open && (
        <div className="mt-3 space-y-2">
          <p className="font-body text-xs text-muted">
            Runs your editor code as{" "}
            <code className="font-mono">{entryPoint}(…args)</code>. Enter the arguments as a
            JSON array.
          </p>
          <textarea
            value={argsText}
            onChange={(e) => setArgsText(e.target.value)}
            rows={2}
            spellCheck={false}
            className="w-full resize-none border-2 border-ink bg-surface p-2 font-mono text-xs outline-none focus:shadow-hard-sm"
          />
          <div className="flex items-center gap-2">
            <button
              type="button"
              className="btn px-3 py-1 text-xs"
              onClick={run}
              disabled={busy}
            >
              {busy ? "Running…" : "Run input"}
            </button>
            {result && (
              <span className="font-mono text-xs text-muted">{result.runtime_ms}ms</span>
            )}
          </div>

          {error && (
            <p className="font-body text-xs text-accent" role="alert">
              {error}
            </p>
          )}

          {result && !error && (
            <div className="space-y-1">
              {result.status === "ok" ? (
                <p className="font-mono text-xs">
                  <span className="text-muted">returned:</span>{" "}
                  {JSON.stringify(result.returned)}
                </p>
              ) : (
                <p className="font-mono text-xs text-accent">
                  {result.status === "timeout" ? "Time Limit Exceeded" : result.stderr}
                </p>
              )}
              {result.stdout && (
                <pre className="overflow-x-auto border-2 border-ink bg-bg p-2 font-mono text-xs">
                  {result.stdout}
                </pre>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
