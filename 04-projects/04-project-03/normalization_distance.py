"""
Chapter 04
04-03-project-03: Normalization, Distance & Sampling
======================================================
Demonstrates:
  - Min-max normalization (scale to any [new_min, new_max])
  - Z-score standardization (center at 0, scale by std dev)
  - Euclidean distance between two points
  - Distance matrix for a set of named points
  - Simple random sampling (with and without replacement)
  - Stratified sampling (sample proportionally per class)

Solves exercise questions Q4 and Q5 explicitly.
Shows the "scale problem": distances change when units change.

Concepts: Ch.4 normalization, Euclidean distance, sampling

Usage:
    python normalization_distance.py
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys    # command-line arguments for load_csv file mode
import csv    # read CSV files
import math   # sqrt for distance and std dev
import random # random sampling


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# Exercise Q4: data from Q1 (same list)
EX_Q4_DATA = [31, 38, 42, 29, 46, 23, 83, 43, 51, 55, 27, 35]

# Expected Q4 results (rounded to 3 decimal places)
EX_Q4_EXPECTED = [0.133, 0.250, 0.317, 0.100, 0.383, 0.000, 1.000,
                  0.333, 0.467, 0.533, 0.067, 0.200]

# Exercise Q5: Euclidean distance
EX_Q5_X = [1, 3, -2, 5]
EX_Q5_Y = [2, 4,  1, 6]
EX_Q5_EXPECTED = math.sqrt(12)   # = 2*sqrt(3) ~= 3.464


# ============================================================
# 3. DEMO DATASET
# ============================================================

# FRIENDS dataset with numeric attributes for normalization demo
DEMO_DATA = {
    "name":   ["Rachel", "Monica", "Joey", "Chandler", "Phoebe",
                "Ross", "Richard", "Gunther", "Janice", "Mike"],
    "age":    [26, 26, 27, 28, 28, 29, 39, 26, 30, 31],
    "weight": [54, 57, 73, 73, 52, 77, 80, 68, 61, 78],
    "height": [165, 162, 180, 178, 170, 186, 183, 175, 163, 179],
    "salary": [45000, 52000, 38000, 71000, 29000,
               83000, 95000, 22000, 41000, 67000],
    "gender": ["F", "F", "M", "M", "F", "M", "M", "M", "F", "M"],
}

# Scale problem: Bernhard/Gwyneth/James from the lecture
LECTURE_PEOPLE = {
    "Bernhard": {"age_years": 43, "salary": 72000},
    "Gwyneth":  {"age_years": 38, "salary": 55000},
    "James":    {"age_years": 42, "salary": 84000},
}


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def compute_mean(numbers):
    """
    Compute the arithmetic mean of a list of floats.

    Returns 0.0 if the list is empty.
    """
    if len(numbers) == 0:
        return 0.0
    total = 0.0
    for x in numbers:
        total = total + x
    return total / len(numbers)


def compute_std(numbers, use_population=False):
    """
    Compute the standard deviation of a list of floats.

    Parameters:
        numbers        : list of numeric values
        use_population : if True, divide by N (population std); else divide by N-1 (sample std)

    Returns:
        Standard deviation as a float. Returns 0.0 if list has < 2 values.
    """
    n = len(numbers)
    if n < 2:
        return 0.0

    mean = compute_mean(numbers)
    sq_diffs = []
    for x in numbers:
        diff = x - mean
        sq_diffs.append(diff * diff)

    variance_sum = 0.0
    for d in sq_diffs:
        variance_sum = variance_sum + d

    if use_population:
        variance = variance_sum / n
    else:
        variance = variance_sum / (n - 1)   # sample std dev

    return math.sqrt(variance)


# ============================================================
# 5. CORE FUNCTIONS
# ============================================================

def minmax_normalize(values, new_min=0.0, new_max=1.0):
    """
    Apply min-max normalization to a list of numeric values.

    Formula: v' = (v - min_A) / (max_A - min_A) * (new_max - new_min) + new_min

    Parameters:
        values  : list of numeric values
        new_min : lower bound of target range (default 0.0)
        new_max : upper bound of target range (default 1.0)

    Returns:
        A new list of normalized floats.

    Edge case: if all values are identical (max == min), returns new_min for all.
    """
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val

    normalized = []
    for v in values:
        if range_val == 0:
            # All values are the same; map everything to new_min
            normalized.append(new_min)
        else:
            v_prime = (v - min_val) / range_val * (new_max - new_min) + new_min
            normalized.append(v_prime)
    return normalized


def zscore_normalize(values):
    """
    Apply z-score standardization to a list of numeric values.

    Formula: v' = (v - mean) / std_dev

    Returns:
        A new list of standardized floats (mean ~= 0, std ~= 1).

    Uses sample standard deviation (divides by N-1).
    If std_dev == 0, returns 0.0 for all values (no variation in column).
    """
    mean_val = compute_mean(values)
    std_val  = compute_std(values)

    standardized = []
    for v in values:
        if std_val == 0:
            standardized.append(0.0)
        else:
            standardized.append((v - mean_val) / std_val)
    return standardized


def euclidean_distance(point_a, point_b):
    """
    Compute the Euclidean distance between two n-dimensional points.

    Formula: d = sqrt( sum_i (a_i - b_i)^2 )

    Parameters:
        point_a : list or tuple of numeric coordinates
        point_b : list or tuple of numeric coordinates (same length as point_a)

    Returns:
        Float: the straight-line distance between the two points.
    """
    if len(point_a) != len(point_b):
        raise ValueError("Points must have the same number of dimensions.")

    sum_of_squares = 0.0
    for i in range(len(point_a)):
        diff = point_a[i] - point_b[i]
        sum_of_squares = sum_of_squares + diff * diff

    return math.sqrt(sum_of_squares)


def distance_matrix(points_dict):
    """
    Compute the distance between every pair of named points.

    Parameters:
        points_dict : dict {name: [coord1, coord2, ...]}

    Returns:
        A dict {(name_i, name_j): distance} for all i < j pairs.

    Also prints a formatted distance table.
    """
    names = list(points_dict.keys())
    dist_dict = {}

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            name_i = names[i]
            name_j = names[j]
            d = euclidean_distance(points_dict[name_i], points_dict[name_j])
            dist_dict[(name_i, name_j)] = d

    return dist_dict


def random_sample(items, n, with_replacement=False, seed=42):
    """
    Draw a random sample of n items from a list.

    Parameters:
        items           : list of items to sample from
        n               : number of items to draw
        with_replacement: if True, items can be drawn multiple times
        seed            : random seed for reproducibility

    Returns:
        A list of n sampled items.
    """
    rng = random.Random(seed)   # local Random instance so we don't affect global state

    if with_replacement:
        sample = []
        for _ in range(n):
            sample.append(rng.choice(items))
        return sample
    else:
        if n > len(items):
            raise ValueError("Cannot sample {} items without replacement from {} items.".format(
                n, len(items)))
        # Shuffle a copy and take the first n
        shuffled = list(items)
        rng.shuffle(shuffled)
        return shuffled[:n]


def stratified_sample(columns, target_col, n_per_class, seed=42):
    """
    Sample n_per_class rows from each class in target_col.

    Parameters:
        columns      : column-oriented data dict
        target_col   : name of the column to stratify on
        n_per_class  : number of rows to sample per class
        seed         : random seed for reproducibility

    Returns:
        A list of row indices selected (sorted).

    Prints which indices were selected from each class.
    """
    rng = random.Random(seed)

    # Group row indices by class
    class_indices = {}
    class_col = columns[target_col]
    for i in range(len(class_col)):
        cls = class_col[i]
        if cls not in class_indices:
            class_indices[cls] = []
        class_indices[cls].append(i)

    selected_indices = []
    for cls in sorted(class_indices.keys()):
        indices = class_indices[cls]
        n_available = len(indices)
        n_draw = min(n_per_class, n_available)

        # Shuffle and take first n_draw
        shuffled = list(indices)
        rng.shuffle(shuffled)
        chosen = shuffled[:n_draw]
        selected_indices.extend(chosen)

        print("    Class '{}' : {} available, {} sampled -> indices {}".format(
            cls, n_available, n_draw, sorted(chosen)))

    return sorted(selected_indices)


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def separator(char="-", width=70):
    """Print a horizontal separator line."""
    print(char * width)


def print_normalization_table(original, minmax, zscore, title):
    """
    Print a side-by-side comparison of original, min-max, and z-score values.
    """
    print("\n  " + title)
    separator(".")
    print("  {:>8}  {:>10}  {:>10}".format("Original", "Min-Max", "Z-Score"))
    separator(".", 50)
    for i in range(len(original)):
        print("  {:>8.2f}  {:>10.4f}  {:>10.4f}".format(
            float(original[i]), minmax[i], zscore[i]))


def print_distance_matrix(points_dict, dist_dict, title):
    """
    Print a formatted pairwise distance table.
    """
    print("\n  " + title)
    separator(".")
    names = list(points_dict.keys())
    # Header row
    header = "  {:>12}".format("")
    for name in names:
        header = header + "  {:>10}".format(name)
    print(header)
    separator(".", 70)
    for i in range(len(names)):
        row_str = "  {:>12}".format(names[i])
        for j in range(len(names)):
            if i == j:
                row_str = row_str + "  {:>10}".format("0.000")
            else:
                key1 = (names[i], names[j])
                key2 = (names[j], names[i])
                if key1 in dist_dict:
                    d = dist_dict[key1]
                else:
                    d = dist_dict[key2]
                row_str = row_str + "  {:>10.3f}".format(d)
        print(row_str)


# ============================================================
# 7. FILE I/O FUNCTIONS
# ============================================================

def load_csv(csv_file):
    """
    Read a CSV file and return a column-oriented dictionary.

    Returns:
        columns : dict {column_name: [value1, value2, ...]}
        n_rows  : number of data rows (not counting the header)

    CSV files are row-oriented (each line = one record).
    We pivot to column-oriented because most analysis works column by column.

    Before: rows = [{"age": "25", "name": "Alice"}, {"age": "30", "name": "Bob"}]
    After:  columns = {"age": ["25", "30"], "name": ["Alice", "Bob"]}
    """
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if len(rows) == 0:
        raise ValueError("The CSV file is empty.")

    # Pivot from row-oriented to column-oriented
    columns = {}
    for col_name in rows[0]:
        columns[col_name] = []
        for row in rows:
            columns[col_name].append(row[col_name])

    return columns, len(rows)


# ============================================================
# 8. MAIN PROGRAM
# ============================================================

def run_demo():
    """
    Solve exercise Q4 and Q5, then demonstrate normalization,
    distance, and sampling on the FRIENDS dataset.
    """
    separator("=")
    print("  NORMALIZATION, DISTANCE & SAMPLING -- Chapter 4 Demo")
    separator("=")

    # --------------------------------------------------
    # Q4: Min-Max Normalization
    # --------------------------------------------------
    separator("=")
    print("  EXERCISE Q4 -- Min-Max Normalize Q1 data to [0, 1]")
    print("  Data: {}".format(EX_Q4_DATA))
    separator("=")

    q4_normalized = minmax_normalize(EX_Q4_DATA, new_min=0.0, new_max=1.0)
    min_val = min(EX_Q4_DATA)
    max_val = max(EX_Q4_DATA)
    print("\n  min={}, max={}, formula: v' = (v - {}) / {}".format(
        min_val, max_val, min_val, max_val - min_val))
    print("\n  {:>6}  {:>10}  {:>10}  {:>8}".format(
        "v", "Expected", "Computed", "Match"))
    separator(".", 50)

    all_match_q4 = True
    for i in range(len(EX_Q4_DATA)):
        computed  = round(q4_normalized[i], 3)
        expected  = EX_Q4_EXPECTED[i]
        match     = abs(computed - expected) < 0.001
        if not match:
            all_match_q4 = False
        print("  {:>6}  {:>10.3f}  {:>10.3f}  {:>8}".format(
            EX_Q4_DATA[i], expected, computed, "YES" if match else "NO"))

    print("\n  Overall match: {}".format("YES" if all_match_q4 else "NO"))

    # --------------------------------------------------
    # Q5: Euclidean Distance
    # --------------------------------------------------
    separator("=")
    print("  EXERCISE Q5 -- Euclidean Distance")
    print("  x = {}".format(EX_Q5_X))
    print("  y = {}".format(EX_Q5_Y))
    separator("=")

    q5_distance = euclidean_distance(EX_Q5_X, EX_Q5_Y)

    print("\n  Computation steps:")
    # Build differences and squares using explicit loops
    diffs = []
    squares = []
    for i in range(len(EX_Q5_X)):
        d = EX_Q5_X[i] - EX_Q5_Y[i]
        diffs.append(d)
        squares.append(d * d)
    print("  differences : {}".format(diffs))
    print("  squares     : {}".format(squares))
    print("  sum         : {}".format(sum(squares)))
    print("  sqrt        : {:.4f}".format(q5_distance))

    print("\n  Expected: {:.4f}  Computed: {:.4f}  Match: {}".format(
        EX_Q5_EXPECTED, q5_distance,
        "YES" if abs(q5_distance - EX_Q5_EXPECTED) < 0.001 else "NO"))

    # --------------------------------------------------
    # Scale Problem: Bernhard / Gwyneth / James
    # --------------------------------------------------
    separator("=")
    print("  SCALE PROBLEM DEMO -- Bernhard, Gwyneth, James")
    print("  Age in years vs. decades -> same data, different distances!")
    separator("=")

    # Build point vectors: [age_years, salary]
    names_bgj = list(LECTURE_PEOPLE.keys())
    pts_years = {}
    pts_decades = {}
    for name in names_bgj:
        age_y = LECTURE_PEOPLE[name]["age_years"]
        sal   = LECTURE_PEOPLE[name]["salary"]
        pts_years[name]   = [age_y, sal]
        pts_decades[name] = [age_y / 10.0, sal]

    print("\n  -- Distances using age in YEARS (not normalized) --")
    dm_years = distance_matrix(pts_years)
    for key in sorted(dm_years.keys()):
        print("    {} <-> {} : {:.2f}".format(key[0], key[1], dm_years[key]))

    print("\n  -- Distances using age in DECADES (same data, different unit) --")
    dm_decades = distance_matrix(pts_decades)
    for key in sorted(dm_decades.keys()):
        print("    {} <-> {} : {:.2f}".format(key[0], key[1], dm_decades[key]))

    print("\n  The salary dominates in both cases, making age irrelevant.")
    print("  Solution: normalize both attributes first.")

    # Normalize both attributes with min-max, then compute distances
    all_ages    = [LECTURE_PEOPLE[n]["age_years"] for n in names_bgj]
    all_salaries = [LECTURE_PEOPLE[n]["salary"] for n in names_bgj]

    norm_ages    = minmax_normalize(all_ages)
    norm_salaries = minmax_normalize(all_salaries)

    pts_normalized = {}
    for i in range(len(names_bgj)):
        pts_normalized[names_bgj[i]] = [norm_ages[i], norm_salaries[i]]

    print("\n  -- Distances after min-max normalization (BOTH age and salary) --")
    dm_norm = distance_matrix(pts_normalized)
    for key in sorted(dm_norm.keys()):
        print("    {} <-> {} : {:.4f}".format(key[0], key[1], dm_norm[key]))

    print("\n  Now distances reflect BOTH attributes equally.")

    # --------------------------------------------------
    # FRIENDS Dataset: Normalization Comparison
    # --------------------------------------------------
    separator("=")
    print("  FRIENDS DATASET -- Before and After Normalization")
    separator("=")

    ages     = DEMO_DATA["age"]
    salaries = DEMO_DATA["salary"]

    ages_mm   = minmax_normalize(ages)
    ages_z    = zscore_normalize(ages)
    sal_mm    = minmax_normalize(salaries)
    sal_z     = zscore_normalize(salaries)

    print_normalization_table(ages, ages_mm, ages_z, "Age column")
    print_normalization_table(salaries, sal_mm, sal_z, "Salary column")

    print("\n  After normalization both age and salary are on similar scales.")
    print("  Min-max: both in [0, 1]; Z-score: both have mean ~0, std ~1.")

    # --------------------------------------------------
    # Distance Matrix on FRIENDS (first 5 people, age + height normalized)
    # --------------------------------------------------
    separator("=")
    print("  DISTANCE MATRIX -- First 5 FRIENDS (normalized age + height)")
    separator("=")

    first5_names   = DEMO_DATA["name"][:5]
    first5_ages    = minmax_normalize(DEMO_DATA["age"][:5])
    first5_heights = minmax_normalize(DEMO_DATA["height"][:5])

    pts_friends = {}
    for i in range(5):
        pts_friends[first5_names[i]] = [first5_ages[i], first5_heights[i]]

    dm_friends = distance_matrix(pts_friends)
    print_distance_matrix(pts_friends, dm_friends, "Distance matrix (normalized age, height)")

    # --------------------------------------------------
    # Sampling Demo
    # --------------------------------------------------
    separator("=")
    print("  SAMPLING DEMO")
    separator("=")

    all_names = DEMO_DATA["name"]

    print("\n  Simple random sample, n=5, WITHOUT replacement (seed=42):")
    sample_no_rep = random_sample(all_names, n=5, with_replacement=False, seed=42)
    print("    {}".format(sample_no_rep))

    print("\n  Simple random sample, n=5, WITH replacement (seed=42):")
    sample_rep = random_sample(all_names, n=5, with_replacement=True, seed=42)
    print("    {}".format(sample_rep))
    dups = [x for x in sample_rep if sample_rep.count(x) > 1]
    if dups:
        print("    (Note: duplicates present because with_replacement=True)")

    print("\n  Stratified sample, 2 per gender class (seed=42):")
    # Convert FRIENDS data to use string values for the column dict
    friends_cols = {}
    for col in DEMO_DATA:
        friends_cols[col] = [str(v) for v in DEMO_DATA[col]]
    selected_idx = stratified_sample(friends_cols, target_col="gender", n_per_class=2, seed=42)
    print("    Selected row indices: {}".format(selected_idx))
    print("    Selected names: {}".format([DEMO_DATA["name"][i] for i in selected_idx]))
    print("    Selected genders: {}".format([DEMO_DATA["gender"][i] for i in selected_idx]))

    separator("=")
    print("  Demo complete.")
    separator("=")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_demo()
    else:
        print("Usage: python normalization_distance.py")
        print("  (no file argument; this project runs a built-in demo)")
        sys.exit(0)
