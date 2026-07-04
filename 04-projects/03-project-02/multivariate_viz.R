# Chapter 03
# 03-03-project-02: Multivariate Visualization (R version)
# =========================================================
# Answers Iris dataset exercise questions Q1-Q5, Q8, Q9 from Ch.03.
#
# Required packages:
#   install.packages(c("ggplot2", "scatterplot3d", "MASS", "aplpack"))
#
# Usage: source("multivariate_viz.R")
# =========================================================


# ---------------------------------------------------------------
# PACKAGES
# ---------------------------------------------------------------
library(ggplot2)        # Q1, Q2, Q9: scatter plots and box plots
library(scatterplot3d)  # Q3: 3D scatter plot
library(MASS)           # Q4: parcoord() for parallel coordinates
library(aplpack)        # Q8: faces() for Chernoff faces


# ---------------------------------------------------------------
# DATASET: Iris
# ---------------------------------------------------------------
# The iris dataset is built into R.
# str(iris)  ->  150 obs, 5 variables:
#   Sepal.Length, Sepal.Width, Petal.Length, Petal.Width (numeric)
#   Species (factor: setosa, versicolor, virginica)

data(iris)

# Extract the 4 numeric columns as a matrix (used in Q4, Q5, Q8)
iris_numeric <- iris[, c("Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width")]

cat("===================================================================\n")
cat("  Ch.03 Mini Project 02 -- Multivariate Visualization (R, Iris)\n")
cat("===================================================================\n\n")


# ---------------------------------------------------------------
# EXERCISE Q1
# Scatter plot: Sepal.Length (x) vs Sepal.Width (y)
# Third attribute: Petal.Length encoded as the SIZE of each point
# ---------------------------------------------------------------
cat("--- Q1: Scatter plot (Sepal Length vs Sepal Width; size = Petal Length) ---\n\n")

# ggplot2: aes() maps columns to visual aesthetics
# size = Petal.Length makes larger petals appear as bigger points
p_q1 <- ggplot(iris, aes(x = Sepal.Length,
                          y = Sepal.Width,
                          size = Petal.Length)) +
  geom_point(alpha = 0.6, color = "steelblue") +
  scale_size_continuous(name = "Petal Length") +
  labs(
    title = "Q1: Sepal Length vs Sepal Width  (size = Petal Length)",
    x     = "Sepal Length (cm)",
    y     = "Sepal Width (cm)"
  ) +
  theme_bw()

print(p_q1)


# ---------------------------------------------------------------
# EXERCISE Q2
# Scatter plot: Sepal.Length vs Sepal.Width
# Third attribute: Species encoded as BOTH color AND marker shape
# ---------------------------------------------------------------
cat("--- Q2: Scatter plot with Species as color + shape ---\n\n")

# color = Species -> different color per species
# shape = Species -> different point shape per species
# Using both color and shape together is better for accessibility
# (works even for viewers with color blindness)
p_q2 <- ggplot(iris, aes(x     = Sepal.Length,
                          y     = Sepal.Width,
                          color = Species,
                          shape = Species)) +
  geom_point(size = 2.5, alpha = 0.75) +
  labs(
    title = "Q2: Sepal Length vs Sepal Width  (color + shape = Species)",
    x     = "Sepal Length (cm)",
    y     = "Sepal Width (cm)"
  ) +
  theme_bw()

print(p_q2)


# ---------------------------------------------------------------
# EXERCISE Q3
# 3D scatter plot: Sepal.Length, Sepal.Width, Petal.Length
# ---------------------------------------------------------------
cat("--- Q3: 3D scatter plot (Sepal Length, Sepal Width, Petal Length) ---\n\n")

# Assign a color for each species level
# as.numeric(iris$Species) gives 1, 2, 3 for the three species
species_colors <- c("red", "green3", "blue")
point_colors   <- species_colors[as.numeric(iris$Species)]

# scatterplot3d() draws a static 3D scatter in base-R graphics
s3d <- scatterplot3d(
  x    = iris$Sepal.Length,
  y    = iris$Sepal.Width,
  z    = iris$Petal.Length,
  color  = point_colors,
  pch    = 16,                     # filled circles
  main   = "Q3: 3D Scatter -- Iris Dataset",
  xlab   = "Sepal Length",
  ylab   = "Sepal Width",
  zlab   = "Petal Length",
  angle  = 55                      # viewing angle; adjust if needed
)

