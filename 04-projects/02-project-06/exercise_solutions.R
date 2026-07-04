# ==============================================================================
# Chapter 02
# 02-03-project-06: Chapter 2 Exercise Solutions  (R version)
# ==============================================================================
# Solves the three Ch.2 exercise questions using base R:
#
#   Ex02a Q1   Frequency table for the Weight attribute (Friends dataset)
#   Ex02a Q2   Mode, Median, Q1, Q3 for the Years attribute
#   Ex02b Q1   Covariance, Pearson r, Spearman rho for two short vectors
#
# Each section verifies its result against the expected exercise answer.
#
# Usage:
#   Rscript exercise_solutions.R
#   source("exercise_solutions.R")
# ==============================================================================


# ==============================================================================
# Helper: print a separator line
# ==============================================================================

sep_line <- function(char = "-", width = 70) {
  cat(paste(rep(char, width), collapse = ""), "\n")
}


# ==============================================================================
# Friends dataset (full version with Years column)
# ==============================================================================

friends <- data.frame(
  Friend   = c("Andrew","Bernhard","Carolina","Dennis","Eve","Fred",
               "Gwyneth","Hayden","Irene","James","Kevin","Lea","Marcus","Nigel"),
  Max_temp = c(25, 31, 15, 20, 10, 12, 16, 26, 15, 21, 30, 13,  8, 12),
  Weight   = c(77,110, 70, 85, 65, 75, 75, 63, 55, 66, 95, 72, 83,115),
  Height   = c(175,195,172,180,168,173,180,165,158,163,190,172,185,192),
  Gender   = c("M","M","F","M","F","M","F","F","F","M","M","F","F","M"),
  Company  = c("Good","Good","Bad","Good","Bad","Good","Bad","Bad",
               "Bad","Good","Bad","Good","Bad","Good"),
  Years    = c(5, 14, 2, 3, 16, 6, 11, 2, 15, 12, 0, 10, 1, 3),
  stringsAsFactors = FALSE
)

# Expected answers (for verification)
expected_years_mode   <- c(2, 3)
expected_years_median <- 5.5
expected_years_q1     <- 2.0
expected_years_q3     <- 12.0
expected_cov          <- -2.1
expected_pearson_r    <- -0.7626
expected_spearman_rho <- -0.8117


# ==============================================================================
# HELPER: custom mode function (R has no built-in mode for statistics)
# ==============================================================================

stat_mode <- function(x) {
  # Returns all values with the highest frequency (handles ties)
  counts    <- table(x)
  max_count <- max(counts)
  modes     <- as.numeric(names(counts[counts == max_count]))
  sort(modes)
}


# ==============================================================================
# Ex02a Q1 -- Frequency table for Weight
# ==============================================================================

sep_line("=")
cat("  Ex02a Q1  --  Frequency table for Weight\n")
sep_line("=")

weight <- friends$Weight
n      <- length(weight)

# Build absolute frequencies using table()
abs_freq <- table(weight)

# Relative frequency = absolute / n
rel_freq <- prop.table(abs_freq)

# Cumulative frequencies
cum_abs  <- cumsum(abs_freq)
cum_rel  <- cumsum(rel_freq)

# Print the table
cat(sprintf("\n  n = %d\n\n", n))
cat(sprintf("  %-8s  %9s  %9s  %8s  %8s\n",
            "Value", "Abs Freq", "Rel Freq", "Cum Abs", "Cum Rel"))
sep_line("-")
vals <- as.numeric(names(abs_freq))
for (i in seq_along(vals)) {
  cat(sprintf("  %-8g  %9d  %9.4f  %8d  %8.4f\n",
              vals[i],
              as.integer(abs_freq[i]),
              rel_freq[i],
              as.integer(cum_abs[i]),
              cum_rel[i]))
}
sep_line("=")
cat("\n")

# Verification: compare counts to expected
cat("  Verification:\n")
expected_weight_freq <- c(
  "55"=1, "63"=1, "65"=1, "66"=1, "70"=1, "72"=1, "75"=2,
  "77"=1, "83"=1, "85"=1, "95"=1, "110"=1, "115"=1
)
all_ok <- TRUE
for (nm in names(expected_weight_freq)) {
  computed <- as.integer(abs_freq[nm])
  expected <- expected_weight_freq[nm]
  status   <- ifelse(computed == expected, "PASS", "FAIL")
  if (status == "FAIL") all_ok <- FALSE
  cat(sprintf("    Weight = %3s  freq = %d  expected = %d  [%s]\n",
              nm, computed, expected, status))
}
if (all_ok) {
  cat("  All frequencies match the exercise key.\n")
}
cat("\n")


# ==============================================================================
# Ex02a Q2 -- Mode, Median, Q1, Q3 for Years
# ==============================================================================

sep_line("=")
cat("  Ex02a Q2  --  Mode, Median, Q1, Q3 for Years\n")
sep_line("=")

years        <- friends$Years
sorted_years <- sort(years)
n_years      <- length(years)

cat(sprintf("\n  Original : %s\n", paste(years, collapse = "  ")))
cat(sprintf("  Sorted   : %s   (n = %d)\n\n", paste(sorted_years, collapse = "  "), n_years))

# Mode
mode_vals <- stat_mode(years)
cat(sprintf("  Mode     : %s\n", paste(mode_vals, collapse = ", ")))

# Median
med_val <- median(years)
cat(sprintf("  Median   : %.1f\n", med_val))
cat(sprintf("             (n=%d is even -> average of positions %d and %d: (%d+%d)/2 = %.1f)\n",
            n_years, n_years/2, n_years/2+1,
            sorted_years[n_years/2], sorted_years[n_years/2+1], med_val))

