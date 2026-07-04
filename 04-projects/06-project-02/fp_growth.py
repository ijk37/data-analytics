# =============================================================================
# SECTION 1: IMPORTS AND CONFIGURATION
# =============================================================================
import csv
import os


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
    return raw


# =============================================================================
# SECTION 3: FP-TREE NODE CLASS
# =============================================================================

class FPNode:
    """
    A single node in the FP-tree.

    Attributes
    ----------
    item      : str or None  — item name (None for the root)
    count     : int          — how many transactions pass through this node
    parent    : FPNode       — parent node
    children  : dict         — maps item name -> child FPNode
    node_link : FPNode       — next node with the same item (for header table traversal)
    """

    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.node_link = None

    def increment(self, count):
        """Increase the count of this node."""
        self.count = self.count + count


# =============================================================================
# SECTION 4: FP-TREE CONSTRUCTION
# =============================================================================

def count_items(transactions):
    """
    Count the frequency of each individual item across all transactions.

    Returns
    -------
    dict mapping item_name -> count
    """
    counts = {}
    for transaction in transactions:
        for item in transaction:
            if item not in counts:
                counts[item] = 0
            counts[item] = counts[item] + 1
    return counts


def build_fp_tree(transactions, min_support):
    """
    Build an FP-tree from a list of transactions.

    Step 1: Count all item frequencies and keep only frequent items.
    Step 2: For each transaction, sort items by frequency (descending),
            then insert the sorted transaction into the tree.

    Parameters
    ----------
    transactions : list of lists (each list = one transaction's items)
    min_support  : int — minimum absolute support count

    Returns
    -------
    (root_node, header_table)
    root_node    : FPNode — the root of the FP-tree (item=None)
    header_table : dict mapping item -> [count, first_node_link]
    """
    # Step 1: count items and filter by min_support
    item_counts = count_items(transactions)
    frequent_items = {}
    for item, cnt in item_counts.items():
        if cnt >= min_support:
            frequent_items[item] = cnt

    if len(frequent_items) == 0:
        return None, {}

    # Build header table: item -> [total_count, first_link_node]
    header_table = {}
    for item, cnt in frequent_items.items():
        header_table[item] = [cnt, None]

    # Step 2: create root node
    root = FPNode(None, 0, None)

    # Step 3: insert each transaction into the tree
    for transaction in transactions:
        # Keep only frequent items
        filtered = []
        for item in transaction:
            if item in frequent_items:
                filtered.append(item)

        if len(filtered) == 0:
            continue

        # Sort by support descending (ties broken alphabetically for consistency)
        filtered.sort(key=lambda x: (-frequent_items[x], x))

        # Insert sorted transaction into tree
        insert_transaction(root, filtered, header_table, count=1)

    return root, header_table


def insert_transaction(node, items, header_table, count):
    """
    Recursively insert a list of items (sorted) into the FP-tree.
    If the first item already exists as a child, increment its count.
    Otherwise, create a new child node and update the header table link.

    Parameters
    ----------
    node         : FPNode — current node (start with root)
    items        : list of strings — items to insert
    header_table : dict — to update node links
    count        : int — the count to add (usually 1)
    """
    if len(items) == 0:
        return

    first_item = items[0]
    rest = items[1:]

    if first_item in node.children:
        # Node already exists: increment its count
        node.children[first_item].increment(count)
    else:
        # Create a new node
        new_node = FPNode(first_item, count, node)
        node.children[first_item] = new_node

        # Update header table: add link from last node to this new node
        update_header(header_table, first_item, new_node)

    # Continue inserting the rest of the items
    insert_transaction(node.children[first_item], rest, header_table, count)


def update_header(header_table, item, target_node):
    """
    Update the node link in the header table so that all nodes with the
    same item are linked together (for traversal during mining).

    Parameters
    ----------
    header_table : dict — item -> [count, first_node]
    item         : str
    target_node  : FPNode — the new node to add to the linked list
    """
    if header_table[item][1] is None:
        # First node for this item
        header_table[item][1] = target_node
    else:
        # Follow the node link chain to the end
        current = header_table[item][1]
        while current.node_link is not None:
            current = current.node_link
        current.node_link = target_node


# =============================================================================
# SECTION 5: FP-GROWTH MINING
# =============================================================================

def find_prefix_path(node):
    """
    Find the prefix path leading to this node (not including the node itself).

    Returns a list of item names from the parent up to (not including) the root.
    """
    path = []
    current = node.parent
    while current.item is not None:  # stop at root
        path.append(current.item)
        current = current.parent
    return path


