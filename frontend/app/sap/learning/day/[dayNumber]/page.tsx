"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { sapApi } from "@/lib/sap/api";
import type { SapDayDetail, SapLessonDetail, SapProgressResponse } from "@/lib/sap/types";
import { SapLessonShell } from "@/components/sap/SapLessonShell";

export default function SapDayDetailPage() {
  const params = useParams();
  const router = useRouter();
  const dayNumber = Number(params?.dayNumber);

  const [day, setDay] = useState<SapDayDetail | null>(null);
  const [lesson, setLesson] = useState<SapLessonDetail | null>(null);
  const [progress, setProgress] = useState<SapProgressResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
  const [completeSuccess, setCompleteSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!dayNumber || isNaN(dayNumber)) return;
    setLoading(true);

    // Fetch curriculum overview, authored lesson content, and learner progress in parallel
    Promise.allSettled([
      sapApi.getDayDetail(dayNumber),
      sapApi.getLesson(dayNumber),
      sapApi.getProgress(),
    ])
      .then(([dayRes, lessonRes, progressRes]) => {
        if (dayRes.status === "fulfilled") {
          setDay(dayRes.value);
        }
        if (lessonRes.status === "fulfilled") {
          setLesson(lessonRes.value);
        }
        if (progressRes.status === "fulfilled" && progressRes.value) {
          setProgress(progressRes.value);
        }
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Failed to load SAP milestone.");
        setLoading(false);
      });
  }, [dayNumber]);

  const handleMarkComplete = async () => {
    if (!dayNumber) return;
    setCompleting(true);
    setError(null);
    try {
      await sapApi.completeLesson(dayNumber);
      setCompleteSuccess(true);
      setTimeout(() => {
        router.push("/sap/learning");
      }, 1200);
    } catch (err: any) {
      setError(err.message || "Failed to mark lesson complete.");
    } finally {
      setCompleting(false);
    }
  };

  if (loading) {
    return (
      <AppShell>
        <div className="mx-auto max-w-[1000px] px-4 py-16 text-center text-sm font-bold text-muted">
          Loading SAP Day {dayNumber} Milestone…
        </div>
      </AppShell>
    );
  }

  if (error || (!day && !lesson)) {
    return (
      <AppShell>
        <div className="mx-auto max-w-[800px] px-4 py-12">
          <div className="border-3 border-ink bg-red-100 p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <h2 className="text-lg font-black text-ink">Unable to Load Milestone</h2>
            <p className="text-sm text-red-700 mt-1">{error || "Milestone not found."}</p>
            <Link
              href="/sap/learning"
              className="mt-4 inline-block border-2 border-ink bg-surface px-4 py-2 text-xs font-bold text-ink"
            >
              ← Back to 100-Day Roadmap
            </Link>
          </div>
        </div>
      </AppShell>
    );
  }

  const dayState = progress?.day_states?.[String(dayNumber)];
  const isUnlocked =
    dayNumber === 1 ||
    Boolean(dayState?.unlocked) ||
    Boolean(dayState?.waived) ||
    Boolean(progress && dayNumber <= progress.current_day);

  // Authoritative server-gating: If learner has progress record and this milestone is locked, block access
  if (progress && !isUnlocked) {
    return (
      <AppShell>
        <div className="mx-auto max-w-[800px] px-4 py-16">
          <div className="border-4 border-ink bg-surface p-8 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] text-center space-y-4">
            <div className="mx-auto flex h-14 w-14 items-center justify-center border-3 border-ink bg-amber-100 text-2xl">
              🔒
            </div>
            <h1 className="text-2xl font-black text-ink">
              Milestone Day {dayNumber} is Locked
            </h1>
            <p className="text-sm text-muted max-w-md mx-auto leading-relaxed">
              This milestone requires completing previous prerequisite days. Your current recommended active milestone is{" "}
              <strong className="text-ink font-mono font-black">Day {progress.current_day}</strong>.
            </p>
            <div className="pt-2 flex flex-wrap items-center justify-center gap-3">
              <Link
                href={`/sap/learning/day/${progress.current_day}`}
                className="border-3 border-ink bg-emerald-400 px-5 py-2.5 text-xs font-black uppercase text-ink shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-300 transition-all"
              >
                Go to Active Day {progress.current_day} →
              </Link>
              <Link
                href="/sap/learning"
                className="border-2 border-ink bg-surface px-5 py-2 text-xs font-bold text-ink hover:bg-surface-raised shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
              >
                View Full Roadmap
              </Link>
            </div>
          </div>
        </div>
      </AppShell>
    );
  }

  const nextDayNumber = (day?.day_number || dayNumber) + 1;
  const nextDayState = progress?.day_states?.[String(nextDayNumber)];
  const isNextUnlocked =
    Boolean(nextDayState?.unlocked) ||
    Boolean(nextDayState?.waived) ||
    Boolean(progress && nextDayNumber <= progress.current_day);

  return (
    <AppShell>
      <div className="mx-auto max-w-[1100px] px-4 py-8">
        {/* Breadcrumb Navigation */}
        <div className="mb-6 flex items-center justify-between">
          <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-xs font-mono font-bold text-muted">
            <ol className="flex items-center gap-2">
              <li>
                <Link href="/sap" className="hover:text-ink underline focus-visible:ring-2 focus-visible:ring-ink">
                  SAP HUB
                </Link>
              </li>
              <li aria-hidden="true">/</li>
              <li>
                <Link href="/sap/learning" className="hover:text-ink underline focus-visible:ring-2 focus-visible:ring-ink">
                  ROADMAP
                </Link>
              </li>
              <li aria-hidden="true">/</li>
              <li>
                <span className="text-ink" aria-current="page">DAY {dayNumber}</span>
              </li>
            </ol>
          </nav>
          <Link
            href="/sap/learning"
            className="border border-ink bg-surface px-3 py-1 text-xs font-bold text-ink hover:bg-surface-raised focus-visible:ring-2 focus-visible:ring-ink"
          >
            ← All Milestones
          </Link>
        </div>

        {/* If complete interactive 8-step lesson content exists (Days 1–8), render SapLessonShell */}
        {lesson ? (
          <SapLessonShell
            lesson={lesson}
            initialDayState={dayState}
            onDayComplete={() => setCompleteSuccess(true)}
          />
        ) : day ? (
          /* Fallback for unauthored days (Days 9–100): render curriculum manifest overview */
          <div className="border-4 border-ink bg-surface p-6 sm:p-8 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] mb-8">
            <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
              <div className="flex items-center gap-2">
                <span className="border-2 border-ink bg-ink text-surface px-2.5 py-0.5 text-xs font-black font-mono">
                  DAY {day.day_number}
                </span>
                <span className="border border-ink bg-purple-200 px-2 py-0.5 text-xs font-mono font-bold text-ink">
                  Phase {day.phase_number}
                </span>
              </div>
              <span className="text-xs font-mono font-bold text-muted">
                Est. {day.estimated_minutes} Minutes • Tier {day.tier}
              </span>
            </div>

            <h1 className="text-2xl sm:text-3xl font-black text-ink mb-3">{day.title}</h1>
            <p className="text-sm text-muted leading-relaxed mb-6">{day.description}</p>

            {/* Environment Requirements Metadata */}
            <div className="mb-6 border-2 border-ink bg-surface-raised p-4">
              <div className="text-xs font-bold uppercase tracking-wider text-muted mb-1">
                Required Practice Environment
              </div>
              <div className="flex items-center gap-2">
                <span aria-hidden="true" className="inline-block h-2.5 w-2.5 rounded-full bg-emerald-500 animate-ping"></span>
                <span className="font-mono text-sm font-black text-ink capitalize">
                  {day.env_tier.replace(/_/g, " ")}
                </span>
              </div>
              <p className="text-xs text-muted mt-1">
                Deterministic environment metadata managed centrally in the curriculum manifest.
              </p>
            </div>

            {/* Learning Objectives */}
            <div className="mb-6">
              <h2 className="text-sm font-black uppercase text-ink tracking-wider mb-2">
                Learning Objectives
              </h2>
              <ul className="space-y-1.5">
                {day.objectives.map((obj, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-xs sm:text-sm text-ink">
                    <span className="text-emerald-600 font-bold">✓</span>
                    <span>{obj}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Atomic Concepts */}
            <div className="mb-8">
              <h2 className="text-sm font-black uppercase text-ink tracking-wider mb-2">
                Atomic Concepts in Knowledge DAG
              </h2>
              <div className="flex flex-wrap gap-2">
                {day.atomic_concepts.map((concept) => (
                  <span
                    key={concept}
                    className="border-2 border-ink bg-blue-50 px-3 py-1 text-xs font-mono font-bold text-ink"
                  >
                    #{concept}
                  </span>
                ))}
              </div>
            </div>

            {/* Completion Action */}
            <div className="border-t-2 border-ink pt-6 flex flex-wrap items-center justify-between gap-4">
              {completeSuccess ? (
                <div className="border-2 border-ink bg-emerald-300 px-4 py-2 text-xs font-bold text-ink">
                  ✓ Milestone marked complete! Redirecting to roadmap…
                </div>
              ) : (
                <button
                  onClick={handleMarkComplete}
                  disabled={completing}
                  className="border-3 border-ink bg-emerald-400 px-6 py-3 text-sm font-black text-ink shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] transition-all disabled:opacity-50"
                >
                  {completing ? "Recording Progression…" : "Mark Day Complete & Unlock Next →"}
                </button>
              )}

              <div className="flex items-center gap-2">
                {day.day_number > 1 && (
                  <Link
                    href={`/sap/learning/day/${day.day_number - 1}`}
                    className="border border-ink bg-surface px-3 py-1.5 text-xs font-bold text-ink hover:bg-surface-raised"
                  >
                    ← Day {day.day_number - 1}
                  </Link>
                )}
                {day.day_number < 100 && (
                  isNextUnlocked ? (
                    <Link
                      href={`/sap/learning/day/${day.day_number + 1}`}
                      className="border border-ink bg-surface px-3 py-1.5 text-xs font-bold text-ink hover:bg-surface-raised"
                    >
                      Day {day.day_number + 1} →
                    </Link>
                  ) : (
                    <span
                      className="border border-ink/30 bg-muted/10 px-3 py-1.5 text-xs font-bold text-muted cursor-not-allowed opacity-60"
                      title="Next milestone is locked. Complete this day to unlock."
                    >
                      Day {day.day_number + 1} 🔒
                    </span>
                  )
                )}
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </AppShell>
  );
}
