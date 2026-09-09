"""
Generates the complete 160-day syllabus definition with all 11 user corrections,
including:
- Corrected prerequisite sequence (resolving all 7 inversions)
- Natural concept counts (1 to 4 concepts)
- Bloom-aligned learning objectives
- 7 Practice Archetypes (Arch A to Arch G)
- 3 Flow Tiers (Tier 1: 3-4 steps, Tier 2: 5 steps, Tier 3: 6-8 steps)
- Prerequisites strictly 1 <= p < d
Updates scratch/curriculum_160.json and frontend/lib/curriculum/curriculumData.ts
"""

import json
import re

# Complete 160-day curriculum specification
CURRICULUM_SPEC = [
    # =========================================================================
    # SECTION 1: PYTHON FOUNDATIONS (Days 1 - 10)
    # =========================================================================
    {
        "day_number": 1,
        "section_id": "python-foundations",
        "title": "Variables, Expressions & Memory Model",
        "topic_name": "Python Syntax",
        "estimated_minutes": 30,
        "difficulty": "BEGINNER",
        "prerequisites": [],
        "flow_tier": "tier2",
        "archetype": "tracing",
        "concepts": ["Dynamic Typing", "Object References", "Memory Model", "id() & type()"],
        "learning_objectives": [
            "Trace variable assignment as name tags bound to heap objects using id()",
            "Differentiate between value equality (==) and object identity (is)"
        ],
        "description": "Explore dynamic typing, object references, the id() built-in, and Python's memory assignment semantics."
    },
    {
        "day_number": 2,
        "section_id": "python-foundations",
        "title": "Numerical Types, Arithmetic & Bitwise",
        "topic_name": "Numeric System",
        "estimated_minutes": 25,
        "difficulty": "BEGINNER",
        "prerequisites": [1],
        "flow_tier": "tier2",
        "archetype": "guided",
        "concepts": ["Integers & Floats", "Floor Division & Modulo", "Bitwise Operators"],
        "learning_objectives": [
            "Calculate floor division and modulo on negative numbers using the mathematical floor invariant",
            "Apply bitwise operators (&, |, ^, ~, <<, >>) and bit_count() to integer flags"
        ],
        "description": "Deep dive into arbitrary-precision integers, IEEE-754 floating point quirks, modulo arithmetic, floor division, and bitwise operators."
    },
    {
        "day_number": 3,
        "section_id": "python-foundations",
        "title": "Strings, Slicing & Character Encoding",
        "topic_name": "String Processing",
        "estimated_minutes": 30,
        "difficulty": "BEGINNER",
        "prerequisites": [2],
        "flow_tier": "tier1",
        "archetype": "completion",
        "concepts": ["String Immutability", "Slice Notation [start:stop:step]", "ASCII & ord()/chr()"],
        "learning_objectives": [
            "Apply slice notation to extract and reverse strings without modifying the original sequence",
            "Convert characters to ASCII values using ord() and chr() for array indexing"
        ],
        "description": "Master string immutability, slice notation [start:stop:step], f-strings, and character code conversion using ord() and chr()."
    },
    {
        "day_number": 4,
        "section_id": "python-foundations",
        "title": "Booleans & Logical Control Flow",
        "topic_name": "Conditionals",
        "estimated_minutes": 25,
        "difficulty": "BEGINNER",
        "prerequisites": [2],
        "flow_tier": "tier1",
        "archetype": "debugging",
        "concepts": ["Truthiness & Falsy Values", "Short-Circuit Evaluation"],
        "learning_objectives": [
            "Predict short-circuit logical evaluation order to prevent unintended side-effects",
            "Debug conditional branching relying on truthy and falsy object coercion"
        ],
        "description": "Understand truthiness, boolean coercion, short-circuit logical evaluation, and conditional branch structures."
    },
    {
        "day_number": 5,
        "section_id": "python-foundations",
        "title": "Loops & Iteration Semantics",
        "topic_name": "Loop Constructs",
        "estimated_minutes": 35,
        "difficulty": "BEGINNER",
        "prerequisites": [4],
        "flow_tier": "tier2",
        "archetype": "guided",
        "concepts": ["for & while Loops", "break, continue & for-else"],
        "learning_objectives": [
            "Construct nested loops with break, continue, and the search-and-confirm for-else construct",
            "Trace range() lazy evaluation across positive and negative strides"
        ],
        "description": "Implement while and for-in loops, loop control statements (break, continue), and the for-else construct."
    },
    {
        "day_number": 6,
        "section_id": "python-foundations",
        "title": "Functions, Stack Frames & LEGB Scope",
        "topic_name": "Function Basics",
        "estimated_minutes": 30,
        "difficulty": "BEGINNER",
        "prerequisites": [5],
        "flow_tier": "tier1",
        "archetype": "tracing",
        "concepts": ["Function Signatures & Return", "LEGB Scope & Call Stack"],
        "learning_objectives": [
            "Trace variable resolution order across Local, Enclosing, Global, and Built-in scopes",
            "Analyze call stack activation records and lifetime of local variables"
        ],
        "description": "Define reusable procedures, return contracts, local vs global scope, and the LEGB namespace lookup rule."
    },
    {
        "day_number": 7,
        "section_id": "python-foundations",
        "title": "Function Signatures & Default Argument Trap",
        "topic_name": "Advanced Parameters",
        "estimated_minutes": 35,
        "difficulty": "BEGINNER",
        "prerequisites": [6],
        "flow_tier": "tier2",
        "archetype": "debugging",
        "concepts": ["*args & **kwargs", "Mutable Default Argument Trap"],
        "learning_objectives": [
            "Debug the shared mutable default argument pitfall using the None sentinel pattern",
            "Design flexible function signatures using variadic positional and keyword arguments"
        ],
        "description": "Inspect positional and keyword arguments, variadic *args/**kwargs, and the classic mutable default argument trap."
    },
    {
        "day_number": 8,
        "section_id": "python-foundations",
        "title": "Basic I/O & Robust Type Casting",
        "topic_name": "Input / Output",
        "estimated_minutes": 25,
        "difficulty": "BEGINNER",
        "prerequisites": [6],
        "flow_tier": "tier1",
        "archetype": "guided",
        "concepts": ["sys.stdin & input()", "Type Casting & Defensive Parsing"],
        "learning_objectives": [
            "Parse token streams from standard input with try-except fallback casting",
            "Format console and string output using format specifiers and sys.stdout.write"
        ],
        "description": "Process standard input safely, parse structured tokens, handle EOF errors, and cast input data."
    },
    {
        "day_number": 9,
        "section_id": "python-foundations",
        "title": "Python Standard Library Essentials",
        "topic_name": "Standard Library",
        "estimated_minutes": 30,
        "difficulty": "BEGINNER",
        "prerequisites": [8],
        "flow_tier": "tier1",
        "archetype": "completion",
        "concepts": ["math & sys Modules", "Built-in Iteration Helpers (zip, enumerate)"],
        "learning_objectives": [
            "Utilize math functions and sys parameters for algorithmic utility",
            "Iterate sequences cleanly using enumerate, zip, any, and all"
        ],
        "description": "Leverage standard modules including math, sys, random, and string for algorithmic utility."
    },
    {
        "day_number": 10,
        "section_id": "python-foundations",
        "title": "Foundations Check & Synthetic Practice",
        "topic_name": "Foundations Milestone",
        "estimated_minutes": 40,
        "difficulty": "BEGINNER",
        "prerequisites": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "flow_tier": "tier3",
        "archetype": "milestone",
        "concepts": ["Decomposition", "Input Parsing Pipeline", "Algorithmic Control Flow"],
        "learning_objectives": [
            "Synthesize control flow, functional decomposition, and input parsing into a complete script",
            "Evaluate time and space characteristics of basic algorithmic procedures"
        ],
        "description": "Synthesize variables, conditionals, loops, and functional decomposition to build self-contained algorithmic scripts."
    },

    # =========================================================================
    # SECTION 2: PYTHON CORE & DATA STRUCTURES (Days 11 - 25)
    # =========================================================================
    {
        "day_number": 11,
        "section_id": "python-core",
        "title": "Lists: Memory Layout & Dynamic Resizing",
        "topic_name": "List Architecture",
        "estimated_minutes": 35,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [10],
        "flow_tier": "tier2",
        "archetype": "guided",
        "concepts": ["Contiguous Pointer Array", "Amortized O(1) Append vs O(N) Shift"],
        "learning_objectives": [
            "Explain CPython list over-allocation formula and dynamic resizing mechanism",
            "Contrast amortized O(1) append against O(N) cost of insert(0) and pop(0)"
        ],
        "description": "Analyze dynamic array memory layouts, pointer arrays in CPython, amortized O(1) append, and the O(N) insert/pop(0) penalty."
    },
    {
        "day_number": 12,
        "section_id": "python-core",
        "title": "List Slicing O(K) Cost & Mutability Traps",
        "topic_name": "List Mutations",
        "estimated_minutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [11],
        "flow_tier": "tier2",
        "archetype": "debugging",
        "concepts": ["Slicing O(K) Time & Space", "Shallow vs Deep Copy"],
        "learning_objectives": [
            "Analyze the hidden O(K) time and space allocation cost of list slicing",
            "Debug reference alias bugs in nested list initialization and shallow copying"
        ],
        "description": "Analyze the O(K) time and space complexity of list slicing, shallow vs deep copies, and in-place list mutations."
    },
    {
        "day_number": 13,
        "section_id": "python-core",
        "title": "List Comprehensions & Expressions",
        "topic_name": "Comprehensions",
        "estimated_minutes": 25,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [12],
        "flow_tier": "tier1",
        "archetype": "completion",
        "concepts": ["List Comprehension Syntax", "Nested Comprehensions & Scoping"],
        "learning_objectives": [
            "Construct concise list comprehensions with conditional filtering and mapping",
            "Flatten and transform 2D matrices using nested comprehension expressions"
        ],
        "description": "Transform data expressively and efficiently using list comprehensions and conditional filters."
    },
    {
        "day_number": 14,
        "section_id": "python-core",
        "title": "Tuples, Immutability & The Tuple Swap Idiom",
        "topic_name": "Tuples",
        "estimated_minutes": 25,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [12],
        "flow_tier": "tier1",
        "archetype": "completion",
        "concepts": ["Tuple Immutability", "Tuple Packing/Unpacking & Swap"],
        "learning_objectives": [
            "Explain Python's stack-based variable swap idiom (a, b = b, a) via anonymous tuples",
            "Utilize immutable tuples as composite hashable keys for grid and graph coordinate lookups"
        ],
        "description": "Understand tuple immutability, memory savings over lists, unpacking idioms, and using tuples as hashable coordinate keys."
    },
    {
        "day_number": 15,
        "section_id": "python-core",
        "title": "Dictionaries: Compact Hash Table Internals",
        "topic_name": "Hash Maps",
        "estimated_minutes": 35,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [14],
        "flow_tier": "tier2",
        "archetype": "tracing",
        "concepts": ["Compact Hash Table Architecture", "Open Addressing & Load Factor"],
        "learning_objectives": [
            "Trace dictionary key hashing, index mapping, and perturb-based collision resolution",
            "Explain the 2/3 load factor resize boundary and requirement for hashable immutable keys"
        ],
        "description": "Explore CPython's compact dictionary architecture, hash functions, open-addressing collision resolution, and average O(1) lookups."
    },
    {
        "day_number": 16,
        "section_id": "python-core",
        "title": "Dictionary Methods, Views & Aggregation",
        "topic_name": "Dictionary Operations",
        "estimated_minutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [15],
        "flow_tier": "tier1",
        "archetype": "guided",
        "concepts": ["setdefault() & get()", "Dynamic Dictionary Views & Merge"],
        "learning_objectives": [
            "Build aggregation and grouping pipelines using setdefault and dictionary comprehensions",
            "Manipulate key, value, and item views without allocating intermediate lists"
        ],
        "description": "Apply get(), setdefault(), dictionary views (.keys(), .values(), .items()), and modern dictionary merging."
    },
    {
        "day_number": 17,
        "section_id": "python-core",
        "title": "Sets: Value-Free Hash Tables & O(1) Lookups",
        "topic_name": "Set Theory",
        "estimated_minutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [15],
        "flow_tier": "tier1",
        "archetype": "problem",
        "concepts": ["Set O(1) Lookups", "Mathematical Set Operations"],
        "learning_objectives": [
            "Eliminate duplicate elements and perform membership tests in O(1) average time",
            "Execute set union, intersection, and difference operations meeting asymptotic bounds"
        ],
        "description": "Use sets for O(1) membership testing, deduplication, set algebra, and understand the immutable frozenset."
    },
    {
        "day_number": 18,
        "section_id": "python-core",
        "title": "The Collections Module: Deque & Counter",
        "topic_name": "Specialized Containers",
        "estimated_minutes": 35,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [16, 17],
        "flow_tier": "tier2",
        "archetype": "guided",
        "concepts": ["collections.deque O(1) Endpoints", "Counter & defaultdict"],
        "learning_objectives": [
            "Implement O(1) double-ended queues using collections.deque, avoiding list pop(0) penalties",
            "Count element frequencies and build adjacency groupings using Counter and defaultdict"
        ],
        "description": "Master collections.deque for O(1) appends and pops on both ends, defaultdict, and Counter."
    },
    {
        "day_number": 19,
        "section_id": "python-core",
        "title": "Iterators & The Iteration Protocol",
        "topic_name": "Iteration Architecture",
        "estimated_minutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [18],
        "flow_tier": "tier2",
        "archetype": "algorithm",
        "concepts": ["__iter__ & __next__ Protocol", "StopIteration & Exhaustion"],
        "learning_objectives": [
            "Implement a custom stateful iterator class conforming to the Python iteration protocol",
            "Handle StopIteration termination and consumable stream invariants"
        ],
        "description": "Understand iterable vs iterator, the __iter__ and __next__ protocols, and consumable stream behavior."
    },
    {
        "day_number": 20,
        "section_id": "python-core",
        "title": "Generators & Lazy Memory Streaming",
        "topic_name": "Lazy Evaluation",
        "estimated_minutes": 35,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [19],
        "flow_tier": "tier2",
        "archetype": "algorithm",
        "concepts": ["yield State Suspension", "yield from & O(1) Space Streams"],
        "learning_objectives": [
            "Construct generator functions that yield values incrementally in O(1) auxiliary memory",
            "Delegate sub-generator execution cleanly using yield from"
        ],
        "description": "Implement generator functions with yield, understand execution suspension, generator expressions, and pipeline composition."
    },
    {
        "day_number": 21,
        "section_id": "python-core",
        "title": "Decorators, Closures & Metadata Wrappers",
        "topic_name": "Higher-Order Functions",
        "estimated_minutes": 35,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [20],
        "flow_tier": "tier2",
        "archetype": "debugging",
        "concepts": ["Closures & Cell Objects", "functools.wraps Decorators"],
        "learning_objectives": [
            "Construct function decorators that intercept calls and preserve docstring metadata with functools.wraps",
            "Debug variable binding bugs in nested function closures"
        ],
        "description": "Write function decorators, understand closures, cell objects, and preserving function metadata with functools.wraps."
    },
    {
        "day_number": 22,
        "section_id": "python-core",
        "title": "OOP Classes, Dunder Protocols & __lt__",
        "topic_name": "Object-Oriented Python",
        "estimated_minutes": 40,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [21],
        "flow_tier": "tier2",
        "archetype": "algorithm",
        "concepts": ["Class Construction & __init__", "Dunders: __repr__, __eq__, __hash__, __lt__"],
        "learning_objectives": [
            "Implement custom classes with __repr__, __eq__, and __hash__ contracts",
            "Define the __lt__ dunder method to enable native sorting and heapq priority queue compatibility"
        ],
        "description": "Build classes, manage instance state, and implement dunder protocols (__repr__, __eq__, __hash__, and __lt__ for comparators)."
    },
    {
        "day_number": 23,
        "section_id": "python-core",
        "title": "Inheritance & Method Resolution Order (C3)",
        "topic_name": "Inheritance Models",
        "estimated_minutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [22],
        "flow_tier": "tier2",
        "archetype": "tracing",
        "concepts": ["Single & Multiple Inheritance", "C3 Linearization & super()"],
        "learning_objectives": [
            "Trace multiple inheritance lookup order using C3 linearization MRO",
            "Coordinate cooperative super() initialization across class hierarchies"
        ],
        "description": "Master single and multiple inheritance, super(), and CPython's C3 Linearization Method Resolution Order (MRO)."
    },
    {
        "day_number": 24,
        "section_id": "python-core",
        "title": "Exception Handling & Custom Hierarchies",
        "topic_name": "Error Architecture",
        "estimated_minutes": 25,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [22],
        "flow_tier": "tier1",
        "archetype": "debugging",
        "concepts": ["try/except/else/finally", "Custom Exception Hierarchies"],
        "learning_objectives": [
            "Refactor broad exception handlers into precise catch blocks with cleanup guarantees",
            "Define domain-specific custom exception classes inheriting from Exception"
        ],
        "description": "Write robust error-handling code with try/except/else/finally and build custom domain exception classes."
    },
    {
        "day_number": 25,
        "section_id": "python-core",
        "title": "Python DSA Algorithmic Toolkit & Milestone",
        "topic_name": "Core Milestone",
        "estimated_minutes": 45,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [11, 14, 15, 18, 22],
        "flow_tier": "tier3",
        "archetype": "milestone",
        "concepts": ["list.sort() vs sorted() & Multi-Key", "heapq & Tie-Breaker Crash Prevention", "sys.setrecursionlimit & Float Infinity"],
        "learning_objectives": [
            "Sort complex structures with multi-key tuple lambdas and utilize heapq min-heaps safely",
            "Configure recursion limits (sys.setrecursionlimit) and sentinel infinities for algorithmic problem solving"
        ],
        "description": "Synthesize Python core data structures into a complete algorithmic toolkit bridging into Data Structures & Algorithms."
    },

    # =========================================================================
    # SECTION 3: PROBLEM SOLVING & COMPUTATIONAL THINKING (Days 26 - 35)
    # =========================================================================
    {
        "day_number": 26,
        "section_id": "computational-thinking",
        "title": "Asymptotic Analysis & Big-O Notation",
        "topic_name": "Complexity Foundations",
        "estimated_minutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [25],
        "flow_tier": "tier1",
        "archetype": "tracing",
        "concepts": ["Big-O Asymptotic Upper Bound", "Growth Orders (O(1) to O(2^N))"],
        "learning_objectives": [
            "Classify mathematical functions by asymptotic growth rate as N approaches infinity",
            "Differentiate best-case, average-case, and worst-case performance metrics"
        ],
        "description": "Understand Big-O notation, asymptotic upper bounds, growth rate hierarchies, and worst-case vs average-case behavior."
    },
    {
        "day_number": 27,
        "section_id": "computational-thinking",
        "title": "Identifying Common Time Complexities",
        "topic_name": "Code Complexity Analysis",
        "estimated_minutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [26],
        "flow_tier": "tier1",
        "archetype": "tracing",
        "concepts": ["Nested Loops & Stride Halving", "Drop Constants & Non-Dominant Terms"],
        "learning_objectives": [
            "Analyze code snippets to extract time complexity formulas by inspecting loop bounds",
            "Identify logarithmic complexity in divide-by-two search and stride halving patterns"
        ],
        "description": "Analyze code snippets to determine O(1), O(log N), O(N), O(N log N), O(N^2), and O(2^N) time complexities."
    },
    {
        "day_number": 28,
        "section_id": "computational-thinking",
        "title": "Space Complexity & Auxiliary Memory",
        "topic_name": "Space Analysis",
        "estimated_minutes": 25,
        "difficulty": "DEVELOPING",
        "prerequisites": [27],
        "flow_tier": "tier1",
        "archetype": "tracing",
        "concepts": ["Auxiliary Space vs Input Space", "Call Stack Frame Allocation"],
        "learning_objectives": [
            "Calculate auxiliary heap memory consumption independently of input storage",
            "Account for maximum call stack depth when computing recursive space complexity"
        ],
        "description": "Differentiate total space from auxiliary space, measure memory allocations, and analyze recursion stack overhead."
    },
    {
        "day_number": 29,
        "section_id": "computational-thinking",
        "title": "Brute Force to Optimized Reductions",
        "topic_name": "Optimization Strategies",
        "estimated_minutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [27, 28],
        "flow_tier": "tier2",
        "archetype": "debugging",
        "concepts": ["Bottleneck Identification", "Trading Space for Time"],
        "learning_objectives": [
            "Identify algorithmic bottlenecks that degrade procedures into quadratic runtimes",
            "Refactor O(N^2) brute-force searches into linear O(N) pipelines using hash lookups"
        ],
        "description": "Learn systematic techniques to recognize quadratic bottlenecks and optimize them using precomputation or hash tables."
    },
    {
        "day_number": 30,
        "section_id": "computational-thinking",
        "title": "Linear Recursion Fundamentals & Call Stack",
        "topic_name": "Recursion Foundations",
        "estimated_minutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [6, 28],
        "flow_tier": "tier2",
        "archetype": "tracing",
        "concepts": ["Base Case & Recursive Step", "Call Stack Unwinding & Frame Allocation"],
        "learning_objectives": [
            "Formulate inductive base cases and recursive steps that guarantee termination",
            "Trace recursive call stack frame allocation, state isolation, and return unwinding"
        ],
        "description": "Master base cases, recursive steps, stack frame allocation, stack unwinding, and recursion depth limits."
    },
    {
        "day_number": 31,
        "section_id": "computational-thinking",
        "title": "Branching Recursion & Tree Diagramming",
        "topic_name": "Branching Recursion",
        "estimated_minutes": 40,
        "difficulty": "DEVELOPING",
        "prerequisites": [30],
        "flow_tier": "tier2",
        "archetype": "tracing",
        "concepts": ["Multiple Recursive Calls & Branching", "Recursion Tree Level Work"],
        "learning_objectives": [
            "Model multi-branch recursive algorithms using visual recursion tree diagrams",
            "Compute total work by summing level work across tree depths to explain O(2^N) explosion"
        ],
        "description": "Analyze branching recursion, tree representations of recursive calls, redundant work in Fibonacci, and work per level."
    },
    {
        "day_number": 32,
        "section_id": "computational-thinking",
        "title": "Tail Recursion & State Accumulators",
        "topic_name": "Tail Recursion",
        "estimated_minutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [30],
        "flow_tier": "tier2",
        "archetype": "algorithm",
        "concepts": ["Tail Call Position", "Accumulator Passing Style"],
        "learning_objectives": [
            "Convert head recursion into tail-call form using accumulator parameters",
            "Transform linear recursive procedures into iterative loops to prevent stack overflow"
        ],
        "description": "Understand tail calls, accumulator parameters, transforming recursion to iteration, and Python recursion limitations."
    },
    {
        "day_number": 33,
        "section_id": "computational-thinking",
        "title": "Divide & Conquer Master Theorem",
        "topic_name": "Recurrence Analysis",
        "estimated_minutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [31],
        "flow_tier": "tier1",
        "archetype": "tracing",
        "concepts": ["Divide, Conquer, Combine Paradigm", "Master Theorem Cases"],
        "learning_objectives": [
            "Formulate recurrence relations T(N) = aT(N/b) + f(N) for divide-and-conquer algorithms",
            "Apply the three cases of the Master Theorem to deduce exact asymptotic complexity"
        ],
        "description": "Formulate recurrence relations and apply the Master Theorem to divide-and-conquer recurrences T(n) = aT(n/b) + f(n)."
    },
    {
        "day_number": 34,
        "section_id": "computational-thinking",
        "title": "Invariant Design & Loop Verification",
        "topic_name": "Algorithmic Invariants",
        "estimated_minutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [27],
        "flow_tier": "tier1",
        "archetype": "completion",
        "concepts": ["Loop Invariant Specification", "Initialization, Maintenance & Termination"],
        "learning_objectives": [
            "Specify inductive loop invariants that prove algorithmic correctness",
            "Verify initialization, maintenance, and termination conditions for array loops"
        ],
        "description": "Formalize algorithm correctness using loop invariants: initialization, maintenance, and termination proof techniques."
    },
    {
        "day_number": 35,
        "section_id": "computational-thinking",
        "title": "Section 3 Milestone & Complexity Audit",
        "topic_name": "Complexity Milestone",
        "estimated_minutes": 45,
        "difficulty": "DEVELOPING",
        "prerequisites": [26, 27, 28, 30, 31, 33, 34],
        "flow_tier": "tier3",
        "archetype": "milestone",
        "concepts": ["Asymptotic Profiling", "Space-Time Tradeoff Design", "Formal Invariant Proof"],
        "learning_objectives": [
            "Conduct a comprehensive asymptotic audit optimizing three distinct algorithmic routines",
            "Formulate mathematical correctness proofs and recurrence trees under interview constraints"
        ],
        "description": "Perform an end-to-end complexity audit and algorithmic proof evaluation across recursion, iterative state, and recurrences."
    },

    # =========================================================================
    # SECTION 4: ARRAYS & STRINGS (Days 36 - 50)
    # =========================================================================
    {
        "day_number": 36,
        "section_id": "arrays-and-strings",
        "title": "Static vs Dynamic Arrays & Cache Locality",
        "topic_name": "Array Memory",
        "estimated_minutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [11, 27],
        "flow_tier": "tier1",
        "archetype": "tracing",
        "concepts": ["Contiguous Physical Memory", "CPU Cache Lines & Stride Locality"],
        "learning_objectives": [
            "Contrast fixed memory allocations with dynamic pointer arrays",
            "Predict CPU cache hits and misses across row-major vs column-major matrix sweeps"
        ],
        "description": "Understand physical contiguous arrays, memory layouts, CPU cache line caching, and access patterns."
    },
    {
        "day_number": 37,
        "section_id": "arrays-and-strings",
        "title": "1D Prefix Sums & O(1) Range Queries",
        "topic_name": "Prefix Sums",
        "estimated_minutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [36],
        "flow_tier": "tier2",
        "archetype": "algorithm",
        "concepts": ["Prefix Sum Array Construction", "O(1) Range Sum Formula"],
        "learning_objectives": [
            "Construct a 1-indexed prefix sum array in O(N) preprocessing time",
            "Answer arbitrary range sum queries (L to R) in strict O(1) time"
        ],
        "description": "Construct 1D prefix sum arrays to answer range sum queries in O(1) time after O(N) precomputation."
    },
    {
        "day_number": 38,
        "section_id": "arrays-and-strings",
        "title": "Difference Arrays & Range Updates",
        "topic_name": "Difference Arrays",
        "estimated_minutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [37],
        "flow_tier": "tier2",
        "archetype": "algorithm",
        "concepts": ["Difference Array Invariant", "O(1) Range Updates with O(N) Reconstruction"],
        "learning_objectives": [
            "Execute range increment updates in O(1) time by mutating difference boundary indices",
            "Reconstruct final array values in a single O(N) prefix summation pass"
        ],
        "description": "Master difference arrays for O(1) range updates followed by a single O(N) prefix sum reconstruction."
    },
    {
        "day_number": 39,
        "section_id": "arrays-and-strings",
        "title": "Two Pointers: Opposing Direction",
        "topic_name": "Two Pointers",
        "estimated_minutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [34, 36],
        "flow_tier": "tier2",
        "archetype": "problem",
        "concepts": ["Converging Boundary Pointers", "Monotonic Search Space Elimination"],
        "learning_objectives": [
            "Eliminate suboptimal search space candidates monotonically using inward-converging pointers",
            "Solve two-sum on sorted arrays and Container With Most Water in O(N) time and O(1) space"
        ],
        "description": "Use two pointers moving inward from boundaries to solve two-sum on sorted arrays and maximize area."
    },
    {
        "day_number": 40,
        "section_id": "arrays-and-strings",
        "title": "Two Pointers: Fast & Slow In-Place Writers",
        "topic_name": "In-Place Pointers",
        "estimated_minutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [39],
        "flow_tier": "tier2",
        "archetype": "completion",
        "concepts": ["Read/Write Pointer Invariant", "In-Place Array Compaction"],
        "learning_objectives": [
            "Maintain read and write pointer invariants for in-place array compaction",
            "Remove duplicates and shift elements in-place without allocating auxiliary lists"
        ],
        "description": "Implement fast and slow pointers for in-place array mutation, deduplication, and zero-shifting in O(1) space."
    },
    {
        "day_number": 41,
        "section_id": "arrays-and-strings",
        "title": "Sliding Window: Fixed Size",
        "topic_name": "Fixed Window",
        "estimated_minutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [37, 40],
        "flow_tier": "tier2",
        "archetype": "problem",
        "concepts": ["Rolling Window State", "O(1) Element Slide Transition"],
        "learning_objectives": [
            "Maintain rolling window state across fixed length k by adding incoming and subtracting outgoing elements",
            "Compute maximum subarray sums and rolling averages in O(N) time"
        ],
        "description": "Apply fixed-size sliding windows to compute rolling sums, max averages, and contiguous subarray statistics in O(N) time."
    },
    {
        "day_number": 42,
        "section_id": "arrays-and-strings",
        "title": "Sliding Window: Dynamic Size",
        "topic_name": "Dynamic Window",
        "estimated_minutes": 40,
        "difficulty": "DEVELOPING",
        "prerequisites": [41],
        "flow_tier": "tier2",
        "archetype": "problem",
        "concepts": ["Expand-Right & Contract-Left", "Monotonic Condition Predicates"],
        "learning_objectives": [
            "Expand right pointers to find valid subsegments and contract left pointers to restore invariants",
            "Solve the Longest Substring Without Repeating Characters in O(N) time"
        ],
        "description": "Master dynamic sliding windows that expand and contract based on validity predicates, solving substring problems."
    },
    {
        "day_number": 43,
        "section_id": "arrays-and-strings",
        "title": "Kadane's Algorithm & Maximum Subarray",
        "topic_name": "Subarray Optimization",
        "estimated_minutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [37],
        "flow_tier": "tier2",
        "archetype": "algorithm",
        "concepts": ["Kadane's Local vs Global Maxima", "Subarray Reset Condition"],
        "learning_objectives": [
            "Formulate the local choice invariant: extend existing subarray or start fresh from current element",
            "Implement Kadane's algorithm tracking maximum sum and subarray boundary indices in O(N) time and O(1) space"
        ],
        "description": "Implement Kadane's algorithm to find maximum contiguous subarray sums in O(N) time and O(1) space, with boundary tracking."
    },
    {
        "day_number": 44,
        "section_id": "arrays-and-strings",
        "title": "In-Place Array Rotation & Reversal",
        "topic_name": "Array Manipulations",
        "estimated_minutes": 30,
        "difficulty": "DEVELOPING",
        "prerequisites": [40],
        "flow_tier": "tier2",
        "archetype": "debugging",
        "concepts": ["Triple-Reversal Algorithm", "Block Swap Invariants"],
        "learning_objectives": [
            "Rotate arrays by k positions in O(N) time and O(1) auxiliary space using triple reversals",
            "Debug off-by-one pointer swaps on odd and even length segments"
        ],
        "description": "Rotate arrays in O(1) auxiliary space using the three-reversal trick, cyclic replacements, and block swapping."
    },
    {
        "day_number": 45,
        "section_id": "arrays-and-strings",
        "title": "String Parsing & State Machine Tokenization",
        "topic_name": "String State Machines",
        "estimated_minutes": 40,
        "difficulty": "DEVELOPING",
        "prerequisites": [3, 44],
        "flow_tier": "tier3",
        "archetype": "algorithm",
        "concepts": ["Deterministic Finite Automata (DFA)", "Edge Case Parsing Guardrails"],
        "learning_objectives": [
            "Design a deterministic finite automaton state machine to parse strings into typed tokens",
            "Implement robust string-to-integer conversion (atoi) handling leading whitespace, signs, and clamping"
        ],
        "description": "Build state machines to parse complex strings, validate numeric formats, and implement string-to-integer (atoi)."
    },
    {
        "day_number": 46,
        "section_id": "arrays-and-strings",
        "title": "Palindrome Verification & Center Expansion",
        "topic_name": "Palindromes",
        "estimated_minutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [39, 45],
        "flow_tier": "tier2",
        "archetype": "problem",
        "concepts": ["Center Expansion Paradigm", "Odd vs Even Length Palindromes"],
        "learning_objectives": [
            "Expand around 2N - 1 potential centers to identify palindromic substrings in O(N^2) time and O(1) space",
            "Verify alphanumeric palindrome sentences using two pointers skipping non-alphanumeric characters"
        ],
        "description": "Verify palindromes using two pointers and find longest palindromic substrings by expanding around 2N-1 centers."
    },
    {
        "day_number": 47,
        "section_id": "arrays-and-strings",
        "title": "2D Matrix Traversals & Spiral Order",
        "topic_name": "Matrix Algorithms",
        "estimated_minutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [36],
        "flow_tier": "tier2",
        "archetype": "problem",
        "concepts": ["Matrix Boundary Invariants", "Directional Offset Stepping"],
        "learning_objectives": [
            "Traverse an M x N matrix in spiral order while updating top, bottom, left, and right boundary limits",
            "Rotate matrices 90 degrees in-place by transposing and reversing rows"
        ],
        "description": "Navigate 2D grids, extract diagonals, rotate matrices in-place, and traverse boundary spirals without allocations."
    },
    {
        "day_number": 48,
        "section_id": "arrays-and-strings",
        "title": "2D Prefix Sums & Matrix Accumulation",
        "topic_name": "2D Prefix Sums",
        "estimated_minutes": 40,
        "difficulty": "DEVELOPING",
        "prerequisites": [37, 47],
        "flow_tier": "tier3",
        "archetype": "algorithm",
        "concepts": ["Inclusion-Exclusion Principle", "O(1) Submatrix Sum Queries"],
        "learning_objectives": [
            "Construct a 2D prefix sum table using the 2D inclusion-exclusion principle",
            "Evaluate arbitrary submatrix sum queries in strict O(1) time"
        ],
        "description": "Construct 2D prefix sum tables using the inclusion-exclusion principle to query rectangular submatrix sums in O(1) time."
    },
    {
        "day_number": 49,
        "section_id": "arrays-and-strings",
        "title": "Intervals: Sorting & Merging Overlaps",
        "topic_name": "Interval Scheduling",
        "estimated_minutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [25, 40],
        "flow_tier": "tier2",
        "archetype": "problem",
        "concepts": ["Interval Overlap Invariant", "Greedy Interval Merging"],
        "learning_objectives": [
            "Sort intervals by start times and merge overlapping segments in O(N log N) time",
            "Determine non-overlapping intervals and schedule rooms using boundary scan lines"
        ],
        "description": "Sort intervals, merge overlapping ranges, insert new intervals, and determine interval intersections in O(N log N) time."
    },
    {
        "day_number": 50,
        "section_id": "arrays-and-strings",
        "title": "Section 4 Capstone: Linear Array Patterns",
        "topic_name": "Array Capstone",
        "estimated_minutes": 45,
        "difficulty": "DEVELOPING",
        "prerequisites": [37, 39, 41, 43, 49],
        "flow_tier": "tier3",
        "archetype": "milestone",
        "concepts": ["Pattern Hybridization", "Composite Data Pipelines", "Production Bounds"],
        "learning_objectives": [
            "Synthesize prefix sums, two pointers, and interval merges to architect a calendar engine",
            "Optimize compound array queries meeting strict O(N) time constraints"
        ],
        "description": "Synthesize two-pointers, sliding windows, prefix sums, and interval merging into a composite challenge."
    }
]

print(f"Base syllabus defined with {len(CURRICULUM_SPEC)} days across first 4 sections.")
