import Link from "next/link";

import { Hero3D } from "@/components/Hero3D";

const PILLARS = [
  {
    title: "Reviewed, not just graded",
    body: "A senior engineer's read on your code: complexity, readability, edge cases — scored across five dimensions, not one pass/fail bit.",
  },
  {
    title: "Difficulty that tracks you",
    body: "A rolling weighted average moves each topic's tier independently. Tier 4 in arrays and tier 2 in graphs is a normal profile, not a bug.",
  },
  {
    title: "Memory across sessions",
    body: "Every review leaves a note. Come back in a week and the tutor already knows the mistake you keep making.",
  },
];

export default function LandingPage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12 sm:py-20">
      <section className="grid items-center gap-8 lg:grid-cols-[1.15fr_0.85fr]">
        <div>
          <p className="label mb-3">Placement prep, sharpened</p>
          <h1 className="font-display text-4xl font-bold leading-[1.05] sm:text-6xl">
            Stop guessing why
            <br />
            your code is <span className="text-accent">weak</span>.
          </h1>
          <p className="mt-5 max-w-xl font-body text-base leading-relaxed text-muted">
            Most platforms tell you whether the tests passed. CodeMentor tells you what a
            reviewer would say, adjusts the next problem to your real level, and remembers
            the pattern you keep repeating.
          </p>
          <div className="mt-7 flex flex-wrap gap-3">
            <Link href="/login" className="btn btn-primary">
              Start practising
            </Link>
            <Link href="/practice" className="btn">
              Browse problems
            </Link>
          </div>
        </div>

        <div className="card p-4">
          <Hero3D />
        </div>
      </section>

      <section className="mt-16 grid gap-4 sm:grid-cols-3">
        {PILLARS.map((pillar) => (
          <div key={pillar.title} className="card p-4">
            <h2 className="font-display text-lg font-bold leading-tight">{pillar.title}</h2>
            <p className="mt-2 font-body text-sm leading-relaxed text-muted">{pillar.body}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
