import { DailyLessonPackage } from "./types";

export async function getLessonPackage(dayNumber: number): Promise<DailyLessonPackage | null> {
  if (dayNumber < 1 || dayNumber > 160) return null;

  try {
    if (dayNumber >= 1 && dayNumber <= 20) {
      const mod = await import("./batches/batch1");
      return mod.BATCH_1_LESSONS[dayNumber] || null;
    }
    if (dayNumber >= 21 && dayNumber <= 40) {
      const mod = await import("./batches/batch2");
      return mod.BATCH_2_LESSONS[dayNumber] || null;
    }
    if (dayNumber >= 41 && dayNumber <= 60) {
      const mod = await import("./batches/batch3");
      return mod.BATCH_3_LESSONS[dayNumber] || null;
    }
    if (dayNumber >= 61 && dayNumber <= 80) {
      const mod = await import("./batches/batch4");
      return mod.BATCH_4_LESSONS[dayNumber] || null;
    }
    if (dayNumber >= 81 && dayNumber <= 100) {
      const mod = await import("./batches/batch5");
      return mod.BATCH_5_LESSONS[dayNumber] || null;
    }
    if (dayNumber >= 101 && dayNumber <= 120) {
      const mod = await import("./batches/batch6");
      return mod.BATCH_6_LESSONS[dayNumber] || null;
    }
    if (dayNumber >= 121 && dayNumber <= 140) {
      const mod = await import("./batches/batch7");
      return mod.BATCH_7_LESSONS[dayNumber] || null;
    }
    if (dayNumber >= 141 && dayNumber <= 160) {
      const mod = await import("./batches/batch8");
      return mod.BATCH_8_LESSONS[dayNumber] || null;
    }
    return null;
  } catch (error) {
    console.error(`[getLessonPackage] Failed to load batch for Day ${dayNumber}:`, error);
    return null;
  }
}
