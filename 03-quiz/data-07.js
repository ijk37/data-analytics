// ── Chapter 07 — Classification ──────────────────────────────────────────────
QUESTIONS["07"] = [
  {
    q: "In supervised learning, what is the TEST set used for?",
    options: [
      "Training the model's parameters",
      "Evaluating the model's performance on held-out data it never trained on",
      "Replacing the training set entirely",
      "Only visualizing the data",
    ],
    answer: 1,
    explain: "The test set must be held out and never used during training — its only job is to give an honest estimate of how the model performs on data it hasn't seen.",
  },
  {
    q: "For a pure node (all examples belong to one class), what is its entropy H(S)?",
    options: ["1", "0.5", "0", "Undefined"],
    answer: 2,
    explain: "H(S) = -Σ p_i·log2(p_i). If one class has p=1 and all others p=0, entropy is exactly 0 — the convention 0·log2(0)=0 avoids an undefined term, and 0 entropy means the node is perfectly pure.",
  },
  {
    q: "Which impurity measure does the ID3 algorithm use to choose the best split attribute?",
    options: ["Gini impurity", "Information Gain (based on entropy)", "Euclidean distance", "F1 score"],
    answer: 1,
    explain: "ID3 (and C4.5) pick the attribute A that maximizes Information Gain: IG(S,A) = H(S) - Σ (|Sv|/|S|)·H(Sv). CART uses Gini impurity instead.",
  },
  {
    q: "Why does Gain Ratio improve on plain Information Gain?",
    options: [
      "It removes the need for entropy entirely",
      "It normalizes IG by SplitInfo, correcting IG's bias toward attributes with many distinct values",
      "It only works for binary classification",
      "It always picks a different attribute than IG",
    ],
    answer: 1,
    explain: "Plain IG is biased toward high-cardinality attributes (like an ID column, which perfectly 'predicts' the class by splitting into singleton groups but is useless for generalization). Gain Ratio divides by SplitInfo to penalize splits that fragment the data too finely.",
  },
  {
    q: "For the Friends Food dataset (6 good, 3 bad, n=9), what is the Gini impurity of the root node?",
    options: ["0", "0.444", "0.918", "1.0"],
    answer: 1,
    explain: "Gini(S) = 1 - ((6/9)² + (3/9)²) = 1 - (0.444 + 0.111) = 0.444. (The entropy of the same node, by comparison, is 0.918 — different formula, same idea of 'how mixed is this node'.)",
  },
  {
    q: "What must you do to numeric features before running k-NN, and why?",
    options: [
      "Nothing — k-NN works fine on raw scales",
      "Normalize them (min-max or z-score), so no single large-scale feature dominates the distance calculation",
      "Convert them all to nominal categories first",
      "Remove all numeric features",
    ],
    answer: 1,
    explain: "k-NN relies on distance (typically Euclidean), so an unnormalized feature with a huge numeric range (like income) would swamp a feature with a small range (like age in years) in every distance calculation.",
  },
  {
    q: "What happens to the k-NN decision boundary as k gets very large?",
    options: [
      "It becomes extremely jagged and sensitive to noise",
      "It becomes smoother, which can lead to underfitting",
      "k has no effect on the boundary",
      "The model stops requiring training data",
    ],
    answer: 1,
    explain: "k=1 gives a highly complex, noise-sensitive boundary (overfitting risk); as k grows, the majority vote smooths the boundary, but too large a k can blur over genuine local structure (underfitting).",
  },
  {
    q: "In Naive Bayes, what does the 'naive' independence assumption actually assume?",
    options: [
      "That there is only one feature",
      "That every feature is conditionally independent of the others, given the class",
      "That all classes have equal size",
      "That features must be numeric",
    ],
    answer: 1,
    explain: "P(X|C) = P(x1|C)·P(x2|C)·...·P(xn|C) — treating each feature as independent given the class label. This assumption is rarely exactly true in practice, but the method still often works well.",
  },
  {
    q: "Why is Laplace smoothing needed in Naive Bayes?",
    options: [
      "To make computation faster",
      "To prevent an unseen (value, class) combination — which has raw probability 0 — from zeroing out the entire product",
      "It's only needed for numeric (Gaussian) features",
      "To increase the number of classes",
    ],
    answer: 1,
    explain: "Without smoothing, one never-seen combination gives P(x_j|C)=0, which multiplies the whole class score to zero regardless of how strong the other evidence is. Adding 1 to every count (and the domain size to the denominator) avoids this.",
  },
  {
    q: "In the Laplace-smoothed formula P(x_j|C) = (count(x_j,C) + 1) / (count(C) + |domain(x_j)|), what does |domain(x_j)| represent?",
    options: [
      "The total number of training examples",
      "The number of distinct values feature x_j can take",
      "The number of classes",
      "Always exactly 2",
    ],
    answer: 1,
    explain: "The denominator adds one 'pseudo-count' for every possible value the feature could take, which is why you divide by the count of distinct values in that feature's domain, not just add a flat 1.",
  },
  {
    q: "In a confusion matrix, what does a False Positive (FP) mean?",
    options: [
      "Predicted negative, actually positive",
      "Predicted positive, but actually negative",
      "Correctly predicted positive",
      "Correctly predicted negative",
    ],
    answer: 1,
    explain: "FP = model said 'positive' but the true label was negative (a Type I error). The opposite case — predicted negative but actually positive — is a False Negative (FN, Type II error).",
  },
  {
    q: "Precision answers which question?",
    options: [
      "Of all actual positives, how many did the model correctly catch?",
      "Of all instances the model predicted positive, how many actually are positive?",
      "What fraction of all predictions were correct overall?",
      "How balanced are the two classes?",
    ],
    answer: 1,
    explain: "Precision = TP / (TP + FP) — it only looks at the predicted-positive group and asks how many were right. Recall = TP / (TP + FN) instead asks how many of the actual positives were found.",
  },
  {
    q: "Given TP=40, FP=10, FN=5, TN=45, what is the F1 score?",
    options: ["0.80", "0.842", "0.889", "0.85"],
    answer: 1,
    explain: "Precision = 40/50 = 0.80. Recall = 40/45 ≈ 0.889. F1 = 2×(0.80×0.889)/(0.80+0.889) ≈ 1.422/1.689 ≈ 0.842.",
  },
  {
    q: "Why is k-fold cross-validation generally preferred over a single train/test split?",
    options: [
      "It trains the model only once, saving time",
      "It averages performance across k different train/test partitions, giving a more reliable estimate than one lucky/unlucky split",
      "It eliminates the need for a test set entirely",
      "It always increases the reported accuracy",
    ],
    answer: 1,
    explain: "A single split's accuracy depends heavily on which rows land in the test set by chance. k-fold CV rotates every fold through as the test set once, and averaging (with the standard deviation) gives a much more stable estimate of true performance.",
  },
  {
    q: "What does STRATIFIED k-fold cross-validation add on top of standard k-fold?",
    options: [
      "It uses a larger k automatically",
      "Each fold preserves the original class proportions, preventing any fold from being accidentally almost all one class",
      "It removes the need for multiple folds",
      "It only works with Naive Bayes",
    ],
    answer: 1,
    explain: "Without stratification, a fold from a small or imbalanced dataset could randomly end up mostly one class, badly skewing that fold's accuracy. Stratified k-fold deliberately keeps each fold's class balance matching the overall dataset.",
  },
];
