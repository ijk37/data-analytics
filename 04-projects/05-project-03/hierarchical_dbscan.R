# =============================================================================
# Project 03: Hierarchical and Density-Based Clustering
# Chapter 5 - Clustering
# Data Analytics Course
#
# Uses R built-in hclust() for hierarchical clustering and the
# dbscan package for DBSCAN. Demonstrates:
#   1. hclust() with all 4 linkage methods on the Friends dataset
#   2. Dendrogram plots
#   3. cutree() to extract K clusters
#   4. DBSCAN on the Friends dataset and the Iris dataset
# =============================================================================


# =============================================================================
# SECTION 1: FRIENDS DATASET
# =============================================================================

friends <- data.frame(
  Person    = c("Andrew", "Bernhard", "Carolina", "Dennis", "Eve",
                "Fred", "Gwyneth", "Hayden", "Irene", "James"),
  Age       = c(55, 43, 37, 82, 23, 46, 38, 50, 29, 42),
  Education = c(1.0, 2.0, 5.0, 3.0, 3.2, 5.0, 4.2, 4.0, 4.5, 4.1),
  stringsAsFactors = FALSE
)

cat("Friends Dataset:\n")
print(friends)
cat("\n")

# Numeric features only for distance computation
friends_data <- friends[, c("Age", "Education")]
rownames(friends_data) <- friends$Person


# =============================================================================
# SECTION 2: COMPUTE DISTANCE MATRIX
# =============================================================================

cat("=============================================================\n")
cat("Distance Matrix (Euclidean)\n")
cat("=============================================================\n\n")

dist_friends <- dist(friends_data, method = "euclidean")
cat("Euclidean distance matrix:\n")
print(round(as.matrix(dist_friends), 2))
cat("\n")


# =============================================================================
# SECTION 3: HIERARCHICAL CLUSTERING — ALL 4 LINKAGE METHODS
# =============================================================================

cat("=============================================================\n")
cat("HIERARCHICAL CLUSTERING — ALL 4 LINKAGE METHODS\n")
cat("=============================================================\n\n")

# Run hclust with all four methods
hc_single   <- hclust(dist_friends, method = "single")
hc_complete <- hclust(dist_friends, method = "complete")
hc_average  <- hclust(dist_friends, method = "average")
hc_ward     <- hclust(dist_friends, method = "ward.D2")

# Set up 2x2 plot layout for dendrograms
par(mfrow = c(2, 2))

plot(hc_single,
  main = "Single Linkage (MIN)",
  xlab = "", sub = "", ylab = "Distance",
  hang = -1
)

plot(hc_complete,
  main = "Complete Linkage (MAX)",
  xlab = "", sub = "", ylab = "Distance",
  hang = -1
)

plot(hc_average,
  main = "Average Linkage",
  xlab = "", sub = "", ylab = "Distance",
  hang = -1
)

plot(hc_ward,
  main = "Ward's Method",
  xlab = "", sub = "", ylab = "Distance",
  hang = -1
)

# Reset to single plot layout
par(mfrow = c(1, 1))

cat("Plot 1 created: All 4 dendrograms in a 2x2 grid.\n\n")

# Print cluster heights (merge distances) for Ward's
cat("Ward's merge sequence (height = distance at each merge):\n")
ward_heights <- round(hc_ward$height, 4)
for (i in seq_along(ward_heights)) {
  cat(sprintf("  Step %2d: merged at distance %.4f\n", i, ward_heights[i]))
}
cat("\n")


# =============================================================================
# SECTION 4: CUTTING THE DENDROGRAM
# =============================================================================

cat("=============================================================\n")
cat("CUTTING THE DENDROGRAM AT DIFFERENT K VALUES\n")
cat("=============================================================\n\n")

for (k in c(2, 3, 4)) {
  cut_single   <- cutree(hc_single,   k = k)
  cut_complete <- cutree(hc_complete, k = k)
  cut_average  <- cutree(hc_average,  k = k)
  cut_ward     <- cutree(hc_ward,     k = k)

  cat(sprintf("K = %d:\n", k))

  # Show clusters for Ward's (most commonly used)
  cat("  Ward's clusters:\n")
  for (cid in 1:k) {
    members <- friends$Person[cut_ward == cid]
    cat(sprintf("    Cluster %d: %s\n", cid, paste(members, collapse = ", ")))
  }
  cat("\n")
}

