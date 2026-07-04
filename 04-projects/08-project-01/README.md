# Project 01 — End-to-End Data Pipeline

## Overview

You receive a raw dataset with quality issues. The pipeline cleans it, explores it
statistically, clusters it, then builds a classifier. This project ties together
preprocessing, descriptive statistics, clustering, and classification in a single
realistic workflow.

## Chapters Combined

| Step | Chapter | Topic                              |
|------|---------|------------------------------------|
| 1-2  | Ch4     | Data quality audit and cleaning    |
| 3    | Ch2     | Univariate descriptive statistics  |
| 4    | Ch3     | Bivariate correlation matrix       |
| 5    | Ch4     | Min-max normalization              |
| 6    | Ch5     | K-means clustering (K=2)           |
| 7    | Ch7     | Classification + prediction        |
| 8    | All     | Final summary report               |

## Dataset

The FRIENDS dataset: 14 people (with one injected missing value and one duplicate row).

Features: Max_temp, Weight, Height, Years, Gender
Target label: Company (Good / Bad)

## How to Run

### Python
```
python full_pipeline.py
```
No external libraries required. Pure Python stdlib only.

### R
```
Rscript full_pipeline.R
```
Requires: e1071 (install.packages("e1071"))

## Expected Output (Python)

```
===== STEP 1: DATA QUALITY AUDIT =====
Missing values detected: 1
  Eve -> Weight: ?
Duplicate rows detected: 1
  Row 15 is a duplicate of row 1 (Andrew)

===== STEP 2: CLEAN DATA =====
Filled Eve Weight with Female group mean: 68.3
Removed 1 duplicate row.
Dataset size after cleaning: 14 rows

===== STEP 3: UNIVARIATE STATS =====
Column      Mean    Median  Std     Q1      Q3
Max_temp    18.50   15.50   7.29    12.00   25.25
...

===== STEP 4: CORRELATION MATRIX =====
            Max_temp  Weight  Height  Years
Max_temp    1.000     0.427   0.319   0.612
...

===== STEP 5: NORMALIZATION =====
Normalized numeric columns to [0,1]

===== STEP 6: K-MEANS CLUSTERING (K=2) =====
Cluster 0: Andrew, Dennis, James, Lea, Bernhard, Nigel
Cluster 1: Carolina, Eve, Gwyneth, Hayden, Irene, Kevin, Marcus

===== STEP 7: CLASSIFICATION =====
New object 1 prediction: Good
New object 2 prediction: Bad

===== STEP 8: FINAL REPORT =====
Summary of pipeline findings...
```

## File Structure

```
08-03-project-01/
    project_README.md      -- this file
    full_pipeline.py       -- Python implementation (pure stdlib)
    full_pipeline.R        -- R implementation
```
