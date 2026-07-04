# =============================================================================
# SECTION 1: IMPORTS AND CONFIGURATION
# =============================================================================
import csv
import os
import random
import itertools

# Try to import mlxtend; fall back to from-scratch if unavailable
MLXTEND_AVAILABLE = False
try:
    import pandas as pd
    from mlxtend.preprocessing import TransactionEncoder
    from mlxtend.frequent_patterns import apriori as mlxtend_apriori
    from mlxtend.frequent_patterns import association_rules as mlxtend_assoc_rules
    MLXTEND_AVAILABLE = True
except ImportError:
    pass


# =============================================================================
# SECTION 2: DATA LOADING
# =============================================================================

def load_csv(csv_file):
    """Load a CSV file and return a column-oriented dict and row count."""
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


def get_cuisine_transactions():
    """Return the Friends Cuisine dataset as a list of lists."""
    return [
        ["Indian", "Mediterranean"],
        ["Indian", "Oriental", "FastFood"],
        ["Indian", "Mediterranean", "Oriental"],
        ["Arabic", "Mediterranean"],
        ["Oriental"],
        ["Indian", "Mediterranean", "Oriental"],
        ["Arabic", "Mediterranean"],
        ["Indian", "Oriental", "FastFood"],
        ["Indian", "Mediterranean", "Oriental"],
        ["Arabic", "Mediterranean"],
    ]


def generate_synthetic_grocery(n_transactions=50, seed=42):
    """
    Generate a synthetic grocery dataset with n_transactions transactions.
    Items are drawn from a realistic grocery list with varying frequencies.

    Parameters
    ----------
    n_transactions : int
    seed           : int — random seed for reproducibility

    Returns
    -------
    list of lists (each list = items in one transaction)
    """
    random.seed(seed)

    # Grocery items with rough probability of appearing in a transaction
    item_probs = [
        ("Milk", 0.6),
        ("Bread", 0.55),
        ("Butter", 0.4),
        ("Eggs", 0.5),
        ("Cheese", 0.35),
        ("Yogurt", 0.3),
        ("Apple", 0.45),
        ("Banana", 0.4),
        ("Orange", 0.3),
        ("Chicken", 0.35),
        ("Beef", 0.25),
        ("Fish", 0.2),
        ("Rice", 0.4),
        ("Pasta", 0.35),
        ("Tomato", 0.45),
        ("Onion", 0.5),
        ("Potato", 0.4),
        ("Coffee", 0.4),
        ("Tea", 0.35),
        ("Juice", 0.3),
    ]

    transactions = []
    for i in range(n_transactions):
        transaction = []
        for item, prob in item_probs:
            if random.random() < prob:
                transaction.append(item)
        # Ensure at least one item
        if len(transaction) == 0:
            transaction.append(item_probs[0][0])
        transactions.append(transaction)

    return transactions


# =============================================================================
# SECTION 3: FROM-SCRATCH APRIORI (FALLBACK)
# =============================================================================
# This is a compact version of the Apriori from Project 01
# used when mlxtend is not installed.

def _compute_support(transactions, itemset):
    """Count how many transactions contain itemset."""
    count = 0
    for t in transactions:
        t_set = frozenset(t)
        if itemset.issubset(t_set):
            count = count + 1
    return count


def _apriori_scratch(transactions, min_support_count):
    """
    Run Apriori algorithm from scratch.
    Returns dict {frozenset: absolute_count}.
    """
    # Count all individual items
    item_counts = {}
    for transaction in transactions:
        for item in transaction:
            key = frozenset([item])
            if key not in item_counts:
                item_counts[key] = 0
            item_counts[key] = item_counts[key] + 1

    # Find frequent 1-itemsets
    freq_k = {}
    for itemset, count in item_counts.items():
        if count >= min_support_count:
            freq_k[itemset] = count

    all_frequent = dict(freq_k)
    k = 2

    while len(freq_k) > 0:
        # Generate candidates
        candidates = set()
        itemset_list = list(freq_k.keys())
        for i in range(len(itemset_list)):
            for j in range(i + 1, len(itemset_list)):
                union = itemset_list[i] | itemset_list[j]
                if len(union) == k:
                    candidates.add(union)

        # Prune: check all (k-1)-subsets are frequent
        pruned = set()
        for candidate in candidates:
            items_list = list(candidate)
            ok = True
            for i in range(len(items_list)):
                subset = frozenset(items_list[:i] + items_list[i+1:])
                if subset not in freq_k:
                    ok = False
                    break
            if ok:
                pruned.add(candidate)

        # Count support
        freq_k = {}
        for candidate in pruned:
            cnt = _compute_support(transactions, candidate)
            if cnt >= min_support_count:
                freq_k[candidate] = cnt

        all_frequent.update(freq_k)
        k = k + 1

    return all_frequent


