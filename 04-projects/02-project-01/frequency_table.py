"""
Chapter 02
02-03-project-01: Frequency Table Builder
==========================================
Given any CSV, build a complete frequency table for any column:
  - Absolute frequency       -> how many times each value appears
  - Relative frequency       -> percentage of total (= empirical distribution)
  - Absolute cumulative freq -> count of values up to and including this one
  - Relative cumulative freq -> percentage up to and including this one (= empirical CDF)

Concepts covered:
  Ch.2 - Univariate frequency analysis, empirical distributions, CDFs

Usage:
    python frequency_table.py                         (runs built-in demo)
    python frequency_table.py data.csv                (all columns in a CSV)
    python frequency_table.py data.csv Weight         (one specific column)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys                       # command-line arguments and exit
import csv                       # read CSV files
from collections import Counter  # count value frequencies efficiently


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# Values that count as "missing" and should be skipped
MISSING_MARKERS = ("", "na", "nan", "null", "none", "?")


# ============================================================
# 3. DEMO DATASET
# ============================================================

# The Friends dataset from the Ch.2 lecture slides.
# Stored as a column-oriented dict so it matches the format
# returned by load_csv and can be passed directly to the analysis functions.
FRIENDS = {
    "Friend":   ["Andrew", "Bernhard", "Carolina", "Dennis", "Eve", "Fred",
                 "Gwyneth", "Hayden", "Irene", "James", "Kevin", "Lea", "Marcus", "Nigel"],
    "Max_temp": ["25", "31", "15", "20", "10", "12", "16", "26", "15", "21", "30", "13", "8", "12"],
    "Weight":   ["77", "110", "70", "85", "65", "75", "75", "63", "55", "66", "95", "72", "83", "115"],
    "Height":   ["175", "195", "172", "180", "168", "173", "180", "165", "158", "163", "190", "172", "185", "192"],
    "Gender":   ["M", "M", "F", "M", "F", "M", "F", "F", "F", "M", "M", "F", "F", "M"],
    "Company":  ["Good", "Good", "Bad", "Good", "Bad", "Good", "Bad", "Bad",
                 "Bad", "Good", "Bad", "Good", "Bad", "Good"],
}


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def remove_missing(raw_values):
    """
    Go through raw_values and return only the non-missing ones.
    Also return how many were missing, so we can report it.

    What counts as missing: empty string, "NA", "NaN", "null", "none", "?"
    """
    clean         = []   # values we will keep
    missing_count = 0    # how many we skipped

    for value in raw_values:
        # Strip whitespace from both ends before checking
        v = value.strip()

        # Check if this value is a missing marker (case-insensitive)
        if v.lower() in MISSING_MARKERS:
            missing_count += 1
        else:
            clean.append(v)

    return clean, missing_count


def is_numeric_column(clean_values):
    """
    Try to convert every value to a float.
    Return True only if ALL values can be converted.
    Even one text value makes the column non-numeric.
    """
    for v in clean_values:
        try:
            float(v)
        except ValueError:
            # This value is not a number, so the whole column is non-numeric
            return False
    return True


def sorted_unique_values(clean_values, is_numeric):
    """
    Return the unique values in the right order for the table:
      - Numeric columns -> sorted by number  (55, 63, 65, 66, ...)
      - Text columns    -> sorted alphabetically (Bad, Good)
    """
    unique = list(set(clean_values))  # set() removes duplicates

    if is_numeric:
        # Sort numerically: convert to float for comparison
        unique.sort(key=float)
    else:
        # Sort alphabetically
        unique.sort()

    return unique


def compute_mean(all_nums):
    """
    Arithmetic mean = sum of all values / count of values.
    """
    total = sum(all_nums)
    return total / len(all_nums)


def compute_median(sorted_nums):
    """
    Median = middle value in a sorted list.

    If the count is odd  -> the single middle element
    If the count is even -> the average of the two middle elements
    """
    n   = len(sorted_nums)
    mid = n // 2  # integer division gives the middle index

    if n % 2 == 1:
        # Odd count: one exact middle element
        return sorted_nums[mid]
    else:
        # Even count: average the two elements on either side of the middle
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2


def find_modes(table):
    """
    Find the most frequent value(s) in the frequency table.

    A dataset can have:
      - One mode     (unimodal)    -> only one value reaches the top frequency
      - Two modes    (bimodal)     -> two values tied for most-frequent
      - Many modes   (multimodal)  -> three or more values tied at the top

    Bug to avoid: using max() returns only ONE value even when multiple
    values are tied at the same frequency. We must find the highest frequency
    first, then collect ALL values that reach that frequency.

    Parameters:
        table -- a list of row dicts from build_frequency_table;
                 each dict has keys "value" and "abs_freq"

    Returns:
        modes        -- list of all values tied at the highest frequency
        highest_freq -- the frequency those values share
    """
    # Step A: find the highest frequency anywhere in the table
    highest_freq = 0
    for row in table:
        if row["abs_freq"] > highest_freq:
            highest_freq = row["abs_freq"]

    # Step B: collect every value that appears at the highest frequency
    modes = []
    for row in table:
        if row["abs_freq"] == highest_freq:
            modes.append(row["value"])

    return modes, highest_freq


# ============================================================
# 5. CORE ANALYSIS FUNCTIONS
# ============================================================

def build_frequency_table(col_name, raw_values):
    """
    Build a complete frequency table for one column.

    Steps:
      1. Remove missing values
      2. Count how many times each unique value appears (absolute frequency)
      3. Sort values (numerically or alphabetically)
      4. Build rows with absolute freq, relative freq, and cumulative versions

    Returns:
        table         -- list of row dicts, one per unique value, in sorted order
        n             -- number of non-missing values
        missing_count -- number of missing values that were skipped
    """
    # Step 1: remove missing values
    clean_values, missing_count = remove_missing(raw_values)
    n = len(clean_values)

    if n == 0:
        return [], 0, missing_count

    # Step 2: count how many times each value appears (absolute frequency)
    counts = Counter(clean_values)

    # Step 3: decide sort order (numeric vs. alphabetical)
    numeric      = is_numeric_column(clean_values)
    sorted_vals  = sorted_unique_values(clean_values, numeric)

    # Step 4: build one row per unique value, keeping a running cumulative total
    table           = []
    running_abs_cum = 0   # running sum of absolute frequencies so far

    for value in sorted_vals:
        abs_freq = counts[value]           # how many times this value appears
        rel_freq = abs_freq / n            # what fraction of the total

        running_abs_cum += abs_freq        # add this row to the running total
        rel_cum_freq = running_abs_cum / n # what fraction are <= this value

        table.append({
            "value":        value,
            "abs_freq":     abs_freq,
            "rel_freq":     rel_freq,
            "abs_cum_freq": running_abs_cum,
            "rel_cum_freq": rel_cum_freq,
        })

    return table, n, missing_count


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def print_separator(char="-", width=78):
    """Print a horizontal line made of the given character."""
    print(char * width)


def print_frequency_table(col_name, raw_values):
    """
    Build and print a nicely formatted frequency table for one column.
    Also prints summary statistics (mode, mean, median) at the bottom.
    """
    table, n, missing_count = build_frequency_table(col_name, raw_values)
    total_records = n + missing_count

    print_separator("=")
    print(f"  FREQUENCY TABLE  |  Column: {col_name}")
    print(f"  Total records: {total_records}  |  Non-missing: {n}  |  Missing: {missing_count}")
    print_separator("=")

    if n == 0:
        print("  (no non-missing values to display)")
        print_separator("=")
        print()
        return

    # Figure out how wide the "Value" column needs to be for alignment
    max_value_len = len("Value")
    for row in table:
        if len(str(row["value"])) > max_value_len:
            max_value_len = len(str(row["value"]))
    val_width = max_value_len + 2   # add a small padding

    # Print the header row
    print(
        f"  {'Value':<{val_width}}"
        f"  {'Abs. Freq':>10}"
        f"  {'Rel. Freq':>10}"
        f"  {'Abs. Cum.':>10}"
        f"  {'Rel. Cum.':>10}"
        f"  Bar"
    )
    print_separator("-")

    # Print one row per unique value
    for row in table:
        # Build a simple bar proportional to relative frequency
        # Scale: 20 "|" characters = 100%
        bar_length = round(row["rel_freq"] * 20)
        bar        = "|" * bar_length

        print(
            f"  {str(row['value']):<{val_width}}"
            f"  {row['abs_freq']:>10}"
            f"  {row['rel_freq']:>9.2%}"
            f"  {row['abs_cum_freq']:>10}"
            f"  {row['rel_cum_freq']:>9.2%}"
            f"    {bar}"
        )

    print_separator("-")

    # Summary statistics at the bottom
    print()
    print(f"  Unique values : {len(table)}")

    # Mode -- valid for ALL scales (nominal, ordinal, quantitative)
    modes, mode_freq = find_modes(table)
    mode_display     = ", ".join(str(m) for m in modes)

    if len(modes) == 1:
        mode_label = "Mode (unimodal)"
    elif len(modes) == 2:
        mode_label = "Mode (bimodal)"
    else:
        mode_label = f"Mode ({len(modes)}-modal)"

    print(f"  {mode_label:<20}: {mode_display}  (each appears {mode_freq} times)")

    # Mean and median -- only valid for numeric (quantitative) columns
    numeric = is_numeric_column([row["value"] for row in table])
    if numeric:
        # Reconstruct the full list of numbers (respecting frequencies).
        # e.g., if 75 appears twice, add 75.0 twice to all_nums.
        all_nums = []
        for row in table:
            count          = row["abs_freq"]
            value_as_float = float(row["value"])
            for _ in range(count):
                all_nums.append(value_as_float)

        # all_nums is already in sorted order (we built table in sorted order)
        mean_val   = compute_mean(all_nums)
        median_val = compute_median(all_nums)

        print(f"  {'Mean':<20}: {mean_val:.4f}")
        print(f"  {'Median':<20}: {median_val:.4f}")
        print(f"  {'Range':<20}: [{min(all_nums):.2f}, {max(all_nums):.2f}]")

    print()
    print_separator("=")
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
    """Run the built-in demo using the Friends dataset from the Ch.2 lecture."""
    print("\n  [Demo -- Friends dataset (from Ch.2 lecture slides)]\n")
    # These four columns cover all interesting cases:
    # Company and Gender are nominal; Height and Weight are ratio/numeric.
    for col in ("Company", "Gender", "Height", "Weight"):
        print_frequency_table(col, FRIENDS[col])


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments: run the built-in demo
        run_demo()

    elif len(sys.argv) == 2:
        # One argument: path to a CSV file -> print all columns
        path = sys.argv[1]
        try:
            columns, _ = load_csv(path)
            for col_name, values in columns.items():
                print_frequency_table(col_name, values)
        except FileNotFoundError:
            print(f"Error: file '{path}' not found.")
            sys.exit(1)

    elif len(sys.argv) == 3:
        # Two arguments: path + column name -> print just that column
        path       = sys.argv[1]
        target_col = sys.argv[2]
        try:
            columns, _ = load_csv(path)
            if target_col not in columns:
                print(f"Error: column '{target_col}' not found.")
                print(f"Available columns: {list(columns.keys())}")
                sys.exit(1)
            print_frequency_table(target_col, columns[target_col])
        except FileNotFoundError:
            print(f"Error: file '{path}' not found.")
            sys.exit(1)

    else:
        print("Usage:")
        print("  python frequency_table.py")
        print("  python frequency_table.py data.csv")
        print("  python frequency_table.py data.csv ColumnName")
        sys.exit(1)
