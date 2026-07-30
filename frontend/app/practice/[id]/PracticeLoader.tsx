"use client";

import { useQuery } from "@tanstack/react-query";

import { AppShell } from "@/components/AppShell";
import { PracticeScreen } from "@/components/PracticeScreen";
import { api } from "@/lib/api";

export function PracticeLoader({ problemId }: { problemId: string }) {
  const problem = useQuery({
    queryKey: ["problem", problemId],
    queryFn: () => api.getProblem(problemId),
  });

  return (
    <AppShell>
      {problem.isLoading && (
        <p className="p-6 font-body text-sm text-muted">Loading problem…</p>
      )}
      {problem.isError && (
        <p className="p-6 font-body text-sm text-accent">
          Could not load this problem. It may have been removed.
        </p>
      )}
      {problem.data && <PracticeScreen problem={problem.data} />}
    </AppShell>
  );
}
