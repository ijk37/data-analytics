# &#9997; 04: Data Quality & Preprocessing — Exercise

<div align="center" markdown>

![Data Analytics](../assets/banner.svg)

<img src="https://img.shields.io/badge/Chapter_04-Data_Quality_%26_Preprocessing-34526B?style=for-the-badge&labelColor=22384A" alt="Chapter 04: Data Quality & Preprocessing"> <img src="https://img.shields.io/badge/5_questions-1E9E75?style=for-the-badge&labelColor=167A5A" alt="5 questions">

[![Home](https://img.shields.io/badge/⌂_Home-22384A?style=flat-square)](../index.md) [![Notes](https://img.shields.io/badge/Notes-22384A?style=flat-square)](../01-notes/04-data-quality-and-preprocessing.md) [![All Exercises](https://img.shields.io/badge/All_Exercises-22384A?style=flat-square)](README.md) [![Quiz](https://img.shields.io/badge/▶_Quiz-1E9E75?style=flat-square&labelColor=167A5A)](../03-quiz/index.html)

</div>

> [!TIP]
> **Practice —** try each question first, then expand the answer to check your reasoning.

**Data for Q1–Q4:** 31, 38, 42, 29, 46, 23, 83, 43, 51, 55, 27, 35 (min = 23, max = 83, range = 60, n = 12)

---

### &#128202; Q1. Discretize the data above into 4 bins using **equal-width** partitioning, then using **equal-depth** partitioning.

<details>
<summary><strong>Show answer</strong></summary>

**Equal-width** (bin width = 60/4 = 15): Bin 1: 23–37 · Bin 2: 38–52 · Bin 3: 53–67 · Bin 4: 68–83

| Data | 31 | 38 | 42 | 29 | 46 | 23 | 83 | 43 | 51 | 55 | 27 | 35 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bin | 1 | 2 | 2 | 1 | 2 | 1 | 4 | 2 | 2 | 3 | 1 | 1 |

**Equal-depth** (12 values ÷ 4 bins = 3 values/bin, sorted first): Bin 1: {23,27,29} · Bin 2: {31,35,38} · Bin 3: {42,43,46} · Bin 4: {51,55,83}

| Data | 31 | 38 | 42 | 29 | 46 | 23 | 83 | 43 | 51 | 55 | 27 | 35 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bin | 2 | 2 | 3 | 1 | 3 | 1 | 4 | 3 | 4 | 4 | 1 | 2 |

Equal-width bins have equal *ranges* but can hold very different *counts* (bin 4 here only has the outlier 83). Equal-depth bins have equal *counts* but ranges that stretch to absorb outliers.
</details>

---

**Data for Q2–Q3:** a Food/Distance/Company table, first 5 rows: Chinese/far/good, Italian/very close/good, Italian/close/good, American/far/bad, Chinese/very far/good.

### &#128290; Q2. One-hot encode the **Food** values in the first 5 rows (unique order: American, Chinese, Italian, Japanese).

<details>
<summary><strong>Show answer</strong></summary>

| Row | Food | One-hot [American, Chinese, Italian, Japanese] |
| --- | --- | --- |
| 1 | Chinese | [0, 1, 0, 0] |
| 2 | Italian | [0, 0, 1, 0] |
| 3 | Italian | [0, 0, 1, 0] |
| 4 | American | [1, 0, 0, 0] |
| 5 | Chinese | [0, 1, 0, 0] |

One-hot encoding gives each category its own binary column with no implied ordering — appropriate because Food is **nominal**.
</details>

---

### &#128290; Q3. Convert the **Distance** values in the first 5 rows to 3-bit Gray code, given the natural order: very close < close < far < very far < too far.

<details>
<summary><strong>Show answer</strong></summary>

Gray code sequence: very close→000, close→001, far→011, very far→010, too far→110

| Row | Distance | Gray code |
| --- | --- | --- |
| 1 | far | 011 |
| 2 | very close | 000 |
| 3 | close | 001 |
| 4 | far | 011 |
| 5 | very far | 010 |

Gray code changes only **1 bit** between adjacent ordinal values (000→001→011→010→110), which preserves the ordering better than plain binary counting for ordinal attributes.
</details>

---

### &#128202; Q4. Apply min-max normalization to the Q1 dataset so all values fall in [0, 1].

<details>
<summary><strong>Show answer</strong></summary>

Formula: x&#8242; = (x − min) / (max − min) = (x − 23) / 60

| Real | 31 | 38 | 42 | 29 | 46 | 23 | 83 | 43 | 51 | 55 | 27 | 35 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0,1] | 0.133 | 0.250 | 0.317 | 0.100 | 0.383 | 0.000 | 1.000 | 0.333 | 0.467 | 0.533 | 0.067 | 0.200 |

The min maps to 0, the max maps to 1, and everything else is a proportional position between them.
</details>

---

### &#128207; Q5. What is the Euclidean distance between x = (1, 3, −2, 5) and y = (2, 4, 1, 6)?

<details>
<summary><strong>Show answer</strong></summary>

Difference (y − x) = (1, 1, 3, 1)

d(x, y) = &radic;(1&sup2; + 1&sup2; + 3&sup2; + 1&sup2;) = &radic;(1+1+9+1) = &radic;12 = 2&radic;3 ≈ **3.464**
</details>

---

[📚 All Exercises](README.md)  ·  **Next:** [Chapter 05 — Clustering](05-exercise.md) ➡️

<div align="center" markdown>

[All Exercises](README.md) &nbsp;|&nbsp; [Chapter 04 Notes](../01-notes/04-data-quality-and-preprocessing.md) &nbsp;|&nbsp; <strong>Next:</strong> [05: Clustering — Exercise](05-exercise.md)

</div>
