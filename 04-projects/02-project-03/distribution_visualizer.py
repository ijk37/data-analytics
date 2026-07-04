"""
Chapter 02
02-03-project-03: Distribution Visualizer
==========================================
Visualizes empirical distributions for numeric columns:
  - Histogram  (with square-root bin rule from the lecture)
  - Box plot   (min, Q1, median, Q3, max with skewness annotation)
  - Normal distribution overlay fitted to the data
  - Normal vs. Uniform distribution side-by-side comparison
  - Combined histogram + box plot (as shown in lecture slides)

Concepts covered:
  Ch.2 - Histograms, bin selection, box plots, skewness,
          Normal distribution N(mu, sigma), Uniform distribution U(a, b)

Dependencies: matplotlib  (pip install matplotlib)

Usage:
    python distribution_visualizer.py               (built-in demo)
    python distribution_visualizer.py data.csv      (all numeric columns)
    python distribution_visualizer.py data.csv Age  (single column)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys   # command-line arguments and exit
import csv   # read CSV files
import math  # sqrt, ceil, pi, exp

# Try to import matplotlib. If it is not installed, we fall back to ASCII output.
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: matplotlib not found. Install with:  pip install matplotlib")
    print("Running in ASCII-only mode.\n")


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# Values that count as "missing" and should be skipped
MISSING_MARKERS = ("", "na", "nan", "null", "none", "?")


# ============================================================
# 3. DEMO DATASET
# ============================================================

# The Friends dataset from the Ch.2 lecture slides.
# Only the numeric columns are needed here.
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
    Returns a sorted list (sorting is required for quartile/median formulas).
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
    nums.sort()
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
    Returns 0 if there are fewer than 2 values.
    """
    n = len(nums)
    if n < 2:
        return 0.0

    sum_sq = 0.0
    for x in nums:
        sum_sq += (x - the_mean) ** 2

    return math.sqrt(sum_sq / (n - 1))


def compute_quartile(sorted_nums, k):
    """
    Lecture position method for Q1 (k=1), Q2 (k=2), Q3 (k=3).
    List must be sorted in ascending order.
    """
    n = len(sorted_nums)
    p = n * (k / 4)

    if p == int(p):
        idx = int(p)
        return (sorted_nums[idx - 1] + sorted_nums[idx]) / 2
    else:
        idx = math.ceil(p)
        return sorted_nums[idx - 1]


def compute_skewness(nums, the_mean, the_std):
    """
    Fisher's moment coefficient of skewness.
    Positive -> right-skewed, Negative -> left-skewed, ~0 -> symmetric.
    """
    n = len(nums)
    if n < 3 or the_std == 0:
        return 0.0

    sum_cubed = 0.0
    for x in nums:
        sum_cubed += (x - the_mean) ** 3

    return (sum_cubed / n) / (the_std ** 3)


def skewness_label(skew):
    """Plain-English label for a skewness value."""
    if abs(skew) < 0.5:
        return "~symmetric"
    elif skew > 0:
        return "right-skewed"
    else:
        return "left-skewed"


def suggest_bins(n):
    """
    Square-root rule of thumb for histogram bin count: bins ~ sqrt(n).
    The lecture says this is a starting point, not a strict rule.
    We use at least 3 bins so the histogram is never trivially small.
    """
    return max(3, round(math.sqrt(n)))


def normal_pdf(x, mu, sigma):
    """
    Normal (Gaussian) distribution probability density function.

    Formula: f(x) = (1 / (sigma * sqrt(2*pi))) * exp(-0.5 * ((x - mu) / sigma)^2)

    Parameters:
      mu    -- mean (center of the bell curve)
      sigma -- standard deviation (controls the width)
    """
    if sigma == 0:
        return 0.0
    exponent    = -0.5 * ((x - mu) / sigma) ** 2
    coefficient = 1.0 / (sigma * math.sqrt(2 * math.pi))
    return coefficient * math.exp(exponent)


def uniform_pdf(x, a, b):
    """
    Uniform distribution probability density function.

    Formula: f(x) = 1 / (b - a)  if a <= x <= b,  else 0

    All values in [a, b] have equal probability density.
    """
    if b == a:
        return 0.0
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0


