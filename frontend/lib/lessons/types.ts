export type LessonStepType =
  | "explanation"
  | "visualizer"
  | "checkpoint"
  | "practice"
  | "completion";

export interface BaseLessonStep {
  id: string;
  stepNumber: number; // 1-indexed (e.g. 1 to 9)
  title: string;
  shortLabel: string;
  type: LessonStepType;
  isGated: boolean;
}

export interface ExplanationCallout {
  type: "tip" | "warning" | "deep-dive";
  title: string;
  content: string;
}

export interface ExplanationSnippet {
  title?: string;
  code: string;
  language: string;
  caption?: string;
}

export interface ExplanationStep extends BaseLessonStep {
  type: "explanation";
  heading: string;
  subheading?: string;
  markdownContent: string[];
  snippets?: ExplanationSnippet[];
  callouts?: ExplanationCallout[];
  keyTakeaway?: string;
}

export interface VisualizerMemoryObject {
  id: string; // e.g., "0x10A4" or "addr_1"
  type: "int" | "str" | "float" | "list";
  value: string;
  isNew?: boolean;
  isMutated?: boolean;
}

export interface VisualizerVariable {
  name: string;
  targetObjectId: string;
  isNew?: boolean;
  isReassigned?: boolean;
}

export interface VisualizerFrame {
  stepNumber: number;
  codeLine: string;
  description: string;
  variables: VisualizerVariable[];
  objects: VisualizerMemoryObject[];
  note?: string;
}

export type VisualizerKind =
  | "memory"
  | "division-modulo"
  | "array-pointer"
  | "linked-list"
  | "tree"
  | "graph"
  | "dp-table"
  | "recursion";

export interface VisualizerStep extends BaseLessonStep {
  type: "visualizer";
  visualizerKind?: VisualizerKind;
  heading: string;
  subheading?: string;
  initialCode?: string;
  frames?: VisualizerFrame[];
  initialDividend?: number;
  initialDivisor?: number;
  keyTakeaway: string;
}

export interface CheckpointOption {
  id: string; // "A" | "B" | "C" | "D"
  label: string;
  subtext?: string;
}

export interface CheckpointItem {
  id: string;
  question: string;
  codeSnippet?: string;
  options: CheckpointOption[];
  correctOptionId: string;
  explanations: Record<string, string>; // Maps option id to specific explanation
}

export interface CheckpointStep extends BaseLessonStep {
  type: "checkpoint";
  heading: string;
  subheading?: string;
  checkpoints: CheckpointItem[];
  keyTakeaway?: string;
}

export interface PracticeTask {
  title: string;
  instructions: string[];
  starterCode: string;
  solutionCode?: string;
  expectedOutputPatterns: string[];
  hint: string;
}

export interface PracticeStep extends BaseLessonStep {
  type: "practice";
  heading: string;
  subheading?: string;
  task: PracticeTask;
  keyTakeaway?: string;
}

export interface MasteryRecapRow {
  concept: string;
  naiveIntuition: string;
  pythonReality: string;
}

export interface CompletionStep extends BaseLessonStep {
  type: "completion";
  dayNumber: number;
  heading: string;
  subheading: string;
  recapRows: MasteryRecapRow[];
  solidifiedConcepts: string[];
  nextDayPreview: {
    dayNumber: number;
    title: string;
    description: string;
  };
}

export type LessonStep =
  | ExplanationStep
  | VisualizerStep
  | CheckpointStep
  | PracticeStep
  | CompletionStep;

export interface LessonProgress {
  dayNumber: number;
  currentStepIndex: number; // 0-indexed into steps array
  maxUnlockedStepIndex: number; // 0-indexed
  checkpointAnswers: Record<string, { selectedOptionId: string; isCorrect: boolean }>;
  codeDraft: string;
  practiceCompleted: boolean;
  isCompleted: boolean;
  completedAt?: number;
}

export type LessonDifficulty =
  | "BEGINNER"
  | "FOUNDATIONAL"
  | "DEVELOPING"
  | "INTERMEDIATE"
  | "ADVANCED"
  | "EXPERT";
export type PracticeArchetype =
  | "guided"
  | "completion"
  | "debugging"
  | "tracing"
  | "algorithm"
  | "problem"
  | "milestone";

export type FlowTier = "tier1" | "tier2" | "tier3";

export interface DailyLessonPackage {
  dayNumber: number;
  title: string;
  topicName: string;
  sectionId: string;
  estimatedMinutes: number;
  difficulty?: LessonDifficulty;
  prerequisites?: number[];
  concepts?: string[];
  learningObjectives?: string[];
  practiceSkills?: string[];
  practiceArchetype?: PracticeArchetype;
  flowTier?: FlowTier;
  steps: LessonStep[];
}

