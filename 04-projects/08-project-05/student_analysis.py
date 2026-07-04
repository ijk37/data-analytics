"""
Project 05: Student Performance Predictor
Chapter 8 - Final Projects (Capstone)
Data Analytics Course

A school wants to predict which students will fail, cluster students by
performance profile, and understand what subject combinations co-occur
in weak students.

Phases:
  1  (Ch1)  Attribute type identification
  2  (Ch2)  Descriptive statistics
  3  (Ch4)  Preprocessing: outliers, discretisation, normalisation
  4  (Ch3)  Multivariate analysis: correlation matrix
  5  (Ch6)  Frequent pattern mining: Apriori on grade-label transactions
  6  (Ch5)  Clustering: K-means K=3, cluster profiling
  7  (Ch7)  Classification: k-NN + Naive Bayes + evaluation

Pure Python standard library only.  No external packages required.
Run with:  python student_analysis.py
"""

# ===== SECTION 1: IMPORTS =====

import csv
import math
import collections


# ===== SECTION 2: CONSTANTS =====

# Numeric feature columns
NUMERIC_COLS  = ["Math", "Science", "English", "History", "StudyHours", "Absences"]
SUBJECT_COLS  = ["Math", "Science", "English", "History"]
CLASS_COL     = "Result"
CLASSES       = ["Pass", "Fail"]
MISSING_MARKERS = {"?", "NA", "N/A", "nan", ""}

# Grade-label discretisation thresholds and labels (for Apriori)
# Score: <50 -> Fail_grade, 50-69 -> Satisfactory, 70-84 -> Good, >=85 -> Excellent
GRADE_BINS   = [50, 70, 85]
GRADE_LABELS = ["Fail_grade", "Satisfactory", "Good", "Excellent"]


# ===== SECTION 3: DEMO DATASET =====

# 25 students, hardcoded
# Fields: Name, Math, Science, English, History, StudyHours, Absences, Result

STUDENT_RAW = [
    ("Alice",   85, 88, 90, 82, 6, 2,  "Pass"),
    ("Bob",     42, 38, 55, 45, 2, 8,  "Fail"),
    ("Carlos",  72, 68, 75, 70, 4, 3,  "Pass"),
    ("Diana",   91, 95, 88, 93, 7, 1,  "Pass"),
    ("Ethan",   35, 40, 48, 38, 1, 12, "Fail"),
    ("Fiona",   78, 72, 80, 75, 5, 2,  "Pass"),
    ("George",  55, 48, 60, 52, 3, 7,  "Fail"),
    ("Hannah",  88, 92, 85, 90, 7, 1,  "Pass"),
    ("Ivan",    48, 45, 52, 50, 2, 9,  "Fail"),
    ("Julia",   80, 75, 82, 78, 5, 2,  "Pass"),
    ("Kevin",   38, 35, 42, 40, 1, 11, "Fail"),
    ("Laura",   92, 90, 94, 88, 8, 0,  "Pass"),
    ("Mike",    60, 65, 68, 62, 4, 5,  "Pass"),
    ("Nancy",   45, 42, 50, 48, 2, 8,  "Fail"),
    ("Oscar",   75, 70, 78, 72, 5, 3,  "Pass"),
    ("Paula",   30, 32, 38, 35, 1, 14, "Fail"),
    ("Quinn",   82, 85, 80, 88, 6, 2,  "Pass"),
    ("Rachel",  52, 50, 58, 55, 3, 6,  "Fail"),
    ("Sam",     70, 68, 72, 65, 4, 4,  "Pass"),
    ("Tina",    44, 48, 52, 46, 2, 9,  "Fail"),
    ("Uma",     86, 88, 84, 90, 6, 1,  "Pass"),
    ("Victor",  40, 38, 45, 42, 2, 10, "Fail"),
    ("Wendy",   77, 74, 80, 76, 5, 3,  "Pass"),
    ("Xavier",  58, 55, 62, 60, 3, 6,  "Pass"),
    ("Yara",    33, 30, 40, 35, 1, 13, "Fail"),
]

