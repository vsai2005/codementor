import { LessonStep } from "./types";

export const DAY_2_STEPS: LessonStep[] = [
  // =========================================================================
  // STEP 1: Numbers in Python (Integers vs Decimals)
  // =========================================================================
  {
    id: "day2-step1",
    stepNumber: 1,
    title: "Numbers: Whole vs Decimals",
    shortLabel: "01. Number Types",
    type: "explanation",
    isGated: false,
    heading: "Whole Numbers and Decimals",
    subheading: "Python works with two main kinds of numbers: integers (int) and decimals (float).",
    markdownContent: [
      "Yesterday on Day 1, you learned how to store numbers in variables like `age = 20`.",
      "Today, we explore how Python does calculations. Python has two main types of numbers:",
      "### 1. Integers (`int`)",
      "Integers are **whole numbers** without any decimal point. They can be positive, negative, or zero:",
      "- `count = 5`",
      "- `temperature = -10`",
      "- `score = 0`",
      "### 2. Floating-Point Numbers (`float`)",
      "Floats are **numbers with a decimal point**. We use them for measurements, prices, and precise fractions:",
      "- `price = 19.99`",
      "- `pi = 3.14`",
      "- `weight = 72.5`",
      "### The Decimal Point Rule",
      "If you include a decimal point, Python treats it as a `float`, even if the decimal is `.0`:",
      "`4` is an integer, but `4.0` is a float!",
    ],
    snippets: [
      {
        title: "Integers and Floats",
        code: `items = 3            # Integer (whole number)
price_per_item = 4.50 # Float (decimal number)

print("Items:", items)
print("Price:", price_per_item)`,
        language: "python",
        caption: "Whole numbers are integers; anything with a dot '.' is a float.",
      },
    ],
    callouts: [
      {
        type: "tip",
        title: "Quick Tip",
        content:
          "You don't have to specify whether a number is an integer or a float. Python looks at whether you typed a decimal point and decides automatically.",
      },
    ],
    keyTakeaway:
      "Integers are whole numbers (5, -3); floats have a decimal point (5.0, 3.14).",
  },

  // =========================================================================
  // STEP 2: Basic Arithmetic Operators (+, -, *, /)
  // =========================================================================
  {
    id: "day2-step2",
    stepNumber: 2,
    title: "The 4 Core Operators",
    shortLabel: "02. Core Math",
    type: "explanation",
    isGated: false,
    heading: "Addition, Subtraction, Multiplication & Division",
    subheading: "How Python acts as your instant high-speed calculator.",
    markdownContent: [
      "Python uses the standard mathematical symbols you already know from keyboards:",
      "- `+` **Addition**: `10 + 5` becomes `15`",
      "- `-` **Subtraction**: `10 - 3` becomes `7`",
      "- `*` **Multiplication** (the asterisk): `4 * 5` becomes `20`",
      "- `/` **Division** (the forward slash): `15 / 3` becomes `5.0`",
      "### The Special Rule for Division (`/`):",
      "In Python, standard division (`/`) **always produces a float with a decimal point**, even if the numbers divide evenly!",
      "For example:",
      "- `10 / 2` gives `5.0`, not `5`.",
      "- `7 / 2` gives `3.5`.",
      "This is a wonderful feature of Python: you never have to worry about accidentally losing your decimal remainder when dividing.",
    ],
    snippets: [
      {
        title: "Basic Math Examples",
        code: `print("10 + 5 =", 10 + 5)   # 15
print("20 - 8 =", 20 - 8)   # 12
print("6 * 7 =", 6 * 7)     # 42
print("8 / 2 =", 8 / 2)     # 4.0 (Notice the .0!)
print("9 / 2 =", 9 / 2)     # 4.5`,
        language: "python",
        caption: "Division always gives a float with a decimal point.",
      },
    ],
    callouts: [
      {
        type: "tip",
        title: "Float 'Contagion'",
        content:
          "Whenever you do math between an integer and a float (like 10 + 2.5), the result is always a float: 12.5.",
      },
    ],
    keyTakeaway:
      "+, -, and * work as expected. Standard division / always results in a float (e.g. 10 / 2 is 5.0).",
  },

  // =========================================================================
  // STEP 3: Floor Division (//) and Modulo (%)
  // =========================================================================
  {
    id: "day2-step3",
    stepNumber: 3,
    title: "Floor Division & Modulo",
    shortLabel: "03. // and %",
    type: "explanation",
    isGated: false,
    heading: "How Many Times Does It Fit, and What is Left Over?",
    subheading: "Two indispensable tools for problem solving: // and %.",
    markdownContent: [
      "Imagine you have **14 cookies** to share equally among **4 friends**.",
      "How many whole cookies does each friend get, and how many are left over?",
      "Python gives you two specific operators to answer these exact questions:",
      "### 1. Floor Division (`//`) — 'How many whole times does it fit?'",
      "`14 // 4` gives `3`.",
      "It divides and **chops off any decimal part**, keeping only the whole number. Each friend gets 3 whole cookies.",
      "### 2. Modulo (`%`) — 'What is the remainder left over?'",
      "`14 % 4` gives `2`.",
      "Because $4 \\times 3 = 12$, there are $14 - 12 = 2$ leftover cookies.",
      "### The Clock Math Analogy for Modulo (`%`)",
      "Think of a 12-hour clock. If it is currently 12 o'clock, what time will it be in 14 hours?",
      "It will be 2 o'clock, because `14 % 12 == 2`!",
      "Whenever you want a value to wrap around in a circle or check if a number is even, modulo `%` is your best friend:",
      "- Any even number `% 2` is `0` (e.g., `8 % 2 == 0`).",
      "- Any odd number `% 2` is `1` (e.g., `9 % 2 == 1`).",
    ],
    snippets: [
      {
        title: "Floor Division vs Modulo",
        code: `total_cookies = 14
friends = 4

cookies_each = total_cookies // friends  # 3 whole cookies
leftover = total_cookies % friends        # 2 cookies left over

print("Each friend gets:", cookies_each)
print("Cookies leftover:", leftover)

# Checking if a number is even or odd
number = 17
print("Is 17 odd (remainder when divided by 2)?", number % 2) # 1`,
        language: "python",
        caption: "// gives the whole quotient; % gives the remainder.",
      },
    ],
    callouts: [
      {
        type: "tip",
        title: "Mental Model",
        content:
          "Floor division // answers 'How many boxes can we fill?'. Modulo % answers 'How many loose items remain?'.",
      },
    ],
    keyTakeaway:
      "// gives the whole integer result (chops decimals); % gives the leftover remainder.",
  },

  // =========================================================================
  // STEP 4: Interactive Predict Checkpoint
  // =========================================================================
  {
    id: "day2-step4",
    stepNumber: 4,
    title: "Checkpoint: Math Prediction",
    shortLabel: "04. Predict",
    type: "checkpoint",
    isGated: true,
    heading: "Predict the Calculation Output",
    subheading: "Test your understanding of /, //, and % before writing code.",
    checkpoints: [
      {
        id: "chk-2-division-type",
        question: "What does `print(12 / 3)` output in Python?",
        options: [
          {
            id: "A",
            label: "4.0",
            subtext: "A float with a decimal point",
          },
          {
            id: "B",
            label: "4",
            subtext: "An integer",
          },
          {
            id: "C",
            label: "12/3",
            subtext: "The literal string",
          },
          {
            id: "D",
            label: "0",
            subtext: "The remainder",
          },
        ],
        correctOptionId: "A",
        explanations: {
          A: "Spot on! The standard division operator / in Python ALWAYS returns a float (4.0), even when the division is exact.",
          B: "Incorrect: Standard division / always returns a float (4.0). If you want an integer 4, use floor division: 12 // 3.",
          C: "Incorrect: Numbers and operators without quotes are calculated immediately by Python.",
          D: "Incorrect: The / operator computes division, not remainder.",
        },
      },
      {
        id: "chk-2-floor-mod",
        question: "What do `19 // 5` and `19 % 5` evaluate to?",
        options: [
          {
            id: "A",
            label: "3 and 4",
            subtext: "5 fits 3 times (15), leaving 4 remainder",
          },
          {
            id: "B",
            label: "3.8 and 4",
            subtext: "Decimal and remainder",
          },
          {
            id: "C",
            label: "4 and 3",
            subtext: "Swapped quotient and remainder",
          },
          {
            id: "D",
            label: "3 and 0",
            subtext: "Zero remainder assumption",
          },
        ],
        correctOptionId: "A",
        explanations: {
          A: "Correct! 5 fits into 19 three whole times (5 * 3 = 15). The remainder is 19 - 15 = 4.",
          B: "Incorrect: Floor division // truncates the decimal part completely, producing 3.",
          C: "Incorrect: // gives the quotient (3) and % gives the remainder (4).",
          D: "Incorrect: 19 is not evenly divisible by 5, so the remainder is not 0.",
        },
      },
    ],
    keyTakeaway:
      "Standard division / gives floats (4.0); // gives whole quotients; % gives remainders.",
  },

  // =========================================================================
  // STEP 5: Order of Operations (PEMDAS) & Powers (**)
  // =========================================================================
  {
    id: "day2-step5",
    stepNumber: 5,
    title: "Order of Operations & Exponents",
    shortLabel: "05. Precedence",
    type: "explanation",
    isGated: false,
    heading: "Parentheses and Powers (**)",
    subheading: "How Python decides what to calculate first.",
    markdownContent: [
      "Just like in elementary school math, Python follows the **Order of Operations** (often remembered as **PEMDAS** or **BODMAS**):",
      "1. **P**arentheses `( )` first!",
      "2. **E**xponents `**` (powers: `2 ** 3` means $2^3 = 8$)",
      "3. **M**ultiplication `*`, **D**ivision `/`, `//`, and Modulo `%`",
      "4. **A**ddition `+` and **S**ubtraction `-`",
      "### Always Use Parentheses for Clarity",
      "Consider this calculation:",
      "```python\nresult = 2 + 3 * 4  # 3 * 4 is done first! result is 14.\n```",
      "If you wanted to add $2 + 3$ first, use parentheses:",
      "```python\nresult = (2 + 3) * 4  # (2 + 3) = 5. 5 * 4 is 20!\n```",
      "**Golden Rule:** When in doubt, wrap the math you want done first in parentheses `( )`. It makes your code 100% bug-free and easy to read.",
    ],
    snippets: [
      {
        title: "Parentheses and Exponents",
        code: `# Exponents (powers) use **
print("2 cubed (2 ** 3) =", 2 ** 3)  # 8
print("5 squared (5 ** 2) =", 5 ** 2) # 25

# Parentheses control the order
total_without_parens = 10 + 2 * 5    # 10 + 10 = 20
total_with_parens = (10 + 2) * 5       # 12 * 5 = 60

print("Without parens:", total_without_parens)
print("With parens:", total_with_parens)`,
        language: "python",
        caption: "Parentheses let you explicitly choose what is calculated first.",
      },
    ],
    callouts: [
      {
        type: "tip",
        title: "Powers in Python",
        content:
          "In some languages, ^ is used for powers. In Python, ^ is a bitwise operator! Always use ** for exponents (e.g., 3 ** 2 = 9).",
      },
    ],
    keyTakeaway:
      "Python calculates parentheses first, then exponents (**), then * / // %, and finally + -. Use parentheses to be crystal clear.",
  },

  // =========================================================================
  // STEP 6: Guided Hands-on Practice
  // =========================================================================
  {
    id: "day2-step6",
    stepNumber: 6,
    title: "Guided Practice: Bill Splitter",
    shortLabel: "06. Practice",
    type: "practice",
    isGated: true,
    heading: "Build a Dinner Bill Splitter",
    subheading: "Put all of today's math operators to work in an interactive script.",
    task: {
      title: "Restaurant Bill Calculator",
      instructions: [
        "1. You and 3 friends went to dinner (4 people total). The food bill is $80.00.",
        "2. In TODO 1, calculate the `tip_amount` as 15% of the bill: `total_food_bill * 0.15`.",
        "3. In TODO 2, calculate `grand_total` by adding `total_food_bill` and `tip_amount`.",
        "4. In TODO 3, calculate `cost_per_person` by dividing `grand_total` by `number_of_people`.",
        "5. Click **Run Code** to verify your calculation outputs!",
      ],
      starterCode: `# -------------------------------------------------------------
# CodeMentor Day 2 Practice: Dinner Bill Calculator
# -------------------------------------------------------------

total_food_bill = 80.0
number_of_people = 4

# TODO 1: Calculate 15% tip (multiply total_food_bill by 0.15)
# Replace 0.0 with your calculation:
tip_amount = 0.0

# TODO 2: Calculate grand_total (total_food_bill + tip_amount)
# Replace 0.0 with your calculation:
grand_total = 0.0

# TODO 3: Calculate each person's equal share (grand_total / number_of_people)
# Replace 0.0 with your calculation:
cost_per_person = 0.0

# Print the breakdown
print("Tip amount:", tip_amount)
print("Grand total:", grand_total)
print("Cost per person:", cost_per_person)
`,
      expectedOutputPatterns: [
        "Tip amount: 12.0",
        "Grand total: 92.0",
        "Cost per person: 23.0",
      ],
      hint:
        "tip_amount = total_food_bill * 0.15. grand_total = total_food_bill + tip_amount. cost_per_person = grand_total / number_of_people.",
    },
    keyTakeaway:
      "You combined floats, arithmetic operators, and variables to build a useful real-world calculator!",
  },

  // =========================================================================
  // STEP 7: Day 2 Knowledge Check
  // =========================================================================
  {
    id: "day2-step7",
    stepNumber: 7,
    title: "Knowledge Check",
    shortLabel: "07. Checkpoint",
    type: "checkpoint",
    isGated: true,
    heading: "Solidify Your Math Skills",
    subheading: "Two quick questions to confirm you're ready to master strings tomorrow.",
    checkpoints: [
      {
        id: "chk-2-even-odd-check",
        question: "How can you check if an integer variable `n` is an EVEN number?",
        options: [
          {
            id: "A",
            label: "Check if n % 2 == 0 (remainder is 0 when divided by 2)",
          },
          {
            id: "B",
            label: "Check if n // 2 == 0",
          },
          {
            id: "C",
            label: "Check if n / 2 == 1",
          },
          {
            id: "D",
            label: "Check if n ** 2 == 2",
          },
        ],
        correctOptionId: "A",
        explanations: {
          A: "Spot on! Even numbers divide cleanly by 2 with 0 remainder. So n % 2 == 0 is the universal test for even numbers.",
          B: "Incorrect: n // 2 gives the whole quotient, which is 0 only for 0 and 1.",
          C: "Incorrect: n / 2 == 1 is only true when n is 2.",
          D: "Incorrect: That squares the number.",
        },
      },
      {
        id: "chk-2-parens-check",
        question: "What is the result of `(10 + 2) * (8 - 3)`?",
        options: [
          {
            id: "A",
            label: "60",
            subtext: "12 * 5 = 60",
          },
          {
            id: "B",
            label: "20",
            subtext: "Without parentheses",
          },
          {
            id: "C",
            label: "15",
            subtext: "Adding intermediate steps",
          },
          {
            id: "D",
            label: "25",
            subtext: "Incorrect precedence",
          },
        ],
        correctOptionId: "A",
        explanations: {
          A: "Correct! Python evaluates both parentheses first: (10 + 2) = 12, and (8 - 3) = 5. Then it multiplies 12 * 5 = 60.",
          B: "Incorrect: Both parenthesized expressions are evaluated before the multiplication.",
          C: "Incorrect: 12 * 5 is 60.",
          D: "Incorrect: Check the arithmetic.",
        },
      },
    ],
    keyTakeaway:
      "n % 2 == 0 tests for even numbers. Parentheses guarantee calculation order.",
  },

  // =========================================================================
  // STEP 8: Day 2 Completion
  // =========================================================================
  {
    id: "day2-step8",
    stepNumber: 8,
    title: "Day 2 Complete",
    shortLabel: "08. Complete",
    type: "completion",
    isGated: false,
    dayNumber: 2,
    heading: "Day 2 Complete — You Mastered Python Calculations!",
    subheading: "You now know all of Python's arithmetic operators and how to structure real calculations.",
    recapRows: [
      {
        concept: "Integer (int)",
        naiveIntuition: "Any number",
        pythonReality: "Exact whole numbers (e.g. 5, -2, 100) without any decimal point",
      },
      {
        concept: "Float (float)",
        naiveIntuition: "Numbers that 'float' in memory",
        pythonReality: "Any number written with a decimal point (e.g. 4.5, 2.0)",
      },
      {
        concept: "Standard Division (/)",
        naiveIntuition: "Always gives an integer if numbers divide evenly",
        pythonReality: "Always returns a float (10 / 2 is 5.0)",
      },
      {
        concept: "Floor Division (//)",
        naiveIntuition: "Rounding to nearest number",
        pythonReality: "Chops off any decimal part, returning the whole quotient (14 // 4 is 3)",
      },
      {
        concept: "Modulo (%)",
        naiveIntuition: "Percentage calculation",
        pythonReality: "Computes the leftover remainder after division (14 % 4 is 2)",
      },
      {
        concept: "Powers (**)",
        naiveIntuition: "Using ^ for exponents",
        pythonReality: "In Python, ** is the power operator (2 ** 3 is 8)",
      },
    ],
    solidifiedConcepts: [
      "Difference between whole numbers (int) and decimals (float)",
      "The 4 basic arithmetic operators: +, -, *, /",
      "Floor division (//) for whole quotients and Modulo (%) for remainders",
      "Checking even vs odd with n % 2 == 0",
      "Controlling calculation order with parentheses (PEMDAS)",
      "Exponents using the ** operator",
    ],
    nextDayPreview: {
      dayNumber: 3,
      title: "Strings & Text: Manipulating Words and Characters",
      description:
        "Learn how Python handles sentences, letters, combining text with f-strings, and finding letters by their index position.",
    },
  },
];