# Q1 and Q3 -- using type=2 matches the textbook "lower/upper half" method
# type=2: (x[floor(n*p)] + x[ceiling(n*p)]) / 2  -- matches the textbook split
q1_val <- quantile(years, 0.25, type = 2)
q3_val <- quantile(years, 0.75, type = 2)
cat(sprintf("  Q1       : %.1f\n", q1_val))
cat(sprintf("  Q3       : %.1f\n", q3_val))
cat("\n")

# NOTE on quantile types:
# R's default quantile() uses type=7 (interpolation) which may give a
# different result from the textbook's "split halves" method.
# type=2 is closest to the textbook approach used in Ch.2 lecture slides.
cat("  Note: quantile(type=2) matches textbook 'lower/upper half' method.\n")
cat("\n")

# Verification
sep_line("-")
cat("  Verification:\n")

mode_match <- identical(mode_vals, expected_years_mode)
cat(sprintf("    Mode     : computed = [%s]  expected = [%s]  [%s]\n",
            paste(mode_vals, collapse=","),
            paste(expected_years_mode, collapse=","),
            ifelse(mode_match, "PASS", "FAIL")))

check <- function(label, computed, expected, tol=0.001) {
  status <- ifelse(abs(computed - expected) < tol, "PASS", "FAIL")
  cat(sprintf("    %-8s : computed = %8.4f  expected = %8.4f  [%s]\n",
              label, computed, expected, status))
}
check("Median", med_val,  expected_years_median)
check("Q1",     q1_val,   expected_years_q1)
check("Q3",     q3_val,   expected_years_q3)
sep_line("=")
cat("\n")


# ==============================================================================
# Ex02b Q1 -- Covariance, Pearson r, Spearman rho
# ==============================================================================

sep_line("=")
cat("  Ex02b Q1  --  Covariance, Pearson r, Spearman rho\n")
sep_line("=")

x <- c(2, -1, 0, 1, -2, -3)
y <- c(-1,  1, -2, 0,  1,  2)
n_xy <- length(x)

cat(sprintf("\n  x = (%s)\n", paste(x, collapse=", ")))
cat(sprintf("  y = (%s)\n\n", paste(y, collapse=", ")))

# ---------------------------------------------------------------------------
# Covariance (sample formula: divide by n-1)
# ---------------------------------------------------------------------------

x_bar <- mean(x)
y_bar <- mean(y)
cat(sprintf("  x_bar = %.4f   y_bar = %.4f\n\n", x_bar, y_bar))

# Step-by-step table
cat(sprintf("  %3s  %6s  %6s  %10s  %10s  %10s\n",
            "i", "xi", "yi", "xi-x_bar", "yi-y_bar", "product"))
sep_line("-", 60)
total_prod <- 0.0
for (i in seq_along(x)) {
  dx   <- x[i] - x_bar
  dy   <- y[i] - y_bar
  prod <- dx * dy
  total_prod <- total_prod + prod
  cat(sprintf("  %3d  %6g  %6g  %10.4f  %10.4f  %10.4f\n",
              i, x[i], y[i], dx, dy, prod))
}
sep_line("-", 60)
cov_manual <- total_prod / (n_xy - 1)
cat(sprintf("  Sum of products = %.4f\n", total_prod))
cat(sprintf("  cov = %.4f / %d = %.4f\n\n", total_prod, n_xy - 1, cov_manual))

# Using R's built-in cov()
cov_r <- cov(x, y)
cat(sprintf("  cov(x, y) via R's cov()  = %.4f\n", cov_r))
cat("\n")

# ---------------------------------------------------------------------------
# Pearson r
# ---------------------------------------------------------------------------

r_val <- cor(x, y, method = "pearson")
sx    <- sd(x)
sy    <- sd(y)
cat(sprintf("  PEARSON r\n"))
sep_line("-", 60)
cat(sprintf("  Formula: r = cov(x,y) / (sx * sy)\n"))
cat(sprintf("  sx = %.4f   sy = %.4f   sx*sy = %.4f\n", sx, sy, sx*sy))
cat(sprintf("  r  = %.4f / %.4f = %.4f\n\n", cov_r, sx*sy, r_val))

# ---------------------------------------------------------------------------
# Spearman rho
# ---------------------------------------------------------------------------

rho_val <- cor(x, y, method = "spearman")
rank_x  <- rank(x)
rank_y  <- rank(y)   # average ties by default

cat("  SPEARMAN rho\n")
sep_line("-", 60)
cat("  Method: Pearson's r on RANKS of x and y (ties -> average rank)\n\n")
cat(sprintf("  %3s  %6s  %6s  %8s  %8s\n", "i", "xi", "yi", "rank_x", "rank_y"))
sep_line("-", 60)
for (i in seq_along(x)) {
  cat(sprintf("  %3d  %6g  %6g  %8.1f  %8.1f\n",
              i, x[i], y[i], rank_x[i], rank_y[i]))
}
sep_line("-", 60)
cat("  Note: y has two values of 1 (sorted positions 4 and 5)\n")
cat("        -> each gets rank (4+5)/2 = 4.5\n")
cat(sprintf("  rho = cor(rank_x, rank_y) = %.4f\n\n", rho_val))

# ---------------------------------------------------------------------------
# Verification summary
# ---------------------------------------------------------------------------

sep_line("=")
cat("  VERIFICATION SUMMARY  --  Ex02b Q1\n")
sep_line("-")
check("Covariance",   cov_r,   expected_cov)
check("Pearson r",    r_val,   expected_pearson_r)
check("Spearman rho", rho_val, expected_spearman_rho)
sep_line("=")
cat("\n")
