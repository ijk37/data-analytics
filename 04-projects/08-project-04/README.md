# Project 04: The Iris Complete Walkthrough

## Overview

This capstone project applies **every technique from every chapter** (Ch1–Ch7)
to the classic Iris dataset in a single end-to-end analysis.  It is the
"all chapters in one script" integration project that shows how the techniques
connect in a real data-analytics pipeline.

## Chapters Combined

| Phase | Chapter | Technique |
|-------|---------|-----------|
| 1 | Ch 1 | Dataset profiling, attribute scale types |
| 2 | Ch 2 | Univariate descriptive statistics |
| 3 | Ch 3 | Multivariate statistics, correlation, scatter |
| 4 | Ch 4 | Preprocessing: missing values, normalisation |
| 5 | Ch 5 | Clustering: K-means, elbow / SSE |
| 6 | Ch 6 | Frequent pattern mining: Apriori, association rules |
| 7 | Ch 7 | Classification: Naive Bayes + k-NN, evaluation metrics |

## Dataset

**Iris** — the canonical benchmark dataset in machine learning.

- 150 objects, 4 numeric attributes, 1 class attribute
- Attributes: SepalLength, SepalWidth, PetalLength, PetalWidth (all Ratio scale)
- Class: Species — setosa, versicolor, virginica (Nominal, 50 each)

The Python script uses a hardcoded 30-row representative sample (10 per
species) for speed.  The R script uses the full built-in `iris` dataset
(150 rows).

## Files

| File | Description |
|------|-------------|
| `iris_complete.py` | Pure-stdlib Python, 8-section structure, 7 analysis phases |
| `iris_complete.R`  | Base R + optional arules, 7 matching phases |
| `project_README.md` | This file |

## How to Run

### Python

```bash
# No external libraries required — pure standard library
python iris_complete.py
```

### R

```r
# Base R is sufficient for most phases.
# Phase 6 (arules) is optional — the script checks and skips if not installed.
# To install arules:  install.packages("arules")
Rscript iris_complete.R
# or inside RStudio: source("iris_complete.R")
```

## Expected Output (Python)

```
=== PHASE 1 (Ch1): DATASET PROFILING ===
  Attribute      Scale      Discrete/Continuous
  SepalLength    Ratio      Continuous
  ...

=== PHASE 2 (Ch2): UNIVARIATE STATISTICS ===
  SepalLength: min=4.40 max=7.60 mean=5.68 median=5.65 ...
  ...

=== PHASE 3 (Ch3): MULTIVARIATE STATISTICS ===
  Pearson Correlation Matrix (SL, SW, PL, PW):
  ...

=== PHASE 4 (Ch4): PREPROCESSING ===
  Injecting 2 missing values...
  ...

=== PHASE 5 (Ch5): CLUSTERING (K-MEANS) ===
  K=3 cluster assignments: ...
  Purity: ...

=== PHASE 6 (Ch6): FREQUENT PATTERN MINING ===
  Frequent itemsets (min_support=5):
  ...

=== PHASE 7 (Ch7): CLASSIFICATION + EVALUATION ===
  Naive Bayes predictions: ...
  k-NN (k=3) predictions: ...
  Comparison table: ...
```

## Learning Objectives

After completing this project you will be able to:

1. Identify attribute scale types and describe a dataset (Ch1)
2. Compute and interpret univariate statistics (Ch2)
3. Build and read a correlation matrix and ASCII scatter plot (Ch3)
4. Handle missing values and normalise data (Ch4)
5. Run K-means clustering and evaluate with SSE (Ch5)
6. Mine frequent itemsets and extract association rules (Ch6)
7. Train, evaluate, and compare two classifiers (Ch7)