def mine_fp_tree(header_table, min_support, prefix, frequent_itemsets):
    """
    Recursively mine the FP-tree using the conditional pattern base approach.

    For each item in the header table (processed bottom-up by support):
      1. Combine item with current prefix -> new frequent itemset
      2. Find all prefix paths for this item (conditional pattern base)
      3. Build conditional FP-tree from these prefix paths
      4. Recurse on the conditional FP-tree

    Parameters
    ----------
    header_table      : dict item -> [count, first_node]
    min_support       : int
    prefix            : frozenset — current prefix itemset
    frequent_itemsets : dict — accumulates {frozenset: support_count}
    """
    # Sort items by support ascending (mine bottom-up)
    items_by_support = sorted(header_table.keys(), key=lambda x: header_table[x][0])

    for item in items_by_support:
        item_count = header_table[item][0]

        # This item combined with current prefix forms a new frequent itemset
        new_itemset = prefix | frozenset([item])
        frequent_itemsets[new_itemset] = item_count

        # Build conditional pattern base:
        # traverse all nodes with this item via node links
        conditional_patterns = []
        node = header_table[item][1]
        while node is not None:
            path = find_prefix_path(node)
            if len(path) > 0:
                conditional_patterns.append((path, node.count))
            node = node.node_link

        # Build conditional FP-tree from the conditional pattern base
        cond_tree, cond_header = build_fp_tree_from_patterns(conditional_patterns, min_support)

        # Recurse if the conditional tree is non-empty
        if cond_header is not None and len(cond_header) > 0:
            mine_fp_tree(cond_header, min_support, new_itemset, frequent_itemsets)


def build_fp_tree_from_patterns(patterns, min_support):
    """
    Build an FP-tree from a list of (path, count) pairs.
    Used for building conditional FP-trees during recursive mining.

    Parameters
    ----------
    patterns    : list of ([item, item, ...], count) tuples
    min_support : int

    Returns
    -------
    (root_node, header_table) or (None, {}) if empty
    """
    if len(patterns) == 0:
        return None, {}

    # Count item frequencies in the pattern base
    item_counts = {}
    for path, count in patterns:
        for item in path:
            if item not in item_counts:
                item_counts[item] = 0
            item_counts[item] = item_counts[item] + count

    # Keep only frequent items
    frequent_items = {}
    for item, cnt in item_counts.items():
        if cnt >= min_support:
            frequent_items[item] = cnt

    if len(frequent_items) == 0:
        return None, {}

    # Build header table
    header_table = {}
    for item, cnt in frequent_items.items():
        header_table[item] = [cnt, None]

    # Build tree
    root = FPNode(None, 0, None)
    for path, count in patterns:
        # Filter to frequent items only
        filtered = []
        for item in path:
            if item in frequent_items:
                filtered.append(item)

        if len(filtered) == 0:
            continue

        # Sort by frequency descending
        filtered.sort(key=lambda x: (-frequent_items[x], x))
        insert_transaction(root, filtered, header_table, count)

    return root, header_table


# =============================================================================
# SECTION 6: MAXIMAL AND CLOSED ITEMSETS
# =============================================================================

def find_maximal_itemsets(frequent_itemsets):
    """
    Find all maximal frequent itemsets.
    An itemset X is maximal if no superset of X is in frequent_itemsets.

    Parameters
    ----------
    frequent_itemsets : dict mapping frozenset -> count

    Returns
    -------
    dict mapping frozenset -> count for maximal frequent itemsets only
    """
    all_itemsets = list(frequent_itemsets.keys())
    maximal = {}

    for itemset in all_itemsets:
        is_maximal = True
        for other in all_itemsets:
            # Check if 'other' is a proper superset of 'itemset'
            if other != itemset and itemset.issubset(other):
                is_maximal = False
                break
        if is_maximal:
            maximal[itemset] = frequent_itemsets[itemset]

    return maximal


def find_closed_itemsets(frequent_itemsets, transactions):
    """
    Find all closed frequent itemsets.
    An itemset X is closed if no superset of X has the same support as X.

    Parameters
    ----------
    frequent_itemsets : dict mapping frozenset -> count
    transactions      : list of lists (original transactions)

    Returns
    -------
    dict mapping frozenset -> count for closed frequent itemsets only
    """
    # Convert transactions to frozensets for subset checking
    transaction_sets = []
    for t in transactions:
        transaction_sets.append(frozenset(t))

    all_itemsets = list(frequent_itemsets.keys())
    closed = {}

    for itemset in all_itemsets:
        itemset_count = frequent_itemsets[itemset]
        is_closed = True

        # Check all supersets in the frequent itemsets
        for other in all_itemsets:
            if other != itemset and itemset.issubset(other):
                # 'other' is a proper superset — does it have the same support?
                if frequent_itemsets[other] == itemset_count:
                    is_closed = False
                    break

        if is_closed:
            closed[itemset] = itemset_count

    return closed


# =============================================================================
# SECTION 7: VISUALIZATION AND DISPLAY
# =============================================================================

