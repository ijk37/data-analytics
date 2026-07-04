# Chapter 03
# 03-03-project-03: Correlation & Heatmap Analysis (R version)
# =============================================================
# Answers Iris dataset exercise questions Q10, Q11, Q12 from Ch.03.
# Also computes covariance and correlation for the Friends dataset.
#
# Required packages:
#   install.packages(c("ggplot2", "GGally", "corrplot", "pheatmap"))
#
# Usage: source("correlation_analysis.R")
# =============================================================


# ---------------------------------------------------------------
# PACKAGES
# ---------------------------------------------------------------
library(ggplot2)  # for ggpairs dependency
library(GGally)   # Q10: ggpairs() scatter plot matrix
library(corrplot) # Q11: corrplot() correlogram
library(pheatmap) # Q12: pheatmap() heatmap with dendrogram


# ---------------------------------------------------------------
# DATASETS
# ---------------------------------------------------------------

# ---- Iris dataset (Q10, Q11, Q12) ----
data(iris)
iris_numeric <- iris[, c("Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width")]

# ---- Friends dataset (bonus: covariance + correlation) ----
friends <- data.frame(
  Max_temp = c(25, 31, 15, 20, 10, 12, 16, 26, 15, 21, 30, 13,  8, 12),
  Weight   = c(77,110, 70, 85, 65, 75, 75, 63, 55, 66, 95, 72, 83,115),
  Height   = c(175,195,172,180,168,173,180,165,158,163,190,172,185,192),
  Years    = c(10, 12,  2, 16,  0,  6,  3,  2,  5, 14,  1, 11,  3, 15)
)


cat("===================================================================\n")
cat("  Ch.03 Mini Project 03 -- Correlation & Heatmap Analysis (R)\n")
cat("===================================================================\n\n")


# ---------------------------------------------------------------
# EXERCISE Q10
# Scatter plot matrix with Pearson r values (Iris dataset)
# ---------------------------------------------------------------
cat("--- Q10: Scatter plot matrix with Pearson r values (Iris) ---\n\n")

# GGally::ggpairs() creates the full scatter plot matrix (SPLOM).
# - Lower triangle: scatter plots
# - Upper triangle: correlation coefficients (Pearson r by default)
# - Diagonal: density plots (or histograms)
# - color = Species: each species gets a different color throughout
p_q10 <- ggpairs(
  iris,
  columns = 1:4,                      # use the 4 numeric columns
  aes(color = Species, alpha = 0.5),  # color by species
  title   = "Q10: Scatter Plot Matrix -- Iris Dataset (color = Species)"
)

print(p_q10)


# ---------------------------------------------------------------
# EXERCISE Q11
# Correlogram (visual representation of the correlation matrix)
# ---------------------------------------------------------------
cat("--- Q11: Correlogram (Iris dataset) ---\n\n")

# First compute the Pearson correlation matrix
iris_cor <- cor(iris_numeric)

cat("Pearson correlation matrix (Iris):\n")
print(round(iris_cor, 4))
cat("\n")

# corrplot() draws the correlation matrix as a visual correlogram.
# method = "color": filled squares, darker = stronger correlation.
# addCoef.col = "black": write the r value inside each square.
# type = "upper": show only the upper triangle (lower mirrors it).
corrplot(
  iris_cor,
  method      = "color",     # colored squares
  addCoef.col = "black",     # r values as text inside cells
  tl.col      = "black",     # axis label color
  tl.srt      = 45,          # rotate axis labels 45 degrees
  title       = "Q11: Correlogram -- Iris Dataset",
  mar         = c(0, 0, 1, 0)
)

# Alternative: method = "circle" shows circles whose size + color encode r
corrplot(
  iris_cor,
  method      = "circle",
  tl.col      = "black",
  tl.srt      = 45,
  title       = "Q11: Correlogram (circles) -- Iris Dataset",
  mar         = c(0, 0, 1, 0)
)


# ---------------------------------------------------------------
# EXERCISE Q12
# Heatmap with hierarchical clustering dendrogram (Iris dataset)
# ---------------------------------------------------------------
cat("--- Q12: Heatmap with dendrogram (Iris dataset) ---\n\n")

# pheatmap() draws a heatmap where:
#   - Rows   = objects (individual flowers)
#   - Columns = attributes
#   - Cell color = attribute value (scaled per column by default)
#   - Rows and columns are reordered by hierarchical clustering
#   - Dendrograms are drawn on the sides to show the clustering structure
#
# scale = "column": each attribute is z-score normalized before coloring
#   so that attributes with very different ranges can be compared visually.
pheatmap(
  as.matrix(iris_numeric),
  scale          = "column",          # z-score normalize each attribute
  clustering_distance_rows = "euclidean",
  clustering_method        = "complete",
  show_rownames  = FALSE,             # 150 row labels would be too crowded
  show_colnames  = TRUE,
  main           = "Q12: Heatmap with Dendrogram -- Iris Dataset (scaled)",
  color          = colorRampPalette(c("blue", "white", "red"))(50)
)

# Optional: add Species annotation as a colored sidebar
species_annotation <- data.frame(Species = iris$Species)
rownames(species_annotation) <- rownames(iris)

pheatmap(
  as.matrix(iris_numeric),
  scale              = "column",
  annotation_row     = species_annotation,   # Species color bar on the left
  clustering_distance_rows = "euclidean",
  clustering_method        = "complete",
  show_rownames      = FALSE,
  main               = "Q12: Heatmap with Species Annotation -- Iris Dataset",
  color              = colorRampPalette(c("blue", "white", "red"))(50)
)


# ---------------------------------------------------------------
# BONUS: Friends dataset -- covariance and correlation
# ---------------------------------------------------------------
cat("--- BONUS: Friends Dataset Covariance and Correlation ---\n\n")

# Covariance matrix (scale-dependent)
friends_cov <- cov(friends)
cat("Covariance matrix (Friends):\n")
print(round(friends_cov, 2))
cat("\n")

# Expected values from lecture:
cat("Verification against lecture values:\n")
cat(sprintf("  cov(Max_temp, Max_temp) = %.2f  [lecture: 55.52]\n",
            friends_cov["Max_temp", "Max_temp"]))
cat(sprintf("  cov(Weight,   Weight)   = %.2f  [lecture: 302.15]\n",
            friends_cov["Weight", "Weight"]))
cat(sprintf("  cov(Weight,   Height)   = %.2f  [lecture: 184.62]\n",
            friends_cov["Weight", "Height"]))
cat("\n")

# Pearson correlation matrix (scale-independent, range -1 to +1)
friends_cor <- cor(friends)
cat("Pearson correlation matrix (Friends):\n")
print(round(friends_cor, 4))
cat("\n")

cat(sprintf("  r(Weight, Height) = %.4f  [lecture: 0.94]\n",
            friends_cor["Weight", "Height"]))
cat("\n")

# Correlogram for Friends
corrplot(
  friends_cor,
  method      = "color",
  addCoef.col = "black",
  tl.col      = "black",
  tl.srt      = 45,
  title       = "Correlogram -- Friends Dataset",
  mar         = c(0, 0, 1, 0)
)

# Heatmap for Friends
pheatmap(
  as.matrix(friends),
  scale          = "column",
  clustering_distance_rows = "euclidean",
  clustering_method        = "complete",
  show_rownames  = TRUE,
  main           = "Heatmap -- Friends Dataset (scaled)"
)

cat("===================================================================\n")
cat("  All plots complete (Q10, Q11, Q12 + Friends bonus)\n")
cat("===================================================================\n")
