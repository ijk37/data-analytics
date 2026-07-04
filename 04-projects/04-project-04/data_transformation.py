"""
Chapter 4 -- Data Quality and Preprocessing
Mini-Project 04-03-04: Data Transformation

Demonstrates log, sqrt, absolute value, and Box-Cox transformations
using pure Python standard library only.

Run: python data_transformation.py
"""

# ===== SECTION 1: IMPORTS =====

import csv
import math


# ===== SECTION 2: CONSTANTS =====

EPSILON = 1e-10  # small value to avoid log(0)
BOXCOX_LAMBDAS = [-1.0, -0.5, 0.0, 0.5, 1.0, 2.0]  # lambdas to try


# ===== SECTION 3: DEMO DATASET =====

DEMO_SALARIES = [
    {"Person": "Alice",  "Salary": 35000,  "Years_exp": 1},
    {"Person": "Bob",    "Salary": 42000,  "Years_exp": 2},
    {"Person": "Carol",  "Salary": 38000,  "Years_exp": 1},
    {"Person": "Dave",   "Salary": 45000,  "Years_exp": 3},
    {"Person": "Eve",    "Salary": 52000,  "Years_exp": 4},
    {"Person": "Frank",  "Salary": 48000,  "Years_exp": 3},
    {"Person": "Grace",  "Salary": 95000,  "Years_exp": 8},
    {"Person": "Hank",   "Salary": 120000, "Years_exp": 12},
    {"Person": "Irene",  "Salary": 58000,  "Years_exp": 5},
    {"Person": "Jack",   "Salary": 67000,  "Years_exp": 6},
    {"Person": "Karl",   "Salary": 250000, "Years_exp": 15},
    {"Person": "Lea",    "Salary": 310000, "Years_exp": 20},
    {"Person": "Marcus", "Salary": 72000,  "Years_exp": 7},
    {"Person": "Nina",   "Salary": 880000, "Years_exp": 25},
    {"Person": "Oscar",  "Salary": 55000,  "Years_exp": 5},
]

# Temperature deviations from a baseline (can be negative)
DEMO_DEVIATIONS = [-15, 8, -3, 22, -18, 5, -9, 14, -7, 11, -20, 3, -1, 16, -12]


# ===== SECTION 4: HELPER FUNCTIONS =====

def compute_mean(values):
    """Return the arithmetic mean of a list of numbers."""
    total = 0.0
    for v in values:
        total += v
    return total / len(values)


def compute_median(values):
    """Return the median of a list of numbers."""
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 1:
        # Odd count: middle element
        return float(sorted_vals[mid])
    else:
        # Even count: average of two middle elements
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0


def compute_std(values):
    """Return the population standard deviation of a list of numbers."""
    mean = compute_mean(values)
    squared_diffs_sum = 0.0
    for v in values:
        diff = v - mean
        squared_diffs_sum += diff * diff
    variance = squared_diffs_sum / len(values)
    return math.sqrt(variance)


def compute_skewness(values):
    """
    Return Pearson's moment coefficient of skewness.
    Formula: skewness = (1/n) * sum( ((xi - mean) / std)^3 )
    """
    n = len(values)
    mean = compute_mean(values)
    std = compute_std(values)
    if std < EPSILON:
        # All values identical -- no skewness
        return 0.0
    cube_sum = 0.0
    for v in values:
        standardized = (v - mean) / std
        cube_sum += standardized ** 3
    return cube_sum / n


def describe_skewness(skew_value):
    """
    Return a human-readable description of skewness.
    Thresholds: |skew| < 0.5 -> symmetric, 0.5-1.0 -> moderate, >1.0 -> strong
    """
    if skew_value > 0.5:
        return "right-skewed (positive)"
    elif skew_value < -0.5:
        return "left-skewed (negative)"
    else:
        return "approximately symmetric"


# ===== SECTION 5: CORE ANALYSIS =====

