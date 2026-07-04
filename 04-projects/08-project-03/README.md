# Project 03 — Predictive Analytics: Full Classification Study

## Overview

Compare three classifiers on the same dataset using proper evaluation. The same
preprocessing, train/test split, and metrics are applied to each classifier so
results are directly comparable.

## Chapters Combined

| Phase | Chapter | Topic                                          |
|-------|---------|------------------------------------------------|
| 1     | Ch2/Ch3 | EDA: class distribution, per-class means, corr |
| 2     | Ch4     | Gender encoding, min-max normalization, split   |
| 3     | Ch7     | Majority-class baseline, k-NN (k=3), Naive Bayes|
| 4     | Ch7     | Confusion matrix, accuracy, precision, recall, F1|

## Dataset

Extended FRIENDS dataset: 20 objects.
- Features: Max_temp, Weight, Height, Years, Gender (M/F)
- Target: Company (Good / Bad)
- Train: first 14 rows, Test: last 6 rows

## How to Run

### Python
```
python classification_study.py
```
No external libraries required. Pure Python stdlib only.

### R
```
Rscript classification_study.R
```
Requires: class, e1071 (install.packages(c("class","e1071")))
Optional: caret (install.packages("caret"))

## Expected Output (Python)

```
PHASE 1 -- EDA
Class distribution:
  Good: 10 (50.0%)
  Bad:  10 (50.0%)

Per-class feature means:
             Max_temp  Weight  Height   Years
Good         21.7      84.0    178.3    10.9
Bad          15.2      68.4    170.9    2.3

Correlation matrix:
             Max_temp  Weight  Height  Years
Max_temp     1.000     0.404   0.329   0.659
...

PHASE 2 -- PREPROCESSING
Gender encoded: M=1, F=0
Normalized to [0,1].
Train: 14 rows, Test: 6 rows

PHASE 3 -- CLASSIFIERS
[Baseline] Always predicts: Good
[k-NN k=3] Predictions: Good, Good, Bad, Bad, Good, Bad
[Naive Bayes] Predictions: Good, Good, Bad, Bad, Good, Bad

PHASE 4 -- EVALUATION
Classifier    Accuracy  Precision  Recall    F1
Baseline      0.500     0.333      0.500     0.400
k-NN (k=3)    0.833     0.833      1.000     0.909
Naive Bayes   1.000     1.000      1.000     1.000

Verdict: Naive Bayes performed best...
```

## File Structure

```
08-03-project-03/
    project_README.md          -- this file
    classification_study.py    -- Python implementation (pure stdlib)
    classification_study.R     -- R implementation
```
