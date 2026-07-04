# Ch.02 Mini Project 02 — Location & Dispersion Statistics Explorer

**Concept:** All Ch.2 univariate statistics — location (central tendency) and dispersion — implemented from scratch using only the Python standard library.

## What it does

For every numeric column in a CSV (or the built-in demo), `statistics_explorer.py`:

1. **Location statistics** — Min, Max, Mean, Mode, Median, Q1, Q2, Q3
2. **Dispersion statistics** — Amplitude, IQR, MAD, Standard Deviation, Variance
3. **Skewness** — computed and classified (symmetric / positive / negative)
4. **ASCII box plot** — visual five-number summary (min, Q1, median, Q3, max)
5. **Central tendency check** — compares mean vs. median to confirm skew direction

## Usage

```bash
# Built-in demo (Weight, Height, Max_temp from the Ch.2 Friends dataset)
python statistics_explorer.py

# All numeric columns from a CSV
python statistics_explorer.py my_data.csv
```

No external dependencies — pure Python 3 standard library only.

## Sample Output

```
======================================================================
  STATISTICS REPORT: Weight
  n = 14  |  Missing = 0
======================================================================

  LOCATION STATISTICS
--------------------------------------------------
  Min                       55.0000
  Max                      115.0000
  Mean (x-bar)              79.0000
  Mode                      75.0  (freq=2)
  Median (Q2)               75.0000
  Q1 (25th pct)             66.0000
  Q3 (75th pct)             85.0000

  DISPERSION STATISTICS
--------------------------------------------------
  Amplitude (max-min)       60.0000
  IQR (Q3-Q1)               19.0000
  MAD (sample)              14.3077
  Std Dev (sample)          17.3848
  Variance (sample)        302.0769

  SHAPE
--------------------------------------------------
  Skewness                  +0.8812
                            Positive (right) skew

  Box plot: Weight
  |-----------[======|=======]-----------|
```

## Formulas Implemented

| Statistic | Formula used | Notes |
|-----------|-------------|-------|
| Mean | Σxᵢ / n | Arithmetic mean |
| Median | Middle value (sorted) | Exact lecture formula |
| Quartiles | Position method n×(k/4) | Exact lecture method |
| MAD | Σ\|xᵢ − x̄\| / (n−1) | Sample formula |
| Std Dev | √(Σ(xᵢ−x̄)² / (n−1)) | Bessel's correction (n−1) |
| Skewness | Σ(xᵢ−x̄)³/n / s³ | Fisher's moment coefficient |

## Key Concepts from Ch.2 Applied

| Concept | Where it appears |
|---------|-----------------|
| Central tendency statistics | `compute_mean/median/mode()` |
| Quartile position method | `compute_quartile()` |
| Bessel's correction (n−1) | `compute_std()`, `compute_mad()` |
| Skewness taxonomy | `classify_skewness()` |
| Five-number summary | `ascii_boxplot()` |

## Limitations & Future Ideas

- Extension: add a `--population` flag to switch to population formulas (÷n instead of ÷n−1).
- Extension: add percentile computation for arbitrary quantiles.
- Extension: add the coefficient of variation (std/mean × 100%) as a relative dispersion measure.
