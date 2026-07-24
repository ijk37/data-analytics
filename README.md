<div align="center">

<a href="https://ijk37.com/data-analytics/"><img src="assets/banner.svg" alt="Data Analytics" width="100%"></a>

<p>
  <a href="https://ijk37.com/data-analytics/"><img src="https://img.shields.io/badge/%F0%9F%87%A7%F0%9F%87%A9_View_the_Live_Site-IJK37.COM-F42A41?style=for-the-badge&labelColor=006A4E" alt="View the live site — ijk37.com"></a>
</p>

<p>
  <a href="01-notes/README.md"><img src="https://img.shields.io/badge/Notes-8_chapters-34526B?style=for-the-badge&labelColor=22384A" alt="Course Notes"></a>
  <a href="02-exercises/README.md"><img src="https://img.shields.io/badge/Exercises-8_sets-34526B?style=for-the-badge&labelColor=22384A" alt="Exercises"></a>
  <a href="https://ijk37.com/data-analytics/03-quiz/"><img src="https://img.shields.io/badge/Quiz_Hub-Open-1E9E75?style=for-the-badge&labelColor=167A5A" alt="Quiz Hub"></a>
  <a href="04-projects/README.md"><img src="https://img.shields.io/badge/Projects-33_labs-34526B?style=for-the-badge&labelColor=22384A" alt="Projects"></a>
</p>

<p>
  <img src="https://img.shields.io/badge/Languages-Python_%C2%B7_R_%C2%B7_Excel-1E9E75?style=flat-square&labelColor=167A5A" alt="Languages">
  <img src="https://img.shields.io/badge/Chapters-8-34526B?style=flat-square&labelColor=22384A" alt="Chapters">
  <img src="https://img.shields.io/badge/Projects-33-34526B?style=flat-square&labelColor=22384A" alt="Projects count">
</p>

<p><em>A complete, hands-on implementation of every topic from a university-level data analytics course — notes, exercises, quizzes, and mini-projects in <strong>Python</strong>, <strong>R</strong>, and <strong>Excel</strong>.</em></p>

</div>

---

## Course Dashboard

