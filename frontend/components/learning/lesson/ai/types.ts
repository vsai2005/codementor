export type QuickActionType =
  | "explain_simply"
  | "give_example"
  | "explain_deeper"
  | "show_visually"
  | "connect_concept"
  | "teach_prerequisite"
  | "give_hint"
  | "find_mistake"
  | "quiz_me";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: Date;
  quickAction?: QuickActionType | string;
  relatedConcepts?: Array<{ day: number; title: string; section: string }> | string[];
  visual?: any;
  isFallback?: boolean;
}

export interface QuickActionItem {
  id: QuickActionType;
  label: string;
  icon: string;
  description: string;
}

export const QUICK_ACTIONS: QuickActionItem[] = [
  { id: "explain_simply", label: "Explain Simply", icon: "\ud83d\udca1", description: "Break down into simple intuition" },
  { id: "give_example", label: "Give Example", icon: "\ud83d\udccb", description: "Show a tiny, clear Python example" },
  { id: "explain_deeper", label: "Explain Deeper", icon: "\ud83d\udd2c", description: "Under the hood and complexity" },
  { id: "show_visually", label: "Show Visually", icon: "\ud83d\udcca", description: "ASCII diagram and mental model" },
  { id: "connect_concept", label: "Connect Concept", icon: "\ud83d\udd17", description: "How this connects to broader DSA" },
  { id: "teach_prerequisite", label: "Prerequisites", icon: "\ud83e\uddf1", description: "Foundations to know first" },
  { id: "give_hint", label: "Give Me a Hint", icon: "\ud83e\udded", description: "Get progressive guidance" },
  { id: "find_mistake", label: "Find My Mistake", icon: "\ud83d\udd0d", description: "Diagnose bug in your code" },
  { id: "quiz_me", label: "Quiz Me", icon: "\u2753", description: "Active recall check-in" },
];
