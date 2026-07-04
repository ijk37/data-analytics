"""
Chapter 02
02-03-project-02: Location & Dispersion Statistics Explorer
============================================================
Computes all Ch.2 location and dispersion statistics for every
numeric column in a CSV (or the built-in demo dataset):

  Location  : min, max, mode, mean, median, Q1, Q2, Q3
  Dispersion: amplitude, IQR, MAD, std dev (sample), variance (sample)
  Shape     : skewness (direction and label)

Concepts covered:
  Ch.2 - Central tendency, dispersion, quartile position method,
          Bessel's correction (n-1), skewness, ASCII box plot

Usage:
    python statistics_explorer.py               (runs built-in demo)
    python statistics_explorer.py data.csv      (all numeric columns)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys                       # command-line arguments and exit
import csv                       # read CSV files
import math                      # sqrt, ceil
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

def parse_numeric(raw_values):
    """
    Go through raw_values, skip missing markers, try to convert each to float.
    Return a sorted list of the successfully parsed numbers.

    If a value cannot be converted to a number, it is silently skipped.
    The result is sorted in ascending order (needed for median and quartiles).
    """
    nums = []

    for v in raw_values:
        v = str(v).strip()

        # Skip missing values
        if v.lower() in MISSING_MARKERS:
            continue

        # Try to parse as a number
        try:
            nums.append(float(v))
        except ValueError:
            pass   # not a number, just skip it

    nums.sort()    # sort ascending (required for median / quartile formulas)
    return nums


def compute_mean(nums):
    """
    Arithmetic mean = sum of all values / count of values.
    Also called "average" or "x-bar" (sample mean).
    Valid scale: Quantitative (Interval / Ratio).
    """
    total = 0.0
    for x in nums:
        total += x
    return total / len(nums)


def compute_median(sorted_nums):
    """
    Median = the middle value of a sorted list.

    Requires the list to be SORTED first.

    Rules:
      - n is odd  -> median is the single middle element
      - n is even -> median is the average of the two middle elements

    Valid scale: Ordinal and Quantitative.
    """
    n   = len(sorted_nums)
    mid = n // 2   # integer division gives the index of the middle

    if n % 2 == 1:
        # Odd: there is one exact middle element
        return sorted_nums[mid]
    else:
        # Even: take the average of the two elements on either side of the gap
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2


def compute_mode(nums):
    """
    Mode = the most frequently occurring value(s).

    A dataset can be:
      - Unimodal   -> exactly one most-frequent value
      - Bimodal    -> exactly two values tied for most-frequent
      - Multimodal -> three or more values tied for most-frequent

    Returns:
        modes     -- list of all values that tied at the highest frequency
        max_freq  -- the frequency those values appeared at

    Bug to avoid: using max() returns only ONE value even when multiple
    values are tied. We must find the highest frequency first, then
    collect ALL values that reach that frequency.

    Valid scale: ALL scales (Nominal, Ordinal, Quantitative).
    """
    # Step 1: count how many times each value appears
    counts = Counter(nums)

    # Step 2: find the highest frequency (without using max())
    highest_freq = 0
    for freq in counts.values():
        if freq > highest_freq:
            highest_freq = freq

    # Step 3: collect ALL values that appear at the highest frequency
    modes = []
    for value, freq in counts.items():
        if freq == highest_freq:
            modes.append(value)

    modes.sort()   # sort for consistent display
    return modes, highest_freq


def compute_quartile(sorted_nums, k):
    """
    Compute the k-th quartile (k must be 1, 2, or 3) using the exact
    position method taught in the Ch.2 lecture:

    Steps:
      1. Calculate position  p = n * (k / 4)
      2. If p is a whole number  -> Q = average of values at positions p and p+1
         If p is not a whole number -> round p up, Q = value at that position
         (positions are 1-indexed, so subtract 1 for Python list access)

    The list must already be sorted in ascending order.
    """
    n = len(sorted_nums)
    p = n * (k / 4)    # exact position (may be a decimal)

    if p == int(p):
        # p is a whole number -> average of two positions
        # Example: n=10, k=2 -> p=5 -> average of positions 5 and 6
        idx   = int(p)                   # 1-indexed position
        left  = sorted_nums[idx - 1]     # convert to 0-indexed
        right = sorted_nums[idx]
        return (left + right) / 2
    else:
        # p is not a whole number -> round up, take that element
        # Example: n=14, k=1 -> p=3.5 -> round up to 4 -> position 4
        idx = math.ceil(p)               # 1-indexed position (rounded up)
        return sorted_nums[idx - 1]      # convert to 0-indexed


def compute_amplitude(sorted_nums):
    """
    Amplitude = max - min.
    The total spread of the data from lowest to highest.
    Simple but sensitive to outliers (one extreme value inflates it).
    """
    return sorted_nums[-1] - sorted_nums[0]   # last - first in sorted list


def compute_mad(nums, the_mean):
    """
    Mean Absolute Deviation (sample formula, denominator n-1).

    Formula: MAD = sum( |xi - mean| ) / (n - 1)

    Measures the average distance each value is from the mean.
    Uses n-1 instead of n (Bessel's correction) because we are working
    with a sample, not the full population.
    """
    n = len(nums)
    if n < 2:
        return 0.0

    # Sum of absolute deviations from the mean
    total_abs_deviation = 0.0
    for x in nums:
        total_abs_deviation += abs(x - the_mean)

    return total_abs_deviation / (n - 1)


def compute_std(nums, the_mean):
    """
    Sample standard deviation (Bessel's correction, denominator n-1).

    Formula: s = sqrt( sum( (xi - mean)^2 ) / (n - 1) )

    Steps:
      1. Subtract the mean from each value to get the deviation
      2. Square each deviation (makes negatives positive)
      3. Sum all squared deviations
      4. Divide by (n - 1)  <- Bessel's correction for sample estimate
      5. Take the square root to get back to original units

    The variance is the result before step 5 (squared std dev).
    """
    n = len(nums)
    if n < 2:
        return 0.0

    # Steps 1 + 2 + 3: sum of squared deviations
    sum_squared_deviations = 0.0
    for x in nums:
        deviation  = x - the_mean        # step 1: how far is x from the mean
        squared    = deviation ** 2       # step 2: square it
        sum_squared_deviations += squared  # step 3: add to running sum

    # Step 4: divide by (n - 1)
    variance = sum_squared_deviations / (n - 1)

    # Step 5: square root to get standard deviation
    std_dev = math.sqrt(variance)

    return std_dev


def compute_skewness(nums, the_mean, the_std):
    """
    Fisher's moment coefficient of skewness.

    Tells us whether the distribution has a longer tail on the left or right.

    Formula: skewness = ( sum( (xi - mean)^3 ) / n ) / std^3

    Result interpretation:
       ~0       -> symmetric (tails are roughly equal)
      Positive  -> right-skewed (long tail on the RIGHT, mass on LEFT)
      Negative  -> left-skewed  (long tail on the LEFT,  mass on RIGHT)
    """
    n = len(nums)
    if n < 3 or the_std == 0:
        return 0.0

    sum_cubed = 0.0
    for x in nums:
        sum_cubed += (x - the_mean) ** 3

    return (sum_cubed / n) / (the_std ** 3)


def skewness_label(skew):
    """
    Turn the numeric skewness value into a plain-English description
    matching the Ch.2 lecture taxonomy.
    """
    if abs(skew) < 0.5:
        return "Approximately symmetric"
    elif skew > 0:
        return "Positive (right) skew  -- long tail on the RIGHT"
    else:
        return "Negative (left) skew   -- long tail on the LEFT"


# ============================================================
# 5. CORE ANALYSIS FUNCTIONS
# ============================================================

def compute_all_stats(col_name, raw_values):
    """
    Compute every location and dispersion statistic for one numeric column.

    Returns a dict of all results, or None if there are no numeric values.
    """
    nums = parse_numeric(raw_values)
    n    = len(nums)

    if n == 0:
        return None   # nothing to compute; column has no numeric values

    # ---- Location ----
    the_mean   = compute_mean(nums)
    the_median = compute_median(nums)
    modes, mode_freq = compute_mode(nums)
    q1 = compute_quartile(nums, 1)
    q2 = compute_quartile(nums, 2)   # Q2 should equal the median
    q3 = compute_quartile(nums, 3)

    # ---- Dispersion ----
    amplitude = compute_amplitude(nums)
    iqr       = q3 - q1                         # Interquartile Range
    mad       = compute_mad(nums, the_mean)
    std       = compute_std(nums, the_mean)
    variance  = std ** 2

    # ---- Shape ----
    skew = compute_skewness(nums, the_mean, std)

    return {
        "col_name":    col_name,
        "n":           n,
        "missing":     len(raw_values) - n,
        # Location
        "min":         nums[0],       # first element of sorted list
        "max":         nums[-1],      # last element of sorted list
        "mean":        the_mean,
        "median":      the_median,
        "modes":       modes,
        "mode_freq":   mode_freq,
        "q1":          q1,
        "q2":          q2,
        "q3":          q3,
        # Dispersion
        "amplitude":   amplitude,
        "iqr":         iqr,
        "mad":         mad,
        "std":         std,
        "variance":    variance,
        # Shape
        "skewness":    skew,
        "skew_label":  skewness_label(skew),
        # Keep the raw sorted numbers for the box plot
        "sorted_nums": nums,
    }


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def print_separator(char="-", width=70):
    """Print a horizontal line made of the given character."""
    print(char * width)


def ascii_boxplot(stats, plot_width=60):
    """
    Draw a simple ASCII box plot showing the five-number summary:
        min  |  Q1  |  median  |  Q3  |  max

    How it works:
      - Map each value to a character position on a fixed-width line
      - Draw whisker lines (---) from min to Q1 and from Q3 to max
      - Draw the box (===) from Q1 to Q3
      - Mark special positions: | for min/median/max, [ for Q1, ] for Q3
    """
    lo  = stats["min"]
    hi  = stats["max"]
    rng = hi - lo

    if rng == 0:
        print("  (all values are identical, box plot not meaningful)")
        return

    def value_to_position(v):
        """Convert a data value to a character column index (0 to plot_width)."""
        return round((v - lo) / rng * plot_width)

    # Calculate character positions for each key value
    pos_min    = value_to_position(stats["min"])
    pos_q1     = value_to_position(stats["q1"])
    pos_median = value_to_position(stats["median"])
    pos_q3     = value_to_position(stats["q3"])
    pos_max    = value_to_position(stats["max"])

    # Build a list of spaces, then overwrite positions with the right characters
    line = [" "] * (plot_width + 1)

    # Draw left whisker: dashes from min to Q1
    for i in range(pos_min, pos_q1):
        line[i] = "-"

    # Draw right whisker: dashes from Q3 to max
    for i in range(pos_q3, pos_max + 1):
        line[i] = "-"

    # Draw the box: equals signs from Q1 to Q3
    for i in range(pos_q1, pos_q3 + 1):
        line[i] = "="

    # Draw the special markers (these overwrite the background characters)
    line[pos_min]    = "|"   # minimum
    line[pos_q1]     = "["   # first quartile (start of box)
    line[pos_median] = "|"   # median line inside the box
    line[pos_q3]     = "]"   # third quartile (end of box)
    line[pos_max]    = "|"   # maximum

    plot_string = "".join(line)

    print(f"\n  Box plot: {stats['col_name']}")
    print(
        f"  Min={stats['min']:.1f}  Q1={stats['q1']:.1f}  "
        f"Median={stats['median']:.1f}  Q3={stats['q3']:.1f}  Max={stats['max']:.1f}"
    )
    print(f"  {plot_string}")


def print_stats_report(stats):
    """
    Print all location, dispersion, and shape statistics for one column,
    plus an ASCII box plot and central tendency check.
    """
    if stats is None:
        return

    print_separator("=")
    print(f"  STATISTICS REPORT  |  Column: {stats['col_name']}")
    print(f"  n = {stats['n']}  |  Missing = {stats['missing']}")
    print_separator("=")

    # ---- Location statistics ----
    print("\n  LOCATION STATISTICS")
    print_separator("-", 50)
    print(f"  {'Min':<25} {stats['min']:.4f}")
    print(f"  {'Max':<25} {stats['max']:.4f}")
    print(f"  {'Mean (average)':<25} {stats['mean']:.4f}")

    # Mode: show ALL modes, and label whether it is uni/bi/multimodal
    mode_values_str = ", ".join(str(m) for m in stats["modes"])
    if len(stats["modes"]) == 1:
        mode_type = "unimodal"
    elif len(stats["modes"]) == 2:
        mode_type = "bimodal"
    else:
        mode_type = f"{len(stats['modes'])}-modal"
    print(f"  {'Mode':<25} {mode_values_str}  (freq={stats['mode_freq']}, {mode_type})")

    print(f"  {'Median (Q2)':<25} {stats['median']:.4f}")
    print(f"  {'Q1 (25th percentile)':<25} {stats['q1']:.4f}")
    print(f"  {'Q2 check':<25} {stats['q2']:.4f}  <- should equal Median")
    print(f"  {'Q3 (75th percentile)':<25} {stats['q3']:.4f}")

    # ---- Dispersion statistics ----
    print("\n  DISPERSION STATISTICS")
    print_separator("-", 50)
    print(f"  {'Amplitude (max - min)':<25} {stats['amplitude']:.4f}")
    print(f"  {'IQR (Q3 - Q1)':<25} {stats['iqr']:.4f}")
    print(f"  {'MAD (sample)':<25} {stats['mad']:.4f}")
    print(f"  {'Std Dev (sample)':<25} {stats['std']:.4f}")
    print(f"  {'Variance (sample)':<25} {stats['variance']:.4f}")

    # ---- Shape ----
    print("\n  SHAPE")
    print_separator("-", 50)
    print(f"  {'Skewness':<25} {stats['skewness']:+.4f}")
    print(f"  {'':<25} {stats['skew_label']}")

    # ASCII box plot
    ascii_boxplot(stats)

    # Central tendency check: compare mean vs median to confirm skew direction
    the_mean   = stats["mean"]
    the_median = stats["median"]

    print(f"\n  Central tendency check (from lecture):")

    if len(stats["modes"]) > 1:
        # Multimodal: just compare mean and median
        print(f"    Note: data is {len(stats['modes'])}-modal (modes: {mode_values_str})")
        print(f"    Median = {the_median:.2f}    Mean = {the_mean:.2f}")
    else:
        mode_val = float(stats["modes"][0])
        print(f"    Mode={mode_val:.2f}   Median={the_median:.2f}   Mean={the_mean:.2f}")

    if the_mean > the_median:
        print("    Mean > Median -> consistent with right (positive) skew")
    elif the_mean < the_median:
        print("    Mean < Median -> consistent with left (negative) skew")
    else:
        print("    Mean = Median -> consistent with symmetric distribution")

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
    """Run using the Friends dataset from the Ch.2 lecture slides."""
    print("\n  [Demo -- Friends dataset (from Ch.2 lecture slides)]\n")
    for col in ("Weight", "Height", "Max_temp"):
        stats = compute_all_stats(col, FRIENDS[col])
        print_stats_report(stats)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments: run the built-in demo
        run_demo()
    else:
        # One argument: path to a CSV file -> analyze all numeric columns
        path = sys.argv[1]
        try:
            columns, _ = load_csv(path)
            found_any = False
            for col_name, values in columns.items():
                stats = compute_all_stats(col_name, values)
                if stats is not None:
                    found_any = True
                    print_stats_report(stats)
            if not found_any:
                print("No numeric columns found in the file.")
        except FileNotFoundError:
            print(f"Error: file '{path}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
