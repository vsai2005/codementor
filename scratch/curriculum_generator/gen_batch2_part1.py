import json
import os

from scratch.curriculum_generator.common import (
    CURRICULUM_MAP,
    get_difficulty,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)
from scratch.curriculum_generator.sec2_core_part3 import get_sec2_part3_days
from scratch.curriculum_generator.sec3_computational import get_sec3_days

def get_batch2_days():
    days = {}
    days.update(get_sec2_part3_days()) # Days 21-25
    days.update(get_sec3_days())       # Days 26-27

    # DAY 28: Recursion Fundamentals & Call Stack Frames
    days[28] = {
        "dayNumber": 28,
        "title": "Recursion Fundamentals & Call Stack",
        "topicName": "Recursion Foundations",
        "sectionId": "computational-thinking",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [27],
        "concepts": ["Base Case Invariant", "Recursive Step", "Call Stack Unwinding", "Recursion Depth Limits"],
        "practiceSkills": ["Base Case Design", "Call Stack Tracing", "Recursive Decomposition"],
        "steps": [
            make_explanation_step(
                "day28-step1", 1, "The Anatomy of Recursion", "Base Case & Step",
                "How Recursion Works: Base Case, Recursive Leap, and Stack Frames",
                "Master the two essential components that prevent infinite recursion.",
                [
                    "Recursion is a programming paradigm where a function solves a problem by calling itself on smaller instances of the exact same problem.",
                    "Every valid recursive function must contain two essential parts:",
                    "1. **Base Case(s)**: A terminating condition that returns a result immediately without making further recursive calls.",
                    "2. **Recursive Step**: Reduces the problem size toward the base case and combines the returned result.",
                    "Without a base case, or if the recursive step does not shrink the input, the function pushes frames indefinitely until hitting Python's `sys.getrecursionlimit()`."
                ],
                snippets=[{
                    "title": "Anatomy of Factorial Recursion",
                    "code": "def factorial(n):\n    # 1. Base Case: stop condition\n    if n <= 1:\n        return 1\n    # 2. Recursive Step: shrink problem size toward base case\n    return n * factorial(n - 1)",
                    "language": "python",
                    "caption": "Clear base case and shrinking recursive subproblem."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Recursion Limit in Python",
                    "content": "Python's default recursion limit is 1,000 frames. Deep recursion ($N > 1000$) will crash with `RecursionError` unless rewritten iteratively."
                }],
                takeaway="Recursion requires a base case to terminate and a recursive step that shrinks toward the base case."
            ),
            make_explanation_step(
                "day28-step2", 2, "Call Stack Unwinding & Return Phase", "Unwinding Phase",
                "Winding vs Unwinding: How Values Propagate Back Up the Stack",
                "Understand the two phases of recursive execution.",
                [
                    "A recursive call involves two distinct phases:",
                    "1. **Winding Phase (Downwards)**: Frames are pushed onto the stack as the problem is broken down into subproblems.",
                    "2. **Unwinding Phase (Upwards)**: Once the base case is reached, each frame computes its result using the returned value from its child frame and pops off the stack.",
                    "Work performed before the recursive call executes on the way down; work performed after the recursive call executes on the way up during unwinding."
                ],
                snippets=[{
                    "title": "Pre-order vs Post-order Actions in Recursion",
                    "code": "def countdown_and_up(n):\n    if n == 0:\n        print('Liftoff!')\n        return\n    print('Down:', n)         # Pre-recursion (winding)\n    countdown_and_up(n - 1)\n    print('Up:', n)           # Post-recursion (unwinding)",
                    "language": "python",
                    "caption": "Actions executed before vs after the recursive call."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Think Subproblem, Not Stack",
                    "content": "When writing recursion, trust that `solve(n - 1)` correctly computes the subproblem, then focus only on how to combine it with `n`."
                }],
                takeaway="Work before the call runs on the way down; work after the call runs on the way up as frames unwind."
            ),
            make_checkpoint_step(
                "day28-step3", 3, "Recursion Checkpoint", "Checkpoint",
                "Test Your Understanding of Recursive Invariants",
                "Identify base case flaws and trace stack unwinding.",
                [
                    {
                        "id": "chk-d28-q1",
                        "question": "What happens if a recursive function does NOT make progress toward its base case?",
                        "options": [
                            {"id": "A", "label": "It returns None"},
                            {"id": "B", "label": "It enters an infinite loop until Python raises RecursionError"},
                            {"id": "C", "label": "It automatically converts to an iterative loop"},
                            {"id": "D", "label": "The CPU halts"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: It never reaches a return statement.",
                            "B": "Correct! Without shrinking the input, recursive calls push frames until exceeding sys.getrecursionlimit(), raising RecursionError: maximum recursion depth exceeded.",
                            "C": "Incorrect: Python has no automatic iteration compiler.",
                            "D": "Incorrect: The Python runtime intercepts stack overflow gracefully."
                        }
                    },
                    {
                        "id": "chk-d28-q2",
                        "question": "In `def f(n): if n == 0: return; print(n); f(n-1); print(n)`, what prints for `f(2)`?",
                        "options": [
                            {"id": "A", "label": "2, 1, 1, 2"},
                            {"id": "B", "label": "2, 1, 2, 1"},
                            {"id": "C", "label": "1, 2, 2, 1"},
                            {"id": "D", "label": "2, 1"}
                        ],
                        "correctOptionId": "A",
                        "explanations": {
                            "A": "Correct! On the way down: prints 2, then 1. On unwinding: prints 1, then 2. Result: 2, 1, 1, 2.",
                            "B": "Incorrect: Unwinding pops the innermost frame (n=1) first.",
                            "C": "Incorrect: The first print executes before recursive call.",
                            "D": "Incorrect: The second print executes during unwinding."
                        }
                    }
                ],
                takeaway="Recursion unwinds in LIFO order; failing to shrink inputs triggers RecursionError."
            ),
            make_practice_step(
                "day28-step4", 4, "Recursive String Reversal", "Practice",
                "Reverse a String Recursively Without Slices",
                "Implement string reversal by decomposing into head character and tail substring.",
                "Recursive Reverser",
                [
                    "Write a recursive function `reverse_str(s)`.",
                    "Base case: if `len(s) <= 1`, return `s`.",
                    "Recursive step: return `reverse_str(s[1:]) + s[0]`.",
                    "Call `reverse_str('algorithm')` and print `'Reversed:', result`."
                ],
                """# Day 28 Practice: Recursive Reverser

def reverse_str(s):
    # TODO: Implement base case and recursive step
    if len(s) <= 1:
        return s
    return reverse_str(s[1:]) + s[0]

result = reverse_str("algorithm")
print("Reversed:", result)
""",
                """def reverse_str(s):
    if len(s) <= 1:
        return s
    return reverse_str(s[1:]) + s[0]

result = reverse_str("algorithm")
print("Reversed:", result)
""",
                ["Reversed: mhtirogla"],
                "Return `s` when `len(s) <= 1`, otherwise return `reverse_str(s[1:]) + s[0]`.",
                takeaway="Recursion unwinds strings by appending the head character after reversing the tail."
            ),
            make_completion_step(
                "day28-step5", 5, "Recursion Fundamentals Mastery", "Recap",
                28, "Day 28 Complete: Recursion Fundamentals & Call Stack",
                "You have mastered base case design, call stack unwinding, and recursion depth limits.",
                [
                    {
                        "concept": "Base Case Omission",
                        "naiveIntuition": "The compiler will detect if a loop or recursion doesn't stop",
                        "pythonReality": "Missing base cases cause runtime stack overflow (RecursionError)"
                    },
                    {
                        "concept": "Execution Order",
                        "naiveIntuition": "All statements execute before recursive calls",
                        "pythonReality": "Statements after the recursive call execute on stack unwinding in reverse order"
                    }
                ],
                ["Base Case Invariant", "Recursive Problem Shrinking", "Stack Winding and Unwinding", "RecursionError Limit Guard"],
                get_next_preview(28)
            )
        ]
    }

    # DAY 29: Recurrence Relations & Master Theorem
    days[29] = {
        "dayNumber": 29,
        "title": "Recurrence Relations & Master Theorem",
        "topicName": "Recurrences & Master Theorem",
        "sectionId": "computational-thinking",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [28],
        "concepts": ["Recurrence Equations", "Master Theorem Cases", "Recursion Trees", "Divide & Conquer Scaling"],
        "practiceSkills": ["Recurrence Formulation", "Master Theorem Application", "Tree Depth Derivation"],
        "steps": [
            make_explanation_step(
                "day29-step1", 1, "Formulating Recurrence Relations", "Recurrences",
                "Expressing Algorithmic Runtimes as Mathematical Equations",
                "How to express recursive time complexity as $T(N) = a T(N/b) + f(N)$.",
                [
                    "A **recurrence relation** expresses the time required to solve a problem of size $N$ in terms of the time required to solve smaller subproblems.",
                    "The standard divide-and-conquer recurrence has the form: $$T(N) = a \\cdot T(N/b) + f(N)$$ where:",
                    "- $a \\ge 1$: Number of recursive subproblems created.",
                    "- $b > 1$: Factor by which input size is divided at each step.",
                    "- $f(N)$: Non-recursive work required to divide the problem and merge solutions.",
                    "For example, Merge Sort divides an array into $2$ halves ($a=2, b=2$) and takes $O(N)$ linear time to merge them: $T(N) = 2T(N/2) + O(N)$."
                ],
                snippets=[{
                    "title": "Merge Sort Recurrence",
                    "code": "# T(N) = 2 * T(N / 2) + O(N)\n# At depth d: 2^d subproblems of size N / 2^d\n# Total levels: log2(N)\n# Work per level: N\n# Total Time: O(N log N)",
                    "language": "python",
                    "caption": "Merge sort recursion tree derivation."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Tree Depth",
                    "content": "Dividing $N$ by $b$ at each step yields a tree of depth $\\log_b N$."
                }],
                takeaway="Recurrences model divide-and-conquer algorithms via subproblem count, division factor, and merge work."
            ),
            make_explanation_step(
                "day29-step2", 2, "The Master Theorem", "Master Theorem",
                "Instant Complexity Analysis with the 3 Master Theorem Cases",
                "Compare subproblem creation rate against leaf work.",
                [
                    "The **Master Theorem** solves recurrences $T(N) = a T(N/b) + \\Theta(N^c)$ by comparing the critical exponent $\\log_b a$ against $c$:",
                    "1. **Case 1 (Leaf Dominated)**: If $\\log_b a > c$, leaf work dominates: $$T(N) = \\Theta(N^{\\log_b a})$$",
                    "2. **Case 2 (Balanced Work)**: If $\\log_b a = c$, all levels do equal work: $$T(N) = \\Theta(N^c \\log N)$$ *(e.g. Merge Sort: $\\log_2 2 = 1 = c \\implies O(N \\log N)$)*",
                    "3. **Case 3 (Root Dominated)**: If $\\log_b a < c$, root/split work dominates: $$T(N) = \\Theta(N^c)$$"
                ],
                snippets=[{
                    "title": "Master Theorem Quick Checks",
                    "code": "# Binary Search: T(N) = 1*T(N/2) + O(1)\n# a=1, b=2, c=0 -> log2(1) = 0 == c -> Case 2 -> O(log N)\n\n# Karatsuba Multiplication: T(N) = 3*T(N/2) + O(N)\n# a=3, b=2, c=1 -> log2(3) = 1.585 > 1 -> Case 1 -> O(N^1.585)",
                    "language": "python",
                    "caption": "Applying the Master Theorem across classic algorithms."
                }],
                callouts=[{
                    "type": "deep-dive",
                    "title": "When Master Theorem Doesn't Apply",
                    "content": "Master Theorem only applies when subproblems are equal in size ($N/b$). It cannot solve Fibonacci ($T(N) = T(N-1) + T(N-2)$); use characteristic equations or recurrence trees instead."
                }],
                takeaway="Compare log_b(a) with c to instantly identify whether leaves, root, or all levels dominate."
            ),
            make_checkpoint_step(
                "day29-step3", 3, "Master Theorem Checkpoint", "Checkpoint",
                "Test Your Mastery of Recurrence Relations",
                "Classify recurrences and apply the Master Theorem.",
                [
                    {
                        "id": "chk-d29-q1",
                        "question": "What is the time complexity of the recurrence $T(N) = 4 T(N/2) + O(N)$?",
                        "options": [
                            {"id": "A", "label": "O(N log N)"},
                            {"id": "B", "label": "O(N^2)"},
                            {"id": "C", "label": "O(N)"},
                            {"id": "D", "label": "O(4^N)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: log2(4) = 2, which is strictly greater than c = 1.",
                            "B": "Correct! a = 4, b = 2, c = 1. Critical exponent log_b(a) = log2(4) = 2. Since 2 > 1, Case 1 applies: T(N) = Theta(N^2).",
                            "C": "Incorrect: Subproblem creation rate dwarfs the linear merge work.",
                            "D": "Incorrect: Polynomial, not exponential."
                        }
                    },
                    {
                        "id": "chk-d29-q2",
                        "question": "What recurrence relation represents standard Binary Search?",
                        "options": [
                            {"id": "A", "label": "T(N) = 2 T(N/2) + O(1)"},
                            {"id": "B", "label": "T(N) = T(N/2) + O(1)"},
                            {"id": "C", "label": "T(N) = T(N - 1) + O(1)"},
                            {"id": "D", "label": "T(N) = 2 T(N/2) + O(N)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Binary search only searches one half, not both.",
                            "B": "Correct! It creates 1 subproblem of size N/2 and performs O(1) comparison work: T(N) = T(N/2) + O(1), giving O(log N).",
                            "C": "Incorrect: It divides the search space in half, rather than subtracting 1.",
                            "D": "Incorrect: That is Merge Sort."
                        }
                    }
                ],
                takeaway="T(N) = 4T(N/2) + O(N) yields O(N^2); Binary Search is T(N) = T(N/2) + O(1) -> O(log N)."
            ),
            make_practice_step(
                "day29-step4", 4, "Simulate Recurrence Tree Operations", "Practice",
                "Trace Work Per Level in a Recurrence Tree",
                "Simulate level-by-level work calculation for $T(N) = 2T(N/2) + N$.",
                "Recurrence Tree Work Calculator",
                [
                    "Given `n = 16`, calculate the total work across all levels of the recurrence tree for $T(N) = 2T(N/2) + N$.",
                    "At level 0, there is 1 node of size 16 (work: 16).",
                    "At each subsequent level, node count doubles and node size halves, so work per level remains $N = 16$.",
                    "The number of levels is `math.log2(n) + 1`.",
                    "Compute `total_work = n * int(math.log2(n) + 1)` and print `'Total operations:', total_work`."
                ],
                """# Day 29 Practice: Recurrence Tree Work Calculator
import math

n = 16

# TODO: Compute levels = int(math.log2(n)) + 1
levels = int(math.log2(n)) + 1
# Total work is n * levels
total_work = n * levels

print("Total operations:", total_work)
""",
                """import math

n = 16
levels = int(math.log2(n)) + 1
total_work = n * levels

print("Total operations:", total_work)
""",
                ["Total operations: 80"],
                "Levels is log2(16) + 1 = 5 levels; 16 * 5 = 80 operations.",
                takeaway="When each tree level performs equal work, total complexity is work_per_level * depth."
            ),
            make_completion_step(
                "day29-step5", 5, "Recurrence Relations Mastery", "Recap",
                29, "Day 29 Complete: Recurrence Relations & Master Theorem",
                "You have mastered recurrence modeling, the 3 Master Theorem cases, and recursion trees.",
                [
                    {
                        "concept": "Balanced Work Case",
                        "naiveIntuition": "Dividing in half always gives O(log N)",
                        "pythonReality": "Only if merge work is O(1); if merge work is O(N), total time is O(N log N)"
                    },
                    {
                        "concept": "Unequal Subproblems",
                        "naiveIntuition": "Master theorem works on all recursive functions",
                        "pythonReality": "It only applies to equal division (N/b); unequal splits require tree summation"
                    }
                ],
                ["T(N) = aT(N/b) + f(N) Formulation", "Critical Exponent log_b(a)", "3 Master Theorem Regimes", "Recursion Tree Level Summation"],
                get_next_preview(29)
            )
        ]
    }

    # DAY 30: Divide and Conquer Paradigm
    days[30] = {
        "dayNumber": 30,
        "title": "Divide and Conquer Paradigm",
        "topicName": "Divide & Conquer",
        "sectionId": "computational-thinking",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [29],
        "concepts": ["Divide, Conquer, Combine", "Subproblem Independence", "Binary Search on Arrays", "Merge Sort Preview"],
        "practiceSkills": ["Problem Partitioning", "Subproblem Recombination", "Recursive Conquering"],
        "steps": [
            make_explanation_step(
                "day30-step1", 1, "The Three Pillars of Divide & Conquer", "Divide & Conquer",
                "Divide, Conquer, Combine: The Blueprint for Efficient Algorithms",
                "A structured approach to transforming intractable problems into logarithmic layers.",
                [
                    "The **Divide-and-Conquer** paradigm operates in three distinct phases:",
                    "1. **Divide**: Partition the problem into smaller, independent subproblems of the same type.",
                    "2. **Conquer**: Recursively solve each subproblem. When subproblems become small enough (base cases), solve them directly.",
                    "3. **Combine**: Merge the subproblem solutions into a solution for the original problem.",
                    "For Divide-and-Conquer to be optimal, subproblems must be **independent** (non-overlapping). If subproblems overlap, Dynamic Programming is preferred to avoid redundant recomputations."
                ],
                snippets=[{
                    "title": "Divide and Conquer Template",
                    "code": "def divide_and_conquer(problem):\n    if is_base_case(problem):\n        return solve_directly(problem)\n    \n    subproblems = divide(problem)\n    sub_solutions = [divide_and_conquer(sub) for sub in subproblems]\n    return combine(sub_solutions)",
                    "language": "python",
                    "caption": "Canonical Divide-and-Conquer architecture."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Subproblem Independence",
                    "content": "Merge Sort and Binary Search are classic Divide-and-Conquer because left and right halves are completely independent."
                }],
                takeaway="Divide into independent subproblems, conquer recursively, and combine solutions."
            ),
            make_explanation_step(
                "day30-step2", 2, "Fast Exponentiation (Binary Exponentiation)", "Binary Exponentiation",
                "Computing x^N in O(log N) Time Instead of O(N)",
                "How divide-and-conquer slashes exponential loops to logarithmic time.",
                [
                    "Calculating $x^N$ by multiplying $x$ by itself $N$ times takes $O(N)$ operations.",
                    "By Divide-and-Conquer (Binary Exponentiation):",
                    "- If $N$ is even: $x^N = (x^{N/2})^2$",
                    "- If $N$ is odd: $x^N = x \\cdot (x^{(N-1)/2})^2$",
                    "At each step, the exponent $N$ is halved. Total multiplications drop from $N$ to **$O(\\log N)$**!",
                    "This pattern is fundamental in cryptography (RSA modular exponentiation) and matrix exponentiation."
                ],
                snippets=[{
                    "title": "Fast Exponentiation Implementation",
                    "code": "def fast_pow(x, n):\n    if n == 0:\n        return 1\n    half = fast_pow(x, n // 2)\n    if n % 2 == 0:\n        return half * half\n    else:\n        return x * half * half\n\nprint(fast_pow(2, 10)) # 1024 in only 4 recursive steps!",
                    "language": "python",
                    "caption": "Logarithmic power computation via binary halving."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Avoid Double Calls",
                    "content": "Writing `fast_pow(x, n//2) * fast_pow(x, n//2)` calls the subproblem TWICE, destroying the $O(\\log N)$ speed and reverting to $O(N)$! Always store `half = fast_pow(...)` in a variable."
                }],
                takeaway="Binary exponentiation computes x^N in O(log N) time by squaring subproblem halves."
            ),
            make_checkpoint_step(
                "day30-step3", 3, "Divide and Conquer Checkpoint", "Checkpoint",
                "Test Your Mastery of Divide and Conquer",
                "Evaluate subproblem independence and binary halving.",
                [
                    {
                        "id": "chk-d30-q1",
                        "question": "Why is naive recursive Fibonacci `fib(n) = fib(n-1) + fib(n-2)` NOT an efficient Divide-and-Conquer algorithm?",
                        "options": [
                            {"id": "A", "label": "It does not have a base case"},
                            {"id": "B", "label": "The subproblems overlap heavily, recomputing identical values exponentially (O(2^N))"},
                            {"id": "C", "label": "It divides by 2 instead of 3"},
                            {"id": "D", "label": "Fibonacci numbers cannot be computed recursively"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: fib(0) and fib(1) are base cases.",
                            "B": "Correct! Divide-and-conquer requires independent subproblems. fib(n-1) and fib(n-2) overlap extensively, making memoization (DP) necessary.",
                            "C": "Incorrect: It subtracts 1 and 2.",
                            "D": "Incorrect: It can be computed recursively with memoization."
                        }
                    },
                    {
                        "id": "chk-d30-q2",
                        "question": "How many multiplications does `fast_pow(x, 1024)` perform?",
                        "options": [
                            {"id": "A", "label": "1024"},
                            {"id": "B", "label": "10"},
                            {"id": "C", "label": "512"},
                            {"id": "D", "label": "2"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: That is the naive linear loop.",
                            "B": "Correct! log2(1024) = 10. The exponent halves at each step: 1024 -> 512 -> 256 -> 128 -> 64 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1, taking 10 steps.",
                            "C": "Incorrect: Halving occurs recursively at all levels.",
                            "D": "Incorrect: 2^10 = 1024."
                        }
                    }
                ],
                takeaway="Divide and Conquer requires independent subproblems; binary exponentiation takes log2(N) steps."
            ),
            make_practice_step(
                "day30-step4", 4, "Build Modular Fast Exponentiation", "Practice",
                "Implement Modular Fast Exponentiation (pow_mod)",
                "Compute (base^exp) % mod in O(log exp) time.",
                "Modular Exponentiation Engine",
                [
                    "Write `mod_pow(base, exp, mod)` using divide-and-conquer.",
                    "If `exp == 0`, return `1 % mod`.",
                    "Compute `half = mod_pow(base, exp // 2, mod)`.",
                    "If `exp % 2 == 0`, return `(half * half) % mod`; else `(base * half * half) % mod`.",
                    "Test with `base = 3, exp = 13, mod = 7` and print `'Result:', result`."
                ],
                """# Day 30 Practice: Modular Exponentiation Engine

def mod_pow(base, exp, mod):
    # TODO: Implement fast modular exponentiation
    if exp == 0:
        return 1 % mod
    half = mod_pow(base, exp // 2, mod)
    if exp % 2 == 0:
        return (half * half) % mod
    else:
        return (base * half * half) % mod

result = mod_pow(3, 13, 7)
print("Result:", result)
""",
                """def mod_pow(base, exp, mod):
    if exp == 0:
        return 1 % mod
    half = mod_pow(base, exp // 2, mod)
    if exp % 2 == 0:
        return (half * half) % mod
    else:
        return (base * half * half) % mod

result = mod_pow(3, 13, 7)
print("Result:", result)
""",
                ["Result: 3"],
                "3^13 % 7: 3^1=3, 3^2=2, 3^3=6, 3^6=1, 3^12=1, 3^13=3.",
                takeaway="Modular exponentiation applies modulo at each halving step, preventing massive integer bit growth."
            ),
            make_completion_step(
                "day30-step5", 5, "Divide and Conquer Mastery", "Recap",
                30, "Day 30 Complete: Divide and Conquer Paradigm",
                "You have mastered divide-and-conquer decomposition, binary exponentiation, and subproblem independence.",
                [
                    {
                        "concept": "Recursive Call Storage",
                        "naiveIntuition": "Calling f(n//2) * f(n//2) is the same as half * half",
                        "pythonReality": "Calling f(n//2) twice creates two recursive branches, degrading O(log N) back to O(N)"
                    },
                    {
                        "concept": "Overlapping Subproblems",
                        "naiveIntuition": "All recursive problems are Divide and Conquer",
                        "pythonReality": "Only problems with independent subproblems qualify; overlapping ones require DP"
                    }
                ],
                ["Divide, Conquer, Combine Framework", "Subproblem Independence Invariant", "Binary Exponentiation O(log N)", "Modular Reduction in Recursion"],
                get_next_preview(30)
            )
        ]
    }

    return days
