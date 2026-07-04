# Chapter 7: Classification

## 1. Supervised Learning

- **Goal**: learn a function f: X -> Y from labeled training examples, then predict Y for new X
- **Training set**: labeled data used to build the model
- **Test set**: held-out data used to evaluate model performance (NEVER used during training)
- **Class label**: the target variable Y (categorical)

```
Training data -> Model Building -> Model
New object    -> Model          -> Predicted Class
```

---

## 2. Decision Trees

### Structure
- **Internal node**: tests one attribute
- **Branch**: one outcome of the test (e.g., "yes" or "no", or a specific value)
- **Leaf node**: class label prediction
- Trees are built top-down, greedily (ID3, C4.5, CART algorithms)

### Key Impurity Measures

#### Entropy (used by ID3, C4.5)
```
H(S) = -sum over classes i: p_i * log2(p_i)
```
- p_i = fraction of examples in class i
- H(S) = 0 means all examples have the same class (pure)
- H(S) = 1 means equal split between 2 classes (maximum impurity for binary)
- Convention: 0 * log2(0) = 0

#### Information Gain
```
IG(S, A) = H(S) - sum over values v of A: (|S_v| / |S|) * H(S_v)
```
- S_v = subset of S where attribute A has value v
- Choose the attribute A that maximizes IG(S, A)
- Bias: favors attributes with many distinct values

#### Gain Ratio (C4.5 improvement)
```
SplitInfo(S, A) = -sum over values v: (|S_v| / |S|) * log2(|S_v| / |S|)
GR(S, A) = IG(S, A) / SplitInfo(S, A)
```
- Normalizes IG by how much the split itself spreads the data
- Avoids bias toward high-cardinality attributes

#### Gini Impurity (used by CART)
```
Gini(S) = 1 - sum over classes i: p_i^2
Gini_split(S, A) = sum over values v: (|S_v| / |S|) * Gini(S_v)
```
- Gini = 0 means pure, Gini = 0.5 means maximum impurity for 2 classes
- Choose attribute A that minimizes Gini_split(S, A)

### Algorithm Pseudocode (ID3-style)

```
BuildTree(S, attributes):
  if all examples in S have the same class c:
    return Leaf(c)
  if attributes is empty:
    return Leaf(majority class in S)
  if |S| < min_samples_split:
    return Leaf(majority class in S)

  best_attr = argmax over A in attributes: IG(S, A)
  node = InternalNode(best_attr)
  for each value v of best_attr:
    S_v = {examples in S where best_attr = v}
    if S_v is empty:
      node.add_branch(v, Leaf(majority class in S))
    else:
      node.add_branch(v, BuildTree(S_v, attributes - {best_attr}))
  return node
```

### Worked Example

Dataset (Friends Food classifier):
```
Food      Age  Distance   Company
chinese   51   close      good
italian   43   very_close good
italian   82   close      good
burgers   23   far        bad
chinese   46   very_far   good
chinese   29   too_far    bad
burgers   42   very_far   good
chinese   38   close      bad
italian   31   far        good
```

Target: Company (good/bad)  |  9 examples: 6 good, 3 bad

Step 1 - Overall entropy:
  p_good = 6/9 = 0.667,  p_bad = 3/9 = 0.333
  H(S) = -(0.667)*log2(0.667) - (0.333)*log2(0.333)
       = -(0.667)*(-0.585) - (0.333)*(-1.585)
       = 0.390 + 0.528 = 0.918

Step 2 - IG for "Food":
  chinese (4): 2 good, 2 bad  -> H = 1.0
  italian (3): 3 good, 0 bad  -> H = 0.0
  burgers (2): 1 good, 1 bad  -> H = 1.0
  IG(S, Food) = 0.918 - (4/9)*1.0 - (3/9)*0.0 - (2/9)*1.0
              = 0.918 - 0.444 - 0 - 0.222 = 0.252

