"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { useAuth } from "@/lib/auth";
import { sapApi } from "@/lib/sap/api";
import type { PlacementQuestion, SapPlacementProfile } from "@/lib/sap/types";

type Stage = "select_level" | "assessment" | "results";
type TrackType = "experienced" | "not_sure";

export default function SapPlacementPage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();

  // Navigation / stage state
  const [stage, setStage] = useState<Stage>("select_level");
  const [activeTrack, setActiveTrack] = useState<TrackType>("experienced");

  // Existing profile state
  const [currentProfile, setCurrentProfile] = useState<SapPlacementProfile | null>(null);
  const [loadingProfile, setLoadingProfile] = useState(true);
  const [profileError, setProfileError] = useState<string | null>(null);

  // Assessment questions & answers state (answers preserved across errors/navigation)
  const [questions, setQuestions] = useState<PlacementQuestion[]>([]);
  const [loadingQuestions, setLoadingQuestions] = useState(false);
  const [questionsError, setQuestionsError] = useState<string | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});

  // Submission & evaluation state
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [placementResult, setPlacementResult] = useState<SapPlacementProfile | null>(null);

  // Override start day state
  const [changingStart, setChangingStart] = useState(false);
  const [changeStartError, setChangeStartError] = useState<string | null>(null);

  const loadProfile = async () => {
    setLoadingProfile(true);
    setProfileError(null);
    try {
      const data = await sapApi.getPlacementProfile();
      if (data) {
        setCurrentProfile(data);
      }
    } catch (err: any) {
      // 404 or 401 is normal for new/unauthenticated users
      if (err?.status !== 404 && err?.status !== 401) {
        setProfileError(err?.message || "Could not retrieve existing placement profile.");
      }
    } finally {
      setLoadingProfile(false);
    }
  };

  useEffect(() => {
    if (!authLoading) {
      if (user) {
        loadProfile();
      } else {
        setLoadingProfile(false);
        setCurrentProfile(null);
      }
    }
  }, [user, authLoading]);

  // Handler for Fresher (No assessment needed -> Day 1)
  const handleFresherStart = async () => {
    setSubmitError(null);
    if (!user) {
      router.push("/login?redirect=/sap/placement");
      return;
    }

    setSubmitting(true);
    try {
      const res = await sapApi.submitPlacement({
        experience_level: "fresher",
        answers: {},
      });
      setPlacementResult(res);
      setCurrentProfile(res);
      setStage("results");
    } catch (err: any) {
      setSubmitError(err?.message || "Failed to submit placement. Please check your connection and retry.");
    } finally {
      setSubmitting(false);
    }
  };

  // Handler for launching an assessment track
  const handleStartAssessment = async (track: TrackType) => {
    setActiveTrack(track);
    setLoadingQuestions(true);
    setQuestionsError(null);
    setSubmitError(null);
    setCurrentQuestionIndex(0);

    try {
      const data = await sapApi.getPlacementQuestions(track);
      if (!data || data.length === 0) {
        throw new Error("No assessment questions were returned by the server.");
      }
      setQuestions(data);
      setStage("assessment");
    } catch (err: any) {
      setQuestionsError(err?.message || "Failed to load assessment questions. Please try again.");
    } finally {
      setLoadingQuestions(false);
    }
  };

  // Select an option for the current question (persists in answers map)
  const handleSelectOption = (questionId: string, optionId: string) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: optionId,
    }));
  };

  // Submit assessment answers
  const handleSubmitAssessment = async () => {
    setSubmitError(null);
    if (!user) {
      router.push("/login?redirect=/sap/placement");
      return;
    }

    setSubmitting(true);
    try {
      const res = await sapApi.submitPlacement({
        experience_level: activeTrack,
        answers,
      });
      setPlacementResult(res);
      setCurrentProfile(res);
      setStage("results");
    } catch (err: any) {
      // NOTE: answers state is NOT cleared on failure, so user answers are preserved!
      setSubmitError(err?.message || "Assessment submission failed. Your answers are preserved — click Retry.");
    } finally {
      setSubmitting(false);
    }
  };

  // Override to Start from Day 1
  const handleChooseStartDayOne = async () => {
    setChangeStartError(null);
    setChangingStart(true);
    try {
      const updated = await sapApi.chooseStartDay(1);
      setPlacementResult(updated);
      setCurrentProfile(updated);
      router.push("/sap/learning/day/1");
    } catch (err: any) {
      setChangeStartError(err?.message || "Could not switch starting day to Day 1.");
      setChangingStart(false);
    }
  };

  const answeredCount = questions.filter((q) => Boolean(answers[q.id])).length;
  const currentQuestion = questions[currentQuestionIndex];

  return (
    <AppShell>
      <div className="mx-auto max-w-[1000px] px-4 py-8">
        {/* Navigation Breadcrumb */}
        <div className="mb-6 flex items-center gap-2 text-xs font-mono font-bold text-muted">
          <Link href="/sap" className="hover:text-ink underline">
            SAP HUB
          </Link>
          <span>/</span>
          <span className="text-ink">DIAGNOSTIC PLACEMENT</span>
        </div>

        {/* Guest Mode Alert */}
        {!authLoading && !user && (
          <div className="mb-6 border-2 border-ink bg-amber-50 p-4 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <div className="text-xs font-mono font-bold uppercase text-amber-900">
                  Guest Mode Notice
                </div>
                <p className="text-xs text-ink mt-1">
                  You are viewing as a guest. Sign in to save your diagnostic placement, unlock waived days, and sync your S/4HANA learning progress.
                </p>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <Link
                  href="/login?redirect=/sap/placement"
                  className="border-2 border-ink bg-amber-300 px-3 py-1.5 text-xs font-black text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px] transition-all"
                >
                  Sign In
                </Link>
                <Link
                  href="/register?redirect=/sap/placement"
                  className="border-2 border-ink bg-surface px-3 py-1.5 text-xs font-black text-ink hover:bg-surface-raised transition-all"
                >
                  Register
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* ==================================================================== */}
        {/* STAGE 1: SELECT EXPERIENCE LEVEL                                     */}
        {/* ==================================================================== */}
        {stage === "select_level" && (
          <div className="border-4 border-ink bg-surface p-6 sm:p-8 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">
            <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
              <h1 className="text-2xl sm:text-3xl font-black text-ink">
                SAP S/4HANA Placement Diagnostic
              </h1>
              <span className="border-2 border-ink bg-cyan-200 px-2.5 py-0.5 text-xs font-mono font-bold uppercase text-ink">
                Adaptive Onboarding
              </span>
            </div>
            <p className="text-sm text-muted mb-6 max-w-2xl leading-relaxed">
              We determine your curriculum starting point through an objective evaluation of enterprise concepts and prerequisite mastery. Select your background to begin.
            </p>

            {/* Active profile banner if one exists */}
            {currentProfile && !loadingProfile && (
              <div className="mb-6 border-2 border-ink bg-emerald-50 p-4 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <div className="text-[11px] font-mono font-bold uppercase text-emerald-900">
                      Active Placement on Record
                    </div>
                    <div className="text-sm font-black text-ink mt-0.5">
                      Persona: {currentProfile.persona.toUpperCase()} • Starting Day: Day {currentProfile.recommended_start_day}
                    </div>
                    <p className="text-xs text-muted mt-1 max-w-xl">{currentProfile.rationale}</p>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <button
                      onClick={() => {
                        setPlacementResult(currentProfile);
                        setStage("results");
                      }}
                      className="border-2 border-ink bg-emerald-300 px-3 py-1.5 text-xs font-bold text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-200"
                    >
                      View Results &amp; Path
                    </button>
                    <Link
                      href={`/sap/learning/day/${currentProfile.recommended_start_day}`}
                      className="border-2 border-ink bg-ink text-surface px-3 py-1.5 text-xs font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-neutral-800"
                    >
                      Go to Day {currentProfile.recommended_start_day} →
                    </Link>
                  </div>
                </div>
              </div>
            )}

            {/* Error alerts */}
            {profileError && (
              <div className="mb-6 border-2 border-red-500 bg-red-100 p-4 text-xs font-bold text-red-900 shadow-[3px_3px_0px_0px_rgba(239,68,68,1)] flex items-center justify-between">
                <span>⚠ {profileError}</span>
                <button
                  onClick={loadProfile}
                  className="underline font-black hover:text-red-700 ml-2"
                >
                  Retry Loading Profile
                </button>
              </div>
            )}
            {questionsError && (
              <div className="mb-6 border-2 border-red-500 bg-red-100 p-4 text-xs font-bold text-red-900 shadow-[3px_3px_0px_0px_rgba(239,68,68,1)]">
                <span>⚠ {questionsError}</span>
              </div>
            )}
            {submitError && (
              <div className="mb-6 border-2 border-red-500 bg-red-100 p-4 text-xs font-bold text-red-900 shadow-[3px_3px_0px_0px_rgba(239,68,68,1)]">
                <span>⚠ {submitError}</span>
              </div>
            )}

            {currentProfile?.placement_locked && (
              <div
                role="status"
                className="mb-6 border-2 border-ink bg-sky-50 p-4 text-xs text-ink shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]"
              >
                <div className="font-mono font-bold uppercase text-sky-900">Placement locked</div>
                <p className="mt-1 leading-relaxed">
                  You have started SAP learning, so your placement can no longer be retaken or changed.
                  Your completed and in-progress days are preserved. To earn concepts from days your
                  placement skipped, use <span className="font-bold">Take Challenge</span> on those days in the roadmap.
                </p>
              </div>
            )}

            {/* 3 Experience Options */}
            {!currentProfile?.placement_locked && (
            <div className="space-y-4 mb-8">
              {/* Option 1: Fresher */}
              <div className="border-3 border-ink bg-surface p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all hover:translate-x-[1px] hover:translate-y-[1px]">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="border border-ink bg-emerald-200 px-2 py-0.5 text-xs font-mono font-bold text-ink">
                      OPTION 1
                    </span>
                    <h3 className="text-base font-black text-ink">Fresher / New to ERP</h3>
                  </div>
                  <span className="border border-ink bg-emerald-100 px-2 py-0.5 text-xs font-mono font-bold text-emerald-900">
                    NO ASSESSMENT REQUIRED
                  </span>
                </div>
                <p className="text-xs text-muted mb-4 leading-relaxed">
                  Completely new to enterprise computing or SAP. You will start directly from Day 1 with foundational scaffolding on enterprise architecture, ERP cross-functional flows, and SAP navigation.
                </p>
                <button
                  onClick={handleFresherStart}
                  disabled={submitting || authLoading}
                  className="border-2 border-ink bg-emerald-300 px-4 py-2 text-xs font-black text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-200 disabled:opacity-50 flex items-center gap-2"
                >
                  {submitting && (
                    <div className="h-3 w-3 animate-spin rounded-full border-2 border-ink border-t-transparent" />
                  )}
                  {submitting ? "Placing at Day 1…" : "Start Learning from Day 1 →"}
                </button>
              </div>

              {/* Option 2: Experienced */}
              <div className="border-3 border-ink bg-surface p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all hover:translate-x-[1px] hover:translate-y-[1px]">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="border border-ink bg-cyan-200 px-2 py-0.5 text-xs font-mono font-bold text-ink">
                      OPTION 2
                    </span>
                    <h3 className="text-base font-black text-ink">Experienced SAP Practitioner</h3>
                  </div>
                  <span className="border border-ink bg-cyan-100 px-2 py-0.5 text-xs font-mono font-bold text-cyan-900">
                    10 TECHNICAL QUESTIONS (~8 MIN)
                  </span>
                </div>
                <p className="text-xs text-muted mb-4 leading-relaxed">
                  Familiar with classic ECC, ABAP, business processes, or modern S/4HANA. Take a 10-question technical diagnostic covering architecture, ACDOCA, MATDOC, CDS views, associations, Clean Core, and RAP. Fast-tracks you to Day 9, 23, 45, or 77 based on objective mastery.
                </p>
                <button
                  onClick={() => handleStartAssessment("experienced")}
                  disabled={loadingQuestions || submitting}
                  className="border-2 border-ink bg-cyan-300 px-4 py-2 text-xs font-black text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-cyan-200 disabled:opacity-50 flex items-center gap-2"
                >
                  {loadingQuestions && activeTrack === "experienced" && (
                    <div className="h-3 w-3 animate-spin rounded-full border-2 border-ink border-t-transparent" />
                  )}
                  Take Technical Assessment (10 Questions) →
                </button>
              </div>

              {/* Option 3: Not Sure */}
              <div className="border-3 border-ink bg-surface p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all hover:translate-x-[1px] hover:translate-y-[1px]">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="border border-ink bg-purple-200 px-2 py-0.5 text-xs font-mono font-bold text-ink">
                      OPTION 3
                    </span>
                    <h3 className="text-base font-black text-ink">Not Sure / Semi-Familiar</h3>
                  </div>
                  <span className="border border-ink bg-purple-100 px-2 py-0.5 text-xs font-mono font-bold text-purple-900">
                    6 FOUNDATIONAL QUESTIONS (~4 MIN)
                  </span>
                </div>
                <p className="text-xs text-muted mb-4 leading-relaxed">
                  General IT exposure, business analyst background, or exploring SAP. Take a quick 6-question check on ERP fundamentals, master data, procurement cycles, and HANA in-memory drivers to see if you can fast-track past Day 8.
                </p>
                <button
                  onClick={() => handleStartAssessment("not_sure")}
                  disabled={loadingQuestions || submitting}
                  className="border-2 border-ink bg-purple-300 px-4 py-2 text-xs font-black text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-purple-200 disabled:opacity-50 flex items-center gap-2"
                >
                  {loadingQuestions && activeTrack === "not_sure" && (
                    <div className="h-3 w-3 animate-spin rounded-full border-2 border-ink border-t-transparent" />
                  )}
                  Take Fundamentals Check (6 Questions) →
                </button>
              </div>
            </div>
            )}

            <div className="border-t-2 border-ink pt-4 flex items-center justify-between">
              <Link
                href="/sap/learning"
                className="text-xs font-bold text-muted hover:text-ink underline"
              >
                Skip diagnostic and browse full 100-day roadmap
              </Link>
            </div>
          </div>
        )}

        {/* ==================================================================== */}
        {/* STAGE 2: INTERACTIVE ASSESSMENT                                      */}
        {/* ==================================================================== */}
        {stage === "assessment" && currentQuestion && (
          <div className="border-4 border-ink bg-surface p-6 sm:p-8 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">
            {/* Header / Stepper Progress */}
            <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-ink pb-4 mb-6">
              <div>
                <span className="border border-ink bg-amber-200 px-2 py-0.5 text-[10px] font-mono font-bold uppercase text-ink">
                  {activeTrack === "experienced" ? "Experienced Technical Track" : "Fundamentals Track"}
                </span>
                <div className="text-sm font-mono font-bold text-ink mt-1">
                  Question {currentQuestionIndex + 1} of {questions.length}
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs font-mono font-bold text-muted">
                  {answeredCount} / {questions.length} Answered
                </span>
                <button
                  onClick={() => {
                    if (confirm("Are you sure you want to exit? Your answered questions will be saved if you re-enter.")) {
                      setStage("select_level");
                    }
                  }}
                  className="border border-ink bg-surface-raised px-2.5 py-1 text-xs font-bold text-muted hover:text-ink"
                >
                  Exit
                </button>
              </div>
            </div>

            {/* Topic Badge */}
            <div className="mb-3">
              <span className="border border-ink bg-cyan-100 px-2.5 py-1 text-xs font-mono font-bold uppercase text-cyan-950">
                {currentQuestion.topic_label || currentQuestion.topic}
              </span>
            </div>

            {/* Question Prompt */}
            <h2 className="text-base sm:text-lg font-black text-ink mb-6 leading-snug">
              {currentQuestion.question}
            </h2>

            {/* Options List */}
            <div className="space-y-3 mb-8">
              {currentQuestion.options.map((opt) => {
                const isSelected = answers[currentQuestion.id] === opt.id;
                return (
                  <button
                    key={opt.id}
                    type="button"
                    onClick={() => handleSelectOption(currentQuestion.id, opt.id)}
                    className={`w-full text-left border-2 border-ink p-4 transition-all flex items-start gap-3 ${
                      isSelected
                        ? "bg-amber-200 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] translate-x-[1px] translate-y-[1px]"
                        : "bg-surface hover:bg-surface-raised shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
                    }`}
                  >
                    <span
                      className={`inline-flex h-6 w-6 shrink-0 items-center justify-center border-2 border-ink text-xs font-mono font-black ${
                        isSelected ? "bg-ink text-surface" : "bg-surface text-ink"
                      }`}
                    >
                      {opt.id.toUpperCase()}
                    </span>
                    <span className="text-xs sm:text-sm font-medium text-ink leading-relaxed">
                      {opt.text}
                    </span>
                  </button>
                );
              })}
            </div>

            {/* Submission Error Banner with preserved answers */}
            {submitError && (
              <div className="mb-6 border-2 border-red-500 bg-red-100 p-4 text-xs font-bold text-red-900 shadow-[3px_3px_0px_0px_rgba(239,68,68,1)]">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <span>⚠ {submitError}</span>
                  <button
                    onClick={handleSubmitAssessment}
                    className="border border-red-900 bg-red-200 px-3 py-1 text-xs font-black uppercase hover:bg-red-300 shrink-0"
                  >
                    Retry Submission
                  </button>
                </div>
              </div>
            )}

            {/* Stepper Navigation & Jump Palette */}
            <div className="border-t-2 border-ink pt-6">
              {/* Question number dots palette */}
              <div className="flex flex-wrap gap-2 mb-6">
                {questions.map((q, idx) => {
                  const isCurrent = idx === currentQuestionIndex;
                  const isAnswered = Boolean(answers[q.id]);
                  return (
                    <button
                      key={q.id}
                      onClick={() => setCurrentQuestionIndex(idx)}
                      className={`h-8 w-8 text-xs font-mono font-black border-2 border-ink transition-all ${
                        isCurrent
                          ? "bg-cyan-300 ring-2 ring-ink ring-offset-1"
                          : isAnswered
                          ? "bg-emerald-200"
                          : "bg-surface text-muted hover:bg-surface-raised"
                      }`}
                      title={`Go to Question ${idx + 1}`}
                    >
                      {idx + 1}
                    </button>
                  );
                })}
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center justify-between gap-3">
                <button
                  type="button"
                  onClick={() => setCurrentQuestionIndex((prev) => Math.max(0, prev - 1))}
                  disabled={currentQuestionIndex === 0}
                  className="border-2 border-ink bg-surface px-4 py-2 text-xs font-bold text-ink hover:bg-surface-raised disabled:opacity-40"
                >
                  ← Previous
                </button>

                <div className="flex items-center gap-2">
                  {currentQuestionIndex < questions.length - 1 ? (
                    <button
                      type="button"
                      onClick={() =>
                        setCurrentQuestionIndex((prev) =>
                          Math.min(questions.length - 1, prev + 1)
                        )
                      }
                      className="border-2 border-ink bg-surface px-4 py-2 text-xs font-bold text-ink hover:bg-surface-raised"
                    >
                      Next →
                    </button>
                  ) : null}

                  <button
                    type="button"
                    onClick={handleSubmitAssessment}
                    disabled={submitting}
                    className="border-3 border-ink bg-emerald-300 px-5 py-2 text-xs font-black text-ink shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-200 disabled:opacity-50 flex items-center gap-2"
                  >
                    {submitting && (
                      <div className="h-3 w-3 animate-spin rounded-full border-2 border-ink border-t-transparent" />
                    )}
                    {submitting
                      ? "Evaluating Diagnostic…"
                      : `Submit Assessment (${answeredCount}/${questions.length})`}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ==================================================================== */}
        {/* STAGE 3: RESULTS & AUTHORITATIVE ROUTING                             */}
        {/* ==================================================================== */}
        {stage === "results" && placementResult && (
          <div className="border-4 border-ink bg-surface p-6 sm:p-8 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">
            <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
              <span className="border-2 border-ink bg-emerald-300 px-2.5 py-0.5 text-xs font-mono font-bold uppercase text-ink">
                ✓ Diagnostic Evaluated
              </span>
              {placementResult.diagnostic_score > 0 && (
                <span className="border-2 border-ink bg-amber-200 px-3 py-0.5 text-xs font-mono font-black text-ink">
                  Diagnostic Score: {Math.round(placementResult.diagnostic_score)}%
                </span>
              )}
            </div>

            <h1 className="text-2xl sm:text-3xl font-black text-ink mb-1">
              Your SAP S/4HANA Learning Pathway
            </h1>
            <div className="text-sm font-mono font-bold text-ink mb-6">
              Assigned Track: <span className="underline">{placementResult.persona.replace(/_/g, " ").toUpperCase()}</span>
            </div>

            {/* Recommended Start Box */}
            <div className="mb-6 border-3 border-ink bg-cyan-100 p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
              <div className="text-xs font-mono font-bold uppercase text-cyan-950 mb-1">
                Recommended Curriculum Starting Point
              </div>
              <div className="text-2xl font-black text-ink mb-2">
                DAY {placementResult.recommended_start_day}
              </div>
              <p className="text-xs sm:text-sm text-ink leading-relaxed">
                {placementResult.rationale}
              </p>
            </div>

            {/* Topic Breakdown */}
            {placementResult.topic_breakdown && placementResult.topic_breakdown.length > 0 && (
              <div className="mb-6 border-2 border-ink bg-surface p-4">
                <h3 className="text-xs font-mono font-bold uppercase text-muted mb-3">
                  Objective Topic Performance
                </h3>
                <div className="space-y-2.5">
                  {placementResult.topic_breakdown.map((t) => (
                    <div key={t.topic} className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-xs">
                      <span className="font-bold text-ink">{t.label || t.topic}</span>
                      <div className="flex items-center gap-3">
                        <div className="h-2.5 w-32 border border-ink bg-surface-raised overflow-hidden">
                          <div
                            className={`h-full ${
                              t.score >= 70 ? "bg-emerald-400" : t.score >= 40 ? "bg-amber-300" : "bg-red-400"
                            }`}
                            style={{ width: `${Math.min(100, Math.max(0, t.score))}%` }}
                          />
                        </div>
                        <span className="w-12 text-right font-mono font-bold text-ink">
                          {Math.round(t.score)}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Demonstrated Concepts Cloud */}
            {placementResult.demonstrated_concepts && placementResult.demonstrated_concepts.length > 0 && (
              <div className="mb-6">
                <h3 className="text-xs font-mono font-bold uppercase text-muted mb-2">
                  Demonstrated Concept Mastery ({placementResult.demonstrated_concepts.length})
                </h3>
                <div className="flex flex-wrap gap-1.5">
                  {placementResult.demonstrated_concepts.map((c) => (
                    <span
                      key={c}
                      className="border border-ink bg-emerald-100 px-2 py-0.5 text-[11px] font-mono font-bold text-emerald-950"
                    >
                      ✓ {c}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Identified Gaps */}
            {placementResult.gap_concepts && placementResult.gap_concepts.length > 0 && (
              <div className="mb-8">
                <h3 className="text-xs font-mono font-bold uppercase text-muted mb-2">
                  Targeted Learning Gaps
                </h3>
                <div className="flex flex-wrap gap-1.5">
                  {placementResult.gap_concepts.map((g) => (
                    <span
                      key={g}
                      className="border border-ink bg-surface-raised px-2 py-0.5 text-[11px] font-mono text-muted"
                    >
                      • {g}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Override error banner */}
            {changeStartError && (
              <div className="mb-6 border-2 border-red-500 bg-red-100 p-3 text-xs font-bold text-red-900">
                ⚠ {changeStartError}
              </div>
            )}

            {/* Primary Action Buttons */}
            <div className="border-t-2 border-ink pt-6 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
              <div className="flex flex-wrap items-center gap-3">
                {/* Main recommended day start button */}
                <Link
                  href={`/sap/learning/day/${placementResult.recommended_start_day}`}
                  className="border-3 border-ink bg-emerald-400 px-6 py-3 text-sm font-black text-ink shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px] hover:bg-emerald-300 transition-all text-center"
                >
                  {placementResult.recommended_start_day === 1
                    ? "START LEARNING (DAY 1) →"
                    : `START FROM DAY ${placementResult.recommended_start_day} →`}
                </Link>

                {/* Option to start from Day 1 if recommended Day > 1 (only before learning starts) */}
                {placementResult.recommended_start_day > 1 && !placementResult.placement_locked && (
                  <button
                    onClick={handleChooseStartDayOne}
                    disabled={changingStart}
                    className="border-2 border-ink bg-surface px-4 py-3 text-xs font-black text-ink shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:bg-surface-raised disabled:opacity-50 transition-all flex items-center gap-2 justify-center"
                  >
                    {changingStart && (
                      <div className="h-3 w-3 animate-spin rounded-full border-2 border-ink border-t-transparent" />
                    )}
                    {changingStart ? "Switching to Day 1…" : "Start from Day 1 Instead"}
                  </button>
                )}
              </div>

              <div className="flex items-center gap-4 justify-end">
                {!placementResult.placement_locked && (
                  <button
                    onClick={() => {
                      setStage("select_level");
                      setAnswers({});
                    }}
                    className="text-xs font-bold text-muted hover:text-ink underline"
                  >
                    Retake Diagnostic
                  </button>
                )}
                <Link
                  href="/sap/learning"
                  className="text-xs font-bold text-ink underline"
                >
                  View 100-Day Roadmap →
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
