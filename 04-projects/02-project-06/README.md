# Ch.02 Mini Project 06 — Chapter 2 Exercise Solutions

**Concept:** Univariate frequency analysis, measures of location and spread (mode, median, quartiles), and bivariate correlation (covariance, Pearson r, Spearman rho with tie handling).

## What it does

Solves three Ch.2 exercise questions, showing step-by-step computations and verifying each result against the exercise key:

| Exercise | Question | Concept |
|----------|----------|---------|
| Ex02a Q1 | Frequency table for `Weight` (Friends dataset) | Absolute, relative, cumulative frequencies |
| Ex02a Q2 | Mode, Median, Q1, Q3 for `Years` (Friends dataset) | Measures of location; quartile split method |
| Ex02b Q1 | Covariance, Pearson r, Spearman rho for two vectors | Bivariate correlation; tie handling |

## Files

| File | Description |
|------|-------------|
| `exercise_solutions.py` | Python — step-by-step solutions, verification output |
| `exercise_solutions.R`  | R — same solutions using base R functions |
| `exercise_solutions_excel.md` | Excel step-by-step guide with formulas |
| `project_README.md` | This file |

## Usage

```bash
# Python
python exercise_solutions.py

# R
Rscript exercise_solutions.R
```

No external dependencies — pure Python 3 standard library and base R only.

## Exercise Answers

### Ex02a Q1 — Frequency table for Weight

The Friends dataset has 14 friends with weights:  
`55, 63, 65, 66, 70, 72, 75, 75, 77, 83, 85, 95, 110, 115`

Weight 75 appears twice (frequency = 2); all others appear once.

### Ex02a Q2 — Mode, Median, Q1, Q3 for Years

Years values: `0, 1, 2, 2, 3, 3, 5, 6, 10, 11, 12, 14, 15, 16`  
(n = 14, sorted)

| Statistic | Value | How computed |
|-----------|-------|--------------|
| Mode | **2 and 3** | Both appear twice (highest frequency) |
| Median | **5.5** | n=14 even: (sorted[7] + sorted[8]) / 2 = (5+6)/2 |
| Q1 | **2** | Median of lower half: 0,1,2,2,3,3,5 -> (2+2)/2 |
| Q3 | **12** | Median of upper half: 6,10,11,12,14,15,16 -> (12+12)/2 |

### Ex02b Q1 — Covariance, Pearson r, Spearman rho

Given:  
`x = (2, -1, 0, 1, -2, -3)`  
`y = (-1, 1, -2, 0, 1, 2)`

| Statistic | Formula | Value |
|-----------|---------|-------|
| Sample covariance | `(1/(n-1)) * sum((xi - x_bar)(yi - y_bar))` | **-2.1** |
| Pearson r | `cov(x,y) / (sx * sy)` | **-0.7626** |
| Spearman rho | Pearson r on ranks (tie: two y=1 get rank 4.5 each) | **-0.8117** |

## Key Concepts Applied

- **Frequency table**: `Counter` → sort unique values → accumulate abs/rel frequencies.
- **Mode**: all values sharing the maximum count.
- **Median for even n**: average the two middle values of the sorted list.
- **Quartile split method**: for even n split into two equal halves; Q1 = median of lower half, Q3 = median of upper half.
- **Sample covariance**: uses denominator `n-1` (Bessel's correction).
- **Spearman tie handling**: tied values share the average of the ranks they would have occupied.

## Relation to Other Projects

| Project | What it adds |
|---------|-------------|
| `02-03-project-01` (frequency_table.py) | General frequency table for any CSV column |
| `02-03-project-02` (statistics_explorer.py) | Location & dispersion stats (mean, std, IQR) |
| `02-03-project-04` (bivariate_quantitative.py) | Full bivariate analysis with scatter plots |
| **This project (06)** | Explicit exercise solutions with step-by-step traces and answer verification |
