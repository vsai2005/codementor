"use client";

import React, { useState } from "react";
import { VisualizerStep } from "@/lib/lessons/types";

interface DivisionPreset {
  label: string;
  a: number;
  b: number;
  description: string;
}

const PRESETS: DivisionPreset[] = [
  { label: "14 // 4", a: 14, b: 4, description: "Standard positive division: 3 groups of 4 with 2 leftover." },
  { label: "17 // 5", a: 17, b: 5, description: "Quotient 3, remainder 2. Notice (3 * 5) + 2 == 17." },
  { label: "-7 // 3", a: -7, b: 3, description: "The Python Floor Trap: floors down to -3, leaving positive remainder +2!" },
  { label: "7 // -3", a: 7, b: -3, description: "Negative divisor: floors down to -3, remainder takes divisor's sign (-2)." },
  { label: "10 / 2", a: 10, b: 2, description: "True division always produces float 5.0." },
];

interface DivisionModuloVisualizerProps {
  step: VisualizerStep;
}

export function DivisionModuloVisualizer({ step }: DivisionModuloVisualizerProps) {
  const [a, setA] = useState<number>(step.initialDividend ?? 14);
  const [b, setB] = useState<number>(step.initialDivisor ?? 4);

  // Python arithmetic semantics:
  // Floor division rounds down toward negative infinity
  const isZeroDivisor = b === 0;
  const trueDiv = !isZeroDivisor ? (a / b).toFixed(3) : "ZeroDivisionError";
  const floorDiv = !isZeroDivisor ? Math.floor(a / b) : 0;
  // Modulo in Python: r = a - (floorDiv * b)
  const modulo = !isZeroDivisor ? a - floorDiv * b : 0;

  // For positive visual grouping:
  const numBuckets = !isZeroDivisor && floorDiv > 0 ? floorDiv : 0;
  const remainderCount = !isZeroDivisor && modulo > 0 ? modulo : 0;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="card p-6 bg-surface">
        <div className="flex items-center gap-2">
          <span className="label text-accent font-bold">Step {String(step.stepNumber).padStart(2, "0")}</span>
          <span className="text-muted text-xs">•</span>
          <span className="font-mono text-xs font-bold uppercase text-accent">
            Interactive Arithmetic Engine
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

      {/* Visualizer Master Card */}
      <div className="card overflow-hidden bg-surface border-2 border-ink shadow-hard">
        {/* Preset Toolbar */}
        <div className="border-b-2 border-ink bg-bg/60 p-4 space-y-3">
          <div className="flex items-center justify-between">
            <span className="font-mono text-xs font-bold uppercase text-ink">
              Preset Scenarios
            </span>
            <span className="font-mono text-[11px] text-muted">
              Choose a scenario or adjust steppers
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {PRESETS.map((preset) => {
              const isActive = a === preset.a && b === preset.b;
              return (
                <button
                  key={preset.label}
                  type="button"
                  onClick={() => {
                    setA(preset.a);
                    setB(preset.b);
                  }}
                  className={`min-h-[44px] px-3.5 py-2 font-mono text-xs font-bold border-2 transition-all ${
                    isActive
                      ? "border-accent bg-accent text-white dark:text-bg shadow-hard-accent"
                      : "border-ink bg-surface text-ink hover:bg-bg shadow-hard-sm"
                  }`}
                >
                  {preset.label}
                </button>
              );
            })}
          </div>

          {/* Steppers */}
          <div className="flex flex-wrap items-center gap-6 pt-3 border-t border-ink/15">
            {/* Dividend a */}
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-muted">Dividend (a):</span>
              <div className="flex items-center">
                <button
                  type="button"
                  aria-label="Decrease Dividend"
                  onClick={() => setA((prev) => prev - 1)}
                  className="w-11 h-11 border-2 border-ink bg-surface font-mono font-bold text-base hover:bg-bg active:bg-muted/20 flex items-center justify-center transition-colors"
                >
                  −
                </button>
                <div className="min-w-[52px] h-11 border-y-2 border-ink bg-surface font-mono text-sm font-bold flex items-center justify-center text-ink">
                  {a}
                </div>
                <button
                  type="button"
                  aria-label="Increase Dividend"
                  onClick={() => setA((prev) => prev + 1)}
                  className="w-11 h-11 border-2 border-ink bg-surface font-mono font-bold text-base hover:bg-bg active:bg-muted/20 flex items-center justify-center transition-colors"
                >
                  +
                </button>
              </div>
            </div>

            {/* Divisor b */}
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-muted">Divisor (b):</span>
              <div className="flex items-center">
                <button
                  type="button"
                  aria-label="Decrease Divisor"
                  onClick={() => setB((prev) => (prev - 1 === 0 ? prev - 2 : prev - 1))}
                  className="w-11 h-11 border-2 border-ink bg-surface font-mono font-bold text-base hover:bg-bg active:bg-muted/20 flex items-center justify-center transition-colors"
                >
                  −
                </button>
                <div className="min-w-[52px] h-11 border-y-2 border-ink bg-surface font-mono text-sm font-bold flex items-center justify-center text-ink">
                  {b}
                </div>
                <button
                  type="button"
                  aria-label="Increase Divisor"
                  onClick={() => setB((prev) => (prev + 1 === 0 ? prev + 2 : prev + 1))}
                  className="w-11 h-11 border-2 border-ink bg-surface font-mono font-bold text-base hover:bg-bg active:bg-muted/20 flex items-center justify-center transition-colors"
                >
                  +
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Live Invariant & Metrics Grid */}
        <div className="p-5 bg-surface space-y-6">
          {/* Formula Invariant */}
          <div className="p-3 sm:p-4 border-2 border-ink bg-bg/80 flex flex-wrap items-center justify-center gap-2 font-mono text-xs sm:text-sm font-bold shadow-hard-sm">
            <span className="text-ink">Dividend ({a})</span>
            <span className="text-muted">=</span>
            <span className="px-2 py-0.5 border border-accent-2 bg-accent-2/15 text-accent-2">
              Quotient ({floorDiv}) × Divisor ({b})
            </span>
            <span className="text-muted">+</span>
            <span className="px-2 py-0.5 border border-accent bg-accent/20 text-accent font-extrabold">
              Remainder ({modulo})
            </span>
            <span className="ml-2 font-mono text-[11px] px-2 py-0.5 border border-emerald-500 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300">
              ✓ Invariant Holds
            </span>
          </div>

          {/* 3-Column Operator Metric Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="border-2 border-ink bg-surface p-3.5 shadow-hard-sm space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-muted">True Division (/)</span>
                <span className="font-mono text-[10px] uppercase font-bold px-1.5 py-0.5 border border-ink bg-bg text-ink">
                  float
                </span>
              </div>
              <div className="font-mono text-xl font-bold text-ink">
                {a} / {b} = <span className="text-accent">{trueDiv}</span>
              </div>
              <p className="font-body text-xs text-ink/70">Always produces a float object</p>
            </div>

            <div className="border-2 border-accent-2 bg-accent-2/10 p-3.5 shadow-hard-sm space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-accent-2">Floor Division (//)</span>
                <span className="font-mono text-[10px] uppercase font-bold px-1.5 py-0.5 border border-accent-2 bg-accent-2 text-white dark:text-bg">
                  int
                </span>
              </div>
              <div className="font-mono text-xl font-bold text-accent-2">
                {a} // {b} = <span className="underline">{floorDiv}</span>
              </div>
              <p className="font-body text-xs text-ink/70">Floors down toward −∞</p>
            </div>

            <div className="border-2 border-accent bg-accent/10 p-3.5 shadow-hard-accent space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-accent">Modulo Remainder (%)</span>
                <span className="font-mono text-[10px] uppercase font-bold px-1.5 py-0.5 border border-accent bg-accent text-white dark:text-bg">
                  int
                </span>
              </div>
              <div className="font-mono text-xl font-bold text-accent">
                {a} % {b} = <span className="underline">{modulo}</span>
              </div>
              <p className="font-body text-xs text-ink/70">Sign matches divisor {b}</p>
            </div>
          </div>

          {/* Interactive Graphic Representation */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
            {/* Visual Buckets */}
            <div className="space-y-3">
              <div className="flex items-center justify-between border-b-2 border-ink/20 pb-1.5">
                <span className="font-mono text-xs font-bold uppercase text-ink">
                  Partition Buckets (Quotient: {numBuckets})
                </span>
                <span className="font-mono text-[11px] text-muted">
                  Holds {Math.abs(b)} items each
                </span>
              </div>

              {numBuckets > 0 ? (
                <div className="space-y-2.5 max-h-64 overflow-y-auto pr-1">
                  {Array.from({ length: Math.min(numBuckets, 6) }).map((_, bIdx) => (
                    <div key={bIdx} className="border-2 border-ink bg-surface p-3 shadow-hard-sm space-y-1.5">
                      <div className="flex items-center justify-between font-mono text-[11px] text-muted">
                        <span className="font-bold text-accent-2">Bucket #{bIdx + 1}</span>
                        <span>Filled ({Math.abs(b)} items)</span>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {Array.from({ length: Math.abs(b) }).map((_, i) => (
                          <span
                            key={i}
                            className="h-6 w-6 border border-ink bg-accent-2/25 text-accent-2 font-mono text-xs font-bold flex items-center justify-center"
                          >
                            •
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                  {numBuckets > 6 && (
                    <div className="font-mono text-xs text-muted text-center py-1">
                      + {numBuckets - 6} more full buckets...
                    </div>
                  )}
                </div>
              ) : (
                <div className="p-4 border-2 border-dashed border-ink/30 text-center font-mono text-xs text-muted">
                  {a < 0
                    ? "Negative numbers round down toward negative infinity; inspect number line below."
                    : "Quotient is 0 (a < b). Zero full buckets formed."}
                </div>
              )}

              {/* Remainder Tray */}
              <div className="border-2 border-dashed border-accent bg-accent/15 p-3.5 shadow-hard-sm space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-accent uppercase">
                    Remainder Tray (Leftovers)
                  </span>
                  <span className="font-mono text-xs font-bold px-2 py-0.5 bg-accent text-white dark:text-bg border border-ink">
                    r = {modulo}
                  </span>
                </div>
                {remainderCount > 0 ? (
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {Array.from({ length: Math.min(remainderCount, 20) }).map((_, i) => (
                      <span
                        key={i}
                        className="h-7 w-7 border-2 border-ink bg-amber-500 text-slate-950 font-mono text-xs font-bold flex items-center justify-center shadow-hard-sm"
                      >
                        {i + 1}
                      </span>
                    ))}
                    {remainderCount > 20 && (
                      <span className="font-mono text-xs text-muted self-center ml-2">
                        +{remainderCount - 20} more...
                      </span>
                    )}
                  </div>
                ) : (
                  <p className="font-mono text-xs text-muted italic">
                    Zero remainder. Dividend is cleanly divisible by {b}.
                  </p>
                )}
              </div>
            </div>

            {/* Real Number Line */}
            <div className="space-y-3">
              <div className="flex items-center justify-between border-b-2 border-ink/20 pb-1.5">
                <span className="font-mono text-xs font-bold uppercase text-ink">
                  Number Line Floor Vector (//)
                </span>
                <span className="font-mono text-[11px] text-muted">
                  Rounds leftward (towards −∞)
                </span>
              </div>

              <div className="border-2 border-ink bg-bg p-4 shadow-hard-sm space-y-4">
                <p className="font-body text-xs text-ink/90 leading-relaxed">
                  In Python, floor division <code className="font-mono text-accent font-bold">//</code> is defined as{" "}
                  <strong>$\lfloor a / b \rfloor$</strong>. It never truncates decimals toward zero; it always rounds to the nearest smaller integer.
                </p>

                {/* Number line schematic */}
                <div className="py-4 px-2 bg-surface border border-ink/30 space-y-3">
                  <div className="flex items-center justify-between font-mono text-xs font-bold text-muted border-b-2 border-ink pb-2">
                    <span>−4</span>
                    <span>−3</span>
                    <span>−2</span>
                    <span>−1</span>
                    <span>0</span>
                    <span>+1</span>
                    <span>+2</span>
                    <span>+3</span>
                    <span>+4</span>
                  </div>

                  <div className="space-y-1.5 font-mono text-xs">
                    <div className="flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full bg-accent" />
                      <span className="text-muted">Exact True Div ({a}/{b}):</span>
                      <strong className="text-accent">{trueDiv}</strong>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full bg-accent-2" />
                      <span className="text-muted">Floored Result ({a}//{b}):</span>
                      <strong className="text-accent-2">{floorDiv}</strong>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                      <span className="text-muted">Remainder ({a}%{b}):</span>
                      <strong className="text-ink">{modulo}</strong>
                    </div>
                  </div>
                </div>

                {/* Technical Interview Callout */}
                <div className="p-3 border-2 border-accent bg-accent/10 font-body text-xs text-ink space-y-1">
                  <span className="font-mono text-[10px] font-bold text-accent uppercase tracking-wider block">
                    ⚠️ CRUCIAL FOR TECHNICAL INTERVIEWS
                  </span>
                  <p>
                    Unlike C/Java (which truncate toward zero), Python guarantees that if <code className="font-mono">b &gt; 0</code>, then <code className="font-mono">a % b &gt;= 0</code> always!
                    Hence, <code className="font-mono font-bold">-7 % 3 == 2</code>, because <code className="font-mono">-7 = (-3 × 3) + 2</code>.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer Note */}
        <div className="border-t-2 border-ink bg-bg/50 p-4 font-mono text-xs text-muted flex items-center gap-2">
          <span>🔬</span>
          <span>
            Python integers never overflow; floats represent 64-bit IEEE-754 approximations.
          </span>
        </div>
      </div>

      {/* Key Takeaway Card */}
      <div className="card p-5 bg-accent/10 border-2 border-accent shadow-hard-accent">
        <span className="label text-accent font-bold uppercase tracking-wider">
          Key Mental Takeaway
        </span>
        <p className="mt-1 font-body text-base font-bold text-ink">
          {step.keyTakeaway}
        </p>
      </div>
    </div>
  );
}
