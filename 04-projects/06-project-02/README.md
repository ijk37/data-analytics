# Project 06-03-02: FP-Growth and Pattern Types

## Overview
This project implements the FP-Growth algorithm for efficient frequent pattern
mining without candidate generation. It also demonstrates maximal and closed
frequent itemsets as compact representations of the full frequent itemset space.

## Concepts Covered
- **FP-Tree**: compressed transaction representation as a prefix tree
- **Header Table**: links to all occurrences of each frequent item in the tree
- **FP-Growth**: recursive mining via conditional pattern bases and conditional FP-trees
- **Maximal Itemsets**: frequent itemsets with no frequent superset
- **Closed Itemsets**: frequent itemsets with no superset of equal support

## Dataset
The Friends Cuisine dataset: 10 transactions with items from {Indian, Mediterranean,
Oriental, Arabic, FastFood}. Used with min_support=3.

## Files
- `fp_growth.py` — complete FP-tree and FP-growth implementation
- `project_README.md` — this file

## How to Run
```
python fp_growth.py
```
No external libraries required. Pure Python standard library.

## Expected Output
- ASCII visualization of the FP-tree
- All frequent itemsets mined via FP-Growth
- Maximal frequent itemsets
- Closed frequent itemsets
- Comparison with Apriori results

## Key Concepts
```
Maximal   X is frequent but no superset of X is frequent
Closed    X is frequent but no superset of X has the same support

Maximal is a subset of Closed is a subset of All Frequent
```