# Side-by-side comparison at K=3
cat("Cluster comparison at K=3 (all linkage methods):\n")
cut3_single   <- cutree(hc_single,   k = 3)
cut3_complete <- cutree(hc_complete, k = 3)
cut3_average  <- cutree(hc_average,  k = 3)
cut3_ward     <- cutree(hc_ward,     k = 3)

comparison <- data.frame(
  Person   = friends$Person,
  Single   = cut3_single,
  Complete = cut3_complete,
  Average  = cut3_average,
  Ward     = cut3_ward
)
print(comparison)
cat("\n")


# =============================================================================
# SECTION 5: VISUALIZATION OF WARD'S K=3 CLUSTERING
# =============================================================================

cat("=============================================================\n")
cat("CLUSTER VISUALIZATION — Ward's Linkage, K=3\n")
cat("=============================================================\n\n")

colors_3 <- c("red", "blue", "green3")

plot(
  friends$Age, friends$Education,
  col = colors_3[cut3_ward],
  pch = 19, cex = 1.5,
  xlab = "Age", ylab = "Education",
  main = "Friends Dataset: Hierarchical Clustering (Ward's, K=3)"
)

text(
  friends$Age, friends$Education,
  labels = friends$Person,
  pos = 3, cex = 0.75
)

legend("topright",
  legend = paste("Cluster", 1:3),
  col    = colors_3,
  pch    = 19,
  cex    = 0.8
)

cat("Plot 2 created: Ward's K=3 cluster scatter plot.\n\n")


# =============================================================================
# SECTION 6: DBSCAN ON FRIENDS DATASET
# =============================================================================

cat("=============================================================\n")
cat("DBSCAN — Friends Dataset\n")
cat("=============================================================\n\n")

# Install dbscan if needed (run once):
# install.packages("dbscan")

# Load the dbscan package
if (!requireNamespace("dbscan", quietly = TRUE)) {
  cat("Package 'dbscan' not found. Installing...\n")
  install.packages("dbscan", repos = "https://cran.r-project.org")
}

library(dbscan)

# Run DBSCAN on Friends data
# Eps chosen by looking at k-NN distances; MinPts = 3
eps_val  <- 12
min_pts  <- 3

db_friends <- dbscan(friends_data, eps = eps_val, minPts = min_pts)

cat(sprintf("DBSCAN parameters: Eps=%.1f, MinPts=%d\n", eps_val, min_pts))
cat("Cluster assignments (0 = noise):\n")
friends_result <- data.frame(
  Person  = friends$Person,
  Age     = friends$Age,
  Edu     = friends$Education,
  Cluster = db_friends$cluster
)
print(friends_result)
cat("\n")

n_clusters_f <- length(unique(db_friends$cluster[db_friends$cluster > 0]))
n_noise_f    <- sum(db_friends$cluster == 0)
cat(sprintf("Clusters found: %d\n", n_clusters_f))
cat(sprintf("Noise points:   %d\n\n", n_noise_f))

# Visualize DBSCAN on Friends
cluster_colors_db <- c("gray50", "red", "blue", "green3", "purple", "orange")
db_col <- cluster_colors_db[db_friends$cluster + 1]

plot(
  friends$Age, friends$Education,
  col = db_col,
  pch = ifelse(db_friends$cluster == 0, 4, 19),
  cex = 1.5,
  xlab = "Age", ylab = "Education",
  main = sprintf("DBSCAN on Friends (Eps=%.1f, MinPts=%d)", eps_val, min_pts)
)

text(
  friends$Age, friends$Education,
  labels = friends$Person,
  pos = 3, cex = 0.75
)

legend("topright",
  legend = c("Noise", paste("Cluster", 1:n_clusters_f)),
  col    = cluster_colors_db[1:(n_clusters_f + 1)],
  pch    = c(4, rep(19, n_clusters_f)),
  cex    = 0.8
)

