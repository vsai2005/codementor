"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { sapApi } from "@/lib/sap/api";
import type { SapLessonDetail, SapLessonStep } from "@/lib/sap/types";
import { ProcessFlow } from "./ProcessFlow";
import { OrgStructureMapper } from "./OrgStructureMapper";
import { MasterDataClassifier } from "./MasterDataClassifier";
import { ArchitectureLayerMapper } from "./ArchitectureLayerMapper";
import { SAPProductSelector } from "./SAPProductSelector";
import { ModuleInteractionVisualizer } from "./ModuleInteractionVisualizer";
import { ScenarioDecision } from "./ScenarioDecision";
import { MissionRecommendation } from "./MissionRecommendation";

interface SapLessonShellProps {
  lesson: SapLessonDetail;
  onDayComplete?: () => void;
}

const STEP_LABELS = [
  "1. Learn",
  "2. Understand",
  "3. Visual / Example",
  "4. Interactive Practice",
  "5. Challenge",
  "6. Assessment",
  "7. Evidence",
  "8. Completion",
];

export function SapLessonShell({ lesson, onDayComplete }: SapLessonShellProps) {
  const router = useRouter();
  const [currentStepIdx, setCurrentStepIdx] = useState<number>(0);
  const [maxUnlockedIdx, setMaxUnlockedIdx] = useState<number>(5); // Steps 0-5 open; 6-7 unlocked after assessment

  // Assessment State
  const [assessmentAnswers, setAssessmentAnswers] = useState<Record<string, string>>({});
  const [submittingAssessment, setSubmittingAssessment] = useState<boolean>(false);
  const [assessmentResult, setAssessmentResult] = useState<any>(null);
  const [assessmentError, setAssessmentError] = useState<string | null>(null);

  // Lesson Completion State
  const [completingLesson, setCompletingLesson] = useState<boolean>(false);
  const [lessonCompleted, setLessonCompleted] = useState<boolean>(false);

  const steps = lesson.steps || [];
  const currentStep = steps[currentStepIdx] || steps[0];

  if (!currentStep) {
    return (
      <div className="border-3 border-ink bg-surface p-8 text-center text-sm font-bold text-muted shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
        No steps authored for this milestone.
      </div>
    );
  }

  const handleNext = () => {
    if (currentStepIdx < steps.length - 1) {
      const nextIdx = currentStepIdx + 1;
      setCurrentStepIdx(nextIdx);
      if (nextIdx > maxUnlockedIdx) {
        setMaxUnlockedIdx(nextIdx);
      }
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handlePrev = () => {
    if (currentStepIdx > 0) {
      setCurrentStepIdx(currentStepIdx - 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleStepJump = (idx: number) => {
    if (idx <= maxUnlockedIdx) {
      setCurrentStepIdx(idx);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  // Submit Assessment
  const handleSubmitAssessment = async () => {
    if (!currentStep) return;
    setSubmittingAssessment(true);
    setAssessmentError(null);

    const questions = currentStep.questions || [];
    const payloadAnswers: Record<string, string> = {};
    questions.forEach((q: any) => {
      payloadAnswers[q.question_id] = assessmentAnswers[q.question_id] || "";
    });

    try {
      const res = await sapApi.submitAssessment({
        day_number: lesson.day_number,
        assessment_id: currentStep.step_id || `day-${lesson.day_number}-assessment`,
        assessment_type: currentStep.multi_concept_eval ? "capstone_multi_concept" : "mcq",
        submission_payload: {
          answers: payloadAnswers,
        },
      });

      setAssessmentResult(res);
      if (res.passed) {
        setMaxUnlockedIdx(steps.length - 1);
      }
    } catch (err: any) {
      setAssessmentError(err.message || "Failed to submit assessment.");
    } finally {
      setSubmittingAssessment(false);
    }
  };

  // Complete Day
  const handleFinishLesson = async () => {
    setCompletingLesson(true);
    try {
      await sapApi.completeLesson(lesson.day_number);
      setLessonCompleted(true);
      if (onDayComplete) {
        onDayComplete();
      }
      setTimeout(() => {
        router.push("/sap/learning");
      }, 1200);
    } catch (err: any) {
      alert(err.message || "Failed to complete lesson.");
    } finally {
      setCompletingLesson(false);
    }
  };

  // Helper to render practice step
  const renderPracticeComponent = (step: SapLessonStep) => {
    switch (step.component_type) {
      case "ProcessFlow":
        return <ProcessFlow flowData={step.flow_data || []} />;
      case "OrgStructureMapper":
        return <OrgStructureMapper units={step.units || []} />;
      case "MasterDataClassifier":
        return <MasterDataClassifier items={step.items || []} />;
      case "ArchitectureLayerMapper":
        return <ArchitectureLayerMapper flowData={step.flow_data || []} />;
      case "SAPProductSelector":
        return <SAPProductSelector scenarios={step.scenarios || []} />;
      case "ModuleInteractionVisualizer":
        return <ModuleInteractionVisualizer flowData={step.flow_data || []} />;
      case "ScenarioDecision":
        return (
          <ScenarioDecision
            title={step.title}
            scenarioMd={step.instruction || ""}
            options={step.options || []}
          />
        );
      default:
        return (
          <div className="border-2 border-ink bg-surface-raised p-4 text-xs font-mono">
            Interactive Practice Component: {step.component_type || "Domain Component"}
          </div>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header Card */}
      <div className="border-4 border-ink bg-surface p-6 shadow-[5px_5px_0px_0px_rgba(0,0,0,1)]">
        <div className="flex flex-wrap items-center justify-between gap-3 mb-2">
          <div className="flex items-center gap-2">
            <span className="border-2 border-ink bg-ink text-surface px-2.5 py-0.5 text-xs font-black font-mono">
              DAY {lesson.day_number}
            </span>
            <span className="text-xs font-mono font-bold text-muted">
              {lesson.estimated_minutes} min • Guided Sequence
            </span>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {lesson.atomic_concepts.map((concept) => (
              <span
                key={concept}
                className="border border-ink/40 bg-purple-50 text-purple-950 px-2 py-0.5 text-[11px] font-mono font-bold"
              >
                #{concept}
              </span>
            ))}
          </div>
        </div>

        <h1 className="text-2xl sm:text-3xl font-black text-ink">
          {lesson.title}
        </h1>
        {lesson.subtitle && (
          <p className="text-xs sm:text-sm text-muted mt-1 font-medium">
            {lesson.subtitle}
          </p>
        )}
      </div>

      {/* 8-Stage Progress Stepper Bar with Responsive Indicator */}
      <div className="border-3 border-ink bg-surface p-3 shadow-hard">
        <div className="sm:hidden mb-2 flex items-center justify-between text-xs font-mono font-bold text-ink">
          <span>STAGE {currentStepIdx + 1} OF {steps.length}</span>
          <span className="uppercase text-muted font-bold">{currentStep.step_type.replace(/_/g, " ")}</span>
        </div>
        <div role="tablist" aria-label="Milestone Stages" className="flex items-center justify-between overflow-x-auto gap-1 pb-1 scrollbar-thin">
          {STEP_LABELS.map((label, idx) => {
            const isCurrent = idx === currentStepIdx;
            const isUnlocked = idx <= maxUnlockedIdx;
            const isPassed = idx < currentStepIdx;

            return (
              <button
                key={idx}
                role="tab"
                aria-selected={isCurrent}
                aria-disabled={!isUnlocked}
                type="button"
                onClick={() => handleStepJump(idx)}
                disabled={!isUnlocked}
                className={`flex-1 min-w-[95px] text-center py-2 px-1 text-[11px] font-mono font-black border-2 border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink focus-visible:outline-none ${
                  isCurrent
                    ? "bg-ink text-surface shadow-[2px_2px_0px_0px_rgba(147,51,234,1)] scale-[1.02]"
                    : isPassed
                    ? "bg-emerald-100 text-emerald-950 hover:bg-emerald-200 border-emerald-700 font-bold"
                    : isUnlocked
                    ? "bg-surface hover:bg-surface-raised text-ink"
                    : "bg-muted/15 text-muted border-ink/30 cursor-not-allowed opacity-75"
                }`}
              >
                {label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Step Content Container */}
      <div className="min-h-[420px]">
        {/* STEP 1: LEARN */}
        {currentStep.step_type === "learn" && (
          <div className="border-3 border-ink bg-surface p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] space-y-5">
            <div className="border-b-2 border-ink pb-3">
              <span className="text-[10px] font-mono font-bold uppercase bg-blue-100 border border-ink text-ink px-2 py-0.5 mr-2">
                Stage 1 • Theoretical Foundation
              </span>
              <h2 className="text-xl font-black text-ink mt-2">
                {currentStep.title}
              </h2>
            </div>

            <div className="prose max-w-none text-sm text-ink leading-relaxed whitespace-pre-line font-medium">
              {currentStep.content_md}
            </div>

            {/* Key Terms */}
            {currentStep.key_terms && currentStep.key_terms.length > 0 && (
              <div className="border-2 border-ink bg-surface-raised p-4">
                <div className="text-xs font-mono font-black uppercase text-ink mb-3">
                  Key Enterprise Vocabulary
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {currentStep.key_terms.map((item, i) => (
                    <div key={i} className="border border-ink/40 bg-surface p-3 text-xs">
                      <div className="font-bold text-ink font-mono mb-1">
                        {item.term}
                      </div>
                      <div className="text-muted leading-relaxed">
                        {item.definition}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Takeaway */}
            {currentStep.takeaway && (
              <div className="border-2 border-emerald-500 bg-emerald-50 p-4 text-xs sm:text-sm text-emerald-950 font-medium">
                <span className="font-bold">Core Takeaway: </span>
                {currentStep.takeaway}
              </div>
            )}
          </div>
        )}

        {/* STEP 2: UNDERSTAND */}
        {currentStep.step_type === "understand" && (
          <div className="border-3 border-ink bg-surface p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] space-y-5">
            <div className="border-b-2 border-ink pb-3">
              <span className="text-[10px] font-mono font-bold uppercase bg-purple-100 border border-ink text-ink px-2 py-0.5 mr-2">
                Stage 2 • Deep Architectural Insight
              </span>
              <h2 className="text-xl font-black text-ink mt-2">
                {currentStep.title}
              </h2>
            </div>

            <div className="prose max-w-none text-sm text-ink leading-relaxed whitespace-pre-line font-medium">
              {currentStep.content_md}
            </div>
          </div>
        )}

        {/* STEP 3: VISUAL / EXAMPLE */}
        {(currentStep.step_type === "visual_example" || currentStep.step_type === "example") && (
          <div className="border-3 border-ink bg-surface p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] space-y-5">
            <div className="border-b-2 border-ink pb-3">
              <span className="text-[10px] font-mono font-bold uppercase bg-indigo-100 border border-ink text-ink px-2 py-0.5 mr-2">
                Stage 3 • Real Digital Twin Case Study
              </span>
              <h2 className="text-xl font-black text-ink mt-2">
                {currentStep.title}
              </h2>
            </div>

            {currentStep.company_context && (
              <div className="border-2 border-ink bg-purple-50 p-3 text-xs font-mono font-bold text-purple-900 flex flex-wrap gap-4">
                <span>Enterprise: {currentStep.company_context.name || currentStep.company_context.company_name || "Nova Manufacturing Corp"}</span>
                <span>Code: {currentStep.company_context.code || currentStep.company_context.company_code || "NM01"}</span>
                {currentStep.company_context.industry && (
                  <span>Industry: {currentStep.company_context.industry}</span>
                )}
              </div>
            )}

            <div className="prose max-w-none text-sm text-ink leading-relaxed whitespace-pre-line font-medium">
              {currentStep.content_md}
            </div>
          </div>
        )}

        {/* STEP 4: INTERACTIVE PRACTICE */}
        {(currentStep.step_type === "interactive_practice" || currentStep.step_type === "practice") && (
          <div className="space-y-4">
            <div className="border-3 border-ink bg-surface p-4 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] font-mono font-bold uppercase bg-emerald-100 border border-ink text-ink px-2 py-0.5">
                  Stage 4 • Hands-On Interactive Lab
                </span>
                <span className="text-xs font-mono text-muted">
                  Component: {currentStep.component_type}
                </span>
              </div>
              <h2 className="text-lg font-black text-ink">
                {currentStep.title}
              </h2>
            </div>

            {renderPracticeComponent(currentStep)}
          </div>
        )}

        {/* STEP 5: CHALLENGE */}
        {currentStep.step_type === "challenge" && (
          <ScenarioDecision
            title={currentStep.title}
            scenarioMd={currentStep.scenario_md || ""}
            options={currentStep.options || []}
          />
        )}

        {/* STEP 6: ASSESSMENT */}
        {currentStep.step_type === "assessment" && (
          <div className="border-3 border-ink bg-surface p-6 shadow-[5px_5px_0px_0px_rgba(0,0,0,1)] space-y-6">
            <div className="border-b-2 border-ink pb-3 flex flex-wrap items-center justify-between gap-2">
              <div>
                <span className="text-[10px] font-mono font-bold uppercase bg-rose-100 border border-ink text-ink px-2 py-0.5 mr-2">
                  Stage 6 • Skill Verification & Evaluation
                </span>
                <h2 className="text-xl font-black text-ink mt-2">
                  {currentStep.title}
                </h2>
              </div>
              <div className="text-xs font-mono font-bold text-muted">
                Passing Threshold: 70%
              </div>
            </div>

            {/* Questions List */}
            <div className="space-y-5">
              {(currentStep.questions || []).map((q: any, qIdx: number) => {
                const selectedVal = assessmentAnswers[q.question_id];
                return (
                  <fieldset
                    key={q.question_id}
                    className="border-2 border-ink bg-surface-raised p-4"
                  >
                    <legend className="sr-only">
                      Question {qIdx + 1} of {(currentStep.questions || []).length}: {q.prompt}
                    </legend>
                    <div className="flex items-center justify-between text-xs font-mono font-bold mb-2">
                      <span className="text-ink">Question {qIdx + 1} of {(currentStep.questions || []).length}</span>
                      {q.concept_slug && (
                        <span className="bg-purple-100 text-purple-900 border border-purple-300 px-1.5 py-0.5 rounded text-[10px]">
                          Concept: #{q.concept_slug}
                        </span>
                      )}
                    </div>

                    <div className="text-sm font-black text-ink mb-3 leading-snug">
                      {q.prompt}
                    </div>

                    <div className="space-y-2">
                      {(q.options || []).map((opt: any) => {
                        const isChosen = selectedVal === opt.id;
                        return (
                          <label
                            key={opt.id}
                            className={`flex items-start gap-3 p-3 border-2 border-ink cursor-pointer transition-all focus-within:ring-2 focus-within:ring-purple-600 focus-within:outline-none ${
                              isChosen
                                ? "bg-ink text-surface font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
                                : "bg-surface hover:bg-surface-raised text-ink"
                            }`}
                          >
                            <input
                              type="radio"
                              name={q.question_id}
                              value={opt.id}
                              checked={isChosen}
                              onChange={() =>
                                setAssessmentAnswers((prev) => ({
                                  ...prev,
                                  [q.question_id]: opt.id,
                                }))
                              }
                              className="mt-0.5 accent-purple-600 focus:ring-0"
                            />
                            <span className="text-xs sm:text-sm font-medium">
                              <span className="font-mono font-black mr-2">
                                [{opt.id}]
                              </span>
                              {opt.label}
                            </span>
                          </label>
                        );
                      })}
                    </div>
                  </fieldset>
                );
              })}
            </div>

            {assessmentError && (
              <div role="alert" className="border-2 border-red-500 bg-red-100 p-3 text-xs text-red-900 font-bold">
                {assessmentError}
              </div>
            )}

            {/* Assessment Feedback & Remediation Capsule Alerts */}
            {assessmentResult && (
              <div role="alert" className="border-3 border-ink p-4 space-y-3 bg-surface-raised">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="text-sm font-black text-ink">
                    Assessment Evaluation:{" "}
                    <span
                      className={
                        assessmentResult.passed
                          ? "text-emerald-700 bg-emerald-100 px-2 py-0.5 border border-emerald-500 font-bold"
                          : "text-red-700 bg-red-100 px-2 py-0.5 border border-red-500 font-bold"
                      }
                    >
                      {Math.round(assessmentResult.score)}%{" "}
                      {assessmentResult.passed ? "— PASSED" : "— NEEDS REVIEW"}
                    </span>
                  </div>
                  {assessmentResult.passed && (
                    <button
                      type="button"
                      onClick={() => handleStepJump(6)}
                      className="border-2 border-ink bg-emerald-300 hover:bg-emerald-200 text-ink px-3 py-1 text-xs font-black uppercase shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all"
                    >
                      Proceed to Step 7: Skill Evidence →
                    </button>
                  )}
                </div>

                {/* Concept-by-Concept breakdown for multi-concept capstones */}
                {assessmentResult.concept_evaluations && (
                  <div className="border border-ink/30 bg-surface p-3">
                    <div className="text-[10px] font-mono font-bold uppercase text-muted mb-2">
                      Multi-Concept Mastery Breakdown
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                      {Object.entries(assessmentResult.concept_evaluations).map(
                        ([concept, evalData]: [string, any]) => (
                          <div
                            key={concept}
                            className={`p-2 border ${
                              evalData.passed
                                ? "border-emerald-300 bg-emerald-50 text-emerald-950"
                                : "border-rose-300 bg-rose-50 text-rose-950"
                            }`}
                          >
                            <div className="font-mono font-bold">#{concept}</div>
                            <div className="text-[11px]">
                              Score: {Math.round(evalData.score)}% ({evalData.passed ? "Validated" : "Deficient"})
                            </div>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}

                {/* Remediation Capsule Recommendation */}
                {assessmentResult.all_remediations &&
                  assessmentResult.all_remediations.length > 0 && (
                    <div className="border-2 border-rose-500 bg-rose-50 p-4 space-y-2">
                      <div className="text-xs font-mono font-black uppercase text-rose-900">
                        ⚡ Targeted Remediation Capsules Triggered
                      </div>
                      <p className="text-xs text-rose-950 leading-relaxed font-medium">
                        Your performance indicated knowledge gaps in the prerequisite DAG. Review these targeted capsules before continuing:
                      </p>
                      <div className="space-y-2">
                        {assessmentResult.all_remediations.map(
                          (capsule: any) => (
                            <div
                              key={capsule.capsule_id}
                              className="border border-rose-400 bg-white p-2.5 text-xs text-ink flex flex-col sm:flex-row sm:items-center justify-between gap-2"
                            >
                              <div>
                                <div className="font-bold text-rose-900">
                                  {capsule.title || "Remediation Topic"}
                                </div>
                                <div className="text-muted text-[11px] mt-0.5">
                                  Prerequisite Concept: #{capsule.deficiency_concept_slug || capsule.target_concept_slug}
                                </div>
                              </div>
                              <span className="self-start sm:self-auto text-[10px] font-mono font-bold uppercase bg-rose-100 text-rose-800 border border-rose-300 px-2 py-0.5">
                                Capsule Active
                              </span>
                            </div>
                          )
                        )}
                      </div>
                    </div>
                  )}

                {assessmentResult.passed && (
                  <div className="text-xs text-emerald-800 font-bold">
                    ✓ Mastery evidence recorded! Step 7 (Evidence) and Step 8 (Completion) are now unlocked.
                  </div>
                )}
              </div>
            )}

            <div className="flex items-center justify-end">
              <button
                type="button"
                onClick={handleSubmitAssessment}
                disabled={submittingAssessment}
                className="border-3 border-ink bg-emerald-400 px-6 py-2.5 text-xs font-black uppercase tracking-wider text-ink shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-300 disabled:opacity-50"
              >
                {submittingAssessment ? "Evaluating Evidence…" : "Submit Assessment →"}
              </button>
            </div>
          </div>
        )}

        {/* STEP 7: EVIDENCE */}
        {(currentStep.step_type === "mastery_evidence" || currentStep.step_type === "evidence") && (
          <div className="border-3 border-ink bg-surface p-6 shadow-[5px_5px_0px_0px_rgba(0,0,0,1)] space-y-5">
            <div className="border-b-2 border-ink pb-3">
              <span className="text-[10px] font-mono font-bold uppercase bg-emerald-100 border border-ink text-ink px-2 py-0.5 mr-2">
                Stage 7 • Enterprise Skill Evidence
              </span>
              <h2 className="text-xl font-black text-ink mt-2">
                {currentStep.title}
              </h2>
            </div>

            <div className="border-2 border-ink bg-gradient-to-r from-emerald-50 to-teal-50 p-5">
              <div className="flex items-center gap-2 text-xs font-mono font-bold text-emerald-900 mb-2">
                <span>🛡️ Skill Evidence Verified & Logged</span>
              </div>
              <h3 className="text-base font-black text-ink mb-1">
                Deterministic Competency Proof
              </h3>
              <p className="text-xs sm:text-sm text-ink/80 leading-relaxed font-medium">
                {currentStep.evidence_rule ||
                  "Demonstrated architectural understanding and practical decision capability in Nova Manufacturing Corp."}
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
              <div className="border border-ink/40 bg-surface p-3">
                <div className="text-muted text-[10px] uppercase font-bold">Domain Mode</div>
                <div className="font-bold text-ink mt-0.5">GUIDED LEARNING</div>
              </div>
              <div className="border border-ink/40 bg-surface p-3">
                <div className="text-muted text-[10px] uppercase font-bold">Mastery Weight</div>
                <div className="font-bold text-ink mt-0.5">0.4 Moving Average Impact</div>
              </div>
              <div className="border border-ink/40 bg-surface p-3">
                <div className="text-muted text-[10px] uppercase font-bold">Verification Category</div>
                <div className="font-bold text-ink mt-0.5">STATIC_VALIDATION</div>
              </div>
            </div>
          </div>
        )}

        {/* STEP 8: COMPLETION */}
        {currentStep.step_type === "completion" && (
          <div className="space-y-6">
            <div className="border-3 border-ink bg-surface p-6 shadow-[5px_5px_0px_0px_rgba(0,0,0,1)] space-y-4">
              <div className="border-b-2 border-ink pb-3">
                <span className="text-[10px] font-mono font-bold uppercase bg-emerald-300 border border-ink text-ink px-2.5 py-0.5 mr-2">
                  Stage 8 • Milestone Accomplished
                </span>
                <h2 className="text-xl font-black text-ink mt-2">
                  Day {lesson.day_number} Milestone Complete!
                </h2>
              </div>

              <div className="prose max-w-none text-sm text-ink leading-relaxed whitespace-pre-line font-medium">
                {currentStep.summary_md}
              </div>

              {lessonCompleted ? (
                <div className="border-2 border-ink bg-emerald-300 px-4 py-3 text-xs font-bold text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
                  ✓ Day progression successfully saved! Returning to roadmap…
                </div>
              ) : (
                <button
                  type="button"
                  onClick={handleFinishLesson}
                  disabled={completingLesson}
                  className="border-3 border-ink bg-emerald-400 px-8 py-3 text-sm font-black uppercase tracking-wider text-ink shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-300 hover:translate-x-0.5 hover:translate-y-0.5 transition-all disabled:opacity-50"
                >
                  {completingLesson ? "Saving Day Progression…" : "Mark Day Complete & Unlock Next Milestone →"}
                </button>
              )}
            </div>

            {/* Companion Mission Recommendation Card */}
            {currentStep.recommended_mission && (
              <MissionRecommendation
                mission={currentStep.recommended_mission}
              />
            )}
          </div>
        )}
      </div>

      {/* Step Navigation Bottom Bar */}
      <div className="flex items-center justify-between border-t-2 border-ink pt-4">
        <button
          type="button"
          onClick={handlePrev}
          disabled={currentStepIdx === 0}
          className="border-2 border-ink bg-surface px-4 py-2 text-xs font-bold text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-surface-raised disabled:opacity-40 disabled:cursor-not-allowed"
        >
          ← Previous Stage
        </button>

        <div className="text-xs font-mono text-muted">
          Step {currentStepIdx + 1} of {steps.length}
        </div>

        <button
          type="button"
          onClick={handleNext}
          disabled={currentStepIdx === steps.length - 1 || currentStepIdx >= maxUnlockedIdx}
          className="border-2 border-ink bg-ink text-surface px-5 py-2 text-xs font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-ink/90 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          Next Stage →
        </button>
      </div>
    </div>
  );
}
