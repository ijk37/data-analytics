# market_analysis.py
# Project 02 -- Market Basket & Customer Segmentation
# Chapters: Ch2/Ch3 (stats) + Ch4 (preprocessing) + Ch6 (Apriori) + Ch5 (K-means)

# ===== SECTION 1: IMPORTS =====
import csv
import math


# ===== SECTION 2: CONSTANTS =====
K_CLUSTERS = 3
K_MAX_ITER = 200
MIN_SUPPORT_COUNT = 5    # out of 20 = 25%
MIN_CONFIDENCE = 0.5
NUMERIC_FEATURES = ["Age", "Visits", "Spend"]


# ===== SECTION 3: DEMO DATASET =====
CUSTOMERS = [
    {"id": "C01", "Age": 34, "Visits": 12, "Spend": 280, "Items": ["bread", "milk", "butter", "eggs"]},
    {"id": "C02", "Age": 52, "Visits": 3,  "Spend": 95,  "Items": ["beer", "chips", "soda"]},
    {"id": "C03", "Age": 27, "Visits": 20, "Spend": 450, "Items": ["bread", "milk", "yogurt", "fruit", "veg"]},
    {"id": "C04", "Age": 45, "Visits": 8,  "Spend": 320, "Items": ["meat", "veg", "fruit", "milk"]},
    {"id": "C05", "Age": 23, "Visits": 2,  "Spend": 45,  "Items": ["beer", "chips"]},
    {"id": "C06", "Age": 38, "Visits": 15, "Spend": 380, "Items": ["bread", "butter", "eggs", "milk", "yogurt"]},
    {"id": "C07", "Age": 61, "Visits": 5,  "Spend": 180, "Items": ["meat", "veg", "bread"]},
    {"id": "C08", "Age": 29, "Visits": 18, "Spend": 420, "Items": ["milk", "yogurt", "fruit", "bread", "eggs"]},
    {"id": "C09", "Age": 44, "Visits": 9,  "Spend": 290, "Items": ["meat", "veg", "beer"]},
    {"id": "C10", "Age": 33, "Visits": 11, "Spend": 310, "Items": ["bread", "milk", "butter", "fruit"]},
    {"id": "C11", "Age": 55, "Visits": 4,  "Spend": 140, "Items": ["chips", "soda", "beer"]},
    {"id": "C12", "Age": 26, "Visits": 22, "Spend": 480, "Items": ["milk", "yogurt", "fruit", "veg", "bread", "eggs"]},
    {"id": "C13", "Age": 48, "Visits": 7,  "Spend": 260, "Items": ["meat", "veg", "milk"]},
    {"id": "C14", "Age": 31, "Visits": 16, "Spend": 390, "Items": ["bread", "eggs", "butter", "milk"]},
    {"id": "C15", "Age": 19, "Visits": 1,  "Spend": 30,  "Items": ["chips", "soda"]},
    {"id": "C16", "Age": 42, "Visits": 10, "Spend": 295, "Items": ["meat", "veg", "fruit", "bread"]},
    {"id": "C17", "Age": 57, "Visits": 6,  "Spend": 210, "Items": ["meat", "beer", "bread"]},
    {"id": "C18", "Age": 36, "Visits": 13, "Spend": 355, "Items": ["milk", "yogurt", "fruit", "eggs", "bread"]},
    {"id": "C19", "Age": 24, "Visits": 3,  "Spend": 80,  "Items": ["chips", "beer", "soda"]},
    {"id": "C20", "Age": 50, "Visits": 8,  "Spend": 300, "Items": ["meat", "veg", "milk", "bread"]},
]


# ===== SECTION 4: HELPER FUNCTIONS =====

def compute_mean(values):
    total = 0.0
    for v in values:
        total = total + v
    return total / len(values)


def compute_std(values):
    n = len(values)
    if n < 2:
        return 0.0
    m = compute_mean(values)
    total = 0.0
    for v in values:
        total = total + (v - m) ** 2
    return math.sqrt(total / (n - 1))


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


def min_max_normalize_list(values):
    mn = min(values)
    mx = max(values)
    result = []
    for v in values:
        if mx == mn:
            result.append(0.0)
        else:
            result.append((v - mn) / (mx - mn))
    return result, mn, mx


def apply_norm(value, mn, mx):
    if mx == mn:
        return 0.0
    return (value - mn) / (mx - mn)


def euclidean_distance(a, b):
    total = 0.0
    for i in range(len(a)):
        total = total + (a[i] - b[i]) ** 2
    return math.sqrt(total)


def get_all_items(customers):
    item_set = []
    for c in customers:
        for item in c["Items"]:
            if item not in item_set:
                item_set.append(item)
    item_set.sort()
    return item_set


def frozenset_to_str(fs):
    parts = sorted(list(fs))
    return "{" + ", ".join(parts) + "}"


