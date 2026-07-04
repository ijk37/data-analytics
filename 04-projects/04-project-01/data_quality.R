# ============================================================
# Chapter 04
# 04-03-project-01: Data Quality Auditor (R)
# ============================================================
# Demonstrates detection and repair of common data quality problems
# using base R only:
#   - Missing value detection (is.na, complete.cases)
#   - Fill with mean, median, mode
#   - Per-class (per-group) imputation
#   - Duplicate detection and removal (duplicated)
#   - Outlier detection via IQR fencing
#
# Usage: Rscript data_quality.R
# ============================================================


# ============================================================
# 1. DEMO DATASET
# ============================================================

# FRIENDS-inspired dataset with injected quality problems:
#   - Phoebe (row 5): age is NA
#   - Gunther (row 8): weight is NA
#   - Janice (row 9): city is NA
#   - Mike (row 10): exact duplicate of Richard (row 7)
#   - Joey (row 3): weight = 1100 (clearly inconsistent)

demo_data <- data.frame(
  name   = c("Rachel","Monica","Joey","Chandler","Phoebe","Ross","Richard","Gunther","Janice","Mike"),
  age    = c(26, 26, 27, 28, NA, 29, 39, 26, 30, 31),
  weight = c(54, 57, 1100, 73, 52, 77, 80, NA, 61, 78),
  height = c(165, 162, 180, 178, 170, 186, 183, 175, 163, 179),
  city   = c("New York","New York","New York","New York","New York","New York","New York","New York",NA,"New York"),
  gender = c("F","F","M","M","F","M","M","M","F","M"),
  stringsAsFactors = FALSE
)


# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================

# Custom mode function (base R has no built-in mode for statistics)
compute_mode <- function(x) {
  # Remove NA values before computing
  x_clean <- x[!is.na(x)]
  if (length(x_clean) == 0) return(NA)

  # Count frequencies using table()
  freq_table <- table(x_clean)

  # Find the maximum frequency
  max_freq <- max(freq_table)

  # Return the first value with that frequency (alphabetical tie-break)
  mode_val <- names(freq_table)[freq_table == max_freq][1]
  return(mode_val)
}


# ============================================================
# 3. SECTION: MISSING VALUE AUDIT
# ============================================================

cat("======================================================================\n")
cat("  DATA QUALITY AUDITOR -- Chapter 4 Demo (R)\n")
cat("  Dataset: FRIENDS cast (with injected quality issues)\n")
cat("======================================================================\n\n")

cat("--- STEP 1: MISSING VALUE AUDIT ---\n\n")

# is.na() returns a logical vector: TRUE where value is NA
# colSums counts TRUE values per column
missing_counts <- colSums(is.na(demo_data))
n_rows <- nrow(demo_data)

cat("Missing values per column:\n")
for (col in names(missing_counts)) {
  cnt <- missing_counts[col]
  pct <- cnt / n_rows * 100
  if (cnt > 0) {
    cat(sprintf("  %-10s : %d missing  (%.1f%%)\n", col, cnt, pct))
  }
}

# complete.cases() returns TRUE for rows with NO missing values
n_complete <- sum(complete.cases(demo_data))
cat(sprintf("\n  Complete rows (no missing values): %d / %d\n", n_complete, n_rows))


# ============================================================
# 4. SECTION: FILL MISSING VALUES
# ============================================================

cat("\n--- STEP 2: FILLING MISSING VALUES ---\n\n")

# Work on a copy so we can compare before/after
df <- demo_data

# -- age: quantitative, symmetric -> fill with mean --
age_mean <- mean(df$age, na.rm = TRUE)   # na.rm=TRUE skips NA in computation
cat(sprintf("  age: mean of non-missing values = %.2f\n", age_mean))

missing_age_rows <- which(is.na(df$age))   # which() returns indices of TRUE
cat(sprintf("  Filling row(s) %s with mean %.2f\n",
            paste(missing_age_rows, collapse=", "), age_mean))
df$age[is.na(df$age)] <- age_mean   # replace NA with mean


# -- weight: has outlier (1100) -> fill with median for robustness --
weight_median <- median(df$weight, na.rm = TRUE)
cat(sprintf("\n  weight: median of non-missing values = %.2f\n", weight_median))

missing_weight_rows <- which(is.na(df$weight))
cat(sprintf("  Filling row(s) %s with median %.2f\n",
            paste(missing_weight_rows, collapse=", "), weight_median))
