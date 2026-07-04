# =============================================================================
# knn_naive_bayes.R
# Project 07-03-02: k-NN and Naive Bayes (R)
# =============================================================================
# Uses:
#   class   package -> knn() for k-Nearest Neighbor
#   e1071   package -> naiveBayes() for Naive Bayes
#
# Install with:
#   install.packages(c("class", "e1071"))
# =============================================================================


# =============================================================================
# PART 0: Load packages
# =============================================================================

# Check if packages are available; install if missing
if (!requireNamespace("class", quietly = TRUE)) {
  install.packages("class")
}
if (!requireNamespace("e1071", quietly = TRUE)) {
  install.packages("e1071")
}

library(class)    # for knn()
library(e1071)    # for naiveBayes()


# =============================================================================
# PART 1: Friends Classification Dataset
# =============================================================================

cat("=============================================================\n")
cat("Friends Classification Dataset\n")
cat("=============================================================\n\n")

# Build the friends dataset as a data frame
friends_df <- data.frame(
  Food     = c("chinese", "italian", "italian", "burgers", "chinese",
               "chinese", "burgers", "chinese", "italian"),
  Age      = c(51, 43, 82, 23, 46, 29, 42, 38, 31),
  Distance = c("close", "very_close", "close", "far", "very_far",
               "too_far", "very_far", "close", "far"),
  Company  = c("good", "good", "good", "bad", "good",
               "bad", "good", "bad", "good"),
  stringsAsFactors = TRUE
)

cat("Training data:\n")
print(friends_df)
cat("\n")
cat("Dimensions:", nrow(friends_df), "rows x", ncol(friends_df), "columns\n")
cat("Class distribution:\n")
print(table(friends_df$Company))
cat("\n")


# =============================================================================
# PART 2: k-NN on Friends Dataset (numeric features only)
# =============================================================================

cat("=============================================================\n")
cat("PART 2: k-NN on Friends Dataset\n")
cat("=============================================================\n\n")

# For k-NN we use numeric features only.
# Here: Age is the only numeric feature.
# Min-Max normalize it.
age_min  <- min(friends_df$Age)
age_max  <- max(friends_df$Age)
friends_df$Age_norm <- (friends_df$Age - age_min) / (age_max - age_min)

cat("Normalized Age values:\n")
print(friends_df[, c("Age", "Age_norm", "Company")])
cat("\n")

# Training matrix: just normalized Age
train_x <- as.matrix(friends_df[, "Age_norm", drop = FALSE])
train_y <- friends_df$Company

# Define two test objects
test_ages_raw <- c(40, 65)
test_ages_norm <- (test_ages_raw - age_min) / (age_max - age_min)
test_x <- matrix(test_ages_norm, ncol = 1)
colnames(test_x) <- "Age_norm"

cat("Test objects (raw age -> normalized):\n")
for (i in seq_along(test_ages_raw)) {
  cat(sprintf("  Test %d: age=%d -> norm=%.4f\n", i, test_ages_raw[i], test_ages_norm[i]))
}
cat("\n")

# Run k-NN for k = 1, 3, 5
for (k_val in c(1, 3, 5)) {
  # Set seed for reproducible tie-breaking
  set.seed(42)
  pred <- knn(train  = train_x,
              test   = test_x,
              cl     = train_y,
              k      = k_val)
  cat(sprintf("k=%d predictions: Test1=%s, Test2=%s\n",
              k_val, as.character(pred[1]), as.character(pred[2])))
}
cat("\n")


# =============================================================================
# PART 3: k-NN on Iris Dataset
# =============================================================================

cat("=============================================================\n")
cat("PART 3: k-NN on Iris Dataset\n")
cat("=============================================================\n\n")

# Load the Iris dataset (built-in)
data(iris)
cat("Iris dataset: first 6 rows\n")
print(head(iris))
cat("\nClass distribution:\n")
print(table(iris$Species))
cat("\n")

# Split into 80% train / 20% test (using fixed indices for reproducibility)
set.seed(42)
n_iris    <- nrow(iris)
test_size <- floor(0.2 * n_iris)
test_idx  <- sample(1:n_iris, test_size)
train_idx <- setdiff(1:n_iris, test_idx)

# Normalize numeric features (columns 1-4) using training min/max
iris_features <- as.matrix(iris[, 1:4])
train_min <- apply(iris_features[train_idx, ], 2, min)
train_max <- apply(iris_features[train_idx, ], 2, max)

# Function to normalize using training statistics
normalize_matrix <- function(mat, col_min, col_max) {
  result <- mat
  for (j in 1:ncol(mat)) {
    if (col_max[j] != col_min[j]) {
      result[, j] <- (mat[, j] - col_min[j]) / (col_max[j] - col_min[j])
    } else {
      result[, j] <- 0
    }
  }
  return(result)
}

