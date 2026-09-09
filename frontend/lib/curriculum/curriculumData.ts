import { CurriculumSection } from "./types";

export const TOTAL_CURRICULUM_DAYS = 160;

export const CURRICULUM_SECTIONS: CurriculumSection[] = [
  {
    id: "python-foundations",
    section_number: 1,
    title: "Python Foundations",
    tagline: "Core syntax, data types, execution model, and control structures",
    day_start: 1,
    day_end: 10,
    icon: "Terminal",
    days: [
      {
        day_number: 1,
        title: "Variables, Expressions & Memory Model",
        topic_name: "Python Syntax",
        section_id: "python-foundations",
        estimated_minutes: 30,
        description: "Explore dynamic typing, object references, the id() built-in, and Python's memory assignment semantics.",
        concepts: ["Dynamic Typing", "Object References", "Memory Model", "id() & type()"]
      },
      {
        day_number: 2,
        title: "Numerical Types, Arithmetic & Bitwise",
        topic_name: "Numeric System",
        section_id: "python-foundations",
        estimated_minutes: 25,
        description: "Deep dive into arbitrary-precision integers, IEEE-754 floating point quirks, modulo arithmetic, floor division, and bitwise operators.",
        concepts: ["Integers & Floats", "Floor Division & Modulo", "Bitwise Operators"]
      },
      {
        day_number: 3,
        title: "Strings, Slicing & Character Encoding",
        topic_name: "String Processing",
        section_id: "python-foundations",
        estimated_minutes: 30,
        description: "Master string immutability, slice notation [start:stop:step], f-strings, and character code conversion using ord() and chr().",
        concepts: ["String Immutability", "Slice Notation [start:stop:step]", "ASCII & ord()/chr()"]
      },
      {
        day_number: 4,
        title: "Booleans & Logical Control Flow",
        topic_name: "Conditionals",
        section_id: "python-foundations",
        estimated_minutes: 25,
        description: "Understand truthiness, boolean coercion, short-circuit logical evaluation, and conditional branch structures.",
        concepts: ["Truthiness & Falsy Values", "Short-Circuit Evaluation"]
      },
      {
        day_number: 5,
        title: "Loops & Iteration Semantics",
        topic_name: "Loop Constructs",
        section_id: "python-foundations",
        estimated_minutes: 35,
        description: "Implement while and for-in loops, loop control statements (break, continue), and the for-else construct.",
        concepts: ["for & while Loops", "break, continue & for-else"]
      },
      {
        day_number: 6,
        title: "Functions, Stack Frames & LEGB Scope",
        topic_name: "Function Basics",
        section_id: "python-foundations",
        estimated_minutes: 30,
        description: "Define reusable procedures, return contracts, local vs global scope, and the LEGB namespace lookup rule.",
        concepts: ["Function Signatures & Return", "LEGB Scope & Call Stack"]
      },
      {
        day_number: 7,
        title: "Function Signatures & Default Argument Trap",
        topic_name: "Advanced Parameters",
        section_id: "python-foundations",
        estimated_minutes: 35,
        description: "Inspect positional and keyword arguments, variadic *args/**kwargs, and the classic mutable default argument trap.",
        concepts: ["*args & **kwargs", "Mutable Default Argument Trap"]
      },
      {
        day_number: 8,
        title: "Basic I/O & Robust Type Casting",
        topic_name: "Input / Output",
        section_id: "python-foundations",
        estimated_minutes: 25,
        description: "Process standard input safely, parse structured tokens, handle EOF errors, and cast input data.",
        concepts: ["sys.stdin & input()", "Type Casting & Defensive Parsing"]
      },
      {
        day_number: 9,
        title: "Python Standard Library Essentials",
        topic_name: "Standard Library",
        section_id: "python-foundations",
        estimated_minutes: 30,
        description: "Leverage standard modules including math, sys, random, and string for algorithmic utility.",
        concepts: ["math & sys Modules", "Built-in Iteration Helpers (zip, enumerate)"]
      },
      {
        day_number: 10,
        title: "Foundations Check & Synthetic Practice",
        topic_name: "Foundations Milestone",
        section_id: "python-foundations",
        estimated_minutes: 40,
        description: "Synthesize variables, conditionals, loops, and functional decomposition to build self-contained algorithmic scripts.",
        concepts: ["Decomposition", "Input Parsing Pipeline", "Algorithmic Control Flow"]
      },
    ]
  },
  {
    id: "python-core",
    section_number: 2,
    title: "Python Core & Data Structures",
    tagline: "Containers, iteration protocols, generator streams, OOP, and memory models",
    day_start: 11,
    day_end: 25,
    icon: "Code",
    days: [
      {
        day_number: 11,
        title: "Lists: Memory Layout & Dynamic Resizing",
        topic_name: "List Architecture",
        section_id: "python-core",
        estimated_minutes: 35,
        description: "Analyze dynamic array memory layouts, pointer arrays in CPython, amortized O(1) append, and the O(N) insert/pop(0) penalty.",
        concepts: ["Contiguous Pointer Array", "Amortized O(1) Append vs O(N) Shift"]
      },
      {
        day_number: 12,
        title: "List Slicing O(K) Cost & Mutability Traps",
        topic_name: "List Mutations",
        section_id: "python-core",
        estimated_minutes: 30,
        description: "Analyze the O(K) time and space complexity of list slicing, shallow vs deep copies, and in-place list mutations.",
        concepts: ["Slicing O(K) Time & Space", "Shallow vs Deep Copy"]
      },
      {
        day_number: 13,
        title: "List Comprehensions & Expressions",
        topic_name: "Comprehensions",
        section_id: "python-core",
        estimated_minutes: 25,
        description: "Transform data expressively and efficiently using list comprehensions and conditional filters.",
        concepts: ["List Comprehension Syntax", "Nested Comprehensions & Scoping"]
      },
      {
        day_number: 14,
        title: "Tuples, Immutability & The Tuple Swap Idiom",
        topic_name: "Tuples",
        section_id: "python-core",
        estimated_minutes: 25,
        description: "Understand tuple immutability, memory savings over lists, unpacking idioms, and using tuples as hashable coordinate keys.",
        concepts: ["Tuple Immutability", "Tuple Packing/Unpacking & Swap"]
      },
      {
        day_number: 15,
        title: "Dictionaries: Compact Hash Table Internals",
        topic_name: "Hash Maps",
        section_id: "python-core",
        estimated_minutes: 35,
        description: "Explore CPython's compact dictionary architecture, hash functions, open-addressing collision resolution, and average O(1) lookups.",
        concepts: ["Compact Hash Table Architecture", "Open Addressing & Load Factor"]
      },
      {
        day_number: 16,
        title: "Dictionary Methods, Views & Aggregation",
        topic_name: "Dictionary Operations",
        section_id: "python-core",
        estimated_minutes: 30,
        description: "Apply get(), setdefault(), dictionary views (.keys(), .values(), .items()), and modern dictionary merging.",
        concepts: ["setdefault() & get()", "Dynamic Dictionary Views & Merge"]
      },
      {
        day_number: 17,
        title: "Sets: Value-Free Hash Tables & O(1) Lookups",
        topic_name: "Set Theory",
        section_id: "python-core",
        estimated_minutes: 30,
        description: "Use sets for O(1) membership testing, deduplication, set algebra, and understand the immutable frozenset.",
        concepts: ["Set O(1) Lookups", "Mathematical Set Operations"]
      },
      {
        day_number: 18,
        title: "The Collections Module: Deque & Counter",
        topic_name: "Specialized Containers",
        section_id: "python-core",
        estimated_minutes: 35,
        description: "Master collections.deque for O(1) appends and pops on both ends, defaultdict, and Counter.",
        concepts: ["collections.deque O(1) Endpoints", "Counter & defaultdict"]
      },
      {
        day_number: 19,
        title: "Iterators & The Iteration Protocol",
        topic_name: "Iteration Architecture",
        section_id: "python-core",
        estimated_minutes: 30,
        description: "Understand iterable vs iterator, the __iter__ and __next__ protocols, and consumable stream behavior.",
        concepts: ["__iter__ & __next__ Protocol", "StopIteration & Exhaustion"]
      },
      {
        day_number: 20,
        title: "Generators & Lazy Memory Streaming",
        topic_name: "Lazy Evaluation",
        section_id: "python-core",
        estimated_minutes: 35,
        description: "Implement generator functions with yield, understand execution suspension, generator expressions, and pipeline composition.",
        concepts: ["yield State Suspension", "yield from & O(1) Space Streams"]
      },
      {
        day_number: 21,
        title: "Decorators, Closures & Metadata Wrappers",
        topic_name: "Higher-Order Functions",
        section_id: "python-core",
        estimated_minutes: 35,
        description: "Write function decorators, understand closures, cell objects, and preserving function metadata with functools.wraps.",
        concepts: ["Closures & Cell Objects", "functools.wraps Decorators"]
      },
      {
        day_number: 22,
        title: "OOP Classes, Dunder Protocols & __lt__",
        topic_name: "Object-Oriented Python",
        section_id: "python-core",
        estimated_minutes: 40,
        description: "Build classes, manage instance state, and implement dunder protocols (__repr__, __eq__, __hash__, and __lt__ for comparators).",
        concepts: ["Class Construction & __init__", "Dunders: __repr__, __eq__, __hash__, __lt__"]
      },
      {
        day_number: 23,
        title: "Inheritance & Method Resolution Order (C3)",
        topic_name: "Inheritance Models",
        section_id: "python-core",
        estimated_minutes: 30,
        description: "Master single and multiple inheritance, super(), and CPython's C3 Linearization Method Resolution Order (MRO).",
        concepts: ["Single & Multiple Inheritance", "C3 Linearization & super()"]
      },
      {
        day_number: 24,
        title: "Exception Handling & Custom Hierarchies",
        topic_name: "Error Architecture",
        section_id: "python-core",
        estimated_minutes: 25,
        description: "Write robust error-handling code with try/except/else/finally and build custom domain exception classes.",
        concepts: ["try/except/else/finally", "Custom Exception Hierarchies"]
      },
      {
        day_number: 25,
        title: "Python DSA Algorithmic Toolkit & Milestone",
        topic_name: "Core Milestone",
        section_id: "python-core",
        estimated_minutes: 45,
        description: "Synthesize Python core data structures into a complete algorithmic toolkit bridging into Data Structures & Algorithms.",
        concepts: ["list.sort() vs sorted() & Multi-Key", "heapq & Tie-Breaker Crash Prevention", "sys.setrecursionlimit & Float Infinity"]
      },
    ]
  },
  {
    id: "computational-thinking",
    section_number: 3,
    title: "Problem Solving & Computational Thinking",
    tagline: "Asymptotic analysis, call stacks, recursion models, invariants, and complexity",
    day_start: 26,
    day_end: 35,
    icon: "Cpu",
    days: [
      {
        day_number: 26,
        title: "Asymptotic Analysis & Big-O Notation",
        topic_name: "Complexity Foundations",
        section_id: "computational-thinking",
        estimated_minutes: 30,
        description: "Understand Big-O notation, asymptotic upper bounds, growth rate hierarchies, and worst-case vs average-case behavior.",
        concepts: ["Big-O Asymptotic Upper Bound", "Growth Orders (O(1) to O(2^N))"]
      },
      {
        day_number: 27,
        title: "Identifying Common Time Complexities",
        topic_name: "Code Complexity Analysis",
        section_id: "computational-thinking",
        estimated_minutes: 30,
        description: "Analyze code snippets to determine O(1), O(log N), O(N), O(N log N), O(N^2), and O(2^N) time complexities.",
        concepts: ["Nested Loops & Stride Halving", "Drop Constants & Non-Dominant Terms"]
      },
      {
        day_number: 28,
        title: "Space Complexity & Auxiliary Memory",
        topic_name: "Space Analysis",
        section_id: "computational-thinking",
        estimated_minutes: 25,
        description: "Differentiate total space from auxiliary space, measure memory allocations, and analyze recursion stack overhead.",
        concepts: ["Auxiliary Space vs Input Space", "Call Stack Frame Allocation"]
      },
      {
        day_number: 29,
        title: "Brute Force to Optimized Reductions",
        topic_name: "Optimization Strategies",
        section_id: "computational-thinking",
        estimated_minutes: 35,
        description: "Learn systematic techniques to recognize quadratic bottlenecks and optimize them using precomputation or hash tables.",
        concepts: ["Bottleneck Identification", "Trading Space for Time"]
      },
      {
        day_number: 30,
        title: "Linear Recursion Fundamentals & Call Stack",
        topic_name: "Recursion Foundations",
        section_id: "computational-thinking",
        estimated_minutes: 35,
        description: "Master base cases, recursive steps, stack frame allocation, stack unwinding, and recursion depth limits.",
        concepts: ["Base Case & Recursive Step", "Call Stack Unwinding & Frame Allocation"]
      },
      {
        day_number: 31,
        title: "Branching Recursion & Tree Diagramming",
        topic_name: "Branching Recursion",
        section_id: "computational-thinking",
        estimated_minutes: 40,
        description: "Analyze branching recursion, tree representations of recursive calls, redundant work in Fibonacci, and work per level.",
        concepts: ["Multiple Recursive Calls & Branching", "Recursion Tree Level Work"]
      },
      {
        day_number: 32,
        title: "Tail Recursion & State Accumulators",
        topic_name: "Tail Recursion",
        section_id: "computational-thinking",
        estimated_minutes: 30,
        description: "Understand tail calls, accumulator parameters, transforming recursion to iteration, and Python recursion limitations.",
        concepts: ["Tail Call Position", "Accumulator Passing Style"]
      },
      {
        day_number: 33,
        title: "Divide & Conquer Master Theorem",
        topic_name: "Recurrence Analysis",
        section_id: "computational-thinking",
        estimated_minutes: 30,
        description: "Formulate recurrence relations and apply the Master Theorem to divide-and-conquer recurrences T(n) = aT(n/b) + f(n).",
        concepts: ["Divide, Conquer, Combine Paradigm", "Master Theorem Cases"]
      },
      {
        day_number: 34,
        title: "Invariant Design & Loop Verification",
        topic_name: "Algorithmic Invariants",
        section_id: "computational-thinking",
        estimated_minutes: 30,
        description: "Formalize algorithm correctness using loop invariants: initialization, maintenance, and termination proof techniques.",
        concepts: ["Loop Invariant Specification", "Initialization, Maintenance & Termination"]
      },
      {
        day_number: 35,
        title: "Section 3 Milestone & Complexity Audit",
        topic_name: "Complexity Milestone",
        section_id: "computational-thinking",
        estimated_minutes: 45,
        description: "Perform an end-to-end complexity audit and algorithmic proof evaluation across recursion, iterative state, and recurrences.",
        concepts: ["Asymptotic Profiling", "Space-Time Tradeoff Design", "Formal Invariant Proof"]
      },
    ]
  },
  {
    id: "arrays-and-strings",
    section_number: 4,
    title: "Arrays & Strings",
    tagline: "Prefix sums, difference arrays, two pointers, sliding windows, and linear sweeps",
    day_start: 36,
    day_end: 50,
    icon: "Layers",
    days: [
      {
        day_number: 36,
        title: "Static vs Dynamic Arrays & Cache Locality",
        topic_name: "Array Memory",
        section_id: "arrays-and-strings",
        estimated_minutes: 30,
        description: "Understand physical contiguous arrays, memory layouts, CPU cache line caching, and access patterns.",
        concepts: ["Contiguous Physical Memory", "CPU Cache Lines & Stride Locality"]
      },
      {
        day_number: 37,
        title: "1D Prefix Sums & O(1) Range Queries",
        topic_name: "Prefix Sums",
        section_id: "arrays-and-strings",
        estimated_minutes: 35,
        description: "Construct 1D prefix sum arrays to answer range sum queries in O(1) time after O(N) precomputation.",
        concepts: ["Prefix Sum Array Construction", "O(1) Range Sum Formula"]
      },
      {
        day_number: 38,
        title: "Difference Arrays & Range Updates",
        topic_name: "Difference Arrays",
        section_id: "arrays-and-strings",
        estimated_minutes: 35,
        description: "Master difference arrays for O(1) range updates followed by a single O(N) prefix sum reconstruction.",
        concepts: ["Difference Array Invariant", "O(1) Range Updates with O(N) Reconstruction"]
      },
      {
        day_number: 39,
        title: "Two Pointers: Opposing Direction",
        topic_name: "Two Pointers",
        section_id: "arrays-and-strings",
        estimated_minutes: 35,
        description: "Use two pointers moving inward from boundaries to solve two-sum on sorted arrays and maximize area.",
        concepts: ["Converging Boundary Pointers", "Monotonic Search Space Elimination"]
      },
      {
        day_number: 40,
        title: "Two Pointers: Fast & Slow In-Place Writers",
        topic_name: "In-Place Pointers",
        section_id: "arrays-and-strings",
        estimated_minutes: 30,
        description: "Implement fast and slow pointers for in-place array mutation, deduplication, and zero-shifting in O(1) space.",
        concepts: ["Read/Write Pointer Invariant", "In-Place Array Compaction"]
      },
      {
        day_number: 41,
        title: "Sliding Window: Fixed Size",
        topic_name: "Fixed Window",
        section_id: "arrays-and-strings",
        estimated_minutes: 35,
        description: "Apply fixed-size sliding windows to compute rolling sums, max averages, and contiguous subarray statistics in O(N) time.",
        concepts: ["Rolling Window State", "O(1) Element Slide Transition"]
      },
      {
        day_number: 42,
        title: "Sliding Window: Dynamic Size",
        topic_name: "Dynamic Window",
        section_id: "arrays-and-strings",
        estimated_minutes: 40,
        description: "Master dynamic sliding windows that expand and contract based on validity predicates, solving substring problems.",
        concepts: ["Expand-Right & Contract-Left", "Monotonic Condition Predicates"]
      },
      {
        day_number: 43,
        title: "Kadane's Algorithm & Maximum Subarray",
        topic_name: "Subarray Optimization",
        section_id: "arrays-and-strings",
        estimated_minutes: 35,
        description: "Implement Kadane's algorithm to find maximum contiguous subarray sums in O(N) time and O(1) space, with boundary tracking.",
        concepts: ["Kadane's Local vs Global Maxima", "Subarray Reset Condition"]
      },
      {
        day_number: 44,
        title: "In-Place Array Rotation & Reversal",
        topic_name: "Array Manipulations",
        section_id: "arrays-and-strings",
        estimated_minutes: 30,
        description: "Rotate arrays in O(1) auxiliary space using the three-reversal trick, cyclic replacements, and block swapping.",
        concepts: ["Triple-Reversal Algorithm", "Block Swap Invariants"]
      },
      {
        day_number: 45,
        title: "String Parsing & State Machine Tokenization",
        topic_name: "String State Machines",
        section_id: "arrays-and-strings",
        estimated_minutes: 40,
        description: "Build state machines to parse complex strings, validate numeric formats, and implement string-to-integer (atoi).",
        concepts: ["Deterministic Finite Automata (DFA)", "Edge Case Parsing Guardrails"]
      },
      {
        day_number: 46,
        title: "Palindrome Verification & Center Expansion",
        topic_name: "Palindromes",
        section_id: "arrays-and-strings",
        estimated_minutes: 35,
        description: "Verify palindromes using two pointers and find longest palindromic substrings by expanding around 2N-1 centers.",
        concepts: ["Center Expansion Paradigm", "Odd vs Even Length Palindromes"]
      },
      {
        day_number: 47,
        title: "2D Matrix Traversals & Spiral Order",
        topic_name: "Matrix Algorithms",
        section_id: "arrays-and-strings",
        estimated_minutes: 35,
        description: "Navigate 2D grids, extract diagonals, rotate matrices in-place, and traverse boundary spirals without allocations.",
        concepts: ["Matrix Boundary Invariants", "Directional Offset Stepping"]
      },
      {
        day_number: 48,
        title: "2D Prefix Sums & Matrix Accumulation",
        topic_name: "2D Prefix Sums",
        section_id: "arrays-and-strings",
        estimated_minutes: 40,
        description: "Construct 2D prefix sum tables using the inclusion-exclusion principle to query rectangular submatrix sums in O(1) time.",
        concepts: ["Inclusion-Exclusion Principle", "O(1) Submatrix Sum Queries"]
      },
      {
        day_number: 49,
        title: "Intervals: Sorting & Merging Overlaps",
        topic_name: "Interval Scheduling",
        section_id: "arrays-and-strings",
        estimated_minutes: 35,
        description: "Sort intervals, merge overlapping ranges, insert new intervals, and determine interval intersections in O(N log N) time.",
        concepts: ["Interval Overlap Invariant", "Greedy Interval Merging"]
      },
      {
        day_number: 50,
        title: "Section 4 Capstone: Linear Array Patterns",
        topic_name: "Array Capstone",
        section_id: "arrays-and-strings",
        estimated_minutes: 45,
        description: "Synthesize two-pointers, sliding windows, prefix sums, and interval merging into a composite challenge.",
        concepts: ["Pattern Hybridization", "Composite Data Pipelines", "Production Bounds"]
      },
    ]
  },
  {
    id: "searching-and-sorting",
    section_number: 5,
    title: "Searching & Sorting Algorithms",
    tagline: "Binary search boundaries, divide and conquer, Timsort, and non-comparison sorting",
    day_start: 51,
    day_end: 65,
    icon: "Search",
    days: [
      {
        day_number: 51,
        title: "Linear Search vs Binary Search Halving",
        topic_name: "Search Foundations",
        section_id: "searching-and-sorting",
        estimated_minutes: 30,
        description: "Contrast linear search with binary search, proving O(log N) runtime through search-space halving.",
        concepts: ["Linear Scan vs Logarithmic Halving", "Search Space Invariant"]
      },
      {
        day_number: 52,
        title: "Classical Binary Search & Boundary Indices",
        topic_name: "Binary Search Boundaries",
        section_id: "searching-and-sorting",
        estimated_minutes: 35,
        description: "Master boundary conditions, lower and upper bounds, bisect semantics, and avoiding infinite loops in binary search.",
        concepts: ["Midpoint Calculation (L + (R-L)//2)", "Bisect Left & Right Boundaries"]
      },
      {
        day_number: 53,
        title: "Binary Search on Monotonic Answer Space",
        topic_name: "Answer Space Search",
        section_id: "searching-and-sorting",
        estimated_minutes: 40,
        description: "Apply binary search to monotonic answer spaces to find optimal parameters meeting problem constraints.",
        concepts: ["Monotonic Feasibility Predicate", "Answer Space Search Invariant"]
      },
      {
        day_number: 54,
        title: "Rotated Sorted Arrays & Peak Finding",
        topic_name: "Rotated Search",
        section_id: "searching-and-sorting",
        estimated_minutes: 35,
        description: "Find elements in rotated sorted arrays and locate local peaks using modified binary search predicates.",
        concepts: ["Sorted Half Identification", "Inflection Point Invariants"]
      },
      {
        day_number: 55,
        title: "Quadratic Sorts: Bubble, Selection, Insertion",
        topic_name: "Quadratic Sorts",
        section_id: "searching-and-sorting",
        estimated_minutes: 30,
        description: "Analyze Bubble, Selection, and Insertion Sort, proving O(N^2) bounds and stability trade-offs.",
        concepts: ["Insertion Sort Invariant", "Stability in Sorting Algorithms"]
      },
      {
        day_number: 56,
        title: "Merge Sort: Divide, Conquer, Combine",
        topic_name: "Merge Sort",
        section_id: "searching-and-sorting",
        estimated_minutes: 45,
        description: "Implement Merge Sort recursively, trace recursion trees, and prove the O(N log N) stable sorting guarantee.",
        concepts: ["Divide & Conquer Merge Step", "Stable O(N log N) Guarantee"]
      },
      {
        day_number: 57,
        title: "Quick Sort & Hoare Partitioning",
        topic_name: "Quick Sort",
        section_id: "searching-and-sorting",
        estimated_minutes: 45,
        description: "Implement Quick Sort, master Lomuto and Hoare partitioning, analyze expected O(N log N) time, and avoid worst-case pivots.",
        concepts: ["Hoare vs Lomuto Partitioning", "Pivot Selection & O(N^2) Degeneracy"]
      },
      {
        day_number: 58,
        title: "Quickselect: Expected O(N) Kth Order",
        topic_name: "Order Statistics",
        section_id: "searching-and-sorting",
        estimated_minutes: 35,
        description: "Use Quickselect to find the Kth smallest or largest element in expected O(N) time without full sorting.",
        concepts: ["Single-Sided Partition Discarding", "Expected O(N) Recurrence"]
      },
      {
        day_number: 59,
        title: "Counting Sort & Non-Comparison Bounds",
        topic_name: "Counting Sort",
        section_id: "searching-and-sorting",
        estimated_minutes: 35,
        description: "Break the Omega(N log N) comparison barrier with stable Counting Sort over bounded integer ranges.",
        concepts: ["Non-Comparison Sorting Invariant", "Cumulative Frequency Offsets"]
      },
      {
        day_number: 60,
        title: "Radix Sort & Bucket Sort",
        topic_name: "Distribution Sorts",
        section_id: "searching-and-sorting",
        estimated_minutes: 40,
        description: "Implement Radix Sort and Bucket Sort for linear-time sorting of fixed-width integers and uniform numbers.",
        concepts: ["LSD vs MSD Radix Passes", "Bucket Sort Distribution"]
      },
      {
        day_number: 61,
        title: "Python's Timsort Architecture",
        topic_name: "Timsort Architecture",
        section_id: "searching-and-sorting",
        estimated_minutes: 35,
        description: "Examine Python's built-in Timsort algorithm, minruns, run merging invariants, and galloping mode.",
        concepts: ["Natural Runs & Galloping Mode", "Minrun Computation & Stack Balance"]
      },
      {
        day_number: 62,
        title: "Custom Comparators & Multi-Key Sorting",
        topic_name: "Custom Sorting",
        section_id: "searching-and-sorting",
        estimated_minutes: 30,
        description: "Master Python's key parameter in sorted(), multi-level tuple keys, and functools.cmp_to_key.",
        concepts: ["key Function Lambdas", "Multi-Attribute Tuple Keys"]
      },
      {
        day_number: 63,
        title: "Inversion Counting with Merge Sort",
        topic_name: "Inversion Counting",
        section_id: "searching-and-sorting",
        estimated_minutes: 35,
        description: "Count the number of inverted pairs in an array in O(N log N) time by augmenting the merge sort procedure.",
        concepts: ["Inversion Pair Invariant", "Merge Step Accumulation"]
      },
      {
        day_number: 64,
        title: "Ternary Search on Unimodal Functions",
        topic_name: "Ternary Search",
        section_id: "searching-and-sorting",
        estimated_minutes: 30,
        description: "Apply ternary search to find extrema of unimodal functions by dividing intervals into three equal segments.",
        concepts: ["Unimodal Function Extremum", "Trisection Convergence"]
      },
      {
        day_number: 65,
        title: "Section 5 Review & Search/Sort Mastery",
        topic_name: "Search & Sort Milestone",
        section_id: "searching-and-sorting",
        estimated_minutes: 45,
        description: "Synthesize binary search paradigms, comparison and non-comparison sorting algorithms, and custom comparators.",
        concepts: ["Search/Sort Hybridization", "Asymptotic Trade-off Selection", "Adaptive Pipelines"]
      },
    ]
  },
  {
    id: "hashing-and-hash-tables",
    section_number: 6,
    title: "Hashing & Hash Tables",
    tagline: "Collision resolution, frequency mapping, prefix hash maps, and caching architectures",
    day_start: 66,
    day_end: 75,
    icon: "Hash",
    days: [
      {
        day_number: 66,
        title: "Hash Functions, Prime Moduli & Distribution",
        topic_name: "Hash Functions",
        section_id: "hashing-and-hash-tables",
        estimated_minutes: 30,
        description: "Understand hash function properties: uniformity, determinism, avalanche effect, and prime-number modulo bucketing.",
        concepts: ["Uniform Distribution & Avalanche Effect", "Prime Modulo Bucketing"]
      },
      {
        day_number: 67,
        title: "Collision Resolution: Chaining vs Probing",
        topic_name: "Collision Resolution",
        section_id: "hashing-and-hash-tables",
        estimated_minutes: 35,
        description: "Implement collision resolution via separate chaining and open addressing (linear, quadratic, and double hashing).",
        concepts: ["Separate Chaining with Buckets", "Linear & Quadratic Probing"]
      },
      {
        day_number: 68,
        title: "Frequency Counting & Anagram Detection",
        topic_name: "Frequency Hashing",
        section_id: "hashing-and-hash-tables",
        estimated_minutes: 30,
        description: "Use frequency tables and hash maps to solve anagram detection and character count equality in O(N) time.",
        concepts: ["Fixed Alphabet Frequency Arrays", "Valid Anagram Verification"]
      },
      {
        day_number: 69,
        title: "Subarray Sums = K with Prefix Hash Maps",
        topic_name: "Prefix Hash Maps",
        section_id: "hashing-and-hash-tables",
        estimated_minutes: 40,
        description: "Combine prefix sums with hash maps to count contiguous subarrays summing to K in O(N) time.",
        concepts: ["Prefix Sum Frequency Invariant", "Two-Sum Reduction (pref - k)"]
      },
      {
        day_number: 70,
        title: "Grouping & Canonical Equivalence Keys",
        topic_name: "Equivalence Hashing",
        section_id: "hashing-and-hash-tables",
        estimated_minutes: 30,
        description: "Design canonical hash keys to group anagrams, coordinate patterns, and equivalence classes in O(N * K) time.",
        concepts: ["Canonical Representation Tuple", "Multi-Element Grouping"]
      },
      {
        day_number: 71,
        title: "Hash Sets for O(1) Consecutive Sequences",
        topic_name: "Sequence Hashing",
        section_id: "hashing-and-hash-tables",
        estimated_minutes: 35,
        description: "Find the longest consecutive integer sequence in unsorted arrays in O(N) time using O(1) hash set lookups.",
        concepts: ["Sequence Start Verification (num - 1)", "O(1) Set Membership Streak"]
      },
      {
        day_number: 72,
        title: "Rolling Hash & Rabin-Karp Substring Search",
        topic_name: "Rolling Hash",
        section_id: "hashing-and-hash-tables",
        estimated_minutes: 45,
        description: "Implement polynomial rolling hashes and the Rabin-Karp algorithm for average O(N + M) substring matching.",
        concepts: ["Polynomial Rolling Hash Formula", "Spurious Hit Spurious Verification"]
      },
      {
        day_number: 73,
        title: "LRU Cache Architecture via OrderedDict",
        topic_name: "OrderedDict LRU",
        section_id: "hashing-and-hash-tables",
        estimated_minutes: 35,
        description: "Build an O(1) Least Recently Used (LRU) Cache utilizing collections.OrderedDict as an introductory bridge.",
        concepts: ["Doubly Linked Hash Table Concept", "O(1) Move-to-End Eviction"]
      },
      {
        day_number: 74,
        title: "LFU Cache Design Principles",
        topic_name: "LFU Cache",
        section_id: "hashing-and-hash-tables",
        estimated_minutes: 45,
        description: "Architect an O(1) Least Frequently Used (LFU) cache using nested frequency buckets and reciprocal pointers.",
        concepts: ["Frequency Bucket Doubly Linked Lists", "Min-Frequency Pointer Invariant"]
      },
      {
        day_number: 75,
        title: "Section 6 Review & Hashing Mastery",
        topic_name: "Hashing Milestone",
        section_id: "hashing-and-hash-tables",
        estimated_minutes: 40,
        description: "Synthesize hash maps, hash sets, rolling hashes, and cache architectures into a complete caching engine.",
        concepts: ["Hash Table Architectural Trade-offs", "Collision Resistance", "Cache Policy Integration"]
      },
    ]
  },
  {
    id: "linked-lists",
    section_number: 7,
    title: "Linked Lists",
    tagline: "Node pointers, sentinel dummies, in-place reversals, fast/slow runners, and cycles",
    day_start: 76,
    day_end: 85,
    icon: "GitCommit",
    days: [
      {
        day_number: 76,
        title: "Singly Linked List: Structure & Traversal",
        topic_name: "Linked List Basics",
        section_id: "linked-lists",
        estimated_minutes: 30,
        description: "Define ListNode nodes, manage head references, traverse lists, and analyze non-contiguous heap allocations.",
        concepts: ["ListNode Pointer Reference", "Sequential Pointer Traversal"]
      },
      {
        day_number: 77,
        title: "Insertion, Deletion & Dummy Sentinels",
        topic_name: "Sentinel Nodes",
        section_id: "linked-lists",
        estimated_minutes: 35,
        description: "Use dummy sentinel nodes to eliminate special cases when inserting or deleting nodes at list boundaries.",
        concepts: ["Dummy Sentinel Head Node", "Predecessor Pointer Rewiring"]
      },
      {
        day_number: 78,
        title: "In-Place Linked List Pointer Reversal",
        topic_name: "List Reversal",
        section_id: "linked-lists",
        estimated_minutes: 35,
        description: "Reverse singly linked lists iteratively in O(N) time and O(1) space using three pointers (prev, curr, next_node).",
        concepts: ["Three-Pointer Iterative Reversal", "next_node Forward Caching"]
      },
      {
        day_number: 79,
        title: "Fast & Slow Pointers (Tortoise & Hare)",
        topic_name: "Runner Technique",
        section_id: "linked-lists",
        estimated_minutes: 35,
        description: "Use the fast and slow pointer technique to find list midpoints and Kth-from-end nodes in a single traversal.",
        concepts: ["2x Speed Differential", "Midpoint & Kth-from-End Extraction"]
      },
      {
        day_number: 80,
        title: "Floyd's Cycle Detection & Entry Proof",
        topic_name: "Cycle Detection",
        section_id: "linked-lists",
        estimated_minutes: 40,
        description: "Implement Floyd's Cycle Detection algorithm, prove 2k - k = k cycle convergence, and locate cycle start nodes.",
        concepts: ["Floyd's Tortoise & Hare Cycle", "Mathematical Entry Point Derivation"]
      },
      {
        day_number: 81,
        title: "Merge Two Sorted Lists & K-Way Splicing",
        topic_name: "List Merging",
        section_id: "linked-lists",
        estimated_minutes: 35,
        description: "Merge two sorted linked lists in-place in O(N1 + N2) time and introduce K-way list splicing.",
        concepts: ["Sentinel Splice Invariant", "Iterative In-Place Splice"]
      },
      {
        day_number: 82,
        title: "Doubly Linked Lists & Bi-Directional Nodes",
        topic_name: "Doubly Linked Lists",
        section_id: "linked-lists",
        estimated_minutes: 30,
        description: "Implement Doubly Linked Lists, manage prev/next pointers, and achieve O(1) arbitrary node detachment.",
        concepts: ["prev & next Bi-Directional Pointers", "O(1) Self-Detachment"]
      },
      {
        day_number: 83,
        title: "Scratch-Built LRU Cache (DLL + Hash Map)",
        topic_name: "Scratch LRU Cache",
        section_id: "linked-lists",
        estimated_minutes: 45,
        description: "Build a production-grade O(1) LRU Cache from scratch combining a Hash Map with a Doubly Linked List with sentinels.",
        concepts: ["Hash Map to DLL Node Pointers", "O(1) get() and put() Operations"]
      },
      {
        day_number: 84,
        title: "Reverse Nodes in K-Group",
        topic_name: "K-Group Reversal",
        section_id: "linked-lists",
        estimated_minutes: 45,
        description: "Reverse linked lists in groups of K nodes, handling subsegment reversals and boundary reconnects in O(N) time.",
        concepts: ["K-Node Segment Isolation", "Boundary Pointer Re-Wiring"]
      },
      {
        day_number: 85,
        title: "Section 7 Review & Pointer Discipline",
        topic_name: "Linked List Milestone",
        section_id: "linked-lists",
        estimated_minutes: 40,
        description: "Synthesize pointer manipulation disciplines, sentinel architectures, and recursive linked-list sorting.",
        concepts: ["Pointer Leak Prevention", "In-Place List Merge Sort", "Sentinel Standardization"]
      },
    ]
  },
  {
    id: "stacks-and-queues",
    section_number: 8,
    title: "Stacks & Queues",
    tagline: "LIFO/FIFO mechanics, monotonic stacks, sliding window max, and parsing machines",
    day_start: 86,
    day_end: 95,
    icon: "Minimize2",
    days: [
      {
        day_number: 86,
        title: "Stack LIFO Mechanics & Array Backing",
        topic_name: "Stack Foundations",
        section_id: "stacks-and-queues",
        estimated_minutes: 30,
        description: "Understand Last-In-First-Out (LIFO) stack mechanics, amortized O(1) list backing, and underflow guards.",
        concepts: ["LIFO Ordering & Operations", "Stack Overflow & Underflow Guards"]
      },
      {
        day_number: 87,
        title: "Parentheses Matching & Balanced Syntax",
        topic_name: "Balanced Syntax",
        section_id: "stacks-and-queues",
        estimated_minutes: 30,
        description: "Solve balanced parentheses matching with multiple bracket types in O(N) time using a LIFO stack.",
        concepts: ["Closing-to-Opening Hash Map", "Stack Emptiness Termination Invariant"]
      },
      {
        day_number: 88,
        title: "Min-Stack Design with O(1) Retrieval",
        topic_name: "Min-Stack",
        section_id: "stacks-and-queues",
        estimated_minutes: 35,
        description: "Design a stack supporting push, pop, top, and retrieving the minimum element in O(1) auxiliary time.",
        concepts: ["Auxiliary Min-Tracker Stack", "Value-Min State Tuples"]
      },
      {
        day_number: 89,
        title: "Queue FIFO Mechanics & Circular Ring Buffers",
        topic_name: "Queue Foundations",
        section_id: "stacks-and-queues",
        estimated_minutes: 35,
        description: "Implement First-In-First-Out (FIFO) queue semantics, circular array buffers, and avoid list pop(0) penalties.",
        concepts: ["FIFO Ordering & Head/Tail Indices", "Circular Ring Buffer Modulo Math"]
      },
      {
        day_number: 90,
        title: "Implement Queue Using Two Stacks",
        topic_name: "Two-Stack Queue",
        section_id: "stacks-and-queues",
        estimated_minutes: 30,
        description: "Implement a FIFO queue using two LIFO stacks, proving amortized O(1) time per operation via lazy transfers.",
        concepts: ["Input Stack & Output Stack", "Amortized O(1) Transfer Invariant"]
      },
      {
        day_number: 91,
        title: "Monotonic Stack: Next Greater Element",
        topic_name: "Monotonic Stack",
        section_id: "stacks-and-queues",
        estimated_minutes: 40,
        description: "Master the monotonic stack pattern to solve Next Greater Element and stock span problems in linear O(N) time.",
        concepts: ["Monotonically Decreasing Stack", "Immediate Pop Resolution"]
      },
      {
        day_number: 92,
        title: "Monotonic Stack: Largest Histogram Rectangle",
        topic_name: "Histogram Monotonic Stack",
        section_id: "stacks-and-queues",
        estimated_minutes: 45,
        description: "Apply monotonic stacks to compute the largest rectangular area in histograms and maximal binary rectangles in O(N) time.",
        concepts: ["Left & Right Smaller Bounds", "Width Calculation from Popped Index"]
      },
      {
        day_number: 93,
        title: "Monotonic Queue & Sliding Window Maximum",
        topic_name: "Monotonic Queue",
        section_id: "stacks-and-queues",
        estimated_minutes: 40,
        description: "Implement monotonic double-ended queues (deques) to solve the Sliding Window Maximum problem in O(N) time.",
        concepts: ["Monotonically Decreasing Deque", "Out-of-Window Index Eviction"]
      },
      {
        day_number: 94,
        title: "Expression Parsing & Shunting-Yard Algorithm",
        topic_name: "Expression Parsing",
        section_id: "stacks-and-queues",
        estimated_minutes: 45,
        description: "Implement Dijkstra's Shunting-Yard algorithm to parse infix expressions into postfix RPN and evaluate them.",
        concepts: ["Operator Precedence & Associativity", "Dijkstra's Shunting-Yard (Infix to Postfix)"]
      },
      {
        day_number: 95,
        title: "Section 8 Review & Linear State Machines",
        topic_name: "Stacks & Queues Milestone",
        section_id: "stacks-and-queues",
        estimated_minutes: 40,
        description: "Synthesize stacks, queues, deques, and monotonic patterns into a complete expression and state evaluation engine.",
        concepts: ["Linear Data Structure Selection", "State Machine Buffer Coordination", "Amortized Bounds"]
      },
    ]
  },
  {
    id: "trees-and-bst",
    section_number: 9,
    title: "Trees & Binary Search Trees",
    tagline: "Hierarchical DFS/BFS, BST invariants, LCA, Morris traversal, AVL rotations, and tries",
    day_start: 96,
    day_end: 110,
    icon: "GitBranch",
    days: [
      {
        day_number: 96,
        title: "Tree Terminology & Hierarchical Anatomy",
        topic_name: "Tree Foundations",
        section_id: "trees-and-bst",
        estimated_minutes: 30,
        description: "Understand tree terminology: root, leaves, depth, height, ancestor/descendant relationships, and TreeNode classes.",
        concepts: ["Hierarchical Node Anatomy", "Height, Depth & Edge Counts"]
      },
      {
        day_number: 97,
        title: "Recursive Traversals: Pre, In, Post-Order",
        topic_name: "Recursive Traversals",
        section_id: "trees-and-bst",
        estimated_minutes: 35,
        description: "Implement recursive pre-order (NLR), in-order (LNR), and post-order (LRN) binary tree traversals in O(N) time.",
        concepts: ["NLR, LNR, LRN Visiting Orders", "Call Stack Tree Traversal"]
      },
      {
        day_number: 98,
        title: "Iterative Tree Traversals via Explicit Stack",
        topic_name: "Iterative Traversals",
        section_id: "trees-and-bst",
        estimated_minutes: 40,
        description: "Implement pre-order, in-order, and post-order tree traversals iteratively using an explicit stack in O(N) time.",
        concepts: ["Explicit Stack Simulation", "Left-Spine Descent Invariant"]
      },
      {
        day_number: 99,
        title: "BFS & Level-Order Queue Traversal",
        topic_name: "Level-Order BFS",
        section_id: "trees-and-bst",
        estimated_minutes: 35,
        description: "Implement breadth-first search (BFS) level-order traversal on trees using queues, handling level batching.",
        concepts: ["FIFO Queue Level Batching", "Zigzag & Level Width Tracking"]
      },
      {
        day_number: 100,
        title: "Tree Properties: Height, Diameter & Symmetry",
        topic_name: "Tree Properties",
        section_id: "trees-and-bst",
        estimated_minutes: 35,
        description: "Compute tree height, diameter, balance factors, and test tree symmetry using bottom-up post-order DFS in O(N) time.",
        concepts: ["Post-Order State Aggregation", "Global Diameter Calculation (Left + Right)"]
      },
      {
        day_number: 101,
        title: "Binary Search Tree (BST) Invariant & Search",
        topic_name: "BST Invariant",
        section_id: "trees-and-bst",
        estimated_minutes: 35,
        description: "Understand the BST property (Left < Root < Right), validate BST invariants, and perform O(H) key lookups.",
        concepts: ["Left < Root < Right Invariant", "Recursive Boundary Validation (low, high)"]
      },
      {
        day_number: 102,
        title: "BST Insertion, Deletion & Successor Rewiring",
        topic_name: "BST Mutations",
        section_id: "trees-and-bst",
        estimated_minutes: 45,
        description: "Implement BST insertion and deletion, handling 0, 1, and 2-child cases and in-order successor replacements.",
        concepts: ["In-Order Successor Substitution", "Two-Child Deletion Rewiring"]
      },
      {
        day_number: 103,
        title: "Lowest Common Ancestor (LCA) in BST and Tree",
        topic_name: "Lowest Common Ancestor",
        section_id: "trees-and-bst",
        estimated_minutes: 35,
        description: "Find the Lowest Common Ancestor (LCA) in BSTs in O(H) time and general binary trees in O(N) time via DFS.",
        concepts: ["BST Value-Guided Bifurcation", "General Tree Dual-Branch DFS"]
      },
      {
        day_number: 104,
        title: "Tree Serialization & Deserialization",
        topic_name: "Tree Serialization",
        section_id: "trees-and-bst",
        estimated_minutes: 40,
        description: "Serialize binary trees into flat string representations and reconstruct them using pre-order and BFS iterators.",
        concepts: ["Pre-order String Representation", "None Marker Stream Reconstruction"]
      },
      {
        day_number: 105,
        title: "Morris In-Order Traversal & Threaded Pointers",
        topic_name: "Morris Traversal",
        section_id: "trees-and-bst",
        estimated_minutes: 45,
        description: "Traverse binary trees in-order in O(1) auxiliary space using Morris Traversal and threaded binary tree pointers.",
        concepts: ["In-Order Predecessor Rightmost Pointer", "O(1) Auxiliary Space Invariant"]
      },
      {
        day_number: 106,
        title: "Balanced BSTs: AVL Tree Rotations (LL, RR)",
        topic_name: "AVL Rotations",
        section_id: "trees-and-bst",
        estimated_minutes: 45,
        description: "Understand AVL balance factors, height-balance invariants, and implement left and right tree rotations.",
        concepts: ["Height Balance Factor (-1, 0, +1)", "Single & Double Rotations (LL, RR, LR, RL)"]
      },
      {
        day_number: 107,
        title: "Red-Black Tree Principles & Invariants",
        topic_name: "Red-Black Trees",
        section_id: "trees-and-bst",
        estimated_minutes: 35,
        description: "Analyze Red-Black tree color invariants, black-height guarantees, and compare performance trade-offs against AVL trees.",
        concepts: ["Red/Black Color Invariants", "Black-Height Invariant & Recolor Rules"]
      },
      {
        day_number: 108,
        title: "Tries (Prefix Trees): Structure & Lookup",
        topic_name: "Trie Architecture",
        section_id: "trees-and-bst",
        estimated_minutes: 35,
        description: "Build a Trie (Prefix Tree) data structure supporting O(L) word insertion, full-word search, and prefix matching.",
        concepts: ["26-Child Alphabet TrieNode", "is_end Word Termination Flag"]
      },
      {
        day_number: 109,
        title: "Trie Applications: Autocomplete & Wildcards",
        topic_name: "Trie Applications",
        section_id: "trees-and-bst",
        estimated_minutes: 40,
        description: "Apply Tries to autocomplete dictionary queries and wildcard pattern searches using recursive backtracking.",
        concepts: ["DFS Prefix Subtree Collection", "Wildcard '.' Branching Traversal"]
      },
      {
        day_number: 110,
        title: "Section 9 Review & Tree Recursion Mastery",
        topic_name: "Trees Milestone",
        section_id: "trees-and-bst",
        estimated_minutes: 45,
        description: "Synthesize binary tree recursions, BST search invariants, self-balancing rotations, and prefix Trie indexing.",
        concepts: ["Recursive Tree Decomposition", "BST Balancing Trade-offs", "Trie Indexing Integration"]
      },
    ]
  },
  {
    id: "heaps-and-priority-queues",
    section_number: 10,
    title: "Heaps & Priority Queues",
    tagline: "Binary heap arrays, sift-up/down, heapq tie-breakers, streaming medians, and scheduling",
    day_start: 111,
    day_end: 120,
    icon: "TrendingUp",
    days: [
      {
        day_number: 111,
        title: "Binary Heap Layout in Flat Arrays",
        topic_name: "Heap Array Layout",
        section_id: "heaps-and-priority-queues",
        estimated_minutes: 30,
        description: "Examine binary heap flat-array indexing (parent = (i-1)//2, left = 2i+1, right = 2i+2) and complete tree layouts.",
        concepts: ["Complete Binary Tree Property", "0-Indexed Parent/Child Formulas"]
      },
      {
        day_number: 112,
        title: "Heapify, Sift-Up & Sift-Down Mechanics",
        topic_name: "Heap Mechanics",
        section_id: "heaps-and-priority-queues",
        estimated_minutes: 45,
        description: "Implement sift-up and sift-down operations, and prove that bottom-up heapify runs in linear O(N) time.",
        concepts: ["Sift-Up (Bubble-Up) & Sift-Down", "Linear O(N) Bottom-Up Heapify"]
      },
      {
        day_number: 113,
        title: "Python's heapq Module & Tie-Breaker Patterns",
        topic_name: "heapq Mechanics",
        section_id: "heaps-and-priority-queues",
        estimated_minutes: 30,
        description: "Master Python's heapq module, simulate max-heaps via negation, and use counter tie-breakers to prevent comparison crashes.",
        concepts: ["heapq Min-Heap Primitives", "Tuple Tie-Breaker Crash Prevention"]
      },
      {
        day_number: 114,
        title: "Top K Frequent Elements in Data Streams",
        topic_name: "Top-K Streaming",
        section_id: "heaps-and-priority-queues",
        estimated_minutes: 35,
        description: "Find the K most frequent items in continuous streams in O(N log K) time using bounded min-heaps.",
        concepts: ["Bounded Min-Heap of Size K", "O(N log K) Extraction"]
      },
      {
        day_number: 115,
        title: "Merge K Sorted Lists via Min-Heap",
        topic_name: "K-Way Merging",
        section_id: "heaps-and-priority-queues",
        estimated_minutes: 40,
        description: "Merge K sorted lists or streams into a single sorted list in O(N log K) time using priority queue frontiers.",
        concepts: ["Frontier Pointer Min-Heap", "O(N log K) Multi-Stream Merging"]
      },
      {
        day_number: 116,
        title: "Two-Heap Pattern: Median of a Stream",
        topic_name: "Two Heaps",
        section_id: "heaps-and-priority-queues",
        estimated_minutes: 45,
        description: "Implement the two-heap pattern (max-heap for lower half, min-heap for upper half) to find stream medians in O(1) time.",
        concepts: ["Max-Heap (Lower) & Min-Heap (Upper)", "O(1) Median & O(log N) Insertion"]
      },
      {
        day_number: 117,
        title: "Task Scheduler & Priority Reorganization",
        topic_name: "Task Scheduling",
        section_id: "heaps-and-priority-queues",
        estimated_minutes: 40,
        description: "Schedule CPU tasks with cooling intervals using greedy max-heaps and cooldown queue staging in O(N) time.",
        concepts: ["Greedy Max-Frequency Extraction", "Cooldown Queue Waiting Line"]
      },
      {
        day_number: 118,
        title: "Indexed Priority Queue Principles",
        topic_name: "Indexed Priority Queue",
        section_id: "heaps-and-priority-queues",
        estimated_minutes: 45,
        description: "Design an Indexed Priority Queue supporting O(log N) arbitrary priority updates (decrease-key) and deletions.",
        concepts: ["Position Lookup Mapping (Key -> Index)", "O(log N) decrease_key Operation"]
      },
      {
        day_number: 119,
        title: "Kth Smallest Element in Sorted Matrix",
        topic_name: "Matrix Kth Smallest",
        section_id: "heaps-and-priority-queues",
        estimated_minutes: 35,
        description: "Locate the Kth smallest element in row/column sorted matrices using heap frontier exploration in O(K log N) time.",
        concepts: ["Row/Column Frontier Min-Heap", "O(K log(min(K, N))) Search"]
      },
      {
        day_number: 120,
        title: "Section 10 Review & Priority Queue Design",
        topic_name: "Heaps Milestone",
        section_id: "heaps-and-priority-queues",
        estimated_minutes: 45,
        description: "Synthesize binary heap algorithms, running median dual-heaps, and indexed priority queues into a streaming scheduler.",
        concepts: ["Priority Queue Engineering", "Dynamic Rebalancing", "Stream Processing Under SLA"]
      },
    ]
  },
  {
    id: "graphs",
    section_number: 11,
    title: "Graphs & Graph Algorithms",
    tagline: "Adjacency lists, BFS/DFS, topological sort, Dijkstra, DSU, MST, and bridges/SCCs",
    day_start: 121,
    day_end: 135,
    icon: "Share2",
    days: [
      {
        day_number: 121,
        title: "Graph Representations & Adjacency Lists",
        topic_name: "Graph Representations",
        section_id: "graphs",
        estimated_minutes: 30,
        description: "Represent graphs using adjacency lists, adjacency matrices, and edge lists; evaluate density trade-offs.",
        concepts: ["Adjacency List vs Adjacency Matrix", "Directed, Undirected & Weighted Graphs"]
      },
      {
        day_number: 122,
        title: "BFS & Unweighted Shortest Path",
        topic_name: "Breadth-First Search",
        section_id: "graphs",
        estimated_minutes: 35,
        description: "Implement BFS using collections.deque to find shortest paths on unweighted graphs and reconstruct shortest paths.",
        concepts: ["FIFO Queue Level Expansion", "Predecessor Array & Distance Tracking"]
      },
      {
        day_number: 123,
        title: "DFS, Connected Components & Flood Fill",
        topic_name: "Depth-First Search",
        section_id: "graphs",
        estimated_minutes: 35,
        description: "Implement recursive and iterative DFS, count connected components, and solve 2D grid flood fill problems.",
        concepts: ["Recursive DFS Traversal", "Visited Set & Grid Flood Fill"]
      },
      {
        day_number: 124,
        title: "Cycle Detection in Directed Graphs (3-Color)",
        topic_name: "Cycle Detection",
        section_id: "graphs",
        estimated_minutes: 35,
        description: "Detect cycles in directed graphs using three-color DFS marking (Unvisited, Visiting, Visited) and back-edge identification.",
        concepts: ["Three-Color State Marking (White, Gray, Black)", "Back-Edge Detection"]
      },
      {
        day_number: 125,
        title: "Topological Sort: Kahn's In-Degree BFS",
        topic_name: "Topological Sort BFS",
        section_id: "graphs",
        estimated_minutes: 40,
        description: "Implement Kahn's algorithm for topological sorting of DAGs using in-degree arrays and zero-degree queues.",
        concepts: ["In-Degree Array Construction", "Zero-In-Degree FIFO Queue"]
      },
      {
        day_number: 126,
        title: "Topological Sort: DFS Post-Order Reversal",
        topic_name: "Topological Sort DFS",
        section_id: "graphs",
        estimated_minutes: 35,
        description: "Implement topological sort using DFS post-order traversal reversal and detect invalid cyclic dependencies.",
        concepts: ["DFS Finishing Time Post-Order", "Reversed Post-Order Sequence"]
      },
      {
        day_number: 127,
        title: "Bipartite Graph Verification (2-Coloring)",
        topic_name: "Bipartite Verification",
        section_id: "graphs",
        estimated_minutes: 30,
        description: "Determine whether a graph is bipartite (2-colorable) using alternating BFS/DFS vertex coloring in O(V + E) time.",
        concepts: ["Vertex 2-Coloring Invariant", "Odd-Length Cycle Non-Bipartite Rule"]
      },
      {
        day_number: 128,
        title: "Dijkstra's Algorithm: Shortest Paths",
        topic_name: "Dijkstra's Algorithm",
        section_id: "graphs",
        estimated_minutes: 45,
        description: "Implement Dijkstra's algorithm using priority queues to compute single-source shortest paths with non-negative edge weights.",
        concepts: ["Greedy Distance Relaxation (d[v] = d[u] + w)", "Min-Heap Optimization O((V+E) log V)"]
      },
      {
        day_number: 129,
        title: "Bellman-Ford & Negative Cycle Detection",
        topic_name: "Bellman-Ford",
        section_id: "graphs",
        estimated_minutes: 45,
        description: "Implement the Bellman-Ford algorithm in O(V * E) time, handle negative weights, and detect reachable negative cycles.",
        concepts: ["V-1 Edge Relaxation Passes", "Negative Weight Cycle Detection on Pass V"]
      },
      {
        day_number: 130,
        title: "Disjoint Set Union (DSU / Union-Find)",
        topic_name: "Disjoint Set Union",
        section_id: "graphs",
        estimated_minutes: 45,
        description: "Implement Disjoint Set Union (DSU) with Path Compression and Union by Rank, achieving near-O(1) amortized time.",
        concepts: ["Path Compression Invariant", "Union by Rank/Size & Inverse Ackermann O(alpha(N))"]
      },
      {
        day_number: 131,
        title: "Minimum Spanning Tree: Kruskal's with DSU",
        topic_name: "Kruskal's MST",
        section_id: "graphs",
        estimated_minutes: 45,
        description: "Implement Kruskal's algorithm to find Minimum Spanning Trees (MST) by sorting edges and avoiding cycles with DSU.",
        concepts: ["Greedy Edge Weight Sorting", "Cycle Avoidance via DSU"]
      },
      {
        day_number: 132,
        title: "Minimum Spanning Tree: Prim's Algorithm",
        topic_name: "Prim's MST",
        section_id: "graphs",
        estimated_minutes: 40,
        description: "Implement Prim's algorithm for Minimum Spanning Trees using priority queues to select minimum crossing edges.",
        concepts: ["Growing Subtree Frontier Cut", "Min-Heap Crossing Edge Selection"]
      },
      {
        day_number: 133,
        title: "Undirected Bridges & Articulation Points",
        topic_name: "Bridges & Articulation",
        section_id: "graphs",
        estimated_minutes: 45,
        description: "Find all bridges and articulation points in undirected graphs using Tarjan's discovery time (tin) and low-link (low) DFS.",
        concepts: ["DFS Discovery Times (tin)", "Low-Link Values (low) & Bridge Condition (low[v] > tin[u])"]
      },
      {
        day_number: 134,
        title: "Strongly Connected Components (Kosaraju)",
        topic_name: "Strongly Connected Components",
        section_id: "graphs",
        estimated_minutes: 45,
        description: "Implement Kosaraju's two-pass DFS algorithm on graphs and their transposes to find Strongly Connected Components in DAGs.",
        concepts: ["Transpose Graph Reversal", "Kosaraju's Two-Pass DFS Algorithm"]
      },
      {
        day_number: 135,
        title: "Section 11 Review & Graph Synthesis",
        topic_name: "Graph Milestone",
        section_id: "graphs",
        estimated_minutes: 45,
        description: "Synthesize BFS, DFS, topological sorting, Dijkstra, DSU, MSTs, and SCC algorithms into a comprehensive network router.",
        concepts: ["Shortest Path vs MST Selection", "Topological Pipeline Architecture", "Component Condensation"]
      },
    ]
  },
  {
    id: "greedy-algorithms",
    section_number: 12,
    title: "Greedy Algorithms",
    tagline: "Greedy-choice proofs, interval scheduling, reachability frontiers, and two-pass greedy",
    day_start: 136,
    day_end: 145,
    icon: "Zap",
    days: [
      {
        day_number: 136,
        title: "Greedy Choice Property & Exchange Arguments",
        topic_name: "Greedy Foundations",
        section_id: "greedy-algorithms",
        estimated_minutes: 30,
        description: "Understand the Greedy Choice Property, Optimal Substructure, and prove optimality using exchange arguments.",
        concepts: ["Greedy-Choice Property", "Exchange Argument Proof Technique"]
      },
      {
        day_number: 137,
        title: "Activity Selection & Interval Scheduling",
        topic_name: "Activity Selection",
        section_id: "greedy-algorithms",
        estimated_minutes: 35,
        description: "Solve the Activity Selection problem by sorting on earliest finish time, proving optimality via exchange arguments.",
        concepts: ["Earliest Finishing Time Greedy Sort", "Non-Overlapping Choice Invariant"]
      },
      {
        day_number: 138,
        title: "Fractional Knapsack & Value Density Sorting",
        topic_name: "Fractional Knapsack",
        section_id: "greedy-algorithms",
        estimated_minutes: 35,
        description: "Implement the Fractional Knapsack problem in O(N log N) time by greedily sorting items by value-to-weight density.",
        concepts: ["Value-to-Weight Ratio Density", "Continuous Item Partitioning"]
      },
      {
        day_number: 139,
        title: "Huffman Coding & Optimal Prefix Trees",
        topic_name: "Huffman Coding",
        section_id: "greedy-algorithms",
        estimated_minutes: 45,
        description: "Construct optimal variable-length prefix codes using Huffman's algorithm with priority queues in O(N log N) time.",
        concepts: ["Optimal Prefix Code Invariant", "Min-Heap Bottom-Up Tree Merging"]
      },
      {
        day_number: 140,
        title: "Jump Game & Reachability Frontiers",
        topic_name: "Reachability Greedy",
        section_id: "greedy-algorithms",
        estimated_minutes: 35,
        description: "Solve Jump Game I (reachability) and Jump Game II (minimum jumps) using greedy frontier advancement in O(N) time.",
        concepts: ["Max Reachability Frontier Invariant", "Boundary Jump Step Increments"]
      },
      {
        day_number: 141,
        title: "Partition Labels & Last Seen Indices",
        topic_name: "Partition Labels",
        section_id: "greedy-algorithms",
        estimated_minutes: 35,
        description: "Partition strings into maximal parts such that each character appears in at most one part in O(N) time.",
        concepts: ["Last Occurrence Index Hash Map", "Frontier Extension Invariant"]
      },
      {
        day_number: 142,
        title: "Gas Station & Circular Circuit Greedy",
        topic_name: "Circular Greedy",
        section_id: "greedy-algorithms",
        estimated_minutes: 40,
        description: "Determine the starting gas station to complete a circular tour in O(N) time using net balance greedy sweeps.",
        concepts: ["Total Gas >= Total Cost Invariant", "Deficit Reset Starting Point Shift"]
      },
      {
        day_number: 143,
        title: "Candy Distribution: Two-Pass Greedy",
        topic_name: "Two-Pass Greedy",
        section_id: "greedy-algorithms",
        estimated_minutes: 40,
        description: "Solve the Candy distribution problem using two independent greedy passes (left-to-right, right-to-left) in O(N) time.",
        concepts: ["Left-to-Right & Right-to-Left Passes", "Local Rating Maximization"]
      },
      {
        day_number: 144,
        title: "Frequency Decrementing for Uniqueness",
        topic_name: "Unique Frequencies",
        section_id: "greedy-algorithms",
        estimated_minutes: 30,
        description: "Find the minimum character deletions to make all character frequencies unique using greedy decrement sets.",
        concepts: ["Seen-Frequencies Set Invariant", "Greedy Deletion Count Minimization"]
      },
      {
        day_number: 145,
        title: "Section 12 Review & Greedy Proof Formalism",
        topic_name: "Greedy Milestone",
        section_id: "greedy-algorithms",
        estimated_minutes: 45,
        description: "Synthesize greedy choice proofs, interval scheduling, reachability frontiers, and distinguish greedy from DP.",
        concepts: ["Greedy vs Dynamic Programming Discrimination", "Formal Exchange Proofs", "Deadline Scheduling"]
      },
    ]
  },
  {
    id: "dynamic-programming",
    section_number: 13,
    title: "Dynamic Programming",
    tagline: "State formulation, 1D/2D grid DP, knapsack variations, LIS, LCS, and interval DP",
    day_start: 146,
    day_end: 155,
    icon: "Grid",
    days: [
      {
        day_number: 146,
        title: "Memoization vs Tabulation Paradigms",
        topic_name: "DP Foundations",
        section_id: "dynamic-programming",
        estimated_minutes: 35,
        description: "Understand overlapping subproblems, optimal substructure, top-down memoization (lru_cache) vs bottom-up tabulation.",
        concepts: ["Overlapping Subproblems & Optimal Substructure", "Top-Down Memoization vs Bottom-Up Tabulation"]
      },
      {
        day_number: 147,
        title: "1D DP: Climbing Stairs & House Robber",
        topic_name: "1D State Recurrences",
        section_id: "dynamic-programming",
        estimated_minutes: 35,
        description: "Formulate 1D DP recurrences (Climbing Stairs, House Robber) and optimize auxiliary space to O(1) rolling variables.",
        concepts: ["State Transition Recurrence", "O(1) Rolling Variable Space Optimization"]
      },
      {
        day_number: 148,
        title: "2D Grid DP: Unique Paths & Min Path Sum",
        topic_name: "2D Grid DP",
        section_id: "dynamic-programming",
        estimated_minutes: 40,
        description: "Solve grid dynamic programming problems (Unique Paths, Minimum Path Sum) and compress 2D tables into 1D rows in O(M*N) time.",
        concepts: ["2D Grid State dp[r][c]", "In-Place Matrix Space Compression"]
      },
      {
        day_number: 149,
        title: "0/1 Knapsack: Table to 1D Reverse Pass",
        topic_name: "0/1 Knapsack",
        section_id: "dynamic-programming",
        estimated_minutes: 45,
        description: "Master the classical 0/1 Knapsack problem, formulate 2D state tables, and optimize space via 1D reverse-capacity sweeps.",
        concepts: ["Capacity Inclusion-Exclusion Choice", "1D Reverse Traversal to Prevent Item Re-use"]
      },
      {
        day_number: 150,
        title: "Unbounded Knapsack & Coin Change Combinations",
        topic_name: "Unbounded Knapsack",
        section_id: "dynamic-programming",
        estimated_minutes: 45,
        description: "Solve Unbounded Knapsack and Coin Change (min coins and combinations count) using 1D forward capacity loops in O(N * W) time.",
        concepts: ["Forward Capacity Loop Invariant", "Min Coins (Minimization) vs Ways (Counting)"]
      },
      {
        day_number: 151,
        title: "Longest Increasing Subsequence (O(N log N))",
        topic_name: "LIS Optimization",
        section_id: "dynamic-programming",
        estimated_minutes: 45,
        description: "Optimize Longest Increasing Subsequence from O(N^2) DP to O(N log N) using patience sorting and binary search.",
        concepts: ["O(N^2) Tabulation Recurrence", "Patience Sorting & Tails Array O(N log N)"]
      },
      {
        day_number: 152,
        title: "Longest Common Subsequence (LCS)",
        topic_name: "LCS Alignment",
        section_id: "dynamic-programming",
        estimated_minutes: 40,
        description: "Implement Longest Common Subsequence (LCS) for two strings, formulate 2D transitions, and reconstruct alignments.",
        concepts: ["2D Sequence Matching Recurrence", "Backtracking Alignment Reconstruction"]
      },
      {
        day_number: 153,
        title: "Edit Distance (Levenshtein Distance)",
        topic_name: "Edit Distance",
        section_id: "dynamic-programming",
        estimated_minutes: 45,
        description: "Compute the Levenshtein Edit Distance between two strings with insertion, deletion, and replacement operations in O(M*N) time.",
        concepts: ["Insert, Delete, Replace Cost Operations", "2D Distance Matrix Invariant"]
      },
      {
        day_number: 154,
        title: "Interval DP: Matrix Chain & Burst Balloons",
        topic_name: "Interval DP",
        section_id: "dynamic-programming",
        estimated_minutes: 45,
        description: "Master Interval DP by iterating over subarray lengths, formulating boundary transitions (Burst Balloons, Matrix Chain).",
        concepts: ["Subarray Span Iteration (len 2 to N)", "Last Operation Partition Choice"]
      },
      {
        day_number: 155,
        title: "Section 13 Review & Multi-State DP Design",
        topic_name: "DP Milestone",
        section_id: "dynamic-programming",
        estimated_minutes: 45,
        description: "Synthesize 1D, 2D, knapsack, subsequence, interval, and state-machine DP patterns into a comprehensive DP master class.",
        concepts: ["Finite State Machine DP (Buy/Sell/Cooldown)", "Multi-Dimensional State Formulation", "Space Optimization"]
      },
    ]
  },
  {
    id: "advanced-dsa",
    section_number: 14,
    title: "Advanced DSA & Interview Mastery",
    tagline: "Bit manipulation, state-space backtracking, segment trees, system design, and capstone",
    day_start: 156,
    day_end: 160,
    icon: "Award",
    days: [
      {
        day_number: 156,
        title: "Bit Manipulation, Bitmasks & Brian Kernighan",
        topic_name: "Bitmask Mastery",
        section_id: "advanced-dsa",
        estimated_minutes: 35,
        description: "Master bitwise operations, Brian Kernighan's algorithm, power-of-two tests, and subset generation with bitmasks.",
        concepts: ["Brian Kernighan's Algorithm (n & (n-1))", "Bitmask Subsets & State Representation"]
      },
      {
        day_number: 157,
        title: "Backtracking & State-Space Pruning (N-Queens)",
        topic_name: "Backtracking & Pruning",
        section_id: "advanced-dsa",
        estimated_minutes: 45,
        description: "Implement systematic backtracking with search-space pruning, bitmask tracking, and solve the N-Queens problem.",
        concepts: ["State-Space Decision Tree Exploration", "Constraint Propagation & Diagonal Bitmasks"]
      },
      {
        day_number: 158,
        title: "Segment Trees & Fenwick Trees Primer",
        topic_name: "Range Query Trees",
        section_id: "advanced-dsa",
        estimated_minutes: 45,
        description: "Build array-based Segment Trees and Fenwick Trees supporting O(log N) range queries and point updates.",
        concepts: ["Array-Based Segment Tree (2*i, 2*i+1)", "O(log N) Range Query & Point Update"]
      },
      {
        day_number: 159,
        title: "Complex Problem Decomposition & System Design",
        topic_name: "System Decomposition",
        section_id: "advanced-dsa",
        estimated_minutes: 45,
        description: "Decompose complex end-to-end coding interview challenges into interconnected DS/algorithm components.",
        concepts: ["Hybrid Algorithmic Architecture", "Concurrency & Cache Invalidation", "Trade-off Communication"]
      },
      {
        day_number: 160,
        title: "The 160-Day Capstone: Interview Readiness",
        topic_name: "160-Day Capstone",
        section_id: "advanced-dsa",
        estimated_minutes: 60,
        description: "Complete the comprehensive 160-day curriculum capstone, demonstrating complete technical mastery from Python foundations to advanced DSA.",
        concepts: ["Comprehensive Interview Synthesis", "Asymptotic Optimality Verification", "Production-Ready Engineering"]
      },
    ]
  },
];
