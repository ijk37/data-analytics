# classification_study.py
# Project 03 -- Predictive Analytics: Full Classification Study
# Chapters: Ch2/Ch3 (EDA) + Ch4 (preprocessing) + Ch7 (classifiers + evaluation)

# ===== SECTION 1: IMPORTS =====
import csv
import math


# ===== SECTION 2: CONSTANTS =====
NUMERIC_FEATURES = ["Max_temp", "Weight", "Height", "Years"]
GENDER_COL = "Gender"
TARGET_COL = "Company"
NAME_COL = "Friend"
TRAIN_SIZE = 14   # first 14 rows for training
K_NN = 3
POSITIVE_CLASS = "Good"
NEGATIVE_CLASS = "Bad"


# ===== SECTION 3: DEMO DATASET =====
DATASET = [
    {"Friend": "Andrew",   "Max_temp": 25, "Weight": 77,  "Height": 175, "Years": 10, "Gender": "M", "Company": "Good"},
    {"Friend": "Bernhard", "Max_temp": 31, "Weight": 110, "Height": 195, "Years": 12, "Gender": "M", "Company": "Good"},
    {"Friend": "Carolina", "Max_temp": 15, "Weight": 70,  "Height": 172, "Years": 2,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Dennis",   "Max_temp": 20, "Weight": 85,  "Height": 180, "Years": 16, "Gender": "M", "Company": "Good"},
    {"Friend": "Eve",      "Max_temp": 10, "Weight": 65,  "Height": 168, "Years": 0,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Fred",     "Max_temp": 12, "Weight": 75,  "Height": 173, "Years": 6,  "Gender": "M", "Company": "Good"},
    {"Friend": "Gwyneth",  "Max_temp": 16, "Weight": 75,  "Height": 180, "Years": 3,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Hayden",   "Max_temp": 26, "Weight": 63,  "Height": 165, "Years": 2,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Irene",    "Max_temp": 15, "Weight": 55,  "Height": 158, "Years": 5,  "Gender": "F", "Company": "Bad"},
    {"Friend": "James",    "Max_temp": 21, "Weight": 66,  "Height": 163, "Years": 14, "Gender": "M", "Company": "Good"},
    {"Friend": "Kevin",    "Max_temp": 30, "Weight": 95,  "Height": 190, "Years": 1,  "Gender": "M", "Company": "Bad"},
    {"Friend": "Lea",      "Max_temp": 13, "Weight": 72,  "Height": 172, "Years": 11, "Gender": "F", "Company": "Good"},
    {"Friend": "Marcus",   "Max_temp": 8,  "Weight": 83,  "Height": 185, "Years": 3,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Nigel",    "Max_temp": 12, "Weight": 115, "Height": 192, "Years": 15, "Gender": "M", "Company": "Good"},
    # 6 test objects
    {"Friend": "Oscar",    "Max_temp": 22, "Weight": 80,  "Height": 178, "Years": 8,  "Gender": "M", "Company": "Good"},
    {"Friend": "Paula",    "Max_temp": 18, "Weight": 68,  "Height": 165, "Years": 4,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Quinn",    "Max_temp": 28, "Weight": 90,  "Height": 183, "Years": 13, "Gender": "M", "Company": "Good"},
    {"Friend": "Rachel",   "Max_temp": 14, "Weight": 60,  "Height": 160, "Years": 1,  "Gender": "F", "Company": "Bad"},
    {"Friend": "Sam",      "Max_temp": 24, "Weight": 72,  "Height": 170, "Years": 9,  "Gender": "M", "Company": "Good"},
    {"Friend": "Tina",     "Max_temp": 11, "Weight": 58,  "Height": 162, "Years": 2,  "Gender": "F", "Company": "Bad"},
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


def euclidean_distance(a, b):
    total = 0.0
    for i in range(len(a)):
        total = total + (a[i] - b[i]) ** 2
    return math.sqrt(total)


def apply_norm(value, mn, mx):
    if mx == mn:
        return 0.0
    return (value - mn) / (mx - mn)


def gaussian_pdf(x, mean, std):
    if std == 0.0:
        if abs(x - mean) < 1e-9:
            return 1.0
        return 1e-10
    exponent = -0.5 * ((x - mean) / std) ** 2
    coeff = 1.0 / (std * math.sqrt(2.0 * math.pi))
    return coeff * math.exp(exponent)


def get_feature_vector(row):
    """Return [Max_temp, Weight, Height, Years, Gender_num] as floats."""
    vec = []
    for feat in NUMERIC_FEATURES:
        vec.append(float(row[feat]))
    gender_num = 1.0 if row[GENDER_COL] == "M" else 0.0
    vec.append(gender_num)
    return vec


def majority_vote(labels):
    counts = {}
    for label in labels:
        if label not in counts:
            counts[label] = 0
        counts[label] = counts[label] + 1
    best = None
    best_count = -1
    for label, count in counts.items():
        if count > best_count:
            best_count = count
            best = label
    return best


def confusion_matrix(actual, predicted):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(len(actual)):
        a = actual[i]
        p = predicted[i]
        if a == POSITIVE_CLASS and p == POSITIVE_CLASS:
            tp = tp + 1
        elif a == NEGATIVE_CLASS and p == NEGATIVE_CLASS:
            tn = tn + 1
        elif a == NEGATIVE_CLASS and p == POSITIVE_CLASS:
            fp = fp + 1
        elif a == POSITIVE_CLASS and p == NEGATIVE_CLASS:
            fn = fn + 1
    return tp, tn, fp, fn


def compute_metrics(tp, tn, fp, fn):
    n = tp + tn + fp + fn
    accuracy = (tp + tn) / n if n > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return round(accuracy, 3), round(precision, 3), round(recall, 3), round(f1, 3)


# ===== SECTION 5: CORE ANALYSIS =====

def phase1_eda(data):
    """Ch2/Ch3: Class distribution, per-class feature means, correlation matrix."""
    classes = [POSITIVE_CLASS, NEGATIVE_CLASS]
    n = len(data)

    class_counts = {}
    for cls in classes:
        count = 0
        for row in data:
            if row[TARGET_COL] == cls:
                count = count + 1
        class_counts[cls] = count

    # Per-class mean for each numeric feature
    per_class_means = {}
    for cls in classes:
        per_class_means[cls] = {}
        for feat in NUMERIC_FEATURES:
            vals = []
            for row in data:
                if row[TARGET_COL] == cls:
                    vals.append(float(row[feat]))
            per_class_means[cls][feat] = round(compute_mean(vals), 1)

    # Pearson correlation matrix
    col_data = {}
    for feat in NUMERIC_FEATURES:
        col_data[feat] = []
        for row in data:
            col_data[feat].append(float(row[feat]))

    corr = {}
    for f1 in NUMERIC_FEATURES:
        corr[f1] = {}
        for f2 in NUMERIC_FEATURES:
            corr[f1][f2] = round(pearson_r(col_data[f1], col_data[f2]), 3)

    return class_counts, n, per_class_means, corr


def phase2_preprocess(data):
    """Ch4: Encode Gender (M=1, F=0), min-max normalize, split train/test."""
    # Compute normalization params on ALL data (then apply to train/test)
    norm_params = {}
    for feat in NUMERIC_FEATURES:
        vals = []
        for row in data:
            vals.append(float(row[feat]))
        norm_params[feat] = (min(vals), max(vals))

    processed = []
    for row in data:
        new_row = {}
        new_row[NAME_COL] = row[NAME_COL]
        new_row[TARGET_COL] = row[TARGET_COL]
        new_row[GENDER_COL] = row[GENDER_COL]
        for feat in NUMERIC_FEATURES:
            mn, mx = norm_params[feat]
            new_row[feat] = apply_norm(float(row[feat]), mn, mx)
        new_row["Gender_num"] = 1.0 if row[GENDER_COL] == "M" else 0.0
        processed.append(new_row)

    train = processed[:TRAIN_SIZE]
    test  = processed[TRAIN_SIZE:]
    return train, test, norm_params


def phase3a_baseline(train, test):
    """Ch7 Baseline: Always predict the most common training class."""
    train_labels = []
    for row in train:
        train_labels.append(row[TARGET_COL])
    majority = majority_vote(train_labels)
    predictions = []
    for _ in test:
        predictions.append(majority)
    return predictions, majority


def phase3b_knn(train, test):
    """Ch7 k-NN (k=3): Euclidean distance on normalized features."""
    all_features = NUMERIC_FEATURES + ["Gender_num"]
    predictions = []
    for test_row in test:
        test_vec = []
        for feat in all_features:
            test_vec.append(float(test_row[feat]))

        distances = []
        for train_row in train:
            train_vec = []
            for feat in all_features:
                train_vec.append(float(train_row[feat]))
            d = euclidean_distance(test_vec, train_vec)
            distances.append((d, train_row[TARGET_COL]))

        # Sort by distance (bubble sort to keep stdlib only)
        for i in range(len(distances)):
            for j in range(i + 1, len(distances)):
                if distances[j][0] < distances[i][0]:
                    distances[i], distances[j] = distances[j], distances[i]

        k_labels = []
        for i in range(K_NN):
            k_labels.append(distances[i][1])

        pred = majority_vote(k_labels)
        predictions.append(pred)
    return predictions


def phase3c_naive_bayes(train, test):
    """Ch7 Gaussian Naive Bayes: Gaussian for numeric, count-based for gender."""
    all_features = NUMERIC_FEATURES  # numeric features only
    classes = [POSITIVE_CLASS, NEGATIVE_CLASS]

    # Compute class priors
    class_prior = {}
    n_train = len(train)
    for cls in classes:
        count = 0
        for row in train:
            if row[TARGET_COL] == cls:
                count = count + 1
        class_prior[cls] = count / n_train

    # Compute mean/std per class per numeric feature
    class_stats = {}
    for cls in classes:
        class_stats[cls] = {}
        for feat in all_features:
            vals = []
            for row in train:
                if row[TARGET_COL] == cls:
                    vals.append(float(row[feat]))
            m = compute_mean(vals)
            s = compute_std(vals)
            if s < 0.001:
                s = 0.001
            class_stats[cls][feat] = (m, s)

        # Gender: count-based with Laplace smoothing
        gender_m_count = 0
        gender_f_count = 0
        cls_total = 0
        for row in train:
            if row[TARGET_COL] == cls:
                cls_total = cls_total + 1
                if row[GENDER_COL] == "M":
                    gender_m_count = gender_m_count + 1
                else:
                    gender_f_count = gender_f_count + 1
        # Laplace smoothing: add 1, denominator += 2
        class_stats[cls]["P_gender_M"] = (gender_m_count + 1) / (cls_total + 2)
        class_stats[cls]["P_gender_F"] = (gender_f_count + 1) / (cls_total + 2)

    predictions = []
    for test_row in test:
        posteriors = {}
        for cls in classes:
            log_prob = math.log(class_prior[cls])
            for feat in all_features:
                m, s = class_stats[cls][feat]
                p = gaussian_pdf(float(test_row[feat]), m, s)
                if p <= 0.0:
                    p = 1e-15
                log_prob = log_prob + math.log(p)
            # Gender
            if test_row[GENDER_COL] == "M":
                p_gender = class_stats[cls]["P_gender_M"]
            else:
                p_gender = class_stats[cls]["P_gender_F"]
            log_prob = log_prob + math.log(p_gender)
            posteriors[cls] = log_prob

        best_cls = None
        best_val = None
        for cls, val in posteriors.items():
            if best_val is None or val > best_val:
                best_val = val
                best_cls = cls
        predictions.append(best_cls)

    return predictions


def phase4_evaluate(test, baseline_preds, knn_preds, nb_preds):
    """Ch7: Confusion matrix and metrics for each classifier."""
    actual = []
    for row in test:
        actual.append(row[TARGET_COL])

    results = {}
    for name, preds in [("Baseline", baseline_preds),
                         ("k-NN (k=3)", knn_preds),
                         ("Naive Bayes", nb_preds)]:
        tp, tn, fp, fn = confusion_matrix(actual, preds)
        acc, prec, rec, f1 = compute_metrics(tp, tn, fp, fn)
        results[name] = {
            "tp": tp, "tn": tn, "fp": fp, "fn": fn,
            "accuracy": acc, "precision": prec, "recall": rec, "f1": f1,
            "predictions": preds,
        }
    return results, actual


# ===== SECTION 6: PRINTING / REPORTING =====

def print_separator(char="-", width=62):
    print(char * width)


def print_phase_header(n, title):
    print("")
    print("=" * 62)
    print("  PHASE " + str(n) + " -- " + title)
    print("=" * 62)


def print_phase1(class_counts, n, per_class_means, corr):
    print_phase_header(1, "EXPLORATORY DATA ANALYSIS (Ch2/Ch3)")

    print("  Class distribution:")
    for cls in [POSITIVE_CLASS, NEGATIVE_CLASS]:
        pct = round(100.0 * class_counts[cls] / n, 1)
        print("    " + cls + ": " + str(class_counts[cls]) + " (" + str(pct) + "%)")

    print("")
    print("  Per-class feature means:")
    header = "  {:<12}".format("Feature")
    for cls in [POSITIVE_CLASS, NEGATIVE_CLASS]:
        header = header + " {:>10}".format(cls)
    print(header)
    print_separator("-", 34)
    for feat in NUMERIC_FEATURES:
        row_str = "  {:<12}".format(feat)
        for cls in [POSITIVE_CLASS, NEGATIVE_CLASS]:
            row_str = row_str + " {:>10.1f}".format(per_class_means[cls][feat])
        print(row_str)

    print("")
    print("  Pearson Correlation Matrix (numeric features):")
    header = "  {:<12}".format("")
    for feat in NUMERIC_FEATURES:
        header = header + " {:>10}".format(feat[:10])
    print(header)
    print_separator("-", 54)
    for f1 in NUMERIC_FEATURES:
        row_str = "  {:<12}".format(f1)
        for f2 in NUMERIC_FEATURES:
            row_str = row_str + " {:>10.3f}".format(corr[f1][f2])
        print(row_str)


def print_phase2(train, test):
    print_phase_header(2, "PREPROCESSING (Ch4)")
    print("  Gender encoded: M=1, F=0")
    print("  All features normalized to [0,1] (min-max)")
    print("  Train set: " + str(len(train)) + " rows (rows 1-14)")
    print("  Test set:  " + str(len(test)) + " rows (rows 15-20)")
    print("")
    print("  Test objects:")
    for row in test:
        parts = []
        for feat in NUMERIC_FEATURES:
            parts.append(feat + "=" + str(round(row[feat], 2)))
        parts.append("Gender=" + row[GENDER_COL])
        print("    " + row[NAME_COL] + " -> " + ", ".join(parts) +
              " | Label: " + row[TARGET_COL])


def print_phase3(test, baseline_preds, baseline_majority, knn_preds, nb_preds):
    print_phase_header(3, "THREE CLASSIFIERS (Ch7)")

    actual = []
    for row in test:
        actual.append(row[TARGET_COL])
    names = []
    for row in test:
        names.append(row[NAME_COL])

    print("  [Baseline] Always predicts majority class: " + baseline_majority)
    print("  [k-NN k=" + str(K_NN) + "]  Predictions: " + ", ".join(knn_preds))
    print("  [Naive Bayes]  Predictions: " + ", ".join(nb_preds))
    print("")
    print("  Prediction detail (test objects):")
    header = "  {:<12} {:>8} {:>10} {:>12} {:>12}".format(
        "Name", "Actual", "Baseline", "k-NN", "NaiveBayes"
    )
    print(header)
    print_separator("-", 58)
    for i in range(len(test)):
        row_str = "  {:<12} {:>8} {:>10} {:>12} {:>12}".format(
            names[i], actual[i],
            baseline_preds[i], knn_preds[i], nb_preds[i]
        )
        print(row_str)


def print_confusion_matrix(tp, tn, fp, fn, name):
    print("  Confusion Matrix -- " + name + ":")
    print("                 Pred Good   Pred Bad")
    print("  Actual Good  :   TP=" + str(tp) + "        FN=" + str(fn))
    print("  Actual Bad   :   FP=" + str(fp) + "        TN=" + str(tn))


def print_phase4(results, actual):
    print_phase_header(4, "EVALUATION (Ch7)")

    for name, r in results.items():
        print_confusion_matrix(r["tp"], r["tn"], r["fp"], r["fn"], name)
        print("")

    print("  Comparison Table:")
    header = "  {:<14} {:>10} {:>12} {:>8} {:>6}".format(
        "Classifier", "Accuracy", "Precision", "Recall", "F1"
    )
    print(header)
    print_separator("-", 54)
    for name, r in results.items():
        row_str = "  {:<14} {:>10.3f} {:>12.3f} {:>8.3f} {:>6.3f}".format(
            name, r["accuracy"], r["precision"], r["recall"], r["f1"]
        )
        print(row_str)

    # Verdict
    print("")
    print("  VERDICT:")
    best_name = None
    best_f1 = -1.0
    for name, r in results.items():
        if r["f1"] > best_f1:
            best_f1 = r["f1"]
            best_name = name
    print("  Best classifier by F1: " + best_name + " (F1=" + str(best_f1) + ")")
    print("  Baseline establishes the lower bound; k-NN uses distance in feature")
    print("  space; Naive Bayes uses probabilistic independence assumption.")
    print("  On this small dataset with clear numeric separation between classes,")
    print("  Gaussian Naive Bayes typically performs best due to the near-Gaussian")
    print("  distribution of features within each class.")


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
    print("  FULL CLASSIFICATION STUDY")
    print("  Chapters: Ch2, Ch3, Ch4, Ch7")
    print("=" * 62)

    # Phase 1: EDA
    class_counts, n, per_class_means, corr = phase1_eda(DATASET)
    print_phase1(class_counts, n, per_class_means, corr)

    # Phase 2: Preprocessing
    train, test, norm_params = phase2_preprocess(DATASET)
    print_phase2(train, test)

    # Phase 3: Classifiers
    baseline_preds, baseline_majority = phase3a_baseline(train, test)
    knn_preds = phase3b_knn(train, test)
    nb_preds  = phase3c_naive_bayes(train, test)
    print_phase3(test, baseline_preds, baseline_majority, knn_preds, nb_preds)

    # Phase 4: Evaluation
    results, actual = phase4_evaluate(test, baseline_preds, knn_preds, nb_preds)
    print_phase4(results, actual)

    print("")
    print("Done.")


if __name__ == "__main__":
    main()
