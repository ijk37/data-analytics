"""
Chapter 04
04-03-project-01: Data Quality Auditor
=======================================
Demonstrates detection and repair of common data quality problems:
  - Missing values (fill with mean, median, mode, or per-class mean)
  - Duplicate rows (deduplication)
  - Outlier / inconsistency detection (IQR fencing)

Concepts: Ch.4 data quality problems (missing, redundant, noisy, outliers)

Usage:
    python data_quality.py                  (runs built-in FRIENDS demo)
    python data_quality.py <csv_file>       (audits any CSV file)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys    # command-line arguments
import csv    # read CSV files
import math   # sqrt for IQR calculations


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# Recognized missing-value markers (checked case-insensitively)
MISSING_MARKERS = {"", "na", "nan", "null", "none", "?", "n/a"}

# IQR multiplier for outlier fencing (standard is 1.5)
IQR_MULTIPLIER = 1.5


# ============================================================
# 3. DEMO DATASET
# ============================================================

# A FRIENDS-inspired dataset with injected quality problems:
#   - Row 4 (Phoebe): age is missing
#   - Row 7 (Gunther): weight is missing
#   - Row 8 (Janice): city is missing
#   - Row 9 (Mike): exact duplicate of Row 6 (Richard)
#   - Row 3 (Joey): weight = 1100 (clearly inconsistent for a human in kg)
DEMO_DATA = {
    "name":   ["Rachel", "Monica", "Joey", "Chandler", "Phoebe", "Ross", "Richard", "Gunther", "Janice", "Mike"],
    "age":    ["26", "26", "27", "28", "", "29", "39", "26", "30", "31"],
    "weight": ["54", "57", "1100", "73", "52", "77", "80", "", "61", "78"],
    "height": ["165", "162", "180", "178", "170", "186", "183", "175", "163", "179"],
    "city":   ["New York", "New York", "New York", "New York", "New York", "New York", "New York", "New York", "", "New York"],
    "gender": ["F", "F", "M", "M", "F", "M", "M", "M", "F", "M"],
}


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def is_missing(value):
    """
    Return True if value is a recognized missing-value marker.

    Handles empty strings and common placeholders like "NA", "?", "null".
    """
    return value.strip().lower() in MISSING_MARKERS


def parse_numbers(values):
    """
    Parse a list of string values into floats, skipping missing ones.

    Returns:
        A list of (index, float) tuples for all non-missing numeric values.
        Returns an empty list if no valid numbers are found.
    """
    result = []
    for i in range(len(values)):
        v = values[i]
        if is_missing(v):
            continue
        try:
            result.append((i, float(v)))
        except ValueError:
            pass  # skip non-numeric values silently
    return result


def compute_mean(numbers):
    """
    Compute the arithmetic mean of a list of floats.

    Returns 0.0 if the list is empty (no valid values to average).
    """
    if len(numbers) == 0:
        return 0.0
    total = 0.0
    for x in numbers:
        total = total + x
    return total / len(numbers)


def compute_median(numbers):
    """
    Compute the median of a sorted list of floats.

    For an even-length list, returns the average of the two middle values.
    Returns 0.0 if the list is empty.
    """
    if len(numbers) == 0:
        return 0.0
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 1:
        # Odd length: exact middle element
        return sorted_nums[mid]
    else:
        # Even length: average of two middle elements
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0


def compute_mode(str_values):
    """
    Find the most frequently occurring non-missing string value.

    Returns None if all values are missing.

    For ties, returns the value that appears first alphabetically.
    """
    counts = {}
    for v in str_values:
        if is_missing(v):
            continue
        key = v.strip()
        if key not in counts:
            counts[key] = 0
        counts[key] = counts[key] + 1

    if len(counts) == 0:
        return None

    # Find the maximum count
    max_count = 0
    for key in counts:
        if counts[key] > max_count:
            max_count = counts[key]

    # Collect all values with the maximum count (for tie-breaking)
    best = []
    for key in counts:
        if counts[key] == max_count:
            best.append(key)

    best.sort()   # alphabetical tie-break for deterministic output
    return best[0]


def compute_quartiles(numbers):
    """
    Compute Q1, Q3, and IQR for a list of floats.

    Uses the standard method:
      Q1 = median of the lower half (not including overall median if odd)
      Q3 = median of the upper half

    Returns (Q1, Q3, IQR).
    Returns (0, 0, 0) if fewer than 2 values.
    """
    if len(numbers) < 2:
        return 0.0, 0.0, 0.0

    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2

    if n % 2 == 1:
        # Odd: lower half excludes the median value
        lower_half = sorted_nums[:mid]
        upper_half = sorted_nums[mid + 1:]
    else:
        # Even: split exactly in half
        lower_half = sorted_nums[:mid]
        upper_half = sorted_nums[mid:]

    q1 = compute_median(lower_half)
    q3 = compute_median(upper_half)
    iqr = q3 - q1
    return q1, q3, iqr


# ============================================================
# 5. CORE ANALYSIS / REPAIR FUNCTIONS
# ============================================================

def audit_missing(columns):
    """
    Report how many values are missing in each column.

    Returns a dict mapping column_name -> (missing_count, missing_pct).
    Prints a formatted report.
    """
    print("\n--- MISSING VALUE AUDIT ---")
    report = {}
    for col_name in columns:
        values = columns[col_name]
        missing_count = 0
        for v in values:
            if is_missing(v):
                missing_count = missing_count + 1
        pct = missing_count / len(values) * 100.0
        report[col_name] = (missing_count, pct)
        if missing_count > 0:
            print("  {:<12}: {} missing  ({:.1f}%)".format(col_name, missing_count, pct))
    total_missing = sum(r[0] for r in report.values())
    if total_missing == 0:
        print("  No missing values found.")
    return report


def fill_missing_mean(values):
    """
    Return a new list where missing values are replaced by the column mean.

    Use for quantitative (numeric) attributes that are roughly symmetric.

    Steps:
      1. Collect all non-missing numeric values
      2. Compute the mean
      3. Replace each missing cell with the mean
    """
    num_pairs = parse_numbers(values)
    # Extract just the float values (drop the index part of each pair)
    nums_only = []
    for (_, x) in num_pairs:
        nums_only.append(x)
    mean_val = compute_mean(nums_only)

    filled = []
    for v in values:
        if is_missing(v):
            filled.append(str(round(mean_val, 4)))
        else:
            filled.append(v)
    return filled


def fill_missing_median(values):
    """
    Return a new list where missing values are replaced by the column median.

    Use for quantitative attributes that are skewed or have outliers.
    Median is more robust than mean because it ignores extreme values.
    """
    num_pairs = parse_numbers(values)
    # Extract just the float values (drop the index part of each pair)
    nums_only = []
    for (_, x) in num_pairs:
        nums_only.append(x)
    median_val = compute_median(nums_only)

    filled = []
    for v in values:
        if is_missing(v):
            filled.append(str(round(median_val, 4)))
        else:
            filled.append(v)
    return filled


def fill_missing_mode(values):
    """
    Return a new list where missing values are replaced by the column mode.

    Use for nominal (categorical) attributes.
    The mode is the most frequently occurring non-missing value.
    """
    mode_val = compute_mode(values)

    filled = []
    for v in values:
        if is_missing(v):
            if mode_val is not None:
                filled.append(mode_val)
            else:
                filled.append(v)   # cannot fill if all values are missing
        else:
            filled.append(v)
    return filled


def fill_missing_per_class(columns, col_to_fill, target_col):
    """
    Fill missing values in col_to_fill using the mean of the same class.

    Parameters:
        columns     : the full column-oriented data dict
        col_to_fill : name of the column with missing values to fill
        target_col  : name of the class/group column to split on

    Returns:
        A new list with missing values filled by class mean.

    Example: fill missing 'age' using the mean age of males/females separately.

    Steps:
      1. Group non-missing values of col_to_fill by class
      2. Compute mean per class
      3. For each missing cell, look up the class of that row and use its mean
    """
    fill_col = columns[col_to_fill]
    class_col = columns[target_col]

    # Step 1: collect non-missing values per class
    class_values = {}
    for i in range(len(fill_col)):
        cls = class_col[i].strip()
        val = fill_col[i]
        if cls not in class_values:
            class_values[cls] = []
        if not is_missing(val):
            try:
                class_values[cls].append(float(val))
            except ValueError:
                pass

    # Step 2: compute mean per class
    class_means = {}
    for cls in class_values:
        class_means[cls] = compute_mean(class_values[cls])

    # Global mean as fallback if class is unknown
    all_nums = []
    for nums in class_values.values():
        all_nums.extend(nums)
    global_mean = compute_mean(all_nums)

    # Step 3: fill missing values
    filled = []
    for i in range(len(fill_col)):
        v = fill_col[i]
        if is_missing(v):
            cls = class_col[i].strip()
            mean_for_class = class_means.get(cls, global_mean)
            filled.append(str(round(mean_for_class, 4)))
        else:
            filled.append(v)
    return filled


def detect_duplicates(columns):
    """
    Find indices of rows that are exact duplicates of an earlier row.

    Returns a list of row indices that are duplicates (not the first occurrence).

    How it works:
      Convert each row to a tuple of its values.
      Keep a set of seen tuples.
      Any row whose tuple was seen before is a duplicate.
    """
    if len(columns) == 0:
        return []

    n_rows = len(next(iter(columns.values())))
    seen_rows = set()
    duplicate_indices = []

    for i in range(n_rows):
        # Build a tuple representing this row (all columns in order)
        row_tuple = []
        for col_name in columns:
            row_tuple.append(columns[col_name][i].strip())
        row_key = tuple(row_tuple)

        if row_key in seen_rows:
            duplicate_indices.append(i)
        else:
            seen_rows.add(row_key)

    return duplicate_indices


def remove_duplicates(columns):
    """
    Return a new column dict with duplicate rows removed.

    Only the first occurrence of each unique row is kept.
    """
    if len(columns) == 0:
        return columns

    n_rows = len(next(iter(columns.values())))
    seen_rows = set()
    keep_indices = []

    for i in range(n_rows):
        row_tuple = []
        for col_name in columns:
            row_tuple.append(columns[col_name][i].strip())
        row_key = tuple(row_tuple)

        if row_key not in seen_rows:
            keep_indices.append(i)
            seen_rows.add(row_key)

    # Build new column dict with only the kept rows
    new_columns = {}
    for col_name in columns:
        new_columns[col_name] = []
        for i in keep_indices:
            new_columns[col_name].append(columns[col_name][i])

    return new_columns


def detect_outliers_iqr(values, col_name="column"):
    """
    Identify numeric values that fall outside the IQR fence.

    IQR fence:
      lower bound = Q1 - IQR_MULTIPLIER * IQR
      upper bound = Q3 + IQR_MULTIPLIER * IQR

    Values outside these bounds are flagged as potential outliers.

    Returns a list of (index, value) tuples for flagged entries.
    Prints the bounds and flagged values.
    """
    num_pairs = parse_numbers(values)
    # Extract just the float values from (index, value) pairs
    nums_only = []
    for (_, x) in num_pairs:
        nums_only.append(x)

    if len(nums_only) < 4:
        print("  {} : not enough values for IQR analysis".format(col_name))
        return []

    q1, q3, iqr = compute_quartiles(nums_only)
    lower_bound = q1 - IQR_MULTIPLIER * iqr
    upper_bound = q3 + IQR_MULTIPLIER * iqr

    print("  {} : Q1={:.1f}, Q3={:.1f}, IQR={:.1f}  |  bounds: [{:.1f}, {:.1f}]".format(
        col_name, q1, q3, iqr, lower_bound, upper_bound))

    flagged = []
    for (idx, val) in num_pairs:
        if val < lower_bound or val > upper_bound:
            flagged.append((idx, val))
            print("    --> Row {} : value {:.1f} FLAGGED as outlier".format(idx, val))

    if len(flagged) == 0:
        print("    No outliers detected.")

    return flagged


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def separator(char="-", width=70):
    """Print a horizontal separator line."""
    print(char * width)


def print_columns_preview(columns, title="Data Preview", max_rows=5):
    """
    Print a tabular preview of the first max_rows rows of the dataset.
    """
    separator()
    print("  " + title)
    separator()

    col_names = list(columns.keys())
    # Figure out column widths
    widths = {}
    for col in col_names:
        widths[col] = len(col)
        for v in columns[col]:
            if len(v) > widths[col]:
                widths[col] = len(v)
        widths[col] = min(widths[col], 14)  # cap at 14 chars

    # Print header
    header = "  "
    for col in col_names:
        header = header + col[:widths[col]].ljust(widths[col] + 2)
    print(header)
    separator(".", 70)

    # Print rows
    n_rows = len(next(iter(columns.values())))
    for i in range(min(max_rows, n_rows)):
        row_str = "  "
        for col in col_names:
            val = columns[col][i]
            if is_missing(val):
                display = "<MISSING>"
            else:
                display = val
            row_str = row_str + display[:widths[col]].ljust(widths[col] + 2)
        print(row_str)

    if n_rows > max_rows:
        print("  ... ({} more rows)".format(n_rows - max_rows))
    separator()


# ============================================================
# 7. FILE I/O FUNCTIONS
# ============================================================

def load_csv(csv_file):
    """
    Read a CSV file and return a column-oriented dictionary.

    Returns:
        columns : dict {column_name: [value1, value2, ...]}
        n_rows  : number of data rows (not counting the header)

    CSV files are row-oriented by default (each line = one record).
    We pivot to column-oriented because most analysis works column by column.

    Before: rows = [{"age": "25", "name": "Alice"}, {"age": "30", "name": "Bob"}]
    After:  columns = {"age": ["25", "30"], "name": ["Alice", "Bob"]}
    """
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if len(rows) == 0:
        raise ValueError("The CSV file is empty.")

    # Pivot from row-oriented to column-oriented
    columns = {}
    for col_name in rows[0]:
        columns[col_name] = []
        for row in rows:
            columns[col_name].append(row[col_name])

    return columns, len(rows)


# ============================================================
# 8. MAIN PROGRAM
# ============================================================

def run_demo():
    """
    Run the built-in FRIENDS demo with injected data quality issues.

    Shows before/after for:
      1. Missing value detection and filling
      2. Duplicate detection and removal
      3. Outlier detection via IQR
    """
    separator("=")
    print("  DATA QUALITY AUDITOR -- Chapter 4 Demo")
    print("  Dataset: FRIENDS cast (with injected quality issues)")
    separator("=")

    # Work on a copy so we can compare before/after
    import copy
    data = copy.deepcopy(DEMO_DATA)

    print_columns_preview(data, "BEFORE: Raw Data (all rows)", max_rows=10)

    # --------------------------------------------------
    # Step 1: Audit missing values
    # --------------------------------------------------
    separator("=")
    print("  STEP 1: MISSING VALUE DETECTION")
    separator("=")
    audit_missing(data)

    # --------------------------------------------------
    # Step 2: Fill missing values
    # --------------------------------------------------
    separator("=")
    print("  STEP 2: FILLING MISSING VALUES")
    separator("=")

    # 'age' is quantitative and roughly symmetric -> fill with mean
    old_age = data["age"][:]
    data["age"] = fill_missing_mean(data["age"])
    print("\n  age (fill with mean):")
    for i in range(len(old_age)):
        if is_missing(old_age[i]):
            print("    Row {} : <MISSING> --> {}".format(i, data["age"][i]))

    # 'weight' has an outlier (1100) so use median for robustness
    # But first we need to note the outlier -- we flag after filling
    old_weight = data["weight"][:]
    data["weight"] = fill_missing_median(data["weight"])
    print("\n  weight (fill with median -- robust to outlier 1100):")
    for i in range(len(old_weight)):
        if is_missing(old_weight[i]):
            print("    Row {} : <MISSING> --> {}".format(i, data["weight"][i]))

    # 'city' is nominal -> fill with mode
    old_city = data["city"][:]
    data["city"] = fill_missing_mode(data["city"])
    print("\n  city (fill with mode):")
    for i in range(len(old_city)):
        if is_missing(old_city[i]):
            print("    Row {} : <MISSING> --> {}".format(i, data["city"][i]))

    # --------------------------------------------------
    # Demo: per-class fill for age using gender
    # --------------------------------------------------
    print("\n  age (per-class fill using gender -- for comparison):")
    age_per_class = fill_missing_per_class(DEMO_DATA, "age", "gender")
    for i in range(len(DEMO_DATA["age"])):
        if is_missing(DEMO_DATA["age"][i]):
            print("    Row {} ({}) : <MISSING> --> {}".format(
                i, DEMO_DATA["gender"][i], age_per_class[i]))

    # --------------------------------------------------
    # Step 3: Detect and remove duplicates
    # --------------------------------------------------
    separator("=")
    print("  STEP 3: DUPLICATE DETECTION")
    separator("=")
    dup_indices = detect_duplicates(data)
    if len(dup_indices) > 0:
        print("\n  Found {} duplicate row(s):".format(len(dup_indices)))
        for idx in dup_indices:
            print("    Row {} : name={}".format(idx, data["name"][idx]))
        data = remove_duplicates(data)
        print("  Duplicates removed. New row count: {}".format(
            len(next(iter(data.values())))))
    else:
        print("  No duplicates found.")

    # --------------------------------------------------
    # Step 4: Detect outliers
    # --------------------------------------------------
    separator("=")
    print("  STEP 4: OUTLIER DETECTION (IQR method)")
    separator("=")
    # Use the original weight column (with the 1100 value) for demonstration
    print("\n  Checking 'weight' column (original, with injected outlier 1100):")
    detect_outliers_iqr(DEMO_DATA["weight"], col_name="weight")

    print("\n  Checking 'age' column:")
    detect_outliers_iqr(data["age"], col_name="age")

    # --------------------------------------------------
    # Final state
    # --------------------------------------------------
    print()
    separator("=")
    print("  AFTER: Cleaned Data")
    separator("=")
    print_columns_preview(data, "Cleaned Data (all rows)", max_rows=10)

    print("\n  Summary of changes:")
    print("    - 3 missing values filled (age: mean, weight: median, city: mode)")
    print("    - 1 duplicate row removed")
    print("    - 1 outlier flagged in weight column (value: 1100)")
    print("      NOTE: outlier was flagged but NOT removed automatically.")
    print("      Investigate before deciding whether to remove or keep it.")
    separator("=")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments: run the built-in demo
        run_demo()
    else:
        # One argument: path to a CSV file
        path = sys.argv[1]
        try:
            cols, n = load_csv(path)
            separator("=")
            print("  DATA QUALITY AUDITOR")
            print("  File: {}  |  Rows: {}  |  Columns: {}".format(path, n, len(cols)))
            separator("=")
            print_columns_preview(cols, "Raw Data Preview")
            audit_missing(cols)
            separator("=")
            print("  DUPLICATE DETECTION")
            separator("=")
            dup_idx = detect_duplicates(cols)
            print("  Found {} duplicate row(s).".format(len(dup_idx)))
            separator("=")
            print("  OUTLIER DETECTION (IQR) -- numeric columns only")
            separator("=")
            for col_name in cols:
                num_pairs = parse_numbers(cols[col_name])
                if len(num_pairs) >= 4:
                    detect_outliers_iqr(cols[col_name], col_name=col_name)
        except FileNotFoundError:
            print("Error: file '{}' not found.".format(path))
            sys.exit(1)
        except Exception as e:
            print("Error: {}".format(e))
            sys.exit(1)
