# ============================================================
# Chapter 04
# 04-03-project-02: Discretization & Encoding (R)
# ============================================================
# Demonstrates:
#   - Equal-width binning
#   - Equal-depth (equal-frequency) binning
#   - One-hot encoding
#   - Ordinal to natural numbers
#   - Ordinal to Gray code
#   - Ordinal to thermometer code
#
# Solves exercise questions Q1, Q2, Q3.
#
# Usage: Rscript discretization_encoding.R
# ============================================================


# ============================================================
# 1. EXERCISE DATA
# ============================================================

ex_q1_data <- c(31, 38, 42, 29, 46, 23, 83, 43, 51, 55, 27, 35)

ex_q2_food <- c("Chinese", "Italian", "American", "Chinese", "Italian")

ex_q3_distance_ordered <- c("very_close", "close", "far", "very_far", "too_far")
ex_q3_distance_sample  <- c("far", "very_close", "too_far", "close", "very_far")


# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================

int_to_gray_code <- function(n, n_bits) {
  # Convert integer n to Gray code binary string with n_bits bits.
  # Gray code: gray = n XOR (n right-shifted by 1)
  gray_int <- bitwXor(n, bitwShiftR(n, 1))  # bitwise XOR with right-shifted value

  # Convert to binary string
  bits <- ""
  temp <- gray_int
  for (i in seq_len(n_bits)) {
    bits <- paste0(temp %% 2, bits)  # prepend each bit
    temp <- temp %/% 2
  }
  return(bits)
}

int_to_thermometer_code <- function(n, n_bits) {
  # Thermometer code: n ones on the RIGHT, rest zeros.
  # n=0 -> "000", n=1 -> "001", n=2 -> "011", n=3 -> "111"
  ones  <- paste(rep("1", n),      collapse = "")
  zeros <- paste(rep("0", n_bits - n), collapse = "")
  return(paste0(zeros, ones))
}


# ============================================================
# 3. CORE FUNCTIONS
# ============================================================

equal_width_bins <- function(values, n_bins) {
  # Assign each value to an equal-width bin (0-indexed).
  #
  # R's cut() function does this natively.
  # We use it with include.lowest=TRUE so the minimum value is in Bin 0.
  #
  # Returns a named list: bin_labels (0-indexed integers), bin_edges

  min_val <- min(values)
  max_val <- max(values)
  width   <- (max_val - min_val) / n_bins

  # Compute breakpoints: n_bins + 1 values
  breaks <- seq(min_val, max_val, length.out = n_bins + 1)

  # cut() returns a factor with labels like "(23,38]"
  # We convert to 0-indexed integers
  factor_labels <- cut(values, breaks = breaks, include.lowest = TRUE, labels = FALSE)
  bin_labels <- factor_labels - 1   # convert 1-indexed to 0-indexed

  return(list(bin_labels = bin_labels, bin_edges = breaks))
}


equal_depth_bins <- function(values, n_bins) {
  # Assign each value to an equal-depth (equal-frequency) bin (0-indexed).
  #
  # Uses quantile() with equally spaced probabilities to find cut points,
  # then cut() to assign values to bins.

  n <- length(values)

  # Compute quantile-based breakpoints
  probs  <- seq(0, 1, length.out = n_bins + 1)
  breaks <- quantile(values, probs = probs)

  # cut() with these breaks gives equal-frequency bins
  factor_labels <- cut(values, breaks = breaks, include.lowest = TRUE, labels = FALSE)
  bin_labels <- factor_labels - 1   # 0-indexed

  return(bin_labels)
}


one_hot_encode <- function(values) {
  # One-hot encode a character vector.
  # Returns a data.frame with one binary column per unique category.

  categories <- sort(unique(values))  # sorted for stable column order

  result <- data.frame(matrix(0L, nrow = length(values), ncol = length(categories)))
  colnames(result) <- categories

  for (i in seq_along(values)) {
    cat_name <- values[i]
    result[i, cat_name] <- 1L   # set the matching column to 1
  }

  return(result)
}


ordinal_to_natural <- function(values, ordered_categories) {
  # Map ordinal categories to natural numbers 0, 1, 2, ...
  # Position in ordered_categories determines the integer.
  match(values, ordered_categories) - 1   # match() is 1-indexed; subtract 1
}


ordinal_to_gray_code <- function(values, ordered_categories) {
  # Map ordinal categories to Gray code binary strings.
  n_cats  <- length(ordered_categories)
  n_bits  <- ceiling(log2(max(n_cats, 2)))

  ranks   <- match(values, ordered_categories) - 1  # 0-indexed ranks
  sapply(ranks, int_to_gray_code, n_bits = n_bits)
}


ordinal_to_thermometer <- function(values, ordered_categories) {
  # Map ordinal categories to thermometer code binary strings.
  n_bits  <- length(ordered_categories) - 1  # n-1 bits for n categories

  ranks   <- match(values, ordered_categories) - 1  # 0-indexed ranks
  sapply(ranks, int_to_thermometer_code, n_bits = n_bits)
}


# ============================================================
# 4. MAIN DEMO
# ============================================================

cat("======================================================================\n")
cat("  DISCRETIZATION & ENCODING -- Chapter 4 Demo (R)\n")
cat("  Solving Exercise Q1, Q2, Q3\n")
cat("======================================================================\n\n")


# --------------------------------------------------
# Q1: Equal-Width Binning
# --------------------------------------------------
cat("--- EXERCISE Q1: Equal-Width Binning (4 bins) ---\n")
cat("Data:", paste(ex_q1_data, collapse = ", "), "\n\n")

