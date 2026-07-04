# Chapter 03
# 03-03-project-01: Multivariate Statistics Explorer (R version)
# ==============================================================
# Computes four multivariate summary tables:
#   1. Location matrix    -- min, Q1, median, mean, Q3, max per attribute
#   2. Dispersion matrix  -- amplitude, IQR, MAD, std dev, variance per attribute
#   3. Covariance matrix  -- sample covariance for every pair
#   4. Pearson correlation matrix -- scale-independent r for every pair
#
# Concepts covered:
#   Ch.3 - Multivariate location/dispersion statistics, covariance matrix,
#           Pearson correlation matrix
#
# Requirements: base R only (no packages needed)
#
# Usage: source("multivariate_statistics.R")
# ==============================================================


# ---------------------------------------------------------------
# DATASET
# ---------------------------------------------------------------

# The Friends dataset from the Ch.3 lecture slides.
# Only the four numeric columns are used here.
friends <- data.frame(
  Max_temp = c(25, 31, 15, 20, 10, 12, 16, 26, 15, 21, 30, 13,  8, 12),
  Weight   = c(77,110, 70, 85, 65, 75, 75, 63, 55, 66, 95, 72, 83,115),
  Height   = c(175,195,172,180,168,173,180,165,158,163,190,172,185,192),
  Years    = c(10, 12,  2, 16,  0,  6,  3,  2,  5, 14,  1, 11,  3, 15)
)

cat("===================================================================\n")
cat("  Ch.03 Mini Project 01 -- Multivariate Statistics Explorer (R)\n")
cat("  Dataset: Friends (14 objects, 4 numeric attributes)\n")
cat("===================================================================\n\n")


# ---------------------------------------------------------------
# 1. LOCATION STATISTICS MATRIX
# ---------------------------------------------------------------
# apply(df, 2, FUN) applies FUN to every column (margin=2).
# We call summary() which returns min, Q1, median, mean, Q3, max.

cat("--- LOCATION STATISTICS MATRIX ---\n\n")

# summary() gives a named vector for each column
location_matrix <- apply(friends, 2, summary)

# summary() returns: Min, 1st Qu., Median, Mean, 3rd Qu., Max
print(round(location_matrix, 4))

cat("\n")

# Mode is not provided by summary(); compute it manually.
# A simple mode function: find the value(s) with the highest frequency.
compute_mode <- function(x) {
  # Get a frequency table of values
  freq_table <- table(x)
  # Find the maximum frequency
  max_freq <- max(freq_table)
  # Return all values that reach that frequency
  as.numeric(names(freq_table[freq_table == max_freq]))
}

cat("Modes per column:\n")
for (col in names(friends)) {
  modes <- compute_mode(friends[[col]])
  cat(sprintf("  %-10s : %s\n", col, paste(modes, collapse = " / ")))
}
cat("\n")


# ---------------------------------------------------------------
# 2. DISPERSION STATISTICS MATRIX
# ---------------------------------------------------------------
# We build the matrix row by row, one statistic at a time.

cat("--- DISPERSION STATISTICS MATRIX ---\n\n")

# Amplitude (range = max - min)
amplitudes <- apply(friends, 2, function(x) max(x) - min(x))

# IQR (interquartile range = Q3 - Q1)
iqr_values <- apply(friends, 2, IQR)

# MAD (median absolute deviation)
# mad() in base R uses a scaling constant by default (1.4826).
# Set constant = 1 to get the raw median of absolute deviations.
mad_values <- apply(friends, 2, mad, constant = 1)

# Standard deviation (sample, denominator n-1)
std_values <- apply(friends, 2, sd)

# Variance (sample, denominator n-1)
var_values <- apply(friends, 2, var)

# Combine into one matrix (rows = statistics, cols = attributes)
dispersion_matrix <- rbind(
  Amplitude = amplitudes,
  IQR       = iqr_values,
  MAD       = mad_values,
  StdDev    = std_values,
  Variance  = var_values
)

