# =============================================================================
# SECTION 1: IMPORTS AND CONFIGURATION
# =============================================================================
# Standard library only — no external packages needed.
import csv
import os
import itertools


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


def load_transactions(csv_file):
    """
    Load a CSV file where each row is a transaction.
    All non-empty cell values become items in that transaction.
    Returns a list of frozensets, one per transaction.
    """
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        transactions = []
        for row in reader:
            # Collect all non-empty values in the row
            items = []
            for cell in row:
                cell = cell.strip()
                if cell != "":
                    items.append(cell)
            if len(items) > 0:
                transactions.append(frozenset(items))
    return transactions


def get_cuisine_transactions():
    """
    Return the Friends Cuisine dataset as a list of frozensets.
    Hardcoded so the script runs without any CSV file.
    """
    raw = [
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
    transactions = []
    for row in raw:
        transactions.append(frozenset(row))
    return transactions


# =============================================================================
# SECTION 3: SUPPORT COMPUTATION
# =============================================================================

def compute_support(transactions, itemset):
    """
    Compute absolute and relative support for a given itemset.

    Parameters
    ----------
    transactions : list of frozensets
    itemset      : frozenset — the set of items to count

    Returns
    -------
    (absolute_count, relative_support) as (int, float)
    """
    count = 0
    for transaction in transactions:
        # Check if every item in itemset is in this transaction
        if itemset.issubset(transaction):
            count = count + 1
    relative = count / len(transactions)
    return count, relative


# =============================================================================
# SECTION 4: FREQUENT ITEMSET DISCOVERY — APRIORI ALGORITHM
# =============================================================================

def find_frequent_1itemsets(transactions, min_support):
    """
    Scan all transactions once to find all single-item frequent itemsets.

    Parameters
    ----------
    transactions : list of frozensets
    min_support  : int — minimum absolute support count

    Returns
    -------
    dict mapping frozenset -> count for all frequent 1-itemsets
    """
    # Count each individual item
    item_counts = {}
    for transaction in transactions:
        for item in transaction:
            key = frozenset([item])
            if key not in item_counts:
                item_counts[key] = 0
            item_counts[key] = item_counts[key] + 1

    # Keep only items with sufficient support
    frequent = {}
    for itemset, count in item_counts.items():
        if count >= min_support:
            frequent[itemset] = count

    return frequent


def generate_candidates(freq_itemsets, k):
    """
    Generate candidate k-itemsets by joining pairs of (k-1)-frequent itemsets.
    Two itemsets are joined when their union has exactly k items.

    Parameters
    ----------
    freq_itemsets : dict mapping frozenset -> count (all same size k-1)
    k             : int — desired candidate size

    Returns
    -------
    set of frozensets, each of size k
    """
    candidates = set()
    itemset_list = list(freq_itemsets.keys())

    # Try every pair of frequent (k-1)-itemsets
    for i in range(len(itemset_list)):
        for j in range(i + 1, len(itemset_list)):
            union = itemset_list[i] | itemset_list[j]
            # Only keep if the union has exactly k items
            if len(union) == k:
                candidates.add(union)

    return candidates


def prune_candidates(candidates, freq_itemsets_prev):
    """
    Prune candidates whose (k-1)-subsets are not all frequent.
    This applies the Apriori anti-monotone property.

    Parameters
    ----------
    candidates          : set of frozensets of size k
    freq_itemsets_prev  : dict of frequent (k-1)-itemsets

    Returns
    -------
    set of frozensets that pass the pruning check
    """
    pruned = set()
    k = None
    for c in candidates:
        k = len(c)
        break  # just need the size

    if k is None:
        return pruned

    for candidate in candidates:
        # Generate all (k-1)-subsets of this candidate
        all_subsets_frequent = True
        items_list = list(candidate)
        for i in range(len(items_list)):
            # Remove item i to get a (k-1)-subset
            subset_items = items_list[:i] + items_list[i+1:]
            subset = frozenset(subset_items)
            if subset not in freq_itemsets_prev:
                all_subsets_frequent = False
                break

        if all_subsets_frequent:
            pruned.add(candidate)

    return pruned


def apriori(transactions, min_support):
    """
    Run the full Apriori algorithm.

    Parameters
    ----------
    transactions : list of frozensets
    min_support  : int — minimum absolute support count

    Returns
    -------
    dict mapping frozenset -> count for all frequent itemsets of all sizes
    """
    all_frequent = {}

    # Step 1: find frequent 1-itemsets
    freq_k = find_frequent_1itemsets(transactions, min_support)
    all_frequent.update(freq_k)

    k = 2
    while len(freq_k) > 0:
        # Step 2a: generate candidates of size k
        candidates = generate_candidates(freq_k, k)

        # Step 2b: prune candidates using Apriori property
        candidates = prune_candidates(candidates, freq_k)

        # Step 2c: count support for remaining candidates
        freq_k = {}
        for candidate in candidates:
            count, _ = compute_support(transactions, candidate)
            if count >= min_support:
                freq_k[candidate] = count

        # Add this level's frequent itemsets to the results
        all_frequent.update(freq_k)
        k = k + 1

    return all_frequent


# =============================================================================
# SECTION 5: ASSOCIATION RULE GENERATION
# =============================================================================

def generate_association_rules(frequent_itemsets, transactions, min_confidence):
    """
    Generate all association rules from the frequent itemsets.

    For each frequent itemset F with |F| >= 2, try every non-empty proper
    subset X of F as antecedent. The consequent is F minus X.

    Parameters
    ----------
    frequent_itemsets : dict mapping frozenset -> count
    transactions      : list of frozensets (needed to compute support of subsets)
    min_confidence    : float in [0,1]

    Returns
    -------
    list of tuples: (antecedent, consequent, support, confidence, lift)
    """
    rules = []
    n = len(transactions)

    for itemset, itemset_count in frequent_itemsets.items():
        # Only itemsets with 2+ items can generate rules
        if len(itemset) < 2:
            continue

        itemset_support = itemset_count / n
        items = list(itemset)

        # Try all non-empty proper subsets as antecedent
        for size in range(1, len(items)):
            for antecedent_items in itertools.combinations(items, size):
                antecedent = frozenset(antecedent_items)
                consequent = itemset - antecedent

                # Get support of antecedent
                ant_count, ant_support = compute_support(transactions, antecedent)

                # Avoid division by zero
                if ant_count == 0:
                    continue

                # Compute confidence = support(X union Y) / support(X)
                confidence = itemset_count / ant_count

                if confidence >= min_confidence:
                    # Compute lift = confidence / support(Y)
                    cons_count, cons_support = compute_support(transactions, consequent)
                    if cons_support > 0:
                        lift = confidence / cons_support
                    else:
                        lift = 0.0

                    rules.append((antecedent, consequent, itemset_support, confidence, lift))

    return rules


# =============================================================================
# SECTION 6: DISPLAY / REPORTING FUNCTIONS
# =============================================================================

def print_frequent_itemsets(freq_itemsets, n_transactions):
    """
    Print a formatted table of all frequent itemsets with their support.

    Parameters
    ----------
    freq_itemsets  : dict mapping frozenset -> count
    n_transactions : int — total number of transactions
    """
    print("")
    print("=" * 65)
    print("FREQUENT ITEMSETS")
    print("=" * 65)
    print("{:<40} {:>8} {:>10}".format("Itemset", "Count", "Support%"))
    print("-" * 65)

    # Group by size for cleaner output
    size_groups = {}
    for itemset, count in freq_itemsets.items():
        s = len(itemset)
        if s not in size_groups:
            size_groups[s] = []
        size_groups[s].append((itemset, count))

    for size in sorted(size_groups.keys()):
        # Sort by count descending within each size group
        group = size_groups[size]
        sorted_group = sorted(group, key=lambda x: x[1], reverse=True)
        print("")
        print("  {}-itemsets:".format(size))
        for itemset, count in sorted_group:
            items_str = "{" + ", ".join(sorted(itemset)) + "}"
            rel_support = 100.0 * count / n_transactions
            print("  {:<38} {:>8} {:>9.1f}%".format(items_str, count, rel_support))

    print("")
    print("Total frequent itemsets found: {}".format(len(freq_itemsets)))
    print("=" * 65)


def print_association_rules(rules, n_transactions):
    """
    Print a formatted table of association rules sorted by lift (descending).

    Parameters
    ----------
    rules          : list of (antecedent, consequent, support, confidence, lift)
    n_transactions : int
    """
    print("")
    print("=" * 85)
    print("ASSOCIATION RULES  (sorted by lift)")
    print("=" * 85)
    print("{:<35} {:<2} {:<20} {:>8} {:>11} {:>6}".format(
        "Antecedent", "->", "Consequent", "Support%", "Confidence", "Lift"))
    print("-" * 85)

    # Sort by lift descending
    sorted_rules = sorted(rules, key=lambda x: x[4], reverse=True)

    for ant, cons, support, confidence, lift in sorted_rules:
        ant_str = "{" + ", ".join(sorted(ant)) + "}"
        cons_str = "{" + ", ".join(sorted(cons)) + "}"
        print("{:<35} ->  {:<20} {:>7.1f}% {:>10.3f} {:>6.3f}".format(
            ant_str, cons_str, support * 100, confidence, lift))

    print("")
    print("Total rules found: {}".format(len(rules)))
    print("=" * 85)


# =============================================================================
# SECTION 7: HELPER UTILITIES
# =============================================================================

def get_all_items(transactions):
    """Return a sorted list of all unique items across all transactions."""
    items = set()
    for transaction in transactions:
        for item in transaction:
            items.add(item)
    return sorted(items)


def summarize_transactions(transactions):
    """Print a brief summary of the transaction database."""
    all_items = get_all_items(transactions)
    print("")
    print("Transaction Database Summary")
    print("-" * 40)
    print("Total transactions : {}".format(len(transactions)))
    print("Unique items       : {}".format(len(all_items)))
    print("Items              : {}".format(", ".join(all_items)))
    avg_size = sum(len(t) for t in transactions) / len(transactions)
    print("Avg transaction size: {:.2f} items".format(avg_size))
    print("")


# =============================================================================
# SECTION 8: MAIN DEMO
# =============================================================================

def main():
    print("=" * 65)
    print("PROJECT 06-03-01: Itemsets and Association Rules")
    print("Apriori Algorithm — Friends Cuisine Dataset")
    print("=" * 65)

    # --- Load Data ---
    transactions = get_cuisine_transactions()
    print("\nFriends Cuisine Transactions:")
    print("-" * 40)
    names = ["Andrew", "Bernhard", "Carolina", "Dennis", "Eve",
             "Fred", "Gwyneth", "Hayden", "Irene", "James"]
    for i, t in enumerate(transactions):
        name = names[i] if i < len(names) else "T{}".format(i)
        print("  {:10s}: {}".format(name, ", ".join(sorted(t))))

    summarize_transactions(transactions)

    # --- Parameters ---
    min_support = 3
    min_confidence = 0.5
    n = len(transactions)

    print("Parameters:")
    print("  min_support    = {} ({}% relative)".format(min_support, 100 * min_support // n))
    print("  min_confidence = {}".format(min_confidence))

    # --- Run Apriori ---
    print("\nRunning Apriori algorithm...")
    frequent_itemsets = apriori(transactions, min_support)

    # --- Display Frequent Itemsets ---
    print_frequent_itemsets(frequent_itemsets, n)

    # --- Generate Rules ---
    print("\nGenerating association rules...")
    rules = generate_association_rules(frequent_itemsets, transactions, min_confidence)

    # --- Display Rules ---
    print_association_rules(rules, n)

    # --- Highlight Top Rules ---
    if len(rules) > 0:
        sorted_rules = sorted(rules, key=lambda x: x[4], reverse=True)
        top = sorted_rules[0]
        ant_str = "{" + ", ".join(sorted(top[0])) + "}"
        cons_str = "{" + ", ".join(sorted(top[1])) + "}"
        print("\nTop rule by lift:")
        print("  {} -> {}".format(ant_str, cons_str))
        print("  Support   : {:.1f}%".format(top[2] * 100))
        print("  Confidence: {:.3f}".format(top[3]))
        print("  Lift      : {:.3f}".format(top[4]))
        if top[4] > 1:
            print("  -> Lift > 1: positive correlation!")
        elif top[4] < 1:
            print("  -> Lift < 1: negative correlation.")
        else:
            print("  -> Lift = 1: independent items.")

    # --- Manual Example: Compute Specific Rule ---
    print("\n--- Manual Verification ---")
    x = frozenset(["Indian", "Oriental"])
    y = frozenset(["Mediterranean"])
    xy = x | y
    xy_count, xy_sup = compute_support(transactions, xy)
    x_count, x_sup = compute_support(transactions, x)
    y_count, y_sup = compute_support(transactions, y)
    if x_count > 0 and y_sup > 0:
        conf = xy_count / x_count
        lift = conf / y_sup
        print("Rule: {{Indian, Oriental}} -> {{Mediterranean}}")
        print("  Support(X union Y) = {}/{} = {:.1f}%".format(xy_count, n, xy_sup * 100))
        print("  Support(X)         = {}/{} = {:.1f}%".format(x_count, n, x_sup * 100))
        print("  Support(Y)         = {}/{} = {:.1f}%".format(y_count, n, y_sup * 100))
        print("  Confidence         = {}/{} = {:.3f}".format(xy_count, x_count, conf))
        print("  Lift               = {:.3f} / {:.3f} = {:.3f}".format(conf, y_sup, lift))

    print("\nDone.")


if __name__ == "__main__":
    main()
