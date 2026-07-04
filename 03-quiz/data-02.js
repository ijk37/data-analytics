// ── Chapter 02 — Descriptive Statistics ─────────────────────────────────────
QUESTIONS["02"] = [
  {
    q: "What's the difference between induction and deduction in statistics?",
    options: [
      "Induction goes population → sample; deduction goes sample → population",
      "Induction goes sample → population (inference); deduction goes population → sample",
      "They are the same thing",
      "Induction only applies to categorical data",
    ],
    answer: 1,
    explain: "Induction (inference) generalizes from a sample to the wider population — the larger the sample, the closer the estimate. Deduction reasons about a sample drawn from an already-known population.",
  },
  {
    q: "Which location statistic is valid for nominal data but NOT the mean or median?",
    options: ["Mode", "Standard deviation", "Variance", "Quartile"],
    answer: 0,
    explain: "Mode just counts the most frequent category, which works for nominal data. Median needs order (ordinal+); mean, variance, and std dev need meaningful arithmetic (interval/ratio only).",
  },
  {
    q: "For the sorted dataset {0,1,2,2,3,3,5,6,10,11,12,14,15,16} (n=14), what is the median?",
    options: ["5", "5.5", "6", "3"],
    answer: 1,
    explain: "n=14 is even, so median = average of the 7th and 8th values. Sorted, those are 5 and 6, so median = (5+6)/2 = 5.5.",
  },
  {
    q: "Why is Bessel's correction (dividing by n−1 instead of n) used for sample variance?",
    options: [
      "It makes the formula simpler",
      "It gives an unbiased estimate of the population variance from a sample",
      "It only matters for very large datasets",
      "It converts variance into standard deviation",
    ],
    answer: 1,
    explain: "Using n-1 (rather than n) in the sample variance/std-dev formula corrects for the fact that a sample's own mean slightly underestimates spread around the true population mean.",
  },
  {
    q: "Which statistic is more ROBUST to outliers: the mean or the median?",
    options: ["Mean", "Median", "Both equally", "Neither — mode is most robust"],
    answer: 1,
    explain: "One extreme value can drag the mean far from the 'typical' value, but the median (a middle-ranked value) barely moves — the classic reason to prefer median for skewed data.",
  },
  {
    q: "If a distribution's mean is greater than its median, what kind of skew does it have?",
    options: ["Symmetric", "Negative (left) skew", "Positive (right) skew", "No skew — this is impossible"],
    answer: 2,
    explain: "A long right tail of high values pulls the mean above the median — that's positive (right) skew. (mean < median indicates negative/left skew.)",
  },
  {
    q: "What does the Interquartile Range (IQR) measure, and how is it computed?",
    options: [
      "The full range (max - min); very sensitive to outliers",
      "Q3 - Q1; the spread of the middle 50% of data, robust to outliers",
      "The average distance from the mean",
      "The variance divided by the mean",
    ],
    answer: 1,
    explain: "IQR = Q3 - Q1 captures the middle 50% of the data and ignores extreme tails, making it a robust dispersion measure — unlike the full range (max-min), which one outlier can blow up.",
  },
  {
    q: "About what percentage of values fall within μ ± 2σ in a Normal distribution?",
    options: ["68%", "95%", "99.7%", "50%"],
    answer: 1,
    explain: "The empirical rule for a Normal (Gaussian) distribution: ~68% within 1 std dev, ~95% within 2, ~99.7% within 3.",
  },
  {
    q: "Covariance between two attributes X and Y is negative. What does that indicate?",
    options: [
      "X and Y increase together",
      "As X increases, Y tends to decrease",
      "X and Y are perfectly uncorrelated",
      "X and Y must be on the same scale",
    ],
    answer: 1,
    explain: "A negative covariance means the two attributes tend to move in opposite directions — one goes up as the other goes down.",
  },
  {
    q: "Why is Pearson's r generally preferred over raw covariance when comparing relationships across different attribute pairs?",
    options: [
      "r is always positive",
      "r is scale-independent (bounded in [-1, 1]), while covariance depends on the attributes' units",
      "r doesn't require paired data",
      "Covariance can only be computed in R, not Python",
    ],
    answer: 1,
    explain: "Covariance's magnitude depends on the units of X and Y, so you can't compare a cov(height,weight) to a cov(income,age) directly. Dividing by the standard deviations (Pearson's r) removes the units, always landing in [-1, 1].",
  },
  {
    q: "When should you prefer Spearman's rank correlation over Pearson's r?",
    options: [
      "When the data is quantitative with no outliers",
      "When the data is ordinal, non-linear (but monotonic), or has outliers",
      "Spearman should always replace Pearson",
      "When you only have one attribute",
    ],
    answer: 1,
    explain: "Spearman applies Pearson's formula to ranks instead of raw values, which handles ordinal data and non-linear monotonic relationships, and is less sensitive to outliers (an outlier just becomes an extreme rank, not an extreme value).",
  },
  {
    q: "What visualization best reveals whether a quantitative attribute's distribution differs across categories of a qualitative attribute?",
    options: ["A single histogram", "A contingency table", "Grouped box plots (one box per category)", "A scatter plot"],
    answer: 2,
    explain: "Grouped box plots put one box-and-whisker per category on a shared axis, letting you directly compare the quantitative distribution (median, spread, outliers) across groups.",
  },
  {
    q: "For two qualitative attributes, what table shows the joint frequency of every combination of their values?",
    options: ["Frequency table", "Contingency table", "Covariance matrix", "Correlation matrix"],
    answer: 1,
    explain: "A contingency table cross-tabulates two categorical attributes: rows are one attribute's values, columns are the other's, and each cell is the joint count — with row/column/grand totals.",
  },
  {
    q: "What is the rule-of-thumb number of bins for a histogram of n data points?",
    options: ["n bins", "log2(n) bins", "√n bins", "Always exactly 10 bins"],
    answer: 2,
    explain: "A common heuristic is roughly √n bins, though the ideal choice is always problem-dependent — too few bins hides structure, too many bins looks noisy.",
  },
  {
    q: "What does a relative CUMULATIVE frequency column represent?",
    options: [
      "The empirical probability density function (PDF)",
      "The empirical cumulative distribution function (CDF) — the fraction of values ≤ v",
      "The mode of the dataset",
      "The variance of the dataset",
    ],
    answer: 1,
    explain: "Relative frequency alone gives the empirical PMF/PDF; running that total up to each value gives the empirical CDF — the proportion of the data at or below that value.",
  },
];