def set_support(itemset, transactions):
    count = 0
    for t in transactions:
        if itemset.issubset(t):
            count = count + 1
    return count


# ===== SECTION 5: CORE ANALYSIS =====

def part_a_descriptive(customers):
    """Ch2/Ch3: Univariate stats and correlation matrix."""
    col_data = {}
    for feat in NUMERIC_FEATURES:
        col_data[feat] = []
        for c in customers:
            col_data[feat].append(c[feat])

    stats = {}
    for feat in NUMERIC_FEATURES:
        vals = col_data[feat]
        stats[feat] = {
            "mean": round(compute_mean(vals), 2),
            "std":  round(compute_std(vals), 2),
            "min":  min(vals),
            "max":  max(vals),
        }

    corr = {}
    for f1 in NUMERIC_FEATURES:
        corr[f1] = {}
        for f2 in NUMERIC_FEATURES:
            corr[f1][f2] = round(pearson_r(col_data[f1], col_data[f2]), 3)

    return stats, corr, col_data


def part_b_normalize(customers):
    """Ch4: Min-max normalize Age, Visits, Spend to [0,1]."""
    norm_params = {}
    for feat in NUMERIC_FEATURES:
        vals = []
        for c in customers:
            vals.append(c[feat])
        _, mn, mx = min_max_normalize_list(vals)
        norm_params[feat] = (mn, mx)

    norm_customers = []
    for c in customers:
        nc = {"id": c["id"], "Items": c["Items"]}
        for feat in NUMERIC_FEATURES:
            mn, mx = norm_params[feat]
            nc[feat] = apply_norm(c[feat], mn, mx)
        norm_customers.append(nc)
    return norm_customers, norm_params


def part_c_apriori(customers):
    """Ch6: Apriori with min_support=5 (25%), min_confidence=0.5."""
    transactions = []
    for c in customers:
        transactions.append(frozenset(c["Items"]))

    all_items = get_all_items(customers)
    n = len(transactions)

    # Generate frequent 1-itemsets
    freq_1 = []
    for item in all_items:
        s = set_support(frozenset([item]), transactions)
        if s >= MIN_SUPPORT_COUNT:
            freq_1.append((frozenset([item]), s))

    all_frequent = list(freq_1)
    prev_level = freq_1

    # Generate frequent k-itemsets from frequent (k-1)-itemsets
    k = 2
    while len(prev_level) > 0:
        # Generate candidates: union of pairs from prev level that share k-2 items
        candidates = []
        prev_items = [fs for fs, _ in prev_level]
        for i in range(len(prev_items)):
            for j in range(i + 1, len(prev_items)):
                union = prev_items[i].union(prev_items[j])
                if len(union) == k:
                    if union not in candidates:
                        candidates.append(union)

        # Prune: every (k-1) subset must be frequent
        freq_level = []
        prev_item_sets = [fs for fs, _ in prev_level]
        for candidate in candidates:
            candidate_list = sorted(list(candidate))
            all_subsets_frequent = True
            for idx in range(len(candidate_list)):
                subset = frozenset(candidate_list[:idx] + candidate_list[idx+1:])
                if subset not in prev_item_sets:
                    all_subsets_frequent = False
                    break
            if all_subsets_frequent:
                s = set_support(candidate, transactions)
                if s >= MIN_SUPPORT_COUNT:
                    freq_level.append((candidate, s))

        all_frequent = all_frequent + freq_level
        prev_level = freq_level
        k = k + 1

    # Generate association rules
    rules = []
    for itemset, supp in all_frequent:
        if len(itemset) < 2:
            continue
        item_list = sorted(list(itemset))
        # Generate all non-empty proper subsets as antecedents
        subsets = []
        for mask in range(1, 2 ** len(item_list) - 1):
            subset = []
            for bit in range(len(item_list)):
                if mask & (1 << bit):
                    subset.append(item_list[bit])
            subsets.append(frozenset(subset))

        for antecedent in subsets:
            consequent = itemset - antecedent
            if len(consequent) == 0:
                continue
            ant_supp = set_support(antecedent, transactions)
            if ant_supp == 0:
                continue
            conf = supp / ant_supp
            if conf >= MIN_CONFIDENCE:
                cons_supp = set_support(consequent, transactions)
                lift = conf / (cons_supp / n) if cons_supp > 0 else 0.0
                rules.append({
                    "antecedent": antecedent,
                    "consequent": consequent,
                    "support":    supp,
                    "confidence": round(conf, 3),
                    "lift":       round(lift, 3),
                })

    # Sort by lift descending
    for i in range(len(rules)):
        for j in range(i + 1, len(rules)):
            if rules[j]["lift"] > rules[i]["lift"]:
                rules[i], rules[j] = rules[j], rules[i]

    return all_frequent, rules, n


