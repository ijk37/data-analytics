// ── Chapter 08 — Course Summary (Mixed Review, all chapters) ────────────────
QUESTIONS["08"] = [
  {
    q: "(Ch1) Which measurement scale allows meaningful ratios (e.g., '20kg is twice 10kg')?",
    options: ["Nominal", "Ordinal", "Interval", "Ratio"],
    answer: 3,
    explain: "Only the ratio scale has a true zero, which is what makes multiplicative comparisons like 'twice as much' meaningful. Interval scales (like Celsius) support differences but not ratios.",
  },
  {
    q: "(Ch1) You can always convert a ratio-scale attribute DOWN to ordinal, but never the reverse. Why?",
    options: [
      "It's an arbitrary convention with no real reason",
      "Going down (ratio→ordinal) discards information; going up (ordinal→ratio) would require inventing information that was never measured",
      "Ordinal scales always have more data than ratio scales",
      "There is no such rule",
    ],
    answer: 1,
    explain: "A ratio value like age=37 can always be re-expressed as an ordinal bucket like 'young/middle/old', but an ordinal label like 'good/bad' can't be turned into a precise numeric ratio value that was never actually recorded.",
  },
  {
    q: "(Ch2) If mean < median < mode for a distribution, what kind of skew is present?",
    options: ["Positive (right) skew", "Negative (left) skew", "No skew (symmetric)", "This combination is impossible"],
    answer: 1,
    explain: "A long left tail pulls the mean below the median and mode — that ordering (mean < median < mode) is the signature of negative (left) skew.",
  },
  {
    q: "(Ch2) Which correlation measure should you use when the relationship between two attributes is monotonic but NOT linear?",
    options: ["Pearson's r", "Covariance", "Spearman's rank correlation", "Mode"],
    answer: 2,
    explain: "Spearman applies Pearson's formula to ranks rather than raw values, so it captures any monotonic relationship (not just straight-line ones) and is more robust to outliers.",
  },
  {
    q: "(Ch3) In a p×p covariance matrix, what always appears on the diagonal?",
    options: ["Zeros", "Ones", "The variance of each attribute", "Correlation coefficients"],
    answer: 2,
    explain: "S[i][i] = cov(Xi, Xi), which is exactly the sample variance of attribute i by definition.",
  },
  {
    q: "(Ch3) Which multivariate plot maps each object to a polyline crossing one axis per attribute?",
    options: ["Scatter plot matrix", "Parallel coordinates plot", "Mosaic plot", "Correlogram"],
    answer: 1,
    explain: "Parallel coordinates draws one vertical axis per attribute and connects each object's values into a polyline — good for spotting clusters, outliers, and correlated attributes across many dimensions at once.",
  },
  {
    q: "(Ch4) A dataset has a duplicate row (the exact same customer entered twice). What data quality issue is this, and what's the fix?",
    options: [
      "Missing values — fill with the mode",
      "Redundant data — deduplicate (remove the repeated row)",
      "Inconsistent data — treat as missing",
      "Noise — apply a k-NN smoothing filter",
    ],
    answer: 1,
    explain: "Two rows representing the same real-world entity are a duplicate/redundancy problem, fixed by deduplication — different from missing values, domain-violating inconsistent values, or random measurement noise.",
  },
  {
    q: "(Ch4) Between min-max normalization and z-score standardization, which is generally MORE robust to outliers?",
    options: ["Min-max normalization", "Z-score standardization", "Neither — both are equally sensitive", "Normalization is never affected by outliers"],
    answer: 1,
    explain: "One extreme value in min-max normalization compresses the entire scaled range (since it redefines the min or max); z-score standardization is comparatively less distorted, though not immune, since it uses mean/std rather than min/max.",
  },
  {
    q: "(Ch5) What's the main difference between K-means and DBSCAN in terms of required inputs?",
    options: [
      "K-means requires K in advance; DBSCAN instead requires Eps and MinPts, and discovers the number of clusters itself",
      "Both require exactly the same parameters",
      "DBSCAN requires K in advance; K-means does not",
      "Neither requires any parameters",
    ],
    answer: 0,
    explain: "K-means needs the number of clusters K specified upfront. DBSCAN instead takes a neighborhood radius (Eps) and a density threshold (MinPts), and the number of resulting clusters emerges from the data's density structure.",
  },
  {
    q: "(Ch5) Which hierarchical linkage method tends to produce clusters similar in spirit to K-means (compact, similar-sized)?",
    options: ["Single (MIN) linkage", "Ward's method", "Neither — hierarchical and K-means are unrelated", "Complete linkage always ties with single linkage"],
    answer: 1,
    explain: "Ward's method merges the pair of clusters that causes the smallest increase in total SSE, which tends to produce compact, similarly-sized clusters — much like K-means' own SSE-minimizing objective.",
  },
  {
    q: "(Ch6) Lift(X→Y) is computed as...",
    options: [
      "Support(X→Y) / Confidence(X→Y)",
      "Confidence(X→Y) / Support(Y)",
      "Support(X) × Support(Y)",
      "Confidence(X→Y) × Support(X)",
    ],
    answer: 1,
    explain: "Lift = confidence(X→Y) / support(Y) = P(Y|X)/P(Y). Lift > 1 means X and Y co-occur more than random chance; lift = 1 means independence.",
  },
  {
    q: "(Ch6) What relationship holds between maximal frequent itemsets, closed frequent itemsets, and all frequent itemsets?",
    options: [
      "Maximal ⊂ Closed ⊂ Frequent",
      "Frequent ⊂ Maximal ⊂ Closed",
      "They're always identical sets",
      "Closed ⊂ Maximal ⊂ Frequent",
    ],
    answer: 0,
    explain: "Maximal itemsets (no frequent superset) are the smallest, most-compressed representation; closed itemsets (no equal-support superset) are a slightly larger lossless representation; both are subsets of the full frequent-itemset collection.",
  },
  {
    q: "(Ch7) Which classifier explicitly assumes that all input features are conditionally independent given the class?",
    options: ["Decision tree", "k-NN", "Naive Bayes", "None of these"],
    answer: 2,
    explain: "Naive Bayes' defining ('naive') assumption is P(X|C) = product of P(xi|C) across all features — decision trees and k-NN make no such independence assumption.",
  },
  {
    q: "(Ch7) A model has high precision but low recall. What does that tell you?",
    options: [
      "When it predicts positive, it's usually right, but it MISSES many actual positive cases",
      "It catches every actual positive case, but many of its positive predictions are wrong",
      "The model is perfect",
      "Precision and recall can never differ",
    ],
    answer: 0,
    explain: "High precision (TP/(TP+FP)) means few false positives among its positive predictions. Low recall (TP/(TP+FN)) means it's leaving many real positives undetected (high false negatives) — a conservative, 'only predict positive when very sure' model.",
  },
  {
    q: "(Capstone) You need to segment customers into unlabeled groups AND later predict whether a new customer will churn. Which two techniques from this course would you combine?",
    options: [
      "Clustering (Ch5) for segmentation, then Classification (Ch7) for the churn prediction",
      "Frequent pattern mining (Ch6) alone covers both tasks",
      "Only Descriptive Statistics (Ch2) is needed for both",
      "Data Quality (Ch4) alone solves both tasks",
    ],
    answer: 0,
    explain: "Clustering (unsupervised) naturally fits 'find groups with no labels' (segmentation); classification (supervised) fits 'predict a known target label' (churn yes/no) — this is exactly the pattern used in the Market Basket & Customer Segmentation and Retail Sales Analytics capstone projects.",
  },
  {
    q: "(Capstone) Before running k-means, k-NN, or computing Euclidean distances on a raw dataset with mixed scales (age in years, income in dollars), what preprocessing step (Ch4) is essential?",
    options: [
      "Nothing — raw scales work fine for distance-based methods",
      "Normalize/standardize the numeric attributes (min-max or z-score) so no single attribute dominates the distance",
      "Convert every attribute to nominal categories",
      "Remove all numeric attributes",
    ],
    answer: 1,
    explain: "Any distance-based method (k-means, k-NN, hierarchical clustering) is scale-sensitive — without normalization, a large-range attribute like income would completely dominate the distance calculation over a small-range attribute like age.",
  },
];
