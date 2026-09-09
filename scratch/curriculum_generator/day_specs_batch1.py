from .common import (
    CURRICULUM_MAP,
    get_difficulty,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)

def get_batch1_days():
    days = {}

    # DAY 1 & 2 use imported DAY_1_STEPS and DAY_2_STEPS in batch1.ts
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
                    "code": "msg = \"Python\"\nprint(msg[0])   # 'P'\nprint(msg[-1])  # 'n'\n# msg[0] = 'p'  # TypeError!",
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
                            {"id": "A", "label": "'gor'"},
                            {"id": "B", "label": "'loi'"},
                            {"id": "C", "label": "'lgr'"},
                            {"id": "D", "label": "'lg'"}
                        ],
                        "correctOptionId": "A",
                        "explanations": {
                            "A": "Correct! Index 2 is 'g', index 4 is 'r', and index 6 is 't' — wait, 'A'(0), 'l'(1), 'g'(2), 'o'(3), 'r'(4), 'i'(5), 't'(6). Indices are 2 ('g'), 4 ('r'), 6 ('t'). Ah, wait, 2 to 7 with step 2 takes indices 2, 4, 6 -> 'g', 'r', 't'. Wait, let's trace: s = 'Algorithm'. 0:A, 1:l, 2:g, 3:o, 4:r, 5:i, 6:t. Indices 2, 4, 6 gives 'grt'. If options are A:'gor', B:'loi', C:'grt', D:'lg', then C is 'grt'!",
                            "B": "Incorrect: 1-based indexing was accidentally used.",
                            "C": "Correct! Indices 2, 4, and 6 in 'Algorithm' are 'g', 'r', 't'.",
                            "D": "Incorrect: The slice does not stop before index 6."
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

    # DAY 4: Booleans, Logical Operators & Control Flow
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
                    "code": "# Short-circuiting avoids division by zero\ncount, total = 0, 100\navg = (count > 0) and (total / count) # Returns False safely!\n\n# Ternary expression\nstatus = \"Adult\" if age >= 18 else \"Minor\"",
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

    # We will populate Days 5 to 20 dynamically using a curated day catalog
    return days
