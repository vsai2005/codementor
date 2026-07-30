"use client";

import { useQuery } from "@tanstack/react-query";

import { AppShell } from "@/components/AppShell";
import { GenerateProblemButton } from "@/components/GenerateProblemButton";
import { MasteryGrid } from "@/components/MasteryGrid";
import { MisconceptionPanel } from "@/components/MisconceptionPanel";
import { MomentumCard } from "@/components/MomentumCard";
import { NextProblemCard } from "@/components/NextProblemCard";
import { ReviewQueueCard } from "@/components/ReviewQueueCard";
import { ScoreTrendChart } from "@/components/ScoreTrendChart";
import { api } from "@/lib/api";

export default function DashboardPage() {
  const progress = useQuery({ queryKey: ["progress"], queryFn: api.progress });
  const trend = useQuery({ queryKey: ["trend"], queryFn: () => api.trend(20) });
  const next = useQuery({
    queryKey: ["next-problem"],
    queryFn: api.nextProblem,
    retry: false,
  });
  const reviewQueue = useQuery({
    queryKey: ["review-queue"],
    queryFn: api.reviewQueue,
    retry: false,
  });
  const misconceptions = useQuery({
    queryKey: ["misconceptions"],
    queryFn: api.misconceptions,
    retry: false,
  });
  const momentum = useQuery({
    queryKey: ["momentum"],
    queryFn: api.momentum,
    retry: false,
  });

  return (
    <AppShell>
      <div className="mx-auto max-w-[1200px] space-y-6 px-3 py-6 sm:px-4">
        <h1 className="font-display text-3xl font-bold">Dashboard</h1>

        <MomentumCard data={momentum.data} />

        <GenerateProblemButton />

        <NextProblemCard problem={next.data ?? null} />

        <ReviewQueueCard data={reviewQueue.data} />

        <MisconceptionPanel data={misconceptions.data} />

        <section>
          <h2 className="label mb-2">Topic mastery</h2>
          {progress.isLoading ? (
            <p className="font-body text-sm text-muted">Loading…</p>
          ) : progress.isError ? (
            <p className="font-body text-sm text-accent">Could not load your progress.</p>
          ) : (
            <MasteryGrid topics={progress.data?.topics ?? []} />
          )}
        </section>

        <section>
          {trend.isLoading ? (
            <p className="font-body text-sm text-muted">Loading trend…</p>
          ) : (
            <ScoreTrendChart points={trend.data?.points ?? []} />
          )}
        </section>
      </div>
    </AppShell>
  );
}
