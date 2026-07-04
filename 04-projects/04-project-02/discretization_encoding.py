"""
Chapter 04
04-03-project-02: Discretization & Encoding
=============================================
Demonstrates converting continuous and ordinal data into discrete codes:
  - Equal-width binning (uniform bin boundaries)
  - Equal-depth binning (equal count per bin)
  - One-hot encoding (nominal -> binary columns)
  - Natural number encoding (ordinal -> integers)
  - Gray code encoding (ordinal -> bit-flip-minimized binary)
  - Thermometer code encoding (ordinal -> cumulative binary)

Solves exercise questions Q1, Q2, Q3 explicitly.

Concepts: Ch.4 discretization, scale type conversions

Usage:
    python discretization_encoding.py
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys    # not used in demo but included for load_csv file mode
import csv    # read CSV files
import math   # math.log2 for bit-width calculation


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# Exercise Q1 data from the lecture (ex04)
EX_Q1_DATA = [31, 38, 42, 29, 46, 23, 83, 43, 51, 55, 27, 35]

# Exercise Q2 data: Food column (first 5 rows)
EX_Q2_FOOD = ["Chinese", "Italian", "American", "Chinese", "Italian"]

# Exercise Q3 data: Distance ordinal column
EX_Q3_DISTANCE_ORDERED = ["very_close", "close", "far", "very_far", "too_far"]
EX_Q3_DISTANCE_SAMPLE  = ["far", "very_close", "too_far", "close", "very_far"]


# ============================================================
# 3. DEMO DATASET (not used in exercise demo, but available)
# ============================================================

# A small dataset for demonstration of encoding pipelines
DEMO_DATA = {
    "name":     ["Rachel", "Monica", "Joey", "Chandler", "Phoebe",
                 "Ross", "Richard", "Gunther", "Janice", "Mike"],
    "food_pref": ["Italian", "American", "American", "Chinese", "Italian",
                  "American", "Italian", "Chinese", "American", "Italian"],
    "travel_dist": ["far", "very_close", "too_far", "close", "very_far",
                    "close", "far", "very_close", "close", "far"],
    "income":   [54000, 72000, 41000, 83000, 38000,
                 95000, 61000, 29000, 47000, 88000],
}


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def int_to_gray_code(n, n_bits):
    """
    Convert a non-negative integer n to its Gray code as a binary string.

    Gray code rule: gray = n XOR (n right-shifted by 1)
    This ensures consecutive integers differ by exactly 1 bit.

    Parameters:
        n      : non-negative integer to convert
        n_bits : total number of bits in the output string (zero-padded on left)

    Example:
        int_to_gray_code(3, 3) -> "010"
        int_to_gray_code(4, 3) -> "110"
    """
    gray_int = n ^ (n >> 1)   # XOR n with n right-shifted by 1
    # Convert to binary string, remove "0b" prefix, zero-pad to n_bits
    binary_str = bin(gray_int)[2:]          # e.g. "11" for gray_int=3
    padded = binary_str.zfill(n_bits)       # e.g. "011" for n_bits=3
    return padded


def int_to_thermometer_code(n, n_bits):
    """
    Convert an integer n (0-indexed rank) to thermometer code as a binary string.

    Thermometer code: the n-th category has n ones followed by (n_bits - n) zeros.
    Fills from LEFT to RIGHT.

    Examples (n_bits=3):
        n=0 -> "000"
        n=1 -> "001"
        n=2 -> "011"
        n=3 -> "111"

    Note: n must be <= n_bits.
    """
    # n ones at the right, rest zeros
    # E.g. n=2, n_bits=3: "011"
    ones_part  = "1" * n                     # n ones
    zeros_part = "0" * (n_bits - n)          # remaining zeros
    return zeros_part + ones_part            # zeros first (left), ones fill from right


def required_bits(n_categories):
    """
    Compute the minimum number of bits needed to represent n_categories values.

    For Gray code: need ceil(log2(n_categories)) bits.
    For thermometer code: need exactly (n_categories - 1) bits.

    Returns the larger of the two so one function covers both.
    """
    if n_categories <= 1:
        return 1
    gray_bits = math.ceil(math.log2(n_categories))  # ceil(log2) for gray
    therm_bits = n_categories - 1                    # n-1 bits for thermometer
    return max(gray_bits, therm_bits)


# ============================================================
# 5. CORE FUNCTIONS
# ============================================================

def equal_width_bins(values, n_bins):
    """
    Assign each value in 'values' to an equal-width bin (0-indexed).

    Bin width: W = (max_val - min_val) / n_bins
    Bin k covers: [min_val + k*W, min_val + (k+1)*W)
    The last bin is closed on the right: includes max_val.

    Returns:
        bin_labels  : list of bin indices (integers), one per value
        bin_edges   : list of n_bins+1 boundary values (the edges)

    Parameters:
        values  : list of numeric values
        n_bins  : number of equal-width bins to create
    """
    min_val = min(values)
    max_val = max(values)
    width   = (max_val - min_val) / n_bins

    # Compute the edges: n_bins+1 values
    bin_edges = []
    for k in range(n_bins + 1):
        edge = min_val + k * width
        bin_edges.append(edge)

    bin_labels = []
    for v in values:
        assigned = -1
        for k in range(n_bins):
            left  = bin_edges[k]
            right = bin_edges[k + 1]
            # Last bin: include the right edge (max value)
            if k == n_bins - 1:
                if left <= v <= right:
                    assigned = k
                    break
            else:
                if left <= v < right:
                    assigned = k
                    break
        if assigned == -1:
            # Fallback: clamp to last bin (handles floating-point edge cases)
            assigned = n_bins - 1
        bin_labels.append(assigned)

    return bin_labels, bin_edges


def equal_depth_bins(values, n_bins):
    """
    Assign each value in 'values' to an equal-depth (equal-frequency) bin.

    Steps:
      1. Sort values with their original indices
      2. Distribute into n_bins groups of approximately equal size
      3. Map each original index back to its bin label

    Returns:
        bin_labels : list of bin indices (integers), one per value in original order

    Parameters:
        values  : list of numeric values
        n_bins  : number of bins; each will contain floor(len/n_bins) values
    """
    n = len(values)

    # Sort values keeping track of original positions
    indexed = []
    for i in range(n):
        indexed.append((values[i], i))
    # Sort by the value (first element of each tuple).
    # We use a small helper instead of a lambda to stay beginner-friendly.
    def get_value(pair):
        return pair[0]
    indexed.sort(key=get_value)

    # Assign bin labels in sorted order
    bin_labels_sorted = []
    for rank in range(n):
        # Which bin does this sorted position belong to?
        bin_index = int(rank * n_bins / n)
        # Clamp to [0, n_bins-1] to avoid off-by-one at the last position
        if bin_index >= n_bins:
            bin_index = n_bins - 1
        bin_labels_sorted.append(bin_index)

    # Map back to original order
    bin_labels_original = [0] * n
    for sorted_rank in range(n):
        original_idx = indexed[sorted_rank][1]
        bin_labels_original[original_idx] = bin_labels_sorted[sorted_rank]

    return bin_labels_original


def one_hot_encode(values):
    """
    One-hot encode a list of nominal (categorical) string values.

    Steps:
      1. Find all unique categories (sorted alphabetically for stability)
      2. For each value, create a binary vector: 1 at the category's position, 0 elsewhere
      3. Return the category list and the encoded vectors

    Returns:
        categories : sorted list of unique category strings
        encoded    : list of lists, each inner list is a binary vector for one row

    Example:
        values     = ["Chinese", "Italian", "American"]
        categories = ["American", "Chinese", "Italian"]
        encoded    = [[0,1,0], [0,0,1], [1,0,0]]
    """
    # Step 1: find all unique categories in sorted order
    unique_set = set()
    for v in values:
        unique_set.add(v)
    categories = sorted(list(unique_set))

    # Step 2: encode each value
    encoded = []
    for v in values:
        row_vector = []
        for cat in categories:
            if v == cat:
                row_vector.append(1)
            else:
                row_vector.append(0)
        encoded.append(row_vector)

    return categories, encoded


def ordinal_to_natural(values, ordered_categories):
    """
    Map ordinal categories to natural numbers 0, 1, 2, ...

    The position in 'ordered_categories' determines the integer code.

    Returns:
        A list of integers, one per value in 'values'.

    Parameters:
        values             : list of category strings to encode
        ordered_categories : list of category strings in ascending order
    """
    # Build a lookup: category -> integer
    rank_map = {}
    for i in range(len(ordered_categories)):
        rank_map[ordered_categories[i]] = i

    result = []
    for v in values:
        result.append(rank_map[v])
    return result


def ordinal_to_gray_code(values, ordered_categories):
    """
    Map ordinal categories to Gray code binary strings.

    Gray code: consecutive integers differ by exactly 1 bit.
    Construction: gray = n XOR (n >> 1)

    Returns:
        A list of binary string codes, one per value.

    Parameters:
        values             : list of category strings to encode
        ordered_categories : list of category strings in ascending order
    """
    n_cats = len(ordered_categories)
    n_bits = math.ceil(math.log2(max(n_cats, 2)))  # bits needed

    rank_map = {}
    for i in range(n_cats):
        rank_map[ordered_categories[i]] = i

    result = []
    for v in values:
        rank = rank_map[v]
        result.append(int_to_gray_code(rank, n_bits))
    return result


def ordinal_to_thermometer(values, ordered_categories):
    """
    Map ordinal categories to thermometer (unary) binary strings.

    Thermometer code: n-th category has n ones from the right.
      rank 0 -> 000...0
      rank 1 -> 000...1
      rank 2 -> 000..11
      rank k -> k ones on the right, rest zeros

    Number of bits = len(ordered_categories) - 1

    Returns:
        A list of binary string codes, one per value.

    Parameters:
        values             : list of category strings to encode
        ordered_categories : list of category strings in ascending order
    """
    n_cats = len(ordered_categories)
    n_bits = n_cats - 1   # thermometer needs exactly n-1 bits for n categories

    rank_map = {}
    for i in range(n_cats):
        rank_map[ordered_categories[i]] = i

    result = []
    for v in values:
        rank = rank_map[v]
        result.append(int_to_thermometer_code(rank, n_bits))
    return result


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def separator(char="-", width=70):
    """Print a horizontal separator line."""
    print(char * width)


def print_bins_table(values, bin_labels, bin_edges, title):
    """
    Print a table showing each value and its assigned bin,
    along with the bin boundary definitions.
    """
    print("\n  " + title)
    separator(".")

    # Print bin boundaries first
    n_bins = len(bin_edges) - 1
    print("  Bin boundaries:")
    for k in range(n_bins):
        left  = bin_edges[k]
        right = bin_edges[k + 1]
        # Collect values in this bin
        vals_in_bin = []
        for i in range(len(values)):
            if bin_labels[i] == k:
                vals_in_bin.append(values[i])
        vals_str = str(sorted(vals_in_bin))
        print("    Bin {}: [{:.0f}, {:.0f}]  ->  {}".format(k, left, right, vals_str))

    # Print per-value assignment
    print("\n  Value -> Bin assignments:")
    print("  {:>6}  {:>5}".format("Value", "Bin"))
    for i in range(len(values)):
        print("  {:>6}  {:>5}".format(values[i], bin_labels[i]))


def print_depth_bins_table(values, bin_labels, title):
    """
    Print a table for equal-depth binning results.
    """
    print("\n  " + title)
    separator(".")

    n_bins = max(bin_labels) + 1

    for k in range(n_bins):
        vals_in_bin = []
        for i in range(len(values)):
            if bin_labels[i] == k:
                vals_in_bin.append(values[i])
        print("    Bin {}: {}".format(k, sorted(vals_in_bin)))

    print("\n  Value -> Bin assignments:")
    print("  {:>6}  {:>5}".format("Value", "Bin"))
    for i in range(len(values)):
        print("  {:>6}  {:>5}".format(values[i], bin_labels[i]))


def print_one_hot_table(values, categories, encoded, title):
    """
    Print a formatted one-hot encoding table.
    """
    print("\n  " + title)
    separator(".")

    # Header
    header = "  {:<12}".format("Value")
    for cat in categories:
        header = header + "  {:>10}".format(cat)
    print(header)
    separator(".", 70)

    for i in range(len(values)):
        row_str = "  {:<12}".format(values[i])
        for bit in encoded[i]:
            row_str = row_str + "  {:>10}".format(bit)
        print(row_str)


def print_ordinal_encoding_table(categories, nat_codes, gray_codes, therm_codes, title):
    """
    Print a table showing all three ordinal encoding schemes side by side.
    """
    print("\n  " + title)
    separator(".")
    print("  {:<12}  {:>8}  {:>10}  {:>16}".format(
        "Category", "Natural", "Gray", "Thermometer"))
    separator(".", 70)
    for i in range(len(categories)):
        print("  {:<12}  {:>8}  {:>10}  {:>16}".format(
            categories[i], nat_codes[i], gray_codes[i], therm_codes[i]))


# ============================================================
# 7. FILE I/O FUNCTIONS
# ============================================================

def load_csv(csv_file):
    """
    Read a CSV file and return a column-oriented dictionary.

    Returns:
        columns : dict {column_name: [value1, value2, ...]}
        n_rows  : number of data rows (not counting the header)

    CSV files are row-oriented (each line = one record).
    We pivot to column-oriented because most analysis works column by column.

    Before: rows = [{"age": "25", "name": "Alice"}, {"age": "30", "name": "Bob"}]
    After:  columns = {"age": ["25", "30"], "name": ["Alice", "Bob"]}
    """
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if len(rows) == 0:
        raise ValueError("The CSV file is empty.")

    # Pivot from row-oriented to column-oriented
    columns = {}
    for col_name in rows[0]:
        columns[col_name] = []
        for row in rows:
            columns[col_name].append(row[col_name])

    return columns, len(rows)


# ============================================================
# 8. MAIN PROGRAM
# ============================================================

def run_demo():
    """
    Solve exercise questions Q1, Q2, Q3 and print Expected vs. Computed.
    """
    separator("=")
    print("  DISCRETIZATION & ENCODING -- Chapter 4 Demo")
    print("  Solving Exercise Q1, Q2, Q3")
    separator("=")

    # --------------------------------------------------
    # Q1: Equal-Width Binning
    # --------------------------------------------------
    separator("=")
    print("  EXERCISE Q1 -- Equal-Width Binning (4 bins)")
    print("  Data: {}".format(EX_Q1_DATA))
    separator("=")

    ew_labels, ew_edges = equal_width_bins(EX_Q1_DATA, n_bins=4)

    print_bins_table(EX_Q1_DATA, ew_labels, ew_edges, "Equal-Width Bins (computed)")

    # Compare with expected answer
    # Expected bin labels from lecture: bins [23-37], [38-52], [53-67], [68-83]
    # Values:  31,38,42,29,46,23,83,43,51,55,27,35
    # Labels:   0, 1, 1, 0, 1, 0, 3, 1, 1, 2, 0, 0
    expected_ew = [0, 1, 1, 0, 1, 0, 3, 1, 1, 2, 0, 0]
    print("\n  Verification:")
    print("  Expected labels : {}".format(expected_ew))
    print("  Computed labels : {}".format(ew_labels))
    match_ew = (ew_labels == expected_ew)
    print("  Match: {}".format("YES" if match_ew else "CHECK -- small diffs may be boundary convention"))

    # --------------------------------------------------
    # Q1: Equal-Depth Binning
    # --------------------------------------------------
    separator("=")
    print("  EXERCISE Q1 -- Equal-Depth Binning (4 bins)")
    print("  Data: {}".format(EX_Q1_DATA))
    separator("=")

    ed_labels = equal_depth_bins(EX_Q1_DATA, n_bins=4)

    print_depth_bins_table(EX_Q1_DATA, ed_labels, "Equal-Depth Bins (computed)")

    # Expected from lecture:
    # Sorted: 23,27,29,31,35,38,42,43,46,51,55,83
    # Bin 0: {23,27,29}, Bin 1: {31,35,38}, Bin 2: {42,43,46}, Bin 3: {51,55,83}
    # Original order: 31,38,42,29,46,23,83,43,51,55,27,35
    # Labels:          1, 1, 2, 0, 2, 0, 3, 2, 3, 3, 0, 1
    expected_ed = [1, 1, 2, 0, 2, 0, 3, 2, 3, 3, 0, 1]
    print("\n  Verification:")
    print("  Expected labels : {}".format(expected_ed))
    print("  Computed labels : {}".format(ed_labels))
    match_ed = (ed_labels == expected_ed)
    print("  Match: {}".format("YES" if match_ed else "NO"))

    # --------------------------------------------------
    # Q2: One-Hot Encoding
    # --------------------------------------------------
    separator("=")
    print("  EXERCISE Q2 -- One-Hot Encoding")
    print("  Food column: {}".format(EX_Q2_FOOD))
    separator("=")

    # All unique categories from the exercise (American, Chinese, Italian, Other)
    # We add "Other" explicitly since it doesn't appear in the 5 rows but is a category
    all_food_cats = ["American", "Chinese", "Italian", "Other"]

    # Encode using only the values present (the categories determine the columns)
    categories_q2, encoded_q2 = one_hot_encode(EX_Q2_FOOD)
    print_one_hot_table(EX_Q2_FOOD, categories_q2, encoded_q2, "One-Hot Encoding (computed)")

    # Expected from lecture:
    # Categories sorted: American, Chinese, Italian
    # (Other does not appear in the 5 rows, so no column for it from these rows)
    expected_q2 = {
        "Chinese":  [0, 1, 0],
        "Italian":  [0, 0, 1],
        "American": [1, 0, 0],
    }
    print("\n  Verification (expected for categories: {})".format(categories_q2))
    all_match_q2 = True
    for i in range(len(EX_Q2_FOOD)):
        food = EX_Q2_FOOD[i]
        computed = encoded_q2[i]
        expected = expected_q2.get(food, None)
        if expected is not None:
            match = (computed == expected)
            if not match:
                all_match_q2 = False
            print("    {:<10}  Expected: {}  Got: {}  Match: {}".format(
                food, expected, computed, "YES" if match else "NO"))
    print("  Overall match: {}".format("YES" if all_match_q2 else "NO"))

    # --------------------------------------------------
    # Q3: Gray Code Encoding
    # --------------------------------------------------
    separator("=")
    print("  EXERCISE Q3 -- Gray Code for Distance")
    print("  Ordered categories: {}".format(EX_Q3_DISTANCE_ORDERED))
    separator("=")

    gray_codes_q3 = ordinal_to_gray_code(EX_Q3_DISTANCE_ORDERED, EX_Q3_DISTANCE_ORDERED)
    nat_codes_q3  = ordinal_to_natural(EX_Q3_DISTANCE_ORDERED, EX_Q3_DISTANCE_ORDERED)
    therm_codes_q3 = ordinal_to_thermometer(EX_Q3_DISTANCE_ORDERED, EX_Q3_DISTANCE_ORDERED)

    print_ordinal_encoding_table(
        EX_Q3_DISTANCE_ORDERED, nat_codes_q3, gray_codes_q3, therm_codes_q3,
        "Ordinal Encoding Table (computed)")

    # Expected from lecture:
    # very_close=000, close=001, far=011, very_far=010, too_far=110
    expected_gray_q3 = {
        "very_close": "000",
        "close":      "001",
        "far":        "011",
        "very_far":   "010",
        "too_far":    "110",
    }
    print("\n  Verification (Gray codes):")
    all_match_q3 = True
    for i in range(len(EX_Q3_DISTANCE_ORDERED)):
        cat = EX_Q3_DISTANCE_ORDERED[i]
        computed = gray_codes_q3[i]
        expected = expected_gray_q3[cat]
        match = (computed == expected)
        if not match:
            all_match_q3 = False
        print("    {:<12}  Expected: {}  Got: {}  Match: {}".format(
            cat, expected, computed, "YES" if match else "NO"))
    print("  Overall match: {}".format("YES" if all_match_q3 else "NO"))

    # --------------------------------------------------
    # BONUS: Encode the sample Distance column using all three methods
    # --------------------------------------------------
    separator("=")
    print("  BONUS: Encode Distance sample column using all 3 methods")
    print("  Sample: {}".format(EX_Q3_DISTANCE_SAMPLE))
    separator("=")

    nat_sample   = ordinal_to_natural(EX_Q3_DISTANCE_SAMPLE, EX_Q3_DISTANCE_ORDERED)
    gray_sample  = ordinal_to_gray_code(EX_Q3_DISTANCE_SAMPLE, EX_Q3_DISTANCE_ORDERED)
    therm_sample = ordinal_to_thermometer(EX_Q3_DISTANCE_SAMPLE, EX_Q3_DISTANCE_ORDERED)

    print("  {:<12}  {:>8}  {:>10}  {:>16}".format("Distance", "Natural", "Gray", "Thermometer"))
    separator(".", 70)
    for i in range(len(EX_Q3_DISTANCE_SAMPLE)):
        print("  {:<12}  {:>8}  {:>10}  {:>16}".format(
            EX_Q3_DISTANCE_SAMPLE[i], nat_sample[i], gray_sample[i], therm_sample[i]))

    # --------------------------------------------------
    # BONUS: Encode the demo dataset food_pref column
    # --------------------------------------------------
    separator("=")
    print("  BONUS: One-Hot Encode FRIENDS food_pref column")
    separator("=")

    food_pref = DEMO_DATA["food_pref"]
    cats_food, encoded_food = one_hot_encode(food_pref)
    print_one_hot_table(food_pref, cats_food, encoded_food, "FRIENDS food_pref encoding")

    separator("=")
    print("  Demo complete.")
    separator("=")


if __name__ == "__main__":
    run_demo()
