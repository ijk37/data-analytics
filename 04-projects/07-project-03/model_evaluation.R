# =============================================================================
# model_evaluation.R
# Project 07-03-03: Model Evaluation (R)
# =============================================================================
# Uses:
#   caret   package -> confusionMatrix(), trainControl(), train()
#   rpart   package -> decision tree classifier
#   pROC    package -> ROC curve (optional)
#
# Install with:
#   install.packages(c("caret", "rpart"))
#   install.packages("pROC")   # optional
# =============================================================================


# =============================================================================
# PART 0: Load packages
# =============================================================================

if (!requireNamespace("caret", quietly = TRUE)) {
  install.packages("caret")
}
if (!requireNamespace("rpart", quietly = TRUE)) {
  install.packages("rpart")
}

library(caret)
library(rpart)

# Check if pROC is available (optional for ROC curves)
has_pROC <- requireNamespace("pROC", quietly = TRUE)
if (has_pROC) {
  library(pROC)
  cat("pROC package available. ROC curves will be plotted.\n")
} else {
  cat("pROC not installed. ROC curve section will be skipped.\n")
  cat("To install: install.packages('pROC')\n")
}
cat("\n")


# =============================================================================
# PART 1: Manual Confusion Matrix on Sample Predictions
# =============================================================================

cat("=============================================================\n")
cat("PART 1: Manual Confusion Matrix (good/bad)\n")
cat("=============================================================\n\n")

# Sample predictions
true_labels <- c("good", "good", "good", "bad",  "good",
                 "bad",  "good", "bad",  "good", "bad",
                 "good", "bad",  "good", "good", "bad")
pred_labels <- c("good", "good", "bad",  "bad",  "good",
                 "good", "good", "bad",  "good", "bad",
                 "bad",  "bad",  "good", "good", "good")

# Convert to factors so table() produces a proper 2x2 matrix
true_factor <- factor(true_labels, levels = c("bad", "good"))
pred_factor <- factor(pred_labels, levels = c("bad", "good"))

# Manual confusion matrix using table()
cm_manual <- table(Predicted = pred_factor, Actual = true_factor)
cat("Confusion Matrix (table):\n")
print(cm_manual)
cat("\n")

# Extract TP, FP, FN, TN for positive class = "good"
TP <- cm_manual["good", "good"]
FP <- cm_manual["good", "bad"]
FN <- cm_manual["bad",  "good"]
TN <- cm_manual["bad",  "bad"]

cat(sprintf("For positive class = 'good':\n"))
cat(sprintf("  TP = %d  (predicted good, actually good)\n", TP))
cat(sprintf("  FP = %d  (predicted good, actually bad)\n",  FP))
cat(sprintf("  FN = %d  (predicted bad,  actually good)\n", FN))
cat(sprintf("  TN = %d  (predicted bad,  actually bad)\n",  TN))
cat("\n")

# Compute metrics manually
accuracy  <- (TP + TN) / (TP + TN + FP + FN)
precision <- TP / (TP + FP)
recall    <- TP / (TP + FN)
f1        <- 2 * precision * recall / (precision + recall)

cat("Manual metrics (positive class = good):\n")
cat(sprintf("  Accuracy  = %d / %d = %.4f  (%.1f%%)\n",
            TP + TN, TP + TN + FP + FN, accuracy, accuracy * 100))
cat(sprintf("  Precision = %d / (%d + %d) = %.4f\n", TP, TP, FP, precision))
cat(sprintf("  Recall    = %d / (%d + %d) = %.4f\n", TP, TP, FN, recall))
cat(sprintf("  F1        = 2 * %.4f * %.4f / (%.4f + %.4f) = %.4f\n",
            precision, recall, precision, recall, f1))
cat("\n")


# =============================================================================
# PART 2: caret confusionMatrix() on Sample Predictions
# =============================================================================

cat("=============================================================\n")
cat("PART 2: caret confusionMatrix()\n")
cat("=============================================================\n\n")

# caret::confusionMatrix needs factors with the same levels
cm_caret <- confusionMatrix(
  data      = pred_factor,
  reference = true_factor,
  positive  = "good"
)
print(cm_caret)
cat("\n")


# =============================================================================
# PART 3: Friends Dataset — Decision Tree with Manual Evaluation
# =============================================================================

cat("=============================================================\n")
cat("PART 3: Friends Dataset — rpart + Manual Evaluation\n")
cat("=============================================================\n\n")

# Build Friends dataset
friends_df <- data.frame(
  Food     = c("chinese", "italian", "italian", "burgers", "chinese",
               "chinese", "burgers", "chinese", "italian"),
  Age_bin  = c("old", "middle", "old", "young", "middle",
               "young", "middle", "middle", "young"),
  Distance = c("close", "very_close", "close", "far", "very_far",
               "too_far", "very_far", "close", "far"),
  Company  = c("good", "good", "good", "bad", "good",
               "bad", "good", "bad", "good"),
  stringsAsFactors = TRUE
)

cat("Friends dataset:\n")
print(friends_df)
cat("\n")

# Train a decision tree on all data
friends_tree <- rpart(Company ~ Food + Age_bin + Distance,
                      data   = friends_df,
                      method = "class",
                      control = rpart.control(minsplit = 2, cp = 0.01))

cat("Decision tree structure:\n")
print(friends_tree)
cat("\n")

cat("Variable importance:\n")
if (!is.null(friends_tree$variable.importance)) {
  print(friends_tree$variable.importance)
} else {
  cat("  (no splits made — all examples have the same class, or minsplit not met)\n")
}
cat("\n")