Step 3 - IG for "Distance":
  close (3):     2 good, 1 bad  -> H = 0.918
  very_close(1): 1 good, 0 bad  -> H = 0.0
  far (2):       1 good, 1 bad  -> H = 1.0
  very_far (2):  2 good, 0 bad  -> H = 0.0
  too_far (1):   0 good, 1 bad  -> H = 0.0
  IG(S, Distance) = 0.918 - (3/9)*0.918 - (1/9)*0 - (2/9)*1 - (2/9)*0 - (1/9)*0
                  = 0.918 - 0.306 - 0.222 = 0.390

Distance (IG=0.390) > Food (IG=0.252) -> split on Distance first.

### Stopping Conditions
1. All examples in a node have the same class -> leaf
2. No more attributes to split on -> leaf with majority class
3. Node has fewer than min_samples examples -> leaf with majority class

### Overfitting and Pruning
- Deep trees overfit training data
- **Pre-pruning**: stop early (min_samples, max_depth parameters)
- **Post-pruning**: grow full tree, then prune branches that do not improve validation accuracy

---

## 3. k-Nearest Neighbor (k-NN)

### Algorithm Steps
```
For a new point x:
  1. Compute distance from x to every training point
  2. Select the k training points with the smallest distance
  3. Predict the most common class among those k neighbors (majority vote)
  4. In case of tie: use lower k, or pick randomly
```

### Distance Metrics
```
Euclidean: d(a,b) = sqrt( sum_i (a_i - b_i)^2 )
Manhattan: d(a,b) = sum_i |a_i - b_i|
```

### Choosing k
| k value | Effect |
|---------|--------|
| k = 1 | Very sensitive to noise, complex decision boundary |
| k = 3..5 | Common default, balanced |
| Large k | Smoother boundary, may underfit |

### Feature Normalization (Required Before k-NN)
Without normalization, features with large scales dominate the distance.
- **Min-Max**: x_norm = (x - x_min) / (x_max - x_min)  -> range [0, 1]
- **Z-score**: x_norm = (x - mean) / std_dev            -> mean 0, std 1

### Pros and Cons
| Pro | Con |
|-----|-----|
| Simple, no training phase | Slow prediction O(n) per query |
| Naturally handles multi-class | Sensitive to irrelevant features |
| Non-parametric | Needs feature normalization |

---

## 4. Naive Bayes

### Bayes' Theorem
```
P(C | X) = P(X | C) * P(C) / P(X)
```
- P(C) = prior probability of class C
- P(X | C) = likelihood: probability of seeing features X given class C
- P(X) = constant for all classes (can be ignored for classification)
- P(C | X) = posterior: probability of class C given observed features X

### Naive Independence Assumption
```
P(X | C) = P(x1 | C) * P(x2 | C) * ... * P(xn | C)
```
Each feature is assumed to be conditionally independent given the class.

### Classification Rule
```
Predict C* = argmax over C:  P(C) * P(x1|C) * P(x2|C) * ... * P(xn|C)
```

### Parameter Estimation
```
P(C)        = count(C) / n_total
P(x_j | C) = count(x_j in class C) / count(C)
```

### Laplace Smoothing
Problem: if a (value, class) pair was never seen, P(x_j | C) = 0 -> zeroes the whole product.
Solution: add 1 to every count:
```
P(x_j | C) = (count(x_j, C) + 1) / (count(C) + |domain(x_j)|)
```
where |domain(x_j)| = number of distinct values that feature x_j can take.

### Example Calculation
Friends dataset, predict Company for: Food=chinese, Distance=close
  P(good) = 6/9,  P(bad) = 3/9
  P(Food=chinese | good) = 2/6 = 0.333
  P(Food=chinese | bad)  = 2/3 = 0.667
  P(Dist=close   | good) = 2/6 = 0.333
  P(Dist=close   | bad)  = 1/3 = 0.333

  Score(good) ~ (6/9) * (2/6) * (2/6) = 0.667 * 0.333 * 0.333 = 0.074
  Score(bad)  ~ (3/9) * (2/3) * (1/3) = 0.333 * 0.667 * 0.333 = 0.074
  Tie -> predict good (or random)

