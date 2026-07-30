import type { TopicProgress } from "@/lib/types";
import { TIER_LABELS } from "@/lib/types";

const MASTERY_TONE: Record<string, string> = {
  strong: "bg-accent-2 text-white",
  learning: "bg-surface text-ink",
  weak: "bg-accent text-white",
};

export function MasteryGrid({ topics }: { topics: TopicProgress[] }) {
  if (topics.length === 0) {
    return (
      <div className="card-flat p-4">
        <p className="font-body text-sm text-muted">
          No topics practised yet. Solve a problem to start building your profile.
        </p>
      </div>
    );
  }

  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      {topics.map((entry) => (
        <div key={entry.topic.id} className="card p-3">
          <div className="mb-2 flex items-start justify-between gap-2">
            <h3 className="font-display text-base font-bold leading-tight">
              {entry.topic.name}
            </h3>
            <span
              className={`shrink-0 border-2 border-ink px-1.5 py-0.5 font-body text-[10px] font-bold uppercase ${
                MASTERY_TONE[entry.mastery] ?? "bg-surface"
              }`}
            >
              {entry.mastery}
            </span>
          </div>

          <div className="h-3 w-full border-2 border-ink bg-surface">
            <div
              className={entry.avg_score >= 80 ? "h-full bg-accent-2" : "h-full bg-accent"}
              style={{ width: `${Math.max(0, Math.min(100, entry.avg_score))}%` }}
            />
          </div>

          <p className="mt-2 font-mono text-xs text-muted">
            {TIER_LABELS[entry.current_tier] ?? `T${entry.current_tier}`} · avg{" "}
            {entry.avg_score.toFixed(0)} · {entry.attempts} attempts
          </p>
        </div>
      ))}
    </div>
  );
}
