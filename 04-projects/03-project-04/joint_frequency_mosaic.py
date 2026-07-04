"""
joint_frequency_mosaic.py
Chapter 3 — Multivariate Frequency Tables & Mosaic Plots
Demo dataset: Friends (Gender, Company, Food_pref)
"""

import sys

# ===== SECTION 1: IMPORTS =====
import csv
import math

# ===== SECTION 2: CONSTANTS =====
MISSING_MARKERS = ["", "NA", "N/A", "?", "null", "NULL", "nan", "NaN", "-"]

# ===== SECTION 3: DEMO DATASET =====
DEMO_DATA = [
    {"Friend": "Andrew",   "Gender": "M", "Company": "Good", "Food_pref": "Meat"},
    {"Friend": "Bernhard", "Gender": "M", "Company": "Good", "Food_pref": "Meat"},
    {"Friend": "Carolina", "Gender": "F", "Company": "Bad",  "Food_pref": "Vegetarian"},
    {"Friend": "Dennis",   "Gender": "M", "Company": "Good", "Food_pref": "Meat"},
    {"Friend": "Eve",      "Gender": "F", "Company": "Bad",  "Food_pref": "Vegetarian"},
    {"Friend": "Fred",     "Gender": "M", "Company": "Good", "Food_pref": "Mixed"},
    {"Friend": "Gwyneth",  "Gender": "F", "Company": "Bad",  "Food_pref": "Mixed"},
    {"Friend": "Hayden",   "Gender": "F", "Company": "Bad",  "Food_pref": "Vegetarian"},
    {"Friend": "Irene",    "Gender": "F", "Company": "Bad",  "Food_pref": "Vegetarian"},
    {"Friend": "James",    "Gender": "M", "Company": "Good", "Food_pref": "Meat"},
    {"Friend": "Kevin",    "Gender": "M", "Company": "Bad",  "Food_pref": "Meat"},
    {"Friend": "Lea",      "Gender": "F", "Company": "Good", "Food_pref": "Mixed"},
    {"Friend": "Marcus",   "Gender": "M", "Company": "Bad",  "Food_pref": "Vegetarian"},
    {"Friend": "Nigel",    "Gender": "M", "Company": "Good", "Food_pref": "Meat"},
]

# ===== SECTION 4: HELPER FUNCTIONS =====

def is_missing(val):
    """Return True if val is considered a missing/NA marker."""
    return str(val).strip() in MISSING_MARKERS


def get_unique_values(values_list):
    """
    Return a sorted list of unique non-missing values from values_list.
    Sorting is alphabetical (works for strings and numbers).
    """
    seen = set()
    for v in values_list:
        if not is_missing(v):
            seen.add(v)
    unique = list(seen)
    unique.sort()
    return unique


# ===== SECTION 5: CORE ANALYSIS =====

def build_joint_frequency_table(col_a_values, col_b_values):
    """
    Build a 2D joint frequency (cross-tabulation) table.

    Parameters
    ----------
    col_a_values : list  — values for attribute A  (rows)
    col_b_values : list  — values for attribute B  (columns)

    Returns
    -------
    counts_dict  : dict { val_a: { val_b: int } }
    row_totals   : dict { val_a: int }
    col_totals   : dict { val_b: int }
    grand_total  : int
    """
    unique_a = get_unique_values(col_a_values)
    unique_b = get_unique_values(col_b_values)

    # Initialise all cells to zero
    counts_dict = {}
    for val_a in unique_a:
        counts_dict[val_a] = {}
        for val_b in unique_b:
            counts_dict[val_a][val_b] = 0

    row_totals = {}
    for val_a in unique_a:
        row_totals[val_a] = 0

    col_totals = {}
    for val_b in unique_b:
        col_totals[val_b] = 0

    grand_total = 0

    # Count each observation
    for i in range(len(col_a_values)):
        val_a = col_a_values[i]
        val_b = col_b_values[i]

        # Skip rows where either attribute is missing
        if is_missing(val_a) or is_missing(val_b):
            continue

        counts_dict[val_a][val_b] += 1
        row_totals[val_a] += 1
        col_totals[val_b] += 1
        grand_total += 1

    return counts_dict, row_totals, col_totals, grand_total


