# Project 07-03-02: k-NN and Naive Bayes

## Overview

This project implements two classification algorithms from scratch:
- **k-Nearest Neighbor (k-NN)**: distance-based, non-parametric classifier
- **Naive Bayes**: probabilistic classifier using Bayes' theorem with the naive independence assumption

Both are applied to the Friends classification dataset and compared.

## Concepts Covered

- Euclidean distance computation for numeric features
- Min-Max normalization (required before k-NN)
- Majority vote among k nearest neighbors
- Bayes' theorem: P(C|X) proportional to P(C) * P(X|C)
- Naive independence assumption: P(X|C) = product of P(x_i|C)
- Laplace smoothing to handle zero-count problem
- Step-by-step posterior probability calculation

## Files

| File | Description |
|------|-------------|
| `knn_naive_bayes.py` | Python implementation (pure stdlib) |
| `knn_naive_bayes.R` | R implementation using class and e1071 packages |

## Dataset

Friends classification dataset (9 training examples):

```
Food     Age  Distance    Company (target)
chinese  51   close       good
italian  43   very_close  good
italian  82   close       good
burgers  23   far         bad
chinese  46   very_far    good
chinese  29   too_far     bad
burgers  42   very_far    good
chinese  38   close       bad
italian  31   far         good
```

## How to Run

### Python
```bash
python knn_naive_bayes.py
```

Requirements: Python 3.6+ with standard library only (no external packages).

### R
```r
source("knn_naive_bayes.R")
```

Required packages: `class`, `e1071`  
Install with: `install.packages(c("class", "e1071"))`

## Expected Output

- k-NN predictions for 2 test objects with k=1, 3, 5
- Normalized feature values shown
- Naive Bayes step-by-step posterior calculation for one test object
- Final predictions from both classifiers
