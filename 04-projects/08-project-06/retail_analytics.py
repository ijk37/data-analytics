# ============================================================
# PROJECT 06: Retail Sales Analytics
# Chapters combined: Ch1 + Ch2 + Ch3 + Ch4 + Ch5 + Ch6 + Ch7
# Pure Python stdlib only — no external packages required.
# ============================================================

import csv
import math
import collections
import io

# ===== SECTION 1: DATASET =====

RAW_CSV = """CustomerID,Age,Gender,Purchases,AvgSpend,Returns,Months_Active,Category1,Category2,Category3,Category4,Churned
C01,34,M,12,85,1,3,1,0,1,0,No
C02,52,F,3,210,0,1,0,1,0,0,Yes
C03,27,M,20,45,2,3,0,0,1,1,No
C04,45,F,8,320,1,2,1,1,0,0,No
C05,23,M,2,30,0,1,0,0,1,0,Yes
C06,38,F,15,95,3,3,0,1,1,0,No
C07,61,M,5,180,0,2,1,0,0,1,No
C08,29,F,18,65,1,3,0,0,1,1,No
C09,44,M,9,290,2,2,1,0,0,0,Yes
C10,33,F,11,110,1,3,0,1,0,1,No
C11,55,M,4,140,0,1,0,0,1,0,Yes
C12,26,F,22,55,2,3,0,0,1,1,No
C13,48,M,7,260,1,2,1,1,0,0,No
C14,31,F,16,80,2,3,0,0,1,0,No
C15,19,M,1,20,0,1,0,0,0,1,Yes
C16,42,F,10,195,1,2,1,0,1,0,No
C17,57,M,6,210,0,2,0,1,0,1,Yes
C18,36,F,13,75,1,3,0,0,1,1,No
C19,24,M,3,40,0,1,0,0,1,0,Yes
C20,50,F,8,300,2,2,1,1,0,0,No
C21,39,M,14,90,1,3,0,1,1,0,No
C22,63,F,2,250,0,1,0,0,0,1,Yes
C23,28,M,19,50,3,3,0,0,1,1,No
C24,46,F,9,275,1,2,1,0,0,0,No
C25,32,M,12,100,2,3,0,1,1,0,No
C26,58,F,4,220,0,1,0,1,0,0,Yes
C27,25,M,21,60,2,3,0,0,1,0,No
C28,43,F,7,185,1,2,1,0,0,1,No
C29,37,M,15,85,1,3,0,0,1,1,No
C30,54,F,5,240,0,1,0,1,0,0,Yes
"""

# ===== SECTION 2: UTILITY FUNCTIONS =====

def load_csv_from_string(raw):
    """Parse the hardcoded CSV string into a column dictionary."""
    reader = csv.DictReader(io.StringIO(raw.strip()))
    rows = list(reader)
    if len(rows) == 0:
        raise ValueError("CSV data is empty.")
    columns = {}
    for col_name in rows[0]:
        columns[col_name] = []
        for row in rows:
            columns[col_name].append(row[col_name])
    return columns, len(rows)


def load_csv(csv_file):
    """Standard load_csv for file-based loading."""
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


def to_float(lst):
    """Convert a list of strings to floats."""
    result = []
    for v in lst:
        result.append(float(v))
    return result


def mean(lst):
    """Arithmetic mean."""
    if len(lst) == 0:
        return 0.0
    return sum(lst) / len(lst)


def std_dev(lst):
    """Population standard deviation."""
    if len(lst) < 2:
        return 0.0
    m = mean(lst)
    variance = sum((x - m) ** 2 for x in lst) / len(lst)
    return math.sqrt(variance)


def pearson(x_list, y_list):
    """Pearson correlation coefficient between two numeric lists."""
    n = len(x_list)
    mx = mean(x_list)
    my = mean(y_list)
    num = 0.0
    dx = 0.0
    dy = 0.0
    for i in range(n):
        num += (x_list[i] - mx) * (y_list[i] - my)
        dx += (x_list[i] - mx) ** 2
        dy += (y_list[i] - my) ** 2
    denom = math.sqrt(dx * dy)
    if denom == 0:
        return 0.0
    return num / denom


