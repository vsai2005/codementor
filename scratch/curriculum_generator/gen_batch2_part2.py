from .common import (
    CURRICULUM_MAP,
    get_difficulty,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)

def get_batch2_part2_days():
    days = {}

    # DAY 31: Dynamic Arrays vs Static Arrays
    days[31] = {
        "dayNumber": 31,
        "title": "Dynamic Arrays vs Static Arrays",
        "topicName": "Array Data Structures",
        "sectionId": "computational-thinking",
        "estimatedMinutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [30],
        "concepts": ["Static vs Dynamic Allocations", "Amortized Geometric Resizing", "Memory Locality & Cache Lines", "O(1) Access vs O(N) Inserts"],
        "practiceSkills": ["Dynamic Array Simulation", "Amortized Cost Calculation", "Cache Locality Optimization"],
        "steps": [
            make_explanation_step(
                "day31-step1", 1, "Static Arrays & Hardware Memory", "Static Arrays & Hardware",
                "Fixed-Size Buffers, Memory Locality, and CPU Cache Lines",
                "Why contiguous memory buffers are the fastest data structure on modern hardware.",
                [
                    "A **static array** is a contiguous block of fixed-size memory allocated upfront. Because elements are adjacent in physical RAM, computing the address of element `i` is an instantaneous hardware operation: `base_address + i * element_size`.",
                    "Contiguous arrays have exceptional **spatial locality**: when the CPU reads element `arr[0]`, the hardware prefetcher loads the entire 64-byte **CPU cache line** containing `arr[1]...arr[7]` into ultra-fast L1 cache.",
                    "However, static arrays cannot grow. If you need more capacity, you must allocate a new, larger buffer and copy all elements over."
                ],
                snippets=[{
                    "title": "Hardware Address Offset Calculation",
                    "code": "# Static array access is pure arithmetic:\n# address(i) = base + i * 8 bytes (on 64-bit architectures)\n# No pointer chasing, O(1) direct hardware indexing",
                    "language": "python",
                    "caption": "Hardware indexing via base offset."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Cache Locality Advantage",
                    "content": "Iterating over a contiguous array can be 10x-50x faster than traversing a linked list of the same size due to CPU cache hits vs cache misses."
                }],
                takeaway="Contiguous array indexing is a single address calculation benefiting from CPU cache line prefetching."
            ),
            make_explanation_step(
                "day31-step2", 2, "Dynamic Resizing & Geometric Amortization", "Amortized Resizing",
                "Why Dynamic Arrays Double Capacity: Geometric Growth vs Arithmetic Growth",
                "The mathematical proof of amortized O(1) append.",
                [
                    "A **dynamic array** wraps a static buffer. When full, it allocates a new buffer of size $2 \\times$ (or $1.5 \\times$) capacity and copies existing elements.",
                    "If capacity grew arithmetically (+10 each time), copying $N$ elements would cost $O(N^2)$ total, making each append cost $O(N)$.",
                    "Under **geometric growth** (doubling), resizing occurs at sizes $1, 2, 4, 8, ..., N$. The total elements copied across all resizings is: $$1 + 2 + 4 + ... + N = 2N - 1 < 2N$$",
                    "Dividing $2N$ copies across $N$ total appends yields $\\le 2$ copies per append—proving **amortized $O(1)$** cost!"
                ],
                snippets=[{
                    "title": "Geometric Amortization Proof",
                    "code": "# N appends trigger resizes at 1, 2, 4, 8, 16... N\n# Total copy operations: sum_{i=0}^{k} 2^i = 2^(k+1) - 1 ~ 2N\n# Amortized work per append: 2N / N = O(1) constant!",
                    "language": "python",
                    "caption": "Geometric series proving amortized O(1) complexity."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Fixed Over-Allocation Penalty",
                    "content": "Appending to an array with fixed additions (`capacity += 1`) degrades total append time from $O(N)$ to catastrophic $O(N^2)$."
                }],
                takeaway="Geometric capacity scaling (multiplying by a factor) guarantees amortized O(1) insertion."
            ),
            make_checkpoint_step(
                "day31-step3", 3, "Arrays Checkpoint", "Checkpoint",
                "Test Your Mastery of Array Architecture",
                "Evaluate cache locality and resizing mechanics.",
                [
                    {
                        "id": "chk-d31-q1",
                        "question": "Why does doubling array capacity give amortized O(1) append, whereas increasing capacity by +100 gives O(N) append?",
                        "options": [
                            {"id": "A", "label": "Doubling is supported by CPU hardware instructions"},
                            {"id": "B", "label": "Geometric doubling spreads infrequent O(N) copies over exponentially many O(1) inserts, bounding total copies to 2N"},
                            {"id": "C", "label": "Doubling avoids memory allocation"},
                            {"id": "D", "label": "There is no difference in asymptotic complexity"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: It is a mathematical property of geometric series, not a CPU instruction.",
                            "B": "Correct! Total copies for doubling is bounded by 2N, yielding 2N/N = O(1) per insert. Fixed additions copy N elements every 100 inserts, yielding O(N^2)/N = O(N) per insert.",
                            "C": "Incorrect: Resizing still allocates memory.",
                            "D": "Incorrect: One is O(1) amortized, the other is O(N)."
                        }
                    },
                    {
                        "id": "chk-d31-q2",
                        "question": "What primary hardware mechanism makes iterating an array faster than traversing a linked list?",
                        "options": [
                            {"id": "A", "label": "CPU branch prediction"},
                            {"id": "B", "label": "Spatial locality and CPU cache line prefetching"},
                            {"id": "C", "label": "Instruction pipelining only"},
                            {"id": "D", "label": "Virtual memory paging"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Branch prediction predicts conditionals.",
                            "B": "Correct! Contiguous memory allows hardware prefetchers to load entire 64-byte cache lines, reducing high-latency RAM round-trips.",
                            "C": "Incorrect: Pipelining benefits both, but memory latency dominates.",
                            "D": "Incorrect: Paging handles OS virtual memory."
                        }
                    }
                ],
                takeaway="Geometric doubling yields amortized O(1) append; spatial locality optimizes CPU cache performance."
            ),
            make_practice_step(
                "day31-step4", 4, "Simulate Dynamic Resizing", "Practice",
                "Track Resizing Events in a Dynamic Array Buffer",
                "Simulate a dynamic array and count how many elements are copied during growth.",
                "Dynamic Array Capacity Simulator",
                [
                    "Initialize `capacity = 1`, `size = 0`, and `total_copies = 0`.",
                    "Simulate appending 8 elements (values 1 through 8).",
                    "When `size == capacity`, double capacity: `capacity *= 2`, and add the old `size` to `total_copies`.",
                    "Increment `size += 1` on each append.",
                    "Print `'Final capacity:', capacity` and `'Total elements copied:', total_copies`."
                ],
                """# Day 31 Practice: Dynamic Array Capacity Simulator
capacity = 1
size = 0
total_copies = 0

for val in range(1, 9):
    if size == capacity:
        total_copies += size
        capacity *= 2
    size += 1

print("Final capacity:", capacity)
print("Total elements copied:", total_copies)
""",
                """capacity = 1
size = 0
total_copies = 0

for val in range(1, 9):
    if size == capacity:
        total_copies += size
        capacity *= 2
    size += 1

print("Final capacity:", capacity)
print("Total elements copied:", total_copies)
""",
                ["Final capacity: 8", "Total elements copied: 7"],
                "Resizes happen at size 1 (1 copy), 2 (2 copies), 4 (4 copies) -> Total = 7 copies for 8 items (< 2N).",
                takeaway="Total copies during geometric doubling remain strictly less than input size N."
            ),
            make_completion_step(
                "day31-step5", 5, "Dynamic Arrays Mastery", "Recap",
                31, "Day 31 Complete: Dynamic Arrays vs Static Arrays",
                "You have mastered contiguous memory layout, CPU cache locality, and geometric amortized analysis.",
                [
                    {
                        "concept": "Resizing Overhead",
                        "naiveIntuition": "Every append has an unpredictable execution time",
                        "pythonReality": "Resizes are rare; across N appends, amortized time is constant O(1)"
                    },
                    {
                        "concept": "Cache Locality",
                        "naiveIntuition": "Linked lists and arrays have identical sequential access speed",
                        "pythonReality": "Arrays are dramatically faster because adjacent memory loads into CPU cache lines"
                    }
                ],
                ["Spatial Locality & Cache Lines", "Geometric Doubling Mathematics", "Amortized O(1) Proof", "Static vs Dynamic Buffer Tradeoffs"],
                get_next_preview(31)
            )
        ]
    }

    # DAY 32: Prefix Sums & Range Queries (1D)
    days[32] = {
        "dayNumber": 32,
        "title": "Prefix Sums & Range Queries (1D)",
        "topicName": "Prefix Sums",
        "sectionId": "computational-thinking",
        "estimatedMinutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [31],
        "concepts": ["Prefix Sum Array", "O(1) Range Queries", "1-based Indexing Invariant", "Subarray Sum Equals K Preview"],
        "practiceSkills": ["Prefix Array Construction", "O(1) Range Sum Querying", "Boundary Off-by-One Avoidance"],
        "steps": [
            make_explanation_step(
                "day32-step1", 1, "The Power of Prefix Sums", "Prefix Sums",
                "Transforming O(N) Range Sum Queries into O(1) Instant Lookups",
                "Precompute cumulative sums once to answer any range query in constant time.",
                [
                    "If you are given an array of size $N$ and asked to answer $Q$ range sum queries (`sum(arr[L:R+1])`), the naive approach sums the elements in $O(N)$ per query, taking $O(Q \\times N)$ total time.",
                    "By precomputing a **Prefix Sum Array** in $O(N)$ time, every subsequent range query is answered in **$O(1)$ constant time**, dropping total complexity to **$O(N + Q)$**!",
                    "Let `prefix[i]` be the sum of the first `i` elements: `prefix[i] = prefix[i - 1] + arr[i - 1]`. The sum of any range from index `L` to `R` (inclusive) is simply: $$\\text{sum}(L, R) = \\text{prefix}[R + 1] - \\text{prefix}[L]$$"
                ],
                snippets=[{
                    "title": "1-Indexed Prefix Sum Array",
                    "code": "arr = [3, 1, 4, 1, 5, 9]\nn = len(arr)\n# 1-indexed prefix sum array of size n + 1 (prefix[0] = 0)\npref = [0] * (n + 1)\nfor i in range(n):\n    pref[i + 1] = pref[i] + arr[i]\n# pref: [0, 3, 4, 8, 9, 14, 23]\n\n# Query sum from index 1 to 4 (values: 1, 4, 1, 5 -> sum = 11):\n# pref[4 + 1] - pref[1] = pref[5] - pref[1] = 14 - 3 = 11 (O(1)!)\nprint(pref[5] - pref[1]) # 11",
                    "language": "python",
                    "caption": "Constructing and querying 1-indexed prefix sums."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Why 1-Based Prefix Arrays?",
                    "content": "Setting `prefix[0] = 0` eliminates messy edge cases when querying from index 0 (`L = 0`). `prefix[R + 1] - prefix[0]` works without an `if L == 0` check."
                }],
                takeaway="Prefix sums preprocess an array in O(N) time to answer any range sum query in O(1) time."
            ),
            make_explanation_step(
                "day32-step2", 2, "Cumulative State & Prefix Invariants", "Prefix Invariants",
                "Extending Prefix Sums to Frequencies, Products, and Parity",
                "Apply the prefix pattern beyond simple addition.",
                [
                    "The prefix concept applies to any associative, invertible operation:",
                    "- **Prefix Products**: `prefix_prod[i]` for range products (guarding against zeroes).",
                    "- **Prefix XOR**: Range XOR queries: `xor(L, R) = pref[R + 1] ^ pref[L]` (used in range query problems).",
                    "- **Prefix Frequencies**: Counting character occurrences within ranges in $O(1)$ time.",
                    "- **Subarray Sum Equals K**: If `pref[j] - pref[i] == k`, then `pref[i] == pref[j] - k`. Combining prefix sums with a hash map finds target sum subarrays in $O(N)$ time!"
                ],
                snippets=[{
                    "title": "Prefix XOR Invariant",
                    "code": "# Because X ^ X == 0:\n# pref[R + 1] ^ pref[L] cancels out all elements before L,\n# leaving exact range XOR arr[L] ^ ... ^ arr[R] in O(1) time!",
                    "language": "python",
                    "caption": "Invertible operations with prefix arrays."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Static Arrays Only",
                    "content": "Standard prefix sum arrays are designed for **static** arrays. If array elements update frequently, recomputing the prefix sum takes $O(N)$. For dynamic range updates and queries, use a Binary Indexed Tree (Fenwick) or Segment Tree."
                }],
                takeaway="Prefix precomputation applies to any invertible operation; combined with hash maps it finds target subarrays."
            ),
            make_checkpoint_step(
                "day32-step3", 3, "Prefix Sums Checkpoint", "Checkpoint",
                "Test Your Mastery of Prefix Sums",
                "Calculate range query formula and identify off-by-one errors.",
                [
                    {
                        "id": "chk-d32-q1",
                        "question": "Given `arr = [2, 3, 5, 7, 11]` and 1-indexed `pref = [0, 2, 5, 10, 17, 28]`, how do you compute `sum(arr[1:4])` (indices 1 to 3 inclusive: 3 + 5 + 7)?",
                        "options": [
                            {"id": "A", "label": "pref[4] - pref[1]"},
                            {"id": "B", "label": "pref[3] - pref[0]"},
                            {"id": "C", "label": "pref[4] - pref[2]"},
                            {"id": "D", "label": "pref[3] - pref[1]"}
                        ],
                        "correctOptionId": "A",
                        "explanations": {
                            "A": "Correct! Formula is pref[R + 1] - pref[L]. For L = 1 and R = 3: pref[3 + 1] - pref[1] = pref[4] - pref[1] = 17 - 2 = 15 (3 + 5 + 7 = 15).",
                            "B": "Incorrect: That would calculate range from index 0 to 2.",
                            "C": "Incorrect: Subtracting pref[2] would exclude index 1.",
                            "D": "Incorrect: Missing boundary."
                        }
                    },
                    {
                        "id": "chk-d32-q2",
                        "question": "What is the total time complexity to answer Q range queries on an array of size N using prefix sums?",
                        "options": [
                            {"id": "A", "label": "O(N * Q)"},
                            {"id": "B", "label": "O(N + Q)"},
                            {"id": "C", "label": "O(Q log N)"},
                            {"id": "D", "label": "O(N log N)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: That is the naive un-preprocessed time.",
                            "B": "Correct! Building the prefix array takes O(N) preprocessing, and each of the Q queries takes O(1) time. Total time: O(N + Q).",
                            "C": "Incorrect: Binary search is not needed for range lookups.",
                            "D": "Incorrect: Sorting is not performed."
                        }
                    }
                ],
                takeaway="Range sum from L to R is pref[R + 1] - pref[L]; total complexity for Q queries is O(N + Q)."
            ),
            make_practice_step(
                "day32-step4", 4, "Build Range Sum Query Engine", "Practice",
                "Implement a RangeSumQuery Class",
                "Create a class that precomputes prefix sums and answers range queries in O(1).",
                "Range Sum Query Engine",
                [
                    "Build class `NumArray` with `__init__(self, nums)`.",
                    "Build a 1-indexed prefix array `self.pref` of size `len(nums) + 1` with `self.pref[0] = 0`.",
                    "Implement `sum_range(self, left, right)` returning `self.pref[right + 1] - self.pref[left]`.",
                    "Test with `nums = [-2, 0, 3, -5, 2, -1]`.",
                    "Query `sum_range(0, 2)` (should be 1) and `sum_range(2, 5)` (should be -1).",
                    "Print `'Query 1:', q1` and `'Query 2:', q2`."
                ],
                """# Day 32 Practice: Range Sum Query Engine

class NumArray:
    def __init__(self, nums):
        n = len(nums)
        self.pref = [0] * (n + 1)
        for i in range(n):
            self.pref[i + 1] = self.pref[i] + nums[i]

    def sum_range(self, left, right):
        # TODO: Return range sum in O(1) time
        return self.pref[right + 1] - self.pref[left]

obj = NumArray([-2, 0, 3, -5, 2, -1])
q1 = obj.sum_range(0, 2)
q2 = obj.sum_range(2, 5)

print("Query 1:", q1)
print("Query 2:", q2)
""",
                """class NumArray:
    def __init__(self, nums):
        n = len(nums)
        self.pref = [0] * (n + 1)
        for i in range(n):
            self.pref[i + 1] = self.pref[i] + nums[i]

    def sum_range(self, left, right):
        return self.pref[right + 1] - self.pref[left]

obj = NumArray([-2, 0, 3, -5, 2, -1])
q1 = obj.sum_range(0, 2)
q2 = obj.sum_range(2, 5)

print("Query 1:", q1)
print("Query 2:", q2)
""",
                ["Query 1: 1", "Query 2: -1"],
                "Use `self.pref[right + 1] - self.pref[left]` to answer range sum queries in O(1) time.",
                takeaway="1-indexed prefix sums eliminate edge-case branches and provide instant range answers."
            ),
            make_completion_step(
                "day32-step5", 5, "Prefix Sums Mastery", "Recap",
                32, "Day 32 Complete: Prefix Sums & Range Queries (1D)",
                "You have mastered prefix sum construction, 1-indexed padding, and O(1) range query algebra.",
                [
                    {
                        "concept": "Query Bounds",
                        "naiveIntuition": "Range sum is prefix[R] - prefix[L]",
                        "pythonReality": "To include index R, you must subtract from prefix[R + 1] with 1-indexing"
                    },
                    {
                        "concept": "Dynamic Updates",
                        "naiveIntuition": "Prefix sums are great when array values change frequently",
                        "pythonReality": "Updating a single value takes O(N) to recompute prefix sums; use Fenwick trees for dynamic arrays"
                    }
                ],
                ["1-Indexed Prefix Array Convention", "O(1) Range Formula: pref[R+1] - pref[L]", "O(N + Q) Query Amortization", "Associative/Invertible Operation Extensions"],
                get_next_preview(32)
            )
        ]
    }

    # We will complete Days 33-40 with equal rigor
    return days
