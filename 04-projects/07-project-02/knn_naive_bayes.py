# =============================================================================
# SECTION 1: IMPORTS AND CONFIGURATION
# =============================================================================
# Standard library only — no external packages needed.
import csv
import os
import math


# =============================================================================
# SECTION 2: DATA LOADING
# =============================================================================

def load_csv(csv_file):
    """
    Read a CSV file and return a column-oriented dictionary:
        { column_name: [value1, value2, ...], ... }

    Also returns the number of data rows (not counting the header).
    """
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # first row is automatically used as header
        rows = list(reader)

    if len(rows) == 0:
        raise ValueError("The CSV file is empty.")

    # Pivot from row-oriented to column-oriented
    # Before: rows = [{"Age": "25", "Name": "Alice"}, {"Age": "30", "Name": "Bob"}]
    # After:  columns = {"Age": ["25", "30"], "Name": ["Alice", "Bob"]}
    columns = {}
    for col_name in rows[0]:          # get column names from the first row
        columns[col_name] = []
        for row in rows:              # go through every data row
            columns[col_name].append(row[col_name])

    return columns, len(rows)


def get_friends_data():
    """
    Return the Friends classification dataset as parallel lists.
    Each index i represents one training example.

    Columns: Food, Age (numeric), Distance, Company (label)
    """
    # Raw data rows
    data = [
        ["chinese", 51, "close",      "good"],
        ["italian", 43, "very_close", "good"],
        ["italian", 82, "close",      "good"],
        ["burgers", 23, "far",        "bad"],
        ["chinese", 46, "very_far",   "good"],
        ["chinese", 29, "too_far",    "bad"],
        ["burgers", 42, "very_far",   "good"],
        ["chinese", 38, "close",      "bad"],
        ["italian", 31, "far",        "good"],
    ]
    # Separate each column into its own list
    food_col     = []
    age_col      = []
    distance_col = []
    label_col    = []
    for row in data:
        food_col.append(row[0])
        age_col.append(row[1])
        distance_col.append(row[2])
        label_col.append(row[3])
    return food_col, age_col, distance_col, label_col


# =============================================================================
# SECTION 3: k-NN HELPER FUNCTIONS
# =============================================================================

def normalize_list(values):
    """
    Apply Min-Max normalization to a list of numeric values.
    Each value is scaled to the range [0, 1]:
        x_norm = (x - x_min) / (x_max - x_min)

    Parameters
    ----------
    values : list of numbers

    Returns
    -------
    list of floats in [0, 1]
    """
    # Find the minimum and maximum in the list
    min_val = values[0]
    max_val = values[0]
    for v in values:
        if v < min_val:
            min_val = v
        if v > max_val:
            max_val = v

    # Avoid division by zero if all values are equal
    if max_val == min_val:
        # All values are the same -> normalized to 0
        result = []
        for v in values:
            result.append(0.0)
        return result

    # Apply normalization to each value
    result = []
    for v in values:
        normalized = (v - min_val) / (max_val - min_val)
        result.append(normalized)
    return result


def normalize_new_value(value, train_values):
    """
    Normalize a single new value using the min and max from the training data.
    This ensures the test point is scaled using the same reference as training.

    Parameters
    ----------
    value        : float — the new value to normalize
    train_values : list of floats — the original training values (before normalization)

    Returns
    -------
    float — normalized value
    """
    min_val = train_values[0]
    max_val = train_values[0]
    for v in train_values:
        if v < min_val:
            min_val = v
        if v > max_val:
            max_val = v

    if max_val == min_val:
        return 0.0

    return (value - min_val) / (max_val - min_val)


def euclidean_dist_numeric(row_a, row_b):
    """
    Compute Euclidean distance between two rows using only their numeric features.

    Parameters
    ----------
    row_a : list of floats (numeric features only)
    row_b : list of floats (numeric features only)

    Returns
    -------
    float — Euclidean distance
    """
    # Sum of squared differences
    sum_sq = 0.0
    for i in range(len(row_a)):
        diff = row_a[i] - row_b[i]
        sum_sq = sum_sq + diff * diff
    return math.sqrt(sum_sq)


