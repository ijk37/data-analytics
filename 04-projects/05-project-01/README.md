# Project 01: Distance Measures

## Overview

This project implements and demonstrates all distance measures covered in Chapter 5
of the Data Analytics course. Understanding distance (or similarity) is foundational
to all clustering algorithms — they all depend on some notion of how "far apart" two
objects are.

## Concepts Covered

### Single-Attribute Distances
- **Quantitative distance:** |a - b| — for continuous numeric attributes like age or income
- **Ordinal distance:** |pos_a - pos_b| / (n-1) — for ranked attributes like education level
- **Nominal distance:** 0 if equal, 1 if different — for categorical attributes like color or country

### Multi-Attribute Distances (Minkowski Family)
- **Minkowski distance (general):** (sum |x_k - y_k|^r)^(1/r)
- **Manhattan distance (r=1):** Sum of absolute differences — useful for grid-like spaces
- **Euclidean distance (r=2):** Straight-line distance — most common in practice
- **Chebyshev distance (r=inf):** Maximum of absolute differences

### String/Sequence Distances
- **Hamming distance:** Number of positions that differ (equal-length strings/binary)
- **Edit (Levenshtein) distance:** Minimum insert/delete/substitute operations to convert one string to another

## Files

| File | Description |
|------|-------------|
| `distance_measures.py` | All distance functions with demos |
| `project_README.md` | This file |

## How to Run

```bash
python distance_measures.py
```

No external libraries required. Uses Python standard library only.

## Expected Output

The script will print:

1. Single-attribute distances for the Friends dataset (Andrew vs Carolina)
2. Minkowski distances for r = 1, 2, 3, and infinity
3. Hamming distance examples from the lecture
4. Edit distance example: "Johnny" vs "Jonston"
5. Full distance matrix for the 6-person Friends dataset

## Friends Dataset Used

```
Person    Age   Education
Andrew    55    1
Bernhard  43    2
Carolina  37    5
Dennis    82    3
Eve       23    3.2
Fred      46    5
```

## Key Formulas

```
Quantitative:  d(a,b) = |a - b|
Ordinal:       d(a,b) = |pos_a - pos_b| / (n - 1)
Nominal:       d(a,b) = 0 if a==b, else 1
Minkowski:     d(x,y) = (sum_k |x_k - y_k|^r)^(1/r)
Hamming:       d(s1,s2) = count of positions where s1[i] != s2[i]
Edit:          d(s1,s2) = min cost of insert + delete + substitute operations
```

## Learning Goals

After completing this project you should be able to:
- Explain the difference between quantitative, ordinal, and nominal distance
- Compute Manhattan and Euclidean distance by hand for small examples
- Understand why Hamming requires equal-length strings but edit distance does not
- Compute a distance matrix for a small dataset
