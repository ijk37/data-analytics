# Ch.01 Mini Project — Attribute Auditor

**Concept:** Stevens' attribute taxonomy (Nominal → Ordinal → Interval → Ratio), discrete vs. continuous, appropriate summary statistics per scale.

## What it does

Given any CSV file, `attribute_audit.py` will:

1. **Infer each column's attribute type** using name-hinting heuristics and value analysis
2. **Classify discrete vs. continuous**
3. **Flag missing values** per column
4. **Print a column-type summary** (bar chart of type distribution)

## Usage

```bash
# Run the built-in demo (mirrors Ch.1 textbook dataset)
python attribute_audit.py

# Audit your own CSV
python attribute_audit.py my_dataset.csv
```

No external dependencies — pure Python 3 standard library only.

## Sample Output

```
════════════════════════════════════════════════════════════════════════════════
  ATTRIBUTE AUDIT REPORT
  Source  : Demo (Ch.1 textbook dataset + extras)
  Rows    : 10   |   Columns: 7
════════════════════════════════════════════════════════════════════════════════

  Column  : Name
  Type    : Nominal       |  Discrete
  Notes   : 10 unique values.
············...

  Column  : Age
  Type    : Ratio         |  Discrete
  Notes   : Range [23.00, 82.00]
············...

  Column  : Temperature_C
  Type    : Interval      |  Continuous
  Notes   : Date/time/calendar-based column.
············...

  COLUMN TYPE SUMMARY
  Ratio      ███ 3
  Nominal    ██ 2
  Ordinal    █ 1
  Interval   █ 1
```

## Key Concepts from Ch.1 Applied

| Concept | Where it appears in code |
|---------|--------------------------|
| Stevens' 4 attribute types | `infer_attribute_type()` return value |
| True-zero test for Ratio | `has_true_zero()` heuristic |
| Discrete vs. continuous | `is_integer_valued()` check |
| Missing value handling | counted and reported per column |

## Known Issues

- `infer_attribute_type()` is **defined twice** — first stub (incomplete) then full implementation. Python silently uses the last definition; the stub should be removed.

## Limitations & Future Ideas

- Type inference is **heuristic** — column name + value analysis. Always verify manually for real datasets.
- Extension: `--force-type colname=Ordinal` CLI flag to override inference per column.
- Extension: `compute_stats()` — scale-appropriate statistics (mode for Nominal, median for Ordinal, mean/std for Interval/Ratio).
- Extension: JSON output mode for use in downstream pipelines.
