# Project 03: Hierarchical and Density-Based Clustering

## Overview

This project implements two clustering families that go beyond K-means:

1. **Hierarchical Clustering (Agglomerative):** Builds a nested tree of clusters bottom-up,
   supporting all four linkage methods: MIN (single), MAX (complete), Group Average, and Ward's.
2. **DBSCAN:** Density-Based Spatial Clustering that finds arbitrarily shaped clusters and
   explicitly labels noise points.

Both algorithms are implemented from scratch in Python, and the R version uses
built-in/library functions for comparison.

## Concepts Covered

### Hierarchical Clustering (Agglomerative)
- **Bottom-up approach:** Start with n singletons, merge until 1 cluster
- **Linkage methods:**
  - MIN (single linkage): distance = minimum pairwise distance
  - MAX (complete linkage): distance = maximum pairwise distance
  - Average linkage: average of all pairwise distances
  - Ward's method: minimize increase in SSE when merging
- **Dendrogram:** Tree diagram showing the merge sequence and distances

### DBSCAN
- **Core point:** Has at least MinPts neighbors within radius Eps
- **Border point:** Not core, but within Eps of a core point
- **Noise point:** Neither core nor border — labeled as -1
- **Density-reachability:** Chain of core points connecting two points

## Files

| File | Description |
|------|-------------|
| `hierarchical_dbscan.py` | Python implementation from scratch |
| `hierarchical_dbscan.R` | R implementation using hclust() and dbscan |
| `project_README.md` | This file |

## How to Run

**Python:**
```bash
python hierarchical_dbscan.py
```
No external libraries required. Uses Python standard library only.

**R:**
```r
source("hierarchical_dbscan.R")
```
Requires the `dbscan` package. Install it once with:
```r
install.packages("dbscan")
```

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

## Linkage Method Formulas

```
MIN (single):    d(A,B) = min_{a in A, b in B} dist(a,b)
MAX (complete):  d(A,B) = max_{a in A, b in B} dist(a,b)
Average:         d(A,B) = (1 / |A|*|B|) * sum_{a,b} dist(a,b)
Ward's:          delta_SSE = (|A|*|B|)/(|A|+|B|) * dist^2(centroid_A, centroid_B)
```

## DBSCAN Definitions

```
Core point:   |N_Eps(p)| >= MinPts  (including p itself)
Border point: not core, but within Eps of a core point
Noise point:  not core, not within Eps of any core point  -> label = -1
```

## Linkage Comparison

| Method | Shape | Noise | Notes |
|--------|-------|-------|-------|
| MIN | Non-elliptical | Very sensitive | Chaining effect |
| MAX | Globular | Less sensitive | Equal-diameter bias |
| Average | Moderate | Moderate | Balance |
| Ward | Globular | Less sensitive | Equal-size bias |

## Learning Goals

After completing this project you should be able to:
- Trace through agglomerative clustering step by step
- Explain why different linkage methods produce different cluster shapes
- Read a dendrogram and cut it to get K clusters
- Classify points as core, border, or noise in DBSCAN
- Choose appropriate Eps and MinPts for a dataset
