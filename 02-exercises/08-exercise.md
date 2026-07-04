# &#9997; 08: Mixed Review — Exercise

<div align="center" markdown>

![Data Analytics](../assets/banner.svg)

<img src="https://img.shields.io/badge/Chapter_08-Mixed_Review-34526B?style=for-the-badge&labelColor=22384A" alt="Chapter 08: Mixed Review"> <img src="https://img.shields.io/badge/8_questions-1E9E75?style=for-the-badge&labelColor=167A5A" alt="8 questions">

[![Home](https://img.shields.io/badge/⌂_Home-22384A?style=flat-square)](../index.md) [![Notes](https://img.shields.io/badge/Notes-22384A?style=flat-square)](../01-notes/08-summary.md) [![All Exercises](https://img.shields.io/badge/All_Exercises-22384A?style=flat-square)](README.md) [![Quiz](https://img.shields.io/badge/▶_Quiz-1E9E75?style=flat-square&labelColor=167A5A)](../03-quiz/)

</div>

> [!TIP]
> **Practice —** a quick capstone review, one question per chapter, before moving on to the [Projects](../04-projects/README.md). Try each one from memory first.

---

### &#128313; Q1. (Ch01) A dataset column stores product ratings 1–5 stars. Is this ordinal or interval, and why does it matter for which statistics you can compute?

<details>
<summary><strong>Show answer</strong></summary>

**Ordinal** — the stars are ordered (5 &gt; 4 &gt; ... &gt; 1), but the "distance" between 4 and 5 stars isn't guaranteed to equal the distance between 1 and 2 stars in the rater's mind. That means mode and median are always safe, but the arithmetic **mean** technically assumes equal intervals — common in practice, but statistically an approximation for ordinal data.
</details>

---

### &#128202; Q2. (Ch02) A distribution has mean = 50 and median = 42. Is it left-skewed or right-skewed?

<details>
<summary><strong>Show answer</strong></summary>

**Right-skewed (positively skewed)** — the mean is pulled above the median by a long tail of high values. Rule of thumb: mean &gt; median → right-skewed; mean &lt; median → left-skewed.
</details>

---

### &#128200; Q3. (Ch03) You need to compare 6 numeric attributes across 40 objects in one static image. Name two multivariate visualization techniques that could work, and one that would not scale well.

<details>
<summary><strong>Show answer</strong></summary>

Good fits: **parallel coordinates** (one axis per attribute, works well up to a dozen or so attributes) and a **correlogram/heatmap** (summarizes all pairwise relationships in one grid). A **scatter plot matrix** (`ggpairs`-style) technically works but becomes visually cramped once you're past ~6–8 attributes since it draws every pair.
</details>

---

### &#129513; Q4. (Ch04) Why must categorical attributes typically be one-hot encoded (or similarly transformed) before feeding them into distance-based methods like k-means or k-NN?

<details>
<summary><strong>Show answer</strong></summary>

Distance formulas like Euclidean distance assume numeric, ordered values where subtraction is meaningful. Nominal categories (e.g., "chinese", "italian", "burgers") have no numeric ordering — encoding them as 1, 2, 3 would falsely imply italian is "between" chinese and burgers. One-hot encoding avoids this by giving each category its own binary dimension with no artificial ordering or distance relationship imposed.
</details>

---

### &#128200; Q5. (Ch05) K-means requires you to choose k in advance and is sensitive to outliers. Name one clustering method that doesn't require k up front, and one that's more robust to outliers.

<details>
<summary><strong>Show answer</strong></summary>

**Hierarchical clustering** doesn't require k in advance — you build the full dendrogram and cut it at whatever level gives the desired number of clusters afterward. **DBSCAN** is more robust to outliers than k-means because it explicitly labels low-density points as **noise** rather than forcing every point into some cluster (which is what drags k-means centroids toward outliers).
</details>

---

### &#128279; Q6. (Ch06) An itemset {bread, milk} has support 0.4. The rule {bread} &rarr; {milk} has confidence 0.8. What is P(milk)... can you tell from this alone, and what would let you compute the rule's lift?

<details>
<summary><strong>Show answer</strong></summary>

Support and confidence alone don't give you P(milk) directly — you'd also need **support({milk})** (or equivalently support({bread})), since confidence({bread}&rarr;{milk}) = support({bread,milk}) / support({bread}). Lift = confidence / support({milk}), so once you know support({milk}) you can compute lift = 0.8 / support({milk}) — lift &gt; 1 means bread and milk co-occur more than chance would predict.
</details>

---

### &#127795; Q7. (Ch07) Between a decision tree and Naive Bayes, which one assumes feature independence, and what's one practical downside of that assumption?

<details>
<summary><strong>Show answer</strong></summary>

**Naive Bayes** assumes every feature is conditionally independent given the class. In practice, features are often correlated (e.g., Age and Distance-traveled might both relate to Company in similar ways) — Naive Bayes will effectively "double count" that shared signal, which can bias the posterior even though the predicted class often still comes out right in simple cases.
</details>

---

### &#127942; Q8. (Capstone) You're asked to build an early-warning system for at-risk students from grades, attendance, and demographics. Name one technique from each of Chapters 4, 5/6, and 7 you'd use, and in what order.

<details>
<summary><strong>Show answer</strong></summary>

A reasonable pipeline: **(Ch4) clean and normalize** the data first — handle missing grades, encode categorical demographics, min-max/z-score the numeric scores; **(Ch5) cluster** students (k-means or hierarchical) to discover natural risk groups without labels, as an exploratory step; **(Ch7) classify** using a decision tree or k-NN trained on a labeled "at-risk / not at-risk" outcome to get an actual predictive early-warning score, evaluated with a confusion matrix and k-fold CV. This mirrors the [Student Performance Predictor](../04-projects/08-project-05/README.md) capstone project.
</details>

---

[📚 All Exercises](README.md)

<div align="center" markdown>

[All Exercises](README.md) &nbsp;|&nbsp; [Course Summary Notes](../01-notes/08-summary.md) &nbsp;|&nbsp; <strong>Next:</strong> [Projects](../04-projects/README.md)

</div>
