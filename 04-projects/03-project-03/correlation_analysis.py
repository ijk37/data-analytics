"""
Chapter 03
03-03-project-03: Correlation & Heatmap Analysis
=================================================
Computes and visualizes correlation structure for multivariate data:
  1. Scatter plot matrix (SPLOM)     -- all pairs of attributes as scatter plots
  2. Correlation heatmap             -- color-coded Pearson r for all pairs
  3. ASCII correlation table         -- text table with significance stars
  4. Spearman correlation matrix     -- rank-based correlation (robust to outliers)

Concepts covered:
  Ch.3 - Scatter plot matrix (Draftsman's display), Pearson correlation matrix,
          Spearman correlation, correlogram/heatmap

Dependencies: matplotlib  (pip install matplotlib)
              pure-stdlib ASCII output works without matplotlib

Usage:
    python correlation_analysis.py              (built-in Friends demo)
    python correlation_analysis.py data.csv     (all numeric columns of a CSV)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys   # command-line arguments and exit
import csv   # read CSV files
import math  # sqrt

# Try to import matplotlib; fall back to text-only mode if not installed.
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: matplotlib not found.  Install with:  pip install matplotlib")
    print("Running in text-only mode.\n")


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
# Only the four numeric columns used for correlation analysis.
# Expected: r(Weight, Height) = 0.94  (very strong positive)
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
            pass   # non-numeric text; skip
    return result


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


def compute_covariance(x_vals, y_vals):
    """
    Sample covariance.
    Formula: (1/(n-1)) * sum[ (xi - x_bar)(yi - y_bar) ]
    """
    n = len(x_vals)
    if n < 2:
        return 0.0

    x_bar = compute_mean(x_vals)
    y_bar = compute_mean(y_vals)

    total = 0.0
    for i in range(n):
        total += (x_vals[i] - x_bar) * (y_vals[i] - y_bar)

    return total / (n - 1)


def compute_pearson_r(x_vals, y_vals):
    """
    Pearson correlation coefficient.
    r = cov(X,Y) / (std(X) * std(Y))
    Range: -1 to +1; scale-independent.
    """
    x_mean = compute_mean(x_vals)
    y_mean = compute_mean(y_vals)
    sx     = compute_std(x_vals, x_mean)
    sy     = compute_std(y_vals, y_mean)

    if sx == 0 or sy == 0:
        return 0.0

    cov = compute_covariance(x_vals, y_vals)
    return cov / (sx * sy)


def get_second_element(pair):
    """
    Return the second element of a (index, value) pair.
    Used as a sort key in assign_ranks() to avoid lambda expressions.
    """
    return pair[1]


def assign_ranks(values):
    """
    Assign ranks (1 = smallest) to each value.
    Tied values receive the AVERAGE of the positions they would have occupied.

    Example:
      [5, 3, 3, 7]  ->  sorted: 3(1), 3(2), 5(3), 7(4)
      Both 3s tie at positions 1 and 2 -> rank = (1+2)/2 = 1.5
      Result: [3.0, 1.5, 1.5, 4.0]
    """
    n = len(values)

    # Create (original_index, value) pairs and sort by value
    index_value_pairs = []
    for i in range(n):
        index_value_pairs.append((i, values[i]))
    index_value_pairs.sort(key=get_second_element)

    ranks = [0.0] * n

    i = 0
    while i < n:
        # Find the end of a group of equal (tied) values
        j = i
        while j < n - 1 and index_value_pairs[j + 1][1] == index_value_pairs[j][1]:
            j += 1

        # Average rank for this tie group (1-indexed positions i+1 .. j+1)
        avg_rank = (i + 1 + j + 1) / 2.0

        # Write the average rank back to the original positions
        for k in range(i, j + 1):
            original_index      = index_value_pairs[k][0]
            ranks[original_index] = avg_rank

        i = j + 1

    return ranks


def compute_spearman_rho(x_vals, y_vals):
    """
    Spearman rank correlation = Pearson r applied to the ranks of X and Y.

    Advantages over Pearson:
      1. Detects any MONOTONIC relationship (not just linear)
      2. Robust to outliers (outliers only shift ranks slightly)
      3. Works for ordinal data

    Formula: rho = Pearson_r(rank(X), rank(Y))
    """
    rank_x = assign_ranks(x_vals)
    rank_y = assign_ranks(y_vals)
    return compute_pearson_r(rank_x, rank_y)


def interpret_r(r):
    """
    Plain-English strength label for a correlation coefficient.
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


