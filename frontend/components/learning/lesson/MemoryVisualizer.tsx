"use client";

import React, { useState } from "react";
import { VisualizerStep, VisualizerFrame } from "@/lib/lessons/types";

interface MemoryVisualizerProps {
  step: VisualizerStep;
}

export function MemoryVisualizer({ step }: MemoryVisualizerProps) {
  const [currentFrameIndex, setCurrentFrameIndex] = useState(0);
  const [hoveredVar, setHoveredVar] = useState<string | null>(null);

  const frames = step.frames || [];
  const totalFrames = frames.length;
  const currentFrame: VisualizerFrame = (frames[currentFrameIndex] || frames[0]) || {
    stepNumber: 1,
    codeLine: "",
    description: "",
    variables: [],
    objects: [],
  };

  const handleNext = () => {
    setCurrentFrameIndex((prev) => Math.min(totalFrames - 1, prev + 1));
  };

  const handlePrev = () => {
    setCurrentFrameIndex((prev) => Math.max(0, prev - 1));
  };

  const handleReset = () => {
    setCurrentFrameIndex(0);
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="card p-6 bg-surface">
        <div className="flex items-center gap-2">
          <span className="label text-accent font-bold">Step {String(step.stepNumber).padStart(2, "0")}</span>
          <span className="text-muted text-xs">•</span>
          <span className="font-mono text-xs font-bold uppercase text-accent-2">
            Interactive Visualizer
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

      {/* Visualizer Interactive Stage */}
      <div className="card overflow-hidden bg-surface border-2 border-ink shadow-hard">
        {/* Stage Toolbar */}
        <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-ink bg-bg/60 p-4">
          <div className="flex items-center gap-3">
            <span className="font-mono text-xs font-bold uppercase text-ink px-2 py-0.5 border border-ink/30 bg-surface">
              Line {currentFrameIndex + 1} of {totalFrames}
            </span>
            <code className="font-mono text-xs sm:text-sm font-bold text-accent bg-accent/10 px-2.5 py-1 border border-accent/40 rounded">
              {currentFrame.codeLine}
            </code>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleReset}
              disabled={currentFrameIndex === 0}
              className="border border-ink/40 bg-surface min-h-[44px] px-3 py-2 font-mono text-xs font-semibold hover:border-ink focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              ↺ Reset
            </button>
            <button
              type="button"
              onClick={handlePrev}
              disabled={currentFrameIndex === 0}
              className="border-2 border-ink bg-surface min-h-[44px] px-3.5 py-2 font-mono text-xs font-bold hover:bg-bg focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              ◀ Prev Line
            </button>
            <button
              type="button"
              onClick={handleNext}
              disabled={currentFrameIndex >= totalFrames - 1}
              className="btn btn-primary min-h-[44px] px-4 text-xs font-bold disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Next Line ▶
            </button>
          </div>
        </div>

        {/* Dynamic Diagram Canvas */}
        <div className="p-4 sm:p-8 bg-surface">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start relative">
            {/* Column 1: Local Namespace (Name Tags) */}
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b-2 border-ink/20 pb-2">
                <span className="font-mono text-xs font-bold uppercase tracking-wider text-ink">
                  Local Namespace
                </span>
                <span className="font-mono text-[11px] text-muted">
                  (Variable Name Tags)
                </span>
              </div>

              <div className="space-y-4 pt-2">
                {currentFrame.variables.map((variable) => {
                  const isHovered = hoveredVar === variable.name;

                  return (
                    <div
                      key={variable.name}
                      tabIndex={0}
                      onClick={() => setHoveredVar(hoveredVar === variable.name ? null : variable.name)}
                      onFocus={() => setHoveredVar(variable.name)}
                      onBlur={() => setHoveredVar(null)}
                      onMouseEnter={() => setHoveredVar(variable.name)}
                      onMouseLeave={() => setHoveredVar(null)}
                      className={`relative flex items-center justify-between p-3.5 border-2 transition-all cursor-pointer select-none ${
                        variable.isNew
                          ? "border-accent bg-accent/15 shadow-hard-accent"
                          : variable.isReassigned
                          ? "border-amber-500 bg-amber-500/15 shadow-hard-sm"
                          : "border-ink bg-bg shadow-hard-sm"
                      } ${isHovered ? "ring-2 ring-accent" : ""}`}
                    >
                      <div className="flex items-center gap-2">
                        <span className="h-2 w-2 rounded-full border border-ink bg-surface" />
                        <span className="font-mono text-base font-bold text-ink">
                          {variable.name}
                        </span>
                        {variable.isNew && (
                          <span className="font-mono text-[10px] uppercase font-bold px-1.5 py-0.5 bg-accent text-white dark:text-bg border border-ink">
                            NEW
                          </span>
                        )}
                        {variable.isReassigned && (
                          <span className="font-mono text-[10px] uppercase font-bold px-1.5 py-0.5 bg-amber-500 text-slate-900 border border-ink">
                            REBOUND
                          </span>
                        )}
                      </div>

                      <div className="flex items-center gap-1.5 font-mono text-xs text-muted">
                        <span>points to</span>
                        <span className="font-bold text-ink px-1.5 py-0.5 border border-ink/20 bg-surface">
                          {variable.targetObjectId}
                        </span>
                        {/* Desktop arrow right towards heap column; Mobile arrow down towards stacked heap section */}
                        <span className="text-accent font-bold text-base hidden md:inline">→</span>
                        <span className="text-accent font-bold text-base md:hidden">↓</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Column 2: Heap Memory (Allocated Objects) */}
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b-2 border-ink/20 pb-2">
                <span className="font-mono text-xs font-bold uppercase tracking-wider text-ink">
                  Python Memory Space
                </span>
                <span className="font-mono text-[11px] text-muted">
                  (Values in Memory)
                </span>
              </div>

              <div className="space-y-4 pt-2">
                {currentFrame.objects.map((obj) => {
                  const isTargetOfHovered =
                    hoveredVar &&
                    currentFrame.variables.some(
                      (v) => v.name === hoveredVar && v.targetObjectId === obj.id
                    );

                  return (
                    <div
                      key={obj.id}
                      tabIndex={0}
                      className={`p-4 border-2 transition-all ${
                        obj.isNew
                          ? "border-accent-2 bg-accent-2/15 shadow-hard"
                          : "border-ink bg-surface shadow-hard-sm"
                      } ${isTargetOfHovered ? "ring-2 ring-accent scale-[1.02]" : ""}`}
                    >
                      <div className="flex items-center justify-between border-b border-ink/15 pb-2">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-accent px-1.5 py-0.5 border border-accent/30 bg-accent/10">
                            {obj.type}
                          </span>
                          <span className="font-mono text-xs text-muted">
                            ID: {obj.id}
                          </span>
                        </div>
                      </div>

                      <div className="mt-3 flex items-center justify-between">
                        <span className="font-body text-xs text-muted">Value:</span>
                        <span className="font-mono text-2xl font-bold text-ink">
                          {obj.value}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Interactive Trace Commentary */}
          <div className="mt-8 border-2 border-ink bg-bg p-4 sm:p-5 shadow-hard-sm">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold uppercase text-accent">
                Architectural Trace
              </span>
              <span className="text-muted text-xs">•</span>
              <span className="font-mono text-xs font-bold text-ink">
                Line {currentFrame.stepNumber}: {currentFrame.codeLine}
              </span>
            </div>
            <p className="mt-2 font-body text-sm text-ink leading-relaxed">
              {currentFrame.description}
            </p>
            {currentFrame.note && (
              <p className="mt-2 font-mono text-xs text-muted border-t border-ink/10 pt-2">
                💡 {currentFrame.note}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Key Takeaway */}
      {step.keyTakeaway && (
        <div className="card border-2 border-accent bg-accent/10 p-4 sm:p-5 shadow-hard-accent">
          <span className="label text-accent font-bold uppercase tracking-wider">
            Crucial Takeaway
          </span>
          <p className="mt-1 font-body text-sm sm:text-base font-semibold text-ink leading-relaxed">
            {step.keyTakeaway}
          </p>
        </div>
      )}
    </div>
  );
}
