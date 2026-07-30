"use client";

import type { MomentumSummary } from "@/lib/types";

/**
 * Dashboard momentum widget: level + XP progress, current streak, today's goal,
 * and the badge shelf. Motivation and visible progress are what turn a practice
 * session into a habit — the real driver of long-term learning.
 */
export function MomentumCard({ data }: { data?: MomentumSummary }) {
  if (!data) {
    return (
      <div className="card p-4">
        <p className="label mb-1">🚀 Momentum</p>
        <p className="font-body text-sm text-muted">Loading your progress…</p>
      </div>
    );
  }

  const pct =
    data.level_span > 0
      ? Math.min(100, Math.round((data.level_progress / data.level_span) * 100))
      : 0;
  const goalPct = Math.min(100, Math.round((data.solved_today / data.daily_goal) * 100));
  const goalMet = data.solved_today >= data.daily_goal;

  return (
    <div className="card space-y-4 p-4">
      <div className="flex items-center justify-between">
        <p className="label">🚀 Momentum</p>
        <span className="font-mono text-xs text-muted">{data.xp} XP total</span>
      </div>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        {/* Level + XP bar */}
        <div className="card-flat p-3">
          <div className="flex items-baseline justify-between">
            <p className="font-display text-2xl font-bold">Lv {data.level}</p>
            <span className="font-mono text-xs text-muted">
              {data.level_progress}/{data.level_span}
            </span>
          </div>
          <div className="mt-2 h-3 w-full border-2 border-ink bg-surface">
            <div className="h-full bg-accent-2" style={{ width: `${pct}%` }} />
          </div>
          <p className="mt-1 font-body text-xs text-muted">
            {data.level_span - data.level_progress} XP to next level
          </p>
        </div>

        {/* Streak */}
        <div className="card-flat p-3">
          <p className="font-display text-2xl font-bold">🔥 {data.streak}</p>
          <p className="font-body text-xs text-muted">
            day streak{data.streak === 1 ? "" : "s"}
          </p>
          <p className="mt-1 font-mono text-xs text-muted">best {data.longest_streak}</p>
        </div>

        {/* Daily goal */}
        <div className="card-flat p-3">
          <p className="font-display text-2xl font-bold">
            {data.solved_today}/{data.daily_goal}
          </p>
          <p className="font-body text-xs text-muted">solved today</p>
          <div className="mt-2 h-3 w-full border-2 border-ink bg-surface">
            <div
              className={`h-full ${goalMet ? "bg-accent-2" : "bg-accent"}`}
              style={{ width: `${goalPct}%` }}
            />
          </div>
          <p className="mt-1 font-body text-xs text-muted">
            {goalMet ? "Goal met — nice! ✅" : "Keep going!"}
          </p>
        </div>
      </div>

      {/* Badge shelf */}
      <div>
        <p className="label mb-2">
          Badges · {data.earned_count}/{data.badges.length}
        </p>
        <div className="flex flex-wrap gap-2">
          {data.badges.map((b) => (
            <div
              key={b.id}
              title={`${b.label} — ${b.desc}`}
              className={`flex items-center gap-1.5 border-2 border-ink px-2 py-1 ${
                b.earned ? "bg-surface" : "bg-bg opacity-40 grayscale"
              }`}
            >
              <span className="text-base" aria-hidden>
                {b.emoji}
              </span>
              <span className="font-body text-xs font-semibold">{b.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
