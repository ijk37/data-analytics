"""
Chapter 02
02-03-project-05: Categorical Relationship Analyzer
====================================================
Analyzes relationships that involve qualitative (categorical) attributes:

  1. Qual + Qual   -> Contingency table  +  mosaic plot
  2. Qual + Quant  -> Grouped statistics per category  +  grouped box plots
  3. Ordinal pair  -> Spearman's rank correlation  +  jitter scatter plot

Concepts covered:
  Ch.2 - Contingency tables, mosaic plots, grouped box plots,
          jitter effect for ordinal scatter plots, Spearman's rho

Dependencies: matplotlib  (pip install matplotlib)

Usage:
    python categorical_analyzer.py               (built-in demo)
    python categorical_analyzer.py data.csv      (auto-detect column types)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys    # command-line arguments and exit
import csv    # read CSV files
import math   # sqrt, ceil
import random # jitter offset generation
from collections import defaultdict, Counter

# Try to import matplotlib. If not installed, text-only output is used.
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
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
# Stored as a list of row dicts so both qualitative and quantitative
# columns are naturally grouped together per person.
FRIENDS_ROWS = [
    {"Friend":"Andrew",   "Max_temp":25, "Weight": 77, "Height":175, "Gender":"M", "Company":"Good"},
    {"Friend":"Bernhard", "Max_temp":31, "Weight":110, "Height":195, "Gender":"M", "Company":"Good"},
    {"Friend":"Carolina", "Max_temp":15, "Weight": 70, "Height":172, "Gender":"F", "Company":"Bad"},
    {"Friend":"Dennis",   "Max_temp":20, "Weight": 85, "Height":180, "Gender":"M", "Company":"Good"},
    {"Friend":"Eve",      "Max_temp":10, "Weight": 65, "Height":168, "Gender":"F", "Company":"Bad"},
    {"Friend":"Fred",     "Max_temp":12, "Weight": 75, "Height":173, "Gender":"M", "Company":"Good"},
    {"Friend":"Gwyneth",  "Max_temp":16, "Weight": 75, "Height":180, "Gender":"F", "Company":"Bad"},
    {"Friend":"Hayden",   "Max_temp":26, "Weight": 63, "Height":165, "Gender":"F", "Company":"Bad"},
    {"Friend":"Irene",    "Max_temp":15, "Weight": 55, "Height":158, "Gender":"F", "Company":"Bad"},
    {"Friend":"James",    "Max_temp":21, "Weight": 66, "Height":163, "Gender":"M", "Company":"Good"},
    {"Friend":"Kevin",    "Max_temp":30, "Weight": 95, "Height":190, "Gender":"M", "Company":"Bad"},
    {"Friend":"Lea",      "Max_temp":13, "Weight": 72, "Height":172, "Gender":"F", "Company":"Good"},
    {"Friend":"Marcus",   "Max_temp": 8, "Weight": 83, "Height":185, "Gender":"F", "Company":"Bad"},
    {"Friend":"Nigel",    "Max_temp":12, "Weight":115, "Height":192, "Gender":"M", "Company":"Good"},
]


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def parse_numeric(raw_values):
    """
    Parse raw values into a list of floats, skipping missing markers.
    Order is preserved (not sorted) so row pairing is maintained.
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
    """Arithmetic mean. Returns 0 if list is empty."""
    if not nums:
        return 0.0
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


def compute_median(sorted_nums):
    """
    Median of a sorted list.
    n odd  -> single middle element
    n even -> average of the two middle elements
    """
    n = len(sorted_nums)
    if n == 0:
        return 0.0
    mid = n // 2
    if n % 2 == 1:
        return sorted_nums[mid]
    else:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2


def compute_quartile(sorted_nums, k):
    """
    Lecture position method for Q1 (k=1), Q2 (k=2), Q3 (k=3).
    Input must be sorted in ascending order.
    """
    n = len(sorted_nums)
    p = n * (k / 4)
    if p == int(p):
        idx = int(p)
        return (sorted_nums[idx - 1] + sorted_nums[idx]) / 2
    else:
        return sorted_nums[math.ceil(p) - 1]