# Add a legend manually (scatterplot3d does not build one automatically)
legend("topright",
       legend = levels(iris$Species),
       col    = species_colors,
       pch    = 16,
       cex    = 0.8,
       title  = "Species")


# ---------------------------------------------------------------
# EXERCISE Q4
# Parallel coordinates for all 4 numeric attributes
# Line color = Species
# ---------------------------------------------------------------
cat("--- Q4: Parallel coordinates (Species = line color) ---\n\n")

# MASS::parcoord() draws a parallel coordinates plot.
# Each row = one flower = one polyline crossing all four attribute axes.
# Axes are auto-scaled to [0, 1] per attribute.

# Map species to colors (3 species -> 3 colors)
parcoord_colors <- c("red", "green3", "blue")[as.numeric(iris$Species)]

# Open a new plot window with a title
par(mar = c(4, 2, 3, 2))   # adjust margins
parcoord(
  iris_numeric,
  col   = parcoord_colors,
  main  = "Q4: Parallel Coordinates -- Iris Dataset  (color = Species)",
  lty   = 1,
  lwd   = 0.8
)

# Add a legend
legend("topright",
       legend = levels(iris$Species),
       col    = c("red", "green3", "blue"),
       lty    = 1,
       lwd    = 2,
       cex    = 0.8,
       title  = "Species")


# ---------------------------------------------------------------
# EXERCISE Q5
# Star plots (spider / radar charts) for the first 20 objects
# ---------------------------------------------------------------
cat("--- Q5: Star plots for first 20 objects ---\n\n")

# stars() is a base-R function.
# Each row becomes one star; each column is one spoke.
# The key.loc argument places a legend key in the plot.
stars(
  iris_numeric[1:20, ],           # first 20 rows, all 4 numeric columns
  labels    = as.character(1:20), # label each star with its row number
  main      = "Q5: Star Plots -- First 20 Iris Objects",
  key.loc   = c(11, 2),           # position for the legend star
  full      = FALSE               # draw semi-circle stars (easier to read)
)


# ---------------------------------------------------------------
# EXERCISE Q8
# Chernoff faces for the first 20 objects
# ---------------------------------------------------------------
cat("--- Q8: Chernoff faces for first 20 objects ---\n\n")

# aplpack::faces() maps each column to a facial feature.
# With 4 columns, the assignments are:
#   Sepal.Length -> face width
#   Sepal.Width  -> upper/lower face
#   Petal.Length -> upper hair line
#   Petal.Width  -> lower hair line
# Objects with similar profiles will have similar-looking faces.
faces(
  iris_numeric[1:20, ],
  main = "Q8: Chernoff Faces -- First 20 Iris Objects"
)


# ---------------------------------------------------------------
# EXERCISE Q9
# Box plots for all 4 numeric attributes
# ---------------------------------------------------------------
cat("--- Q9: Box plots for all 4 numeric attributes ---\n\n")

# To use ggplot2 with multiple attributes side by side, we reshape
# the data from wide format (4 columns) to long format (1 column of
# values + 1 column of attribute name).

# tidyr::pivot_longer() would be the modern approach, but we want
# base-R compatible code. We reshape manually with reshape().

# Add a row-ID column first so reshape() can match rows
iris_with_id           <- iris_numeric
iris_with_id$id        <- 1:nrow(iris_numeric)
iris_with_id$Species   <- iris$Species

# reshape from wide to long:
#   each flower now appears 4 times (once per attribute)
iris_long <- reshape(
  iris_with_id,
  direction  = "long",
  varying    = c("Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"),
  v.names    = "Value",
  timevar    = "Attribute",
  times      = c("Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"),
  idvar      = "id"
)

# Draw one box plot per attribute, using ggplot2
p_q9 <- ggplot(iris_long, aes(x = Attribute, y = Value, fill = Attribute)) +
  geom_boxplot(alpha = 0.7, outlier.shape = 16, outlier.size = 1.5) +
  labs(
    title = "Q9: Box Plots for All 4 Numeric Attributes -- Iris Dataset",
    x     = "Attribute",
    y     = "Value (cm)"
  ) +
  theme_bw() +
  theme(legend.position = "none")   # no legend needed; x-axis labels are enough

print(p_q9)

cat("\n===================================================================\n")
cat("  All exercise plots complete (Q1, Q2, Q3, Q4, Q5, Q8, Q9)\n")
cat("===================================================================\n")
