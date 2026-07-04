# Ch.03 Mini Project 01 — Multivariate Statistics Explorer

**Concept:** Location statistics matrix, dispersion statistics matrix, covariance
matrix, and Pearson correlation matrix for multivariate data.

## What it does

Given any CSV file (or the built-in Friends dataset), the project computes and
prints four multivariate summary tables:

1. **Location matrix** — min, Q1, median, mean, mode, Q3, max for every numeric column
2. **Dispersion matrix** — amplitude, IQR, MAD, std dev, variance for every numeric column
3. **Covariance matrix** — sample covariance for every pair of numeric columns
4. **Pearson correlation matrix** — scale-independent linear correlation for every pair

### Expected output (Friends dataset)

The printed correlation matrix should show:
- Weight / Height: r = 0.94 (very strong positive)
- All diagonal entries: 1.00

## Files

| File | Language | Description |
|------|----------|-------------|
| `multivariate_statistics.py` | Python 3 | Pure stdlib; beginner-friendly step-by-step |
| `multivariate_statistics.R`  | R        | Base R only; uses `apply()`, `cov()`, `cor()` |

## Usage

### Python

```bash
# Built-in demo (Friends dataset)
python multivariate_statistics.py

# From a CSV file
python multivariate_statistics.py data.csv
```

No external dependencies — pure Python 3 standard library.

### R

```r
source("multivariate_statistics.R")
```

Base R only — no packages needed.

## Key Concepts from Ch.03 Applied

| Concept | Where it appears |
|---------|-----------------|
| Location statistics matrix | `print_location_matrix()` |
| Dispersion statistics matrix | `print_dispersion_matrix()` |
| Sample covariance | `compute_covariance_matrix()` |
| Pearson correlation | `compute_correlation_matrix()` |
| Symmetric matrices | Diagonal = 1 (correlation); symmetric off-diagonal |

## Formulas Used

```
Covariance:   cov(X,Y) = (1/(n-1)) * sum[ (xi - x_bar)(yi - y_bar) ]
Pearson r:    r(X,Y)   = cov(X,Y) / (std(X) * std(Y))
MAD:          median( |xi - median(X)| )
IQR:          Q3 - Q1
Amplitude:    max - min
```
