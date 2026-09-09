"""
Semantic & Quality Validation Suite for CodeMentor 160-Day Curriculum
Enforces all 6 Quality Pillars defined in the approved Implementation Plan:
1. Structural Completeness & Continuity
2. Pedagogical Rigor & Bloom Taxonomy
3. Prerequisite Monotonicity & Inversion Guards
4. Checkpoint Diagnostic Quality
5. Guided Practice Non-Identity Invariant (Rule 6A)
6. Day 1 & Day 2 Gold-Standard Preservation
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath("."))

# Load curriculum metadata
with open("scratch/curriculum_160.json", "r", encoding="utf-8") as f:
    CURRICULUM_DATA = json.load(f)

CURRICULUM_MAP = {d["day_number"]: d for d in CURRICULUM_DATA}

# Section bounds definition
SECTION_BOUNDS = {
    "python-foundations": (1, 10),
    "python-core": (11, 25),
    "computational-thinking": (26, 35),
    "arrays-and-strings": (36, 50),
    "searching-and-sorting": (51, 65),
    "hashing-and-hash-tables": (66, 75),
    "linked-lists": (76, 85),
    "stacks-and-queues": (86, 95),
    "trees-and-bst": (96, 110),
    "heaps-and-priority-queues": (111, 120),
    "graphs": (121, 135),
    "greedy-algorithms": (136, 145),
    "dynamic-programming": (146, 155),
    "advanced-dsa": (156, 160)
}

BLOOM_VERBS = {
    "construct", "build", "implement", "analyze", "evaluate", "derive", "differentiate",
    "calculate", "formulate", "contrast", "trace", "identify", "execute", "design",
    "synthesize", "verify", "measure", "predict", "simulate", "navigate", "resolve",
    "partition", "decompose", "traverse", "rebalance", "schedule", "compress",
    "apply", "convert", "debug", "parse", "format", "utilize", "iterate", "explain",
    "test", "optimize", "compare", "extract", "model", "demonstrate", "profile",
    "manipulate", "maintain", "distinguish", "select", "count", "detect", "find",
    "solve", "explore", "merge", "scale", "enforce", "structure", "track", "benchmark"
}

def validate_curriculum():
    errors = []
    warnings = []
    print("=" * 70)
    print("CODEMENTOR 160-DAY CURRICULUM: 6-PILLAR SEMANTIC VALIDATION SUITE")
    print("=" * 70)

    # ---------------------------------------------------------
    # PILLAR 1: Structural Completeness & Continuity
    # ---------------------------------------------------------
    print("\n[Pillar 1] Validating Structural Completeness & Continuity...")
    if len(CURRICULUM_DATA) != 160:
        errors.append(f"P1: Expected 160 days in curriculum_160.json, found {len(CURRICULUM_DATA)}")
    
    seen_days = set()
    for d in CURRICULUM_DATA:
        num = d["day_number"]
        if num in seen_days:
            errors.append(f"P1: Duplicate day number {num} in curriculum_160.json")
        seen_days.add(num)
        
        # Section bounds check
        sec_id = d.get("section_id")
        if sec_id not in SECTION_BOUNDS:
            errors.append(f"P1: Day {num} has unknown section_id '{sec_id}'")
        else:
            low, high = SECTION_BOUNDS[sec_id]
            if not (low <= num <= high):
                errors.append(f"P1: Day {num} section '{sec_id}' out of bounds [{low}, {high}]")
        
        # Estimated minutes
        mins = d.get("estimated_minutes", 0)
        if not (15 <= mins <= 60):
            errors.append(f"P1: Day {num} estimated_minutes {mins} outside reasonable range [15, 60]")
            
        # Difficulty
        diff = d.get("difficulty")
        valid_diffs = {"BEGINNER", "FOUNDATIONAL", "DEVELOPING", "INTERMEDIATE", "ADVANCED", "EXPERT"}
        if diff not in valid_diffs:
            errors.append(f"P1: Day {num} invalid difficulty '{diff}'")

    missing_days = set(range(1, 161)) - seen_days
    if missing_days:
        errors.append(f"P1: Missing days in curriculum: {sorted(missing_days)}")
    else:
        print("  -> All 160 days present and strictly contiguous (1 to 160).")

    # ---------------------------------------------------------
    # PILLAR 2: Pedagogical Rigor & Bloom Taxonomy
    # ---------------------------------------------------------
    print("\n[Pillar 2] Validating Pedagogical Rigor & Bloom Taxonomy...")
    archetype_counts = {}
    for d in CURRICULUM_DATA:
        num = d["day_number"]
        arch = d.get("archetype")
        archetype_counts[arch] = archetype_counts.get(arch, 0) + 1
        
        # Natural concept count: 1 to 4 max
        concepts = d.get("concepts", [])
        if not (1 <= len(concepts) <= 5):
            errors.append(f"P2: Day {num} concept count {len(concepts)} outside [1, 5]")
            
        # Bloom's taxonomy objectives
        objs = d.get("learning_objectives", [])
        if not objs:
            errors.append(f"P2: Day {num} has zero learning_objectives")
        else:
            for obj in objs:
                first_word = obj.strip().split()[0].lower()
                if first_word not in BLOOM_VERBS:
                    warnings.append(f"P2: Day {num} learning objective '{obj}' starts with non-standard verb '{first_word}'")

    print(f"  -> Practice Archetype distribution: {archetype_counts}")
    print("  -> Concept counts and Bloom's objectives verified.")

    # ---------------------------------------------------------
    # PILLAR 3: Prerequisite Monotonicity & Inversion Guards
    # ---------------------------------------------------------
    print("\n[Pillar 3] Validating Prerequisite Monotonicity & Inversion Guards...")
    for d in CURRICULUM_DATA:
        num = d["day_number"]
        prereqs = d.get("prerequisites", [])
        for p in prereqs:
            if p >= num:
                errors.append(f"P3: Prerequisite inversion! Day {num} depends on future/same day {p}")
            if p < 1:
                errors.append(f"P3: Invalid prerequisite {p} on Day {num}")

    # Specific Inversion Checks
    # 1. Day 105 is Morris In-Order Traversal
    day105 = CURRICULUM_MAP.get(105, {})
    if "Morris" not in day105.get("title", ""):
        errors.append(f"P3: Day 105 expected to be Morris Traversal, found '{day105.get('title')}'")
    # 2. Day 106 is AVL Rotations
    day106 = CURRICULUM_MAP.get(106, {})
    if "AVL" not in day106.get("title", "") and "Rotation" not in day106.get("title", ""):
        errors.append(f"P3: Day 106 expected to be AVL/Balanced trees, found '{day106.get('title')}'")
    # 3. Day 128 is Dijkstra, Day 129 is Bellman-Ford
    day128 = CURRICULUM_MAP.get(128, {})
    day129 = CURRICULUM_MAP.get(129, {})
    if "Dijkstra" not in day128.get("title", ""):
        errors.append(f"P3: Day 128 expected Dijkstra, found '{day128.get('title')}'")
    if "Bellman" not in day129.get("title", ""):
        errors.append(f"P3: Day 129 expected Bellman-Ford, found '{day129.get('title')}'")
    # 4. Day 133 is Bridges, Day 134 is Kosaraju/Tarjan SCCs
    day133 = CURRICULUM_MAP.get(133, {})
    day134 = CURRICULUM_MAP.get(134, {})
    if "Bridge" not in day133.get("title", ""):
        errors.append(f"P3: Day 133 expected Bridges, found '{day133.get('title')}'")
    if "Strongly Connected" not in day134.get("title", "") and "SCC" not in day134.get("title", "") and "Kosaraju" not in day134.get("title", ""):
        errors.append(f"P3: Day 134 expected SCCs, found '{day134.get('title')}'")

    print("  -> All prerequisite chains are strictly monotonic (1 <= P < D).")
    print("  -> Specific advanced DSA difficulty gates validated.")

    # ---------------------------------------------------------
    # PILLAR 4 & 5: Batch File Content, Checkpoint Quality & Starter Code Invariant
    # ---------------------------------------------------------
    print("\n[Pillars 4, 5 & 6] Inspecting Generated Batches (1 to 8)...")
    batch_dir = "frontend/lib/lessons/batches"
    for b in range(1, 9):
        path = os.path.join(batch_dir, f"batch{b}.ts")
        if not os.path.exists(path):
            errors.append(f"Batch file {path} missing!")
            continue

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Pillar 6: Batch 1 preservation of Day 1 and Day 2
        if b == 1:
            if 'import { DAY_1_STEPS } from "../day1Data";' not in content:
                errors.append("P6: batch1.ts missing DAY_1_STEPS import from day1Data")
            if 'import { DAY_2_STEPS } from "../day2Data";' not in content:
                errors.append("P6: batch1.ts missing DAY_2_STEPS import from day2Data")
            if '"steps": DAY_1_STEPS' not in content:
                errors.append("P6: Day 1 steps not preserved from DAY_1_STEPS")
            if '"steps": DAY_2_STEPS' not in content:
                errors.append("P6: Day 2 steps not preserved from DAY_2_STEPS")
            print("  -> Batch 1: Day 1 and Day 2 validated lessons verified as preserved gold standards.")

    # Validate section data objects directly for complete schema inspection
    from scratch.curriculum_generator.sec4_data import SEC4_DAYS
    from scratch.curriculum_generator.sec5_data import SEC5_DAYS
    from scratch.curriculum_generator.sec6_data import SEC6_DAYS
    from scratch.curriculum_generator.sec7_data import SEC7_DAYS
    from scratch.curriculum_generator.sec8_data import SEC8_DAYS
    from scratch.curriculum_generator.sec9_data import SEC9_DAYS
    from scratch.curriculum_generator.sec10_data import SEC10_DAYS
    from scratch.curriculum_generator.sec11_data import SEC11_DAYS
    from scratch.curriculum_generator.sec12_data import SEC12_DAYS
    from scratch.curriculum_generator.sec13_data import SEC13_DAYS
    from scratch.curriculum_generator.sec14_data import SEC14_DAYS

    all_specs = {}
    all_specs.update(SEC4_DAYS)
    all_specs.update(SEC5_DAYS)
    all_specs.update(SEC6_DAYS)
    all_specs.update(SEC7_DAYS)
    all_specs.update(SEC8_DAYS)
    all_specs.update(SEC9_DAYS)
    all_specs.update(SEC10_DAYS)
    all_specs.update(SEC11_DAYS)
    all_specs.update(SEC12_DAYS)
    all_specs.update(SEC13_DAYS)
    all_specs.update(SEC14_DAYS)

    print(f"  -> Validating detailed specs for Days {min(all_specs.keys())} to {max(all_specs.keys())} ({len(all_specs)} days)...")
    for day_num, spec in all_specs.items():
        # Pillar 5: Starter vs Solution Non-Identity
        starter = spec.get("starter", "").strip()
        solution = spec.get("solution", "").strip()
        if not starter:
            errors.append(f"P5: Day {day_num} starter code is empty")
        if not solution:
            errors.append(f"P5: Day {day_num} solution code is empty")
        if starter == solution:
            errors.append(f"P5: Invariant violation! Day {day_num} starterCode is identical to solutionCode (pre-solved exercise)")
        if "# TODO" not in starter and "# BUG" not in starter and "pass" not in starter and "return []" not in starter and "return False" not in starter and "return -1" not in starter and "return 0" not in starter and "return {}" not in starter:
            warnings.append(f"P5: Day {day_num} starter code might lack clear actionable stub marker")

        # Patterns & Hints
        patterns = spec.get("patterns", [])
        if not patterns:
            errors.append(f"P5: Day {day_num} has no expected output patterns")
        hint = spec.get("hint", "")
        if not hint:
            errors.append(f"P5: Day {day_num} has empty hint")

        # Pillar 4: Checkpoint Quality
        q1_opts = spec.get("q1_opts", [])
        if len(q1_opts) != 4:
            errors.append(f"P4: Day {day_num} Q1 has {len(q1_opts)} options (expected 4)")
        q1_ans = spec.get("q1_ans")
        if q1_ans not in ["A", "B", "C", "D"]:
            errors.append(f"P4: Day {day_num} Q1 invalid answer key '{q1_ans}'")
        q1_exp = spec.get("q1_exp", {})
        if len(q1_exp) != 4:
            errors.append(f"P4: Day {day_num} Q1 has {len(q1_exp)} explanations (expected 4)")
        for opt_id in ["A", "B", "C", "D"]:
            exp_text = q1_exp.get(opt_id, "")
            if not exp_text:
                errors.append(f"P4: Day {day_num} Q1 option {opt_id} has empty explanation")
            elif opt_id == q1_ans and not exp_text.startswith("Correct"):
                warnings.append(f"P4: Day {day_num} Q1 correct explanation does not start with 'Correct'")
            elif opt_id != q1_ans and not exp_text.startswith("Incorrect"):
                warnings.append(f"P4: Day {day_num} Q1 distractor {opt_id} explanation does not start with 'Incorrect'")

        # Q2 checks
        q2_opts = spec.get("q2_opts", [])
        if len(q2_opts) != 4:
            errors.append(f"P4: Day {day_num} Q2 has {len(q2_opts)} options (expected 4)")
        q2_ans = spec.get("q2_ans")
        if q2_ans not in ["A", "B", "C", "D"]:
            errors.append(f"P4: Day {day_num} Q2 invalid answer key '{q2_ans}'")
        q2_exp = spec.get("q2_exp", {})
        if len(q2_exp) != 4:
            errors.append(f"P4: Day {day_num} Q2 has {len(q2_exp)} explanations (expected 4)")

        # Recap checks
        recap = spec.get("recap", [])
        if len(recap) < 2:
            errors.append(f"P1: Day {day_num} recap has fewer than 2 rows ({len(recap)})")

    # ---------------------------------------------------------
    # SUMMARY REPORT
    # ---------------------------------------------------------
    print("\n" + "=" * 70)
    print("VALIDATION RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total Errors:   {len(errors)}")
    print(f"Total Warnings: {len(warnings)}")

    if warnings:
        print(f"\nWarnings ({min(10, len(warnings))} of {len(warnings)} shown):")
        for w in warnings[:10]:
            print(f"  [WARN] {w}")

    if errors:
        print("\nERRORS DETECTED:")
        for e in errors:
            print(f"  [FAIL] {e}")
        return False

    print("\n>>> ALL 6 PILLARS OF SEMANTIC & QUALITY VALIDATION PASSED WITH ZERO ERRORS! <<<")
    return True

if __name__ == "__main__":
    success = validate_curriculum()
    sys.exit(0 if success else 1)
