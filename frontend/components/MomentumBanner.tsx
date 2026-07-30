"use client";

import type { MomentumDelta } from "@/lib/types";

/**
 * Ephemeral post-submit reward strip: shows XP earned, level, streak, and any
 * newly unlocked badges. Immediate feedback is what makes the momentum loop
 * feel good. Dismissible; rendered only when a submission returned momentum.
 */
export function MomentumBanner({
  momentum,
  onDismiss,
}: {
  momentum: MomentumDelta;
  onDismiss: () => void;
}) {
  return (
    <div className="card-flat mb-3 flex flex-wrap items-center gap-x-4 gap-y-1 border-l-4 border-l-accent-2 p-3">
      <span className="font-display text-sm font-bold">+{momentum.xp_earned} XP</span>
      <span className="font-body text-sm text-muted">Level {momentum.level}</span>
      <span className="font-body text-sm text-muted">🔥 {momentum.streak}-day streak</span>
      <span className="font-body text-sm text-muted">
        {momentum.solved_today}/{momentum.daily_goal} today
      </span>

      {momentum.new_badges.length > 0 && (
        <span className="flex flex-wrap items-center gap-2">
          {momentum.new_badges.map((b) => (
            <span
              key={b.id}
              className="flex items-center gap-1 border-2 border-ink bg-surface px-2 py-0.5 font-body text-xs font-semibold shadow-hard-sm"
            >
              <span aria-hidden>{b.emoji}</span> {b.label} unlocked!
            </span>
          ))}
        </span>
      )}

      <button
        type="button"
        onClick={onDismiss}
        aria-label="Dismiss"
        className="ml-auto font-mono text-xs text-muted underline"
      >
        dismiss
      </button>
    </div>
  );
}
