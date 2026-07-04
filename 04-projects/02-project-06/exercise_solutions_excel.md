# Ch.2 Exercise Solutions — Excel Step-by-Step Guide

This guide shows how to solve each Ch.2 exercise question using Microsoft Excel formulas.  
All examples assume the Friends dataset is pasted into a worksheet starting at cell **A1** (header row).

---

## Dataset Layout

Paste the Friends dataset so that:

| Column | A | B | C | D | E | F | G |
|--------|---|---|---|---|---|---|---|
| Row 1 (header) | Friend | Max_temp | Weight | Height | Gender | Company | Years |
| Row 2 | Andrew | 25 | 77 | 175 | M | Good | 5 |
| Row 3 | Bernhard | 31 | 110 | 195 | M | Good | 14 |
| ... | ... | ... | ... | ... | ... | ... | ... |
| Row 15 | Nigel | 12 | 115 | 192 | M | Good | 3 |

Data rows: **C2:C15** (Weight), **G2:G15** (Years).

---

## Ex02a Q1 — Frequency Table for Weight

### Step 1: Get the sorted unique values

In a new area (e.g., column I), list the sorted unique Weight values.  
Either type them manually: 55, 63, 65, 66, 70, 72, 75, 77, 83, 85, 95, 110, 115  
or use `SMALL()` to extract sorted values programmatically:

```
I2 =SMALL($C$2:$C$15, ROW()-1)
```
Copy down for all 13 unique values (some SMALL() calls may repeat for 75; handle manually or use a helper).

### Step 2: Absolute frequency (COUNTIF)

In column J, count how many times each value appears in the Weight column:

```
J2 =COUNTIF($C$2:$C$15, I2)
```
Copy down through J14.

### Step 3: Relative frequency

In column K, divide each absolute frequency by the total count:

```
K2 =J2/COUNT($C$2:$C$15)
```
Copy down.  Format the column as **Percentage** or **Number** with 4 decimal places.

### Step 4: Cumulative absolute frequency

In column L:

```
L2 =J2
L3 =L2+J3
```
Copy L3 down through L14.

### Step 5: Cumulative relative frequency

In column M:

```
M2 =K2
M3 =M2+K3
```
Copy M3 down through M14.

### Expected result (first and last rows)

| Value | Abs Freq | Rel Freq | Cum Abs | Cum Rel |
|-------|----------|----------|---------|---------|
| 55 | 1 | 0.0714 | 1 | 0.0714 |
| 75 | 2 | 0.1429 | 8 | 0.5714 |
| 115 | 1 | 0.0714 | 14 | 1.0000 |

---

## Ex02a Q2 — Mode, Median, Q1, Q3 for Years

Assume Years data is in **G2:G15**.

### Mode

```
=MODE(G2:G15)
```
Returns the smallest mode if there are ties.  To see ALL modes use:

```
=MODE.MULT(G2:G15)
```
Enter as an **array formula** (Ctrl+Shift+Enter in older Excel; regular Enter in Excel 365).  
Expected: **{2, 3}** (both appear twice).

### Median

```
=MEDIAN(G2:G15)
```
Expected: **5.5**

### Q1 (first quartile)

```
=QUARTILE(G2:G15, 1)
```
or  
```
=PERCENTILE(G2:G15, 0.25)
```
Expected: **2**

> Note: Excel's `QUARTILE` / `PERCENTILE` use interpolation (equivalent to R's `type=7`), which may give a slightly different answer from the textbook's "split-halves" method.  The textbook answer is Q1 = 2.

### Q3 (third quartile)

```
=QUARTILE(G2:G15, 3)
```
or  
```
=PERCENTILE(G2:G15, 0.75)
```
Expected: **12**

### Summary

| Statistic | Formula | Expected |
|-----------|---------|----------|
| Mode | `=MODE.MULT(G2:G15)` | 2, 3 |
| Median | `=MEDIAN(G2:G15)` | 5.5 |
| Q1 | `=QUARTILE(G2:G15,1)` | 2 |
| Q3 | `=QUARTILE(G2:G15,3)` | 12 |

---

## Ex02b Q1 — Covariance, Pearson r, Spearman rho

### Setup

Paste the two vectors in a new sheet:

| | A | B |
|--|---|---|
| 1 | x | y |
| 2 | 2 | -1 |
| 3 | -1 | 1 |
| 4 | 0 | -2 |
| 5 | 1 | 0 |
| 6 | -2 | 1 |
| 7 | -3 | 2 |

Data: **A2:A7** (x), **B2:B7** (y).

### Sample Covariance

```
=COVARIANCE.S(A2:A7, B2:B7)
```

> Use `COVARIANCE.S` for the **sample** formula (denominator n-1).  
> `COVARIANCE.P` uses the population formula (denominator n) — that is NOT what the exercise expects.

Expected: **-2.1**

### Pearson r

```
=CORREL(A2:A7, B2:B7)
```

Expected: **-0.7626**

### Spearman rho

Excel has no built-in Spearman function, so you compute it by ranking x and y first, then correlating the ranks.

#### Step 1: Rank x (with average-tie handling)

In column C (header "rank_x"):

```
C2 =RANK.AVG(A2, $A$2:$A$7, 1)
```
Copy down through C7.

`RANK.AVG` assigns the average rank to tied values (matches the textbook tie-handling method).

#### Step 2: Rank y (with average-tie handling)

In column D (header "rank_y"):

```
D2 =RANK.AVG(B2, $B$2:$B$7, 1)
```
Copy down through D7.

Note: y has two values of 1 (rows 3 and 6).  `RANK.AVG` will assign them each rank **4.5** — which matches the Spearman tie correction.

#### Step 3: Pearson r on the ranks

```
=CORREL(C2:C7, D2:D7)
```

Expected: **-0.8117**

### Verification Table

| Statistic | Formula | Expected |
|-----------|---------|----------|
| Covariance | `=COVARIANCE.S(A2:A7,B2:B7)` | -2.1 |
| Pearson r | `=CORREL(A2:A7,B2:B7)` | -0.7626 |
| Spearman rho | `=CORREL(rank_x, rank_y)` | -0.8117 |

---

## Tips

- Always use **`COVARIANCE.S`** (sample, n-1) unless the problem says "population covariance".
- Always use **`RANK.AVG`** for Spearman to handle ties correctly.
- For quartiles, **`QUARTILE.INC`** is the modern name for `QUARTILE` in Excel 2010+; both use the interpolation method.
