# ==============================================================================
# Chapter 01
# 01-03-project-03: Attribute Scale Exercises  (R version)
# ==============================================================================
# Demonstrates the five Ch.1 Exercise Q1 examples using R's type system.
#
# Key idea: R's built-in types map directly onto Stevens' measurement scales:
#
#   Nominal   -> factor (unordered)              factor(c("A","B","A"))
#   Ordinal   -> factor with ordered=TRUE         factor(..., ordered=TRUE)
#   Interval  -> numeric (no true zero context)   numeric / double
#   Ratio     -> numeric (true zero present)      numeric / double
#
# The difference between Interval and Ratio is conceptual in R -- both use
# numeric/double storage.  The analyst must decide which operations are valid.
#
# Usage:
#   Rscript scale_exercises.R
#   source("scale_exercises.R")   # from within R / RStudio
# ==============================================================================


# ==============================================================================
# Helper: print a section separator
# ==============================================================================

separator <- function(char = "-", width = 70) {
  cat(paste(rep(char, width), collapse = ""), "\n")
}


# ==============================================================================
# Stevens' scale reference table
# ==============================================================================

cat("\n")
separator("=")
cat("  STEVENS' MEASUREMENT SCALES -- QUICK REFERENCE\n")
separator("=")
cat(sprintf("  %-10s  %-7s  %-13s  %-12s\n",
            "Scale", "Order?", "Equal gaps?", "True zero?"))
separator("-")
scale_table <- data.frame(
  Scale     = c("Nominal", "Ordinal", "Interval", "Ratio"),
  Order     = c("No",      "Yes",     "Yes",       "Yes"),
  EqualGaps = c("No",      "No",      "Yes",       "Yes"),
  TrueZero  = c("No",      "No",      "No",        "Yes")
)
for (i in seq_len(nrow(scale_table))) {
  cat(sprintf("  %-10s  %-7s  %-13s  %-12s\n",
              scale_table$Scale[i],
              scale_table$Order[i],
              scale_table$EqualGaps[i],
              scale_table$TrueZero[i]))
}
separator("=")
cat("\n")


# ==============================================================================
# EXAMPLE (a): University students' letter grades  ->  ORDINAL
# ==============================================================================

separator("=")
cat("  Q1(a)  University students' letter grades  -->  ORDINAL\n")
separator("-")

# Create as an ORDERED factor: A > B > C > D > F
grades <- factor(
  c("B", "A", "C", "A", "D", "B", "F", "C", "A", "B"),
  levels  = c("F", "D", "C", "B", "A"),   # lowest to highest
  ordered = TRUE
)

cat("  Data:       "); cat(as.character(grades), sep = "  "); cat("\n")
cat(sprintf("  R type:     %s\n", class(grades)))
cat(sprintf("  Ordered?    %s\n", is.ordered(grades)))
cat(sprintf("  Levels:     %s\n", paste(levels(grades), collapse = " < ")))
cat("\n")
cat("  Valid operation -- sorting (ordering makes sense):\n")
cat("  sorted:", paste(sort(grades), collapse = "  "), "\n")
cat("\n")
cat("  Valid operation -- table / mode:\n")
print(table(grades))
cat("\n")
cat("  INVALID for ordinal -- DO NOT compute mean():\n")
# Suppress the error for demonstration; just show the intention
cat("    mean(as.numeric(grades)) =", mean(as.numeric(grades)),
    "  <- misleading: assumes equal gaps\n")
cat("\n")
cat("  Reasoning: clear order A>B>C>D>F, but gap sizes are NOT measurable.\n")
separator("=")
cat("\n")


# ==============================================================================
# EXAMPLE (b): Level of urgency in an emergency room  ->  ORDINAL
# ==============================================================================

separator("=")
cat("  Q1(b)  Level of urgency in an emergency room  -->  ORDINAL\n")
separator("-")

# ER triage categories (standard 4-level scale used in many hospitals)
urgency <- factor(
  c("moderate", "critical", "low", "urgent", "moderate", "critical",
    "low", "urgent", "moderate", "low"),
  levels  = c("low", "moderate", "urgent", "critical"),
  ordered = TRUE
)

cat("  Data:       "); cat(as.character(urgency), sep = "  "); cat("\n")
cat(sprintf("  R type:     %s\n", class(urgency)))
cat(sprintf("  Levels:     %s\n", paste(levels(urgency), collapse = " < ")))
cat("\n")
cat("  Valid -- comparison: is patient 1 more urgent than patient 3?\n")
cat(sprintf("    urgency[1] > urgency[3]  ->  %s\n",
            urgency[1] > urgency[3]))
cat("\n")
cat("  Valid -- table:\n")
print(table(urgency))
cat("\n")
cat("  Reasoning: ordered categories, but gaps between levels are NOT equal.\n")
separator("=")
cat("\n")


# ==============================================================================
# EXAMPLE (c): Classification of animals in a zoo  ->  NOMINAL
# ==============================================================================

