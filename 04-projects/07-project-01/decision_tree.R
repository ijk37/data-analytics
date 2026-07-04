# =============================================================================
# decision_tree.R
# Project 07-03-01: Decision Trees (R)
# =============================================================================
# Uses the rpart package (Recursive Partitioning) for decision tree learning.
# Optional: rpart.plot for better visualization.
#
# Install required packages:
#   install.packages("rpart")
#   install.packages("rpart.plot")  # optional but recommended
# =============================================================================


# ---- SECTION 1: Setup -------------------------------------------------------

# Install rpart if needed
if (!requireNamespace("rpart", quietly = TRUE)) {
  cat("Installing rpart...\n")
  install.packages("rpart", repos = "https://cran.r-project.org")
}
library(rpart)

# Check for rpart.plot
HAS_RPART_PLOT <- requireNamespace("rpart.plot", quietly = TRUE)
if (!HAS_RPART_PLOT) {
  cat("Note: rpart.plot not installed. Using base plot.\n")
  cat("      Install with: install.packages('rpart.plot')\n\n")
} else {
  library(rpart.plot)
}

cat("=============================================================\n")
cat("PROJECT 07-03-01: Decision Trees\n")
cat("=============================================================\n\n")


# ---- SECTION 2: Friends Dataset ---------------------------------------------

friends <- data.frame(
  Food     = c("chinese", "italian", "italian", "burgers", "chinese",
               "chinese", "burgers", "chinese", "italian"),
  Age      = c(51, 43, 82, 23, 46, 29, 42, 38, 31),
  Distance = c("close", "very_close", "close", "far", "very_far",
               "too_far", "very_far", "close", "far"),
  Company  = c("good", "good", "good", "bad", "good",
               "bad", "good", "bad", "good"),
  stringsAsFactors = TRUE  # factors needed for classification
)

cat("Friends Dataset:\n")
print(friends)
cat("\n")

cat("Class distribution:\n")
print(table(friends$Company))
cat("\n")


# ---- SECTION 3: Entropy Calculation (manual) --------------------------------

cat("--- Manual Entropy Calculation ---\n")

# Compute entropy by hand
compute_entropy <- function(labels) {
  n <- length(labels)
  if (n == 0) return(0)
  props <- table(labels) / n
  props <- props[props > 0]
  -sum(props * log2(props))
}

cat("Overall entropy H(S):", round(compute_entropy(friends$Company), 4), "\n")

# Entropy after splitting on Food
cat("\nEntropy after split on Food:\n")
food_groups <- split(friends$Company, friends$Food)
for (food_val in names(food_groups)) {
  grp <- food_groups[[food_val]]
  h <- compute_entropy(grp)
  cat("  Food =", food_val, ": n =", length(grp),
      "  labels =", paste(sort(grp), collapse = ", "),
      "  H =", round(h, 4), "\n")
}
n <- nrow(friends)
weighted_h_food <- sum(sapply(food_groups, function(g) length(g) / n * compute_entropy(g)))
ig_food <- compute_entropy(friends$Company) - weighted_h_food
cat("  IG(S, Food) =", round(ig_food, 4), "\n")

# Entropy after splitting on Distance
cat("\nEntropy after split on Distance:\n")
dist_groups <- split(friends$Company, friends$Distance)
for (dist_val in names(dist_groups)) {
  grp <- dist_groups[[dist_val]]
  h <- compute_entropy(grp)
  cat("  Distance =", dist_val, ": n =", length(grp),
      "  H =", round(h, 4), "\n")
}
weighted_h_dist <- sum(sapply(dist_groups, function(g) length(g) / n * compute_entropy(g)))
ig_dist <- compute_entropy(friends$Company) - weighted_h_dist
cat("  IG(S, Distance) =", round(ig_dist, 4), "\n")

cat("\nBest split:", ifelse(ig_dist > ig_food, "Distance", "Food"), "\n\n")


# ---- SECTION 4: Build Decision Tree with rpart ------------------------------

cat("--- Decision Tree (rpart, information gain) ---\n")

