# =============================================================================
# Project 05: Student Performance Predictor (R Version)
# Chapter 8 - Final Projects (Capstone)
# Data Analytics Course
#
# A school wants to predict which students will fail, cluster them by
# performance profile, and find co-occurrence patterns in weak students.
#
# Phases:
#   1  (Ch1)  Attribute type identification
#   2  (Ch2)  Descriptive statistics
#   3  (Ch4)  Preprocessing: outlier detection, discretisation, normalisation
#   4  (Ch3)  Multivariate analysis: correlation matrix
#   5  (Ch6)  Frequent pattern mining (arules, optional)
#   6  (Ch5)  Clustering: K-means K=3 + cluster profiling
#   7  (Ch7)  Classification: knn + naiveBayes + evaluation
#
# Optional packages: arules, class, e1071
#   install.packages(c("arules", "class", "e1071"))
#
# Run: Rscript student_analysis.R
#      or source("student_analysis.R") in RStudio
# =============================================================================

cat(strrep("=", 65), "\n")
cat("  Student Performance Predictor -- R\n")
cat(strrep("=", 65), "\n\n")

# Helper
print_phase <- function(num, chapter, title) {
  cat("\n")
  cat(strrep("=", 65), "\n")
  cat(sprintf("=== PHASE %d (Ch%d): %s ===\n", num, chapter, title))
  cat(strrep("=", 65), "\n\n")
}


# =============================================================================
# DATASET: 25 students, hardcoded
# =============================================================================

student_df <- data.frame(
  Name       = c("Alice","Bob","Carlos","Diana","Ethan","Fiona","George",
                 "Hannah","Ivan","Julia","Kevin","Laura","Mike","Nancy",
                 "Oscar","Paula","Quinn","Rachel","Sam","Tina","Uma",
                 "Victor","Wendy","Xavier","Yara"),
  Math       = c(85,42,72,91,35,78,55,88,48,80,38,92,60,45,75,30,82,52,70,44,86,40,77,58,33),
  Science    = c(88,38,68,95,40,72,48,92,45,75,35,90,65,42,70,32,85,50,68,48,88,38,74,55,30),
  English    = c(90,55,75,88,48,80,60,85,52,82,42,94,68,50,78,38,80,58,72,52,84,45,80,62,40),
  History    = c(82,45,70,93,38,75,52,90,50,78,40,88,62,48,72,35,88,55,65,46,90,42,76,60,35),
  StudyHours = c(6,2,4,7,1,5,3,7,2,5,1,8,4,2,5,1,6,3,4,2,6,2,5,3,1),
  Absences   = c(2,8,3,1,12,2,7,1,9,2,11,0,5,8,3,14,2,6,4,9,1,10,3,6,13),
  Result     = c("Pass","Fail","Pass","Pass","Fail","Pass","Fail","Pass","Fail",
                 "Pass","Fail","Pass","Pass","Fail","Pass","Fail","Pass","Fail",
                 "Pass","Fail","Pass","Fail","Pass","Pass","Fail"),
  stringsAsFactors = FALSE
)

# Convert Result to factor for classifiers
student_df$Result <- as.factor(student_df$Result)

numeric_cols <- c("Math","Science","English","History","StudyHours","Absences")
subject_cols <- c("Math","Science","English","History")


# =============================================================================
# PHASE 1 (Ch1): ATTRIBUTE TYPE IDENTIFICATION
# =============================================================================
print_phase(1, 1, "ATTRIBUTE TYPE IDENTIFICATION")

attr_table <- data.frame(
  Attribute  = c("Math","Science","English","History","StudyHours","Absences","Result"),
  Scale      = c("Ratio","Ratio","Ratio","Ratio","Ratio","Ratio","Nominal"),
  Disc_Cont  = c("Continuous","Continuous","Continuous","Continuous",
                 "Continuous","Continuous","Discrete"),
  Notes      = c("0-100","0-100","0-100","0-100","hrs/week","days","Pass/Fail"),
  stringsAsFactors = FALSE
)
print(attr_table, row.names = FALSE)


