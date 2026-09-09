"use client";

import { useState, useEffect } from "react";
import { CurriculumDay, CurriculumSection, DayStatus } from "@/lib/curriculum/types";
import { DayNode } from "./DayNode";

interface SectionCardProps {
  section: CurriculumSection;
  getDayStatus: (dayNumber: number) => DayStatus;
  isCurrentSection: boolean;
  onSelectDay: (day: CurriculumDay) => void;
  onToggleComplete: (dayNumber: number) => void;
}

export function SectionCard({
  section,
  getDayStatus,
  isCurrentSection,
  onSelectDay,
  onToggleComplete,
}: SectionCardProps) {
  const [isOpen, setIsOpen] = useState(isCurrentSection || section.section_number === 1);

  // Automatically open section if it becomes the current active section
  useEffect(() => {
    if (isCurrentSection) {
      setIsOpen(true);
    }
  }, [isCurrentSection]);

  // Calculate section statistics
  const totalDays = section.days.length;
  const completedDays = section.days.filter((d) => getDayStatus(d.day_number) === "completed").length;
  const progressPercent = Math.round((completedDays / totalDays) * 100);
  const hasCurrentDay = section.days.some((d) => getDayStatus(d.day_number) === "current");

  return (
    <section
      id={`section-${section.id}`}
      className={`card scroll-mt-20 transition-all duration-200 ${
        hasCurrentDay ? "border-ink shadow-hard" : "border-ink/80"
      }`}
      aria-labelledby={`section-title-${section.id}`}
    >
      {/* Section Header */}
      <div
        onClick={() => setIsOpen((prev) => !prev)}
        className="flex cursor-pointer flex-wrap items-center justify-between gap-3 border-b-2 border-ink/20 bg-surface/80 p-4 transition-colors hover:bg-surface sm:p-5"
        role="button"
        tabIndex={0}
        aria-expanded={isOpen}
        aria-controls={`section-days-${section.id}`}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            setIsOpen((prev) => !prev);
          }
        }}
      >
        <div className="flex items-start gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center border-2 border-ink bg-bg font-mono text-xs font-bold text-ink shadow-hard-sm">
            {String(section.section_number).padStart(2, "0")}
          </div>

          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="font-mono text-xs font-bold uppercase tracking-wider text-muted">
                Section {section.section_number} • Days {section.day_start}–{section.day_end}
              </span>
              {hasCurrentDay && (
                <span className="rounded border border-accent bg-accent/15 px-1.5 py-0.5 text-[10px] font-mono font-bold uppercase text-accent">
                  Current Section
                </span>
              )}
              {completedDays === totalDays && totalDays > 0 && (
                <span className="rounded border border-accent-2 bg-accent-2/15 px-1.5 py-0.5 text-[10px] font-mono font-bold uppercase text-accent-2">
                  Completed
                </span>
              )}
            </div>

            <h3
              id={`section-title-${section.id}`}
              className="font-display text-lg sm:text-xl font-bold text-ink"
            >
              {section.title}
            </h3>
            <p className="mt-0.5 font-body text-xs text-muted">
              {section.tagline}
            </p>
          </div>
        </div>

        {/* Section Right Stats & Collapse Indicator */}
        <div className="flex items-center gap-4 ml-auto sm:ml-0">
          <div className="text-right">
            <div className="font-mono text-xs font-bold text-ink">
              {completedDays}/{totalDays} Days
            </div>
            <div className="mt-1 h-1.5 w-24 sm:w-32 rounded-full border border-ink/20 bg-bg overflow-hidden">
              <div
                className="h-full bg-accent-2 transition-all duration-300"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>

          <div
            className="flex h-9 w-9 items-center justify-center border-2 border-ink bg-surface shadow-hard-sm transition-transform hover:-translate-y-0.5"
            aria-hidden="true"
          >
            <svg
              className={`h-4 w-4 transform transition-transform duration-200 ${
                isOpen ? "rotate-180" : ""
              }`}
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </div>

      {/* Section Day Nodes Grid */}
      {isOpen && (
        <div
          id={`section-days-${section.id}`}
          className="p-4 sm:p-5 bg-bg/30 border-t border-ink/10"
        >
          <div className="grid gap-3.5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {section.days.map((day) => (
              <DayNode
                key={day.day_number}
                day={day}
                status={getDayStatus(day.day_number)}
                onSelectDay={onSelectDay}
                onToggleComplete={onToggleComplete}
              />
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
