"use client";

import { useState, useCallback } from "react";
import { AppShell } from "@/components/AppShell";
import {
  JourneyHero,
  SectionNavigator,
  SectionCard,
  DayDetailModal,
} from "@/components/learning";
import { CURRICULUM_SECTIONS } from "@/lib/curriculum/curriculumData";
import { useJourney } from "@/lib/curriculum/useJourney";
import { CurriculumDay } from "@/lib/curriculum/types";

export default function LearningDashboardPage() {
  const {
    currentDay,
    completedDays,
    isLoaded,
    getDayStatus,
    toggleDayComplete,
    resetProgress,
    currentDayData,
    currentSection,
  } = useJourney();

  const [selectedDay, setSelectedDay] = useState<CurriculumDay | null>(null);

  const handleToggleComplete = useCallback(
    (dayNumber: number) => {
      toggleDayComplete(dayNumber);
    },
    [toggleDayComplete]
  );

  const handleContinue = useCallback(() => {
    if (currentDayData) {
      setSelectedDay(currentDayData);
    }
    setTimeout(() => {
      const el = document.getElementById(`day-${currentDay}`);
      if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }, 50);
  }, [currentDay, currentDayData]);

  const handleCloseModal = useCallback(() => {
    setSelectedDay(null);
  }, []);

  if (!isLoaded) {
    return (
      <AppShell>
        <div className="mx-auto max-w-[1400px] px-3 py-12 sm:px-4 text-center">
          <p className="font-body text-sm text-muted">Loading curriculum roadmap…</p>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="mx-auto max-w-[1400px] space-y-6 px-3 py-6 sm:px-4">
        {/* Top Hero Banner */}
        <JourneyHero
          currentDay={currentDay}
          completedDays={completedDays}
          currentDayData={currentDayData}
          currentSection={currentSection}
          onContinue={handleContinue}
          onReset={resetProgress}
        />

        {/* Section Jump Bar */}
        <SectionNavigator
          sections={CURRICULUM_SECTIONS}
          activeSectionId={currentSection?.id}
          completedDays={completedDays}
        />

        {/* 14 Sections Stack */}
        <div className="space-y-6">
          {CURRICULUM_SECTIONS.map((section) => (
            <SectionCard
              key={section.id}
              section={section}
              getDayStatus={getDayStatus}
              isCurrentSection={currentSection?.id === section.id}
              onSelectDay={setSelectedDay}
              onToggleComplete={handleToggleComplete}
            />
          ))}
        </div>

        {/* Day Detail & Inspection Modal */}
        {selectedDay && (
          <DayDetailModal
            day={selectedDay}
            status={getDayStatus(selectedDay.day_number)}
            onClose={handleCloseModal}
            onToggleComplete={handleToggleComplete}
          />
        )}
      </div>
    </AppShell>
  );
}
