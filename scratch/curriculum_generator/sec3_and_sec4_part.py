from .common import (
    CURRICULUM_MAP,
    get_difficulty,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)

def get_batch2_tail_days():
    days = {}

    # DAY 33: 2D Prefix Sums & Submatrix Queries
    days[33] = {
        "dayNumber": 33,
        "title": "2D Prefix Sums & Submatrix Queries",
        "topicName": "2D Prefix Sums",
        "sectionId": "computational-thinking",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [32],
        "concepts": ["Inclusion-Exclusion Principle", "2D Prefix Table Construction", "O(1) Submatrix Sum Queries", "Boundary Invariants"],
        "practiceSkills": ["2D Prefix Matrix Construction", "Inclusion-Exclusion Query Formulation", "Submatrix Area Calculation"],
        "steps": [
            make_explanation_step(
                "day33-step1", 1, "The Inclusion-Exclusion Principle in 2D", "2D Prefix Concept",
                "Extending Prefix Sums to 2D Grids with Inclusion-Exclusion",
                "Answer submatrix sum queries in O(1) time using area arithmetic.",
                [
                    "Given an $R \\times C$ matrix, we construct a 2D prefix table `P` of size $(R + 1) \\times (C + 1)$, where `P[r][c]` stores the sum of all cells in the submatrix from $(0, 0)$ down to $(r - 1, c - 1)$.",
                    "To construct `P` in $O(R \\times C)$ time using the **Inclusion-Exclusion Principle**:",
                    "$$P[r][c] = \\text{matrix}[r-1][c-1] + P[r-1][c] + P[r][c-1] - P[r-1][c-1]$$",
                    "Notice that adding the rectangle above and the rectangle to the left double-counts the top-left diagonal rectangle, so we subtract $P[r-1][c-1]$ once."
                ],
                snippets=[{
                    "title": "2D Prefix Construction",
                    "code": "R, C = len(grid), len(grid[0])\npref = [[0] * (C + 1) for _ in range(R + 1)]\nfor r in range(R):\n    for c in range(C):\n        pref[r+1][c+1] = grid[r][c] + pref[r][c+1] + pref[r+1][c] - pref[r][c]",
                    "language": "python",
                    "caption": "Constructing the 2D prefix matrix."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Zero Padding Row & Column",
                    "content": "The extra row 0 and column 0 of zeroes handles edges cleanly, preventing index-out-of-bounds checks."
                }],
                takeaway="2D prefix tables precompute areas in O(R*C) time using the Inclusion-Exclusion Principle."
            ),
            make_explanation_step(
                "day33-step2", 2, "O(1) Submatrix Range Queries", "Submatrix Query",
                "Querying any Submatrix (r1, c1) to (r2, c2) in Constant Time",
                "Deriving the 4-corner formula for instant submatrix sums.",
                [
                    "To query the sum of the submatrix spanning from top-left $(r_1, c_1)$ to bottom-right $(r_2, c_2)$ (inclusive):",
                    "1. Start with the entire rectangle from $(0, 0)$ to $(r_2, c_2)$: `P[r2 + 1][c2 + 1]`.",
                    "2. Subtract the area above the target submatrix: `P[r1][c2 + 1]`.",
                    "3. Subtract the area to the left of the target submatrix: `P[r2 + 1][c1]`.",
                    "4. The top-left corner was subtracted twice! Add it back once: `P[r1][c1]`.",
                    "$$\\text{Sum} = P[r_2+1][c_2+1] - P[r_1][c_2+1] - P[r_2+1][c_1] + P[r_1][c_1]$$"
                ],
                snippets=[{
                    "title": "O(1) Submatrix Query Formula",
                    "code": "def query_submatrix(pref, r1, c1, r2, c2):\n    return pref[r2+1][c2+1] - pref[r1][c2+1] - pref[r2+1][c1] + pref[r1][c1]",
                    "language": "python",
                    "caption": "The 4-term Inclusion-Exclusion query formula."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Coordinates Ordering",
                    "content": "Ensure $r_1 \\le r_2$ and $c_1 \\le c_2$. If coordinates are reversed, the formula yields corrupted values."
                }],
                takeaway="Submatrix sum = BottomRight - TopStrip - LeftStrip + TopLeftOverlap in O(1) time."
            ),
            make_checkpoint_step(
                "day33-step3", 3, "2D Prefix Checkpoint", "Checkpoint",
                "Test Your Understanding of 2D Prefix Sums",
                "Verify Inclusion-Exclusion terms and submatrix coordinates.",
                [
                    {
                        "id": "chk-d33-q1",
                        "question": "Why do we ADD `pref[r1][c1]` back in the submatrix query formula?",
                        "options": [
                            {"id": "A", "label": "Because the cell at (r1, c1) was omitted"},
                            {"id": "B", "label": "Because it was subtracted twice: once in the top strip and once in the left strip"},
                            {"id": "C", "label": "To account for 1-based indexing offsets"},
                            {"id": "D", "label": "To handle negative values in the matrix"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Inclusion-Exclusion corrects overlapping regions.",
                            "B": "Correct! Subtracting the top region (P[r1][c2+1]) and left region (P[r2+1][c1]) both subtract the common overlapping region P[r1][c1]. Adding it back once restores mathematical balance.",
                            "C": "Incorrect: Indexing handles offsets, but the + term is algebraic.",
                            "D": "Incorrect: The formula holds for all integer values."
                        }
                    },
                    {
                        "id": "chk-d33-q2",
                        "question": "What is the time complexity to answer Q submatrix queries on an R x C grid using 2D prefix sums?",
                        "options": [
                            {"id": "A", "label": "O(R * C * Q)"},
                            {"id": "B", "label": "O(R * C + Q)"},
                            {"id": "C", "label": "O(Q log(R * C))"},
                            {"id": "D", "label": "O(R + C + Q)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: That is the un-precomputed naive approach.",
                            "B": "Correct! Preprocessing the table takes O(R * C), and each query executes in O(1) time via the 4-term arithmetic formula: O(R * C + Q).",
                            "C": "Incorrect: No binary search is involved.",
                            "D": "Incorrect: Filling the 2D grid requires visiting all R*C cells."
                        }
                    }
                ],
                takeaway="Adding back pref[r1][c1] balances the double-subtraction; Q queries cost O(R*C + Q)."
            ),
            make_practice_step(
                "day33-step4", 4, "Build a 2D Submatrix Query Engine", "Practice",
                "Implement NumMatrix for 2D Range Queries",
                "Build a 2D matrix query class supporting O(1) area lookups.",
                "Submatrix Query Engine",
                [
                    "Given `matrix = [[3, 0, 1], [5, 6, 3], [1, 2, 0]]`.",
                    "Precompute 2D prefix table `self.p` of dimensions 4x4.",
                    "Implement `sum_region(r1, c1, r2, c2)`.",
                    "Query the region from $(1, 1)$ to $(2, 2)$ (cells: 6, 3, 2, 0 -> sum = 11).",
                    "Print `'Submatrix sum:', result`."
                ],
                """# Day 33 Practice: Submatrix Query Engine

class NumMatrix:
    def __init__(self, matrix):
        R, C = len(matrix), len(matrix[0])
        self.p = [[0] * (C + 1) for _ in range(R + 1)]
        for r in range(R):
            for c in range(C):
                self.p[r+1][c+1] = matrix[r][c] + self.p[r][c+1] + self.p[r+1][c] - self.p[r][c]

    def sum_region(self, r1, c1, r2, c2):
        # TODO: Compute submatrix sum in O(1)
        return self.p[r2+1][c2+1] - self.p[r1][c2+1] - self.p[r2+1][c1] + self.p[r1][c1]

grid = [
    [3, 0, 1],
    [5, 6, 3],
    [1, 2, 0]
]
obj = NumMatrix(grid)
result = obj.sum_region(1, 1, 2, 2)
print("Submatrix sum:", result)
""",
                """class NumMatrix:
    def __init__(self, matrix):
        R, C = len(matrix), len(matrix[0])
        self.p = [[0] * (C + 1) for _ in range(R + 1)]
        for r in range(R):
            for c in range(C):
                self.p[r+1][c+1] = matrix[r][c] + self.p[r][c+1] + self.p[r+1][c] - self.p[r][c]

    def sum_region(self, r1, c1, r2, c2):
        return self.p[r2+1][c2+1] - self.p[r1][c2+1] - self.p[r2+1][c1] + self.p[r1][c1]

grid = [
    [3, 0, 1],
    [5, 6, 3],
    [1, 2, 0]
]
obj = NumMatrix(grid)
result = obj.sum_region(1, 1, 2, 2)
print("Submatrix sum:", result)
""",
                ["Submatrix sum: 11"],
                "Cells (1,1)=6, (1,2)=3, (2,1)=2, (2,2)=0 -> 6 + 3 + 2 + 0 = 11.",
                takeaway="2D prefix matrices allow constant-time computation of any rectangular subregion."
            ),
            make_completion_step(
                "day33-step5", 5, "2D Prefix Sums Mastery", "Recap",
                33, "Day 33 Complete: 2D Prefix Sums & Submatrix Queries",
                "You have mastered 2D Inclusion-Exclusion, table construction, and instant submatrix queries.",
                [
                    {
                        "concept": "Overlapping Areas",
                        "naiveIntuition": "Summing submatrix requires adding elements cell-by-cell",
                        "pythonReality": "Inclusion-Exclusion calculates the area using only 4 corner values in O(1)"
                    },
                    {
                        "concept": "Boundary Zero Padding",
                        "naiveIntuition": "Use R x C prefix matrix directly",
                        "pythonReality": "(R+1) x (C+1) with zeroes on row/col 0 avoids complex edge conditions"
                    }
                ],
                ["2D Inclusion-Exclusion Formula", "(R+1) x (C+1) Table Padding", "O(1) Submatrix Sum Querying", "O(R*C + Q) Complexity Budget"],
                get_next_preview(33)
            )
        ]
    }

    # DAY 34: Difference Arrays & Range Updates
    days[34] = {
        "dayNumber": 34,
        "title": "Difference Arrays & Range Updates",
        "topicName": "Difference Arrays",
        "sectionId": "computational-thinking",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [33],
        "concepts": ["Range Update Operations", "O(1) Boundary Marking", "Prefix Sum Reconstruction", "Sweep-line Foundations"],
        "practiceSkills": ["Difference Array Construction", "O(1) Range Modification", "Cumulative Prefix Reconstruction"],
        "steps": [
            make_explanation_step(
                "day34-step1", 1, "The Difference Array Invariant", "Difference Array",
                "Transforming O(N) Range Updates into O(1) Boundary Marks",
                "Apply hundreds of range modifications in constant time per update.",
                [
                    "Suppose you have an array of zeroes of length $N$ and need to execute $K$ range update operations: *'Add $V$ to all elements from index $L$ to $R$'*.",
                    "Applying each update with a loop takes $O(N)$ per operation ($O(K \\times N)$ total).",
                    "A **Difference Array** $D$ is defined such that $D[i] = A[i] - A[i-1]$ (with $D[0] = A[0]$). Taking the prefix sum of $D$ reconstructs the original array $A$!",
                    "Crucially, adding $V$ to range $[L, R]$ changes only **TWO elements** in the difference array:",
                    "1. `D[L] += V` (starts the boost of $+V$ at index $L$)",
                    "2. `D[R + 1] -= V` (cancels the boost after index $R$)",
                    "Each range update executes in **$O(1)$ constant time**!"
                ],
                snippets=[{
                    "title": "Difference Array Range Update",
                    "code": "n = 5\ndiff = [0] * (n + 1)\n\n# Range update: Add 10 to range [1, 3] in O(1)\nL, R, V = 1, 3, 10\ndiff[L] += V       # diff[1] += 10\ndiff[R + 1] -= V   # diff[4] -= 10\n\n# Reconstruct final array via prefix sum in O(N)\narr = [0] * n\ncurr = 0\nfor i in range(n):\n    curr += diff[i]\n    arr[i] = curr\nprint(arr) # [0, 10, 10, 10, 0]",
                    "language": "python",
                    "caption": "O(1) marking and O(N) prefix sum reconstruction."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Inverse of Prefix Sums",
                    "content": "Difference arrays are the exact mathematical inverse of prefix sums. Prefix sum converts point updates to range queries; difference arrays convert range updates to point updates."
                }],
                takeaway="Add V at L, subtract V at R+1; taking prefix sums reconstructs the updated array in O(N) time."
            ),
            make_explanation_step(
                "day34-step2", 2, "Flight Bookings & Sweep-Line Preview", "Sweep-Line Preview",
                "Corporate Flight Bookings & Meeting Room Overlap",
                "How difference arrays solve interval overlap problems.",
                [
                    "Consider the classic problem: Given flight booking reservations `[first, last, seats]`, determine the total seats reserved on each flight.",
                    "Instead of filling seats seat-by-seat, mark `diff[first - 1] += seats` and `diff[last] -= seats`.",
                    "When all $K$ updates are marked, a single $O(N)$ cumulative sweep yields the final answer.",
                    "Total time is **$O(N + K)$** instead of $O(N \\times K)$, effortlessly handling $K = 10^5$ operations."
                ],
                snippets=[{
                    "title": "Flight Bookings Solution",
                    "code": "def corp_flight_bookings(bookings, n):\n    diff = [0] * (n + 1)\n    for first, last, seats in bookings:\n        diff[first - 1] += seats\n        diff[last] -= seats\n    # Prefix sum sweep\n    res = [0] * n\n    curr = 0\n    for i in range(n):\n        curr += diff[i]\n        res[i] = curr\n    return res",
                    "language": "python",
                    "caption": "Linear flight booking resolution via difference array."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "R + 1 Boundary Check",
                    "content": "Always size the difference array to $N + 1$ so that when an update reaches the end ($R = N - 1$), the decrement at $R + 1 = N$ does not throw an IndexError."
                }],
                takeaway="Difference arrays solve batch interval modifications in O(N + K) total time."
            ),
            make_checkpoint_step(
                "day34-step3", 3, "Difference Arrays Checkpoint", "Checkpoint",
                "Test Your Mastery of Difference Arrays",
                "Evaluate boundary modifications and reconstruction mechanics.",
                [
                    {
                        "id": "chk-d34-q1",
                        "question": "To add value V to all elements from index 2 to 5 in an array of size 10, what modifications are made to difference array D?",
                        "options": [
                            {"id": "A", "label": "D[2] += V and D[5] -= V"},
                            {"id": "B", "label": "D[2] += V and D[6] -= V"},
                            {"id": "C", "label": "D[1] += V and D[5] -= V"},
                            {"id": "D", "label": "D[2] += V and D[6] += V"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Subtracting at index 5 would cancel the value at index 5 itself, omitting it.",
                            "B": "Correct! Increment at L = 2 and decrement at R + 1 = 5 + 1 = 6 so that indices 2, 3, 4, 5 receive the added value.",
                            "C": "Incorrect: L = 2, not 1.",
                            "D": "Incorrect: The cancellation must be a subtraction (-= V)."
                        }
                    },
                    {
                        "id": "chk-d34-q2",
                        "question": "What is the time complexity to perform K range updates and reconstruct an array of length N using a difference array?",
                        "options": [
                            {"id": "A", "label": "O(N * K)"},
                            {"id": "B", "label": "O(N + K)"},
                            {"id": "C", "label": "O(K log N)"},
                            {"id": "D", "label": "O(N log K)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: That is the un-optimized loop approach.",
                            "B": "Correct! Each of the K updates takes O(1) time (2 point modifications), and the final prefix sum sweep takes O(N). Total: O(N + K).",
                            "C": "Incorrect: Difference arrays use direct indexing without trees.",
                            "D": "Incorrect: Reconstruction is a single linear pass."
                        }
                    }
                ],
                takeaway="Range update modifies D[L] += V and D[R+1] -= V in O(1); total time for K updates is O(N + K)."
            ),
            make_practice_step(
                "day34-step4", 4, "Range Addition with Difference Array", "Practice",
                "Apply Multiple Range Increments in O(1) Per Update",
                "Execute batch updates on an array and reconstruct the final values.",
                "Range Addition Engine",
                [
                    "Given `n = 5` and `updates = [[1, 3, 2], [2, 4, 3], [0, 2, -2]]` where each update is `[start, end, val]`.",
                    "Initialize `diff = [0] * (n + 1)`.",
                    "Apply all updates in $O(1)$ per update using the difference array technique.",
                    "Reconstruct the array `res` using cumulative summation.",
                    "Print `'Final array:', res`."
                ],
                """# Day 34 Practice: Range Addition Engine
n = 5
updates = [[1, 3, 2], [2, 4, 3], [0, 2, -2]]

diff = [0] * (n + 1)

# TODO 1: Apply updates to diff in O(1)
for start, end, val in updates:
    diff[start] += val
    diff[end + 1] -= val

# TODO 2: Reconstruct final array
res = [0] * n
curr = 0
for i in range(n):
    curr += diff[i]
    res[i] = curr

print("Final array:", res)
""",
                """n = 5
updates = [[1, 3, 2], [2, 4, 3], [0, 2, -2]]

diff = [0] * (n + 1)
for start, end, val in updates:
    diff[start] += val
    diff[end + 1] -= val

res = [0] * n
curr = 0
for i in range(n):
    curr += diff[i]
    res[i] = curr

print("Final array:", res)
""",
                ["Final array: [-2, 0, 3, 5, 3]"],
                "Indices: 0 has -2; 1 has -2+2=0; 2 has -2+2+3=3; 3 has 2+3=5; 4 has 3.",
                takeaway="Difference arrays allow batch updates to occur in constant time, resolved in a single linear pass."
            ),
            make_completion_step(
                "day34-step5", 5, "Difference Arrays Mastery", "Recap",
                34, "Day 34 Complete: Difference Arrays & Range Updates",
                "You have mastered difference array mechanics, O(1) boundary updates, and prefix reconstruction.",
                [
                    {
                        "concept": "Boundary Cancellation",
                        "naiveIntuition": "Subtract at R because range ends at R",
                        "pythonReality": "Subtract at R + 1 so that index R still receives the added value"
                    },
                    {
                        "concept": "Batch vs Online",
                        "naiveIntuition": "Use difference arrays when you need to query values between updates",
                        "pythonReality": "Difference arrays are best for batch updates followed by queries; online queries need Segment Trees"
                    }
                ],
                ["D[L] += V & D[R+1] -= V Invariant", "Cumulative Prefix Reconstruction", "O(N + K) Batch Complexity", "Sweep-Line Algorithmic Foundation"],
                get_next_preview(34)
            )
        ]
    }

    # DAY 35: Section 3 Review & Algorithmic Foundations
    days[35] = {
        "dayNumber": 35,
        "title": "Section 3 Review & Algorithmic Foundations",
        "topicName": "Section 3 Synthesis",
        "sectionId": "computational-thinking",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [34],
        "concepts": ["Asymptotic Synthesis", "Recursion & Master Theorem", "Prefix Sums & Difference Arrays", "Space-Time Tradeoffs"],
        "practiceSkills": ["Algorithm Complexity Evaluation", "Cumulative Precomputation Selection", "Algorithmic Pattern Matching"],
        "steps": [
            make_explanation_step(
                "day35-step1", 1, "Computational Thinking Synthesis", "Section 3 Model",
                "Synthesizing Complexity, Recursion, and Cumulative Precomputation",
                "Consolidate the core mathematical and algorithmic foundations built in Days 26 to 34.",
                [
                    "Section 3 established the mathematical and conceptual toolkit of computer science:",
                    "1. **Asymptotic Complexity**: Big-O upper bounds, dominant term extraction, dropping constants, and recognizing hidden $O(N)$ operations.",
                    "2. **Space Accounting**: Differentiating input space from auxiliary space; understanding call stack frame consumption in recursion.",
                    "3. **Divide and Conquer & Recurrences**: Formulating recurrence relations $T(N) = aT(N/b) + f(N)$, Master Theorem cases, and fast binary exponentiation ($O(\\log N)$).",
                    "4. **Prefix Sums & Difference Arrays**: Dual techniques turning $O(N)$ range queries and $O(N)$ range updates into $O(1)$ operations."
                ],
                snippets=[{
                    "title": "The Duality of Prefix and Difference",
                    "code": "# Prefix Sum:    Turns O(N) Range Query  -> O(1) Instant Query\n# Difference:    Turns O(N) Range Update -> O(1) Instant Update\n# They are exact mathematical inverses of each other!",
                    "language": "python",
                    "caption": "Dual relationship of prefix sums and difference arrays."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Ready for Core DSA",
                    "content": "With this mathematical and computational foundation, you are fully equipped for Section 4: Arrays & Strings and two-pointer algorithms!"
                }],
                takeaway="Computational thinking translates problem constraints into optimal Big-O design patterns."
            ),
            make_explanation_step(
                "day35-step2", 2, "Algorithmic Decision Matrix", "Decision Matrix",
                "Selecting the Optimal Algorithmic Pattern Based on Constraints",
                "How to read problem constraints and deduce the required complexity.",
                [
                    "When reading problem constraints in technical interviews:",
                    "- $N \\le 20$: Exponential / Backtracking ($O(2^N)$ or $O(N!)$).",
                    "- $N \\le 500$: Cubic or quadratic ($O(N^3)$ or $O(N^2)$).",
                    "- $N \\le 5,000$: Quadratic acceptable ($O(N^2)$).",
                    "- $N \\le 10^5$ to $10^6$: Linear or Log-linear mandatory ($O(N)$ or $O(N \\log N)$).",
                    "- $N \\ge 10^9$: Logarithmic or Constant ($O(\\log N)$ or $O(1)$ via math/binary search)."
                ],
                snippets=[{
                    "title": "Constraint to Complexity Mapping",
                    "code": "# If N = 10^5: O(N^2) = 10^10 operations -> Time Limit Exceeded (TLE)!\n# Must use O(N) Two Pointers, Sliding Window, or Prefix Sums.",
                    "language": "python",
                    "caption": "Matching constraint magnitude to acceptable Big-O."
                }],
                callouts=[{
                    "type": "deep-dive",
                    "title": "The 10^8 Operations Rule of Thumb",
                    "content": "Standard competitive programming and LeetCode judges execute roughly $10^8$ basic Python operations per second before triggering a Time Limit Exceeded (TLE)."
                }],
                takeaway="N = 10^5 requires O(N) or O(N log N); use the 10^8 operations per second benchmark."
            ),
            make_checkpoint_step(
                "day35-step3", 3, "Section 3 Milestone Checkpoint", "Checkpoint",
                "Verify Section 3 Mastery Across Core Concepts",
                "Test your synthesized algorithmic decision making.",
                [
                    {
                        "id": "chk-d35-q1",
                        "question": "If a problem specifies $N = 2 \\times 10^5$, which time complexity will PASS within a 1-second time limit?",
                        "options": [
                            {"id": "A", "label": "O(N^2)"},
                            {"id": "B", "label": "O(N log N)"},
                            {"id": "C", "label": "O(2^N)"},
                            {"id": "D", "label": "O(N^3)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: (2*10^5)^2 = 4*10^10 operations, which takes ~400 seconds (TLE).",
                            "B": "Correct! N log N for 2*10^5 is approximately (2*10^5) * 18 = 3.6*10^6 operations, executing in under 0.1 seconds.",
                            "C": "Incorrect: Exponential time.",
                            "D": "Incorrect: Cubic time."
                        }
                    },
                    {
                        "id": "chk-d35-q2",
                        "question": "When should you prefer a Difference Array over a standard loop for updates?",
                        "options": [
                            {"id": "A", "label": "When you have a single point update"},
                            {"id": "B", "label": "When you have many batch range updates on an array before querying the final state"},
                            {"id": "C", "label": "When array elements are floating point numbers"},
                            {"id": "D", "label": "Only on linked lists"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Point updates are already O(1) in arrays.",
                            "B": "Correct! Difference arrays turn each range update into 2 point modifications (O(1)), resolving all updates in a single final prefix sweep.",
                            "C": "Incorrect: Data type is irrelevant.",
                            "D": "Incorrect: Difference arrays require direct index access."
                        }
                    }
                ],
                takeaway="N = 10^5 demands O(N log N) or faster; difference arrays excel at batch range updates."
            ),
            make_practice_step(
                "day35-step4", 4, "Equilibrium Index Finder", "Practice",
                "Find Equilibrium Index Using Total Sum and Running Prefix",
                "Find an index where sum of elements to left equals sum of elements to right in O(N) time and O(1) space.",
                "Equilibrium Index Solver",
                [
                    "Given `nums = [1, 7, 3, 6, 5, 6]`.",
                    "Calculate `total_sum = sum(nums)` in $O(N)$ time.",
                    "Maintain a running `left_sum = 0` as you iterate with index `i`.",
                    "At index `i`, the right sum is `total_sum - left_sum - nums[i]`.",
                    "If `left_sum == right_sum`, return `i`.",
                    "Otherwise add `nums[i]` to `left_sum`.",
                    "Print `'Equilibrium index:', eq_idx`."
                ],
                """# Day 35 Practice: Equilibrium Index Solver
nums = [1, 7, 3, 6, 5, 6]

total_sum = sum(nums)
left_sum = 0
eq_idx = -1

# TODO: Iterate with enumerate(nums)
# If left_sum == total_sum - left_sum - x: set eq_idx = i and break
# Else add x to left_sum

print("Equilibrium index:", eq_idx)
""",
                """nums = [1, 7, 3, 6, 5, 6]

total_sum = sum(nums)
left_sum = 0
eq_idx = -1

for i, x in enumerate(nums):
    right_sum = total_sum - left_sum - x
    if left_sum == right_sum:
        eq_idx = i
        break
    left_sum += x

print("Equilibrium index:", eq_idx)
""",
                ["Equilibrium index: 3"],
                "At index 3 (value 6): left sum is 1+7+3=11; right sum is 5+6=11. Matches in O(N) time and O(1) auxiliary space!",
                takeaway="Combining total sum with running prefix achieves O(N) time with O(1) auxiliary memory."
            ),
            make_completion_step(
                "day35-step5", 5, "Section 3 Synthesis Mastery", "Recap",
                35, "Day 35 Complete: Section 3 Review & Algorithmic Foundations",
                "Congratulations! You have completed Section 3: Problem Solving & Computational Thinking.",
                [
                    {
                        "concept": "Big-O Scale Limits",
                        "naiveIntuition": "O(N^2) is fine for all LeetCode problems",
                        "pythonReality": "When N >= 10^4, O(N^2) exceeds 10^8 operations and triggers TLE"
                    },
                    {
                        "concept": "Running Sum vs Array",
                        "naiveIntuition": "Prefix sums always require allocating a full prefix array",
                        "pythonReality": "If only past sums are needed, a single running accumulator achieves O(1) space"
                    }
                ],
                ["Asymptotic Scaling Invariants", "Recursion & Master Theorem", "Prefix Sums & Difference Arrays", "10^8 Operations Benchmark"],
                get_next_preview(35)
            )
        ]
    }

    # DAY 36: String Invariants, Building & Manipulation
    days[36] = {
        "dayNumber": 36,
        "title": "String Invariants & Manipulation",
        "topicName": "String Manipulation",
        "sectionId": "arrays-and-strings",
        "estimatedMinutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [35],
        "concepts": ["String Immutability Pitfalls", "O(N) join vs O(N^2) Concatenation", "Two Pointers on Strings", "Palindrome Verification"],
        "practiceSkills": ["Two-Pointer Palindrome Check", "Efficient String Assembly", "Alphanumeric Filtering"],
        "steps": [
            make_explanation_step(
                "day36-step1", 1, "String Invariants in DSA", "String Invariants",
                "Why String Concatenation in Loops is O(N^2) and How to Avoid It",
                "Master Python's memory model for high-performance string manipulation.",
                [
                    "In Python, strings are immutable. Every time you write `s += char` inside a loop of length $N$, Python must allocate a new string of size $1, 2, ..., N$ and copy all previous characters.",
                    "The total operations required are: $$1 + 2 + 3 + ... + N = \\frac{N(N + 1)}{2} = O(N^2)$$",
                    "To build strings in linear **$O(N)$ time**, always append characters to a `list` and combine them once at the end with `''.join(chars)`."
                ],
                snippets=[{
                    "title": "O(N) List Buffer vs O(N^2) Concatenation",
                    "code": "# DANGEROUS: O(N^2) time\ns = ''\nfor ch in stream:\n    s += ch\n\n# OPTIMAL: O(N) time\nbuffer = []\nfor ch in stream:\n    buffer.append(ch)\ns_clean = ''.join(buffer)",
                    "language": "python",
                    "caption": "Using list buffer and ''.join() for linear string construction."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Memory Pre-allocation in CPython",
                    "content": "`''.join()` calculates the exact total byte length of all strings, allocates the buffer once, and copies data via high-speed C `memcpy`."
                }],
                takeaway="Always assemble strings using list buffers and ''.join() to avoid quadratic O(N^2) overhead."
            ),
            make_explanation_step(
                "day36-step2", 2, "Valid Palindrome with Two Pointers", "Palindrome Check",
                "Two-Pointer Technique for In-Place String Verification",
                "Verify palindromes with O(1) auxiliary space without reversing strings.",
                [
                    "A string is a palindrome if it reads the same forward and backward.",
                    "While `s == s[::-1]` checks palindromes, creating the reversed slice allocates an extra $O(N)$ copy of the string in memory.",
                    "The **Two-Pointer technique** places `left = 0` and `right = len(s) - 1`. While `left < right`, compare characters. If they mismatch, return `False`. Increment `left` and decrement `right`.",
                    "This achieves **$O(N)$ time** and **$O(1)$ auxiliary space**, handling character normalization on-the-fly."
                ],
                snippets=[{
                    "title": "Two-Pointer Palindrome Verification",
                    "code": "def is_palindrome(s):\n    left, right = 0, len(s) - 1\n    while left < right:\n        if s[left] != s[right]:\n            return False\n        left += 1\n        right -= 1\n    return True",
                    "language": "python",
                    "caption": "O(1) auxiliary space palindrome check."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Alphanumeric Filtering",
                    "content": "In LeetCode 'Valid Palindrome', skip non-alphanumeric characters on-the-fly (`ch.isalnum()`) without creating a pre-filtered copy string."
                }],
                takeaway="Two pointers verify palindromes in O(N) time with zero extra string allocations (O(1) space)."
            ),
            make_checkpoint_step(
                "day36-step3", 3, "Strings Checkpoint", "Checkpoint",
                "Test Your Mastery of String Performance",
                "Evaluate concatenation complexities and two-pointer pointers.",
                [
                    {
                        "id": "chk-d36-q1",
                        "question": "What is the time complexity of building a string of length N by executing `result += ch` N times in a loop?",
                        "options": [
                            {"id": "A", "label": "O(N)"},
                            {"id": "B", "label": "O(N^2)"},
                            {"id": "C", "label": "O(N log N)"},
                            {"id": "D", "label": "O(1)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Each concatenation allocates a new string copy.",
                            "B": "Correct! Because strings are immutable, copying characters on each step sums to 1 + 2 + ... + N = N(N+1)/2 = O(N^2) quadratic time.",
                            "C": "Incorrect: It is polynomial.",
                            "D": "Incorrect: String concatenation is not constant time."
                        }
                    },
                    {
                        "id": "chk-d36-q2",
                        "question": "What is the auxiliary space complexity of `s == s[::-1]` vs two-pointer palindrome check?",
                        "options": [
                            {"id": "A", "label": "Both are O(1)"},
                            {"id": "B", "label": "s[::-1] is O(N) space; two pointers is O(1) space"},
                            {"id": "C", "label": "s[::-1] is O(1) space; two pointers is O(N) space"},
                            {"id": "D", "label": "Both are O(N)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Slicing creates a new string object.",
                            "B": "Correct! s[::-1] allocates a complete reversed string copy of size N (O(N) space), whereas two pointers only tracks two integer index variables (O(1) space).",
                            "C": "Incorrect: Slicing allocates memory.",
                            "D": "Incorrect: Two pointers uses constant variables."
                        }
                    }
                ],
                takeaway="Concatenation in loops is O(N^2); s[::-1] allocates O(N) space while two pointers is O(1) space."
            ),
            make_practice_step(
                "day36-step4", 4, "Valid Palindrome with Normalization", "Practice",
                "Check Palindrome Ignoring Case & Punctuation",
                "Verify if a string is a palindrome using two pointers while ignoring spaces and punctuation.",
                "Robust Palindrome Checker",
                [
                    "Given `s = 'A man, a plan, a canal: Panama'`.",
                    "Use two pointers `left = 0` and `right = len(s) - 1`.",
                    "While `left < right`: skip `s[left]` if not `s[left].isalnum()`; skip `s[right]` if not `s[right].isalnum()`.",
                    "Compare `s[left].lower() != s[right].lower()`. If mismatch, return `False`.",
                    "Advance pointers appropriately.",
                    "Print `'Is palindrome:', is_valid`."
                ],
                """# Day 36 Practice: Robust Palindrome Checker
s = "A man, a plan, a canal: Panama"

def check_palindrome(text):
    left, right = 0, len(text) - 1
    while left < right:
        while left < right and not text[left].isalnum():
            left += 1
        while left < right and not text[right].isalnum():
            right -= 1
        if text[left].lower() != text[right].lower():
            return False
        left += 1
        right -= 1
    return True

is_valid = check_palindrome(s)
print("Is palindrome:", is_valid)
""",
                """s = "A man, a plan, a canal: Panama"

def check_palindrome(text):
    left, right = 0, len(text) - 1
    while left < right:
        while left < right and not text[left].isalnum():
            left += 1
        while left < right and not text[right].isalnum():
            right -= 1
        if text[left].lower() != text[right].lower():
            return False
        left += 1
        right -= 1
    return True

is_valid = check_palindrome(s)
print("Is palindrome:", is_valid)
""",
                ["Is palindrome: True"],
                "Skipping non-alphanumeric characters on the fly achieves O(N) time and O(1) auxiliary space.",
                takeaway="In-place two-pointer traversal solves string validation problems with minimal memory."
            ),
            make_completion_step(
                "day36-step5", 5, "String Manipulation Mastery", "Recap",
                36, "Day 36 Complete: String Invariants & Manipulation",
                "You have mastered string immutability performance, ''.join() buffers, and O(1) space two-pointer checks.",
                [
                    {
                        "concept": "String Concatenation",
                        "naiveIntuition": "s += ch is harmless inside small loops",
                        "pythonReality": "It allocates a new string copy every step, degrading loops to O(N^2)"
                    },
                    {
                        "concept": "Palindrome Checks",
                        "naiveIntuition": "Always reverse the string with s[::-1]",
                        "pythonReality": "Slicing allocates O(N) extra memory; two pointers is in-place O(1) space"
                    }
                ],
                ["O(N) List Buffer & ''.join() Invariant", "Two-Pointer Opposing Traversal", "In-Place Alphanumeric Skipping", "O(1) Auxiliary Space Palindrome Proof"],
                get_next_preview(36)
            )
        ]
    }

    # DAY 37: Subarrays vs Subsequences vs Substrings
    days[37] = {
        "dayNumber": 37,
        "title": "Subarrays vs Subsequences",
        "topicName": "Subarrays vs Subsequences",
        "sectionId": "arrays-and-strings",
        "estimatedMinutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [36],
        "concepts": ["Contiguous vs Non-Contiguous", "Total Counts: N(N+1)/2 vs 2^N", "Subarray Algorithms", "Subsequence Algorithms"],
        "practiceSkills": ["Taxonomy Identification", "Subsequence Verification (Two Pointers)", "Subarray Generation"],
        "steps": [
            make_explanation_step(
                "day37-step1", 1, "The Three Core Sequence Substructures", "Sequence Taxonomy",
                "Subarrays vs Substrings vs Subsequences vs Subsets",
                "Never confuse contiguous slices with non-contiguous orderings.",
                [
                    "Algorithmic problems frequently ask about sequence substructures. Differentiating them is critical for selecting the right algorithm:",
                    "1. **Subarray / Substring**: A **contiguous** slice of the original sequence. For an array of size $N$, there are exactly $\\frac{N(N + 1)}{2} = O(N^2)$ non-empty subarrays. Solved with **Sliding Window**, **Prefix Sums**, or **Two Pointers**.",
                    "2. **Subsequence**: A sequence derived by deleting zero or more elements **without changing the relative order** of remaining elements. For size $N$, there are $2^N$ subsequences. Solved with **Dynamic Programming** or **Greedy** algorithms.",
                    "3. **Subset**: An unordered selection of elements (order does not matter)."
                ],
                snippets=[{
                    "title": "Subarray vs Subsequence Examples",
                    "code": "# arr = [1, 2, 3]\n# Subarrays (contiguous, O(N^2)): \n# [1], [2], [3], [1, 2], [2, 3], [1, 2, 3]\n\n# Subsequences (ordered non-contiguous, 2^N):\n# [], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]\n# Notice [1, 3] is a subsequence but NOT a subarray!",
                    "language": "python",
                    "caption": "[1, 3] maintains relative order but is not contiguous."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Counting Formula",
                    "content": "Subarrays: $O(N^2)$ polynomial. Subsequences: $O(2^N)$ exponential. If a problem asks for 'longest subsequence', brute-force enumeration will TLE!"
                }],
                takeaway="Subarrays are strictly contiguous (O(N^2)); subsequences preserve relative order but can skip elements (2^N)."
            ),
            make_explanation_step(
                "day37-step2", 2, "Is Subsequence? Two-Pointer Greedy Check", "Subsequence Check",
                "Checking if String s is a Subsequence of String t in O(len(t)) Time",
                "A linear greedy two-pointer scan.",
                [
                    "To determine if `s` is a subsequence of `t` (e.g. `s = 'ace'`, `t = 'abcde'`):",
                    "- Place pointer `i = 0` on `s` and pointer `j = 0` on `t`.",
                    "- While `i < len(s)` and `j < len(t)`: if `s[i] == t[j]`, advance `i` (match found!).",
                    "- Always advance `j` to examine the next character in `t`.",
                    "- At the end, `s` is a subsequence if and only if `i == len(s)`.",
                    "Time complexity is strictly **$O(\\text{len}(t))$** with **$O(1)$ auxiliary space**."
                ],
                snippets=[{
                    "title": "is_subsequence Implementation",
                    "code": "def is_subsequence(s, t):\n    i, j = 0, 0\n    while i < len(s) and j < len(t):\n        if s[i] == t[j]:\n            i += 1\n        j += 1\n    return i == len(s)\n\nprint(is_subsequence('ace', 'abcde')) # True\nprint(is_subsequence('aec', 'abcde')) # False (wrong order!)",
                    "language": "python",
                    "caption": "Greedy linear scan to verify subsequences."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Order Matters in Subsequences",
                    "content": "`'aec'` is NOT a subsequence of `'abcde'` because `'e'` appears before `'c'` in the query, violating the original sequence order."
                }],
                takeaway="Subsequence verification checks relative ordering in linear O(len(t)) time using two pointers."
            ),
            make_checkpoint_step(
                "day37-step3", 3, "Substructures Checkpoint", "Checkpoint",
                "Test Your Mastery of Sequence Taxonomy",
                "Classify substructures and calculate combinatorial counts.",
                [
                    {
                        "id": "chk-d37-q1",
                        "question": "Which of the following is a SUBSEQUENCE of [1, 2, 3, 4, 5] but NOT a SUBARRAY?",
                        "options": [
                            {"id": "A", "label": "[2, 3, 4]"},
                            {"id": "B", "label": "[1, 3, 5]"},
                            {"id": "C", "label": "[5, 4, 3]"},
                            {"id": "D", "label": "[1, 2]"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: [2, 3, 4] is contiguous, so it is both a subarray and a subsequence.",
                            "B": "Correct! [1, 3, 5] skips elements 2 and 4 (non-contiguous, so not a subarray), but preserves relative left-to-right order, making it a valid subsequence.",
                            "C": "Incorrect: Elements are in reversed order, so it is neither a subarray nor a subsequence.",
                            "D": "Incorrect: Contiguous subarray."
                        }
                    },
                    {
                        "id": "chk-d37-q2",
                        "question": "How many total non-empty contiguous subarrays exist for an array of length N = 4?",
                        "options": [
                            {"id": "A", "label": "16 (2^4)"},
                            {"id": "B", "label": "10 (4 * 5 / 2)"},
                            {"id": "C", "label": "24 (4!)"},
                            {"id": "D", "label": "8"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: 2^N is the count of subsequences.",
                            "B": "Correct! The number of non-empty contiguous subarrays is N*(N+1)/2 = 4*5/2 = 10 (4 of length 1, 3 of length 2, 2 of length 3, 1 of length 4).",
                            "C": "Incorrect: N! is permutations.",
                            "D": "Incorrect: Miscalculation."
                        }
                    }
                ],
                takeaway="Subarrays are contiguous (N*(N+1)/2); subsequences skip elements while preserving relative order."
            ),
            make_practice_step(
                "day37-step4", 4, "Subsequence Matcher", "Practice",
                "Verify Multiple Subsequence Queries",
                "Write a function to test whether target words are valid subsequences.",
                "Subsequence Batch Checker",
                [
                    "Given source string `source = 'ahbgdc'` and test words `words = ['abc', 'axc', 'bgd']`.",
                    "Implement `check_subseq(s, t)` using the two-pointer greedy pattern.",
                    "Count how many words in `words` are valid subsequences of `source`.",
                    "Print `'Valid subsequence count:', valid_count`."
                ],
                """# Day 37 Practice: Subsequence Batch Checker
source = "ahbgdc"
words = ["abc", "axc", "bgd"]

def is_sub(s, t):
    i, j = 0, 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1
    return i == len(s)

valid_count = sum(1 for w in words if is_sub(w, source))
print("Valid subsequence count:", valid_count)
""",
                """source = "ahbgdc"
words = ["abc", "axc", "bgd"]

def is_sub(s, t):
    i, j = 0, 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1
    return i == len(s)

valid_count = sum(1 for w in words if is_sub(w, source))
print("Valid subsequence count:", valid_count)
""",
                ["Valid subsequence count: 2"],
                "'abc' and 'bgd' are valid; 'axc' fails because 'x' is not present in source.",
                takeaway="Two pointers greedily advance through the source string to match subsequence characters."
            ),
            make_completion_step(
                "day37-step5", 5, "Substructures Mastery", "Recap",
                37, "Day 37 Complete: Subarrays vs Subsequences",
                "You have mastered sequence taxonomy, combinatorial bounds, and linear subsequence checks.",
                [
                    {
                        "concept": "Subarray vs Subsequence",
                        "naiveIntuition": "Subarray and subsequence are interchangeable terms",
                        "pythonReality": "Subarrays are strictly contiguous slices; subsequences preserve order but can skip items"
                    },
                    {
                        "concept": "Count Growth",
                        "naiveIntuition": "Both have roughly the same number of variations",
                        "pythonReality": "Subarrays grow polynomially (O(N^2)); subsequences grow exponentially (O(2^N))"
                    }
                ],
                ["Contiguous Subarrays (N*(N+1)/2)", "Non-contiguous Subsequences (2^N)", "Linear Two-Pointer Subsequence Match", "Combinatorial Bounds Invariants"],
                get_next_preview(37)
            )
        ]
    }

    # DAY 38: In-Place Array Transformations
    days[38] = {
        "dayNumber": 38,
        "title": "In-Place Array Transformations",
        "topicName": "In-Place Transformations",
        "sectionId": "arrays-and-strings",
        "estimatedMinutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [37],
        "concepts": ["Write-Pointer Technique", "Remove Duplicates Pattern", "Move Zeroes Invariant", "O(1) Auxiliary Space"],
        "practiceSkills": ["Write-Pointer Coordination", "In-Place Compaction", "Stable Zero Shifting"],
        "steps": [
            make_explanation_step(
                "day38-step1", 1, "The Write-Pointer Invariant", "Write-Pointer",
                "Overwriting Elements In-Place with Read/Write Pointer Decoupling",
                "Modify arrays with O(1) auxiliary space without element shifting penalties.",
                [
                    "Many algorithmic challenges require modifying an array **in-place** (e.g. *'Remove duplicates from sorted array'*, *'Move zeroes'*), returning the length of the valid prefix.",
                    "Using `arr.pop(i)` or `arr.remove(x)` inside a loop costs $O(N)$ per deletion, resulting in $O(N^2)$ time.",
                    "The optimal paradigm decouples traversal into two pointers:",
                    "- **Read Pointer (`read`)**: Scans through every element of the array.",
                    "- **Write Pointer (`write`)**: Marks the position where the next valid element should be placed.",
                    "Because `write <= read` at all times, the write pointer never overwrites unprocessed data! Total time is strictly **$O(N)$** with **$O(1)$ auxiliary space**."
                ],
                snippets=[{
                    "title": "Remove Duplicates In-Place",
                    "code": "def remove_duplicates(nums):\n    if not nums:\n        return 0\n    write = 1\n    for read in range(1, len(nums)):\n        if nums[read] != nums[read - 1]:\n            nums[write] = nums[read]\n            write += 1\n    return write # Length of unique prefix",
                    "language": "python",
                    "caption": "Write-pointer compaction pattern."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "write <= read Invariant",
                    "content": "Since the write pointer advances at or slower than the read pointer, reading is always safe from premature overwrites."
                }],
                takeaway="Decoupling read and write pointers enables in-place array compaction in O(N) time and O(1) space."
            ),
            make_explanation_step(
                "day38-step2", 2, "The Move Zeroes Pattern", "Move Zeroes",
                "Maintaining Relative Order While Shifting Zeroes to the End",
                "Compact non-zero elements forward and fill the remainder with zeroes.",
                [
                    "Consider *Move Zeroes*: move all zeroes to the end while preserving the relative order of non-zero numbers.",
                    "1. Walk through the array with `read`. Whenever `arr[read] != 0`, write it to `arr[write]` and increment `write`.",
                    "2. Once `read` reaches the end, all non-zero elements occupy indices `0` to `write - 1` in their original order.",
                    "3. Fill the remaining positions from `write` to `len(arr) - 1` with `0`.",
                    "Alternatively, swap `arr[write], arr[read] = arr[read], arr[write]` whenever `arr[read] != 0`."
                ],
                snippets=[{
                    "title": "Move Zeroes via Swapping",
                    "code": "def move_zeroes(nums):\n    write = 0\n    for read in range(len(nums)):\n        if nums[read] != 0:\n            nums[write], nums[read] = nums[read], nums[write]\n            write += 1\n\narr = [0, 1, 0, 3, 12]\nmove_zeroes(arr)\nprint(arr) # [1, 3, 12, 0, 0]",
                    "language": "python",
                    "caption": "In-place zero swapping."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Do Not Use pop(i)",
                    "content": "Popping elements while iterating causes skipped indices and degrades performance to $O(N^2)$."
                }],
                takeaway="Swapping or compacting with a write pointer moves target elements in O(N) time with O(1) space."
            ),
            make_checkpoint_step(
                "day38-step3", 3, "In-Place Transformations Checkpoint", "Checkpoint",
                "Test Your Mastery of In-Place Array Compaction",
                "Evaluate read/write pointer states and array prefixes.",
                [
                    {
                        "id": "chk-d38-q1",
                        "question": "Why is `write <= read` a crucial invariant in write-pointer algorithms?",
                        "options": [
                            {"id": "A", "label": "It guarantees that the write pointer never overwrites an element before the read pointer has inspected it"},
                            {"id": "B", "label": "It ensures the array remains sorted"},
                            {"id": "C", "label": "It prevents list index out of range errors on write"},
                            {"id": "D", "label": "It forces O(1) time complexity"}
                        ],
                        "correctOptionId": "A",
                        "explanations": {
                            "A": "Correct! Because write <= read, the write pointer only modifies positions that have already been processed by the read pointer, preventing data loss.",
                            "B": "Incorrect: Sorting depends on comparison logic.",
                            "C": "Incorrect: Boundaries are capped by array length.",
                            "D": "Incorrect: Complexity is O(N)."
                        }
                    },
                    {
                        "id": "chk-d38-q2",
                        "question": "In `remove_duplicates([1, 1, 2, 2, 3])`, what is the value of `write` at termination?",
                        "options": [
                            {"id": "A", "label": "5"},
                            {"id": "B", "label": "3"},
                            {"id": "C", "label": "2"},
                            {"id": "D", "label": "4"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: 5 is the original length.",
                            "B": "Correct! There are 3 unique elements: 1, 2, 3. The write pointer stops at index 3, defining the prefix length.",
                            "C": "Incorrect: Miscounted unique items.",
                            "D": "Incorrect: Duplicates are eliminated."
                        }
                    }
                ],
                takeaway="write <= read prevents data loss; write pointer index indicates length of unique compacted prefix."
            ),
            make_practice_step(
                "day38-step4", 4, "Remove Element In-Place", "Practice",
                "Implement In-Place Value Removal",
                "Remove all instances of `val = 3` from `nums` in-place and return the new length.",
                "In-Place Element Remover",
                [
                    "Given `nums = [3, 2, 2, 3, 4, 3, 5]` and `val = 3`.",
                    "Initialize `write = 0`.",
                    "Iterate `read` from 0 to `len(nums) - 1`.",
                    "If `nums[read] != val`, set `nums[write] = nums[read]` and increment `write += 1`.",
                    "Print `'New length:', write` and `'Compacted prefix:', nums[:write]`."
                ],
                """# Day 38 Practice: In-Place Element Remover
nums = [3, 2, 2, 3, 4, 3, 5]
val = 3

write = 0
for read in range(len(nums)):
    if nums[read] != val:
        nums[write] = nums[read]
        write += 1

print("New length:", write)
print("Compacted prefix:", nums[:write])
""",
                """nums = [3, 2, 2, 3, 4, 3, 5]
val = 3

write = 0
for read in range(len(nums)):
    if nums[read] != val:
        nums[write] = nums[read]
        write += 1

print("New length:", write)
print("Compacted prefix:", nums[:write])
""",
                ["New length: 4", "Compacted prefix: [2, 2, 4, 5]"],
                "Elements != 3 are 2, 2, 4, 5. Write pointer stops at index 4.",
                takeaway="In-place element removal compacts valid data into the array prefix with O(1) auxiliary space."
            ),
            make_completion_step(
                "day38-step5", 5, "In-Place Transformations Mastery", "Recap",
                38, "Day 38 Complete: In-Place Array Transformations",
                "You have mastered read/write pointer decoupling, array compaction, and O(1) auxiliary space mutations.",
                [
                    {
                        "concept": "Deletion In-Place",
                        "naiveIntuition": "Call pop(i) or remove(x) when duplicate is found",
                        "pythonReality": "pop(i) shifts all following elements taking O(N); write pointer overwrites in O(1)"
                    },
                    {
                        "concept": "Prefix Validity",
                        "naiveIntuition": "Array elements beyond the new length must be deleted",
                        "pythonReality": "LeetCode only checks elements up to the returned prefix length write"
                    }
                ],
                ["Read vs Write Pointer Decoupling", "write <= read Safety Invariant", "Zero Shifting and Swapping", "O(N) Time and O(1) Space Guarantees"],
                get_next_preview(38)
            )
        ]
    }

    # DAY 39: Two Pointers: Opposing Direction
    days[39] = {
        "dayNumber": 39,
        "title": "Two Pointers: Opposing Direction",
        "topicName": "Opposing Two Pointers",
        "sectionId": "arrays-and-strings",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [38],
        "concepts": ["Two Sum in Sorted Array", "Container With Most Water", "Monotonicity Invariant", "Greedy Elimination"],
        "practiceSkills": ["Opposing Pointers Coordination", "Container Area Maximization", "Monotonic State Elimination"],
        "steps": [
            make_explanation_step(
                "day39-step1", 1, "The Opposing Two-Pointer Pattern", "Opposing Pointers",
                "Exploiting Monotonicity to Eliminate Search Space in O(N) Time",
                "Solve Two Sum and optimization problems on sorted arrays without hash maps.",
                [
                    "When an array is sorted, elements exhibit **monotonicity**: elements increase from left to right.",
                    "In **Two Sum II (Sorted Array)**, we want to find two numbers that sum to `target`:",
                    "- Place `left = 0` (smallest element) and `right = len(arr) - 1` (largest element).",
                    "- Compute `current_sum = arr[left] + arr[right]`.",
                    "- If `current_sum == target`: Return the pair!",
                    "- If `current_sum < target`: The sum is too small. Because `arr[right]` is already the largest remaining element, pairing `arr[left]` with ANY other element will also be too small! We can safely eliminate `left` by doing `left += 1`.",
                    "- If `current_sum > target`: The sum is too large. We can safely eliminate `right` by doing `right -= 1`.",
                    "At each step, we eliminate an entire row or column of potential pairs, achieving **$O(N)$ time** and **$O(1)$ space**!"
                ],
                snippets=[{
                    "title": "Two Sum II Opposing Pointers",
                    "code": "def two_sum_sorted(nums, target):\n    left, right = 0, len(nums) - 1\n    while left < right:\n        s = nums[left] + nums[right]\n        if s == target:\n            return (left, right)\n        elif s < target:\n            left += 1   # Need a larger sum\n        else:\n            right -= 1  # Need a smaller sum\n    return None",
                    "language": "python",
                    "caption": "O(N) search on sorted arrays via monotonic elimination."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Sorted Array Prerequisite",
                    "content": "Opposing two pointers for sum targets strictly requires a **sorted array**. If the array is unsorted, either sort it in $O(N \\log N)$ or use an $O(N)$ hash map."
                }],
                takeaway="Monotonicity guarantees that adjusting left or right safely eliminates an entire row of candidates."
            ),
            make_explanation_step(
                "day39-step2", 2, "Container With Most Water", "Container Problem",
                "Greedy Elimination in Container With Most Water",
                "Why moving the shorter line is the only choice that could increase area.",
                [
                    "In *Container With Most Water*, given heights `h`, find two lines that hold the most water: $$\\text{Area} = (\\text{right} - \\text{left}) \\times \\min(h[\\text{left}], h[\\text{right}])$$",
                    "Start with maximum width: `left = 0, right = len(h) - 1`.",
                    "To find a larger area, the width $(\\text{right} - \\text{left})$ MUST decrease by 1 at the next step. Therefore, the **only way the area can increase is if the limiting height increases**!",
                    "Since the area is bounded by the shorter line, moving the taller line can NEVER increase area (width decreases, height cannot exceed shorter line).",
                    "Thus, we must **greedily move the pointer pointing to the shorter line** inward!"
                ],
                snippets=[{
                    "title": "Container With Most Water Implementation",
                    "code": "def max_area(height):\n    left, right = 0, len(height) - 1\n    best = 0\n    while left < right:\n        w = right - left\n        h = min(height[left], height[right])\n        best = max(best, w * h)\n        if height[left] < height[right]:\n            left += 1\n        else:\n            right -= 1\n    return best",
                    "language": "python",
                    "caption": "Greedy shorter-line elimination in O(N) time."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Equal Heights Case",
                    "content": "If `height[left] == height[right]`, you can move either pointer (or both inward), because neither can be part of a larger area with the other line fixed."
                }],
                takeaway="Always move the pointer corresponding to the bottleneck (shorter line) to seek a taller boundary."
            ),
            make_checkpoint_step(
                "day39-step3", 3, "Opposing Two Pointers Checkpoint", "Checkpoint",
                "Test Your Mastery of Opposing Pointers",
                "Evaluate pointer movements and greedy elimination logic.",
                [
                    {
                        "id": "chk-d39-q1",
                        "question": "In 'Container With Most Water', why do we move the pointer at the SHORTER line rather than the taller line?",
                        "options": [
                            {"id": "A", "label": "Because moving the taller line would make width negative"},
                            {"id": "B", "label": "Because width decreases; if we move the taller line, the new height cannot exceed the current shorter line, so area can only decrease or stay same"},
                            {"id": "C", "label": "It is an arbitrary convention; moving either gives identical results"},
                            {"id": "D", "label": "To sort the array"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Width is right - left > 0.",
                            "B": "Correct! The bottleneck is the shorter line. Moving the taller line decreases width while the height remains capped by the shorter line, guaranteeing a strictly smaller area. Moving the shorter line is the only possibility to find a taller bottleneck.",
                            "C": "Incorrect: Moving the taller line misses the optimal solution.",
                            "D": "Incorrect: The heights are not being sorted."
                        }
                    },
                    {
                        "id": "chk-d39-q2",
                        "question": "Given sorted `nums = [1, 3, 5, 8, 12]` and `target = 11`, with `left = 0 (1)` and `right = 4 (12)`. What is the next pointer move?",
                        "options": [
                            {"id": "A", "label": "left += 1"},
                            {"id": "B", "label": "right -= 1"},
                            {"id": "C", "label": "Both increment"},
                            {"id": "D", "label": "Return 1"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: That would increase the sum further.",
                            "B": "Correct! Current sum is 1 + 12 = 13. Since 13 > 11, the sum is too large. We decrement right -= 1 to reduce the sum.",
                            "C": "Incorrect: Only one pointer moves per step.",
                            "D": "Incorrect: Target is not yet matched."
                        }
                    }
                ],
                takeaway="Move left pointer when sum < target; move right pointer when sum > target; move shorter container line."
            ),
            make_practice_step(
                "day39-step4", 4, "Container With Most Water Solver", "Practice",
                "Maximize Water Retention Between Vertical Lines",
                "Implement the O(N) two-pointer solution for Container With Most Water.",
                "Water Container Maximizer",
                [
                    "Given `heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]`.",
                    "Initialize `left = 0, right = len(heights) - 1, max_water = 0`.",
                    "While `left < right`: compute area `(right - left) * min(heights[left], heights[right])`.",
                    "Update `max_water = max(max_water, area)`.",
                    "Advance the pointer pointing to the smaller height.",
                    "Print `'Max water container:', max_water`."
                ],
                """# Day 39 Practice: Water Container Maximizer
heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]

left, right = 0, len(heights) - 1
max_water = 0

while left < right:
    w = right - left
    h = min(heights[left], heights[right])
    max_water = max(max_water, w * h)
    if heights[left] < heights[right]:
        left += 1
    else:
        right -= 1

print("Max water container:", max_water)
""",
                """heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]

left, right = 0, len(heights) - 1
max_water = 0

while left < right:
    w = right - left
    h = min(heights[left], heights[right])
    max_water = max(max_water, w * h)
    if heights[left] < heights[right]:
        left += 1
    else:
        right -= 1

print("Max water container:", max_water)
""",
                ["Max water container: 49"],
                "Optimal lines are index 1 (height 8) and index 8 (height 7): width = 7, min_height = 7 -> 7 * 7 = 49.",
                takeaway="Opposing two pointers evaluate maximum width configurations and eliminate suboptimal bottlenecks in O(N) time."
            ),
            make_completion_step(
                "day39-step5", 5, "Opposing Two Pointers Mastery", "Recap",
                39, "Day 39 Complete: Two Pointers: Opposing Direction",
                "You have mastered sorted monotonicity elimination, Two Sum II, and Container With Most Water.",
                [
                    {
                        "concept": "Sorting Prerequisite",
                        "naiveIntuition": "Opposing two pointers works on any arbitrary list for target sum",
                        "pythonReality": "It strictly requires a sorted sequence so pointer movements have predictable effects"
                    },
                    {
                        "concept": "Container Bottleneck",
                        "naiveIntuition": "Always move the taller line to try and find an even taller one",
                        "pythonReality": "The shorter line caps container volume; moving it is the only way to increase area"
                    }
                ],
                ["Two Sum II Monotonic Elimination", "O(N) Time and O(1) Auxiliary Space", "Container With Most Water Invariant", "Greedy Bottleneck Advancement"],
                get_next_preview(39)
            )
        ]
    }

    # DAY 40: Two Pointers: Fast & Slow Pointers
    days[40] = {
        "dayNumber": 40,
        "title": "Two Pointers: Fast & Slow",
        "topicName": "Fast & Slow Pointers",
        "sectionId": "arrays-and-strings",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [39],
        "concepts": ["Floyd's Tortoise and Hare", "Cycle Detection in Arrays", "Duplicate Number Finding", "Linked List Preview"],
        "practiceSkills": ["Cycle Traversal Simulation", "Tortoise & Hare Index Mapping", "Floyd's Phase 1 & Phase 2"],
        "steps": [
            make_explanation_step(
                "day40-step1", 1, "Floyd's Cycle Detection Algorithm", "Tortoise & Hare",
                "The Tortoise and Hare: Detecting Cycles with Relative Speed",
                "How two pointers moving at different speeds guarantee cycle detection in O(N) time and O(1) space.",
                [
                    "**Floyd's Cycle Detection Algorithm** (also called the Tortoise and Hare) uses two pointers traversing a sequence:",
                    "- **Slow Pointer (`slow`)**: Advances by 1 step each iteration.",
                    "- **Fast Pointer (`fast`)**: Advances by 2 steps each iteration.",
                    "If the sequence is linear without a cycle, `fast` reaches the end and terminates.",
                    "If a cycle exists, `fast` will enter the cycle first. Inside the cycle, the relative distance between `fast` and `slow` decreases by 1 step on every iteration! Therefore, `fast` is mathematically **guaranteed to catch and collide with `slow`** in at most $C$ iterations (where $C$ is cycle length)."
                ],
                snippets=[{
                    "title": "Floyd's Collision Principle",
                    "code": "# On each iteration:\n# distance_gap = (distance_gap + 2 - 1) % cycle_length\n# distance_gap increases by 1 modulo C each step\n# Collision is guaranteed within C steps of slow entering cycle!",
                    "language": "python",
                    "caption": "Relative speed guarantee of cycle collision."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "O(1) Auxiliary Space",
                    "content": "A hash set of seen nodes detects cycles in $O(N)$ space. Floyd's algorithm detects cycles in **$O(1)$ auxiliary space** using only two pointers!"
                }],
                takeaway="Moving at 1x and 2x speeds guarantees collision within cycles in O(N) time and O(1) space."
            ),
            make_explanation_step(
                "day40-step2", 2, "Finding the Duplicate Number (LeetCode 287)", "Duplicate Detection",
                "Mapping an Array to a Functional Graph: nums[i] as a Pointer",
                "Solve 'Find the Duplicate Number' in O(N) time and O(1) space without modifying the array.",
                [
                    "Given an array `nums` of size $N + 1$ containing integers between $1$ and $N$, the Pigeonhole Principle guarantees at least one duplicate exists.",
                    "If we treat the array as a directed graph where index `i` points to `nums[i]`:",
                    "- Because a duplicate value exists, at least two distinct indices point to the same target index (in-degree $\\ge 2$).",
                    "- This forms a **cycle**, where the duplicate number is the **entry point of the cycle**!",
                    "**Phase 1 (Collision)**: Advance `slow = nums[slow]` and `fast = nums[nums[fast]]` until `slow == fast`.",
                    "**Phase 2 (Entry Point)**: Reset `slow = 0`. Keep `fast` at the collision point. Advance both by 1 step (`slow = nums[slow]`, `fast = nums[fast]`). The point where they meet is the duplicate number!"
                ],
                snippets=[{
                    "title": "Find the Duplicate Number Implementation",
                    "code": "def find_duplicate(nums):\n    # Phase 1: Find collision\n    slow = nums[0]\n    fast = nums[0]\n    while True:\n        slow = nums[slow]\n        fast = nums[nums[fast]]\n        if slow == fast:\n            break\n    # Phase 2: Find cycle entrance\n    slow = nums[0]\n    while slow != fast:\n        slow = nums[slow]\n        fast = nums[fast]\n    return slow",
                    "language": "python",
                    "caption": "Floyd's algorithm for finding duplicate numbers."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Read-Only Invariant",
                    "content": "This algorithm runs in $O(N)$ time and $O(1)$ space without mutating `nums`, satisfying interview constraints that forbid sorting or negative marking."
                }],
                takeaway="Mapping index to value nums[i] creates a functional graph where cycle entrance is the duplicate."
            ),
            make_checkpoint_step(
                "day40-step3", 3, "Fast & Slow Pointers Checkpoint", "Checkpoint",
                "Test Your Mastery of Floyd's Algorithm",
                "Verify cycle collision mathematics and Phase 2 mechanics.",
                [
                    {
                        "id": "chk-d40-q1",
                        "question": "Once the fast and slow pointers collide in Phase 1 of Floyd's algorithm, how is the cycle entrance located in Phase 2?",
                        "options": [
                            {"id": "A", "label": "Move fast backward by one step"},
                            {"id": "B", "label": "Reset slow to the starting node, and advance BOTH pointers at 1 step per iteration until they meet"},
                            {"id": "C", "label": "Continue moving fast at 2 steps until it collides again"},
                            {"id": "D", "label": "Return the collision point directly"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Linked structures cannot traverse backwards.",
                            "B": "Correct! Mathematical proof shows that the distance from start to cycle entry equals the distance from collision point to cycle entry. Advancing both at 1 step per cycle causes them to meet exactly at the cycle entrance.",
                            "C": "Incorrect: That would simply circle the loop again.",
                            "D": "Incorrect: The collision point is inside the cycle, not necessarily at the entry."
                        }
                    },
                    {
                        "id": "chk-d40-q2",
                        "question": "Why is Floyd's algorithm preferred over a hash set for cycle detection in memory-constrained environments?",
                        "options": [
                            {"id": "A", "label": "A hash set is O(N^2) time"},
                            {"id": "B", "label": "Floyd's uses O(1) auxiliary space, whereas a hash set stores all N visited nodes (O(N) space)"},
                            {"id": "C", "label": "Floyd's works on unhashable objects"},
                            {"id": "D", "label": "Floyd's algorithm executes in O(log N) time"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Hash set is O(N) time.",
                            "B": "Correct! A hash set allocates O(N) memory to record seen nodes. Floyd's tracks only two pointer variables, achieving O(1) auxiliary space.",
                            "C": "Incorrect: Floyd's still requires addressable nodes.",
                            "D": "Incorrect: Both algorithms are O(N) time."
                        }
                    }
                ],
                takeaway="Phase 2 resets one pointer to start and advances both by 1 step; Floyd's achieves O(1) auxiliary space."
            ),
            make_practice_step(
                "day40-step4", 4, "Find Duplicate in Array", "Practice",
                "Implement Floyd's Tortoise and Hare on Array Graph",
                "Find the duplicate number in an array of N+1 integers without extra space.",
                "Duplicate Number Finder",
                [
                    "Given `nums = [1, 3, 4, 2, 2]`.",
                    "In Phase 1, advance `slow = nums[slow]` and `fast = nums[nums[fast]]` until collision.",
                    "In Phase 2, reset `slow = 0` (or `nums[0]` if start is 0) and advance both by 1 step until they meet.",
                    "Return the meeting value as the duplicate.",
                    "Print `'Duplicate number:', duplicate`."
                ],
                """# Day 40 Practice: Duplicate Number Finder
nums = [1, 3, 4, 2, 2]

def find_duplicate(arr):
    # Phase 1: Collision
    slow = arr[0]
    fast = arr[0]
    while True:
        slow = arr[slow]
        fast = arr[arr[fast]]
        if slow == fast:
            break
            
    # Phase 2: Entrance
    slow = arr[0]
    while slow != fast:
        slow = arr[slow]
        fast = arr[fast]
        
    return slow

duplicate = find_duplicate(nums)
print("Duplicate number:", duplicate)
""",
                """nums = [1, 3, 4, 2, 2]

def find_duplicate(arr):
    slow = arr[0]
    fast = arr[0]
    while True:
        slow = arr[slow]
        fast = arr[arr[fast]]
        if slow == fast:
            break
            
    slow = arr[0]
    while slow != fast:
        slow = arr[slow]
        fast = arr[fast]
        
    return slow

duplicate = find_duplicate(nums)
print("Duplicate number:", duplicate)
""",
                ["Duplicate number: 2"],
                "Indices: 0->1->3->2->4->2. The cycle is 2->4->2; entrance is 2.",
                takeaway="Floyd's algorithm treats arrays as functional graphs to locate cycles in O(N) time and O(1) space."
            ),
            make_completion_step(
                "day40-step5", 5, "Fast & Slow Pointers Mastery", "Recap",
                40, "Day 40 Complete: Two Pointers: Fast & Slow",
                "Congratulations! You have completed Batch 2 (Days 21 to 40) with complete mastery of asymptotics, recursion, prefix systems, and two-pointer paradigms.",
                [
                    {
                        "concept": "Cycle Collision Proof",
                        "naiveIntuition": "Fast might hop over slow and never meet inside a cycle",
                        "pythonReality": "Fast closes the gap by exactly 1 step per cycle, guaranteeing collision"
                    },
                    {
                        "concept": "Array as Graph",
                        "naiveIntuition": "Linked list cycle algorithms cannot be applied to arrays",
                        "pythonReality": "Treating index -> nums[i] maps arrays directly to functional graphs"
                    }
                ],
                ["Floyd's Tortoise & Hare Mechanics", "Relative Speed Collision Guarantee", "Phase 1 & Phase 2 Proof", "Batch 2 (Days 21-40) Completion"],
                get_next_preview(40)
            )
        ]
    }

    return days
