# Chapter 5: Clustering — Comprehensive Notes

---

## Table of Contents
1. [Clustering Concept](#1-clustering-concept)
2. [Distance Measures](#2-distance-measures)
3. [Types of Clusters and Clusterings](#3-types-of-clusters-and-clusterings)
4. [K-Means Clustering](#4-k-means-clustering)
5. [Hierarchical Clustering](#5-hierarchical-clustering)
6. [DBSCAN](#6-dbscan)
7. [Comparison Table](#7-comparison-table)
8. [Quick Reference](#8-quick-reference)

---

## 1. Clustering Concept

**Goal:** Partition a dataset into groups (clusters) such that:
- **Intra-cluster distance is minimized** — objects within the same cluster are as similar as possible
- **Inter-cluster distance is maximized** — objects in different clusters are as dissimilar as possible

Clustering is an **unsupervised** learning task — there are no predefined class labels.

**Use cases:** Customer segmentation, document grouping, anomaly detection, image compression, gene expression analysis.

---

## 2. Distance Measures

### 2.1 Single-Attribute Distances

#### Quantitative (Continuous)
```
d(a, b) = |a - b|
```
Example: age difference between two people.

#### Ordinal
Ordinal attributes have a meaningful order (e.g., low < medium < high).
```
d(a, b) = |pos_a - pos_b| / (n - 1)
```
- `pos_a`, `pos_b`: the rank/position of values a and b (0-indexed or normalized)
- `n`: number of distinct possible values
- Result is always in [0, 1]

Example: Education levels {none=0, primary=1, secondary=2, bachelor=3, master=4, PhD=5}, n=6.
d(primary, master) = |1 - 4| / (6 - 1) = 3/5 = 0.6

#### Nominal (Categorical)
No inherent order — values are just labels.
```
d(a, b) = 0  if a == b
d(a, b) = 1  if a != b
```
Example: d("male", "female") = 1; d("male", "male") = 0.

---

### 2.2 Minkowski Distance (Multi-Attribute)

Generalizes several common distances for two points x = (x1, x2, ..., xd) and y = (y1, y2, ..., yd):

```
d(x, y) = ( sum_{k=1}^{d} |x_k - y_k|^r )^(1/r)
```

| r value | Name | Also Called |
|---------|------|-------------|
| r = 1 | Manhattan Distance | City-block distance, L1 norm, Taxicab distance |
| r = 2 | Euclidean Distance | Straight-line distance, L2 norm |
| r -> inf | Chebyshev Distance | L-infinity norm: max(|x_k - y_k|) |

**Manhattan (r=1):**
```
d(x, y) = sum_{k=1}^{d} |x_k - y_k|
```

**Euclidean (r=2):**
```
d(x, y) = sqrt( sum_{k=1}^{d} (x_k - y_k)^2 )
```

---

### 2.3 Hamming Distance

Used for **strings of equal length** or **binary vectors**.

```
d(s1, s2) = number of positions where s1[i] != s2[i]
```

Examples:
- d("James", "Jimmy") = 3  (positions 1, 3, 4 differ: a/i, e/m, s/y)
- d("1011101", "1001001") = 2  (positions 3 and 5 differ)

**Note:** Both strings must have the same length.

---

### 2.4 Edit Distance (Levenshtein Distance)

Minimum number of single-character operations to transform one string into another:
- **Insert** a character
- **Delete** a character
- **Substitute** one character for another

Computed via **dynamic programming**:

```
Let dp[i][j] = edit distance between s1[0..i-1] and s2[0..j-1]

Base cases:
  dp[i][0] = i   (delete i chars)
  dp[0][j] = j   (insert j chars)

Recurrence:
  if s1[i-1] == s2[j-1]:
      dp[i][j] = dp[i-1][j-1]             (no operation needed)
  else:
      dp[i][j] = 1 + min(
          dp[i-1][j],     (delete from s1)
          dp[i][j-1],     (insert into s1)
          dp[i-1][j-1]    (substitute)
      )
```

Example: d("Johnny", "Jonston") = 5

---

## 3. Types of Clusters and Clusterings

### 3.1 Types of Clusters

| Type | Description | Example |
|------|-------------|---------|
| **Well-separated** | Each point is closer to all members of its cluster than to any point in another cluster | Naturally separated blobs |
| **Prototype-based** | Each point is closest to its cluster's representative | Centroid-based (K-means) or medoid-based (K-medoids) |
| **Contiguity-based** | Points connected to at least one other point in the cluster | Nearest-neighbor / chain clusters |
| **Density-based** | Clusters are dense regions surrounded by low-density space | DBSCAN clusters |

### 3.2 Types of Clusterings

| Type | Description |
|------|-------------|
| **Partitional** | Non-overlapping, non-hierarchical division into K groups |
| **Hierarchical** | Nested clusters organized as a tree (dendrogram) |
| **Fuzzy** | Each point has a fractional membership in multiple clusters |
| **Exclusive vs Overlapping** | Whether a point belongs to exactly one vs multiple clusters |

---

## 4. K-Means Clustering

### 4.1 Algorithm

```
INPUT: dataset D with n points, number of clusters K
OUTPUT: cluster assignments and K centroids

1. Choose K initial centroids (randomly or by K-means++)
2. REPEAT:
   a. Assignment step:
      For each point x in D:
          Assign x to the cluster with the nearest centroid
          (ties broken arbitrarily)
   b. Update step:
      For each cluster i:
          Recompute centroid m_i = mean of all points assigned to cluster i
3. UNTIL centroids do not change (convergence)
```

### 4.2 SSE Objective Function

K-means minimizes the **Sum of Squared Errors (SSE)**:

```
SSE = sum_{i=1}^{K} sum_{x in C_i} dist^2(m_i, x)
```

Where:
- `C_i` = set of points in cluster i
- `m_i` = centroid of cluster i
- `dist^2(m_i, x)` = squared Euclidean distance

Lower SSE = tighter, more compact clusters.

### 4.3 Complexity

```
O(n * K * d * I)
```
- n = number of data points
- K = number of clusters
- d = number of dimensions (attributes)
- I = number of iterations until convergence

K-means is generally linear in n, K, d and converges in few iterations.

### 4.4 K-Means++ Initialization

Standard K-means uses random initialization, which can lead to poor local minima. K-means++ uses smarter initialization:

```
ALGORITHM K-means++:
1. Choose the first centroid c1 uniformly at random from D
2. For each remaining centroid c2, c3, ..., cK:
   a. For each point x in D, compute D(x) = min distance to nearest already-chosen centroid
   b. Choose the next centroid from D with probability proportional to D(x)^2
      (points far from existing centroids are more likely to be chosen)
3. Proceed with standard K-means using these K initial centroids
```

**Benefit:** Reduces number of iterations and avoids degenerate solutions. Provides O(log K) approximation guarantee on SSE.

### 4.5 Elbow Curve Method (Choosing K)

```
PROCEDURE:
1. Run K-means for K = 1, 2, 3, ..., max_K
2. Record SSE for each K
3. Plot SSE vs K
4. Find the "elbow" -- the point where SSE decrease rate slows sharply
5. The K at the elbow is a good choice
```

As K increases, SSE always decreases. The elbow point represents diminishing returns on adding more clusters.

### 4.6 Friends Dataset Example

```
Person    Age   Education
Andrew    55    1
Bernhard  43    2
Carolina  37    5
Dennis    82    3
Eve       23    3.2
Fred      46    5
Gwyneth   38    4.2
Hayden    50    4
Irene     29    4.5
James     42    4.1
```

**Exercise Q1 (6-person subset, K=2):**
- Initial centroids: Andrew(55,1) and Carolina(37,5)
- Distances to Andrew: A=0, B=12.0, C=17.2, D=27.1, E=32.4, F=9.85
- Distances to Carolina: A=17.2, B=6.7, C=0, D=45.2, E=14.0, F=9.0
- Cluster 1 (Andrew): {A, D}  -> new centroid = (68.5, 2)
- Cluster 2 (Carolina): {B, C, E, F}  -> new centroid = (37.25, 3.8)

**Full 10-person, K=4 result:**
- Cluster 1: {Andrew, Bernhard, Dennis}
- Cluster 2: {Eve, Irene}
- Cluster 3: {Gwyneth, Hayden, Fred, James, Carolina}

### 4.7 K-Means Limitations

| Limitation | Description |
|-----------|-------------|
| Assumes convex/globular clusters | Fails on crescent, ring, or irregular shapes |
| Sensitive to outliers | Outliers pull centroids away from true cluster centers |
| Different cluster sizes | Large clusters dominate SSE optimization |
| Different cluster densities | Dense and sparse clusters not handled equally |
| Non-globular shapes | Elongated or curved shapes misclassified |
| Requires K upfront | K must be specified before running |

---

## 5. Hierarchical Clustering

### 5.1 Approaches

**Agglomerative (Bottom-Up):**
```
1. Start: each of n points is its own cluster (n clusters)
2. Repeat:
   a. Find the two closest clusters
   b. Merge them into one
3. Until: only 1 cluster remains
```

**Divisive (Top-Down):**
```
1. Start: all n points in one cluster
2. Repeat:
   a. Select a cluster to split
   b. Split it into two subclusters
3. Until: each cluster has 1 point
```

The result is recorded as a **dendrogram** -- a tree diagram showing the sequence and distances of merges/splits.

### 5.2 Linkage Methods

The linkage method defines how inter-cluster distance is computed when two clusters A and B are compared.

#### MIN (Single Linkage)
```
d(A, B) = min_{a in A, b in B} dist(a, b)
```
- Uses the **closest pair** of points between clusters
- Can find non-elliptical shapes
- Sensitive to noise (chaining effect)

#### MAX (Complete Linkage)
```
d(A, B) = max_{a in A, b in B} dist(a, b)
```
- Uses the **farthest pair** of points between clusters
- Less sensitive to noise and outliers
- Biased toward globular, equal-diameter clusters

#### Group Average (Average Linkage)
```
d(A, B) = (1 / (|A| * |B|)) * sum_{a in A} sum_{b in B} dist(a, b)
```
- Uses the **average** of all pairwise distances
- Less extreme than MIN or MAX
- Biased toward globular clusters

#### Ward's Method
Minimize the increase in SSE when merging two clusters:
```
delta_SSE(A, B) = (|A| * |B|) / (|A| + |B|) * dist^2(centroid_A, centroid_B)
```
- Merge the pair that results in the **smallest SSE increase**
- Similar to group average but uses squared distances
- Tends to produce compact, equal-sized clusters

### 5.3 Comparison of Linkages

| Method | Cluster Shape | Noise Sensitivity | Bias |
|--------|--------------|-------------------|------|
| Single | Non-elliptical | High | Chaining |
| Complete | Globular | Low | Equal-diameter |
| Average | Moderate | Moderate | Globular |
| Ward | Globular | Low | Equal-size |

### 5.4 Dendrogram Reading

- **Y-axis:** Distance (or dissimilarity) at which clusters were merged
- **X-axis:** Individual data points (leaves)
- **Cut height:** Cutting the dendrogram horizontally at a given height yields K clusters
- Agglomerative dendrograms are read bottom-up; divisive are read top-down

### 5.5 Complexity

Agglomerative with naive implementation: **O(n^3)** in time, **O(n^2)** in space.
With optimized data structures: **O(n^2 log n)**.

---

## 6. DBSCAN

**Density-Based Spatial Clustering of Applications with Noise**

### 6.1 Key Parameters
- **Eps (epsilon):** Radius defining the neighborhood of a point
- **MinPts:** Minimum number of points required to form a dense region (core point)

### 6.2 Point Classification

```
Given parameters Eps and MinPts:

Core point:   |N_Eps(p)| >= MinPts
              (p has at least MinPts points within distance Eps, including itself)

Border point: |N_Eps(p)| < MinPts  BUT  p is within Eps of some core point

Noise point:  not a core point AND not within Eps of any core point
```

Where `N_Eps(p)` = neighborhood of p = {q : dist(p, q) <= Eps}

### 6.3 Algorithm

```
DBSCAN(D, Eps, MinPts):
1. Label all points as Core, Border, or Noise
2. Eliminate noise points (label = -1)
3. For each core point p not yet assigned to a cluster:
   a. Create a new cluster C
   b. Add p to C
   c. Add all points density-reachable from p to C
      (density-reachable: can reach via chain of core points within Eps)
4. For each border point:
   Assign to the cluster of the nearest core point
```

**Density-reachability:** Point q is density-reachable from p if there exists a chain p = p1, p2, ..., pn = q where each pi+1 is within Eps of pi and p1, ..., pn-1 are core points.

### 6.4 Advantages and Disadvantages

| Advantages | Disadvantages |
|-----------|---------------|
| Finds arbitrarily shaped clusters | Struggles with varying-density clusters |
| Resistant to noise and outliers | Sensitive to Eps and MinPts parameter choice |
| Does not require K upfront | High-dimensional data degrades performance |
| Can identify noise explicitly | Border points may be assigned non-deterministically |

### 6.5 Choosing Parameters

- **MinPts:** Rule of thumb: MinPts >= d + 1 where d = dimensions. Often use 4 or 2*d.
- **Eps:** Sort distances to the k-th nearest neighbor (k = MinPts - 1), plot sorted values, look for the elbow.

---

## 7. Comparison Table

| Property | K-Means | Hierarchical | DBSCAN |
|----------|---------|-------------|--------|
| **Cluster shape** | Globular/convex | Any (depends on linkage) | Arbitrary |
| **Requires K** | Yes | No (cut dendrogram) | No |
| **Handles noise** | No | Partially | Yes (explicit noise label) |
| **Scalability** | O(n*K*d*I) -- good | O(n^2) to O(n^3) -- poor | O(n log n) with index |
| **Deterministic** | No (random init) | Yes | Mostly yes |
| **Cluster sizes** | Assumes similar | Flexible | Flexible |
| **Interpretability** | High (centroids) | High (dendrogram) | Moderate |
| **Parameter sensitivity** | K | linkage + cut height | Eps + MinPts |
| **Best for** | Large datasets, known K | Nested structure, small datasets | Spatial data, unknown K, noise |

---

## 8. Quick Reference

### Distance Formula Summary

| Measure | Formula | Use Case |
|---------|---------|---------|
| Quantitative | `\|a - b\|` | Age, income, temperature |
| Ordinal | `\|pos_a - pos_b\| / (n-1)` | Education level, rankings |
| Nominal | `0 if a==b, else 1` | Color, gender, category |
| Manhattan (L1) | `sum \|x_k - y_k\|` | Grid-like movement |
| Euclidean (L2) | `sqrt(sum (x_k - y_k)^2)` | Straight-line distance |
| Minkowski (Lr) | `(sum \|x_k - y_k\|^r)^(1/r)` | General case |
| Hamming | `# positions that differ` | Strings, binary vectors |
| Edit/Levenshtein | `min insert+delete+substitute` | Fuzzy string matching |

### K-Means Checklist

- [ ] Choose K (use elbow method or domain knowledge)
- [ ] Normalize features (if scales differ greatly)
- [ ] Use K-means++ for better initialization
- [ ] Run multiple times, keep best SSE
- [ ] Validate with silhouette score or domain knowledge

### DBSCAN Checklist

- [ ] Choose Eps using k-distance graph elbow method
- [ ] Choose MinPts >= d + 1 (at least 4 for 2D data)
- [ ] Check that noise proportion is reasonable
- [ ] Try different Eps values if clusters are fragmented or merged

### Key Formulas

```
SSE       = sum_i sum_{x in C_i} ||x - m_i||^2
Minkowski = ( sum_k |x_k - y_k|^r )^(1/r)
Ordinal   = |pos_a - pos_b| / (n - 1)
Ward's    = (|A|*|B|)/(|A|+|B|) * ||m_A - m_B||^2
Avg Link  = (1/(|A|*|B|)) * sum_{a,b} dist(a,b)
```
