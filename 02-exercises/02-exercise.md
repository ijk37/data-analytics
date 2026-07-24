# &#9997; 02: Descriptive Statistics — Exercise

<div align="center" markdown>

![Data Analytics](../assets/banner.svg)

<img src="https://img.shields.io/badge/Chapter_02-Descriptive_Statistics-34526B?style=for-the-badge&labelColor=22384A" alt="Chapter 02: Descriptive Statistics"> <img src="https://img.shields.io/badge/4_questions-1E9E75?style=for-the-badge&labelColor=167A5A" alt="4 questions">

[![Home](https://img.shields.io/badge/⌂_Home-22384A?style=flat-square)](../index.md) [![Notes](https://img.shields.io/badge/Notes-22384A?style=flat-square)](../01-notes/02-descriptive-statistics.md) [![All Exercises](https://img.shields.io/badge/All_Exercises-22384A?style=flat-square)](README.md) [![Quiz](https://img.shields.io/badge/▶_Quiz-1E9E75?style=flat-square&labelColor=167A5A)](../03-quiz/index.html)

</div>

> [!TIP]
> **Practice —** try each question first, then expand the answer to check your reasoning.

**Part A** uses the *Friends* dataset. **Part B** uses a small paired (x, y) sample to practice covariance and correlation by hand.

**Friends dataset (Part A):**

| Friend | Max temp | Weight | Height | Years | Gender | Company |
| --- | --- | --- | --- | --- | --- | --- |
| Andrew | 25 | 77 | 175 | 10 | M | Good |
| Bernhard | 31 | 110 | 195 | 12 | M | Good |
| Carolina | 15 | 70 | 172 | 2 | F | Bad |
| Dennis | 20 | 85 | 180 | 16 | M | Good |
| Eve | 10 | 65 | 168 | 0 | F | Bad |
| Fred | 12 | 75 | 173 | 6 | M | Good |
| Gwyneth | 16 | 75 | 180 | 3 | F | Bad |
| Hayden | 26 | 63 | 165 | 2 | F | Bad |
| Irene | 15 | 55 | 158 | 5 | F | Bad |
| James | 21 | 66 | 163 | 14 | M | Good |
| Kevin | 30 | 95 | 190 | 1 | M | Bad |
| Lea | 13 | 72 | 172 | 11 | F | Good |
| Marcus | 8 | 83 | 185 | 3 | F | Bad |
| Nigel | 12 | 115 | 192 | 15 | M | Good |

---

### &#128202; Q1. (Part A) Build the absolute, relative, absolute-cumulative, and relative-cumulative frequency table for **Weight**.

<details>
<summary><strong>Show answer</strong></summary>

n = 14. Every weight value in this sample is unique except 75 (appears twice).

| Weight | Absolute | Relative | Abs. Cumulative | Rel. Cumulative |
| --- | --- | --- | --- | --- |
| 55 | 1 | 7.14% | 1 | 7.14% |
| 63 | 1 | 7.14% | 2 | 14.29% |
| 65 | 1 | 7.14% | 3 | 21.43% |
| 66 | 1 | 7.14% | 4 | 28.57% |
| 70 | 1 | 7.14% | 5 | 35.71% |
| 72 | 1 | 7.14% | 6 | 42.86% |
| 75 | 2 | 14.29% | 8 | 57.14% |
| 77 | 1 | 7.14% | 9 | 64.29% |
| 83 | 1 | 7.14% | 10 | 71.43% |
| 85 | 1 | 7.14% | 11 | 78.57% |
| 95 | 1 | 7.14% | 12 | 85.71% |
| 110 | 1 | 7.14% | 13 | 92.86% |
| 115 | 1 | 7.14% | 14 | 100% |

Relative frequency = absolute / 14; cumulative columns are running totals of the columns to their left, in sorted order.
</details>

---

### &#128200; Q2. (Part A) Find the mode, median, 1st quartile (Q1), and 3rd quartile (Q3) for **Years**.

<details>
<summary><strong>Show answer</strong></summary>

Sorted **Years**: 0, 1, 2, 2, 3, 3, 5, 6, 10, 11, 12, 14, 15, 16 (n = 14)

- **Mode** — values 2 and 3 each occur twice (every other value occurs once) → **bimodal: 2 and 3**.
- **Median** — n is even, so median = average of the 7th and 8th sorted values = (5 + 6) / 2 = **5.5**.
- **Q1** — median of the lower half {0, 1, 2, 2, 3, 3, 5} (7 values, odd) → the 4th value = **2**.
- **Q3** — median of the upper half {6, 10, 11, 12, 14, 15, 16} (7 values, odd) → the 4th value = **12**.
</details>

---

**Part B dataset** (paired samples):

| x | 2 | −1 | 0 | 1 | −2 | −3 |
| --- | --- | --- | --- | --- | --- | --- |
| y | −1 | 1 | −2 | 0 | 1 | 2 |

### &#128202; Q3. (Part B) Compute the covariance and Pearson correlation coefficient between x and y.

<details>
<summary><strong>Show answer</strong></summary>

n = 6, x&#772; = −0.5, y&#772; = 0.1667

| x−x&#772; | 2.5 | −0.5 | 0.5 | 1.5 | −1.5 | −2.5 |
| --- | --- | --- | --- | --- | --- | --- |
| y−y&#772; | −1.1667 | 0.8333 | −2.1667 | −0.1667 | 0.8333 | 1.8333 |

&Sigma;(x−x&#772;)(y−y&#772;) = −10.5, &Sigma;(x−x&#772;)&sup2; = 17.5, &Sigma;(y−y&#772;)&sup2; = 10.8333

- **Cov(x, y)** = −10.5 / (n−1) = −10.5 / 5 = **−2.1**
- **Pearson r** = −10.5 / &radic;(17.5 &times; 10.8333) = −10.5 / 13.769 ≈ **−0.76**

A strong negative linear relationship — as x increases, y tends to decrease.
</details>

---

### &#128200; Q4. (Part B) Compute Spearman's rank correlation for the same data.

<details>
<summary><strong>Show answer</strong></summary>

Rank x (ascending, 1 = smallest): rx = 6, 3, 4, 5, 2, 1 (mean 3.5)
Rank y (ties averaged): ry = 2, 4.5, 1, 3, 4.5, 6 (mean 3.5)

&Sigma;(rx−rx&#772;)(ry−ry&#772;) = −14, &Sigma;(rx−rx&#772;)&sup2; = 17.5, &Sigma;(ry−ry&#772;)&sup2; = 17

**Spearman &rho;** = −14 / &radic;(17.5 &times; 17) = −14 / 17.249 ≈ **−0.81**

Spearman agrees in sign and magnitude with Pearson r here, confirming a consistent negative monotonic relationship.
</details>

---

[📚 All Exercises](README.md)  ·  **Next:** [Chapter 03 — Multivariate Analysis](03-exercise.md) ➡️

<div align="center" markdown>

[All Exercises](README.md) &nbsp;|&nbsp; [Chapter 02 Notes](../01-notes/02-descriptive-statistics.md) &nbsp;|&nbsp; <strong>Next:</strong> [03: Multivariate Analysis — Exercise](03-exercise.md)

</div>