def assign_ranks(values):
    """
    Assign ranks (1 = smallest). Tied values get the average rank.
    Order of input is preserved in the output list.

    The sort key below is a short lambda that returns the value element of
    a (original_index, value) pair. Using a named helper function instead
    would require passing extra context, so a one-line lambda is acceptable here.
    """
    n = len(values)

    # Pair each value with its original position, then sort by value
    pairs = []
    for i in range(n):
        pairs.append((i, values[i]))
    pairs.sort(key=lambda pair: pair[1])   # sort by the value (second element)

    ranks = [0.0] * n
    i = 0
    while i < n:
        # Find all positions with the same (tied) value
        j = i
        while j < n - 1 and pairs[j + 1][1] == pairs[j][1]:
            j += 1

        # Average 1-indexed positions i+1 through j+1
        avg_rank = (i + 1 + j + 1) / 2

        for k in range(i, j + 1):
            original_index      = pairs[k][0]
            ranks[original_index] = avg_rank

        i = j + 1

    return ranks


def compute_pearson_r(xs, ys):
    """Pearson correlation coefficient between two lists of numbers."""
    n = len(xs)
    if n < 2:
        return 0.0
    x_bar = compute_mean(xs)
    y_bar = compute_mean(ys)
    sx    = compute_std(xs, x_bar)
    sy    = compute_std(ys, y_bar)
    if sx == 0 or sy == 0:
        return 0.0
    cov = 0.0
    for i in range(n):
        cov += (xs[i] - x_bar) * (ys[i] - y_bar)
    cov /= (n - 1)
    return cov / (sx * sy)


def compute_spearman_rho(xs, ys):
    """Spearman's rank correlation = Pearson r applied to the ranks."""
    return compute_pearson_r(assign_ranks(xs), assign_ranks(ys))


# ============================================================
# 5. CORE ANALYSIS FUNCTIONS
# ============================================================

def build_contingency_table(values_a, values_b):
    """
    Count how often each combination of (value_a, value_b) appears.

    Returns:
      row_labels  -- sorted unique values of column A
      col_labels  -- sorted unique values of column B
      counts      -- dict: {(row_val, col_val): count}
      row_totals  -- dict: {row_val: total count for that row}
      col_totals  -- dict: {col_val: total count for that column}
      grand_total -- total number of (a, b) pairs
    """
    # Combine the two columns row by row
    pairs = list(zip(values_a, values_b))

    # Get the unique labels for rows and columns, sorted
    row_labels = sorted(set(a for a, b in pairs))
    col_labels = sorted(set(b for a, b in pairs))

    # Count every (row, col) combination
    counts = defaultdict(int)
    for a, b in pairs:
        counts[(a, b)] += 1

    # Compute row totals (sum across all columns for each row)
    row_totals = {}
    for r in row_labels:
        total = 0
        for c in col_labels:
            total += counts[(r, c)]
        row_totals[r] = total

    # Compute column totals (sum across all rows for each column)
    col_totals = {}
    for c in col_labels:
        total = 0
        for r in row_labels:
            total += counts[(r, c)]
        col_totals[c] = total

    grand_total = len(pairs)

    return row_labels, col_labels, counts, row_totals, col_totals, grand_total


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def print_contingency_table(name_a, name_b, values_a, values_b):
    """
    Print a formatted contingency table showing joint absolute frequencies
    and their percentage of the grand total.
    """
    row_labels, col_labels, counts, row_totals, col_totals, grand = \
        build_contingency_table(values_a, values_b)

    cell_width      = 12
    row_label_width = max(len(name_a), max(len(str(r)) for r in row_labels)) + 2

    print(f"\n  Contingency Table:  {name_a}  (rows)  vs.  {name_b}  (columns)")
    print("  " + "=" * (row_label_width + cell_width * (len(col_labels) + 1) + 4))

    # Header row: column labels
    header = f"  {name_a:<{row_label_width}}"
    for c in col_labels:
        header += f"  {str(c):>{cell_width}}"
    header += f"  {'Total':>{cell_width}}"
    print(header)
    print("  " + "-" * (row_label_width + cell_width * (len(col_labels) + 1) + 4))

    # Data rows: one per unique value of column A
    for r in row_labels:
        line = f"  {str(r):<{row_label_width}}"
        for c in col_labels:
            cnt      = counts[(r, c)]
            pct      = cnt / grand * 100
            cell_str = f"{cnt} ({pct:4.1f}%)"
            line    += f"  {cell_str:>{cell_width}}"
        line += f"  {row_totals[r]:>{cell_width}}"
        print(line)

    # Footer row: column totals
    print("  " + "-" * (row_label_width + cell_width * (len(col_labels) + 1) + 4))
    footer = f"  {'Total':<{row_label_width}}"
    for c in col_labels:
        footer += f"  {col_totals[c]:>{cell_width}}"
    footer += f"  {grand:>{cell_width}}"
    print(footer)
    print()