def build_relative_joint_table(counts_dict, grand_total):
    """
    Convert absolute joint counts to joint relative frequencies.
    relative[val_a][val_b] = count / grand_total

    Returns a dict with the same structure as counts_dict but float values.
    """
    relative = {}
    for val_a in counts_dict:
        relative[val_a] = {}
        for val_b in counts_dict[val_a]:
            if grand_total > 0:
                relative[val_a][val_b] = counts_dict[val_a][val_b] / grand_total
            else:
                relative[val_a][val_b] = 0.0
    return relative


def build_conditional_table(counts_dict, row_totals):
    """
    Build the conditional frequency table P(B = v | A = u).
    For each row u (value of A) and each column v (value of B):
        P(B=v | A=u) = count(A=u, B=v) / row_total(A=u)

    Returns a dict { val_a: { val_b: float } }
    """
    conditional = {}
    for val_a in counts_dict:
        conditional[val_a] = {}
        row_n = row_totals[val_a]
        for val_b in counts_dict[val_a]:
            if row_n > 0:
                conditional[val_a][val_b] = counts_dict[val_a][val_b] / row_n
            else:
                conditional[val_a][val_b] = 0.0
    return conditional


def build_3way_frequency(col_a, col_b, col_c):
    """
    Build a 3-way joint frequency table for three qualitative attributes.

    Returns nested dict { val_a: { val_b: { val_c: int } } }
    """
    unique_a = get_unique_values(col_a)
    unique_b = get_unique_values(col_b)
    unique_c = get_unique_values(col_c)

    # Initialise all cells to zero
    table = {}
    for val_a in unique_a:
        table[val_a] = {}
        for val_b in unique_b:
            table[val_a][val_b] = {}
            for val_c in unique_c:
                table[val_a][val_b][val_c] = 0

    # Count each observation
    for i in range(len(col_a)):
        va = col_a[i]
        vb = col_b[i]
        vc = col_c[i]

        if is_missing(va) or is_missing(vb) or is_missing(vc):
            continue

        table[va][vb][vc] += 1

    return table


# ===== SECTION 6: PRINTING / REPORTING =====

def print_joint_table(counts_dict, row_totals, col_totals, grand_total,
                      label_a, label_b, mode="absolute"):
    """
    Print a formatted ASCII cross-tabulation table.

    mode : "absolute"   — raw counts
           "relative"   — fractions (counts_dict should already be floats)
           "percent"    — multiply relative by 100
    """
    unique_a = sorted(counts_dict.keys())
    # Derive unique_b from the first row's keys (all rows share same keys)
    unique_b = sorted(counts_dict[unique_a[0]].keys())

    # Determine column widths
    header_label = "{} x {}".format(label_a, label_b)
    row_label_width = max(len(header_label), max(len(str(v)) for v in unique_a)) + 1

    col_widths = []
    for val_b in unique_b:
        w = max(len(str(val_b)), 6) + 2
        col_widths.append(w)
    total_col_width = max(len("Total"), 6) + 2

    # --- Header line ---
    header = "{:<{}}".format(header_label, row_label_width)
    for idx, val_b in enumerate(unique_b):
        header += "| {:<{}} ".format(str(val_b), col_widths[idx] - 3)
    header += "| {:<{}} ".format("Total", total_col_width - 3)

    separator = "-" * row_label_width
    for w in col_widths:
        separator += "+" + "-" * w
    separator += "+" + "-" * total_col_width

    title_mode = mode.capitalize()
    print()
    print("  [{} Joint Frequency Table]  {} x {}".format(title_mode, label_a, label_b))
    print(header)
    print(separator)

    # --- Data rows ---
    for val_a in unique_a:
        row_line = "{:<{}}".format(str(val_a), row_label_width)
        for idx, val_b in enumerate(unique_b):
            cell = counts_dict[val_a][val_b]
            if mode == "percent":
                cell_str = "{:.1f}%".format(cell * 100)
            elif mode == "relative":
                cell_str = "{:.4f}".format(cell)
            else:
                cell_str = str(cell)
            row_line += "| {:<{}} ".format(cell_str, col_widths[idx] - 3)

        # Row total
        rt = row_totals[val_a]
        if mode == "percent":
            rt_str = "{:.1f}%".format(rt * 100) if isinstance(rt, float) else str(rt)
        elif mode == "relative":
            rt_str = "{:.4f}".format(rt) if isinstance(rt, float) else str(rt)
        else:
            rt_str = str(rt)
        row_line += "| {:<{}} ".format(rt_str, total_col_width - 3)
        print(row_line)

    print(separator)

    # --- Column totals row ---
    tot_line = "{:<{}}".format("Total", row_label_width)
    for idx, val_b in enumerate(unique_b):
        ct = col_totals[val_b]
        if mode == "percent":
            ct_str = "{:.1f}%".format(ct * 100) if isinstance(ct, float) else str(ct)
        elif mode == "relative":
            ct_str = "{:.4f}".format(ct) if isinstance(ct, float) else str(ct)
        else:
            ct_str = str(ct)
        tot_line += "| {:<{}} ".format(ct_str, col_widths[idx] - 3)

    gt = grand_total
    if mode == "percent":
        gt_str = "{:.1f}%".format(gt * 100) if isinstance(gt, float) else str(gt)
    elif mode == "relative":
        gt_str = "{:.4f}".format(gt) if isinstance(gt, float) else str(gt)
    else:
        gt_str = str(gt)
    tot_line += "| {:<{}} ".format(gt_str, total_col_width - 3)
    print(tot_line)
    print()


