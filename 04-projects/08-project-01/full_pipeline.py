# full_pipeline.py
# Project 01 — End-to-End Data Pipeline
# Chapters: Ch4 (preprocessing) + Ch2/Ch3 (stats) + Ch5 (clustering) + Ch7 (classification)

# ===== SECTION 1: IMPORTS =====
import csv
import math


# ===== SECTION 2: CONSTANTS =====
K_CLUSTERS = 2
K_MAX_ITER = 100
NUMERIC_COLS = ["Max_temp", "Weight", "Height", "Years"]
TARGET_COL = "Company"
NAME_COL = "Friend"
GENDER_COL = "Gender"
MISSING_TOKEN = "?"


# ===== SECTION 3: DEMO DATASET =====
# Raw dataset with one missing value (Eve Weight=?) and one duplicate row (Andrew repeated)
RAW_DATA = [
    {"Friend": "Andrew",   "Max_temp": 25, "Weight": 77,  "Height": 175, "Years": 10, "Gender": "M", "Company": "Good"},
    {"Friend": "Bernhard", "Max_temp": 31, "Weight": 110, "Height": 195, "Years": 12, "Gender": "M", "Company": "Good"},
    {"Friend": "Carolina", "Max_temp": 15, "Weight": 70,  "Height": 172, "Years": 2,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Dennis",   "Max_temp": 20, "Weight": 85,  "Height": 180, "Years": 16, "Gender": "M", "Company": "Good"},
    {"Friend": "Eve",      "Max_temp": 10, "Weight": "?", "Height": 168, "Years": 0,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Fred",     "Max_temp": 12, "Weight": 75,  "Height": 173, "Years": 6,  "Gender": "M", "Company": "Good"},
    {"Friend": "Gwyneth",  "Max_temp": 16, "Weight": 75,  "Height": 180, "Years": 3,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Hayden",   "Max_temp": 26, "Weight": 63,  "Height": 165, "Years": 2,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Irene",    "Max_temp": 15, "Weight": 55,  "Height": 158, "Years": 5,  "Gender": "F", "Company": "Bad"},
    {"Friend": "James",    "Max_temp": 21, "Weight": 66,  "Height": 163, "Years": 14, "Gender": "M", "Company": "Good"},
    {"Friend": "Kevin",    "Max_temp": 30, "Weight": 95,  "Height": 190, "Years": 1,  "Gender": "M", "Company": "Bad"},
    {"Friend": "Lea",      "Max_temp": 13, "Weight": 72,  "Height": 172, "Years": 11, "Gender": "F", "Company": "Good"},
    {"Friend": "Marcus",   "Max_temp": 8,  "Weight": 83,  "Height": 185, "Years": 3,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Nigel",    "Max_temp": 12, "Weight": 115, "Height": 192, "Years": 15, "Gender": "M", "Company": "Good"},
    {"Friend": "Andrew",   "Max_temp": 25, "Weight": 77,  "Height": 175, "Years": 10, "Gender": "M", "Company": "Good"},  # duplicate
]

# Two synthetic test objects for Step 7
NEW_OBJECTS = [
    {"Friend": "NewPerson1", "Max_temp": 22, "Weight": 80, "Height": 178, "Years": 9,  "Gender": "M"},
    {"Friend": "NewPerson2", "Max_temp": 11, "Weight": 60, "Height": 162, "Years": 1,  "Gender": "F"},
]


# ===== SECTION 4: HELPER FUNCTIONS =====

def compute_mean(values):
    total = 0.0
    for v in values:
        total = total + v
    return total / len(values)


def compute_median(values):
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 1:
        return float(sorted_vals[mid])
    else:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0


def compute_std(values):
    n = len(values)
    if n < 2:
        return 0.0
    m = compute_mean(values)
    total = 0.0
    for v in values:
        total = total + (v - m) ** 2
    return math.sqrt(total / (n - 1))


def compute_percentile(values, p):
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    idx = (p / 100.0) * (n - 1)
    lo = int(math.floor(idx))
    hi = int(math.ceil(idx))
    if lo == hi:
        return float(sorted_vals[lo])
    frac = idx - lo
    return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac


def euclidean_distance(a, b):
    total = 0.0
    for i in range(len(a)):
        total = total + (a[i] - b[i]) ** 2
    return math.sqrt(total)


def get_numeric_vector(row, cols):
    vec = []
    for col in cols:
        vec.append(float(row[col]))
    return vec


def pearson_r(x_vals, y_vals):
    n = len(x_vals)
    mx = compute_mean(x_vals)
    my = compute_mean(y_vals)
    num = 0.0
    sum_sq_x = 0.0
    sum_sq_y = 0.0
    for i in range(n):
        dx = x_vals[i] - mx
        dy = y_vals[i] - my
        num = num + dx * dy
        sum_sq_x = sum_sq_x + dx * dx
        sum_sq_y = sum_sq_y + dy * dy
    denom = math.sqrt(sum_sq_x * sum_sq_y)
    if denom == 0.0:
        return 0.0
    return num / denom


def min_max_normalize(values):
    mn = min(values)
    mx = max(values)
    result = []
    for v in values:
        if mx == mn:
            result.append(0.0)
        else:
            result.append((v - mn) / (mx - mn))
    return result, mn, mx


def apply_normalization(value, mn, mx):
    if mx == mn:
        return 0.0
    return (value - mn) / (mx - mn)


def gaussian_pdf(x, mean, std):
    if std == 0.0:
        if x == mean:
            return 1.0
        return 1e-9
    exponent = -0.5 * ((x - mean) / std) ** 2
    coeff = 1.0 / (std * math.sqrt(2.0 * math.pi))
    return coeff * math.exp(exponent)


# ===== SECTION 5: CORE ANALYSIS =====

def step1_quality_audit(data):
    """Ch4: Detect missing values and duplicate rows."""
    missing_log = []
    for row in data:
        for col in NUMERIC_COLS:
            val = row[col]
            if str(val) == MISSING_TOKEN or str(val).strip() == "":
                missing_log.append((row[NAME_COL], col))

    seen = []
    dup_indices = []
    for i, row in enumerate(data):
        key = (row[NAME_COL], row["Max_temp"], row["Weight"], row["Height"], row["Years"], row["Gender"])
        if key in seen:
            dup_indices.append(i)
        else:
            seen.append(key)

    return missing_log, dup_indices


def step2_clean(data, missing_log, dup_indices):
    """Ch4: Fill missing values with gender-group mean, remove duplicates."""
    cleaned = []
    for i, row in enumerate(data):
        if i not in dup_indices:
            cleaned.append(dict(row))

    # Fill missing numeric values with gender-group mean
    fill_log = []
    for miss_name, miss_col in missing_log:
        # Collect values from same gender group (excluding missing)
        target_row = None
        for row in cleaned:
            if row[NAME_COL] == miss_name:
                target_row = row
                break
        if target_row is None:
            continue
        gender = target_row[GENDER_COL]
        group_vals = []
        for row in cleaned:
            if row[NAME_COL] != miss_name and row[GENDER_COL] == gender:
                v = row[miss_col]
                if str(v) != MISSING_TOKEN and str(v).strip() != "":
                    group_vals.append(float(v))
        if len(group_vals) > 0:
            fill_val = round(compute_mean(group_vals), 1)
        else:
            # Fall back to global mean
            all_vals = []
            for row in cleaned:
                v = row[miss_col]
                if str(v) != MISSING_TOKEN and str(v).strip() != "":
                    all_vals.append(float(v))
            fill_val = round(compute_mean(all_vals), 1)
        target_row[miss_col] = fill_val
        fill_log.append((miss_name, miss_col, fill_val))

    # Convert numeric cols to float
    for row in cleaned:
        for col in NUMERIC_COLS:
            row[col] = float(row[col])

    return cleaned, fill_log


def step3_univariate_stats(data):
    """Ch2: Compute mean/median/std/Q1/Q3 for each numeric column."""
    stats = {}
    for col in NUMERIC_COLS:
        vals = []
        for row in data:
            vals.append(row[col])
        stats[col] = {
            "mean":   round(compute_mean(vals), 3),
            "median": round(compute_median(vals), 3),
            "std":    round(compute_std(vals), 3),
            "q1":     round(compute_percentile(vals, 25), 3),
            "q3":     round(compute_percentile(vals, 75), 3),
        }
    return stats


def step4_correlation_matrix(data):
    """Ch3: Pearson correlation matrix for numeric columns."""
    col_vals = {}
    for col in NUMERIC_COLS:
        col_vals[col] = []
        for row in data:
            col_vals[col].append(row[col])

    matrix = {}
    for c1 in NUMERIC_COLS:
        matrix[c1] = {}
        for c2 in NUMERIC_COLS:
            r = pearson_r(col_vals[c1], col_vals[c2])
            matrix[c1][c2] = round(r, 3)
    return matrix


def step5_normalize(data):
    """Ch4: Min-max normalize all numeric columns to [0,1]."""
    norm_params = {}
    for col in NUMERIC_COLS:
        vals = []
        for row in data:
            vals.append(row[col])
        mn = min(vals)
        mx = max(vals)
        norm_params[col] = (mn, mx)

    normalized = []
    for row in data:
        new_row = dict(row)
        for col in NUMERIC_COLS:
            mn, mx = norm_params[col]
            new_row[col] = apply_normalization(row[col], mn, mx)
        normalized.append(new_row)
    return normalized, norm_params


def step6_kmeans(data):
    """Ch5: K-means with K=2 on normalized numeric columns."""
    # Initialize centroids: pick first K objects
    centroids = []
    for i in range(K_CLUSTERS):
        centroids.append(get_numeric_vector(data[i], NUMERIC_COLS))

    assignments = [0] * len(data)

    for iteration in range(K_MAX_ITER):
        new_assignments = []
        for row in data:
            vec = get_numeric_vector(row, NUMERIC_COLS)
            best_k = 0
            best_dist = euclidean_distance(vec, centroids[0])
            for k in range(1, K_CLUSTERS):
                d = euclidean_distance(vec, centroids[k])
                if d < best_dist:
                    best_dist = d
                    best_k = k
            new_assignments.append(best_k)

        # Check convergence
        changed = False
        for i in range(len(assignments)):
            if assignments[i] != new_assignments[i]:
                changed = True
                break
        assignments = new_assignments

        if not changed:
            break

        # Recompute centroids
        for k in range(K_CLUSTERS):
            members = []
            for i, row in enumerate(data):
                if assignments[i] == k:
                    members.append(get_numeric_vector(row, NUMERIC_COLS))
            if len(members) > 0:
                new_centroid = []
                for dim in range(len(NUMERIC_COLS)):
                    dim_vals = []
                    for m in members:
                        dim_vals.append(m[dim])
                    new_centroid.append(compute_mean(dim_vals))
                centroids[k] = new_centroid

    clusters = {}
    for k in range(K_CLUSTERS):
        clusters[k] = []
    for i, row in enumerate(data):
        clusters[assignments[i]].append(row[NAME_COL])

    return assignments, clusters, centroids


def step7_classify(train_data, assignments, norm_params, new_objects):
    """Ch7: Majority-class classifier per cluster + Gaussian Naive Bayes for prediction."""
    # Build per-cluster class distribution
    cluster_class_counts = {}
    for k in range(K_CLUSTERS):
        cluster_class_counts[k] = {}
    for i, row in enumerate(train_data):
        k = assignments[i]
        label = row[TARGET_COL]
        if label not in cluster_class_counts[k]:
            cluster_class_counts[k][label] = 0
        cluster_class_counts[k][label] = cluster_class_counts[k][label] + 1

    # Majority class per cluster
    cluster_majority = {}
    for k in range(K_CLUSTERS):
        best_label = None
        best_count = -1
        for label, count in cluster_class_counts[k].items():
            if count > best_count:
                best_count = count
                best_label = label
        cluster_majority[k] = best_label

    # Gaussian Naive Bayes trained on full training set
    classes = []
    for row in train_data:
        if row[TARGET_COL] not in classes:
            classes.append(row[TARGET_COL])

    class_stats = {}
    for cls in classes:
        class_stats[cls] = {}
        for col in NUMERIC_COLS:
            vals = []
            for row in train_data:
                if row[TARGET_COL] == cls:
                    vals.append(row[col])
            class_stats[cls][col] = {
                "mean": compute_mean(vals),
                "std":  compute_std(vals) if compute_std(vals) > 0 else 0.01,
            }
        # Gender: M=1, F=0, count-based
        gender_counts = {"M": 0, "F": 0}
        total_cls = 0
        for row in train_data:
            if row[TARGET_COL] == cls:
                gender_counts[row[GENDER_COL]] = gender_counts.get(row[GENDER_COL], 0) + 1
                total_cls = total_cls + 1
        class_stats[cls]["Gender_M"] = (gender_counts["M"] + 1) / (total_cls + 2)  # Laplace
        class_stats[cls]["Gender_F"] = (gender_counts["F"] + 1) / (total_cls + 2)

    # Prior probabilities
    class_prior = {}
    n_total = len(train_data)
    for cls in classes:
        count = 0
        for row in train_data:
            if row[TARGET_COL] == cls:
                count = count + 1
        class_prior[cls] = count / n_total

    # Normalize new objects and predict
    predictions = []
    for obj in new_objects:
        norm_obj = {}
        for col in NUMERIC_COLS:
            mn, mx = norm_params[col]
            norm_obj[col] = apply_normalization(float(obj[col]), mn, mx)
        norm_obj[GENDER_COL] = obj[GENDER_COL]

        posteriors = {}
        for cls in classes:
            log_prob = math.log(class_prior[cls])
            for col in NUMERIC_COLS:
                p = gaussian_pdf(norm_obj[col], class_stats[cls][col]["mean"], class_stats[cls][col]["std"])
                if p > 0:
                    log_prob = log_prob + math.log(p)
                else:
                    log_prob = log_prob + math.log(1e-15)
            gender_key = "Gender_" + norm_obj[GENDER_COL]
            log_prob = log_prob + math.log(class_stats[cls][gender_key])
            posteriors[cls] = log_prob

        best_cls = None
        best_val = None
        for cls, val in posteriors.items():
            if best_val is None or val > best_val:
                best_val = val
                best_cls = cls
        predictions.append((obj["Friend"], best_cls, posteriors))

    return predictions, cluster_majority, class_stats


# ===== SECTION 6: PRINTING / REPORTING =====

def print_separator(char="-", width=60):
    print(char * width)


def print_step_header(n, title):
    print("")
    print("=" * 60)
    print("  STEP " + str(n) + ": " + title)
    print("=" * 60)


def print_step1(missing_log, dup_indices):
    print_step_header(1, "DATA QUALITY AUDIT (Ch4)")
    print("Missing values detected: " + str(len(missing_log)))
    for name, col in missing_log:
        print("  " + name + " -> " + col + ": " + MISSING_TOKEN)
    print("Duplicate rows detected: " + str(len(dup_indices)))
    for idx in dup_indices:
        print("  Row index " + str(idx) + " is a duplicate")


def print_step2(fill_log, n_before, n_after, n_dups):
    print_step_header(2, "CLEAN DATA (Ch4)")
    for name, col, val in fill_log:
        print("  Filled " + name + " " + col + " with group mean: " + str(val))
    print("  Removed " + str(n_dups) + " duplicate row(s).")
    print("  Dataset size: " + str(n_before) + " -> " + str(n_after) + " rows")


def print_step3(stats):
    print_step_header(3, "UNIVARIATE STATISTICS (Ch2)")
    header = "{:<12} {:>8} {:>8} {:>8} {:>8} {:>8}".format(
        "Column", "Mean", "Median", "Std", "Q1", "Q3"
    )
    print(header)
    print_separator("-", 60)
    for col in NUMERIC_COLS:
        s = stats[col]
        row_str = "{:<12} {:>8.3f} {:>8.3f} {:>8.3f} {:>8.3f} {:>8.3f}".format(
            col, s["mean"], s["median"], s["std"], s["q1"], s["q3"]
        )
        print(row_str)


def print_step4(matrix):
    print_step_header(4, "PEARSON CORRELATION MATRIX (Ch3)")
    # Header row
    header = "{:<12}".format("")
    for col in NUMERIC_COLS:
        header = header + " {:>10}".format(col[:10])
    print(header)
    print_separator("-", 60)
    for c1 in NUMERIC_COLS:
        row_str = "{:<12}".format(c1[:12])
        for c2 in NUMERIC_COLS:
            row_str = row_str + " {:>10.3f}".format(matrix[c1][c2])
        print(row_str)


def print_step5(norm_params):
    print_step_header(5, "NORMALIZATION (Ch4) — Min-Max to [0,1]")
    for col in NUMERIC_COLS:
        mn, mx = norm_params[col]
        print("  " + col + ": min=" + str(round(mn, 2)) + ", max=" + str(round(mx, 2)))
    print("  All numeric columns normalized.")


def print_step6(clusters, centroids):
    print_step_header(6, "K-MEANS CLUSTERING K=2 (Ch5)")
    for k in range(K_CLUSTERS):
        members = ", ".join(clusters[k])
        print("  Cluster " + str(k) + ": " + members)
    print("")
    print("  Centroids (normalized space):")
    for k in range(K_CLUSTERS):
        parts = []
        for i, col in enumerate(NUMERIC_COLS):
            parts.append(col + "=" + str(round(centroids[k][i], 3)))
        print("    Cluster " + str(k) + ": " + ", ".join(parts))


def print_step7(predictions, cluster_majority):
    print_step_header(7, "CLASSIFICATION — Naive Bayes (Ch7)")
    print("  Cluster majority labels:")
    for k in range(K_CLUSTERS):
        print("    Cluster " + str(k) + ": " + str(cluster_majority[k]))
    print("")
    print("  Naive Bayes predictions for new objects:")
    for name, pred, posteriors in predictions:
        parts = []
        for cls, val in posteriors.items():
            parts.append(cls + "=" + str(round(val, 3)))
        print("  " + name + " -> Predicted: " + pred + "  (log posteriors: " + ", ".join(parts) + ")")


def print_step8(data_before, data_after, missing_log, dup_indices, stats, assignments, predictions):
    print_step_header(8, "FINAL REPORT SUMMARY")
    print_separator("=", 60)
    print("  [Step 1] Raw rows: " + str(len(data_before)) +
          " | Missing: " + str(len(missing_log)) +
          " | Duplicates: " + str(len(dup_indices)))
    print("  [Step 2] Cleaned rows: " + str(len(data_after)))
    print("  [Step 3] Key stats:")
    for col in NUMERIC_COLS:
        s = stats[col]
        print("           " + col + ": mean=" + str(s["mean"]) + ", std=" + str(s["std"]))
    n_cluster = {}
    for k in range(K_CLUSTERS):
        n_cluster[k] = 0
    for a in assignments:
        n_cluster[a] = n_cluster[a] + 1
    print("  [Step 6] Cluster sizes: " + str(dict(n_cluster)))
    print("  [Step 7] Predictions:")
    for name, pred, _ in predictions:
        print("           " + name + " -> " + pred)
    print_separator("=", 60)


# ===== SECTION 7: FILE I/O =====

def load_csv(csv_file):
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


def save_report(filename, lines):
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


# ===== SECTION 8: MAIN =====

def main():
    print("=" * 60)
    print("  END-TO-END DATA PIPELINE")
    print("  Chapters: Ch2, Ch3, Ch4, Ch5, Ch7")
    print("=" * 60)

    # Step 1: Quality audit
    missing_log, dup_indices = step1_quality_audit(RAW_DATA)
    print_step1(missing_log, dup_indices)

    # Step 2: Clean
    cleaned_data, fill_log = step2_clean(RAW_DATA, missing_log, dup_indices)
    print_step2(fill_log, len(RAW_DATA), len(cleaned_data), len(dup_indices))

    # Step 3: Univariate stats
    stats = step3_univariate_stats(cleaned_data)
    print_step3(stats)

    # Step 4: Correlation matrix
    corr = step4_correlation_matrix(cleaned_data)
    print_step4(corr)

    # Step 5: Normalize
    norm_data, norm_params = step5_normalize(cleaned_data)
    print_step5(norm_params)

    # Step 6: K-means
    assignments, clusters, centroids = step6_kmeans(norm_data)
    print_step6(clusters, centroids)

    # Step 7: Classify
    predictions, cluster_majority, class_stats = step7_classify(
        norm_data, assignments, norm_params, NEW_OBJECTS
    )
    print_step7(predictions, cluster_majority)

    # Step 8: Final report
    print_step8(RAW_DATA, cleaned_data, missing_log, dup_indices, stats, assignments, predictions)


if __name__ == "__main__":
    main()
