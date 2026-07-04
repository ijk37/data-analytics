# Chapter 6 — FP-Growth with arules
# Shows FP-tree concept and FP-growth mining

# ============================================================
# STEP 1: Setup
# ============================================================
# install.packages("arules")   # uncomment if needed
library(arules)

# ============================================================
# STEP 2: Dataset
# ============================================================
# Same Friends cuisine dataset

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
cuisine_trans <- as(cuisine_list, "transactions")

# ============================================================
# STEP 3: Explain FP-tree concept (printed to console)
# ============================================================

cat("============================================================\n")
cat("FP-TREE CONCEPT\n")
cat("============================================================\n")
cat("An FP-tree is a compact prefix-tree representation of all transactions.\n")
cat("Each path from root to leaf encodes a frequent pattern.\n\n")

# Step 3a: Find frequent 1-itemsets (header table items)
cat("Step 1: Count all items to build the header table.\n")
item_counts <- sort(itemFrequency(cuisine_trans, type="absolute"), decreasing=TRUE)
min_sup_abs <- 3  # min_support = 0.3 = 3/10
cat("Item counts (descending):\n")
for (i in seq_along(item_counts)) {
  freq_mark <- ifelse(item_counts[i] >= min_sup_abs, "[FREQUENT]", "[pruned]  ")
  cat(sprintf("  %-20s %d  %s\n", names(item_counts)[i], item_counts[i], freq_mark))
}

# Step 3b: Show how each transaction is inserted into the FP-tree
cat("\nStep 2: Insert each transaction in frequency order.\n")
frequent_items <- names(item_counts[item_counts >= min_sup_abs])
cat("Frequent items (header table order): ", paste(frequent_items, collapse=" -> "), "\n\n")

for (name in names(cuisine_list)) {
  items <- cuisine_list[[name]]
  # Keep only frequent items, sort by frequency
  filtered <- items[items %in% frequent_items]
  ordered_filtered <- frequent_items[frequent_items %in% filtered]
  cat(sprintf("  %-12s original: %-45s  insert: %s\n",
      name,
      paste(items, collapse=", "),
      paste(ordered_filtered, collapse=" -> ")))
}

# ============================================================
# STEP 4: Mine frequent itemsets using arules (FP-growth equivalent)
# ============================================================

cat("\n============================================================\n")
cat("MINING FREQUENT ITEMSETS\n")
cat("============================================================\n")
cat("(arules uses an efficient algorithm equivalent to FP-growth)\n\n")

all_freq <- apriori(cuisine_trans,
                    parameter = list(supp=0.3, target="frequent itemsets", minlen=1))

cat("All frequent itemsets (support >= 0.3):\n")
inspect(sort(all_freq, by="support"))

# ============================================================
# STEP 5: Identify Maximal Frequent Itemsets
# ============================================================

cat("\n============================================================\n")
cat("MAXIMAL FREQUENT ITEMSETS\n")
cat("(no frequent proper superset exists)\n")
cat("============================================================\n")

# An itemset is maximal if no superset of it is also frequent
all_labels <- labels(all_freq)
all_items_list <- LIST(items(all_freq))

is_maximal <- function(idx) {
  current <- all_items_list[[idx]]
  current_size <- length(current)
  # Check if any larger frequent itemset is a superset
  for (j in seq_along(all_items_list)) {
    other <- all_items_list[[j]]
    if (length(other) > current_size) {
      if (all(current %in% other)) {
        return(FALSE)  # found a frequent superset
      }
    }
  }
  return(TRUE)
}

maximal_indices <- c()
for (i in seq_along(all_items_list)) {
  if (is_maximal(i)) {
    maximal_indices <- c(maximal_indices, i)
  }
}
maximal_itemsets <- all_freq[maximal_indices]
cat("Maximal frequent itemsets:\n")
inspect(sort(maximal_itemsets, by="support"))

# ============================================================
# STEP 6: Identify Closed Frequent Itemsets
# ============================================================

cat("\n============================================================\n")
cat("CLOSED FREQUENT ITEMSETS\n")
cat("(no proper superset has the same support)\n")
cat("============================================================\n")

# Get support values
all_supports <- quality(all_freq)$support

is_closed <- function(idx) {
  current <- all_items_list[[idx]]
  current_sup <- all_supports[idx]
  current_size <- length(current)
  for (j in seq_along(all_items_list)) {
    other <- all_items_list[[j]]
    if (length(other) > current_size) {
      if (all(current %in% other)) {
        if (abs(all_supports[j] - current_sup) < 1e-9) {
          return(FALSE)  # superset with equal support found
        }
      }
    }
  }
  return(TRUE)
}

closed_indices <- c()
for (i in seq_along(all_items_list)) {
  if (is_closed(i)) {
    closed_indices <- c(closed_indices, i)
  }
}
closed_itemsets <- all_freq[closed_indices]
cat("Closed frequent itemsets:\n")
inspect(sort(closed_itemsets, by="support"))

# ============================================================
# STEP 7: Summary comparison
# ============================================================

cat("\n============================================================\n")
cat("SUMMARY: Itemset Type Counts\n")
cat("============================================================\n")
cat(sprintf("All frequent itemsets  : %d\n", length(all_freq)))
cat(sprintf("Closed frequent        : %d\n", length(closed_itemsets)))
cat(sprintf("Maximal frequent       : %d\n", length(maximal_itemsets)))
cat("\nRelationship: Maximal is subset of Closed, Closed is subset of All Frequent\n")

# ============================================================
# STEP 8: FP-growth vs Apriori comparison note
# ============================================================

cat("\n============================================================\n")
cat("FP-GROWTH vs APRIORI\n")
cat("============================================================\n")
cat("| Aspect            | Apriori           | FP-Growth         |\n")
cat("|-------------------|-------------------|-------------------|\n")
cat("| DB scans          | 2k (k = max size) | 2                 |\n")
cat("| Candidate gen     | Yes (expensive)   | No                |\n")
cat("| Memory            | Candidates list   | FP-tree           |\n")
cat("| Best for          | Low support       | High support      |\n")
cat("| Speed             | Slower            | Faster            |\n")
