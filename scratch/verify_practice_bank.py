"""Unified Master Verification Suite for the CodeMentor Practice Problem Bank.

Performs rigorous, end-to-end verification of:
1. Topic and problem catalog structure (16 topics, 178 problems).
2. Schema completeness (slug, title, tier, entry_point, starter_code, test_cases, reference_solution).
3. 100% reference solution execution against all test cases with deepcopy input isolation.
4. Anti-vacuous pass verification (empty `return None` stub must fail).
5. Full 160-day Curriculum Practice Map integrity (160 days, 100% slug resolution, no broken links).
"""

import copy
import json
import os
import sys
import time
import uuid

sys.path.insert(0, os.path.abspath("."))
import dev_backend.server as s
SEED_TOPICS, SEED_PROBLEMS = s.TOPICS_RAW, s.PROBLEMS_RAW

NS = uuid.UUID("00000000-0000-0000-0000-0000000c0de0")


def run_verification():
    print("=" * 80)
    print("CODEMENTOR PRACTICE PROBLEM BANK - MASTER VERIFICATION SUITE")
    print("=" * 80)

    # 1. Topic Verification
    print("\n[CHECK 1/5] Verifying Topics...")
    assert len(SEED_TOPICS) == 16, f"Expected 16 topics, found {len(SEED_TOPICS)}"
    topic_slugs = {slug for slug, _ in SEED_TOPICS}
    print(f"  + 16/16 topics validated: {', '.join(sorted(topic_slugs))}")

    # 2. Problem Schema Completeness
    print("\n[CHECK 2/5] Verifying Problem Catalog & Schema Integrity...")
    assert len(SEED_PROBLEMS) == 178, f"Expected 178 problems, found {len(SEED_PROBLEMS)}"

    seen_slugs = set()
    total_test_cases = 0

    for p in SEED_PROBLEMS:
        slug = p["slug"]
        assert slug not in seen_slugs, f"Duplicate slug: {slug}"
        seen_slugs.add(slug)

        assert p["topic"] in topic_slugs, f"Invalid topic {p['topic']} in {slug}"
        assert 1 <= p["difficulty_tier"] <= 5, f"Invalid tier {p['difficulty_tier']} in {slug}"
        assert p["title"], f"Missing title in {slug}"
        assert p["entry_point"], f"Missing entry_point in {slug}"
        assert p["statement_md"], f"Missing statement_md in {slug}"
        assert p["constraints_md"], f"Missing constraints_md in {slug}"
        assert "python" in p["starter_code"], f"Missing Python starter_code in {slug}"
        assert len(p["test_cases"]) >= 2, f"Fewer than 2 test cases in {slug}"
        assert "reference_solution" in p and p["reference_solution"].strip(), f"Missing reference_solution in {slug}"

        total_test_cases += len(p["test_cases"])

    print(f"  + 178/178 problems verified with complete schemas.")
    print(f"  + Total test cases across problem bank: {total_test_cases}")

    # 3. Reference Solution Execution (100% Test Pass Guarantee)
    print("\n[CHECK 3/5] Executing Reference Solutions against 100% of Test Cases...")
    t0 = time.time()
    passed_problems = 0
    failed_problems = []
    passed_cases_total = 0

    for p in SEED_PROBLEMS:
        slug = p["slug"]
        entry_point = p["entry_point"]
        ref_code = p["reference_solution"]
        cases = p["test_cases"]

        local_ns = {}
        try:
            exec(ref_code, local_ns)
        except Exception as e:
            failed_problems.append((slug, f"Compilation error: {e}"))
            continue

        fn = local_ns.get(entry_point)
        if not fn or not callable(fn):
            failed_problems.append((slug, f"Entry point {entry_point} not callable"))
            continue

        problem_passed = True
        for idx, tc in enumerate(cases):
            # Isolate input args with deepcopy to prevent in-place mutation side-effects
            args_copy = copy.deepcopy(tc["args"])
            expected = tc["expected"]

            try:
                actual = fn(*args_copy)
            except Exception as e:
                failed_problems.append((slug, f"Runtime error on case {idx} ({args_copy}): {e}"))
                problem_passed = False
                break

            # Check equality (with float tolerance if floats are involved)
            if isinstance(expected, float) and isinstance(actual, (float, int)):
                if abs(actual - expected) > 1e-4:
                    failed_problems.append((slug, f"Case {idx} mismatch: expected {expected}, got {actual}"))
                    problem_passed = False
                    break
            elif actual != expected:
                failed_problems.append((slug, f"Case {idx} mismatch: expected {expected}, got {actual}"))
                problem_passed = False
                break

            passed_cases_total += 1

        if problem_passed:
            passed_problems += 1

    dt = time.time() - t0
    print(f"  + Reference solutions tested: {len(SEED_PROBLEMS)}")
    print(f"  + Problems passing 100% of test cases: {passed_problems}/{len(SEED_PROBLEMS)}")
    print(f"  + Total test cases passed: {passed_cases_total}/{total_test_cases}")
    print(f"  + Total execution time: {dt:.2f} seconds")

    if failed_problems:
        print("\n  [FAILURES ENCOUNTERED]")
        for f in failed_problems[:10]:
            print(f"    - {f[0]}: {f[1]}")
        sys.exit(1)
    else:
        print("  + ZERO test failures. 100% of reference solutions verified!")

    # 4. Anti-Vacuous Pass Check
    print("\n[CHECK 4/5] Running Anti-Vacuous Pass Check (empty stubs must fail)...")
    vacuous_passes = []
    for p in SEED_PROBLEMS:
        slug = p["slug"]
        cases = p["test_cases"]
        # If all cases have expected == None, return None is valid; otherwise it must fail
        has_non_none = any(tc["expected"] is not None for tc in cases)
        if has_non_none:
            # Test a stub function that returns None
            stub_code = f"def {p['entry_point']}(*args, **kwargs):\n    return None\n"
            local_ns = {}
            exec(stub_code, local_ns)
            fn = local_ns[p["entry_point"]]
            all_stub_passed = True
            for tc in cases:
                if fn(*copy.deepcopy(tc["args"])) != tc["expected"]:
                    all_stub_passed = False
                    break
            if all_stub_passed:
                vacuous_passes.append(slug)

    print(f"  + Vacuous pass check passed! {len(vacuous_passes)} vacuous problems found.")
    assert len(vacuous_passes) == 0, f"Vacuous problems: {vacuous_passes}"

    # 5. Curriculum Practice Map Integrity Check
    print("\n[CHECK 5/5] Verifying 160-Day Curriculum -> Practice Map Integrity...")
    ts_path = os.path.join("frontend", "lib", "curriculum", "practiceCoverageMap.ts")
    assert os.path.exists(ts_path), f"File {ts_path} does not exist"

    with open(ts_path, "r", encoding="utf-8") as f:
        ts_content = f.read()

    import re
    # Extract entries: day_number, primary_problem_slug, practice_problem_slugs
    day_matches = re.findall(r'(\d+):\s*\{([^}]+)\}', ts_content)
    assert len(day_matches) == 160, f"Expected 160 day entries in TS file, found {len(day_matches)}"

    mapped_slugs = set()
    for day_str, block in day_matches:
        day = int(day_str)
        pri_match = re.search(r'primary_problem_slug:\s*"([^"]+)"', block)
        assert pri_match, f"Missing primary_problem_slug for day {day}"
        primary = pri_match.group(1)
        assert primary in seen_slugs, f"Primary slug '{primary}' for Day {day} not in problem bank"
        mapped_slugs.add(primary)

        slugs_match = re.search(r'practice_problem_slugs:\s*(\[[^\]]+\])', block)
        assert slugs_match, f"Missing practice_problem_slugs for day {day}"
        slugs_list = json.loads(slugs_match.group(1))
        for s_slug in slugs_list:
            assert s_slug in seen_slugs, f"Practice slug '{s_slug}' for Day {day} not in problem bank"
            mapped_slugs.add(s_slug)

    print(f"  + 160/160 curriculum days mapped with 100% valid slug resolution.")
    print(f"  + Distinct problems leveraged across the 160 days: {len(mapped_slugs)}")

    print("\n" + "=" * 80)
    print("ALL VERIFICATION CHECKS PASSED WITH ZERO ERRORS!")
    print("=" * 80)


if __name__ == "__main__":
    run_verification()
