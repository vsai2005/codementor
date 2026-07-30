"use client";

import { useState } from "react";

/**
 * "Plan first, then code" prompt above the editor. Naming your approach in one
 * sentence before typing forces active recall and gives the AI Coach something
 * to compare your code against in the debrief. It's a soft gate — you can Skip —
 * so it encourages the habit without ever blocking you from coding.
 */
export function PlanFirst({
  plan,
  done,
  onLock,
  onSkip,
  onEdit,
}: {
  plan: string;
  done: boolean;
  onLock: (plan: string) => void;
  onSkip: () => void;
  onEdit: () => void;
}) {
  const [draft, setDraft] = useState(plan);

  if (done) {
    return (
      <div className="card-flat border-l-4 border-l-accent-2 p-3">
        <div className="flex items-center justify-between gap-2">
          <p className="label">🧭 Your plan {plan ? "✓" : "· skipped"}</p>
          <button
            type="button"
            className="font-mono text-xs text-muted underline"
            onClick={onEdit}
          >
            edit
          </button>
        </div>
        {plan && <p className="mt-1 font-body text-sm leading-relaxed">{plan}</p>}
      </div>
    );
  }

  return (
    <div className="card-flat border-l-4 border-l-accent-2 p-3">
      <p className="font-display text-sm font-bold">🧭 Plan first — then code</p>
      <p className="mt-1 font-body text-xs text-muted">
        In one sentence, what&apos;s your approach? Naming it before you type is how the insight
        sticks — and your Coach will check your code against it afterwards.
      </p>
      <textarea
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        rows={2}
        placeholder="e.g. Use a hash set to remember seen values, return true on the first repeat…"
        className="mt-2 w-full resize-none border-2 border-ink bg-surface p-2 font-body text-sm outline-none focus:shadow-hard-sm"
      />
      <div className="mt-2 flex gap-2">
        <button
          type="button"
          className="btn btn-primary px-3 py-1 text-xs"
          onClick={() => onLock(draft.trim())}
          disabled={draft.trim() === ""}
        >
          Lock in my plan
        </button>
        <button type="button" className="btn px-3 py-1 text-xs" onClick={onSkip}>
          Skip
        </button>
      </div>
    </div>
  );
}
