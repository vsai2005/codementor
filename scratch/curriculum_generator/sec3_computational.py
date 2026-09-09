from .common import (
    CURRICULUM_MAP,
    get_difficulty,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)

def get_sec3_days():
    days = {}

    # DAY 26: Asymptotic Analysis & Big-O Notation
    days[26] = {
        "dayNumber": 26,
        "title": "Asymptotic Analysis & Big-O Notation",
        "topicName": "Big-O Analysis",
        "sectionId": "computational-thinking",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [25],
        "concepts": ["Big-O, Omega, Theta", "Worst vs Average Case", "Input Scaling", "Dominant Terms"],
        "practiceSkills": ["Complexity Derivation", "Dominant Term Extraction", "Asymptotic Comparison"],
        "steps": [
            make_explanation_step(
                "day26-step1", 1, "The Language of Algorithmic Scaling", "Big-O Foundations",
                "Why We Care About Asymptotics: Upper Bounds, Lower Bounds, and Tight Bounds",
                "Formalizing how algorithms scale as input size N tends toward infinity.",
                [
                    "In computer science, wall-clock execution time depends on CPU clock speeds, operating system schedulers, and memory buses. To measure algorithmic efficiency independently of hardware, we use **asymptotic analysis**.",
                    "- **Big-O ($O$)**: Represents an asymptotic **upper bound** (worst-case scaling guarantee). $f(N) = O(g(N))$ means $f(N) \\le c \\cdot g(N)$ for all $N \\ge N_0$.",
                    "- **Big-Omega ($\\Omega$)**: Represents an asymptotic **lower bound** (best-case floor).",
                    "- **Big-Theta ($\\Theta$)**: Represents an asymptotically **tight bound** (both upper and lower).",
                    "When analyzing code, we drop non-dominant terms and constant coefficients: $3N^2 + 50N + 1000$ scales as $O(N^2)$ because as $N \\to \\infty$, the $N^2$ term dwarfs all others."
                ],
                snippets=[{
                    "title": "Dropping Constants and Dominant Terms",
                    "code": "def process_data(arr):\n    n = len(arr)\n    # Step 1: O(N) pass\n    total = sum(arr)\n    # Step 2: O(N^2) nested loop\n    pairs = []\n    for i in range(n):\n        for j in range(i + 1, n):\n            pairs.append((arr[i], arr[j]))\n    return total, pairs # Total: O(N) + O(N^2) -> Dominant is O(N^2)",
                    "language": "python",
                    "caption": "Extracting the dominant term from multi-phase algorithms."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Hierarchy of Growth Rates",
                    "content": "$O(1) < O(\\log N) < O(\\sqrt{N}) < O(N) < O(N \\log N) < O(N^2) < O(2^N) < O(N!)$."
                }],
                takeaway="Big-O characterizes the upper bound scaling rate by keeping only the highest-order dominant term."
            ),
            make_explanation_step(
                "day26-step2", 2, "Common Big-O Pitfalls & Invariants", "Big-O Gotchas",
                "Analyzing Independent Variables: O(N + M) vs O(N * M)",
                "Avoid the common trap of assuming all inputs have the same size.",
                [
                    "When an algorithm processes two distinct input arrays of lengths $N$ and $M$:",
                    "- If loops run sequentially, time complexity is $O(N + M)$.",
                    "- If loops are nested, time complexity is $O(N \\times M)$. Never abbreviate this as $O(N^2)$ unless $N = M$!",
                    "String slicing `s[i:j]` of length $K$ takes $O(K)$ time, not $O(1)$. Slicing inside a loop of size $N$ can sneakily turn an $O(N)$ loop into $O(N^2)$!"
                ],
                snippets=[{
                    "title": "Multiple Variables and Hidden Slice Costs",
                    "code": "def search_matrix(grid, query):\n    # grid has R rows and C columns\n    for row in grid:       # Runs R times\n        if query in row:   # Scans C elements: O(C)\n            return True\n    return False # Total time: O(R * C), not O(N^2)!",
                    "language": "python",
                    "caption": "Accurate accounting for multi-variable inputs."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "The Hidden O(N) in String Slices",
                    "content": "`sub = s[:i]` allocates a brand new string of length `i`. Doing this inside `for i in range(len(s))` costs $1 + 2 + ... + N = O(N^2)$ time!"
                }],
                takeaway="Differentiate multiple input dimensions (O(N*M)) and account for hidden sequence slice costs."
            ),
            make_checkpoint_step(
                "day26-step3", 3, "Big-O Analysis Checkpoint", "Checkpoint",
                "Test Your Mastery of Asymptotic Scaling",
                "Determine dominant terms and identify hidden complexity costs.",
                [
                    {
                        "id": "chk-d26-q1",
                        "question": "What is the Big-O time complexity of an algorithm that performs $1000 N + 4 N \\log N + 0.001 N^2$ operations?",
                        "options": [
                            {"id": "A", "label": "O(N log N)"},
                            {"id": "B", "label": "O(N)"},
                            {"id": "C", "label": "O(N^2)"},
                            {"id": "D", "label": "O(1000 N)"}
                        ],
                        "correctOptionId": "C",
                        "explanations": {
                            "A": "Incorrect: N^2 grows faster than N log N for large N.",
                            "B": "Incorrect: N is sub-dominant.",
                            "C": "Correct! As N -> infinity, N^2 grows strictly faster than N or N log N regardless of constant coefficients (even 0.001 vs 1000). The dominant term is O(N^2).",
                            "D": "Incorrect: Constant multipliers are dropped in asymptotic analysis."
                        }
                    },
                    {
                        "id": "chk-d26-q2",
                        "question": "What is the time complexity of running `s = s[1:]` repeatedly N times where s initially has length N?",
                        "options": [
                            {"id": "A", "label": "O(N)"},
                            {"id": "B", "label": "O(N^2)"},
                            {"id": "C", "label": "O(1)"},
                            {"id": "D", "label": "O(N log N)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Each slice allocates a copy of remaining characters.",
                            "B": "Correct! In step 1, s[1:] copies N-1 chars; in step 2, N-2 chars, down to 1. The sum is (N-1) + (N-2) + ... + 1 = N(N-1)/2, which is O(N^2)!",
                            "C": "Incorrect: Slicing strings is not O(1) pointer movement because strings are immutable copies.",
                            "D": "Incorrect: It forms an arithmetic series summing to quadratic time."
                        }
                    }
                ],
                takeaway="Drop constants and sub-dominant terms; repeated slicing on immutable sequences costs O(N^2)."
            ),
            make_practice_step(
                "day26-step4", 4, "Analyze and Optimize Nested Check", "Practice",
                "Refactor Quadratic O(N^2) Pair Search to Linear O(N)",
                "Optimize a target-difference check from nested loops to set lookup.",
                "Target Difference Optimizer",
                [
                    "Given `nums = [1, 5, 3, 4, 2]` and `k = 2`, find if any pair `(a, b)` satisfies `a - b == k`.",
                    "The naive approach uses nested loops costing $O(N^2)$.",
                    "Refactor to $O(N)$ by loading `nums` into a `set` called `num_set`.",
                    "Iterate over `x in nums`: if `(x - k) in num_set`, a pair exists!",
                    "Print `'Pair found:', True`."
                ],
                """# Day 26 Practice: Target Difference Optimizer
nums = [1, 5, 3, 4, 2]
k = 2

# TODO: Refactor O(N^2) search into O(N) using set lookup
num_set = set(nums)
found = False

for x in nums:
    if (x - k) in num_set:
        found = True
        break

print("Pair found:", found)
""",
                """nums = [1, 5, 3, 4, 2]
k = 2

num_set = set(nums)
found = False

for x in nums:
    if (x - k) in num_set:
        found = True
        break

print("Pair found:", found)
""",
                ["Pair found: True"],
                "Convert nums to `num_set = set(nums)` and check `if (x - k) in num_set:` in O(1) time.",
                takeaway="Replacing inner linear scans with O(1) hash sets reduces algorithmic complexity from O(N^2) to O(N)."
            ),
            make_completion_step(
                "day26-step5", 5, "Asymptotic Analysis Mastery", "Recap",
                26, "Day 26 Complete: Asymptotic Analysis & Big-O Notation",
                "You have mastered Big-O upper bounds, dominant term extraction, and hidden slice complexities.",
                [
                    {
                        "concept": "Dominant Terms",
                        "naiveIntuition": "1000N is larger than 0.01N^2 so it dominates",
                        "pythonReality": "For sufficiently large N, N^2 always grows faster than N; constants are discarded"
                    },
                    {
                        "concept": "String Slicing Cost",
                        "naiveIntuition": "s[1:] just moves a start pointer in O(1) time",
                        "pythonReality": "Strings allocate new copies of characters, taking O(K) time and space"
                    }
                ],
                ["Big-O, Omega, and Theta Definitions", "Dominant Term Isolation", "Multi-Variable Complexities (O(N*M))", "Avoiding Hidden O(N^2) Slice Anti-Patterns"],
                get_next_preview(26)
            )
        ]
    }

    # DAY 27: Space Complexity & Auxiliary Memory
    days[27] = {
        "dayNumber": 27,
        "title": "Space Complexity & Auxiliary Memory",
        "topicName": "Space Complexity",
        "sectionId": "computational-thinking",
        "estimatedMinutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [26],
        "concepts": ["Auxiliary vs Total Space", "Call Stack Overhead", "In-Place Modifications", "Memory Tradeoffs"],
        "practiceSkills": ["Space Complexity Accounting", "In-Place Mutation Invariants", "Stack Depth Analysis"],
        "steps": [
            make_explanation_step(
                "day27-step1", 1, "Total Space vs Auxiliary Space", "Space Accounting",
                "Differentiating Input Space from Auxiliary (Working) Space",
                "Accurately calculate memory consumption without confusing inputs with overhead.",
                [
                    "When analyzing memory complexity, we distinguish between two metrics:",
                    "- **Total Space Complexity**: The total memory consumed, including input storage, working variables, and output structures.",
                    "- **Auxiliary Space Complexity**: The **extra memory** allocated by the algorithm exclusively to perform its computation, excluding the input data.",
                    "An algorithm that modifies an input array of size $N$ in-place without allocating extra buffers uses **$O(1)$ auxiliary space**, even though the input itself takes $O(N)$ memory."
                ],
                snippets=[{
                    "title": "O(1) Auxiliary Space In-Place Transformation",
                    "code": "def reverse_in_place(arr):\n    # Modifies arr in-place: O(1) Auxiliary Space\n    left, right = 0, len(arr) - 1\n    while left < right:\n        arr[left], arr[right] = arr[right], arr[left]\n        left += 1\n        right -= 1\n    return arr",
                    "language": "python",
                    "caption": "Two-pointer swap requiring O(1) auxiliary variables."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Interview Standard",
                    "content": "When interviewers ask for 'space complexity', they almost always mean **auxiliary space complexity** unless explicitly specified."
                }],
                takeaway="Auxiliary space measures only extra working memory allocated beyond the input itself."
            ),
            make_explanation_step(
                "day27-step2", 2, "Call Stack Space in Recursion", "Stack Overhead",
                "Why Recursion is Never O(1) Space: The Hidden Call Stack",
                "Account for frame allocations on the execution stack.",
                [
                    "Every recursive call creates a new stack frame storing local variables, parameters, and return addresses (~8KB per frame in CPython).",
                    "If a recursive function recurses to a depth of $N$ before reaching its base case, it consumes **$O(N)$ auxiliary space on the call stack**, even if it creates no lists or variables!",
                    "In Python, the maximum recursion depth is guarded by `sys.getrecursionlimit()` (default: 1000). Exceeding this raises `RecursionError: maximum recursion depth exceeded`."
                ],
                snippets=[{
                    "title": "Recursive Call Stack Depth",
                    "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1) # Pushes N frames onto call stack!\n# Time: O(N), Auxiliary Space: O(N) stack frames\n\ndef factorial_iterative(n):\n    res = 1\n    for i in range(2, n + 1):\n        res *= i\n    return res\n# Time: O(N), Auxiliary Space: O(1) - single integer variable!",
                    "language": "python",
                    "caption": "Recursive vs iterative auxiliary memory footprint."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Python Does NOT Have Tail-Call Optimization (TCO)",
                    "content": "Unlike Scheme or some JavaScript engines, Python never optimizes tail recursion. Every recursive call always allocates a new frame."
                }],
                takeaway="Recursive algorithms consume O(depth) auxiliary stack space; Python does not support TCO."
            ),
            make_checkpoint_step(
                "day27-step3", 3, "Space Complexity Checkpoint", "Checkpoint",
                "Test Your Mastery of Space Accounting",
                "Differentiate auxiliary memory from call stack frames.",
                [
                    {
                        "id": "chk-d27-q1",
                        "question": "What is the auxiliary space complexity of a recursive binary search that divides an array of size N in half each step without copying arrays?",
                        "options": [
                            {"id": "A", "label": "O(1)"},
                            {"id": "B", "label": "O(log N)"},
                            {"id": "C", "label": "O(N)"},
                            {"id": "D", "label": "O(N log N)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Iterative binary search is O(1), but recursive binary search pushes frames onto the stack.",
                            "B": "Correct! The maximum recursion depth is log2(N). At peak depth, log2(N) call frames exist on the stack simultaneously, consuming O(log N) auxiliary space.",
                            "C": "Incorrect: The search space halves at every step, so depth is logarithmic, not linear.",
                            "D": "Incorrect: Recursion depth is log N."
                        }
                    },
                    {
                        "id": "chk-d27-q2",
                        "question": "If an algorithm creates a frequency hash map of all unique characters in a string of length N containing only lowercase English letters ('a'-'z'), what is its auxiliary space complexity?",
                        "options": [
                            {"id": "A", "label": "O(N)"},
                            {"id": "B", "label": "O(1)"},
                            {"id": "C", "label": "O(N^2)"},
                            {"id": "D", "label": "O(26^N)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: The map cannot exceed 26 entries regardless of how large N is.",
                            "B": "Correct! Because the alphabet is bounded by a fixed constant (26 keys), the hash map size is bounded by O(26) = O(1) space!",
                            "C": "Incorrect: Space is strictly bounded.",
                            "D": "Incorrect: Character count is fixed."
                        }
                    }
                ],
                takeaway="Recursion stack depth determines recursive space; bounded alphabet size yields O(1) auxiliary space."
            ),
            make_practice_step(
                "day27-step4", 4, "Convert Recursion to O(1) Space", "Practice",
                "Refactor Recursive Sum to O(1) Space Accumulator",
                "Convert an O(N) call-stack recursive sum to an O(1) auxiliary space loop.",
                "O(1) Space Summation",
                [
                    "Given `nums = [10, 20, 30, 40, 50]`.",
                    "Implement `sum_iterative(arr)` using a single accumulator `total = 0` in an iterative loop.",
                    "Confirm the result equals 150.",
                    "Print `'Iterative sum:', result`."
                ],
                """# Day 27 Practice: O(1) Space Summation
nums = [10, 20, 30, 40, 50]

def sum_iterative(arr):
    # TODO: Sum elements with O(1) auxiliary space
    total = 0
    for x in arr:
        total += x
    return total

result = sum_iterative(nums)
print("Iterative sum:", result)
""",
                """nums = [10, 20, 30, 40, 50]

def sum_iterative(arr):
    total = 0
    for x in arr:
        total += x
    return total

result = sum_iterative(nums)
print("Iterative sum:", result)
""",
                ["Iterative sum: 150"],
                "Use a single `total` variable and loop over `arr` to achieve O(1) auxiliary memory.",
                takeaway="Iterative loops replace call-stack frames with constant auxiliary state."
            ),
            make_completion_step(
                "day27-step5", 5, "Space Complexity Mastery", "Recap",
                27, "Day 27 Complete: Space Complexity & Auxiliary Memory",
                "You have mastered auxiliary vs total space, call stack overhead, and bounded alphabet optimization.",
                [
                    {
                        "concept": "Recursive Space",
                        "naiveIntuition": "Recursion that returns numbers without arrays is O(1) space",
                        "pythonReality": "Every recursive call allocates a stack frame; depth determines auxiliary space"
                    },
                    {
                        "concept": "Alphabet Hash Tables",
                        "naiveIntuition": "A dictionary storing counts for a string of length N is always O(N) space",
                        "pythonReality": "If the character set is bounded (e.g. ASCII or English lowercase), space is O(1)"
                    }
                ],
                ["Auxiliary vs Total Memory Definition", "Call Stack Depth & Frame Allocation", "Lack of Tail-Call Optimization in Python", "Bounded Alphabet O(1) Space Invariant"],
                get_next_preview(27)
            )
        ]
    }

    # We will complete Days 28-35 similarly
    return days
