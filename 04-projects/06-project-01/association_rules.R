# Chapter 6 — Association Rules with arules
# This script mirrors association_rules.py using R's arules package

# ============================================================
# STEP 1: Setup
# ============================================================
# install.packages("arules")  # uncomment if needed
library(arules)

# ============================================================
# STEP 2: Create the Friends Cuisine Dataset as transactions
# ============================================================
# Same data used in Python: 10 friends with food preferences

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

# Convert to transactions object
cuisine_trans <- as(cuisine_list, "transactions")

# ============================================================
# STEP 3: Explore the transaction data
# ============================================================
cat("=== Transaction Summary ===\n")
summary(cuisine_trans)

cat("\nFirst 5 transactions:\n")
inspect(head(cuisine_trans, 5))

# Item frequency (absolute counts)
cat("\n=== Item Frequencies ===\n")
item_counts <- itemFrequency(cuisine_trans, type = "absolute")
print(sort(item_counts, decreasing = TRUE))

# ============================================================
# STEP 4: Find Frequent Itemsets with Apriori
# ============================================================
# min_support = 0.3 (= 3 out of 10 transactions)

cat("\n=== Frequent Itemsets (min support = 0.3) ===\n")
freq_itemsets <- apriori(
  cuisine_trans,
  parameter = list(
    supp   = 0.3,
    target = "frequent itemsets",
    minlen = 1
  )
)

cat("Total frequent itemsets found:", length(freq_itemsets), "\n")
inspect(sort(freq_itemsets, by = "support"))

# Show 1-itemsets, 2-itemsets, 3-itemsets separately
for (k in 1:3) {
  sub <- freq_itemsets[size(freq_itemsets) == k]
  if (length(sub) > 0) {
    cat("\n--- ", k, "-itemsets ---\n", sep = "")
    inspect(sort(sub, by = "support"))
  }
}

# ============================================================
# STEP 5: Generate Association Rules
# ============================================================
# min_confidence = 0.5

cat("\n=== Association Rules (min support=0.3, min confidence=0.5) ===\n")
rules <- apriori(
  cuisine_trans,
  parameter = list(
    supp   = 0.3,
    conf   = 0.5,
    minlen = 2
  )
)

cat("Total rules found:", length(rules), "\n\n")

# Sort by lift (most interesting rules first)
cat("Rules sorted by Lift:\n")
inspect(sort(rules, by = "lift"))

# Sort by confidence
cat("\nRules sorted by Confidence:\n")
inspect(sort(rules, by = "confidence"))

# ============================================================
# STEP 6: Manual verification of key rules
# ============================================================
# Verify the top rule by lift manually

cat("\n=== Manual Verification of Support/Confidence/Lift ===\n")
cat("Rule: {Indian} => {Oriental}\n")
n_trans <- length(cuisine_trans)
# Indian appears in: Bernhard, Carolina, Fred, Hayden, Irene, Andrew = 6
# Indian AND Oriental: Bernhard, Carolina, Fred, Hayden, Irene = 5
support_Indian <- 6 / n_trans
support_Indian_Oriental <- 5 / n_trans
confidence <- support_Indian_Oriental / support_Indian
# Oriental appears in: Bernhard, Carolina, Eve, Fred, Hayden, Irene = 6
support_Oriental <- 6 / n_trans
lift_val <- confidence / support_Oriental
cat(sprintf("  support({Indian,Oriental}) = %.3f\n", support_Indian_Oriental))
cat(sprintf("  support({Indian})          = %.3f\n", support_Indian))
cat(sprintf("  confidence                 = %.3f\n", confidence))
cat(sprintf("  support({Oriental})        = %.3f\n", support_Oriental))
cat(sprintf("  lift                       = %.3f\n", lift_val))

# ============================================================
# STEP 7: Effect of different support thresholds
# ============================================================

cat("\n=== Itemset Count at Different Support Levels ===\n")
thresholds <- c(0.1, 0.2, 0.3, 0.4, 0.5)
for (s in thresholds) {
  fi <- apriori(cuisine_trans,
                parameter = list(supp=s, target="frequent itemsets", minlen=1))
  cat(sprintf("  support >= %.1f : %d frequent itemsets\n", s, length(fi)))
}

# ============================================================
# STEP 8: Apriori Property Demonstration
# ============================================================

cat("\n=== Apriori Anti-Monotone Property ===\n")
cat("If {Oriental, FastFood} is infrequent, then:\n")
cat("  {Indian, Oriental, FastFood} must also be infrequent\n")

# Check support of {Oriental, FastFood}
fi_low <- apriori(cuisine_trans,
                  parameter = list(supp=0.25, target="frequent itemsets", minlen=2))
of_item <- fi_low[which(labels(fi_low) == "{FastFood,Oriental}")]
if (length(of_item) > 0) {
  cat("  {FastFood, Oriental} support: ")
  inspect(of_item)
} else {
  cat("  {FastFood, Oriental} is NOT frequent at support=0.25\n")
  cat("  => Any superset containing both FastFood and Oriental is also pruned\n")
}