separator("=")
cat("  Q1(c)  Classification of animals in a zoo  -->  NOMINAL\n")
separator("-")

# Unordered factor -- no natural ranking among animal classes
animals <- factor(
  c("mammal", "reptile", "bird", "mammal", "insect",
    "bird", "fish", "mammal", "amphibian", "reptile"),
  ordered = FALSE   # explicitly unordered
)

cat("  Data:       "); cat(as.character(animals), sep = "  "); cat("\n")
cat(sprintf("  R type:     %s\n", class(animals)))
cat(sprintf("  Ordered?    %s\n", is.ordered(animals)))
cat(sprintf("  Levels:     %s\n", paste(levels(animals), collapse = ", ")))
cat("\n")
cat("  Valid -- frequency count (mode is the only valid center measure):\n")
print(table(animals))
cat("\n")
cat("  INVALID for nominal -- DO NOT compare or sort:\n")
cat("    There is no sense in which 'bird' > 'fish'.\n")
cat("\n")
cat("  Reasoning: pure categories, no natural order, no arithmetic.\n")
separator("=")
cat("\n")


# ==============================================================================
# EXAMPLE (d): Carbon dioxide levels in the atmosphere  ->  RATIO
# ==============================================================================

separator("=")
cat("  Q1(d)  Carbon dioxide levels in the atmosphere  -->  RATIO\n")
separator("-")

# CO2 concentration in parts per million (ppm) -- numeric, true zero present
co2_ppm <- c(415.2, 420.0, 411.8, 418.5, 422.1,
             414.7, 416.9, 419.3, 413.0, 417.6)

cat("  Data (ppm): "); cat(co2_ppm, sep = "  "); cat("\n")
cat(sprintf("  R type:     %s\n", class(co2_ppm)))
cat("\n")
cat("  Valid -- all arithmetic and summary statistics:\n")
cat(sprintf("    mean    = %.2f ppm\n", mean(co2_ppm)))
cat(sprintf("    sd      = %.4f ppm\n", sd(co2_ppm)))
cat(sprintf("    min     = %.1f ppm\n", min(co2_ppm)))
cat(sprintf("    max     = %.1f ppm\n", max(co2_ppm)))
cat("\n")
cat("  Valid -- ratios are meaningful:\n")
cat(sprintf("    %.1f ppm is %.2f x more CO2 than %.1f ppm\n",
            max(co2_ppm), max(co2_ppm) / min(co2_ppm), min(co2_ppm)))
cat("\n")
cat("  Reasoning: 0 ppm = no CO2 present (true zero). Ratios are meaningful.\n")
separator("=")
cat("\n")


# ==============================================================================
# EXAMPLE (e): Distance from center of campus  ->  RATIO
# ==============================================================================

separator("=")
cat("  Q1(e)  Distance from center of campus  -->  RATIO\n")
separator("-")

# Distances in meters from the central point of a campus
distance_m <- c(120.0, 350.5, 0.0, 85.3, 210.0,
                450.2, 175.8, 30.0, 290.0, 62.5)

cat("  Data (m):   "); cat(distance_m, sep = "  "); cat("\n")
cat(sprintf("  R type:     %s\n", class(distance_m)))
cat("\n")
cat("  Valid -- all arithmetic and summary statistics:\n")
cat(sprintf("    mean    = %.2f m\n", mean(distance_m)))
cat(sprintf("    median  = %.2f m\n", median(distance_m)))
cat(sprintf("    sd      = %.4f m\n", sd(distance_m)))
cat(sprintf("    range   = %.1f m to %.1f m\n", min(distance_m), max(distance_m)))
cat("\n")
cat("  Valid -- ratios are meaningful:\n")
cat(sprintf("    %.1f m is %.2f x further than %.1f m\n",
            max(distance_m), max(distance_m) / distance_m[4], distance_m[4]))
cat("\n")
cat("  True zero: 0 m = at the exact center of campus (not arbitrary).\n")
cat("  Reasoning: positive numeric measurement, true zero, ratios valid.\n")
separator("=")
cat("\n")


# ==============================================================================
# FINAL SUMMARY TABLE
# ==============================================================================

separator("=")
cat("  SUMMARY: Ch.1 Exercise Q1 Answers\n")
separator("-")
cat(sprintf("  %-43s  %-10s\n", "Attribute", "Scale"))
separator("-")

summary_rows <- list(
  c("a. University students' letter grades",    "Ordinal"),
  c("b. Level of urgency in emergency room",    "Ordinal"),
  c("c. Classification of animals in a zoo",    "Nominal"),
  c("d. Carbon dioxide levels in atmosphere",   "Ratio"),
  c("e. Distance from center of campus",        "Ratio")
)

for (row in summary_rows) {
  cat(sprintf("  %-43s  %-10s\n", row[1], row[2]))
}
separator("=")
cat("\n")
