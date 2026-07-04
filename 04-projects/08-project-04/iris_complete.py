"""
Project 04: The Iris Complete Walkthrough
Chapter 8 - Final Projects (Capstone)
Data Analytics Course

Applies EVERY technique from Chapters 1-7 to the classic Iris dataset
in one end-to-end analysis pipeline.

Phases:
  1  (Ch1)  Dataset profiling & attribute types
  2  (Ch2)  Univariate descriptive statistics
  3  (Ch3)  Multivariate statistics & ASCII scatter
  4  (Ch4)  Preprocessing: missing values & normalisation
  5  (Ch5)  Clustering: K-means + SSE elbow
  6  (Ch6)  Frequent pattern mining: Apriori + association rules
  7  (Ch7)  Classification: Naive Bayes + k-NN + evaluation

Pure Python standard library only.  No external packages required.
Run with:  python iris_complete.py
"""

# ===== SECTION 1: IMPORTS =====

import csv
import math
import collections
import random


# ===== SECTION 2: CONSTANTS =====

IRIS_COLS = ["SepalLength", "SepalWidth", "PetalLength", "PetalWidth"]
SPECIES_LIST = ["setosa", "versicolor", "virginica"]
MISSING_MARKERS = {"?", "NA", "N/A", "nan", ""}

# Short column aliases used in correlation matrix header
COL_ALIASES = {"SepalLength": "SL", "SepalWidth": "SW",
               "PetalLength": "PL", "PetalWidth": "PW"}


# ===== SECTION 3: DEMO DATASET =====

# 30-row representative sample: 10 per species (hardcoded)
# Format: [SepalLength, SepalWidth, PetalLength, PetalWidth, Species]

IRIS_RAW = [
    # --- setosa (10 rows) ---
    [5.1, 3.5, 1.4, 0.2, "setosa"],
    [4.9, 3.0, 1.4, 0.2, "setosa"],
    [4.7, 3.2, 1.3, 0.2, "setosa"],
    [4.6, 3.1, 1.5, 0.2, "setosa"],
    [5.0, 3.6, 1.4, 0.2, "setosa"],
    [5.4, 3.9, 1.7, 0.4, "setosa"],
    [4.6, 3.4, 1.4, 0.3, "setosa"],
    [5.0, 3.4, 1.5, 0.2, "setosa"],
    [4.4, 2.9, 1.4, 0.2, "setosa"],
    [4.9, 3.1, 1.5, 0.1, "setosa"],
    # --- versicolor (10 rows) ---
    [7.0, 3.2, 4.7, 1.4, "versicolor"],
    [6.4, 3.2, 4.5, 1.5, "versicolor"],
    [6.9, 3.1, 4.9, 1.5, "versicolor"],
    [5.5, 2.3, 4.0, 1.3, "versicolor"],
    [6.5, 2.8, 4.6, 1.5, "versicolor"],
    [5.7, 2.8, 4.5, 1.3, "versicolor"],
    [6.3, 3.3, 4.7, 1.6, "versicolor"],
    [4.9, 2.4, 3.3, 1.0, "versicolor"],
    [6.6, 2.9, 4.6, 1.3, "versicolor"],
    [5.2, 2.7, 3.9, 1.4, "versicolor"],
    # --- virginica (10 rows) ---
    [6.3, 3.3, 6.0, 2.5, "virginica"],
    [5.8, 2.7, 5.1, 1.9, "virginica"],
    [7.1, 3.0, 5.9, 2.1, "virginica"],
    [6.3, 2.9, 5.6, 1.8, "virginica"],
    [6.5, 3.0, 5.8, 2.2, "virginica"],
    [7.6, 3.0, 6.6, 2.1, "virginica"],
    [4.9, 2.5, 4.5, 1.7, "virginica"],
    [7.3, 2.9, 6.3, 1.8, "virginica"],
    [6.7, 2.5, 5.8, 1.8, "virginica"],
    [7.2, 3.6, 6.1, 2.5, "virginica"],
]

# Build list-of-dicts
IRIS_DATA = []
for _row in IRIS_RAW:
    IRIS_DATA.append({
        "SepalLength": _row[0],
        "SepalWidth":  _row[1],
        "PetalLength": _row[2],
        "PetalWidth":  _row[3],
        "Species":     _row[4],
    })


# ===== SECTION 4: HELPER FUNCTIONS =====

# ---- basic math helpers ----

def mean_of(values):
    """Return arithmetic mean of a list of numbers."""
    if len(values) == 0:
        return 0.0
    total = 0.0
    for v in values:
        total = total + v
    return total / len(values)


def median_of(values):
    """Return median of a list of numbers."""
    if len(values) == 0:
        return 0.0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 1:
        return float(sorted_vals[mid])
    return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0


def std_dev_of(values):
    """Return population standard deviation."""
    if len(values) < 2:
        return 0.0
    m = mean_of(values)
    total = 0.0
    for v in values:
        total = total + (v - m) ** 2
    return math.sqrt(total / len(values))


