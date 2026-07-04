# =============================================================================
# SECTION 1: IMPORTS AND CONFIGURATION
# =============================================================================
import csv
import os
import math


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


def get_friends_dataset():
    """
    Return the Friends Food dataset as a column-oriented dict.
    Target: Company (good/bad)
    Features: Food, Distance (Age omitted for clarity — categorical focus)
    """
    columns = {
        "Food":     ["chinese", "italian", "italian", "burgers", "chinese",
                     "chinese", "burgers", "chinese", "italian"],
        "Distance": ["close", "very_close", "close", "far", "very_far",
                     "too_far", "very_far", "close", "far"],
        "Age":      ["51", "43", "82", "23", "46", "29", "42", "38", "31"],
        "Company":  ["good", "good", "good", "bad", "good",
                     "bad", "good", "bad", "good"],
    }
    return columns, 9


# =============================================================================
# SECTION 3: IMPURITY MEASURES
# =============================================================================

def compute_entropy(labels):
    """
    Compute the entropy H(S) of a list of class labels.

    H(S) = -sum over classes i: p_i * log2(p_i)

    Parameters
    ----------
    labels : list of strings — class labels

    Returns
    -------
    float — entropy value in [0, log2(n_classes)]
    """
    if len(labels) == 0:
        return 0.0

    # Count occurrences of each class
    counts = {}
    for label in labels:
        if label not in counts:
            counts[label] = 0
        counts[label] = counts[label] + 1

    n = len(labels)
    entropy = 0.0
    for label, count in counts.items():
        p = count / n
        if p > 0:
            # log2(p) is negative for 0 < p < 1, so we negate
            entropy = entropy - p * math.log2(p)

    return entropy


def compute_gini(labels):
    """
    Compute the Gini impurity of a list of class labels.

    Gini(S) = 1 - sum over classes i: p_i^2

    Parameters
    ----------
    labels : list of strings

    Returns
    -------
    float — Gini impurity in [0, 1 - 1/n_classes]
    """
    if len(labels) == 0:
        return 0.0

    counts = {}
    for label in labels:
        if label not in counts:
            counts[label] = 0
        counts[label] = counts[label] + 1

    n = len(labels)
    sum_sq = 0.0
    for label, count in counts.items():
        p = count / n
        sum_sq = sum_sq + p * p

    return 1.0 - sum_sq


def compute_information_gain(labels, attribute_values):
    """
    Compute the Information Gain of splitting labels by the given attribute values.

    IG(S, A) = H(S) - sum_v (|S_v| / |S|) * H(S_v)

    Parameters
    ----------
    labels           : list of strings — class labels
    attribute_values : list of strings — corresponding attribute values (same length as labels)

    Returns
    -------
    float — information gain
    """
    parent_entropy = compute_entropy(labels)

    # Group labels by attribute value
    groups = {}
    for i in range(len(labels)):
        val = attribute_values[i]
        if val not in groups:
            groups[val] = []
        groups[val].append(labels[i])

    n = len(labels)
    weighted_entropy = 0.0
    for val, group_labels in groups.items():
        weight = len(group_labels) / n
        weighted_entropy = weighted_entropy + weight * compute_entropy(group_labels)

    return parent_entropy - weighted_entropy


def compute_gain_ratio(labels, attribute_values):
    """
    Compute the Gain Ratio of splitting labels by the given attribute values.

    GR(S, A) = IG(S, A) / SplitInfo(S, A)
    SplitInfo = -sum_v (|S_v|/|S|) * log2(|S_v|/|S|)

    Parameters
    ----------
    labels           : list of strings
    attribute_values : list of strings

    Returns
    -------
    float — gain ratio
    """
    ig = compute_information_gain(labels, attribute_values)

    # Compute SplitInfo
    value_counts = {}
    for val in attribute_values:
        if val not in value_counts:
            value_counts[val] = 0
        value_counts[val] = value_counts[val] + 1

    n = len(attribute_values)
    split_info = 0.0
    for val, count in value_counts.items():
        p = count / n
        if p > 0:
            split_info = split_info - p * math.log2(p)

    if split_info == 0:
        return 0.0

    return ig / split_info