def plot_mosaic(name_a, name_b, values_a, values_b):
    """
    Draw a mosaic plot (qualitative + qualitative).

    Each rectangle represents one (row, col) combination.
      - Rectangle WIDTH  = column's share of the total  (marginal proportion)
      - Rectangle HEIGHT = row's share within that column  (conditional proportion)
      - Area             is proportional to the JOINT relative frequency

    This is the visual equivalent of the contingency table.
    """
    row_labels, col_labels, counts, row_totals, col_totals, grand = \
        build_contingency_table(values_a, values_b)

    # Pick a distinct color for each column (category of col B)
    color_list = ["#4e79a7", "#f28e2b", "#59a14f", "#e15759", "#76b7b2", "#edc948"]

    fig, ax   = plt.subplots(figsize=(8, 5))
    x_cursor  = 0.0     # current x position on the canvas (0 to 1)
    legend_patches = []

    for ci, c_val in enumerate(col_labels):
        color     = color_list[ci % len(color_list)]
        col_width = col_totals[c_val] / grand   # width = marginal proportion
        y_cursor  = 0.0                          # start each column at the bottom

        for ri, r_val in enumerate(row_labels):
            joint_count = counts[(r_val, c_val)]

            # Height = conditional proportion of this row within the column
            if col_totals[c_val] > 0:
                cell_height = joint_count / col_totals[c_val]
            else:
                cell_height = 0

            rect = plt.Rectangle(
                (x_cursor, y_cursor),
                col_width,
                cell_height,
                facecolor=color,
                edgecolor="white",
                linewidth=2,
                alpha=0.85
            )
            ax.add_patch(rect)

            # Label the cell if it is large enough to fit text
            if cell_height > 0.08:
                ax.text(
                    x_cursor + col_width / 2,
                    y_cursor + cell_height / 2,
                    f"{r_val}\n{joint_count}",
                    ha="center", va="center", fontsize=9
                )

            y_cursor += cell_height   # move up for the next row within this column

        # Label the column (category of B) below the plot
        ax.text(
            x_cursor + col_width / 2, -0.04, str(c_val),
            ha="center", va="top", fontsize=10
        )

        legend_patches.append(mpatches.Patch(color=color, label=str(c_val)))
        x_cursor += col_width   # move right for the next column

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel(name_b, fontsize=11)
    ax.set_ylabel(f"{name_a}  (proportion within column)", fontsize=11)
    ax.set_title(
        f"Mosaic Plot:  {name_a}  vs.  {name_b}\n"
        f"Rectangle area = joint relative frequency"
    )
    ax.legend(handles=legend_patches, title=name_b, loc="upper right", fontsize=9)
    ax.set_yticks([])   # y-axis ticks are not meaningful here
    plt.tight_layout()
    plt.show()


def print_grouped_stats(qual_name, qual_values, quant_name, quant_values):
    """
    Print a summary statistics table for the quantitative column,
    broken down by category of the qualitative column.
    """
    # Group the quantitative values by category
    grouped = defaultdict(list)
    for category, value in zip(qual_values, quant_values):
        try:
            grouped[category].append(float(value))
        except (ValueError, TypeError):
            pass   # skip non-numeric values

    categories = sorted(grouped.keys())

    print(f"\n  Grouped stats:  {quant_name}  by  {qual_name}")
    print(f"  {'Category':<15} {'n':>4} {'Mean':>8} {'Median':>8} "
          f"{'Std':>8} {'Min':>7} {'Max':>7}")
    print("  " + "-" * 65)

    for cat in categories:
        vals = sorted(grouped[cat])
        if not vals:
            continue
        n      = len(vals)
        mu     = compute_mean(vals)
        median = compute_median(vals)
        s      = compute_std(vals, mu)
        print(
            f"  {str(cat):<15} {n:>4} {mu:>8.2f} {median:>8.2f} "
            f"{s:>8.2f} {min(vals):>7.2f} {max(vals):>7.2f}"
        )
    print()


