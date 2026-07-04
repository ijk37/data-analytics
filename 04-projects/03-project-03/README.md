# Ch.03 Mini Project 03 — Correlation & Heatmap Analysis

**Concept:** Scatter plot matrix (SPLOM), correlation matrix visualization,
correlogram, Pearson and Spearman correlation, heatmap with clustering.

## What it does

### Python (`correlation_analysis.py`)

Uses the Friends dataset (built-in) to demonstrate three correlation/heatmap
visualization types:

1. **Scatter plot matrix (SPLOM)** — all pairs of numeric attributes shown as a
   grid of scatter plots; diagonal shows attribute name
2. **Correlation heatmap** — color-coded Pearson r matrix for all attribute pairs
   at once; values annotated inside cells
3. **ASCII correlation table** — text-only Pearson r table with significance stars
   (`***` p<0.001, `**` p<0.01, `*` p<0.05)
4. **Spearman correlation matrix** — rank-based alternative; also printed as ASCII
   and as a color heatmap

### R (`correlation_analysis.R`)

Answers the Iris dataset exercise questions Q10, Q11, Q12 from Ch.03,
and also computes covariance/correlation for the Friends dataset:

| Exercise | Plot type | R function |
|----------|-----------|-----------|
| Q10 | Scatter plot matrix with Pearson r values | GGally::ggpairs |
| Q11 | Correlogram | corrplot::corrplot |
| Q12 | Heatmap with clustering dendrogram | pheatmap::pheatmap |
| — | Friends covariance + correlation | base R cov(), cor() |

## Files

| File | Language | Description |
|------|----------|-------------|
| `correlation_analysis.py` | Python 3 | Pure stdlib + optional matplotlib |
| `correlation_analysis.R`  | R        | GGally, corrplot, pheatmap |

## Usage

### Python

```bash
# Built-in demo (Friends dataset)
python correlation_analysis.py

# From a CSV file
python correlation_analysis.py data.csv
```

No external dependencies for text output. Install matplotlib for plots:
```bash
pip install matplotlib
```

### R

```r
# Install required packages once:
install.packages(c("ggplot2", "GGally", "corrplot", "pheatmap"))

source("correlation_analysis.R")
```

## Key Concepts from Ch.03 Applied

| Concept | Where it appears |
|---------|-----------------|
| Scatter plot matrix (SPLOM) | `plot_scatter_matrix()` |
| Pearson correlation heatmap | `plot_correlation_heatmap()` |
| Spearman correlation | `compute_spearman_matrix()` |
| Correlogram | R: corrplot, Python: heatmap with color scale |
| Heatmap + dendrogram | R: pheatmap |

## Formulas

```
Pearson r:   r = cov(X,Y) / (std(X) * std(Y))   [linear only]
Spearman rho: apply Pearson r to the RANKS of X and Y  [monotonic, robust]
```

## Significance thresholds (for starred table)

| Stars | Meaning |
|-------|---------|
| `***` | Very likely not zero (|r| >= 0.70) |
| `**`  | Probably not zero  (|r| >= 0.50) |
| `*`   | Possibly not zero  (|r| >= 0.30) |
| ` `   | Negligible / near zero |
