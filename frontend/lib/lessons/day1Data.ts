import { LessonStep } from "./types";

export const DAY_1_STEPS: LessonStep[] = [
  // =========================================================================
  // STEP 1: Your First Line of Python
  // =========================================================================
  {
    id: "day1-step1",
    stepNumber: 1,
    title: "Your First Python Program",
    shortLabel: "01. First Program",
    type: "explanation",
    isGated: false,
    heading: "Talking to the Computer",
    subheading: "How to make the computer display text on your screen with print().",
    markdownContent: [
      "Welcome to your coding journey! If you have never written a single line of code before, you are in the exact right place.",
      "In Python, when we want the computer to say something out loud or show text on the screen, we use a command called `print()`.",
      "Inside the parentheses `( )`, you write the words you want to say, surrounded by quotation marks `\"...\"`:",
      "```python\nprint(\"Hello, World!\")\n```",
      "When you tell Python to run this instruction, it reads the words inside the quotes and prints them directly to your screen.",
      "That is your very first program! You just commanded a computer to do something.",
    ],
    snippets: [
      {
        title: "Your First Program",
        code: `print("Hello, World!")
print("Welcome to CodeMentor!")
print("Learning to code is going to be fun.")`,
        language: "python",
        caption: "Each print() command writes text on a new line on the screen.",
      },
    ],
    callouts: [
      {
        type: "tip",
        title: "Why quotes matter",
        content:
          "Quotation marks tell Python: 'Treat this exactly as plain text words, not as programming commands.'",
      },
    ],
    keyTakeaway:
      "print(\"...\") is Python's voice — it displays whatever text you put inside quotes onto the screen.",
  },

  // =========================================================================
  // STEP 2: Giving Names to Data (Variables)
  // =========================================================================
  {
    id: "day1-step2",
    stepNumber: 2,
    title: "Variables: Naming Your Data",
    shortLabel: "02. Variables",
    type: "explanation",
    isGated: false,
    heading: "Teaching Python to Remember",
    subheading: "A variable is like putting a name tag or label on a piece of information.",
    markdownContent: [
      "Imagine meeting someone new. They say, *'My name is Sai.'* Your brain attaches the label **name** to the value **'Sai'** so you can remember it.",
      "In Python, we do the exact same thing using the equal sign (`=`):",
      "```python\nname = \"Sai\"\n```",
      "This line creates the word `\"Sai\"` and gives it the name tag `name`.",
      "Now, whenever you tell Python to use `name`, it remembers who you are talking about:",
      "```python\nprint(name)\n```",
      "### Notice the Key Difference:",
      "- `print(\"name\")` with quotes prints the literal four letters: `name`.",
      "- `print(name)` without quotes tells Python: *'Look up the information stored under the label name!'* It prints: `Sai`.",
    ],
    snippets: [
      {
        title: "Creating and Using Variables",
        code: `# Storing a name
name = "Sai"
print(name)

# Changing the name to someone else
name = "Alex"
print(name)`,
        language: "python",
        caption: "When you reassign a variable, Python simply moves the name tag to the new value.",
      },
    ],
    callouts: [
      {
        type: "tip",
        title: "The = Sign in Python",
        content:
          "In programming, '=' does not mean math equality. It means 'Store the value on the right under the name on the left.'",
      },
    ],
    keyTakeaway:
      "A variable gives a friendly name to a piece of data so your program can remember and reuse it.",
  },

  // =========================================================================
  // STEP 3: Numbers and Simple Math
  // =========================================================================
  {
    id: "day1-step3",
    stepNumber: 3,
    title: "Working with Numbers",
    shortLabel: "03. Numbers & Math",
    type: "explanation",
    isGated: false,
    heading: "Variables with Numbers",
    subheading: "Python can remember numbers and perform calculations instantly.",
    markdownContent: [
      "Text needs quotation marks, but **numbers do not**.",
      "To store a number, just write the digits directly:",
      "```python\nage = 20\nprint(age)\n```",
      "Python is also an incredible calculator. You can do math with variables:",
      "```python\nage = 20\nnext_year = age + 1\nprint(next_year)\n```",
      "### How Python Reads `next_year = age + 1`:",
      "1. **Right side first:** Python looks at `age + 1`. Since `age` is `20`, `20 + 1` becomes `21`.",
      "2. **Store on the left:** Python gives the answer `21` the new name tag `next_year`.",
      "You can also print text and variables together by separating them with a comma:",
      "```python\nprint(\"Next year, you will be:\", next_year)\n```",
    ],
    snippets: [
      {
        title: "Simple Arithmetic with Variables",
        code: `age = 20
years_in_future = 5

future_age = age + years_in_future
print("Current age:", age)
print("Future age in 5 years:", future_age)`,
        language: "python",
        caption: "Separating items with commas in print() prints them with spaces in between.",
      },
    ],
    callouts: [
      {
        type: "tip",
        title: "Naming Rule",
        content:
          "Variable names in Python should be lowercase words separated by underscores, like user_age or total_score. They cannot have spaces.",
      },
    ],
    keyTakeaway:
      "Numbers don't use quotes. Python calculates the right side first, then stores the result in the name on the left.",
  },

  // =========================================================================
  // STEP 4: Predict the Output Checkpoint
  // =========================================================================
  {
    id: "day1-step4",
    stepNumber: 4,
    title: "Checkpoint: Predicting Output",
    shortLabel: "04. Predict",
    type: "checkpoint",
    isGated: true,
    heading: "Can You Predict What Happens?",
    subheading: "Test your intuition on how Python executes lines one by one.",
    checkpoints: [
      {
        id: "chk-1-predict-name",
        question: "Look at this 3-line program:\n\n```python\npet = \"Dog\"\npet = \"Cat\"\nprint(pet)\n```\nWhat will be displayed on the screen when this runs?",
        options: [
          {
            id: "A",
            label: "Cat",
            subtext: "The newest value stored in pet",
          },
          {
            id: "B",
            label: "Dog",
            subtext: "The first value stored in pet",
          },
          {
            id: "C",
            label: "Dog Cat",
            subtext: "Both values combined",
          },
          {
            id: "D",
            label: "pet",
            subtext: "The word pet literally",
          },
        ],
        correctOptionId: "A",
        explanations: {
          A: "Spot on! Python runs code from top to bottom. Line 1 sets pet to 'Dog'. Then Line 2 updates pet to 'Cat'. When print(pet) runs on line 3, pet is holding 'Cat'.",
          B: "Incorrect: When line 2 (pet = 'Cat') runs, it replaces the previous value 'Dog'.",
          C: "Incorrect: Assigning a new value replaces the old one; it does not glue them together.",
          D: "Incorrect: Since pet does not have quotation marks around it, Python looks up the value inside the variable instead of printing the letters p-e-t.",
        },
      },
      {
        id: "chk-1-predict-math",
        question: "Look at this code:\n\n```python\nscore = 10\nscore = score + 5\nprint(score)\n```\nWhat is printed?",
        options: [
          {
            id: "A",
            label: "15",
            subtext: "10 + 5 = 15",
          },
          {
            id: "B",
            label: "10",
            subtext: "The original score",
          },
          {
            id: "C",
            label: "105",
            subtext: "Numbers glued side by side",
          },
          {
            id: "D",
            label: "score + 5",
            subtext: "The text of the formula",
          },
        ],
        correctOptionId: "A",
        explanations: {
          A: "Correct! Python calculates score + 5 first (which is 10 + 5 = 15), and then assigns 15 back to score. So it prints 15.",
          B: "Incorrect: score was updated on line 2 by adding 5 to it.",
          C: "Incorrect: Because these are numbers without quotes, Python adds them mathematically (10 + 5 = 15), rather than sticking text together.",
          D: "Incorrect: Python evaluates math expressions to get a result; it doesn't print the raw formula unless you put it in quotes.",
        },
      },
    ],
    keyTakeaway:
      "Python reads code top to bottom. Variables update when you assign a new value to them.",
  },

  // =========================================================================
  // STEP 5: Visualizing Variables (Interactive Visualizer)
  // =========================================================================
  {
    id: "day1-step5",
    stepNumber: 5,
    title: "Visualizing Variables",
    shortLabel: "05. Visualizer",
    type: "visualizer",
    isGated: false,
    heading: "How Python Sees Variables",
    subheading: "Step through the code below to see how name tags attach to values.",
    initialCode: `name = "Sai"
age = 20
age = age + 1`,
    frames: [
      {
        stepNumber: 1,
        codeLine: 'name = "Sai"',
        description:
          "Python creates the text value 'Sai' and attaches the name tag 'name' to it.",
        variables: [{ name: "name", targetObjectId: "val-1", isNew: true }],
        objects: [{ id: "val-1", type: "str", value: '"Sai"', isNew: true }],
        note: "Variable 'name' is created and points to \"Sai\".",
      },
      {
        stepNumber: 2,
        codeLine: "age = 20",
        description:
          "Python creates the number value 20 and attaches the name tag 'age' to it.",
        variables: [
          { name: "name", targetObjectId: "val-1" },
          { name: "age", targetObjectId: "val-2", isNew: true },
        ],
        objects: [
          { id: "val-1", type: "str", value: '"Sai"' },
          { id: "val-2", type: "int", value: "20", isNew: true },
        ],
        note: "Variable 'age' is created with value 20.",
      },
      {
        stepNumber: 3,
        codeLine: "age = age + 1",
        description:
          "Python calculates 20 + 1 = 21, and moves the name tag 'age' to point to 21.",
        variables: [
          { name: "name", targetObjectId: "val-1" },
          { name: "age", targetObjectId: "val-3", isReassigned: true },
        ],
        objects: [
          { id: "val-1", type: "str", value: '"Sai"' },
          { id: "val-2", type: "int", value: "20" },
          { id: "val-3", type: "int", value: "21", isNew: true },
        ],
        note: "Variable 'age' is updated to 21.",
      },
    ],
    keyTakeaway:
      "Variables are name tags that point to values. Reassigning a variable simply points the name tag to the new result.",
  },

  // =========================================================================
  // STEP 6: Guided Hands-on Practice
  // =========================================================================
  {
    id: "day1-step6",
    stepNumber: 6,
    title: "Guided Practice",
    shortLabel: "06. Practice",
    type: "practice",
    isGated: true,
    heading: "Write Your First Python Script",
    subheading: "Create your own variables and calculate your future age in the interactive editor.",
    task: {
      title: "Personal Profile Generator",
      instructions: [
        "1. In TODO 1, set `my_name` to your own name inside quotes (e.g. \"Sai\").",
        "2. In TODO 2, set `current_age` to your age as an integer number (e.g. 20).",
        "3. In TODO 3, calculate `age_in_5_years` by replacing 0 with `current_age + 5`.",
        "4. Click **Run Code** to execute your program and see your profile printed!",
      ],
      starterCode: `# -------------------------------------------------------------
# CodeMentor Day 1 Practice: Your First Python Script
# -------------------------------------------------------------

# TODO 1: Create a variable named 'my_name' with your name (as text in quotes)
my_name = "Sai"

# TODO 2: Create a variable named 'current_age' with a number
current_age = 20

# TODO 3: Calculate what your age will be in 5 years!
# Replace 0 with an expression that adds 5 to current_age:
age_in_5_years = 0

# Print your profile
print("Hello! My name is", my_name)
print("In 5 years, I will be", age_in_5_years)
`,
      expectedOutputPatterns: [
        "Hello! My name is",
        "In 5 years, I will be",
      ],
      hint:
        "Replace 0 in TODO 3 with: current_age + 5. Then click Run Code!",
    },
    keyTakeaway:
      "You wrote real Python code that stores data in variables, computes math, and displays personalized output!",
  },

  // =========================================================================
  // STEP 7: Knowledge Check / Synthesis
  // =========================================================================
  {
    id: "day1-step7",
    stepNumber: 7,
    title: "Knowledge Check",
    shortLabel: "07. Checkpoint",
    type: "checkpoint",
    isGated: true,
    heading: "Solidify Your Day 1 Understanding",
    subheading: "Three quick questions to lock in what you've learned today.",
    checkpoints: [
      {
        id: "chk-syn-quotes",
        question: "What is the difference between `print(\"greeting\")` and `print(greeting)`?",
        options: [
          {
            id: "A",
            label: "print(\"greeting\") prints the literal text 'greeting', while print(greeting) looks up the variable named greeting.",
          },
          {
            id: "B",
            label: "They both do the exact same thing.",
          },
          {
            id: "C",
            label: "print(\"greeting\") is an error because quotes are forbidden in print.",
          },
          {
            id: "D",
            label: "print(greeting) prints the number of letters in greeting.",
          },
        ],
        correctOptionId: "A",
        explanations: {
          A: "Spot on! Quotation marks designate literal text. Without quotes, Python looks for a variable with that name.",
          B: "Incorrect: Quotes tell Python to treat the characters literally.",
          C: "Incorrect: Quotes are required whenever you want to write literal text.",
          D: "Incorrect: It prints the value stored under the variable greeting.",
        },
      },
      {
        id: "chk-syn-naming",
        question: "Which of the following is a valid, good variable name in Python?",
        options: [
          {
            id: "A",
            label: "player_score",
          },
          {
            id: "B",
            label: "player score",
          },
          {
            id: "C",
            label: "1st_player",
          },
          {
            id: "D",
            label: "player-score",
          },
        ],
        correctOptionId: "A",
        explanations: {
          A: "Correct! In Python, words are written in lowercase with underscores separating them (snake_case).",
          B: "Incorrect: Variable names cannot have spaces.",
          C: "Incorrect: Variable names cannot start with a number.",
          D: "Incorrect: The dash '-' is the minus operator in Python, not allowed in variable names.",
        },
      },
      {
        id: "chk-syn-order",
        question: "In the line `total = price + tax`, what does Python do first?",
        options: [
          {
            id: "A",
            label: "It calculates price + tax first, then stores the result in total.",
          },
          {
            id: "B",
            label: "It creates total first and checks if it's equal to price.",
          },
          {
            id: "C",
            label: "It clears the screen.",
          },
          {
            id: "D",
            label: "It runs from left to right, locking total as a permanent formula.",
          },
        ],
        correctOptionId: "A",
        explanations: {
          A: "Exactly right! Python always evaluates the right side of the '=' sign first, and then assigns that result to the variable on the left.",
          B: "Incorrect: '=' is an assignment operator, not a comparison check.",
          C: "Incorrect: Assignment has nothing to do with clearing the screen.",
          D: "Incorrect: Variables store static values, not live formulas.",
        },
      },
    ],
    keyTakeaway:
      "Variables give names to data. Quotes indicate literal text. Python always computes the right side first before storing.",
  },

  // =========================================================================
  // STEP 8: Day 1 Completion & Next Steps
  // =========================================================================
  {
    id: "day1-step8",
    stepNumber: 8,
    title: "Day 1 Complete",
    shortLabel: "08. Complete",
    type: "completion",
    isGated: false,
    dayNumber: 1,
    heading: "Day 1 Complete — You Are Officially a Programmer!",
    subheading: "You learned how to display output, store information in variables, and do math with Python.",
    recapRows: [
      {
        concept: "print(...)",
        naiveIntuition: "Printing on paper with an ink printer",
        pythonReality: "Displays text and numbers onto your computer screen",
      },
      {
        concept: "Quotes (\"...\")",
        naiveIntuition: "Just punctuation",
        pythonReality: "Tells Python 'this is literal text/words', not a variable name",
      },
      {
        concept: "Variables (name = \"Sai\")",
        naiveIntuition: "Complicated computer memory addresses",
        pythonReality: "Friendly name tags that label and remember pieces of data",
      },
      {
        concept: "Assignment (=)",
        naiveIntuition: "Math equality (like in algebra)",
        pythonReality: "Computes the right side first, then stores the answer under the name on the left",
      },
      {
        concept: "Reassignment",
        naiveIntuition: "You can never change a variable once set",
        pythonReality: "Assigning again simply moves the name tag to the newest value",
      },
    ],
    solidifiedConcepts: [
      "Running Python code and displaying output with print()",
      "Text literals with quotation marks vs variable names without quotes",
      "Declaring variables and giving friendly names to data",
      "Performing arithmetic (+, -) and saving results to new variables",
      "Python's top-to-bottom line execution order",
    ],
    nextDayPreview: {
      dayNumber: 2,
      title: "Numbers, Basic Math & Doing Calculations",
      description:
        "Learn how Python handles whole numbers, decimals, division, and the powerful modulo (%) operator using simple clock math.",
    },
  },
];
