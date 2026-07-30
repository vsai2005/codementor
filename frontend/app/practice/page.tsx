"use client";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useState } from "react";

import { AppShell } from "@/components/AppShell";
import { GenerateProblemButton } from "@/components/GenerateProblemButton";
import { TopicPill } from "@/components/TopicPill";
import { api } from "@/lib/api";

export default function PracticeListPage() {
  const [tier, setTier] = useState<number | undefined>(undefined);
  const queryClient = useQueryClient();

  const problems = useQuery({
    queryKey: ["problems", tier],
    queryFn: () => api.listProblems(tier === undefined ? {} : { tier }),
  });

  // Warm the cache the moment a card is hovered/focused so opening it is instant.
  const prefetch = (id: string) =>
    queryClient.prefetchQuery({
      queryKey: ["problem", id],
      queryFn: () => api.getProblem(id),
      staleTime: 30_000,
    });

  return (
    <AppShell>
      <div className="mx-auto max-w-[1000px] space-y-5 px-3 py-6 sm:px-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h1 className="font-display text-3xl font-bold">Problems</h1>
          <GenerateProblemButton variant="inline" />
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            className={`btn px-3 py-1 text-xs ${tier === undefined ? "btn-primary" : ""}`}
            onClick={() => setTier(undefined)}
          >
            All tiers
          </button>
          {[1, 2, 3, 4, 5].map((t) => (
            <button
              key={t}
              type="button"
              className={`btn px-3 py-1 text-xs ${tier === t ? "btn-primary" : ""}`}
              onClick={() => setTier(t)}
            >
              Tier {t}
            </button>
          ))}
        </div>

        {problems.isLoading && <p className="font-body text-sm text-muted">Loading…</p>}
        {problems.isError && (
          <p className="font-body text-sm text-accent">Could not load problems.</p>
        )}

        <ul className="space-y-2">
          {(problems.data?.items ?? []).map((problem) => (
            <li key={problem.id}>
              <Link
                href={`/practice/${problem.id}`}
                prefetch
                onMouseEnter={() => prefetch(problem.id)}
                onFocus={() => prefetch(problem.id)}
                className="card flex items-center justify-between gap-3 p-3 hover:-translate-x-[1px] hover:-translate-y-[1px]"
              >
                <span className="flex min-w-0 items-center gap-2">
                  {problem.generated && (
                    <span
                      className="shrink-0 border-2 border-ink bg-surface px-1.5 py-0.5 font-mono text-[10px] font-bold"
                      title="AI-generated problem"
                    >
                      ✨ AI
                    </span>
                  )}
                  <span className="truncate font-display text-base font-bold">{problem.title}</span>
                </span>
                <TopicPill label={problem.topic.name} tier={problem.difficulty_tier} />
              </Link>
            </li>
          ))}
        </ul>

        {problems.data && problems.data.items.length === 0 && (
          <p className="font-body text-sm text-muted">No problems at this tier yet.</p>
        )}
      </div>
    </AppShell>
  );
}
