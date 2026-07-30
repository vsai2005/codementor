"use client";

import { useQuery } from "@tanstack/react-query";

import { AppShell } from "@/components/AppShell";
import { MasteryGrid } from "@/components/MasteryGrid";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function ProfilePage() {
  const { user } = useAuth();
  const progress = useQuery({ queryKey: ["progress"], queryFn: api.progress });

  return (
    <AppShell>
      <div className="mx-auto max-w-[1000px] space-y-6 px-3 py-6 sm:px-4">
        <h1 className="font-display text-3xl font-bold">Profile</h1>

        <div className="card p-4">
          <p className="label mb-1">Account</p>
          <p className="font-body text-sm">{user?.name}</p>
          <p className="font-mono text-xs text-muted">@{user?.username}</p>
          {user?.email && <p className="font-mono text-xs text-muted">{user.email}</p>}
        </div>

        <section>
          <h2 className="label mb-2">Topic history</h2>
          <MasteryGrid topics={progress.data?.topics ?? []} />
        </section>
      </div>
    </AppShell>
  );
}
