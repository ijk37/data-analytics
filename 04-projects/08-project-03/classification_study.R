# classification_study.R
# Project 03 -- Predictive Analytics: Full Classification Study
# Chapters: Ch2/Ch3 (EDA) + Ch4 (preprocessing) + Ch7 (3 classifiers + evaluation)

# Required: install.packages(c("class", "e1071"))
# Optional: install.packages("caret")
library(class)
library(e1071)

cat("============================================================\n")
cat("  FULL CLASSIFICATION STUDY (R)\n")
cat("  Chapters: Ch2, Ch3, Ch4, Ch7\n")
cat("============================================================\n\n")

# ============================================================
# DATASET (20 rows)
# ============================================================
dataset <- data.frame(
  Friend   = c("Andrew","Bernhard","Carolina","Dennis","Eve","Fred","Gwyneth",
               "Hayden","Irene","James","Kevin","Lea","Marcus","Nigel",
               "Oscar","Paula","Quinn","Rachel","Sam","Tina"),
  Max_temp = c(25,31,15,20,10,12,16,26,15,21,30,13, 8,12, 22,18,28,14,24,11),
  Weight   = c(77,110,70,85,65,75,75,63,55,66,95,72,83,115, 80,68,90,60,72,58),
  Height   = c(175,195,172,180,168,173,180,165,158,163,190,172,185,192,178,165,183,160,170,162),
  Years    = c(10,12, 2,16, 0, 6, 3, 2, 5,14, 1,11, 3,15,  8, 4,13, 1, 9, 2),
  Gender   = c("M","M","F","M","F","M","F","F","F","M","M","F","F","M","M","F","M","F","M","F"),
  Company  = c("Good","Good","Bad","Good","Bad","Good","Bad","Bad","Bad","Good",
               "Bad","Good","Bad","Good","Good","Bad","Good","Bad","Good","Bad"),
  stringsAsFactors = FALSE
)

TRAIN_SIZE <- 14
POSITIVE   <- "Good"

# ============================================================
# PHASE 1 (Ch2/Ch3): EDA
# ============================================================
cat("==========================================================\n")
cat("  PHASE 1 -- EXPLORATORY DATA ANALYSIS (Ch2/Ch3)\n")
cat("==========================================================\n")

# Class distribution
class_table <- table(dataset$Company)
cat("  Class distribution:\n")
for (cls in names(class_table)) {
  pct <- round(100 * class_table[cls] / nrow(dataset), 1)
  cat("   ", cls, ":", class_table[cls], "(", pct, "%)\n")
}

# Per-class feature means
numeric_cols <- c("Max_temp", "Weight", "Height", "Years")
cat("\n  Per-class feature means:\n")
cat(sprintf("  %-12s %10s %10s\n", "Feature", "Good", "Bad"))
cat("  ", strrep("-", 34), "\n")
for (col in numeric_cols) {
  mean_good <- round(mean(dataset[[col]][dataset$Company == "Good"]), 1)
  mean_bad  <- round(mean(dataset[[col]][dataset$Company == "Bad"]),  1)
  cat(sprintf("  %-12s %10.1f %10.1f\n", col, mean_good, mean_bad))
}

# Correlation matrix
cat("\n  Pearson Correlation Matrix:\n")
corr_matrix <- cor(dataset[, numeric_cols])
print(round(corr_matrix, 3))

# ============================================================
# PHASE 2 (Ch4): PREPROCESSING
# ============================================================
cat("\n==========================================================\n")
cat("  PHASE 2 -- PREPROCESSING (Ch4)\n")
cat("==========================================================\n")

# Encode Gender: M=1, F=0
dataset$Gender_num <- ifelse(dataset$Gender == "M", 1, 0)
cat("  Gender encoded: M=1, F=0\n")

# Min-max normalization (fit on ALL data, then apply)
norm_params <- list()
dataset_norm <- dataset
all_features <- c(numeric_cols, "Gender_num")

for (col in all_features) {
  mn <- min(dataset[[col]])
  mx <- max(dataset[[col]])
  norm_params[[col]] <- list(min = mn, max = mx)
  if (mx > mn) {
    dataset_norm[[col]] <- (dataset[[col]] - mn) / (mx - mn)
  } else {
    dataset_norm[[col]] <- 0
  }
}
cat("  All features normalized to [0,1]\n")

# Train/test split
train_idx <- 1:TRAIN_SIZE
test_idx  <- (TRAIN_SIZE + 1):nrow(dataset)

train_data  <- dataset_norm[train_idx, ]
test_data   <- dataset_norm[test_idx, ]
train_labels <- as.factor(dataset$Company[train_idx])
test_labels  <- dataset$Company[test_idx]

cat("  Train size:", length(train_idx), " | Test size:", length(test_idx), "\n")

# ============================================================
# PHASE 3 (Ch7): THREE CLASSIFIERS
# ============================================================
cat("\n==========================================================\n")
cat("  PHASE 3 -- THREE CLASSIFIERS (Ch7)\n")
cat("==========================================================\n")

