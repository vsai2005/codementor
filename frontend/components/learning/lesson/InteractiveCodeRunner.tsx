"use client";

import React, { useState, useEffect, useRef } from "react";
import { PracticeStep } from "@/lib/lessons/types";
import { api } from "@/lib/api";
import { renderInlineText } from "./LessonMarkdown";

interface InteractiveCodeRunnerProps {
  step: PracticeStep;
  dayNumber?: number;
  savedCode: string;
  isCompleted: boolean;
  onCodeChange: (code: string) => void;
  onCompletePractice: () => void;
}

export function InteractiveCodeRunner({
  step,
  dayNumber = 1,
  savedCode,
  isCompleted,
  onCodeChange,
  onCompletePractice,
}: InteractiveCodeRunnerProps) {
  const task = step.task;
  const [code, setCode] = useState<string>(savedCode || task.starterCode);
  const [isRunning, setIsRunning] = useState(false);
  const [output, setOutput] = useState<{
    stdout: string;
    stderr: string;
    status: string;
    runtime_ms: number;
  } | null>(null);
  const [showHint, setShowHint] = useState(false);
  const inFlight = useRef(false);

  useEffect(() => {
    if (savedCode) {
      setCode(savedCode);
    }
  }, [savedCode]);

  const handleCodeChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const val = e.target.value;
    setCode(val);
    onCodeChange(val);
  };

  const handleReset = () => {
    if (window.confirm("Reset code back to original starter template?")) {
      setCode(task.starterCode);
      onCodeChange(task.starterCode);
      setOutput(null);
    }
  };

  const handleRun = async () => {
    if (inFlight.current || isRunning) return;
    inFlight.current = true;
    setIsRunning(true);
    try {
      const res = await api.runLessonSnippet({
        code,
        day_number: dayNumber,
      });

      setOutput(res);

      // Verify output against expected patterns
      const stdout = res.stdout || "";
      const allPassed =
        res.status === "ok" &&
        task.expectedOutputPatterns.every((pattern) => stdout.includes(pattern));

      if (allPassed) {
        onCompletePractice();
      }
    } catch (err: any) {
      setOutput({
        stdout: "",
        stderr: err?.message || "Failed to communicate with execution sandbox.",
        status: "error",
        runtime_ms: 0,
      });
    } finally {
      setIsRunning(false);
      inFlight.current = false;
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      handleRun();
      return;
    }

    if (e.key === "Tab") {
      e.preventDefault();
      const textarea = e.currentTarget;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newCode = code.substring(0, start) + "    " + code.substring(end);
      setCode(newCode);
      onCodeChange(newCode);
      requestAnimationFrame(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 4;
      });
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="card p-6 bg-surface">
        <div className="flex items-center gap-2">
          <span className="label text-accent font-bold">Step {String(step.stepNumber).padStart(2, "0")}</span>
          <span className="text-muted text-xs">•</span>
          <span className="font-mono text-xs font-bold uppercase text-accent">
            Guided Practice & Execution
          </span>
        </div>
        <h2 className="mt-1.5 font-display text-2xl sm:text-3xl font-bold text-ink leading-tight">
          {step.heading}
        </h2>
        {step.subheading && (
          <p className="mt-2 font-body text-sm sm:text-base text-ink/80 leading-relaxed">
            {step.subheading}
          </p>
        )}
      </div>

      {/* Task Instructions */}
      <div className="card p-6 bg-surface space-y-4">
        <div className="flex items-center justify-between border-b-2 border-ink/10 pb-3">
          <h3 className="font-display text-lg font-bold text-ink">
            {task.title}
          </h3>
          <button
            type="button"
            onClick={() => setShowHint(!showHint)}
            className="font-mono text-xs text-accent hover:underline font-semibold"
          >
            {showHint ? "Hide Hint" : "Need a Hint?"}
          </button>
        </div>

        <div className="space-y-2 font-body text-sm text-ink leading-relaxed">
          {task.instructions.map((inst, i) => (
            <div key={i} className="flex items-start gap-2">
              <span className="font-mono text-xs font-bold text-accent shrink-0 mt-0.5">•</span>
              <div className="flex-1">{renderInlineText(inst)}</div>
            </div>
          ))}
        </div>

        {showHint && (
          <div className="border-2 border-dashed border-accent/40 bg-accent/10 p-4 font-body text-xs sm:text-sm text-ink leading-relaxed">
            💡 <strong>Hint:</strong> {renderInlineText(task.hint)}
          </div>
        )}
      </div>

      {/* Code Editor & Execution Panel */}
      <div className="card overflow-hidden bg-surface border-2 border-ink shadow-hard">
        {/* Editor Toolbar */}
        <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-ink bg-bg/60 px-4 py-2.5">
          <div className="flex items-center gap-2 font-mono text-xs">
            <span className="font-bold text-ink">main.py</span>
            <span className="text-muted">•</span>
            <span className="text-muted text-[11px]">Python 3.12 Sandbox</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleReset}
              disabled={isRunning}
              className="border border-ink/40 bg-surface min-h-[44px] px-3 py-2 font-mono text-xs font-semibold hover:border-ink focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-40 transition-colors"
            >
              ↺ Reset Template
            </button>
            <button
              type="button"
              onClick={handleRun}
              disabled={isRunning}
              className="btn btn-primary min-h-[44px] px-4 text-xs font-bold flex items-center gap-2 focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-50"
            >
              {isRunning ? (
                <span>Executing…</span>
              ) : (
                <>
                  <span>▶ Run Code</span>
                  <span className="font-mono text-[10px] opacity-75 hidden sm:inline">(Ctrl+Enter)</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Code Input */}
        <div className="p-0">
          <textarea
            value={code}
            onChange={handleCodeChange}
            onKeyDown={handleKeyDown}
            rows={16}
            spellCheck={false}
            className="w-full p-4 font-mono text-xs sm:text-sm bg-[#141d2b] dark:bg-[#121110] text-[#f2ede3] focus:outline-none focus:ring-2 focus:ring-accent focus:ring-inset resize-y leading-relaxed"
            placeholder="Write your Python code here..."
          />
        </div>

        {/* Terminal Output Drawer with aria-live */}
        <div
          role="region"
          aria-label="Terminal Output"
          aria-live="polite"
          className="border-t-2 border-ink bg-[#121110] text-[#f2ede3] p-4 font-mono text-xs sm:text-sm space-y-3"
        >
          <div className="flex items-center justify-between border-b border-ink/40 pb-2 text-[11px] text-muted">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-accent-2" />
              <span className="uppercase font-bold tracking-wider">Terminal Output (stdout)</span>
            </div>
            {output && (
              <div className="flex items-center gap-3">
                <span>Runtime: {output.runtime_ms}ms</span>
                <span
                  className={`px-1.5 py-0.5 border font-bold uppercase ${
                    output.status === "ok" ? "bg-accent-2/20 text-accent-2 border-accent-2/40" : "bg-accent/20 text-accent border-accent/40"
                  }`}
                >
                  {output.status}
                </span>
              </div>
            )}
          </div>

          {output ? (
            <div className="space-y-2">
              {output.stdout && (
                <pre className="whitespace-pre-wrap leading-relaxed text-[#f2ede3]">
                  {output.stdout}
                </pre>
              )}
              {output.stderr && (
                <pre className="whitespace-pre-wrap leading-relaxed text-accent bg-accent/10 p-2.5 border border-accent/30">
                  {output.stderr}
                </pre>
              )}
            </div>
          ) : (
            <div className="text-muted/60 italic py-2">
              Click &quot;▶ Run Code&quot; or press Ctrl+Enter to execute your script in the Python sandbox.
            </div>
          )}

          {/* Practice Verification Banner */}
          {isCompleted && (
            <div role="status" aria-live="polite" className="mt-4 border-2 border-accent-2 bg-accent-2/20 p-4 text-[#f2ede3] font-body animate-in fade-in duration-200">
              <div className="flex items-center gap-2">
                <span className="bg-accent-2 text-white dark:text-bg font-mono text-xs font-bold uppercase px-2 py-0.5 border border-ink">
                  ✓ VERIFIED
                </span>
                <span className="font-display font-bold text-sm sm:text-base text-white">
                  Practice Objective Accomplished!
                </span>
              </div>
              <p className="mt-1.5 text-xs sm:text-sm text-[#f2ede3]/90 leading-relaxed font-body">
                Your script printed the telemetry badge and confirmed that rebinding <code>daily_coding_hours</code> allocated a new object address in memory (<code>id != new_id</code>). Next Step unlocked!
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
