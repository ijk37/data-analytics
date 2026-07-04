# Project 06: Retail Sales Analytics

**Subtitle:** Chapters combined: Ch1 + Ch2 + Ch3 + Ch4 + Ch5 + Ch6 + Ch7

---

## What This Project Does

A retail company has collected three months of customer sales data. This project applies the
complete data analytics pipeline to answer four business questions:

1. **Who are our customers?** (Descriptive analytics — Ch1, Ch2)
2. **What patterns do they exhibit?** (Pattern mining — Ch6)
3. **Can we group them into segments?** (Clustering — Ch5)
4. **Who is likely to churn?** (Classification — Ch7)

The project intentionally touches every major technique taught in the course so you can see how
they connect in a single, coherent business scenario.

---

## Dataset Description

**30 customer records** (hardcoded — no external file needed for the Python version; an inline
CSV is written at runtime for the R version).

| Column | Type | Description |
|---|---|---|
| CustomerID | Nominal | Unique identifier (C01–C30) |
| Age | Ratio/Continuous | Customer age in years |
| Gender | Nominal/Binary | M or F |
| Purchases | Ratio/Discrete | Number of purchases in 3 months |
| AvgSpend | Ratio/Continuous | Average spend per purchase (USD) |
| Returns | Ratio/Discrete | Number of items returned |
| Months_Active | Ratio/Discrete | How many of the 3 months they shopped |
| Category1 | Nominal/Binary | Bought Electronics (1/0) |
| Category2 | Nominal/Binary | Bought Clothing (1/0) |
| Category3 | Nominal/Binary | Bought Food (1/0) |
| Category4 | Nominal/Binary | Bought Books (1/0) |
| Churned | Nominal/Binary | Did the customer stop buying? (Yes/No) |

**Class balance:** ~10 churners out of 30 customers (~33%).

---

## How to Run

### Python
```
python retail_analytics.py
```
Requires only Python standard library (csv, math, collections, random). No pip installs needed.

### R
```
Rscript retail_analytics.R
```
Requires: `arules` (install.packages("arules")), `e1071` (install.packages("e1071")),
`class` (install.packages("class")).

---

## What to Look For in Output

| Phase | Key question |
|---|---|
| Phase 1 | Do churned vs non-churned customers differ in purchases and spend? |
| Phase 2 | Which features are correlated? Is AvgSpend negatively correlated with Purchases? |
| Phase 3 | Are there outliers in AvgSpend that might need log-transformation? |
| Phase 4 | Which category combinations appear most frequently? Do single-category buyers churn more? |
| Phase 5 | Does K-means separate high-spend/low-frequency vs low-spend/high-frequency segments? |
| Phase 6 | Which classifier achieves higher recall on churners? (Recall matters most — missing a churner costs more than a false alarm.) |

---

## Learning Objectives

After working through this project you should be able to:
- Explain why recall is more important than precision for churn prediction.
- Describe what an association rule means in a retail context.
- Interpret K-means cluster centroids as customer personas.
- Explain why log-transforming AvgSpend before clustering/classification helps.
