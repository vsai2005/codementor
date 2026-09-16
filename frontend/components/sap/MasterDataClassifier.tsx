"use client";

import React, { useState } from "react";

export interface DataItem {
  id?: string;
  item?: string;
  name?: string;
  category: string;
  views?: string;
  type?: "master" | "transactional";
}

interface MasterDataClassifierProps {
  items?: DataItem[];
  title?: string;
  instruction?: string;
}

export function MasterDataClassifier({
  items = [],
  title = "Enterprise Data Model Classifier",
  instruction = "Classify each operational record into Master Data vs. Transactional Data. Test your ability to distinguish durable enterprise entities from dynamic event records.",
}: MasterDataClassifierProps) {
  const [classifications, setClassifications] = useState<
    Record<number, "master" | "transactional">
  >({});
  const [selectedIdx, setSelectedIdx] = useState<number>(0);
  const [submitted, setSubmitted] = useState<boolean>(false);

  const getItemName = (item?: DataItem): string => {
    if (!item) return "Record";
    return item.item || item.name || "Enterprise Record";
  };

  const getCorrectType = (item?: DataItem): "master" | "transactional" => {
    if (!item) return "master";
    if (item.type) return item.type;
    return item.category.toLowerCase().includes("transactional") ? "transactional" : "master";
  };

  const handleClassify = (idx: number, type: "master" | "transactional") => {
    if (submitted) return; // Disallow mutation once submitted
    setClassifications((prev) => ({ ...prev, [idx]: type }));
    if (idx < items.length - 1) {
      setSelectedIdx(idx + 1);
    }
  };

  const allClassified = items.length > 0 && Object.keys(classifications).length === items.length;
  const correctCount = items.filter(
    (item, idx) => classifications[idx] === getCorrectType(item)
  ).length;

  const activeItem = items[selectedIdx] || items[0];

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      <div className="mb-4">
        <h3 className="text-base font-black text-ink">{title}</h3>
        <p className="text-xs text-muted mt-0.5">{instruction}</p>
      </div>

      {/* Progress & Stats Bar */}
      <div className="flex items-center justify-between border-b-2 border-ink pb-3 mb-4 text-xs font-mono">
        <div>
          Classified: <span className="font-bold">{Object.keys(classifications).length}</span> / {items.length}
        </div>
        {submitted && (
          <div className="font-bold">
            Score:{" "}
            <span
              className={
                correctCount === items.length
                  ? "text-emerald-800 bg-emerald-100 px-2 py-0.5 border-2 border-emerald-500 font-black"
                  : "text-amber-900 bg-amber-100 px-2 py-0.5 border-2 border-amber-500 font-black"
              }
            >
              {correctCount} / {items.length} Correct
            </span>
          </div>
        )}
      </div>

      {/* Item Selector Chips */}
      <div role="tablist" aria-label="Records to classify" className="flex flex-wrap gap-2 mb-4">
        {items.map((item, idx) => {
          const userChoice = classifications[idx];
          const isSelected = idx === selectedIdx;
          const isCorrect = submitted && userChoice === getCorrectType(item);
          const isWrong = submitted && userChoice && !isCorrect;

          let badgeColor = "bg-surface hover:bg-surface-raised text-ink border-ink";
          if (isSelected) {
            badgeColor = "bg-ink text-surface border-ink shadow-hard-sm";
          } else if (submitted) {
            badgeColor = isCorrect
              ? "bg-emerald-100 border-emerald-600 text-emerald-950 font-bold"
              : isWrong
              ? "bg-red-100 border-red-600 text-red-950 font-bold"
              : "bg-surface text-ink border-ink";
          } else if (userChoice) {
            badgeColor = "bg-blue-50 border-blue-500 text-blue-950 font-bold";
          }

          const chipLabel = getItemName(item).split(/[:\s]/)[0] || `#${idx + 1}`;

          return (
            <button
              key={idx}
              role="tab"
              aria-selected={isSelected}
              type="button"
              onClick={() => setSelectedIdx(idx)}
              className={`border-2 px-3 py-1.5 text-xs font-mono font-bold transition-all text-left focus-visible:ring-2 focus-visible:ring-ink focus-visible:outline-none ${badgeColor}`}
            >
              #{idx + 1} {chipLabel}
            </button>
          );
        })}
      </div>

      {/* Active Item Card & Interactive Classification */}
      {activeItem && (
        <div className="border-2 border-ink bg-surface-raised p-4 mb-4">
          <div className="text-[10px] font-mono font-bold uppercase text-muted mb-1">
            Active Enterprise Record #{selectedIdx + 1}
          </div>
          <div className="text-base font-black text-ink mb-2">
            {getItemName(activeItem)}
          </div>

          <div className="border border-ink/30 bg-surface p-3 mb-4 text-xs font-mono">
            <span className="text-muted font-bold">Category & Views: </span>
            <span className="text-ink font-semibold">
              {activeItem.category} {activeItem.views ? `• ${activeItem.views}` : ""}
            </span>
          </div>

          {/* Classification Action Buttons */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <button
              type="button"
              disabled={submitted}
              onClick={() => handleClassify(selectedIdx, "master")}
              className={`border-2 border-ink p-3 text-left transition-all focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:outline-none ${
                classifications[selectedIdx] === "master"
                  ? "bg-blue-600 text-white shadow-hard-sm font-bold"
                  : "bg-surface hover:bg-blue-50 text-ink"
              } ${submitted ? "cursor-not-allowed opacity-90" : ""}`}
            >
              <div className="text-xs font-black uppercase mb-0.5">
                🏛️ Master Data
              </div>
              <div className="text-[10px] opacity-85">
                Durable enterprise entity (Material, BP, GL, BOM) configured across org levels.
              </div>
            </button>

            <button
              type="button"
              disabled={submitted}
              onClick={() => handleClassify(selectedIdx, "transactional")}
              className={`border-2 border-ink p-3 text-left transition-all focus-visible:ring-2 focus-visible:ring-amber-600 focus-visible:outline-none ${
                classifications[selectedIdx] === "transactional"
                  ? "bg-amber-600 text-white shadow-hard-sm font-bold"
                  : "bg-surface hover:bg-amber-50 text-ink"
              } ${submitted ? "cursor-not-allowed opacity-90" : ""}`}
            >
              <div className="text-xs font-black uppercase mb-0.5">
                ⚡ Transactional Data
              </div>
              <div className="text-[10px] opacity-85">
                Short-lived business event record (PO, SO, Delivery, Material Document, Invoice).
              </div>
            </button>
          </div>

          {/* Submitted Feedback */}
          {submitted && (
            <div role="alert" className="mt-4 pt-3 border-t-2 border-ink text-xs">
              {classifications[selectedIdx] === getCorrectType(activeItem) ? (
                <div className="text-emerald-950 bg-emerald-50 border-2 border-emerald-500 p-3 font-medium">
                  <span className="font-bold">✓ Correct!</span> {getItemName(activeItem)} is classified as {getCorrectType(activeItem) === "master" ? "Master Data" : "Transactional Data"}.
                </div>
              ) : (
                <div className="text-red-950 bg-red-50 border-2 border-red-500 p-3 font-medium">
                  <span className="font-bold">✗ Incorrect:</span> {getItemName(activeItem)} is {getCorrectType(activeItem) === "master" ? "Master Data" : "Transactional Data"} ({activeItem.category}).
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Submit / Reset Evaluation Footer */}
      <div className="flex items-center justify-between pt-2">
        <button
          type="button"
          onClick={() => setSelectedIdx((prev) => Math.max(0, prev - 1))}
          disabled={selectedIdx === 0}
          className="border border-ink bg-surface px-3 py-1.5 text-xs font-bold disabled:opacity-40 focus-visible:ring-2 focus-visible:ring-ink"
        >
          ← Previous
        </button>

        {!submitted ? (
          <button
            type="button"
            onClick={() => setSubmitted(true)}
            disabled={!allClassified}
            className="border-2 border-ink bg-emerald-400 px-5 py-2 text-xs font-black uppercase text-ink shadow-hard-sm hover:bg-emerald-300 disabled:opacity-40 focus-visible:ring-2 focus-visible:ring-ink"
          >
            Check Classifications →
          </button>
        ) : (
          <button
            type="button"
            onClick={() => {
              setSubmitted(false);
              setClassifications({});
              setSelectedIdx(0);
            }}
            className="border-2 border-ink bg-surface px-4 py-1.5 text-xs font-bold text-ink hover:bg-surface-raised shadow-hard-sm focus-visible:ring-2 focus-visible:ring-ink"
          >
            Reset Practice ↻
          </button>
        )}

        <button
          type="button"
          onClick={() => setSelectedIdx((prev) => Math.min(items.length - 1, prev + 1))}
          disabled={selectedIdx === items.length - 1}
          className="border border-ink bg-surface px-3 py-1.5 text-xs font-bold disabled:opacity-40 focus-visible:ring-2 focus-visible:ring-ink"
        >
          Next →
        </button>
      </div>
    </div>
  );
}