df$weight[is.na(df$weight)] <- weight_median


# -- city: nominal -> fill with mode --
city_mode <- compute_mode(df$city)
cat(sprintf("\n  city: mode = '%s'\n", city_mode))

missing_city_rows <- which(is.na(df$city))
cat(sprintf("  Filling row(s) %s with mode '%s'\n",
            paste(missing_city_rows, collapse=", "), city_mode))
df$city[is.na(df$city)] <- city_mode


# -- Per-class fill: fill age using gender group mean --
cat("\n  Per-class fill (age by gender group) -- for comparison:\n")

# tapply computes mean per group, ignoring NAs
class_means <- tapply(demo_data$age, demo_data$gender, mean, na.rm = TRUE)
cat("  Group means:\n")
for (g in names(class_means)) {
  cat(sprintf("    gender=%s : mean age = %.2f\n", g, class_means[g]))
}

# Apply per-class fill to original (with NA)
age_per_class <- demo_data$age
for (i in which(is.na(age_per_class))) {
  grp <- demo_data$gender[i]
  age_per_class[i] <- class_means[grp]
}
cat("  Rows filled by class:\n")
for (i in which(is.na(demo_data$age))) {
  cat(sprintf("    Row %d (%s) : NA --> %.2f\n",
              i, demo_data$gender[i], age_per_class[i]))
}


# ============================================================
# 5. SECTION: DUPLICATE DETECTION
# ============================================================

cat("\n--- STEP 3: DUPLICATE DETECTION ---\n\n")

# duplicated() returns TRUE for every row that is a duplicate of an earlier row
dup_flags <- duplicated(df)
n_dups <- sum(dup_flags)
cat(sprintf("  Duplicate rows found: %d\n", n_dups))

if (n_dups > 0) {
  cat("  Duplicate row indices:\n")
  dup_rows <- which(dup_flags)
  for (i in dup_rows) {
    cat(sprintf("    Row %d : name = %s\n", i, df$name[i]))
  }
  # Remove duplicates: keep only rows where duplicated() is FALSE
  df_dedup <- df[!dup_flags, ]
  cat(sprintf("  After deduplication: %d rows remain\n", nrow(df_dedup)))
  df <- df_dedup
}


# ============================================================
# 6. SECTION: OUTLIER DETECTION (IQR)
# ============================================================

cat("\n--- STEP 4: OUTLIER DETECTION (IQR method) ---\n\n")

detect_outliers_iqr <- function(values, col_name, multiplier = 1.5) {
  # Remove NAs before computing quartiles
  clean_vals <- values[!is.na(values)]

  if (length(clean_vals) < 4) {
    cat(sprintf("  %s : not enough values for IQR analysis\n", col_name))
    return(invisible(NULL))
  }

  q1  <- quantile(clean_vals, 0.25)
  q3  <- quantile(clean_vals, 0.75)
  iqr <- q3 - q1

  lower <- q1 - multiplier * iqr
  upper <- q3 + multiplier * iqr

  cat(sprintf("  %s : Q1=%.1f, Q3=%.1f, IQR=%.1f  |  bounds: [%.1f, %.1f]\n",
              col_name, q1, q3, iqr, lower, upper))

  # Find indices of flagged values (check against original, including NAs)
  for (i in seq_along(values)) {
    v <- values[i]
    if (!is.na(v) && (v < lower || v > upper)) {
      cat(sprintf("    --> Index %d : value %.1f FLAGGED as outlier\n", i, v))
    }
  }
}

# Check weight (original data, including the injected 1100 outlier)
detect_outliers_iqr(demo_data$weight, "weight (original with 1100)")

# Check age
detect_outliers_iqr(df$age, "age (after fill)")


# ============================================================
# 7. FINAL STATE
# ============================================================

cat("\n======================================================================\n")
cat("  AFTER: Cleaned Data\n")
cat("======================================================================\n")
print(df)

cat("\nSummary of changes:\n")
cat("  - 3 missing values filled (age: mean, weight: median, city: mode)\n")
cat("  - 1 duplicate row removed\n")
cat("  - 1 outlier flagged in weight column (value: 1100)\n")
cat("    NOTE: outlier was flagged but NOT removed automatically.\n")
cat("    Investigate before deciding to remove.\n")
cat("======================================================================\n")
