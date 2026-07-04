# Project 06-03-03: Pattern Mining with mlxtend / arules

## Overview
This project uses real data mining libraries to perform frequent pattern mining:
`mlxtend` in Python and `arules` in R. When libraries are not available, the
Python script falls back to the from-scratch Apriori from Project 01. A larger
synthetic grocery dataset is also generated to demonstrate scalability.

## Concepts Covered
- Using `TransactionEncoder` to convert transaction lists to binary matrices
- `mlxtend.frequent_patterns.apriori` for frequent itemset mining
- `mlxtend.frequent_patterns.association_rules` for rule generation
- R `arules` package: `transactions()`, `apriori()`, `inspect()`, `sort()`
- Visualization with `arulesViz` (if available)

## Files
- `pattern_mining.py` — Python implementation with mlxtend (or fallback)
- `pattern_mining.R` — R implementation with arules
- `project_README.md` — this file

## How to Run

### Python
```
pip install mlxtend pandas
python pattern_mining.py
```
If mlxtend is not installed, the script automatically falls back to
the from-scratch Apriori implementation.

### R
```R
install.packages("arules")
install.packages("arulesViz")   # optional, for visualization
source("pattern_mining.R")
```

## Datasets
1. **Friends Cuisine** (10 transactions) — used in all examples
2. **Synthetic Grocery** (50 transactions) — randomly generated to show scalability