def significance_stars(r):
    """
    Return significance star string based on |r| thresholds.
    These are approximate; true significance depends on n.

    |r| >= 0.70 -> ***  (very likely not zero)
    |r| >= 0.50 -> **   (probably not zero)
    |r| >= 0.30 -> *    (possibly not zero)
    else        -> (space)  (negligible)
    """
    abs_r = abs(r)
    if abs_r >= 0.70:
        return "***"
    elif abs_r >= 0.50:
        return "** "
    elif abs_r >= 0.30:
        return "*  "
    else:
        return "   "


# ============================================================
# 5. CORE ANALYSIS FUNCTIONS
# ============================================================

def compute_pearson_matrix(numeric_cols):
    """
    Compute the p x p Pearson correlation matrix.

    Returns:
        col_names -- ordered list of column names
        matrix    -- 2D dict { name_i: { name_j: r_value } }
    """
    col_names = list(numeric_cols.keys())
    matrix = {}

    for name_i in col_names:
        matrix[name_i] = {}
        for name_j in col_names:
            if name_i == name_j:
                matrix[name_i][name_j] = 1.0
            else:
                matrix[name_i][name_j] = compute_pearson_r(
                    numeric_cols[name_i],
                    numeric_cols[name_j]
                )

    return col_names, matrix


def compute_spearman_matrix(numeric_cols):
    """
    Compute the p x p Spearman rank correlation matrix.

    Returns:
        col_names -- ordered list of column names
        matrix    -- 2D dict { name_i: { name_j: rho_value } }
    """
    col_names = list(numeric_cols.keys())
    matrix = {}

    for name_i in col_names:
        matrix[name_i] = {}
        for name_j in col_names:
            if name_i == name_j:
                matrix[name_i][name_j] = 1.0
            else:
                matrix[name_i][name_j] = compute_spearman_rho(
                    numeric_cols[name_i],
                    numeric_cols[name_j]
                )

    return col_names, matrix


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def print_sep(char="-", width=None):
    """Print a horizontal separator line."""
    if width is None:
        width = SEPARATOR_WIDTH
    print(char * width)


def print_correlation_table(col_names, matrix, title="Pearson Correlation Matrix"):
    """
    Print the correlation matrix as an ASCII table with significance stars.

    Stars:
      *** -> |r| >= 0.70
      **  -> |r| >= 0.50
      *   -> |r| >= 0.30
      (space) -> negligible

    Parameters:
        col_names -- ordered list of column names
        matrix    -- 2D dict from compute_pearson_matrix or compute_spearman_matrix
        title     -- heading to print above the table
    """
    print_sep("=")
    print(f"  {title}")
    print("  Stars: *** |r|>=0.70  ** |r|>=0.50  * |r|>=0.30  (blank) negligible")
    print_sep("=")

    col_w = 10  # width of each data column

    # Print header row
    header = f"  {'':>14}"
    for name in col_names:
        short = name[:col_w]
        header += f"  {short:>{col_w}}"
    print(header)
    print_sep("-")

    # Print each row
    for row_name in col_names:
        short_row = row_name[:14]
        line = f"  {short_row:<14}"
        for col_name in col_names:
            r     = matrix[row_name][col_name]
            stars = significance_stars(r) if row_name != col_name else "   "
            # Format: value + stars in one cell
            cell = f"{r:+.3f}{stars}"
            line += f"  {cell:>{col_w + 3}}"
        print(line)

    print_sep("=")
    print()


