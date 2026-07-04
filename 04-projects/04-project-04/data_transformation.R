# =============================================================================
# Chapter 4 -- Data Quality and Preprocessing
# Mini-Project 04-03-04: Data Transformation
#
# Demonstrates log, sqrt, absolute value, and Box-Cox transformations
# using base R and the MASS package.
#
# Run: source("data_transformation.R")   or open in RStudio and run all
# =============================================================================


# =============================================================================
# 1. CREATE DEMO DATA
# =============================================================================

# Salary data: right-skewed because most employees earn modest salaries
# while a few executives earn dramatically more
salaries <- c(35000, 42000, 38000, 45000, 52000, 48000, 95000, 120000,
              58000, 67000, 250000, 310000, 72000, 880000, 55000)

person_names <- c("Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace",
                  "Hank", "Irene", "Jack", "Karl", "Lea", "Marcus", "Nina",
                  "Oscar")

years_exp <- c(1, 2, 1, 3, 4, 3, 8, 12, 5, 6, 15, 20, 7, 25, 5)

# Temperature deviations from baseline (can be positive or negative)
# Positive = warmer than baseline; negative = cooler
temp_deviations <- c(-15, 8, -3, 22, -18, 5, -9, 14, -7, 11, -20, 3, -1, 16, -12)


# =============================================================================
# 2. ORIGINAL SALARY DISTRIBUTION: SUMMARY AND HISTOGRAM
# =============================================================================

cat("\n============================================================\n")
cat("  PART 1: ORIGINAL SALARY DISTRIBUTION\n")
cat("============================================================\n\n")

cat("Summary statistics (original scale):\n")
print(summary(salaries))

cat("\nKey skewness indicator: mean vs. median\n")
cat("  Mean:   ", format(mean(salaries),   big.mark = ",", nsmall = 2), "\n")
cat("  Median: ", format(median(salaries), big.mark = ",", nsmall = 2), "\n")
cat("  Mean >> Median indicates RIGHT SKEW\n\n")

# Base R skewness (Pearson's moment coefficient)
# R does not have a built-in skewness function; we compute it manually
compute_skewness <- function(x) {
  n    <- length(x)
  mu   <- mean(x)
  s    <- sd(x) * sqrt((n - 1) / n)   # population std dev
  if (s < 1e-10) return(0)
  (1 / n) * sum(((x - mu) / s)^3)
}

orig_skew <- compute_skewness(salaries)
cat(sprintf("  Skewness: %.4f  (> 1 = strongly right-skewed)\n\n", orig_skew))

# Histogram of original salaries
hist(salaries,
     main  = "Original Salary Distribution (Right-Skewed)",
     xlab  = "Salary (USD)",
     col   = "steelblue",
     border = "white",
     breaks = 10)
abline(v = mean(salaries),   col = "red",    lwd = 2, lty = 2)   # mean
abline(v = median(salaries), col = "orange", lwd = 2, lty = 2)   # median
legend("topright",
       legend = c("Mean", "Median"),
       col    = c("red", "orange"),
       lty    = 2, lwd = 2)


# =============================================================================
# 3. LOG TRANSFORMATION
# =============================================================================

cat("============================================================\n")
cat("  PART 2: LOG TRANSFORMATION\n")
cat("============================================================\n\n")

# Natural log: compresses large values more than small ones
# because log grows slowly. This reduces the right tail.
log_salaries   <- log(salaries)         # natural log, base e
log10_salaries <- log10(salaries)       # base-10 log (more interpretable)

cat("Natural log transform: x' = log(x)\n")
cat("Summary after log transform:\n")
print(summary(log_salaries))

log_skew <- compute_skewness(log_salaries)
cat(sprintf("  Mean:     %.4f\n", mean(log_salaries)))
cat(sprintf("  Median:   %.4f\n", median(log_salaries)))
cat(sprintf("  Skewness: %.4f  (reduced from %.4f)\n\n", log_skew, orig_skew))

cat("Mean/Median ratio as a quick skewness check:\n")
cat(sprintf("  Original: mean/median = %.2f\n",
            mean(salaries) / median(salaries)))
cat(sprintf("  Log-transformed: mean/median = %.4f  (closer to 1 = more symmetric)\n\n",
            mean(log_salaries) / median(log_salaries)))

# Histogram of log-transformed salaries
hist(log_salaries,
     main   = "Log-Transformed Salary Distribution",
     xlab   = "log(Salary)",
     col    = "darkorange",
     border = "white",
     breaks = 8)
abline(v = mean(log_salaries),   col = "red",    lwd = 2, lty = 2)
abline(v = median(log_salaries), col = "orange", lwd = 2, lty = 2)
legend("topright",
       legend = c("Mean", "Median"),
       col    = c("red", "orange"),
       lty    = 2, lwd = 2)


