# Ch.02 Mini Project 04 — Bivariate Quantitative Analyzer

**Concept:** Bivariate analysis for two quantitative attributes — covariance, Pearson's r, Spearman's rho, scatter plots, and correlation matrix heatmap.

## What it does

`bivariate_quantitative.py` analyzes every pair of numeric columns:

1. **Covariance** — sample formula; sign shows direction, value is scale-dependent
2. **Pearson's r** — scale-independent linear correlation; always in [−1, 1]
3. **Spearman's rho** — rank-based correlation; robust to outliers; valid for ordinal data
4. **Scatter plot** with trend line and both coefficients annotated
5. **Correlation matrix heatmap** — all pairs at a glance (blue = positive, red = negative)

## Dependencies

```bash
pip install matplotlib
```

## Usage

```bash
# Built-in demo (Ch.2 Friends dataset — reproduces the lecture results)
python bivariate_quantitative.py

# All numeric column pairs in a CSV
python bivariate_quantitative.py my_data.csv
```

## Expected results (lecture verification)

| Pair | Pearson r | Spearman rho | Interpretation |
|------|-----------|-------------|----------------|
| Weight, Height | **0.94** | **0.96** | Very strong positive relationship |

Both match the lecture slide values exactly.

## Key formulas

### Covariance (sample)
```
cov(xi, xj) = (1/(n-1)) * sum_k( (xki - x_bar_i) * (xkj - x_bar_j) )
```

### Pearson r
```
r(xi, xj) = cov(xi, xj) / (si * sj)    <- range: [-1, 1]
```

### Spearman rho
1. Replace each value with its rank (ties → average rank)
2. Apply Pearson's formula to the ranked columns

## Pearson vs Spearman — when to use which

| Situation | Use |
|-----------|-----|
| Linear relationship, no major outliers | Pearson r |
| Ordinal data | Spearman rho |
| Outliers present | Spearman rho (more robust) |
| Monotonic but non-linear relationship | Spearman rho |
| Both give similar values | Data is roughly elliptical, no outliers |

## Key Concepts from Ch.2 Applied

| Concept | Where it appears |
|---------|-----------------|
| Covariance formula | `covariance()` |
| Scale-independence of Pearson r | Division by sx * sy in `pearson_r()` |
| Rank assignment with tie handling | `assign_ranks()` |
| Spearman as Pearson on ranks | `spearman_rho()` calls `pearson_r(rx, ry)` |
| Correlation matrix | `plot_correlation_matrix()` |

## Limitations & Future Ideas

- Extension: add a p-value (statistical significance test) for the correlation.
- Extension: add a 3D histogram for joint frequency of two attributes.
- Extension: detect if Pearson and Spearman differ significantly (outlier warning).