# =============================================================================
# PHASE 2 (Ch2): DESCRIPTIVE STATISTICS
# =============================================================================
print_phase(2, 2, "DESCRIPTIVE STATISTICS")

cat("--- Overall summary ---\n")
print(summary(student_df[, numeric_cols]))

cat("\n--- Per-class (Pass vs Fail) means ---\n\n")
pass_rows <- student_df[student_df$Result == "Pass", ]
fail_rows <- student_df[student_df$Result == "Fail", ]

class_means <- data.frame(
  Attribute = numeric_cols,
  Pass_mean = sapply(numeric_cols, function(col) round(mean(pass_rows[[col]]), 2)),
  Fail_mean = sapply(numeric_cols, function(col) round(mean(fail_rows[[col]]), 2)),
  stringsAsFactors = FALSE
)
class_means$Abs_diff <- round(abs(class_means$Pass_mean - class_means$Fail_mean), 2)
class_means <- class_means[order(-class_means$Abs_diff), ]
print(class_means, row.names = FALSE)

cat("\n--- Most discriminating attribute ---\n")
cat(sprintf("  %s has the largest gap (%.2f) between Pass and Fail groups.\n",
            class_means$Attribute[1], class_means$Abs_diff[1]))

cat("\n--- Standard deviation per attribute ---\n")
print(round(sapply(student_df[, numeric_cols], sd), 2))

cat("\n--- Result distribution ---\n")
print(table(student_df$Result))
cat(sprintf("  Pass rate: %.1f%%\n",
            sum(student_df$Result == "Pass") / nrow(student_df) * 100))


# =============================================================================
# PHASE 3 (Ch4): PREPROCESSING
# =============================================================================
print_phase(3, 4, "PREPROCESSING")

# Step 3a: IQR outlier detection on Absences
cat("--- Step 3a: IQR outlier detection on 'Absences' ---\n")
q1_abs <- quantile(student_df$Absences, 0.25)
q3_abs <- quantile(student_df$Absences, 0.75)
iqr_abs <- q3_abs - q1_abs
lower_fence <- q1_abs - 1.5 * iqr_abs
upper_fence <- q3_abs + 1.5 * iqr_abs
cat(sprintf("  Q1=%.2f  Q3=%.2f  IQR=%.2f\n", q1_abs, q3_abs, iqr_abs))
cat(sprintf("  Lower fence: %.2f  Upper fence: %.2f\n", lower_fence, upper_fence))

outlier_rows <- student_df[student_df$Absences < lower_fence |
                              student_df$Absences > upper_fence, ]
if (nrow(outlier_rows) == 0) {
  cat("  No outliers detected.\n")
} else {
  cat("  Outliers:\n")
  print(outlier_rows[, c("Name","Absences","Result")], row.names = FALSE)
}

# Step 3b: Grade discretisation
cat("\n--- Step 3b: Grade-label discretisation ---\n")
cat("  Bins: <50=Fail_grade  50-69=Satisfactory  70-84=Good  >=85=Excellent\n\n")

for (col in subject_cols) {
  col_disc <- cut(student_df[[col]],
                  breaks = c(-Inf, 49.9999, 69.9999, 84.9999, Inf),
                  labels = c("Fail_grade","Satisfactory","Good","Excellent"))
  student_df[[paste0(col, "_grade")]] <- col_disc
}

# Show grade columns
grade_cols <- paste0(subject_cols, "_grade")
disc_view <- student_df[, c("Name", grade_cols, "Result")]
print(disc_view, row.names = FALSE)

# Step 3c: Min-max normalisation
cat("\n--- Step 3c: Min-max normalisation ---\n")
cat("  3 sample rows BEFORE normalisation:\n")
print(student_df[c(1, 2, 3), c("Name", numeric_cols, "Result")], row.names = FALSE)

student_norm <- student_df
for (col in numeric_cols) {
  mn <- min(student_norm[[col]])
  mx <- max(student_norm[[col]])
  student_norm[[col]] <- (student_norm[[col]] - mn) / (mx - mn)
}

