# ============================================================
# Chapter 04
# 04-03-project-03: Normalization, Distance & Sampling (R)
# ============================================================
# Demonstrates:
#   - Min-max normalization
#   - Z-score standardization (scale())
#   - Euclidean distance (dist())
#   - Simple random sampling (sample())
#   - Stratified sampling
#
# Solves exercise Q4 and Q5.
#
# Usage: Rscript normalization_distance.R
# ============================================================


# ============================================================
# 1. DATA
# ============================================================

ex_q4_data <- c(31, 38, 42, 29, 46, 23, 83, 43, 51, 55, 27, 35)

ex_q4_expected <- c(0.133, 0.250, 0.317, 0.100, 0.383, 0.000, 1.000,
                    0.333, 0.467, 0.533, 0.067, 0.200)

ex_q5_x <- c(1, 3, -2, 5)
ex_q5_y <- c(2, 4,  1, 6)

# FRIENDS dataset
friends <- data.frame(
  name   = c("Rachel","Monica","Joey","Chandler","Phoebe","Ross","Richard","Gunther","Janice","Mike"),
  age    = c(26, 26, 27, 28, 28, 29, 39, 26, 30, 31),
  weight = c(54, 57, 73, 73, 52, 77, 80, 68, 61, 78),
  height = c(165, 162, 180, 178, 170, 186, 183, 175, 163, 179),
  salary = c(45000, 52000, 38000, 71000, 29000, 83000, 95000, 22000, 41000, 67000),
  gender = c("F","F","M","M","F","M","M","M","F","M"),
  stringsAsFactors = FALSE
)

# Lecture example: Bernhard, Gwyneth, James
people_df <- data.frame(
  name       = c("Bernhard", "Gwyneth", "James"),
  age_years  = c(43, 38, 42),
  salary     = c(72000, 55000, 84000),
  stringsAsFactors = FALSE
)


# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================

minmax_normalize <- function(x, new_min = 0, new_max = 1) {
  # Min-max normalization: maps x to [new_min, new_max]
  # Formula: v' = (v - min) / (max - min) * (new_max - new_min) + new_min
  x_min <- min(x, na.rm = TRUE)
  x_max <- max(x, na.rm = TRUE)
  x_range <- x_max - x_min

  if (x_range == 0) {
    return(rep(new_min, length(x)))   # all values the same -> map to new_min
  }

  (x - x_min) / x_range * (new_max - new_min) + new_min
}


# R built-in: scale() for z-score
# scale(x) returns column-wise mean=0, sd=1
# We also show the manual formula for clarity

zscore_normalize_manual <- function(x) {
  # Z-score: (v - mean) / sd  [sample sd: divides by n-1]
  (x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE)
}


# ============================================================
# 3. EXERCISE Q4: MIN-MAX NORMALIZATION
# ============================================================

cat("======================================================================\n")
cat("  NORMALIZATION, DISTANCE & SAMPLING -- Chapter 4 Demo (R)\n")
cat("======================================================================\n\n")

cat("--- EXERCISE Q4: Min-Max Normalize Q1 data to [0, 1] ---\n")
cat("Data:", paste(ex_q4_data, collapse = ", "), "\n\n")

q4_normalized <- minmax_normalize(ex_q4_data)

min_val <- min(ex_q4_data)
max_val <- max(ex_q4_data)
cat(sprintf("  min=%d, max=%d, formula: v' = (v - %d) / %d\n\n",
            min_val, max_val, min_val, max_val - min_val))

cat(sprintf("  %6s  %10s  %10s  %8s\n", "v", "Expected", "Computed", "Match"))
cat(paste(rep("-", 48), collapse = ""), "\n")

all_match_q4 <- TRUE
for (i in seq_along(ex_q4_data)) {
  computed <- round(q4_normalized[i], 3)
  expected <- ex_q4_expected[i]
  match    <- abs(computed - expected) < 0.001
  if (!match) all_match_q4 <- FALSE
  cat(sprintf("  %6d  %10.3f  %10.3f  %8s\n",
              ex_q4_data[i], expected, computed,
              ifelse(match, "YES", "NO")))
}
cat(sprintf("\n  Overall match: %s\n\n", ifelse(all_match_q4, "YES", "NO")))


# ============================================================
# 4. EXERCISE Q5: EUCLIDEAN DISTANCE
# ============================================================

cat("--- EXERCISE Q5: Euclidean Distance ---\n")
cat("  x =", paste(ex_q5_x, collapse = ", "), "\n")
cat("  y =", paste(ex_q5_y, collapse = ", "), "\n\n")

# Manual calculation
diffs   <- ex_q5_x - ex_q5_y
squares <- diffs ^ 2
dist_q5 <- sqrt(sum(squares))

