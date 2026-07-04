# Project 06-03-01: Itemsets and Association Rules

## Overview
This project implements the core concepts of frequent pattern mining from scratch:
support counting, frequent itemset discovery using the Apriori algorithm, and
association rule generation with support, confidence, and lift metrics.

## Concepts Covered
- **Itemsets**: sets of items found together in transactions
- **Support**: how frequently an itemset appears (absolute and relative)
- **Frequent Itemsets**: itemsets whose support exceeds a minimum threshold
- **Apriori Property**: if X is infrequent, all supersets of X are infrequent (pruning)
- **Association Rules**: X -> Y relationships mined from frequent itemsets
- **Confidence**: P(Y | X) = how reliably Y follows X
- **Lift**: Confidence / Support(Y) — >1 means positive correlation

## Dataset
The Friends Cuisine dataset: 10 transactions with items from {Indian, Mediterranean,
Oriental, Arabic, FastFood}. Used with min_support=3, min_confidence=0.5.

## Files
- `association_rules.py` — complete from-scratch implementation
- `project_README.md` — this file

## How to Run
```
python association_rules.py
```
No external libraries required. Pure Python standard library.

## Expected Output
- All frequent itemsets with their support counts
- All association rules sorted by lift (highest first)
- Summary statistics

## Key Formulas
```
Support(X)         = count(X in transactions) / total_transactions
Confidence(X -> Y) = Support(X union Y) / Support(X)
Lift(X -> Y)       = Confidence(X -> Y) / Support(Y)
```
