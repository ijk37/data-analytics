# Ch.01 Mini Project 03 — Attribute Scale Exercises

**Concept:** Stevens' four measurement scales (Nominal, Ordinal, Interval, Ratio) applied to five real-world examples from the Ch.1 exercises.

## What it does

`scale_exercises.py` / `scale_exercises.R`:

1. Print a quick-reference legend for all four Stevens scales
2. Walk through each of the five Ch.1 Exercise Q1 examples
3. Show the correct scale, detailed reasoning, and a heuristic cross-check against the `attribute_audit.py` (project-01) logic
4. Optional interactive quiz mode (Python only) — guess each scale before the answer is revealed

## Files

| File | Description |
|------|-------------|
| `scale_exercises.py` | Python solution — show all / quiz mode |
| `scale_exercises.R`  | R solution — typed vectors demonstrating each scale |
| `project_README.md`  | This file |

## Usage

```bash
# Python -- show all answers with reasoning
python scale_exercises.py

# Python -- interactive quiz mode
python scale_exercises.py --quiz

# R
Rscript scale_exercises.R
```

No external dependencies — pure Python 3 standard library and base R only.

## Exercise Q1 Answers

| # | Attribute | Correct Scale | Why |
|---|-----------|--------------|-----|
| a | University students' letter grades | **Ordinal** | Order A>B>C exists; gaps not measurable |
| b | Level of urgency in emergency room | **Ordinal** | Ranked low–critical; intervals not measurable |
| c | Classification of animals in a zoo | **Nominal** | Pure categories; no natural ordering |
| d | Carbon dioxide levels in atmosphere | **Ratio** | Numeric, true zero (0 ppm = no CO2), ratios valid |
| e | Distance from center of campus | **Ratio** | Numeric, true zero (0 m = center), ratios valid |

## Key Concepts from Ch.1 Applied

| Operation | Nominal | Ordinal | Interval | Ratio |
|-----------|---------|---------|----------|-------|
| Equality (=, !=) | Yes | Yes | Yes | Yes |
| Ordering (<, >) | No | Yes | Yes | Yes |
| Differences (+ / -) | No | No | Yes | Yes |
| Ratios (x / y) | No | No | No | Yes |

## How R Types Map to Stevens' Scales

```r
# Nominal  -> unordered factor
factor(c("mammal", "bird", "fish"), ordered = FALSE)

# Ordinal  -> ordered factor
factor(c("A","B","C"), levels=c("F","D","C","B","A"), ordered = TRUE)

# Interval -> numeric  (analyst decides: no true zero)
c(22.5, 23.0, 19.8)   # temperature in Celsius

# Ratio    -> numeric  (analyst decides: true zero present)
c(0.0, 120.5, 350.0)  # distance in meters
```

## Relation to Project-01

`attribute_audit.py` (project-01) infers scale automatically from column names and values. The heuristic cross-check in `scale_exercises.py` shows where the automated approach agrees with the manual analysis — and where domain knowledge is still needed (e.g., distinguishing Interval from Ratio requires knowing whether the zero is meaningful, which a keyword scan cannot always determine).