---

## 5. Model Evaluation

### Confusion Matrix (Binary Classification)

```
                   Predicted Positive    Predicted Negative
Actual Positive         TP (True Pos)         FN (False Neg)
Actual Negative         FP (False Pos)        TN (True Neg)
```

- TP: correctly predicted positive
- TN: correctly predicted negative
- FP: predicted positive but actually negative (Type I error)
- FN: predicted negative but actually positive (Type II error)

### Metric Formulas
```
Accuracy    = (TP + TN) / (TP + TN + FP + FN)
Precision   = TP / (TP + FP)     <- of predicted positives, how many are correct?
Recall      = TP / (TP + FN)     <- of actual positives, how many did we catch?
F1 Score    = 2 * Precision * Recall / (Precision + Recall)
Specificity = TN / (TN + FP)     <- true negative rate
```

### k-Fold Cross-Validation

```
Algorithm:
  1. Split dataset D into k equal-sized folds (F1, F2, ..., Fk)
  2. For i = 1 to k:
       Train on (F1, ..., Fk) minus Fi
       Evaluate on Fi
       Record accuracy_i
  3. Final accuracy = mean(accuracy_1, ..., accuracy_k)
  4. Standard deviation shows stability
```
- Common choices: k=5 (fast) or k=10 (more reliable)
- More reliable than a single train/test split
- **Stratified k-fold**: ensures each fold preserves class proportions

---

## 6. Algorithm Comparison

| Aspect | Decision Tree | k-NN | Naive Bayes |
|--------|--------------|------|-------------|
| Training | Build tree once | Store all data | Compute counts |
| Prediction | Traverse tree O(depth) | Search k neighbors O(n) | Multiply probs O(features) |
| Interpretable | Yes | No | Partially |
| Handles missing values | Yes (skip split) | Hard | Can skip feature |
| Handles irrelevant features | Yes (won't split on them) | No (hurts distance) | Partially |
| Assumption | None (greedy splits) | Smooth decision boundary | Feature independence |
| Best for | Mixed feature types | Small datasets | Text classification |

---

## 7. Friends Dataset Reference

```
Food      Age  Distance    Company
chinese   51   close       good
italian   43   very_close  good
italian   82   close       good
burgers   23   far         bad
chinese   46   very_far    good
chinese   29   too_far     bad
burgers   42   very_far    good
chinese   38   close       bad
italian   31   far         good
```

Features: Food (chinese/italian/burgers), Age (numeric), Distance (close/very_close/far/very_far/too_far)
Target: Company (good/bad)   |   9 examples   |   6 good, 3 bad

---

## 8. Summary of All Formulas

```
---- Decision Trees ----
Entropy:     H(S) = -sum_i p_i * log2(p_i)
Info Gain:   IG(S,A) = H(S) - sum_v (|S_v|/|S|) * H(S_v)
Split Info:  SplitInfo(S,A) = -sum_v (|S_v|/|S|) * log2(|S_v|/|S|)
Gain Ratio:  GR(S,A) = IG(S,A) / SplitInfo(S,A)
Gini:        Gini(S) = 1 - sum_i p_i^2
Gini Split:  Gini_split(S,A) = sum_v (|S_v|/|S|) * Gini(S_v)

---- k-NN ----
Euclidean:   d(a,b) = sqrt(sum_i (a_i - b_i)^2)
Min-Max:     x_norm = (x - x_min) / (x_max - x_min)

---- Naive Bayes ----
Bayes:       P(C|X) proportional to P(C) * prod_j P(x_j|C)
Laplace:     P(x_j|C) = (count(x_j,C) + 1) / (count(C) + |values_j|)

---- Evaluation ----
Accuracy:    (TP+TN) / total
Precision:   TP / (TP+FP)
Recall:      TP / (TP+FN)
F1:          2 * P * R / (P + R)
```
