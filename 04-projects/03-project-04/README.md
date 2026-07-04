# Project 03-03-04: Multivariate Frequency Tables & Mosaic Plots

## What This Project Covers

This mini-project explores how to describe relationships between two or more
qualitative (categorical) attributes using cross-tabulation and mosaic plots.
It is part of Chapter 3 — Descriptive Multivariate Analysis.

### Concepts Demonstrated

| Concept | Description |
|---|---|
| **Joint frequency table** | 2D cross-tabulation: rows = values of attribute A, columns = values of attribute B, cells = co-occurrence counts |
| **Joint relative frequency** | Each cell count divided by the grand total n; measures how common each combination is overall |
| **Marginal frequencies** | Row totals and column totals; the 1D distribution of each attribute ignoring the other |
| **Conditional frequencies** | P(B = v | A = u) = cell count / row total; how B is distributed *within* each level of A |
| **3-way frequency table** | Extends cross-tabulation to three qualitative attributes: a nested dict / 3D array of counts |
| **Mosaic plot** | Visual representation of a 2D (or 3D) cross-tabulation: column width proportional to the marginal frequency of the column variable; segment height within each column proportional to the conditional frequency of the row variable given that column value |

### Dataset

The **Friends dataset** (n = 14) records three qualitative attributes for each friend:

- `Gender` — M or F
- `Company` — Good or Bad
- `Food_pref` — Meat, Mixed, or Vegetarian

All analyses use this dataset as a worked example.

---

## Files

| File | Language | Purpose |
|---|---|---|
| `joint_frequency_mosaic.py` | Python 3 (stdlib only) | Full analysis with ASCII tables and ASCII mosaic plot |
| `joint_frequency_mosaic.R` | R (base only) | Same analysis using `table()`, `prop.table()`, and `mosaicplot()` |
| `project_README.md` | Markdown | This file |

---

## How to Run

### Python

```
python joint_frequency_mosaic.py
```

The script runs the demo automatically. To analyse your own CSV file:

```
python joint_frequency_mosaic.py your_data.csv
```

You will be prompted to select which columns to use as attribute A and B.
A third column can optionally be chosen for a 3-way table.

**Requirements:** Python 3.x, standard library only (no pip installs needed).

### R

```
Rscript joint_frequency_mosaic.R
```

Or open the file in RStudio and run it section by section.

**Requirements:** Base R (no additional packages needed). Graphical windows
will open for each mosaic plot.

---

## Expected Output

### Python

Running `python joint_frequency_mosaic.py` prints to the terminal:

1. **Absolute joint frequency table** for Gender x Company with row/column totals
2. **Relative joint frequency table** (fractions summing to 1)
3. **Conditional frequency table** P(Company | Gender) as percentages (each row sums to 100%)
4. **ASCII mosaic plot** for Gender x Company — columns sized by Company marginal, segments by conditional Gender
5. **Absolute joint frequency table** for Gender x Food_pref
6. **ASCII mosaic plot** for Gender x Food_pref
7. **3-way frequency table** Gender x Company x Food_pref (one sub-table per Gender value)

Example snippet of the absolute Gender x Company table:

```
  [Absolute Joint Frequency Table]  Gender x Company
Gender x Company | Bad  | Good | Total
-----------------+------+------+------
F                | 5    | 1    | 6
M                | 2    | 6    | 8
-----------------+------+------+------
Total            | 7    | 7    | 14
```

Example snippet of the ASCII mosaic (Gender x Company):

```
  MOSAIC: Gender x Company
  ====================================================
  |##################################################|                    |
  |##################################################|                    |
  ...
  |##################################################|----------|  F (42.9%)
  |--------------------------------------------------|----------|
  ...
                     Bad              Good
```

### R

Running the R script prints the same tables to the console and opens
graphical mosaic plots:

1. `table()` absolute counts for Gender x Company with `addmargins()`
2. `prop.table()` relative and conditional frequencies
3. Mosaic plot window: Gender x Company (base R `mosaicplot()`)
4. Tables for Gender x Food_pref
5. Mosaic plot window: Gender x Food_pref
6. `ftable()` for the 3-way Gender x Company x Food_pref table
7. Mosaic plot window: 3-way mosaic

---

## Key Takeaways

- A joint frequency table is the foundation for all multivariate categorical analysis.
- Marginal frequencies collapse the joint table to a single attribute, recovering the 1D distribution.
- Conditional frequencies reveal whether and how the distribution of one attribute shifts across levels of another — this is the first step toward detecting association.
- A mosaic plot makes the joint and conditional structure visible at a glance: if all column segments have the same relative heights, the two attributes are independent; unequal heights indicate association.
- Extending to three attributes (3-way table / 3-way mosaic) allows detection of interaction effects — whether the relationship between two attributes changes depending on the value of a third.