# Predict on training data (note: optimistic accuracy)
friends_pred <- predict(friends_tree, friends_df, type = "class")
cm_friends   <- table(Predicted = friends_pred, Actual = friends_df$Company)
cat("Confusion matrix (train set):\n")
print(cm_friends)
acc_friends <- mean(friends_pred == friends_df$Company)
cat(sprintf("Training accuracy: %.1f%%\n\n", acc_friends * 100))


# =============================================================================
# PART 4: Iris Dataset — 5-Fold CV with rpart
# =============================================================================

cat("=============================================================\n")
cat("PART 4: Iris Dataset — 5-Fold CV with rpart (caret)\n")
cat("=============================================================\n\n")

data(iris)
cat("Iris dataset summary:\n")
cat("  Rows:", nrow(iris), "  Columns:", ncol(iris), "\n")
cat("  Class distribution:\n")
print(table(iris$Species))
cat("\n")

# Set up 5-fold cross-validation control
train_control <- trainControl(
  method    = "cv",       # k-fold cross-validation
  number    = 5,          # k = 5
  verboseIter = FALSE,
  savePredictions = "final"
)

# Train decision tree with 5-fold CV
set.seed(42)
cv_model <- train(
  Species ~ .,
  data      = iris,
  method    = "rpart",
  trControl = train_control,
  metric    = "Accuracy"
)

cat("Cross-validation results:\n")
print(cv_model)
cat("\n")

cat("Best tuning parameter (cp):", cv_model$bestTune$cp, "\n")
cat("CV Accuracy (mean): ", round(max(cv_model$results$Accuracy), 4), "\n\n")

# Confusion matrix from CV predictions
if (!is.null(cv_model$pred)) {
  cv_cm <- confusionMatrix(
    data      = cv_model$pred$pred,
    reference = cv_model$pred$obs
  )
  cat("Confusion Matrix from cross-validation predictions:\n")
  print(cv_cm$table)
  cat(sprintf("\nCV Overall Accuracy: %.4f  (%.1f%%)\n\n",
              cv_cm$overall["Accuracy"],
              cv_cm$overall["Accuracy"] * 100))
}

# Final model on full dataset
final_tree <- cv_model$finalModel
cat("Final tree structure (trained on all data):\n")
print(final_tree)
cat("\n")


# =============================================================================
# PART 5: Per-Fold Accuracy Detail
# =============================================================================

cat("=============================================================\n")
cat("PART 5: Per-Fold CV Results Detail\n")
cat("=============================================================\n\n")

# Extract per-fold results from resamples
resamp <- cv_model$resample
cat("Per-fold accuracy:\n")
for (i in 1:nrow(resamp)) {
  cat(sprintf("  Fold %d: Accuracy = %.4f  (%.1f%%)\n",
              i, resamp$Accuracy[i], resamp$Accuracy[i] * 100))
}
cat(sprintf("\nMean    : %.4f  (%.1f%%)\n", mean(resamp$Accuracy), mean(resamp$Accuracy) * 100))
cat(sprintf("Std Dev : %.4f\n\n", sd(resamp$Accuracy)))


# =============================================================================
# PART 6: ROC Curve (optional, requires pROC)
# =============================================================================

cat("=============================================================\n")
cat("PART 6: ROC Curve (binary Iris subset)\n")
cat("=============================================================\n\n")

if (has_pROC) {
  # Use setosa vs non-setosa (binary problem)
  iris_binary <- iris
  iris_binary$IsSetosa <- ifelse(iris$Species == "setosa", 1, 0)

  # Train logistic model (use rpart probability)
  set.seed(42)
  idx_train <- sample(1:150, 120)
  idx_test  <- setdiff(1:150, idx_train)

  tree_binary <- rpart(
    IsSetosa ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,
    data   = iris_binary[idx_train, ],
    method = "class"
  )
  prob_pred <- predict(tree_binary, iris_binary[idx_test, ], type = "prob")[, "1"]
  actual    <- iris_binary$IsSetosa[idx_test]

  roc_obj <- roc(actual, prob_pred, quiet = TRUE)
  cat(sprintf("AUC (setosa vs rest): %.4f\n", auc(roc_obj)))
  cat("Plotting ROC curve...\n")
  plot(roc_obj,
       main = "ROC Curve: Setosa vs. Non-Setosa",
       col  = "blue",
       lwd  = 2)
  abline(a = 0, b = 1, lty = 2, col = "gray")
} else {
  cat("pROC not installed. Skipping ROC curve.\n")
  cat("Install with: install.packages('pROC')\n")
}
cat("\n")


# =============================================================================
# PART 7: Summary
# =============================================================================

cat("=============================================================\n")
cat("PART 7: Summary\n")
cat("=============================================================\n\n")

cat("Key metrics for binary classification (positive = good):\n")
cat(sprintf("  Accuracy  : %.4f\n", accuracy))
cat(sprintf("  Precision : %.4f\n", precision))
cat(sprintf("  Recall    : %.4f\n", recall))
cat(sprintf("  F1        : %.4f\n", f1))
cat("\n")

cat("Iris 5-fold CV (rpart decision tree):\n")
cat(sprintf("  Mean accuracy : %.4f  (%.1f%%)\n",
            mean(resamp$Accuracy), mean(resamp$Accuracy) * 100))
cat(sprintf("  Std deviation : %.4f\n", sd(resamp$Accuracy)))
cat("\n")

cat("Reminder:\n")
cat("  - Training accuracy is optimistic (model has seen the test data)\n")
cat("  - Cross-validation gives a more honest estimate\n")
cat("  - k=5 or k=10 fold CV is standard practice\n")
cat("  - Always beat the majority-class baseline before claiming model works\n")
cat("\n")
cat("Done.\n")
