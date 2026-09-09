"use client";

import React, { useState } from "react";

// =========================================================================
// 1. INLINE FORMATTING RENDERER
// =========================================================================

/**
 * Safely renders inline markdown:
 * - Bold + Italic: ***text***
 * - Bold: **text**
 * - Italic: *text*
 * - Inline Code: `code` (guaranteed non-empty, NO orphan rectangular boxes)
 */
export function renderInlineText(text: string): React.ReactNode[] {
  if (!text) return [];

  // Match bold-italic (***...***), bold (**...**), inline code (`...`), or italic (*...*)
  // Note: we require at least 1 character inside delimiters to prevent empty boxes
  const tokens = text.split(/(\*\*\*[^*]+?\*\*\*|\*\*[^*]+?\*\*|`[^`\n]+?`|\*[^*]+?\*)/g);

  return tokens.map((token, index) => {
    if (!token) return null;

    if (token.startsWith("***") && token.endsWith("***") && token.length > 6) {
      return (
        <strong key={index} className="font-bold text-ink">
          <em className="italic">{renderInlineText(token.slice(3, -3))}</em>
        </strong>
      );
    }

    if (token.startsWith("**") && token.endsWith("**") && token.length > 4) {
      return (
        <strong key={index} className="font-bold text-ink">
          {renderInlineText(token.slice(2, -2))}
        </strong>
      );
    }

    if (token.startsWith("`") && token.endsWith("`") && token.length > 2) {
      const codeContent = token.slice(1, -1);
      if (!codeContent.trim()) return null;
      return (
        <code
          key={index}
          className="font-mono text-xs font-semibold px-1.5 py-0.5 rounded border border-ink/25 bg-bg/80 text-accent dark:text-accent-2"
        >
          {codeContent}
        </code>
      );
    }

    if (token.startsWith("*") && token.endsWith("*") && token.length > 2 && !token.startsWith("**")) {
      return (
        <em key={index} className="italic text-ink/95">
          {renderInlineText(token.slice(1, -1))}
        </em>
      );
    }

    return <span key={index}>{token}</span>;
  });
}

// =========================================================================
// 2. CODE BLOCK COMPONENT
// =========================================================================

export function CodeBlock({
  code,
  language = "python",
  title,
}: {
  code: string;
  language?: string;
  title?: string;
}) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const displayLang = language && language.trim() ? language.toLowerCase() : "python";

  return (
    <div className="card overflow-hidden my-3 border-2 border-ink bg-[#141d2b] dark:bg-[#121110] shadow-hard-sm">
      <div className="flex items-center justify-between border-b border-ink/30 bg-bg/20 px-3 py-1.5">
        <div className="flex items-center gap-2 font-mono text-[11px]">
          {title ? (
            <span className="font-bold text-[#f2ede3]">{title}</span>
          ) : (
            <span className="font-bold uppercase tracking-wider text-accent-2/90">
              {displayLang}
            </span>
          )}
        </div>
        <button
          type="button"
          onClick={handleCopy}
          className="font-mono text-[11px] text-white/70 hover:text-white px-2 py-0.5 rounded border border-white/20 hover:border-white/40 transition-colors focus-visible:ring-2 focus-visible:ring-accent"
          title="Copy code to clipboard"
        >
          {copied ? "✓ Copied" : "Copy"}
        </button>
      </div>
      <pre className="p-3.5 overflow-x-auto font-mono text-xs sm:text-sm text-[#f2ede3] leading-relaxed whitespace-pre">
        <code>{code}</code>
      </pre>
    </div>
  );
}

// =========================================================================
// 3. BLOCK PARSER & RENDERER
// =========================================================================

interface CodeBlockToken {
  type: "code";
  language: string;
  code: string;
}

interface HeadingBlockToken {
  type: "heading";
  level: number;
  text: string;
}

interface BlockquoteToken {
  type: "blockquote";
  text: string;
}

interface OrderedListToken {
  type: "ordered-list";
  items: Array<{ number: string; text: string }>;
}

interface UnorderedListToken {
  type: "unordered-list";
  items: string[];
}

interface ParagraphToken {
  type: "paragraph";
  text: string;
}

type BlockToken =
  | CodeBlockToken
  | HeadingBlockToken
  | BlockquoteToken
  | OrderedListToken
  | UnorderedListToken
  | ParagraphToken;

export function parseMarkdownBlocks(rawInput: string | string[]): BlockToken[] {
  let fullText = "";
  if (Array.isArray(rawInput)) {
    fullText = rawInput.join("\n\n");
  } else {
    fullText = String(rawInput || "");
  }

  const lines = fullText.split(/\r?\n/);
  const blocks: BlockToken[] = [];

  let inCodeFence = false;
  let fenceLang = "python";
  let fenceLines: string[] = [];

  let currentParaLines: string[] = [];
  let currentOrderedItems: Array<{ number: string; text: string }> = [];
  let currentUnorderedItems: string[] = [];

  const flushPara = () => {
    if (currentParaLines.length > 0) {
      const text = currentParaLines.join("\n").trim();
      if (text) {
        blocks.push({ type: "paragraph", text });
      }
      currentParaLines = [];
    }
  };

  const flushOrdered = () => {
    if (currentOrderedItems.length > 0) {
      blocks.push({ type: "ordered-list", items: [...currentOrderedItems] });
      currentOrderedItems = [];
    }
  };

  const flushUnordered = () => {
    if (currentUnorderedItems.length > 0) {
      blocks.push({ type: "unordered-list", items: [...currentUnorderedItems] });
      currentUnorderedItems = [];
    }
  };

  const flushAllLists = () => {
    flushOrdered();
    flushUnordered();
  };

  for (const line of lines) {
    const stripped = line.trim();

    // 1. Single-line code fence: ```python age = 20 ```
    const singleFence = stripped.match(/^```([a-zA-Z0-9_-]*)\s+(.+?)\s*```$/);
    if (singleFence && !inCodeFence) {
      flushPara();
      flushAllLists();
      blocks.push({
        type: "code",
        language: singleFence[1] || "python",
        code: singleFence[2] ?? "",
      });
      continue;
    }

    // 2. Code fence opening: ```python
    const fenceStart = stripped.match(/^```([a-zA-Z0-9_-]*)$/);
    if (fenceStart && !inCodeFence) {
      flushPara();
      flushAllLists();
      inCodeFence = true;
      fenceLang = fenceStart[1] || "python";
      fenceLines = [];
      continue;
    }

    // 3. Code fence closing: ```
    if (stripped.startsWith("```") && inCodeFence) {
      inCodeFence = false;
      blocks.push({
        type: "code",
        language: fenceLang,
        code: fenceLines.join("\n"),
      });
      fenceLines = [];
      continue;
    }

    // 4. Content inside code fence
    if (inCodeFence) {
      fenceLines.push(line);
      continue;
    }

    // 5. Blank line
    if (!stripped) {
      flushPara();
      continue;
    }

    // 6. Heading: #, ##, ###, ####
    const headingMatch = stripped.match(/^(#{1,4})\s+(.*)$/);
    if (headingMatch && headingMatch[1] && headingMatch[2] !== undefined) {
      flushPara();
      flushAllLists();
      blocks.push({
        type: "heading",
        level: headingMatch[1].length,
        text: headingMatch[2].trim(),
      });
      continue;
    }

    // 7. Blockquote: > ...
    const bqMatch = stripped.match(/^>\s*(.*)$/);
    if (bqMatch && bqMatch[1] !== undefined) {
      flushPara();
      flushAllLists();
      blocks.push({
        type: "blockquote",
        text: bqMatch[1].trim(),
      });
      continue;
    }

    // 8. Ordered list item: 1. ...
    const olMatch = stripped.match(/^(\d+)\.\s+(.*)$/);
    if (olMatch && olMatch[1] !== undefined && olMatch[2] !== undefined) {
      flushPara();
      flushUnordered();
      currentOrderedItems.push({
        number: olMatch[1],
        text: olMatch[2].trim(),
      });
      continue;
    }

    // 9. Unordered list item: - ..., * ..., • ...
    const ulMatch = stripped.match(/^[-*•]\s+(.*)$/);
    if (ulMatch && ulMatch[1] !== undefined) {
      flushPara();
      flushOrdered();
      currentUnorderedItems.push(ulMatch[1].trim());
      continue;
    }

    // 10. Regular paragraph text
    flushAllLists();
    currentParaLines.push(line);
  }

  // Handle any open fence or buffered items
  if (inCodeFence) {
    blocks.push({
      type: "code",
      language: fenceLang,
      code: fenceLines.join("\n"),
    });
  }
  flushPara();
  flushAllLists();

  return blocks;
}

export function LessonMarkdown({
  content,
  className = "space-y-4",
}: {
  content: string | string[];
  className?: string;
}) {
  const blocks = parseMarkdownBlocks(content);

  return (
    <div className={className}>
      {blocks.map((block, idx) => {
        if (block.type === "code") {
          return (
            <CodeBlock
              key={idx}
              code={block.code}
              language={block.language}
            />
          );
        }

        if (block.type === "heading") {
          if (block.level === 1) {
            return (
              <h1 key={idx} className="font-display text-2xl font-bold text-ink pt-3 pb-1">
                {renderInlineText(block.text)}
              </h1>
            );
          }
          if (block.level === 2) {
            return (
              <h2 key={idx} className="font-display text-xl font-bold text-ink pt-2.5 pb-1">
                {renderInlineText(block.text)}
              </h2>
            );
          }
          return (
            <h3 key={idx} className="font-display text-lg sm:text-xl font-bold text-ink pt-2 pb-0.5">
              {renderInlineText(block.text)}
            </h3>
          );
        }

        if (block.type === "blockquote") {
          return (
            <blockquote
              key={idx}
              className="border-l-4 border-accent pl-4 italic text-ink/90 bg-accent/5 py-2 my-2 rounded-r"
            >
              {renderInlineText(block.text)}
            </blockquote>
          );
        }

        if (block.type === "ordered-list") {
          return (
            <ol key={idx} className="space-y-2.5 my-3">
              {block.items.map((item, itemIdx) => (
                <li key={itemIdx} className="flex items-start gap-2.5 text-ink/90">
                  <span className="font-mono text-xs font-bold px-1.5 py-0.5 rounded border border-ink/20 bg-bg/80 text-accent dark:text-accent-2 shrink-0 mt-0.5">
                    {item.number}
                  </span>
                  <div className="flex-1 leading-relaxed">
                    {renderInlineText(item.text)}
                  </div>
                </li>
              ))}
            </ol>
          );
        }

        if (block.type === "unordered-list") {
          return (
            <ul key={idx} className="space-y-2 my-2.5">
              {block.items.map((item, itemIdx) => (
                <li key={itemIdx} className="flex items-start gap-2.5 text-ink/90">
                  <span className="font-mono text-xs font-bold text-accent shrink-0 mt-1">•</span>
                  <div className="flex-1 leading-relaxed">
                    {renderInlineText(item)}
                  </div>
                </li>
              ))}
            </ul>
          );
        }

        // Paragraph
        return (
          <p key={idx} className="text-ink/90 leading-relaxed">
            {renderInlineText(block.text)}
          </p>
        );
      })}
    </div>
  );
}
