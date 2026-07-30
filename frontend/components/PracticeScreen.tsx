"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { ApiError, api } from "@/lib/api";
import { useAutosave } from "@/lib/useAutosave";
import type { MomentumDelta, ProblemDetail, TestsResponse } from "@/lib/types";
import { AiCoach, type CoachSubmission } from "./AiCoach";
import { CodeEditor } from "./CodeEditor";
import { ConceptLesson } from "./ConceptLesson";
import { MomentumBanner } from "./MomentumBanner";
import { PlanFirst } from "./PlanFirst";
import { ProblemStatement } from "./ProblemStatement";
import { ReferenceSolution } from "./ReferenceSolution";
import { ReviewPanel, type ReviewPanelState } from "./ReviewPanel";
import { TestResultsPanel } from "./TestResultsPanel";
import { TestSandbox } from "./TestSandbox";

type MobileTab = "problem" | "editor" | "review";

const TABS: { id: MobileTab; label: string }[] = [
  { id: "problem", label: "Problem" },
  { id: "editor", label: "Code" },
  { id: "review", label: "Review" },
];

export function PracticeScreen({ problem }: { problem: ProblemDetail }) {
  const starter = problem.starter_code["python"] ?? "";
  const [code, setCode] = useState(starter);
  const [tests, setTests] = useState<TestsResponse | null>(null);
  const [review, setReview] = useState<ReviewPanelState>({ kind: "idle" });
  const [running, setRunning] = useState(false);
  const [tab, setTab] = useState<MobileTab>("problem");
  const [nextProblem, setNextProblem] = useState<ProblemDetail | null>(null);
  // Third column can show the scored Review or the conversational AI Coach.
  const [assistTab, setAssistTab] = useState<"review" | "coach">("coach");
  const [coachSubmission, setCoachSubmission] = useState<CoachSubmission | null>(null);
  // "Plan first" — the learner's one-sentence approach, captured before coding.
  const [plan, setPlan] = useState("");
  const [planDone, setPlanDone] = useState(false);
  // Momentum reward strip + whether the problem has been solved (unlocks the
  // reference solution).
  const [momentum, setMomentum] = useState<MomentumDelta | null>(null);
  const [solved, setSolved] = useState(false);

  const { restored, savedAt } = useAutosave(problem.id, code);

  // A ref, not the `running` state: two clicks in the same tick both read the
  // pre-update state value, so state alone does not deduplicate them.
  const inFlight = useRef(false);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (restored !== null && restored !== "") setCode(restored);
  }, [restored]);

  useEffect(() => () => abortRef.current?.abort(), []);

  const submitting = review.kind === "loading";
  const busy = submitting || running;

  const handleRun = useCallback(async () => {
    if (inFlight.current) return;
    inFlight.current = true;
    setRunning(true);
    abortRef.current = new AbortController();

    try {
      const result = await api.runTests(
        { problem_id: problem.id, language: "python", code },
        abortRef.current.signal,
      );
      setTests(result);
    } catch (error) {
      const message =
        error instanceof ApiError ? error.message : "Could not run your code. Try again.";
      setReview({ kind: "error", message });
      setTab("review");
    } finally {
      inFlight.current = false;
      setRunning(false);
    }
  }, [code, problem.id]);

  const handleSubmit = useCallback(async () => {
    if (inFlight.current) return;
    inFlight.current = true;
    setReview({ kind: "loading" });
    setTab("review");
    abortRef.current = new AbortController();

    try {
      const result = await api.submit(
        { problem_id: problem.id, language: "python", code, plan },
        abortRef.current.signal,
      );
      setTests(result.tests);
      setReview({ kind: "result", review: result.review, difficulty: result.difficulty });
      // Hand the finished submission to the AI Coach and surface the warm
      // debrief (praise + where to improve) right after submitting. The plan
      // (if any) lets the coach check whether the code matched the intent.
      setCoachSubmission({
        key: result.submission_id,
        review: result.review,
        tests: result.tests,
        plan,
      });
      setAssistTab("coach");
      // Reward strip (XP / streak / badges) + unlock the reference solution.
      if (result.momentum) setMomentum(result.momentum);
      if (result.tests.all_passed) setSolved(true);
      // Only unlock "next problem" once every test passes — a failing solution
      // keeps you on this problem.
      if (result.tests.all_passed) {
        api.nextProblem().then(setNextProblem).catch(() => setNextProblem(null));
      } else {
        setNextProblem(null);
      }
    } catch (error) {
      // The user's code stays in state and in localStorage — never cleared here.
      if (error instanceof ApiError) {
        setReview({ kind: "error", message: error.message, retryAfterS: error.retryAfterS });
      } else {
        setReview({
          kind: "error",
          message: "Something went wrong reaching the server. Your code is safe.",
        });
      }
    } finally {
      inFlight.current = false;
    }
  }, [code, problem.id, plan]);

  const columnClass = (id: MobileTab) =>
    `${tab === id ? "block" : "hidden"} lg:block min-w-0`;

  return (
    <div className="mx-auto w-full max-w-[1600px] px-3 py-4 sm:px-4">
      {/* Mobile tab bar — hidden once three columns fit */}
      <div className="mb-3 flex gap-2 lg:hidden" role="tablist">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            role="tab"
            aria-selected={tab === t.id}
            onClick={() => setTab(t.id)}
            className={`btn flex-1 px-2 text-xs ${tab === t.id ? "btn-primary" : ""}`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {momentum && (
        <MomentumBanner momentum={momentum} onDismiss={() => setMomentum(null)} />
      )}

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[minmax(0,0.95fr)_minmax(0,1.3fr)_minmax(0,1fr)]">
        {/* Column 1 — problem */}
        <section className={columnClass("problem")} aria-label="Problem statement">
          <div className="card h-full space-y-4 overflow-y-auto p-4 lg:max-h-[calc(100vh-8rem)]">
            {problem.generated && (
              <div className="card-flat border-l-4 border-l-accent-2 p-2">
                <p className="font-body text-xs">
                  <span className="font-bold">✨ AI-generated</span>
                  {problem.generation
                    ? ` · ${problem.generation.topic} · Tier ${problem.generation.tier} · ${problem.generation.validated_cases} validated tests`
                    : " · a fresh problem targeting your weakest area"}
                </p>
              </div>
            )}
            <ProblemStatement problem={problem} />
            <ConceptLesson concept={problem.concept} />
            <ReferenceSolution problemId={problem.id} unlocked={solved} />
          </div>
        </section>

        {/* Column 2 — editor */}
        <section className={columnClass("editor")} aria-label="Code editor">
          <div className="flex h-full flex-col gap-3">
            <PlanFirst
              plan={plan}
              done={planDone}
              onLock={(p) => {
                setPlan(p);
                setPlanDone(true);
              }}
              onSkip={() => setPlanDone(true)}
              onEdit={() => setPlanDone(false)}
            />
            <div className="min-h-[320px] flex-1 lg:max-h-[calc(100vh-14rem)]">
              <CodeEditor value={code} onChange={setCode} readOnly={busy} />
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <button type="button" className="btn" onClick={handleRun} disabled={busy}>
                {running ? "Running…" : "Run"}
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleSubmit}
                disabled={busy}
              >
                {submitting ? "Reviewing…" : "Submit"}
              </button>
              <span className="ml-auto font-mono text-xs text-muted">
                {savedAt ? `saved ${new Date(savedAt).toLocaleTimeString()}` : "autosave on"}
              </span>
            </div>

            {tests && <TestResultsPanel tests={tests} />}

            <TestSandbox problemId={problem.id} code={code} entryPoint={problem.entry_point} />
          </div>
        </section>

        {/* Column 3 — AI Coach + scored review, toggled by sub-tabs */}
        <section className={columnClass("review")} aria-label="Assistant panel">
          <div className="flex h-full flex-col lg:max-h-[calc(100vh-8rem)]">
            <div className="mb-2 flex gap-2" role="tablist" aria-label="Assistant view">
              <button
                type="button"
                role="tab"
                aria-selected={assistTab === "coach"}
                onClick={() => setAssistTab("coach")}
                className={`btn flex-1 px-2 py-1 text-xs ${assistTab === "coach" ? "btn-primary" : ""}`}
              >
                🤖 AI Coach
              </button>
              <button
                type="button"
                role="tab"
                aria-selected={assistTab === "review"}
                onClick={() => setAssistTab("review")}
                className={`btn flex-1 px-2 py-1 text-xs ${assistTab === "review" ? "btn-primary" : ""}`}
              >
                Review
                {review.kind === "result" && <span className="ml-1">✓</span>}
              </button>
            </div>

            <div className="card min-h-0 flex-1 overflow-y-auto p-4">
              {assistTab === "coach" ? (
                <AiCoach problem={problem} code={code} submission={coachSubmission} />
              ) : (
                <ReviewPanel state={review} onRetry={handleSubmit} nextProblem={nextProblem} />
              )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
