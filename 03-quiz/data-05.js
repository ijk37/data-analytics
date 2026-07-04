// ── Chapter 05 — Clustering ──────────────────────────────────────────────────
QUESTIONS["05"] = [
  {
    q: "What is the primary goal of clustering?",
    options: [
      "Maximize intra-cluster distance and minimize inter-cluster distance",
      "Minimize intra-cluster distance and maximize inter-cluster distance",
      "Predict a known class label for each object",
      "Always produce exactly 2 clusters",
    ],
    answer: 1,
    explain: "Clustering wants objects within the same group to be as similar (close) as possible, and objects in different groups to be as dissimilar (far apart) as possible — it's unsupervised, with no predefined labels.",
  },
  {
    q: "For an ordinal attribute with n possible values, the distance formula |pos_a - pos_b| / (n-1) always produces a result in what range?",
    options: ["[0, n]", "[0, 1]", "[-1, 1]", "[1, n]"],
    answer: 1,
    explain: "Dividing by (n-1), the maximum possible position difference, normalizes the distance into [0, 1] regardless of how many ordinal levels exist.",
  },
  {
    q: "Which Minkowski distance (r value) corresponds to Manhattan distance?",
    options: ["r = 1", "r = 2", "r → ∞", "r = 0"],
    answer: 0,
    explain: "r=1 gives Manhattan (city-block/L1) distance: sum of absolute differences. r=2 is Euclidean (L2); r→∞ is Chebyshev (max absolute difference).",
  },
  {
    q: "What is the Hamming distance between the binary strings '1011101' and '1001001'?",
    options: ["1", "2", "3", "4"],
    answer: 1,
    explain: "Comparing position by position, they differ at exactly 2 positions (3rd and 5th) — Hamming distance requires equal-length strings and counts mismatched positions.",
  },
  {
    q: "What does edit (Levenshtein) distance measure?",
    options: [
      "The count of differing positions in equal-length strings only",
      "The minimum number of insertions, deletions, and substitutions to transform one string into another",
      "The number of shared characters between two strings",
      "Always the same as Hamming distance",
    ],
    answer: 1,
    explain: "Unlike Hamming distance, edit distance allows strings of different lengths by counting the minimum single-character insert/delete/substitute operations needed, computed via dynamic programming.",
  },
  {
    q: "What does K-means minimize as its objective function?",
    options: [
      "The number of clusters K",
      "SSE — the Sum of Squared (Euclidean) distances from each point to its assigned centroid",
      "The total number of iterations",
      "The Manhattan distance only",
    ],
    answer: 1,
    explain: "SSE = Σ over clusters Σ over points in that cluster of dist²(point, centroid). Lower SSE means tighter, more compact clusters.",
  },
  {
    q: "In K-means, using Andrew(55,1) and Carolina(37,5) as initial centroids, Bernhard(43,2) has distance 12.0 to Andrew and 6.7 to Carolina. Which cluster is Bernhard assigned to on this iteration?",
    options: ["Andrew's cluster (Cluster 1)", "Carolina's cluster (Cluster 2)", "Neither — it's noise", "Both clusters equally"],
    answer: 1,
    explain: "K-means assigns each point to its NEAREST centroid. Bernhard is closer to Carolina (6.7) than to Andrew (12.0), so it joins Carolina's cluster.",
  },
  {
    q: "What advantage does K-means++ have over standard random centroid initialization?",
    options: [
      "It removes the need to choose K at all",
      "It picks new centroids with probability proportional to their squared distance from existing centroids, avoiding poor local minima",
      "It always converges in exactly 1 iteration",
      "It only works for K=2",
    ],
    answer: 1,
    explain: "By favoring points that are far from already-chosen centroids, K-means++ spreads the initial centroids out, reducing the chance of a bad random start and typically converging faster to a better solution.",
  },
  {
    q: "In the elbow method for choosing K, what are you looking for?",
    options: [
      "The K where SSE stops decreasing entirely",
      "The point where the SSE-vs-K curve's decrease rate slows sharply (diminishing returns)",
      "The K with the maximum SSE",
      "Always K = number of data points",
    ],
    answer: 1,
    explain: "SSE always decreases as K increases (more clusters = tighter fit), but at some point adding another cluster barely helps — that bend or 'elbow' in the curve is the recommended K.",
  },
  {
    q: "Which is a known WEAKNESS of K-means?",
    options: [
      "It cannot handle numeric data",
      "It assumes roughly globular/convex clusters and is sensitive to outliers",
      "It never converges",
      "It doesn't require choosing K in advance",
    ],
    answer: 1,
    explain: "K-means struggles with non-globular (elongated, ring-shaped) clusters, varying densities/sizes, and outliers (which pull centroids away from the true cluster center) — and it does require K upfront.",
  },
  {
    q: "In hierarchical clustering, which linkage method uses the CLOSEST pair of points between two clusters?",
    options: ["Complete (MAX) linkage", "Single (MIN) linkage", "Average linkage", "Ward's method"],
    answer: 1,
    explain: "Single (MIN) linkage measures inter-cluster distance as the minimum distance between any pair of points — it can trace non-elliptical shapes but is prone to a 'chaining' effect on noisy data.",
  },
  {
    q: "Which linkage method tends to produce compact, roughly equal-diameter clusters and is less sensitive to noise?",
    options: ["Single (MIN) linkage", "Complete (MAX) linkage", "None of these differ", "K-means only"],
    answer: 1,
    explain: "Complete (MAX) linkage uses the FARTHEST pair of points between two clusters, which biases the result toward compact, globular, similarly-sized clusters and resists chaining from noise.",
  },
  {
    q: "In a dendrogram, what does cutting the tree horizontally at a given height produce?",
    options: [
      "A fixed number of clusters (always 2)",
      "A set of K clusters, where K depends on the cut height chosen",
      "The original ungrouped dataset",
      "Nothing — dendrograms cannot be cut",
    ],
    answer: 1,
    explain: "The dendrogram's y-axis is the merge distance; cutting at a chosen height slices through some number of branches, and each remaining branch below the cut becomes one cluster — so you don't need to fix K in advance.",
  },
  {
    q: "In DBSCAN, what is a CORE point?",
    options: [
      "Any point at the center of the dataset",
      "A point with at least MinPts points (including itself) within distance Eps",
      "A point that is never assigned to any cluster",
      "The single densest point in the whole dataset",
    ],
    answer: 1,
    explain: "A core point has a 'dense enough' neighborhood — at least MinPts points within radius Eps — and core points are the seeds that clusters grow from via density-reachability.",
  },
  {
    q: "What is a key ADVANTAGE of DBSCAN over K-means?",
    options: [
      "DBSCAN requires you to specify K in advance",
      "DBSCAN can find arbitrarily shaped clusters and explicitly labels outliers as noise",
      "DBSCAN always runs faster on every dataset",
      "DBSCAN has no parameters to tune",
    ],
    answer: 1,
    explain: "Unlike K-means (which assumes globular clusters and forces every point into some cluster), DBSCAN finds clusters of any shape using density and explicitly marks low-density points as noise rather than distorting a cluster to include them.",
  },
];
