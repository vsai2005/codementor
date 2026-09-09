import sys
import os
import copy
import math

# Add current path
sys.path.insert(0, os.path.abspath('.'))

from scratch.practice_generator.sec1_sec2 import SEC1_SEC2_PROBLEMS
from scratch.practice_generator.sec3_sec4 import SEC3_SEC4_PROBLEMS
from scratch.practice_generator.sec5_sec6 import SEC5_SEC6_PROBLEMS
from scratch.practice_generator.sec7_sec8 import SEC7_SEC8_PROBLEMS
from scratch.practice_generator.sec9_trees import SEC9_TREES_PROBLEMS
from scratch.practice_generator.sec10_heaps import SEC10_HEAPS_PROBLEMS
from scratch.practice_generator.sec11_graphs import SEC11_GRAPHS_PROBLEMS
from scratch.practice_generator.sec12_greedy import SEC12_GREEDY_PROBLEMS
from scratch.practice_generator.sec13_dp import SEC13_DP_PROBLEMS
from scratch.practice_generator.sec14_adv import SEC14_ADV_PROBLEMS

ALL_NEW = (
    SEC1_SEC2_PROBLEMS +
    SEC3_SEC4_PROBLEMS +
    SEC5_SEC6_PROBLEMS +
    SEC7_SEC8_PROBLEMS +
    SEC9_TREES_PROBLEMS +
    SEC10_HEAPS_PROBLEMS +
    SEC11_GRAPHS_PROBLEMS +
    SEC12_GREEDY_PROBLEMS +
    SEC13_DP_PROBLEMS +
    SEC14_ADV_PROBLEMS
)

print(f"Loaded {len(ALL_NEW)} newly authored problems.")

errors = []
passed_cases = 0
total_cases = 0

for prob in ALL_NEW:
    slug = prob["slug"]
    entry = prob["entry_point"]
    ref = prob["reference_solution"]
    cases = prob["test_cases"]

    if not ref:
        errors.append(f"Problem {slug} has NO reference solution!")
        continue

    # Execute reference solution in clean namespace
    ns = {}
    try:
        exec(ref, ns)
    except Exception as e:
        errors.append(f"Problem {slug} reference solution failed to compile: {e}")
        continue

    fn = ns.get(entry)
    if not fn:
        errors.append(f"Problem {slug} entry point '{entry}' not found in namespace!")
        continue

    for i, case in enumerate(cases):
        total_cases += 1
        args_copy = copy.deepcopy(case["args"])
        expected = case["expected"]

        try:
            actual = fn(*args_copy)
            # Check equality (with float tolerance if needed)
            if isinstance(expected, float) and isinstance(actual, (int, float)):
                match = math.isclose(actual, expected, rel_tol=1e-4, abs_tol=1e-4)
            else:
                match = (actual == expected)

            if match:
                passed_cases += 1
            else:
                errors.append(f"Problem {slug} case #{i+1} FAIL: args={case['args']} -> expected {expected} but got {actual}")
        except Exception as e:
            errors.append(f"Problem {slug} case #{i+1} ERROR: args={case['args']} -> raised {e}")

print("==================================================")
print(f"Test Execution Results: {passed_cases}/{total_cases} test cases passed across {len(ALL_NEW)} problems.")
if errors:
    print(f"FAILED WITH {len(errors)} ERRORS:")
    for err in errors[:20]:
        print("  [ERROR]", err)
    sys.exit(1)
else:
    print(">>> ALL 108 REFERENCE SOLUTIONS PASSED 100% OF TEST CASES! <<<")
    print("==================================================")
