# Chapter 4: Data Quality and Preprocessing — Study Notes

---

## Table of Contents

1. [Why Data Quality Matters](#1-why-data-quality-matters)
2. [Data Quality Problems](#2-data-quality-problems)
3. [Sampling](#3-sampling)
4. [Discretization](#4-discretization)
5. [Scale Type Conversions (Encoding)](#5-scale-type-conversions-encoding)
6. [Normalization](#6-normalization)
7. [Euclidean Distance](#7-euclidean-distance)
8. [Data Transformation](#8-data-transformation)
9. [Quick Reference Summary](#9-quick-reference-summary)
10. [Decision Guide: When to Use Which Technique](#10-decision-guide-when-to-use-which-technique)
11. [Exercise Q&A (ex04)](#11-exercise-qa-ex04)

---

## 1. Why Data Quality Matters

Real-world datasets are almost never clean. Before any meaningful analysis or modeling, raw data must be examined and preprocessed to correct or mitigate quality issues. Garbage in, garbage out — even the best algorithm fails on dirty data.

**Key preprocessing goals:**
- Remove or repair missing, redundant, inconsistent, and noisy data
- Transform attributes into formats suitable for algorithms (normalization, encoding, binning)
- Reduce the influence of scale differences on distance-based methods

---

## 2. Data Quality Problems

### 2.1 Missing Values

A value is missing when it was not recorded for a particular attribute of an object.

**Causes:**
- Attribute was not considered relevant at the start of data collection
- Value is unknown (e.g., patient does not know their weight)
- Device or sensor fault during measurement
- Respondent distraction or refusal (e.g., survey non-response)

**Handling approaches:**

| Approach | When to Use | Notes |
|---|---|---|
| Ignore the object | Missing in the class label | Removes the entire row |
| Remove the object | Many attributes missing | Loses data; only if row is mostly empty |
| Fill with **mean** | Quantitative attribute | Preserves mean; reduces variance |
| Fill with **median** | Ordinal or skewed quantitative | Robust to outliers |
| Fill with **mode** | Nominal attribute | Most frequent category |
| Fill **per class** | Target class is known | Better than global fill; uses class structure |
| Prediction model | High-quality data needed | Most accurate; use k-NN, regression, etc. |

**Per-class filling example:** If the dataset contains male/female genders, fill missing height values with the mean height of the same gender group rather than the global mean.

---

### 2.2 Redundant Data

**Duplicate objects:** Two rows that represent the same real-world entity.
- Fix: **Deduplication** — detect identical (or near-identical) rows and remove one.

**Redundant attributes:** An attribute that can be derived from other attributes already in the dataset.
- Example: `BMI` is derivable from `height` and `weight`. Keeping all three is redundant.
- Fix: Drop derived columns, or keep only the derived one if more informative.

---

### 2.3 Inconsistent Data

Attribute values that violate known domain relationships.

**Examples:**
- A zip code that does not match the recorded city
- A birth date that makes the person 200 years old
- A weight of 1100 kg for a human

**Fix:** Treat the violating value as missing and apply a missing-value strategy.

---

### 2.4 Noisy Data

Noise = random errors or distortions in the measured values. Different from outliers (see below).

**Types:**
- **Feature noise:** incorrect attribute values (e.g., a sensor reads 37.2 instead of 36.8)
- **Label noise:** incorrect class/target labels (e.g., a spam email labeled as non-spam)

**Handling:**
- Noise filters (often k-NN based): replace a value with the average of its k nearest neighbors
- Smooth values using binning (see Discretization, section 4)
- Collect more / better data

---

### 2.5 Outliers

Outliers are values that are far from the majority of data but may be **legitimate**.

| | Noise | Outlier |
|---|---|---|
| Cause | Measurement error | Genuine unusual event |
| Action | Remove / smooth | Investigate before deciding |
| Example | Sensor glitch reads 999 | CEO salary of $50M in a salary dataset |

**Detection methods:**
- IQR rule: flag values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR
- Z-score rule: flag values with |z| > 3
- Visual: box plots, scatter plots

---

## 3. Sampling

Sampling selects a representative subset when working with the full dataset is too expensive.

### 3.1 Simple Random Sampling

Every item has an equal probability of being selected.

### 3.2 Without Replacement

Once an item is selected, it is removed from the pool. No item appears twice.

### 3.3 With Replacement

A selected item is put back; it can be picked again. Used in bootstrapping.

### 3.4 Stratified Sampling

Split the data into non-overlapping partitions (strata) based on a known attribute (e.g., class label), then sample from each stratum independently.

**Why:** Ensures every class/group is represented proportionally, even rare ones.

```
Total dataset: 900 class A, 100 class B  (imbalanced)
Simple random 10% -> ~90 A, ~10 B  (still imbalanced)
Stratified 10% -> exactly 90 A AND 10 B (proportional guarantee)
```

---

## 4. Discretization

Discretization converts a **continuous** (or fine-grained) attribute into an **ordinal** attribute with a finite number of bins/intervals.

**Why:** Some algorithms (e.g., Naive Bayes with discrete features, association rule mining) require categorical inputs.

### 4.1 Equal-Width (Equal-Distance) Binning

Divide the value range into N bins of equal width.

```
W = (max - min) / N

Bin boundaries:
  Bin 1: [min,         min + W)
  Bin 2: [min + W,     min + 2W)
  ...
  Bin N: [min+(N-1)*W, max]
```

**Weakness:** If there are outliers, most data may cluster in one or two bins.

### 4.2 Equal-Depth (Equal-Frequency) Binning

Sort all values and divide so that each bin contains approximately the same number of data points.

```
Target count per bin = total_values / N
```

**Strength:** More balanced bins; robust to outliers.
**Weakness:** Bin boundaries are harder to interpret.

### Comparison Table

| Property | Equal-Width | Equal-Depth |
|---|---|---|
| Bin width | Same for all bins | Varies |
| Bin count | Varies | Same for all bins |
| Outlier sensitivity | HIGH (outliers widen range) | LOW |
| Interpretability | Easy (fixed boundaries) | Harder (data-driven) |

---

## 5. Scale Type Conversions (Encoding)

### 5.1 Nominal to Quantitative: One-Hot Encoding (1-of-N)

Create one binary column per category. Only one column is 1 (hot) for each row.

**Example: Food column with categories {American, Chinese, Italian, Other}**

| Food     | American | Chinese | Italian | Other |
|----------|----------|---------|---------|-------|
| Chinese  | 0        | 1       | 0       | 0     |
| Italian  | 0        | 0       | 1       | 0     |
| American | 1        | 0       | 0       | 0     |
| Other    | 0        | 0       | 0       | 1     |

**Alternative: Frequency encoding** — replace each category with its frequency in the dataset.

### 5.2 Ordinal to Numeric Codes

Three encoding schemes for ordered categories.

**Example: Size = {small, medium, large, very_large}**

| Category   | Natural Number | Gray Code | Thermometer Code |
|------------|---------------|-----------|------------------|
| small      | 0             | 000       | 000              |
| medium     | 1             | 001       | 001              |
| large      | 2             | 011       | 011              |
| very_large | 3             | 010       | 111              |

**Natural Number (0, 1, 2, 3...):**
- Simple integer mapping; preserves order
- Arithmetic differences may be misleading

**Gray Code:**
- Consecutive codes differ by exactly **1 bit**
- Reduces error when transitioning between adjacent categories
- Construction: `gray = n XOR (n >> 1)`

**Thermometer Code (left-to-right filling):**
- n-th category has n ones from the left
- Preserves strict ordering; each step adds exactly one 1
- Also called unary or one-cold encoding

---

## 6. Normalization

Normalization rescales attribute values so different attributes can be compared on the same scale.

### 6.1 Min-Max Normalization

Maps values to a target range [new_min, new_max].

```
v' = (v - min_A) / (max_A - min_A) * (new_max - new_min) + new_min
```

**Default range [0, 1]:**
```
v' = (v - min_A) / (max_A - min_A)
```

**Example:** Income, min = $12,000, max = $98,000, value = $73,600
```
v' = (73600 - 12000) / (98000 - 12000)
   = 61600 / 86000
   = 0.716
```

**Properties:**
- All values land in [new_min, new_max]
- Sensitive to outliers (one extreme value compresses all others)

---

### 6.2 Z-Score (Standardization)

Centers data at mean 0 with standard deviation 1.

```
v' = (v - mu) / sigma
```

where mu = mean of attribute A, sigma = standard deviation of attribute A.

**Example:** Income, mu = $54,000, sigma = $16,000, value = $73,600
```
v' = (73600 - 54000) / 16000
   = 19600 / 16000
   = 1.225
```

**Properties:**
- No bounded output range (typically -3 to +3 for normal distributions)
- More robust to outliers than min-max

---

### Normalization Comparison

| Property | Min-Max | Z-Score |
|---|---|---|
| Output range | [new_min, new_max] | Unbounded |
| Outlier sensitivity | HIGH | LOWER |
| Requires | min, max | mean, std dev |
| Best for | Bounded input algorithms (neural nets) | Gaussian-assumption algorithms (SVM, PCA) |

---

## 7. Euclidean Distance

Measures the straight-line distance between two points in n-dimensional space.

```
d(x, y) = sqrt( sum_{i=1}^{n} (x_i - y_i)^2 )
```

**Example:**
```
x = (1,  3, -2, 5)
y = (2,  4,  1, 6)

differences:  -1,  -1,  -3,  -1
squares:       1,   1,   9,   1
sum:          12
distance:     sqrt(12) = 2*sqrt(3) ~= 3.464
```

### The Scale Problem

If attributes have different units/scales, the attribute with the largest numeric range dominates the distance calculation.

**Lecture example (Bernhard, Gwyneth, James):**
- Age in years: large numeric range -> dominates distance
- Age in decades: small numeric range -> same data, different result

**Fix:** Normalize all attributes before computing distances.

---

## 8. Data Transformation

### 8.1 Log Transformation

Used to reduce right-skewness in distributions.

```
v' = log(v)    (or log10, log2 depending on context)
```

**When to use:** Salary, income, population — values span several orders of magnitude.

**Lecture example:**

| Person | Salary    | Dinner Bill |
|--------|-----------|-------------|
| Marcus | $830,000  | $92         |
| Nigel  | $1,000,000| $120        |

Without transformation, the large salary difference drowns the dinner difference. Log transformation compresses the range while preserving relative ordering.

### 8.2 Absolute Value Conversion

```
v' = |v|
```

Used when the sign carries no meaning (e.g., deviation from target, regardless of direction).

---

## 9. Quick Reference Summary

| Task | Technique | Formula / Key Rule |
|---|---|---|
| Handle missing quantitative | Fill mean or median | `fill = mean(non_missing)` |
| Handle missing nominal | Fill mode | Most frequent category |
| Handle missing by group | Per-class fill | Class-specific mean/mode |
| Remove duplicates | Deduplication | Compare all attribute values row-by-row |
| Detect outliers | IQR rule | Flag if x < Q1-1.5*IQR or x > Q3+1.5*IQR |
| Continuous to ordinal | Equal-width bins | W = (max-min)/N |
| Continuous to ordinal | Equal-depth bins | Sort, then N bins of equal count |
| Nominal to numeric | One-hot encoding | Binary column per category |
| Ordinal to numeric | Natural numbers | 0, 1, 2, ... |
| Ordinal to numeric | Gray code | Consecutive codes differ by 1 bit |
| Ordinal to numeric | Thermometer code | n ones for n-th category |
| Rescale to [0,1] | Min-max normalization | (v-min)/(max-min) |
| Center and scale | Z-score standardization | (v-mu)/sigma |
| n-dim distance | Euclidean distance | sqrt(sum((xi-yi)^2)) |
| Reduce skewness | Log transformation | log(v) |

---

## 10. Decision Guide: When to Use Which Technique

### Handling Missing Values

```
Is the attribute nominal?
  YES -> fill with MODE (most frequent value)
  NO  -> Is the attribute ordinal?
           YES -> fill with MEDIAN
           NO  -> Is the data skewed?
                    YES -> fill with MEDIAN (robust to skew)
                    NO  -> fill with MEAN

Do you have a class label available?
  YES -> consider PER-CLASS filling for better accuracy

Is the missing rate very high (>50% of rows missing this attribute)?
  YES -> consider removing the attribute entirely
```

### Binning / Discretization

```
Are there significant outliers?
  YES -> prefer EQUAL-DEPTH (outliers do not affect bin boundaries)
  NO  -> either works; EQUAL-WIDTH is simpler to explain

Do you need interpretable fixed boundaries?
  YES -> EQUAL-WIDTH

Do you want balanced bin counts?
  YES -> EQUAL-DEPTH
```

### Encoding Ordinal Data

```
Will the encoded values be used in arithmetic distance computations?
  YES -> THERMOMETER CODE (preserves strict ordering, distances are meaningful)
  NO  -> NATURAL NUMBERS (simplest)

Is minimizing bit-flip errors important (e.g., hardware or noisy channel)?
  YES -> GRAY CODE
```

### Normalization

```
Does the algorithm require input in [0, 1]?
  YES -> MIN-MAX NORMALIZATION

Does the algorithm assume Gaussian / zero-mean input?
  YES -> Z-SCORE STANDARDIZATION

Are there significant outliers?
  YES -> Z-SCORE (more robust than min-max)
  NO  -> both work; min-max preferred for interpretability
```

### Distance Computation

```
Do attributes have different units or scales?
  YES -> NORMALIZE FIRST (min-max or z-score), then compute distance
  NO  -> compute Euclidean distance directly
```

---

## 11. Exercise Q&A (ex04)

### Q1: Discretize [31,38,42,29,46,23,83,43,51,55,27,35] into 4 bins

**Sorted:** 23, 27, 29, 31, 35, 38, 42, 43, 46, 51, 55, 83

**Equal-Width (W = (83-23)/4 = 15):**

| Bin | Range     | Values              |
|-----|-----------|---------------------|
| 1   | [23, 37]  | 23, 27, 29, 31, 35  |
| 2   | [38, 52]  | 38, 42, 43, 46, 51  |
| 3   | [53, 67]  | 55                  |
| 4   | [68, 83]  | 83                  |

**Equal-Depth (12 values / 4 bins = 3 per bin):**

| Bin | Values           |
|-----|------------------|
| 1   | {23, 27, 29}     |
| 2   | {31, 35, 38}     |
| 3   | {42, 43, 46}     |
| 4   | {51, 55, 83}     |

---

### Q2: One-Hot Encoding for Food column (first 5 rows)

Categories: {American, Chinese, Italian, Other}

| Food     | American | Chinese | Italian | Other |
|----------|----------|---------|---------|-------|
| Chinese  | 0        | 1       | 0       | 0     |
| Italian  | 0        | 0       | 1       | 0     |
| American | 1        | 0       | 0       | 0     |
| Chinese  | 0        | 1       | 0       | 0     |
| Italian  | 0        | 0       | 1       | 0     |

---

### Q3: Gray Code for Distance values

Categories (ordered): very_close < close < far < very_far < too_far

| Distance   | Integer | Gray Code |
|------------|---------|-----------|
| very_close | 0       | 000       |
| close      | 1       | 001       |
| far        | 2       | 011       |
| very_far   | 3       | 010       |
| too_far    | 4       | 110       |

---

### Q4: Min-Max Normalize Q1 data to [0, 1]

min = 23, max = 83, formula: v' = (v - 23) / 60

| v  | v'    |
|----|-------|
| 31 | 0.133 |
| 38 | 0.250 |
| 42 | 0.317 |
| 29 | 0.100 |
| 46 | 0.383 |
| 23 | 0.000 |
| 83 | 1.000 |
| 43 | 0.333 |
| 51 | 0.467 |
| 55 | 0.533 |
| 27 | 0.067 |
| 35 | 0.200 |

---

### Q5: Euclidean Distance between x=(1,3,-2,5) and y=(2,4,1,6)

```
differences:      (1-2)=-1   (3-4)=-1   (-2-1)=-3   (5-6)=-1
squares:               1          1           9           1
sum of squares:   12
distance:         sqrt(12) = 2*sqrt(3) ~= 3.464
```

**Answer: sqrt(12) ~= 3.464**