# Build list-of-dicts
STUDENT_DATA = []
for _r in STUDENT_RAW:
    STUDENT_DATA.append({
        "Name":       _r[0],
        "Math":       float(_r[1]),
        "Science":    float(_r[2]),
        "English":    float(_r[3]),
        "History":    float(_r[4]),
        "StudyHours": float(_r[5]),
        "Absences":   float(_r[6]),
        "Result":     _r[7],
    })


# ===== SECTION 4: HELPER FUNCTIONS =====

# ---- basic math ----

def mean_of(values):
    """Arithmetic mean of a numeric list."""
    if len(values) == 0:
        return 0.0
    return sum(values) / len(values)


def std_dev_of(values):
    """Population standard deviation."""
    if len(values) < 2:
        return 0.0
    m = mean_of(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / len(values))


def median_of(values):
    """Median of a numeric list."""
    if len(values) == 0:
        return 0.0
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return float(s[mid])
    return (s[mid - 1] + s[mid]) / 2.0


def quartiles_of(values):
    """Return (Q1, Q3) using the median-split method."""
    if len(values) == 0:
        return 0.0, 0.0
    s = sorted(values)
    n = len(s)
    mid = n // 2
    lower = s[:mid]
    upper = s[mid + 1:] if n % 2 == 1 else s[mid:]
    return median_of(lower), median_of(upper)


def pearson_corr(x_vals, y_vals):
    """Pearson correlation coefficient between two numeric lists."""
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
    """Euclidean distance between two numeric lists of equal length."""
    total = 0.0
    for i in range(len(a)):
        total = total + (a[i] - b[i]) ** 2
    return math.sqrt(total)


# ---- data extraction ----

def get_col(data, col_name):
    """Extract a column as a list from list-of-dicts."""
    result = []
    for row in data:
        result.append(row[col_name])
    return result


def get_numeric_col(data, col_name):
    """Extract a column as a list of floats, skipping non-numeric."""
    result = []
    for row in data:
        v = row[col_name]
        try:
            result.append(float(v))
        except (ValueError, TypeError):
            pass
    return result


def get_col_by_class(data, col_name, class_value):
    """Extract numeric column values for rows matching class_value."""
    result = []
    for row in data:
        if row[CLASS_COL] == class_value:
            result.append(float(row[col_name]))
    return result


# ---- discretisation ----

def discretize_score(score):
    """
    Map a 0-100 score to a grade-label string.
    <50 -> Fail_grade, 50-69 -> Satisfactory, 70-84 -> Good, >=85 -> Excellent
    """
    if score < 50:
        return "Fail_grade"
    elif score < 70:
        return "Satisfactory"
    elif score < 85:
        return "Good"
    else:
        return "Excellent"


# ---- normalisation ----

def minmax_normalize_col(values):
    """Return min-max normalised list and (min, max)."""
    mn = min(values)
    mx = max(values)
    span = mx - mn
    normed = []
    for v in values:
        normed.append((v - mn) / span if span != 0.0 else 0.0)
    return normed, mn, mx


# ===== SECTION 5: CORE ANALYSIS =====

# ------ K-means ------

def kmeans(data, k, col_names, n_iter=100):
    """
    K-means clustering.

    Returns (labels, centroids, sse).
    labels    : list of cluster index (0..k-1) per row
    centroids : list of k centroid vectors
    sse       : total within-cluster sum of squared errors
    """
    n = len(data)
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

        for ki in range(k):
            cluster_points = []
            for i in range(n):
                if labels[i] == ki:
                    cluster_points.append([float(data[i][col]) for col in col_names])
            if len(cluster_points) == 0:
                continue
            new_c = []
            for d in range(len(col_names)):
                coord_vals = []
                for pt in cluster_points:
                    coord_vals.append(pt[d])
                new_c.append(mean_of(coord_vals))
            centroids[ki] = new_c

    sse = 0.0
    for i in range(n):
        point = [float(data[i][col]) for col in col_names]
        c = centroids[labels[i]]
        for d in range(len(col_names)):
            sse = sse + (point[d] - c[d]) ** 2

    return labels, centroids, sse


# ------ Apriori ------

