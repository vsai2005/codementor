"use client";

import { useEffect, useState } from "react";

import type {
  DifficultyChange,
  Issue,
  MemoryNote,
  ProblemDetail,
  Review,
  Severity,
} from "@/lib/types";
import { DifficultyBanner } from "./DifficultyBanner";
import { MemoryNoteCard } from "./MemoryNoteCard";
import { NextProblemCard } from "./NextProblemCard";
import { ScoreBar } from "./ScoreBar";

export type ReviewPanelState =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "result"; review: Review; difficulty: DifficultyChange; notes?: MemoryNote[] }
  | { kind: "error"; message: string; retryAfterS?: number | null };

const SEVERITY_STYLES: Record<Severity, string> = {
  critical: "border-l-4 border-l-accent bg-accent/5",
  major: "border-l-4 border-l-accent",
  minor: "border-l-4 border-l-muted",
};

const STAGES = [
  "Running tests…",
  "Analysing complexity…",
  "Reviewing code…",
  "Scoring submission…",
];

const TIMEOUT_MS = 8000;

/** PRD 4.4: staged progress text, timing out at 8s with a clear message. */
function LoadingState() {
  const [stage, setStage] = useState(0);
  const [timedOut, setTimedOut] = useState(false);

  useEffect(() => {
    const ticker = window.setInterval(() => {
      setStage((s) => Math.min(s + 1, STAGES.length - 1));
    }, 1800);
    const timeout = window.setTimeout(() => setTimedOut(true), TIMEOUT_MS);
    return () => {
      window.clearInterval(ticker);
      window.clearTimeout(timeout);
    };
  }, []);

  return (
    <div className="space-y-4" aria-live="polite" aria-busy="true">
      <p className="font-body text-sm font-semibold">
        {timedOut ? "Still working — this is slower than usual." : STAGES[stage]}
      </p>

      <div className="space-y-2">
        {[0, 1, 2, 3, 4].map((i) => (
          <div key={i} className="h-3 w-full border-2 border-ink bg-surface">
            <div
              className="h-full animate-pulse bg-ink/15"
              style={{ width: `${40 + ((i * 17) % 50)}%` }}
            />
          </div>
        ))}
      </div>

      {timedOut && (
        <p className="font-body text-xs text-muted">
          Your code is saved. If this does not finish shortly, submit again — the review
          may come back without the AI analysis.
        </p>
      )}
    </div>
  );
}

function IssueRow({ issue }: { issue: Issue }) {
  return (
    <li className={`${SEVERITY_STYLES[issue.severity]} bg-surface p-2 pl-3`}>
      <p className="font-body text-sm font-semibold">
        {issue.title}
        {issue.line !== null && (
          <span className="ml-2 font-mono text-xs text-muted">line {issue.line}</span>
        )}
      </p>
      <p className="mt-0.5 font-body text-xs text-muted">{issue.detail}</p>
    </li>
  );
}

function ScoreBadge({ score, degraded }: { score: number; degraded: boolean }) {
  const tone = score >= 80 ? "bg-accent-2" : score >= 50 ? "bg-accent" : "bg-ink";
  return (
    <div className="flex items-center gap-3">
      <div
        className={`flex h-16 w-16 shrink-0 items-center justify-center border-2 border-ink ${tone} text-white shadow-hard`}
      >
        <span className="font-display text-2xl font-bold tabular-nums">{score}</span>
      </div>
      <div>
        <p className="label">Overall score</p>
        {degraded && (
          <p className="mt-0.5 font-body text-xs text-accent">
            Tests only — the AI reviewer was unavailable.
          </p>
        )}
      </div>
    </div>
  );
}

function ResultState({
  review,
  difficulty,
  notes,
  nextProblem,
}: {
  review: Review;
  difficulty: DifficultyChange;
  notes?: MemoryNote[];
  nextProblem?: ProblemDetail | null;
}) {
  return (
    <div className="space-y-4">
      <ScoreBadge score={review.overall_score} degraded={review.review_degraded} />

      <DifficultyBanner difficulty={difficulty} />

      <div className="space-y-2">
        <p className="label">Breakdown</p>
        <ScoreBar label="Correctness" value={review.scores.correctness} weight={0.4} />
        <ScoreBar label="Time complexity" value={review.scores.time_complexity} weight={0.25} />
        <ScoreBar label="Readability" value={review.scores.readability} weight={0.15} />
        <ScoreBar label="Edge cases" value={review.scores.edge_cases} weight={0.12} />
        <ScoreBar label="Space complexity" value={review.scores.space_complexity} weight={0.08} />
      </div>

      <div className="card-flat p-3">
        <p className="label mb-1">Complexity</p>
        <dl className="grid grid-cols-2 gap-2 font-mono text-sm">
          <div>
            <dt className="text-xs text-muted">yours</dt>
            <dd>
              {review.detected_complexity.time} / {review.detected_complexity.space}
            </dd>
          </div>
          <div>
            <dt className="text-xs text-muted">optimal</dt>
            <dd>
              {review.optimal_complexity.time} / {review.optimal_complexity.space}
            </dd>
          </div>
        </dl>
      </div>

      <div>
        <p className="label mb-1">Summary</p>
        <p className="font-body text-sm leading-relaxed">{review.summary}</p>
      </div>

      {review.issues.length > 0 && (
        <div>
          <p className="label mb-1">Issues</p>
          <ul className="space-y-2">
            {review.issues.map((issue, i) => (
              <IssueRow key={`${issue.title}-${i}`} issue={issue} />
            ))}
          </ul>
        </div>
      )}

      <div className="card-flat border-l-4 border-l-accent-2 p-3">
        <p className="label mb-1">Improvement hint</p>
        <p className="font-body text-sm">{review.improvement_hint}</p>
      </div>

      {review.weak_topics.length > 0 && (
        <div>
          <p className="label mb-1">Flagged weak topics</p>
          <div className="flex flex-wrap gap-2">
            {review.weak_topics.map((topic) => (
              <span
                key={topic}
                className="border-2 border-ink bg-surface px-2 py-0.5 font-body text-xs font-semibold"
              >
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}

      {notes && notes.length > 0 && (
        <div className="space-y-2">
          {notes.map((note) => (
            <MemoryNoteCard key={note.id} note={note} />
          ))}
        </div>
      )}

      {nextProblem && <NextProblemCard problem={nextProblem} />}
    </div>
  );
}

interface ReviewPanelProps {
  state: ReviewPanelState;
  onRetry: () => void;
  nextProblem?: ProblemDetail | null;
}

export function ReviewPanel({ state, onRetry, nextProblem }: ReviewPanelProps) {
  if (state.kind === "idle") {
    return (
      <div className="flex h-full min-h-[200px] items-center justify-center p-6 text-center">
        <p className="font-body text-sm text-muted">Submit your solution to get a review.</p>
      </div>
    );
  }

  if (state.kind === "loading") return <LoadingState />;

  if (state.kind === "error") {
    return (
      <div className="space-y-3" role="alert">
        <p className="font-display text-lg font-bold">Review failed</p>
        <p className="font-body text-sm text-muted">{state.message}</p>
        {state.retryAfterS ? (
          <p className="font-mono text-xs text-muted">Try again in {state.retryAfterS}s.</p>
        ) : null}
        <p className="font-body text-xs text-muted">Your code has not been lost.</p>
        <button type="button" className="btn btn-primary" onClick={onRetry}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <ResultState
      review={state.review}
      difficulty={state.difficulty}
      notes={state.notes}
      nextProblem={nextProblem}
    />
  );
}
