import Link from "next/link";

import type { ProblemDetail } from "@/lib/types";
import { TIER_LABELS } from "@/lib/types";

export function NextProblemCard({ problem }: { problem: ProblemDetail | null }) {
  if (!problem) {
    return (
      <div className="card-flat p-4">
        <p className="label mb-1">Recommended next</p>
        <p className="font-body text-sm text-muted">
          Nothing queued — you have cleared the available problems at your level.
        </p>
      </div>
    );
  }

  return (
    <div className="card p-4">
      <p className="label mb-1">Recommended next</p>
      <h3 className="font-display text-xl font-bold leading-tight">{problem.title}</h3>
      <p className="mt-1 font-mono text-xs text-muted">
        {problem.topic.name} ·{" "}
        {TIER_LABELS[problem.difficulty_tier] ?? `T${problem.difficulty_tier}`}
      </p>
      <Link href={`/practice/${problem.id}`} className="btn btn-primary mt-3 inline-block">
        Start
      </Link>
    </div>
  );
}