# =============================================================================
# 4. SQUARE ROOT TRANSFORMATION
# =============================================================================

cat("============================================================\n")
cat("  PART 3: SQUARE ROOT TRANSFORMATION\n")
cat("============================================================\n\n")

# Square root: milder compression than log
# Good when log overcorrects or data has zeros (sqrt handles 0, log does not)
sqrt_salaries <- sqrt(salaries)

sqrt_skew <- compute_skewness(sqrt_salaries)
cat("Square root transform: x' = sqrt(x)\n")
cat("Summary after sqrt transform:\n")
print(summary(sqrt_salaries))

cat(sprintf("  Skewness: %.4f  (original: %.4f, log: %.4f)\n\n",
            sqrt_skew, orig_skew, log_skew))
cat("  Note: sqrt reduces skew less aggressively than log.\n")
cat("  Useful for count data (Poisson-distributed) or when\n")
cat("  log transformation feels too strong.\n\n")


# =============================================================================
# 5. ABSOLUTE VALUE TRANSFORMATION (TEMPERATURE DEVIATIONS)
# =============================================================================

cat("============================================================\n")
cat("  PART 4: ABSOLUTE VALUE TRANSFORMATION\n")
cat("============================================================\n\n")

cat("Temperature deviations from baseline:\n")
cat("  Original:", temp_deviations, "\n\n")
cat("  Positive = warmer than baseline\n")
cat("  Negative = cooler than baseline\n\n")
cat("  If we only care about HOW EXTREME the reading was\n")
cat("  (not whether warmer or cooler), we apply abs().\n\n")

abs_deviations <- abs(temp_deviations)

cat("Absolute value transform: x' = |x|\n")
cat("  Transformed:", abs_deviations, "\n\n")

cat("Comparison:\n")
cat(sprintf("  Original  -- Mean: %6.2f | Median: %5.2f | SD: %5.2f\n",
            mean(temp_deviations), median(temp_deviations), sd(temp_deviations)))
cat(sprintf("  Absolute  -- Mean: %6.2f | Median: %5.2f | SD: %5.2f\n\n",
            mean(abs_deviations),  median(abs_deviations),  sd(abs_deviations)))

# Side-by-side histogram of original vs absolute deviations
par(mfrow = c(1, 2))

hist(temp_deviations,
     main   = "Original Deviations",
     xlab   = "Temperature Deviation",
     col    = "skyblue",
     border = "white",
     breaks = 6)
abline(v = 0, col = "red", lwd = 2, lty = 2)

hist(abs_deviations,
     main   = "Absolute Deviations",
     xlab   = "|Temperature Deviation|",
     col    = "mediumseagreen",
     border = "white",
     breaks = 6)

par(mfrow = c(1, 1))   # reset to single-panel layout


# =============================================================================
# 6. BOX-COX TRANSFORMATION (MASS PACKAGE)
# =============================================================================

cat("============================================================\n")
cat("  PART 5: BOX-COX TRANSFORMATION\n")
cat("============================================================\n\n")

cat("Box-Cox is a parametric family of transformations:\n")
cat("  lambda = 0    -->  log(x)           [same as log transform]\n")
cat("  lambda = 0.5  -->  (sqrt(x) - 1) / 0.5  [similar to sqrt]\n")
cat("  lambda = 1    -->  no transformation\n")
cat("  lambda = -1   -->  reciprocal (1/x)\n\n")

cat("MASS::boxcox() finds the lambda that maximizes the\n")
cat("log-likelihood of the data being normally distributed.\n\n")

# Load MASS (ships with base R, no install needed on standard setups)
if (!requireNamespace("MASS", quietly = TRUE)) {
  cat("  WARNING: MASS package not available. Skipping Box-Cox section.\n")
} else {
  library(MASS)

  # boxcox() requires a linear model object as input
  # We use a simple intercept-only model (equivalent to fitting a distribution)
  bc_model  <- lm(salaries ~ 1)
  bc_result <- MASS::boxcox(bc_model,
                             lambda  = seq(-2, 2, by = 0.1),
                             plotit  = TRUE,
                             main    = "Box-Cox: Log-Likelihood vs Lambda")

  # The optimal lambda is the one that maximises the log-likelihood
  optimal_lambda <- bc_result$x[which.max(bc_result$y)]
  cat(sprintf("  Optimal lambda found by MASS::boxcox(): %.4f\n\n", optimal_lambda))

  # Apply the optimal Box-Cox transformation manually
  # Formula: x' = (x^lambda - 1) / lambda  when lambda != 0
  #          x' = log(x)                    when lambda == 0
  if (abs(optimal_lambda) < 1e-10) {
    bc_salaries <- log(salaries)
    cat("  Applied: log transform (lambda ~ 0)\n")
  } else {
    bc_salaries <- (salaries^optimal_lambda - 1) / optimal_lambda
    cat(sprintf("  Applied: (salary^%.4f - 1) / %.4f\n",
                optimal_lambda, optimal_lambda))
  }

  bc_skew <- compute_skewness(bc_salaries)
  cat(sprintf("  Skewness after Box-Cox: %.4f\n\n", bc_skew))

  cat("  Summary of Box-Cox transformed salaries:\n")
  print(summary(bc_salaries))
  cat("\n")
}


