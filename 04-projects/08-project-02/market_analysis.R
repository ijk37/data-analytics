# market_analysis.R
# Project 02 -- Market Basket & Customer Segmentation
# Chapters: Ch2/Ch3 (stats) + Ch4 (preprocessing) + Ch6 (arules) + Ch5 (K-means)

# Required: install.packages("arules")
library(arules)

cat("============================================================\n")
cat("  MARKET BASKET & CUSTOMER SEGMENTATION (R)\n")
cat("  Chapters: Ch2, Ch3, Ch4, Ch5, Ch6\n")
cat("============================================================\n\n")

# ============================================================
# DATASET
# ============================================================
customer_df <- data.frame(
  id     = paste0("C", sprintf("%02d", 1:20)),
  Age    = c(34, 52, 27, 45, 23, 38, 61, 29, 44, 33, 55, 26, 48, 31, 19, 42, 57, 36, 24, 50),
  Visits = c(12,  3, 20,  8,  2, 15,  5, 18,  9, 11,  4, 22,  7, 16,  1, 10,  6, 13,  3,  8),
  Spend  = c(280, 95, 450, 320, 45, 380, 180, 420, 290, 310, 140, 480, 260, 390, 30, 295, 210, 355, 80, 300),
  stringsAsFactors = FALSE
)

# Transaction items as a list of character vectors
items_list <- list(
  c("bread","milk","butter","eggs"),
  c("beer","chips","soda"),
  c("bread","milk","yogurt","fruit","veg"),
  c("meat","veg","fruit","milk"),
  c("beer","chips"),
  c("bread","butter","eggs","milk","yogurt"),
  c("meat","veg","bread"),
  c("milk","yogurt","fruit","bread","eggs"),
  c("meat","veg","beer"),
  c("bread","milk","butter","fruit"),
  c("chips","soda","beer"),
  c("milk","yogurt","fruit","veg","bread","eggs"),
  c("meat","veg","milk"),
  c("bread","eggs","butter","milk"),
  c("chips","soda"),
  c("meat","veg","fruit","bread"),
  c("meat","beer","bread"),
  c("milk","yogurt","fruit","eggs","bread"),
  c("chips","beer","soda"),
  c("meat","veg","milk","bread")
)

# ============================================================
# PART A (Ch2/Ch3): DESCRIPTIVE STATISTICS
# ============================================================
cat("==========================================================\n")
cat("  PART A -- DESCRIPTIVE STATISTICS (Ch2/Ch3)\n")
cat("==========================================================\n")

numeric_cols <- c("Age", "Visits", "Spend")

cat(sprintf("%-10s %8s %8s %8s %8s\n", "Column", "Mean", "Std", "Min", "Max"))
cat(strrep("-", 46), "\n")
for (col in numeric_cols) {
  vals <- customer_df[[col]]
  cat(sprintf("%-10s %8.2f %8.2f %8d %8d\n",
              col, mean(vals), sd(vals), min(vals), max(vals)))
}

cat("\n  Pearson Correlation Matrix:\n")
corr_matrix <- cor(customer_df[, numeric_cols])
print(round(corr_matrix, 3))

# ASCII scatter: Age (y) vs Spend (x)
cat("\n  ASCII Scatter: Age vs Spend\n")
cat("  (each * = one customer)\n")
width  <- 50
height <- 20
ages   <- customer_df$Age
spends <- customer_df$Spend
age_min <- min(ages); age_max <- max(ages)
sp_min  <- min(spends); sp_max <- max(spends)

grid <- matrix(" ", nrow = height, ncol = width)
for (i in seq_along(ages)) {
  y <- round((1 - (ages[i]  - age_min) / (age_max - age_min)) * (height - 1)) + 1
  x <- round(    (spends[i] - sp_min)  / (sp_max  - sp_min)  * (width  - 1)) + 1
  y <- max(1, min(height, y))
  x <- max(1, min(width,  x))
  grid[y, x] <- "*"
}
cat("  Age\n")
cat("  ", age_max, "|", strrep("-", width), "\n")
for (r in 1:height) {
  cat("    |", paste(grid[r,], collapse=""), "\n")
}
cat("  ", age_min, "|", strrep("-", width), "\n")
cat("      ", sp_min, strrep(" ", 18), "Spend", sp_max, "\n")

