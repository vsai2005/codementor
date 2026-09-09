"""
Fix and re-align Section 8 (Stacks/Queues) and Section 12 (Greedy) data files.
"""

import pprint
import sys
sys.path.insert(0, ".")

def fix_sec12():
    from scratch.curriculum_generator.sec12_data import SEC12_DAYS

    # CURR:
    # 141: Partition Labels (was 143)
    # 142: Gas Station (was 141)
    # 143: Candy Distribution (was 142)
    gas_station = SEC12_DAYS[141]
    candy = SEC12_DAYS[142]
    partition_labels = SEC12_DAYS[143]

    new_sec12 = dict(SEC12_DAYS)
    new_sec12[141] = partition_labels
    new_sec12[142] = gas_station
    new_sec12[143] = candy

    code = '"""\nSection 12: Greedy Algorithms (Days 136 to 145)\n"""\n\nSEC12_DAYS = ' + pprint.pformat(new_sec12, indent=4, width=120) + "\n"
    with open("scratch/curriculum_generator/sec12_data.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("sec12_data.py re-aligned successfully!")


def fix_sec8():
    from scratch.curriculum_generator.sec8_data import SEC8_DAYS

    # CURR:
    # 88: Min-Stack Design with O(1) Retrieval (was 90)
    # 89: Queue FIFO Mechanics & Circular Ring Buffers (was 88/89)
    # 90: Implement Queue Using Two Stacks (new / aligned)
    # 94: Expression Parsing & Shunting-Yard (new / aligned)
    min_stack = SEC8_DAYS[90]
    queue_fifo = SEC8_DAYS[89]

    # Queue using Two Stacks
    queue_two_stacks_90 = {
        "summary": "Implementing a FIFO Queue using Two LIFO Stacks transfers elements from an input stack to an output stack lazily, achieving amortized O(1) push and pop.",
        "mechanics": "Maintain two stacks: `in_stack` (for push) and `out_stack` (for pop/peek). Push appends to `in_stack` in O(1). When popping or peeking: if `out_stack` is empty, pop all elements from `in_stack` and push them into `out_stack`, reversing their order to restore FIFO! Amortized analysis: each element is pushed and popped at most twice, averaging O(1) across all operations.",
        "takeaway": "Reversing LIFO twice yields FIFO; lazy batch transfers ensure amortized O(1) queue operations.",
        "sample_code": "# Queue using Two Stacks\nclass MyQueue:\n    def __init__(self):\n        self.in_stk = []; self.out_stk = []\n    def push(self, x):\n        self.in_stk.append(x)\n    def pop(self):\n        self.peek()\n        return self.out_stk.pop()\n    def peek(self):\n        if not self.out_stk:\n            while self.in_stk: self.out_stk.append(self.in_stk.pop())\n        return self.out_stk[-1]\n    def empty(self):\n        return not self.in_stk and not self.out_stk",
        "q1": "Why is the amortized time complexity of `pop()` and `peek()` in a two-stack queue O(1), even though transferring elements takes O(N) when out_stack is empty?",
        "q1_opts": [
            {"id": "A", "label": "Each element is moved from in_stack to out_stack exactly once across its entire lifetime in the queue; the O(N) transfer cost is distributed over N individual O(1) operations"},
            {"id": "B", "label": "Because transferring uses a C compiler optimization"},
            {"id": "C", "label": "Because out_stack is never empty"},
            {"id": "D", "label": "Because Python stacks are doubly linked lists"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! By the accounting method of amortized analysis, each item has 2 pushes and 2 pops across its entire journey. 4 operations per item = amortized O(1) constant time.",
            "B": "Incorrect: Algorithmic complexity is mathematical, not compiler dependent.",
            "C": "Incorrect: out_stack starts empty.",
            "D": "Incorrect: Python lists are contiguous arrays."
        },
        "q2": "When should elements be moved from `in_stack` to `out_stack`?",
        "q2_opts": [
            {"id": "A", "label": "ONLY when out_stack is completely empty; premature transfers would scramble the relative FIFO arrival order of newer elements"},
            {"id": "B", "label": "After every single push"},
            {"id": "C", "label": "Whenever in_stack has more than 5 elements"},
            {"id": "D", "label": "At random intervals"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! If out_stack still holds older elements, pouring newer elements on top of them would violate FIFO order. Only refill out_stack when it is fully drained.",
            "B": "Incorrect: Transferring after every push would degrade push to O(N).",
            "C": "Incorrect: Transfers must be strictly demand-driven.",
            "D": "Incorrect: Data structures require deterministic ordering invariants."
        },
        "practice_task": "Implement a First-In, First-Out (FIFO) queue using two LIFO stacks.",
        "starter": "class MyQueue:\n    def __init__(self):\n        self.in_stack = []\n        self.out_stack = []\n\n    # TODO: Implement push(x), pop() -> int, peek() -> int, and empty() -> bool\n\nq = MyQueue()\nq.push(1)\nq.push(2)\nprint('Peek:', q.peek()) # 1\nprint('Pop:', q.pop())   # 1\nprint('Empty:', q.empty()) # False\n",
        "solution": "class MyQueue:\n    def __init__(self):\n        self.in_stack = []\n        self.out_stack = []\n\n    def push(self, x: int) -> None:\n        self.in_stack.append(x)\n\n    def pop(self) -> int:\n        self.peek()\n        return self.out_stack.pop()\n\n    def peek(self) -> int:\n        if not self.out_stack:\n            while self.in_stack:\n                self.out_stack.append(self.in_stack.pop())\n        return self.out_stack[-1]\n\n    def empty(self) -> bool:\n        return not self.in_stack and not self.out_stack\n\nq = MyQueue()\nq.push(1)\nq.push(2)\nprint('Peek:', q.peek())\nprint('Pop:', q.pop())\nprint('Empty:', q.empty())\n",
        "patterns": ["Peek: 1", "Pop: 1", "Empty: False"],
        "hint": "In push: in_stack.append(x). In peek: if not out_stack: while in_stack: out_stack.append(in_stack.pop()); return out_stack[-1]. In pop: peek() and out_stack.pop().",
        "recap": [
            {"concept": "Double Inversion Identity", "naiveIntuition": "Stacks can never act as queues", "pythonReality": "Inverting a stack twice restores the original FIFO order, proving structural duality between queues and stacks"},
            {"concept": "Amortized Efficiency", "naiveIntuition": "Occasional O(N) operations mean the algorithm is slow", "pythonReality": "Infrequent batch transfers averaged over thousands of items maintain sub-microsecond latency"}
        ]
    }

    # Day 94: Shunting-Yard Algorithm & Expression Parsing
    shunting_yard_94 = {
        "summary": "The Shunting-Yard Algorithm parses infix mathematical expressions into Postfix (Reverse Polish Notation) or directly evaluates them using an Operator Stack and Operand Stack.",
        "mechanics": "Read tokens left to right: (1) If number, push to values. (2) If '(', push to ops. (3) If ')', pop and apply operators until '(' is matched. (4) If operator (+, -, *, /): while top of ops has >= precedence, pop and apply. Push current operator. At end, apply remaining operators in ops. Evaluates expressions in strictly O(N) time.",
        "takeaway": "Operator precedence stacks ensure high-precedence operations (*, /) execute before lower-precedence ones (+, -).",
        "sample_code": "# Basic Calculator Expression Evaluator\ndef calculate(s):\n    vals, ops = [], []\n    prec = {'+': 1, '-': 1, '*': 2, '/': 2}\n    def apply():\n        op = ops.pop(); b = vals.pop(); a = vals.pop()\n        if op == '+': vals.append(a + b)\n        elif op == '-': vals.append(a - b)\n        elif op == '*': vals.append(a * b)\n        elif op == '/': vals.append(int(a / b))\n    i = 0\n    while i < len(s):\n        if s[i].isdigit():\n            n = 0\n            while i < len(s) and s[i].isdigit(): n = n * 10 + int(s[i]); i += 1\n            vals.append(n); continue\n        elif s[i] in prec:\n            while ops and ops[-1] in prec and prec[ops[-1]] >= prec[s[i]]: apply()\n            ops.append(s[i])\n        elif s[i] == '(': ops.append('(')\n        elif s[i] == ')':\n            while ops[-1] != '(': apply()\n            ops.pop()\n        i += 1\n    while ops: apply()\n    return vals[0]",
        "q1": "Why does the Shunting-Yard algorithm pop and evaluate existing operators when encountering a new operator of LOWER or EQUAL precedence?",
        "q1_opts": [
            {"id": "A", "label": "Higher or equal precedence operators already waiting on the stack must be evaluated immediately because their binding to preceding numbers is now complete"},
            {"id": "B", "label": "Because stacks can only hold 2 operators"},
            {"id": "C", "label": "To prevent numbers from overflowing"},
            {"id": "D", "label": "Because parenthesis matching requires empty operator stacks"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! E.g. in `2 * 3 + 4`, when encountering `+` (precedence 1), the waiting `*` (precedence 2) has higher precedence and must be evaluated (`2 * 3 = 6`) before `+` can be stored.",
            "B": "Incorrect: Operator stacks can grow to arbitrary depth.",
            "C": "Incorrect: Precedence enforcement is syntactic.",
            "D": "Incorrect: Parentheses create isolated precedence scopes."
        },
        "q2": "What is the time complexity of evaluating an arithmetic expression string of length N using the Shunting-Yard algorithm?",
        "q2_opts": [
            {"id": "A", "label": "O(N) linear time, because each character, number, and operator is pushed and popped at most once"},
            {"id": "B", "label": "O(N^2) quadratic time"},
            {"id": "C", "label": "O(2^N) exponential time"},
            {"id": "D", "label": "O(N log N) time"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Every token is pushed onto the operand or operator stack once and popped at most once. Total operations are proportional to N.",
            "B": "Incorrect: Stack passes do not re-scan the string.",
            "C": "Incorrect: Shunting-Yard is strictly polynomial linear.",
            "D": "Incorrect: No sorting or divide-and-conquer is involved."
        },
        "practice_task": "Evaluate a mathematical expression containing +, -, *, and parentheses.",
        "starter": "def eval_expression(s: str) -> int:\n    # TODO: Implement Shunting-Yard / 2-stack expression evaluator\n    return 0\n\nprint('3 + 2 * 2 =', eval_expression('3 + 2 * 2'))       # 7\nprint('(1 + (4 + 5 + 2) - 3) =', eval_expression('(1 + (4 + 5 + 2) - 3)')) # 9\n",
        "solution": "def eval_expression(s: str) -> int:\n    vals, ops = [], []\n    prec = {'+': 1, '-': 1, '*': 2, '/': 2}\n    def apply():\n        op = ops.pop()\n        b = vals.pop()\n        a = vals.pop()\n        if op == '+':\n            vals.append(a + b)\n        elif op == '-':\n            vals.append(a - b)\n        elif op == '*':\n            vals.append(a * b)\n        elif op == '/':\n            vals.append(int(a / b))\n    i = 0\n    while i < len(s):\n        if s[i] == ' ':\n            i += 1\n            continue\n        if s[i].isdigit():\n            n = 0\n            while i < len(s) and s[i].isdigit():\n                n = n * 10 + int(s[i])\n                i += 1\n            vals.append(n)\n            continue\n        elif s[i] == '(':\n            ops.append('(')\n        elif s[i] == ')':\n            while ops and ops[-1] != '(':\n                apply()\n            if ops and ops[-1] == '(':\n                ops.pop()\n        elif s[i] in prec:\n            while ops and ops[-1] in prec and prec[ops[-1]] >= prec[s[i]]:\n                apply()\n            ops.append(s[i])\n        i += 1\n    while ops:\n        apply()\n    return vals[0] if vals else 0\n\nprint('3 + 2 * 2 =', eval_expression('3 + 2 * 2'))\nprint('(1 + (4 + 5 + 2) - 3) =', eval_expression('(1 + (4 + 5 + 2) - 3)'))\n",
        "patterns": ["3 + 2 * 2 = 7", "(1 + (4 + 5 + 2) - 3) = 9"],
        "hint": "Track vals and ops stacks. If digit parse full integer. If '(' push to ops. If ')' pop and apply until '('. If operator, while top op has >= precedence apply, then push operator.",
        "recap": [
            {"concept": "Operator Precedence Invariant", "naiveIntuition": "Evaluate expressions strictly left-to-right", "pythonReality": "Stack-based precedence deferral guarantees that multiplication and division resolve before addition and subtraction"},
            {"concept": "Syntactic Stack Scoping", "naiveIntuition": "Parentheses require recursive parsing", "pythonReality": "Pushing '(' onto the operator stack scopes precedence evaluation without needing recursion"}
        ]
    }

    new_sec8 = dict(SEC8_DAYS)
    new_sec8[88] = min_stack
    new_sec8[89] = queue_fifo
    new_sec8[90] = queue_two_stacks_90
    new_sec8[94] = shunting_yard_94

    code = '"""\nSection 8: Stacks & Queues (Days 86 to 95)\n"""\n\nSEC8_DAYS = ' + pprint.pformat(new_sec8, indent=4, width=120) + "\n"
    with open("scratch/curriculum_generator/sec8_data.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("sec8_data.py re-aligned successfully!")

if __name__ == "__main__":
    fix_sec12()
    fix_sec8()