def quartiles_of(values):
    """Return (Q1, Q3) using the median-split method."""
    if len(values) == 0:
        return 0.0, 0.0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 1:
        lower_half = sorted_vals[:mid]
        upper_half = sorted_vals[mid + 1:]
    else:
        lower_half = sorted_vals[:mid]
        upper_half = sorted_vals[mid:]
    q1 = median_of(lower_half)
    q3 = median_of(upper_half)
    return q1, q3


def pearson_corr(x_vals, y_vals):
    """Return Pearson correlation coefficient between two numeric lists."""
    n = len(x_vals)
    if n < 2:
        return 0.0
    mx = mean_of(x_vals)
    my = mean_of(y_vals)
    num = 0.0
    dx2 = 0.0
    dy2 = 0.0
    for i in range(n):
        dx = x_vals[i] - mx
        dy = y_vals[i] - my
        num = num + dx * dy
        dx2 = dx2 + dx * dx
        dy2 = dy2 + dy * dy
    denom = math.sqrt(dx2 * dy2)
    if denom == 0.0:
        return 0.0
    return num / denom


def euclidean_distance(a, b):
    """Euclidean distance between two numeric lists."""
    total = 0.0
    for i in range(len(a)):
        total = total + (a[i] - b[i]) ** 2
    return math.sqrt(total)


# ---- normalisation helper ----

def minmax_normalize(col_values):
    """
    Min-max normalise a list of numeric values to [0, 1].
    Returns (normalised_list, min_val, max_val).
    """
    min_v = min(col_values)
    max_v = max(col_values)
    span = max_v - min_v
    normed = []
    for v in col_values:
        if span == 0.0:
            normed.append(0.0)
        else:
            normed.append((v - min_v) / span)
    return normed, min_v, max_v


# ---- data extraction helpers ----

def get_col(data, col_name):
    """Extract a column (list) from a list-of-dicts dataset."""
    result = []
    for row in data:
        result.append(row[col_name])
    return result


def get_numeric_col(data, col_name):
    """Extract a numeric column, skipping non-numeric entries."""
    result = []
    for row in data:
        v = row[col_name]
        if isinstance(v, (int, float)):
            result.append(float(v))
        else:
            try:
                result.append(float(v))
            except (ValueError, TypeError):
                pass  # skip missing / non-numeric
    return result


def get_col_by_species(data, col_name, species):
    """Extract numeric column values for a specific species."""
    result = []
    for row in data:
        if row["Species"] == species:
            v = row[col_name]
            if isinstance(v, (int, float)):
                result.append(float(v))
            else:
                try:
                    result.append(float(v))
                except (ValueError, TypeError):
                    pass
    return result


# ===== SECTION 5: CORE ANALYSIS =====

# ------ Phase 1 helpers ------

def print_attribute_types(data):
    """Print scale type and discrete/continuous for each column."""
    print_separator()
    print("  Attribute type identification:")
    print()
    header = "  {:<16} {:<12} {}".format("Attribute", "Scale", "Discrete/Continuous")
    print(header)
    print("  " + "-" * 46)
    numeric_cols = [("SepalLength", "Ratio", "Continuous"),
                    ("SepalWidth",  "Ratio", "Continuous"),
                    ("PetalLength", "Ratio", "Continuous"),
                    ("PetalWidth",  "Ratio", "Continuous"),
                    ("Species",     "Nominal", "Discrete")]
    for attr, scale, disc in numeric_cols:
        print("  {:<16} {:<12} {}".format(attr, scale, disc))


def print_dataset_summary(data):
    """Print n objects, n attributes, class distribution."""
    print()
    print("  Dataset summary:")
    print("    Total objects    : {}".format(len(data)))
    print("    Numeric attributes: {}".format(len(IRIS_COLS)))
    print("    Class attribute  : Species (Nominal)")
    print()
    print("  Class distribution:")
    counts = collections.Counter()
    for row in data:
        counts[row["Species"]] = counts[row["Species"]] + 1
    total = len(data)
    for sp in SPECIES_LIST:
        cnt = counts[sp]
        pct = cnt / total * 100.0
        print("    {:12s}  {:3d} rows  ({:.1f}%)".format(sp, cnt, pct))


# ------ Phase 2 helpers ------

def compute_univariate_stats(values):
    """
    Return dict of statistics for a numeric list.
    Keys: min, max, mean, median, q1, q3, iqr, std, skew_sign
    """
    sorted_vals = sorted(values)
    mn   = sorted_vals[0]
    mx   = sorted_vals[-1]
    avg  = mean_of(values)
    med  = median_of(values)
    q1, q3 = quartiles_of(values)
    iqr  = q3 - q1
    std  = std_dev_of(values)
    # Pearson skewness approximation: (mean - median)
    skew_sign = "right-skewed" if avg > med else ("left-skewed" if avg < med else "symmetric")
    return {
        "min": mn, "max": mx, "mean": avg, "median": med,
        "q1": q1, "q3": q3, "iqr": iqr, "std": std,
        "skew_sign": skew_sign
    }