def print_fp_tree_ascii(node, header_table=None, indent=0):
    """
    Print an ASCII visualization of the FP-tree.

    Parameters
    ----------
    node         : FPNode — current node (start with root)
    header_table : dict (optional) — to show item totals at root
    indent       : int — current indentation level
    """
    if node.item is None:
        print("ROOT")
        if header_table is not None:
            print("  Header Table:")
            sorted_items = sorted(header_table.keys(), key=lambda x: -header_table[x][0])
            for item in sorted_items:
                print("    [{}] count={}".format(item, header_table[item][0]))
            print("")
    else:
        prefix = "  " * indent + "|-- "
        print("{}[{}] count={}".format(prefix, node.item, node.count))

    for child_item in sorted(node.children.keys()):
        print_fp_tree_ascii(node.children[child_item], indent=indent + 1)


def print_itemset_table(itemsets, title, n_transactions):
    """
    Print a formatted table of itemsets.

    Parameters
    ----------
    itemsets       : dict frozenset -> count
    title          : str
    n_transactions : int
    """
    print("")
    print("=" * 60)
    print(title)
    print("=" * 60)
    print("{:<38} {:>8} {:>8}".format("Itemset", "Count", "Support%"))
    print("-" * 60)

    sorted_items = sorted(itemsets.items(), key=lambda x: (-len(x[0]), -x[1]))
    for itemset, count in sorted_items:
        items_str = "{" + ", ".join(sorted(itemset)) + "}"
        rel = 100.0 * count / n_transactions
        print("{:<38} {:>8} {:>7.1f}%".format(items_str, count, rel))

    print("")
    print("Total: {}".format(len(itemsets)))
    print("=" * 60)


# =============================================================================
# SECTION 8: MAIN DEMO
# =============================================================================

def main():
    print("=" * 60)
    print("PROJECT 06-03-02: FP-Growth and Pattern Types")
    print("=" * 60)

    # --- Load data ---
    raw_transactions = get_cuisine_transactions()
    names = ["Andrew", "Bernhard", "Carolina", "Dennis", "Eve",
             "Fred", "Gwyneth", "Hayden", "Irene", "James"]

    print("\nTransactions:")
    print("-" * 40)
    for i, t in enumerate(raw_transactions):
        name = names[i] if i < len(names) else "T{}".format(i)
        print("  {:10s}: {}".format(name, ", ".join(sorted(t))))

    min_support = 3
    n = len(raw_transactions)
    print("\nmin_support = {} ({:.0f}%)".format(min_support, 100.0 * min_support / n))

    # --- Build FP-Tree ---
    print("\n--- Building FP-Tree ---")
    root, header_table = build_fp_tree(raw_transactions, min_support)

    if root is None:
        print("No frequent items found.")
        return

    print("\nFP-Tree Structure:")
    print("-" * 40)
    print_fp_tree_ascii(root, header_table)

    # --- Mine FP-Tree ---
    print("\n--- Mining FP-Tree ---")
    frequent_itemsets = {}
    mine_fp_tree(header_table, min_support, frozenset(), frequent_itemsets)

    print_itemset_table(frequent_itemsets, "All Frequent Itemsets (FP-Growth)", n)

    # --- Maximal Itemsets ---
    maximal = find_maximal_itemsets(frequent_itemsets)
    print_itemset_table(maximal, "Maximal Frequent Itemsets", n)

    # --- Closed Itemsets ---
    closed = find_closed_itemsets(frequent_itemsets, raw_transactions)
    print_itemset_table(closed, "Closed Frequent Itemsets", n)

    # --- Summary ---
    print("\n--- Summary ---")
    print("Total frequent itemsets : {}".format(len(frequent_itemsets)))
    print("Closed frequent         : {}".format(len(closed)))
    print("Maximal frequent        : {}".format(len(maximal)))
    print("")
    print("Relationship:")
    print("  Maximal ({}) is a subset of Closed ({}) is a subset of All ({})".format(
        len(maximal), len(closed), len(frequent_itemsets)))

    # --- Verify: compare with known result from Apriori ---
    print("\n--- Verification: Known Frequent Itemsets ---")
    expected = [
        frozenset(["Indian"]),
        frozenset(["Mediterranean"]),
        frozenset(["Oriental"]),
        frozenset(["Arabic"]),
        frozenset(["Indian", "Mediterranean"]),
        frozenset(["Indian", "Oriental"]),
        frozenset(["Mediterranean", "Oriental"]),
        frozenset(["Mediterranean", "Arabic"]),
        frozenset(["Indian", "Mediterranean", "Oriental"]),
    ]
    print("Expected frequent itemsets (from Apriori with min_sup=3):")
    for e in expected:
        in_result = e in frequent_itemsets
        items_str = "{" + ", ".join(sorted(e)) + "}"
        status = "FOUND" if in_result else "MISSING"
        print("  {:45s} {}".format(items_str, status))

    print("\nDone.")


if __name__ == "__main__":
    main()