def apriori(transactions, min_support):
    """Simple Apriori frequent-itemset miner (absolute support count)."""
    item_counts = collections.Counter()
    for t in transactions:
        for item in t:
            key = frozenset([item])
            item_counts[key] = item_counts[key] + 1

    all_frequent = {}
    current_frequent = {}
    for itemset, count in item_counts.items():
        if count >= min_support:
            current_frequent[itemset] = count
            all_frequent[itemset] = count

    k = 1
    while len(current_frequent) > 0:
        current_list = list(current_frequent.keys())
        candidates = {}
        for i in range(len(current_list)):
            for j in range(i + 1, len(current_list)):
                union_set = current_list[i] | current_list[j]
                if len(union_set) == k + 1:
                    candidates[union_set] = 0

        for t in transactions:
            for candidate in candidates:
                if candidate.issubset(t):
                    candidates[candidate] = candidates[candidate] + 1

        next_frequent = {}
        for itemset, count in candidates.items():
            if count >= min_support:
                next_frequent[itemset] = count
                all_frequent[itemset] = count

        current_frequent = next_frequent
        k = k + 1

    return all_frequent


def generate_rules(frequent_itemsets, min_confidence):
    """
    Generate association rules from frequent itemsets.
    Returns list of (antecedent, consequent, support, confidence).
    """
    support_map = {}
    for itemset, count in frequent_itemsets.items():
        support_map[itemset] = count

    rules = []
    for itemset in frequent_itemsets:
        if len(itemset) < 2:
            continue
        items = list(itemset)
        num_subsets = 2 ** len(items)
        for mask in range(1, num_subsets - 1):
            ant_items  = []
            cons_items = []
            for bit in range(len(items)):
                if mask & (1 << bit):
                    ant_items.append(items[bit])
                else:
                    cons_items.append(items[bit])
            if len(cons_items) == 0:
                continue
            ant  = frozenset(ant_items)
            cons = frozenset(cons_items)
            if ant not in support_map:
                continue
            ant_support = support_map[ant]
            if ant_support == 0:
                continue
            confidence = support_map[itemset] / ant_support
            if confidence >= min_confidence:
                rules.append((ant, cons, support_map[itemset], confidence))

    seen = set()
    unique_rules = []
    for ant, cons, sup, conf in rules:
        key = (ant, cons)
        if key not in seen:
            seen.add(key)
            unique_rules.append((ant, cons, sup, conf))

    return unique_rules


# ------ Classification ------

def gaussian_prob(x, mean_v, std_v):
    """Gaussian PDF P(x | mean, std)."""
    if std_v == 0.0:
        return 1.0 if x == mean_v else 1e-10
    exp_val = -((x - mean_v) ** 2) / (2 * std_v ** 2)
    return (1.0 / (math.sqrt(2 * math.pi) * std_v)) * math.exp(exp_val)


def train_naive_bayes(train_data, col_names, class_col=CLASS_COL):
    """Train Gaussian Naive Bayes. Returns model dict."""
    model = {}
    total = len(train_data)
    class_counts = collections.Counter()
    for row in train_data:
        class_counts[row[class_col]] = class_counts[row[class_col]] + 1

    for cls in class_counts:
        class_rows = [row for row in train_data if row[class_col] == cls]
        model[cls] = {"_prior": len(class_rows) / total}
        for col in col_names:
            vals = [float(row[col]) for row in class_rows]
            model[cls][col] = (mean_of(vals), std_dev_of(vals))

    return model


def predict_naive_bayes(model, row, col_names):
    """Return predicted class for one row using Naive Bayes."""
    best_cls   = None
    best_score = float("-inf")
    for cls in model:
        log_prob = math.log(model[cls]["_prior"])
        for col in col_names:
            mean_v, std_v = model[cls][col]
            p = gaussian_prob(float(row[col]), mean_v, std_v)
            log_prob = log_prob + math.log(max(p, 1e-10))
        if log_prob > best_score:
            best_score = log_prob
            best_cls   = cls
    return best_cls