iris_norm <- normalize_matrix(iris_features, train_min, train_max)

train_x_iris <- iris_norm[train_idx, ]
test_x_iris  <- iris_norm[test_idx,  ]
train_y_iris <- iris$Species[train_idx]
test_y_iris  <- iris$Species[test_idx]

# k-NN with k=5
set.seed(42)
pred_iris_knn <- knn(train = train_x_iris,
                     test  = test_x_iris,
                     cl    = train_y_iris,
                     k     = 5)

# Confusion matrix
cat("k-NN (k=5) on Iris — Confusion Matrix:\n")
cm_iris_knn <- table(Predicted = pred_iris_knn, Actual = test_y_iris)
print(cm_iris_knn)

# Accuracy
acc_iris_knn <- sum(diag(cm_iris_knn)) / sum(cm_iris_knn)
cat(sprintf("\nAccuracy: %.1f%%\n\n", acc_iris_knn * 100))


# =============================================================================
# PART 4: Naive Bayes on Friends Dataset
# =============================================================================

cat("=============================================================\n")
cat("PART 4: Naive Bayes on Friends Dataset\n")
cat("=============================================================\n\n")

# Train Naive Bayes using Food and Distance as predictors
nb_model_friends <- naiveBayes(Company ~ Food + Distance, data = friends_df)

cat("Naive Bayes model — prior probabilities:\n")
print(nb_model_friends$apriori)
cat("\n")

cat("Conditional probability tables:\n")
print(nb_model_friends$tables)
cat("\n")

# Predict on the training data (leave-one-out would be better, but this demos the function)
pred_friends_nb <- predict(nb_model_friends, newdata = friends_df[, c("Food", "Distance")])
cat("Predictions on training data:\n")
result_df <- data.frame(
  Food     = friends_df$Food,
  Distance = friends_df$Distance,
  Actual   = friends_df$Company,
  Predicted = pred_friends_nb
)
print(result_df)

# Training accuracy (optimistic — same data used to train)
acc_friends_nb <- mean(pred_friends_nb == friends_df$Company)
cat(sprintf("\nTraining accuracy: %.1f%%\n", acc_friends_nb * 100))
cat("(Note: training accuracy is optimistic — use cross-validation for real evaluation)\n\n")

# Predict two new test objects
test_new <- data.frame(
  Food     = c("chinese", "italian"),
  Distance = c("close",   "very_close"),
  stringsAsFactors = TRUE
)
cat("Predictions for new objects:\n")
print(test_new)
new_preds    <- predict(nb_model_friends, newdata = test_new)
new_probs    <- predict(nb_model_friends, newdata = test_new, type = "raw")
cat("Predicted classes:\n")
print(new_preds)
cat("Posterior probabilities:\n")
print(round(new_probs, 4))
cat("\n")


# =============================================================================
# PART 5: Naive Bayes on Iris Dataset
# =============================================================================

cat("=============================================================\n")
cat("PART 5: Naive Bayes on Iris Dataset\n")
cat("=============================================================\n\n")

# Train on training split, evaluate on test split
nb_model_iris <- naiveBayes(Species ~ ., data = iris[train_idx, ])

# Summary of model
cat("Naive Bayes model (Iris) — prior probabilities:\n")
print(nb_model_iris$apriori)
cat("\n")

# Predict on test set
pred_iris_nb <- predict(nb_model_iris, newdata = iris[test_idx, 1:4])

# Confusion matrix
cat("Naive Bayes on Iris — Confusion Matrix:\n")
cm_iris_nb <- table(Predicted = pred_iris_nb, Actual = test_y_iris)
print(cm_iris_nb)

# Accuracy
acc_iris_nb <- sum(diag(cm_iris_nb)) / sum(cm_iris_nb)
cat(sprintf("\nAccuracy: %.1f%%\n\n", acc_iris_nb * 100))


# =============================================================================
# PART 6: Comparison Summary
# =============================================================================

cat("=============================================================\n")
cat("PART 6: Summary Comparison\n")
cat("=============================================================\n\n")

cat("Iris Dataset Results:\n")
cat(sprintf("  k-NN (k=5)   accuracy: %.1f%%\n", acc_iris_knn * 100))
cat(sprintf("  Naive Bayes  accuracy: %.1f%%\n", acc_iris_nb  * 100))
cat("\n")

cat("Notes:\n")
cat("  - k-NN uses all 4 numeric features (normalized)\n")
cat("  - Naive Bayes uses all 4 numeric features with Gaussian assumption\n")
cat("  - Both use 80/20 train-test split (seed=42)\n")
cat("  - For robust comparison, use k-fold cross-validation (see project-03)\n")
cat("\n")
cat("Done.\n")
