# Ch.03 Mini Project 02 — Multivariate Visualization

**Concept:** Parallel coordinates, star/radar plots, bubble charts, 3D scatter
plots, heatmaps — all for visualizing multivariate data.

## What it does

### Python (`multivariate_viz.py`)

Uses the Friends dataset (built-in) to demonstrate five multivariate plot types:

1. **Parallel coordinates** — each friend is a polyline crossing vertical axes,
   colored by Company (Good/Bad)
2. **Star plots** — one radar/spider chart per friend showing their numeric profile
3. **Bubble chart** — Weight vs Height, bubble size = Max_temp, color = Gender
4. **3D scatter** — Max_temp, Weight, Height in a 3D point cloud
5. **Heatmap** — color-coded grid showing all attribute values per friend

matplotlib is required for plots. If not available, a text description is printed.

### R (`multivariate_viz.R`)

Answers the Iris dataset exercise questions from Ch.03:

| Exercise | Plot type | R function |
|----------|-----------|-----------|
| Q1 | Scatter: Sepal.Length vs Sepal.Width; Petal.Length = size | ggplot2 |
| Q2 | Scatter: same axes; Species = color + shape | ggplot2 |
| Q3 | 3D scatter: Sepal.Length, Sepal.Width, Petal.Length | scatterplot3d |
| Q4 | Parallel coordinates; Species = color | MASS::parcoord |
| Q5 | Star plots for first 20 objects | stars() |
| Q8 | Chernoff faces for first 20 objects | aplpack::faces |
| Q9 | Box plots for all 4 numeric attributes | ggplot2 |

## Files

| File | Language | Description |
|------|----------|-------------|
| `multivariate_viz.py` | Python 3 | matplotlib; beginner-friendly |
| `multivariate_viz.R`  | R        | ggplot2, scatterplot3d, MASS, aplpack |

## Usage

### Python

```bash
# Built-in demo (Friends dataset)
python multivariate_viz.py
```

Install matplotlib if needed:
```bash
pip install matplotlib
```

### R

```r
# Install required packages once:
install.packages(c("ggplot2", "scatterplot3d", "MASS", "aplpack"))

source("multivariate_viz.R")
```

## Key Concepts from Ch.03 Applied

| Concept | Function |
|---------|---------|
| Parallel coordinates | `plot_parallel_coordinates()` |
| Star / radar plots | `plot_star_plots()` |
| Bubble chart (4 attributes) | `plot_bubble_chart()` |
| 3D scatter | `plot_3d_scatter()` |
| Heatmap | `plot_heatmap()` |
| Color / shape encoding | Color by class in all plots |
