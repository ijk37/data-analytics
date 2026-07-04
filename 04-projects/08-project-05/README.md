# Project 05: Student Performance Predictor

## Overview

A school wants to:
1. **Predict** which students will fail before the term ends.
2. **Cluster** students by performance profile to group them for intervention.
3. **Understand** which subject-grade combinations co-occur in weak students.

This capstone project combines techniques from every chapter (Ch1–Ch7) on a
25-student dataset with real-world school-report variables.

## Chapters Combined

| Phase | Chapter | Technique |
|-------|---------|-----------|
| 1 | Ch 1 | Attribute type identification |
| 2 | Ch 2 | Descriptive statistics (per-class means, std, group differences) |
| 3 | Ch 4 | Preprocessing: outlier detection, discretisation, normalisation |
| 4 | Ch 3 | Multivariate: Pearson correlation matrix, top correlations |
| 5 | Ch 6 | Frequent pattern mining: Apriori on grade-label transactions |
| 6 | Ch 5 | Clustering: K-means K=3, cluster profiling, labelling |
| 7 | Ch 7 | Classification: k-NN + Naive Bayes, confusion matrix, accuracy |

## Dataset

**Student Performance** — 25 students, hardcoded.

| Attribute | Type | Scale |
|-----------|------|-------|
| Math | Score 0-100 | Ratio, Continuous |
| Science | Score 0-100 | Ratio, Continuous |
| English | Score 0-100 | Ratio, Continuous |
| History | Score 0-100 | Ratio, Continuous |
| StudyHours | Hours/week | Ratio, Continuous |
| Absences | Days absent | Ratio, Continuous |
| Result | Pass/Fail | Nominal, Discrete |

## Files

| File | Description |
|------|-------------|
| `student_analysis.py` | Pure-stdlib Python, 8-section structure, 7 phases |
| `student_analysis.R`  | Base R + optional arules/class/e1071, 7 matching phases |
| `project_README.md`   | This file |

## How to Run

### Python

```bash
# No external libraries required — pure Python standard library
python student_analysis.py
```

### R

```r
# Base R covers most phases.
# Optional packages: arules, class, e1071
# Install with: install.packages(c("arules", "class", "e1071"))
Rscript student_analysis.R
# or inside RStudio: source("student_analysis.R")
```

## Expected Output Highlights (Python)

```
=== PHASE 1 (Ch1): ATTRIBUTE TYPE IDENTIFICATION ===
  Attribute    Scale      Discrete/Continuous
  Math         Ratio      Continuous
  ...

=== PHASE 2 (Ch2): DESCRIPTIVE STATISTICS ===
  Per-class means (Pass vs Fail):
  Attribute       Pass_mean   Fail_mean   Abs_diff
  Math            79.73       38.78       40.95  <-- largest gap
  ...

=== PHASE 3 (Ch4): PREPROCESSING ===
  IQR outlier detection (Absences): ...
  Grade discretisation: ...
  Min-max normalisation applied.

=== PHASE 4 (Ch3): MULTIVARIATE ANALYSIS ===
  Correlation matrix (6x6): ...
  Top correlations: ...

=== PHASE 5 (Ch6): FREQUENT PATTERN MINING ===
  Rules predicting Fail_grade:
  [Science_Fail_grade] => [Math_Fail_grade]  conf=1.000

=== PHASE 6 (Ch5): CLUSTERING ===
  Cluster 0 -- "High Achievers"  (Pass dominant)
  Cluster 1 -- "At Risk"         (Fail dominant)
  Cluster 2 -- "Average Students"

=== PHASE 7 (Ch7): CLASSIFICATION ===
  k-NN Accuracy : ...
  NB  Accuracy  : ...
  Recommendation: ...
```

## Learning Objectives

1. Identify and justify attribute scale types (Ch1)
2. Compare groups statistically to find the most predictive features (Ch2)
3. Detect outliers with IQR, discretise scores, and normalise data (Ch4)
4. Read a correlation matrix and identify redundant features (Ch3)
5. Mine association rules that reveal failure co-occurrence patterns (Ch6)
6. Cluster students and assign interpretable cluster labels (Ch5)
7. Build, compare, and select classifiers for an early-warning system (Ch7)
