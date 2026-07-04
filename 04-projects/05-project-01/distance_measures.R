# =============================================================================
# Project 01: Distance Measures (R Version)
# Chapter 5 - Clustering
# Data Analytics Course
#
# Demonstrates all distance measures from the lecture:
#   - Quantitative, ordinal, nominal (single-attribute)
#   - Minkowski family: Manhattan, Euclidean, general r
#   - Hamming distance (strings and binary sequences)
#   - Edit / Levenshtein distance (dynamic programming)
#   - Distance matrix computation for the Friends dataset
#
# Base R only -- no external packages required.
# Run with: source("distance_measures.R")  or  Rscript distance_measures.R
# =============================================================================


# =============================================================================
# SECTION 1: SINGLE-ATTRIBUTE DISTANCE FUNCTIONS
# =============================================================================

#' Quantitative (continuous) single-attribute distance.
#' Formula: d(a, b) = |a - b|
diff_quantitative <- function(a, b) {
  return(abs(a - b))
}

#' Ordinal single-attribute distance.
#' Normalises rank positions to [0, 1].
#' Formula: d(a, b) = |pos_a - pos_b| / (n_values - 1)
#'
#' @param a      Rank position of first value (0-indexed).
#' @param b      Rank position of second value (0-indexed).
#' @param n_values  Total number of distinct ordinal levels.
diff_ordinal <- function(a, b, n_values) {
  return(abs(a - b) / (n_values - 1))
}

#' Nominal (categorical) single-attribute distance.
#' Formula: d(a, b) = 0 if a == b, else 1
diff_nominal <- function(a, b) {
  if (a == b) return(0)
  return(1)
}


# =============================================================================
# SECTION 2: MINKOWSKI DISTANCE FUNCTIONS
# =============================================================================

#' General Minkowski distance of order r.
#' Formula: d(x, y) = ( sum |x_k - y_k|^r )^(1/r)
#'   r = 1  ->  Manhattan (city-block)
#'   r = 2  ->  Euclidean
#'   r -> inf  ->  Chebyshev (max absolute difference)
#'
#' @param x  Numeric vector (first point).
#' @param y  Numeric vector (second point, same length as x).
#' @param r  Order of the norm (default 2).
minkowski_distance <- function(x, y, r = 2) {
  total <- 0
  for (i in seq_along(x)) {
    total <- total + abs(x[i] - y[i])^r
  }
  return(total^(1 / r))
}

#' Manhattan distance (Minkowski r=1).
#' Formula: sum |x_k - y_k|
manhattan_distance <- function(x, y) {
  total <- 0
  for (i in seq_along(x)) {
    total <- total + abs(x[i] - y[i])
  }
  return(total)
}

#' Euclidean distance (Minkowski r=2).
#' Formula: sqrt( sum (x_k - y_k)^2 )
euclidean_distance <- function(x, y) {
  total <- 0
  for (i in seq_along(x)) {
    total <- total + (x[i] - y[i])^2
  }
  return(sqrt(total))
}


# =============================================================================
# SECTION 3: HAMMING DISTANCE FUNCTIONS
# =============================================================================

#' Hamming distance between two equal-length strings.
#' Counts character positions where the strings differ.
#'
#' @param s1  First string.
#' @param s2  Second string (must be same length).
#' @return    Number of differing positions (integer).
hamming_distance_string <- function(s1, s2) {
  chars1 <- strsplit(s1, "")[[1]]
  chars2 <- strsplit(s2, "")[[1]]
  if (length(chars1) != length(chars2)) {
    stop(paste("Hamming distance requires equal-length strings.",
               "Got lengths", length(chars1), "and", length(chars2)))
  }
  count <- 0
  for (i in seq_along(chars1)) {
    if (chars1[i] != chars2[i]) {
      count <- count + 1
    }
  }
  return(count)
}

#' Hamming distance between two equal-length binary strings.
#' Identical logic to hamming_distance_string; kept separate for clarity.
#'
#' @param b1  First binary string (e.g. "1011101").
#' @param b2  Second binary string.
hamming_distance_binary <- function(b1, b2) {
  bits1 <- strsplit(b1, "")[[1]]
  bits2 <- strsplit(b2, "")[[1]]
  if (length(bits1) != length(bits2)) {
    stop(paste("Hamming distance requires equal-length strings.",
               "Got lengths", length(bits1), "and", length(bits2)))
  }
  count <- 0
  for (i in seq_along(bits1)) {
    if (bits1[i] != bits2[i]) {
      count <- count + 1
    }
  }
  return(count)
}


