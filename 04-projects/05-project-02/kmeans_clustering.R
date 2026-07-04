# =============================================================================
# Project 02: K-Means Clustering
# Chapter 5 - Clustering
# Data Analytics Course
#
# Uses R's built-in kmeans() function to:
#   1. Reproduce Exercise Q1 step-by-step (manual distance computation)
#   2. Cluster the full 10-person Friends dataset with K=4
#   3. Plot clusters with different colors
#   4. Show the elbow curve using SSE vs K
# =============================================================================


# =============================================================================
# SECTION 1: FRIENDS DATASET
# =============================================================================

# Full 10-person dataset from the lecture
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


# =============================================================================
# SECTION 2: EXERCISE Q1 — MANUAL K-MEANS STEP (6-PERSON SUBSET)
# =============================================================================

cat("=============================================================\n")
cat("EXERCISE Q1: K-Means, K=2, 6-Person Subset\n")
cat("=============================================================\n\n")

# 6-person subset
friends_6 <- friends[1:6, ]

# Initial centroids from the exercise
centroid1 <- c(55, 1.0)   # Andrew
centroid2 <- c(37, 5.0)   # Carolina

cat("Initial centroids:\n")
cat("  Centroid 1 (Andrew):   Age=55, Education=1.0\n")
cat("  Centroid 2 (Carolina): Age=37, Education=5.0\n\n")

# Euclidean distance helper
euclid <- function(p, centroid) {
  sqrt(sum((p - centroid)^2))
}

# Compute distances for each person
cat("Iteration 1 - Distances:\n")
cat(sprintf("  %-10s  %14s  %16s  %s\n",
            "Person", "Dist to Cent1", "Dist to Cent2", "Assigned"))
cat("  ", strrep("-", 60), "\n", sep = "")

assignments_q1 <- integer(6)

for (i in 1:6) {
  pt <- c(friends_6$Age[i], friends_6$Education[i])
  d1 <- euclid(pt, centroid1)
  d2 <- euclid(pt, centroid2)

  if (d1 <= d2) {
    assignments_q1[i] <- 1
    assigned_str <- "Cluster 1 (Andrew)"
  } else {
    assignments_q1[i] <- 2
    assigned_str <- "Cluster 2 (Carolina)"
  }

  cat(sprintf("  %-10s  %14.4f  %16.4f  %s\n",
              friends_6$Person[i], d1, d2, assigned_str))
}

# Compute new centroids
cluster1_pts <- friends_6[assignments_q1 == 1, c("Age", "Education")]
cluster2_pts <- friends_6[assignments_q1 == 2, c("Age", "Education")]

new_c1 <- colMeans(cluster1_pts)
new_c2 <- colMeans(cluster2_pts)

cat("\nCluster 1 members:", paste(friends_6$Person[assignments_q1 == 1], collapse = ", "), "\n")
cat("New Centroid 1: Age =", new_c1["Age"], ", Education =", new_c1["Education"], "\n\n")

cat("Cluster 2 members:", paste(friends_6$Person[assignments_q1 == 2], collapse = ", "), "\n")
cat("New Centroid 2: Age =", new_c2["Age"], ", Education =", new_c2["Education"], "\n\n")

cat("Expected from exercise:\n")
cat("  Cluster 1: {Andrew, Dennis} -> centroid = (68.5, 2.0)\n")
cat("  Cluster 2: {Bernhard, Carolina, Eve, Fred} -> centroid = (37.25, 3.8)\n\n")

# Scatter plot for exercise Q1
plot(
  friends_6$Age, friends_6$Education,
  col = ifelse(assignments_q1 == 1, "red", "blue"),
  pch = 19, cex = 1.5,
  xlab = "Age", ylab = "Education",
  main = "Exercise Q1: K-Means K=2 (Iteration 1 Assignment)"
)

# Label each point
text(
  friends_6$Age, friends_6$Education,
  labels = friends_6$Person,
  pos = 3, cex = 0.8
)

# Plot centroids
points(centroid1[1], centroid1[2], pch = 8, cex = 2, col = "red",    lwd = 2)
points(centroid2[1], centroid2[2], pch = 8, cex = 2, col = "blue",   lwd = 2)
points(new_c1[1],   new_c1[2],    pch = 4, cex = 2, col = "darkred", lwd = 2)
points(new_c2[1],   new_c2[2],    pch = 4, cex = 2, col = "navy",    lwd = 2)

