"""
Chapter 01
01-03-project-03: Attribute Scale Exercises
============================================
Demonstrates and verifies the five attribute-scale examples from
Ch.1 Exercise Q1 (Stevens' measurement scales).

For each example the script shows:
  - A description of the attribute
  - The correct Stevens scale (Nominal / Ordinal / Interval / Ratio)
  - The reasoning behind the answer

An optional interactive quiz mode lets the user guess the scale
before the answer is revealed.

Concepts: Stevens' four measurement scales, why ordering / arithmetic /
true-zero each matter, and how to pick the right scale for real data.

Usage:
    python scale_exercises.py           (show all answers, no interaction)
    python scale_exercises.py --quiz    (interactive quiz mode)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys   # command-line arguments


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# ---------------------------------------------------------------------------
# The five exercise examples from Ch.1 Ex.Q1, stored as a list of dicts.
# Each dict has:
#   label       - short name used in headings
#   description - the full question text
#   scale       - correct answer (one of the four Stevens' scales)
#   reasoning   - explanation of WHY this scale is correct
# ---------------------------------------------------------------------------
EXERCISE_ANSWERS = [
    {
        "label":       "a. University students' letter grades",
        "description": "Letter grades assigned to university students (A, B, C, D, F).",
        "scale":       "Ordinal",
        "reasoning": (
            "Letter grades have a clear, meaningful order: A > B > C > D > F.\n"
            "However, the GAP between grades is not measurable -- we cannot say\n"
            "that the difference between A and B equals the difference between B\n"
            "and C.  Arithmetic (mean, ratio) is therefore not meaningful.\n"
            "=> Ordinal: order YES, equal intervals NO, true zero NO."
        ),
    },
    {
        "label":       "b. Level of urgency in an emergency room",
        "description": (
            "Triage categories such as: low, moderate, urgent, critical."
        ),
        "scale":       "Ordinal",
        "reasoning": (
            "The urgency levels have a natural order from least to most urgent.\n"
            "But the 'distance' between consecutive levels is not a fixed, known\n"
            "quantity -- 'critical' is not twice as urgent as 'moderate' in any\n"
            "measurable sense.  This rules out Interval and Ratio.\n"
            "=> Ordinal: order YES, equal intervals NO, true zero NO."
        ),
    },
    {
        "label":       "c. Classification of animals in a zoo",
        "description": (
            "Animal classification categories: mammal, reptile, bird, fish, "
            "amphibian, insect ..."
        ),
        "scale":       "Nominal",
        "reasoning": (
            "Animal classes are pure categories with no natural numeric order.\n"
            "There is no sense in which 'mammal > reptile', and doing arithmetic\n"
            "on these labels (mean class, ratio of classes) is meaningless.\n"
            "Only operations that test equality (=, !=) are valid here.\n"
            "=> Nominal: identity/category only.  No order, no arithmetic."
        ),
    },
    {
        "label":       "d. Carbon dioxide levels in the atmosphere",
        "description": (
            "Atmospheric CO2 concentration measured in parts per million (ppm)."
        ),
        "scale":       "Ratio",
        "reasoning": (
            "CO2 concentration is a numeric quantity with a TRUE ZERO:\n"
            "  0 ppm means 'no CO2 present'.\n"
            "All four operations are valid: we can say 800 ppm is twice as much\n"
            "as 400 ppm (ratio is meaningful).  Mean, standard deviation, and\n"
            "all arithmetic are appropriate.\n"
            "=> Ratio: order YES, equal intervals YES, true zero YES."
        ),
    },
    {
        "label":       "e. Distance from center of campus",
        "description": (
            "Physical distance of a location from the geographic center of campus,\n"
            "measured in meters."
        ),
        "scale":       "Ratio",
        "reasoning": (
            "Distance is measured on a ratio scale:\n"
            "  0 meters = 'at the center point' (true zero, not arbitrary).\n"
            "All arithmetic is valid: 200 m is twice as far as 100 m.\n"
            "Mean distance, standard deviation, and ratios are all meaningful.\n"
            "=> Ratio: order YES, equal intervals YES, true zero YES."
        ),
    },
]

# Valid scale names accepted in quiz mode (case-insensitive input)
VALID_SCALES = ("Nominal", "Ordinal", "Interval", "Ratio")

# Display width used for separator lines
SEPARATOR_WIDTH = 72


# ============================================================
# 3. DEMO DATASET
# ============================================================

# A reference table showing what operations are valid on each scale.
# Used when printing the scale legend at the start of the script.
SCALE_LEGEND = [
    # (scale,      order, equal_intervals, true_zero, example)
    ("Nominal",  "No",  "No",  "No",  "animal class, gender, city name"),
    ("Ordinal",  "Yes", "No",  "No",  "letter grade, urgency level, rank"),
    ("Interval", "Yes", "Yes", "No",  "temperature (Celsius), calendar year"),
    ("Ratio",    "Yes", "Yes", "Yes", "weight, distance, CO2 ppm, age"),
]


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def separator(char="-", width=SEPARATOR_WIDTH):
    """Print a horizontal line made of the given character."""
    print(char * width)


def print_scale_legend():
    """
    Print a compact reference table of the four Stevens' scales.
    Shows which operations are valid on each scale.
    """
    separator("=")
    print("  STEVENS' MEASUREMENT SCALES -- QUICK REFERENCE")
    separator("=")
    header = (
        f"  {'Scale':<10}  {'Order?':<7}  {'Equal gaps?':<13}"
        f"  {'True zero?':<12}  Example"
    )
    print(header)
    separator("-")
    for row in SCALE_LEGEND:
        scale, order, gaps, zero, example = row
        print(
            f"  {scale:<10}  {order:<7}  {gaps:<13}  {zero:<12}  {example}"
        )
    separator("=")
    print()


def prompt_user_guess(question_label):
    """
    Ask the user to type their guess for the scale of one attribute.

    Keeps prompting until a valid scale name is entered (case-insensitive).
    Returns the user's answer with canonical capitalisation.
    """
    valid_lower = [s.lower() for s in VALID_SCALES]
    choices = " / ".join(VALID_SCALES)

    while True:
        raw = input(f"  Your answer [{choices}]: ").strip()
        if raw.lower() in valid_lower:
            # Return the canonically-capitalised version
            index = valid_lower.index(raw.lower())
            return VALID_SCALES[index]
        print(f"  Please enter one of: {choices}")


# ============================================================
# 5. CORE ANALYSIS FUNCTIONS
# ============================================================

def run_attribute_audit_logic(description, scale):
    """
    Apply the same scale-inference logic used in project-01 (attribute_audit.py)
    to illustrate how the automated tool would classify these examples.

    NOTE: The heuristic in project-01 relies on COLUMN NAMES and NUMERIC values.
    For these exercise examples the 'column names' we provide are short slugs
    that hint at the correct answer, so the audit logic mostly agrees.

    Returns a string: the scale that the heuristic would infer.
    """
    # Simple keyword-based heuristic (mirrors project-01 logic)
    desc_lower = description.lower()

    # Ratio keywords
    ratio_kws = ["distance", "co2", "concentration", "ppm", "carbon dioxide",
                 "weight", "height", "age", "salary", "count", "amount"]
    for kw in ratio_kws:
        if kw in desc_lower:
            return "Ratio"

    # Ordinal keywords
    ordinal_kws = ["grade", "level", "rank", "urgency", "triage", "rating",
                   "priority", "tier"]
    for kw in ordinal_kws:
        if kw in desc_lower:
            return "Ordinal"

    # Nominal keywords
    nominal_kws = ["classification", "category", "class", "type", "species",
                   "animal", "gender", "name", "label"]
    for kw in nominal_kws:
        if kw in desc_lower:
            return "Nominal"

    # Interval keywords
    interval_kws = ["temperature", "celsius", "fahrenheit", "year", "date"]
    for kw in interval_kws:
        if kw in desc_lower:
            return "Interval"

    return "Unknown"


def evaluate_answer(user_answer, correct_answer):
    """
    Compare the user's guess with the correct answer.
    Returns True if they match (case-insensitive).
    """
    return user_answer.lower() == correct_answer.lower()


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def print_exercise_answer(index, item, show_answer=True):
    """
    Print one exercise item.

    Parameters
    ----------
    index       : 1-based position of this item (for display only)
    item        : dict from EXERCISE_ANSWERS
    show_answer : if True, print the correct scale and reasoning immediately
    """
    separator("=")
    print(f"  Q1({item['label']})")
    separator("-")
    print(f"  Attribute: {item['description']}")
    print()

    if show_answer:
        print(f"  Correct scale : {item['scale']}")
        separator(".")
        print("  Reasoning:")
        for line in item["reasoning"].split("\n"):
            print(f"    {line}")
        separator(".")

        # Run the heuristic to show how project-01 would classify this
        heuristic_result = run_attribute_audit_logic(item["description"], item["scale"])
        match_str = "MATCH" if heuristic_result == item["scale"] else "MISMATCH"
        print(f"  Heuristic (project-01 logic) : {heuristic_result}  [{match_str}]")


def print_quiz_result(user_answer, correct_answer):
    """
    After the user has guessed, reveal whether they were right and show
    the reasoning.
    """
    if evaluate_answer(user_answer, correct_answer):
        print("  Correct! Well done.")
    else:
        print(f"  Incorrect. The correct answer is: {correct_answer}")


def print_summary(score, total):
    """Print a quiz score summary."""
    separator("=")
    print(f"  QUIZ COMPLETE")
    print(f"  Score: {score} / {total}")
    pct = score * 100 // total
    bar_filled = pct // 5    # each '#' represents 5 percentage points
    bar_empty  = 20 - bar_filled
    bar = "#" * bar_filled + "-" * bar_empty
    print(f"  [{bar}] {pct}%")
    separator("=")


# ============================================================
# 7. FILE I/O FUNCTIONS
# ============================================================

def load_csv(csv_file):
    """
    Read a CSV file and return a column-oriented dictionary.
    Not used in this project (no CSV input needed), but included for
    structural consistency with the other mini-project files.

    Pivot: row-oriented -> column-oriented
    Before: rows = [{"Col": "A"}, {"Col": "B"}]
    After:  columns = {"Col": ["A", "B"]}
    """
    import csv as csv_module
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv_module.DictReader(f)
        rows = list(reader)

    if len(rows) == 0:
        raise ValueError("The CSV file is empty.")

    columns = {}
    for col_name in rows[0]:
        columns[col_name] = []
        for row in rows:
            columns[col_name].append(row[col_name])

    return columns, len(rows)


# ============================================================
# 8. MAIN PROGRAM
# ============================================================

def run_show_all():
    """
    Display all exercise answers with reasoning, then print a
    comparison table showing which heuristic results matched.
    """
    print()
    print("  Ch.1 Exercise Q1 -- Attribute Scale Identification")
    print("  Five real-world attributes; identify the correct Stevens scale.")
    print()

    print_scale_legend()

    for i, item in enumerate(EXERCISE_ANSWERS):
        print_exercise_answer(i + 1, item, show_answer=True)
        print()

    # Summary comparison table
    separator("=")
    print("  SUMMARY TABLE")
    separator("-")
    print(f"  {'Attribute':<40}  {'Correct Scale':<10}  Heuristic")
    separator("-")
    for item in EXERCISE_ANSWERS:
        heuristic = run_attribute_audit_logic(item["description"], item["scale"])
        match_str = "OK" if heuristic == item["scale"] else "MISS"
        print(
            f"  {item['label']:<40}  {item['scale']:<10}  "
            f"{heuristic:<10}  [{match_str}]"
        )
    separator("=")
    print()


def run_quiz():
    """
    Interactive quiz mode: for each attribute the user guesses the scale,
    then the correct answer and reasoning are revealed.
    """
    print()
    print("  Ch.1 Exercise Q1 -- QUIZ MODE")
    print("  Guess the Stevens scale for each attribute.")
    print()
    print_scale_legend()

    score = 0
    total = len(EXERCISE_ANSWERS)

    for i, item in enumerate(EXERCISE_ANSWERS):
        separator("=")
        print(f"  Question {i + 1} of {total}")
        print(f"  Q1({item['label']})")
        separator("-")
        print(f"  Attribute: {item['description']}")
        print()

        user_answer = prompt_user_guess(item["label"])
        print()

        print_quiz_result(user_answer, item["scale"])

        if evaluate_answer(user_answer, item["scale"]):
            score += 1

        print()
        print("  Reasoning:")
        for line in item["reasoning"].split("\n"):
            print(f"    {line}")
        print()

    print_summary(score, total)


if __name__ == "__main__":
    args = [a.lower() for a in sys.argv[1:]]

    if "--quiz" in args or "-q" in args:
        run_quiz()
    else:
        run_show_all()