# =============================================================================
# SECTION 4: EDIT / LEVENSHTEIN DISTANCE (DYNAMIC PROGRAMMING)
# =============================================================================

#' Levenshtein (edit) distance between two strings.
#' Minimum number of single-character insertions, deletions, or substitutions
#' needed to transform s1 into s2.
#'
#' Uses a full (n+1) x (m+1) dynamic-programming matrix.
#'
#' @param s1  Source string.
#' @param s2  Target string.
#' @return    Integer edit distance.
edit_distance <- function(s1, s2) {
  chars1 <- strsplit(s1, "")[[1]]
  chars2 <- strsplit(s2, "")[[1]]
  n <- length(chars1)
  m <- length(chars2)

  # Initialise (n+1) x (m+1) matrix with zeros
  dp <- matrix(0, nrow = n + 1, ncol = m + 1)

  # Base cases: converting to/from empty string
  for (i in 0:n) dp[i + 1, 1] <- i   # delete i chars from s1
  for (j in 0:m) dp[1, j + 1] <- j   # insert j chars into s1

  # Fill the DP table
  for (i in 1:n) {
    for (j in 1:m) {
      if (chars1[i] == chars2[j]) {
        # Characters match: no extra cost
        dp[i + 1, j + 1] <- dp[i, j]
      } else {
        delete_cost <- dp[i,     j + 1] + 1  # delete from s1
        insert_cost <- dp[i + 1, j    ] + 1  # insert into s1
        subst_cost  <- dp[i,     j    ] + 1  # substitute
        dp[i + 1, j + 1] <- min(delete_cost, insert_cost, subst_cost)
      }
    }
  }

  return(dp[n + 1, m + 1])
}


# =============================================================================
# SECTION 5: DISTANCE MATRIX
# =============================================================================

#' Compute the full pairwise distance matrix for a list of points.
#'
#' @param points    List of numeric vectors (each vector = one point).
#' @param dist_func Function(x, y) returning a numeric distance.
#' @return          n x n numeric matrix of pairwise distances.
compute_distance_matrix <- function(points, dist_func) {
  n <- length(points)
  mat <- matrix(0, nrow = n, ncol = n)
  for (i in 1:n) {
    for (j in 1:n) {
      mat[i, j] <- dist_func(points[[i]], points[[j]])
    }
  }
  return(mat)
}

#' Print a formatted distance matrix with row/column labels.
#'
#' @param mat    Numeric matrix (n x n).
#' @param names  Character vector of labels (length n).
print_distance_matrix <- function(mat, names) {
  col_w <- 9
  n <- nrow(mat)

  # Header line
  header <- formatC("", width = 11)
  for (nm in names) {
    header <- paste0(header, formatC(substr(nm, 1, col_w), width = col_w, flag = " "))
  }
  cat(header, "\n")

  # Data rows
  for (i in 1:n) {
    row_str <- formatC(names[i], width = 11)
    for (j in 1:n) {
      row_str <- paste0(row_str, formatC(sprintf("%.2f", mat[i, j]), width = col_w, flag = " "))
    }
    cat(row_str, "\n")
  }
}


# =============================================================================
# SECTION 6: HELPER PRINT FUNCTIONS
# =============================================================================

print_section <- function(title) {
  cat("\n")
  cat(strrep("=", 60), "\n")
  cat("  ", title, "\n")
  cat(strrep("=", 60), "\n")
}

print_subsection <- function(title) {
  cat("\n  ---", title, "---\n")
}


# =============================================================================
# SECTION 7: MAIN DEMONSTRATION
# =============================================================================

