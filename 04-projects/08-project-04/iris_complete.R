# =============================================================================
# Project 04: The Iris Complete Walkthrough (R Version)
# Chapter 8 - Final Projects (Capstone)
# Data Analytics Course
#
# Applies EVERY technique from Chapters 1-7 to the built-in iris dataset
# (all 150 rows) using base R with optional packages.
#
# Phases:
#   1  (Ch1)  Dataset profiling & attribute types
#   2  (Ch2)  Univariate statistics
#   3  (Ch3)  Multivariate statistics & correlation
#   4  (Ch4)  Preprocessing: missing values & normalisation
#   5  (Ch5)  Clustering: K-means + elbow
#   6  (Ch6)  Frequent pattern mining (arules, optional)
#   7  (Ch7)  Classification: knn + naiveBayes + evaluation
#
# Required packages (install once):
#   install.packages(c("class", "e1071", "arules"))
#
# Run: Rscript iris_complete.R
#      or source("iris_complete.R") in RStudio
# =============================================================================

cat(strrep("=", 65), "\n")
cat("  Iris Complete Walkthrough -- R\n")
cat(strrep("=", 65), "\n\n")

# Helper to print phase headers
print_phase <- function(num, chapter, title) {
  cat("\n")
  cat(strrep("=", 65), "\n")
  cat(sprintf("=== PHASE %d (Ch%d): %s ===\n", num, chapter, title))
  cat(strrep("=", 65), "\n\n")
}


# =============================================================================
# PHASE 1 (Ch1): DATASET PROFILING
# =============================================================================
print_phase(1, 1, "DATASET PROFILING")

# Use the built-in iris dataset (150 rows, 5 columns)
data(iris)

cat("--- Structure ---\n")
str(iris)

cat("\n--- Column classes ---\n")
print(sapply(iris, class))

cat("\n--- Attribute scale types ---\n")
attr_info <- data.frame(
  Attribute  = c("Sepal.Length", "Sepal.Width", "Petal.Length",
                 "Petal.Width", "Species"),
  Scale      = c("Ratio", "Ratio", "Ratio", "Ratio", "Nominal"),
  Disc_Cont  = c("Continuous", "Continuous", "Continuous",
                 "Continuous", "Discrete"),
  stringsAsFactors = FALSE
)
print(attr_info, row.names = FALSE)

cat("\n--- Dataset summary ---\n")
cat(sprintf("Total objects    : %d\n", nrow(iris)))
cat(sprintf("Numeric attributes: %d\n", 4))
cat(sprintf("Class attribute  : Species (Nominal)\n\n"))

cat("Class distribution:\n")
species_counts <- table(iris$Species)
species_rel    <- prop.table(species_counts)
for (sp in names(species_counts)) {
  cat(sprintf("  %-14s  %3d rows  (%.1f%%)\n",
              sp, species_counts[sp], species_rel[sp] * 100))
}


# =============================================================================
# PHASE 2 (Ch2): UNIVARIATE STATISTICS
# =============================================================================
print_phase(2, 2, "UNIVARIATE STATISTICS")

cat("--- Summary statistics per numeric attribute ---\n\n")
# apply summary across all 4 numeric columns
print(apply(iris[, 1:4], 2, summary))

cat("\n--- Standard deviation per attribute ---\n")
print(apply(iris[, 1:4], 2, sd))

cat("\n--- Skewness sign (mean vs median) ---\n")
for (col in names(iris)[1:4]) {
  m   <- mean(iris[[col]])
  med <- median(iris[[col]])
  sign <- if (m > med) "right-skewed" else if (m < med) "left-skewed" else "symmetric"
  cat(sprintf("  %-14s  mean=%.3f  median=%.3f  -> %s\n", col, m, med, sign))
}

cat("\n--- IQR per attribute ---\n")
for (col in names(iris)[1:4]) {
  q1  <- quantile(iris[[col]], 0.25)
  q3  <- quantile(iris[[col]], 0.75)
  cat(sprintf("  %-14s  Q1=%.3f  Q3=%.3f  IQR=%.3f\n", col, q1, q3, q3 - q1))
}

cat("\n--- Species frequency table ---\n")
freq_table <- data.frame(
  Species  = names(species_counts),
  Count    = as.integer(species_counts),
  Rel_Freq = round(as.numeric(species_rel), 4),
  stringsAsFactors = FALSE
)
print(freq_table, row.names = FALSE)