def log_transform(values, base="natural", shift=0):
    """
    Apply log transformation to each value.

    Parameters
    ----------
    values : list of float
    base   : "natural" -> math.log, "10" -> math.log10, "2" -> math.log2
    shift  : added to each value before logging (use shift=1 when data may be 0)

    Returns
    -------
    list of float

    Raises
    ------
    ValueError if any (x + shift) <= 0
    """
    result = []
    for x in values:
        arg = x + shift
        if arg <= 0:
            raise ValueError(
                "log_transform: value {} + shift {} = {} is not positive. "
                "Use shift=1 or remove non-positive values.".format(x, shift, arg)
            )
        if base == "natural":
            result.append(math.log(arg))
        elif base == "10":
            result.append(math.log10(arg))
        elif base == "2":
            result.append(math.log2(arg))
        else:
            raise ValueError("base must be 'natural', '10', or '2'. Got: {}".format(base))
    return result


def sqrt_transform(values, shift=0):
    """
    Apply square root transformation: x' = sqrt(x + shift).

    Parameters
    ----------
    values : list of float
    shift  : added before taking sqrt (use shift > 0 for negative values)

    Raises
    ------
    ValueError if any (x + shift) < 0
    """
    result = []
    for x in values:
        arg = x + shift
        if arg < 0:
            raise ValueError(
                "sqrt_transform: value {} + shift {} = {} is negative.".format(x, shift, arg)
            )
        result.append(math.sqrt(arg))
    return result


def abs_transform(values):
    """
    Apply absolute value transformation: x' = |x|.
    Useful when only the magnitude matters, not the direction.

    Returns list of non-negative floats.
    """
    result = []
    for x in values:
        result.append(abs(x))
    return result


def boxcox_transform(values, lam):
    """
    Apply the Box-Cox transformation with a given lambda.

    Formula:
        if lam == 0: x' = log(x)
        else:        x' = (x^lam - 1) / lam

    All values must be strictly positive.

    Returns list of transformed floats.
    """
    result = []
    for x in values:
        if x <= 0:
            raise ValueError(
                "boxcox_transform requires strictly positive values. Got: {}".format(x)
            )
        if abs(lam) < EPSILON:
            # lambda == 0 case: log transform
            result.append(math.log(x))
        else:
            result.append((x ** lam - 1.0) / lam)
    return result


def find_best_boxcox_lambda(values, lambdas):
    """
    Try each lambda in the list, compute skewness of the transformed data,
    and return the lambda that produces skewness closest to 0.

    Returns (best_lambda, list_of_skewness_values) in the same order as lambdas.
    """
    skewness_values = []
    for lam in lambdas:
        try:
            transformed = boxcox_transform(values, lam)
            skew = compute_skewness(transformed)
            skewness_values.append(skew)
        except ValueError:
            # If transform fails for this lambda, record a large skewness
            skewness_values.append(float("inf"))

    # Find the lambda index with skewness closest to 0
    best_idx = 0
    best_abs_skew = abs(skewness_values[0])
    for i in range(1, len(skewness_values)):
        if abs(skewness_values[i]) < best_abs_skew:
            best_abs_skew = abs(skewness_values[i])
            best_idx = i

    return lambdas[best_idx], skewness_values


# ===== SECTION 6: PRINTING / REPORTING =====