def print_univariate_stats(data):
    """Print per-column univariate statistics table."""
    print_separator()
    for col in IRIS_COLS:
        vals = get_numeric_col(data, col)
        s = compute_univariate_stats(vals)
        print("  {}:".format(col))
        print("    min={:.3f}  max={:.3f}  mean={:.3f}  median={:.3f}".format(
            s["min"], s["max"], s["mean"], s["median"]))
        print("    Q1={:.3f}   Q3={:.3f}   IQR={:.3f}   std={:.3f}".format(
            s["q1"], s["q3"], s["iqr"], s["std"]))
        print("    Distribution: {}".format(s["skew_sign"]))
        print()
    # Species frequency table
    print("  Species frequency table:")
    print("  {:<14} {:>6}  {:>10}".format("Species", "Count", "Rel.Freq."))
    print("  " + "-" * 34)
    total = len(data)
    counts = collections.Counter()
    for row in data:
        counts[row["Species"]] = counts[row["Species"]] + 1
    for sp in SPECIES_LIST:
        cnt = counts[sp]
        print("  {:<14} {:>6}  {:>9.3f}".format(sp, cnt, cnt / total))


# ------ Phase 3 helpers ------

def compute_correlation_matrix(data):
    """Return 4x4 Pearson correlation matrix as list of lists."""
    matrix = []
    for col_i in IRIS_COLS:
        row = []
        xi = get_numeric_col(data, col_i)
        for col_j in IRIS_COLS:
            xj = get_numeric_col(data, col_j)
            row.append(pearson_corr(xi, xj))
        matrix.append(row)
    return matrix


def print_correlation_matrix(matrix):
    """Print the 4x4 correlation matrix with column aliases."""
    aliases = [COL_ALIASES[c] for c in IRIS_COLS]
    col_w = 8
    header = "  " + " " * 4
    for alias in aliases:
        header = header + alias.rjust(col_w)
    print(header)
    print("  " + "-" * (4 + col_w * len(aliases)))
    for i in range(len(IRIS_COLS)):
        row_str = "  " + aliases[i].ljust(4)
        for j in range(len(IRIS_COLS)):
            row_str = row_str + "{:.3f}".format(matrix[i][j]).rjust(col_w)
        print(row_str)


def print_location_matrix(data):
    """Print min/mean/max per attribute in a compact table."""
    print()
    print("  Location matrix (min / mean / max per attribute):")
    header = "  {:<14} {:>8} {:>8} {:>8}".format("Attribute", "min", "mean", "max")
    print(header)
    print("  " + "-" * 42)
    for col in IRIS_COLS:
        vals = get_numeric_col(data, col)
        print("  {:<14} {:>8.3f} {:>8.3f} {:>8.3f}".format(
            col, min(vals), mean_of(vals), max(vals)))


def print_ascii_scatter(data):
    """
    Print a 20-col x 10-row ASCII scatter of PetalLength vs PetalWidth.
    Uses s=setosa, v=versicolor, g=virginica.
    """
    grid_w = 20
    grid_h = 10

    pl_vals = get_numeric_col(data, "PetalLength")
    pw_vals = get_numeric_col(data, "PetalWidth")
    pl_min = min(pl_vals)
    pl_max = max(pl_vals)
    pw_min = min(pw_vals)
    pw_max = max(pw_vals)

    symbol = {"setosa": "s", "versicolor": "v", "virginica": "g"}

    # Build empty grid
    grid = []
    for r in range(grid_h):
        grid.append(["."] * grid_w)

    for row in data:
        pl = row["PetalLength"]
        pw = row["PetalWidth"]
        if not isinstance(pl, float) or not isinstance(pw, float):
            continue
        # Map to grid coordinates
        col_idx = int((pl - pl_min) / (pl_max - pl_min + 1e-9) * (grid_w - 1))
        row_idx = grid_h - 1 - int((pw - pw_min) / (pw_max - pw_min + 1e-9) * (grid_h - 1))
        col_idx = max(0, min(grid_w - 1, col_idx))
        row_idx = max(0, min(grid_h - 1, row_idx))
        sp = row["Species"]
        grid[row_idx][col_idx] = symbol.get(sp, "?")

    print()
    print("  ASCII scatter: PetalLength (x-axis) vs PetalWidth (y-axis)")
    print("  s=setosa  v=versicolor  g=virginica")
    print()
    print("  PW ^")
    for r in range(grid_h):
        print("     |" + "".join(grid[r]))
    x_axis = "     +" + "-" * grid_w + "> PL"
    print(x_axis)
    print("      {:.1f}{}{}  {:.1f}".format(
        pl_min, " " * (grid_w - 7), "", pl_max))


# ------ Phase 4 helpers ------

def detect_missing(data):
    """Return list of (row_index, col_name) for missing values."""
    missing = []
    for i in range(len(data)):
        for col in IRIS_COLS:
            v = data[i][col]
            if str(v).strip() in MISSING_MARKERS:
                missing.append((i, col))
            elif not isinstance(v, (int, float)):
                try:
                    float(v)
                except (ValueError, TypeError):
                    missing.append((i, col))
    return missing


def impute_with_species_mean(data, missing_list):
    """Fill each missing value with the per-species column mean."""
    # Compute per-species means (skip missing)
    species_means = {}
    for sp in SPECIES_LIST:
        species_means[sp] = {}
        for col in IRIS_COLS:
            vals = []
            for row in data:
                if row["Species"] == sp:
                    v = row[col]
                    if isinstance(v, (int, float)):
                        vals.append(float(v))
            species_means[sp][col] = mean_of(vals) if vals else 0.0

    for idx, col in missing_list:
        sp = data[idx]["Species"]
        data[idx][col] = species_means[sp][col]
        print("    Imputed row {:2d} '{}' ({}) with species mean: {:.3f}".format(
            idx, col, sp, species_means[sp][col]))