def _generate_rules_scratch(frequent_itemsets, transactions, min_confidence):
    """Generate association rules from frequent itemsets (scratch version)."""
    n = len(transactions)
    rules = []

    for itemset, itemset_count in frequent_itemsets.items():
        if len(itemset) < 2:
            continue

        items = list(itemset)
        for size in range(1, len(items)):
            for ant_items in itertools.combinations(items, size):
                ant = frozenset(ant_items)
                cons = itemset - ant
                ant_count = _compute_support(transactions, ant)
                if ant_count == 0:
                    continue
                conf = itemset_count / ant_count
                if conf >= min_confidence:
                    cons_count = _compute_support(transactions, cons)
                    cons_sup = cons_count / n
                    lift = conf / cons_sup if cons_sup > 0 else 0.0
                    rules.append({
                        "antecedents": ant,
                        "consequents": cons,
                        "support": itemset_count / n,
                        "confidence": conf,
                        "lift": lift,
                    })
    return rules


# =============================================================================
# SECTION 4: MLXTEND-BASED MINING
# =============================================================================

def mine_with_mlxtend(transactions, min_support_relative, min_confidence):
    """
    Mine frequent itemsets and association rules using mlxtend.

    Parameters
    ----------
    transactions          : list of lists
    min_support_relative  : float — minimum relative support (e.g., 0.3)
    min_confidence        : float — minimum confidence for rules

    Returns
    -------
    (frequent_itemsets_df, rules_df) — pandas DataFrames
    """
    # Encode transactions as a binary matrix
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_array, columns=te.columns_)

    # Find frequent itemsets
    freq_df = mlxtend_apriori(df, min_support=min_support_relative, use_colnames=True)

    # Generate rules
    rules_df = mlxtend_assoc_rules(freq_df, metric="confidence", min_threshold=min_confidence)

    return freq_df, rules_df


def print_mlxtend_results(freq_df, rules_df, title=""):
    """Print mlxtend results in a readable format."""
    if title:
        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)

    print("\nFrequent Itemsets:")
    print("-" * 50)
    print("{:<40} {:>8}".format("Itemset", "Support%"))
    print("-" * 50)
    for _, row in freq_df.sort_values("support", ascending=False).iterrows():
        items_str = "{" + ", ".join(sorted(row["itemsets"])) + "}"
        print("{:<40} {:>7.1f}%".format(items_str, row["support"] * 100))

    print("\nAssociation Rules (sorted by lift):")
    print("-" * 80)
    print("{:<28} {:<2} {:<20} {:>8} {:>11} {:>6}".format(
        "Antecedent", "->", "Consequent", "Support%", "Confidence", "Lift"))
    print("-" * 80)
    for _, row in rules_df.sort_values("lift", ascending=False).iterrows():
        ant_str = "{" + ", ".join(sorted(row["antecedents"])) + "}"
        cons_str = "{" + ", ".join(sorted(row["consequents"])) + "}"
        print("{:<28} ->  {:<20} {:>7.1f}% {:>10.3f} {:>6.3f}".format(
            ant_str, cons_str, row["support"] * 100, row["confidence"], row["lift"]))

    print("\nTotal frequent itemsets: {}".format(len(freq_df)))
    print("Total rules: {}".format(len(rules_df)))