main <- function() {

  # --------------------------------------------------------------------------
  # DEMO 1: Single-attribute distances
  # --------------------------------------------------------------------------
  print_section("DEMO 1: Single-Attribute Distances (Friends Dataset)")
  cat("\n")
  cat("Comparing Andrew (Age=55, Education_ordinal=4) vs",
      "Carolina (Age=37, Education_ordinal=5)\n\n")

  # Quantitative: Age
  age_andrew   <- 55
  age_carolina <- 37
  age_diff <- diff_quantitative(age_andrew, age_carolina)
  cat("  Quantitative distance (Age):\n")
  cat(sprintf("    d(%d, %d) = |%d - %d| = %g\n",
              age_andrew, age_carolina, age_andrew, age_carolina, age_diff))

  # Ordinal: Education_ordinal
  # Scale: {1=none, 2=primary, 3=some_college, 4=college, 5=grad_school}
  # Andrew  = 4 (college)    -> position 3 (0-indexed in 1..5)
  # Carolina= 5 (grad_school)-> position 4
  # n_values = 5
  edu_andrew_pos   <- 3   # position of level 4 in {1,2,3,4,5}
  edu_carolina_pos <- 4   # position of level 5 in {1,2,3,4,5}
  n_edu <- 5
  edu_diff <- diff_ordinal(edu_andrew_pos, edu_carolina_pos, n_edu)
  cat("\n  Ordinal distance (Education_ordinal, scale 1-5, n=5):\n")
  cat(sprintf("    Andrew pos=%d, Carolina pos=%d\n",
              edu_andrew_pos, edu_carolina_pos))
  cat(sprintf("    d(%d, %d) = |%d - %d| / (5-1) = %.4f\n",
              edu_andrew_pos, edu_carolina_pos,
              edu_andrew_pos, edu_carolina_pos, edu_diff))

  # Nominal: Name (just to show the concept)
  name_diff      <- diff_nominal("Andrew",   "Carolina")
  same_name_diff <- diff_nominal("Andrew",   "Andrew")
  cat("\n  Nominal distance (Name):\n")
  cat(sprintf("    d('Andrew', 'Carolina') = %d  (different)\n", name_diff))
  cat(sprintf("    d('Andrew', 'Andrew')   = %d  (same)\n", same_name_diff))

  # --------------------------------------------------------------------------
  # DEMO 2: Minkowski distances
  # --------------------------------------------------------------------------
  print_section("DEMO 2: Minkowski Distance (Andrew vs Carolina)")
  cat("\n")
  cat("Andrew   = (Age=55, Edu_ord=4)\n")
  cat("Carolina = (Age=37, Edu_ord=5)\n\n")

  andrew   <- c(55, 4)
  carolina <- c(37, 5)

  d_r1  <- manhattan_distance(andrew, carolina)
  d_r2  <- euclidean_distance(andrew, carolina)
  d_r3  <- minkowski_distance(andrew, carolina, r = 3)
  d_r10 <- minkowski_distance(andrew, carolina, r = 10)

  cat(sprintf("  r=1  (Manhattan):  |55-37| + |4-5| = 18 + 1 = %.4f\n",  d_r1))
  cat(sprintf("  r=2  (Euclidean):  sqrt(18^2 + 1^2) = sqrt(325) = %.4f\n", d_r2))
  cat(sprintf("  r=3  (Minkowski):  (18^3 + 1^3)^(1/3) = %.4f\n",        d_r3))
  cat(sprintf("  r=10 (approx Chebyshev): %.4f  (approaches max(18,1)=18)\n", d_r10))
  cat("\n  Note: As r increases the distance approaches the maximum\n")
  cat("  absolute difference in any single dimension (Chebyshev).\n")

  # --------------------------------------------------------------------------
  # DEMO 3: Hamming distance
  # --------------------------------------------------------------------------
  print_section("DEMO 3: Hamming Distance")
  cat("\n")

  # String example from lecture
  s1 <- "James"
  s2 <- "Jimmy"
  d_h <- hamming_distance_string(s1, s2)
  cat("  String Hamming distance:\n")
  cat(sprintf("    s1 = '%s'\n", s1))
  cat(sprintf("    s2 = '%s'\n", s2))
  cat("    Comparing character by character:\n")
  chars1 <- strsplit(s1, "")[[1]]
  chars2 <- strsplit(s2, "")[[1]]
  for (i in seq_along(chars1)) {
    label <- if (chars1[i] == chars2[i]) "same" else "DIFF"
    cat(sprintf("      pos %d: '%s' vs '%s' -> %s\n", i - 1, chars1[i], chars2[i], label))
  }
  cat(sprintf("    d('%s', '%s') = %d\n", s1, s2, d_h))

  s3 <- "Tom"
  s4 <- "Tim"
  d_h2 <- hamming_distance_string(s3, s4)
  cat(sprintf("\n  Another example: d('%s', '%s') = %d\n", s3, s4, d_h2))

  # Binary Hamming from lecture
  b1 <- "1011101"
  b2 <- "1001001"
  d_bin <- hamming_distance_binary(b1, b2)
  cat("\n  Binary Hamming distance:\n")
  cat(sprintf("    b1 = '%s'\n", b1))
  cat(sprintf("    b2 = '%s'\n", b2))
  cat("    Bit comparison:\n")
  bits1 <- strsplit(b1, "")[[1]]
  bits2 <- strsplit(b2, "")[[1]]
  for (i in seq_along(bits1)) {
    label <- if (bits1[i] == bits2[i]) "same" else "DIFF"
    cat(sprintf("      pos %d: %s vs %s -> %s\n", i - 1, bits1[i], bits2[i], label))
  }
  cat(sprintf("    d('%s', '%s') = %d\n", b1, b2, d_bin))

  # --------------------------------------------------------------------------
  # DEMO 4: Edit (Levenshtein) distance
  # --------------------------------------------------------------------------
  print_section("DEMO 4: Edit (Levenshtein) Distance")
  cat("\n")

  pairs <- list(
    c("Johnny",  "Jonston"),
    c("kitten",  "sitting"),
    c("data",    "date"),
    c("",        "abc")
  )

  for (pair in pairs) {
    d_edit <- edit_distance(pair[1], pair[2])
    cat(sprintf("  d('%s', '%s') = %d\n", pair[1], pair[2], d_edit))
  }

  cat("\n  Lecture example verified: d('Johnny','Jonston') =",
      edit_distance("Johnny", "Jonston"), "\n")
  cat("  (Expected: 5)\n")

  # --------------------------------------------------------------------------
  # DEMO 5: Distance matrix for the Friends subset
  #
  # Friends subset data:
  #   Andrew:   Age=55, Education_ordinal=4 (college)
  #   Bernhard: Age=43, Education_ordinal=3 (some college)
  #   Carolina: Age=37, Education_ordinal=5 (grad school)
  #   Dennis:   Age=82, Education_ordinal=3 (some college)
  #   Eve:      Age=23, Education_ordinal=4 (college)
  #   Fred:     Age=46, Education_ordinal=5 (grad school)
  # --------------------------------------------------------------------------
  print_section("DEMO 5: Distance Matrix for Friends Dataset (Euclidean)")
  cat("\n  Using Age and Education_ordinal as the two dimensions.\n\n")

  friends_names <- c("Andrew", "Bernhard", "Carolina", "Dennis", "Eve", "Fred")
  friends_data <- list(
    c(55, 4),   # Andrew
    c(43, 3),   # Bernhard
    c(37, 5),   # Carolina
    c(82, 3),   # Dennis
    c(23, 4),   # Eve
    c(46, 5)    # Fred
  )

  dist_matrix <- compute_distance_matrix(friends_data, euclidean_distance)

  print_distance_matrix(dist_matrix, friends_names)

  # Verification: distances from Andrew
  cat("\n  Distances from Andrew to each person:\n\n")
  andrew_idx <- 1
  for (i in seq_along(friends_names)) {
    cat(sprintf("    Andrew -> %-10s : %.2f\n",
                friends_names[i], dist_matrix[andrew_idx, i]))
  }

  # Verification: distances from Carolina
  cat("\n  Distances from Carolina to each person:\n\n")
  carolina_idx <- 3
  for (i in seq_along(friends_names)) {
    cat(sprintf("    Carolina -> %-10s : %.2f\n",
                friends_names[i], dist_matrix[carolina_idx, i]))
  }

  # --------------------------------------------------------------------------
  # DEMO 6: Manhattan distance matrix (same Friends dataset)
  # --------------------------------------------------------------------------
  print_section("DEMO 6: Distance Matrix for Friends Dataset (Manhattan)")
  cat("\n  Using Age and Education_ordinal as the two dimensions.\n\n")

  dist_matrix_man <- compute_distance_matrix(friends_data, manhattan_distance)
  print_distance_matrix(dist_matrix_man, friends_names)

  cat("\n")
  cat(strrep("=", 60), "\n")
  cat("  All distance measure demonstrations complete.\n")
  cat(strrep("=", 60), "\n")
}

# Run the demonstration
main()
