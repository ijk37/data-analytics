# Ch.03 — Descriptive Multivariate Analysis

Multivariate analysis considers **three or more attributes** simultaneously.
The goals are the same as in univariate/bivariate analysis — understand location,
spread, and relationships — but extended to every pair of attributes at once.

---

## 1. Multivariate Frequencies

### Independent (Marginal) Frequencies

Computed **separately for each attribute**, exactly like univariate analysis.
Each attribute gets its own frequency table.

### Joint Frequency

Counts how often a **specific combination of values** occurs across two or more
qualitative attributes.

Example (Friends dataset, Gender x Company):

```
          Bad   Good   Total
F          5      1       6
M          2      6       8
Total      7      7      14
```

Joint relative frequency = count / total n.

---

## 2. Multivariate Data Visualization

### 3D Scatter Plot
- Three quantitative attributes plotted on x, y, z axes.
- Harder to read than 2D; rotate to inspect the point cloud from multiple angles.

### Bubble Chart (4 attributes)
- **x axis** — 1st quantitative attribute
- **y axis** — 2nd quantitative attribute
- **bubble size** — 3rd quantitative attribute
- **bubble color** — 4th attribute (quantitative or qualitative)

### Color / Shape Encoding for a Qualitative 3rd Attribute
- Scatter plot of two quantitative attributes with a categorical variable
  encoded as **color** and/or **marker shape**.
- Allows class separation to be visually assessed.

### Parallel Coordinates (Profile Plot)
- One vertical axis per attribute, equally spaced.
- Each **object** becomes a polyline (broken line) connecting its value on each axis.
- Color lines by class to see group structure.
- Good for detecting clusters, outliers, and correlated attributes.
- Limitation: order of axes matters — only adjacent axes appear "connected".

### Star Plots (Spider / Radar Charts)
- One spoke per attribute, radiating at **equal angles** from the centre.
- The **length** of each spoke is proportional to the attribute value (after normalization).
- Points at the spoke tips are connected to form a polygon.
- Each **object** gets its own star; objects with similar profiles look similar.
- Useful for comparing a small number of objects on many attributes.

### Chernoff Faces
- Each attribute is mapped to a **facial feature**:
  eyes (size, shape, position), ears, eyebrows, nose, mouth (shape, curvature),
  hair, face shape, etc.
- The human visual system is very sensitive to face differences, which can reveal
  subtle cluster structure.
- Limitation: the choice of which attribute maps to which feature is arbitrary
  and affects interpretation.

### Heatmap with Dendrograms
- **Rows** = objects, **Columns** = attributes (or vice versa).
- Cell color encodes the attribute value (e.g., low = blue, high = red).
- Rows and columns are **reordered by hierarchical clustering (dendrogram)**
  so that similar objects and similar attributes end up together.
- Gives a simultaneous view of object clusters and attribute patterns.

### Mosaic Plot
- For **qualitative** attributes only (up to 3).
- Tiles are drawn; the **area** of each tile is proportional to the joint frequency
  of the corresponding combination of category values.
- Deviations from independence show up as large tiles in unexpected places.

### Scatter Plot Matrix (Draftsman's Display / SPLOM)
- A **p × p grid** of scatter plots, one for every pair of quantitative attributes.
- The diagonal usually shows univariate summaries (histogram or density).
- Off-diagonal cell (i, j) plots attribute i on y vs. attribute j on x.
- Allows simultaneous pairwise inspection of all attributes.
- Often annotated with Pearson r values in each cell.

---

## 3. Location Statistics Matrix

For a dataset with p numeric attributes and n objects, the location matrix is a
**7 × p** table:

| Statistic | Attr 1 | Attr 2 | ... | Attr p |
|-----------|--------|--------|-----|--------|
| Min       |        |        |     |        |
| Q1        |        |        |     |        |
| Median    |        |        |     |        |
| Mean      |        |        |     |        |
| Mode      |        |        |     |        |
| Q3        |        |        |     |        |
| Max       |        |        |     |        |