cat("\n--- Boxplot (saved to iris_boxplot.png if possible) ---\n")
tryCatch({
  png("iris_boxplot.png", width = 600, height = 400)
  boxplot(iris[, 1:4],
          main  = "Iris: Boxplots of Numeric Attributes",
          col   = c("#AED6F1","#A9DFBF","#F9E79F","#F5CBA7"),
          notch = FALSE,
          las   = 2)
  dev.off()
  cat("  Saved iris_boxplot.png\n")
}, error = function(e) {
  cat("  (boxplot skipped in non-graphic environment)\n")
})


# =============================================================================
# PHASE 3 (Ch3): MULTIVARIATE STATISTICS
# =============================================================================
print_phase(3, 3, "MULTIVARIATE STATISTICS")

cat("--- 4x4 Pearson Correlation Matrix ---\n\n")
corr_mat <- cor(iris[, 1:4])
print(round(corr_mat, 3))

cat("\n--- Location matrix (min / mean / max per attribute) ---\n\n")
loc_mat <- rbind(
  Min  = apply(iris[, 1:4], 2, min),
  Mean = apply(iris[, 1:4], 2, mean),
  Max  = apply(iris[, 1:4], 2, max)
)
print(round(loc_mat, 3))

cat("\n--- Pairs scatter plot (saved to iris_pairs.png if possible) ---\n")
tryCatch({
  png("iris_pairs.png", width = 700, height = 700)
  pairs(iris[, 1:4],
        col  = as.integer(iris$Species),
        pch  = 19,
        main = "Iris: Pairs Plot (1=setosa, 2=versicolor, 3=virginica)")
  dev.off()
  cat("  Saved iris_pairs.png\n")
}, error = function(e) {
  cat("  (pairs plot skipped)\n")
})

# Optional corrplot
if (requireNamespace("corrplot", quietly = TRUE)) {
  library(corrplot)
  tryCatch({
    png("iris_corrplot.png", width = 500, height = 500)
    corrplot(corr_mat, method = "color", addCoef.col = "black", tl.cex = 0.9)
    dev.off()
    cat("  Saved iris_corrplot.png (corrplot package)\n")
  }, error = function(e) {
    cat("  (corrplot skipped)\n")
  })
} else {
  cat("  corrplot package not installed -- skipping corrplot.\n")
}

cat("\n--- Top correlations ---\n")
corr_long <- data.frame(
  Col1 = character(), Col2 = character(), r = numeric(),
  stringsAsFactors = FALSE
)
num_cols <- names(iris)[1:4]
for (i in 1:(length(num_cols) - 1)) {
  for (j in (i + 1):length(num_cols)) {
    corr_long <- rbind(corr_long, data.frame(
      Col1 = num_cols[i], Col2 = num_cols[j],
      r    = corr_mat[i, j],
      stringsAsFactors = FALSE
    ))
  }
}
corr_long <- corr_long[order(-abs(corr_long$r)), ]
print(head(corr_long, 6), row.names = FALSE)


# =============================================================================
# PHASE 4 (Ch4): PREPROCESSING
# =============================================================================
print_phase(4, 4, "PREPROCESSING")

# Work on a copy
iris_work <- iris

cat("--- Step 4a: Inject 2 missing values ---\n")
iris_work[6,  "Sepal.Width"]  <- NA
iris_work[16, "Petal.Length"] <- NA
cat("  Set row  6 Sepal.Width  = NA\n")
cat("  Set row 16 Petal.Length = NA\n")

cat("\n--- Step 4b: Detect missing values ---\n")
missing_positions <- which(is.na(iris_work), arr.ind = TRUE)
for (i in 1:nrow(missing_positions)) {
  r <- missing_positions[i, "row"]
  c <- missing_positions[i, "col"]
  cat(sprintf("  Missing at row %2d, col '%s'  (Species: %s)\n",
              r, names(iris_work)[c], iris_work$Species[r]))
}

cat("\n--- Step 4c: Impute with per-species column mean ---\n")
for (col in names(iris_work)[1:4]) {
  na_rows <- which(is.na(iris_work[[col]]))
  for (r in na_rows) {
    sp   <- iris_work$Species[r]
    vals <- iris_work[[col]][iris_work$Species == sp & !is.na(iris_work[[col]])]
    fill <- mean(vals)
    iris_work[r, col] <- fill
    cat(sprintf("  Imputed row %2d '%s' (%s) with species mean: %.3f\n",
                r, col, sp, fill))
  }
}

cat("\n--- Step 4d: Min-max normalisation ---\n")
cat("  3 sample rows BEFORE normalisation:\n")
print(iris_work[c(1, 51, 101), ], row.names = TRUE)

iris_norm <- iris_work
for (col in names(iris_norm)[1:4]) {
  mn <- min(iris_norm[[col]])
  mx <- max(iris_norm[[col]])
  iris_norm[[col]] <- (iris_norm[[col]] - mn) / (mx - mn)
}

