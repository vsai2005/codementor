"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { sapApi } from "@/lib/sap/api";
import type {
  SapMissionDetail,
  SapAssistanceLevel,
  SapMissionStepAttemptResponse,
} from "@/lib/sap/types";

export default function SapMissionDetailPage() {
  const params = useParams();
  const slug = params.slug as string;

  const [mission, setMission] = useState<SapMissionDetail | null>(null);
  const [assistanceLevel, setAssistanceLevel] = useState<SapAssistanceLevel>("TRAINING");
  const [loading, setLoading] = useState(true);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [selectedOptionId, setSelectedOptionId] = useState<string>("");
  const [submitting, setSubmitting] = useState(false);
  const [stepResult, setStepResult] = useState<SapMissionStepAttemptResponse | null>(null);
  const [missionComplete, setMissionComplete] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;

    sapApi
      .getModes()
      .then((m) => {
        const level = m?.assistance_level || "TRAINING";
        setAssistanceLevel(level);
        return sapApi.getMissionDetail(slug, level);
      })
      .then((detail) => {
        setMission(detail);
        if (detail.current_attempt?.current_step_index) {
          setCurrentStepIndex(detail.current_attempt.current_step_index);
        }
        if (detail.current_attempt?.status === "COMPLETED") {
          setMissionComplete(true);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load mission:", err);
        setLoading(false);
      });
  }, [slug]);

  const handleStartMission = async () => {
    try {
      setActionError(null);
      await sapApi.startMission(slug, assistanceLevel);
      const detail = await sapApi.getMissionDetail(slug, assistanceLevel);
      setMission(detail);
      setCurrentStepIndex(0);
      setStepResult(null);
      setMissionComplete(false);
    } catch (err) {
      console.error("Failed to start mission:", err);
    }
  };

  const handleExecuteStep = async () => {
    if (!mission) return;
    const currentStep = mission.steps[currentStepIndex];
    if (!currentStep) return;

    if (!selectedOptionId) {
      setActionError("Please select an action or configuration parameter to execute.");
      return;
    }

    setActionError(null);
    setSubmitting(true);
    try {
      const res: SapMissionStepAttemptResponse = await sapApi.attemptMissionStep(slug, {
        step_id: currentStep.step_id,
        payload: { selected_option_id: selectedOptionId },
        assistance_level: assistanceLevel,
      });

      setStepResult(res);

      if (res.mission_completed) {
        setMissionComplete(true);
      } else if (res.step_success) {
        // Automatically proceed or wait for next step
      }
    } catch (err: any) {
      setActionError(err.message || "Failed to submit mission step.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleNextStep = () => {
    if (!mission) return;
    setActionError(null);
    setStepResult(null);
    setSelectedOptionId("");
    setCurrentStepIndex((prev) => Math.min(mission.steps.length - 1, prev + 1));
  };

  if (loading) {
    return (
      <AppShell>
        <div className="mx-auto max-w-[1200px] px-4 py-16 text-center">
          <div className="text-xl font-bold font-mono">Loading mission scenario...</div>
        </div>
      </AppShell>
    );
  }

  if (!mission) {
    return (
      <AppShell>
        <div className="mx-auto max-w-[1200px] px-4 py-16 text-center">
          <h1 className="text-2xl font-black text-ink">Mission Not Found</h1>
          <p className="mt-2 text-sm text-muted">The requested mission scenario could not be loaded.</p>
          <Link
            href="/sap/missions"
            className="mt-4 inline-block border-2 border-ink bg-amber-300 px-4 py-2 text-xs font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
          >
            ← Back to Missions
          </Link>
        </div>
      </AppShell>
    );
  }

  const currentStep = mission.steps[currentStepIndex];
  const totalSteps = mission.steps.length;

  return (
    <AppShell>
      <div className="mx-auto max-w-[1200px] px-4 py-8">
        {/* Top Header */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Link
              href="/sap/missions"
              className="text-xs font-mono font-bold underline hover:text-amber-700"
            >
              ← Mission Control
            </Link>
            <span className="text-xs text-muted">/</span>
            <span className="text-xs font-mono font-bold uppercase">{mission.slug}</span>
          </div>

          <div className="flex items-center gap-3 text-xs font-mono">
            <span className="border border-ink bg-surface-raised px-2 py-1">
              Enterprise: <strong>{mission.enterprise_code}</strong>
            </span>
            <span className="border border-ink bg-amber-200 px-2 py-1 font-bold">
              Level: {assistanceLevel}
            </span>
          </div>
        </div>

        {/* Mission Briefing Card */}
        <div className="border-4 border-ink bg-surface p-6 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] mb-8">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
            <span className="border border-ink bg-amber-300 text-ink px-2.5 py-0.5 text-xs font-mono font-bold uppercase">
              {mission.mission_type}
            </span>
            <span className="text-xs font-mono text-muted">
              Estimated Duration: {mission.estimated_minutes} min
            </span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-black text-ink mb-3">{mission.title}</h1>
          <p className="text-sm text-muted leading-relaxed mb-6">{mission.description}</p>

          {/* Context & Assistance Bar */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 border-t-2 border-ink pt-4 text-xs font-mono">
            <div>
              <span className="text-muted block text-[10px] uppercase font-bold">Target Landscape</span>
              <span className="text-ink font-bold">
                {String(mission.company_context?.landscape || "S/4HANA Private Cloud")}
              </span>
            </div>
            <div>
              <span className="text-muted block text-[10px] uppercase font-bold">Aligned Guided Days</span>
              <div className="flex gap-1 mt-0.5">
                {mission.related_days.map((d) => (
                  <Link
                    key={d}
                    href={`/sap/learning/day/${d}`}
                    className="border border-ink bg-emerald-100 hover:bg-emerald-200 px-1.5 py-0.2 text-[10px] font-bold"
                  >
                    Day {d}
                  </Link>
                ))}
              </div>
            </div>
            <div>
              <span className="text-muted block text-[10px] uppercase font-bold">Prerequisite Concepts</span>
              <div className="flex flex-wrap gap-1 mt-0.5">
                {mission.concept_slugs.map((c) => (
                  <span key={c} className="border border-ink/40 bg-surface-raised px-1 py-0.2 text-[9px]">
                    {c}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Assistance Rules / Hints Drawer */}
        {mission.assistance_rules?.allow_hints && mission.assistance_rules.hints && mission.assistance_rules.hints.length > 0 && (
          <div className="border-3 border-ink bg-sky-50 p-4 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] mb-8">
            <div className="text-xs font-mono font-bold uppercase text-sky-900 mb-1">
              ℹ Architecture Hints ({assistanceLevel} Mode)
            </div>
            <ul className="list-disc list-inside space-y-1 text-xs text-sky-950">
              {mission.assistance_rules.hints.map((hint, i) => (
                <li key={i}>{hint}</li>
              ))}
            </ul>
          </div>
        )}

        {assistanceLevel === "JOB" && (
          <div className="border-3 border-ink bg-surface-raised p-3 text-xs font-mono text-muted mb-8">
            ⚠ <strong>Job Role Mode Active:</strong> Hints and primers are disabled. Actions directly affect mission evaluation and skill evidence confidence.
          </div>
        )}

        {/* Mission Execution Workspace */}
        {missionComplete ? (
          <div className="border-4 border-ink bg-emerald-50 p-8 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] text-center">
            <div className="text-4xl mb-2">🎉</div>
            <h2 className="text-2xl font-black text-emerald-950 mb-2">Mission Accomplished!</h2>
            <p className="text-sm text-emerald-900 max-w-xl mx-auto mb-6">
              You have successfully completed the tasks for <strong>{mission.title}</strong>. Nova Manufacturing digital twin state has been updated, and verified evidence has been recorded to your shared skill graph.
            </p>

            <div className="inline-block border-2 border-ink bg-surface p-4 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] mb-6 text-left">
              <div className="text-xs font-mono uppercase text-muted mb-2">Skill Evidence Recorded:</div>
              <ul className="space-y-1 text-xs font-mono">
                {mission.concept_slugs.map((slug) => (
                  <li key={slug} className="flex items-center gap-2">
                    <span className="text-emerald-700 font-bold">✓</span>
                    <span>{slug}</span>
                    <span className="text-muted text-[10px]">(Direct Mastery Impact)</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="flex justify-center gap-4">
              <button
                onClick={handleStartMission}
                className="border-2 border-ink bg-surface hover:bg-surface-raised px-4 py-2 text-xs font-bold text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
              >
                ↻ Retake Mission
              </button>
              <Link
                href="/sap/missions"
                className="border-2 border-ink bg-amber-300 hover:bg-amber-400 px-4 py-2 text-xs font-bold text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
              >
                Return to Missions →
              </Link>
            </div>
          </div>
        ) : (
          <div className="border-4 border-ink bg-surface p-6 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">
            {/* Step Progress Tracker */}
            <div className="flex items-center justify-between border-b-2 border-ink pb-4 mb-6">
              <div>
                <span className="text-xs font-mono uppercase text-muted">
                  Task Step {currentStepIndex + 1} of {totalSteps}
                </span>
                <h2 className="text-xl font-black text-ink">{currentStep?.title}</h2>
              </div>
              <div className="text-xs font-mono font-bold text-muted">
                Progress: {Math.round(((currentStepIndex) / totalSteps) * 100)}%
              </div>
            </div>

            {/* Step Instruction */}
            <div className="mb-6">
              <p className="text-sm text-ink leading-relaxed font-sans">{currentStep?.instruction}</p>
            </div>

            {/* Step Options / Interactive Input */}
            {currentStep?.options && (
              <fieldset className="space-y-3 mb-6">
                <legend className="text-xs font-mono uppercase text-muted font-bold block mb-2">
                  Select Proposed Action / Value:
                </legend>
                {currentStep.options.map((opt) => (
                  <label
                    key={opt.id}
                    className={`block border-2 border-ink p-3.5 cursor-pointer transition-all focus-within:ring-2 focus-within:ring-ink focus-within:outline-none ${
                      selectedOptionId === opt.id
                        ? "bg-amber-100 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] translate-x-[2px]"
                        : "bg-surface hover:bg-surface-raised"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <input
                        type="radio"
                        name="mission_option"
                        value={opt.id}
                        checked={selectedOptionId === opt.id}
                        onChange={() => {
                          setSelectedOptionId(opt.id);
                          setActionError(null);
                        }}
                        className="h-4 w-4 border-2 border-ink focus:ring-0"
                      />
                      <span className="text-sm font-semibold text-ink">{opt.label}</span>
                    </div>
                  </label>
                ))}
              </fieldset>
            )}

            {/* In-place Action Error Banner */}
            {actionError && (
              <div role="alert" className="border-2 border-rose-500 bg-rose-100 p-3 mb-6 text-xs text-rose-950 font-bold">
                ⚠️ {actionError}
              </div>
            )}

            {/* Step Feedback Banner */}
            {stepResult && (
              <div
                role="alert"
                className={`border-3 border-ink p-4 mb-6 ${
                  stepResult.step_success ? "bg-emerald-100 text-emerald-950" : "bg-rose-100 text-rose-950"
                }`}
              >
                <div className="font-bold font-mono text-xs mb-1">
                  {stepResult.step_success ? "✓ Step Verified Successfully" : "✗ Step Verification Failed"}
                </div>
                <div className="text-xs font-medium">{stepResult.step_feedback}</div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex items-center justify-between border-t-2 border-ink pt-4">
              <Link
                href="/sap/missions"
                className="text-xs font-mono text-muted underline hover:text-ink"
              >
                Cancel Mission
              </Link>

              <div className="flex gap-3">
                {stepResult?.step_success && !stepResult.mission_completed ? (
                  <button
                    onClick={handleNextStep}
                    className="border-2 border-ink bg-emerald-400 hover:bg-emerald-500 px-5 py-2.5 text-xs font-bold text-ink shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]"
                  >
                    Proceed to Step {currentStepIndex + 2} →
                  </button>
                ) : (
                  <button
                    onClick={handleExecuteStep}
                    disabled={submitting || !selectedOptionId}
                    className="border-2 border-ink bg-amber-300 hover:bg-amber-400 px-5 py-2.5 text-xs font-bold text-ink shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] disabled:opacity-50 transition-all"
                  >
                    {submitting ? "Evaluating in Digital Twin..." : "Execute & Validate Step →"}
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