legend("topright",
  legend = c("Cluster 1 points", "Cluster 2 points",
             "Initial centroids", "New centroids"),
  col    = c("red", "blue", "black", "darkgray"),
  pch    = c(19, 19, 8, 4),
  cex    = 0.8
)

cat("Plot 1 created: Exercise Q1 K-Means assignment\n\n")


# =============================================================================
# SECTION 3: FULL 10-PERSON FRIENDS DATASET WITH K=4
# =============================================================================

cat("=============================================================\n")
cat("FULL FRIENDS DATASET: K-Means, K=4\n")
cat("=============================================================\n\n")

# Use just the numeric features for clustering
friends_numeric <- friends[, c("Age", "Education")]

# Run K-means with K=4
set.seed(42)
km4 <- kmeans(friends_numeric, centers = 4, nstart = 25)

# Show results
cat("K-means result (K=4):\n")
cat("Cluster assignments:\n")
for (k in 1:4) {
  members <- friends$Person[km4$cluster == k]
  cat(sprintf("  Cluster %d: %s\n", k, paste(members, collapse = ", ")))
}

cat("\nFinal centroids:\n")
print(round(km4$centers, 4))

cat("\nSSE (within-cluster sum of squares):", round(km4$tot.withinss, 4), "\n\n")

cat("Lecture reference clusters (K=4):\n")
cat("  {Andrew, Bernhard, Dennis}\n")
cat("  {Eve, Irene}\n")
cat("  {Gwyneth, Hayden, Fred, James, Carolina}\n\n")

# Color palette for 4 clusters
cluster_colors <- c("red", "blue", "green3", "purple")

# Plot K=4 clusters
plot(
  friends$Age, friends$Education,
  col = cluster_colors[km4$cluster],
  pch = 19, cex = 1.5,
  xlab = "Age", ylab = "Education",
  main = "Friends Dataset: K-Means Clustering (K=4)"
)

# Labels
text(
  friends$Age, friends$Education,
  labels = friends$Person,
  pos = 3, cex = 0.75
)

# Plot centroids
points(
  km4$centers[, "Age"], km4$centers[, "Education"],
  pch = 8, cex = 2.5, col = cluster_colors, lwd = 2
)

legend("topright",
  legend = paste("Cluster", 1:4),
  col    = cluster_colors,
  pch    = 19,
  cex    = 0.8
)

cat("Plot 2 created: Full Friends dataset K=4 clustering\n\n")


# =============================================================================
# SECTION 4: ELBOW CURVE
# =============================================================================

cat("=============================================================\n")
cat("ELBOW CURVE: SSE vs K\n")
cat("=============================================================\n\n")

# Compute SSE for K = 1 to 8
max_k <- 8
sse_values <- numeric(max_k)

for (k in 1:max_k) {
  set.seed(42)
  result <- kmeans(friends_numeric, centers = k, nstart = 25)
  sse_values[k] <- result$tot.withinss
}

# Print SSE values
cat("SSE values:\n")
for (k in 1:max_k) {
  cat(sprintf("  K=%d: SSE = %.4f\n", k, sse_values[k]))
}
cat("\n")

# Plot elbow curve
plot(
  1:max_k, sse_values,
  type = "b",
  pch  = 19,
  col  = "steelblue",
  xlab = "Number of Clusters K",
  ylab = "Total Within-Cluster SSE",
  main = "Elbow Curve: SSE vs K (Friends Dataset)"
)

# Mark each K with its SSE value
text(
  1:max_k, sse_values,
  labels = round(sse_values, 1),
  pos = 3, cex = 0.7
)

# Add a horizontal grid for readability
abline(h = seq(0, max(sse_values), length.out = 5),
       col = "lightgray", lty = "dashed")

cat("Plot 3 created: Elbow curve SSE vs K\n")
cat("Interpretation: Look for the 'elbow' where SSE decrease rate slows.\n\n")

cat("=============================================================\n")
cat("K-Means R demonstration complete.\n")
cat("=============================================================\n")
