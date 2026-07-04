# Project 02 — Market Basket & Customer Segmentation

## Overview

A small grocery store wants to understand purchase patterns and segment its customers.
This project mines association rules from shopping baskets and clusters customers by
demographics and spending behaviour.

## Chapters Combined

| Part | Chapter | Topic                                       |
|------|---------|---------------------------------------------|
| A    | Ch2/Ch3 | Descriptive statistics + correlation matrix |
| B    | Ch4     | Min-max normalization                       |
| C    | Ch6     | Apriori frequent itemset + association rules|
| D    | Ch5     | K-means customer segmentation (K=3)         |

## Dataset

20 synthetic grocery customers. Each customer has:
- Age, Visits (per month), Spend (monthly spend in $)
- Items: list of purchased product categories

## How to Run

### Python
```
python market_analysis.py
```
No external libraries required. Pure Python stdlib only.

### R
```
Rscript market_analysis.R
```
Requires: arules (install.packages("arules"))

## Expected Output (Python)

```
PART A -- DESCRIPTIVE STATISTICS
Column     Mean    Std     Min     Max
Age        37.90   11.77   19      61
Visits     9.75    5.64    1       22
Spend      283.25  130.97  30      480

PART A -- CORRELATION MATRIX
           Age       Visits    Spend
Age        1.000     0.057     0.135
Visits     0.057     1.000     0.951
Spend      0.135     0.951     1.000

PART A -- ASCII SCATTER (Age vs Spend)
...

PART B -- NORMALIZED (first 3 rows shown):
C01: Age=0.357, Visits=0.524, Spend=0.556

PART C -- FREQUENT ITEMSETS (min_support=5/20=0.25)
{bread}: support=12 (0.60)
{milk}: support=12 (0.60)
...
ASSOCIATION RULES (sorted by lift):
milk -> yogurt: support=7, confidence=0.583, lift=1.750
...

PART D -- CUSTOMER SEGMENTS (K=3)
Cluster 0 (Young Low-Spend): C02, C05, C11, C15, C19 ...
Cluster 1 (Regular Shoppers): C01, C07, C09, C13, C17 ...
Cluster 2 (Loyal High-Spend): C03, C06, C08, C12, C14, C18 ...
```

## File Structure

```
08-03-project-02/
    project_README.md      -- this file
    market_analysis.py     -- Python implementation (pure stdlib)
    market_analysis.R      -- R implementation
```
