"use client";

import { useState } from "react";
import Editor, { type OnMount } from "@monaco-editor/react";

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  language?: string;
  readOnly?: boolean;
  /** Block pasting into the editor (copy still works) so learners type it out. */
  blockPaste?: boolean;
}

export function CodeEditor({
  value,
  onChange,
  language = "python",
  readOnly = false,
  blockPaste = true,
}: CodeEditorProps) {
  const [pasteBlocked, setPasteBlocked] = useState(false);

  const handleMount: OnMount = (editor, monaco) => {
    if (!blockPaste) return;
    const dom = editor.getDomNode();
    // Copy/cut stay enabled — we only intercept paste so a full solution can't
    // be dropped in. Catch it at the DOM level (Ctrl/Cmd+V, middle-click, menu).
    dom?.addEventListener(
      "paste",
      (event: ClipboardEvent) => {
        event.preventDefault();
        event.stopPropagation();
        flashBlocked();
      },
      true,
    );
    // Also swallow the keybinding so Monaco's own paste command never fires.
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyV, flashBlocked);

    function flashBlocked() {
      setPasteBlocked(true);
      window.setTimeout(() => setPasteBlocked(false), 2200);
    }
  };

  return (
    <div className="relative h-full min-h-[280px] border-2 border-ink bg-surface">
      <Editor
        height="100%"
        defaultLanguage={language}
        language={language}
        value={value}
        onChange={(next) => onChange(next ?? "")}
        onMount={handleMount}
        loading={
          <div className="flex h-full items-center justify-center font-body text-sm text-muted">
            Loading editor…
          </div>
        }
        options={{
          readOnly,
          minimap: { enabled: false },
          fontSize: 14,
          fontFamily: "ui-monospace, Menlo, monospace",
          lineNumbers: "on",
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          renderLineHighlight: "none",
          padding: { top: 12, bottom: 12 },
        }}
      />
      {pasteBlocked && (
        <div
          role="status"
          className="pointer-events-none absolute bottom-3 right-3 border-2 border-ink bg-accent px-3 py-1.5 font-body text-xs font-semibold text-white shadow-hard"
        >
          Pasting is off here — type it out to learn it. ✍️
        </div>
      )}
    </div>
  );
}