# ============================================================
# 5. CORE ANALYSIS FUNCTIONS
# (No separate core function needed -- distribution computations
#  are performed directly inside the display/plot functions below)
# ============================================================


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def ascii_histogram(nums, col_name, n_bins=None):
    """
    Print a basic text histogram when matplotlib is not installed.
    Values are grouped into equal-width bins and a bar of # characters is drawn.
    """
    n = len(nums)
    if n_bins is None:
        n_bins = suggest_bins(n)

    lo  = min(nums)
    hi  = max(nums)
    rng = hi - lo

    if rng == 0:
        print(f"  {col_name}: all values are {lo}, histogram not meaningful.")
        return

    bin_width = rng / n_bins

    # Count how many values fall into each bin
    bin_counts = [0] * n_bins
    for v in nums:
        # Figure out which bin this value belongs to
        bin_index = int((v - lo) / bin_width)
        # The last value exactly equals hi, so clamp it to the last bin
        if bin_index >= n_bins:
            bin_index = n_bins - 1
        bin_counts[bin_index] += 1

    # Scale bars so the tallest bin = 40 characters
    max_count = max(bin_counts)
    bar_scale = 40.0 / max_count

    print(f"\n  ASCII Histogram: {col_name}")
    print(f"  n={n}, bins={n_bins}, bin width={bin_width:.2f}")
    print(f"  {'Range':<22}  {'Count':>5}  Bar")
    print("  " + "-" * 60)

    for i in range(n_bins):
        low_edge  = lo + i * bin_width
        high_edge = lo + (i + 1) * bin_width
        count = bin_counts[i]
        bar   = "#" * round(count * bar_scale)
        print(f"  [{low_edge:8.2f}, {high_edge:8.2f})  {count:>5}  {bar}")

    print()


def plot_combined(nums, col_name):
    """
    Combined chart: box plot on top + histogram below, sharing the same x-axis.
    This is the chart style shown on lecture slide p.45.

    Also overlays the fitted Normal PDF on the histogram to show whether
    the data looks approximately normal.
    """
    n_bins   = suggest_bins(len(nums))
    mu       = compute_mean(nums)
    sigma    = compute_std(nums, mu)
    skew     = compute_skewness(nums, mu, sigma)
    skew_lbl = skewness_label(skew)

    # Create two subplots that share the x-axis
    # The box plot is 1/4 as tall as the histogram
    fig, (ax_box, ax_hist) = plt.subplots(
        2, 1,
        figsize=(9, 6),
        sharex=True,
        gridspec_kw={"height_ratios": [1, 3], "hspace": 0.05}
    )

    # --- Top: horizontal box plot ---
    ax_box.boxplot(
        nums, vert=False, patch_artist=True,
        boxprops=dict(facecolor="lightblue", color="navy"),
        medianprops=dict(color="red", linewidth=2),
        whiskerprops=dict(color="navy"),
        capprops=dict(color="navy")
    )
    ax_box.set_yticks([])
    ax_box.set_title(
        f"Distribution of {col_name}  |  "
        f"skewness={skew:+.3f}  ({skew_lbl})"
    )

    # --- Bottom: histogram (density=True so y-axis matches the PDF) ---
    ax_hist.hist(
        nums, bins=n_bins, density=True,
        color="steelblue", alpha=0.7, edgecolor="white",
        label=f"Histogram (bins={n_bins}, sqrt rule)"
    )

    # --- Overlay fitted normal PDF ---
    if sigma > 0:
        # Generate 300 evenly-spaced x values spanning mu +/- 4 sigma
        x_start = mu - 4 * sigma
        x_end   = mu + 4 * sigma
        x_step  = (x_end - x_start) / 300

        x_vals = []
        y_vals = []
        x = x_start
        while x <= x_end:
            x_vals.append(x)
            y_vals.append(normal_pdf(x, mu, sigma))
            x += x_step

        ax_hist.plot(
            x_vals, y_vals, "r-", linewidth=2,
            label=f"Normal N(mu={mu:.1f}, sigma={sigma:.1f})"
        )

    # Vertical reference lines for mean and median
    ax_hist.axvline(mu, color="red", linestyle="--", alpha=0.7, label=f"Mean={mu:.1f}")
    median = compute_quartile(nums, 2)
    ax_hist.axvline(median, color="orange", linestyle="-.", alpha=0.7,
                    label=f"Median={median:.1f}")

    # Rug plot: tiny tick marks at the bottom showing individual data points
    rug_y = [-0.002] * len(nums)
    ax_hist.plot(nums, rug_y, "|", color="navy", alpha=0.5,
                 markersize=8, label="Individual values")

    ax_hist.set_xlabel(col_name)
    ax_hist.set_ylabel("Density")
    ax_hist.legend(fontsize=9)

    plt.tight_layout()
    plt.show()


