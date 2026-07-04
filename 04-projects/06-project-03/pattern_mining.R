# =============================================================================
# pattern_mining.R
# Project 06-03-03: Pattern Mining with arules (R)
# =============================================================================
# Uses the arules package for frequent itemset mining and association rules.
# Optional: arulesViz for visualization.
#
# Install required packages:
#   install.packages("arules")
#   install.packages("arulesViz")  # optional
# =============================================================================


# ---- SECTION 1: Setup -------------------------------------------------------

# Install arules if not already installed
if (!requireNamespace("arules", quietly = TRUE)) {
  cat("Installing arules...\n")
  install.packages("arules", repos = "https://cran.r-project.org")
}
library(arules)

# Check if arulesViz is available for visualization
HAS_VIZ <- requireNamespace("arulesViz", quietly = TRUE)
if (!HAS_VIZ) {
  cat("Note: arulesViz not installed. Skipping visualization.\n")
  cat("      Install with: install.packages('arulesViz')\n\n")
} else {
  library(arulesViz)
}


# ---- SECTION 2: Data — Friends Cuisine Dataset ------------------------------

cat("=============================================================\n")
cat("PROJECT 06-03-03: Pattern Mining with arules\n")
cat("=============================================================\n\n")

# Define transactions as a list of character vectors
cuisine_list <- list(
  Andrew   = c("Indian", "Mediterranean"),
  Bernhard = c("Indian", "Oriental", "FastFood"),
  Carolina = c("Indian", "Mediterranean", "Oriental"),
  Dennis   = c("Arabic", "Mediterranean"),
  Eve      = c("Oriental"),
  Fred     = c("Indian", "Mediterranean", "Oriental"),
  Gwyneth  = c("Arabic", "Mediterranean"),
  Hayden   = c("Indian", "Oriental", "FastFood"),
  Irene    = c("Indian", "Mediterranean", "Oriental"),
  James    = c("Arabic", "Mediterranean")
)

cat("Cuisine transactions loaded:", length(cuisine_list), "\n\n")

# Convert to arules transactions object
cuisine_trans <- as(cuisine_list, "transactions")

cat("Transaction summary:\n")
summary(cuisine_trans)

cat("\nItem frequency (absolute):\n")
itemFrequency(cuisine_trans, type = "absolute")


# ---- SECTION 3: Frequent Itemsets with Apriori ------------------------------

cat("\n--- Frequent Itemsets (min_support = 0.3) ---\n")

# Find all frequent itemsets
freq_sets <- apriori(
  cuisine_trans,
  parameter = list(
    support    = 0.3,     # 30% = 3 out of 10 transactions
    confidence = 0.0,     # no confidence threshold for itemsets only
    minlen     = 1,
    maxlen     = 10,
    target     = "frequent itemsets"
  )
)

cat("Number of frequent itemsets found:", length(freq_sets), "\n\n")

# Display sorted by support
cat("Frequent itemsets sorted by support:\n")
inspect(sort(freq_sets, by = "support"))


# ---- SECTION 4: Association Rules -------------------------------------------

cat("\n--- Association Rules (min_support=0.3, min_confidence=0.5) ---\n")

# Mine association rules
cuisine_rules <- apriori(
  cuisine_trans,
  parameter = list(
    support    = 0.3,
    confidence = 0.5,
    minlen     = 2,
    target     = "rules"
  )
)

cat("Number of rules found:", length(cuisine_rules), "\n\n")

# Display rules sorted by lift
cat("Rules sorted by lift (highest first):\n")
inspect(sort(cuisine_rules, by = "lift"))

# Display rules sorted by confidence
cat("\nRules sorted by confidence:\n")
inspect(sort(cuisine_rules, by = "confidence"))


# ---- SECTION 5: Filtering Rules ---------------------------------------------

cat("\n--- Filtering Rules ---\n")

# Rules with lift > 1.2 (strong positive correlation)
strong_rules <- subset(cuisine_rules, lift > 1.2)
cat("Rules with lift > 1.2:", length(strong_rules), "\n")
if (length(strong_rules) > 0) {
  inspect(sort(strong_rules, by = "lift"))
}

