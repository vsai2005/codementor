// Run with: npm run test:unit   (node --test, no extra dependencies; Node >= 22.18 or 24)
import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { percentComplete, pythonCourseCard, sapCourseCard } from "./hub.ts";

const sapProgress = (over = {}) => ({
  course_slug: "sap-s4hana",
  current_day: 1,
  completed_days: [],
  waived_days: [],
  total_days: 100,
  day_states: {},
  ...over,
});

const dayState = (over = {}) => ({
  day_number: 1,
  lesson_completed: false,
  practice_completed: false,
  assessment_passed: false,
  completed: false,
  unlocked: true,
  status: "in_progress",
  ...over,
});

describe("percentComplete", () => {
  it("rounds and clamps", () => {
    assert.equal(percentComplete(0, 160), 0);
    assert.equal(percentComplete(80, 160), 50);
    assert.equal(percentComplete(1, 160), 1);
    assert.equal(percentComplete(500, 160), 100);
    assert.equal(percentComplete(5, 0), 0);
  });
});

describe("pythonCourseCard", () => {
  it("offers Start for a brand-new learner and points at day 1", () => {
    const card = pythonCourseCard({ currentDay: 1, completedDays: [], dayRecords: {} });
    assert.equal(card.status, "not_started");
    assert.equal(card.primaryLabel, "Start course");
    assert.equal(card.primaryHref, "/learning/day/1");
    assert.equal(card.totalDays, 160);
    assert.equal(card.percent, 0);
  });

  it("offers Continue with the current day once days are completed", () => {
    const card = pythonCourseCard({ currentDay: 13, completedDays: Array.from({ length: 12 }, (_, i) => i + 1) });
    assert.equal(card.status, "in_progress");
    assert.equal(card.primaryLabel, "Continue — Day 13");
    assert.equal(card.primaryHref, "/learning/day/13");
    assert.equal(card.completedDays, 12);
    assert.equal(card.percent, 8);
  });

  it("treats a half-finished day (lesson done, practice pending) as started", () => {
    const card = pythonCourseCard({
      currentDay: 1,
      completedDays: [],
      dayRecords: { 1: { lesson_completed: true, practice_passed: false } },
    });
    assert.equal(card.status, "in_progress");
    assert.equal(card.primaryHref, "/learning/day/1");
  });

  it("does not let duplicate or out-of-range days inflate progress", () => {
    const card = pythonCourseCard({ currentDay: 2, completedDays: [1, 1, 1, 0, -4, 999, 2.5] });
    assert.equal(card.completedDays, 1);
  });

  it("clamps an invalid current day", () => {
    assert.equal(pythonCourseCard({ currentDay: 0, completedDays: [1] }).currentDay, 1);
    assert.equal(pythonCourseCard({ currentDay: 900, completedDays: [1] }).currentDay, 160);
    assert.equal(pythonCourseCard({ currentDay: Number.NaN, completedDays: [1] }).currentDay, 1);
  });

  it("offers Review once all 160 days are done", () => {
    const card = pythonCourseCard({ currentDay: 160, completedDays: Array.from({ length: 160 }, (_, i) => i + 1) });
    assert.equal(card.status, "completed");
    assert.equal(card.percent, 100);
    assert.equal(card.primaryLabel, "Review course");
    assert.equal(card.primaryHref, "/learning/python");
  });

  it("always exposes the roadmap as the secondary action", () => {
    const card = pythonCourseCard({ currentDay: 1, completedDays: [] });
    assert.equal(card.secondaryHref, "/learning/python");
  });
});

describe("sapCourseCard", () => {
  it("offers Start (via placement) for a new or signed-out learner", () => {
    for (const card of [sapCourseCard(null, null), sapCourseCard(sapProgress(), null)]) {
      assert.equal(card.status, "not_started");
      assert.equal(card.primaryLabel, "Start course");
      assert.equal(card.primaryHref, "/sap/placement");
      assert.equal(card.totalDays, 100);
      assert.equal(card.completedDays, 0);
    }
  });

  it("offers Continue at the current day once progress exists", () => {
    const card = sapCourseCard(
      sapProgress({ current_day: 7, completed_days: [1, 2, 3, 4, 5, 6] }),
      null
    );
    assert.equal(card.status, "in_progress");
    assert.equal(card.primaryLabel, "Continue — Day 7");
    assert.equal(card.primaryHref, "/sap/learning/day/7");
    assert.equal(card.percent, 6);
  });

  it("falls back to the placement start day when progress is unavailable", () => {
    const card = sapCourseCard(null, { recommended_start_day: 12 });
    assert.equal(card.status, "in_progress");
    assert.equal(card.currentDay, 12);
    assert.equal(card.primaryHref, "/sap/learning/day/12");
  });

  it("never counts waived days as completed", () => {
    const card = sapCourseCard(
      sapProgress({ current_day: 9, completed_days: [1, 2, 3, 4], waived_days: [3, 4] }),
      null
    );
    assert.equal(card.completedDays, 2);
    assert.equal(card.percent, 2);
  });

  it("prefers the server's current day over the placement day, as the SAP page does", () => {
    const card = sapCourseCard(sapProgress({ current_day: 5, completed_days: [1] }), { recommended_start_day: 12 });
    assert.equal(card.currentDay, 5);
  });

  it("uses server waivers over the placement fallback when progress is available", () => {
    const card = sapCourseCard(
      sapProgress({ current_day: 3, completed_days: [1, 2], waived_days: [] }),
      { recommended_start_day: 3, waived_days: [1, 2] }
    );
    assert.equal(card.completedDays, 2);
  });

  it("detects a started learner from day states even with no completed days", () => {
    const card = sapCourseCard(
      sapProgress({ day_states: { 1: dayState({ lesson_completed: true }) } }),
      null
    );
    assert.equal(card.status, "in_progress");
    assert.equal(card.primaryHref, "/sap/learning/day/1");
  });

  it("honours the server-reported course length", () => {
    const card = sapCourseCard(sapProgress({ total_days: 50, completed_days: [1, 2, 3, 4, 5], current_day: 6 }), null);
    assert.equal(card.totalDays, 50);
    assert.equal(card.percent, 10);
  });

  it("offers Review once every day is completed", () => {
    const all = Array.from({ length: 100 }, (_, i) => i + 1);
    const card = sapCourseCard(sapProgress({ current_day: 100, completed_days: all }), null);
    assert.equal(card.status, "completed");
    assert.equal(card.percent, 100);
    assert.equal(card.primaryLabel, "Review course");
    assert.equal(card.primaryHref, "/sap");
  });

  it("keeps the course overview as the secondary action", () => {
    assert.equal(sapCourseCard(null, null).secondaryHref, "/sap");
  });
});