Each cell is computed **independently** for that attribute — this is just univariate
statistics applied to every column.

### Friends Dataset — Location Matrix

| Statistic | Max_temp | Weight | Height | Years |
|-----------|----------|--------|--------|-------|
| Min       |  8       |  55    | 158    |  0    |
| Q1        | 12       |  67.5  | 169    |  2    |
| Median    | 15.5     |  75    | 174    |  5.5  |
| Mean      | 18.14    |  79.36 | 176.43 |  6.43 |
| Mode      | 12, 15   |  75    | 172,180|  2, 3 |
| Q3        | 25.75    |  87.5  | 182.5  | 13.25 |
| Max       | 31       | 115    | 195    | 16    |

---

## 4. Dispersion Statistics Matrix

A **4 × p** (or 5 × p) table covering spread measures for each attribute.

| Statistic | Attr 1 | Attr 2 | ... | Attr p |
|-----------|--------|--------|-----|--------|
| Amplitude (range) | max - min | | | |
| IQR       | Q3 - Q1 | | | |
| MAD       | median of |xi - median| | | |
| Std Dev   | sqrt(sample variance) | | | |
| Variance  | sample variance | | | |

### Friends Dataset — Dispersion Matrix

| Statistic | Max_temp | Weight  | Height | Years |
|-----------|----------|---------|--------|-------|
| Amplitude |  23      |  60     |  37    |  16   |
| IQR       |  13.75   |  20     |  13.5  |  11.25|
| MAD       |  4.5     |   7     |   6    |   3.5 |
| Std Dev   |  7.45    |  17.38  |  11.25 |   5.65|

---

## 5. Covariance Matrix

The **p × p covariance matrix** S captures the variance of each attribute (on the
diagonal) and the pairwise covariance between every pair (off-diagonal).

### Formula

```
S[i][j] = cov(Xi, Xj) = (1 / (n-1)) * sum_k( (Xi_k - mean_Xi) * (Xj_k - mean_Xj) )
```

When i = j this reduces to the **sample variance**:

```
S[i][i] = var(Xi) = (1 / (n-1)) * sum_k( (Xi_k - mean_Xi)^2 )
```

### Properties
- **Symmetric**: S[i][j] = S[j][i]
- **Diagonal entries**: variances (always >= 0)
- **Off-diagonal entries**: positive = same-direction variation; negative = opposite direction
- **Scale-dependent**: changing units changes values

### Friends Dataset — Covariance Matrix

|           | Max_temp | Weight  | Height  | Years  |
|-----------|----------|---------|---------|--------|
| Max_temp  |  55.52   |  34.46  |  20.19  |  5.82  |
| Weight    |  34.46   | 302.15  | 184.62  | 42.39  |
| Height    |  20.19   | 184.62  | 126.53  | 14.03  |
| Years     |   5.82   |  42.39  |  14.03  | 31.98  |

Interpretation examples:
- cov(Weight, Height) = 184.62 — strong positive co-variation (tall people tend to be heavier)
- cov(Max_temp, Years) = 5.82 — mild positive co-variation

---

## 6. Pearson Correlation Matrix

The correlation matrix **R** standardizes the covariance matrix so all values
fall in [-1, +1]:

### Formula

```
R[i][j] = cov(Xi, Xj) / (std(Xi) * std(Xj))
         = S[i][j] / sqrt(S[i][i] * S[j][j])
```

### Properties
- **Symmetric**: R[i][j] = R[j][i]
- **Diagonal**: always 1.00 (every attribute is perfectly correlated with itself)
- **Range**: -1 (perfect negative linear) to +1 (perfect positive linear)
- **Scale-independent**: units do not affect values

### Interpretation Guide

| |r|       | Label               |
|-----------|---------------------|
| 0.90–1.00 | Very strong         |
| 0.70–0.89 | Strong              |
| 0.50–0.69 | Moderate            |
| 0.30–0.49 | Weak                |
| 0.00–0.29 | Negligible          |

### Friends Dataset — Pearson Correlation Matrix