def knn_predict(train_data, test_row, col_names, k, class_col=CLASS_COL):
    """Return k-NN prediction for one test row."""
    distances = []
    for train_row in train_data:
        a = [float(train_row[col]) for col in col_names]
        b = [float(test_row[col])  for col in col_names]
        distances.append((euclidean_distance(a, b), train_row[class_col]))
    distances.sort(key=lambda pair: pair[0])
    vote_counts = collections.Counter()
    for _, label in distances[:k]:
        vote_counts[label] = vote_counts[label] + 1
    return vote_counts.most_common(1)[0][0]


def build_confusion_matrix(true_labels, pred_labels, classes):
    """Build confusion matrix as dict of dicts."""
    confusion = {}
    for cls in classes:
        confusion[cls] = {}
        for cls2 in classes:
            confusion[cls][cls2] = 0
    for true, pred in zip(true_labels, pred_labels):
        confusion[true][pred] = confusion[true][pred] + 1
    return confusion


def compute_accuracy(confusion, classes):
    """Compute overall accuracy from confusion matrix."""
    correct = 0
    total   = 0
    for cls in classes:
        for cls2 in classes:
            cnt = confusion[cls][cls2]
            total = total + cnt
            if cls == cls2:
                correct = correct + cnt
    return correct / total if total > 0 else 0.0


# ===== SECTION 6: PRINTING / REPORTING =====

def print_separator(char="=", width=65):
    print(char * width)


def print_phase_header(phase_num, chapter, description):
    print()
    print_separator()
    print("=== PHASE {} (Ch{}): {} ===".format(phase_num, chapter, description))
    print_separator()


def print_table(headers, rows, col_widths=None):
    """Print a simple ASCII table."""
    if col_widths is None:
        col_widths = [max(14, len(str(h)) + 2) for h in headers]
    header_str = "  " + "".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_str)
    print("  " + "-" * sum(col_widths))
    for row in rows:
        row_str = "  "
        for i in range(len(row)):
            cell = str(row[i])
            w = col_widths[i] if i < len(col_widths) else 14
            row_str = row_str + cell.ljust(w)
        print(row_str)


