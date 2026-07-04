# Data Analytics Super-Summary — Cheat Sheet
> Scan time: ~10 minutes. Vital concepts only.

---

## Ch1 — Data & Attribute Types

### Stevens' 4 Measurement Scales

| Scale    | Order? | Equal Intervals? | True Zero? | Example               | Operations          |
|----------|--------|-----------------|------------|-----------------------|---------------------|
| Nominal  | No     | No              | No         | Gender, Color, ZIP    | =, !=               |
| Ordinal  | Yes    | No              | No         | Rankings, Grades A-F  | =, !=, <, >         |
| Interval | Yes    | Yes             | No         | Temperature (C/F)     | +, -, mean, std     |
| Ratio    | Yes    | Yes             | Yes        | Weight, Height, Age   | all ops, ratios OK  |

**Key rule:** You can always go DOWN the scale (treat ratio as ordinal) but never UP.

### Dataset Types

| Type        | Structure                        | Example                        |
|-------------|----------------------------------|--------------------------------|
| Record/Matrix | Rows = objects, Cols = attrs   | Spreadsheet, CSV               |
| Document    | Term-frequency vectors           | Bag-of-words                   |
| Transaction | Sets of items per record         | Shopping baskets               |
| Graph       | Nodes + edges                    | Social networks, Web           |
| Ordered     | Sequence / time-series           | Stock prices, sensor logs      |

### Discrete vs Continuous
- **Discrete:** countable values (number of children, dice roll)
- **Continuous:** measurable on a real line (height, temperature)

---

## Ch2 — Descriptive Statistics (Univariate & Bivariate)

### Location Measures

| Measure | Formula / Definition             | Notes                              |
|---------|----------------------------------|------------------------------------|
| Mode    | Most frequent value              | Can be multiple; use for nominal   |
| Median  | Middle value (sorted)            | Robust to outliers                 |
| Mean    | sum(xi) / n                      | Sensitive to outliers              |
| Q1      | 25th percentile                  |                                    |
| Q3      | 75th percentile                  |                                    |
| IQR     | Q3 - Q1                          | Middle 50% spread                  |

### Dispersion Measures

| Measure  | Formula                                  | Notes                    |
|----------|------------------------------------------|--------------------------|
| Range    | max - min                                | Very sensitive to outliers|
| IQR      | Q3 - Q1                                  | Robust                   |
| MAD      | mean( |xi - median| )                     | Robust                   |
| Variance | sum((xi - mean)^2) / (n-1)               | Sample variance          |
| Std Dev  | sqrt(variance)                           | Same units as data       |

### Skewness

```
Positive skew:  long tail to the RIGHT   =>  mean > median > mode
Symmetric:      bell-shaped              =>  mean = median = mode
Negative skew:  long tail to the LEFT    =>  mean < median < mode
```

### Boxplot
```
  [min*]  Q1 [====median====] Q3  [max*]
            |<------ IQR ----->|

Whiskers: lower = Q1 - 1.5*IQR,  upper = Q3 + 1.5*IQR
Outliers: points beyond whiskers (plotted individually)
```

### Bivariate Statistics

| Measure        | Formula                                           | Range    |
|----------------|---------------------------------------------------|----------|
| Covariance     | sum((xi-xbar)(yi-ybar)) / (n-1)                   | (-inf,+inf)|
| Pearson r      | cov(X,Y) / (sx * sy)                              | [-1, +1] |
| Spearman rho   | Pearson r computed on RANKS of X and Y            | [-1, +1] |

- r = +1: perfect positive linear; r = -1: perfect negative; r = 0: no linear correlation
- Spearman: use when data is ordinal OR relationship is monotone but not linear

---

## Ch3 — Descriptive Statistics (Multivariate)

### Summary Matrices

| Matrix            | Size    | Diagonal      | Symmetry  | Content              |
|-------------------|---------|---------------|-----------|----------------------|
| Location matrix   | 7 x p   | N/A           | No        | min/Q1/med/mean/mode/Q3/max per column |
| Covariance matrix | p x p   | variances     | Symmetric | cov(Xi, Xj)          |
| Correlation matrix| p x p   | all 1s        | Symmetric | Pearson r(Xi, Xj)    |

### Key Multivariate Plots

| Plot                  | Best for                                              |
|-----------------------|-------------------------------------------------------|
| Scatter matrix        | All pairwise relationships at once                    |
| Parallel coordinates  | Each object = polyline; spot clusters/outliers        |
| Star/Radar chart      | One polygon per object; compare profiles              |
| Chernoff faces        | Encode attributes as facial features; detect groups   |
| Heatmap + dendrogram  | Similarity structure; combined with clustering        |

