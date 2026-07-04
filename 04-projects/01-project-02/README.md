# Ch.01 Mini Project 02 — Dataset Type Explorer

**Concept:** Ch.1 data structure taxonomy — Record, Data Matrix, Document, Transaction, Graph, and Ordered data. Each has a characteristic shape that can be detected from column names and value patterns.

## What it does

Given any CSV file, `dataset_type_explorer.py` will:

1. **Classify the dataset** into one of the six Ch.1 structure types
2. **Report confidence level** (High / Medium) and the evidence behind the decision
3. **Show a column-type breakdown** (numeric vs. text columns)
4. **Print a structure preview** — first few rows in aligned columns
5. **Link the result back to Ch.1** with a short reference note

## Detection Logic (priority order)

| Priority | Signal | Detected Type |
|----------|--------|---------------|
| 1 | Column name contains graph keywords (source, target, node, edge) | Graph Data |
| 2 | Column name contains time/sequence keywords (date, timestamp, year) | Ordered Data |
| 3 | ≥70% of columns are binary (0/1) and ≥5 columns | Transaction Data |
| 4 | ≥70% of columns have word-like names AND numeric values | Document Data |
| 5 | All columns are numeric | Data Matrix |
| 6 | (fallback) mixed types, no structure detected | Record Data |

## Usage

```bash
# Run the built-in demo (four types shown back-to-back)
python dataset_type_explorer.py

# Classify your own CSV
python dataset_type_explorer.py my_dataset.csv
```

No external dependencies — pure Python 3 standard library only.

## Sample Output

```
================================================================================
  DATASET TYPE EXPLORER
  Source  : Demo: Transaction Data (binary item matrix)
  Rows    : 5   |   Columns: 5
================================================================================

  Detected Type : Transaction Data
  Confidence    : High
  Shape         : 5 transactions, 5 items (columns).

  Evidence:
    - 5/5 columns are binary (0/1) - looks like item-presence flags.
    - Wide binary layout is characteristic of transaction/basket data.

  Column breakdown:
    Numeric  ##### 5
    Text      0
--------------------------------------------------------------------------------
  Structure Preview:

  milk            bread           butter          eggs            juice
  ...
```

## Key Concepts from Ch.1 Applied

| Concept | Where it appears |
|---------|-----------------|
| Six data structure types | `classify_dataset()` return value |
| Binary / numeric detection | `_is_binary_col()`, `_is_numeric_col()` |
| Graph keyword matching | `GRAPH_KEYWORDS` set |
| Time/order detection | `ORDERED_KEYWORDS` set |
| Structure preview | `visualize_structure()` |

## Limitations & Future Ideas

- Detection is **heuristic** — verify manually for real datasets.
- Graph Data requires edge-list format (source/target columns); adjacency matrices are classified as Data Matrix.
- Extension: detect genomic data (columns named A, T, C, G or single-character values from {A,T,C,G}).
- Extension: output a confidence score (0–100%) instead of High/Medium.
