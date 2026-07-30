"use client";

import Link from "next/link";

import type { ReviewQueueResponse } from "@/lib/types";

/**
 * Spaced-repetition queue on the dashboard. Solved problems come back for
 * review on an expanding SM-2 schedule; re-retrieving them just before you'd
 * forget is what turns practice into durable memory. Shows what's due now and,
 * when nothing is due yet, the upcoming schedule so the mechanism is visible.
 */
export function ReviewQueueCard({ data }: { data?: ReviewQueueResponse }) {
  const due = data?.due ?? [];
  const upcoming = data?.upcoming ?? [];
  const tracked = data?.tracked_count ?? 0;

  if (tracked === 0) {
    return (
      <div className="card p-4">
        <p className="label mb-1">🔁 Spaced review</p>
        <p className="font-body text-sm text-muted">
          Solve a problem and it&apos;ll return here for review at just the right time — spaced
          repetition is what makes what you learn actually stick.
        </p>
      </div>
    );
  }

  return (
    <div className="card space-y-3 p-4">
      <div className="flex items-center justify-between">
        <p className="label">🔁 Spaced review</p>
        <span className="font-mono text-xs text-muted">{tracked} tracked</span>
      </div>

      {due.length > 0 ? (
        <>
          <p className="font-display text-lg font-bold">Due now: {due.length}</p>
          <ul className="space-y-2">
            {due.map((p) => (
              <li key={p.id}>
                <Link
                  href={`/practice/${p.id}`}
                  className="card-flat flex items-center justify-between gap-2 p-2 hover:-translate-y-[1px]"
                >
                  <span className="font-body text-sm font-semibold">{p.title}</span>
                  <span className="font-mono text-xs text-muted">
                    last {p.last_score ?? "–"}/100
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </>
      ) : (
        <p className="font-body text-sm">You&apos;re all caught up — nothing due right now. 🎉</p>
      )}

      {upcoming.length > 0 && (
        <div>
          <p className="label mb-1">Upcoming</p>
          <ul className="space-y-1">
            {upcoming.slice(0, 5).map((p) => (
              <li
                key={p.id}
                className="flex items-center justify-between gap-2 font-body text-xs text-muted"
              >
                <span>{p.title}</span>
                <span className="font-mono">
                  in {p.due_in_days <= 0 ? "<1" : p.due_in_days} day
                  {p.due_in_days === 1 ? "" : "s"}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