def knn_classify(train_numeric, train_labels, new_numeric, k=3):
    """
    Classify a new point using k-Nearest Neighbor (k-NN).

    Steps:
      1. Compute Euclidean distance from new_point to each training point
      2. Sort by distance (ascending)
      3. Take the k nearest neighbors
      4. Return the most frequent class (majority vote)

    Parameters
    ----------
    train_numeric : list of lists — one list of numeric features per training point
    train_labels  : list of str — class label for each training point
    new_numeric   : list of floats — numeric features of the new point (normalized)
    k             : int — number of neighbors

    Returns
    -------
    str — predicted class label
    """
    # Step 1: Compute distance to each training point
    distances = []
    for i in range(len(train_numeric)):
        dist = euclidean_dist_numeric(train_numeric[i], new_numeric)
        distances.append((dist, train_labels[i], i))

    # Step 2: Sort by distance (ascending) — manual insertion sort
    for i in range(1, len(distances)):
        key = distances[i]
        j = i - 1
        while j >= 0 and distances[j][0] > key[0]:
            distances[j + 1] = distances[j]
            j = j - 1
        distances[j + 1] = key

    # Step 3: Take top-k neighbors
    neighbors = distances[:k]

    # Step 4: Count votes for each class
    vote_counts = {}
    for dist, label, idx in neighbors:
        if label not in vote_counts:
            vote_counts[label] = 0
        vote_counts[label] = vote_counts[label] + 1

    # Step 5: Find the class with most votes
    best_class = None
    best_count = -1
    for cls, count in vote_counts.items():
        if count > best_count:
            best_count = count
            best_class = cls

    return best_class, neighbors


# =============================================================================
# SECTION 4: NAIVE BAYES FUNCTIONS
# =============================================================================

def compute_priors(labels):
    """
    Compute the prior probability of each class:
        P(C) = count(C) / total_examples

    Parameters
    ----------
    labels : list of str — class label for each training example

    Returns
    -------
    dict {class_label: probability}
    """
    # Count occurrences of each class
    counts = {}
    for label in labels:
        if label not in counts:
            counts[label] = 0
        counts[label] = counts[label] + 1

    # Convert counts to probabilities
    total = len(labels)
    priors = {}
    for cls, count in counts.items():
        priors[cls] = count / total

    return priors


def get_distinct_values(col_values):
    """
    Return a sorted list of all distinct values in a column.

    Parameters
    ----------
    col_values : list of values

    Returns
    -------
    list of distinct values
    """
    seen = set()
    distinct = []
    for v in col_values:
        if v not in seen:
            seen.add(v)
            distinct.append(v)
    return sorted(distinct)


def compute_likelihoods(feature_cols, labels):
    """
    Compute likelihood tables for all features using Laplace smoothing:
        P(x_j = v | C) = (count(x_j=v in class C) + 1) / (count(C) + |distinct values of x_j|)

    Parameters
    ----------
    feature_cols : dict {col_name: list of values}  — categorical feature columns
    labels       : list of str — class labels (same length as each column)

    Returns
    -------
    Nested dict: {class_label: {col_name: {value: probability}}}
    """
    # Find all distinct classes
    all_classes = get_distinct_values(labels)

    # Count class sizes (used in Laplace denominator)
    class_counts = {}
    for cls in all_classes:
        class_counts[cls] = 0
    for label in labels:
        class_counts[label] = class_counts[label] + 1

    # Build likelihood table for each (class, feature, value) combination
    likelihoods = {}
    for cls in all_classes:
        likelihoods[cls] = {}

    for col_name, col_values in feature_cols.items():
        # Get all distinct values for this feature
        distinct_vals = get_distinct_values(col_values)
        n_distinct = len(distinct_vals)

        for cls in all_classes:
            likelihoods[cls][col_name] = {}

            # Count how often each value appears in this class
            val_counts = {}
            for v in distinct_vals:
                val_counts[v] = 0

            # Go through all training examples
            for i in range(len(col_values)):
                if labels[i] == cls:
                    val = col_values[i]
                    val_counts[val] = val_counts[val] + 1

            # Apply Laplace smoothing to get probabilities
            for v in distinct_vals:
                # (count + 1) / (class_total + number_of_distinct_values)
                prob = (val_counts[v] + 1) / (class_counts[cls] + n_distinct)
                likelihoods[cls][col_name][v] = prob

    return likelihoods, all_classes