# Build tree using information gain (parms = list(split = "information"))
tree_info <- rpart(
  Company ~ Food + Distance,
  data   = friends,
  method = "class",
  parms  = list(split = "information"),
  control = rpart.control(
    minsplit = 1,   # allow splits on small nodes
    minbucket = 1,
    cp = 0          # no pruning (complexity parameter = 0)
  )
)

cat("\nTree summary:\n")
print(tree_info)

cat("\nTree rules (text output):\n")
print(tree_info, digits = 4)


# ---- SECTION 5: Visualize the Tree ------------------------------------------

cat("\n--- Tree Visualization ---\n")

if (HAS_RPART_PLOT) {
  # Fancy plot with rpart.plot
  rpart.plot(tree_info,
             main   = "Decision Tree: Friends Food Dataset",
             type   = 2,      # show split labels on branches
             extra  = 104,    # show class, probability, n
             fallen.leaves = TRUE)
} else {
  # Base R plot
  plot(tree_info, uniform = TRUE, main = "Decision Tree: Friends Food Dataset")
  text(tree_info, use.n = TRUE, all = TRUE, cex = 0.8)
}


# ---- SECTION 6: Predictions on Training Data --------------------------------

cat("\n--- Training Predictions ---\n")

train_preds <- predict(tree_info, friends, type = "class")
cat("Predictions vs Actual:\n")
comparison <- data.frame(
  Food     = friends$Food,
  Distance = friends$Distance,
  Actual   = friends$Company,
  Predicted = train_preds,
  Correct  = (train_preds == friends$Company)
)
print(comparison)

accuracy <- mean(train_preds == friends$Company)
cat("\nTraining accuracy:", round(accuracy * 100, 1), "%\n")


# ---- SECTION 7: Predict New Observations ------------------------------------

cat("\n--- Predicting New Observations ---\n")

new_data <- data.frame(
  Food     = c("chinese", "italian", "burgers", "chinese", "italian"),
  Distance = c("close", "very_far", "far", "too_far", "close"),
  stringsAsFactors = TRUE
)

# Ensure factor levels match training data
levels(new_data$Food)     <- levels(friends$Food)
levels(new_data$Distance) <- levels(friends$Distance)

new_preds <- predict(tree_info, new_data, type = "class")
new_probs <- predict(tree_info, new_data, type = "prob")

cat("Predictions with probabilities:\n")
result <- data.frame(
  Food      = new_data$Food,
  Distance  = new_data$Distance,
  Predicted = new_preds,
  Prob_bad  = round(new_probs[, "bad"],  3),
  Prob_good = round(new_probs[, "good"], 3)
)
print(result)


# ---- SECTION 8: Iris Dataset — Multi-Class Tree ----------------------------

cat("\n=============================================================\n")
cat("Bonus: Iris Dataset (multi-class classification)\n")
cat("=============================================================\n\n")

data(iris)
cat("Iris dataset dimensions:", nrow(iris), "rows x", ncol(iris), "cols\n")
cat("Class distribution:\n")
print(table(iris$Species))

# Build tree using Gini (rpart default for classification)
iris_tree <- rpart(
  Species ~ .,
  data    = iris,
  method  = "class",
  control = rpart.control(minsplit = 5, cp = 0.01)
)

cat("\nIris tree structure:\n")
print(iris_tree)

if (HAS_RPART_PLOT) {
  rpart.plot(iris_tree,
             main  = "Decision Tree: Iris Dataset",
             type  = 2,
             extra = 104)
} else {
  plot(iris_tree, uniform = TRUE, main = "Iris Decision Tree")
  text(iris_tree, use.n = TRUE, cex = 0.8)
}

# Training accuracy on Iris
iris_preds <- predict(iris_tree, iris, type = "class")
iris_acc <- mean(iris_preds == iris$Species)
cat("\nIris training accuracy:", round(iris_acc * 100, 1), "%\n")

# Confusion matrix
cat("\nConfusion matrix:\n")
print(table(Actual = iris$Species, Predicted = iris_preds))

# Extract variable importance
cat("\nVariable importance:\n")
print(iris_tree$variable.importance)

# Show rules as text
cat("\nTree rules (text):\n")
print(iris_tree, digits = 3)

cat("\n=============================================================\n")
cat("Done.\n")
cat("=============================================================\n")