cat("Plot 3 created: DBSCAN on Friends dataset.\n\n")


# =============================================================================
# SECTION 7: DBSCAN ON IRIS DATASET
# =============================================================================

cat("=============================================================\n")
cat("DBSCAN — Iris Dataset (2D: Petal.Length vs Petal.Width)\n")
cat("=============================================================\n\n")

# Use Petal.Length and Petal.Width from the built-in iris dataset
iris_2d <- iris[, c("Petal.Length", "Petal.Width")]

# k-NN distance plot to help choose Eps
knn_dist <- kNNdist(iris_2d, k = 4)
knn_sorted <- sort(knn_dist[, 4])

plot(
  knn_sorted,
  type = "l",
  xlab = "Points sorted by 4-NN distance",
  ylab = "4-NN Distance",
  main = "k-NN Distance Plot for Iris (k=4) — Find Eps Elbow"
)
abline(h = 0.5, col = "red", lty = "dashed")
text(50, 0.55, "Eps = 0.5", col = "red", cex = 0.8)

cat("Plot 4 created: k-NN distance plot for Iris (use elbow to choose Eps).\n\n")

# Run DBSCAN on Iris with chosen Eps
db_iris <- dbscan(iris_2d, eps = 0.5, minPts = 5)

cat("DBSCAN on Iris (Eps=0.5, MinPts=5):\n")
cat("Cluster counts:\n")
print(table(db_iris$cluster))
cat("\n")

n_iris_clusters <- length(unique(db_iris$cluster[db_iris$cluster > 0]))
n_iris_noise    <- sum(db_iris$cluster == 0)
cat(sprintf("Clusters found: %d\n", n_iris_clusters))
cat(sprintf("Noise points:   %d\n\n", n_iris_noise))

# True species for comparison
cat("Comparison with true species labels:\n")
print(table(True = iris$Species, DBSCAN = db_iris$cluster))
cat("\n")

# Plot DBSCAN clusters for Iris
iris_colors <- c("gray50", "red", "blue", "green3", "purple")

plot(
  iris$Petal.Length, iris$Petal.Width,
  col = iris_colors[db_iris$cluster + 1],
  pch = ifelse(db_iris$cluster == 0, 4, 19),
  cex = 0.8,
  xlab = "Petal Length", ylab = "Petal Width",
  main = "DBSCAN on Iris (Eps=0.5, MinPts=5)"
)

legend("topleft",
  legend = c("Noise", paste("Cluster", 1:n_iris_clusters)),
  col    = iris_colors[1:(n_iris_clusters + 1)],
  pch    = c(4, rep(19, n_iris_clusters)),
  cex    = 0.8
)

cat("Plot 5 created: DBSCAN on Iris dataset.\n\n")


# =============================================================================
# SECTION 8: PARAMETER SENSITIVITY ANALYSIS
# =============================================================================

cat("=============================================================\n")
cat("DBSCAN PARAMETER SENSITIVITY — Iris Dataset\n")
cat("=============================================================\n\n")

cat(sprintf("%-6s  %-7s  %-10s  %-10s\n", "Eps", "MinPts", "Clusters", "Noise"))
cat(strrep("-", 40), "\n")

eps_vals    <- c(0.3, 0.5, 0.5, 0.7, 1.0)
minpts_vals <- c(5,   3,   5,   5,   5  )

for (i in seq_along(eps_vals)) {
  result <- dbscan(iris_2d, eps = eps_vals[i], minPts = minpts_vals[i])
  n_c <- length(unique(result$cluster[result$cluster > 0]))
  n_n <- sum(result$cluster == 0)
  cat(sprintf("%-6.1f  %-7d  %-10d  %-10d\n",
              eps_vals[i], minpts_vals[i], n_c, n_n))
}

cat("\n")
cat("Interpretation:\n")
cat("  Smaller Eps  -> more noise, possibly more (smaller) clusters\n")
cat("  Larger Eps   -> less noise, possibly fewer (merged) clusters\n")
cat("  Larger MinPts -> stricter core requirement, more noise\n\n")

cat("=============================================================\n")
cat("Hierarchical + DBSCAN R demonstration complete.\n")
cat("=============================================================\n")
