"use client";

import { useQuery } from "@tanstack/react-query";

import { AppShell } from "@/components/AppShell";
import { MasteryGrid } from "@/components/MasteryGrid";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function ProfilePage() {
  const { user } = useAuth();
  const progress = useQuery({ queryKey: ["progress"], queryFn: api.progress });
  const account = useQuery({
    queryKey: ["account-summary"],
    queryFn: api.accountSummary,
    retry: false,
  });

  const solved = account.data?.solved_count ?? 0;
  const total = account.data?.total_problems ?? 0;
  const avg = account.data?.avg_score ?? 0;

  return (
    <AppShell>
      <div className="mx-auto max-w-[1000px] space-y-6 px-3 py-6 sm:px-4">
        <h1 className="font-display text-3xl font-bold">Profile</h1>

        <div className="card p-4">
          <p className="label mb-1">Account</p>
          <p className="font-body text-sm">{user?.name}</p>
          <p className="font-mono text-xs text-muted">@{user?.username}</p>
          {user?.email && <p className="font-mono text-xs text-muted">{user.email}</p>}

          <div className="mt-4 grid grid-cols-3 gap-3">
            <div className="card-flat p-3 text-center">
              <p className="font-display text-2xl font-bold">
                {solved}
                <span className="text-base text-muted">/{total}</span>
              </p>
              <p className="label mt-1">Solved</p>
            </div>
            <div className="card-flat p-3 text-center">
              <p className="font-display text-2xl font-bold">{avg}</p>
              <p className="label mt-1">Avg score</p>
            </div>
            <div className="card-flat p-3 text-center">
              <p className="font-display text-2xl font-bold">
                {account.data?.attempts ?? 0}
              </p>
              <p className="label mt-1">Attempts</p>
            </div>
          </div>
        </div>

        <section>
          <h2 className="label mb-2">Topic history</h2>
          <MasteryGrid topics={progress.data?.topics ?? []} />
        </section>
      </div>
    </AppShell>
  );
}
