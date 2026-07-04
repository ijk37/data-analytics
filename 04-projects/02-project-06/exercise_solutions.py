"""
Chapter 02
02-03-project-06: Chapter 2 Exercise Solutions
===============================================
Solves the three Ch.2 exercise questions using pure Python:

  Ex02a Q1  Frequency table for the Weight attribute (Friends dataset)
  Ex02a Q2  Mode, Median, Q1, Q3 for the Years attribute (Friends dataset)
  Ex02b Q1  Covariance, Pearson r, and Spearman rho for two short vectors

For each result the script prints:
  - The formula used
  - A step-by-step computation trace
  - The final value
  - Whether the result matches the expected exercise answer

Concepts: frequency tables, measures of location and spread, covariance,
Pearson's r, Spearman's rho (with tie handling).

Usage:
    python exercise_solutions.py
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys      # (not used at runtime, kept for structural consistency)
import math     # sqrt
import csv      # load_csv helper (no CSV needed for this project)
from collections import Counter  # value counting


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# ---------------------------------------------------------------------------
# Friends dataset (Ch.2 lecture slides) -- full version with Years column
# ---------------------------------------------------------------------------
FRIENDS = {
    "Friend":   ["Andrew", "Bernhard", "Carolina", "Dennis", "Eve", "Fred",
                 "Gwyneth", "Hayden", "Irene", "James", "Kevin", "Lea",
                 "Marcus", "Nigel"],
    "Max_temp": [25, 31, 15, 20, 10, 12, 16, 26, 15, 21, 30, 13,  8, 12],
    "Weight":   [77, 110, 70, 85, 65, 75, 75, 63, 55, 66, 95, 72, 83, 115],
    "Height":   [175, 195, 172, 180, 168, 173, 180, 165, 158, 163, 190, 172, 185, 192],
    "Gender":   ["M", "M", "F", "M", "F", "M", "F", "F", "F", "M", "M", "F", "F", "M"],
    "Company":  ["Good", "Good", "Bad", "Good", "Bad", "Good", "Bad", "Bad",
                 "Bad", "Good", "Bad", "Good", "Bad", "Good"],
    # Years of friendship: added for ex02a Q2
    "Years":    [5, 14, 2, 3, 16, 6, 11, 2, 15, 12, 0, 10, 1, 3],
}

# ---------------------------------------------------------------------------
# Ex02b Q1 -- given vectors
# ---------------------------------------------------------------------------
EX02B_X = [2, -1, 0, 1, -2, -3]
EX02B_Y = [-1,  1, -2, 0,  1,  2]

# ---------------------------------------------------------------------------
# Expected answers (from exercise key) -- used to verify results
# ---------------------------------------------------------------------------
EXPECTED = {
    # Ex02a Q1: Weight frequency table counts (sorted unique values)
    "weight_freq": {
        55: 1, 63: 1, 65: 1, 66: 1, 70: 1, 72: 1, 75: 2,
        77: 1, 83: 1, 85: 1, 95: 1, 110: 1, 115: 1,
    },
    # Ex02a Q2
    "years_mode":   [2, 3],          # both appear twice
    "years_median": 5.5,
    "years_q1":     2.0,
    "years_q3":     12.0,
    # Ex02b Q1
    "covariance":   -2.1,
    "pearson_r":    -0.7626,
    "spearman_rho": -0.8117,
}

# Values used as "missing" markers in load_csv
MISSING_MARKERS = ("", "na", "nan", "null", "none", "?")

# Tolerance for floating-point comparisons
TOLERANCE = 0.001

# Display width
SEP_WIDTH = 72


# ============================================================
# 3. DEMO DATASET
# ============================================================

# The Friends dataset is defined in CONSTANTS above (section 2).
# All three exercises use data from that single dataset or the
# short EX02B vectors.


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def separator(char="-", width=SEP_WIDTH):
    """Print a horizontal line made of the given character."""
    print(char * width)


def approx_equal(a, b, tol=TOLERANCE):
    """Return True if a and b differ by less than tol."""
    return abs(a - b) < tol


def compute_mean(nums):
    """Arithmetic mean = sum / count."""
    total = 0.0
    for x in nums:
        total += x
    return total / len(nums)


def compute_sample_std(nums, mean_val):
    """
    Sample standard deviation with Bessel's correction (n - 1).
    Returns 0.0 if fewer than 2 values.
    """
    n = len(nums)
    if n < 2:
        return 0.0
    sq_sum = 0.0
    for x in nums:
        sq_sum += (x - mean_val) ** 2
    return math.sqrt(sq_sum / (n - 1))


def get_value(pair):
    """
    Return the second element of a (index, value) pair.
    Used as sort key in assign_ranks (avoids lambda).
    """
    return pair[1]


def assign_ranks(values):
    """
    Assign ranks (1 = smallest) to each value, averaging ties.

    Tied values share the average of the positions they would occupy.
    Example: [5, 3, 3, 7]
      Sorted: 3(pos1), 3(pos2), 5(pos3), 7(pos4)
      Tied 3s get average rank (1+2)/2 = 1.5
      Result: [3.0, 1.5, 1.5, 4.0]
    """
    n = len(values)
    index_value_pairs = []
    for i in range(n):
        index_value_pairs.append((i, values[i]))
    index_value_pairs.sort(key=get_value)

    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n - 1 and index_value_pairs[j + 1][1] == index_value_pairs[j][1]:
            j += 1
        avg_rank = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            orig_idx = index_value_pairs[k][0]
            ranks[orig_idx] = avg_rank
        i = j + 1
    return ranks


# ============================================================
# 5. CORE ANALYSIS FUNCTIONS
# ============================================================

# ------------------------------------------------------------------
# Ex02a Q1: Frequency table
# ------------------------------------------------------------------

def build_frequency_table(values):
    """
    Build a complete frequency table for a list of numeric values.

    Returns a list of dicts, one per unique value (sorted ascending):
        value       -- the attribute value
        abs_freq    -- absolute frequency (count)
        rel_freq    -- relative frequency (count / total)
        cum_abs     -- cumulative absolute frequency
        cum_rel     -- cumulative relative frequency
    """
    total = len(values)
    counts = Counter(values)
    sorted_vals = sorted(counts.keys())

    rows = []
    cum_abs = 0
    cum_rel = 0.0

    for val in sorted_vals:
        abs_f = counts[val]
        rel_f = abs_f / total
        cum_abs += abs_f
        cum_rel += rel_f
        rows.append({
            "value":    val,
            "abs_freq": abs_f,
            "rel_freq": rel_f,
            "cum_abs":  cum_abs,
            "cum_rel":  cum_rel,
        })

    return rows


# ------------------------------------------------------------------
# Ex02a Q2: Mode, Median, Q1, Q3
# ------------------------------------------------------------------

def compute_mode(values):
    """
    Return a sorted list of all modes (values with the highest frequency).
    If every value is unique, all values are modes -- return them all.
    """
    counts = Counter(values)
    max_count = max(counts.values())
    modes = []
    for val, cnt in counts.items():
        if cnt == max_count:
            modes.append(val)
    modes.sort()
    return modes


def compute_median(sorted_vals):
    """
    Compute the median of an ALREADY SORTED list.
    For even n: average of the two middle values.
    For odd  n: the middle value.
    """
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0
    return float(sorted_vals[mid])


def compute_quartiles(sorted_vals):
    """
    Compute Q1 and Q3 using the textbook method:
      Split the data into a lower half and an upper half.
      For even n  : lower half = first n/2 values,
                    upper half = last  n/2 values.
      For odd n   : the median value is EXCLUDED from both halves.
      Q1 = median of the lower half
      Q3 = median of the upper half

    Returns (Q1, Q3).
    """
    n = len(sorted_vals)
    mid = n // 2

    if n % 2 == 0:
        lower_half = sorted_vals[:mid]
        upper_half = sorted_vals[mid:]
    else:
        lower_half = sorted_vals[:mid]
        upper_half = sorted_vals[mid + 1:]

    q1 = compute_median(lower_half)
    q3 = compute_median(upper_half)
    return q1, q3


# ------------------------------------------------------------------
# Ex02b Q1: Covariance, Pearson r, Spearman rho
# ------------------------------------------------------------------

def compute_covariance(x_vals, y_vals):
    """
    Sample covariance:
        cov(x, y) = (1/(n-1)) * sum( (xi - x_bar) * (yi - y_bar) )

    Returns the covariance value and a list of per-row deviation products
    for the step-by-step trace.
    """
    n = len(x_vals)
    x_bar = compute_mean(x_vals)
    y_bar = compute_mean(y_vals)

    products = []
    for i in range(n):
        dx = x_vals[i] - x_bar
        dy = y_vals[i] - y_bar
        products.append((x_vals[i], y_vals[i], dx, dy, dx * dy))

    total = 0.0
    for item in products:
        total += item[4]    # item[4] is dx * dy

    cov = total / (n - 1)
    return cov, products, x_bar, y_bar


def compute_pearson_r(x_vals, y_vals):
    """
    Pearson's r = cov(x, y) / (sx * sy)

    Returns (r, cov, sx, sy).
    """
    cov, _, x_bar, y_bar = compute_covariance(x_vals, y_vals)
    sx = compute_sample_std(x_vals, x_bar)
    sy = compute_sample_std(y_vals, y_bar)
    if sx == 0 or sy == 0:
        return 0.0, cov, sx, sy
    r = cov / (sx * sy)
    return r, cov, sx, sy


def compute_spearman_rho(x_vals, y_vals):
    """
    Spearman's rho = Pearson's r applied to the ranks of x and y.

    Returns (rho, rank_x, rank_y).
    """
    rank_x = assign_ranks(x_vals)
    rank_y = assign_ranks(y_vals)
    rho, _, _, _ = compute_pearson_r(rank_x, rank_y)
    return rho, rank_x, rank_y


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def print_frequency_table(rows, col_name, n_total):
    """Print a formatted frequency table."""
    separator("=")
    print(f"  FREQUENCY TABLE  --  {col_name}  (n = {n_total})")
    separator("-")
    print(f"  {'Value':>8}  {'Abs Freq':>9}  {'Rel Freq':>9}  "
          f"{'Cum Abs':>8}  {'Cum Rel':>8}")
    separator("-")
    for row in rows:
        print(
            f"  {row['value']:>8}  "
            f"{row['abs_freq']:>9}  "
            f"{row['rel_freq']:>9.4f}  "
            f"{row['cum_abs']:>8}  "
            f"{row['cum_rel']:>8.4f}"
        )
    separator("=")


def print_quartile_analysis(years, mode_vals, median_val, q1_val, q3_val):
    """
    Print a detailed step-by-step solution for Ex02a Q2:
    mode, median, Q1, Q3 for the Years attribute.
    """
    separator("=")
    print("  Ex02a Q2  --  Mode, Median, Q1, Q3  for  Years")
    separator("=")

    sorted_years = sorted(years)
    n = len(sorted_years)

    print(f"  Original values  : {years}")
    print(f"  Sorted values    : {sorted_years}   (n = {n})")
    separator("-")

    # Mode
    counts = Counter(years)
    print(f"  Step 1 -- Mode")
    print(f"    Count each value: {dict(sorted(counts.items()))}")
    max_count = max(counts.values())
    print(f"    Highest frequency = {max_count}")
    print(f"    Mode(s)           = {mode_vals}")
    separator(".")

    # Median
    mid = n // 2
    print(f"  Step 2 -- Median  (n = {n}, even -> average of positions {mid} and {mid+1})")
    print(f"    Sorted: {sorted_years}")
    print(f"    Middle two values: sorted[{mid-1}] = {sorted_years[mid-1]}, "
          f"sorted[{mid}] = {sorted_years[mid]}")
    print(f"    Median = ({sorted_years[mid-1]} + {sorted_years[mid]}) / 2 = {median_val}")
    separator(".")

    # Q1 / Q3
    lower_half = sorted_years[:mid]
    upper_half = sorted_years[mid:]
    print(f"  Step 3 -- Q1 and Q3 (split into two halves of {mid} values each)")
    print(f"    Lower half: {lower_half}")
    print(f"    Upper half: {upper_half}")

    lmid = len(lower_half) // 2
    print(f"    Q1 = median of lower half")
    print(f"       = ({lower_half[lmid-1]} + {lower_half[lmid]}) / 2 = {q1_val}")
    umid = len(upper_half) // 2
    print(f"    Q3 = median of upper half")
    print(f"       = ({upper_half[umid-1]} + {upper_half[umid]}) / 2 = {q3_val}")
    separator("=")


def print_covariance_steps(products, x_bar, y_bar, cov):
    """Print the step-by-step covariance calculation."""
    n = len(products)
    separator("=")
    print("  Ex02b Q1  --  COVARIANCE  (sample formula)")
    separator("=")
    print(f"  Formula: cov(x,y) = (1/(n-1)) * SUM( (xi - x_bar)(yi - y_bar) )")
    separator("-")
    print(f"  n = {n}")
    print(f"  x_bar = {x_bar:.4f}   y_bar = {y_bar:.4f}")
    separator("-")
    print(f"  {'i':>3}  {'xi':>6}  {'yi':>6}  {'xi-x_bar':>10}  "
          f"{'yi-y_bar':>10}  {'product':>10}")
    separator("-")
    total_prod = 0.0
    for i, (xi, yi, dx, dy, prod) in enumerate(products):
        total_prod += prod
        print(f"  {i+1:>3}  {xi:>6}  {yi:>6}  {dx:>10.4f}  {dy:>10.4f}  {prod:>10.4f}")
    separator("-")
    print(f"  Sum of products = {total_prod:.4f}")
    print(f"  cov = {total_prod:.4f} / (n-1) = {total_prod:.4f} / {n-1} = {cov:.4f}")
    separator("=")


def print_pearson_steps(x_vals, y_vals, r, cov, sx, sy):
    """Print the step-by-step Pearson r calculation."""
    n = len(x_vals)
    separator("=")
    print("  Ex02b Q1  --  PEARSON r")
    separator("=")
    print(f"  Formula: r = cov(x,y) / (sx * sy)")
    separator("-")
    print(f"  cov(x,y) = {cov:.4f}   (computed above)")
    print(f"  sx       = {sx:.4f}")
    print(f"  sy       = {sy:.4f}")
    print(f"  sx * sy  = {sx * sy:.4f}")
    print(f"  r        = {cov:.4f} / {sx * sy:.4f} = {r:.4f}")
    separator("=")


def print_spearman_steps(x_vals, y_vals, rho, rank_x, rank_y):
    """Print the step-by-step Spearman rho calculation."""
    separator("=")
    print("  Ex02b Q1  --  SPEARMAN rho")
    separator("=")
    print("  Method: Pearson's r applied to the RANKS of x and y.")
    print("  Ties share the average of their positions.")
    separator("-")
    print(f"  {'i':>3}  {'xi':>6}  {'yi':>6}  {'rank_x':>8}  {'rank_y':>8}")
    separator("-")
    for i in range(len(x_vals)):
        print(f"  {i+1:>3}  {x_vals[i]:>6}  {y_vals[i]:>6}  "
              f"{rank_x[i]:>8.1f}  {rank_y[i]:>8.1f}")
    separator("-")
    print(f"  Tie note: y has two values of 1 (positions 2 and 5 in sorted order)")
    print(f"            -> each gets rank (2+5)/2 = 3.5")
    print(f"  rho = Pearson r(rank_x, rank_y) = {rho:.4f}")
    separator("=")


def print_verification(label, computed, expected, tol=TOLERANCE):
    """
    Print a single-line verification: computed value vs. expected, PASS/FAIL.
    """
    if approx_equal(computed, expected, tol):
        status = "PASS"
    else:
        status = "FAIL"
    print(f"  {label:<30}  computed = {computed:>10.4f}  "
          f"expected = {expected:>10.4f}  [{status}]")


def print_mode_verification(computed_modes, expected_modes):
    """Verification for mode (list comparison)."""
    status = "PASS" if computed_modes == expected_modes else "FAIL"
    print(f"  {'Mode':<30}  computed = {computed_modes}  "
          f"expected = {expected_modes}  [{status}]")


# ============================================================
# 7. FILE I/O FUNCTIONS
# ============================================================

def load_csv(csv_file):
    """
    Read a CSV file and return a column-oriented dictionary:
        { column_name: [value1, value2, ...], ... }

    Also returns the number of data rows (not counting the header).

    Pivot from row-oriented to column-oriented:
    Before: rows = [{"Age": "25", "Name": "Alice"}, {"Age": "30", "Name": "Bob"}]
    After:  columns = {"Age": ["25", "30"], "Name": ["Alice", "Bob"]}
    """
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
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

def solve_ex02a_q1():
    """
    Ex02a Q1: Build and print the frequency table for the Weight attribute
    of the Friends dataset.  Verify each row's absolute frequency against
    the expected answer.
    """
    separator("=")
    print("  Ex02a Q1  --  Frequency Table for Weight (Friends dataset)")
    separator("=")
    print()

    weight_vals = FRIENDS["Weight"]
    n_total = len(weight_vals)

    rows = build_frequency_table(weight_vals)
    print_frequency_table(rows, "Weight", n_total)
    print()

    # Verification
    print("  Verification (absolute frequencies against exercise key):")
    separator("-")
    all_pass = True
    for row in rows:
        val = row["value"]
        expected_count = EXPECTED["weight_freq"].get(val, "?")
        if isinstance(expected_count, int):
            status = "PASS" if row["abs_freq"] == expected_count else "FAIL"
            if status == "FAIL":
                all_pass = False
        else:
            status = "N/A"
        print(f"    Weight = {val:>3}  freq = {row['abs_freq']}  "
              f"expected = {expected_count}  [{status}]")

    print()
    if all_pass:
        print("  All frequency counts match the exercise key.")
    else:
        print("  WARNING: one or more frequencies do not match the exercise key.")
    print()


def solve_ex02a_q2():
    """
    Ex02a Q2: Compute mode, median, Q1, Q3 for the Years attribute.
    Print a step-by-step solution and verify against the exercise key.
    """
    years = FRIENDS["Years"]

    mode_vals  = compute_mode(years)
    sorted_y   = sorted(years)
    median_val = compute_median(sorted_y)
    q1_val, q3_val = compute_quartiles(sorted_y)

    print_quartile_analysis(years, mode_vals, median_val, q1_val, q3_val)
    print()

    print("  Verification:")
    separator("-")
    print_mode_verification(mode_vals, EXPECTED["years_mode"])
    print_verification("Median",  median_val, EXPECTED["years_median"])
    print_verification("Q1",      q1_val,     EXPECTED["years_q1"])
    print_verification("Q3",      q3_val,     EXPECTED["years_q3"])
    print()


def solve_ex02b_q1():
    """
    Ex02b Q1: Compute covariance, Pearson r, and Spearman rho
    for x=(2,-1,0,1,-2,-3) and y=(-1,1,-2,0,1,2).
    Print step-by-step computations and verify against exercise key.
    """
    x = EX02B_X
    y = EX02B_Y

    separator("=")
    print("  Ex02b Q1  --  Bivariate Analysis")
    separator("=")
    print(f"  x = {x}")
    print(f"  y = {y}")
    print()

    # Covariance
    cov, products, x_bar, y_bar = compute_covariance(x, y)
    print_covariance_steps(products, x_bar, y_bar, cov)
    print()

    # Pearson r
    r, _, sx, sy = compute_pearson_r(x, y)
    print_pearson_steps(x, y, r, cov, sx, sy)
    print()

    # Spearman rho
    rho, rank_x, rank_y = compute_spearman_rho(x, y)
    print_spearman_steps(x, y, rho, rank_x, rank_y)
    print()

    # Verification summary
    separator("=")
    print("  VERIFICATION SUMMARY  --  Ex02b Q1")
    separator("-")
    print_verification("Covariance",   cov, EXPECTED["covariance"])
    print_verification("Pearson r",    r,   EXPECTED["pearson_r"])
    print_verification("Spearman rho", rho, EXPECTED["spearman_rho"])
    separator("=")
    print()


def main():
    """Run all three exercise solutions in sequence."""
    print()
    separator("=")
    print("  Ch.2 EXERCISE SOLUTIONS")
    print("  Source: Ch.2 exercises (ex02a and ex02b)")
    separator("=")
    print()

    solve_ex02a_q1()
    solve_ex02a_q2()
    solve_ex02b_q1()


if __name__ == "__main__":
    main()
