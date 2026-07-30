import type { ProblemDetail } from "@/lib/types";
import { TopicPill } from "./TopicPill";

/** Minimal markdown rendering: headings, lists, inline code, bold.
 *  Deliberately not a full markdown library — problem statements are authored
 *  by us in the seed script, so the input is trusted and narrow. Swap in
 *  react-markdown if statements ever become user-authored. */
function renderMarkdown(md: string): React.ReactNode[] {
  return md.split("\n").map((line, i) => {
    const key = `${i}-${line.slice(0, 12)}`;
    const inline = (text: string): React.ReactNode[] =>
      text.split(/(`[^`]+`|\*\*[^*]+\*\*)/g).map((part, j) => {
        if (part.startsWith("`") && part.endsWith("`") && part.length > 1) {
          return (
            <code key={j} className="border border-ink bg-bg px-1 font-mono text-[0.85em]">
              {part.slice(1, -1)}
            </code>
          );
        }
        if (part.startsWith("**") && part.endsWith("**") && part.length > 3) {
          return <strong key={j}>{part.slice(2, -2)}</strong>;
        }
        return <span key={j}>{part}</span>;
      });

    if (line.startsWith("- ")) {
      return (
        <li key={key} className="ml-4 list-disc font-body text-sm leading-relaxed">
          {inline(line.slice(2))}
        </li>
      );
    }
    if (line.trim() === "") return <div key={key} className="h-2" />;
    return (
      <p key={key} className="font-body text-sm leading-relaxed">
        {inline(line)}
      </p>
    );
  });
}

export function ProblemStatement({ problem }: { problem: ProblemDetail }) {
  return (
    <div className="space-y-4">
      <div>
        <h1 className="font-display text-2xl font-bold leading-tight">{problem.title}</h1>
        <div className="mt-2 flex flex-wrap gap-2">
          <TopicPill label={problem.topic.name} tier={problem.difficulty_tier} />
        </div>
      </div>

      <div className="space-y-1">{renderMarkdown(problem.statement_md)}</div>

      {problem.constraints_md.trim() !== "" && (
        <div>
          <h2 className="label mb-1">Constraints</h2>
          <ul className="space-y-1">{renderMarkdown(problem.constraints_md)}</ul>
        </div>
      )}

      <div className="card-flat p-3">
        <p className="label mb-1">Target complexity</p>
        <p className="font-mono text-sm">
          time {problem.optimal_time} · space {problem.optimal_space}
        </p>
      </div>
    </div>
  );
}
