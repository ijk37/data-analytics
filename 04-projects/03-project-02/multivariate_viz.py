"""
Chapter 03
03-03-project-02: Multivariate Visualization
=============================================
Creates five types of multivariate visualizations using the Friends dataset:
  1. Parallel coordinates (profile plot) -- each object = polyline, colored by class
  2. Star plots (radar/spider charts)    -- one chart per object
  3. Bubble chart                        -- 4 attributes: x, y, size, color
  4. 3D scatter plot                     -- three quantitative attributes
  5. Heatmap                             -- color-coded grid (objects x attributes)

Concepts covered:
  Ch.3 - Parallel coordinates, star plots, bubble charts, 3D scatter,
          heatmaps, color/shape encoding for qualitative attributes

Dependencies: matplotlib  (pip install matplotlib)

Usage:
    python multivariate_viz.py          (built-in demo, all five plots)
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import sys   # command-line arguments and exit
import csv   # read CSV files
import math  # sqrt, pi, cos, sin

# Try to import matplotlib; fall back to text-only mode if not installed.
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: matplotlib not found.  Install with:  pip install matplotlib")
    print("Running in text-description mode.\n")


# ============================================================
# 2. CONSTANTS / CONFIGURATION
# ============================================================

# Values that count as "missing" and should be skipped
MISSING_MARKERS = ("", "na", "nan", "null", "none", "?")

# Color palette: maps class values to distinct colors
DEFAULT_COLORS = [
    "#e41a1c",   # red
    "#377eb8",   # blue
    "#4daf4a",   # green
    "#984ea3",   # purple
    "#ff7f00",   # orange
    "#a65628",   # brown
    "#f781bf",   # pink
]

# Marker styles for scatter/bubble plots
DEFAULT_MARKERS = ["o", "s", "^", "D", "v", "P", "*"]


# ============================================================
# 3. DEMO DATASET
# ============================================================

# The Friends dataset from the Ch.3 lecture slides.
# Stored as a column-oriented dict (same format as load_csv).
FRIENDS = {
    "Friend":   ["Andrew", "Bernhard", "Carolina", "Dennis", "Eve", "Fred",
                 "Gwyneth", "Hayden", "Irene", "James", "Kevin", "Lea",
                 "Marcus", "Nigel"],
    "Max_temp": [25, 31, 15, 20, 10, 12, 16, 26, 15, 21, 30, 13,  8, 12],
    "Weight":   [77,110, 70, 85, 65, 75, 75, 63, 55, 66, 95, 72, 83,115],
    "Height":   [175,195,172,180,168,173,180,165,158,163,190,172,185,192],
    "Years":    [10, 12,  2, 16,  0,  6,  3,  2,  5, 14,  1, 11,  3, 15],
    "Gender":   ["M", "M", "F", "M", "F", "M", "F", "F", "F", "M", "M",
                 "F", "F", "M"],
    "Company":  ["Good","Good","Bad","Good","Bad","Good","Bad","Bad",
                 "Bad","Good","Bad","Good","Bad","Good"],
}


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def parse_float(value):
    """
    Try to convert a value to float.
    Returns (float_value, True) on success, (None, False) on failure.
    """
    v = str(value).strip()
    if v.lower() in MISSING_MARKERS:
        return None, False
    try:
        return float(v), True
    except ValueError:
        return None, False


def normalize_column(values):
    """
    Min-max normalize a list of numeric values to the range [0, 1].
    This is needed for star plots and parallel coordinates so that
    attributes with different units are all on the same scale.

    Formula: normalized = (x - min) / (max - min)
    If all values are equal, return 0.5 for every entry.
    """
    min_v = min(values)
    max_v = max(values)

    if max_v == min_v:
        return [0.5] * len(values)

    normalized = []
    for x in values:
        normalized.append((x - min_v) / (max_v - min_v))

    return normalized


def get_class_colors(class_values):
    """
    Assign a color to each unique class value.
    Returns:
        color_map   -- dict { class_value: color_string }
        obj_colors  -- list of colors, one per object (in order)
    """
    unique_classes = []
    for v in class_values:
        if v not in unique_classes:
            unique_classes.append(v)
    unique_classes.sort()

    color_map = {}
    for i in range(len(unique_classes)):
        color_map[unique_classes[i]] = DEFAULT_COLORS[i % len(DEFAULT_COLORS)]

    obj_colors = []
    for v in class_values:
        obj_colors.append(color_map[v])

    return color_map, obj_colors


def get_class_markers(class_values):
    """
    Assign a marker style to each unique class value.
    Returns:
        marker_map  -- dict { class_value: marker_string }
        obj_markers -- list of marker strings, one per object
    """
    unique_classes = []
    for v in class_values:
        if v not in unique_classes:
            unique_classes.append(v)
    unique_classes.sort()

    marker_map = {}
    for i in range(len(unique_classes)):
        marker_map[unique_classes[i]] = DEFAULT_MARKERS[i % len(DEFAULT_MARKERS)]

    obj_markers = []
    for v in class_values:
        obj_markers.append(marker_map[v])

    return marker_map, obj_markers


def build_legend_patches(class_color_map):
    """
    Build matplotlib legend patches from a class->color dict.
    Returns a list of Patch objects ready for ax.legend().
    """
    patches = []
    for class_val in sorted(class_color_map.keys()):
        color = class_color_map[class_val]
        patch = mpatches.Patch(color=color, label=str(class_val))
        patches.append(patch)
    return patches


def print_text_description(plot_name, data_info):
    """
    Print a text description of what would be plotted when matplotlib
    is not available.
    """
    print(f"  [TEXT MODE]  {plot_name}")
    print(f"  {data_info}")
    print()


# ============================================================
# 5. CORE ANALYSIS / VISUALIZATION FUNCTIONS
# ============================================================

def plot_parallel_coordinates(data, numeric_cols, color_col=None, title=None):
    """
    Draw a parallel coordinates plot (profile plot).

    Concept:
      - One vertical axis per attribute, equally spaced on the x axis.
      - All attribute values are min-max normalized to [0, 1] so that
        axes with different scales can be compared side by side.
      - Each OBJECT becomes a polyline that connects its normalized value
        on each axis.
      - When color_col is provided, lines are colored by class value.

    Parameters:
        data        -- column-oriented dict { col_name: [values] }
        numeric_cols-- list of column names to use as axes
        color_col   -- optional column name whose values determine line color
        title       -- optional chart title
    """
    # Build the normalized data for each numeric column
    col_data = {}
    for col in numeric_cols:
        raw = []
        for v in data[col]:
            fv, ok = parse_float(v)
            if ok:
                raw.append(fv)
            else:
                raw.append(0.0)
        col_data[col] = normalize_column(raw)

    n_objects = len(col_data[numeric_cols[0]])
    n_axes    = len(numeric_cols)

    if not HAS_MATPLOTLIB:
        print_text_description(
            "Parallel Coordinates",
            f"  Axes: {numeric_cols}  |  n={n_objects} objects  |  color by: {color_col}"
        )
        # Print a simple text version of the normalized profile
        print(f"  {'Object':<12} " + "  ".join(f"{c[:8]:>8}" for c in numeric_cols))
        label_col = list(data.keys())[0]  # use first column as object label
        for i in range(n_objects):
            label = str(data[label_col][i])[:12]
            vals  = "  ".join(f"{col_data[c][i]:>8.2f}" for c in numeric_cols)
            print(f"  {label:<12} {vals}")
        print()
        return

    # Build colors for lines
    if color_col and color_col in data:
        color_map, obj_colors = get_class_colors(data[color_col])
    else:
        obj_colors = ["steelblue"] * n_objects
        color_map  = {}

    fig, ax = plt.subplots(figsize=(max(8, n_axes * 1.5), 5))

    # Draw a vertical axis line for each attribute
    axis_positions = list(range(n_axes))
    for pos in axis_positions:
        ax.axvline(x=pos, color="gray", linewidth=0.8, linestyle="-")

    # Draw each object as a polyline
    for i in range(n_objects):
        y_points = []
        for col in numeric_cols:
            y_points.append(col_data[col][i])

        ax.plot(axis_positions, y_points,
                color=obj_colors[i], alpha=0.6, linewidth=1.2)

    # Axis labels (the attribute names) at the bottom
    ax.set_xticks(axis_positions)
    ax.set_xticklabels(numeric_cols, rotation=15, ha="right")
    ax.set_ylabel("Normalized value [0, 1]")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title(title or "Parallel Coordinates (Profile Plot)")

    # Legend for color classes
    if color_map:
        patches = build_legend_patches(color_map)
        ax.legend(handles=patches, title=color_col, loc="upper right", fontsize=8)

    plt.tight_layout()
    plt.show()


def plot_star_plots(data, numeric_cols, n_objects=None, label_col=None, title=None):
    """
    Draw a grid of star plots (radar / spider charts), one per object.

    Concept:
      - Equiangular spokes radiate from the centre, one per attribute.
      - The LENGTH of each spoke = the min-max normalized attribute value.
      - The tips of the spokes are connected to form a polygon.
      - Objects with similar profiles look similar.

    Parameters:
        data        -- column-oriented dict
        numeric_cols-- list of attribute column names
        n_objects   -- how many objects to plot (None = all)
        label_col   -- which column to use as the object label
        title       -- overall figure title
    """
    # Build the raw numeric data per column
    col_raw = {}
    for col in numeric_cols:
        raw = []
        for v in data[col]:
            fv, ok = parse_float(v)
            if ok:
                raw.append(fv)
            else:
                raw.append(0.0)
        col_raw[col] = raw

    # Total objects available
    n_total = len(col_raw[numeric_cols[0]])
    if n_objects is None or n_objects > n_total:
        n_objects = n_total

    # Min-max normalize each column over ALL objects (not just the first n_objects)
    # so the scale is consistent across all star plots
    col_norm = {}
    for col in numeric_cols:
        col_norm[col] = normalize_column(col_raw[col])

    # Determine the object labels
    if label_col and label_col in data:
        labels = [str(data[label_col][i]) for i in range(n_objects)]
    else:
        labels = [str(i + 1) for i in range(n_objects)]

    if not HAS_MATPLOTLIB:
        print_text_description(
            "Star Plots",
            f"  Attributes: {numeric_cols}  |  Showing first {n_objects} objects"
        )
        print(f"  {'Object':<12} " + "  ".join(f"{c[:8]:>8}" for c in numeric_cols))
        for i in range(n_objects):
            vals = "  ".join(f"{col_norm[c][i]:>8.2f}" for c in numeric_cols)
            print(f"  {labels[i]:<12} {vals}")
        print()
        return

    # Angle of each spoke in radians (equally spaced, starting from top)
    n_attrs = len(numeric_cols)
    angles  = []
    for k in range(n_attrs):
        angle = (2 * math.pi * k / n_attrs) - math.pi / 2
        angles.append(angle)
    # Close the polygon: append the first angle again at the end
    angles_closed = angles + [angles[0]]

    # Grid layout: try to make it roughly square
    n_cols_grid = max(3, math.ceil(math.sqrt(n_objects)))
    n_rows_grid = math.ceil(n_objects / n_cols_grid)

    fig_w = n_cols_grid * 2.5
    fig_h = n_rows_grid * 2.5
    fig, axes = plt.subplots(n_rows_grid, n_cols_grid,
                             figsize=(fig_w, fig_h),
                             subplot_kw=dict(polar=True))

    # Flatten axes to a 1D list for easy indexing
    if n_rows_grid == 1 and n_cols_grid == 1:
        axes_flat = [axes]
    elif n_rows_grid == 1 or n_cols_grid == 1:
        axes_flat = list(axes)
    else:
        axes_flat = []
        for row in axes:
            for ax in row:
                axes_flat.append(ax)

    for i in range(n_objects):
        ax = axes_flat[i]

        # Collect normalized values, appending the first again to close the polygon
        values = []
        for col in numeric_cols:
            values.append(col_norm[col][i])
        values_closed = values + [values[0]]

        # Convert polar (angle, radius) to cartesian for plotting
        # matplotlib polar axes handle this automatically
        ax.plot(angles_closed, values_closed,
                color="steelblue", linewidth=1.5)
        ax.fill(angles_closed, values_closed,
                color="steelblue", alpha=0.25)

        # Label each spoke with the attribute name
        ax.set_xticks(angles)
        ax.set_xticklabels([c[:6] for c in numeric_cols], fontsize=6)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(["", "", "", ""], fontsize=5)
        ax.set_title(labels[i], fontsize=7, pad=3)

    # Hide unused subplots
    for i in range(n_objects, len(axes_flat)):
        axes_flat[i].set_visible(False)

    fig.suptitle(title or "Star Plots (Radar / Spider Charts)", fontsize=11)
    plt.tight_layout()
    plt.show()


def plot_bubble_chart(data, x_col, y_col, size_col, color_col=None, title=None):
    """
    Draw a bubble chart encoding four attributes simultaneously:
      - x axis   -> x_col  (quantitative)
      - y axis   -> y_col  (quantitative)
      - bubble size -> size_col (quantitative; larger = bigger bubble)
      - bubble color -> color_col (qualitative or quantitative; optional)

    Concept:
      A bubble chart extends a 2D scatter plot to four dimensions.
      Two are shown on the usual x/y axes, a third determines the area
      of the circle, and a fourth can be encoded in color.

    Parameters:
        data      -- column-oriented dict
        x_col     -- column name for x axis
        y_col     -- column name for y axis
        size_col  -- column name for bubble size
        color_col -- optional column name for bubble color
        title     -- optional chart title
    """
    # Extract and parse the x, y, and size values
    x_vals    = []
    y_vals    = []
    size_vals = []

    for v in data[x_col]:
        fv, ok = parse_float(v)
        x_vals.append(fv if ok else 0.0)

    for v in data[y_col]:
        fv, ok = parse_float(v)
        y_vals.append(fv if ok else 0.0)

    for v in data[size_col]:
        fv, ok = parse_float(v)
        size_vals.append(fv if ok else 0.0)

    n = len(x_vals)

    # Scale bubble sizes so the largest is 600 points and smallest is 50
    min_s   = min(size_vals)
    max_s   = max(size_vals)
    range_s = max_s - min_s if max_s != min_s else 1.0

    bubble_sizes = []
    for s in size_vals:
        scaled = 50 + 550 * (s - min_s) / range_s
        bubble_sizes.append(scaled)

    if not HAS_MATPLOTLIB:
        print_text_description(
            "Bubble Chart",
            f"  x={x_col}  y={y_col}  size={size_col}  color={color_col}"
        )
        header = f"  {'Object':>12}  {x_col:>10}  {y_col:>10}  {size_col:>10}"
        if color_col:
            header += f"  {color_col:>10}"
        print(header)
        label_col = list(data.keys())[0]
        for i in range(n):
            row = f"  {str(data[label_col][i]):>12}  {x_vals[i]:>10.1f}  {y_vals[i]:>10.1f}  {size_vals[i]:>10.1f}"
            if color_col:
                row += f"  {str(data[color_col][i]):>10}"
            print(row)
        print()
        return

    # Determine bubble colors
    if color_col and color_col in data:
        color_map, obj_colors = get_class_colors(data[color_col])
    else:
        obj_colors = ["steelblue"] * n
        color_map  = {}

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(x_vals, y_vals,
               s=bubble_sizes, c=obj_colors, alpha=0.65,
               edgecolors="gray", linewidths=0.5)

    # Label each bubble with the first-column identifier
    label_col = list(data.keys())[0]
    for i in range(n):
        ax.annotate(str(data[label_col][i])[:4],
                    (x_vals[i], y_vals[i]),
                    textcoords="offset points",
                    xytext=(0, 5),
                    ha="center",
                    fontsize=7)

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)

    chart_title = title or f"Bubble Chart: {x_col} vs {y_col}  (size = {size_col})"
    if color_col:
        chart_title += f"  (color = {color_col})"
    ax.set_title(chart_title)

    # Legend for color classes
    if color_map:
        patches = build_legend_patches(color_map)
        ax.legend(handles=patches, title=color_col, fontsize=8)

    plt.tight_layout()
    plt.show()


def plot_3d_scatter(data, x_col, y_col, z_col, color_col=None, title=None):
    """
    Draw a 3D scatter plot for three quantitative attributes.

    Concept:
      Extends the 2D scatter plot to a third quantitative axis.
      Objects are plotted as points in a 3D space.
      Requires mpl_toolkits.mplot3d (comes with matplotlib).

    Parameters:
        data      -- column-oriented dict
        x_col     -- column name for x axis
        y_col     -- column name for y axis
        z_col     -- column name for z axis
        color_col -- optional column name for point color
        title     -- optional chart title
    """
    x_vals = []
    y_vals = []
    z_vals = []

    for v in data[x_col]:
        fv, ok = parse_float(v)
        x_vals.append(fv if ok else 0.0)

    for v in data[y_col]:
        fv, ok = parse_float(v)
        y_vals.append(fv if ok else 0.0)

    for v in data[z_col]:
        fv, ok = parse_float(v)
        z_vals.append(fv if ok else 0.0)

    n = len(x_vals)

    if not HAS_MATPLOTLIB:
        print_text_description(
            "3D Scatter Plot",
            f"  x={x_col}  y={y_col}  z={z_col}  color={color_col}"
        )
        print(f"  {x_col:>10}  {y_col:>10}  {z_col:>10}")
        for i in range(n):
            print(f"  {x_vals[i]:>10.1f}  {y_vals[i]:>10.1f}  {z_vals[i]:>10.1f}")
        print()
        return

    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (registers the 3D projection)

    if color_col and color_col in data:
        color_map, obj_colors = get_class_colors(data[color_col])
    else:
        obj_colors = ["steelblue"] * n
        color_map  = {}

    fig = plt.figure(figsize=(8, 6))
    ax  = fig.add_subplot(111, projection="3d")

    ax.scatter(x_vals, y_vals, z_vals,
               c=obj_colors, s=60, alpha=0.75,
               edgecolors="gray", linewidths=0.5)

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_zlabel(z_col)

    chart_title = title or f"3D Scatter: {x_col}, {y_col}, {z_col}"
    ax.set_title(chart_title)

    if color_map:
        patches = build_legend_patches(color_map)
        ax.legend(handles=patches, title=color_col, fontsize=8)

    plt.tight_layout()
    plt.show()


def plot_heatmap(data, numeric_cols, label_col=None, title=None):
    """
    Draw a heatmap where:
      - Rows = objects
      - Columns = numeric attributes
      - Cell color encodes the normalized attribute value
        (dark blue = low, dark red = high)

    Concept:
      A heatmap gives a simultaneous view of all attribute values for all
      objects. In a full analysis you would also add a dendrogram to reorder
      rows by similarity (clustering). Here we show the plain heatmap.

    Parameters:
        data         -- column-oriented dict
        numeric_cols -- list of column names to include
        label_col    -- column to use as row labels
        title        -- optional chart title
    """
    # Extract and normalize each column
    col_raw  = {}
    col_norm = {}

    for col in numeric_cols:
        raw = []
        for v in data[col]:
            fv, ok = parse_float(v)
            raw.append(fv if ok else 0.0)
        col_raw[col]  = raw
        col_norm[col] = normalize_column(raw)

    n_objects = len(col_raw[numeric_cols[0]])
    n_attrs   = len(numeric_cols)

    # Determine row labels
    if label_col and label_col in data:
        row_labels = [str(data[label_col][i]) for i in range(n_objects)]
    else:
        row_labels = [str(i + 1) for i in range(n_objects)]

    if not HAS_MATPLOTLIB:
        print_text_description(
            "Heatmap",
            f"  {n_objects} objects x {n_attrs} attributes  (normalized values shown)"
        )
        header = f"  {'Object':<12} " + " ".join(f"{c[:8]:>8}" for c in numeric_cols)
        print(header)
        for i in range(n_objects):
            vals = " ".join(f"{col_norm[c][i]:>8.2f}" for c in numeric_cols)
            print(f"  {row_labels[i]:<12} {vals}")
        print()
        return

    # Build the 2D array for the heatmap (rows=objects, cols=attributes)
    matrix = []
    for i in range(n_objects):
        row_vals = []
        for col in numeric_cols:
            row_vals.append(col_norm[col][i])
        matrix.append(row_vals)

    fig, ax = plt.subplots(figsize=(max(6, n_attrs * 1.2), max(5, n_objects * 0.4)))

    # Draw colored rectangles for each cell
    for row_i in range(n_objects):
        for col_j in range(n_attrs):
            v = matrix[row_i][col_j]

            # Color: 0 = blue, 0.5 = white, 1 = red  (diverging)
            if v >= 0.5:
                # White -> red
                red   = 1.0
                green = 1.0 - (v - 0.5) * 2
                blue  = 1.0 - (v - 0.5) * 2
            else:
                # Blue -> white
                red   = v * 2
                green = v * 2
                blue  = 1.0

            cell_color = (red, green, blue)

            rect = plt.Rectangle(
                (col_j, n_objects - 1 - row_i), 1, 1,
                facecolor=cell_color, edgecolor="white", linewidth=0.5
            )
            ax.add_patch(rect)

            # Print the original (un-normalized) value inside the cell
            orig_val = col_raw[numeric_cols[col_j]][row_i]
            text_color = "black" if 0.25 < v < 0.75 else "black"
            ax.text(col_j + 0.5, n_objects - 1 - row_i + 0.5,
                    f"{orig_val:.0f}",
                    ha="center", va="center",
                    fontsize=7, color=text_color)

    # Axes
    ax.set_xlim(0, n_attrs)
    ax.set_ylim(0, n_objects)

    col_ticks = [j + 0.5 for j in range(n_attrs)]
    ax.set_xticks(col_ticks)
    ax.set_xticklabels(numeric_cols, rotation=45, ha="right", fontsize=9)

    row_ticks = [n_objects - 1 - i + 0.5 for i in range(n_objects)]
    ax.set_yticks(row_ticks)
    ax.set_yticklabels(row_labels, fontsize=8)

    ax.set_title(title or "Heatmap (blue=low, red=high, normalized per attribute)")

    plt.tight_layout()
    plt.show()


# ============================================================
# 6. PRINTING / DISPLAY FUNCTIONS
# ============================================================

def print_section(title):
    """Print a section banner."""
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)


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
    """
    Run all five multivariate visualization types on the Friends dataset.
    """
    print()
    print("=" * 70)
    print("  Ch.03 Mini Project 02 -- Multivariate Visualization")
    print("  Demo: Friends dataset from lecture slides")
    print("=" * 70)

    numeric_cols = ["Max_temp", "Weight", "Height", "Years"]

    # ---- Plot 1: Parallel Coordinates ----
    print_section("1. Parallel Coordinates  (color by Company)")
    print("  Each friend is drawn as a polyline across all numeric axes.")
    print("  Good company = blue; Bad company = red.")
    print("  Attributes are min-max normalized to [0,1] so they fit the same axes.")
    plot_parallel_coordinates(
        data=FRIENDS,
        numeric_cols=numeric_cols,
        color_col="Company",
        title="Parallel Coordinates -- Friends Dataset (color = Company)"
    )

    # ---- Plot 2: Star Plots ----
    print_section("2. Star Plots (Radar Charts)")
    print("  One spider chart per friend.")
    print("  Each spoke = one attribute; spoke length = normalized value.")
    plot_star_plots(
        data=FRIENDS,
        numeric_cols=numeric_cols,
        n_objects=14,
        label_col="Friend",
        title="Star Plots -- Friends Dataset"
    )

    # ---- Plot 3: Bubble Chart ----
    print_section("3. Bubble Chart  (4 attributes at once)")
    print("  x = Height, y = Weight, size = Max_temp, color = Gender")
    print("  Encodes four attributes simultaneously in one 2D chart.")
    plot_bubble_chart(
        data=FRIENDS,
        x_col="Height",
        y_col="Weight",
        size_col="Max_temp",
        color_col="Gender",
        title="Bubble Chart -- Height vs Weight  (size=Max_temp, color=Gender)"
    )

    # ---- Plot 4: 3D Scatter ----
    print_section("4. 3D Scatter Plot")
    print("  x = Max_temp, y = Weight, z = Height")
    print("  Points colored by Company (Good/Bad).")
    plot_3d_scatter(
        data=FRIENDS,
        x_col="Max_temp",
        y_col="Weight",
        z_col="Height",
        color_col="Company",
        title="3D Scatter -- Friends Dataset (color = Company)"
    )

    # ---- Plot 5: Heatmap ----
    print_section("5. Heatmap")
    print("  Rows = friends, Columns = numeric attributes.")
    print("  Blue = low value, Red = high value (normalized per attribute).")
    plot_heatmap(
        data=FRIENDS,
        numeric_cols=numeric_cols,
        label_col="Friend",
        title="Heatmap -- Friends Dataset"
    )

    print()
    print("  All five plots complete.")
    print()


if __name__ == "__main__":
    run_demo()
