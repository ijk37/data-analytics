"""
Chapter 01
01-03-project-01: Attribute Auditor
====================================
Given any CSV, automatically infer each column's:
  - Attribute type (Nominal / Ordinal / Interval / Ratio)
  - Discrete vs. Continuous

Concepts demonstrated: Ch.1 attribute taxonomy (Stevens),
data types, measurement scales.

Usage:
    python attribute_audit.py                  (runs built-in demo dataset)
    python attribute_audit.py <csv_file>       (audits any CSV file)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys                       # command-line arguments and exit
import math                      # mathematical functions (sqrt, etc.)
import csv                       # read and process CSV files
from collections import Counter  # count frequencies of values efficiently


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# Strategy: before looking at actual values, check if the column name itself
# gives away the attribute type. Ordered by priority in infer_attribute_type().
# These lists are intentionally kept flat for easy manual extension.

# Nominal: categories with no meaningful order (identity only)
NOMINAL_KEYWORDS = [
    "sex",
    "gender",
    "name",
    "department",
    "company",
    "category",
    "type",
    "group",
    "city",
    "state",
    "country",
    "race",
    "ethnicity",
    "status",
    "label",
    "territory",
    "address",
    "postal",
]

# Ordinal: categories with a clear order but unknown gap sizes
# e.g., "grade" could be A/B/C or 1-5 -- order matters, arithmetic does not
ORDINAL_KEYWORDS = [
    "grade",
    "rank",
    "level",
    "rating",
    "score",
    "class",
    "priority",
    "stage",
    "tier",
    "size",
    "quality",
    "education",
]

# Ratio: numeric with a meaningful true zero -- differences AND ratios both valid
# e.g., age=0 means "no age elapsed", salary=0 means "no money" -> true zero
RATIO_KEYWORDS = [
    "age",
    "weight",
    "height",
    "length",
    "count",
    "amount",
    "price",
    "salary",
    "income",
    "distance",
    "area",
    "volume",
    "duration",
    "time",
    "mass",
    "temperature_k",
    "kelvin",
    "per",
]

# Interval: numeric but NO meaningful zero -- differences valid, ratios are not
# e.g., 0 C does not mean "no temperature"; year 0 is arbitrary
INTERVAL_KEYWORDS = [
    "temperature",
    "temp",
    "date",
    "year",
    "month",
    "day",
    "timestamp",
    "celsius",
    "fahrenheit",
]

# Display width for column names in the printed report
COL_WIDTH = 18


# ============================================================
# 3. DEMO DATASET
# ============================================================

# A small hand-crafted dataset that exercises every attribute type:
#   Name           -> Nominal  (identifier, no order)
#   Age            -> Ratio    (true zero, non-negative integer)
#   Educational_level -> Ordinal (keyword match)
#   Company        -> Nominal  (keyword match)
#   Temperature_C  -> Interval (keyword match; negative values possible)
#   Score_rating   -> Ordinal  (keyword match)
#   Salary         -> Ratio    (keyword match; true zero)
DEMO_DATA = {
    "Name": [
        "Andrew", "Bernhard", "Carolina", "Dennis", "Eve",
        "Fred", "Gwyneth", "Hayden", "Irene", "James",
    ],
    "Age": ["55", "43", "37", "82", "23", "46", "38", "50", "29", "42"],
    "Educational_level": ["1", "2", "5", "3", "3.2", "5", "4.2", "4", "4.5", "4.1"],
    "Company": [
        "Good", "Good", "Bad", "Good", "Bad",
        "Good", "Bad", "Bad", "Bad", "Good",
    ],
    "Temperature_C": [
        "22.1", "19.8", "23.5", "18.0", "25.2",
        "21.7", "20.3", "24.6", "17.9", "22.8",
    ],
    "Score_rating": ["7", "5", "9", "6", "8", "7", "4", "9", "5", "8"],
    "Salary": [
        "72000", "55000", "91000", "48000", "63000",
        "88000", "57000", "75000", "52000", "84000",
    ],
}


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def try_numeric(values):
    """
    Try to parse every non-missing value in the list as a float.

    Returns:
        A list of floats if ALL non-missing values are numeric.
        None if even one non-missing value cannot be converted,
              or if every value is missing.

    Skips recognized missing-value markers: "", "na", "nan", "null", "none", "?"
    """
    nums = []
    for v in values:
        v = v.strip()
        # Skip missing markers -- do not let them ruin an otherwise numeric column
        if v == "" or v.lower() in ("na", "nan", "null", "none", "?"):
            continue
        try:
            nums.append(float(v))
        except ValueError:
            # Even one non-numeric token makes the whole column non-numeric
            return None
    # Return None if every row was missing -- cannot say anything about the type
    if nums:
        return nums
    return None


def is_integer_valued(nums):
    """
    Return True if every number in nums has no fractional part.

    Floats like 3.0 are considered integer-valued.
    This distinguishes count data (discrete) from measurements (continuous).

    Examples:
        [3.0, 5.0, 7.0]        -> True  (all whole numbers)
        [3.0, 5.5, 7.0]        -> False (5.5 has a fraction)
    """
    for v in nums:
        if v != int(v):
            return False
    return True


def has_true_zero(col_name, nums):
    """
    Heuristic: does this column have a meaningful absolute zero?

    A ratio scale has a true zero (e.g., weight=0 means "no weight").
    An interval scale does not (e.g., 0 C does not mean "no temperature").

    How we decide:
      1. If the column name matches a RATIO keyword -> True (most reliable)
      2. If all values are non-negative integers    -> True (likely a count)
      Otherwise                                    -> False
    """
    name_lower = col_name.lower()

    # Name-based check takes priority -- most reliable signal
    for kw in RATIO_KEYWORDS:
        if kw in name_lower:
            return True

    # Fallback: non-negative integers are almost always counts -> ratio
    if min(nums) >= 0 and is_integer_valued(nums):
        return True

    return False


# ============================================================
# 5. CORE ANALYSIS FUNCTIONS
# ============================================================

def infer_attribute_type(col_name, raw_values):
    """
    Infer the Stevens measurement scale and discrete/continuous label
    for a single column.

    Returns a dict with three keys:
        steven_type          -- "Nominal", "Ordinal", "Interval", or "Ratio"
        discrete_continuous  -- "Discrete" or "Continuous"
        notes                -- a short human-readable explanation

    Decision priority (highest -> lowest):
      1. Column name ends with 'id'    -> Nominal  (identifier, no arithmetic)
      2. Ordinal keyword in name       -> Ordinal  (ordered but no true gaps)
      3. Binary 0/1 numeric column     -> Nominal  (flag/indicator)
      4. Nominal keyword in name       -> Nominal
      5. Ratio keyword in name         -> Ratio
      6. Interval keyword in name      -> Interval
      7. Non-numeric values (no match) -> Nominal  (text categories)
      8. Numeric, any negatives        -> Interval (negatives rule out true zero)
      9. Numeric, all non-negative     -> Ratio    (true zero assumed)
    """
    name_lower = col_name.lower()

    # --------------------------------------------------
    # 1. ID detection
    # --------------------------------------------------
    # IDs are pure identifiers -- only equality makes sense (=, !=), no ordering.
    if name_lower.endswith("id"):
        return {
            "steven_type":         "Nominal",
            "discrete_continuous": "Discrete",
            "notes":               "Identifier column.",
        }

    # --------------------------------------------------
    # 2. Strong Ordinal keywords
    # --------------------------------------------------
    # Checked before numeric analysis because ordinal columns are often stored
    # as integers (1, 2, 3 for Low/Medium/High), which would otherwise look Ratio.
    for kw in ORDINAL_KEYWORDS:
        if kw in name_lower:
            return {
                "steven_type":         "Ordinal",
                "discrete_continuous": "Discrete",
                "notes":               "Ordered category column.",
            }

    # Try to parse the column's values as numbers for steps 3, 5, 8, 9.
    nums = try_numeric(raw_values)

    # --------------------------------------------------
    # 3. Binary 0/1 detection
    # --------------------------------------------------
    # A column with only {0, 1} is a binary flag (yes/no, active/inactive, etc.).
    # Even though it is numeric, arithmetic on it is meaningless -> Nominal.
    if nums is not None:
        unique_nums = sorted(set(nums))
        if unique_nums == [0.0, 1.0]:
            return {
                "steven_type":         "Nominal",
                "discrete_continuous": "Discrete",
                "notes":               "Binary category coded as 0/1.",
            }

    # --------------------------------------------------
    # 4. Other keyword checks (Nominal / Ratio / Interval)
    # --------------------------------------------------
    # These run AFTER the binary check so a column named "gender" that happens
    # to be encoded 0/1 is already caught above and correctly labeled Nominal.

    for kw in NOMINAL_KEYWORDS:
        if kw in name_lower:
            return {
                "steven_type":         "Nominal",
                "discrete_continuous": "Discrete",
                "notes":               "Category/label column.",
            }

    # Ratio keywords -- checked before Interval because they are more specific
    for kw in RATIO_KEYWORDS:
        if kw in name_lower:
            return {
                "steven_type":         "Ratio",
                "discrete_continuous": "Discrete",
                "notes":               "Quantity/measurement column.",
            }

    for kw in INTERVAL_KEYWORDS:
        if kw in name_lower:
            return {
                "steven_type":         "Interval",
                "discrete_continuous": "Discrete",
                "notes":               "Date/time/calendar-based column.",
            }

    # --------------------------------------------------
    # 5. Numeric analysis (fallback when no keyword matched)
    # --------------------------------------------------

    # Non-numeric: every text column with no keyword match defaults to Nominal.
    if nums is None:
        clean_values = []
        for v in raw_values:
            if v.strip():
                clean_values.append(v.strip())
        n_unique = len(set(clean_values))
        return {
            "steven_type":         "Nominal",
            "discrete_continuous": "Discrete",
            "notes":               f"{n_unique} unique values.",
        }

    # Discrete vs. Continuous:
    #   integer-valued floats (3.0, 5.0) -> Discrete
    #   any fractional value             -> Continuous
    if is_integer_valued(nums):
        disc = "Discrete"
    else:
        disc = "Continuous"

    # Negative minimum -> no true zero -> Interval scale
    # (e.g., temperature in Celsius, delta/change values, z-scores)
    if min(nums) < 0:
        return {
            "steven_type":         "Interval",
            "discrete_continuous": disc,
            "notes":               f"Range [{min(nums):.2f}, {max(nums):.2f}]",
        }

    # All non-negative with no keyword match -> assume Ratio (true zero present)
    return {
        "steven_type":         "Ratio",
        "discrete_continuous": disc,
        "notes":               f"Range [{min(nums):.2f}, {max(nums):.2f}]",
    }


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def separator(char="-", width=80):
    """Print a horizontal line made of the given character."""
    print(char * width)


def print_report(columns, n_rows, source_name):
    """
    Print a full attribute audit report: one section per column,
    plus a type-count summary at the end.
    """
    separator("=")
    print(f"  ATTRIBUTE AUDIT REPORT")
    print(f"  Source  : {source_name}")
    print(f"  Rows    : {n_rows}   |   Columns: {len(columns)}")
    separator("=")

    type_counts = Counter()

    for col_name, values in columns.items():
        info = infer_attribute_type(col_name, values)

        type_counts[info["steven_type"]] += 1

        # Count how many values are missing in this column
        missing = 0
        for v in values:
            v_stripped = v.strip()
            if v_stripped == "" or v_stripped.lower() in ("na", "nan", "null", "none", "?"):
                missing += 1

        print(f"\n  Column  : {col_name}")
        print(f"  Type    : {info['steven_type']:12s}  |  {info['discrete_continuous']}")
        print(f"  Notes   : {info['notes']}")
        if missing:
            print(f"  Missing : {missing} ({missing / len(values) * 100:.1f}%)")
        separator(".", 60)

    separator("=")
    print("\n  COLUMN TYPE SUMMARY")
    for t, cnt in type_counts.most_common():
        bar = "#" * cnt   # one # per column of that type
        print(f"  {t:<10} {bar} {cnt}")
    separator("=")
    print()


# ============================================================
# 7. FILE I/O FUNCTIONS
# ============================================================

def load_csv(csv_file):
    """
    Read a CSV file and return a column-oriented dictionary:
        { column_name: [value1, value2, ...], ... }

    Also returns the number of data rows (not counting the header).
    """
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # first row is automatically used as header
        rows = list(reader)

    if len(rows) == 0:
        raise ValueError("The CSV file is empty.")

    # Pivot from row-oriented to column-oriented
    # Before: rows = [{"Age": "25", "Name": "Alice"}, {"Age": "30", "Name": "Bob"}]
    # After:  columns = {"Age": ["25", "30"], "Name": ["Alice", "Bob"]}
    columns = {}
    for col_name in rows[0]:          # get column names from the first row
        columns[col_name] = []
        for row in rows:              # go through every data row
            columns[col_name].append(row[col_name])

    return columns, len(rows)


# ============================================================
# 8. MAIN PROGRAM
# ============================================================

def run_demo():
    """Run the built-in demo dataset that mirrors the Ch.1 textbook example."""
    print("\n  [Running built-in demo dataset -- mirrors Ch.1 textbook example]\n")
    n_rows = len(next(iter(DEMO_DATA.values())))
    print_report(DEMO_DATA, n_rows, source_name="Demo (Ch.1 textbook dataset + extras)")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments: run the built-in demo
        run_demo()
    else:
        # One argument: path to a CSV file
        path = sys.argv[1]
        try:
            cols, n = load_csv(path)
            print_report(cols, n, source_name=path)
        except FileNotFoundError:
            print(f"Error: file '{path}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
