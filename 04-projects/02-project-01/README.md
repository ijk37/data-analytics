# Ch.02 Mini Project 01 — Frequency Table Builder

**Concept:** Univariate frequency analysis — absolute, relative, and cumulative frequencies; empirical distributions and CDFs.

## What it does

Given any CSV file (or the built-in lecture demo dataset), `frequency_table.py` produces a complete frequency table for each column:

1. **Absolute frequency** — how many times each value appears
2. **Relative frequency** — percentage of total (defines the empirical distribution)
3. **Absolute cumulative frequency** — count of values ≤ this value
4. **Relative cumulative frequency** — fraction of values ≤ this value (empirical CDF)
5. **ASCII frequency bar** — visual proportional bar for each row
6. **Summary statistics** — mode (always), plus mean/median/range for numeric columns

## Usage

```bash
# Built-in demo (Ch.2 Friends dataset — Company, Height, Weight, Gender)
python frequency_table.py

# All columns from a CSV
python frequency_table.py my_data.csv

# One specific column
python frequency_table.py my_data.csv Weight
```

No external dependencies — pure Python 3 standard library only.

## Sample Output

```
==============================================================================
  FREQUENCY TABLE: Company
  Total records: 14  |  Non-missing: 14  |  Missing: 0
==============================================================================
  Value       Abs. Freq   Rel. Freq   Abs. Cum.   Rel. Cum.
------------------------------------------------------------------------------
  Bad                 8      57.14%           8      57.14%    |||||||||||
  Good                6      42.86%          14     100.00%    |||||||||
------------------------------------------------------------------------------

  Unique values: 2
  Mode         : Bad  (appears 8 times, 57.1% of data)

==============================================================================
  FREQUENCY TABLE: Weight
  Total records: 14  |  Non-missing: 14  |  Missing: 0
==============================================================================
  Value       Abs. Freq   Rel. Freq   Abs. Cum.   Rel. Cum.
------------------------------------------------------------------------------
  55.0                1       7.14%           1       7.14%    |
  63.0                1       7.14%           2      14.29%    |
  ...
  Mode: 75  |  Mean: 79.0  |  Median: 75.0  |  Range: [55.0, 115.0]
```

## Key Concepts from Ch.2 Applied

| Concept | Where it appears |
|---------|-----------------|
| Absolute frequency | `abs_freq` column |
| Relative frequency (empirical distribution) | `rel_freq` column |
| Cumulative frequencies (empirical CDF) | `abs_cum_freq`, `rel_cum_freq` columns |
| Mode (valid for all scales) | Summary line |
| Mean & Median (quantitative only) | Summary line, numeric columns only |
| Missing value handling | Counted and excluded before analysis |

## Limitations & Future Ideas

- Sorting is alphabetical for text columns — for ordinal columns you may want a custom order.
- Extension: add PMF vs. PDF labeling based on whether the column is discrete or continuous.
- Extension: add a `--bins` flag to group numeric values into histogram bins before counting.