# Rules where Mediterranean appears in the consequent
med_rules <- subset(cuisine_rules, rhs %pin% "Mediterranean")
cat("\nRules with Mediterranean as consequent:", length(med_rules), "\n")
if (length(med_rules) > 0) {
  inspect(sort(med_rules, by = "confidence"))
}

# Rules involving Indian in either antecedent or consequent
indian_rules <- subset(cuisine_rules, items %pin% "Indian")
cat("\nRules involving Indian:", length(indian_rules), "\n")
if (length(indian_rules) > 0) {
  inspect(sort(indian_rules, by = "lift"))
}


# ---- SECTION 6: Redundant Rules Removal -------------------------------------

cat("\n--- Removing Redundant Rules ---\n")

# A rule is redundant if a more general rule with equal or higher confidence exists
if (length(cuisine_rules) > 0) {
  is_redundant <- is.redundant(cuisine_rules)
  cat("Redundant rules:", sum(is_redundant), "\n")
  non_redundant <- cuisine_rules[!is_redundant]
  cat("Non-redundant rules:", length(non_redundant), "\n")
  if (length(non_redundant) > 0) {
    inspect(sort(non_redundant, by = "lift"))
  }
}


# ---- SECTION 7: Visualization (if arulesViz available) ----------------------

if (HAS_VIZ && length(cuisine_rules) > 0) {
  cat("\n--- Visualization ---\n")

  # Scatter plot: support vs confidence, colored by lift
  plot(cuisine_rules,
       method = "scatterplot",
       measure = c("support", "confidence"),
       shading = "lift",
       main = "Cuisine Rules: Support vs Confidence (shading = lift)")

  # Graph-based visualization (shows item relationships)
  if (length(cuisine_rules) <= 20) {
    plot(cuisine_rules,
         method = "graph",
         main = "Association Rules Graph")
  }

  cat("Visualizations displayed.\n")
} else if (!HAS_VIZ) {
  cat("\nSkipping visualization (arulesViz not installed).\n")
}


# ---- SECTION 8: Synthetic Grocery Dataset -----------------------------------

cat("\n--- Synthetic Grocery Dataset ---\n")

# Generate a simple grocery dataset programmatically
set.seed(42)
grocery_items <- c("Milk", "Bread", "Butter", "Eggs", "Cheese",
                   "Apple", "Banana", "Chicken", "Rice", "Pasta",
                   "Tomato", "Onion", "Coffee", "Tea", "Juice")

# Item probabilities of appearing in a transaction
item_probs <- c(0.6, 0.55, 0.4, 0.5, 0.35,
                0.45, 0.4, 0.35, 0.4, 0.35,
                0.45, 0.5, 0.4, 0.35, 0.3)

n_transactions <- 50
grocery_list <- vector("list", n_transactions)

for (i in seq_len(n_transactions)) {
  # Pick items based on their probability
  present <- grocery_items[runif(length(grocery_items)) < item_probs]
  # Ensure at least one item
  if (length(present) == 0) {
    present <- sample(grocery_items, 1)
  }
  grocery_list[[i]] <- present
}

cat("Generated", n_transactions, "grocery transactions\n")

# Convert to arules transactions
grocery_trans <- as(grocery_list, "transactions")
summary(grocery_trans)

# Mine frequent itemsets
grocery_freq <- apriori(
  grocery_trans,
  parameter = list(
    support    = 0.4,
    confidence = 0.0,
    minlen     = 1,
    target     = "frequent itemsets"
  )
)
cat("\nGrocery frequent itemsets (min_support=40%):", length(grocery_freq), "\n")
inspect(sort(grocery_freq, by = "support")[1:min(10, length(grocery_freq))])

# Mine association rules
grocery_rules <- apriori(
  grocery_trans,
  parameter = list(
    support    = 0.4,
    confidence = 0.5,
    minlen     = 2,
    target     = "rules"
  )
)
cat("\nGrocery association rules:", length(grocery_rules), "\n")
if (length(grocery_rules) > 0) {
  cat("Top rules by lift:\n")
  inspect(sort(grocery_rules, by = "lift")[1:min(10, length(grocery_rules))])
}

cat("\n=============================================================\n")
cat("Done.\n")
cat("=============================================================\n")