print(round(dispersion_matrix, 4))
cat("\n")


# ---------------------------------------------------------------
# 3. COVARIANCE MATRIX
# ---------------------------------------------------------------
# cov() computes the p x p sample covariance matrix (denominator n-1).
# Diagonal entries are the sample variances.
# The matrix is symmetric: cov[i,j] == cov[j,i].

cat("--- COVARIANCE MATRIX ---\n")
cat("  Diagonal = sample variance; symmetric; scale-DEPENDENT\n\n")

# Expected values from the lecture:
#   Max_temp/Max_temp = 55.52,  Weight/Weight = 302.15
#   Height/Height     = 126.53, Years/Years   = 31.98
#   Weight/Height     = 184.62
cov_matrix <- cov(friends)
print(round(cov_matrix, 2))
cat("\n")

# Verify diagonal values match the lecture
cat("Diagonal (should match lecture: 55.52, 302.15, 126.53, 31.98):\n")
cat(sprintf("  %s\n", paste(round(diag(cov_matrix), 2), collapse = "  ")))
cat("\n")


# ---------------------------------------------------------------
# 4. PEARSON CORRELATION MATRIX
# ---------------------------------------------------------------
# cor() computes the p x p Pearson correlation matrix.
# Diagonal entries are always 1.00.
# Values range from -1 to +1; matrix is symmetric.

cat("--- PEARSON CORRELATION MATRIX ---\n")
cat("  Diagonal = 1.00; range -1 to +1; scale-INDEPENDENT\n\n")

# Expected values from the lecture:
#   Weight/Height = 0.94  (very strong positive)
cor_matrix <- cor(friends)
print(round(cor_matrix, 4))
cat("\n")

# Plain-English interpretation of off-diagonal values
cat("Interpretation of off-diagonal r values:\n")
col_names <- names(friends)

for (i in seq_along(col_names)) {
  for (j in seq_along(col_names)) {
    if (j <= i) next   # only print each pair once (upper triangle)

    r    <- cor_matrix[i, j]
    absr <- abs(r)

    # Determine strength label
    if (absr >= 0.90) {
      strength <- "very strong"
    } else if (absr >= 0.70) {
      strength <- "strong"
    } else if (absr >= 0.50) {
      strength <- "moderate"
    } else if (absr >= 0.30) {
      strength <- "weak"
    } else {
      strength <- "negligible"
    }

    # Determine direction label
    if (r > 0) {
      direction <- "positive"
    } else if (r < 0) {
      direction <- "negative"
    } else {
      direction <- "no correlation"
    }

    label <- paste(strength, direction)

    cat(sprintf("  %-10s / %-10s : r = %+.4f  (%s)\n",
                col_names[i], col_names[j], r, label))
  }
}
cat("\n")


# ---------------------------------------------------------------
# SUMMARY: verify key values against lecture slides
# ---------------------------------------------------------------
cat("===================================================================\n")
cat("  VERIFICATION AGAINST LECTURE VALUES\n")
cat("===================================================================\n")
cat(sprintf("  cov(Max_temp, Max_temp) = %.2f  [lecture: 55.52]\n",
            cov_matrix["Max_temp", "Max_temp"]))
cat(sprintf("  cov(Weight,   Weight)   = %.2f  [lecture: 302.15]\n",
            cov_matrix["Weight", "Weight"]))
cat(sprintf("  cov(Height,   Height)   = %.2f  [lecture: 126.53]\n",
            cov_matrix["Height", "Height"]))
cat(sprintf("  cov(Years,    Years)    = %.2f  [lecture: 31.98]\n",
            cov_matrix["Years", "Years"]))
cat(sprintf("  cov(Weight,   Height)   = %.2f  [lecture: 184.62]\n",
            cov_matrix["Weight", "Height"]))
cat(sprintf("  r(Weight,     Height)   = %.4f [lecture: 0.94]\n",
            cor_matrix["Weight", "Height"]))
cat("===================================================================\n")
