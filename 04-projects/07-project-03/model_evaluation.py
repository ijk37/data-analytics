# =============================================================================
# SECTION 1: IMPORTS AND CONFIGURATION
# =============================================================================
# Standard library only — no external packages needed.
import csv
import os
import math
import random


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
    Return the Friends classification dataset as two parallel lists:
    feature rows (dicts) and labels.
    """
    data = [
        {"Food": "chinese", "Age_bin": "old",    "Distance": "close",      "Company": "good"},
        {"Food": "italian", "Age_bin": "middle",  "Distance": "very_close", "Company": "good"},
        {"Food": "italian", "Age_bin": "old",    "Distance": "close",      "Company": "good"},
        {"Food": "burgers", "Age_bin": "young",  "Distance": "far",        "Company": "bad"},
        {"Food": "chinese", "Age_bin": "middle",  "Distance": "very_far",   "Company": "good"},
        {"Food": "chinese", "Age_bin": "young",  "Distance": "too_far",    "Company": "bad"},
        {"Food": "burgers", "Age_bin": "middle",  "Distance": "very_far",   "Company": "good"},
        {"Food": "chinese", "Age_bin": "middle",  "Distance": "close",      "Company": "bad"},
        {"Food": "italian", "Age_bin": "young",  "Distance": "far",        "Company": "good"},
    ]
    rows = []
    labels = []
    for item in data:
        rows.append({k: v for k, v in item.items() if k != "Company"})
        labels.append(item["Company"])
    return rows, labels


# =============================================================================
# SECTION 3: CONFUSION MATRIX CONSTRUCTION
# =============================================================================

def build_confusion_matrix(true_labels, pred_labels):
    """
    Build a confusion matrix from two lists of labels.

    The matrix is stored as a nested dict:
        cm[true_class][pred_class] = count

    Parameters
    ----------
    true_labels : list of str — ground truth labels
    pred_labels : list of str — predicted labels (same length)

    Returns
    -------
    dict {true_class: {pred_class: count}}
    """
    # Gather all unique classes from both lists
    all_classes = set()
    for label in true_labels:
        all_classes.add(label)
    for label in pred_labels:
        all_classes.add(label)
    all_classes = sorted(all_classes)

    # Initialize matrix with zeros
    cm = {}
    for tc in all_classes:
        cm[tc] = {}
        for pc in all_classes:
            cm[tc][pc] = 0

    # Fill in the counts
    for i in range(len(true_labels)):
        true_c = true_labels[i]
        pred_c = pred_labels[i]
        # Make sure both classes are in the matrix
        if true_c not in cm:
            cm[true_c] = {}
            for pc in all_classes:
                cm[true_c][pc] = 0
        if pred_c not in cm[true_c]:
            cm[true_c][pred_c] = 0
        cm[true_c][pred_c] = cm[true_c][pred_c] + 1

    return cm


def get_classes_from_cm(cm):
    """Extract sorted list of class names from a confusion matrix dict."""
    classes = set()
    for true_c in cm:
        classes.add(true_c)
        for pred_c in cm[true_c]:
            classes.add(pred_c)
    return sorted(classes)


def print_confusion_matrix(cm, classes):
    """
    Print the confusion matrix in an ASCII table format.

    Rows = actual class, Columns = predicted class.

    Parameters
    ----------
    cm      : dict {true_class: {pred_class: count}}
    classes : list of str — class names in display order
    """
    # Calculate column widths
    col_width = max(len(c) for c in classes) + 2
    row_label_width = max(len(c) for c in classes) + 2

    print("")
    print("Confusion Matrix:")
    print("  (rows = Actual class, columns = Predicted class)")
    print("")

    # Header row
    header = " " * (row_label_width + 2) + "Predicted:"
    print(header)
    header2 = " " * row_label_width + "  "
    for c in classes:
        header2 = header2 + c.center(col_width)
    print(header2)

    # Divider
    total_width = row_label_width + 2 + col_width * len(classes)
    print("  " + "-" * (total_width - 2))

    # Data rows
    for true_c in classes:
        row_str = "  " + true_c.ljust(row_label_width)
        for pred_c in classes:
            count = cm.get(true_c, {}).get(pred_c, 0)
            row_str = row_str + str(count).center(col_width)
        print(row_str)

    print("")


# =============================================================================
# SECTION 4: METRIC COMPUTATION
# =============================================================================

def compute_accuracy(cm):
    """
    Compute overall accuracy = (sum of diagonal) / (sum of all cells).

    Parameters
    ----------
    cm : dict {true_class: {pred_class: count}}

    Returns
    -------
    float in [0, 1]
    """
    total_correct = 0
    total_all = 0
    for true_c in cm:
        for pred_c in cm[true_c]:
            count = cm[true_c][pred_c]
            total_all = total_all + count
            if true_c == pred_c:
                total_correct = total_correct + count

    if total_all == 0:
        return 0.0
    return total_correct / total_all


def compute_precision(cm, pos_class):
    """
    Compute precision for a given positive class:
        Precision = TP / (TP + FP)

    TP = cm[pos_class][pos_class]
    FP = sum over all other classes c: cm[c][pos_class]

    Parameters
    ----------
    cm        : dict {true_class: {pred_class: count}}
    pos_class : str — the class to treat as "positive"

    Returns
    -------
    float in [0, 1], or 0.0 if denominator is zero
    """
    # TP: predicted pos_class and actually pos_class
    tp = cm.get(pos_class, {}).get(pos_class, 0)

    # FP: predicted pos_class but actually something else
    fp = 0
    for true_c in cm:
        if true_c != pos_class:
            fp = fp + cm[true_c].get(pos_class, 0)

    if tp + fp == 0:
        return 0.0
    return tp / (tp + fp)


def compute_recall(cm, pos_class):
    """
    Compute recall for a given positive class:
        Recall = TP / (TP + FN)

    TP = cm[pos_class][pos_class]
    FN = sum over all other classes c: cm[pos_class][c]

    Parameters
    ----------
    cm        : dict {true_class: {pred_class: count}}
    pos_class : str

    Returns
    -------
    float in [0, 1], or 0.0 if denominator is zero
    """
    # TP: predicted pos_class and actually pos_class
    tp = cm.get(pos_class, {}).get(pos_class, 0)

    # FN: actually pos_class but predicted something else
    fn = 0
    for pred_c in cm.get(pos_class, {}):
        if pred_c != pos_class:
            fn = fn + cm[pos_class][pred_c]

    if tp + fn == 0:
        return 0.0
    return tp / (tp + fn)


def compute_f1(cm, pos_class):
    """
    Compute F1 score for a given class:
        F1 = 2 * Precision * Recall / (Precision + Recall)

    Parameters
    ----------
    cm        : dict {true_class: {pred_class: count}}
    pos_class : str

    Returns
    -------
    float in [0, 1], or 0.0 if both Precision and Recall are zero
    """
    precision = compute_precision(cm, pos_class)
    recall = compute_recall(cm, pos_class)

    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def print_classification_report(cm, classes):
    """
    Print a table with precision, recall, and F1 for each class, plus overall accuracy.

    Parameters
    ----------
    cm      : dict {true_class: {pred_class: count}}
    classes : list of str
    """
    print("")
    print("Classification Report:")
    print("-" * 55)
    print("{:<15} {:>10} {:>10} {:>10}".format("Class", "Precision", "Recall", "F1"))
    print("-" * 55)

    precision_sum = 0.0
    recall_sum = 0.0
    f1_sum = 0.0

    for cls in classes:
        prec = compute_precision(cm, cls)
        rec = compute_recall(cm, cls)
        f1 = compute_f1(cm, cls)
        precision_sum = precision_sum + prec
        recall_sum = recall_sum + rec
        f1_sum = f1_sum + f1
        print("{:<15} {:>10.4f} {:>10.4f} {:>10.4f}".format(cls, prec, rec, f1))

    n_classes = len(classes)
    print("-" * 55)
    # Macro average
    macro_prec = precision_sum / n_classes
    macro_rec = recall_sum / n_classes
    macro_f1 = f1_sum / n_classes
    print("{:<15} {:>10.4f} {:>10.4f} {:>10.4f}".format(
        "Macro avg", macro_prec, macro_rec, macro_f1))

    accuracy = compute_accuracy(cm)
    print("-" * 55)
    print("Overall accuracy: {:.4f}  ({:.1f}%)".format(accuracy, accuracy * 100))
    print("")


# =============================================================================
# SECTION 5: k-FOLD CROSS-VALIDATION HELPERS
# =============================================================================

def kfold_indices(n_samples, k=5, seed=42):
    """
    Generate k-fold train/test index splits.

    The data is shuffled once (using seed), then divided into k roughly
    equal folds. On each iteration, one fold is the test set and the rest
    form the training set.

    Parameters
    ----------
    n_samples : int — total number of examples
    k         : int — number of folds (default 5)
    seed      : int — random seed for shuffling

    Returns
    -------
    list of (train_indices, test_indices) tuples, length k
    """
    # Create a list of all indices and shuffle them
    indices = list(range(n_samples))

    # Manual shuffle using Fisher-Yates with a fixed seed
    rng = random.Random(seed)
    for i in range(n_samples - 1, 0, -1):
        j = rng.randint(0, i)
        indices[i], indices[j] = indices[j], indices[i]

    # Split indices into k folds (some folds may have one extra element)
    folds = []
    fold_size = n_samples // k
    remainder = n_samples % k

    start = 0
    for fold_num in range(k):
        # Distribute the remainder: first `remainder` folds get one extra element
        extra = 1 if fold_num < remainder else 0
        end = start + fold_size + extra
        folds.append(indices[start:end])
        start = end

    # Build (train, test) pairs
    splits = []
    for test_fold_idx in range(k):
        test_indices = folds[test_fold_idx]
        train_indices = []
        for i in range(k):
            if i != test_fold_idx:
                for idx in folds[i]:
                    train_indices.append(idx)
        splits.append((train_indices, test_indices))

    return splits


def majority_class(labels):
    """
    Return the most frequent class in a list of labels.
    Used as the simplest possible classifier (majority-class baseline).

    Parameters
    ----------
    labels : list of str

    Returns
    -------
    str — the most common label
    """
    counts = {}
    for label in labels:
        if label not in counts:
            counts[label] = 0
        counts[label] = counts[label] + 1

    best_class = None
    best_count = -1
    for cls, count in counts.items():
        if count > best_count:
            best_count = count
            best_class = cls
    return best_class


def cross_validate_accuracy(all_labels, k_folds=5, seed=42, verbose=True):
    """
    Evaluate the majority-class baseline classifier using k-fold cross-validation.

    On each fold:
      - Training labels are used to find the majority class
      - The majority class is predicted for every test example
      - Accuracy = fraction of test examples that match the majority class

    Parameters
    ----------
    all_labels : list of str — class labels for all examples
    k_folds    : int — number of folds (default 5)
    seed       : int — random seed (default 42)
    verbose    : bool — if True, print each fold's results

    Returns
    -------
    (mean_accuracy, per_fold_accuracies)
    """
    n = len(all_labels)
    splits = kfold_indices(n, k=k_folds, seed=seed)

    per_fold_accuracies = []

    for fold_num, (train_idx, test_idx) in enumerate(splits):
        # Get training labels for this fold
        train_labels = []
        for i in train_idx:
            train_labels.append(all_labels[i])

        # Find majority class on training data
        pred_class = majority_class(train_labels)

        # Predict majority class for all test examples
        test_labels = []
        for i in test_idx:
            test_labels.append(all_labels[i])

        # Compute accuracy for this fold
        correct = 0
        for true_label in test_labels:
            if true_label == pred_class:
                correct = correct + 1
        fold_acc = correct / len(test_labels)
        per_fold_accuracies.append(fold_acc)

        if verbose:
            print("  Fold {}: train_size={:2d}, test_size={:2d}, "
                  "majority_class={:6s}, accuracy={:.3f}".format(
                      fold_num + 1,
                      len(train_idx),
                      len(test_idx),
                      pred_class,
                      fold_acc))

    # Compute mean accuracy
    total = 0.0
    for acc in per_fold_accuracies:
        total = total + acc
    mean_acc = total / k_folds

    return mean_acc, per_fold_accuracies


# =============================================================================
# SECTION 6: DISPLAY / REPORTING UTILITIES
# =============================================================================

def print_section_header(title):
    """Print a visually distinct section header."""
    print("")
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_fold_detail(fold_num, train_idx, test_idx, all_labels):
    """
    Print the details of one fold: which examples are in train vs test.

    Parameters
    ----------
    fold_num   : int (1-based)
    train_idx  : list of int
    test_idx   : list of int
    all_labels : list of str
    """
    test_labels = [all_labels[i] for i in test_idx]
    train_labels = [all_labels[i] for i in train_idx]

    print("")
    print("  Fold {}:".format(fold_num))
    print("    Train indices (n={}): {}".format(len(train_idx), sorted(train_idx)))
    print("    Test  indices (n={}): {}".format(len(test_idx), sorted(test_idx)))

    # Distribution in test fold
    test_class_counts = {}
    for lbl in test_labels:
        if lbl not in test_class_counts:
            test_class_counts[lbl] = 0
        test_class_counts[lbl] = test_class_counts[lbl] + 1

    print("    Test class distribution: {}".format(test_class_counts))
    maj = majority_class(train_labels)
    print("    Training majority class: {}".format(maj))


def compute_std_dev(values):
    """
    Compute sample standard deviation of a list of numbers.

    Parameters
    ----------
    values : list of floats

    Returns
    -------
    float
    """
    n = len(values)
    if n < 2:
        return 0.0
    mean = sum(values) / n
    variance = 0.0
    for v in values:
        variance = variance + (v - mean) ** 2
    variance = variance / (n - 1)
    return math.sqrt(variance)


# =============================================================================
# SECTION 7: SAMPLE PREDICTIONS AND DEMO HELPERS
# =============================================================================

def make_sample_predictions():
    """
    Return a pair of (true_labels, predicted_labels) for demonstration.
    This simulates a small binary classification result.
    """
    true_labels = [
        "good", "good", "good", "bad",  "good",
        "bad",  "good", "bad",  "good", "bad",
        "good", "bad",  "good", "good", "bad"
    ]
    # A slightly imperfect classifier
    pred_labels = [
        "good", "good", "bad",  "bad",  "good",
        "good", "good", "bad",  "good", "bad",
        "bad",  "bad",  "good", "good", "good"
    ]
    return true_labels, pred_labels


def make_multiclass_predictions():
    """
    Return (true_labels, pred_labels) for a 3-class problem.
    Simulates classification of food types.
    """
    true_labels = [
        "chinese", "chinese", "italian", "italian", "burgers",
        "burgers", "chinese", "italian", "burgers", "chinese",
        "italian", "burgers"
    ]
    pred_labels = [
        "chinese", "italian", "italian", "italian", "burgers",
        "chinese", "chinese", "italian", "burgers", "chinese",
        "burgers", "burgers"
    ]
    return true_labels, pred_labels


# =============================================================================
# SECTION 8: MAIN DEMO
# =============================================================================

def main():
    print("=" * 60)
    print("PROJECT 07-03-03: Model Evaluation")
    print("Confusion Matrix, Metrics, k-Fold Cross-Validation")
    print("=" * 60)

    # ------------------------------------------------------------------
    # DEMO 1: Binary Classification Confusion Matrix
    # ------------------------------------------------------------------
    print_section_header("DEMO 1: Binary Confusion Matrix (good/bad)")

    true_labels, pred_labels = make_sample_predictions()
    n_examples = len(true_labels)

    print("\nSample predictions ({} examples):".format(n_examples))
    print("{:<6} {:<10} {}".format("Index", "Actual", "Predicted"))
    print("-" * 30)
    for i in range(n_examples):
        marker = "OK" if true_labels[i] == pred_labels[i] else "X "
        print("{:>5}  {:<10} {}  [{}]".format(
            i, true_labels[i], pred_labels[i], marker))

    # Build and display confusion matrix
    cm_binary = build_confusion_matrix(true_labels, pred_labels)
    classes_binary = get_classes_from_cm(cm_binary)
    print_confusion_matrix(cm_binary, classes_binary)

    # Show TP, TN, FP, FN breakdown for positive class = "good"
    pos = "good"
    tp = cm_binary.get(pos, {}).get(pos, 0)
    fp = sum(cm_binary.get(c, {}).get(pos, 0) for c in classes_binary if c != pos)
    fn = sum(cm_binary.get(pos, {}).get(c, 0) for c in classes_binary if c != pos)
    tn = 0
    for tc in classes_binary:
        if tc != pos:
            for pc in classes_binary:
                if pc != pos:
                    tn = tn + cm_binary.get(tc, {}).get(pc, 0)

    print("For positive class = '{}':".format(pos))
    print("  TP (predicted good, actually good) = {}".format(tp))
    print("  FP (predicted good, actually bad ) = {}".format(fp))
    print("  FN (predicted bad,  actually good) = {}".format(fn))
    print("  TN (predicted bad,  actually bad ) = {}".format(tn))

    # Print all metrics
    print_classification_report(cm_binary, classes_binary)

    # ------------------------------------------------------------------
    # DEMO 2: Multi-Class Confusion Matrix
    # ------------------------------------------------------------------
    print_section_header("DEMO 2: Multi-Class Confusion Matrix (chinese/italian/burgers)")

    true_mc, pred_mc = make_multiclass_predictions()
    cm_mc = build_confusion_matrix(true_mc, pred_mc)
    classes_mc = get_classes_from_cm(cm_mc)

    print_confusion_matrix(cm_mc, classes_mc)
    print_classification_report(cm_mc, classes_mc)

    # ------------------------------------------------------------------
    # DEMO 3: k-Fold Cross-Validation on Friends Dataset
    # ------------------------------------------------------------------
    print_section_header("DEMO 3: 5-Fold Cross-Validation (Friends Dataset)")

    rows, labels = get_friends_data()
    n = len(labels)

    print("\nFriends dataset labels: {}".format(labels))
    print("n = {}, class distribution: good={}, bad={}".format(
        n,
        labels.count("good"),
        labels.count("bad")
    ))

    print("\nNote: Using majority-class baseline as the classifier.")
    print("This is the simplest possible classifier:")
    print("  -> Always predicts the most frequent class seen in training.\n")

    # Show fold structure first
    splits = kfold_indices(n, k=5, seed=42)
    print("Fold structure (k=5, seed=42):")
    for fold_num, (train_idx, test_idx) in enumerate(splits):
        print_fold_detail(fold_num + 1, train_idx, test_idx, labels)

    print("")
    print("Running 5-fold CV:")
    print("-" * 60)
    mean_acc, per_fold = cross_validate_accuracy(labels, k_folds=5, seed=42, verbose=True)
    std_acc = compute_std_dev(per_fold)

    print("")
    print("Results:")
    print("  Per-fold accuracies: {}".format(
        ", ".join("{:.3f}".format(a) for a in per_fold)))
    print("  Mean accuracy : {:.4f}  ({:.1f}%)".format(mean_acc, mean_acc * 100))
    print("  Std deviation : {:.4f}".format(std_acc))
    print("")
    print("Interpretation:")
    print("  The majority-class baseline predicts '{}' for every example.".format(
        majority_class(labels)))
    print("  Its accuracy reflects the class imbalance in the data.")
    print("  A real classifier should significantly beat this baseline.")

    # ------------------------------------------------------------------
    # DEMO 4: Larger Cross-Validation Example
    # ------------------------------------------------------------------
    print_section_header("DEMO 4: 10-Fold CV on Simulated Larger Dataset")

    # Simulate 50 examples with 3 classes
    random.seed(99)
    sim_labels = []
    for i in range(50):
        r = random.random()
        if r < 0.50:
            sim_labels.append("A")
        elif r < 0.80:
            sim_labels.append("B")
        else:
            sim_labels.append("C")

    class_counts = {}
    for lbl in sim_labels:
        if lbl not in class_counts:
            class_counts[lbl] = 0
        class_counts[lbl] = class_counts[lbl] + 1

    print("\nSimulated dataset: n=50, classes: {}".format(class_counts))
    print("\nRunning 10-fold CV (majority-class baseline):")
    print("-" * 60)
    mean_acc_10, per_fold_10 = cross_validate_accuracy(sim_labels, k_folds=10, seed=42)
    std_10 = compute_std_dev(per_fold_10)

    print("")
    print("Results:")
    print("  Mean accuracy : {:.4f}  ({:.1f}%)".format(mean_acc_10, mean_acc_10 * 100))
    print("  Std deviation : {:.4f}".format(std_10))
    print("  Min fold acc  : {:.4f}".format(min(per_fold_10)))
    print("  Max fold acc  : {:.4f}".format(max(per_fold_10)))

    print("\nDone.")


if __name__ == "__main__":
    main()