def print_confusion_matrix(confusion, classes, classifier_name):
    """Print confusion matrix as ASCII table."""
    print()
    print("  Confusion matrix ({}):".format(classifier_name))
    col_w = 12
    header = "  " + " " * 12
    for cls in classes:
        header = header + ("pred_" + cls).ljust(col_w)
    print(header)
    print("  " + "-" * (12 + col_w * len(classes)))
    for true_cls in classes:
        row_str = "  " + ("true_" + true_cls).ljust(12)
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
    """Run all 7 analysis phases on the Student Performance dataset."""

    import copy
    working_data = copy.deepcopy(STUDENT_DATA)

    # -----------------------------------------------------------------------
    # === PHASE 1 (Ch1): ATTRIBUTE TYPE IDENTIFICATION ===
    # -----------------------------------------------------------------------
    print_phase_header(1, 1, "ATTRIBUTE TYPE IDENTIFICATION")
    print()
    headers = ["Attribute", "Scale", "Discrete/Continuous", "Notes"]
    rows = [
        ["Math",       "Ratio",   "Continuous", "0-100 score"],
        ["Science",    "Ratio",   "Continuous", "0-100 score"],
        ["English",    "Ratio",   "Continuous", "0-100 score"],
        ["History",    "Ratio",   "Continuous", "0-100 score"],
        ["StudyHours", "Ratio",   "Continuous", "hours/week"],
        ["Absences",   "Ratio",   "Continuous", "days absent"],
        ["Result",     "Nominal", "Discrete",   "Pass or Fail"],
    ]
    print_table(headers, rows, [14, 10, 22, 16])

    # -----------------------------------------------------------------------
    # === PHASE 2 (Ch2): DESCRIPTIVE STATISTICS ===
    # -----------------------------------------------------------------------
    print_phase_header(2, 2, "DESCRIPTIVE STATISTICS")
    print()

    # Per-class means
    print("  Per-class means (Pass vs Fail):")
    print()
    comp_headers = ["Attribute", "Pass_mean", "Fail_mean", "Abs_diff"]
    comp_rows = []
    diffs = []
    for col in NUMERIC_COLS:
        pass_vals = get_col_by_class(working_data, col, "Pass")
        fail_vals = get_col_by_class(working_data, col, "Fail")
        pm = mean_of(pass_vals)
        fm = mean_of(fail_vals)
        diff = abs(pm - fm)
        diffs.append((col, diff))
        comp_rows.append([
            col,
            "{:.2f}".format(pm),
            "{:.2f}".format(fm),
            "{:.2f}".format(diff),
        ])
    print_table(comp_headers, comp_rows, [14, 12, 12, 12])

    diffs.sort(key=lambda x: -x[1])
    print()
    print("  Subject with LARGEST gap between Pass and Fail:")
    print("    {} (abs diff = {:.2f})".format(diffs[0][0], diffs[0][1]))
    print()
    print("  Top 3 most discriminating attributes:")
    for rank, (col, diff) in enumerate(diffs[:3], 1):
        print("    {}. {}  (diff = {:.2f})".format(rank, col, diff))

    # Overall stats
    print()
    print("  Overall statistics per attribute:")
    print()
    ov_headers = ["Attribute", "Mean", "Std", "Min", "Max"]
    ov_rows = []
    for col in NUMERIC_COLS:
        vals = get_numeric_col(working_data, col)
        ov_rows.append([
            col,
            "{:.2f}".format(mean_of(vals)),
            "{:.2f}".format(std_dev_of(vals)),
            "{:.1f}".format(min(vals)),
            "{:.1f}".format(max(vals)),
        ])
    print_table(ov_headers, ov_rows, [14, 10, 10, 8, 8])

    # -----------------------------------------------------------------------
    # === PHASE 3 (Ch4): PREPROCESSING ===
    # -----------------------------------------------------------------------
    print_phase_header(3, 4, "PREPROCESSING")
    print()

    # Step 3a: IQR outlier detection on Absences
    print("  Step 3a: IQR outlier detection on 'Absences'")
    absences = get_numeric_col(working_data, "Absences")
    q1, q3 = quartiles_of(absences)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    print("    Q1={:.2f}  Q3={:.2f}  IQR={:.2f}".format(q1, q3, iqr))
    print("    Lower fence: {:.2f}  Upper fence: {:.2f}".format(lower_fence, upper_fence))
    print()
    outliers_found = False
    for row in working_data:
        v = row["Absences"]
        if v < lower_fence or v > upper_fence:
            print("    OUTLIER: {} | Absences={:.0f}  ({}  {}  fences)".format(
                row["Name"], v, row["Result"],
                "below lower" if v < lower_fence else "above upper"))
            outliers_found = True
    if not outliers_found:
        print("    No outliers detected.")

    # Step 3b: Discretise subject scores
    print()
    print("  Step 3b: Grade-label discretisation (per subject)")
    print("           <50=Fail_grade  50-69=Satisfactory  70-84=Good  >=85=Excellent")
    print()
    disc_headers = ["Name"] + SUBJECT_COLS
    disc_rows = []
    for row in working_data:
        disc_row = [row["Name"]]
        for col in SUBJECT_COLS:
            disc_row.append(discretize_score(float(row[col])))
        disc_rows.append(disc_row)
    print_table(disc_headers, disc_rows, [10, 16, 16, 16, 16])

    # Step 3c: Min-max normalise numeric columns; store normed data separately
    print()
    print("  Step 3c: Min-max normalisation of numeric features to [0, 1]")
    print()

    norm_data = copy.deepcopy(working_data)
    norm_ranges = {}
    for col in NUMERIC_COLS:
        vals = get_numeric_col(norm_data, col)
        normed, mn, mx = minmax_normalize_col(vals)
        norm_ranges[col] = (mn, mx)
        for i in range(len(norm_data)):
            norm_data[i][col] = normed[i]

    print("  3 sample rows BEFORE normalisation:")
    sample_idxs = [0, 1, 2]
    samp_headers = ["Name", "Math", "Science", "StudyHours", "Absences", "Result"]
    samp_rows = []
    for idx in sample_idxs:
        r = working_data[idx]
        samp_rows.append([r["Name"], r["Math"], r["Science"],
                          r["StudyHours"], r["Absences"], r["Result"]])
    print_table(samp_headers, samp_rows, [10, 8, 10, 13, 10, 8])

    print()
    print("  3 sample rows AFTER normalisation:")
    samp_rows_normed = []
    for idx in sample_idxs:
        r = norm_data[idx]
        samp_rows_normed.append([
            r["Name"],
            "{:.3f}".format(r["Math"]),
            "{:.3f}".format(r["Science"]),
            "{:.3f}".format(r["StudyHours"]),
            "{:.3f}".format(r["Absences"]),
            r["Result"],
        ])
    print_table(samp_headers, samp_rows_normed, [10, 8, 10, 13, 10, 8])

    # -----------------------------------------------------------------------
    # === PHASE 4 (Ch3): MULTIVARIATE ANALYSIS ===
    # -----------------------------------------------------------------------
    print_phase_header(4, 3, "MULTIVARIATE ANALYSIS")
    print()

    # Build correlation matrix for 6 numeric cols on original data
    corr_cols = NUMERIC_COLS
    n_corr = len(corr_cols)
    corr_matrix = []
    col_vectors = {}
    for col in corr_cols:
        col_vectors[col] = get_numeric_col(working_data, col)

    for i in range(n_corr):
        row_c = []
        for j in range(n_corr):
            r = pearson_corr(col_vectors[corr_cols[i]], col_vectors[corr_cols[j]])
            row_c.append(r)
        corr_matrix.append(row_c)

    # Short aliases
    aliases = {"Math": "Math", "Science": "Sci", "English": "Eng",
               "History": "Hist", "StudyHours": "Study", "Absences": "Abs"}

    print("  Pearson Correlation Matrix (6 x 6):")
    print()
    alias_list = [aliases[c] for c in corr_cols]
    col_w = 8
    header = "  " + " " * 6
    for a in alias_list:
        header = header + a.rjust(col_w)
    print(header)
    print("  " + "-" * (6 + col_w * n_corr))
    for i in range(n_corr):
        row_str = "  " + alias_list[i].ljust(6)
        for j in range(n_corr):
            row_str = row_str + "{:.3f}".format(corr_matrix[i][j]).rjust(col_w)
        print(row_str)

    # Top and bottom correlations
    pairs_corr = []
    for i in range(n_corr):
        for j in range(i + 1, n_corr):
            pairs_corr.append((corr_cols[i], corr_cols[j], corr_matrix[i][j]))

    pairs_corr.sort(key=lambda x: -abs(x[2]))
    print()
    print("  Top 3 highest (absolute) correlations:")
    for col_a, col_b, r in pairs_corr[:3]:
        print("    {} <-> {}  r={:.3f}".format(col_a, col_b, r))

    pairs_corr_signed = sorted(pairs_corr, key=lambda x: x[2])
    print()
    print("  Lowest correlation (weakest linear relationship):")
    col_a, col_b, r = pairs_corr_signed[0]
    print("    {} <-> {}  r={:.3f}".format(col_a, col_b, r))

    # -----------------------------------------------------------------------
    # === PHASE 5 (Ch6): FREQUENT PATTERN MINING ===
    # -----------------------------------------------------------------------
    print_phase_header(5, 6, "FREQUENT PATTERN MINING ON GRADE CATEGORIES")
    print()

    # Build transactions: each student = set of grade labels per subject
    transactions = []
    for row in working_data:
        t_items = []
        for col in SUBJECT_COLS:
            label = col + "_" + discretize_score(float(row[col]))
            t_items.append(label)
        # Add Result as an item too
        t_items.append("Result_" + row["Result"])
        transactions.append(frozenset(t_items))

    print("  Transactions built: {} total".format(len(transactions)))
    print("  Sample (Alice):", sorted(transactions[0]))
    print()

    min_sup  = 5
    min_conf = 0.7
    print("  Apriori: min_support={}, min_confidence={}".format(min_sup, min_conf))

    frequent_itemsets = apriori(transactions, min_sup)

    print()
    print("  Frequent itemsets (support >= {}):".format(min_sup))
    print("  " + "-" * 60)
    sorted_itemsets = sorted(frequent_itemsets.items(), key=lambda x: (-len(x[0]), -x[1]))
    for itemset, count in sorted_itemsets:
        print("    support={:3d}  {}".format(count, sorted(itemset)))

    rules = generate_rules(frequent_itemsets, min_conf)

    print()
    print("  All association rules (confidence >= {}):".format(min_conf))
    print("  " + "-" * 65)
    rules_sorted = sorted(rules, key=lambda r: -r[3])
    for ant, cons, sup, conf in rules_sorted:
        print("    {} => {}".format(sorted(ant), sorted(cons)))
        print("       support={:3d}  confidence={:.3f}".format(sup, conf))

    # Filter rules whose consequent contains a Fail_grade item
    print()
    print("  Rules predicting a Fail_grade outcome:")
    print("  " + "-" * 65)
    fail_rules = []
    for ant, cons, sup, conf in rules_sorted:
        for item in cons:
            if "Fail_grade" in item:
                fail_rules.append((ant, cons, sup, conf))
                break
    if len(fail_rules) == 0:
        print("    (none found at these thresholds)")
    else:
        for ant, cons, sup, conf in fail_rules:
            print("    {} => {}".format(sorted(ant), sorted(cons)))
            print("       support={:3d}  confidence={:.3f}".format(sup, conf))

    # -----------------------------------------------------------------------
    # === PHASE 6 (Ch5): CLUSTERING ===
    # -----------------------------------------------------------------------
    print_phase_header(6, 5, "CLUSTERING (K-MEANS K=3)")
    print()

    cluster_cols = ["Math", "Science", "StudyHours", "Absences"]
    print("  Features used (normalised): {}".format(cluster_cols))
    print()

    labels3, centroids3, sse3 = kmeans(norm_data, k=3, col_names=cluster_cols)

    # Compute cluster profiles
    print("  Cluster assignments:")
    print("  " + "-" * 55)
    for i in range(len(norm_data)):
        row = norm_data[i]
        print("    {:8s}  Result={:<5}  Cluster={}".format(
            row["Name"], row["Result"], labels3[i]))

    # Cluster means (in original scale)
    print()
    print("  Cluster profiles (original scale means):")
    cluster_labels_human = {}
    for ki in range(3):
        cluster_rows = [working_data[i] for i in range(len(working_data)) if labels3[i] == ki]
        if len(cluster_rows) == 0:
            continue
        math_mean  = mean_of([float(r["Math"])       for r in cluster_rows])
        sci_mean   = mean_of([float(r["Science"])     for r in cluster_rows])
        study_mean = mean_of([float(r["StudyHours"])  for r in cluster_rows])
        abs_mean   = mean_of([float(r["Absences"])    for r in cluster_rows])
        result_counts = collections.Counter()
        for r in cluster_rows:
            result_counts[r["Result"]] = result_counts[r["Result"]] + 1
        dominant = max(result_counts, key=lambda x: result_counts[x])

        # Assign human-readable label
        if dominant == "Pass" and math_mean >= 70:
            human_label = "High Achievers"
        elif dominant == "Fail":
            human_label = "At Risk"
        else:
            human_label = "Average Students"
        cluster_labels_human[ki] = human_label

        print()
        print("  Cluster {} -- \"{}\"  ({} students, dominant={})".format(
            ki, human_label, len(cluster_rows), dominant))
        print("    Math mean={:.1f}  Science mean={:.1f}  StudyHours mean={:.1f}  Absences mean={:.1f}".format(
            math_mean, sci_mean, study_mean, abs_mean))
        print("    Result distribution: {}".format(dict(result_counts)))

    print()
    print("  SSE (K=3): {:.4f}".format(sse3))

    # -----------------------------------------------------------------------
    # === PHASE 7 (Ch7): CLASSIFICATION ===
    # -----------------------------------------------------------------------
    print_phase_header(7, 7, "CLASSIFICATION (k-NN + NAIVE BAYES)")
    print()

    # Split: first 20 = train, last 5 = test (on normalised data)
    train_data = norm_data[:20]
    test_data  = norm_data[20:]

    print("  Train: {} students  |  Test: {} students".format(
        len(train_data), len(test_data)))
    print()
    print("  Test students: {}".format(
        [row["Name"] for row in test_data]))
    print()

    feature_cols = NUMERIC_COLS  # 6 normalised features
    true_labels  = get_col(test_data, CLASS_COL)

    # ---- k-NN (k=3) ----
    print("  --- k-NN (k=3) ---")
    knn_predictions = []
    for row in test_data:
        knn_predictions.append(knn_predict(train_data, row, feature_cols, k=3))

    print()
    print("  k-NN predictions:")
    knn_table_rows = []
    for i in range(len(test_data)):
        correct = "YES" if true_labels[i] == knn_predictions[i] else "NO"
        knn_table_rows.append([
            test_data[i]["Name"], true_labels[i], knn_predictions[i], correct
        ])
    print_table(["Name", "True", "Predicted", "Correct?"],
                knn_table_rows, [10, 8, 12, 10])

    knn_confusion = build_confusion_matrix(true_labels, knn_predictions, CLASSES)
    print_confusion_matrix(knn_confusion, CLASSES, "k-NN")
    knn_acc = compute_accuracy(knn_confusion, CLASSES)
    print()
    print("  k-NN Accuracy: {:.3f}  ({}/{})".format(
        knn_acc,
        int(round(knn_acc * len(test_data))),
        len(test_data)))

    # ---- Naive Bayes ----
    print()
    print("  --- Naive Bayes (Gaussian) ---")
    nb_model = train_naive_bayes(train_data, feature_cols)
    nb_predictions = []
    for row in test_data:
        nb_predictions.append(predict_naive_bayes(nb_model, row, feature_cols))

    print()
    print("  Naive Bayes predictions:")
    nb_table_rows = []
    for i in range(len(test_data)):
        correct = "YES" if true_labels[i] == nb_predictions[i] else "NO"
        nb_table_rows.append([
            test_data[i]["Name"], true_labels[i], nb_predictions[i], correct
        ])
    print_table(["Name", "True", "Predicted", "Correct?"],
                nb_table_rows, [10, 8, 12, 10])

    nb_confusion = build_confusion_matrix(true_labels, nb_predictions, CLASSES)
    print_confusion_matrix(nb_confusion, CLASSES, "Naive Bayes")
    nb_acc = compute_accuracy(nb_confusion, CLASSES)
    print()
    print("  Naive Bayes Accuracy: {:.3f}  ({}/{})".format(
        nb_acc,
        int(round(nb_acc * len(test_data))),
        len(test_data)))

    # ---- Comparison ----
    print()
    print("  --- Classifier Comparison ---")
    print()
    comp_headers = ["Classifier", "Accuracy", "Correct/Total"]
    comp_rows2 = [
        ["k-NN (k=3)",   "{:.3f}".format(knn_acc),
         "{}/{}".format(int(round(knn_acc * len(test_data))), len(test_data))],
        ["Naive Bayes",  "{:.3f}".format(nb_acc),
         "{}/{}".format(int(round(nb_acc * len(test_data))), len(test_data))],
    ]
    print_table(comp_headers, comp_rows2, [16, 10, 16])

    # Recommendation
    print()
    print("  --- Recommendation for Early Warning System ---")
    if knn_acc >= nb_acc:
        better = "k-NN (k=3)"
    else:
        better = "Naive Bayes"
    print()
    print("  Recommended classifier: {}".format(better))
    print()
    print("  Reasoning:")
    print("    - Both classifiers use normalised numeric features.")
    print("    - k-NN is distance-based: works well when similar students")
    print("      have similar outcomes (no training phase needed).")
    print("    - Naive Bayes is probabilistic: fast, handles small datasets,")
    print("      gives interpretable class probabilities.")
    print("    - For a school early-warning system, interpretability and speed")
    print("      matter: Naive Bayes is easy to explain to teachers, while")
    print("      k-NN is robust when sufficient historical data is available.")
    print("    - Monitor false-negative rate (failing students predicted as")
    print("      passing) -- this is the most costly error in practice.")

    # -----------------------------------------------------------------------
    print()
    print_separator()
    print("  Student Performance Predictor finished.")
    print("  All 7 phases (Ch1/Ch2/Ch3/Ch4/Ch5/Ch6/Ch7) complete.")
    print_separator()
    print()


if __name__ == "__main__":
    main()