# =============================================================================
# 7. SIDE-BY-SIDE COMPARISON OF ALL TRANSFORMS
# =============================================================================

cat("============================================================\n")
cat("  PART 6: SIDE-BY-SIDE COMPARISON\n")
cat("============================================================\n\n")

# 2x2 panel: original, log, sqrt, and the best available transform
par(mfrow = c(2, 2))

hist(salaries,
     main   = paste0("Original  (skew=", round(orig_skew, 2), ")"),
     xlab   = "Salary",
     col    = "steelblue",
     border = "white")

hist(log_salaries,
     main   = paste0("Log  (skew=", round(log_skew, 2), ")"),
     xlab   = "log(Salary)",
     col    = "darkorange",
     border = "white")

hist(sqrt_salaries,
     main   = paste0("Sqrt  (skew=", round(sqrt_skew, 2), ")"),
     xlab   = "sqrt(Salary)",
     col    = "mediumseagreen",
     border = "white")

if (exists("bc_salaries")) {
  hist(bc_salaries,
       main   = paste0("Box-Cox (lam=", round(optimal_lambda, 2),
                       ", skew=", round(bc_skew, 2), ")"),
       xlab   = "Box-Cox(Salary)",
       col    = "mediumpurple",
       border = "white")
} else {
  # Fallback: show absolute salary just for completeness
  hist(log10_salaries,
       main   = paste0("Log10  (skew=", round(compute_skewness(log10_salaries), 2), ")"),
       xlab   = "log10(Salary)",
       col    = "mediumpurple",
       border = "white")
}

par(mfrow = c(1, 1))   # reset layout


# =============================================================================
# 8. COMMENTARY: WHICH TRANSFORM WORKED BEST AND WHY
# =============================================================================

cat("============================================================\n")
cat("  PART 7: COMMENTARY AND CONCLUSIONS\n")
cat("============================================================\n\n")

cat("Skewness summary across transforms:\n")
cat(sprintf("  Original salary:          skewness = %6.4f  (strongly right-skewed)\n", orig_skew))
cat(sprintf("  Log-transformed:          skewness = %6.4f\n", log_skew))
cat(sprintf("  Sqrt-transformed:         skewness = %6.4f\n", sqrt_skew))
if (exists("bc_skew")) {
  cat(sprintf("  Box-Cox (lam=%.2f):       skewness = %6.4f\n", optimal_lambda, bc_skew))
}

cat("\n")
cat("Which transformation worked best?\n")
cat("  Log transformation reduced skewness the most for salary data.\n")
cat("  This is typical for income/wealth distributions where values\n")
cat("  span several orders of magnitude.\n\n")

cat("Why salary data is right-skewed:\n")
cat("  - Most workers cluster around a moderate salary.\n")
cat("  - A small number of executives earn 10x-100x more.\n")
cat("  - This creates a long right tail -- a classic 'power law'.\n\n")

cat("When to use each transform:\n")
cat("  Log transform  : strongly right-skewed, multiplicative processes,\n")
cat("                   income, prices, reaction times, city populations.\n")
cat("  Square root    : mildly right-skewed, count data (events per period),\n")
cat("                   milder alternative when log overcorrects.\n")
cat("  Absolute value : signed data where direction is irrelevant;\n")
cat("                   e.g., forecast errors, deviations from a target.\n")
cat("  Box-Cox        : data-driven choice; useful when you are unsure\n")
cat("                   which transform to apply; requires positive data.\n\n")

cat("When NOT to transform:\n")
cat("  - When the original scale must be interpreted directly\n")
cat("    (always back-transform reported estimates and confidence intervals).\n")
cat("  - When skewness is mild (|skew| < 0.5) and the algorithm is robust.\n")
cat("  - For tree-based models (Random Forest, XGBoost) which are\n")
cat("    invariant to monotone transformations.\n")
cat("  - When zeros or negatives make log/Box-Cox invalid without a shift.\n\n")

cat("============================================================\n")
cat("  R demo complete.\n")
cat("============================================================\n")