def naive_bayes_classify(priors, likelihoods, all_classes, new_example, feature_names):
    """
    Classify a new example using Naive Bayes.

    Computes log-probability to avoid numeric underflow:
        log P(C|X) ~ log P(C) + sum_j log P(x_j | C)

    Parameters
    ----------
    priors        : dict {class: prior_probability}
    likelihoods   : nested dict {class: {feature: {value: probability}}}
    all_classes   : list of class labels
    new_example   : dict {feature_name: value}
    feature_names : list of feature names to use

    Returns
    -------
    (predicted_class, scores_dict)
    scores_dict maps each class to its log-score
    """
    scores = {}

    for cls in all_classes:
        # Start with log of prior
        log_score = math.log(priors[cls])

        # Add log-likelihood for each feature
        for feat in feature_names:
            val = new_example[feat]
            if feat in likelihoods[cls] and val in likelihoods[cls][feat]:
                log_score = log_score + math.log(likelihoods[cls][feat][val])
            else:
                # Unseen value: use smoothed probability with count=0
                # Approximate: 1 / (class_count + n_distinct)
                # Use a small fallback
                log_score = log_score + math.log(1e-6)

        scores[cls] = log_score

    # Find class with highest log-score
    best_class = None
    best_score = None
    for cls, score in scores.items():
        if best_score is None or score > best_score:
            best_score = score
            best_class = cls

    return best_class, scores


# =============================================================================
# SECTION 5: DISPLAY / REPORTING FUNCTIONS
# =============================================================================

def print_knn_result(new_example_label, new_numeric, neighbors, prediction, k):
    """
    Display the k-NN classification result in a readable format.

    Parameters
    ----------
    new_example_label : str — name or description of the new point
    new_numeric       : list of floats — normalized numeric features
    neighbors         : list of (distance, label, index) tuples
    prediction        : str — predicted class
    k                 : int
    """
    print("")
    print("  k-NN (k={}) for: {}".format(k, new_example_label))
    print("  Normalized features: {}".format(
        ", ".join("{:.3f}".format(v) for v in new_numeric)))
    print("  Top-{} neighbors:".format(k))
    for dist, label, idx in neighbors:
        print("    index={}, class={}, distance={:.4f}".format(idx, label, dist))
    print("  Prediction -> {}".format(prediction))


def print_nb_step_by_step(new_example, priors, likelihoods, all_classes, feature_names):
    """
    Show step-by-step Naive Bayes posterior computation for one example.

    Parameters
    ----------
    new_example   : dict {feature_name: value}
    priors        : dict {class: probability}
    likelihoods   : nested dict {class: {feature: {value: probability}}}
    all_classes   : list of class labels
    feature_names : list of feature names
    """
    print("")
    print("  Naive Bayes step-by-step calculation:")
    print("  New example: {}".format(
        ", ".join("{}={}".format(k, v) for k, v in new_example.items())))
    print("")

    scores = {}
    for cls in all_classes:
        print("  Class = {}:".format(cls))
        print("    P({}) = {:.4f}".format(cls, priors[cls]))

        running = priors[cls]
        for feat in feature_names:
            val = new_example[feat]
            if feat in likelihoods[cls] and val in likelihoods[cls][feat]:
                prob = likelihoods[cls][feat][val]
            else:
                prob = 1e-6
            print("    P({}={} | {}) = {:.4f}".format(feat, val, cls, prob))
            running = running * prob

        scores[cls] = running
        print("    Product = {:.6f}".format(running))
        print("")

    # Normalize to get proper probabilities
    total = sum(scores.values())
    print("  Normalized posteriors:")
    for cls in all_classes:
        if total > 0:
            posterior = scores[cls] / total
        else:
            posterior = 0.0
        print("    P({} | X) = {:.4f}".format(cls, posterior))

    best_class = max(scores, key=scores.get)
    print("")
    print("  Prediction -> {}".format(best_class))
    return best_class