---

## Ch4 — Data Preprocessing

### Missing Values

| Strategy                  | When to use                          |
|---------------------------|--------------------------------------|
| Remove row                | Few missing, dataset large enough    |
| Fill with mean            | Numeric, symmetric distribution      |
| Fill with median          | Numeric, skewed distribution         |
| Fill with mode            | Nominal attribute                    |
| Fill with per-class mean  | When class label is known            |

### Discretization (Numeric -> Bins)

```
Equal-width:  W = (max - min) / N    (bins have equal range)
Equal-depth:  sort, then N/k objects per bin  (bins have equal count)
```

### Encoding Categorical -> Numeric

| Method       | k categories -> | Example (Low/Med/High)  |
|--------------|-----------------|--------------------------|
| One-hot      | k binary cols   | 100 / 010 / 001          |
| Gray code    | log2(k) bits    | 00 / 01 / 11             |
| Thermometer  | k-1 bits        | 00 / 10 / 11             |

### Normalization

```
Min-max:  v' = (v - min) / (max - min) * (new_max - new_min) + new_min
          Typical new range: [0, 1]

Z-score:  v' = (v - mu) / sigma
          Result: mean=0, std=1
```

**Always normalize before computing Euclidean distance.**

### Distance Metrics

| Metric      | Formula                         | Notes                     |
|-------------|---------------------------------|---------------------------|
| Euclidean   | sqrt(sum((xi-yi)^2))            | Standard; sensitive to scale|
| Manhattan   | sum(|xi-yi|)                    | L1 norm; robust to outliers|
| Minkowski   | (sum(|xi-yi|^p))^(1/p)         | Lp: p=1->Manhattan, p=2->Euclidean|
| Hamming     | count of positions where xi!=yi | For strings/bit vectors   |
| Edit/Levenshtein | min insertions/deletions/substitutions | For strings    |

---

## Ch5 — Clustering

### K-Means

```
1. Choose K initial centroids (random or K-means++)
2. Assign each object to nearest centroid
3. Recompute centroids as mean of assigned objects
4. Repeat steps 2-3 until assignments don't change
SSE = sum over all objects of dist(object, its_centroid)^2
Elbow method: plot SSE vs K; pick K at the "elbow"
```

**K-means++:** next centroid chosen with probability proportional to dist^2 from nearest existing centroid — better initial placement, faster convergence.

### Hierarchical (Agglomerative)

```
Start: each object is its own cluster
Repeat: merge the two closest clusters
Stop: when one cluster remains (or desired K reached)
```

| Linkage  | Distance(A,B) =                     | Behavior                      |
|----------|--------------------------------------|-------------------------------|
| MIN (Single)   | min dist between any pair      | Chaining effect; elongated    |
| MAX (Complete) | max dist between any pair      | Compact, roughly equal size   |
| Average  | mean dist between all pairs          | Compromise                    |
| Ward     | minimize increase in SSE after merge | Usually best; similar to K-means|

### DBSCAN

```
Parameters: Eps (radius), MinPts (density threshold)
Core point:   has >= MinPts neighbors within Eps
Border point: within Eps of a core point, but not core itself
Noise point:  neither core nor border
```
- Handles arbitrary cluster shapes
- Automatically finds number of clusters
- Robust to outliers (labeled as noise)

### Comparing Clustering Methods

| Method        | Need K? | Shape     | Outliers | Complexity      |
|---------------|---------|-----------|----------|-----------------|
| K-means       | Yes     | Spherical | Sensitive| O(n*K*iter)     |
| Hierarchical  | No*     | Any       | Sensitive| O(n^2) or O(n^2 log n)|
| DBSCAN        | No      | Arbitrary | Robust   | O(n log n)      |

---

## Ch6 — Frequent Pattern Mining

### Key Definitions

```
Support(X)       = |transactions containing X| / |total transactions|
Confidence(X->Y) = support(X union Y) / support(X)
Lift(X->Y)       = confidence(X->Y) / support(Y)
```

| Lift value | Meaning                          |
|------------|----------------------------------|
| > 1        | Positive correlation (buy together more than chance) |
| = 1        | Independent                      |
| < 1        | Negative correlation             |

### Apriori Algorithm
- **Anti-monotone property:** if itemset X is infrequent, ALL supersets of X are infrequent
- Algorithm: generate candidate k-itemsets from frequent (k-1)-itemsets, prune using anti-monotone
- Weakness: multiple database scans, large candidate sets

### FP-Growth Algorithm
- Build compact FP-tree (prefix tree of transactions)
- Mine conditional pattern bases — no candidate generation
- Faster than Apriori, especially for dense/long patterns
- Requires only 2 database scans

