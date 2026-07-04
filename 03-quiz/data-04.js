// ── Chapter 04 — Data Quality and Preprocessing ─────────────────────────────
QUESTIONS["04"] = [
  {
    q: "A dataset has a birth date implying someone is 200 years old. What data quality problem is this?",
    options: ["Missing value", "Duplicate record", "Inconsistent data", "Noise"],
    answer: 2,
    explain: "This value violates a known domain relationship (nobody is 200 years old), making it inconsistent data — the fix is typically to treat it as missing and apply a missing-value strategy.",
  },
  {
    q: "When the target class label IS known, what's generally the BEST way to fill a missing numeric value?",
    options: [
      "Always use the global mean",
      "Fill with the mean/median computed per class (per-class filling)",
      "Delete the entire dataset",
      "Fill with a random number",
    ],
    answer: 1,
    explain: "Per-class filling (e.g., filling missing height with the mean height of the same gender group) uses more relevant structure than a single global average, and is more accurate when class labels are available.",
  },
  {
    q: "What's the key difference between noise and an outlier?",
    options: [
      "There is no difference",
      "Noise is a measurement/labeling error; an outlier may be a genuine, legitimate unusual value",
      "Outliers are always errors; noise is always legitimate",
      "Noise only applies to categorical data",
    ],
    answer: 1,
    explain: "Noise (e.g., a sensor glitch) should typically be removed/smoothed. An outlier (e.g., a CEO's real $50M salary in a salary dataset) might be genuine and worth investigating rather than deleting.",
  },
  {
    q: "Using the IQR rule, a value is flagged as an outlier if it falls...",
    options: [
      "Anywhere outside the mean ± 1 standard deviation",
      "Below Q1 - 1.5×IQR or above Q3 + 1.5×IQR",
      "Below the minimum recorded value",
      "Exactly at the median",
    ],
    answer: 1,
    explain: "The IQR rule uses the box-plot whiskers: anything beyond 1.5 times the interquartile range past Q1 or Q3 is flagged as a potential outlier.",
  },
  {
    q: "Why is stratified sampling preferred over simple random sampling for an imbalanced dataset (e.g., 900 class A, 100 class B)?",
    options: [
      "It's always faster to compute",
      "It guarantees each class/stratum is represented proportionally, even rare ones",
      "It removes the need for a class label entirely",
      "It always increases dataset size",
    ],
    answer: 1,
    explain: "A simple random 10% sample of an imbalanced dataset could easily under- or over-represent the minority class by chance; stratified sampling deliberately samples proportionally from each stratum (e.g., exactly 90 A and 10 B).",
  },
  {
    q: "Discretizing [23,27,29,31,35,38,42,43,46,51,55,83] into 4 EQUAL-WIDTH bins, what is the bin width?",
    options: ["12", "15", "20", "60"],
    answer: 1,
    explain: "Width = (max - min) / N = (83 - 23) / 4 = 60/4 = 15. Note this leaves bin 4 nearly empty (just the outlier 83) — the classic weakness of equal-width binning with outliers.",
  },
  {
    q: "What is the main strength of equal-DEPTH (equal-frequency) binning over equal-width binning?",
    options: [
      "It always produces exactly 2 bins",
      "Each bin holds roughly the same COUNT of values, making it more robust to outliers",
      "It doesn't require sorting the data",
      "Bin boundaries are always nice round numbers",
    ],
    answer: 1,
    explain: "Equal-depth sorts the data and splits it so each bin has (roughly) the same number of values — an outlier just ends up in the extreme bin without stretching or emptying the others, unlike equal-width.",
  },
  {
    q: "For a nominal attribute like Food = {American, Chinese, Italian, Other}, which encoding is most appropriate before feeding it into a distance-based model?",
    options: [
      "Natural numbers (0, 1, 2, 3)",
      "One-hot encoding (one binary column per category)",
      "Z-score standardization",
      "Log transformation",
    ],
    answer: 1,
    explain: "One-hot encoding avoids implying a false order or distance between categories — natural-number encoding would wrongly suggest 'Italian' (2) is 'between' Chinese (1) and Other (3).",
  },
  {
    q: "What makes Gray code useful for encoding ordinal categories?",
    options: [
      "It uses the fewest bits possible always",
      "Consecutive codes differ by exactly 1 bit, reducing error at category transitions",
      "It ignores the category order entirely",
      "It's only usable for exactly 2 categories",
    ],
    answer: 1,
    explain: "Gray code is constructed so adjacent ordinal values differ by only a single bit flip — useful when minimizing bit-transition errors matters (e.g., noisy channels or hardware).",
  },
  {
    q: "How does thermometer (unary) code represent the n-th category out of k ordered categories?",
    options: [
      "As a single decimal digit n",
      "As n consecutive 1s from the left (n ones total)",
      "As a random binary string",
      "As the category name itself",
    ],
    answer: 1,
    explain: "Thermometer code fills in n ones for the n-th category (e.g., small=000, medium=001, large=011, very_large=111), preserving strict ordering with meaningful step-by-step distances.",
  },
  {
    q: "Min-max normalizing an income of $73,600 where min=$12,000 and max=$98,000 gives approximately...",
    options: ["0.500", "0.716", "0.284", "1.225"],
    answer: 1,
    explain: "v' = (73600-12000)/(98000-12000) = 61600/86000 ≈ 0.716.",
  },
  {
    q: "Compared to min-max normalization, z-score standardization is...",
    options: [
      "Bounded to [0,1] just like min-max",
      "More robust to outliers, and unbounded (typically -3 to +3 for normal data)",
      "Only usable on nominal data",
      "Identical to min-max in every way",
    ],
    answer: 1,
    explain: "Z-score centers data at mean 0 / std 1 without forcing it into a fixed range, so a single extreme value doesn't compress the rest of the data the way min-max normalization can.",
  },
  {
    q: "Why must attributes typically be normalized before computing Euclidean distance?",
    options: [
      "Normalization is never actually necessary",
      "Otherwise the attribute with the largest numeric range dominates the distance calculation",
      "Euclidean distance only works on normalized binary data",
      "It changes the number of dimensions",
    ],
    answer: 1,
    explain: "If one attribute ranges over thousands (e.g., income) and another over single digits (e.g., years of experience), the larger-range attribute swamps the squared differences — normalizing first puts every attribute on comparable footing.",
  },
  {
    q: "What is the Euclidean distance between x=(1,3,-2,5) and y=(2,4,1,6)?",
    options: ["√6 ≈ 2.449", "√12 ≈ 3.464", "6", "12"],
    answer: 1,
    explain: "Differences: (1,1,3,1); squares: (1,1,9,1); sum = 12; distance = √12 = 2√3 ≈ 3.464.",
  },
  {
    q: "When would you apply a log transformation to an attribute like salary?",
    options: [
      "When the attribute is nominal",
      "When the distribution is heavily right-skewed and spans several orders of magnitude",
      "When you want to increase the outlier's influence",
      "Only on binary attributes",
    ],
    answer: 1,
    explain: "Log transformation compresses large values much more than small ones, reducing right-skew and preventing one huge value (like a $1,000,000 salary) from drowning out smaller-scale differences (like a $92 dinner bill) in the same analysis.",
  },
];