def print_stats_comparison(original, transformed, transform_name):
    """
    Print a side-by-side statistics table comparing original vs transformed data.
    """
    orig_mean   = compute_mean(original)
    orig_median = compute_median(original)
    orig_std    = compute_std(original)
    orig_skew   = compute_skewness(original)
    orig_min    = min(original)
    orig_max    = max(original)

    trans_mean   = compute_mean(transformed)
    trans_median = compute_median(transformed)
    trans_std    = compute_std(transformed)
    trans_skew   = compute_skewness(transformed)
    trans_min    = min(transformed)
    trans_max    = max(transformed)

    print("")
    print("  Transformation: {}".format(transform_name))
    print("  {:<12} | {:<14} | {:<14}".format("Statistic", "Original", "Transformed"))
    print("  " + "-" * 46)
    print("  {:<12} | {:<14,.2f} | {:<14,.4f}".format("Mean",    orig_mean,   trans_mean))
    print("  {:<12} | {:<14,.2f} | {:<14,.4f}".format("Median",  orig_median, trans_median))
    print("  {:<12} | {:<14,.2f} | {:<14,.4f}".format("Std Dev", orig_std,    trans_std))
    print("  {:<12} | {:<14,.4f} | {:<14,.4f}".format("Skewness",orig_skew,   trans_skew))
    print("  {:<12} | {:<14,.2f} | {:<14,.4f}".format("Min",     orig_min,    trans_min))
    print("  {:<12} | {:<14,.2f} | {:<14,.4f}".format("Max",     orig_max,    trans_max))

    skew_desc_orig  = describe_skewness(orig_skew)
    skew_desc_trans = describe_skewness(trans_skew)
    print("  Skewness shape: {} --> {}".format(skew_desc_orig, skew_desc_trans))


def print_ascii_histogram(values, n_bins=8, width=40, label=""):
    """
    Print a simple ASCII histogram to visualize the distribution shape.
    Each row represents one bin; bar width is proportional to count.
    """
    if not values:
        print("  (no data)")
        return

    min_val = min(values)
    max_val = max(values)

    if min_val == max_val:
        print("  (all values identical -- no histogram)")
        return

    bin_width = (max_val - min_val) / n_bins

    # Count values in each bin
    counts = [0] * n_bins
    for v in values:
        # Find which bin this value belongs to
        idx = int((v - min_val) / bin_width)
        # Clamp the last value into the last bin
        if idx >= n_bins:
            idx = n_bins - 1
        counts[idx] += 1

    max_count = max(counts)
    if max_count == 0:
        print("  (empty histogram)")
        return

    if label:
        print("  {}".format(label))

    for i in range(n_bins):
        # Compute the left edge of this bin
        left_edge = min_val + i * bin_width
        right_edge = left_edge + bin_width
        # Scale bar length to available width
        bar_len = int((counts[i] / max_count) * width)
        bar = "#" * bar_len
        print("  [{:>10.2f} - {:>10.2f}] {:>3} | {}".format(
            left_edge, right_edge, counts[i], bar
        ))
    print("")


def print_boxcox_search(lambdas, skewness_values, best_lambda):
    """
    Print a table showing each lambda and the resulting skewness,
    with an arrow marking the best (closest to 0) lambda.
    """
    print("")
    print("  Box-Cox Lambda Search Results:")
    print("  {:<10} | {:<14} | {}".format("Lambda", "Skewness", "Note"))
    print("  " + "-" * 45)
    for i in range(len(lambdas)):
        lam = lambdas[i]
        skew = skewness_values[i]
        note = ""
        if abs(lam) < EPSILON:
            note = "(log transform)"
        elif abs(lam - 0.5) < EPSILON:
            note = "(sqrt transform)"
        elif abs(lam - 1.0) < EPSILON:
            note = "(no transform)"
        elif abs(lam - (-1.0)) < EPSILON:
            note = "(reciprocal)"
        elif abs(lam - 2.0) < EPSILON:
            note = "(square)"

        marker = " <-- BEST" if abs(lam - best_lambda) < EPSILON else ""
        if skew == float("inf"):
            print("  {:<10.2f} | {:<14} | {}{}".format(lam, "N/A", note, marker))
        else:
            print("  {:<10.2f} | {:<14.4f} | {}{}".format(lam, skew, note, marker))
    print("")


# ===== SECTION 7: FILE I/O =====

def load_csv(filepath):
    """
    Load a CSV file and return a list of dicts (one per row).
    Uses csv.DictReader; values remain as strings -- caller converts types.
    """
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


# ===== SECTION 8: MAIN =====