cat("\n  3 sample rows AFTER normalisation [0, 1]:\n")
tmp <- iris_norm[c(1, 51, 101), ]
tmp[, 1:4] <- round(tmp[, 1:4], 4)
print(tmp, row.names = TRUE)


# =============================================================================
# PHASE 5 (Ch5): CLUSTERING (K-MEANS)
# =============================================================================
print_phase(5, 5, "CLUSTERING (K-MEANS)")

set.seed(42)

cat("--- K-means with K=3 on (Petal.Length, Petal.Width) [normalised] ---\n\n")
km3 <- kmeans(iris_norm[, 3:4], centers = 3, nstart = 20)

cat("Cluster sizes:\n")
print(km3$size)
cat("\nCluster centroids (in normalised space):\n")
print(round(km3$centers, 4))

cat("\n--- Cluster vs true species cross-table ---\n")
cluster_vs_species <- table(Cluster = km3$cluster, Species = iris_norm$Species)
print(cluster_vs_species)

# Purity
total_correct <- 0
for (cl in rownames(cluster_vs_species)) {
  total_correct <- total_correct + max(cluster_vs_species[cl, ])
}
purity <- total_correct / nrow(iris_norm)
cat(sprintf("\nCluster purity (K=3): %.3f\n", purity))

# Mini elbow
cat("\n--- Mini elbow analysis (SSE vs K) ---\n")
for (k_val in 2:5) {
  km_k <- kmeans(iris_norm[, 3:4], centers = k_val, nstart = 20)
  cat(sprintf("  K=%d  SSE (tot.withinss) = %.4f\n", k_val, km_k$tot.withinss))
}

# Cluster plot saved to file
tryCatch({
  png("iris_cluster.png", width = 600, height = 500)
  plot(iris_norm$Petal.Length, iris_norm$Petal.Width,
       col  = km3$cluster,
       pch  = as.integer(iris_norm$Species),
       main = "K-means (K=3) on Normalised PetalLength vs PetalWidth",
       xlab = "PetalLength (norm)",
       ylab = "PetalWidth  (norm)")
  points(km3$centers, col = 1:3, pch = 8, cex = 2, lwd = 2)
  legend("topleft",
         legend = c("Cluster 1", "Cluster 2", "Cluster 3"),
         col = 1:3, pch = 19, bty = "n")
  dev.off()
  cat("\n  Saved iris_cluster.png\n")
}, error = function(e) {
  cat("  (cluster plot skipped)\n")
})


# =============================================================================
# PHASE 6 (Ch6): FREQUENT PATTERN MINING
# =============================================================================
print_phase(6, 6, "FREQUENT PATTERN MINING")

if (!requireNamespace("arules", quietly = TRUE)) {
  cat("  arules package not installed.\n")
  cat("  Install with: install.packages('arules')\n")
  cat("  Skipping Phase 6.\n")
} else {
  library(arules)

  # Discretise using the ORIGINAL iris (not normalised)
  cat("--- Discretising Petal.Length and Petal.Width ---\n\n")
  iris_disc <- iris  # original 150-row dataset

  iris_disc$PL_bin <- cut(iris_disc$Petal.Length,
                           breaks = c(-Inf, 2, 5, Inf),
                           labels = c("PL_short", "PL_medium", "PL_long"),
                           right  = TRUE)

  iris_disc$PW_bin <- cut(iris_disc$Petal.Width,
                           breaks = c(-Inf, 0.5, 1.5, Inf),
                           labels = c("PW_narrow", "PW_medium", "PW_wide"),
                           right  = TRUE)

  iris_disc$SP_label <- paste0("SP_", iris_disc$Species)

  print(table(iris_disc$PL_bin))
  print(table(iris_disc$PW_bin))

  # Build transactions
  trans_cols <- iris_disc[, c("PL_bin", "PW_bin", "SP_label")]
  trans_cols[] <- lapply(trans_cols, as.factor)
  transactions_obj <- as(trans_cols, "transactions")

  cat(sprintf("\nTransactions: %d\n\n", length(transactions_obj)))

  # Apriori: min_support=5/150, min_confidence=0.6
  min_sup_frac <- 5 / nrow(iris_disc)
  rules <- apriori(transactions_obj,
                   parameter = list(supp = min_sup_frac,
                                    conf = 0.6,
                                    minlen = 2,
                                    target = "rules"),
                   control = list(verbose = FALSE))

  cat("--- Frequent itemsets (support >= 5 out of 150) ---\n")
  freq_sets <- apriori(transactions_obj,
                       parameter = list(supp   = min_sup_frac,
                                        target = "frequent itemsets",
                                        minlen = 1),
                       control = list(verbose = FALSE))
  inspect(sort(freq_sets, by = "count", decreasing = TRUE))

  cat("\n--- Association rules (confidence >= 0.6) ---\n")
  inspect(sort(rules, by = "confidence", decreasing = TRUE))
}