def compute_gini_split(labels, attribute_values):
    """
    Compute the weighted Gini impurity after splitting by the given attribute.

    Gini_split(S, A) = sum_v (|S_v| / |S|) * Gini(S_v)

    Parameters
    ----------
    labels           : list of strings
    attribute_values : list of strings

    Returns
    -------
    float — weighted Gini (lower is better for CART)
    """
    groups = {}
    for i in range(len(labels)):
        val = attribute_values[i]
        if val not in groups:
            groups[val] = []
        groups[val].append(labels[i])

    n = len(labels)
    weighted_gini = 0.0
    for val, group_labels in groups.items():
        weight = len(group_labels) / n
        weighted_gini = weighted_gini + weight * compute_gini(group_labels)

    return weighted_gini


# =============================================================================
# SECTION 4: BEST SPLIT SELECTION
# =============================================================================

def find_best_split(columns, target_col, feature_cols, criterion="info_gain"):
    """
    Find the best attribute to split on using the specified criterion.

    Parameters
    ----------
    columns     : dict — column-oriented data
    target_col  : str — name of the target/class column
    feature_cols: list of str — candidate feature column names
    criterion   : str — "info_gain", "gain_ratio", or "gini"

    Returns
    -------
    (best_feature, best_score)
    best_feature : str — name of the best attribute
    best_score   : float — score for the best attribute
    """
    labels = columns[target_col]

    best_feature = None
    best_score = None

    for feature in feature_cols:
        values = columns[feature]

        if criterion == "info_gain":
            score = compute_information_gain(labels, values)
            # Higher is better
            if best_score is None or score > best_score:
                best_score = score
                best_feature = feature

        elif criterion == "gain_ratio":
            score = compute_gain_ratio(labels, values)
            # Higher is better
            if best_score is None or score > best_score:
                best_score = score
                best_feature = feature

        elif criterion == "gini":
            score = compute_gini_split(labels, values)
            # Lower is better
            if best_score is None or score < best_score:
                best_score = score
                best_feature = feature

    return best_feature, best_score


# =============================================================================
# SECTION 5: TREE CONSTRUCTION
# =============================================================================

def majority_class(labels):
    """Return the most common class label. Ties broken alphabetically."""
    counts = {}
    for label in labels:
        if label not in counts:
            counts[label] = 0
        counts[label] = counts[label] + 1
    # Sort by count descending, then alphabetically for tie-breaking
    sorted_labels = sorted(counts.keys(), key=lambda x: (-counts[x], x))
    return sorted_labels[0]


def build_tree(columns, target_col, feature_cols, criterion="info_gain",
               max_depth=None, min_samples=1, depth=0):
    """
    Build a decision tree recursively (ID3-style).

    Parameters
    ----------
    columns      : dict — column-oriented data (subset of rows)
    target_col   : str — target column name
    feature_cols : list of str — available features to split on
    criterion    : str — "info_gain", "gain_ratio", or "gini"
    max_depth    : int or None — maximum tree depth
    min_samples  : int — minimum samples to split a node
    depth        : int — current depth (used internally)

    Returns
    -------
    dict representing the tree node:
      {"type": "leaf", "class": c}
      {"type": "node", "feature": f, "branches": {value: subtree, ...}, "majority": c}
    """
    labels = columns[target_col]
    n = len(labels)

    # --- Stopping Condition 1: all same class ---
    unique_classes = set(labels)
    if len(unique_classes) == 1:
        return {"type": "leaf", "class": labels[0]}

    # --- Stopping Condition 2: no features left ---
    if len(feature_cols) == 0:
        return {"type": "leaf", "class": majority_class(labels)}

    # --- Stopping Condition 3: too few samples ---
    if n <= min_samples:
        return {"type": "leaf", "class": majority_class(labels)}

    # --- Stopping Condition 4: max depth reached ---
    if max_depth is not None and depth >= max_depth:
        return {"type": "leaf", "class": majority_class(labels)}

    # --- Find best split ---
    best_feature, best_score = find_best_split(columns, target_col, feature_cols, criterion)

    if best_feature is None:
        return {"type": "leaf", "class": majority_class(labels)}

    # --- Build internal node ---
    node = {
        "type": "node",
        "feature": best_feature,
        "score": best_score,
        "majority": majority_class(labels),
        "branches": {}
    }

    # Get all unique values of the best feature
    feature_values = columns[best_feature]
    unique_values = sorted(set(feature_values))

    remaining_features = [f for f in feature_cols if f != best_feature]

    for val in unique_values:
        # Get indices where this feature has value 'val'
        indices = []
        for i in range(n):
            if feature_values[i] == val:
                indices.append(i)

        if len(indices) == 0:
            # No examples with this value -> leaf with majority class
            node["branches"][val] = {"type": "leaf", "class": majority_class(labels)}
        else:
            # Build subset of columns for this branch
            subset_columns = {}
            for col_name in columns:
                subset_columns[col_name] = [columns[col_name][i] for i in indices]

            # Recurse
            node["branches"][val] = build_tree(
                subset_columns, target_col, remaining_features,
                criterion, max_depth, min_samples, depth + 1
            )

    return node


