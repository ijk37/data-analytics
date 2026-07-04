# Chapter 2 — Descriptive Statistics

---

## 1. Statistics Fundamentals

| Term | Definition |
|------|-----------|
| **Statistics** | The discipline of collecting, organizing, analyzing, interpreting, and presenting data |
| **Population** | The complete set of instances of interest (e.g., all students in a school) |
| **Sample** | A subset of the population collected by a defined procedure |
| **Sampling** | Selecting and analyzing a subset to estimate population values in a quantified way |

### Induction vs. Deduction

| Type | Direction | Description |
|------|-----------|-------------|
| **Induction** (inference) | Sample → Population | Generalizing from sample to population; larger sample = closer estimate |
| **Deduction** | Population → Sample | Reasoning about a sample drawn from a known population (probability is deduction) |

### Descriptive Statistics

Methods for **summarizing and visualizing samples** to help humans understand data.

| Scope | Name | Definition |
|-------|------|-----------|
| Single attribute | **Univariate** | Frequency tables, statistics, plots for one column |
| Two attributes | **Bivariate** | Relationships between pairs of columns |
| 3+ attributes | **Multivariate** | Relationships across many columns |

---

## 2. Univariate Analysis — Frequencies

| Frequency Type | Definition | Formula |
|---------------|-----------|---------|
| **Absolute** | Count of occurrences of a value | count(v) |
| **Relative** | Fraction of total occurrences | count(v) / n |
| **Absolute cumulative** | Count of values ≤ v | sum of abs. freqs up to v |
| **Relative cumulative** | Fraction of values ≤ v | sum of rel. freqs up to v |

> The relative frequency column defines an **empirical frequency distribution**.  
> The relative cumulative frequency column defines an **empirical CDF**.

- A **discrete** attribute has a **probability mass function** (PMF)
- A **continuous** attribute has a **probability density function** (PDF)

---

## 3. Univariate Analysis — Location Statistics

Location statistics return a **central** value from a set. Also called *measures of central tendency*.

| Statistic | Definition | Scale validity |
|-----------|-----------|---------------|
| **Minimum** | Smallest value | Ordinal, Quantitative |
| **Maximum** | Largest value | Ordinal, Quantitative |
| **Mode** | Most frequent value | **All scales** (Nominal, Ordinal, Quantitative) |
| **Median** | Middle value in sorted order | Ordinal, Quantitative |
| **Mean** | Sum / n | Quantitative (eventually Ordinal for numeric scales) |

**Median formula** (sorted dataset of n values):
- n odd → median = x[(n+1)/2]
- n even → median = (x[n/2] + x[n/2 + 1]) / 2

> **Robustness:** Median and mode are more robust than mean when data is skewed or has extreme values.

### Quartiles

Quartiles split **sorted** data into four equal parts. There are multiple methods; the position method is the most general:

1. Count n observations and sort them.
2. For Q_k (k = 1, 2, 3): compute n × (k/4).
   - If the result is an **integer** → Q_k = mean of values at positions n×(k/4) and n×(k/4)+1
   - If **not an integer** → round up; Q_k = value at that position

| Quartile | Also known as | Interpretation |
|----------|--------------|---------------|
| Q1 | Lower quartile | Larger than 25% of values |
| Q2 | Median | Larger than 50% of values |
| Q3 | Upper quartile | Larger than 75% of values |

---

## 4. Univariate Analysis — Dispersion Statistics

Dispersion statistics measure **how spread out** the values are.

| Statistic | Formula | Notes |
|-----------|---------|-------|
| **Amplitude** | max − min | Sensitive to outliers |
| **Interquartile Range (IQR)** | Q3 − Q1 | Robust to outliers |
| **MAD** (Mean Absolute Deviation) | Σ\|xᵢ − x̄\| / (n−1) | Average absolute distance from mean (sample) |
| **Standard Deviation** | √(Σ(xᵢ − x̄)² / (n−1)) | Typical distance from mean (sample) |
| **Variance** | s² = Σ(xᵢ − x̄)² / (n−1) | Square of std dev |

**Population vs. Sample formulas:**

| | Population | Sample |
|-|-----------|--------|
| Mean | μ | x̄ |
| Std Dev | σ = √(Σ(xᵢ−μ)²/n) | s = √(Σ(xᵢ−x̄)²/(n−1)) |
| MAD | Σ\|xᵢ−μ\|/n | Σ\|xᵢ−x̄\|/(n−1) |

