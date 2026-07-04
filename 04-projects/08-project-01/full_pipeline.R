# full_pipeline.R
# Project 01 -- End-to-End Data Pipeline
# Chapters: Ch4 (preprocessing) + Ch2/Ch3 (stats) + Ch5 (clustering) + Ch7 (classification)

# Install required packages if missing:
# install.packages("e1071")

library(e1071)

cat("============================================================\n")
cat("  END-TO-END DATA PIPELINE (R)\n")
cat("  Chapters: Ch2, Ch3, Ch4, Ch5, Ch7\n")
cat("============================================================\n\n")

# ============================================================
# RAW DATASET (with missing value and duplicate)
# ============================================================
raw_friends <- data.frame(
  Friend   = c("Andrew","Bernhard","Carolina","Dennis","Eve","Fred","Gwyneth",
               "Hayden","Irene","James","Kevin","Lea","Marcus","Nigel","Andrew"),
  Max_temp = c(25, 31, 15, 20, 10, 12, 16, 26, 15, 21, 30, 13,  8, 12, 25),
  Weight   = c(77,110, 70, 85, NA, 75, 75, 63, 55, 66, 95, 72, 83,115, 77),
  Height   = c(175,195,172,180,168,173,180,165,158,163,190,172,185,192,175),
  Years    = c(10, 12,  2, 16,  0,  6,  3,  2,  5, 14,  1, 11,  3, 15, 10),
  Gender   = c("M","M","F","M","F","M","F","F","F","M","M","F","F","M","M"),
  Company  = c("Good","Good","Bad","Good","Bad","Good","Bad","Bad","Bad","Good",
               "Bad","Good","Bad","Good","Good"),
  stringsAsFactors = FALSE
)

# ============================================================
# STEP 1 (Ch4): DATA QUALITY AUDIT
# ============================================================
cat("==========================================================\n")
cat("  STEP 1: DATA QUALITY AUDIT (Ch4)\n")
cat("==========================================================\n")

missing_count <- sum(is.na(raw_friends))
cat("Missing values detected:", missing_count, "\n")
missing_where <- which(is.na(raw_friends), arr.ind = TRUE)
if (nrow(missing_where) > 0) {
  for (i in seq_len(nrow(missing_where))) {
    row_i <- missing_where[i, "row"]
    col_i <- missing_where[i, "col"]
    cat("  Row:", raw_friends$Friend[row_i],
        "| Column:", colnames(raw_friends)[col_i], "\n")
  }
}

dup_mask <- duplicated(raw_friends)
dup_count <- sum(dup_mask)
cat("Duplicate rows detected:", dup_count, "\n")
if (dup_count > 0) {
  cat("  Duplicate row indices:", which(dup_mask), "\n")
}

# ============================================================
# STEP 2 (Ch4): CLEAN DATA
# ============================================================
cat("\n==========================================================\n")
cat("  STEP 2: CLEAN DATA (Ch4)\n")
cat("==========================================================\n")

# Fill missing Weight with gender-group mean
female_weights <- raw_friends$Weight[raw_friends$Gender == "F" & !is.na(raw_friends$Weight)]
female_mean_weight <- round(mean(female_weights), 1)
cat("Female group mean weight:", female_mean_weight, "\n")

friends <- raw_friends
friends$Weight[is.na(friends$Weight)] <- female_mean_weight
cat("Filled Eve Weight with:", female_mean_weight, "\n")

# Remove duplicates
friends <- friends[!duplicated(friends), ]
cat("Removed", dup_count, "duplicate row(s).\n")
cat("Dataset size after cleaning:", nrow(friends), "rows\n")

# Convert columns to correct types
numeric_cols <- c("Max_temp", "Weight", "Height", "Years")

# ============================================================
# STEP 3 (Ch2): UNIVARIATE STATISTICS
# ============================================================
cat("\n==========================================================\n")
cat("  STEP 3: UNIVARIATE STATISTICS (Ch2)\n")
cat("==========================================================\n")

cat(sprintf("%-12s %8s %8s %8s %8s %8s\n", "Column", "Mean", "Median", "Std", "Q1", "Q3"))
cat(strrep("-", 56), "\n")

for (col in numeric_cols) {
  vals <- friends[[col]]
  col_mean   <- round(mean(vals), 3)
  col_median <- round(median(vals), 3)
  col_std    <- round(sd(vals), 3)
  col_q1     <- round(quantile(vals, 0.25), 3)
  col_q3     <- round(quantile(vals, 0.75), 3)
  cat(sprintf("%-12s %8.3f %8.3f %8.3f %8.3f %8.3f\n",
              col, col_mean, col_median, col_std, col_q1, col_q3))
}

# ============================================================
# STEP 4 (Ch3): PEARSON CORRELATION MATRIX
# ============================================================
cat("\n==========================================================\n")
cat("  STEP 4: PEARSON CORRELATION MATRIX (Ch3)\n")
cat("==========================================================\n")

