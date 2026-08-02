import type { Diagnosis } from "@/lib/types";

const CATEGORY_ICON: Record<string, string> = {
  logic: "🎯",
  "edge-cases": "🧩",
  "runtime-error": "💥",
  efficiency: "⏱️",
};

/**
 * Shown on Run (and Submit) only when something failed. States plainly what is
 * wrong — the exact failing case with expected vs. got — then how to fix it and
 * how to push toward the optimal complexity. Hidden entirely when all tests pass.
 */
export function DiagnosisPanel({ diagnosis }: { diagnosis: Diagnosis }) {
  const icon = CATEGORY_ICON[diagnosis.category] ?? "⚠️";
  const ff = diagnosis.first_failure;

  return (
    <div className="card-flat border-l-4 border-l-accent p-3" role="alert">
      <div className="flex items-center gap-2">
        <span aria-hidden className="text-base">
          {icon}
        </span>
        <p className="font-display text-sm font-bold">What&apos;s wrong: {diagnosis.title}</p>
      </div>

      <p className="mt-2 font-body text-sm">{diagnosis.summary}</p>

      {ff && (
        <div className="mt-3 space-y-1 border border-ink/20 bg-bg p-2 font-mono text-[11px]">
          <div>
            <span className="text-muted">input&nbsp;&nbsp;&nbsp;</span>
            <span className="break-all">{ff.call}</span>
          </div>
          {ff.expected !== null && (
            <div>
              <span className="text-muted">expected </span>
              <span className="break-all text-accent-2">{ff.expected}</span>
            </div>
          )}
          {ff.got !== null && (
            <div>
              <span className="text-muted">your&nbsp;out </span>
              <span className="break-all text-accent">{ff.got}</span>
            </div>
          )}
        </div>
      )}

      <div className="mt-3">
        <p className="label">How to fix</p>
        <p className="mt-0.5 font-body text-sm">{diagnosis.fix}</p>
      </div>

      <div className="mt-3">
        <p className="label">How to optimize</p>
        <p className="mt-0.5 font-body text-sm">{diagnosis.optimize}</p>
      </div>
    </div>
  );
}
