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
  { id: "explain_simply", label: "Explain Simply", icon: "💡", description: "Break down into simple intuition" },
  { id: "give_example", label: "Give Example", icon: "📋", description: "Show a tiny, clear Python example" },
  { id: "explain_deeper", label: "Explain Deeper", icon: "🔬", description: "Under the hood and complexity" },
  { id: "show_visually", label: "Show Visually", icon: "📊", description: "ASCII diagram and mental model" },
  { id: "connect_concept", label: "Connect Concept", icon: "🔗", description: "How this connects to broader DSA" },
  { id: "teach_prerequisite", label: "Prerequisites", icon: "🧱", description: "Foundations to know first" },
  { id: "give_hint", label: "Give Me a Hint", icon: "🧭", description: "Get progressive guidance" },
  { id: "find_mistake", label: "Find My Mistake", icon: "🔍", description: "Diagnose bug in your code" },
  { id: "quiz_me", label: "Quiz Me", icon: "❓", description: "Active recall check-in" },
];
