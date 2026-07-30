import type { DifficultyChange } from "@/lib/types";

/** PRD 4.4: the difficulty change must be shown explicitly. It is the
 *  product's differentiator, so it never renders silently. */
export function DifficultyBanner({ difficulty }: { difficulty: DifficultyChange }) {
  const direction =
    difficulty.to > difficulty.from ? "up" : difficulty.to < difficulty.from ? "down" : "same";

  const tone =
    direction === "up"
      ? "bg-accent-2 text-white"
      : direction === "down"
        ? "bg-accent text-white"
        : "bg-surface text-ink";

  const arrow = direction === "up" ? "▲" : direction === "down" ? "▼" : "＝";

  return (
    <div className={`card-flat flex items-start gap-3 p-3 ${tone}`} role="status">
      <span aria-hidden className="font-mono text-sm leading-6">
        {arrow}
      </span>
      <div>
        <p className="font-body text-sm font-semibold">{difficulty.banner}</p>
        <p className="mt-0.5 font-mono text-xs opacity-80">
          rolling {difficulty.rolling_score.toFixed(1)} · tier {difficulty.from} → {difficulty.to}
        </p>
      </div>
    </div>
  );
}
