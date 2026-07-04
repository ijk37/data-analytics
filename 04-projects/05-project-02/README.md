# Project 02: K-Means Clustering

## Overview

This project implements K-means clustering from scratch in both Python and R.
It covers the core algorithm, SSE objective function, K-means++ initialization,
and the elbow method for choosing K.

The Friends dataset from the lecture is used throughout, and Exercise Q1 is
reproduced step-by-step to verify the algorithm matches the expected output.

## Concepts Covered

- **K-means algorithm:** Assignment step + update step, iterated to convergence
- **SSE (Sum of Squared Errors):** The objective function K-means minimizes
- **K-means++ initialization:** Probabilistic seeding to avoid bad starts
- **Elbow method:** Plotting SSE vs K to identify the optimal number of clusters
- **Feature normalization:** Z-score normalization for fair distance computation

## Files

| File | Description |
|------|-------------|
| `kmeans_clustering.py` | Python implementation from scratch |
| `kmeans_clustering.R` | R implementation using built-in kmeans() |
| `project_README.md` | This file |

## How to Run

**Python:**
```bash
python kmeans_clustering.py
```
No external libraries required. Uses Python standard library only.

**R:**
```r
source("kmeans_clustering.R")
```
Requires base R only (no packages).

## Friends Dataset

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

## Exercise Q1 (Verified)

**Setup:** 6-person subset (Andrew through Fred), K=2
**Initial centroids:** Andrew(55, 1) and Carolina(37, 5)

**Iteration 1:**

| Person | Dist to Andrew | Dist to Carolina | Assigned to |
|--------|---------------|-----------------|-------------|
| Andrew | 0.00 | ~18.44 | Cluster 1 |
| Bernhard | ~12.04 | ~6.71 | Cluster 2 |
| Carolina | ~18.44 | 0.00 | Cluster 2 |
| Dennis | ~27.02 | ~45.18 | Cluster 1 |
| Eve | ~32.58 | ~14.00 | Cluster 2 |
| Fred | ~9.85 | ~9.00 | Cluster 2 |

**New centroids:**
- Cluster 1 (Andrew, Dennis): mean age = (55+82)/2 = 68.5, mean edu = (1+3)/2 = 2.0 → (68.5, 2.0)
- Cluster 2 (Bernhard, Carolina, Eve, Fred): mean age = (43+37+23+46)/4 = 37.25, mean edu = (2+5+3.2+5)/4 = 3.8 → (37.25, 3.8)

## K-Means Algorithm Pseudocode

```
1. Choose K initial centroids
2. Repeat:
   a. Assign each point to nearest centroid
   b. Recompute each centroid as the mean of assigned points
3. Until centroids don't change
```

## SSE Formula

```
SSE = sum over clusters C_i:
        sum over points x in C_i:
          dist(centroid_i, x)^2
```

Lower SSE = tighter, more compact clusters.

## Learning Goals

After completing this project you should be able to:
- Implement K-means from scratch (no libraries)
- Trace through the algorithm step by step
- Compute SSE for a given assignment
- Explain why K-means++ is better than random initialization
- Use the elbow method to choose K