# =============================================================================
# PHASE 7 (Ch7): CLASSIFICATION + EVALUATION
# =============================================================================
print_phase(7, 7, "CLASSIFICATION + EVALUATION")

# Use normalised data (iris_norm) with 80/20 split via set.seed(42)
set.seed(42)
n <- nrow(iris_norm)
train_idx <- sample(1:n, size = floor(0.8 * n), replace = FALSE)
train_set <- iris_norm[ train_idx, ]
test_set  <- iris_norm[-train_idx, ]

cat(sprintf("Train: %d rows  |  Test: %d rows\n\n", nrow(train_set), nrow(test_set)))

true_labels <- test_set$Species

# ---- k-NN ----
if (!requireNamespace("class", quietly = TRUE)) {
  cat("  class package not available. Install with: install.packages('class')\n")
  cat("  Skipping k-NN.\n")
  knn_preds <- rep(NA, nrow(test_set))
} else {
  library(class)
  knn_preds <- knn(train = train_set[, 1:4],
                   test  = test_set[, 1:4],
                   cl    = train_set$Species,
                   k     = 3)
  cat("--- k-NN (k=3) ---\n")
  cat("Predictions:\n")
  pred_df <- data.frame(True = true_labels, kNN_pred = knn_preds,
                        Correct = ifelse(true_labels == knn_preds, "YES", "NO"))
  print(pred_df)
  cat("\nConfusion matrix (k-NN):\n")
  knn_cm <- table(True = true_labels, Predicted = knn_preds)
  print(knn_cm)
  knn_acc <- sum(diag(knn_cm)) / sum(knn_cm)
  cat(sprintf("\nk-NN Accuracy: %.3f\n", knn_acc))
}

# ---- Naive Bayes ----
if (!requireNamespace("e1071", quietly = TRUE)) {
  cat("\n  e1071 package not available. Install with: install.packages('e1071')\n")
  cat("  Skipping Naive Bayes.\n")
  nb_preds <- rep(NA, nrow(test_set))
} else {
  library(e1071)
  nb_model <- naiveBayes(Species ~ ., data = train_set[, c(1:4, 5)])
  nb_preds <- predict(nb_model, test_set[, 1:4])

  cat("\n--- Naive Bayes ---\n")
  cat("Predictions:\n")
  pred_df_nb <- data.frame(True = true_labels, NB_pred = nb_preds,
                            Correct = ifelse(true_labels == nb_preds, "YES", "NO"))
  print(pred_df_nb)
  cat("\nConfusion matrix (Naive Bayes):\n")
  nb_cm <- table(True = true_labels, Predicted = nb_preds)
  print(nb_cm)
  nb_acc <- sum(diag(nb_cm)) / sum(nb_cm)
  cat(sprintf("\nNaive Bayes Accuracy: %.3f\n", nb_acc))
}

# Optional: caret confusionMatrix for detailed metrics
if (requireNamespace("caret", quietly = TRUE)) {
  library(caret)
  cat("\n--- Detailed metrics (caret) ---\n")
  if (!anyNA(knn_preds)) {
    cat("\nk-NN:\n")
    print(confusionMatrix(knn_preds, true_labels))
  }
  if (!anyNA(nb_preds)) {
    cat("\nNaive Bayes:\n")
    print(confusionMatrix(nb_preds, true_labels))
  }
} else {
  cat("\n  (install caret for detailed precision/recall/F1 per class)\n")
}

# ---- Comparison summary ----
cat("\n--- Classifier Comparison ---\n\n")
comp_df <- data.frame(
  Classifier = c("k-NN (k=3)", "Naive Bayes"),
  Accuracy   = c(
    if (!anyNA(knn_preds)) round(sum(diag(table(true_labels, knn_preds))) / length(true_labels), 3) else NA,
    if (!anyNA(nb_preds))  round(sum(diag(table(true_labels, nb_preds)))  / length(true_labels), 3) else NA
  ),
  stringsAsFactors = FALSE
)
print(comp_df, row.names = FALSE)

cat("\n")
cat(strrep("=", 65), "\n")
cat("  Iris Complete Walkthrough (R) finished.\n")
cat("  All 7 phases (Ch1-Ch7) executed successfully.\n")
cat(strrep("=", 65), "\n\n")