def print_comparison_table(col_names, pearson_matrix, spearman_matrix):
    """
    Print Pearson r and Spearman rho side by side for every off-diagonal pair.
    This makes it easy to spot pairs where the two measures differ.
    """
    print_sep("=")
    print("  PEARSON vs. SPEARMAN COMPARISON  (off-diagonal pairs)")
    print("  Large difference -> outliers or non-linear monotonic relationship")
    print_sep("=")
    print(f"  {'Pair':<26}  {'Pearson r':>10}  {'Spearman rho':>12}  {'Diff':>8}  Note")
    print_sep("-")

    for i in range(len(col_names)):
        for j in range(i + 1, len(col_names)):
            ni  = col_names[i]
            nj  = col_names[j]
            r   = pearson_matrix[ni][nj]
            rho = spearman_matrix[ni][nj]
            diff = r - rho

            note = ""
            if abs(diff) > 0.05:
                if diff > 0:
                    note = "outlier may inflate Pearson"
                else:
                    note = "non-linear monotonic trend"

            pair_label = f"{ni[:10]} / {nj[:10]}"
            print(f"  {pair_label:<26}  {r:>+10.4f}  {rho:>+12.4f}  {diff:>+8.4f}  {note}")

    print_sep("=")
    print()


def plot_scatter_matrix(numeric_cols, title=None):
    """
    Draw a scatter plot matrix (SPLOM / Draftsman's display).

    Concept:
      A p x p grid of scatter plots.
      Cell (i, j) shows attribute i on the y-axis vs attribute j on the x-axis.
      The diagonal cell shows the attribute name (no scatter for X vs X).
      Every pair of attributes is visible at a glance.

    Parameters:
        numeric_cols -- { col_name: [float values] }
        title        -- optional figure title
    """
    col_names  = list(numeric_cols.keys())
    col_values = list(numeric_cols.values())
    n_cols     = len(col_names)

    if not HAS_MATPLOTLIB:
        print("  [TEXT MODE] Scatter plot matrix not available without matplotlib.")
        print("  Showing Pearson r instead:\n")
        _, pearson_matrix = compute_pearson_matrix(numeric_cols)
        print_correlation_table(col_names, pearson_matrix,
                                title="Pearson r (replaces scatter matrix in text mode)")
        return

    fig_size = max(6, n_cols * 2)
    fig, axes = plt.subplots(n_cols, n_cols, figsize=(fig_size, fig_size))

    for i in range(n_cols):
        for j in range(n_cols):
            ax = axes[i][j]

            if i == j:
                # Diagonal: show the attribute name in the center
                ax.set_facecolor("#f0f0f0")
                ax.text(0.5, 0.5, col_names[i],
                        ha="center", va="center",
                        fontsize=9, fontweight="bold",
                        transform=ax.transAxes)
                ax.set_xticks([])
                ax.set_yticks([])

            else:
                # Off-diagonal: scatter plot of column j (x) vs column i (y)
                x_data = col_values[j]
                y_data = col_values[i]

                ax.scatter(x_data, y_data,
                           s=12, alpha=0.7, color="steelblue",
                           edgecolors="none")

                # Compute and display Pearson r in the cell corner
                r = compute_pearson_r(x_data, y_data)
                ax.text(0.05, 0.92, f"r={r:+.2f}",
                        transform=ax.transAxes,
                        fontsize=7, color="darkred",
                        va="top")

                # Only show axis labels on the outer edges
                if i == n_cols - 1:
                    ax.set_xlabel(col_names[j], fontsize=7)
                if j == 0:
                    ax.set_ylabel(col_names[i], fontsize=7)

                ax.tick_params(labelsize=6)

    fig.suptitle(title or "Scatter Plot Matrix (SPLOM)",
                 fontsize=12, y=1.01)
    plt.tight_layout()
    plt.show()


