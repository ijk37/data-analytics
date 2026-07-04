# Project 02: Discretization & Encoding

**Chapter 4 — Data Quality and Preprocessing**

---

## What This Project Does

This project demonstrates how to convert continuous and ordinal data into discrete numeric representations:

1. **Equal-Width Binning** — divide the value range into N bins of equal width
2. **Equal-Depth Binning** — divide sorted values into N bins with equal count
3. **One-Hot Encoding** — convert nominal categories into binary columns
4. **Natural Number Encoding** — map ordinal categories to 0, 1, 2, ...
5. **Gray Code Encoding** — adjacent categories differ by exactly 1 bit
6. **Thermometer Code Encoding** — n-th category has n ones from the left

The demo **explicitly solves Exercise Q1, Q2, and Q3** from the Chapter 4 exercise sheet and prints Expected vs. Computed comparisons.

---

## Concepts Covered

| Technique | Use Case | Section in Notes |
|---|---|---|
| Equal-width bins | Continuous → ordinal; uniform boundaries | 4.1 |
| Equal-depth bins | Continuous → ordinal; balanced bin counts | 4.2 |
| One-hot encoding | Nominal → numeric for ML algorithms | 5.1 |
| Natural numbers | Ordinal → simple integer codes | 5.2 |
| Gray code | Ordinal → minimize bit-flip errors | 5.2 |
| Thermometer code | Ordinal → strict cumulative encoding | 5.2 |

---

## Files

| File | Language | Description |
|---|---|---|
| `discretization_encoding.py` | Python 3 | Full implementation, pure stdlib |
| `discretization_encoding.R` | R | Same operations using base R |

---

## Usage

### Python

```
python discretization_encoding.py
```

### R

```
Rscript discretization_encoding.R
```

---

## Exercise Q&A Solved in This Project

### Q1: Discretize [31,38,42,29,46,23,83,43,51,55,27,35] into 4 bins

**Equal-Width:** W = (83-23)/4 = 15
- Bin 0: [23, 37]  -> values: 23, 27, 29, 31, 35
- Bin 1: [38, 52]  -> values: 38, 42, 43, 46, 51
- Bin 2: [53, 67]  -> values: 55
- Bin 3: [68, 83]  -> values: 83

**Equal-Depth:** 3 values per bin (12 values / 4 bins)
- Bin 0: {23, 27, 29}
- Bin 1: {31, 35, 38}
- Bin 2: {42, 43, 46}
- Bin 3: {51, 55, 83}

### Q2: One-Hot Encoding for Food column

Categories: American, Chinese, Italian, Other

| Row | Food     | American | Chinese | Italian | Other |
|-----|----------|----------|---------|---------|-------|
| 0   | Chinese  | 0        | 1       | 0       | 0     |
| 1   | Italian  | 0        | 0       | 1       | 0     |
| 2   | American | 1        | 0       | 0       | 0     |
| 3   | Chinese  | 0        | 1       | 0       | 0     |
| 4   | Italian  | 0        | 0       | 1       | 0     |

### Q3: Gray Code for Distance values

| Distance   | Integer | Gray Code |
|------------|---------|-----------|
| very_close | 0       | 000       |
| close      | 1       | 001       |
| far        | 2       | 011       |
| very_far   | 3       | 010       |
| too_far    | 4       | 110       |

---

## Excel How-To

### Equal-Width Binning with IF / VLOOKUP

Suppose your data is in column A (A2:A13), you want 4 equal-width bins.

**Step 1:** Compute bin width in a helper cell:
```
E1: =( MAX($A$2:$A$13) - MIN($A$2:$A$13) ) / 4
```

**Step 2:** Define bin boundaries in a lookup table (e.g., columns G:H):
```
G1: Lower    H1: Bin_Label
G2: =MIN($A$2:$A$13)          H2: 0
G3: =G2+$E$1                  H3: 1
G4: =G3+$E$1                  H4: 2
G5: =G4+$E$1                  H5: 3
```

**Step 3:** Assign each value a bin using VLOOKUP (approximate match):
```
B2: =VLOOKUP(A2, $G$2:$H$5, 2, TRUE)
```
Copy down to B13.

VLOOKUP with TRUE (approximate match) finds the largest boundary <= the value,
which exactly maps to the equal-width bin definition.

---

### One-Hot Encoding with IF formulas

Suppose Food values are in column A (A2:A6). Categories are American, Chinese, Italian, Other.

**Column B (American):**
```
B2: =IF(A2="American", 1, 0)
```

**Column C (Chinese):**
```
C2: =IF(A2="Chinese", 1, 0)
```

**Column D (Italian):**
```
D2: =IF(A2="Italian", 1, 0)
```

**Column E (Other):**
```
E2: =IF(A2="Other", 1, 0)
```

Copy each formula down the column.

**Tip:** You can also use a single formula with COUNTIF for dynamic categories:
```
B2: =IF($A2=B$1, 1, 0)
```
where row 1 contains the category names (American, Chinese, Italian, Other).
This lets you fill the entire grid by copying one formula in all directions.