# =============================================================================
# SECTION 5: SCRATCH-BASED DISPLAY
# =============================================================================

def print_scratch_results(frequent_itemsets, rules, n_transactions, title=""):
    """Print from-scratch mining results."""
    if title:
        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)

    print("\nFrequent Itemsets:")
    print("-" * 50)
    print("{:<40} {:>8}".format("Itemset", "Support%"))
    print("-" * 50)
    sorted_items = sorted(frequent_itemsets.items(), key=lambda x: x[1], reverse=True)
    for itemset, count in sorted_items:
        items_str = "{" + ", ".join(sorted(itemset)) + "}"
        print("{:<40} {:>7.1f}%".format(items_str, 100.0 * count / n_transactions))

    print("\nAssociation Rules (sorted by lift):")
    print("-" * 80)
    print("{:<28} {:<2} {:<20} {:>8} {:>11} {:>6}".format(
        "Antecedent", "->", "Consequent", "Support%", "Confidence", "Lift"))
    print("-" * 80)
    sorted_rules = sorted(rules, key=lambda x: x["lift"], reverse=True)
    for r in sorted_rules:
        ant_str = "{" + ", ".join(sorted(r["antecedents"])) + "}"
        cons_str = "{" + ", ".join(sorted(r["consequents"])) + "}"
        print("{:<28} ->  {:<20} {:>7.1f}% {:>10.3f} {:>6.3f}".format(
            ant_str, cons_str, r["support"] * 100, r["confidence"], r["lift"]))

    print("\nTotal frequent itemsets: {}".format(len(frequent_itemsets)))
    print("Total rules: {}".format(len(rules)))


# =============================================================================
# SECTION 6: GROCERY DATASET ANALYSIS
# =============================================================================

def analyze_grocery_dataset(transactions, min_support_rel, min_confidence, method):
    """
    Analyze the synthetic grocery dataset.

    Parameters
    ----------
    transactions     : list of lists
    min_support_rel  : float
    min_confidence   : float
    method           : str — "mlxtend" or "scratch"
    """
    n = len(transactions)
    min_sup_count = max(1, int(min_support_rel * n))

    print("\n" + "=" * 60)
    print("Synthetic Grocery Dataset Analysis")
    print("=" * 60)
    print("Transactions: {}".format(n))
    print("min_support:    {} ({:.0f}%)".format(min_sup_count, min_support_rel * 100))
    print("min_confidence: {}".format(min_confidence))

    # Count item frequencies
    item_counts = {}
    for t in transactions:
        for item in t:
            if item not in item_counts:
                item_counts[item] = 0
            item_counts[item] = item_counts[item] + 1

    print("\nTop 10 most frequent items:")
    sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
    for item, cnt in sorted_items[:10]:
        print("  {:<15} count={:3d}  ({:.0f}%)".format(item, cnt, 100.0 * cnt / n))

    if method == "mlxtend":
        freq_df, rules_df = mine_with_mlxtend(transactions, min_support_rel, min_confidence)
        print("\nMlxtend found {} frequent itemsets and {} rules.".format(
            len(freq_df), len(rules_df)))
        if len(rules_df) > 0:
            top_rule = rules_df.sort_values("lift", ascending=False).iloc[0]
            ant = "{" + ", ".join(sorted(top_rule["antecedents"])) + "}"
            cons = "{" + ", ".join(sorted(top_rule["consequents"])) + "}"
            print("Top rule by lift: {} -> {}  lift={:.3f}".format(ant, cons, top_rule["lift"]))
    else:
        freq = _apriori_scratch(transactions, min_sup_count)
        rules = _generate_rules_scratch(freq, transactions, min_confidence)
        print("\nFrom-scratch found {} frequent itemsets and {} rules.".format(
            len(freq), len(rules)))
        if len(rules) > 0:
            top = sorted(rules, key=lambda x: x["lift"], reverse=True)[0]
            ant = "{" + ", ".join(sorted(top["antecedents"])) + "}"
            cons = "{" + ", ".join(sorted(top["consequents"])) + "}"
            print("Top rule by lift: {} -> {}  lift={:.3f}".format(ant, cons, top["lift"]))


