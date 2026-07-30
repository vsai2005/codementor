"use client";

import { AppShell } from "@/components/AppShell";
import { TutorChat } from "@/components/TutorChat";

export default function TutorPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-[820px] px-3 py-6 sm:px-4">
        <h1 className="font-display text-3xl font-bold">Tutor</h1>
        <p className="mt-1 font-body text-sm text-muted">
          Grounded in your past submissions. Recalled notes are shown alongside each reply.
        </p>
        <div className="card mt-4 h-[70vh] p-4">
          <TutorChat />
        </div>
      </div>
    </AppShell>
  );
}