# =============================================================================
# SECTION 6: PREDICTION
# =============================================================================

def predict_one(tree, sample_row):
    """
    Predict the class for a single sample by traversing the tree.

    Parameters
    ----------
    tree       : dict — decision tree (as returned by build_tree)
    sample_row : dict — maps feature name -> feature value

    Returns
    -------
    str — predicted class label
    """
    current_node = tree

    while current_node["type"] == "node":
        feature = current_node["feature"]
        value = sample_row.get(feature, None)

        if value is None or value not in current_node["branches"]:
            # Unknown value — use majority class at this node
            return current_node["majority"]

        current_node = current_node["branches"][value]

    # Reached a leaf node
    return current_node["class"]


def predict_all(tree, columns, feature_cols):
    """
    Predict classes for all rows in the dataset.

    Parameters
    ----------
    tree         : dict — decision tree
    columns      : dict — column-oriented data
    feature_cols : list of str — feature column names

    Returns
    -------
    list of str — predicted class for each row
    """
    n = len(columns[feature_cols[0]])
    predictions = []
    for i in range(n):
        # Build a sample dict for row i
        sample = {}
        for col in feature_cols:
            sample[col] = columns[col][i]
        predictions.append(predict_one(tree, sample))
    return predictions


# =============================================================================
# SECTION 7: VISUALIZATION
# =============================================================================

def print_tree_ascii(tree, indent=0, branch_label=""):
    """
    Print an ASCII visualization of the decision tree.

    Parameters
    ----------
    tree         : dict — decision tree node
    indent       : int — current indentation level
    branch_label : str — label for the branch leading to this node
    """
    prefix = "  " * indent

    if branch_label:
        print("{}|-- [{}]".format(prefix, branch_label))
        prefix = "  " * (indent + 1)

    if tree["type"] == "leaf":
        print("{}PREDICT: {}".format(prefix, tree["class"]))
    else:
        feature = tree["feature"]
        score = tree.get("score", 0)
        print("{}SPLIT on '{}' (score={:.4f})".format(prefix, feature, score))

        for val in sorted(tree["branches"].keys()):
            print_tree_ascii(tree["branches"][val], indent + 1, branch_label="{}={}".format(feature, val))


def print_impurity_table(columns, target_col, feature_cols):
    """
    Print a table comparing all three impurity measures for each feature.
    """
    labels = columns[target_col]
    print("")
    print("=" * 70)
    print("Impurity Measures for Each Feature")
    print("=" * 70)
    print("{:<15} {:>12} {:>12} {:>12}".format(
        "Feature", "InfoGain", "GainRatio", "GiniSplit"))
    print("-" * 70)
    for feature in feature_cols:
        values = columns[feature]
        ig = compute_information_gain(labels, values)
        gr = compute_gain_ratio(labels, values)
        gs = compute_gini_split(labels, values)
        print("{:<15} {:>12.4f} {:>12.4f} {:>12.4f}".format(feature, ig, gr, gs))
    print("")
    print("Overall H(S) = {:.4f}".format(compute_entropy(labels)))
    print("Overall Gini = {:.4f}".format(compute_gini(labels)))
    print("=" * 70)


# =============================================================================
# SECTION 8: MAIN DEMO
# =============================================================================