def iqr_outliers(lst, label):
    """Detect outliers via IQR rule. Returns list of (index, value) pairs."""
    sorted_lst = sorted(lst)
    n = len(sorted_lst)
    q1 = sorted_lst[n // 4]
    q3 = sorted_lst[(3 * n) // 4]
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = []
    for i, v in enumerate(lst):
        if v < lower or v > upper:
            outliers.append((i, v))
    print("  IQR Outlier Detection for %s:" % label)
    print("    Q1=%.2f  Q3=%.2f  IQR=%.2f  Lower fence=%.2f  Upper fence=%.2f" % (
        q1, q3, iqr, lower, upper))
    if outliers:
        for idx, val in outliers:
            print("    OUTLIER at index %d: value=%.2f" % (idx, val))
    else:
        print("    No outliers detected.")
    return outliers


def minmax_normalize(lst):
    """Min-max normalize to [0,1]."""
    mn = min(lst)
    mx = max(lst)
    result = []
    for v in lst:
        if mx == mn:
            result.append(0.0)
        else:
            result.append((v - mn) / (mx - mn))
    return result


def euclidean(a, b):
    """Euclidean distance between two equal-length lists."""
    total = 0.0
    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2
    return math.sqrt(total)


def kmeans(data_rows, k, max_iter=100, seed=42):
    """
    K-means clustering.
    data_rows: list of lists (each inner list is one sample, all floats)
    Returns: (labels list, centroids list)
    """
    # Seed the pseudo-random initialization deterministically
    rng = collections.deque(range(len(data_rows)))
    # Use a simple deterministic pick: spread initial centroids across data
    step = max(1, len(data_rows) // k)
    centroids = []
    for i in range(k):
        centroids.append(list(data_rows[i * step]))

    labels = [0] * len(data_rows)
    for iteration in range(max_iter):
        # Assignment step
        new_labels = []
        for row in data_rows:
            best_k = 0
            best_dist = euclidean(row, centroids[0])
            for ki in range(1, k):
                d = euclidean(row, centroids[ki])
                if d < best_dist:
                    best_dist = d
                    best_k = ki
            new_labels.append(best_k)

        # Check convergence
        if new_labels == labels:
            break
        labels = new_labels

        # Update step
        n_features = len(data_rows[0])
        new_centroids = []
        for ki in range(k):
            members = [data_rows[j] for j in range(len(data_rows)) if labels[j] == ki]
            if len(members) == 0:
                new_centroids.append(centroids[ki])
            else:
                centroid = []
                for f in range(n_features):
                    centroid.append(mean([m[f] for m in members]))
                new_centroids.append(centroid)
        centroids = new_centroids

    return labels, centroids


def confusion_matrix_binary(true_labels, pred_labels, pos_class):
    """
    Build confusion matrix for binary classification.
    Returns: (TP, FP, FN, TN)
    """
    tp = fp = fn = tn = 0
    for t, p in zip(true_labels, pred_labels):
        if t == pos_class and p == pos_class:
            tp += 1
        elif t != pos_class and p == pos_class:
            fp += 1
        elif t == pos_class and p != pos_class:
            fn += 1
        else:
            tn += 1
    return tp, fp, fn, tn


def precision_recall_f1(tp, fp, fn):
    """Compute precision, recall, F1 from counts."""
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return prec, rec, f1


# ===== SECTION 3: APRIORI HELPERS =====

def get_frequent_itemsets(transactions, min_support):
    """
    Simple Apriori implementation.
    transactions: list of frozensets
    min_support: minimum count (integer)
    Returns: dict mapping frozenset -> count, for all frequent itemsets size >= 1
    """
    # Collect all items
    all_items = set()
    for t in transactions:
        for item in t:
            all_items.add(item)

    frequent = {}

    # Size-1 frequent itemsets
    candidates_1 = []
    for item in sorted(all_items):
        candidates_1.append(frozenset([item]))

    current_frequent = []
    for cand in candidates_1:
        count = sum(1 for t in transactions if cand.issubset(t))
        if count >= min_support:
            frequent[cand] = count
            current_frequent.append(cand)

    # Size >= 2
    size = 2
    while len(current_frequent) >= size - 1:
        # Generate candidates of this size from previous frequent items
        prev_items = list(current_frequent)
        candidates = set()
        for i in range(len(prev_items)):
            for j in range(i + 1, len(prev_items)):
                union = prev_items[i] | prev_items[j]
                if len(union) == size:
                    candidates.add(union)

        next_frequent = []
        for cand in sorted(candidates, key=lambda x: sorted(x)):
            count = sum(1 for t in transactions if cand.issubset(t))
            if count >= min_support:
                frequent[cand] = count
                next_frequent.append(cand)

        if len(next_frequent) == 0:
            break
        current_frequent = next_frequent
        size += 1

    return frequent


def generate_rules(frequent, transactions, min_confidence):
    """
    Generate association rules from frequent itemsets.
    Returns list of (antecedent, consequent, support_count, confidence)
    """
    rules = []
    for itemset, count in frequent.items():
        if len(itemset) < 2:
            continue
        items = list(itemset)
        # Try all non-empty proper subsets as antecedents
        for mask in range(1, 2 ** len(items) - 1):
            antecedent = frozenset(items[i] for i in range(len(items)) if mask & (1 << i))
            consequent = itemset - antecedent
            if len(consequent) == 0:
                continue
            ant_count = sum(1 for t in transactions if antecedent.issubset(t))
            if ant_count == 0:
                continue
            confidence = count / ant_count
            if confidence >= min_confidence:
                rules.append((antecedent, consequent, count, confidence))
    # Remove duplicate rules (same ant/con can appear from different itemsets)
    seen = set()
    unique_rules = []
    for r in rules:
        key = (r[0], r[1])
        if key not in seen:
            seen.add(key)
            unique_rules.append(r)
    return unique_rules


# ===== SECTION 4: KNN CLASSIFIER =====

def knn_predict(train_rows, train_labels, test_row, k):
    """
    k-NN prediction for a single test_row.
    train_rows: list of lists (numeric features)
    train_labels: list of class labels
    Returns: predicted class label
    """
    distances = []
    for i, tr in enumerate(train_rows):
        d = euclidean(tr, test_row)
        distances.append((d, train_labels[i]))
    distances.sort(key=lambda pair: pair[0])
    neighbors = distances[:k]
    counter = collections.Counter()
    for _, label in neighbors:
        counter[label] += 1
    return counter.most_common(1)[0][0]


# ===== SECTION 5: NAIVE BAYES (GAUSSIAN) =====

def gaussian_nb_train(train_rows, train_labels):
    """
    Train Gaussian Naive Bayes.
    Returns dict: class -> (prior, [(mean, std), ...] per feature)
    """
    classes = list(set(train_labels))
    model = {}
    n_total = len(train_labels)
    for cls in classes:
        indices = [i for i in range(len(train_labels)) if train_labels[i] == cls]
        prior = len(indices) / n_total
        feature_stats = []
        n_features = len(train_rows[0])
        for f in range(n_features):
            vals = [train_rows[i][f] for i in indices]
            feature_stats.append((mean(vals), std_dev(vals)))
        model[cls] = (prior, feature_stats)
    return model


def gaussian_pdf(x, mu, sigma):
    """Gaussian probability density function."""
    if sigma == 0:
        return 1.0 if x == mu else 1e-9
    exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
    return (1.0 / (math.sqrt(2 * math.pi) * sigma)) * math.exp(exponent)


def gaussian_nb_predict(model, test_row):
    """Predict class for a single test_row using trained Gaussian NB model."""
    best_class = None
    best_log_prob = None
    for cls, (prior, feature_stats) in model.items():
        log_prob = math.log(prior + 1e-9)
        for f, (mu, sigma) in enumerate(feature_stats):
            pdf_val = gaussian_pdf(test_row[f], mu, sigma)
            log_prob += math.log(pdf_val + 1e-9)
        if best_log_prob is None or log_prob > best_log_prob:
            best_log_prob = log_prob
            best_class = cls
    return best_class


# ===== SECTION 6: REPORT HELPERS =====

def print_separator(char="-", width=60):
    print(char * width)


def print_header(title):
    print()
    print("=" * 60)
    print("  " + title)
    print("=" * 60)


# ============================================================
# MAIN ANALYSIS
# ============================================================

def main():

    # ===== SECTION 7: LOAD DATA =====

    columns, n_rows = load_csv_from_string(RAW_CSV)

    # Convert numeric columns to float lists
    age          = to_float(columns["Age"])
    purchases    = to_float(columns["Purchases"])
    avg_spend    = to_float(columns["AvgSpend"])
    returns      = to_float(columns["Returns"])
    months       = to_float(columns["Months_Active"])
    cat1         = to_float(columns["Category1"])
    cat2         = to_float(columns["Category2"])
    cat3         = to_float(columns["Category3"])
    cat4         = to_float(columns["Category4"])
    gender_raw   = columns["Gender"]
    churned_raw  = columns["Churned"]
    customer_ids = columns["CustomerID"]

    # ===== SECTION 8: ANALYSIS PHASES =====

    # === PHASE 1 (Ch1+Ch2): Attribute Profiling and Descriptive Stats ===

    print_header("PHASE 1 (Ch1+Ch2): Attribute Profiling and Descriptive Stats")

    print("\n--- Attribute Type Table ---")
    attr_table = [
        ("CustomerID",    "Nominal",        "Categorical",   "Unique identifier"),
        ("Age",           "Ratio",          "Continuous",    "Years"),
        ("Gender",        "Nominal",        "Binary",        "M or F"),
        ("Purchases",     "Ratio",          "Discrete",      "Count in 3 months"),
        ("AvgSpend",      "Ratio",          "Continuous",    "USD per purchase"),
        ("Returns",       "Ratio",          "Discrete",      "Items returned"),
        ("Months_Active", "Ratio",          "Discrete",      "1-3"),
        ("Category1",     "Nominal",        "Binary",        "Electronics"),
        ("Category2",     "Nominal",        "Binary",        "Clothing"),
        ("Category3",     "Nominal",        "Binary",        "Food"),
        ("Category4",     "Nominal",        "Binary",        "Books"),
        ("Churned",       "Nominal",        "Binary",        "Target: Yes/No"),
    ]
    print("  %-16s %-12s %-14s %s" % ("Attribute", "Scale", "Type", "Notes"))
    print_separator()
    for row in attr_table:
        print("  %-16s %-12s %-14s %s" % row)

    print("\n--- Class Distribution ---")
    churned_yes = [i for i, v in enumerate(churned_raw) if v == "Yes"]
    churned_no  = [i for i, v in enumerate(churned_raw) if v == "No"]
    n_yes = len(churned_yes)
    n_no  = len(churned_no)
    print("  Churned=Yes: %d (%.1f%%)" % (n_yes, 100.0 * n_yes / n_rows))
    print("  Churned=No : %d (%.1f%%)" % (n_no,  100.0 * n_no  / n_rows))

    print("\n--- Per-Churn-Group Means ---")
    numeric_cols = {
        "Age":           age,
        "Purchases":     purchases,
        "AvgSpend":      avg_spend,
        "Returns":       returns,
        "Months_Active": months,
    }
    print("  %-16s %12s %12s %12s" % ("Feature", "Churned=Yes", "Churned=No", "Abs Diff"))
    print_separator()
    diffs = []
    for col_name, col_vals in numeric_cols.items():
        yes_vals = [col_vals[i] for i in churned_yes]
        no_vals  = [col_vals[i] for i in churned_no]
        mean_yes = mean(yes_vals)
        mean_no  = mean(no_vals)
        diff     = abs(mean_yes - mean_no)
        diffs.append((diff, col_name, mean_yes, mean_no))
        print("  %-16s %12.2f %12.2f %12.2f" % (col_name, mean_yes, mean_no, diff))

    print("\n--- Features Ranked by Mean Difference (Churned vs Not) ---")
    diffs.sort(reverse=True)
    for rank, (diff, col_name, mean_yes, mean_no) in enumerate(diffs, 1):
        direction = "higher in churned" if mean_yes > mean_no else "higher in non-churned"
        print("  %d. %-16s  diff=%.2f  (%s)" % (rank, col_name, diff, direction))


    # === PHASE 2 (Ch3): Multivariate Analysis ===

    print_header("PHASE 2 (Ch3): Multivariate Analysis")

    corr_names = ["Age", "Purchases", "AvgSpend", "Returns", "Months_Active"]
    corr_data  = [age, purchases, avg_spend, returns, months]
    n_corr = len(corr_names)

    print("\n--- Pearson Correlation Matrix ---")
    print("  %-16s" % "", end="")
    for name in corr_names:
        print(" %8s" % name[:8], end="")
    print()
    print_separator(width=70)

    corr_matrix = []
    for i in range(n_corr):
        row_corrs = []
        for j in range(n_corr):
            r = pearson(corr_data[i], corr_data[j])
            row_corrs.append(r)
        corr_matrix.append(row_corrs)

    for i, name in enumerate(corr_names):
        print("  %-16s" % name, end="")
        for j in range(n_corr):
            print(" %8.3f" % corr_matrix[i][j], end="")
        print()

    # Find strongest positive and negative correlations (off-diagonal)
    best_pos = None
    best_neg = None
    for i in range(n_corr):
        for j in range(i + 1, n_corr):
            r = corr_matrix[i][j]
            if best_pos is None or r > best_pos[0]:
                best_pos = (r, corr_names[i], corr_names[j])
            if best_neg is None or r < best_neg[0]:
                best_neg = (r, corr_names[i], corr_names[j])

    print("\n--- Key Correlations ---")
    print("  Strongest POSITIVE: %s vs %s  r=%.3f" % (best_pos[1], best_pos[2], best_pos[0]))
    print("  Strongest NEGATIVE: %s vs %s  r=%.3f" % (best_neg[1], best_neg[2], best_neg[0]))
    print("  Interpretation: High AvgSpend tends to go with fewer Purchases (high-value, low-frequency buyers).")


    # === PHASE 3 (Ch4): Preprocessing ===

    print_header("PHASE 3 (Ch4): Preprocessing")

    print("\n--- Outlier Detection (IQR Rule) ---")
    iqr_outliers(avg_spend, "AvgSpend")
    iqr_outliers(returns,   "Returns")

    print("\n--- Log Transform of AvgSpend (log(AvgSpend + 1)) ---")
    log_avg_spend = []
    for v in avg_spend:
        log_avg_spend.append(math.log(v + 1))
    print("  Original AvgSpend mean=%.2f  std=%.2f" % (mean(avg_spend), std_dev(avg_spend)))
    print("  Log-transformed mean=%.4f  std=%.4f  (reduced right skew)" % (
        mean(log_avg_spend), std_dev(log_avg_spend)))

    print("\n--- Min-Max Normalization ---")
    norm_age       = minmax_normalize(age)
    norm_purchases = minmax_normalize(purchases)
    norm_log_spend = minmax_normalize(log_avg_spend)
    norm_returns   = minmax_normalize(returns)
    norm_months    = minmax_normalize(months)

    # Encode gender: M=1, F=0
    gender_encoded = []
    for g in gender_raw:
        if g == "M":
            gender_encoded.append(1.0)
        else:
            gender_encoded.append(0.0)

    print("  All features normalized to [0,1].")
    print("  Gender encoded: M=1, F=0")
    print("  Sample (first 3 customers):")
    print("  %-6s %8s %10s %12s %8s %8s %8s" % (
        "CustID", "Norm_Age", "Norm_Purch", "Norm_LgSpnd", "Norm_Ret", "Norm_Mon", "Gender"))
    for i in range(3):
        print("  %-6s %8.3f %10.3f %12.3f %8.3f %8.3f %8.0f" % (
            customer_ids[i], norm_age[i], norm_purchases[i], norm_log_spend[i],
            norm_returns[i], norm_months[i], gender_encoded[i]))


    # === PHASE 4 (Ch6): Pattern Mining on Category Combinations ===

    print_header("PHASE 4 (Ch6): Pattern Mining on Category Combinations")

    # Build transactions: each customer's purchased categories
    category_names = ["Electronics", "Clothing", "Food", "Books"]
    category_cols  = [cat1, cat2, cat3, cat4]

    all_transactions = []
    churned_transactions = []
    not_churned_transactions = []

    for i in range(n_rows):
        transaction = []
        for c_idx, c_col in enumerate(category_cols):
            if c_col[i] == 1.0:
                transaction.append(category_names[c_idx])
        t_frozenset = frozenset(transaction)
        all_transactions.append(t_frozenset)
        if churned_raw[i] == "Yes":
            churned_transactions.append(t_frozenset)
        else:
            not_churned_transactions.append(t_frozenset)

    print("\n--- Category Transaction Summary ---")
    print("  Churned=Yes customers: %d transactions" % len(churned_transactions))
    print("  Churned=No  customers: %d transactions" % len(not_churned_transactions))

    print("\n  Category frequencies in Churned=Yes group:")
    for cat in category_names:
        cnt = sum(1 for t in churned_transactions if cat in t)
        print("    %-14s: %d / %d  (%.0f%%)" % (
            cat, cnt, len(churned_transactions), 100.0 * cnt / max(1, len(churned_transactions))))

    print("\n  Category frequencies in Churned=No group:")
    for cat in category_names:
        cnt = sum(1 for t in not_churned_transactions if cat in t)
        print("    %-14s: %d / %d  (%.0f%%)" % (
            cat, cnt, len(not_churned_transactions), 100.0 * cnt / max(1, len(not_churned_transactions))))

    print("\n--- Apriori: Frequent Itemsets (min_support=3) on ALL customers ---")
    min_support = 3
    frequent_sets = get_frequent_itemsets(all_transactions, min_support)
    print("  Found %d frequent itemsets." % len(frequent_sets))
    for iset in sorted(frequent_sets.keys(), key=lambda x: (-frequent_sets[x], sorted(x))):
        if len(iset) >= 2:
            items_str = ", ".join(sorted(iset))
            print("  {%s}  support=%d" % (items_str, frequent_sets[iset]))

    print("\n--- Association Rules (min_confidence=0.5) ---")
    min_confidence = 0.5
    rules = generate_rules(frequent_sets, all_transactions, min_confidence)
    rules_sorted = sorted(rules, key=lambda r: -r[3])
    if len(rules_sorted) == 0:
        print("  No rules generated at min_support=3, min_confidence=0.5.")
    else:
        for ant, con, sup, conf in rules_sorted:
            ant_str = "{%s}" % ", ".join(sorted(ant))
            con_str = "{%s}" % ", ".join(sorted(con))
            note = ""
            # Flag rules where consequent is a single category (single-category buyers churn more)
            if len(con) == 1:
                churn_with_cat = sum(
                    1 for i, t in enumerate(all_transactions)
                    if con.issubset(t) and churned_raw[i] == "Yes"
                )
                total_with_cat = sum(1 for t in all_transactions if con.issubset(t))
                if total_with_cat > 0:
                    churn_rate = churn_with_cat / total_with_cat
                    if churn_rate > 0.4:
                        note = "  ** CHURN SIGNAL: %.0f%% of customers buying %s churned **" % (
                            100 * churn_rate, ", ".join(sorted(con)))
            print("  %s => %s  support=%d  confidence=%.2f%s" % (
                ant_str, con_str, sup, conf, note))

    print("\n  Interpretation: Single-category buyers (especially Clothing-only or Food-only)")
    print("  show higher churn rates. Encourage cross-category purchasing to improve retention.")


    # === PHASE 5 (Ch5): Customer Segmentation ===

    print_header("PHASE 5 (Ch5): Customer Segmentation via K-Means (K=3)")

    # Features: normalized Purchases, log_AvgSpend, Months_Active
    clustering_data = []
    for i in range(n_rows):
        clustering_data.append([norm_purchases[i], norm_log_spend[i], norm_months[i]])

    labels, centroids = kmeans(clustering_data, k=3)

    print("\n--- Cluster Membership ---")
    cluster_counts = collections.Counter(labels)
    for ki in range(3):
        count = cluster_counts[ki]
        members = [customer_ids[i] for i in range(n_rows) if labels[i] == ki]
        print("  Cluster %d: %d customers  -> %s" % (ki, count, ", ".join(members)))

    print("\n--- Cluster Profiles (normalized scale 0-1) ---")
    feat_names = ["Norm_Purchases", "Norm_LogSpend", "Norm_Months"]
    print("  %-10s %14s %14s %14s %10s %12s" % (
        "Cluster", feat_names[0], feat_names[1], feat_names[2], "% Churned", "Label"))
    print_separator(width=80)

    cluster_labels_text = []
    for ki in range(3):
        member_indices = [i for i in range(n_rows) if labels[i] == ki]
        c_purch  = mean([norm_purchases[i] for i in member_indices])
        c_spend  = mean([norm_log_spend[i] for i in member_indices])
        c_months = mean([norm_months[i] for i in member_indices])
        n_churned_in_cluster = sum(1 for i in member_indices if churned_raw[i] == "Yes")
        pct_churned = 100.0 * n_churned_in_cluster / max(1, len(member_indices))

        # Auto-label based on centroid characteristics
        if c_purch > 0.55:
            cluster_label = "Frequent Low-Spenders"
        elif c_spend > 0.55:
            cluster_label = "Occasional High-Spenders"
        else:
            cluster_label = "Low-Engagement (At Risk)"

        cluster_labels_text.append(cluster_label)
        print("  %-10s %14.3f %14.3f %14.3f %10.1f %s" % (
            "Cluster %d" % ki, c_purch, c_spend, c_months, pct_churned, cluster_label))

    print("\n  Key insight: Clusters with low Purchases and low Months_Active have higher")
    print("  churn rates. High-Spenders who visit infrequently are also at risk.")


    # === PHASE 6 (Ch7): Churn Prediction ===

    print_header("PHASE 6 (Ch7): Churn Prediction")

    # Feature matrix: all 5 normalized numeric features
    all_features = []
    for i in range(n_rows):
        all_features.append([
            norm_age[i], norm_purchases[i], norm_log_spend[i],
            norm_returns[i], norm_months[i]
        ])

    # Binary target: Yes=1, No=0
    churn_binary = []
    for v in churned_raw:
        if v == "Yes":
            churn_binary.append("Yes")
        else:
            churn_binary.append("No")

    # Train/test split: first 22 train, last 8 test
    split = 22
    train_X = all_features[:split]
    train_y = churn_binary[:split]
    test_X  = all_features[split:]
    test_y  = churn_binary[split:]
    test_ids = customer_ids[split:]

    print("\n  Train set: %d samples  |  Test set: %d samples" % (len(train_y), len(test_y)))
    print("  Target class: Yes=Churned, No=Not Churned")
    print("  Features: Age, Purchases, Log(AvgSpend), Returns, Months_Active (all normalized)")

    # ---- k-NN (k=3) ----
    print("\n--- k-NN Classifier (k=3) ---")
    knn_preds = []
    for test_row in test_X:
        pred = knn_predict(train_X, train_y, test_row, k=3)
        knn_preds.append(pred)

    print("  %-10s %10s %10s" % ("CustomerID", "True", "Predicted"))
    print_separator(width=35)
    for i in range(len(test_y)):
        match = "OK" if knn_preds[i] == test_y[i] else "WRONG"
        print("  %-10s %10s %10s  %s" % (test_ids[i], test_y[i], knn_preds[i], match))

    knn_tp, knn_fp, knn_fn, knn_tn = confusion_matrix_binary(test_y, knn_preds, "Yes")
    knn_acc = (knn_tp + knn_tn) / len(test_y)
    knn_prec, knn_rec, knn_f1 = precision_recall_f1(knn_tp, knn_fp, knn_fn)

    print("\n  Confusion Matrix (Positive class = Yes/Churned):")
    print("               Pred=Yes  Pred=No")
    print("  True=Yes       %3d       %3d   (TP, FN)" % (knn_tp, knn_fn))
    print("  True=No        %3d       %3d   (FP, TN)" % (knn_fp, knn_tn))
    print("  Accuracy : %.3f" % knn_acc)
    print("  Precision: %.3f  (of predicted churners, how many truly churned)" % knn_prec)
    print("  Recall   : %.3f  (of actual churners, how many did we catch)" % knn_rec)
    print("  F1 Score : %.3f" % knn_f1)

    # ---- Naive Bayes (Gaussian) ----
    print("\n--- Naive Bayes (Gaussian) Classifier ---")
    nb_model = gaussian_nb_train(train_X, train_y)
    nb_preds = []
    for test_row in test_X:
        pred = gaussian_nb_predict(nb_model, test_row)
        nb_preds.append(pred)

    print("  %-10s %10s %10s" % ("CustomerID", "True", "Predicted"))
    print_separator(width=35)
    for i in range(len(test_y)):
        match = "OK" if nb_preds[i] == test_y[i] else "WRONG"
        print("  %-10s %10s %10s  %s" % (test_ids[i], test_y[i], nb_preds[i], match))

    nb_tp, nb_fp, nb_fn, nb_tn = confusion_matrix_binary(test_y, nb_preds, "Yes")
    nb_acc = (nb_tp + nb_tn) / len(test_y)
    nb_prec, nb_rec, nb_f1 = precision_recall_f1(nb_tp, nb_fp, nb_fn)

    print("\n  Confusion Matrix (Positive class = Yes/Churned):")
    print("               Pred=Yes  Pred=No")
    print("  True=Yes       %3d       %3d   (TP, FN)" % (nb_tp, nb_fn))
    print("  True=No        %3d       %3d   (FP, TN)" % (nb_fp, nb_tn))
    print("  Accuracy : %.3f" % nb_acc)
    print("  Precision: %.3f" % nb_prec)
    print("  Recall   : %.3f" % nb_rec)
    print("  F1 Score : %.3f" % nb_f1)

    # ---- Comparison ----
    print("\n--- Classifier Comparison ---")
    print("  %-25s %10s %10s %10s %10s" % ("Classifier", "Accuracy", "Precision", "Recall", "F1"))
    print_separator(width=68)
    print("  %-25s %10.3f %10.3f %10.3f %10.3f" % ("k-NN (k=3)", knn_acc, knn_prec, knn_rec, knn_f1))
    print("  %-25s %10.3f %10.3f %10.3f %10.3f" % ("Naive Bayes (Gaussian)", nb_acc, nb_prec, nb_rec, nb_f1))

    if knn_rec >= nb_rec:
        better = "k-NN (k=3)"
        better_rec = knn_rec
    else:
        better = "Naive Bayes (Gaussian)"
        better_rec = nb_rec

    print("\n  *** Recall for Churners (Yes class): %s has higher recall (%.3f) ***" % (
        better, better_rec))
    print("  For churn prediction, RECALL is the priority metric.")
    print("  Missing a churner (False Negative) is more costly than a false alarm (False Positive).")

    print("\n--- Business Recommendation ---")
    print("  1. Deploy the %s model for monthly churn scoring." % better)
    print("  2. Focus retention campaigns on the 'Low-Engagement (At Risk)' K-means cluster.")
    print("  3. Single-category buyers (Food-only, Clothing-only) are high churn risk;")
    print("     use cross-sell promotions to broaden their purchasing behavior.")
    print("  4. High-spenders who visit only 1 month (e.g., C02, C09) need re-engagement")
    print("     offers before the 2nd month ends.")
    print("  5. Re-run the model monthly as new transaction data arrives.")

    print()
    print("=" * 60)
    print("  RETAIL ANALYTICS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