| Section | Purpose | Start Here |
| --- | --- | --- |
| **01 Notes** | Chapter-by-chapter study notes | [Browse notes](01-notes/README.md) |
| **02 Exercises** | Practice questions with worked answers, adapted from the course assignments | [Open exercises](02-exercises/README.md) |
| **03 Quiz** | 120-question interactive review bank with randomized attempts | [Launch quiz hub](https://ijk37.com/data-analytics/03-quiz/) |
| **04 Projects** | 33 mini-projects and capstones in Python and R | [View projects](04-projects/README.md) |
| **05 Toolkit** | Setup guidance, dataset preparation, references, and project checklist | [Open toolkit](05-resources/README.md) |

## Learning Path

```text
Read notes -> Practice exercises -> Take quiz -> Build project -> Review weak areas
```

1. Start with the chapter notes in [`01-notes`](01-notes/README.md).
2. Complete the matching set in [`02-exercises`](02-exercises/README.md).
3. Test recall in the [Quiz Hub](https://ijk37.com/data-analytics/03-quiz/).
4. Apply the concepts through a mini-project or capstone in [`04-projects`](04-projects/README.md).

---

## Repository Structure

```
data-analytics/
├── 01-notes/            # 8 chapter notes files (Markdown)
├── 02-exercises/        # 8 practice sets, worked Q&A
├── 03-quiz/             # Static quiz app (index.html + quiz.html)
├── 04-projects/         # 33 project folders across 8 modules
└── 05-resources/        # Public learning toolkit; source materials stay local-only
```

---

## Chapters at a Glance

### Ch01 — Data & Attribute Types
**Key concepts:** Stevens' 4 measurement scales (Nominal, Ordinal, Interval, Ratio), dataset types (Record, Matrix, Transaction, Graph, Ordered), Discrete vs Continuous.

| Project | What it does | Languages |
|---------|-------------|-----------|
| Attribute Auditor | Infers the scale type of each column from data characteristics | Python |
| Dataset Type Explorer | Classifies a dataset as Record/Matrix/Transaction/Graph/Ordered | Python |
| Scale Exercises | Solves the chapter exercise — identifies scale for 5 real-world attributes | Python, R |

---

### Ch02 — Descriptive Statistics (Univariate & Bivariate)
**Key concepts:** Frequency tables, mode/median/mean/quartiles, IQR, MAD, standard deviation, skewness, box plots, Pearson r, Spearman ρ, covariance.

| Project | What it does | Languages |
|---------|-------------|-----------|
| Frequency Table Builder | Absolute, relative, and cumulative frequency tables | Python |
| Statistics Explorer | Full location & dispersion stats with ASCII box plot | Python |
| Distribution Visualizer | Histograms, bar charts, frequency distributions | Python |
| Bivariate Quantitative | Covariance, Pearson r, Spearman ρ with step-by-step computation | Python |
| Categorical Analyzer | Contingency tables, grouped box plots, chi-square hint | Python |
| Exercise Solutions | Verified solutions for all chapter exercises (frequency table, quartiles, Pearson/Spearman) | Python, R |

---

### Ch03 — Descriptive Multivariate Analysis
**Key concepts:** Multivariate statistics matrices, 3D scatter, bubble charts, parallel coordinates, star/radar plots, Chernoff faces, scatter plot matrix, covariance matrix, Pearson correlation matrix, correlogram, heatmap with dendrograms, mosaic plots.

| Project | What it does | Languages |
|---------|-------------|-----------|
| Multivariate Statistics | Location matrix, dispersion matrix, covariance matrix, correlation matrix | Python, R |
| Multivariate Visualization | Parallel coords, star plots, bubble charts, 3D scatter, Chernoff faces, box plots | Python, R |
| Correlation & Heatmap | Scatter plot matrix, correlogram, Pearson/Spearman comparison, heatmap | Python, R |
| Joint Frequency & Mosaic | Joint frequency tables, mosaic plots for qualitative attributes | Python, R |

---

### Ch04 — Data Quality and Preprocessing
**Key concepts:** Missing values (per-class imputation), duplicates, outlier detection (IQR), discretization (equal-width / equal-depth), one-hot encoding, gray code, thermometer code, min-max normalization, z-score standardization, Euclidean distance, log transformation, stratified sampling.

| Project | What it does | Languages |
|---------|-------------|-----------|
| Data Quality Auditor | Detects and fixes missing values, duplicates, and outliers | Python, R |
| Discretization & Encoding | Equal-width/depth bins, one-hot, gray code, thermometer code | Python, R |
| Normalization & Distance | Min-max, z-score, Euclidean distance, stratified sampling | Python, R |
| Data Transformation | Log transform, absolute value, skewness reduction | Python, R |

---

### Ch05 — Clustering
**Key concepts:** Distance measures (Minkowski L1/L2, Hamming, Levenshtein), K-means, K-means++, SSE, elbow curve, hierarchical clustering (single/complete/average/Ward linkage), dendrograms, DBSCAN (core/border/noise points).

| Project | What it does | Languages |
|---------|-------------|-----------|
| Distance Measures | All distance types from scratch: Minkowski, Hamming, edit distance | Python, R |
| K-Means Clustering | K-means + K-means++ + elbow curve; solves chapter exercise step-by-step | Python, R |
| Hierarchical & DBSCAN | All 4 linkage methods with ASCII dendrogram, BFS-based DBSCAN | Python, R |

---

### Ch06 — Frequent Pattern Mining
**Key concepts:** Itemsets, support, confidence, lift, Apriori algorithm (anti-monotone pruning), FP-tree, FP-growth, maximal and closed frequent itemsets, association rules.

| Project | What it does | Languages |
|---------|-------------|-----------|
| Association Rules | Apriori from scratch + rule generation sorted by lift | Python, R |
| FP-Growth | FP-tree construction, recursive mining, maximal/closed detection | Python, R |
| Pattern Mining Libraries | Practical mining with mlxtend (Python) and arules (R) | Python, R |

---

### Ch07 — Classification
**Key concepts:** Decision trees (entropy, information gain, gain ratio, Gini), k-NN (majority vote, normalization), Naive Bayes (Gaussian, Laplace smoothing), confusion matrix, accuracy, precision, recall, F1 score, k-fold cross-validation.

| Project | What it does | Languages |
|---------|-------------|-----------|
| Decision Trees | Build trees using entropy/IG/Gini; ASCII tree visualization | Python, R |
| k-NN & Naive Bayes | Distance-based k-NN, step-by-step Gaussian Naive Bayes | Python, R |
| Model Evaluation | Confusion matrix, precision/recall/F1, 5-fold cross-validation | Python, R |

---

### Ch08 — Final Projects
Multi-chapter capstone projects that combine techniques from across the course on real-world scenarios.

| Project | Theme | Dataset | Chapters Combined |
|---------|-------|---------|-------------------|
| End-to-End Pipeline | Full pipeline on Friends data | 14 friends | Ch4 → Ch2/3 → Ch5 → Ch7 |
| Market Basket & Segmentation | Purchase patterns + customer clusters | 20 grocery customers | Ch2/3 + Ch4 + Ch6 + Ch5 |
| Classification Study | Compare 3 classifiers with evaluation | 20 friends | Ch2/3 + Ch4 + Ch7 |
| Iris Complete Walkthrough | Every technique applied to Iris | 150 Iris samples | **Ch1 through Ch7** |
| Student Performance Predictor | Grade patterns → early warning system | 25 students | Ch1+Ch2+Ch3+Ch4+Ch5+Ch6+Ch7 |
| Retail Churn Analytics | Identify customers likely to churn | 30 retail customers | Ch1+Ch2+Ch3+Ch4+Ch5+Ch6+Ch7 |
| Medical Heart Risk Capstone | "Know Your Data" — 8-phase clinical analysis | 25 patients | **All Ch1–Ch7** |

See the full dashboard (all 33 projects) in [`04-projects/README.md`](04-projects/README.md).

---

## Quiz Hub

A self-contained, dependency-free quiz app (`03-quiz/`) with 120 questions across eight chapter pools — random subset per attempt, instant scoring, answer explanations, and a full post-quiz review.

| Feature | Details |
| --- | --- |
| Chapter coverage | 8 chapter quizzes + 1 mixed capstone review |
| Question pool | 120 total questions across 8 chapter banks |
| Attempt style | Randomized question subset and shuffled options |
| Access | [Open the Quiz Hub](https://ijk37.com/data-analytics/03-quiz/) |

---

## Tech Stack

| Language | Usage | Key Libraries |
|----------|-------|--------------|
| **Python** | Readable implementations of the course algorithms | Standard library for most labs; optional pandas/mlxtend comparison |
| **R** | Visualization, statistics, libraries | ggplot2, corrplot, pheatmap, arules, rpart, e1071, class, caret |
| **Excel** | Formulas and walkthroughs | COUNTIF, QUARTILE, CORREL, RANK.AVG, COVARIANCE.S |

---

## Python Project Conventions

Python files follow a consistent 8-section structure:

```
Section 1: Imports
Section 2: Constants
Section 3: Demo Dataset
Section 4: Helper Functions
Section 5: Core Analysis
Section 6: Printing / Reporting
Section 7: File I/O  (includes standard load_csv)
Section 8: Main
```

- Most labs use no external libraries; the pattern-mining library comparison optionally uses pandas and mlxtend
- No lambda expressions — explicit for-loops throughout
- ASCII-only output (runs on any terminal/encoding)
- Each script can run standalone as a demo, or accept a CSV file as input

---

## Datasets Used

| Dataset | Description | Used in |
|---------|-------------|---------|
| **Friends** | 14 friends with Max_temp, Weight, Height, Years, Gender, Company | Ch02–Ch05, Ch08 |
| **Iris** | 150 flowers, 4 measurements, 3 species | Ch03 exercises, Ch08 |
| **Friends Cuisine** | 10 friends × 5 food categories (transaction data) | Ch06 |
| **Friends Classification** | 9 friends × Food/Distance/Company (target) | Ch07 |
| **Grocery Customers** | 20 customers × items purchased | Ch08 |
| **Students** | 25 students × 4 subject scores + demographics | Ch08 |
| **Retail Customers** | 30 customers × purchase behavior + churn label | Ch08 |
| **Medical Patients** | 25 patients × cardiovascular risk factors | Ch08 |

---

## Quick Start

**Run any Python project:**
```bash
python path/to/script.py          # runs built-in demo
python path/to/script.py data.csv # loads your own CSV
```

**Run any R project:**
```r
source("path/to/script.R")        # runs in RStudio or Rscript
```

**Required R packages** (install once):
```r
install.packages(c("ggplot2", "GGally", "corrplot", "pheatmap",
                   "scatterplot3d", "aplpack", "MASS",
                   "arules", "arulesViz",
                   "rpart", "rpart.plot",
                   "e1071", "class", "caret", "dbscan"))
```

---

<div align="center">

<strong>Study the notes. Drill the exercises. Prove it in the labs.</strong>

</div>