# ============================================================
# PART B (Ch4): MIN-MAX NORMALIZATION
# ============================================================
cat("\n==========================================================\n")
cat("  PART B -- NORMALIZATION (Ch4) -- Min-Max to [0,1]\n")
cat("==========================================================\n")

norm_params <- list()
customer_norm <- customer_df

for (col in numeric_cols) {
  vals <- customer_df[[col]]
  mn <- min(vals); mx <- max(vals)
  norm_params[[col]] <- list(min = mn, max = mx)
  if (mx > mn) {
    customer_norm[[col]] <- (vals - mn) / (mx - mn)
  } else {
    customer_norm[[col]] <- rep(0, length(vals))
  }
}

cat("  First 3 customers normalized:\n")
for (i in 1:3) {
  parts <- sapply(numeric_cols, function(col) {
    paste0(col, "=", round(customer_norm[[col]][i], 3))
  })
  cat("  ", customer_df$id[i], ":", paste(parts, collapse=", "), "\n")
}

# ============================================================
# PART C (Ch6): ASSOCIATION RULE MINING WITH arules
# ============================================================
cat("\n==========================================================\n")
cat("  PART C -- FREQUENT PATTERN MINING -- Apriori (Ch6)\n")
cat("==========================================================\n")

# Convert to transactions object
trans <- as(items_list, "transactions")

# Run Apriori
rules <- apriori(
  trans,
  parameter = list(support = 0.25, confidence = 0.50, minlen = 2)
)

cat("  Frequent itemsets with support >= 0.25:\n")
freq_sets <- apriori(
  trans,
  parameter = list(support = 0.25, target = "frequent itemsets")
)
inspect(sort(freq_sets, by = "support", decreasing = TRUE))

cat("\n  Association Rules (sorted by lift descending):\n")
rules_sorted <- sort(rules, by = "lift", decreasing = TRUE)
inspect(rules_sorted)

# ============================================================
# PART D (Ch5): K-MEANS CUSTOMER SEGMENTATION K=3
# ============================================================
cat("\n==========================================================\n")
cat("  PART D -- CUSTOMER SEGMENTATION -- K-Means K=3 (Ch5)\n")
cat("==========================================================\n")

set.seed(42)
km_input <- customer_norm[, numeric_cols]
km_result <- kmeans(km_input, centers = 3, nstart = 25, iter.max = 200)

customer_df$Cluster <- km_result$cluster

# Denormalize centroids for interpretation
denorm_centroids <- km_result$centers
for (col in numeric_cols) {
  mn <- norm_params[[col]]$min
  mx <- norm_params[[col]]$max
  denorm_centroids[, col] <- denorm_centroids[, col] * (mx - mn) + mn
}

# Label by Spend (ascending)
spend_order <- order(denorm_centroids[, "Spend"])
label_names <- c("Young Low-Spend", "Regular Shoppers", "Loyal High-Spend")
cluster_labels <- character(3)
for (rank in seq_along(spend_order)) {
  cluster_labels[spend_order[rank]] <- label_names[rank]
}

cat("  Cluster assignments:\n")
for (k in 1:3) {
  members <- customer_df$id[customer_df$Cluster == k]
  cat("  Cluster", k, "(", cluster_labels[k], "):",
      paste(members, collapse=", "), "\n")
}

cat("\n  Cluster mean profiles (original scale):\n")
cat(sprintf("  %-5s %-22s %7s %8s %8s\n", "K", "Label", "Age", "Visits", "Spend"))
cat("  ", strrep("-", 52), "\n")
for (k in 1:3) {
  subset_k <- customer_df[customer_df$Cluster == k, ]
  cat(sprintf("  %-5d %-22s %7.1f %8.1f %8.1f\n",
              k, cluster_labels[k],
              mean(subset_k$Age),
              mean(subset_k$Visits),
              mean(subset_k$Spend)))
}

# Plot
plot(customer_df$Age, customer_df$Spend,
     col = km_result$cluster,
     pch = 19, cex = 1.5,
     main = "K-Means K=3: Age vs Spend",
     xlab = "Age",
     ylab = "Monthly Spend ($)")
legend("topleft",
       legend = paste("Cluster", 1:3, "-", cluster_labels),
       col    = 1:3, pch = 19)
# Add centroid markers
points(denorm_centroids[, "Age"], denorm_centroids[, "Spend"],
       pch = 8, cex = 2, col = "black", lwd = 2)

cat("\nDone.\n")
