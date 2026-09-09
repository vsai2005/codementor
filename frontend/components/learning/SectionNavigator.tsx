"use client";

import { CurriculumSection } from "@/lib/curriculum/types";

interface SectionNavigatorProps {
  sections: CurriculumSection[];
  activeSectionId?: string;
  completedDays: number[];
}

export function SectionNavigator({
  sections,
  activeSectionId,
  completedDays,
}: SectionNavigatorProps) {
  const scrollToSection = (sectionId: string) => {
    const el = document.getElementById(`section-${sectionId}`);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <nav
      aria-label="Sections navigation"
      className="sticky top-0 z-20 -mx-3 mb-6 border-y-2 border-ink bg-surface/95 px-3 py-2.5 backdrop-blur shadow-hard-sm sm:-mx-4 sm:px-4"
    >
      <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs no-scrollbar">
        <span className="font-mono text-[10px] font-bold uppercase tracking-wider text-muted shrink-0 pr-1">
          Jump to:
        </span>
        {sections.map((section) => {
          const isActive = section.id === activeSectionId;
          const sectionCompleted = section.days.every((d) =>
            completedDays.includes(d.day_number)
          );

          return (
            <button
              key={section.id}
              type="button"
              onClick={() => scrollToSection(section.id)}
              aria-label={`Jump to Section ${section.section_number}: ${section.title}`}
              className={`shrink-0 flex items-center gap-1.5 border-2 px-2.5 py-1.5 min-h-[32px] font-mono text-xs transition-all ${
                isActive
                  ? "border-accent bg-accent/10 text-accent font-bold shadow-hard-sm"
                  : sectionCompleted
                  ? "border-accent-2/60 bg-surface text-accent-2 font-medium"
                  : "border-ink/30 bg-surface text-ink/80 hover:border-ink hover:text-ink"
              }`}
            >
              <span>{String(section.section_number).padStart(2, "0")}.</span>
              <span className="truncate max-w-[140px] sm:max-w-none">{section.title}</span>
              {sectionCompleted && (
                <span className="text-[10px] text-accent-2 font-bold">✓</span>
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
