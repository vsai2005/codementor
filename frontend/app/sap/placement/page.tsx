"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { sapApi } from "@/lib/sap/api";
import type { SapPlacementProfile } from "@/lib/sap/types";

const PERSONAS = [
  {
    id: "fresher",
    title: "1. Fresher / ERP Newcomer",
    startingDay: 1,
    description: "New to enterprise computing. Starts from Day 1 with maximum scaffolding across ERP architecture and navigation.",
  },
  {
    id: "beginner",
    title: "2. Beginner / CS Graduate",
    startingDay: 9,
    description: "Familiar with programming or fundamental IT. Skips general ERP basics and begins directly at S/4HANA in-memory architecture.",
  },
  {
    id: "functional_user",
    title: "3. Functional SAP User / Business Analyst",
    startingDay: 23,
    description: "Experienced with SAP GUI/Fiori and business transactions. Fast-tracks to end-to-end P2P, O2C, and cross-module processes.",
  },
  {
    id: "ecc_developer",
    title: "4. ECC Consultant / Classic ABAP Developer",
    startingDay: 45,
    description: "Extensive classic ECC 6.0 and DDIC experience. Fast-tracks past legacy structures to S/4HANA CDS, VDM, and code pushdown.",
  },
  {
    id: "experienced_s4hana",
    title: "5. Experienced S/4HANA Developer",
    startingDay: 77,
    description: "Advanced practitioner proficient in S/4HANA data modeling. Fast-tracks directly to modern ABAP Cloud, RAP, and BTP integration.",
  },
];

export default function SapPlacementPage() {
  const router = useRouter();
  const [selectedPersona, setSelectedPersona] = useState("fresher");
  const [currentProfile, setCurrentProfile] = useState<SapPlacementProfile | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [submittedSuccess, setSubmittedSuccess] = useState(false);

  useEffect(() => {
    sapApi
      .getPlacementProfile()
      .then((data) => {
        if (data) {
          setCurrentProfile(data);
          setSelectedPersona(data.persona);
        }
      })
      .catch(() => null);
  }, []);

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      // Simulate calibrated domain scores based on selected persona
      const domainScores: Record<string, number> = {
        erp_basics: selectedPersona === "fresher" ? 40 : 85,
        ddic_and_sql: ["ecc_developer", "experienced_s4hana"].includes(selectedPersona) ? 90 : 50,
        classic_abap: ["ecc_developer", "experienced_s4hana"].includes(selectedPersona) ? 85 : 30,
        modern_s4hana_rap: selectedPersona === "experienced_s4hana" ? 90 : 20,
        btp_integration: selectedPersona === "experienced_s4hana" ? 80 : 20,
      };

      await sapApi.submitPlacement({
        domain_scores: domainScores,
        persona_self_select: selectedPersona,
      });

      setSubmittedSuccess(true);
      setTimeout(() => {
        router.push("/sap/learning");
      }, 1500);
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AppShell>
      <div className="mx-auto max-w-[1000px] px-4 py-8">
        <div className="mb-6 flex items-center gap-2 text-xs font-mono font-bold text-muted">
          <Link href="/sap" className="hover:text-ink underline">
            SAP HUB
          </Link>
          <span>/</span>
          <span className="text-ink">DIAGNOSTIC PLACEMENT</span>
        </div>

        <div className="border-4 border-ink bg-surface p-6 sm:p-8 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] mb-8">
          <h1 className="text-2xl sm:text-3xl font-black text-ink mb-2">
            SAP Learner Placement Diagnostic
          </h1>
          <p className="text-sm text-muted mb-6 max-w-2xl leading-relaxed">
            The S/4HANA enterprise curriculum adapts to your background. Select your experience profile to fast-track past mastered concepts or start fresh from Day 1.
          </p>

          {currentProfile && (
            <div className="mb-6 border-2 border-ink bg-amber-100 p-4">
              <div className="text-xs font-mono font-bold uppercase text-ink">
                Current Placement Active
              </div>
              <div className="text-sm font-black text-ink mt-1">
                Persona: {currentProfile.persona.toUpperCase()} • Recommended Starting Day: Day {currentProfile.recommended_start_day}
              </div>
              <p className="text-xs text-muted mt-1">{currentProfile.rationale}</p>
            </div>
          )}

          <div className="space-y-3 mb-8">
            {PERSONAS.map((p) => {
              const isSelected = selectedPersona === p.id;
              return (
                <div
                  key={p.id}
                  onClick={() => setSelectedPersona(p.id)}
                  className={`cursor-pointer border-2 border-ink p-4 transition-all ${
                    isSelected
                      ? "bg-amber-100 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] translate-x-[1px] translate-y-[1px]"
                      : "bg-surface hover:bg-surface-raised"
                  }`}
                >
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <span className="text-sm font-black text-ink">{p.title}</span>
                    <span className="border border-ink bg-surface px-2 py-0.5 text-xs font-mono font-bold text-ink">
                      Starts Day {p.startingDay}
                    </span>
                  </div>
                  <p className="text-xs text-muted">{p.description}</p>
                </div>
              );
            })}
          </div>

          <div className="border-t-2 border-ink pt-6 flex flex-wrap items-center justify-between gap-4">
            {submittedSuccess ? (
              <div className="border-2 border-ink bg-emerald-300 px-4 py-2 text-xs font-bold text-ink">
                ✓ Diagnostic recorded! Starting milestones unlocked. Redirecting…
              </div>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={submitting}
                className="border-3 border-ink bg-cyan-300 px-6 py-3 text-sm font-black text-ink shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] transition-all disabled:opacity-50"
              >
                {submitting ? "Evaluating Diagnostic…" : "Confirm Placement & Unlock Track →"}
              </button>
            )}

            <Link
              href="/sap/learning"
              className="text-xs font-bold text-muted hover:text-ink underline"
            >
              Skip diagnostic and browse roadmap
            </Link>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
