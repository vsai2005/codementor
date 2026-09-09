from .common import (
    CURRICULUM_MAP,
    get_difficulty,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)

def get_sec1_days():
    days = {}

    # DAY 1 (Preserved)
    days[1] = {
        "dayNumber": 1,
        "title": CURRICULUM_MAP[1]["title"],
        "topicName": CURRICULUM_MAP[1]["topic_name"],
        "sectionId": CURRICULUM_MAP[1]["section_id"],
        "estimatedMinutes": CURRICULUM_MAP[1]["estimated_minutes"],
        "difficulty": get_difficulty(1),
        "prerequisites": [],
        "concepts": CURRICULUM_MAP[1]["concepts"],
        "practiceSkills": ["Variable Declaration", "Expression Evaluation", "Memory Model Tracing"],
        "_use_imported_steps": "DAY_1_STEPS",
    }

    # DAY 2 (Preserved)
    days[2] = {
        "dayNumber": 2,
        "title": CURRICULUM_MAP[2]["title"],
        "topicName": CURRICULUM_MAP[2]["topic_name"],
        "sectionId": CURRICULUM_MAP[2]["section_id"],
        "estimatedMinutes": CURRICULUM_MAP[2]["estimated_minutes"],
        "difficulty": get_difficulty(2),
        "prerequisites": [1],
        "concepts": CURRICULUM_MAP[2]["concepts"],
        "practiceSkills": ["Arithmetic Computations", "Modulo Calculations", "Type Casting"],
        "_use_imported_steps": "DAY_2_STEPS",
    }

    # DAY 3: Strings & String Formatting
    days[3] = {
        "dayNumber": 3,
        "title": "Strings & String Formatting",
        "topicName": "String Processing",
        "sectionId": "python-foundations",
        "estimatedMinutes": 30,
        "difficulty": "BEGINNER",
        "prerequisites": [2],
        "concepts": ["String Immutability", "Slice Notation", "f-strings", "Encoding (ASCII/UTF-8)"],
        "practiceSkills": ["String Slicing", "f-string Formatting", "String Immutability Reasoning"],
        "steps": [
            make_explanation_step(
                "day3-step1", 1, "String Immutability & Indexing", "Immutability",
                "Strings as Immutable Unicode Sequences",
                "Understanding memory allocation, 0-based indexing, and why strings cannot be modified in place.",
                [
                    "In Python, a string (`str`) is an ordered, immutable sequence of Unicode code points. Once created in heap memory, its characters cannot be altered in place.",
                    "Python uses 0-based indexing for positive offsets (`0` to `len - 1`) and negative indexing from the end (`-1` to `-len`). Attempting to mutate an index like `text[0] = 'h'` raises a `TypeError: 'str' object does not support item assignment`.",
                    "To modify a string, Python requires allocating a new string object containing the desired transformation."
                ],
                snippets=[{
                    "title": "String Indexing and Immutability",
                    "code": "msg = \"Python\"\nprint(msg[0])   # 'P'\nprint(msg[-1])  # 'n'\n# msg[0] = 'p'  # Raises TypeError!",
                    "language": "python",
                    "caption": "Accessing characters via positive and negative indexing."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Strings Cannot Mutate In-Place",
                    "content": "Any string method like `.upper()` or `.replace()` does not alter the original string. It returns a brand new string object."
                }],
                takeaway="Strings in Python are immutable sequences; all transformations create new string objects."
            ),
            make_explanation_step(
                "day3-step2", 2, "Slice Notation & f-strings", "Slicing & Formatting",
                "Mastering [start:stop:step] and Formatted String Literals",
                "Extract substrings cleanly and format values with Python 3.6+ f-strings.",
                [
                    "The slicing syntax `sequence[start:stop:step]` extracts elements from `start` up to but not including `stop`. Slicing never raises `IndexError` even with out-of-range bounds.",
                    "Omitting `start` defaults to `0`, omitting `stop` defaults to sequence length, and a negative step reverses traversal (e.g. `s[::-1]`).",
                    "Formatted string literals (f-strings) prefix strings with `f\"...\"` and evaluate bracketed expressions `{expr}` at runtime with high performance."
                ],
                snippets=[{
                    "title": "Slicing and f-string Patterns",
                    "code": "text = \"CodeMentor\"\nprefix = text[:4]       # 'Code'\nreversed_text = text[::-1] # 'rotnMeMdoC'\n\nname, score = \"Alice\", 98.5\nprint(f\"{name} scored {score:.1f}%\")",
                    "language": "python",
                    "caption": "Slice bounds and f-string formatting specifiers."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "O(K) Slicing Cost",
                    "content": "Slicing a string of length K allocates a new string of length K, costing O(K) time and space."
                }],
                takeaway="Slice notation [start:stop:step] returns a new string, and f-strings evaluate expressions at runtime."
            ),
            make_checkpoint_step(
                "day3-step3", 3, "String Slicing & Mutability Checkpoint", "Checkpoint",
                "Verify Your Understanding of Strings",
                "Test your mental model of indexing, immutability, and slice bounds.",
                [
                    {
                        "id": "chk-d3-q1",
                        "question": "What is the output of the following snippet?\n\n```python\ns = 'Algorithm'\nres = s[2:7:2]\nprint(res)\n```",
                        "options": [
                            {"id": "A", "label": "'grt'"},
                            {"id": "B", "label": "'loi'"},
                            {"id": "C", "label": "'gor'"},
                            {"id": "D", "label": "'lg'"}
                        ],
                        "correctOptionId": "A",
                        "explanations": {
                            "A": "Correct! In 'Algorithm' (indices 0:A, 1:l, 2:g, 3:o, 4:r, 5:i, 6:t), slice 2:7:2 samples indices 2, 4, and 6, producing 'grt'.",
                            "B": "Incorrect: 1-based indexing was accidentally used.",
                            "C": "Incorrect: Step size was skipped or miscalculated.",
                            "D": "Incorrect: The slice includes index 6 ('t') because 6 < 7."
                        }
                    },
                    {
                        "id": "chk-d3-q2",
                        "question": "What happens when executing `word = 'cat'; word[0] = 'b'`?",
                        "options": [
                            {"id": "A", "label": "word becomes 'bat'"},
                            {"id": "B", "label": "TypeError is raised because strings are immutable"},
                            {"id": "C", "label": "SyntaxError is raised during parsing"},
                            {"id": "D", "label": "word becomes ('b', 'a', 't')"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Python strings cannot be modified in-place; they do not support item assignment.",
                            "B": "Correct! Python raises TypeError: 'str' object does not support item assignment.",
                            "C": "Incorrect: The syntax is valid Python; the error is a runtime TypeError.",
                            "D": "Incorrect: String indexing assignment does not convert strings to tuples."
                        }
                    }
                ],
                takeaway="Strings cannot be modified in place, and slices take indices [start, start+step, ... < stop]."
            ),
            make_practice_step(
                "day3-step4", 4, "Format and Transform Strings", "Practice",
                "Build a Formatted User Tag Generator",
                "Write a Python script that formats usernames and extracts domain handles.",
                "User Tag & Clean Username Generator",
                [
                    "Given `raw_user = '  alice_dev  '` and `domain = 'codementor.io'`, strip whitespace from `raw_user`.",
                    "Extract the first 5 characters of the stripped username.",
                    "Construct `user_handle` formatted as `@<clean_user>#<first5>` using f-strings.",
                    "Print the resulting `user_handle`."
                ],
                """# Day 3 Practice: User Tag Generator
raw_user = "  alice_dev  "
domain = "codementor.io"

# TODO 1: Strip leading and trailing whitespace from raw_user
clean_user = ""

# TODO 2: Slice the first 5 characters from clean_user
user_prefix = ""

# TODO 3: Construct the user handle using an f-string: "@{clean_user}#{user_prefix}"
user_handle = ""

print("User handle:", user_handle)
""",
                """raw_user = "  alice_dev  "
domain = "codementor.io"

clean_user = raw_user.strip()
user_prefix = clean_user[:5]
user_handle = f"@{clean_user}#{user_prefix}"

print("User handle:", user_handle)
""",
                ["User handle: @alice_dev#alice"],
                "Use raw_user.strip() to remove padding spaces, clean_user[:5] for the first 5 letters, and f'@{clean_user}#{user_prefix}'.",
                takeaway="String methods like .strip() return clean copies, and f-strings provide elegant interpolation."
            ),
            make_completion_step(
                "day3-step5", 5, "Strings Mastery & Recap", "Recap",
                3, "Day 3 Complete: Strings & String Formatting",
                "You understand string immutability, slice indexing, and modern formatting.",
                [
                    {
                        "concept": "String Modification",
                        "naiveIntuition": "Change characters directly like text[0] = 'A'",
                        "pythonReality": "Strings are immutable; create a new string via slicing or methods"
                    },
                    {
                        "concept": "Slice Out-of-Bounds",
                        "naiveIntuition": "text[0:100] on a 5-char string crashes with IndexError",
                        "pythonReality": "Slicing gracefully clamps to the valid boundaries without raising an error"
                    }
                ],
                ["String Immutability", "Slice Notation [start:stop:step]", "f-string Interpolation", "String Stripping"],
                get_next_preview(3)
            )
        ]
    }

    # DAY 4: Booleans & Logical Control Flow
    days[4] = {
        "dayNumber": 4,
        "title": "Booleans & Logical Control Flow",
        "topicName": "Boolean Logic",
        "sectionId": "python-foundations",
        "estimatedMinutes": 25,
        "difficulty": "BEGINNER",
        "prerequisites": [3],
        "concepts": ["Truthiness", "Short-circuit Evaluation", "if/elif/else", "Ternary Expressions"],
        "practiceSkills": ["Conditional Branching", "Short-Circuit Logic", "Ternary Evaluation"],
        "steps": [
            make_explanation_step(
                "day4-step1", 1, "Boolean Logic & Truthiness", "Truthiness",
                "Boolean Logic, Truth Values, and Truthiness",
                "Learn how Python evaluates every object as truthy or falsy in boolean contexts.",
                [
                    "Python has a built-in `bool` type with two singleton values: `True` and `False`. In conditional contexts, every Python object has an implicit truth value.",
                    "The following objects evaluate to `False` in boolean contexts: `None`, `False`, numeric zeros (`0`, `0.0`, `0j`), empty collections (`''`, `()`, `[]`, `{}`, `set()`), and objects whose `__bool__()` or `__len__()` returns `0` or `False`.",
                    "All other objects evaluate to `True`. This allows concise idiomatic guards like `if items:` instead of `if len(items) > 0:`."
                ],
                snippets=[{
                    "title": "Truthiness in Action",
                    "code": "empty_list = []\nif not empty_list:\n    print(\"List is empty!\")\n\nval = 42\nprint(bool(val))  # True\nprint(bool(0))    # False",
                    "language": "python",
                    "caption": "Implicit truth testing of objects in conditional statements."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Prefer Pythonic Truth Checks",
                    "content": "Write `if text:` rather than `if text != \"\":`. Python tests truthiness directly."
                }],
                takeaway="Every Python object has a boolean value; empty sequences and zeros evaluate to False."
            ),
            make_explanation_step(
                "day4-step2", 2, "Short-Circuiting & Ternary", "Short-Circuit",
                "Short-Circuit Evaluation and Conditional Expressions",
                "How 'and' and 'or' return operands, and how to write clean ternary expressions.",
                [
                    "Logical operators `and` and `or` use short-circuit evaluation. Python evaluates expressions from left to right and stops as soon as the outcome is certain.",
                    "`a and b` evaluates `a`; if `a` is falsy, it returns `a` immediately without evaluating `b`. If `a` is truthy, it returns `b`.",
                    "`a or b` evaluates `a`; if `a` is truthy, it returns `a` immediately. If `a` is falsy, it returns `b`.",
                    "Ternary conditional expressions use the form: `val_if_true if condition else val_if_false`."
                ],
                snippets=[{
                    "title": "Short-Circuiting and Ternary Syntax",
                    "code": "# Short-circuiting avoids division by zero\ncount, total = 0, 100\navg = (count > 0) and (total / count) # Returns False safely!\n\n# Ternary expression\nage = 20\nstatus = \"Adult\" if age >= 18 else \"Minor\"",
                    "language": "python",
                    "caption": "Using short-circuiting as safety guards."
                }],
                callouts=[{
                    "type": "deep-dive",
                    "title": "Logical Operators Return Operands",
                    "content": "In Python, `x or y` does NOT return True/False; it returns the actual object `x` or `y`!"
                }],
                takeaway="'and' and 'or' return the decisive operand, stopping evaluation as soon as the result is known."
            ),
            make_checkpoint_step(
                "day4-step3", 3, "Logic & Short-Circuit Checkpoint", "Checkpoint",
                "Test Your Mastery of Truthiness and Short-Circuiting",
                "Evaluate operands and determine exact return values.",
                [
                    {
                        "id": "chk-d4-q1",
                        "question": "What is the exact value of the expression `\"default\" or 42`?",
                        "options": [
                            {"id": "A", "label": "True"},
                            {"id": "B", "label": "\"default\""},
                            {"id": "C", "label": "42"},
                            {"id": "D", "label": "False"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: 'or' does not convert the result to a boolean; it returns the decisive operand.",
                            "B": "Correct! Non-empty string 'default' is truthy, so 'or' short-circuits immediately and returns 'default'.",
                            "C": "Incorrect: The right operand is never evaluated because the left operand was already truthy.",
                            "D": "Incorrect: 'default' is truthy."
                        }
                    },
                    {
                        "id": "chk-d4-q2",
                        "question": "Which value is considered FALSY in Python?",
                        "options": [
                            {"id": "A", "label": "\"False\""},
                            {"id": "B", "label": "[0]"},
                            {"id": "C", "label": "0.0"},
                            {"id": "D", "label": "{-1}"}
                        ],
                        "correctOptionId": "C",
                        "explanations": {
                            "A": "Incorrect: A non-empty string is always truthy, even if it contains the word 'False'.",
                            "B": "Incorrect: A non-empty list containing element 0 has length 1 and is truthy.",
                            "C": "Correct! Numeric floating-point zero (0.0) is falsy.",
                            "D": "Incorrect: A set containing elements has length > 0 and is truthy."
                        }
                    }
                ],
                takeaway="Short-circuit logic returns the operand that determined the truth outcome."
            ),
            make_practice_step(
                "day4-step4", 4, "Short-Circuit Guard & Ternary Practice", "Practice",
                "Implement a Safe Division Rate Limiter",
                "Build safe mathematical metrics using short-circuiting and ternary expressions.",
                "Safe Metric Evaluator",
                [
                    "Given `total_requests = 150` and `elapsed_seconds = 0`, compute `requests_per_second`.",
                    "Use short-circuiting to ensure division by zero never occurs: if `elapsed_seconds > 0`, compute `total_requests / elapsed_seconds`; otherwise `0.0`.",
                    "Assign `load_status` to `'HIGH'` if `requests_per_second > 50` else `'NORMAL'` using a ternary expression.",
                    "Print both `requests_per_second` and `load_status`."
                ],
                """# Day 4 Practice: Safe Metric Evaluator
total_requests = 150
elapsed_seconds = 0

# TODO 1: Safely compute rps using ternary or short-circuit logic (default to 0.0 if elapsed_seconds == 0)
requests_per_second = 0.0

# TODO 2: Assign load_status ('HIGH' if requests_per_second > 50 else 'NORMAL')
load_status = ""

print("RPS:", requests_per_second)
print("Status:", load_status)
""",
                """total_requests = 150
elapsed_seconds = 0

requests_per_second = (total_requests / elapsed_seconds) if elapsed_seconds > 0 else 0.0
load_status = "HIGH" if requests_per_second > 50 else "NORMAL"

print("RPS:", requests_per_second)
print("Status:", load_status)
""",
                ["RPS: 0.0", "Status: NORMAL"],
                "Use a ternary check `(total / elapsed) if elapsed > 0 else 0.0` to guard against ZeroDivisionError.",
                takeaway="Guarding expressions with conditions prevents runtime crashes and maintains clean data flow."
            ),
            make_completion_step(
                "day4-step5", 5, "Logic & Control Flow Mastery", "Recap",
                4, "Day 4 Complete: Booleans & Logical Control Flow",
                "You have mastered Python truthiness, short-circuit evaluation, and ternary branching.",
                [
                    {
                        "concept": "Return Value of and/or",
                        "naiveIntuition": "and / or always return True or False",
                        "pythonReality": "They return the actual operand object that finalized the decision"
                    },
                    {
                        "concept": "Empty Containers",
                        "naiveIntuition": "Compare len(lst) == 0",
                        "pythonReality": "Empty collections are natively falsy; write `if not lst:`"
                    }
                ],
                ["Truthiness & Falsy Values", "Short-Circuit Evaluation", "Ternary Expressions", "Safe Guard Conditions"],
                get_next_preview(4)
            )
        ]
    }

    # DAY 5: Loops & Iteration Semantics
    days[5] = {
        "dayNumber": 5,
        "title": "Loops & Iteration Semantics",
        "topicName": "Loops & Iteration",
        "sectionId": "python-foundations",
        "estimatedMinutes": 30,
        "difficulty": "BEGINNER",
        "prerequisites": [4],
        "concepts": ["for / while Loops", "break & continue", "for-else Construct", "range() Mechanics"],
        "practiceSkills": ["Loop Execution Control", "Early Termination with break", "Loop-else Logic"],
        "steps": [
            make_explanation_step(
                "day5-step1", 1, "Loop Mechanisms & range()", "Loops & range",
                "Iteration with for, while, and the Lazy range() Sequence",
                "Understand how Python iterates over collections and generates integer ranges on demand.",
                [
                    "Python's `for` loop is fundamentally a foreach iterator: it pulls elements sequentially from any iterable using the iteration protocol.",
                    "`range(start, stop, step)` represents an immutable sequence of numbers. Crucially, `range` does not allocate all numbers in memory at once; it generates them lazily with $O(1)$ memory overhead.",
                    "`while` loops continue executing as long as their condition remains truthy, making them ideal when the total iteration count is unknown beforehand."
                ],
                snippets=[{
                    "title": "for and while loops with range",
                    "code": "for i in range(1, 6): # 1, 2, 3, 4, 5\n    if i % 2 == 0:\n        continue # skip even numbers\n    print(i)",
                    "language": "python",
                    "caption": "Skipping loop iterations with continue."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "range() is O(1) Memory",
                    "content": "`range(10**9)` consumes the same tiny amount of memory as `range(10)` because it only stores start, stop, and step."
                }],
                takeaway="range() produces integers lazily with O(1) memory, and for loops iterate over any sequence."
            ),
            make_explanation_step(
                "day5-step2", 2, "Loop Control & The else Clause", "break & else",
                "Mastering break, continue, and the Unique for-else Construct",
                "Use loop-else for search patterns without boolean flag variables.",
                [
                    "`break` terminates the innermost enclosing loop immediately.",
                    "`continue` skips the rest of the current iteration and jumps to the next cycle.",
                    "Python loops have an optional `else:` clause. The `else` block executes IF AND ONLY IF the loop finished normally without encountering a `break` statement.",
                    "This pattern elegantly solves search problems: if target is found, break; if loop completes without finding, execute the else fallback."
                ],
                snippets=[{
                    "title": "The Search Pattern with for-else",
                    "code": "nums = [2, 4, 6, 8]\ntarget = 5\n\nfor n in nums:\n    if n == target:\n        print(\"Found!\")\n        break\nelse:\n    print(\"Target not found in list\")",
                    "language": "python",
                    "caption": "The else block executes only if no break occurred."
                }],
                callouts=[{
                    "type": "deep-dive",
                    "title": "Think 'no-break' rather than 'else'",
                    "content": "A helpful mental trick is to read `for ... else:` as `for ... if no break:`."
                }],
                takeaway="The else clause of a loop runs only if the loop ran to completion without hitting a break."
            ),
            make_checkpoint_step(
                "day5-step3", 3, "Loop Control Checkpoint", "Checkpoint",
                "Test Your Mastery of Loop Control Flow",
                "Predict the output of break, continue, and loop-else constructs.",
                [
                    {
                        "id": "chk-d5-q1",
                        "question": "What will this code print?\n\n```python\nfor x in [1, 2, 3]:\n    if x == 2:\n        break\nelse:\n    print('Done')\n```",
                        "options": [
                            {"id": "A", "label": "'Done'"},
                            {"id": "B", "label": "Nothing is printed"},
                            {"id": "C", "label": "SyntaxError on else after for"},
                            {"id": "D", "label": "2"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: The loop executed a break statement when x == 2, so the else block is bypassed.",
                            "B": "Correct! Because x == 2 triggers break, the loop terminates immediately and the else block never executes.",
                            "C": "Incorrect: for-else is valid Python syntax.",
                            "D": "Incorrect: There is no print statement inside the loop."
                        }
                    },
                    {
                        "id": "chk-d5-q2",
                        "question": "How much memory does `range(1_000_000_000)` consume in Python 3?",
                        "options": [
                            {"id": "A", "label": "Around 8 Gigabytes of RAM"},
                            {"id": "B", "label": "A fixed small O(1) memory footprint (~48 bytes)"},
                            {"id": "C", "label": "It depends on whether it is assigned to a variable"},
                            {"id": "D", "label": "MemoryError is raised immediately"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: In Python 2, `range` created a full list, but Python 3 `range` is a lazy sequence.",
                            "B": "Correct! Python 3's range object stores only start, stop, and step in fixed O(1) space.",
                            "C": "Incorrect: range is always a lightweight object regardless of assignment.",
                            "D": "Incorrect: No memory error occurs because elements are computed on the fly."
                        }
                    }
                ],
                takeaway="break skips the loop-else block, and range() generates integers lazily in O(1) space."
            ),
            make_practice_step(
                "day5-step4", 4, "Search with Loop-Else", "Practice",
                "Find First Prime Divisor Using Loop-Else",
                "Implement a prime factor search utilizing loop control and loop-else.",
                "Prime Searcher",
                [
                    "Given integer `candidate = 29`, test if any number from 2 up to 28 divides `candidate` evenly.",
                    "If a divisor `d` is found, print `f'Divisible by {d}'` and `break`.",
                    "In the loop's `else` clause, print `'Number is prime'`.",
                    "Run the code to verify that 29 is correctly identified as prime."
                ],
                """# Day 5 Practice: Prime Searcher
candidate = 29

# TODO: Loop through numbers from 2 up to candidate (exclusive)
# If candidate % d == 0, print f"Divisible by {d}" and break
# In the loop's else block, print "Number is prime"

for d in range(2, candidate):
    if candidate % d == 0:
        print(f"Divisible by {d}")
        break
else:
    # TODO: Print prime confirmation
    pass
""",
                """candidate = 29

for d in range(2, candidate):
    if candidate % d == 0:
        print(f"Divisible by {d}")
        break
else:
    print("Number is prime")
""",
                ["Number is prime"],
                "Place `print('Number is prime')` in the `else:` block aligned with `for`.",
                takeaway="Using for-else avoids clumsy boolean flags when searching for matches."
            ),
            make_completion_step(
                "day5-step5", 5, "Loops Mastery & Recap", "Recap",
                5, "Day 5 Complete: Loops & Iteration Semantics",
                "You have mastered lazy range sequences, loop control, and the for-else search pattern.",
                [
                    {
                        "concept": "Loop Else Clause",
                        "naiveIntuition": "Runs on every loop completion or behaves like if-else",
                        "pythonReality": "Runs ONLY if the loop exits naturally without encountering a break"
                    },
                    {
                        "concept": "range Memory",
                        "naiveIntuition": "range(1000000) stores a million integers in memory",
                        "pythonReality": "range is a lazy generator-like sequence consuming O(1) memory"
                    }
                ],
                ["for & while Loops", "break vs continue", "for-else Construct", "Lazy range() Invariant"],
                get_next_preview(5)
            )
        ]
    }

    # DAY 6: Functions & Variable Scope
    days[6] = {
        "dayNumber": 6,
        "title": "Functions & Variable Scope",
        "topicName": "Functions & Scope",
        "sectionId": "python-foundations",
        "estimatedMinutes": 30,
        "difficulty": "BEGINNER",
        "prerequisites": [5],
        "concepts": ["def & return", "LEGB Rule", "global & nonlocal", "Call Stack Basics"],
        "practiceSkills": ["Function Definition", "Scope Resolution (LEGB)", "Encapsulation"],
        "steps": [
            make_explanation_step(
                "day6-step1", 1, "Functions & The Call Stack", "Functions & Call Stack",
                "Functions, Frame Objects, and the Call Stack",
                "Understand what happens in memory when a function is invoked and returned.",
                [
                    "Functions in Python are defined with the `def` keyword. A function definition creates a function object and binds it to a name in the current scope.",
                    "When a function is called, Python pushes a new stack frame onto the call stack. This frame holds the function's local variables, arguments, and return pointer.",
                    "If a function reaches the end of its body without an explicit `return` statement, it implicitly returns `None`."
                ],
                snippets=[{
                    "title": "Function Call and Frame Lifecycle",
                    "code": "def square(n):\n    res = n * n\n    return res\n\nval = square(5) # Pushes frame, computes 25, pops frame\nprint(val)      # 25",
                    "language": "python",
                    "caption": "Frame creation and value return."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Implicit None Return",
                    "content": "A function with no return statement returns None by default. `print(my_func())` will display `None`."
                }],
                takeaway="Every function call pushes a frame onto the call stack; omitting return returns None."
            ),
            make_explanation_step(
                "day6-step2", 2, "The LEGB Scope Resolution Rule", "LEGB Scope",
                "Variable Scoping: Local, Enclosing, Global, Built-in",
                "How Python searches namespaces to resolve variable names.",
                [
                    "When Python resolves a variable name, it follows the LEGB hierarchy strictly in order:",
                    "1. **Local (L)**: Names assigned inside the current function frame.",
                    "2. **Enclosing (E)**: Names in outer enclosing functions (closures).",
                    "3. **Global (G)**: Names assigned at top-level module scope.",
                    "4. **Built-in (B)**: Python's built-in names (`len`, `range`, `print`, `int`).",
                    "Assigning to a variable inside a function makes it local by default, unless declared `global` or `nonlocal`."
                ],
                snippets=[{
                    "title": "LEGB Scope in Action",
                    "code": "x = 'Global'\n\ndef outer():\n    x = 'Enclosing'\n    def inner():\n        x = 'Local'\n        print(x) # Prints 'Local'\n    inner()\nouter()",
                    "language": "python",
                    "caption": "Python stops searching at the first matching scope in LEGB."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "UnboundLocalError Trap",
                    "content": "Assigning to a variable anywhere in a function marks it as local throughout the ENTIRE function. Reading it before assignment raises `UnboundLocalError`."
                }],
                takeaway="Python resolves names from Local -> Enclosing -> Global -> Built-in (LEGB)."
            ),
            make_checkpoint_step(
                "day6-step3", 3, "Scope & Functions Checkpoint", "Checkpoint",
                "Verify Your Mental Model of Python Scope",
                "Trace name resolution and spot scope pitfalls.",
                [
                    {
                        "id": "chk-d6-q1",
                        "question": "What happens when executing this code?\n\n```python\ncounter = 10\ndef inc():\n    counter += 1\ninc()\n```",
                        "options": [
                            {"id": "A", "label": "counter becomes 11"},
                            {"id": "B", "label": "UnboundLocalError is raised"},
                            {"id": "C", "label": "counter remains 10"},
                            {"id": "D", "label": "NameError: counter is not defined"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: counter is not modified because an error occurs first.",
                            "B": "Correct! Because `counter += 1` involves assignment, Python flags `counter` as a local variable. But it attempts to read it before assignment, raising `UnboundLocalError`.",
                            "C": "Incorrect: The function does not complete execution.",
                            "D": "Incorrect: The specific exception is UnboundLocalError, a subclass of NameError."
                        }
                    },
                    {
                        "id": "chk-d6-q2",
                        "question": "What does a Python function return if there is no explicit `return` statement?",
                        "options": [
                            {"id": "A", "label": "0"},
                            {"id": "B", "label": "False"},
                            {"id": "C", "label": "None"},
                            {"id": "D", "label": "Undefined"}
                        ],
                        "correctOptionId": "C",
                        "explanations": {
                            "A": "Incorrect: 0 is a number, not the default return.",
                            "B": "Incorrect: False is a boolean.",
                            "C": "Correct! Python functions implicitly return the singleton object `None` when execution completes without return.",
                            "D": "Incorrect: JavaScript has 'undefined', but Python uses `None`."
                        }
                    }
                ],
                takeaway="Rebinding variables inside a function makes them local; functions return None by default."
            ),
            make_practice_step(
                "day6-step4", 4, "Write Pure Functions with Scope", "Practice",
                "Implement a Pure Metric Formatter",
                "Build a function that transforms scores without polluting outer variables.",
                "Pure Score Normalizer",
                [
                    "Write a function `normalize_score(raw, max_val)` that computes `(raw / max_val) * 100`.",
                    "If `raw < 0` or `max_val <= 0`, return `0.0`.",
                    "Format the result to 1 decimal place as a float: `round(score, 1)`.",
                    "Call `normalize_score(45, 60)` and print `'Normalized:', result`."
                ],
                """# Day 6 Practice: Pure Score Normalizer

def normalize_score(raw, max_val):
    # TODO 1: Guard against invalid inputs (raw < 0 or max_val <= 0)
    if raw < 0 or max_val <= 0:
        return 0.0
    
    # TODO 2: Compute percentage and round to 1 decimal place
    score = 0.0
    return score

result = normalize_score(45, 60)
print("Normalized:", result)
""",
                """def normalize_score(raw, max_val):
    if raw < 0 or max_val <= 0:
        return 0.0
    return round((raw / max_val) * 100, 1)

result = normalize_score(45, 60)
print("Normalized:", result)
""",
                ["Normalized: 75.0"],
                "Compute (raw / max_val) * 100 and pass it to round(..., 1).",
                takeaway="Pure functions encapsulate calculation without mutating outer scope state."
            ),
            make_completion_step(
                "day6-step5", 5, "Functions & Scope Mastery", "Recap",
                6, "Day 6 Complete: Functions & Variable Scope",
                "You have mastered call stack frame lifecycles, LEGB name resolution, and pure function design.",
                [
                    {
                        "concept": "Assignment in Functions",
                        "naiveIntuition": "Assigning to x reads or writes the global x automatically",
                        "pythonReality": "Any assignment inside a function marks that name as local for the entire function scope"
                    },
                    {
                        "concept": "Missing Return",
                        "naiveIntuition": "Functions without return produce an error or return void",
                        "pythonReality": "They return the singleton object None"
                    }
                ],
                ["def & return Semantics", "Call Stack Frames", "LEGB Rule", "UnboundLocalError Pitfall"],
                get_next_preview(6)
            )
        ]
    }

    # DAY 7: Function Arguments & Signatures
    days[7] = {
        "dayNumber": 7,
        "title": "Function Arguments & Signatures",
        "topicName": "Function Signatures",
        "sectionId": "python-foundations",
        "estimatedMinutes": 30,
        "difficulty": "BEGINNER",
        "prerequisites": [6],
        "concepts": ["*args and **kwargs", "Keyword-Only Args", "Mutable Default Trap", "Type Annotations"],
        "practiceSkills": ["Variadic Arguments", "Default Parameter Safety", "Keyword-Only Parameters"],
        "steps": [
            make_explanation_step(
                "day7-step1", 1, "The Mutable Default Argument Trap", "Default Arg Trap",
                "Why You Must Never Use Mutable Objects as Default Arguments",
                "Understand when default arguments are evaluated in Python.",
                [
                    "A critical pitfall in Python is that **default argument values are evaluated once when the function definition is executed, NOT each time the function is called**.",
                    "If you use a mutable object (like a `list` or `dict`) as a default argument, all function invocations that omit that argument share the **exact same object** in heap memory!",
                    "The idiomatic Pythonic solution is to set the default argument to `None` and initialize a new container inside the function body if the argument is `None`."
                ],
                snippets=[{
                    "title": "The Mutable Default Trap and Fix",
                    "code": "# DANGEROUS:\ndef bad_append(item, target=[]):\n    target.append(item)\n    return target\n\n# IDIOMATIC & SAFE:\ndef safe_append(item, target=None):\n    if target is None:\n        target = []\n    target.append(item)\n    return target",
                    "language": "python",
                    "caption": "Always use None as the default sentinel for mutable arguments."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Shared Mutable State",
                    "content": "`bad_append(1)` followed by `bad_append(2)` returns `[1, 2]` because both calls mutate the single shared list attached to the function object!"
                }],
                takeaway="Default arguments evaluate once at function definition time; use None for mutable defaults."
            ),
            make_explanation_step(
                "day7-step2", 2, "*args, **kwargs & Keyword-Only Arguments", "Variadic & Keyword-Only",
                "Flexibility with Variadic Arguments and Enforced Keyword Arguments",
                "Capture arbitrary positional and keyword arguments cleanly.",
                [
                    "`*args` packs extra positional arguments into a `tuple`.",
                    "`**kwargs` packs extra keyword arguments into a `dict`.",
                    "Placing a bare `*` in the parameter list forces all subsequent parameters to be passed strictly as keyword arguments (keyword-only parameters), preventing ambiguous boolean flags."
                ],
                snippets=[{
                    "title": "Keyword-Only and Variadic Parameters",
                    "code": "def configure(mode, *, timeout=30, verbose=False):\n    print(mode, timeout, verbose)\n\n# configure('prod', 10) # TypeError! timeout must be named\nconfigure('prod', timeout=10) # Valid!",
                    "language": "python",
                    "caption": "Enforcing keyword arguments with bare asterisk."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Self-Documenting Code",
                    "content": "Keyword-only arguments prevent confusing calls like `load_data(True, False, 10)`."
                }],
                takeaway="*args gathers positional tuples, **kwargs gathers keyword dicts, and bare * enforces keyword-only args."
            ),
            make_checkpoint_step(
                "day7-step3", 3, "Argument Signatures Checkpoint", "Checkpoint",
                "Test Your Understanding of Python Parameter Binding",
                "Diagnose default argument mutations and variadic packing.",
                [
                    {
                        "id": "chk-d7-q1",
                        "question": "What is the output of running this code?\n\n```python\ndef add_item(val, items=[]):\n    items.append(val)\n    return items\n\nprint(add_item('A'))\nprint(add_item('B'))\n```",
                        "options": [
                            {"id": "A", "label": "['A'] then ['B']"},
                            {"id": "B", "label": "['A'] then ['A', 'B']"},
                            {"id": "C", "label": "['A', 'B'] then ['A', 'B']"},
                            {"id": "D", "label": "TypeError: default list not allowed"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: The default list is not recreated on the second call.",
                            "B": "Correct! Because default arguments are evaluated once at definition time, both calls mutate the exact same list object.",
                            "C": "Incorrect: The first call produces ['A'] before 'B' is added.",
                            "D": "Incorrect: Python allows mutable defaults, but it creates shared state bugs."
                        }
                    },
                    {
                        "id": "chk-d7-q2",
                        "question": "In `def query(table, *, limit=100):`, how must `limit` be passed?",
                        "options": [
                            {"id": "A", "label": "Only as a positional argument: query('users', 50)"},
                            {"id": "B", "label": "Only as a keyword argument: query('users', limit=50)"},
                            {"id": "C", "label": "Either positional or keyword"},
                            {"id": "D", "label": "It cannot be overridden"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: The bare * prevents positional passing.",
                            "B": "Correct! Parameters defined after a bare * are strictly keyword-only.",
                            "C": "Incorrect: That would be the case without the bare *.",
                            "D": "Incorrect: Keyword-only arguments can be freely overridden by passing limit=value."
                        }
                    }
                ],
                takeaway="Mutable defaults share state across calls; bare * enforces keyword-only parameters."
            ),
            make_practice_step(
                "day7-step4", 4, "Build Robust Function Signature", "Practice",
                "Safe Tag Accumulator with Keyword-Only Options",
                "Create a function that collects tags without mutable default side effects.",
                "Safe Tag Register",
                [
                    "Define a function `register_tags(entity, *tags, prefix='#', existing=None)`.",
                    "If `existing is None`, initialize `existing = []` inside the function.",
                    "Iterate over `tags` and append `f'{prefix}{t}'` to `existing`.",
                    "Return `existing`.",
                    "Call `register_tags('Post1', 'python', 'dsa')` and print the returned list."
                ],
                """# Day 7 Practice: Safe Tag Register

def register_tags(entity, *tags, prefix="#", existing=None):
    # TODO 1: Guard against mutable default side-effects
    if existing is None:
        existing = []
    
    # TODO 2: Format each tag with prefix and append to existing
    for t in tags:
        pass
        
    return existing

result = register_tags("Post1", "python", "dsa")
print("Tags:", result)
""",
                """def register_tags(entity, *tags, prefix="#", existing=None):
    if existing is None:
        existing = []
    for t in tags:
        existing.append(f"{prefix}{t}")
    return existing

result = register_tags("Post1", "python", "dsa")
print("Tags:", result)
""",
                ["Tags: ['#python', '#dsa']"],
                "Use `if existing is None: existing = []` and append `f'{prefix}{t}'` for each tag in `tags`.",
                takeaway="Variadic arguments gather elements into a tuple, while sentinel defaults ensure safety."
            ),
            make_completion_step(
                "day7-step5", 5, "Signatures & Arguments Mastery", "Recap",
                7, "Day 7 Complete: Function Arguments & Signatures",
                "You have mastered variadic arguments, keyword-only enforcement, and the mutable default trap.",
                [
                    {
                        "concept": "Default Argument Timing",
                        "naiveIntuition": "Defaults evaluate each time the function is called",
                        "pythonReality": "Defaults evaluate once at definition time; mutable defaults share state across calls"
                    },
                    {
                        "concept": "Keyword-Only Asterisk",
                        "naiveIntuition": "The * symbol can only be used with an argument name like *args",
                        "pythonReality": "A bare * in the parameter list forces all following parameters to be keyword-only"
                    }
                ],
                ["Mutable Default Trap", "None Sentinel Pattern", "*args & **kwargs Packing", "Keyword-Only Parameters"],
                get_next_preview(7)
            )
        ]
    }

    # DAY 8: Basic I/O & Robust Type Casting
    days[8] = {
        "dayNumber": 8,
        "title": "Basic I/O & Robust Type Casting",
        "topicName": "I/O & Type Casting",
        "sectionId": "python-foundations",
        "estimatedMinutes": 25,
        "difficulty": "BEGINNER",
        "prerequisites": [7],
        "concepts": ["sys.stdin vs input()", "Type Casting", "EOF Handling", "Format Specifiers"],
        "practiceSkills": ["Safe Type Conversion", "Input Parsing", "Exception-Resilient Casting"],
        "steps": [
            make_explanation_step(
                "day8-step1", 1, "Input Streams & Fast I/O", "Input & Streams",
                "Standard Input, sys.stdin, and Type Casting",
                "How Python reads input from terminal and competitive programming streams.",
                [
                    "`input()` reads a single line from standard input and always returns a `str` (stripping the trailing newline).",
                    "For competitive programming and large datasets ($10^5+$ lines), `input()` is slow due to prompt handling. `sys.stdin.readline` is significantly faster because it reads directly from the OS buffer without overhead.",
                    "Because input is always textual, numerical computations require explicit type casting: `int()` or `float()`."
                ],
                snippets=[{
                    "title": "Reading and Casting Multiple Values",
                    "code": "# Parsing a line of space-separated integers\nline = \"10 20 30 40\"\nnums = [int(x) for x in line.split()]\nprint(nums)  # [10, 20, 30, 40]",
                    "language": "python",
                    "caption": "Splitting and casting strings into integers."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Fast I/O Pattern",
                    "content": "In performance-critical input scenarios, use `import sys; input = sys.stdin.readline`."
                }],
                takeaway="Input is always string data; fast I/O uses sys.stdin.readline and explicit casting."
            ),
            make_explanation_step(
                "day8-step2", 2, "Robust Casting & Formatting", "Casting & Specifiers",
                "Handling Conversion Errors and Advanced Format Specifiers",
                "Safely parse numbers without crashing and format outputs with precision.",
                [
                    "Attempting to cast invalid strings like `int('abc')` or `int('3.14')` raises `ValueError`.",
                    "To convert float strings to integers, cast through float first: `int(float('3.14'))` yields `3`.",
                    "Format specifiers in f-strings control width, alignment, and decimal precision: `{val:.2f}` rounds to 2 decimal places, `{val:>10}` right-aligns in a 10-character field."
                ],
                snippets=[{
                    "title": "Format Specifiers in Action",
                    "code": "pi = 3.14159265\nprint(f\"{pi:.3f}\")     # '3.142'\n\nval = 42\nprint(f\"{val:06d}\")    # '000042' (padded with zeros)",
                    "language": "python",
                    "caption": "Zero padding and precision formatting."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "int('3.14') Raises ValueError",
                    "content": "`int()` does not automatically parse decimal points. It expects integer string digits or an explicit base."
                }],
                takeaway="Use try/except for robust type casting and f-string format specifiers for structured output."
            ),
            make_checkpoint_step(
                "day8-step3", 3, "I/O & Casting Checkpoint", "Checkpoint",
                "Test Your Mastery of Python Type Casting and Streams",
                "Diagnose type conversion behavior and format outputs.",
                [
                    {
                        "id": "chk-d8-q1",
                        "question": "What happens when executing `int('45.8')` in Python?",
                        "options": [
                            {"id": "A", "label": "Returns 45 (flooring the value)"},
                            {"id": "B", "label": "Returns 46 (rounding up)"},
                            {"id": "C", "label": "Raises ValueError"},
                            {"id": "D", "label": "Returns 45.8 as a float"}
                        ],
                        "correctOptionId": "C",
                        "explanations": {
                            "A": "Incorrect: int() on a string cannot contain decimal dots.",
                            "B": "Incorrect: Python never rounds strings implicitly.",
                            "C": "Correct! int() on a string literal containing a decimal point raises ValueError: invalid literal for int() with base 10: '45.8'.",
                            "D": "Incorrect: int() never returns a float."
                        }
                    },
                    {
                        "id": "chk-d8-q2",
                        "question": "What does `f'{7:04d}'` produce?",
                        "options": [
                            {"id": "A", "label": "'7000'"},
                            {"id": "B", "label": "'0007'"},
                            {"id": "C", "label": "'   7'"},
                            {"id": "D", "label": "'7.0000'"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Zero padding pads on the left.",
                            "B": "Correct! :04d formats an integer with width 4, padding leading spaces with zeros, giving '0007'.",
                            "C": "Incorrect: :4d without 0 would pad with spaces.",
                            "D": "Incorrect: The format specifies integer 'd', not float 'f'."
                        }
                    }
                ],
                takeaway="int() on a string with decimal raises ValueError; :04d zero-pads integers to width 4."
            ),
            make_practice_step(
                "day8-step4", 4, "Robust Input Parser", "Practice",
                "Parse and Aggregate Mixed Sensor Readings",
                "Write a parser that extracts valid numbers from dirty sensor string records.",
                "Sensor Data Stream Parser",
                [
                    "Given `raw_records = [' 42 ', '15.5', 'ERROR', '99', 'N/A', '3.14']`.",
                    "Iterate over `raw_records`, strip whitespace, and attempt to convert each item to a `float`.",
                    "If conversion fails, ignore the item.",
                    "Calculate the sum of all valid numbers, rounded to 2 decimal places.",
                    "Print `'Valid count:', len(valid_nums)` and `'Total sum:', total_sum`."
                ],
                """# Day 8 Practice: Sensor Data Stream Parser
raw_records = [" 42 ", "15.5", "ERROR", "99", "N/A", "3.14"]

valid_nums = []

# TODO: Parse raw_records safely
for rec in raw_records:
    # Try converting rec.strip() to float; if ValueError occurs, continue
    pass

total_sum = round(sum(valid_nums), 2)
print("Valid count:", len(valid_nums))
print("Total sum:", total_sum)
""",
                """raw_records = [" 42 ", "15.5", "ERROR", "99", "N/A", "3.14"]

valid_nums = []
for rec in raw_records:
    try:
        val = float(rec.strip())
        valid_nums.append(val)
    except ValueError:
        continue

total_sum = round(sum(valid_nums), 2)
print("Valid count:", len(valid_nums))
print("Total sum:", total_sum)
""",
                ["Valid count: 4", "Total sum: 159.64"],
                "Use a try / except ValueError block around float(rec.strip()) to safely filter out corrupted records.",
                takeaway="Defensive type casting with try/except ensures robust processing of external streams."
            ),
            make_completion_step(
                "day8-step5", 5, "I/O & Type Casting Mastery", "Recap",
                8, "Day 8 Complete: Basic I/O & Robust Type Casting",
                "You have mastered stream processing, conversion exception safety, and format specifiers.",
                [
                    {
                        "concept": "int() on Float String",
                        "naiveIntuition": "int('12.34') will truncate to 12",
                        "pythonReality": "It raises ValueError; you must parse as float first: int(float('12.34'))"
                    },
                    {
                        "concept": "input() Speed",
                        "naiveIntuition": "input() is identical in speed to sys.stdin.readline()",
                        "pythonReality": "input() has significant interactive overhead; sys.stdin.readline is 3-5x faster"
                    }
                ],
                ["sys.stdin vs input()", "Type Casting Invariants", "Format Specifiers (:04d, :.2f)", "Defensive ValueError Handling"],
                get_next_preview(8)
            )
        ]
    }

    # DAY 9: Python Standard Library Essentials
    days[9] = {
        "dayNumber": 9,
        "title": "Python Standard Library Essentials",
        "topicName": "Standard Library",
        "sectionId": "python-foundations",
        "estimatedMinutes": 30,
        "difficulty": "BEGINNER",
        "prerequisites": [8],
        "concepts": ["math Module", "sys Module", "random Module", "Builtin Functions"],
        "practiceSkills": ["Math Utility Usage", "System Introspection", "Builtin Combinations"],
        "steps": [
            make_explanation_step(
                "day9-step1", 1, "The math & sys Modules", "math & sys Modules",
                "Standard Library Powerhouse: math and sys",
                "Leverage C-accelerated math routines and system properties.",
                [
                    "Python's `math` module provides high-speed C-level mathematical functions: `math.gcd(a, b)`, `math.isqrt(n)` (integer square root), `math.comb(n, k)`, `math.ceil()`, and `math.floor()`.",
                    "`math.isqrt(n)` computes $\\lfloor\\sqrt{n}\\rfloor$ using exact integer arithmetic without floating-point precision inaccuracies—vital for number theory and prime testing.",
                    "The `sys` module provides system-level information: `sys.maxsize` (maximum addressable integer pointer size), `sys.setrecursionlimit()`, and `sys.getsizeof()`."
                ],
                snippets=[{
                    "title": "math and sys Essentials",
                    "code": "import math, sys\n\nprint(math.gcd(48, 180)) # 12\nprint(math.isqrt(27))    # 5 (exact integer floor)\nprint(sys.maxsize > 2**31) # True (on 64-bit platforms)",
                    "language": "python",
                    "caption": "C-accelerated math primitives."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Use math.isqrt instead of int(n**0.5)",
                    "content": "For large numbers ($n > 10^{15}$), `float(n**0.5)` loses precision bits. `math.isqrt(n)` is mathematically exact."
                }],
                takeaway="math.gcd and math.isqrt provide exact, C-optimized numerical operations."
            ),
            make_explanation_step(
                "day9-step2", 2, "Essential Built-ins: zip, enumerate, any, all", "Core Built-ins",
                "Idiomatic Iteration with enumerate, zip, any, and all",
                "Replace manual indexing loops with clean built-in iterators.",
                [
                    "`enumerate(iterable, start=0)` yields `(index, item)` tuples, eliminating manual index counters.",
                    "`zip(*iterables)` aggregates elements from each iterable in parallel, stopping when the shortest iterable is exhausted.",
                    "`any(iterable)` returns `True` if at least one element is truthy (short-circuiting early).",
                    "`all(iterable)` returns `True` only if every element is truthy."
                ],
                snippets=[{
                    "title": "Built-ins in Action",
                    "code": "names = ['Alice', 'Bob', 'Charlie']\nfor idx, name in enumerate(names, start=1):\n    print(f'{idx}. {name}')\n\nscores = [85, 92, 78]\nfor name, score in zip(names, scores):\n    print(f'{name}: {score}')",
                    "language": "python",
                    "caption": "Clean pairing and index tracking."
                }],
                callouts=[{
                    "type": "deep-dive",
                    "title": "any and all Short-Circuit",
                    "content": "`any([False, True, crash()])` will NEVER call `crash()` because it short-circuits on `True`."
                }],
                takeaway="enumerate tracks indices cleanly, zip pairs sequences, and any/all provide short-circuiting tests."
            ),
            make_checkpoint_step(
                "day9-step3", 3, "Standard Library Checkpoint", "Checkpoint",
                "Verify Your Command of Standard Utilities",
                "Evaluate zip, enumerate, and math routines.",
                [
                    {
                        "id": "chk-d9-q1",
                        "question": "What is the result of `list(zip([1, 2, 3], ['a', 'b']))`?",
                        "options": [
                            {"id": "A", "label": "[(1, 'a'), (2, 'b'), (3, None)]"},
                            {"id": "B", "label": "[(1, 'a'), (2, 'b')]"},
                            {"id": "C", "label": "ValueError: unequal sequence lengths"},
                            {"id": "D", "label": "[(1, 'a'), (2, 'b'), (3, '')]"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: zip() does not pad with None (that is itertools.zip_longest).",
                            "B": "Correct! Standard zip() stops as soon as the shortest input sequence is exhausted.",
                            "C": "Incorrect: zip() does not raise ValueError on mismatched lengths.",
                            "D": "Incorrect: No padding occurs."
                        }
                    },
                    {
                        "id": "chk-d9-q2",
                        "question": "Why is `math.isqrt(n)` preferred over `int(math.sqrt(n))` for large integers?",
                        "options": [
                            {"id": "A", "label": "math.sqrt() is deprecated in Python 3"},
                            {"id": "B", "label": "math.sqrt() converts to a 64-bit float, causing precision loss for n > 2^53"},
                            {"id": "C", "label": "math.isqrt() returns a floating point number"},
                            {"id": "D", "label": "math.isqrt() only works for prime numbers"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: math.sqrt() is not deprecated.",
                            "B": "Correct! Floats have 53 bits of precision (~15-17 decimal digits). For large integers, math.sqrt loses precision, while math.isqrt uses exact integer arithmetic.",
                            "C": "Incorrect: math.isqrt() returns an integer.",
                            "D": "Incorrect: math.isqrt works on all non-negative integers."
                        }
                    }
                ],
                takeaway="zip() terminates at the shortest input; math.isqrt() preserves exact integer precision."
            ),
            make_practice_step(
                "day9-step4", 4, "Leaderboard Pairer with zip and enumerate", "Practice",
                "Construct Formatted Ranked Leaderboard",
                "Combine zip and enumerate to rank player scores.",
                "Leaderboard Formatter",
                [
                    "Given `players = ['Diana', 'Bruce', 'Clark']` and `scores = [950, 890, 920]`.",
                    "Pair each player with their score, and sort the pairs in descending order of score.",
                    "Enumerate through the sorted leaderboard starting from rank 1.",
                    "Print each entry formatted as `f'{rank}. {player} - {score} pts'`."
                ],
                """# Day 9 Practice: Leaderboard Formatter
players = ["Diana", "Bruce", "Clark"]
scores = [950, 890, 920]

# TODO 1: Pair players with scores using zip
pairs = list(zip(players, scores))

# TODO 2: Sort pairs descending by score (score is at index 1 of the tuple)
sorted_pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

# TODO 3: Enumerate starting at rank 1 and print each line
for rank, (player, score) in enumerate(sorted_pairs, start=1):
    print(f"{rank}. {player} - {score} pts")
""",
                """players = ["Diana", "Bruce", "Clark"]
scores = [950, 890, 920]

pairs = list(zip(players, scores))
sorted_pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

for rank, (player, score) in enumerate(sorted_pairs, start=1):
    print(f"{rank}. {player} - {score} pts")
""",
                ["1. Diana - 950 pts", "2. Clark - 920 pts", "3. Bruce - 890 pts"],
                "Combine zip(players, scores) and enumerate(sorted_pairs, start=1) to generate ranked outputs.",
                takeaway="Combining built-in iterators like zip and enumerate produces expressive, idiomatic code."
            ),
            make_completion_step(
                "day9-step5", 5, "Standard Library Essentials Mastery", "Recap",
                9, "Day 9 Complete: Python Standard Library Essentials",
                "You have mastered math modules, system properties, and core built-in iterators.",
                [
                    {
                        "concept": "zip Length Handling",
                        "naiveIntuition": "zip pads missing values from shorter lists",
                        "pythonReality": "Standard zip stops at the shortest list; use itertools.zip_longest for padding"
                    },
                    {
                        "concept": "Integer Square Root",
                        "naiveIntuition": "int(n**0.5) is safe for all integers",
                        "pythonReality": "Floating point casting loses precision for large numbers; use math.isqrt(n)"
                    }
                ],
                ["math.gcd & math.isqrt", "enumerate(seq, start=1)", "zip(*iterables) Semantics", "any() & all() Short-Circuiting"],
                get_next_preview(9)
            )
        ]
    }

    # DAY 10: Section 1 Review & Foundations Synthesis
    days[10] = {
        "dayNumber": 10,
        "title": "Foundations Check & Synthetic Practice",
        "topicName": "Section 1 Synthesis",
        "sectionId": "python-foundations",
        "estimatedMinutes": 35,
        "difficulty": "BEGINNER",
        "prerequisites": [9],
        "concepts": ["Control Flow Synthesis", "Decomposition", "Edge Case Handling", "Code Cleanliness"],
        "practiceSkills": ["Multi-Concept Integration", "Algorithm Decomposition", "Edge Case Hardening"],
        "steps": [
            make_explanation_step(
                "day10-step1", 1, "Section 1 Architectural Synthesis", "Synthesis Model",
                "Synthesizing Python Foundations: Memory, Flow & Semantics",
                "Consolidate the core mental models established in Days 1 through 9.",
                [
                    "Over the first 9 days, you built the foundation of Python computation:",
                    "1. **Names & Memory**: Variables are name tags bound to heap objects; numbers and strings are immutable; assignment never copies values into boxes.",
                    "2. **Arithmetic & Logic**: Floor division rounds toward negative infinity (`//`), logical operators return decisive operands, and every object has a boolean truth value.",
                    "3. **Control Flow & Scope**: Loops support lazy evaluation with `range()` and search fallbacks with `else:`; functions encapsulate frames following the LEGB scope rule.",
                    "4. **Argument Protocols & Built-ins**: Default arguments evaluate once; built-ins like `enumerate`, `zip`, and `math` provide C-accelerated primitives."
                ],
                snippets=[{
                    "title": "Integrated Pythonic Pattern",
                    "code": "def process_batch(items, *, max_limit=10, transform=None):\n    \"\"\"Demonstrates keyword-only enforcement and None sentinel defaults.\"\"\"\n    if transform is None:\n        transform = lambda x: x\n    return [transform(x) for x in items[:max_limit]]",
                    "language": "python",
                    "caption": "Combining function signatures, guards, and comprehensions."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Milestone Achievement",
                    "content": "You are now ready to tackle composite data structures (lists, dicts, sets, tuples) in Section 2 with zero misconceptions about memory!"
                }],
                takeaway="A solid understanding of memory references, scope, and control flow enables confident Python architecture."
            ),
            make_explanation_step(
                "day10-step2", 2, "Decomposition & Edge Case Checklist", "Decomposition",
                "Algorithmic Thinking: Breaking Down Multi-Step Problems",
                "A systematic framework for decomposing engineering challenges.",
                [
                    "When solving multi-step programming tasks:",
                    "1. **Input Validation**: Check for empty inputs, zeroes, negative bounds, and unexpected types.",
                    "2. **Invariant Definition**: Identify what condition must hold true before and after each loop iteration.",
                    "3. **State Isolation**: Ensure functions compute results purely without leaking state to outer scopes.",
                    "4. **Complexity Budget**: Verify that your approach scales cleanly within memory and time constraints."
                ],
                snippets=[{
                    "title": "Defensive Decomposition Pattern",
                    "code": "def find_first_peak(nums):\n    if not nums: # Guard empty\n        return None\n    for i in range(len(nums)):\n        left = nums[i-1] if i > 0 else float('-inf')\n        right = nums[i+1] if i < len(nums) - 1 else float('-inf')\n        if nums[i] >= left and nums[i] >= right:\n            return (i, nums[i])\n    return None",
                    "language": "python",
                    "caption": "Guarding boundaries and managing edge states."
                }],
                callouts=[{
                    "type": "deep-dive",
                    "title": "Avoid Clumsy Flags",
                    "content": "Notice how the guard `if not nums:` handles empty inputs upfront, simplifying subsequent logic."
                }],
                takeaway="Guard edge cases early and isolate invariants across loop cycles."
            ),
            make_checkpoint_step(
                "day10-step3", 3, "Foundations Milestone Checkpoint", "Checkpoint",
                "Verify Section 1 Mastery Across Core Tenets",
                "Test your synthesized mental model of Python fundamentals.",
                [
                    {
                        "id": "chk-d10-q1",
                        "question": "Which of the following statements about Python memory and assignment is TRUE?",
                        "options": [
                            {"id": "A", "label": "a = [1, 2]; b = a creates an independent clone of the list in memory"},
                            {"id": "B", "label": "Integers and strings can have their internal characters/values modified in-place"},
                            {"id": "C", "label": "Assignment binds a name tag in the local namespace to an object in heap memory"},
                            {"id": "D", "label": "Variables store values directly inside named memory slots like C structs"}
                        ],
                        "correctOptionId": "C",
                        "explanations": {
                            "A": "Incorrect: b = a binds 'b' to the exact same list object in memory.",
                            "B": "Incorrect: Integers and strings are strictly immutable.",
                            "C": "Correct! In Python, variables are names pointing to heap objects; assignment attaches or rebinds these name tags.",
                            "D": "Incorrect: Python uses object references, not fixed value boxes."
                        }
                    },
                    {
                        "id": "chk-d10-q2",
                        "question": "What will `bool([]) or 'OK' and 0 or [42]` evaluate to?",
                        "options": [
                            {"id": "A", "label": "True"},
                            {"id": "B", "label": "'OK'"},
                            {"id": "C", "label": "[42]"},
                            {"id": "D", "label": "0"}
                        ],
                        "correctOptionId": "C",
                        "explanations": {
                            "A": "Incorrect: Short-circuiting returns the decisive operand object, not a boolean.",
                            "B": "Incorrect: 'and' binds tighter than 'or'. 'OK' and 0 evaluates to 0.",
                            "C": "Correct! Precedence: ('OK' and 0) evaluates to 0. The expression becomes: bool([]) or 0 or [42]. bool([]) is False. False or 0 is 0 (falsy). 0 or [42] returns [42]!",
                            "D": "Incorrect: 0 is falsy, so evaluation continues to [42]."
                        }
                    }
                ],
                takeaway="Operator precedence: 'and' binds tighter than 'or', and short-circuiting returns the decisive operand."
            ),
            make_practice_step(
                "day10-step4", 4, "Synthesize: Transaction Validator", "Practice",
                "Build an End-to-End Account Ledger Validator",
                "Combine functions, loops, safe casting, guards, and formatted outputs.",
                "Financial Ledger Validator",
                [
                    "Given raw ledger entries: `entries = ['100.50', '-25.00', 'INVALID', '50.25', '  -10.75  ', 'N/A']`.",
                    "Parse valid numerical transactions (floats) defensively, ignoring invalid tokens.",
                    "Separate transactions into `credits` (positive amounts) and `debits` (negative amounts).",
                    "Compute `net_balance = sum(credits) + sum(debits)`, rounded to 2 decimal places.",
                    "Print `'Credits count:', len(credits)`",
                    "Print `'Debits count:', len(debits)`",
                    "Print `'Net balance:', f'{net_balance:.2f}'`."
                ],
                """# Day 10 Practice: Financial Ledger Validator
entries = ["100.50", "-25.00", "INVALID", "50.25", "  -10.75  ", "N/A"]

credits = []
debits = []

# TODO: Parse valid transactions and separate into credits and debits
for item in entries:
    pass

net_balance = round(sum(credits) + sum(debits), 2)

print("Credits count:", len(credits))
print("Debits count:", len(debits))
print("Net balance:", f"{net_balance:.2f}")
""",
                """entries = ["100.50", "-25.00", "INVALID", "50.25", "  -10.75  ", "N/A"]

credits = []
debits = []

for item in entries:
    try:
        val = float(item.strip())
        if val >= 0:
            credits.append(val)
        else:
            debits.append(val)
    except ValueError:
        continue

net_balance = round(sum(credits) + sum(debits), 2)

print("Credits count:", len(credits))
print("Debits count:", len(debits))
print("Net balance:", f"{net_balance:.2f}")
""",
                ["Credits count: 2", "Debits count: 2", "Net balance: 115.00"],
                "Use try/except ValueError on float(item.strip()), append positive values to credits and negative values to debits.",
                takeaway="Synthesizing parsing, validation, and control flow builds resilient software foundations."
            ),
            make_completion_step(
                "day10-step5", 5, "Section 1 Foundations Mastery", "Recap",
                10, "Day 10 Complete: Foundations Check & Synthetic Practice",
                "Congratulations! You have completed Section 1: Python Foundations with deep conceptual and practical mastery.",
                [
                    {
                        "concept": "Variables & Memory",
                        "naiveIntuition": "Variables are boxes holding copied values",
                        "pythonReality": "Variables are pointers/labels bound to heap objects"
                    },
                    {
                        "concept": "Operator Precedence",
                        "naiveIntuition": "Expressions evaluate strictly left to right",
                        "pythonReality": "Arithmetic and logical operators adhere to strict precedence ('and' before 'or')"
                    }
                ],
                ["Python Memory Model", "Short-Circuit Logic", "Loop-else Constructs", "LEGB Function Scoping", "Defensive I/O"],
                get_next_preview(10)
            )
        ]
    }

    return days
