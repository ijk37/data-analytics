# Project 07: Comprehensive Course Capstone -- "Know Your Data"

**Subtitle:** Chapters combined: Ch1 + Ch2 + Ch3 + Ch4 + Ch5 + Ch6 + Ch7

---

## What This Project Does

This is the ultimate capstone: every technique from the entire course applied to a single medical
dataset, in a deliberate sequence that mirrors the professional data analytics workflow.

The philosophy is **"Know Your Data"** -- before you model, you must understand:
- What the data IS (attributes, types, scales)
- What each attribute LOOKS like (distributions, skew, outliers)
- How attributes RELATE to each other (correlations, patterns)
- Whether the data is CLEAN (missing values, outliers, transformations needed)
- What NATURAL GROUPS exist (clustering)
- What COMBINATION RULES emerge (pattern mining)
- Whether a PREDICTIVE MODEL can be built (classification)

A structured 8-phase report is printed at the end summarizing key findings.

---

## Dataset Description

**25 patient records** -- medical heart risk assessment data. No external file is needed;
the dataset is hardcoded in both scripts.

| Column | Type | Description |
|---|---|---|
| PatientID | Nominal | Unique identifier (P01--P25) |
| Age | Ratio/Continuous | Patient age in years |
| BMI | Ratio/Continuous | Body Mass Index |
| BloodPressure | Ratio/Continuous | Systolic blood pressure (mmHg) |
| Cholesterol | Ratio/Continuous | Total cholesterol (mg/dL) |
| Glucose | Ratio/Continuous | Fasting glucose (mg/dL) |
| SmokingYears | Ratio/Continuous | Years of smoking (0 = never smoked) |
| ExerciseHrs | Ratio/Continuous | Exercise hours per week |
| Diet | Ordinal | poor < fair < good |
| HeartRisk | Ordinal | low < medium < high (TARGET) |

**Class balance:** 10 high-risk, 5 medium-risk, 10 low-risk patients.

**Deliberate missing values injected in Phase 4** (P05 BMI, P12 Cholesterol) to practice imputation.

---

## How to Run

### Python
```
python course_capstone.py
```
Requires only Python standard library (csv, math, collections, io). No pip installs needed.

### R
```
Rscript course_capstone.R
```
Requires: `arules` (install.packages("arules")), `e1071` (install.packages("e1071")),
`class` (install.packages("class")).
Optional: `corrplot` for visualization (install.packages("corrplot")).

---

## What to Look For in Output

| Phase | Key question |
|---|---|
| Phase 1 | What is the class distribution? Is HeartRisk balanced? |
| Phase 2 | Which attributes have high skewness? (SmokingYears is zero-heavy) |
| Phase 3 | Which pairs of attributes are most strongly correlated? (Expect Cholesterol-Glucose, Age-BP) |
| Phase 4 | How does group-mean imputation differ from global-mean imputation? |
| Phase 5 | Do K-means clusters align with the HeartRisk labels? Check cluster purity. |
| Phase 6 | Which combination of discretized risk factors co-occurs most often? |
| Phase 7 | For "high" risk class, which classifier achieves better recall? (Recall matters most in medicine.) |
| Phase 8 | Are the same 3--4 risk factors identified consistently across correlation, clustering, and classification? |

---

## Learning Objectives

After working through this project you should be able to:
- Explain the full professional analytics workflow from raw data to actionable insights.
- Distinguish ordinal attributes from ratio attributes and explain why it matters for analysis.
- Choose appropriate imputation strategies (global mean vs. group mean) and justify the choice.
- Interpret cluster purity as a validation measure for unsupervised learning.
- Explain why recall for the high-risk class is the most clinically important metric.
- Synthesize findings across multiple techniques into a coherent data story.
