# Project 03: Normalization, Distance & Sampling

**Chapter 4 — Data Quality and Preprocessing**

---

## What This Project Does

This project demonstrates how to prepare numeric data for analysis and how to sample datasets correctly:

1. **Min-Max Normalization** — rescale values to [0, 1] or any target range
2. **Z-Score Standardization** — center at zero, scale by standard deviation
3. **Euclidean Distance** — compute straight-line distance in n-dimensional space
4. **Distance Matrix** — compute all pairwise distances in a dataset
5. **Simple Random Sampling** — with and without replacement
6. **Stratified Sampling** — sample proportionally from each class

The demo **explicitly solves Exercise Q4 and Q5** from the Chapter 4 exercise sheet and prints Expected vs. Computed comparisons.

---

## Concepts Covered

| Technique | Use Case | Section in Notes |
|---|---|---|
| Min-max normalization | Scale to [0, 1]; bounded input (neural nets) | 6.1 |
| Z-score standardization | Center + scale; Gaussian-assumption algorithms | 6.2 |
| Euclidean distance | Measure similarity between two data points | 7 |
| Distance matrix | All pairwise distances in a dataset | 7 |
| Simple random sampling | Select a representative subset randomly | 3.1-3.3 |
| Stratified sampling | Ensure all classes are represented in sample | 3.4 |

---

## Files

| File | Language | Description |
|---|---|---|
| `normalization_distance.py` | Python 3 | Full implementation, pure stdlib |
| `normalization_distance.R` | R | Same operations using base R |

---

## Usage

### Python

```
python normalization_distance.py
```

### R

```
Rscript normalization_distance.R
```

---

## Exercise Q&A Solved in This Project

### Q4: Min-Max Normalize [31,38,42,29,46,23,83,43,51,55,27,35] to [0,1]

Formula: v' = (v - 23) / (83 - 23) = (v - 23) / 60

| v  | v' (Expected) | v' (Computed) |
|----|---------------|---------------|
| 31 | 0.133         | 0.133         |
| 38 | 0.250         | 0.250         |
| 42 | 0.317         | 0.317         |
| 29 | 0.100         | 0.100         |
| 46 | 0.383         | 0.383         |
| 23 | 0.000         | 0.000         |
| 83 | 1.000         | 1.000         |
| 43 | 0.333         | 0.333         |
| 51 | 0.467         | 0.467         |
| 55 | 0.533         | 0.533         |
| 27 | 0.067         | 0.067         |
| 35 | 0.200         | 0.200         |

### Q5: Euclidean Distance between x=(1,3,-2,5) and y=(2,4,1,6)

```
differences: -1, -1, -3, -1
squares:      1,  1,  9,  1
sum:         12
distance:    sqrt(12) ~= 3.464
```

**Expected: 3.464   Computed: 3.464**

---

## The Scale Problem Demonstration

When attributes have different units, the one with the larger numeric range dominates distance calculations.

**Example (from lecture — Bernhard, Gwyneth, James):**

| Person   | Age (years) | Age (decades) |
|----------|-------------|---------------|
| Bernhard | 43          | 4.3           |
| Gwyneth  | 38          | 3.8           |
| James    | 42          | 4.2           |

Computing Euclidean distance in years vs. decades gives different relative rankings — even though the data is identical. The solution is to normalize first.

---

## Excel How-To

### Min-Max Normalization

Suppose your data is in A2:A13. To normalize to [0, 1]:

```
B2: =(A2-MIN($A$2:$A$13))/(MAX($A$2:$A$13)-MIN($A$2:$A$13))
```

Copy down to B13.

**To normalize to a different range [new_min, new_max]**, say [0, 100]:
```
B2: =(A2-MIN($A$2:$A$13))/(MAX($A$2:$A$13)-MIN($A$2:$A$13)) * (100 - 0) + 0
```

### Z-Score (Standardization)

```
C2: =(A2-AVERAGE($A$2:$A$13))/STDEV($A$2:$A$13)
```

Copy down to C13.

Note: Excel's STDEV uses sample standard deviation (divides by n-1). For population std dev use STDEVP.

### Euclidean Distance Between Two Rows

Suppose point x is in row 2 (A2:D2) and point y is in row 3 (A3:D3):

```
=SQRT(SUMPRODUCT((A2:D2 - A3:D3)^2))
```

This works as an array formula — SUMPRODUCT handles the element-wise squaring automatically.

### Stratified Sampling

Excel does not have a built-in stratified sample function. The standard approach:
1. Sort your data by the class/group column
2. Use RAND() to add a random column within each group
3. Sort by group first, then by RAND() within each group
4. Take the top N rows from each group