cat("\n  3 sample rows AFTER normalisation:\n")
tmp <- student_norm[c(1, 2, 3), c("Name", numeric_cols, "Result")]
tmp[, numeric_cols] <- round(tmp[, numeric_cols], 4)
print(tmp, row.names = FALSE)


# =============================================================================
# PHASE 4 (Ch3): MULTIVARIATE ANALYSIS
# =============================================================================
print_phase(4, 3, "MULTIVARIATE ANALYSIS")

cat("--- 6x6 Pearson Correlation Matrix ---\n\n")
corr_mat <- cor(student_df[, numeric_cols])
print(round(corr_mat, 3))

cat("\n--- Top correlations ---\n")
corr_long <- data.frame(
  Col1 = character(), Col2 = character(), r = numeric(),
  stringsAsFactors = FALSE
)
nc <- length(numeric_cols)
for (i in 1:(nc - 1)) {
  for (j in (i + 1):nc) {
    corr_long <- rbind(corr_long, data.frame(
      Col1 = numeric_cols[i], Col2 = numeric_cols[j],
      r    = corr_mat[i, j], stringsAsFactors = FALSE
    ))
  }
}
corr_long <- corr_long[order(-abs(corr_long$r)), ]
cat("  Top 3 strongest correlations:\n")
print(head(corr_long, 3), row.names = FALSE)

cat("\n  Weakest correlation:\n")
corr_long_sorted <- corr_long[order(corr_long$r), ]
print(head(corr_long_sorted, 1), row.names = FALSE)

# Save scatter plot
tryCatch({
  png("student_scatter.png", width = 600, height = 500)
  plot(student_df$Math, student_df$Absences,
       col  = ifelse(student_df$Result == "Pass", "blue", "red"),
       pch  = 19,
       main = "Math Score vs Absences (blue=Pass, red=Fail)",
       xlab = "Math Score",
       ylab = "Absences")
  legend("topright", legend = c("Pass","Fail"),
         col = c("blue","red"), pch = 19, bty = "n")
  dev.off()
  cat("\n  Saved student_scatter.png\n")
}, error = function(e) {
  cat("  (scatter plot skipped)\n")
})


# =============================================================================
# PHASE 5 (Ch6): FREQUENT PATTERN MINING
# =============================================================================
print_phase(5, 6, "FREQUENT PATTERN MINING")

if (!requireNamespace("arules", quietly = TRUE)) {
  cat("  arules not installed. Install with: install.packages('arules')\n")
  cat("  Skipping Phase 5.\n")
} else {
  library(arules)

  cat("--- Building grade-label transactions ---\n\n")

  # Build transaction data frame: grade per subject + Result
  trans_df <- data.frame(
    Math    = paste0("Math_",    as.character(student_df$Math_grade)),
    Science = paste0("Science_", as.character(student_df$Science_grade)),
    English = paste0("English_", as.character(student_df$English_grade)),
    History = paste0("History_", as.character(student_df$History_grade)),
    Result  = paste0("Result_",  as.character(student_df$Result)),
    stringsAsFactors = FALSE
  )
  trans_df[] <- lapply(trans_df, as.factor)
  trans_obj  <- as(trans_df, "transactions")
  cat(sprintf("  Transactions: %d\n\n", length(trans_obj)))

  min_sup_frac <- 5 / nrow(student_df)

  # Frequent itemsets
  cat("--- Frequent itemsets (support >= 5 of 25) ---\n")
  freq_sets <- apriori(trans_obj,
                       parameter = list(supp   = min_sup_frac,
                                        target = "frequent itemsets",
                                        minlen = 1),
                       control = list(verbose = FALSE))
  inspect(sort(freq_sets, by = "count", decreasing = TRUE))

  # Association rules
  cat("\n--- Association rules (confidence >= 0.7) ---\n")
  rules <- apriori(trans_obj,
                   parameter = list(supp   = min_sup_frac,
                                    conf   = 0.7,
                                    minlen = 2,
                                    target = "rules"),
                   control = list(verbose = FALSE))
  inspect(sort(rules, by = "confidence", decreasing = TRUE))

  # Filter rules with Fail_grade in RHS
  cat("\n--- Rules predicting Fail_grade ---\n")
  fail_rules <- subset(rules, grepl("Fail_grade", labels(rhs(rules))))
  if (length(fail_rules) == 0) {
    cat("  No rules with Fail_grade in consequent at these thresholds.\n")
  } else {
    inspect(sort(fail_rules, by = "confidence", decreasing = TRUE))
  }
}