cat("  differences :", paste(diffs,   collapse = ", "), "\n")
cat("  squares     :", paste(squares, collapse = ", "), "\n")
cat("  sum         :", sum(squares), "\n")
cat(sprintf("  sqrt        : %.4f\n\n", dist_q5))

expected_q5 <- sqrt(12)
cat(sprintf("  Expected: %.4f  Computed: %.4f  Match: %s\n\n",
            expected_q5, dist_q5,
            ifelse(abs(dist_q5 - expected_q5) < 0.001, "YES", "NO")))

# Using R's dist() function for verification
points_matrix <- rbind(ex_q5_x, ex_q5_y)
dist_builtin  <- as.numeric(dist(points_matrix, method = "euclidean"))
cat(sprintf("  Verification via R dist(): %.4f\n\n", dist_builtin))


# ============================================================
# 5. SCALE PROBLEM: BERNHARD / GWYNETH / JAMES
# ============================================================

cat("--- SCALE PROBLEM: Bernhard / Gwyneth / James ---\n\n")

# Distances without normalization (age in years)
pts_raw <- people_df[, c("age_years", "salary")]
rownames(pts_raw) <- people_df$name
dm_raw <- as.matrix(dist(pts_raw, method = "euclidean"))

cat("  Distances using age in YEARS (not normalized):\n")
print(round(dm_raw, 2))

# Age in decades (same data, different unit)
pts_decades <- people_df
pts_decades$age_years <- pts_decades$age_years / 10
pts_dec_matrix <- pts_decades[, c("age_years", "salary")]
rownames(pts_dec_matrix) <- pts_decades$name
dm_dec <- as.matrix(dist(pts_dec_matrix, method = "euclidean"))

cat("\n  Distances using age in DECADES (same data, different unit):\n")
print(round(dm_dec, 2))

cat("\n  Salary dominates; age scale is irrelevant. Solution: normalize.\n\n")

# After normalization
people_df$age_norm    <- minmax_normalize(people_df$age_years)
people_df$salary_norm <- minmax_normalize(people_df$salary)

pts_norm <- people_df[, c("age_norm", "salary_norm")]
rownames(pts_norm) <- people_df$name
dm_norm <- as.matrix(dist(pts_norm, method = "euclidean"))

cat("  Distances after min-max normalization:\n")
print(round(dm_norm, 4))

cat("\n  Both attributes now contribute equally.\n\n")


# ============================================================
# 6. FRIENDS DATASET: NORMALIZATION COMPARISON
# ============================================================

cat("--- FRIENDS DATASET: Normalization Comparison ---\n\n")

# Min-max normalization using manual formula
friends$age_mm  <- minmax_normalize(friends$age)
friends$age_z   <- as.numeric(scale(friends$age))   # scale() returns matrix; convert to vector
friends$sal_mm  <- minmax_normalize(friends$salary)
friends$sal_z   <- as.numeric(scale(friends$salary))

cat("  Age normalization:\n")
print(friends[, c("name", "age", "age_mm", "age_z")])

cat("\n  Salary normalization:\n")
print(friends[, c("name", "salary", "sal_mm", "sal_z")])

cat("\n  After normalization both attributes are on comparable scales.\n\n")


# ============================================================
# 7. SAMPLING DEMO
# ============================================================

cat("--- SAMPLING DEMO ---\n\n")

set.seed(42)   # for reproducibility

# Simple random sample WITHOUT replacement
cat("  Simple random sample, n=5, WITHOUT replacement:\n")
sample_no_rep <- sample(friends$name, size = 5, replace = FALSE)
cat("    ", paste(sample_no_rep, collapse = ", "), "\n\n")

# Simple random sample WITH replacement
cat("  Simple random sample, n=5, WITH replacement:\n")
sample_rep <- sample(friends$name, size = 5, replace = TRUE)
cat("    ", paste(sample_rep, collapse = ", "), "\n")
if (any(duplicated(sample_rep))) {
  cat("    (Note: duplicates present because replace=TRUE)\n")
}
cat("\n")

# Stratified sample: 2 per gender
cat("  Stratified sample, 2 per gender class:\n")

strat_sample_indices <- c()
for (cls in sort(unique(friends$gender))) {
  cls_rows <- which(friends$gender == cls)
  n_draw   <- min(2, length(cls_rows))
  chosen   <- sample(cls_rows, size = n_draw, replace = FALSE)
  strat_sample_indices <- c(strat_sample_indices, chosen)
  cat(sprintf("    gender='%s': %d available, %d sampled -> rows %s\n",
              cls, length(cls_rows), n_draw, paste(sort(chosen), collapse=", ")))
}

strat_sample_indices <- sort(strat_sample_indices)
cat("\n  Selected rows:\n")
print(friends[strat_sample_indices, c("name", "gender")])

cat("\n======================================================================\n")
cat("  Demo complete.\n")
cat("======================================================================\n")