# =============================================================================
# SECTION 6: CROSS-VALIDATION HELPERS
# =============================================================================

def leave_one_out_knn(ages, labels, k=3):
    """
    Evaluate k-NN using leave-one-out: for each training point,
    train on all others and predict that point.
    Returns accuracy as a float.

    Parameters
    ----------
    ages   : list of int — the one numeric feature (age)
    labels : list of str — class labels
    k      : int

    Returns
    -------
    float — accuracy
    """
    # Normalize all ages together
    norm_ages = normalize_list(ages)

    correct = 0
    for test_idx in range(len(ages)):
        # Build train set excluding test_idx
        train_numeric = []
        train_labels = []
        for i in range(len(ages)):
            if i != test_idx:
                train_numeric.append([norm_ages[i]])
                train_labels.append(labels[i])

        new_point = [norm_ages[test_idx]]
        pred, _ = knn_classify(train_numeric, train_labels, new_point, k)
        if pred == labels[test_idx]:
            correct = correct + 1

    return correct / len(ages)


# =============================================================================
# SECTION 7: ADDITIONAL UTILITIES
# =============================================================================

def print_training_data_table(food_col, age_col, distance_col, label_col):
    """Print the training dataset as a formatted table."""
    print("")
    print("Training Dataset:")
    print("-" * 55)
    print("{:<10} {:>5} {:<12} {}".format("Food", "Age", "Distance", "Company"))
    print("-" * 55)
    for i in range(len(food_col)):
        print("{:<10} {:>5} {:<12} {}".format(
            food_col[i], age_col[i], distance_col[i], label_col[i]))
    print("-" * 55)
    print("Total examples: {}".format(len(label_col)))


def print_section_header(title):
    """Print a section separator with a title."""
    print("")
    print("=" * 60)
    print(title)
    print("=" * 60)


# =============================================================================
# SECTION 8: MAIN DEMO
# =============================================================================

