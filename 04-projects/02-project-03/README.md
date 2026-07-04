# Ch.02 Mini Project 03 — Distribution Visualizer

**Concept:** Univariate visualization — histograms, box plots, skewness, and common probability distributions (Normal and Uniform).

## What it does

`distribution_visualizer.py` produces four types of plots for any numeric column:

1. **Combined histogram + box plot** (like the lecture slide p.45) — histogram on the bottom, box plot on top, sharing the x-axis
2. **Histogram with Normal overlay** — fits N(mu, sigma) to the data and overlays the PDF
3. **Box plot with annotations** — labels min, Q1, median, Q3, max
4. **Normal vs. Uniform comparison** — side-by-side PDF comparison to understand both distributions

Falls back to **ASCII histograms** if matplotlib is not installed.

## Dependencies

```bash
pip install matplotlib
```

## Usage

```bash
# Built-in demo (Ch.2 Friends dataset — Weight, Height, Max_temp)
python distribution_visualizer.py

# All numeric columns from a CSV
python distribution_visualizer.py my_data.csv

# Single column
python distribution_visualizer.py my_data.csv Age
```

## What each plot shows

### Combined histogram + box plot
- Bin count chosen by the **sqrt rule**: bins ≈ √n
- Rug plot (tick marks) below the histogram shows individual data points
- Normal PDF overlay for visual distribution fit check
- Skewness value and label in the title

### Box plot anatomy (from lecture)
```
  whisker top ─── Max
                  |
  top of box  ─── Q3
  median line ─── Q2  (median)
  bottom of box── Q1
                  |
  whisker bottom─ Min
```

### Normal vs. Uniform comparison
- **Normal N(mu, sigma)**: bell-shaped, symmetric, two parameters — mean (center) and std dev (width)
- **Uniform U(a, b)**: flat, equal probability everywhere in [a, b]

## Key Concepts from Ch.2 Applied

| Concept | Where it appears |
|---------|-----------------|
| Histogram bin selection (sqrt rule) | `suggest_bins()` |
| Normal PDF | `normal_pdf()` |
| Uniform PDF | `uniform_pdf()` |
| Skewness classification | `skewness()` + title annotation |
| Box plot anatomy | `plot_boxplot()` |
| Combined chart | `plot_combined()` |

## Limitations & Future Ideas

- Extension: add Sturges' rule and Freedman-Diaconis rule as alternative bin selectors.
- Extension: add a Q-Q plot to formally test normality.
- Extension: add a kernel density estimate (KDE) as an alternative to the histogram.
