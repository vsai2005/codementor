import React from "react";
import { LessonLoader } from "./LessonLoader";

interface PageProps {
  params: Promise<{
    dayNumber: string;
  }>;
}

export default async function DailyLessonPage({ params }: PageProps) {
  const resolvedParams = await params;
  const dayNumber = parseInt(resolvedParams.dayNumber, 10) || 1;

  return <LessonLoader dayNumber={dayNumber} />;
}