def print_conditional_table(cond_dict, label_a, label_b):
    """
    Print the conditional frequency table P(B | A) as percentages.
    Each row sums to 100%.
    """
    unique_a = sorted(cond_dict.keys())
    unique_b = sorted(cond_dict[unique_a[0]].keys())

    header_label = "P({} | {})".format(label_b, label_a)
    row_label_width = max(len(header_label), max(len(str(v)) for v in unique_a)) + 1
    col_widths = []
    for val_b in unique_b:
        w = max(len(str(val_b)), 8) + 2
        col_widths.append(w)

    print()
    print("  [Conditional Frequency Table]  P({} | {})".format(label_b, label_a))

    header = "{:<{}}".format(header_label, row_label_width)
    for idx, val_b in enumerate(unique_b):
        header += "| {:<{}} ".format(str(val_b), col_widths[idx] - 3)
    header += "| {:<8} ".format("Sum")

    separator = "-" * row_label_width
    for w in col_widths:
        separator += "+" + "-" * w
    separator += "+" + "-" * 10

    print(header)
    print(separator)

    for val_a in unique_a:
        row_line = "{:<{}}".format(str(val_a), row_label_width)
        row_sum = 0.0
        for idx, val_b in enumerate(unique_b):
            p = cond_dict[val_a][val_b]
            row_sum += p
            cell_str = "{:.1f}%".format(p * 100)
            row_line += "| {:<{}} ".format(cell_str, col_widths[idx] - 3)
        row_line += "| {:<8} ".format("{:.1f}%".format(row_sum * 100))
        print(row_line)

    print()


def print_3way_table(table_3way, label_a, label_b, label_c):
    """
    Print a 3-way frequency table as a set of 2D sub-tables,
    one sub-table per value of attribute A.
    """
    unique_a = sorted(table_3way.keys())

    print()
    print("  [3-Way Frequency Table]  {} x {} x {}".format(label_a, label_b, label_c))
    print("  (One sub-table per value of {})".format(label_a))

    for val_a in unique_a:
        subtable = table_3way[val_a]       # { val_b: { val_c: count } }
        unique_b = sorted(subtable.keys())
        unique_c = []
        # Collect unique_c from all val_b entries
        seen_c = set()
        for val_b in unique_b:
            for val_c in subtable[val_b]:
                seen_c.add(val_c)
        unique_c = sorted(seen_c)

        print()
        print("  --- {} = {} ---".format(label_a, val_a))

        # Header
        sub_header_label = "{} \\ {}".format(label_b, label_c)
        row_lw = max(len(sub_header_label), max(len(str(v)) for v in unique_b)) + 1
        col_ws = []
        for val_c in unique_c:
            col_ws.append(max(len(str(val_c)), 5) + 2)
        total_cw = max(len("Total"), 5) + 2

        hdr = "{:<{}}".format(sub_header_label, row_lw)
        for idx, val_c in enumerate(unique_c):
            hdr += "| {:<{}} ".format(str(val_c), col_ws[idx] - 3)
        hdr += "| {:<{}} ".format("Total", total_cw - 3)

        sep = "-" * row_lw
        for w in col_ws:
            sep += "+" + "-" * w
        sep += "+" + "-" * total_cw

        print(hdr)
        print(sep)

        for val_b in unique_b:
            row_total = 0
            row_line = "{:<{}}".format(str(val_b), row_lw)
            for idx, val_c in enumerate(unique_c):
                cnt = subtable[val_b][val_c]
                row_total += cnt
                row_line += "| {:<{}} ".format(str(cnt), col_ws[idx] - 3)
            row_line += "| {:<{}} ".format(str(row_total), total_cw - 3)
            print(row_line)

        print()