# (a) Majority-class baseline
majority_class <- names(sort(table(train_labels), decreasing = TRUE))[1]
baseline_preds <- rep(majority_class, length(test_idx))
cat("  [Baseline] Always predicts:", majority_class, "\n")
cat("  Predictions:", paste(baseline_preds, collapse = ", "), "\n\n")

# (b) k-NN (k=3) using class::knn
knn_train <- train_data[, all_features]
knn_test  <- test_data[, all_features]
knn_preds <- as.character(knn(
  train = knn_train,
  test  = knn_test,
  cl    = train_labels,
  k     = 3
))
cat("  [k-NN k=3] Predictions:", paste(knn_preds, collapse = ", "), "\n\n")

# (c) Naive Bayes using e1071::naiveBayes
nb_train_features <- train_data[, all_features]
nb_model <- naiveBayes(nb_train_features, train_labels)
nb_preds <- as.character(predict(nb_model, test_data[, all_features]))
cat("  [Naive Bayes] Predictions:", paste(nb_preds, collapse = ", "), "\n\n")

# Prediction detail table
cat("  Prediction detail:\n")
cat(sprintf("  %-12s %8s %10s %12s %12s\n", "Name","Actual","Baseline","k-NN","NaiveBayes"))
cat("  ", strrep("-", 58), "\n")
test_names <- dataset$Friend[test_idx]
for (i in seq_along(test_idx)) {
  cat(sprintf("  %-12s %8s %10s %12s %12s\n",
              test_names[i], test_labels[i],
              baseline_preds[i], knn_preds[i], nb_preds[i]))
}

# ============================================================
# PHASE 4 (Ch7): EVALUATION
# ============================================================
cat("\n==========================================================\n")
cat("  PHASE 4 -- EVALUATION (Ch7)\n")
cat("==========================================================\n")

compute_metrics <- function(actual, predicted, pos_class = "Good") {
  tp <- sum(actual == pos_class & predicted == pos_class)
  tn <- sum(actual != pos_class & predicted != pos_class)
  fp <- sum(actual != pos_class & predicted == pos_class)
  fn <- sum(actual == pos_class & predicted != pos_class)

  accuracy  <- (tp + tn) / length(actual)
  precision <- if (tp + fp > 0) tp / (tp + fp) else 0
  recall    <- if (tp + fn > 0) tp / (tp + fn) else 0
  f1        <- if (precision + recall > 0) 2 * precision * recall / (precision + recall) else 0

  list(tp=tp, tn=tn, fp=fp, fn=fn,
       accuracy=round(accuracy,3), precision=round(precision,3),
       recall=round(recall,3), f1=round(f1,3))
}

# Confusion matrices
classifiers <- list(
  "Baseline"   = baseline_preds,
  "k-NN (k=3)" = knn_preds,
  "Naive Bayes"= nb_preds
)

all_metrics <- list()
for (clf_name in names(classifiers)) {
  preds <- classifiers[[clf_name]]
  m <- compute_metrics(test_labels, preds)
  all_metrics[[clf_name]] <- m

  cat("  Confusion Matrix --", clf_name, ":\n")
  cat("                   Pred Good   Pred Bad\n")
  cat("  Actual Good  :   TP=", m$tp, "       FN=", m$fn, "\n")
  cat("  Actual Bad   :   FP=", m$fp, "       TN=", m$tn, "\n\n")
}

# Comparison table
cat("  Comparison Table:\n")
cat(sprintf("  %-14s %10s %12s %8s %6s\n", "Classifier","Accuracy","Precision","Recall","F1"))
cat("  ", strrep("-", 54), "\n")
for (clf_name in names(all_metrics)) {
  m <- all_metrics[[clf_name]]
  cat(sprintf("  %-14s %10.3f %12.3f %8.3f %6.3f\n",
              clf_name, m$accuracy, m$precision, m$recall, m$f1))
}

# Verdict
best_clf <- names(which.max(sapply(all_metrics, function(m) m$f1)))
best_f1  <- all_metrics[[best_clf]]$f1
cat("\n  VERDICT:\n")
cat("  Best classifier by F1:", best_clf, "(F1 =", best_f1, ")\n")
cat("  Baseline establishes the lower bound. k-NN leverages proximity in\n")
cat("  normalized feature space. Naive Bayes uses probabilistic independence.\n")
cat("  On this small dataset with numeric features, Gaussian NB typically\n")
cat("  captures class-conditional distributions well.\n")

# Optional: caret confusionMatrix if available
if (requireNamespace("caret", quietly = TRUE)) {
  cat("\n  [caret] Naive Bayes detailed evaluation:\n")
  library(caret)
  cm <- confusionMatrix(
    factor(nb_preds, levels = c("Good","Bad")),
    factor(test_labels, levels = c("Good","Bad"))
  )
  print(cm)
}

cat("\nDone.\n")