def main():
    print("=" * 60)
    print("        === Data Transformation Demo ===")
    print("  Chapter 4 -- Data Quality and Preprocessing")
    print("=" * 60)

    # ----------------------------------------------------------
    # SALARY DEMO  (right-skewed data)
    # ----------------------------------------------------------
    print("\n" + "=" * 60)
    print("  PART 1: SALARY DATA (Right-Skewed Distribution)")
    print("=" * 60)

    # Extract salary values as a plain list of floats
    salaries = []
    for record in DEMO_SALARIES:
        salaries.append(float(record["Salary"]))

    # Step 1: Original salary stats and histogram
    print("\n--- Step 1: Original Salary Distribution ---")
    print("  n = {}  |  Values range from {:,} to {:,}".format(
        len(salaries), int(min(salaries)), int(max(salaries))
    ))
    print("\n  Why this is right-skewed:")
    print("  Most employees earn modest salaries, but a few executives")
    print("  earn dramatically more -- creating a long right tail.")

    orig_mean   = compute_mean(salaries)
    orig_median = compute_median(salaries)
    orig_skew   = compute_skewness(salaries)
    print("\n  Mean:   {:>12,.2f}  (pulled up by high earners)".format(orig_mean))
    print("  Median: {:>12,.2f}  (more representative of typical salary)".format(orig_median))
    print("  Skewness: {:.4f}  -- {}".format(orig_skew, describe_skewness(orig_skew)))

    print_ascii_histogram(salaries, n_bins=8, width=40, label="\n  Original Salary Distribution:")

    # Step 2: Log transform
    print("\n--- Step 2: Log Transformation ---")
    print("  Formula: x' = log(x)")
    print("  Why: compresses the long right tail; large values are pulled in")
    print("       more than small values because log grows slowly.")

    log_salaries = log_transform(salaries, base="natural", shift=0)
    print_stats_comparison(salaries, log_salaries, "Log (natural)")
    print_ascii_histogram(log_salaries, n_bins=8, width=40, label="\n  Log-Transformed Salary Distribution:")

    # Step 3: Square root transform
    print("\n--- Step 3: Square Root Transformation ---")
    print("  Formula: x' = sqrt(x)")
    print("  Why: milder compression than log; still helps with right skew.")
    print("       Useful when log overcorrects.")

    sqrt_salaries = sqrt_transform(salaries, shift=0)
    print_stats_comparison(salaries, sqrt_salaries, "Square Root")
    print_ascii_histogram(sqrt_salaries, n_bins=8, width=40, label="\n  Sqrt-Transformed Salary Distribution:")

    # Step 4: Box-Cox search
    print("\n--- Step 4: Box-Cox Lambda Search ---")
    print("  The Box-Cox family generalizes log and sqrt transforms.")
    print("  We search for the lambda that makes the data most symmetric.")
    print("  Formula:  x' = (x^lambda - 1) / lambda   when lambda != 0")
    print("            x' = log(x)                    when lambda == 0")

    best_lambda, skewness_vals = find_best_boxcox_lambda(salaries, BOXCOX_LAMBDAS)
    print_boxcox_search(BOXCOX_LAMBDAS, skewness_vals, best_lambda)

    best_boxcox = boxcox_transform(salaries, best_lambda)
    print_stats_comparison(salaries, best_boxcox, "Box-Cox (lambda={:.1f})".format(best_lambda))

    # Step 5: Compare all transforms
    print("\n--- Step 5: Skewness Reduction Summary ---")
    print("  Which transformation reduced skewness the most?")
    print("")

    original_skew = compute_skewness(salaries)
    log_skew      = compute_skewness(log_salaries)
    sqrt_skew     = compute_skewness(sqrt_salaries)
    boxcox_skew   = compute_skewness(best_boxcox)

    transforms_compared = [
        ("Original",                   original_skew),
        ("Log (natural)",              log_skew),
        ("Square Root",                sqrt_skew),
        ("Box-Cox (lam={:.1f})".format(best_lambda), boxcox_skew),
    ]

    print("  {:<30} | {:<10} | {}".format("Transform", "Skewness", "Shape"))
    print("  " + "-" * 60)
    for name, skew in transforms_compared:
        print("  {:<30} | {:<10.4f} | {}".format(name, skew, describe_skewness(skew)))

    # Find best by absolute skewness (closest to 0, excluding original)
    best_name = transforms_compared[1][0]
    best_skew_abs = abs(transforms_compared[1][1])
    for name, skew in transforms_compared[2:]:
        if abs(skew) < best_skew_abs:
            best_skew_abs = abs(skew)
            best_name = name
    print("\n  --> Best transform: {}  (skewness closest to 0)".format(best_name))

    # ----------------------------------------------------------
    # DEVIATION DEMO  (signed data, absolute value)
    # ----------------------------------------------------------
    print("\n" + "=" * 60)
    print("  PART 2: TEMPERATURE DEVIATIONS (Signed Data)")
    print("=" * 60)

    print("\n--- Step 1: Original Temperature Deviations ---")
    print("  Values: {}".format(DEMO_DEVIATIONS))
    print("\n  These are deviations from a baseline (positive = warmer,")
    print("  negative = cooler). If we only care about the magnitude")
    print("  of the swing -- not direction -- we use absolute value.")

    dev_mean   = compute_mean(DEMO_DEVIATIONS)
    dev_median = compute_median(DEMO_DEVIATIONS)
    dev_skew   = compute_skewness(DEMO_DEVIATIONS)
    print("\n  Mean:     {:>8.2f}".format(dev_mean))
    print("  Median:   {:>8.2f}".format(dev_median))
    print("  Skewness: {:>8.4f}  -- {}".format(dev_skew, describe_skewness(dev_skew)))

    print_ascii_histogram(
        [float(v) for v in DEMO_DEVIATIONS],
        n_bins=6, width=30,
        label="\n  Original Deviations Distribution:"
    )

    print("\n--- Step 2: Absolute Value Transformation ---")
    print("  Formula: x' = |x|")
    print("  Why: eliminates sign; only magnitude is preserved.")
    print("       Useful for 'how extreme was this reading?' questions.")

    abs_deviations = abs_transform(DEMO_DEVIATIONS)
    print("\n  Original: {}".format(DEMO_DEVIATIONS))
    print("  Absolute: {}".format([int(v) for v in abs_deviations]))

    print_stats_comparison(
        [float(v) for v in DEMO_DEVIATIONS],
        abs_deviations,
        "Absolute Value"
    )
    print_ascii_histogram(
        abs_deviations, n_bins=6, width=30,
        label="\n  Absolute Deviation Distribution:"
    )

    # ----------------------------------------------------------
    # GUIDANCE: When to use each transform
    # ----------------------------------------------------------
    print("\n" + "=" * 60)
    print("  WHEN TO USE EACH TRANSFORMATION")
    print("=" * 60)
    print("""
  Log transform  (x' = log(x))
    - Best for: strongly right-skewed data (income, population, prices)
    - Requirement: all values must be strictly positive
    - Use log(x+1) if data contains zeros
    - Interpretation: differences on log scale = ratios on original scale

  Square root  (x' = sqrt(x))
    - Best for: mildly right-skewed data, count data (Poisson-like)
    - Milder than log; good when log overcorrects
    - Requirement: all values must be non-negative (use sqrt(x+shift) if needed)

  Absolute value  (x' = |x|)
    - Best for: signed data where direction is irrelevant
    - Use case: deviations, errors, distances, residuals
    - Caveat: loses directional information permanently

  Box-Cox  (parametric family)
    - Best for: when you want data-driven choice of transformation strength
    - lambda=0 -> log,  lambda=0.5 -> sqrt,  lambda=1 -> none,  lambda=-1 -> reciprocal
    - Automatically finds the lambda that best normalizes the data
    - Requirement: all values must be strictly positive

  When NOT to transform:
    - When the original scale has direct interpretability (e.g., reporting
      average salary to stakeholders -- back-transform your results)
    - When the skewness is mild (|skew| < 0.5) and the algorithm is robust
    - When your model explicitly handles non-normality (e.g., tree-based models)
    - When zeros or negatives make log/Box-Cox inapplicable without shifting
""")

    print("=" * 60)
    print("  Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