> Dividing by **n−1** (Bessel's correction) gives an unbiased estimate of the population variance from a sample.

---

## 5. Univariate Analysis — Visualization

| Chart | Best for | Notes |
|-------|----------|-------|
| **Pie chart** | Nominal scales | Parts of a whole |
| **Bar chart** | Qualitative or quantitative with few values | Easy comparison |
| **Line chart** | Time / ordered data | Emphasizes trend |
| **Area chart** | Comparing distributions or time series | Filled region under curve |
| **Histogram** | Quantitative (continuous) distributions | Groups values into bins (cells) |
| **Box plot** | Showing quartiles + spread | Min, Q1, median, Q3, Max |
| **Stacked bar** | Frequency of one attribute split by another | Shows sub-group composition |

**Histogram bin count rule of thumb:** use ≈ √n bins (where n = number of data points). The best value is always problem-dependent.

### Box Plot Anatomy

```
  Max ─┬─ whisker top
       │
  Q3  ─┼─ top of box
       │
  Q2  ─┼─ median line
       │
  Q1  ─┼─ bottom of box
       │
  Min ─┴─ whisker bottom
```

### Skewness

**Skewness** measures the asymmetry of a distribution.

| Skew type | Shape | Tail direction | mean vs. median |
|-----------|-------|---------------|-----------------|
| **Symmetric** | Bell | Both equal | mean ≈ median |
| **Positive (right) skew** | Right tail longer | Mass concentrated on left | mean > median |
| **Negative (left) skew** | Left tail longer | Mass concentrated on right | mean < median |

> A **unimodal** distribution has exactly one peak (mode).

---

## 6. Common Univariate Distributions

### Uniform Distribution x ~ U(a, b)

Values equally distributed in [a, b]; zero probability outside.

- PDF: f(x) = 1/(b−a) for a ≤ x ≤ b, else 0
- CDF: P(x < x₀) = (x₀−a)/(b−a) for a ≤ x₀ ≤ b

### Normal (Gaussian) Distribution x ~ N(μ, σ)

Symmetric bell curve, fully defined by mean μ and standard deviation σ.

- μ: locates the peak (center)
- σ: controls width (spread)
- ~68% of values within μ ± σ; ~95% within μ ± 2σ; ~99.7% within μ ± 3σ

> In a **sample** we speak of proportions (relative frequencies).  
> In a **population** we speak of probabilities.

---

## 7. Bivariate Analysis — Two Quantitative Attributes

### Visualizations

| Chart | Purpose |
|-------|---------|
| **Scatter plot** | Visualize distribution of paired values; reveals general trends |
| **3D histogram** | Show joint frequency of two quantitative attributes |

### Covariance

Measures the **degree of linear co-variation** between two attributes.

```
cov(xi, xj) = (1/(n−1)) × Σ (xki − x̄i)(xkj − x̄j)
```

| Sign | Meaning |
|------|---------|
| Positive | Both attributes increase/decrease together |
| Negative | One increases as the other decreases |
| Near zero | No linear relationship |

> **Limitation:** covariance value depends on the scale of the attributes (not unit-free).

### Pearson's Correlation Coefficient (r)

Scale-independent version of covariance. Always in **[−1, 1]**.

```
r(xi, xj) = cov(xi, xj) / (si × sj)
```

| Value | Interpretation |
|-------|---------------|
| +1 | Perfect positive linear relationship |
| 0 | No linear relationship |
| −1 | Perfect negative linear relationship |

### Spearman's Rank Correlation (ρ)

Pearson's r applied to the **ranks** of the values instead of the values themselves.

- Use when data is ordinal, non-linear, or has outliers
- Less sensitive to outliers than Pearson (outlier gets capped at its rank value)
- ρ = 1 if the relationship is any monotonically increasing function (not just linear)

**How to compute:**
1. Sort each attribute and assign ranks 1, 2, …, n. For ties, use the average rank.
2. Apply Pearson's formula to the rank columns.

> **Pearson vs Spearman:** When data is roughly elliptical with no outliers, both give similar results. Spearman is preferred for ordinal data or when outliers are present.

---

## 8. Bivariate Analysis — Qualitative + Quantitative

Use **grouped box plots**: one box plot per category value, all on the same axis.

- X-axis: categories of the qualitative attribute
- Y-axis: values of the quantitative attribute
- Reveals whether the quantitative distribution differs across groups

---

## 9. Bivariate Analysis — Two Qualitative Attributes

### Contingency Table

Matrix of joint absolute (or relative) frequencies.
- Rows: values of attribute 1
- Columns: values of attribute 2
- Row totals on right; column totals on bottom; grand total bottom-right

### Mosaic Plot

Visual equivalent of a contingency table — areas are proportional to relative joint frequencies.

---

## 10. Bivariate Analysis — Two Ordinal Attributes

Use the same techniques as the qualitative case **plus**:

- **Spearman's rank correlation** (preferred over Pearson for ordinal data)
- **Scatter plots with jitter** — add a small random offset to each point to prevent overlapping dots at the same (rank, rank) position

---

## Quick-Reference: Choosing the Right Method

| Attribute types | Best statistic | Best visualization |
|----------------|---------------|-------------------|
| Nominal (1) | Mode, frequency table | Pie, bar chart |
| Ordinal (1) | Median, quartiles | Bar chart, box plot |
| Quantitative (1) | Mean, std dev, quartiles | Histogram, box plot |
| Quant + Quant | Pearson r, covariance | Scatter plot |
| Qual + Quant | Grouped stats per category | Grouped box plots |
| Qual + Qual | Contingency table | Mosaic plot |
| Ordinal + Ordinal | Spearman ρ | Jitter scatter plot |