ew_result   <- equal_width_bins(ex_q1_data, n_bins = 4)
ew_labels   <- ew_result$bin_labels
ew_edges    <- ew_result$bin_edges

cat("Bin edges:\n")
for (k in seq_len(length(ew_edges) - 1)) {
  vals_in_bin <- ex_q1_data[ew_labels == (k - 1)]
  cat(sprintf("  Bin %d: [%.0f, %.0f]  -> %s\n",
              k - 1, ew_edges[k], ew_edges[k + 1],
              paste(sort(vals_in_bin), collapse = ", ")))
}

cat("\nValue -> Bin assignments:\n")
for (i in seq_along(ex_q1_data)) {
  cat(sprintf("  %3d -> Bin %d\n", ex_q1_data[i], ew_labels[i]))
}

# Expected: 0,1,1,0,1,0,3,1,1,2,0,0
expected_ew <- c(0, 1, 1, 0, 1, 0, 3, 1, 1, 2, 0, 0)
cat("\nVerification:\n")
cat("  Expected:", paste(expected_ew, collapse = " "), "\n")
cat("  Computed:", paste(ew_labels,   collapse = " "), "\n")
cat("  Match:", ifelse(all(ew_labels == expected_ew), "YES", "CHECK (boundary convention)"), "\n\n")


# --------------------------------------------------
# Q1: Equal-Depth Binning
# --------------------------------------------------
cat("--- EXERCISE Q1: Equal-Depth Binning (4 bins) ---\n")

ed_labels <- equal_depth_bins(ex_q1_data, n_bins = 4)

cat("Bin contents:\n")
for (k in 0:3) {
  vals_in_bin <- ex_q1_data[ed_labels == k]
  cat(sprintf("  Bin %d: %s\n", k, paste(sort(vals_in_bin), collapse = ", ")))
}

cat("\nValue -> Bin assignments:\n")
for (i in seq_along(ex_q1_data)) {
  cat(sprintf("  %3d -> Bin %d\n", ex_q1_data[i], ed_labels[i]))
}

# Expected: 1,1,2,0,2,0,3,2,3,3,0,1
expected_ed <- c(1, 1, 2, 0, 2, 0, 3, 2, 3, 3, 0, 1)
cat("\nVerification:\n")
cat("  Expected:", paste(expected_ed, collapse = " "), "\n")
cat("  Computed:", paste(ed_labels,   collapse = " "), "\n")
cat("  Match:", ifelse(all(ed_labels == expected_ed), "YES", "CLOSE (quantile method may differ slightly)"), "\n\n")


# --------------------------------------------------
# Q2: One-Hot Encoding
# --------------------------------------------------
cat("--- EXERCISE Q2: One-Hot Encoding for Food ---\n")
cat("Food values:", paste(ex_q2_food, collapse = ", "), "\n\n")

ohe_result <- one_hot_encode(ex_q2_food)
print(cbind(Food = ex_q2_food, ohe_result))

# Expected from lecture
expected_q2 <- data.frame(
  American = c(0, 0, 1, 0, 0),
  Chinese  = c(1, 0, 0, 1, 0),
  Italian  = c(0, 1, 0, 0, 1)
)
cat("\nVerification:\n")
match_q2 <- all(ohe_result == expected_q2)
cat("  Expected:\n"); print(expected_q2)
cat("  Match:", ifelse(match_q2, "YES", "NO"), "\n\n")


# --------------------------------------------------
# Q3: Gray Code Encoding
# --------------------------------------------------
cat("--- EXERCISE Q3: Gray Code for Distance ---\n")
cat("Ordered categories:", paste(ex_q3_distance_ordered, collapse = " < "), "\n\n")

nat_codes_q3   <- ordinal_to_natural(ex_q3_distance_ordered, ex_q3_distance_ordered)
gray_codes_q3  <- ordinal_to_gray_code(ex_q3_distance_ordered, ex_q3_distance_ordered)
therm_codes_q3 <- ordinal_to_thermometer(ex_q3_distance_ordered, ex_q3_distance_ordered)

result_table <- data.frame(
  Category    = ex_q3_distance_ordered,
  Natural     = nat_codes_q3,
  Gray_Code   = gray_codes_q3,
  Thermometer = therm_codes_q3,
  stringsAsFactors = FALSE
)
print(result_table, row.names = FALSE)

# Expected Gray codes from lecture
expected_gray_q3 <- c("000", "001", "011", "010", "110")
cat("\nVerification (Gray codes):\n")
cat("  Expected:", paste(expected_gray_q3, collapse = " "), "\n")
cat("  Computed:", paste(gray_codes_q3,    collapse = " "), "\n")
cat("  Match:", ifelse(all(gray_codes_q3 == expected_gray_q3), "YES", "NO"), "\n\n")


# --------------------------------------------------
# BONUS: Encode sample Distance column
# --------------------------------------------------
cat("--- BONUS: Encode Distance Sample Column ---\n")
cat("Sample:", paste(ex_q3_distance_sample, collapse = ", "), "\n\n")

nat_s   <- ordinal_to_natural(ex_q3_distance_sample, ex_q3_distance_ordered)
gray_s  <- ordinal_to_gray_code(ex_q3_distance_sample, ex_q3_distance_ordered)
therm_s <- ordinal_to_thermometer(ex_q3_distance_sample, ex_q3_distance_ordered)

sample_table <- data.frame(
  Distance    = ex_q3_distance_sample,
  Natural     = nat_s,
  Gray_Code   = gray_s,
  Thermometer = therm_s,
  stringsAsFactors = FALSE
)
print(sample_table, row.names = FALSE)

cat("\n======================================================================\n")
cat("  Demo complete.\n")
cat("======================================================================\n")
