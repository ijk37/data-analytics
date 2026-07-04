# Ch.02 Mini Project 05 — Categorical Relationship Analyzer

**Concept:** Bivariate analysis involving qualitative attributes — contingency tables, mosaic plots, grouped box plots, and jitter scatter plots for ordinal pairs.

## What it does

`categorical_analyzer.py` covers all three categorical bivariate scenarios from the lecture:

| Attribute pair | Analysis | Visualization |
|----------------|----------|--------------|
| Qual + Qual | Contingency table | Mosaic plot |
| Qual + Quant | Grouped summary stats per category | Grouped box plots |
| Ordinal + Ordinal | Spearman's rho | Jitter scatter plot |

## Dependencies

```bash
pip install matplotlib
```

## Usage

```bash
# Built-in demo (Ch.2 Friends dataset — Company, Gender, Weight, Height)
python categorical_analyzer.py

# Analyze your own CSV (auto-detects column types)
python categorical_analyzer.py my_data.csv
```

## What each analysis shows

### 1. Contingency Table (Qual + Qual)
A matrix of joint frequencies with row totals, column totals, and grand total. Both absolute counts and relative percentages are shown.

```
  Contingency Table: Company (rows) vs. Gender (cols)
  =====================================================
  Company          F         M     Total
  -------------------------------------------------
  Bad       4 (28.6%)  4 (28.6%)        8
  Good      2 (14.3%)  4 (28.6%)        6
  -------------------------------------------------
  Total             6         8       14
```

### 2. Mosaic Plot (Qual + Qual)
A rectangle for each cell of the contingency table. **Width** = column marginal proportion, **height** = conditional proportion within the column. Areas are directly proportional to relative joint frequency.

### 3. Grouped Box Plots (Qual + Quant)
One box plot per category, all on the same axis. Reveals whether the distribution of the numeric attribute differs meaningfully between groups.

### 4. Jitter Scatter Plot (Ordinal + Ordinal)
Adds a small random offset to each point. Without jitter, all identical (rank, rank) pairs overlap as a single dot — making the cloud invisible. Side-by-side comparison of with/without jitter shows why the technique matters.

## Key Concepts from Ch.2 Applied

| Concept | Where it appears |
|---------|-----------------|
| Contingency table | `build_contingency_table()`, `print_contingency_table()` |
| Mosaic plot (area = relative freq) | `plot_mosaic()` |
| Grouped box plots | `plot_grouped_boxplots()` |
| Jitter effect | `plot_jitter_scatter()` |
| Spearman rho (ordinal pair) | `spearman_rho()` — same as project-04 |
| Five-number summary | `five_num_summary()` |

## Limitations & Future Ideas

- Extension: add chi-squared (χ²) test of independence to the contingency table output.
- Extension: add a Cramér's V statistic (strength of association for nominal-nominal pairs).
- Extension: support ordered categories (e.g., Low < Medium < High) in mosaic and contingency tables.
