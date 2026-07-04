"""
Chapter 02
02-03-project-04: Bivariate Quantitative Analyzer
==================================================
Analyzes the relationship between pairs of numeric columns:
  - Scatter plot with trend line
  - Covariance (sample formula)
  - Pearson's correlation coefficient  r   (linear, scale-independent)
  - Spearman's rank correlation        rho (rank-based, robust to outliers)
  - Correlation matrix heatmap for all numeric columns

Concepts covered:
  Ch.2 - Covariance, Pearson r, Spearman rho, scatter plots,
          when to use which correlation measure

Dependencies: matplotlib  (pip install matplotlib)

Usage:
    python bivariate_quantitative.py               (built-in demo)
    python bivariate_quantitative.py data.csv      (all numeric pairs)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys   # command-line arguments and exit
import csv   # read CSV files
import math  # sqrt

# Try to import matplotlib. If it is not installed, text-only output is used.
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: matplotlib not found. Install with:  pip install matplotlib")
    print("Running in text-only mode.\n")


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# Values that count as "missing" and should be skipped
MISSING_MARKERS = ("", "na", "nan", "null", "none", "?")


# ============================================================
# 3. DEMO DATASET
# ============================================================

# The Friends dataset from the Ch.2 lecture slides.
# Only the three numeric columns are needed for bivariate analysis.
# Expected results (from lecture):
#   Pearson  r   (Weight, Height) = 0.94
#   Spearman rho (Weight, Height) = 0.96
FRIENDS = {
    "Max_temp": [25, 31, 15, 20, 10, 12, 16, 26, 15, 21, 30, 13,  8, 12],
    "Weight":   [77,110, 70, 85, 65, 75, 75, 63, 55, 66, 95, 72, 83,115],
    "Height":   [175,195,172,180,168,173,180,165,158,163,190,172,185,192],
}


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def parse_numeric(raw_values):
    """
    Convert raw string values to floats, skipping missing markers.
    The ORDER is preserved so that row i in column X matches row i in column Y.
    (We do NOT sort here, unlike project-02, because pairing rows matters.)
    """
    nums = []
    for v in raw_values:
        v = str(v).strip()
        if v.lower() in MISSING_MARKERS:
            continue
        try:
            nums.append(float(v))
        except ValueError:
            pass
    return nums


def compute_mean(nums):
    """Arithmetic mean = sum / count."""
    total = 0.0
    for x in nums:
        total += x
    return total / len(nums)


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


def get_second_element(pair):
    """
    Return the second element of a (index, value) pair.
    Used as the sort key in assign_ranks to avoid lambda expressions.
    """
    return pair[1]


def assign_ranks(values):
    """
    Assign a rank (1 = smallest) to each value in the list.
    Tied (equal) values get the AVERAGE of the positions they would have used.

    Example:
      values = [5, 3, 3, 7]
      Sorted order:  3(pos 1), 3(pos 2), 5(pos 3), 7(pos 4)
      The two 3s tie -> they share positions 1 and 2 -> rank = (1+2)/2 = 1.5
      Result: [3.0, 1.5, 1.5, 4.0]

    This is the standard tie-handling method described in the Ch.2 lecture.
    """
    n = len(values)

    # Create pairs of (original_index, value) and sort by value.
    # We keep the original index so we can put ranks back in the right places.
    index_value_pairs = []
    for i in range(n):
        index_value_pairs.append((i, values[i]))
    index_value_pairs.sort(key=get_second_element)   # sort by value (ascending)

    ranks = [0.0] * n   # output: rank for each original position

    i = 0
    while i < n:
        # Find the end of the current group of equal (tied) values
        j = i
        while j < n - 1 and index_value_pairs[j + 1][1] == index_value_pairs[j][1]:
            j += 1

        # All positions from i to j (inclusive) are tied.
        # Average rank = average of 1-indexed positions i+1 through j+1.
        avg_rank = (i + 1 + j + 1) / 2

        # Write the average rank back to every tied position
        for k in range(i, j + 1):
            original_index          = index_value_pairs[k][0]
            ranks[original_index]   = avg_rank

        i = j + 1   # move past this group of ties

    return ranks


def interpret_r(r):
    """
    Give a plain-English strength label for a correlation coefficient.

    Thresholds:
      |r| >= 0.9  -> very strong
      |r| >= 0.7  -> strong
      |r| >= 0.5  -> moderate
      |r| >= 0.3  -> weak
      otherwise   -> negligible
    """
    abs_r = abs(r)

    if abs_r >= 0.9:
        strength = "very strong"
    elif abs_r >= 0.7:
        strength = "strong"
    elif abs_r >= 0.5:
        strength = "moderate"
    elif abs_r >= 0.3:
        strength = "weak"
    else:
        strength = "negligible"

    if r > 0:
        direction = "positive"
    elif r < 0:
        direction = "negative"
    else:
        return "no correlation"

    return f"{strength} {direction}"


# ============================================================
# 5. CORE ANALYSIS FUNCTIONS
# ============================================================

def compute_covariance(x_vals, y_vals):
    """
    Sample covariance between two attributes.

    Formula: cov(x, y) = (1 / (n-1)) * sum( (xi - x_bar) * (yi - y_bar) )

    What the sign tells you:
      Positive -> when x is above its mean, y tends to be above its mean too
      Negative -> when x is above its mean, y tends to be below its mean
      Near 0   -> no consistent linear relationship

    Limitation: the VALUE depends on the units/scale of x and y.
      e.g., measuring weight in kg vs. grams gives different covariance values.
    """
    n = len(x_vals)
    if n < 2:
        return 0.0

    x_bar = compute_mean(x_vals)
    y_bar = compute_mean(y_vals)

    # Sum each row's contribution: (xi - x_bar) * (yi - y_bar)
    total = 0.0
    for i in range(n):
        deviation_x = x_vals[i] - x_bar
        deviation_y = y_vals[i] - y_bar
        total += deviation_x * deviation_y

    return total / (n - 1)


def compute_pearson_r(x_vals, y_vals):
    """
    Pearson's correlation: r = cov(x, y) / (sx * sy)

    Dividing by both standard deviations removes the unit dependency,
    giving a value always between -1 and +1.

      r = +1  -> perfect positive LINEAR relationship
      r =  0  -> no linear relationship
      r = -1  -> perfect negative LINEAR relationship

    Note: Pearson only captures LINEAR relationships.
    If the relationship is curved (but still monotonic), Spearman is better.
    """
    sx = compute_std(x_vals, compute_mean(x_vals))
    sy = compute_std(y_vals, compute_mean(y_vals))

    if sx == 0 or sy == 0:
        return 0.0   # one column has no variation; correlation is undefined

    cov = compute_covariance(x_vals, y_vals)
    return cov / (sx * sy)


def compute_spearman_rho(x_vals, y_vals):
    """
    Spearman's rank correlation = Pearson's r applied to the RANKS of x and y.

    Advantages over Pearson:
      1. Works for ORDINAL data (not just quantitative)
      2. Detects any MONOTONIC relationship (not just linear ones)
      3. ROBUST TO OUTLIERS because an outlier only gets a rank at the end,
         not the extreme numeric value that would inflate Pearson

    When data has no outliers and is roughly elliptical in shape,
    Spearman and Pearson give similar results.
    """
    rank_x = assign_ranks(x_vals)
    rank_y = assign_ranks(y_vals)
    return compute_pearson_r(rank_x, rank_y)


def analyze_pair(name_x, x_vals, name_y, y_vals):
    """
    Compute covariance, Pearson r, and Spearman rho for one pair of columns.

    Returns a dict of results, or None if there are too few shared rows.
    """
    n = len(x_vals)
    if n < 3:
        return None   # need at least 3 points for meaningful correlation

    cov = compute_covariance(x_vals, y_vals)
    r   = compute_pearson_r(x_vals, y_vals)
    rho = compute_spearman_rho(x_vals, y_vals)

    return {
        "name_x":         name_x,
        "name_y":         name_y,
        "n":              n,
        "x_vals":         x_vals,
        "y_vals":         y_vals,
        "covariance":     cov,
        "pearson_r":      r,
        "spearman_rho":   rho,
        "pearson_label":  interpret_r(r),
        "spearman_label": interpret_r(rho),
    }


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def print_report(result):
    """Print a readable text report for one (x, y) pair."""
    width = 70
    print(f"\n  {'=' * width}")
    print(f"  Bivariate Analysis:  {result['name_x']}  vs.  {result['name_y']}")
    print(f"  n = {result['n']}")
    print(f"  {'=' * width}")

    # Covariance
    cov = result["covariance"]
    print(f"\n  Covariance (sample formula, scale-DEPENDENT):")
    print(f"    cov = {cov:+.4f}")
    if cov > 0:
        print("    -> Positive: both attributes tend to increase together")
    elif cov < 0:
        print("    -> Negative: one increases as the other decreases")
    else:
        print("    -> Zero: no linear co-variation detected")
    print("    Warning: this value changes if you change the units!")

    # Pearson r
    r = result["pearson_r"]
    print(f"\n  Pearson r  (scale-INDEPENDENT, range: -1 to +1):")
    print(f"    r = {r:+.4f}  ->  {result['pearson_label']} linear relationship")
    print("    Measures LINEAR correlation only")

    # Spearman rho
    rho = result["spearman_rho"]
    print(f"\n  Spearman rho  (rank-based, range: -1 to +1):")
    print(f"    rho = {rho:+.4f}  ->  {result['spearman_label']} monotonic relationship")
    print("    Robust to outliers; works for ordinal data; detects non-linear trends")

    # Flag if Pearson and Spearman differ significantly
    diff = abs(r) - abs(rho)
    if abs(diff) > 0.05:
        print(f"\n  Note: |r| and |rho| differ by {abs(diff):.3f}")
        if diff > 0:
            print("    Pearson > Spearman: outliers may be inflating the linear correlation")
        else:
            print("    Spearman > Pearson: relationship may be monotonic but non-linear")

    print(f"  {'=' * width}\n")


def plot_scatter(result, ax=None):
    """
    Scatter plot for one pair of quantitative attributes.
    Includes a manually-computed least-squares trend line.
    """
    show_now = (ax is None)
    if show_now:
        fig, ax = plt.subplots(figsize=(7, 5))

    xs = result["x_vals"]
    ys = result["y_vals"]
    n  = result["n"]

    # Draw the scatter points
    ax.scatter(xs, ys, color="steelblue", alpha=0.75, s=60,
               edgecolors="navy", linewidths=0.5)

    # Compute the least-squares trend line manually.
    # slope = sum( (xi - x_bar)(yi - y_bar) ) / sum( (xi - x_bar)^2 )
    x_bar = compute_mean(xs)
    y_bar = compute_mean(ys)

    numerator   = 0.0
    denominator = 0.0
    for i in range(n):
        numerator   += (xs[i] - x_bar) * (ys[i] - y_bar)
        denominator += (xs[i] - x_bar) ** 2

    if denominator != 0:
        slope     = numerator / denominator
        intercept = y_bar - slope * x_bar

        x_lo = min(xs)
        x_hi = max(xs)
        y_lo = slope * x_lo + intercept
        y_hi = slope * x_hi + intercept

        ax.plot([x_lo, x_hi], [y_lo, y_hi],
                "r--", linewidth=1.5, alpha=0.7,
                label=f"Trend line (slope={slope:.3f})")

    r   = result["pearson_r"]
    rho = result["spearman_rho"]

    ax.set_title(
        f"{result['name_x']} vs. {result['name_y']}\n"
        f"Pearson r = {r:.4f}  ({result['pearson_label']})\n"
        f"Spearman rho = {rho:.4f}  ({result['spearman_label']})"
    )
    ax.set_xlabel(result["name_x"])
    ax.set_ylabel(result["name_y"])
    ax.legend(fontsize=9)

    if show_now:
        plt.tight_layout()
        plt.show()


def plot_correlation_matrix(numeric_cols):
    """
    Draw a color-coded grid (heatmap) showing Pearson r for every pair.
    Blue = positive correlation, Red = negative, White = near zero.
    """
    col_names  = list(numeric_cols.keys())
    col_values = list(numeric_cols.values())
    n_cols     = len(col_names)

    # Build the n x n matrix of correlation values
    matrix = []
    for i in range(n_cols):
        row = []
        for j in range(n_cols):
            if i == j:
                row.append(1.0)   # every column perfectly correlates with itself
            else:
                row.append(compute_pearson_r(col_values[i], col_values[j]))
        matrix.append(row)

    fig_size = max(6, n_cols * 1.2)
    fig, ax  = plt.subplots(figsize=(fig_size, fig_size * 0.9))

    # Draw one colored rectangle per cell
    for i in range(n_cols):
        for j in range(n_cols):
            r = matrix[i][j]

            # Mix color from white toward blue (positive) or red (negative)
            if r >= 0:
                red   = 1 - r   # less red as r grows
                green = 1 - r   # less green as r grows
                blue  = 1.0     # always full blue
            else:
                red   = 1.0     # always full red
                green = 1 + r   # less green as |r| grows
                blue  = 1 + r   # less blue  as |r| grows

            cell_color = (red, green, blue)

            # Row i is drawn from the BOTTOM, so flip the y-axis for readability
            rect = plt.Rectangle(
                (j, n_cols - 1 - i), 1, 1,
                facecolor=cell_color, edgecolor="gray", linewidth=0.5
            )
            ax.add_patch(rect)

            # Write the r value inside the cell
            text_color = "white" if abs(r) >= 0.7 else "black"
            ax.text(j + 0.5, n_cols - 1 - i + 0.5,
                    f"{r:.2f}",
                    ha="center", va="center", fontsize=9, color=text_color)

    # Axis labels
    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_cols)

    tick_positions = [i + 0.5 for i in range(n_cols)]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(col_names, rotation=45, ha="right")
    ax.set_yticks(tick_positions)
    ax.set_yticklabels(list(reversed(col_names)))

    ax.set_title("Pearson Correlation Matrix\n"
                 "Blue = positive  |  Red = negative  |  White = near zero")
    plt.tight_layout()
    plt.show()


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
    """Run the built-in demo using the Friends dataset."""
    print("\n  [Demo -- Friends dataset (from Ch.2 lecture slides)]\n")
    print("  Expected results (from lecture slides):")
    print("    Pearson  r   (Weight, Height) = 0.94")
    print("    Spearman rho (Weight, Height) = 0.96\n")

    cols      = FRIENDS
    col_names = list(cols.keys())

    # Print the text report for every column pair
    for i in range(len(col_names)):
        for j in range(i + 1, len(col_names)):
            nx     = col_names[i]
            ny     = col_names[j]
            result = analyze_pair(nx, cols[nx], ny, cols[ny])
            if result is not None:
                print_report(result)

    if HAS_MATPLOTLIB:
        # Scatter plots: one per pair, shown side by side
        pairs = []
        for i in range(len(col_names)):
            for j in range(i + 1, len(col_names)):
                pairs.append((col_names[i], col_names[j]))

        fig, axes = plt.subplots(1, len(pairs), figsize=(7 * len(pairs), 5))

        # If there is only one pair, axes is a single Axes object, not a list
        if len(pairs) == 1:
            axes = [axes]

        for ax, (nx, ny) in zip(axes, pairs):
            result = analyze_pair(nx, cols[nx], ny, cols[ny])
            if result is not None:
                plot_scatter(result, ax=ax)

        plt.suptitle("Bivariate Scatter Plots (Ch.2 Friends Dataset)", fontsize=13)
        plt.tight_layout()
        plt.show()

        # Correlation matrix heatmap
        plot_correlation_matrix(cols)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments: run the built-in demo
        run_demo()
    else:
        # One argument: path to a CSV file -> analyze all numeric column pairs
        path = sys.argv[1]
        try:
            columns, _ = load_csv(path)

            # Filter to only numeric columns for bivariate analysis
            numeric_cols = {}
            for col_name, raw_values in columns.items():
                nums = parse_numeric(raw_values)
                if nums:
                    numeric_cols[col_name] = nums

            col_names = list(numeric_cols.keys())

            if len(col_names) < 2:
                print("Need at least 2 numeric columns for bivariate analysis.")
                sys.exit(1)

            # Print text report for every pair
            for i in range(len(col_names)):
                for j in range(i + 1, len(col_names)):
                    nx     = col_names[i]
                    ny     = col_names[j]
                    result = analyze_pair(nx, numeric_cols[nx], ny, numeric_cols[ny])
                    if result is not None:
                        print_report(result)
                        if HAS_MATPLOTLIB:
                            plot_scatter(result)

            if HAS_MATPLOTLIB:
                plot_correlation_matrix(numeric_cols)

        except FileNotFoundError:
            print(f"Error: file '{path}' not found.")
            sys.exit(1)