def part_d_kmeans(norm_customers):
    """Ch5: K-means K=3 on normalized Age, Visits, Spend."""
    # Initialize centroids from first 3 customers
    centroids = []
    for i in range(K_CLUSTERS):
        c = norm_customers[i]
        centroids.append([c[feat] for feat in NUMERIC_FEATURES])

    n = len(norm_customers)
    assignments = [0] * n

    for iteration in range(K_MAX_ITER):
        new_assignments = []
        for c in norm_customers:
            vec = [c[feat] for feat in NUMERIC_FEATURES]
            best_k = 0
            best_d = euclidean_distance(vec, centroids[0])
            for k in range(1, K_CLUSTERS):
                d = euclidean_distance(vec, centroids[k])
                if d < best_d:
                    best_d = d
                    best_k = k
            new_assignments.append(best_k)

        changed = False
        for i in range(n):
            if assignments[i] != new_assignments[i]:
                changed = True
                break
        assignments = new_assignments

        if not changed:
            break

        for k in range(K_CLUSTERS):
            members = []
            for i, c in enumerate(norm_customers):
                if assignments[i] == k:
                    members.append([c[feat] for feat in NUMERIC_FEATURES])
            if len(members) > 0:
                new_c = []
                for dim in range(len(NUMERIC_FEATURES)):
                    dim_vals = [m[dim] for m in members]
                    new_c.append(compute_mean(dim_vals))
                centroids[k] = new_c

    return assignments, centroids


def label_clusters(centroids, norm_params, assignments, customers):
    """Assign human-readable labels based on centroid values."""
    # De-normalize centroids for interpretable labeling
    denorm_centroids = []
    for centroid in centroids:
        dc = {}
        for i, feat in enumerate(NUMERIC_FEATURES):
            mn, mx = norm_params[feat]
            dc[feat] = round(centroid[i] * (mx - mn) + mn, 1)
        denorm_centroids.append(dc)

    # Sort clusters by Spend (ascending)
    cluster_order = sorted(range(K_CLUSTERS), key=lambda k: denorm_centroids[k]["Spend"])
    label_map = {}
    label_names = ["Young Low-Spend", "Regular Shoppers", "Loyal High-Spend"]
    for rank, k in enumerate(cluster_order):
        label_map[k] = label_names[rank]

    # Compute original-scale mean per cluster per feature
    cluster_feature_means = {}
    for k in range(K_CLUSTERS):
        cluster_feature_means[k] = {}
        for feat in NUMERIC_FEATURES:
            vals = []
            for i, c in enumerate(customers):
                if assignments[i] == k:
                    vals.append(c[feat])
            if len(vals) > 0:
                cluster_feature_means[k][feat] = round(compute_mean(vals), 1)
            else:
                cluster_feature_means[k][feat] = 0.0

    return label_map, denorm_centroids, cluster_feature_means


# ===== SECTION 6: PRINTING / REPORTING =====

def print_separator(char="-", width=62):
    print(char * width)


def print_part_header(label, title):
    print("")
    print("=" * 62)
    print("  " + label + " -- " + title)
    print("=" * 62)


