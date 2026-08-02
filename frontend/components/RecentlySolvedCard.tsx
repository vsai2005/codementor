"use client";

import Link from "next/link";

import type { RecentSolvedResponse } from "@/lib/types";

/**
 * The learner's last few solved problems, newest first — a quick "here's what
 * you've done" glance on the dashboard. Each links back to the problem.
 */
export function RecentlySolvedCard({ data }: { data?: RecentSolvedResponse }) {
  const items = data?.items ?? [];
  const total = data?.solved_count ?? 0;

  if (items.length === 0) {
    return (
      <div className="card p-4">
        <p className="label mb-1">✅ Recently solved</p>
        <p className="font-body text-sm text-muted">
          Solve your first problem and it&apos;ll show up here so you can track what
          you&apos;ve completed.
        </p>
      </div>
    );
  }

  return (
    <div className="card space-y-3 p-4">
      <div className="flex items-center justify-between">
        <p className="label">✅ Recently solved</p>
        <span className="font-mono text-xs text-muted">{total} solved</span>
      </div>

      <ul className="space-y-2">
        {items.map((p) => (
          <li key={p.id}>
            <Link
              href={`/practice/${p.id}`}
              className="card-flat flex items-center justify-between gap-2 p-2 hover:-translate-y-[1px]"
            >
              <span className="flex min-w-0 items-center gap-2">
                <span aria-hidden className="shrink-0 text-accent-2">
                  ✓
                </span>
                <span className="truncate font-body text-sm font-semibold">{p.title}</span>
              </span>
              <span className="shrink-0 font-mono text-xs text-muted">{p.topic.name}</span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