def print_ascii_mosaic(counts_dict, row_totals, col_totals, grand_total,
                       label_a, label_b, width=60, height=20):
    """
    Draw an ASCII mosaic plot for a 2D cross-tabulation.

    Layout
    ------
    - Columns correspond to values of attribute B (the column variable).
    - Column width is proportional to col_total / grand_total * width.
    - Within each column, segments correspond to values of attribute A (rows).
    - Segment height is proportional to count(A=u, B=v) / col_total(B=v) * height.
    - Different ASCII fill characters are used per row category.
    - Column labels are printed below the mosaic.
    - Row (segment) labels with percentages are printed on the right.
    """
    FILL_CHARS = ['#', '=', '-', '~', '+', '*', '@', '%']

    unique_a = sorted(counts_dict.keys())
    unique_b = sorted(counts_dict[unique_a[0]].keys())

    if grand_total == 0:
        print("  (No data to plot)")
        return

    # Assign a fill character to each val_a
    fill_map = {}
    for i, val_a in enumerate(unique_a):
        fill_map[val_a] = FILL_CHARS[i % len(FILL_CHARS)]

    # Compute pixel-column width for each val_b
    col_pixel_widths = []
    for val_b in unique_b:
        raw_w = col_totals[val_b] / grand_total * width
        col_pixel_widths.append(max(1, int(round(raw_w))))

    # Build the mosaic grid: list of columns, each column is list of rows (pixel chars)
    # grid[col_idx][row_pixel] = char
    grid_cols = []
    for col_idx, val_b in enumerate(unique_b):
        col_w = col_pixel_widths[col_idx]
        col_total_b = col_totals[val_b]

        # For each row val_a compute how many pixel-rows it occupies
        segment_heights = []
        for val_a in unique_a:
            if col_total_b > 0:
                raw_h = counts_dict[val_a][val_b] / col_total_b * height
            else:
                raw_h = 0.0
            segment_heights.append(raw_h)

        # Convert to integer pixel rows using floor, then distribute remainder
        int_heights = [int(math.floor(h)) for h in segment_heights]
        remainder = height - sum(int_heights)
        # Distribute remaining pixels to segments with largest fractional parts
        fractional_parts = []
        for idx, h in enumerate(segment_heights):
            fractional_parts.append((h - math.floor(h), idx))
        fractional_parts.sort(reverse=True)
        for k in range(remainder):
            int_heights[fractional_parts[k][1]] += 1

        # Build column pixel rows (from top = first val_a to bottom = last val_a)
        column_pixels = []
        for seg_idx, val_a in enumerate(unique_a):
            seg_h = int_heights[seg_idx]
            fill_ch = fill_map[val_a]
            for _ in range(seg_h):
                # Each pixel row is a string of width col_w
                column_pixels.append(fill_ch * col_w)

        # Pad to exactly height rows (should already be correct)
        while len(column_pixels) < height:
            column_pixels.append(' ' * col_w)

        grid_cols.append(column_pixels)

    # Now assemble and print row by row
    # We also want to annotate which row val_a a given pixel-row belongs to
    # Build a mapping: for each column, pixel_row -> val_a
    col_row_labels = []
    for col_idx, val_b in enumerate(unique_b):
        col_total_b = col_totals[val_b]
        segment_heights = []
        for val_a in unique_a:
            if col_total_b > 0:
                raw_h = counts_dict[val_a][val_b] / col_total_b * height
            else:
                raw_h = 0.0
            segment_heights.append(raw_h)
        int_heights_local = [int(math.floor(h)) for h in segment_heights]
        remainder_local = height - sum(int_heights_local)
        frac_parts_local = []
        for idx, h in enumerate(segment_heights):
            frac_parts_local.append((h - math.floor(h), idx))
        frac_parts_local.sort(reverse=True)
        for k in range(remainder_local):
            int_heights_local[frac_parts_local[k][1]] += 1

        row_label_list = []
        for seg_idx, val_a in enumerate(unique_a):
            seg_h = int_heights_local[seg_idx]
            for pixel in range(seg_h):
                row_label_list.append(val_a)
        while len(row_label_list) < height:
            row_label_list.append("")
        col_row_labels.append(row_label_list)

    # Determine the boundary pixel row for each (val_a, last column)
    # We will annotate the LAST row of each segment in the last column
    last_col_idx = len(unique_b) - 1
    last_col_row_labels = col_row_labels[last_col_idx]

    print()
    print("  MOSAIC: {} x {}".format(label_a, label_b))
    print("  " + "=" * (sum(col_pixel_widths) + len(unique_b) + 1))

    for pixel_row in range(height):
        # Build the mosaic line
        line = "  |"
        for col_idx in range(len(unique_b)):
            line += grid_cols[col_idx][pixel_row]
            line += "|"

        # Determine annotation: label the last pixel row of each val_a segment
        annotation = ""
        if pixel_row < len(last_col_row_labels):
            current_val_a = last_col_row_labels[pixel_row]
            # Check if this is the last pixel row for this val_a in the last column
            is_last_pixel = False
            if pixel_row == height - 1:
                is_last_pixel = True
            elif last_col_row_labels[pixel_row + 1] != current_val_a:
                is_last_pixel = True

            if is_last_pixel and current_val_a != "":
                # Compute the marginal percentage for this val_a
                pct = row_totals[current_val_a] / grand_total * 100
                annotation = "  {} ({:.1f}%)".format(current_val_a, pct)

        print(line + annotation)

    # Column labels at the bottom
    col_label_line = "  "
    for col_idx, val_b in enumerate(unique_b):
        w = col_pixel_widths[col_idx]
        # Centre the label within the column width (+1 for separator)
        col_label_line += " " + "{:^{}}".format(str(val_b), w)
    print(col_label_line)
    print()

    # Legend
    print("  Legend (row categories):")
    for val_a in unique_a:
        pct = row_totals[val_a] / grand_total * 100
        print("    '{}' = {} ({:.1f}%)".format(fill_map[val_a], val_a, pct))
    print()