def plot_correlation_heatmap(col_names, matrix, title=None):
    """
    Draw a color-coded heatmap of the correlation matrix.

    Color scale:
      Blue shades  -> positive correlation (deeper = stronger)
      Red shades   -> negative correlation (deeper = stronger)
      Near-white   -> near-zero correlation

    Each cell shows the r value as text, white if |r| >= 0.7 else black.

    Parameters:
        col_names -- ordered list of column names
        matrix    -- 2D dict of correlation values
        title     -- optional chart title
    """
    n_cols = len(col_names)

    if not HAS_MATPLOTLIB:
        print("  [TEXT MODE] Correlation heatmap not available without matplotlib.")
        print("  Use print_correlation_table() for ASCII output.\n")
        return

    fig_size = max(5, n_cols * 1.1)
    fig, ax  = plt.subplots(figsize=(fig_size, fig_size * 0.9))

    for i in range(n_cols):
        for j in range(n_cols):
            r = matrix[col_names[i]][col_names[j]]

            # Build the cell color
            if r >= 0:
                red   = 1.0 - r       # less red as r increases
                green = 1.0 - r       # less green as r increases
                blue  = 1.0           # full blue for positive correlation
            else:
                red   = 1.0           # full red for negative correlation
                green = 1.0 + r       # less green as |r| increases
                blue  = 1.0 + r       # less blue  as |r| increases

            cell_color = (
                max(0.0, min(1.0, red)),
                max(0.0, min(1.0, green)),
                max(0.0, min(1.0, blue))
            )

            # Row i is plotted from the top (flip y axis)
            rect = plt.Rectangle(
                (j, n_cols - 1 - i), 1, 1,
                facecolor=cell_color,
                edgecolor="white",
                linewidth=1.0
            )
            ax.add_patch(rect)

            # Text label inside the cell
            text_color = "white" if abs(r) >= 0.7 else "black"
            ax.text(j + 0.5, n_cols - 1 - i + 0.5,
                    f"{r:+.2f}",
                    ha="center", va="center",
                    fontsize=9, color=text_color)

    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_cols)

    tick_positions = [i + 0.5 for i in range(n_cols)]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(col_names, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(tick_positions)
    ax.set_yticklabels(list(reversed(col_names)), fontsize=9)

    ax.set_title(title or "Correlation Matrix Heatmap\n"
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


def extract_numeric_columns(columns):
    """
    Return only the columns where all non-missing values can be parsed as float.
    Values are converted to float in the returned dict.
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
    Run the full correlation analysis on the given numeric columns.
    """
    col_names = list(numeric_cols.keys())

    if dataset_name:
        print(f"\n  [Dataset: {dataset_name}]")
    print(f"  Numeric columns: {col_names}")
    print(f"  n = {len(list(numeric_cols.values())[0])} objects\n")

    # ---- Pearson correlation matrix ----
    _, pearson_matrix = compute_pearson_matrix(numeric_cols)
    print_correlation_table(col_names, pearson_matrix,
                            title="PEARSON CORRELATION MATRIX")

    # ---- Spearman correlation matrix ----
    _, spearman_matrix = compute_spearman_matrix(numeric_cols)
    print_correlation_table(col_names, spearman_matrix,
                            title="SPEARMAN RANK CORRELATION MATRIX")

    # ---- Pearson vs Spearman comparison ----
    print_comparison_table(col_names, pearson_matrix, spearman_matrix)

    if HAS_MATPLOTLIB:
        # ---- Scatter plot matrix ----
        print("  Displaying scatter plot matrix...")
        plot_scatter_matrix(
            numeric_cols,
            title=f"Scatter Plot Matrix (SPLOM) -- {dataset_name or 'Dataset'}"
        )

        # ---- Pearson correlation heatmap ----
        print("  Displaying Pearson correlation heatmap...")
        plot_correlation_heatmap(
            col_names, pearson_matrix,
            title=f"Pearson Correlation Heatmap -- {dataset_name or 'Dataset'}"
        )

        # ---- Spearman correlation heatmap ----
        print("  Displaying Spearman correlation heatmap...")
        plot_correlation_heatmap(
            col_names, spearman_matrix,
            title=f"Spearman Correlation Heatmap -- {dataset_name or 'Dataset'}"
        )


def run_demo():
    """Run the built-in demo using the Friends dataset from the Ch.3 lecture."""
    print()
    print_sep("=")
    print("  Ch.03 Mini Project 03 -- Correlation & Heatmap Analysis")
    print("  Demo: Friends dataset from lecture slides")
    print_sep("=")
    print()
    print("  Expected Pearson r values (from lecture):")
    print("    Weight / Height   =  0.94  (very strong positive)")
    print("    Max_temp / Weight =  0.27  (negligible)")
    print("    Weight / Years    =  0.43  (weak positive)")
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
            columns, _ = load_csv(path)
            numeric_cols = extract_numeric_columns(columns)

            if len(numeric_cols) < 2:
                print("Need at least 2 numeric columns for correlation analysis.")
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
        print("  python correlation_analysis.py")
        print("  python correlation_analysis.py data.csv")
        sys.exit(1)
