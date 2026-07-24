# &#9997; 07: Classification — Exercise

<div align="center" markdown>

![Data Analytics](../assets/banner.svg)

<img src="https://img.shields.io/badge/Chapter_07-Classification-34526B?style=for-the-badge&labelColor=22384A" alt="Chapter 07: Classification"> <img src="https://img.shields.io/badge/5_questions-1E9E75?style=for-the-badge&labelColor=167A5A" alt="5 questions">

[![Home](https://img.shields.io/badge/⌂_Home-22384A?style=flat-square)](../index.md) [![Notes](https://img.shields.io/badge/Notes-22384A?style=flat-square)](../01-notes/07-classification.md) [![All Exercises](https://img.shields.io/badge/All_Exercises-22384A?style=flat-square)](README.md) [![Quiz](https://img.shields.io/badge/▶_Quiz-1E9E75?style=flat-square&labelColor=167A5A)](../03-quiz/index.html)

</div>

> [!TIP]
> **Practice —** try each question first, then expand the answer to check your reasoning. Q1 and Q3 reuse the **Friends Food classifier** dataset from the notes (9 examples, target = Company, 6 good / 3 bad) — this exercise asks about different splits/queries than the ones already worked out there, so review the [notes](../01-notes/07-classification.md) first.

---

### &#127795; Q1. Compute the Gini impurity of the root node and the Gini split for the "Food" attribute (chinese: 4 rows, 2 good/2 bad · italian: 3 rows, 3 good/0 bad · burgers: 2 rows, 1 good/1 bad).

<details>
<summary><strong>Show answer</strong></summary>

Root: Gini(S) = 1 − ((6/9)&sup2; + (3/9)&sup2;) = 1 − (0.4444 + 0.1111) = **0.4444**

Per-value Gini: chinese = 1 − (0.5&sup2;+0.5&sup2;) = 0.5 · italian = 1 − (1&sup2;+0&sup2;) = 0 · burgers = 1 − (0.5&sup2;+0.5&sup2;) = 0.5

Gini_split(S, Food) = (4/9)(0.5) + (3/9)(0) + (2/9)(0.5) = 0.2222 + 0 + 0.1111 = **0.3333**

Lower Gini_split is better (CART picks the attribute that *minimizes* it) — compare this to the notes' entropy-based IG(Food) = 0.252 computed the same underlying split a different way.
</details>

---

### &#128205; Q2. Training points (x, y, class): (1,1,A), (2,1,A), (4,3,B), (5,4,B), (1,2,A). Classify a new point (3, 2) using k-NN with k = 3.

<details>
<summary><strong>Show answer</strong></summary>

Euclidean distances from (3,2):

| Point | Class | Distance |
| --- | --- | --- |
| (2,1) | A | &radic;(1+1) = 1.414 |
| (4,3) | B | &radic;(1+1) = 1.414 |
| (1,2) | A | &radic;(4+0) = 2.000 |
| (1,1) | A | &radic;(4+1) = 2.236 |
| (5,4) | B | &radic;(4+4) = 2.828 |

3 nearest neighbors: (2,1)=A, (4,3)=B, (1,2)=A → majority vote = **2 A vs 1 B → predict A**.

If two distances tie exactly (as (2,1) and (4,3) do here), either can be picked first for the k-th slot without changing this result — but it's worth checking whether a tie changes the majority in general.
</details>

---

### &#127860; Q3. Using Naive Bayes, classify Food = italian, Distance = far. Why does this query fail without Laplace smoothing, and what does smoothing change?

<details>
<summary><strong>Show answer</strong></summary>

Raw counts from the 9-row dataset: **italian** never appears in a *bad* row (0/3), so P(Food=italian | bad) = 0/3 = **0** — this single zero wipes out the entire product for the "bad" class, regardless of the other evidence.

**With Laplace smoothing** — add 1 to every count; Food has 3 possible values (chinese/italian/burgers), Distance has 5 (close/very_close/far/very_far/too_far):

P(Food=italian&#124;good) = (3+1)/(6+3) = 0.444  ·  P(Food=italian&#124;bad) = (0+1)/(3+3) = 0.167
P(Distance=far&#124;good) = (1+1)/(6+5) = 0.182  ·  P(Distance=far&#124;bad) = (1+1)/(3+5) = 0.250

Score(good) = P(good) &times; 0.444 &times; 0.182 = 0.667 &times; 0.444 &times; 0.182 ≈ **0.0538**
Score(bad) = P(bad) &times; 0.167 &times; 0.250 = 0.333 &times; 0.167 &times; 0.250 ≈ **0.0139**

Score(good) > Score(bad) → **predict good**. Laplace smoothing replaces "impossible" (zero-count) combinations with a small nonzero probability, so one unseen combination no longer silently disqualifies an entire class.
</details>

---

### &#128202; Q4. A model's confusion matrix on a 100-row test set gives TP = 40, FP = 10, FN = 5, TN = 45. Compute accuracy, precision, recall, and F1.

<details>
<summary><strong>Show answer</strong></summary>

- **Accuracy** = (40+45)/100 = **0.85**
- **Precision** = 40/(40+10) = **0.80**
- **Recall** = 40/(40+5) = **0.889**
- **F1** = 2 &times; (0.80 &times; 0.889) / (0.80 + 0.889) = 1.422/1.689 ≈ **0.842**

Precision and recall diverge here (0.80 vs 0.889) because false positives (10) outnumber false negatives (5) — this model is slightly more likely to over-predict the positive class than to miss one.
</details>

---

### &#128260; Q5. Why is 5-fold or 10-fold cross-validation preferred over a single train/test split, and what does *stratified* k-fold add on top of that?

<details>
<summary><strong>Show answer</strong></summary>

A single split gives one accuracy number that depends heavily on which rows happened to land in the test set — an unlucky split can make a good model look bad or vice versa. **k-fold CV** trains and evaluates k times (each fold takes a turn as the held-out test set) and averages the results, so the final accuracy — and its standard deviation — reflects performance across the *whole* dataset rather than one lucky/unlucky split.

**Stratified k-fold** additionally ensures each fold preserves the original class proportions (e.g., if the full dataset is 67% good / 33% bad, every fold is too). Without stratification, a fold could end up almost entirely one class by chance — especially damaging on small or imbalanced datasets like the 9-row Friends example.
</details>

---

[📚 All Exercises](README.md)  ·  **Next:** [Chapter 08 — Mixed Review](08-exercise.md) ➡️

<div align="center" markdown>

[All Exercises](README.md) &nbsp;|&nbsp; [Chapter 07 Notes](../01-notes/07-classification.md) &nbsp;|&nbsp; <strong>Next:</strong> [08: Mixed Review — Exercise](08-exercise.md)

</div>