def main():
    print("=" * 65)
    print("PROJECT 07-03-01: Decision Trees")
    print("Friends Food Dataset")
    print("=" * 65)

    # --- Load data ---
    columns, n = get_friends_dataset()
    target_col = "Company"
    feature_cols = ["Food", "Distance"]

    print("\nDataset:")
    print("-" * 55)
    print("{:<12} {:<12} {:<8} {}".format("Food", "Distance", "Age", "Company"))
    print("-" * 55)
    for i in range(n):
        print("{:<12} {:<12} {:<8} {}".format(
            columns["Food"][i], columns["Distance"][i],
            columns["Age"][i], columns["Company"][i]))

    # --- Impurity measures ---
    print_impurity_table(columns, target_col, feature_cols)

    # --- Build trees with different criteria ---
    criteria = ["info_gain", "gain_ratio", "gini"]

    for criterion in criteria:
        print("\n")
        print("=" * 65)
        print("Decision Tree — criterion: {}".format(criterion))
        print("=" * 65)

        tree = build_tree(columns, target_col, feature_cols, criterion=criterion)
        print_tree_ascii(tree)

        # Training accuracy
        predictions = predict_all(tree, columns, feature_cols)
        correct = 0
        for i in range(n):
            if predictions[i] == columns[target_col][i]:
                correct = correct + 1
        accuracy = correct / n
        print("\nTraining accuracy: {}/{} = {:.1f}%".format(correct, n, accuracy * 100))

    # --- Predict new examples ---
    print("\n" + "=" * 65)
    print("Predictions for New Examples (using info_gain tree)")
    print("=" * 65)

    tree = build_tree(columns, target_col, feature_cols, criterion="info_gain")

    new_examples = [
        {"Food": "chinese",  "Distance": "close",     "expected": "?"},
        {"Food": "italian",  "Distance": "very_far",  "expected": "?"},
        {"Food": "burgers",  "Distance": "far",       "expected": "?"},
        {"Food": "chinese",  "Distance": "too_far",   "expected": "?"},
        {"Food": "italian",  "Distance": "close",     "expected": "?"},
    ]

    print("{:<12} {:<12} -> {}".format("Food", "Distance", "Predicted Company"))
    print("-" * 45)
    for ex in new_examples:
        pred = predict_one(tree, ex)
        print("{:<12} {:<12} -> {}".format(ex["Food"], ex["Distance"], pred))

    # --- Manual step-by-step entropy calculation ---
    print("\n" + "=" * 65)
    print("Step-by-Step Entropy Calculation")
    print("=" * 65)

    labels = columns[target_col]
    counts = {}
    for label in labels:
        if label not in counts:
            counts[label] = 0
        counts[label] = counts[label] + 1

    print("\nOverall dataset (S):")
    for cls, cnt in sorted(counts.items()):
        p = cnt / n
        contribution = -p * math.log2(p)
        print("  Class '{}': count={}, p={:.3f}, -p*log2(p)={:.4f}".format(
            cls, cnt, p, contribution))
    print("  H(S) = {:.4f}".format(compute_entropy(labels)))

    print("\nSplit on Food:")
    food_values = columns["Food"]
    food_groups = {}
    for i in range(n):
        v = food_values[i]
        if v not in food_groups:
            food_groups[v] = []
        food_groups[v].append(labels[i])

    for val in sorted(food_groups.keys()):
        grp = food_groups[val]
        h = compute_entropy(grp)
        weight = len(grp) / n
        print("  {} ({}): H={:.4f}, weight={:.3f}, contribution={:.4f}".format(
            val, grp, h, weight, weight * h))

    ig_food = compute_information_gain(labels, food_values)
    print("  IG(S, Food) = {:.4f}".format(ig_food))

    print("\nSplit on Distance:")
    dist_values = columns["Distance"]
    dist_groups = {}
    for i in range(n):
        v = dist_values[i]
        if v not in dist_groups:
            dist_groups[v] = []
        dist_groups[v].append(labels[i])

    for val in sorted(dist_groups.keys()):
        grp = dist_groups[val]
        h = compute_entropy(grp)
        weight = len(grp) / n
        print("  {} ({}): H={:.4f}, weight={:.3f}, contribution={:.4f}".format(
            val, grp, h, weight, weight * h))

    ig_dist = compute_information_gain(labels, dist_values)
    print("  IG(S, Distance) = {:.4f}".format(ig_dist))

    winner = "Distance" if ig_dist > ig_food else "Food"
    print("\nBest first split: {} (IG={:.4f})".format(winner, max(ig_food, ig_dist)))

    print("\nDone.")


if __name__ == "__main__":
    main()