num_data <- friends[, numeric_cols]
corr_matrix <- cor(num_data)
print(round(corr_matrix, 3))

# ============================================================
# STEP 5 (Ch4): MIN-MAX NORMALIZATION
# ============================================================
cat("\n==========================================================\n")
cat("  STEP 5: NORMALIZATION (Ch4) -- Min-Max to [0,1]\n")
cat("==========================================================\n")

norm_params <- list()
friends_norm <- friends

for (col in numeric_cols) {
  vals <- friends[[col]]
  mn <- min(vals)
  mx <- max(vals)
  norm_params[[col]] <- list(min = mn, max = mx)
  if (mx > mn) {
    friends_norm[[col]] <- (vals - mn) / (mx - mn)
  } else {
    friends_norm[[col]] <- rep(0, length(vals))
  }
  cat("  Normalized", col, ": min =", mn, ", max =", mx, "\n")
}

# ============================================================
# STEP 6 (Ch5): K-MEANS CLUSTERING K=2
# ============================================================
cat("\n==========================================================\n")
cat("  STEP 6: K-MEANS CLUSTERING K=2 (Ch5)\n")
cat("==========================================================\n")

set.seed(42)
km_data <- friends_norm[, numeric_cols]
km_result <- kmeans(km_data, centers = 2, nstart = 10, iter.max = 100)

friends_norm$Cluster <- km_result$cluster
friends$Cluster <- km_result$cluster

for (k in 1:2) {
  members <- friends$Friend[friends$Cluster == k]
  cat("  Cluster", k, ":", paste(members, collapse = ", "), "\n")
}

cat("\n  Cluster centroids (normalized):\n")
print(round(km_result$centers, 3))

# Plot clusters (Age vs Years, colored by cluster)
plot(friends_norm$Max_temp, friends_norm$Years,
     col = km_result$cluster,
     pch = 19,
     main = "K-Means Clusters (K=2): Max_temp vs Years (normalized)",
     xlab = "Max_temp (normalized)",
     ylab = "Years (normalized)")
legend("topright", legend = c("Cluster 1", "Cluster 2"),
       col = 1:2, pch = 19)

# ============================================================
# STEP 7 (Ch7): NAIVE BAYES CLASSIFICATION
# ============================================================
cat("\n==========================================================\n")
cat("  STEP 7: NAIVE BAYES CLASSIFICATION (Ch7)\n")
cat("==========================================================\n")

# Use normalized data + encoded Gender for Naive Bayes
friends_norm$Gender_num <- ifelse(friends_norm$Gender == "M", 1, 0)
friends_norm$Company    <- friends$Company

# Train Naive Bayes on full cleaned dataset
train_features <- friends_norm[, c("Max_temp", "Weight", "Height", "Years", "Gender_num")]
train_labels   <- as.factor(friends_norm$Company)

nb_model <- naiveBayes(train_features, train_labels)

# Two new synthetic objects
new_objects <- data.frame(
  Max_temp   = c(22, 11),
  Weight     = c(80, 60),
  Height     = c(178, 162),
  Years      = c(9, 1),
  Gender_num = c(1, 0)   # M=1, F=0
)

# Normalize new objects using training params
for (col in numeric_cols) {
  mn <- norm_params[[col]]$min
  mx <- norm_params[[col]]$max
  if (mx > mn) {
    new_objects[[col]] <- (new_objects[[col]] - mn) / (mx - mn)
  } else {
    new_objects[[col]] <- 0
  }
}

preds <- predict(nb_model, new_objects)
pred_probs <- predict(nb_model, new_objects, type = "raw")

cat("  Naive Bayes predictions for new objects:\n")
new_names <- c("NewPerson1 (M, warm, heavy)", "NewPerson2 (F, cold, light)")
for (i in seq_along(preds)) {
  cat("  ", new_names[i], "->", as.character(preds[i]),
      "| Posteriors: Good =", round(pred_probs[i, "Good"], 3),
      ", Bad =", round(pred_probs[i, "Bad"], 3), "\n")
}

# ============================================================
# STEP 8: FINAL REPORT SUMMARY
# ============================================================
cat("\n==========================================================\n")
cat("  STEP 8: FINAL REPORT SUMMARY\n")
cat("==========================================================\n")

cat("  [Step 1] Raw rows:", nrow(raw_friends),
    "| Missing:", sum(is.na(raw_friends)),
    "| Duplicates:", dup_count, "\n")
cat("  [Step 2] Cleaned rows:", nrow(friends), "\n")
cat("  [Step 3] Key stats:\n")
for (col in numeric_cols) {
  cat("           ", col, ": mean =", round(mean(friends[[col]]), 2),
      ", std =", round(sd(friends[[col]]), 2), "\n")
}
cat("  [Step 6] Cluster sizes:", table(km_result$cluster), "\n")
cat("  [Step 7] Predictions:\n")
for (i in seq_along(preds)) {
  cat("           ", new_names[i], "->", as.character(preds[i]), "\n")
}

cat("\nDone.\n")