def main():
    print("=" * 60)
    print("PROJECT 07-03-02: k-NN and Naive Bayes")
    print("Friends Cuisine Classification Dataset")
    print("=" * 60)

    # --- Load Data ---
    food_col, age_col, distance_col, label_col = get_friends_data()
    print_training_data_table(food_col, age_col, distance_col, label_col)

    # ==========================================================
    # PART A: k-NEAREST NEIGHBOR
    # ==========================================================
    print_section_header("PART A: k-Nearest Neighbor (k-NN)")

    print("\nFor k-NN we use only the numeric 'Age' feature.")
    print("Other features (Food, Distance) are categorical and would need")
    print("one-hot encoding or a different distance metric.")

    # Normalize the Age column
    norm_ages = normalize_list(age_col)
    print("\nNormalized Age values (Min-Max scaling):")
    print("-" * 40)
    print("{:<10} {:>6} {:>10}".format("Person", "Age", "Norm.Age"))
    print("-" * 40)
    names = ["Andrew", "Bernhard", "Carolina", "Dennis", "Eve",
             "Fred", "Gwyneth", "Hayden", "Irene"]
    for i in range(len(age_col)):
        name = names[i] if i < len(names) else "P{}".format(i)
        print("{:<10} {:>6} {:>10.4f}".format(name, age_col[i], norm_ages[i]))

    # Build numeric training set (just normalized age as a 1D feature)
    train_numeric = []
    for age_norm in norm_ages:
        train_numeric.append([age_norm])

    # Define 2 test objects
    test_objects = [
        {"description": "Chinese food, age=40, close", "age": 40},
        {"description": "Italian food, age=65, very_close", "age": 65},
    ]

    print("\nTest objects (using Age feature only for k-NN):")
    for obj in test_objects:
        norm_age = normalize_new_value(obj["age"], age_col)
        obj["norm_age"] = norm_age
        print("  {} | raw_age={} | norm_age={:.4f}".format(
            obj["description"], obj["age"], norm_age))

    # Try k = 1, 3, 5
    print("\nPredictions for different values of k:")
    print("-" * 55)

    for obj in test_objects:
        new_numeric = [obj["norm_age"]]
        print("")
        print("  >> New point: {}".format(obj["description"]))
        for k_val in [1, 3, 5]:
            pred, neighbors = knn_classify(train_numeric, label_col, new_numeric, k=k_val)
            neighbor_classes = [lbl for _, lbl, _ in neighbors]
            print("     k={}: neighbors={} -> prediction={}".format(
                k_val, neighbor_classes, pred))

    # Detailed output for k=3 on first test object
    obj = test_objects[0]
    new_numeric = [obj["norm_age"]]
    pred, neighbors = knn_classify(train_numeric, label_col, new_numeric, k=3)
    print_knn_result(obj["description"], new_numeric, neighbors, pred, k=3)

    # Leave-one-out accuracy for different k values
    print("")
    print("Leave-one-out cross-validation accuracy (Age feature only):")
    print("-" * 40)
    for k_val in [1, 3, 5]:
        acc = leave_one_out_knn(age_col, label_col, k=k_val)
        print("  k={}: accuracy = {:.1f}%".format(k_val, acc * 100))

    # ==========================================================
    # PART B: NAIVE BAYES
    # ==========================================================
    print_section_header("PART B: Naive Bayes Classifier")

    print("\nFor Naive Bayes we use categorical features: Food and Distance.")
    print("(Age would require discretization; we use Food and Distance here.)")

    # Prepare feature columns for Naive Bayes
    feature_cols = {
        "Food": food_col,
        "Distance": distance_col,
    }
    feature_names = ["Food", "Distance"]

    # Compute priors and likelihoods
    priors = compute_priors(label_col)
    likelihoods, all_classes = compute_likelihoods(feature_cols, label_col)

    # Show prior probabilities
    print("\nPrior probabilities:")
    for cls, prob in priors.items():
        count = round(prob * len(label_col))
        print("  P({}) = {}/{} = {:.4f}".format(cls, count, len(label_col), prob))

    # Show likelihood tables
    print("\nLikelihood tables (with Laplace smoothing):")
    for feat in feature_names:
        print("\n  Feature: {}".format(feat))
        distinct_vals = get_distinct_values(feature_cols[feat])
        header = "  {:<14}".format("Value")
        for cls in all_classes:
            header = header + " {:>10}".format("P(v|{})".format(cls))
        print(header)
        print("  " + "-" * (14 + 12 * len(all_classes)))
        for v in distinct_vals:
            row_str = "  {:<14}".format(v)
            for cls in all_classes:
                if v in likelihoods[cls][feat]:
                    prob = likelihoods[cls][feat][v]
                else:
                    prob = 0.0
                row_str = row_str + " {:>10.4f}".format(prob)
            print(row_str)

    # Classify test objects using Naive Bayes
    nb_test_objects = [
        {"Food": "chinese", "Distance": "close"},
        {"Food": "italian", "Distance": "very_close"},
    ]

    print("\nNaive Bayes Predictions:")
    print("-" * 40)
    for obj in nb_test_objects:
        print("")
        pred, scores = naive_bayes_classify(priors, likelihoods, all_classes, obj, feature_names)
        print("  Example: {}".format(obj))
        for cls in all_classes:
            print("    log-score({}): {:.4f}".format(cls, scores[cls]))
        print("  Prediction -> {}".format(pred))

    # Step-by-step for one example
    print_section_header("Naive Bayes: Step-by-Step for {Food=chinese, Distance=close}")
    example = {"Food": "chinese", "Distance": "close"}
    print_nb_step_by_step(example, priors, likelihoods, all_classes, feature_names)

    print("\nDone.")


if __name__ == "__main__":
    main()
