import React, { useEffect } from "react";
import Link from "next/link";
import { CompletionStep } from "@/lib/lessons/types";
import { getPracticeForDay } from "@/lib/curriculum/practiceCoverageMap";
import { useJourney } from "@/lib/curriculum/useJourney";
import { renderInlineText } from "./LessonMarkdown";

interface LessonCompletionProps {
  step: CompletionStep;
  isCompleted: boolean;
  onFinishDay: () => void;
}

export function LessonCompletion({
  step,
  isCompleted,
  onFinishDay,
}: LessonCompletionProps) {
  const { progress, markLessonComplete } = useJourney();
  const practiceMapping = getPracticeForDay(step.dayNumber);
  const dayRecord = progress.day_records?.[step.dayNumber];
  const isPracticePassed = Boolean(dayRecord?.practice_passed || isCompleted);

  // Mark lesson complete on server/journey when reaching completion screen
  useEffect(() => {
    markLessonComplete(step.dayNumber);
  }, [markLessonComplete, step.dayNumber]);

  return (
    <div className="space-y-6">
      {/* Daily Practice Launchpad Card (when practice is required) */}
      {!isPracticePassed && practiceMapping ? (
        <div className="card p-6 sm:p-8 bg-amber-500/10 border-2 border-amber-600 dark:border-amber-500 shadow-hard space-y-4">
          <div className="flex items-center gap-2">
            <span className="bg-amber-500 text-black font-mono text-xs font-bold uppercase px-2.5 py-1 border border-black shadow-hard-sm">
              🎯 DAILY PRACTICE REQUIRED
            </span>
            <span className="text-muted text-xs">•</span>
            <span className="font-mono text-xs font-bold text-ink">
              Day {String(step.dayNumber).padStart(3, "0")} Milestone
            </span>
          </div>

          <h2 className="font-display text-2xl sm:text-3xl font-bold text-ink leading-tight">
            Lesson Finished! Solve Today&apos;s Challenge to Unlock Day {step.dayNumber < 160 ? step.dayNumber + 1 : 160}
          </h2>

          <p className="font-body text-sm sm:text-base text-ink/80 leading-relaxed">
            You&apos;ve mastered today&apos;s core concepts and mental models. To complete Day {step.dayNumber} and authoritatively unlock the next day, solve the daily practice problem in the Practice Portal.
          </p>

          <div className="p-4 border-2 border-black dark:border-border bg-surface shadow-hard-sm flex flex-wrap items-center justify-between gap-3">
            <div>
              <div className="font-mono text-xs text-muted uppercase tracking-wider">Target Problem</div>
              <div className="font-display text-base sm:text-lg font-bold text-ink">{practiceMapping.primary_problem_slug}</div>
              <div className="font-mono text-xs text-muted mt-0.5">Topic: {practiceMapping.topic_name} • Tier {practiceMapping.difficulty_tier}</div>
            </div>

            <Link
              href={`/practice/${practiceMapping.primary_problem_slug}?day=${step.dayNumber}`}
              className="btn btn-primary font-bold shadow-hard flex items-center gap-2 px-5 py-2.5 text-sm"
            >
              <span>Start Daily Practice</span>
              <span>→</span>
            </Link>
          </div>
        </div>
      ) : (
        /* Celebration Header (when day is fully completed) */
        <div className="card p-6 sm:p-8 bg-surface border-2 border-accent-2 shadow-hard">
          <div className="flex items-center gap-2">
            <span className="bg-accent-2 text-white font-mono text-xs font-bold uppercase px-2.5 py-1 border border-ink">
              🎉 DAY COMPLETED
            </span>
            <span className="text-muted text-xs">•</span>
            <span className="font-mono text-xs font-bold text-accent">
              Day {String(step.dayNumber).padStart(3, "0")}
            </span>
          </div>

          <h2 className="mt-3 font-display text-2xl sm:text-3xl font-bold text-ink leading-tight">
            {step.heading}
          </h2>

          <p className="mt-2 font-body text-sm sm:text-base text-ink/80 leading-relaxed">
            {step.subheading}
          </p>

          {/* Action Button */}
          <div className="mt-6 flex flex-wrap items-center gap-3 border-t-2 border-ink/10 pt-4">
            {step.dayNumber < 160 ? (
              <Link
                href={`/learning/day/${step.dayNumber + 1}`}
                className="btn btn-primary font-bold shadow-hard flex items-center gap-2"
              >
                <span>Continue to Day {step.dayNumber + 1}</span>
                <span>→</span>
              </Link>
            ) : (
              <button
                type="button"
                onClick={onFinishDay}
                className="btn btn-primary font-bold shadow-hard flex items-center gap-2"
              >
                <span>✓ 160-Day Curriculum Completed!</span>
              </button>
            )}

            <Link
              href="/learning"
              className="btn font-semibold text-xs border-2 border-ink shadow-hard-sm hover:shadow-hard"
            >
              ← Return to Roadmap
            </Link>
          </div>
        </div>
      )}


      {/* Mastery Recap Table */}
      <div className="card p-6 bg-surface space-y-4">
        <div className="border-b-2 border-ink/10 pb-3">
          <span className="label text-accent font-bold uppercase tracking-wider">
            Mental Model Shift Summary
          </span>
          <h3 className="mt-1 font-display text-lg sm:text-xl font-bold text-ink">
            Naive Intuition vs. Python Reality
          </h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse font-body text-xs sm:text-sm">
            <thead>
              <tr className="border-b-2 border-ink bg-bg/60">
                <th className="py-2.5 px-3 font-mono font-bold uppercase text-ink">Concept</th>
                <th className="py-2.5 px-3 font-mono font-bold uppercase text-muted">The Flawed Myth</th>
                <th className="py-2.5 px-3 font-mono font-bold uppercase text-accent-2">The Python Reality</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-ink/10">
              {step.recapRows.map((row, i) => (
                <tr key={i} className="hover:bg-bg/40 transition-colors">
                  <td className="py-3 px-3 font-mono font-bold text-ink whitespace-nowrap">
                    {renderInlineText(row.concept)}
                  </td>
                  <td className="py-3 px-3 text-muted line-through opacity-80">
                    {renderInlineText(row.naiveIntuition)}
                  </td>
                  <td className="py-3 px-3 font-medium text-ink">
                    {renderInlineText(row.pythonReality)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Solidified Concepts */}
      <div className="card p-6 bg-surface space-y-4">
        <div className="border-b-2 border-ink/10 pb-3">
          <span className="label text-accent-2 font-bold uppercase tracking-wider">
            Foundations Solidified
          </span>
          <h3 className="mt-1 font-display text-lg font-bold text-ink">
            Core Competencies Mastered Today
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
          {step.solidifiedConcepts.map((concept, i) => (
            <div
              key={i}
              className="flex items-center gap-2.5 p-3 border border-ink/20 bg-bg/40 rounded-sm font-body text-xs sm:text-sm text-ink"
            >
              <span className="text-accent-2 font-bold text-base">✓</span>
              <span>{renderInlineText(concept)}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Next Day Preview & Gating Notice */}
      <div className="border-2 border-dashed border-ink/30 bg-surface/60 p-6 space-y-3">
        <div className="flex items-center gap-2">
          <span className="font-mono text-xs font-bold uppercase px-2 py-0.5 border border-ink/30 bg-bg">
            Next Up: Day {String(step.nextDayPreview.dayNumber).padStart(3, "0")}
          </span>
          <span className="text-muted text-xs">•</span>
          <span className="font-mono text-xs text-muted">Curriculum Roadmap</span>
        </div>

        <h4 className="font-display text-base sm:text-lg font-bold text-ink">
          {renderInlineText(step.nextDayPreview.title)}
        </h4>

        <p className="font-body text-xs sm:text-sm text-muted leading-relaxed">
          {renderInlineText(step.nextDayPreview.description)}
        </p>

        <div className="pt-2 border-t border-ink/10 text-xs font-mono text-muted flex items-center gap-2">
          <span>🔒</span>
          <span>
            Passing today&apos;s daily practice challenge will automatically unlock Day {String(step.nextDayPreview.dayNumber).padStart(3, "0")}.
          </span>
        </div>
      </div>
    </div>
  );
}
