"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { sapApi } from "@/lib/sap/api";
import type { SapAssessmentSubmitResponse, SapWaivedDayChallenge } from "@/lib/sap/types";

/**
 * Waived-day challenge: a learner whose placement skipped this day can earn its concepts
 * by passing the day's assessment. Grading happens on the server; the day stays waived and
 * its lesson stays closed.
 */
export default function SapWaivedDayChallengePage() {
  const params = useParams();
  const dayNumber = Number(params?.dayNumber);

  const [challenge, setChallenge] = useState<SapWaivedDayChallenge | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [result, setResult] = useState<SapAssessmentSubmitResponse | null>(null);

  useEffect(() => {
    if (!dayNumber || isNaN(dayNumber)) return;
    setLoading(true);
    setLoadError(null);
    sapApi
      .getWaivedDayChallenge(dayNumber)
      .then(setChallenge)
      .catch((err: any) => setLoadError(err?.message || "Could not load this challenge."))
      .finally(() => setLoading(false));
  }, [dayNumber]);

  const questions = challenge?.questions || [];
  const qid = (q: SapWaivedDayChallenge["questions"][number], i: number) =>
    q.id || q.question_id || `q${i + 1}`;
  const allAnswered = questions.length > 0 && questions.every((q, i) => Boolean(answers[qid(q, i)]));

  const handleSubmit = async () => {
    if (!challenge) return;
    setSubmitting(true);
    setSubmitError(null);
    try {
      const res = await sapApi.submitWaivedDayChallenge({
        day_number: challenge.day_number,
        assessment_id: challenge.assessment_id,
        assessment_type: challenge.assessment_type as any,
        submission_payload: { answers },
      });
      setResult(res);
    } catch (err: any) {
      setSubmitError(err?.message || "Failed to submit the challenge.");
    } finally {
      setSubmitting(false);
    }
  };

  const retry = () => {
    setResult(null);
    setAnswers({});
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <AppShell>
      <div className="mx-auto max-w-[900px] px-4 py-8">
        <div className="mb-6 flex items-center gap-2 text-xs font-mono font-bold text-muted">
          <Link href="/sap/learning" className="hover:text-ink underline">ROADMAP</Link>
          <span>/</span>
          <span className="text-ink">DAY {dayNumber} CHALLENGE</span>
        </div>

        {loading && <div className="text-sm font-mono font-bold">Loading challenge…</div>}

        {loadError && (
          <div role="alert" className="border-2 border-red-500 bg-red-100 p-4 text-sm font-bold text-red-900">
            ⚠ {loadError}
            <div className="mt-3">
              <Link href="/sap/learning" className="underline">Back to roadmap</Link>
            </div>
          </div>
        )}

        {challenge && (
          <div className="border-4 border-ink bg-surface p-6 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] space-y-6">
            <div>
              <span className="border-2 border-ink bg-sky-200 px-2.5 py-0.5 text-xs font-mono font-bold uppercase text-ink">
                Waived-day challenge
              </span>
              <h1 className="mt-3 text-2xl font-black text-ink">
                Day {challenge.day_number}: {challenge.day_title}
              </h1>
              <p className="mt-2 text-xs text-muted leading-relaxed max-w-2xl">
                Your placement skipped this day. Pass its assessment to earn these concepts toward
                missions and later prerequisites. The day stays waived and does not change your
                current day.
              </p>
            </div>

            {!result && (
              <>
                {questions.map((q, i) => {
                  const id = qid(q, i);
                  return (
                    <fieldset key={id} className="border-2 border-ink p-4">
                      <legend className="px-1 text-xs font-mono font-bold text-muted">
                        Question {i + 1} of {questions.length}
                      </legend>
                      <p className="text-sm font-bold text-ink mb-3">{q.prompt || q.question}</p>
                      <div className="space-y-2">
                        {(q.options || []).map((opt) => (
                          <label
                            key={opt.id}
                            className={`flex items-start gap-3 border-2 border-ink p-3 cursor-pointer ${
                              answers[id] === opt.id ? "bg-amber-100" : "bg-surface hover:bg-surface-raised"
                            }`}
                          >
                            <input
                              type="radio"
                              name={id}
                              value={opt.id}
                              checked={answers[id] === opt.id}
                              onChange={() => setAnswers((prev) => ({ ...prev, [id]: opt.id }))}
                              className="mt-0.5"
                            />
                            <span className="text-sm text-ink">{opt.label || opt.text}</span>
                          </label>
                        ))}
                      </div>
                    </fieldset>
                  );
                })}

                {submitError && (
                  <div role="alert" className="border-2 border-red-500 bg-red-100 p-3 text-xs font-bold text-red-900">
                    ⚠ {submitError}
                  </div>
                )}

                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={!allAnswered || submitting}
                  className="border-2 border-ink bg-emerald-400 hover:bg-emerald-300 disabled:opacity-40 px-5 py-2.5 text-xs font-black uppercase text-ink shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]"
                >
                  {submitting ? "Grading…" : "Submit Challenge →"}
                </button>
              </>
            )}

            {result && (
              <div
                role="alert"
                className={`border-3 border-ink p-5 ${result.passed ? "bg-emerald-50" : "bg-rose-50"}`}
              >
                <div className="font-mono text-xs font-black uppercase">
                  {result.passed ? "✓ Challenge passed" : "✗ Challenge not passed"} — {Math.round(result.score)}%
                </div>
                <p className="mt-2 text-sm text-ink">{result.feedback}</p>
                {result.concept_evaluations?.length > 0 && (
                  <ul className="mt-3 space-y-1 text-xs font-mono">
                    {result.concept_evaluations.map((c) => (
                      <li key={c.concept_slug}>
                        {c.passed ? "✓" : "✗"} {c.concept_slug}: {Math.round(c.score)}%
                      </li>
                    ))}
                  </ul>
                )}
                <div className="mt-4 flex gap-3">
                  {!result.passed && (
                    <button type="button" onClick={retry} className="border-2 border-ink bg-surface px-3 py-1.5 text-xs font-bold">
                      Try again
                    </button>
                  )}
                  <Link href="/sap/learning" className="border-2 border-ink bg-ink text-surface px-3 py-1.5 text-xs font-bold">
                    Back to roadmap
                  </Link>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}
