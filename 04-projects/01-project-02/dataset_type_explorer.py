"""
Chapter 01
01-03-project-02: Dataset Type Explorer
========================================
Given a CSV file, classify it as one of the six Ch.1 data structure types:

  Record Data      -- fixed attribute set per row; mixed types
  Data Matrix      -- all-numeric records; representable as m x n matrix
  Document Data    -- term-frequency vectors; column names are vocabulary words
  Transaction Data -- variable-length item sets; wide binary (0/1) layout
  Graph Data       -- objects are nodes, relationships are edges
  Ordered Data     -- records indexed by time or sequence position

Concepts: Ch.1 section on Data Structures -- each type has a characteristic
shape that can be detected from column names and value patterns.

Usage:
    python dataset_type_explorer.py                  (runs built-in demo)
    python dataset_type_explorer.py <path_to_csv>    (classifies any CSV)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys   # command-line arguments and exit
import csv   # read CSV files


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# Keywords that suggest temporal / sequential ordering in column names
ORDERED_KEYWORDS = {
    "date",
    "time",
    "timestamp",
    "year",
    "month",
    "day",
    "week",
    "hour",
    "minute",
    "second",
    "sequence",
    "seq",
    "step",
    "period",
    "quarter",
}

# Keywords that suggest an edge-list or node-link graph structure
GRAPH_KEYWORDS = {
    "source",
    "target",
    "from",
    "to",
    "node",
    "edge",
    "src",
    "dst",
    "origin",
    "destination",
    "vertex",
}


# ============================================================
# 3. DEMO DATASETS
# ============================================================

# One small dataset per detectable type, so we can showcase all six types.
DEMO_DATASETS = {
    "Record Data (mixed types)": {
        "Name":       ["Alice", "Bob", "Carol", "Dave"],
        "Age":        ["30", "25", "35", "28"],
        "Department": ["HR", "Eng", "Eng", "Sales"],
        "Salary":     ["55000", "72000", "80000", "61000"],
        "Active":     ["1", "1", "0", "1"],
    },
    "Data Matrix (all numeric)": {
        "sepal_length": ["5.1", "4.9", "4.7", "4.6"],
        "sepal_width":  ["3.5", "3.0", "3.2", "3.1"],
        "petal_length": ["1.4", "1.4", "1.3", "1.5"],
        "petal_width":  ["0.2", "0.2", "0.2", "0.2"],
    },
    "Transaction Data (binary item matrix)": {
        "milk":   ["1", "0", "1", "1", "0"],
        "bread":  ["1", "1", "0", "1", "1"],
        "butter": ["0", "1", "1", "0", "0"],
        "eggs":   ["1", "1", "0", "1", "1"],
        "juice":  ["0", "0", "1", "0", "1"],
    },
    "Ordered Data (time series)": {
        "timestamp":   ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
        "temperature": ["22.1", "23.5", "21.8", "24.0"],
        "humidity":    ["60", "62", "58", "65"],
    },
}


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def _is_numeric_col(values):
    """
    Return True if every non-missing value in the column parses as a float.

    Missing-value markers ("", "na", "nan", "null", "none", "?") are skipped.
    A column is numeric only if ALL non-missing values can be converted.
    """
    for v in values:
        v = v.strip()
        if not v or v.lower() in ("na", "nan", "null", "none", "?"):
            continue  # skip missing values
        try:
            float(v)
        except ValueError:
            return False  # found a non-numeric value -> entire column is not numeric
    return True


def _is_binary_col(values):
    """
    Return True if the column contains ONLY the values "0" and "1"
    (both must be present; missing values are ignored).

    This detects market-basket item-presence flags.
    """
    seen = set()
    for v in values:
        v = v.strip()
        if not v or v.lower() in ("na", "nan", "null", "none", "?"):
            continue  # skip missing
        if v not in ("0", "1"):
            return False  # found something other than 0 or 1
        seen.add(v)
    # Require both "0" and "1" to be present (not all-0 or all-1)
    return seen == {"0", "1"}


def _unique_ratio(values):
    """
    Return the fraction of non-missing values that are unique.

    Example: ["A", "B", "A", "C"] -> 3 unique out of 4 -> 0.75
    Used to gauge cardinality.
    """
    clean = []
    for v in values:
        if v.strip():
            clean.append(v.strip())
    if not clean:
        return 0.0
    return len(set(clean)) / len(clean)


def _looks_like_word(token):
    """
    Heuristic: does this column name look like a vocabulary term?

    A term in a document-term matrix is typically a single lowercase
    alphabetic word with no spaces, digits, or underscores.

    Examples:
        "apple"  -> True
        "Word"   -> False (uppercase)
        "age_1"  -> False (contains underscore/digit)
    """
    return token.isalpha() and token == token.lower()


def _has_keyword(col_names, keyword_set):
    """
    Return True if any column name contains at least one keyword
    from the given set (case-insensitive substring match).

    Example:
        col_names   = ["date", "value", "sensor_id"]
        keyword_set = {"date", "time"}
        -> True  (because "date" is in the set)
    """
    for name in col_names:
        for kw in keyword_set:
            if kw in name.lower():
                return True
    return False


# ============================================================
# 5. CORE ANALYSIS FUNCTIONS
# ============================================================

def classify_dataset(columns, n_rows):
    """
    Detect the most likely Ch.1 data structure type for this dataset.

    Detection order matters -- more specific signals are checked first
    so that a dataset with both a time column and all-numeric columns
    is correctly labelled "Ordered" rather than "Data Matrix".

    Returns a dict:
        dataset_type   -- one of the six Ch.1 type names
        confidence     -- "High", "Medium", or "Low"
        evidence       -- list of human-readable reason strings
        structure_hint -- brief description of the detected shape
    """
    col_names     = list(columns.keys())
    n_cols        = len(col_names)
    values_by_col = columns   # alias for clarity

    evidence = []

    # ------------------------------------------------------------------
    # 1. Graph Data -- explicit source/target edge columns
    # ------------------------------------------------------------------
    # A graph CSV typically has columns like "source"+"target" or "from"+"to".
    # This is the most structurally distinctive type, so check it first.
    if _has_keyword(col_names, GRAPH_KEYWORDS):
        evidence.append(
            "Column names suggest node/edge structure (source, target, node, etc.)."
        )
        return {
            "dataset_type":   "Graph Data",
            "confidence":     "Medium",
            "evidence":       evidence,
            "structure_hint": f"{n_rows} rows (edges/nodes), {n_cols} columns.",
        }

    # ------------------------------------------------------------------
    # 2. Ordered / Sequential Data -- time or sequence index column
    # ------------------------------------------------------------------
    # Any dataset with a time/sequence index is Ordered.
    # Checked before Record/Matrix because ordered data can otherwise
    # look like a plain record table.
    if _has_keyword(col_names, ORDERED_KEYWORDS):
        evidence.append(
            "Time or sequence column detected -- data is indexed over time/order."
        )

        # Count how many columns match a time keyword for confidence level
        time_col_count = 0
        for name in col_names:
            for kw in ORDERED_KEYWORDS:
                if kw in name.lower():
                    time_col_count += 1
                    break

        if time_col_count >= 2:
            confidence = "High"
        else:
            confidence = "Medium"

        return {
            "dataset_type":   "Ordered Data",
            "confidence":     confidence,
            "evidence":       evidence,
            "structure_hint": f"{n_rows} ordered records, {n_cols} attributes.",
        }

    # ------------------------------------------------------------------
    # 3. Transaction Data -- wide binary matrix (items as columns)
    # ------------------------------------------------------------------
    # Classic market-basket format: each column is an item, each cell is 0/1.
    # Signal: majority of columns are binary AND there are many columns.
    binary_cols = 0
    for col, vals in values_by_col.items():
        if _is_binary_col(vals):
            binary_cols += 1

    binary_fraction = binary_cols / n_cols if n_cols > 0 else 0

    if binary_fraction >= 0.7 and n_cols >= 5:
        evidence.append(
            f"{binary_cols}/{n_cols} columns are binary (0/1) -- looks like item-presence flags."
        )
        evidence.append(
            "Wide binary layout is characteristic of transaction/basket data."
        )

        if binary_fraction >= 0.9:
            confidence = "High"
        else:
            confidence = "Medium"

        return {
            "dataset_type":   "Transaction Data",
            "confidence":     confidence,
            "evidence":       evidence,
            "structure_hint": f"{n_rows} transactions, {n_cols} items (columns).",
        }

    # ------------------------------------------------------------------
    # 4. Document Data -- word-like column names + numeric values
    # ------------------------------------------------------------------
    # A term-document matrix has single lowercase word column names and
    # non-negative integer counts as values.
    word_like_cols = 0
    for name in col_names:
        if _looks_like_word(name):
            word_like_cols += 1
    word_fraction = word_like_cols / n_cols if n_cols > 0 else 0

    numeric_cols = []
    for col, vals in values_by_col.items():
        if _is_numeric_col(vals):
            numeric_cols.append(col)
    all_numeric_fraction = len(numeric_cols) / n_cols if n_cols > 0 else 0

    if word_fraction >= 0.7 and all_numeric_fraction >= 0.7 and n_cols >= 5:
        evidence.append(
            f"{word_like_cols}/{n_cols} column names look like terms (single lowercase words)."
        )
        evidence.append("Numeric values in word columns suggest term-frequency counts.")
        return {
            "dataset_type":   "Document Data",
            "confidence":     "Medium",
            "evidence":       evidence,
            "structure_hint": f"{n_rows} documents, {n_cols} terms (vocabulary size).",
        }

    # ------------------------------------------------------------------
    # 5. Data Matrix -- all columns are numeric
    # ------------------------------------------------------------------
    # A data matrix is a special case of record data where every attribute
    # is numeric, making the whole table representable as an m x n matrix.
    if all_numeric_fraction == 1.0 and n_cols >= 2:
        evidence.append(
            f"All {n_cols} columns are numeric -> representable as a {n_rows} x {n_cols} matrix."
        )
        evidence.append(
            f"Each row is a point in {n_cols}-dimensional space."
        )
        return {
            "dataset_type":   "Data Matrix",
            "confidence":     "High",
            "evidence":       evidence,
            "structure_hint": f"{n_rows} x {n_cols} numeric matrix.",
        }

    # ------------------------------------------------------------------
    # 6. Record Data -- default fallback
    # ------------------------------------------------------------------
    # Mixed types, no special structure detected -> general record table.
    mixed_count = n_cols - len(numeric_cols)
    evidence.append(
        f"Mixed column types: {len(numeric_cols)} numeric, {mixed_count} non-numeric."
    )
    evidence.append(
        "Fixed attribute schema with no special ordering or structure detected."
    )
    return {
        "dataset_type":   "Record Data",
        "confidence":     "High",
        "evidence":       evidence,
        "structure_hint": f"{n_rows} records, {n_cols} attributes.",
    }


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def separator(char="-", width=80):
    """Print a horizontal line made of the given character."""
    print(char * width)


def print_report(columns, n_rows, source_name):
    """
    Print a formatted dataset-type detection report including:
      - Detected type and confidence
      - Evidence bullets explaining why that type was chosen
      - Column breakdown (numeric vs. text)
      - A Ch.1 note explaining the type
    """
    result = classify_dataset(columns, n_rows)

    separator("=")
    print(f"  DATASET TYPE EXPLORER")
    print(f"  Source  : {source_name}")
    print(f"  Rows    : {n_rows}   |   Columns: {len(columns)}")
    separator("=")

    print(f"\n  Detected Type : {result['dataset_type']}")
    print(f"  Confidence    : {result['confidence']}")
    print(f"  Shape         : {result['structure_hint']}\n")

    print("  Evidence:")
    for point in result["evidence"]:
        print(f"    - {point}")

    # Column-type breakdown (numeric vs. text)
    numeric_count = 0
    for vals in columns.values():
        if _is_numeric_col(vals):
            numeric_count += 1
    text_count = len(columns) - numeric_count

    print(f"\n  Column breakdown:")
    print(f"    Numeric  {'#' * numeric_count} {numeric_count}")
    print(f"    Text     {'#' * text_count} {text_count}")

    separator("-")

    # Brief explanation of what each type means in Ch.1 terms
    TYPE_NOTES = {
        "Record Data":     "Default tabular form -- fixed attribute set per row. (Ch.1 s4a)",
        "Data Matrix":     "All-numeric records -> m x n matrix; each row is a point in n-D space. (Ch.1 s4b)",
        "Document Data":   "Term-frequency vectors; attributes = vocabulary terms. (Ch.1 s4c)",
        "Transaction Data":"Variable-length item sets, often encoded as binary matrix. (Ch.1 s4d)",
        "Graph Data":      "Objects = nodes, relationships = edges. (Ch.1 s4e)",
        "Ordered Data":    "Records indexed by time or sequence position. (Ch.1 s4f)",
    }
    print(f"  Ch.1 Note: {TYPE_NOTES.get(result['dataset_type'], '')}\n")
    separator("=")
    print()


# ============================================================
# 7. FILE I/O FUNCTIONS
# ============================================================

def load_csv(csv_file):
    """
    Read a CSV file and return a column-oriented dictionary:
        { column_name: [value1, value2, ...], ... }

    Also returns the number of data rows (not counting the header).
    """
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # first row is automatically used as header
        rows = list(reader)

    if len(rows) == 0:
        raise ValueError("The CSV file is empty.")

    # Pivot from row-oriented to column-oriented
    # Before: rows = [{"Age": "25", "Name": "Alice"}, {"Age": "30", "Name": "Bob"}]
    # After:  columns = {"Age": ["25", "30"], "Name": ["Alice", "Bob"]}
    columns = {}
    for col_name in rows[0]:          # get column names from the first row
        columns[col_name] = []
        for row in rows:              # go through every data row
            columns[col_name].append(row[col_name])

    return columns, len(rows)


# ============================================================
# 8. MAIN PROGRAM
# ============================================================

def run_demo():
    """Run the built-in demo using one dataset per detectable type."""
    print("\n  [Running built-in demo datasets -- one per detectable type]\n")
    for name, data in DEMO_DATASETS.items():
        n = len(next(iter(data.values())))
        print_report(data, n, source_name=f"Demo: {name}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments: run all built-in demo datasets
        run_demo()
    else:
        # One argument: path to a CSV file to classify
        path = sys.argv[1]
        try:
            cols, n = load_csv(path)
            print_report(cols, n, source_name=path)
        except FileNotFoundError:
            print(f"Error: file '{path}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