|           | Max_temp | Weight | Height | Years  |
|-----------|----------|--------|--------|--------|
| Max_temp  |  1.00    |  0.27  |  0.24  |  0.14  |
| Weight    |  0.27    |  1.00  |  0.94  |  0.43  |
| Height    |  0.24    |  0.94  |  1.00  |  0.22  |
| Years     |  0.14    |  0.43  |  0.22  |  1.00  |

Interpretation:
- Weight / Height: r = 0.94 — **very strong positive** (taller friends tend to be heavier)
- Max_temp / Weight: r = 0.27 — **negligible** (no meaningful linear relationship)
- Weight / Years: r = 0.43 — **weak positive**

---

## 7. Correlogram

A **visual version** of the correlation matrix.

- Each cell is colored: dark = high absolute correlation; light = near zero.
- Color scale: blue shades for positive, red shades for negative (or a diverging palette).
- Cells can also be drawn as circles/ellipses whose size and shape encode r.
- The diagonal is typically darkest (r = 1.00 with itself).
- Symmetry is visible: the lower-left and upper-right triangles mirror each other.

In R: `corrplot::corrplot(cor_matrix, method="color")` or `method="circle"`.
In Python: `seaborn.heatmap()` with `annot=True`, or a custom matplotlib grid.

---

## 8. Quick Reference

| Tool                    | Attributes required        | Best for                         |
|-------------------------|---------------------------|----------------------------------|
| 3D scatter              | 3 quantitative             | Point cloud shape in 3D          |
| Bubble chart            | 2 quant + size + color     | 4 attributes in 2D               |
| Parallel coordinates    | Any number of attributes   | Profiles, clusters, outliers     |
| Star/radar plot         | Many attributes            | Comparing profiles per object    |
| Chernoff faces          | Many attributes (up to ~18)| Revealing face-like clusters     |
| Heatmap + dendrogram    | All numeric                | Clustering rows and columns      |
| Mosaic plot             | 2–3 qualitative            | Joint frequency / independence   |
| Scatter plot matrix     | All pairs of quantitative  | Pairwise linear relationships    |
| Correlogram             | All numeric                | Quick visual of correlation matrix|
| Covariance matrix       | All numeric pairs          | Direction & magnitude of co-variation |
| Pearson correlation matrix | All numeric pairs       | Scale-independent linear corr.   |

---

## 9. Key Formulas at a Glance

```
Sample covariance:
  cov(X, Y) = (1/(n-1)) * SUM[ (xi - x_bar)(yi - y_bar) ]

Sample variance (diagonal of cov matrix):
  var(X) = cov(X, X) = (1/(n-1)) * SUM[ (xi - x_bar)^2 ]

Pearson r (from covariance):
  r(X, Y) = cov(X, Y) / (std(X) * std(Y))
           = S[i][j] / sqrt(S[i][i] * S[j][j])

MAD (Median Absolute Deviation):
  MAD(X) = median( |xi - median(X)| )

IQR:
  IQR(X) = Q3(X) - Q1(X)

Amplitude (Range):
  amplitude(X) = max(X) - min(X)
```

---

## 10. R Code Quick Reference

```r
# Location and dispersion per column
apply(df[, numeric_cols], 2, summary)    # min, Q1, median, mean, Q3, max
apply(df[, numeric_cols], 2, sd)         # standard deviation

# Covariance and correlation matrices
cov(df[, numeric_cols])                  # covariance matrix
cor(df[, numeric_cols])                  # Pearson correlation matrix

# Visualizations
library(corrplot)
corrplot(cor(df[, numeric_cols]), method = "color")   # correlogram

library(pheatmap)
pheatmap(scale(df[, numeric_cols]))                   # heatmap with dendrogram

library(GGally)
ggpairs(df[, numeric_cols])                           # scatter plot matrix

# Parallel coordinates
library(MASS)
parcoord(df[, numeric_cols], col = as.numeric(df$Class))

# Star plots
stars(df[, numeric_cols])

# Chernoff faces
library(aplpack)
faces(df[1:20, numeric_cols])
```
