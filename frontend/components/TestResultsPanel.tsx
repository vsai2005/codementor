import type { TestsResponse } from "@/lib/types";

const STATUS_LABEL: Record<string, string> = {
  ok: "Passed",
  wrong_answer: "Wrong answer",
  timeout: "Time limit exceeded",
  memory: "Memory limit exceeded",
  error: "Runtime error",
};

export function TestResultsPanel({ tests }: { tests: TestsResponse }) {
  return (
    <div className="card-flat p-3">
      <div className="mb-2 flex items-baseline justify-between">
        <p className="label">Test results</p>
        <p className="font-mono text-sm font-semibold">
          {tests.passed}/{tests.total}
        </p>
      </div>

      <ul className="space-y-1">
        {tests.results.map((result) => (
          <li
            key={result.index}
            className="flex items-start gap-2 border-b border-ink/15 py-1 last:border-0"
          >
            <span
              aria-hidden
              className={`mt-0.5 font-mono text-xs ${result.passed ? "text-accent-2" : "text-accent"}`}
            >
              {result.passed ? "✓" : "✕"}
            </span>
            <div className="min-w-0 flex-1">
              <p className="font-mono text-xs">
                Case {result.index + 1} · {STATUS_LABEL[result.status] ?? result.status} ·{" "}
                {result.runtime_ms}ms
              </p>
              {!result.passed && result.stderr !== "" && (
                <pre className="mt-1 overflow-x-auto whitespace-pre-wrap break-words border border-ink/20 bg-bg p-2 font-mono text-[11px] text-muted">
                  {result.stderr.slice(0, 600)}
                </pre>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