def print_part_a(stats, corr, col_data):
    print_part_header("PART A", "DESCRIPTIVE STATISTICS (Ch2/Ch3)")

    print("{:<12} {:>8} {:>8} {:>8} {:>8}".format("Column", "Mean", "Std", "Min", "Max"))
    print_separator("-", 48)
    for feat in NUMERIC_FEATURES:
        s = stats[feat]
        print("{:<12} {:>8.2f} {:>8.2f} {:>8} {:>8}".format(
            feat, s["mean"], s["std"], s["min"], s["max"]
        ))

    print("")
    print("  Correlation Matrix (Pearson r):")
    header = "{:<10}".format("")
    for feat in NUMERIC_FEATURES:
        header = header + " {:>10}".format(feat)
    print(header)
    print_separator("-", 42)
    for f1 in NUMERIC_FEATURES:
        row_str = "{:<10}".format(f1)
        for f2 in NUMERIC_FEATURES:
            row_str = row_str + " {:>10.3f}".format(corr[f1][f2])
        print(row_str)

    # ASCII scatter: Age (y-axis) vs Spend (x-axis)
    print("")
    print("  ASCII Scatter: Age (y) vs Spend (x)")
    print("  (each dot = one customer)")
    width = 50
    height = 20
    age_vals = col_data["Age"]
    spend_vals = col_data["Spend"]
    age_min = min(age_vals)
    age_max = max(age_vals)
    spend_min = min(spend_vals)
    spend_max = max(spend_vals)

    grid = []
    for row_i in range(height):
        grid.append([" "] * width)

    for i in range(len(CUSTOMERS)):
        age = age_vals[i]
        spend = spend_vals[i]
        if age_max > age_min:
            y = int((1.0 - (age - age_min) / (age_max - age_min)) * (height - 1))
        else:
            y = height // 2
        if spend_max > spend_min:
            x = int((spend - spend_min) / (spend_max - spend_min) * (width - 1))
        else:
            x = width // 2
        y = max(0, min(height - 1, y))
        x = max(0, min(width - 1, x))
        grid[y][x] = "*"

    print("  Age")
    print("  " + str(age_max) + " |" + "-" * width)
    for row_i in range(height):
        print("    |" + "".join(grid[row_i]))
    print("  " + str(age_min) + " |" + "-" * width)
    print("     " + str(spend_min) + " " + " " * (width // 2 - 5) + "Spend " + str(spend_max))


def print_part_b(norm_customers):
    print_part_header("PART B", "NORMALIZATION (Ch4) -- Min-Max to [0,1]")
    print("  First 3 customers (normalized):")
    for c in norm_customers[:3]:
        parts = []
        for feat in NUMERIC_FEATURES:
            parts.append(feat + "=" + str(round(c[feat], 3)))
        print("  " + c["id"] + ": " + ", ".join(parts))
    print("  ... (all 20 customers normalized)")


def print_part_c(frequent_sets, rules, n_transactions):
    print_part_header("PART C", "FREQUENT PATTERN MINING -- Apriori (Ch6)")
    print("  min_support=" + str(MIN_SUPPORT_COUNT) + "/" + str(n_transactions) +
          "=" + str(round(MIN_SUPPORT_COUNT / n_transactions, 2)) +
          "  min_confidence=" + str(MIN_CONFIDENCE))
    print("")
    print("  Frequent itemsets:")
    print_separator("-", 50)
    for itemset, supp in sorted(frequent_sets, key=lambda x: (-len(x[0]), -x[1])):
        label = frozenset_to_str(itemset)
        print("  " + label + ": support=" + str(supp) +
              " (" + str(round(supp / n_transactions, 2)) + ")")

    print("")
    print("  Association Rules (sorted by lift descending):")
    print_separator("-", 62)
    print("{:<30} {:>8} {:>12} {:>6}".format("Rule", "Support", "Confidence", "Lift"))
    print_separator("-", 62)
    for rule in rules:
        ant = frozenset_to_str(rule["antecedent"])
        con = frozenset_to_str(rule["consequent"])
        rule_str = ant + " -> " + con
        if len(rule_str) > 29:
            rule_str = rule_str[:26] + "..."
        print("{:<30} {:>8} {:>12.3f} {:>6.3f}".format(
            rule_str, rule["support"], rule["confidence"], rule["lift"]
        ))


def print_part_d(assignments, label_map, denorm_centroids, cluster_feature_means, customers):
    print_part_header("PART D", "CUSTOMER SEGMENTATION -- K-Means K=3 (Ch5)")
    for k in range(K_CLUSTERS):
        members = []
        for i, c in enumerate(customers):
            if assignments[i] == k:
                members.append(c["id"])
        label = label_map[k]
        print("  Cluster " + str(k) + " (" + label + "): " + ", ".join(members))

    print("")
    print("  Cluster mean profiles (original scale):")
    print("{:<5} {:<22} {:>6} {:>8} {:>8}".format(
        "K", "Label", "Age", "Visits", "Spend"
    ))
    print_separator("-", 52)
    for k in range(K_CLUSTERS):
        m = cluster_feature_means[k]
        print("{:<5} {:<22} {:>6.1f} {:>8.1f} {:>8.1f}".format(
            str(k), label_map[k], m["Age"], m["Visits"], m["Spend"]
        ))


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


def save_results(filename, lines):
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


# ===== SECTION 8: MAIN =====

def main():
    print("=" * 62)
    print("  MARKET BASKET & CUSTOMER SEGMENTATION")
    print("  Chapters: Ch2, Ch3, Ch4, Ch5, Ch6")
    print("=" * 62)

    # Part A: Descriptive statistics
    stats, corr, col_data = part_a_descriptive(CUSTOMERS)
    print_part_a(stats, corr, col_data)

    # Part B: Normalize
    norm_customers, norm_params = part_b_normalize(CUSTOMERS)
    print_part_b(norm_customers)

    # Part C: Apriori
    frequent_sets, rules, n_transactions = part_c_apriori(CUSTOMERS)
    print_part_c(frequent_sets, rules, n_transactions)

    # Part D: K-means
    assignments, centroids = part_d_kmeans(norm_customers)
    label_map, denorm_centroids, cluster_feature_means = label_clusters(
        centroids, norm_params, assignments, CUSTOMERS
    )
    print_part_d(assignments, label_map, denorm_centroids, cluster_feature_means, CUSTOMERS)

    print("")
    print("Done.")


if __name__ == "__main__":
    main()