# =============================================================================
# SECTION 7: UTILITY FUNCTIONS
# =============================================================================

def print_library_status():
    """Report which libraries are available."""
    print("\nLibrary Status:")
    print("-" * 40)
    if MLXTEND_AVAILABLE:
        print("  mlxtend  : AVAILABLE")
        import mlxtend
        print("  version  : {}".format(mlxtend.__version__))
    else:
        print("  mlxtend  : NOT INSTALLED")
        print("  -> Install with: pip install mlxtend pandas")
        print("  -> Falling back to from-scratch Apriori")
    print("")


def save_transactions_csv(transactions, filepath):
    """Save transactions to a CSV file (one transaction per row)."""
    max_items = max(len(t) for t in transactions)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for t in transactions:
            row = list(t) + [""] * (max_items - len(t))
            writer.writerow(row)
    print("Saved {} transactions to {}".format(len(transactions), filepath))


# =============================================================================
# SECTION 8: MAIN DEMO
# =============================================================================

def main():
    print("=" * 60)
    print("PROJECT 06-03-03: Pattern Mining with Libraries")
    print("=" * 60)

    print_library_status()

    # Parameters
    min_support_rel = 0.3     # 30% relative support
    min_support_count = 3     # absolute support for cuisine (10 transactions)
    min_confidence = 0.5

    # ---- Part A: Cuisine Dataset ----
    print("\n--- Part A: Friends Cuisine Dataset ---")
    cuisine_transactions = get_cuisine_transactions()
    n_cuisine = len(cuisine_transactions)
    print("Transactions: {}".format(n_cuisine))

    if MLXTEND_AVAILABLE:
        freq_df, rules_df = mine_with_mlxtend(
            cuisine_transactions, min_support_rel, min_confidence)
        print_mlxtend_results(freq_df, rules_df, title="Cuisine — mlxtend Results")
    else:
        print("\n(Using from-scratch Apriori — mlxtend not available)")
        freq = _apriori_scratch(cuisine_transactions, min_support_count)
        rules = _generate_rules_scratch(cuisine_transactions, freq, min_confidence)
        # Wait, correct call order
        rules = _generate_rules_scratch(freq, cuisine_transactions, min_confidence)
        print_scratch_results(freq, rules, n_cuisine, title="Cuisine — From-Scratch Results")

    # ---- Part B: Synthetic Grocery Dataset ----
    print("\n--- Part B: Synthetic Grocery Dataset (50 transactions) ---")
    grocery_transactions = generate_synthetic_grocery(n_transactions=50, seed=42)
    method = "mlxtend" if MLXTEND_AVAILABLE else "scratch"
    analyze_grocery_dataset(grocery_transactions, min_support_rel=0.4,
                            min_confidence=0.5, method=method)

    # ---- Part C: Save datasets to CSV ----
    print("\n--- Part C: Saving datasets to CSV ---")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cuisine_csv = os.path.join(base_dir, "cuisine_transactions.csv")
    grocery_csv = os.path.join(base_dir, "grocery_transactions.csv")
    save_transactions_csv(cuisine_transactions, cuisine_csv)
    save_transactions_csv(grocery_transactions, grocery_csv)

    # ---- Part D: Load from CSV and re-run ----
    print("\n--- Part D: Load from CSV and Verify ---")
    # Load cuisine from CSV
    loaded = []
    with open(cuisine_csv, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            items = [cell.strip() for cell in row if cell.strip() != ""]
            if len(items) > 0:
                loaded.append(items)
    print("Loaded {} transactions from CSV".format(len(loaded)))
    freq_loaded = _apriori_scratch(loaded, min_support_count)
    print("Frequent itemsets from CSV-loaded data: {}".format(len(freq_loaded)))
    expected = 9  # known from previous projects
    match = "OK" if len(freq_loaded) == expected else "MISMATCH (expected {})".format(expected)
    print("Match check: {}".format(match))

    print("\nDone.")


if __name__ == "__main__":
    main()
