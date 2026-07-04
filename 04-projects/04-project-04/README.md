# Mini-Project 04-03-04: Data Transformation

**Chapter 4 -- Data Quality and Preprocessing**

---

## Purpose

This project demonstrates how to identify and correct skewed distributions using
data transformation techniques. By the end you will understand:

- Why transformations are needed (skewness, non-normality, heavy tails)
- How to apply log, square root, absolute value, and Box-Cox transforms
- How to measure whether a transformation improved symmetry (skewness metric)
- When to use each transform -- and when to leave the data alone

---

## Concepts Covered

### Why Transform Data?

Raw data from the real world is often skewed:

- **Income and salary** data: most people earn modest amounts, but a few earners
  push the mean far above the median, creating a long right tail.
- **Right-skewed** (positive skew): mean > median > mode. The log transform is
  the classic remedy.
- **Left-skewed** (negative skew): mean < median < mode. Less common; square or
  exponential transforms can help.

Transformations help by:
- Reducing skewness so the distribution is closer to normal
- Stabilising variance (heteroscedasticity)
- Reducing the influence of extreme outliers
- Meeting normality assumptions required by some statistical models

---

### Transformations Covered

| Transform | Formula | Best for |
|---|---|---|
| Log | `x' = log(x)` | Strongly right-skewed data; income, prices, populations |
| Log + 1 | `x' = log(x + 1)` | Same as log but handles zeros safely |
| Square root | `x' = sqrt(x)` | Mildly right-skewed data; count data |
| Absolute value | `x' = abs(x)` | Signed data where only magnitude matters |
| Box-Cox | `x' = (x^lambda - 1) / lambda` | Data-driven; generalises log and sqrt |

**Box-Cox special cases:**

| Lambda | Transform |
|---|---|
| `lambda = 0` | `log(x)` |
| `lambda = 0.5` | close to `sqrt(x)` |
| `lambda = 1` | no transformation |
| `lambda = -1` | reciprocal `1/x` |

**Skewness rule of thumb:**

| Skewness value | Interpretation |
|---|---|
| > 1.0 | Strongly right-skewed |
| 0.5 to 1.0 | Moderately right-skewed |
| -0.5 to 0.5 | Approximately symmetric |
| -1.0 to -0.5 | Moderately left-skewed |
| < -1.0 | Strongly left-skewed |

---

### When NOT to Transform

- When the original scale has direct interpretability (e.g., reporting mean
  salary to stakeholders -- back-transform your result)
- When skewness is mild (`|skew| < 0.5`) and the algorithm is robust
- For tree-based models (Random Forest, XGBoost) which are invariant to
  monotone transformations
- When zeros or negatives make log / Box-Cox inapplicable without shifting

---

## Demo Datasets

### Salary Data (15 employees)

Strongly right-skewed: most salaries cluster between 35,000 and 95,000, but
three employees (Karl, Lea, Nina) earn 250,000 -- 880,000, pulling the mean
far above the median.

| Person | Salary | Years Exp |
|---|---|---|
| Alice | 35,000 | 1 |
| Bob | 42,000 | 2 |
| ... | ... | ... |
| Nina | 880,000 | 25 |

### Temperature Deviations

Signed deviations from a baseline temperature:
`[-15, 8, -3, 22, -18, 5, -9, 14, -7, 11, -20, 3, -1, 16, -12]`

Used to demonstrate the absolute value transform, where only the magnitude of
deviation matters (not whether it was warmer or cooler).

---

## Files

| File | Description |
|---|---|
| `data_transformation.py` | Pure Python (stdlib only) implementation |
| `data_transformation.R` | R implementation using base R + MASS |
| `project_README.md` | This file |

---

## How to Run

### Python

Requirements: Python 3.6+, no third-party packages needed.

```bash
python data_transformation.py
```

**Expected output:**
- Banner and section headers in the terminal
- Statistics tables comparing original vs transformed data (mean, median, std,
  skewness, min, max)
- ASCII histograms showing the shape of each distribution
- Box-Cox lambda search table with the best lambda highlighted
- Summary table of skewness reduction across all transforms
- Absolute value demo with before/after comparison
- Guide on when to use each transform

### R

Requirements: R 3.5+, MASS package (ships with standard R installations).

```r
source("data_transformation.R")
```

Or open the file in RStudio and click **Source** (top-right of the editor pane).

**Expected output:**
- Console output: summary statistics and skewness values at each step
- Plot 1: Histogram of original salaries (right-skewed shape visible)
- Plot 2: Histogram of log-transformed salaries (more symmetric)
- Plot 3: Side-by-side histograms of original vs absolute temperature deviations
- Plot 4: Box-Cox log-likelihood curve (lambda on x-axis; peak = optimal lambda)
- Plot 5: 2x2 panel comparing original, log, sqrt, and Box-Cox distributions
- Console commentary: which transform worked best and why

---

## Key Takeaways

1. **Log transform** is the go-to fix for right-skewed data that spans orders of
   magnitude (salaries, prices, city populations).
2. **Square root** is a gentler alternative when log feels too aggressive.
3. **Absolute value** is the right tool when signs are noise, not signal.
4. **Box-Cox** generalises all of the above and finds the optimal lambda
   automatically -- but requires strictly positive data.
5. Always **compare skewness before and after** to confirm the transform helped.
6. Remember to **back-transform** reported results when the original scale
   matters to your audience.