# ===== SECTION 7: FILE I/O =====

def load_csv(csv_file):
    """
    Read a CSV file and return a column-oriented dictionary:
        { column_name: [value1, value2, ...], ... }
    Also returns the number of data rows (not counting the header).
    """
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if len(rows) == 0:
        raise ValueError("The CSV file is empty.")
    columns = {}
    for col_name in rows[0]:
        columns[col_name] = []
        for row in rows:
            columns[col_name].append(row[col_name])
    return columns, len(rows)


# ===== SECTION 8: MAIN =====

def extract_column(data_list, col_name):
    """Extract a single column from a list-of-dicts as a plain list."""
    result = []
    for row in data_list:
        result.append(row[col_name])
    return result


def run_demo():
    """Run the full analysis on the Friends demo dataset."""
    print()
    print("=" * 70)
    print("  DEMO: Friends Dataset  (n = {})".format(len(DEMO_DATA)))
    print("=" * 70)

    # Extract columns from demo data
    gender    = extract_column(DEMO_DATA, "Gender")
    company   = extract_column(DEMO_DATA, "Company")
    food_pref = extract_column(DEMO_DATA, "Food_pref")

    # ------------------------------------------------------------------
    # ANALYSIS 1: Gender x Company
    # ------------------------------------------------------------------
    print()
    print("─" * 70)
    print("  ANALYSIS 1: Gender x Company")
    print("─" * 70)

    counts, row_tots, col_tots, grand = build_joint_frequency_table(gender, company)

    # 1a. Absolute counts
    print_joint_table(counts, row_tots, col_tots, grand,
                      "Gender", "Company", mode="absolute")

    # 1b. Relative frequencies
    relative = build_relative_joint_table(counts, grand)
    # For printing relative we also need relative row/col totals
    rel_row_tots = {}
    for val_a in row_tots:
        rel_row_tots[val_a] = row_tots[val_a] / grand
    rel_col_tots = {}
    for val_b in col_tots:
        rel_col_tots[val_b] = col_tots[val_b] / grand
    rel_grand = 1.0
    print_joint_table(relative, rel_row_tots, rel_col_tots, rel_grand,
                      "Gender", "Company", mode="relative")

    # 1c. Conditional frequencies P(Company | Gender)
    conditional = build_conditional_table(counts, row_tots)
    print_conditional_table(conditional, "Gender", "Company")

    # 1d. ASCII mosaic
    print_ascii_mosaic(counts, row_tots, col_tots, grand,
                       "Gender", "Company", width=50, height=16)

    # ------------------------------------------------------------------
    # ANALYSIS 2: Gender x Food_pref
    # ------------------------------------------------------------------
    print()
    print("─" * 70)
    print("  ANALYSIS 2: Gender x Food_pref")
    print("─" * 70)

    counts2, row_tots2, col_tots2, grand2 = build_joint_frequency_table(
        gender, food_pref)

    # Absolute counts
    print_joint_table(counts2, row_tots2, col_tots2, grand2,
                      "Gender", "Food_pref", mode="absolute")

    # ASCII mosaic
    print_ascii_mosaic(counts2, row_tots2, col_tots2, grand2,
                       "Gender", "Food_pref", width=50, height=16)

    # ------------------------------------------------------------------
    # ANALYSIS 3: 3-Way — Gender x Company x Food_pref
    # ------------------------------------------------------------------
    print()
    print("─" * 70)
    print("  ANALYSIS 3: 3-Way  Gender x Company x Food_pref")
    print("─" * 70)

    table3 = build_3way_frequency(gender, company, food_pref)
    print_3way_table(table3, "Gender", "Company", "Food_pref")


