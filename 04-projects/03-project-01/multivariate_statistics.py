"""
Chapter 03
03-03-project-01: Multivariate Statistics Explorer
===================================================
Computes four multivariate summary tables for any numeric dataset:
  1. Location matrix   -- min, Q1, median, mean, mode, Q3, max per attribute
  2. Dispersion matrix -- amplitude, IQR, MAD, std dev, variance per attribute
  3. Covariance matrix -- sample covariance for every pair of numeric attributes
  4. Pearson correlation matrix -- scale-independent linear correlation for every pair

Concepts covered:
  Ch.3 - Multivariate location/dispersion statistics, covariance matrix,
          Pearson correlation matrix

Usage:
    python multivariate_statistics.py              (built-in Friends demo)
    python multivariate_statistics.py data.csv     (all numeric columns of a CSV)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys   # command-line arguments and exit
import csv   # read CSV files
import math  # sqrt


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# Values that count as "missing" and should be skipped
MISSING_MARKERS = ("", "na", "nan", "null", "none", "?")

# Width of printed separators
SEPARATOR_WIDTH = 78


# ============================================================
# 3. DEMO DATASET
# ============================================================

# The Friends dataset from the Ch.3 lecture slides.
# Stored as a column-oriented dict (matches the format returned by load_csv).
# Only the four numeric columns are included here for multivariate analysis.
#
# Expected results (from the lecture):
#   Covariance diagonal:
#     Max_temp/Max_temp = 55.52,  Weight/Weight = 302.15
#     Height/Height     = 126.53, Years/Years   = 31.98
#   Pearson r:
#     Weight/Height = 0.94  (very strong positive)
#     All diagonal  = 1.00
FRIENDS_NUMERIC = {
    "Max_temp": [25, 31, 15, 20, 10, 12, 16, 26, 15, 21, 30, 13,  8, 12],
    "Weight":   [77,110, 70, 85, 65, 75, 75, 63, 55, 66, 95, 72, 83,115],
    "Height":   [175,195,172,180,168,173,180,165,158,163,190,172,185,192],
    "Years":    [10, 12,  2, 16,  0,  6,  3,  2,  5, 14,  1, 11,  3, 15],
}


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def parse_numeric_column(raw_values):
    """
    Convert a list of raw string values to floats, skipping missing markers.
    Returns the list of float values.
    Order is preserved so that row i in column X matches row i in column Y.
    """
    result = []
    for v in raw_values:
        v = str(v).strip()
        if v.lower() in MISSING_MARKERS:
            continue
        try:
            result.append(float(v))
        except ValueError:
            pass   # non-numeric text value; skip silently
    return result


def compute_mean(nums):
    """
    Arithmetic mean = sum of all values / count.
    """
    total = 0.0
    for x in nums:
        total += x
    return total / len(nums)


def compute_median(sorted_nums):
    """
    Median = middle value of a sorted list.
    If even count: average of the two middle values.
    """
    n   = len(sorted_nums)
    mid = n // 2

    if n % 2 == 1:
        return sorted_nums[mid]
    else:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0


def compute_quartiles(nums):
    """
    Compute Q1 and Q3 using the median-split method.

    Steps:
      1. Sort the values.
      2. Split into lower half and upper half (exclude the median for odd n).
      3. Q1 = median of the lower half.
         Q3 = median of the upper half.

    Returns: (Q1, Q3)
    """
    sorted_n = sorted(nums)
    n = len(sorted_n)
    mid = n // 2

    if n % 2 == 0:
        # Even: lower half is first half, upper half is second half
        lower_half = sorted_n[:mid]
        upper_half = sorted_n[mid:]
    else:
        # Odd: exclude the exact middle element from both halves
        lower_half = sorted_n[:mid]
        upper_half = sorted_n[mid + 1:]

    q1 = compute_median(lower_half)
    q3 = compute_median(upper_half)
    return q1, q3


def compute_mode(nums):
    """
    Find the most frequent value(s).
    Returns a list of all values that share the highest frequency.
    """
    # Count occurrences of each value
    counts = {}
    for x in nums:
        if x not in counts:
            counts[x] = 0
        counts[x] += 1

    # Find the highest frequency
    highest_freq = 0
    for freq in counts.values():
        if freq > highest_freq:
            highest_freq = freq

    # Collect all values with that frequency
    modes = []
    for value in sorted(counts.keys()):
        if counts[value] == highest_freq:
            modes.append(value)

    return modes


def compute_std(nums, the_mean):
    """
    Sample standard deviation (denominator n-1, Bessel's correction).
    Returns 0 if fewer than 2 values.
    """
    n = len(nums)
    if n < 2:
        return 0.0

    sum_sq = 0.0
    for x in nums:
        sum_sq += (x - the_mean) ** 2

    return math.sqrt(sum_sq / (n - 1))


def compute_variance(nums, the_mean):
    """
    Sample variance (denominator n-1).
    Returns 0 if fewer than 2 values.
    """
    n = len(nums)
    if n < 2:
        return 0.0

    sum_sq = 0.0
    for x in nums:
        sum_sq += (x - the_mean) ** 2

    return sum_sq / (n - 1)


def compute_mad(nums):
    """
    Median Absolute Deviation (MAD).

    Steps:
      1. Compute the median of the values.
      2. Compute the absolute deviation from the median for each value.
      3. Return the median of those absolute deviations.

    MAD is robust to outliers because it uses medians, not means.
    """
    sorted_n = sorted(nums)
    the_median = compute_median(sorted_n)

    # Build a list of absolute deviations from the median
    abs_deviations = []
    for x in nums:
        abs_deviations.append(abs(x - the_median))

    abs_deviations.sort()
    return compute_median(abs_deviations)


def compute_covariance(x_vals, y_vals):
    """
    Sample covariance between two numeric attributes.

    Formula: cov(X,Y) = (1/(n-1)) * sum[ (xi - x_bar)(yi - y_bar) ]

    Interpretation:
      Positive -> X and Y tend to move in the same direction
      Negative -> X and Y tend to move in opposite directions
      Near 0   -> no consistent linear co-variation

    Limitation: the value depends on the units of X and Y.
    """
    n = len(x_vals)
    if n < 2:
        return 0.0

    x_bar = compute_mean(x_vals)
    y_bar = compute_mean(y_vals)

    total = 0.0
    for i in range(n):
        deviation_x = x_vals[i] - x_bar
        deviation_y = y_vals[i] - y_bar
        total += deviation_x * deviation_y

    return total / (n - 1)


def compute_pearson_r(x_vals, y_vals):
    """
    Pearson correlation coefficient.

    Formula: r = cov(X,Y) / (std(X) * std(Y))

    Range: -1 (perfect negative linear) to +1 (perfect positive linear).
    The diagonal of the correlation matrix is always 1.00 (X vs. X).

    Unlike covariance, Pearson r is scale-independent: changing units
    does NOT change the value.
    """
    x_mean = compute_mean(x_vals)
    y_mean = compute_mean(y_vals)
    sx     = compute_std(x_vals, x_mean)
    sy     = compute_std(y_vals, y_mean)

    if sx == 0 or sy == 0:
        # One column has no variation; correlation is undefined; return 0
        return 0.0

    cov = compute_covariance(x_vals, y_vals)
    return cov / (sx * sy)


def interpret_r(r):
    """
    Return a plain-English label for a Pearson r value.

    Thresholds (absolute value):
      >= 0.90 -> very strong
      >= 0.70 -> strong
      >= 0.50 -> moderate
      >= 0.30 -> weak
      else    -> negligible
    """
    abs_r = abs(r)

    if abs_r >= 0.90:
        strength = "very strong"
    elif abs_r >= 0.70:
        strength = "strong"
    elif abs_r >= 0.50:
        strength = "moderate"
    elif abs_r >= 0.30:
        strength = "weak"
    else:
        strength = "negligible"

    if r > 0.0:
        direction = "positive"
    elif r < 0.0:
        direction = "negative"
    else:
        return "no correlation"

    return strength + " " + direction


# ============================================================
# 5. CORE ANALYSIS FUNCTIONS
# ============================================================

def compute_location_stats(numeric_cols):
    """
    Compute location statistics for every numeric column.

    Returns a dict:
        { col_name: { "min": ..., "q1": ..., "median": ...,
                      "mean": ..., "mode": [...], "q3": ..., "max": ... } }
    """
    result = {}

    for col_name in numeric_cols:
        nums = numeric_cols[col_name]

        if len(nums) == 0:
            continue

        sorted_n  = sorted(nums)
        the_mean  = compute_mean(nums)
        the_med   = compute_median(sorted_n)
        q1, q3    = compute_quartiles(nums)
        modes     = compute_mode(nums)

        result[col_name] = {
            "min":    sorted_n[0],
            "q1":     q1,
            "median": the_med,
            "mean":   the_mean,
            "mode":   modes,
            "q3":     q3,
            "max":    sorted_n[-1],
        }

    return result


def compute_dispersion_stats(numeric_cols):
    """
    Compute dispersion statistics for every numeric column.

    Returns a dict:
        { col_name: { "amplitude": ..., "iqr": ..., "mad": ...,
                      "std": ..., "variance": ... } }
    """
    result = {}

    for col_name in numeric_cols:
        nums = numeric_cols[col_name]

        if len(nums) < 2:
            continue

        the_mean  = compute_mean(nums)
        q1, q3    = compute_quartiles(nums)
        sorted_n  = sorted(nums)

        amplitude = sorted_n[-1] - sorted_n[0]
        iqr       = q3 - q1
        mad       = compute_mad(nums)
        std       = compute_std(nums, the_mean)
        variance  = compute_variance(nums, the_mean)

        result[col_name] = {
            "amplitude": amplitude,
            "iqr":       iqr,
            "mad":       mad,
            "std":       std,
            "variance":  variance,
        }

    return result


def compute_covariance_matrix(numeric_cols):
    """
    Compute the p x p sample covariance matrix for all numeric columns.

    Returns a 2D dict:
        { col_i: { col_j: cov_value } }

    The matrix is symmetric: matrix[i][j] == matrix[j][i].
    Diagonal entries matrix[i][i] are the sample variances.
    """
    col_names = list(numeric_cols.keys())
    matrix = {}

    for name_i in col_names:
        matrix[name_i] = {}
        for name_j in col_names:
            cov_val = compute_covariance(numeric_cols[name_i],
                                         numeric_cols[name_j])
            matrix[name_i][name_j] = cov_val

    return matrix


def compute_correlation_matrix(numeric_cols):
    """
    Compute the p x p Pearson correlation matrix for all numeric columns.

    Returns a 2D dict:
        { col_i: { col_j: r_value } }

    Properties:
      - Diagonal entries are always 1.00
      - Values range from -1 to +1
      - Symmetric: matrix[i][j] == matrix[j][i]
    """
    col_names = list(numeric_cols.keys())
    matrix = {}

    for name_i in col_names:
        matrix[name_i] = {}
        for name_j in col_names:
            if name_i == name_j:
                # A column perfectly correlates with itself
                r_val = 1.0
            else:
                r_val = compute_pearson_r(numeric_cols[name_i],
                                          numeric_cols[name_j])
            matrix[name_i][name_j] = r_val

    return matrix


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def print_sep(char="-", width=None):
    """Print a horizontal separator line."""
    if width is None:
        width = SEPARATOR_WIDTH
    print(char * width)


def print_location_matrix(location_stats):
    """
    Print the location statistics matrix.
    Rows = statistics (min, Q1, median, mean, mode, Q3, max).
    Columns = attribute names.
    """
    col_names = list(location_stats.keys())

    if not col_names:
        print("  (no numeric columns found)")
        return

    # Decide column width: enough to hold any value + column name
    col_w = 12

    print_sep("=")
    print("  LOCATION STATISTICS MATRIX")
    print("  Rows = statistics | Columns = numeric attributes")
    print_sep("=")

    # Header row: statistic label + one column per attribute
    header = f"  {'Statistic':<12}"
    for name in col_names:
        header += f"  {name:>{col_w}}"
    print(header)
    print_sep("-")

    # Define the rows we want to print and how to format each value
    row_labels = ["Min", "Q1", "Median", "Mean", "Mode", "Q3", "Max"]
    row_keys   = ["min", "q1", "median", "mean", "mode", "q3", "max"]

    for label, key in zip(row_labels, row_keys):
        line = f"  {label:<12}"
        for name in col_names:
            stats = location_stats[name]
            value = stats[key]

            if key == "mode":
                # mode is a list; join values with "/"
                mode_str = "/".join(f"{m:.0f}" for m in value)
                # Truncate if too long
                if len(mode_str) > col_w:
                    mode_str = mode_str[:col_w - 2] + ".."
                line += f"  {mode_str:>{col_w}}"
            else:
                line += f"  {value:>{col_w}.2f}"

        print(line)

    print_sep("=")
    print()


def print_dispersion_matrix(dispersion_stats):
    """
    Print the dispersion statistics matrix.
    Rows = statistics (amplitude, IQR, MAD, std dev, variance).
    Columns = attribute names.
    """
    col_names = list(dispersion_stats.keys())

    if not col_names:
        print("  (no numeric columns found)")
        return

    col_w = 12

    print_sep("=")
    print("  DISPERSION STATISTICS MATRIX")
    print("  Rows = statistics | Columns = numeric attributes")
    print_sep("=")

    header = f"  {'Statistic':<12}"
    for name in col_names:
        header += f"  {name:>{col_w}}"
    print(header)
    print_sep("-")

    row_labels = ["Amplitude", "IQR", "MAD", "Std Dev", "Variance"]
    row_keys   = ["amplitude", "iqr", "mad", "std", "variance"]

    for label, key in zip(row_labels, row_keys):
        line = f"  {label:<12}"
        for name in col_names:
            value = dispersion_stats[name][key]
            line += f"  {value:>{col_w}.4f}"
        print(line)

    print_sep("=")
    print()


def print_square_matrix(matrix, col_names, title, subtitle=""):
    """
    Print any square p x p matrix (covariance or correlation).

    Parameters:
        matrix    -- 2D dict { row_name: { col_name: value } }
        col_names -- ordered list of row/column names
        title     -- printed as heading
        subtitle  -- printed as a hint below the title
    """
    if not col_names:
        print("  (no numeric columns found)")
        return

    col_w = 10

    print_sep("=")
    print(f"  {title}")
    if subtitle:
        print(f"  {subtitle}")
    print_sep("=")

    # Header row with column names
    header = f"  {'':>14}"
    for name in col_names:
        # Truncate long names so columns stay aligned
        short = name[:col_w]
        header += f"  {short:>{col_w}}"
    print(header)
    print_sep("-")

    for row_name in col_names:
        # Truncate row label too
        short_row = row_name[:14]
        line = f"  {short_row:<14}"
        for col_name in col_names:
            value = matrix[row_name][col_name]
            line += f"  {value:>{col_w}.4f}"
        print(line)

    print_sep("=")
    print()


def print_correlation_interpretation(matrix, col_names):
    """
    Print a plain-English interpretation of the strongest
    off-diagonal Pearson r values.
    """
    print_sep(".")
    print("  CORRELATION INTERPRETATION  (off-diagonal only)")
    print_sep(".")

    pairs = []
    for i in range(len(col_names)):
        for j in range(i + 1, len(col_names)):
            ni = col_names[i]
            nj = col_names[j]
            r  = matrix[ni][nj]
            pairs.append((abs(r), r, ni, nj))

    # Sort by absolute r value, strongest first
    for k in range(len(pairs)):
        for m in range(k + 1, len(pairs)):
            if pairs[m][0] > pairs[k][0]:
                pairs[k], pairs[m] = pairs[m], pairs[k]

    for abs_r, r, ni, nj in pairs:
        label = interpret_r(r)
        print(f"  {ni} / {nj}: r = {r:+.4f}  ({label})")

    print_sep(".")
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


def extract_numeric_columns(columns):
    """
    Given a column-oriented dict of raw strings, return a new dict
    containing only the columns where all non-missing values are numeric.
    Values are converted to float.
    """
    numeric_cols = {}
    for col_name in columns:
        nums = parse_numeric_column(columns[col_name])
        if len(nums) > 0:
            numeric_cols[col_name] = nums
    return numeric_cols


# ============================================================
# 8. MAIN PROGRAM
# ============================================================

def run_analysis(numeric_cols, dataset_name=""):
    """
    Run the full multivariate statistics analysis on the given numeric columns
    and print all four matrices.
    """
    col_names = list(numeric_cols.keys())

    if dataset_name:
        print(f"\n  [Dataset: {dataset_name}]")
    print(f"  Numeric columns: {col_names}")
    print(f"  n = {len(list(numeric_cols.values())[0])} objects\n")

    # --- Matrix 1: Location statistics ---
    location_stats = compute_location_stats(numeric_cols)
    print_location_matrix(location_stats)

    # --- Matrix 2: Dispersion statistics ---
    dispersion_stats = compute_dispersion_stats(numeric_cols)
    print_dispersion_matrix(dispersion_stats)

    # --- Matrix 3: Covariance matrix ---
    cov_matrix = compute_covariance_matrix(numeric_cols)
    print_square_matrix(
        cov_matrix,
        col_names,
        title="COVARIANCE MATRIX",
        subtitle="Diagonal = variance; symmetric; scale-DEPENDENT"
    )

    # --- Matrix 4: Pearson correlation matrix ---
    cor_matrix = compute_correlation_matrix(numeric_cols)
    print_square_matrix(
        cor_matrix,
        col_names,
        title="PEARSON CORRELATION MATRIX",
        subtitle="Diagonal = 1.00; range -1 to +1; scale-INDEPENDENT"
    )

    # Interpretation of correlation values
    print_correlation_interpretation(cor_matrix, col_names)


def run_demo():
    """Run the built-in demo using the Friends dataset from the Ch.3 lecture."""
    print("\n" + "=" * SEPARATOR_WIDTH)
    print("  Ch.03 Mini Project 01 -- Multivariate Statistics Explorer")
    print("  Demo: Friends dataset from lecture slides")
    print("=" * SEPARATOR_WIDTH)
    print()
    print("  Expected covariance diagonal (from lecture):")
    print("    Max_temp=55.52  Weight=302.15  Height=126.53  Years=31.98")
    print("  Expected Pearson r (from lecture):")
    print("    Weight/Height = 0.94   (very strong positive)")
    print()

    run_analysis(FRIENDS_NUMERIC, dataset_name="Friends (Ch.3 lecture)")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments: run the built-in demo
        run_demo()

    elif len(sys.argv) == 2:
        # One argument: path to a CSV file
        path = sys.argv[1]
        try:
            columns, n_rows = load_csv(path)
            numeric_cols    = extract_numeric_columns(columns)

            if len(numeric_cols) < 2:
                print("Need at least 2 numeric columns for multivariate analysis.")
                sys.exit(1)

            run_analysis(numeric_cols, dataset_name=path)

        except FileNotFoundError:
            print(f"Error: file '{path}' not found.")
            sys.exit(1)
        except ValueError as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    else:
        print("Usage:")
        print("  python multivariate_statistics.py")
        print("  python multivariate_statistics.py data.csv")
        sys.exit(1)
