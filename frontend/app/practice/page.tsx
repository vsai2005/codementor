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
  const [topic, setTopic] = useState<string | undefined>(undefined);
  const queryClient = useQueryClient();

  // Fetch the full list once (carries per-user `solved` flags), then filter in
  // the browser. Keeping every problem client-side lets the topic buttons stay
  // complete and lets topic + tier filters combine instantly.
  const problems = useQuery({
    queryKey: ["problems"],
    queryFn: () => api.listProblems({ page_size: 250 }),
  });

  const allItems = problems.data?.items ?? [];

  // Distinct topics, in first-seen order, for the filter row.
  const topics = Array.from(
    new Map(allItems.map((p) => [p.topic.slug, p.topic])).values(),
  );

  const solvedCount = allItems.filter((p) => p.solved).length;

  const items = allItems.filter(
    (p) =>
      (topic === undefined || p.topic.slug === topic) &&
      (tier === undefined || p.difficulty_tier === tier),
  );

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

        {/* Topic filter */}
        <div className="space-y-2">
          <p className="label">Topic</p>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              className={`btn px-3 py-1 text-xs ${topic === undefined ? "btn-primary" : ""}`}
              onClick={() => setTopic(undefined)}
            >
              All topics
            </button>
            {topics.map((t) => (
              <button
                key={t.slug}
                type="button"
                className={`btn px-3 py-1 text-xs ${topic === t.slug ? "btn-primary" : ""}`}
                onClick={() => setTopic(t.slug)}
              >
                {t.name}
              </button>
            ))}
          </div>
        </div>

        {/* Tier filter */}
        <div className="space-y-2">
          <p className="label">Difficulty</p>
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
        </div>

        {problems.isLoading && <p className="font-body text-sm text-muted">Loading…</p>}
        {problems.isError && (
          <p className="font-body text-sm text-accent">Could not load problems.</p>
        )}

        {!problems.isLoading && !problems.isError && (
          <p className="font-body text-sm text-muted">
            Showing {items.length} of {allItems.length} · {solvedCount} solved
          </p>
        )}

        <ul className="space-y-2">
          {items.map((problem) => (
            <li key={problem.id}>
              <Link
                href={`/practice/${problem.id}`}
                prefetch
                onMouseEnter={() => prefetch(problem.id)}
                onFocus={() => prefetch(problem.id)}
                className="card flex items-center justify-between gap-3 p-3 hover:-translate-x-[1px] hover:-translate-y-[1px]"
              >
                <span className="flex min-w-0 items-center gap-2">
                  <span
                    aria-hidden
                    title={problem.solved ? "Solved" : "Not solved yet"}
                    className={`grid h-5 w-5 shrink-0 place-items-center border-2 text-[11px] font-bold ${
                      problem.solved
                        ? "border-ink bg-accent-2 text-ink"
                        : "border-ink/30 text-transparent"
                    }`}
                  >
                    ✓
                  </span>
                  {problem.generated && (
                    <span
                      className="shrink-0 border-2 border-ink bg-surface px-1.5 py-0.5 font-mono text-[10px] font-bold"
                      title="AI-generated problem"
                    >
                      ✨ AI
                    </span>
                  )}
                  <span className="truncate font-display text-base font-bold">{problem.title}</span>
                  {problem.solved && (
                    <span className="sr-only">Solved</span>
                  )}
                </span>
                <TopicPill label={problem.topic.name} tier={problem.difficulty_tier} />
              </Link>
            </li>
          ))}
        </ul>

        {problems.data && items.length === 0 && (
          <p className="font-body text-sm text-muted">No problems match these filters.</p>
        )}
      </div>
    </AppShell>
  );
}