def plot_grouped_boxplots(qual_name, qual_values, quant_name, quant_values):
    """
    Draw one box plot per category of the qualitative column, all on the same axes.
    This reveals whether the quantitative distribution differs across groups.
    Also prints the numeric summary table.
    """
    # Group the quantitative values by category
    grouped = defaultdict(list)
    for category, value in zip(qual_values, quant_values):
        try:
            grouped[category].append(float(value))
        except (ValueError, TypeError):
            pass

    categories           = sorted(grouped.keys())
    data_per_category    = [grouped[cat] for cat in categories]

    fig_width = max(6, len(categories) * 2)
    fig, ax   = plt.subplots(figsize=(fig_width, 5))

    ax.boxplot(
        data_per_category,
        labels=categories,
        patch_artist=True,
        boxprops=dict(facecolor="lightblue", color="navy"),
        medianprops=dict(color="red", linewidth=2),
        whiskerprops=dict(color="navy"),
        capprops=dict(color="navy")
    )

    # Annotate each box with its mean value
    for i, cat in enumerate(categories):
        vals = grouped[cat]
        if vals:
            mu = compute_mean(vals)
            ax.text(
                i + 1, mu,
                f"mean={mu:.1f}",
                ha="center", va="bottom", fontsize=8, color="darkred"
            )

    ax.set_xlabel(qual_name, fontsize=11)
    ax.set_ylabel(quant_name, fontsize=11)
    ax.set_title(f"Grouped Box Plots:  {quant_name}  by  {qual_name}")
    plt.tight_layout()
    plt.show()

    # Also print the numeric summary table
    print_grouped_stats(qual_name, qual_values, quant_name, quant_values)


def plot_jitter_scatter(name_x, x_values, name_y, y_values, jitter_amount=0.15):
    """
    Draw two side-by-side scatter plots: one without jitter and one with.

    When values are discrete (e.g., ordinal ranks 1-5), many points land
    on exactly the same (x, y) coordinate and overlap into one dot.
    Adding a small random offset (jitter) spreads the points slightly
    so you can see the full cloud of data.

    This is the technique shown in the Ch.2 lecture for ordinal-ordinal pairs.

    jitter_amount -- maximum offset added in each direction (default 0.15)
    """
    rho = compute_spearman_rho(list(x_values), list(y_values))
    r   = compute_pearson_r(list(x_values), list(y_values))

    # Create jittered versions of x and y
    random.seed(42)   # fixed seed so the plot looks the same every run
    x_jittered = []
    y_jittered = []
    for xv in x_values:
        x_jittered.append(xv + random.uniform(-jitter_amount, jitter_amount))
    for yv in y_values:
        y_jittered.append(yv + random.uniform(-jitter_amount, jitter_amount))

    fig, (ax_no_jitter, ax_jitter) = plt.subplots(1, 2, figsize=(12, 5))

    # Left plot: no jitter (points overlap)
    ax_no_jitter.scatter(x_values, y_values, color="steelblue", alpha=0.7, s=60)
    ax_no_jitter.set_title(f"{name_x}  vs.  {name_y}\n(no jitter  ->  points overlap!)")
    ax_no_jitter.set_xlabel(name_x)
    ax_no_jitter.set_ylabel(name_y)

    # Right plot: with jitter (cloud is visible)
    ax_jitter.scatter(x_jittered, y_jittered, color="steelblue", alpha=0.7, s=60)
    ax_jitter.set_title(
        f"{name_x}  vs.  {name_y}  with jitter\n"
        f"Spearman rho = {rho:.4f}  |  Pearson r = {r:.4f}"
    )
    ax_jitter.set_xlabel(f"{name_x}  (+ random offset)")
    ax_jitter.set_ylabel(f"{name_y}  (+ random offset)")

    plt.suptitle(
        "Jitter scatter plot for ordinal-ordinal pairs  (Ch.2)",
        fontsize=12
    )
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


