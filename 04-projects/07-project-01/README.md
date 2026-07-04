# Project 07-03-01: Decision Trees

## Overview
This project implements a decision tree classifier from scratch in Python
and demonstrates it using the rpart package in R. The implementation covers
all three split criteria: Information Gain (entropy), Gain Ratio, and Gini Impurity.

## Concepts Covered
- **Entropy**: H(S) = -sum p_i * log2(p_i)
- **Information Gain**: IG(S,A) = H(S) - weighted sum of H(S_v)
- **Gain Ratio**: IG / SplitInfo (fixes IG bias toward high-cardinality attributes)
- **Gini Impurity**: 1 - sum p_i^2 (used by CART / sklearn)
- **Top-down greedy tree construction** (ID3-style)
- **Prediction**: traverse tree from root to leaf

## Datasets
- **Friends Food dataset**: 9 examples, predict Company (good/bad) from Food and Distance
- **Iris dataset** (R only): classic multi-class classification benchmark

## Files
- `decision_tree.py` — complete from-scratch decision tree implementation
- `decision_tree.R` — R implementation with rpart
- `project_README.md` — this file

## How to Run

### Python
```
python decision_tree.py
```
No external libraries required.

### R
```R
install.packages("rpart")
install.packages("rpart.plot")  # optional
source("decision_tree.R")
```

## Key Formulas
```
Entropy:    H(S) = -sum p_i * log2(p_i)
Info Gain:  IG(S,A) = H(S) - sum_v (|S_v|/|S|) * H(S_v)
Gini:       Gini(S) = 1 - sum p_i^2
```