def plot_distributions_comparison(mu, sigma, a, b):
    """
    Side-by-side comparison of Normal and Uniform distributions.
    Shows the conceptual difference between the two Ch.2 distributions.

    Parameters:
      mu, sigma  -- parameters for the Normal distribution  N(mu, sigma)
      a, b       -- parameters for the Uniform distribution U(a, b)
    """
    fig, (ax_normal, ax_uniform) = plt.subplots(1, 2, figsize=(12, 4))

    # --- Normal distribution ---
    x_lo  = mu - 4 * sigma
    x_hi  = mu + 4 * sigma
    step  = (x_hi - x_lo) / 400

    x_vals_n = []
    y_vals_n = []
    x = x_lo
    while x <= x_hi:
        x_vals_n.append(x)
        y_vals_n.append(normal_pdf(x, mu, sigma))
        x += step

    ax_normal.plot(x_vals_n, y_vals_n, "b-", linewidth=2)
    ax_normal.fill_between(x_vals_n, y_vals_n, alpha=0.3, color="blue")
    ax_normal.axvline(mu, color="red", linestyle="--", label=f"mean = {mu:.1f}")

    # Shade the mu +/- 1 sigma region (contains ~68% of data)
    x_1sigma = []
    y_1sigma = []
    for x in x_vals_n:
        if (mu - sigma) <= x <= (mu + sigma):
            x_1sigma.append(x)
            y_1sigma.append(normal_pdf(x, mu, sigma))
    ax_normal.fill_between(x_1sigma, y_1sigma, alpha=0.4, color="orange",
                           label="mu +/- 1 sigma  (~68%)")

    ax_normal.set_title(f"Normal Distribution  N({mu:.1f}, {sigma:.1f})")
    ax_normal.set_xlabel("x")
    ax_normal.set_ylabel("f(x)  [probability density]")
    ax_normal.legend(fontsize=8)

    # --- Uniform distribution ---
    padding = (b - a) * 0.3   # add space on each side so the flat top is visible
    x_lo_u  = a - padding
    x_hi_u  = b + padding
    step_u  = (x_hi_u - x_lo_u) / 400

    x_vals_u = []
    y_vals_u = []
    x = x_lo_u
    while x <= x_hi_u:
        x_vals_u.append(x)
        y_vals_u.append(uniform_pdf(x, a, b))
        x += step_u

    ax_uniform.plot(x_vals_u, y_vals_u, "g-", linewidth=2)
    ax_uniform.fill_between(x_vals_u, y_vals_u, alpha=0.3, color="green")
    ax_uniform.set_ylim(bottom=0)

    # Label the flat PDF value
    pdf_value = 1.0 / (b - a)
    mid_x     = (a + b) / 2
    ax_uniform.annotate(
        f"f(x) = 1 / ({b}-{a}) = {pdf_value:.3f}",
        xy=(mid_x, pdf_value),
        fontsize=10, ha="center", va="bottom"
    )

    ax_uniform.set_title(f"Uniform Distribution  U({a}, {b})")
    ax_uniform.set_xlabel("x")
    ax_uniform.set_ylabel("f(x)  [probability density]")

    plt.suptitle("Common Univariate Probability Distributions (Ch.2)", fontsize=12)
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

    # Print the suggested bin count for each column
    print("  Square-root bin rule (bins ~ sqrt(n)):")
    for col_name, values in FRIENDS.items():
        n = len(values)
        print(f"    {col_name}: n={n} -> {suggest_bins(n)} bins")
    print()

    if HAS_MATPLOTLIB:
        # Combined plot for each numeric column
        for col_name, values in FRIENDS.items():
            plot_combined(values, col_name)

        # Normal vs Uniform comparison using Weight as the example
        weight  = FRIENDS["Weight"]
        mu_w    = compute_mean(weight)
        sigma_w = compute_std(weight, mu_w)
        plot_distributions_comparison(
            mu=mu_w, sigma=sigma_w,
            a=min(weight), b=max(weight)
        )
    else:
        # Fall back to ASCII histograms
        for col_name, values in FRIENDS.items():
            ascii_histogram(values, col_name)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments: run the built-in demo
        run_demo()

    elif len(sys.argv) >= 2:
        path   = sys.argv[1]
        target = sys.argv[2] if len(sys.argv) == 3 else None

        try:
            columns, _ = load_csv(path)
            for col_name, raw_values in columns.items():
                # Skip columns we are not asked for
                if target is not None and col_name != target:
                    continue

                nums = parse_numeric(raw_values)
                if not nums:
                    continue   # skip columns with no numeric values

                if HAS_MATPLOTLIB:
                    plot_combined(nums, col_name)
                else:
                    ascii_histogram(nums, col_name)

        except FileNotFoundError:
            print(f"Error: file '{path}' not found.")
            sys.exit(1)