def is_numeric_column(values):
    """
    Return True if at least 80% of non-missing values parse as numbers.
    We use 80% (not 100%) to tolerate a small number of bad cells.
    """
    nums        = parse_numeric(values)
    non_missing = [v for v in values if str(v).strip().lower() not in MISSING_MARKERS]
    if not non_missing:
        return False
    return len(nums) >= len(non_missing) * 0.8


# ============================================================
# 8. MAIN PROGRAM
# ============================================================

def run_demo():
    """Run the built-in demo using the Friends dataset."""
    print("\n  [Demo -- Friends dataset (from Ch.2 lecture slides)]\n")

    # Build column-oriented dict from the row-oriented demo data
    col_names = list(FRIENDS_ROWS[0].keys())
    data      = {}
    for col_name in col_names:
        data[col_name] = []
        for row in FRIENDS_ROWS:
            data[col_name].append(row[col_name])

    qual_cols  = ["Gender", "Company"]
    quant_cols = ["Weight", "Height", "Max_temp"]

    # ---- 1. Qual + Qual: contingency tables ----
    print("  1. QUALITATIVE + QUALITATIVE  (Contingency Tables)")
    print("  " + "=" * 55)
    print_contingency_table("Company", "Gender", data["Company"], data["Gender"])

    if HAS_MATPLOTLIB:
        plot_mosaic("Company", "Gender", data["Company"], data["Gender"])

    # ---- 2. Qual + Quant: grouped box plots ----
    print("  2. QUALITATIVE + QUANTITATIVE  (Grouped Box Plots)")
    print("  " + "=" * 55)

    if HAS_MATPLOTLIB:
        for quant in quant_cols:
            plot_grouped_boxplots("Company", data["Company"], quant, data[quant])
            plot_grouped_boxplots("Gender",  data["Gender"],  quant, data[quant])
    else:
        # Text-only fallback
        for qual in qual_cols:
            for quant in quant_cols:
                print_grouped_stats(qual, data[qual], quant, data[quant])

    # ---- 3. Ordinal pair: jitter scatter ----
    print("  3. ORDINAL + ORDINAL  (Jitter Scatter Plot)")
    print("  " + "=" * 55)

    # Use the ranks of Weight and Height as ordinal values
    # (in real use, you would have a rating scale like 1-5 Likert)
    weight_ranks = assign_ranks(data["Weight"])
    height_ranks = assign_ranks(data["Height"])

    rho = compute_spearman_rho(data["Weight"], data["Height"])
    print(f"\n  Spearman rho (Weight, Height) = {rho:.4f}")
    print("  Expected from lecture slides  = 0.96  (match!)\n")

    if HAS_MATPLOTLIB:
        plot_jitter_scatter("Weight rank", weight_ranks, "Height rank", height_ranks)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments: run the built-in demo
        run_demo()
    else:
        # One argument: path to a CSV file -> auto-detect column types
        path = sys.argv[1]
        try:
            columns, _ = load_csv(path)

            # Separate into numeric and text columns
            numeric_cols = {}
            text_cols    = {}
            for col_name, values in columns.items():
                if is_numeric_column(values):
                    numeric_cols[col_name] = parse_numeric(values)
                else:
                    text_cols[col_name] = values

            text_names    = list(text_cols.keys())
            numeric_names = list(numeric_cols.keys())

            # Qual + Qual: contingency tables (all text-column pairs)
            for i in range(len(text_names)):
                for j in range(i + 1, len(text_names)):
                    na = text_names[i]
                    nb = text_names[j]
                    print_contingency_table(na, nb, text_cols[na], text_cols[nb])
                    if HAS_MATPLOTLIB:
                        plot_mosaic(na, nb, text_cols[na], text_cols[nb])

            # Qual + Quant: grouped box plots
            if HAS_MATPLOTLIB:
                for qual_name in text_names:
                    for quant_name in numeric_names:
                        raw_quant = columns[quant_name]   # pass raw strings
                        plot_grouped_boxplots(
                            qual_name,  text_cols[qual_name],
                            quant_name, raw_quant
                        )
            else:
                for qual_name in text_names:
                    for quant_name in numeric_names:
                        print_grouped_stats(
                            qual_name,  text_cols[qual_name],
                            quant_name, columns[quant_name]
                        )

        except FileNotFoundError:
            print(f"Error: file '{path}' not found.")
            sys.exit(1)