# =============================================================================
# PHASE 6 (Ch5): CLUSTERING (K-MEANS K=3)
# =============================================================================
print_phase(6, 5, "CLUSTERING (K-MEANS K=3)")

set.seed(42)
cat("--- K-means with K=3 on normalised (Math, Science, StudyHours, Absences) ---\n\n")

cluster_features <- student_norm[, c("Math","Science","StudyHours","Absences")]
km3 <- kmeans(cluster_features, centers = 3, nstart = 20)

cat("Cluster sizes:\n")
print(km3$size)
cat("\nCluster centroids (normalised space):\n")
print(round(km3$centers, 4))

student_norm$Cluster <- as.factor(km3$cluster)

cat("\n--- Cluster vs Result cross-table ---\n")
print(table(Cluster = km3$cluster, Result = student_norm$Result))

# Cluster profiles in original scale
cat("\n--- Cluster profiles (original scale) ---\n\n")
student_df$Cluster <- km3$cluster
for (cl in sort(unique(km3$cluster))) {
  cl_rows <- student_df[student_df$Cluster == cl, ]
  math_m  <- mean(cl_rows$Math)
  sci_m   <- mean(cl_rows$Science)
  study_m <- mean(cl_rows$StudyHours)
  abs_m   <- mean(cl_rows$Absences)
  dominant_result <- names(sort(table(cl_rows$Result), decreasing = TRUE))[1]

  if (dominant_result == "Pass" && math_m >= 70) {
    human_label <- "High Achievers"
  } else if (dominant_result == "Fail") {
    human_label <- "At Risk"
  } else {
    human_label <- "Average Students"
  }

  cat(sprintf('  Cluster %d -- "%s"  (%d students, dominant=%s)\n',
              cl, human_label, nrow(cl_rows), dominant_result))
  cat(sprintf("    Math=%.1f  Science=%.1f  StudyHours=%.1f  Absences=%.1f\n",
              math_m, sci_m, study_m, abs_m))
  cat(sprintf("    Members: %s\n\n", paste(cl_rows$Name, collapse=", ")))
}

cat(sprintf("  SSE (tot.withinss): %.4f\n", km3$tot.withinss))

# Mini elbow
cat("\n--- Mini elbow (SSE vs K) ---\n")
for (kv in 2:5) {
  km_k <- kmeans(cluster_features, centers = kv, nstart = 20)
  cat(sprintf("  K=%d  SSE = %.4f\n", kv, km_k$tot.withinss))
}

# Cluster plot
tryCatch({
  png("student_cluster.png", width = 600, height = 500)
  plot(student_norm$Math, student_norm$Absences,
       col  = km3$cluster,
       pch  = as.integer(student_norm$Result),
       main = "K-means (K=3): Math vs Absences (normalised)",
       xlab = "Math (norm)", ylab = "Absences (norm)")
  points(km3$centers[, c("Math","Absences")],
         col = 1:3, pch = 8, cex = 2, lwd = 2)
  legend("topright", legend = paste("Cluster", 1:3),
         col = 1:3, pch = 19, bty = "n")
  dev.off()
  cat("\n  Saved student_cluster.png\n")
}, error = function(e) {
  cat("  (cluster plot skipped)\n")
})


# =============================================================================
# PHASE 7 (Ch7): CLASSIFICATION (k-NN + NAIVE BAYES)
# =============================================================================
print_phase(7, 7, "CLASSIFICATION (k-NN + NAIVE BAYES)")

# 80/20 train/test split: first 20 = train, last 5 = test
# (mirrors Python split for comparability)
train_set <- student_norm[1:20, ]
test_set  <- student_norm[21:25, ]

cat(sprintf("Train: %d rows  |  Test: %d rows\n", nrow(train_set), nrow(test_set)))
cat("Test students:", paste(test_set$Name, collapse=", "), "\n\n")