def run_csv_analysis(csv_path):
    """Load a user-supplied CSV file and offer column-pair analysis."""
    print()
    print("  Loading CSV: {}".format(csv_path))
    try:
        columns, n_rows = load_csv(csv_path)
    except Exception as e:
        print("  ERROR loading file: {}".format(e))
        return

    col_names = list(columns.keys())
    print("  Rows loaded: {}".format(n_rows))
    print("  Columns found: {}".format(", ".join(col_names)))

    if len(col_names) < 2:
        print("  Need at least 2 columns for a joint frequency analysis.")
        return

    # Ask user for two columns
    print()
    for idx, name in enumerate(col_names):
        print("    [{}] {}".format(idx, name))

    try:
        idx_a = int(input("\n  Enter index of attribute A (rows): "))
        idx_b = int(input("  Enter index of attribute B (columns): "))
    except ValueError:
        print("  Invalid input — aborting CSV analysis.")
        return

    if idx_a < 0 or idx_a >= len(col_names) or idx_b < 0 or idx_b >= len(col_names):
        print("  Index out of range — aborting.")
        return

    label_a = col_names[idx_a]
    label_b = col_names[idx_b]
    col_a_vals = columns[label_a]
    col_b_vals = columns[label_b]

    counts, row_tots, col_tots, grand = build_joint_frequency_table(
        col_a_vals, col_b_vals)

    print_joint_table(counts, row_tots, col_tots, grand,
                      label_a, label_b, mode="absolute")

    relative = build_relative_joint_table(counts, grand)
    rel_row_tots = {}
    for val_a in row_tots:
        rel_row_tots[val_a] = row_tots[val_a] / grand if grand > 0 else 0.0
    rel_col_tots = {}
    for val_b in col_tots:
        rel_col_tots[val_b] = col_tots[val_b] / grand if grand > 0 else 0.0
    print_joint_table(relative, rel_row_tots, rel_col_tots, 1.0,
                      label_a, label_b, mode="relative")

    conditional = build_conditional_table(counts, row_tots)
    print_conditional_table(conditional, label_a, label_b)

    print_ascii_mosaic(counts, row_tots, col_tots, grand,
                       label_a, label_b, width=50, height=16)

    # Optional 3-way if user wants a third column
    try:
        choice = input("  Add a third attribute for 3-way table? (y/n): ").strip().lower()
    except EOFError:
        choice = "n"

    if choice == "y":
        for idx, name in enumerate(col_names):
            print("    [{}] {}".format(idx, name))
        try:
            idx_c = int(input("  Enter index of attribute C: "))
        except ValueError:
            print("  Invalid input.")
            return
        if idx_c < 0 or idx_c >= len(col_names):
            print("  Index out of range.")
            return
        label_c = col_names[idx_c]
        col_c_vals = columns[label_c]
        table3 = build_3way_frequency(col_a_vals, col_b_vals, col_c_vals)
        print_3way_table(table3, label_a, label_b, label_c)


if __name__ == "__main__":
    # Always run the demo first
    run_demo()

    # If a CSV path was provided as a command-line argument, analyse it too
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
        print()
        print("=" * 70)
        print("  CSV FILE ANALYSIS")
        print("=" * 70)
        run_csv_analysis(csv_path)