def normalize_dataset(data):
    """
    Min-max normalise all 4 numeric columns in-place.
    Returns the normalised data (same list, modified in place).
    """
    for col in IRIS_COLS:
        vals = get_numeric_col(data, col)
        mn = min(vals)
        mx = max(vals)
        span = mx - mn
        for row in data:
            v = row[col]
            if span == 0.0:
                row[col] = 0.0
            else:
                row[col] = (float(v) - mn) / span
    return data


# ------ Phase 5 helpers (K-means) ------

def kmeans(data, k, col_names, n_iter=100):
    """
    Run K-means clustering.

    Parameters
    ----------
    data      : list of dicts
    k         : number of clusters
    col_names : list of column names to use as features
    n_iter    : maximum iterations

    Returns
    -------
    labels    : list of cluster indices (0..k-1) for each row
    centroids : list of k centroid vectors
    sse       : total sum of squared errors
    """
    n = len(data)
    # Initialise centroids by picking k evenly-spaced rows
    step = max(1, n // k)
    centroids = []
    for i in range(k):
        idx = i * step
        c = []
        for col in col_names:
            c.append(float(data[idx][col]))
        centroids.append(c)

    labels = [0] * n

    for iteration in range(n_iter):
        # Assignment step
        new_labels = []
        for row in data:
            point = [float(row[col]) for col in col_names]
            best_k = 0
            best_d = float("inf")
            for ki in range(k):
                d = euclidean_distance(point, centroids[ki])
                if d < best_d:
                    best_d = d
                    best_k = ki
            new_labels.append(best_k)

        if new_labels == labels:
            break
        labels = new_labels

        # Update step
        for ki in range(k):
            cluster_points = []
            for i in range(n):
                if labels[i] == ki:
                    point = [float(data[i][col]) for col in col_names]
                    cluster_points.append(point)
            if len(cluster_points) == 0:
                continue
            new_c = []
            for d in range(len(col_names)):
                coord_vals = []
                for pt in cluster_points:
                    coord_vals.append(pt[d])
                new_c.append(mean_of(coord_vals))
            centroids[ki] = new_c

    # Compute SSE
    sse = 0.0
    for i in range(n):
        point = [float(data[i][col]) for col in col_names]
        c = centroids[labels[i]]
        for d in range(len(col_names)):
            sse = sse + (point[d] - c[d]) ** 2

    return labels, centroids, sse


def compute_purity(labels, data, k):
    """
    Compute cluster purity: for each cluster, fraction of the dominant class.
    Returns overall purity (weighted average).
    """
    cluster_species = {}
    for ki in range(k):
        cluster_species[ki] = collections.Counter()
    for i in range(len(data)):
        sp = data[i]["Species"]
        cluster_species[labels[i]][sp] = cluster_species[labels[i]][sp] + 1

    total_correct = 0
    total = len(data)
    print("  Cluster composition:")
    for ki in range(k):
        counts = cluster_species[ki]
        total_in_cluster = sum(counts.values())
        if total_in_cluster == 0:
            print("    Cluster {} : (empty)".format(ki))
            continue
        dominant = max(counts, key=lambda sp: counts[sp])
        dominant_count = counts[dominant]
        total_correct = total_correct + dominant_count
        print("    Cluster {} ({} items): dominant={}  counts={}".format(
            ki, total_in_cluster, dominant, dict(counts)))

    purity = total_correct / total if total > 0 else 0.0
    return purity


# ------ Phase 6 helpers (Apriori) ------

def discretize_petal(pl, pw):
    """
    Return (PetalLength_bin, PetalWidth_bin).
    PL: <2 -> short, 2-5 -> medium, >5 -> long
    PW: <0.5 -> narrow, 0.5-1.5 -> medium, >1.5 -> wide
    """
    if pl < 2.0:
        pl_bin = "PL_short"
    elif pl <= 5.0:
        pl_bin = "PL_medium"
    else:
        pl_bin = "PL_long"

    if pw < 0.5:
        pw_bin = "PW_narrow"
    elif pw <= 1.5:
        pw_bin = "PW_medium"
    else:
        pw_bin = "PW_wide"

    return pl_bin, pw_bin


def build_transactions(raw_data):
    """
    Build transaction list for Apriori.
    Each transaction = frozenset of {PL_bin, PW_bin, Species_label}.
    Uses IRIS_RAW (original non-normalised values) for binning.
    """
    transactions = []
    for row in raw_data:
        pl = row[2]   # PetalLength (original)
        pw = row[3]   # PetalWidth  (original)
        sp = row[4]
        pl_bin, pw_bin = discretize_petal(pl, pw)
        t = frozenset([pl_bin, pw_bin, "SP_" + sp])
        transactions.append(t)
    return transactions


def apriori(transactions, min_support):
    """
    Simple Apriori frequent-itemset miner.

    Parameters
    ----------
    transactions : list of frozensets
    min_support  : minimum absolute support count (integer)

    Returns
    -------
    all_frequent : dict mapping frozenset -> support_count
    """
    # Get all single items
    item_counts = collections.Counter()
    for t in transactions:
        for item in t:
            item_counts[frozenset([item])] = item_counts[frozenset([item])] + 1

    all_frequent = {}
    current_frequent = {}
    for itemset, count in item_counts.items():
        if count >= min_support:
            current_frequent[itemset] = count
            all_frequent[itemset] = count

    k = 1
    while len(current_frequent) > 0:
        # Generate candidates of size k+1
        current_list = list(current_frequent.keys())
        candidates = {}
        for i in range(len(current_list)):
            for j in range(i + 1, len(current_list)):
                union_set = current_list[i] | current_list[j]
                if len(union_set) == k + 1:
                    candidates[union_set] = 0

        # Count candidates
        for t in transactions:
            for candidate in candidates:
                if candidate.issubset(t):
                    candidates[candidate] = candidates[candidate] + 1

        # Filter by min_support
        next_frequent = {}
        for itemset, count in candidates.items():
            if count >= min_support:
                next_frequent[itemset] = count
                all_frequent[itemset] = count

        current_frequent = next_frequent
        k = k + 1

    return all_frequent


def generate_rules(frequent_itemsets, transactions, min_confidence):
    """
    Generate association rules from frequent itemsets.

    Returns list of (antecedent_frozenset, consequent_frozenset, support, confidence).
    """
    n = len(transactions)
    support_map = {}
    for itemset, count in frequent_itemsets.items():
        support_map[itemset] = count

    rules = []
    for itemset in frequent_itemsets:
        if len(itemset) < 2:
            continue
        items = list(itemset)
        # Generate all non-empty proper subsets as antecedents
        num_subsets = 2 ** len(items)
        for mask in range(1, num_subsets - 1):
            antecedent_items = []
            consequent_items = []
            for bit in range(len(items)):
                if mask & (1 << bit):
                    antecedent_items.append(items[bit])
                else:
                    consequent_items.append(items[bit])
            if len(consequent_items) == 0:
                continue
            ant = frozenset(antecedent_items)
            cons = frozenset(consequent_items)
            if ant not in support_map:
                continue
            ant_support = support_map[ant]
            if ant_support == 0:
                continue
            rule_support = support_map[itemset]
            confidence = rule_support / ant_support
            if confidence >= min_confidence:
                rules.append((ant, cons, rule_support, confidence))

    # Deduplicate
    seen = set()
    unique_rules = []
    for ant, cons, sup, conf in rules:
        key = (ant, cons)
        if key not in seen:
            seen.add(key)
            unique_rules.append((ant, cons, sup, conf))

    return unique_rules


# ------ Phase 7 helpers (Classification) ------

def gaussian_prob(x, mean, std):
    """Gaussian probability density P(x | mean, std)."""
    if std == 0.0:
        return 1.0 if x == mean else 0.0
    exponent = -((x - mean) ** 2) / (2 * std ** 2)
    return (1.0 / (math.sqrt(2 * math.pi) * std)) * math.exp(exponent)


def train_naive_bayes(train_data, col_names, class_col="Species"):
    """
    Train Gaussian Naive Bayes.

    Returns model dict: {class_label: {col: (mean, std), '_prior': p}}
    """
    model = {}
    total = len(train_data)
    class_counts = collections.Counter()
    for row in train_data:
        class_counts[row[class_col]] = class_counts[row[class_col]] + 1

    for cls in class_counts:
        class_rows = [row for row in train_data if row[class_col] == cls]
        model[cls] = {}
        model[cls]["_prior"] = len(class_rows) / total
        for col in col_names:
            vals = []
            for row in class_rows:
                vals.append(float(row[col]))
            model[cls][col] = (mean_of(vals), std_dev_of(vals))

    return model


def predict_naive_bayes(model, row, col_names):
    """Return predicted class label for one row using Naive Bayes."""
    best_cls = None
    best_score = float("-inf")
    for cls in model:
        log_prob = math.log(model[cls]["_prior"])
        for col in col_names:
            mean_v, std_v = model[cls][col]
            p = gaussian_prob(float(row[col]), mean_v, std_v)
            if p > 0:
                log_prob = log_prob + math.log(p)
            else:
                log_prob = log_prob + math.log(1e-10)
        if log_prob > best_score:
            best_score = log_prob
            best_cls = cls
    return best_cls


def knn_predict(train_data, test_row, col_names, k, class_col="Species"):
    """Return k-NN prediction for one test row."""
    distances = []
    for train_row in train_data:
        point_train = [float(train_row[col]) for col in col_names]
        point_test  = [float(test_row[col])  for col in col_names]
        d = euclidean_distance(point_train, point_test)
        distances.append((d, train_row[class_col]))
    distances.sort(key=lambda pair: pair[0])
    neighbors = distances[:k]
    vote_counts = collections.Counter()
    for _, label in neighbors:
        vote_counts[label] = vote_counts[label] + 1
    return vote_counts.most_common(1)[0][0]


def build_confusion_matrix(true_labels, pred_labels, classes):
    """
    Build confusion matrix as dict of dicts.
    confusion[true][pred] = count
    """
    confusion = {}
    for cls in classes:
        confusion[cls] = {}
        for cls2 in classes:
            confusion[cls][cls2] = 0
    for true, pred in zip(true_labels, pred_labels):
        confusion[true][pred] = confusion[true][pred] + 1
    return confusion


def compute_metrics(confusion, classes):
    """
    Compute per-class and macro-averaged precision, recall, F1, accuracy.
    Returns dict with 'accuracy', 'macro_precision', 'macro_recall', 'macro_f1'.
    """
    total = 0
    correct = 0
    precisions = []
    recalls = []
    f1s = []

    for cls in classes:
        tp = confusion[cls][cls]
        fp = sum(confusion[other][cls] for other in classes if other != cls)
        fn = sum(confusion[cls][other] for other in classes if other != cls)
        tn = sum(confusion[r][c] for r in classes for c in classes
                 if r != cls and c != cls)
        total = total + tp + fp + fn + tn
        correct = correct + tp

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec  = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1   = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        precisions.append(prec)
        recalls.append(rec)
        f1s.append(f1)

    n_classes = len(classes)
    accuracy = correct / len(list(confusion.values())[0]) / len(classes) if len(classes) > 0 else 0.0

    # Recompute accuracy correctly
    all_true = 0
    all_total = 0
    for cls in classes:
        for cls2 in classes:
            cnt = confusion[cls][cls2]
            all_total = all_total + cnt
            if cls == cls2:
                all_true = all_true + cnt
    accuracy = all_true / all_total if all_total > 0 else 0.0

    return {
        "accuracy":        accuracy,
        "macro_precision": mean_of(precisions),
        "macro_recall":    mean_of(recalls),
        "macro_f1":        mean_of(f1s),
    }


# ===== SECTION 6: PRINTING / REPORTING =====

def print_separator(char="=", width=60):
    """Print a separator line."""
    print(char * width)


def print_phase_header(phase_num, chapter, description):
    """Print a phase header banner."""
    print()
    print_separator()
    print("=== PHASE {} (Ch{}): {} ===".format(phase_num, chapter, description))
    print_separator()


def print_table(headers, rows, col_widths=None):
    """
    Print a simple ASCII table.

    Parameters
    ----------
    headers    : list of str
    rows       : list of lists
    col_widths : list of int (optional)
    """
    if col_widths is None:
        col_widths = []
        for h in headers:
            col_widths.append(max(12, len(str(h)) + 2))

    # Header
    header_str = "  "
    for i in range(len(headers)):
        header_str = header_str + str(headers[i]).ljust(col_widths[i])
    print(header_str)
    print("  " + "-" * sum(col_widths))

    # Rows
    for row in rows:
        row_str = "  "
        for i in range(len(row)):
            cell = str(row[i])
            if i < len(col_widths):
                row_str = row_str + cell.ljust(col_widths[i])
            else:
                row_str = row_str + cell.ljust(12)
        print(row_str)


def print_confusion_matrix(confusion, classes, classifier_name):
    """Print a confusion matrix in ASCII table format."""
    print()
    print("  Confusion matrix ({}):".format(classifier_name))
    col_w = 14
    header = "  " + " " * 14
    for cls in classes:
        header = header + ("pred_" + cls[:5]).ljust(col_w)
    print(header)
    print("  " + "-" * (14 + col_w * len(classes)))
    for true_cls in classes:
        row_str = "  " + ("true_" + true_cls[:5]).ljust(14)
        for pred_cls in classes:
            row_str = row_str + str(confusion[true_cls][pred_cls]).ljust(col_w)
        print(row_str)


# ===== SECTION 7: FILE I/O =====

def load_csv(csv_file):
    """
    Load a CSV file and return (columns_dict, n_rows).

    columns_dict : dict mapping column name -> list of string values
    n_rows       : integer number of data rows
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


# ===== SECTION 8: MAIN =====

def main():
    """
    Execute all 7 analysis phases on the Iris dataset in order.
    """

    # We work on a working copy so we can inject missing values in Phase 4
    # without corrupting the original IRIS_DATA.
    import copy
    working_data = copy.deepcopy(IRIS_DATA)

    # -----------------------------------------------------------------------
    # === PHASE 1 (Ch1): DATASET PROFILING ===
    # -----------------------------------------------------------------------
    print_phase_header(1, 1, "DATASET PROFILING")
    print_attribute_types(working_data)
    print_dataset_summary(working_data)

    # -----------------------------------------------------------------------
    # === PHASE 2 (Ch2): UNIVARIATE STATISTICS ===
    # -----------------------------------------------------------------------
    print_phase_header(2, 2, "UNIVARIATE STATISTICS")
    print_univariate_stats(working_data)

    # -----------------------------------------------------------------------
    # === PHASE 3 (Ch3): MULTIVARIATE STATISTICS ===
    # -----------------------------------------------------------------------
    print_phase_header(3, 3, "MULTIVARIATE STATISTICS")

    print()
    print("  Pearson Correlation Matrix (SL=SepalLength, SW=SepalWidth,")
    print("                              PL=PetalLength, PW=PetalWidth):")
    print()
    corr_matrix = compute_correlation_matrix(working_data)
    print_correlation_matrix(corr_matrix)

    print_location_matrix(working_data)

    print_ascii_scatter(working_data)

    # -----------------------------------------------------------------------
    # === PHASE 4 (Ch4): PREPROCESSING ===
    # -----------------------------------------------------------------------
    print_phase_header(4, 4, "PREPROCESSING")
    print()

    # Step 4a: inject 2 missing values
    print("  Step 4a: Injecting 2 missing values for demonstration.")
    working_data[5]["SepalWidth"]  = "?"   # row index 5
    working_data[15]["PetalLength"] = "?"  # row index 15
    print("    Set row  5 SepalWidth  = '?'")
    print("    Set row 15 PetalLength = '?'")

    # Step 4b: detect missing
    print()
    print("  Step 4b: Detecting missing values...")
    missing_list = detect_missing(working_data)
    if len(missing_list) == 0:
        print("    No missing values found.")
    else:
        for idx, col in missing_list:
            print("    Missing: row {:2d}, column '{}'  (species: {})".format(
                idx, col, working_data[idx]["Species"]))

    # Step 4c: impute
    print()
    print("  Step 4c: Imputing with per-species column mean...")
    impute_with_species_mean(working_data, missing_list)

    # Step 4d: show 3 rows before normalisation
    print()
    print("  Step 4d: Min-max normalisation (3 sample rows BEFORE):")
    sample_indices = [0, 10, 20]
    headers = ["Row", "SepalL", "SepalW", "PetalL", "PetalW", "Species"]
    before_rows = []
    for idx in sample_indices:
        row = working_data[idx]
        before_rows.append([
            idx,
            "{:.3f}".format(float(row["SepalLength"])),
            "{:.3f}".format(float(row["SepalWidth"])),
            "{:.3f}".format(float(row["PetalLength"])),
            "{:.3f}".format(float(row["PetalWidth"])),
            row["Species"],
        ])
    print_table(headers, before_rows, [6, 8, 8, 8, 8, 12])

    normalize_dataset(working_data)

    print()
    print("  Step 4d: 3 sample rows AFTER normalisation [0,1]:")
    after_rows = []
    for idx in sample_indices:
        row = working_data[idx]
        after_rows.append([
            idx,
            "{:.3f}".format(float(row["SepalLength"])),
            "{:.3f}".format(float(row["SepalWidth"])),
            "{:.3f}".format(float(row["PetalLength"])),
            "{:.3f}".format(float(row["PetalWidth"])),
            row["Species"],
        ])
    print_table(headers, after_rows, [6, 8, 8, 8, 8, 12])

    # -----------------------------------------------------------------------
    # === PHASE 5 (Ch5): CLUSTERING (K-MEANS) ===
    # -----------------------------------------------------------------------
    print_phase_header(5, 5, "CLUSTERING (K-MEANS)")
    print()

    cluster_cols = ["PetalLength", "PetalWidth"]

    # K=3 run
    print("  Running K-means with K=3 on (PetalLength, PetalWidth) [normalised]:")
    print()
    labels3, centroids3, sse3 = kmeans(working_data, k=3, col_names=cluster_cols)

    print("  Cluster assignments (first 30 rows):")
    print("  " + "-" * 50)
    for i in range(len(working_data)):
        sp = working_data[i]["Species"]
        cl = labels3[i]
        print("    Row {:2d}  species={:<12} cluster={}".format(i, sp, cl))

    print()
    purity3 = compute_purity(labels3, working_data, k=3)
    print()
    print("  Cluster purity (K=3): {:.3f}".format(purity3))

    # Mini elbow: K=2,3,4
    print()
    print("  Mini elbow analysis (SSE vs K):")
    print("  " + "-" * 30)
    for k_val in [2, 3, 4]:
        _, _, sse_k = kmeans(working_data, k=k_val, col_names=cluster_cols)
        marker = " <-- optimal" if k_val == 3 else ""
        print("    K={}: SSE = {:.4f}{}".format(k_val, sse_k, marker))

    # -----------------------------------------------------------------------
    # === PHASE 6 (Ch6): FREQUENT PATTERN MINING ===
    # -----------------------------------------------------------------------
    print_phase_header(6, 6, "FREQUENT PATTERN MINING")
    print()

    # Build transactions from original (non-normalised) IRIS_RAW
    transactions = build_transactions(IRIS_RAW)
    print("  Transactions built: {} total".format(len(transactions)))
    print("  Sample transaction (row 0):", sorted(transactions[0]))
    print()

    min_sup  = 5
    min_conf = 0.6
    print("  Running Apriori: min_support={}, min_confidence={}".format(min_sup, min_conf))

    frequent_itemsets = apriori(transactions, min_sup)

    print()
    print("  Frequent itemsets (support >= {}):".format(min_sup))
    print("  " + "-" * 50)
    sorted_itemsets = sorted(frequent_itemsets.items(), key=lambda x: (-len(x[0]), -x[1]))
    for itemset, count in sorted_itemsets:
        print("    support={:3d}  {}".format(count, sorted(itemset)))

    rules = generate_rules(frequent_itemsets, transactions, min_conf)

    print()
    print("  Association rules (confidence >= {}):".format(min_conf))
    print("  " + "-" * 60)
    rules_sorted = sorted(rules, key=lambda r: -r[3])
    for ant, cons, sup, conf in rules_sorted:
        print("    {} => {}".format(sorted(ant), sorted(cons)))
        print("       support={:3d}  confidence={:.3f}".format(sup, conf))

    # -----------------------------------------------------------------------
    # === PHASE 7 (Ch7): CLASSIFICATION + EVALUATION ===
    # -----------------------------------------------------------------------
    print_phase_header(7, 7, "CLASSIFICATION + EVALUATION")
    print()

    # Split: first 7 of each species = train (21), last 3 = test (9)
    train_data = []
    test_data  = []
    for sp in SPECIES_LIST:
        sp_rows = [row for row in working_data if row["Species"] == sp]
        train_data.extend(sp_rows[:7])
        test_data.extend(sp_rows[7:])

    print("  Train size: {}  Test size: {}".format(len(train_data), len(test_data)))
    print()

    feature_cols = IRIS_COLS  # all 4 normalised columns

    # ---- Naive Bayes ----
    print("  --- Naive Bayes (Gaussian) ---")
    nb_model = train_naive_bayes(train_data, feature_cols)
    nb_predictions = []
    for row in test_data:
        nb_predictions.append(predict_naive_bayes(nb_model, row, feature_cols))

    true_labels = get_col(test_data, "Species")

    print()
    print("  Naive Bayes predictions:")
    print("  {:<6} {:<14} {:<14} {}".format("Row", "TrueLabel", "Predicted", "Correct?"))
    print("  " + "-" * 48)
    for i in range(len(test_data)):
        correct = "YES" if true_labels[i] == nb_predictions[i] else "NO "
        print("  {:>4d}  {:<14} {:<14} {}".format(i, true_labels[i], nb_predictions[i], correct))

    nb_confusion = build_confusion_matrix(true_labels, nb_predictions, SPECIES_LIST)
    print_confusion_matrix(nb_confusion, SPECIES_LIST, "Naive Bayes")
    nb_metrics = compute_metrics(nb_confusion, SPECIES_LIST)

    print()
    print("  Naive Bayes metrics:")
    print("    Accuracy : {:.3f}".format(nb_metrics["accuracy"]))
    print("    Precision: {:.3f}  (macro avg)".format(nb_metrics["macro_precision"]))
    print("    Recall   : {:.3f}  (macro avg)".format(nb_metrics["macro_recall"]))
    print("    F1-score : {:.3f}  (macro avg)".format(nb_metrics["macro_f1"]))

    # ---- k-NN ----
    print()
    print("  --- k-NN (k=3) ---")
    knn_predictions = []
    for row in test_data:
        knn_predictions.append(knn_predict(train_data, row, feature_cols, k=3))

    print()
    print("  k-NN predictions:")
    print("  {:<6} {:<14} {:<14} {}".format("Row", "TrueLabel", "Predicted", "Correct?"))
    print("  " + "-" * 48)
    for i in range(len(test_data)):
        correct = "YES" if true_labels[i] == knn_predictions[i] else "NO "
        print("  {:>4d}  {:<14} {:<14} {}".format(i, true_labels[i], knn_predictions[i], correct))

    knn_confusion = build_confusion_matrix(true_labels, knn_predictions, SPECIES_LIST)
    print_confusion_matrix(knn_confusion, SPECIES_LIST, "k-NN (k=3)")
    knn_metrics = compute_metrics(knn_confusion, SPECIES_LIST)

    print()
    print("  k-NN (k=3) metrics:")
    print("    Accuracy : {:.3f}".format(knn_metrics["accuracy"]))
    print("    Precision: {:.3f}  (macro avg)".format(knn_metrics["macro_precision"]))
    print("    Recall   : {:.3f}  (macro avg)".format(knn_metrics["macro_recall"]))
    print("    F1-score : {:.3f}  (macro avg)".format(knn_metrics["macro_f1"]))

    # ---- Comparison table ----
    print()
    print("  --- Classifier Comparison ---")
    print()
    comp_headers = ["Classifier", "Accuracy", "Precision", "Recall", "F1"]
    comp_rows = [
        ["Naive Bayes",
         "{:.3f}".format(nb_metrics["accuracy"]),
         "{:.3f}".format(nb_metrics["macro_precision"]),
         "{:.3f}".format(nb_metrics["macro_recall"]),
         "{:.3f}".format(nb_metrics["macro_f1"])],
        ["k-NN (k=3)",
         "{:.3f}".format(knn_metrics["accuracy"]),
         "{:.3f}".format(knn_metrics["macro_precision"]),
         "{:.3f}".format(knn_metrics["macro_recall"]),
         "{:.3f}".format(knn_metrics["macro_f1"])],
    ]
    print_table(comp_headers, comp_rows, [16, 10, 12, 10, 10])

    # -----------------------------------------------------------------------
    print()
    print_separator()
    print("  Iris Complete Walkthrough finished.")
    print("  All 7 phases (Ch1-Ch7) executed successfully.")
    print_separator()
    print()


if __name__ == "__main__":
    main()