### Itemset Types

| Type              | Definition                                       |
|-------------------|--------------------------------------------------|
| Frequent          | support >= min_support                           |
| Maximal frequent  | Frequent and NO frequent superset exists         |
| Closed frequent   | Frequent and NO superset with SAME support exists|

**Relationship:** Maximal ⊂ Closed ⊂ Frequent

### Association Rules Summary
- Generate rules from frequent itemsets
- Prune by min_confidence
- Rank by lift to find most interesting rules

---

## Ch7 — Classification

### Decision Trees

```
Entropy:   H(S) = -sum(pi * log2(pi))     (0 = pure, 1 = max impurity for 2 classes)
Info Gain: IG(S,A) = H(S) - sum(|Sv|/|S| * H(Sv))   for each split value v
GainRatio: IG / SplitInfo    (penalizes attributes with many values)

Gini:      Gini(S) = 1 - sum(pi^2)
Split:     choose attribute/value minimizing weighted Gini of children
```

### k-Nearest Neighbors (k-NN)

```
1. Normalize all features (min-max or z-score)
2. For test object: compute Euclidean distance to all training objects
3. Find k nearest neighbors
4. Predict: majority class among k neighbors
```
- Larger k: smoother boundary, less overfitting, but may underfit
- k=1: exact fit to training, prone to overfitting
- No training phase (lazy learner)

### Naive Bayes

```
P(C|X) proportional to P(C) * product(P(xi|C))

Numeric features: Gaussian NB
  P(x|C) = (1 / (sigma * sqrt(2*pi))) * exp(-0.5 * ((x - mu) / sigma)^2)

Categorical features: frequency table
  P(xi=v|C) = count(xi=v in class C) / count(class C)

Laplace smoothing: add 1 to counts to avoid zero probabilities
  P(xi=v|C) = (count + 1) / (total + k)  where k = number of distinct values
```

### Evaluation Metrics

```
Confusion Matrix:
              Predicted +    Predicted -
Actual +         TP              FN
Actual -         FP              TN

Accuracy  = (TP + TN) / (TP + TN + FP + FN)
Precision = TP / (TP + FP)      -- "of predicted positive, how many actually positive?"
Recall    = TP / (TP + FN)      -- "of actual positive, how many did we catch?"
F1        = 2 * Precision * Recall / (Precision + Recall)
```

### k-Fold Cross-Validation
```
1. Split dataset into k equal folds
2. For i = 1 to k:
     train on all folds except fold i
     test on fold i
     record accuracy
3. Final accuracy = average of k accuracies
```
- Reduces variance of evaluation estimate
- k=10 is standard; k=n is leave-one-out (LOO-CV)

---

## "When to Use What" — Decision Guide

| Task / Situation                          | Recommended Method              | Key Parameter(s)          |
|-------------------------------------------|---------------------------------|---------------------------|
| Explore distribution of one variable      | Histogram, boxplot              | Bin width                 |
| Find outliers                             | Boxplot (IQR rule)              | 1.5*IQR threshold         |
| Measure linear relationship               | Pearson r                       | —                         |
| Measure monotone (non-linear) relationship| Spearman rho                    | —                         |
| Visualize all pairwise relationships      | Scatter matrix                  | —                         |
| Compare multivariate profiles             | Parallel coordinates / radar    | —                         |
| Handle missing numeric values             | Fill with mean or per-class mean| Class label available?    |
| Handle missing nominal values             | Fill with mode                  | —                         |
| Scale before distance-based methods       | Min-max normalization           | New range [0,1]           |
| Scale for statistical methods             | Z-score normalization           | —                         |
| Cluster: known K, spherical clusters      | K-means                         | K, max_iter               |
| Cluster: unknown K, hierarchical view     | Hierarchical (Ward linkage)     | Linkage type              |
| Cluster: arbitrary shapes, with noise     | DBSCAN                          | Eps, MinPts               |
| Find item co-occurrence rules             | Apriori or FP-growth            | min_support, min_confidence|
| Dense transactions, long patterns         | FP-growth (faster)              | min_support               |
| Classify: interpretable model             | Decision Tree (ID3/C4.5)        | max_depth, min_samples    |
| Classify: no training time needed         | k-NN                            | k, distance metric        |
| Classify: fast, works with small data     | Naive Bayes                     | Laplace smoothing         |
| Evaluate classifier robustly              | k-Fold Cross-Validation         | k (usually 10)            |
| Imbalanced classes: measure performance   | Precision, Recall, F1 (not accuracy) | —                    |
| Attribute selection for decision tree     | Information Gain / Gain Ratio   | Threshold                 |

---

*End of Super-Summary*
