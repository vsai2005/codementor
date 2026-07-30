import type { MemoryNote } from "@/lib/types";

/** PRD 3.3: retrieved notes are shown to the user, labelled as recalled
 *  memory. Making the RAG visible is the demo value. */
export function MemoryNoteCard({ note }: { note: MemoryNote }) {
  return (
    <div className="card-flat p-3">
      <p className="label mb-1">Based on your past attempts</p>
      <p className="font-body text-sm">{note.content}</p>
      <p className="mt-1 font-mono text-xs text-muted">
        similarity {note.similarity.toFixed(2)}
      </p>
    </div>
  );
}
