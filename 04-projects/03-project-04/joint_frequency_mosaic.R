# ============================================================
# joint_frequency_mosaic.R
# Chapter 3 — Multivariate Frequency Tables & Mosaic Plots
# Demo dataset: Friends (Gender, Company, Food_pref)
# ============================================================

# ── 1. Build the Friends data frame ─────────────────────────────────────────

friends <- data.frame(
  Friend = c("Andrew", "Bernhard", "Carolina", "Dennis", "Eve", "Fred",
             "Gwyneth", "Hayden", "Irene", "James", "Kevin", "Lea",
             "Marcus", "Nigel"),
  Gender = c("M", "M", "F", "M", "F", "M",
             "F", "F", "F", "M", "M", "F",
             "M", "M"),
  Company = c("Good", "Good", "Bad", "Good", "Bad", "Good",
              "Bad",  "Bad",  "Bad", "Good", "Bad", "Good",
              "Bad",  "Good"),
  Food_pref = c("Meat",       "Meat",       "Vegetarian", "Meat",       "Vegetarian",
                "Mixed",      "Mixed",      "Vegetarian", "Vegetarian", "Meat",
                "Meat",       "Mixed",      "Vegetarian", "Meat"),
  stringsAsFactors = FALSE
)

cat("\n── Friends dataset ──────────────────────────────────────────\n")
print(friends)
cat("n =", nrow(friends), "\n\n")


# ── 2. Joint frequency table: Gender x Company ──────────────────────────────
# table() counts co-occurrences of all combinations.
# Rows = first argument, columns = second argument.

cat("── SECTION 2: Joint Frequency Table  Gender x Company ──────\n")

freq_gc <- table(Gender = friends$Gender, Company = friends$Company)

cat("\nAbsolute joint frequencies:\n")
print(freq_gc)

# addmargins() appends row and column totals (marginal frequencies)
cat("\nWith marginal totals (addmargins):\n")
print(addmargins(freq_gc))


# ── 3. Joint relative frequencies ───────────────────────────────────────────
# prop.table() divides every cell by the grand total when no margin is given.

cat("\n── SECTION 3: Joint Relative Frequencies ────────────────────\n")

rel_gc <- prop.table(freq_gc)

cat("\nJoint relative frequencies (fractions, sum = 1):\n")
print(round(rel_gc, 4))

cat("\nJoint relative frequencies as percentages:\n")
print(round(rel_gc * 100, 1))

cat("\nWith marginal totals:\n")
print(round(addmargins(rel_gc), 4))


# ── 4. Marginal frequencies ──────────────────────────────────────────────────
# margin.table() collapses over one dimension to give row or column totals.

cat("\n── SECTION 4: Marginal Frequencies ──────────────────────────\n")

# Marginal frequency of Gender (sum across Company columns)
marg_gender <- margin.table(freq_gc, margin = 1)
cat("\nMarginal frequency of Gender:\n")
print(marg_gender)

# Marginal relative frequency of Gender
cat("\nMarginal relative frequency of Gender:\n")
print(round(prop.table(marg_gender), 4))

# Marginal frequency of Company (sum across Gender rows)
marg_company <- margin.table(freq_gc, margin = 2)
cat("\nMarginal frequency of Company:\n")
print(marg_company)

# Marginal relative frequency of Company
cat("\nMarginal relative frequency of Company:\n")
print(round(prop.table(marg_company), 4))


# ── 5. Conditional frequencies ───────────────────────────────────────────────
# prop.table(tbl, margin = 1) divides each cell by its ROW total.
# This gives P(Company | Gender): the probability distribution of Company
# within each level of Gender.

cat("\n── SECTION 5: Conditional Frequencies ──────────────────────\n")

# P(Company | Gender): each row sums to 1
cond_company_given_gender <- prop.table(freq_gc, margin = 1)
cat("\nP(Company | Gender) — fractions (each row sums to 1):\n")
print(round(cond_company_given_gender, 4))

cat("\nP(Company | Gender) — percentages:\n")
print(round(cond_company_given_gender * 100, 1))

# P(Gender | Company): each column sums to 1 (margin = 2)
cond_gender_given_company <- prop.table(freq_gc, margin = 2)
cat("\nP(Gender | Company) — fractions (each column sums to 1):\n")
print(round(cond_gender_given_company, 4))

cat("\nP(Gender | Company) — percentages:\n")
print(round(cond_gender_given_company * 100, 1))


# ── 6. Mosaic plot: Gender x Company ─────────────────────────────────────────
# mosaicplot() is built into base R.
# - Column width is proportional to the marginal frequency of Company.
# - Segment height within a column is proportional to
#   the conditional frequency of Gender given Company.
# - Passing the table directly uses the counts inside it.

cat("\n── SECTION 6: Mosaic Plot  Gender x Company ─────────────────\n")
cat("(A graphical window should open with the mosaic plot.)\n\n")

mosaicplot(
  freq_gc,
  main  = "Mosaic Plot: Gender x Company",
  xlab  = "Company",
  ylab  = "Gender",
  color = c("steelblue", "tomato"),   # one colour per row (Gender) level
  las   = 1                           # horizontal axis tick labels
)


# ── 7. Additional tables: Gender x Food_pref ────────────────────────────────

cat("── SECTION 7: Gender x Food_pref ────────────────────────────\n")

freq_gf <- table(Gender = friends$Gender, Food_pref = friends$Food_pref)

cat("\nAbsolute joint frequencies:\n")
print(addmargins(freq_gf))

cat("\nP(Food_pref | Gender) — percentages:\n")
print(round(prop.table(freq_gf, margin = 1) * 100, 1))

cat("\nMosaic plot: Gender x Food_pref\n")
mosaicplot(
  freq_gf,
  main  = "Mosaic Plot: Gender x Food_pref",
  xlab  = "Food Preference",
  ylab  = "Gender",
  color = c("steelblue", "tomato"),
  las   = 1
)


# ── 8. Three-way frequency table: Gender x Company x Food_pref ──────────────
# table() accepts any number of variables.
# The result is a 3-dimensional array.

cat("\n── SECTION 8: 3-Way Table  Gender x Company x Food_pref ─────\n")

freq_3way <- table(
  Gender    = friends$Gender,
  Company   = friends$Company,
  Food_pref = friends$Food_pref
)

cat("\n3-way absolute frequencies:\n")
print(freq_3way)

cat("\nFlattened view (ftable) — easier to read:\n")
print(ftable(freq_3way))

# Conditional on Gender and Company: P(Food_pref | Gender, Company)
cond_food_given_gc <- prop.table(freq_3way, margin = c(1, 2))
cat("\nP(Food_pref | Gender, Company) — fractions:\n")
print(round(ftable(cond_food_given_gc), 4))


# ── 9. Mosaic plot for the 3-way table ──────────────────────────────────────
# mosaicplot() handles n-dimensional tables natively.
# Each additional dimension adds another level of splitting.

cat("\n── SECTION 9: Mosaic Plot  Gender x Company x Food_pref ─────\n")
cat("(A graphical window should open with the 3-way mosaic plot.)\n\n")

mosaicplot(
  freq_3way,
  main  = "Mosaic Plot: Gender x Company x Food_pref",
  color = TRUE,   # auto-assign colours across categories
  las   = 1
)

cat("\nDone. All analyses completed.\n")