feature_cols <- numeric_cols   # 6 normalised features
true_labels  <- test_set$Result

# ---- k-NN ----
if (!requireNamespace("class", quietly = TRUE)) {
  cat("  class package not available. Install: install.packages('class')\n")
  knn_preds <- rep(NA, nrow(test_set))
} else {
  library(class)
  knn_preds <- knn(train = train_set[, feature_cols],
                   test  = test_set[, feature_cols],
                   cl    = train_set$Result,
                   k     = 3)
  cat("--- k-NN (k=3) ---\n")
  pred_df_knn <- data.frame(
    Name    = test_set$Name,
    True    = true_labels,
    kNN     = knn_preds,
    Correct = ifelse(true_labels == knn_preds, "YES", "NO"),
    stringsAsFactors = FALSE
  )
  print(pred_df_knn, row.names = FALSE)
  cat("\nConfusion matrix (k-NN):\n")
  knn_cm <- table(True = true_labels, Predicted = knn_preds)
  print(knn_cm)
  knn_acc <- sum(diag(knn_cm)) / sum(knn_cm)
  cat(sprintf("k-NN Accuracy: %.3f\n", knn_acc))
}

# ---- Naive Bayes ----
if (!requireNamespace("e1071", quietly = TRUE)) {
  cat("\n  e1071 not available. Install: install.packages('e1071')\n")
  nb_preds <- rep(NA, nrow(test_set))
} else {
  library(e1071)
  formula_str <- paste("Result ~", paste(feature_cols, collapse = " + "))
  nb_model    <- naiveBayes(as.formula(formula_str), data = train_set)
  nb_preds    <- predict(nb_model, test_set[, feature_cols])

  cat("\n--- Naive Bayes ---\n")
  pred_df_nb <- data.frame(
    Name    = test_set$Name,
    True    = true_labels,
    NB      = nb_preds,
    Correct = ifelse(true_labels == nb_preds, "YES", "NO"),
    stringsAsFactors = FALSE
  )
  print(pred_df_nb, row.names = FALSE)
  cat("\nConfusion matrix (Naive Bayes):\n")
  nb_cm  <- table(True = true_labels, Predicted = nb_preds)
  print(nb_cm)
  nb_acc <- sum(diag(nb_cm)) / sum(nb_cm)
  cat(sprintf("Naive Bayes Accuracy: %.3f\n", nb_acc))
}

# ---- Comparison ----
cat("\n--- Classifier Comparison ---\n\n")
comp_data <- data.frame(
  Classifier = c("k-NN (k=3)", "Naive Bayes"),
  Accuracy   = c(
    if (!anyNA(knn_preds)) round(sum(diag(table(true_labels, knn_preds))) / length(true_labels), 3) else NA,
    if (!anyNA(nb_preds))  round(sum(diag(table(true_labels, nb_preds)))  / length(true_labels), 3) else NA
  ),
  stringsAsFactors = FALSE
)
print(comp_data, row.names = FALSE)

# ---- Recommendation ----
cat("\n--- Recommendation for Early Warning System ---\n\n")
cat("  Both k-NN and Naive Bayes are suitable for this problem.\n")
cat("  Key considerations:\n")
cat("  - k-NN: no explicit training phase; requires all data at prediction time;\n")
cat("    good when student profiles cluster tightly by outcome.\n")
cat("  - Naive Bayes: fast, probabilistic, gives confidence scores;\n")
cat("    easier to explain to non-technical school staff.\n")
cat("  - Monitor FALSE NEGATIVES (failing students predicted as passing)\n")
cat("    -- these are the most costly errors for an early-warning system.\n")
cat("  - Recommendation: use Naive Bayes for daily early-warning with k-NN\n")
cat("    as a secondary check when a student is near the decision boundary.\n")

cat("\n")
cat(strrep("=", 65), "\n")
cat("  Student Performance Predictor (R) finished.\n")
cat("  All 7 phases (Ch1-Ch7) executed successfully.\n")
cat(strrep("=", 65), "\n\n")
