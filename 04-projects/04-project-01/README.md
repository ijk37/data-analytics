# Project 01: Data Quality Auditor

**Chapter 4 — Data Quality and Preprocessing**

---

## What This Project Does

This project demonstrates how to detect and fix common data quality problems:

1. **Missing values** — identify which cells are empty, then fill them using mean, median, or mode
2. **Duplicate rows** — detect identical records and remove one copy
3. **Outlier / inconsistency detection** — flag values that fall far outside the expected range (IQR method)

---

## Concepts Covered

| Problem | Technique | Section in Notes |
|---|---|---|
| Missing values | Fill with mean / median / mode | 2.1 |
| Per-class imputation | Fill with class-specific mean | 2.1 |
| Duplicate records | Deduplication | 2.2 |
| Outliers / inconsistencies | IQR fencing | 2.5 |

---

## Files

| File | Language | Description |
|---|---|---|
| `data_quality.py` | Python 3 | Full audit pipeline, pure stdlib |
| `data_quality.R` | R | Same operations using base R |

---

## Usage

### Python

```
python data_quality.py              # runs built-in FRIENDS demo
python data_quality.py mydata.csv   # audits any CSV file
```

### R

```
Rscript data_quality.R
```

Or open `data_quality.R` in RStudio and run it.

---

## Built-In Demo Dataset

The demo uses a FRIENDS-like dataset with **injected quality problems**:

- **Missing values**: a few cells are blank (age, weight, city)
- **Duplicate row**: one person appears twice
- **Inconsistent value**: one weight entry of 1100 kg (clearly wrong for a human)

The program prints a before/after comparison for each fix.

---

## Expected Output (summary)

```
=== DATA QUALITY AUDIT REPORT ===

--- MISSING VALUES ---
age    : 1 missing (10.0%)
weight : 1 missing (10.0%)
city   : 1 missing (10.0%)

--- AFTER FILLING ---
age    filled with mean   : 34.8
weight filled with median : 70.0
city   filled with mode   : New York

--- DUPLICATES ---
Found 1 duplicate row(s). Removed.

--- OUTLIERS (IQR) ---
weight column:
  Value 1100 flagged as outlier  [bounds: 47.5 .. 102.5]
```

---

## Key Functions

| Function | Purpose |
|---|---|
| `audit_missing(columns)` | Report count and % missing per column |
| `fill_missing_mean(values)` | Replace missing with column mean |
| `fill_missing_median(values)` | Replace missing with column median |
| `fill_missing_mode(values)` | Replace missing with most frequent value |
| `fill_missing_per_class(columns, target_col)` | Fill per class group |
| `detect_duplicates(columns)` | Find indices of duplicate rows |
| `remove_duplicates(columns)` | Return deduplicated column dict |
| `detect_outliers_iqr(values)` | Flag values outside Q1-1.5*IQR .. Q3+1.5*IQR |

---

## When to Use Which Fill Strategy

```
Nominal attribute (categories like city, gender)?
  -> fill_missing_mode()

Quantitative attribute, roughly symmetric?
  -> fill_missing_mean()

Quantitative attribute, skewed or has outliers?
  -> fill_missing_median()

Target class is available?
  -> fill_missing_per_class()  (most accurate)
```
