# &#9997; 05: Clustering — Exercise

<div align="center" markdown>

![Data Analytics](../assets/banner.svg)

<img src="https://img.shields.io/badge/Chapter_05-Clustering-34526B?style=for-the-badge&labelColor=22384A" alt="Chapter 05: Clustering"> <img src="https://img.shields.io/badge/3_questions-1E9E75?style=for-the-badge&labelColor=167A5A" alt="3 questions">

[![Home](https://img.shields.io/badge/⌂_Home-22384A?style=flat-square)](../index.md) [![Notes](https://img.shields.io/badge/Notes-22384A?style=flat-square)](../01-notes/05-clustering.md) [![All Exercises](https://img.shields.io/badge/All_Exercises-22384A?style=flat-square)](README.md) [![Quiz](https://img.shields.io/badge/▶_Quiz-1E9E75?style=flat-square&labelColor=167A5A)](../03-quiz/)

</div>

> [!TIP]
> **Practice —** try each question first, then expand the answer to check your reasoning.

**Dataset** (a "social network" sample, Age &amp; Educational level):

| Name | Age | Educational level |
| --- | --- | --- |
| Andrew (A) | 55 | 1 |
| Bernhard (B) | 43 | 2 |
| Carolina (C) | 37 | 5 |
| Dennis (D) | 82 | 3 |
| Eve (E) | 23 | 3.2 |
| Fred (F) | 46 | 5 |

Run **k-means with k = 2**, using Andrew and Carolina as the initial centroids.

---

### &#128200; Q1. Assign each point to its nearest centroid (Euclidean distance) for the first iteration.

<details>
<summary><strong>Show answer</strong></summary>

Centroid 1 = A = (55, 1); Centroid 2 = C = (37, 5)

| Point | Dist to A | Dist to C | Assigned |
| --- | --- | --- | --- |
| A (55,1) | 0 | 17.2 | Cluster 1 |
| B (43,2) | 12.0 | 6.7 | Cluster 2 |
| C (37,5) | 17.2 | 0 | Cluster 2 |
| D (82,3) | 27.1 | 45.2 | Cluster 1 |
| E (23,3.2) | 32.4 | 14.0 | Cluster 2 |
| F (46,5) | 9.85 | 9.0 | Cluster 2 |

**Cluster 1** = {A, D}; **Cluster 2** = {B, C, E, F}. Each distance uses d = &radic;((x&#8321;−x&#8322;)&sup2; + (y&#8321;−y&#8322;)&sup2;).
</details>

---

### &#128260; Q2. Recompute the centroids of both clusters after this first assignment.

<details>
<summary><strong>Show answer</strong></summary>

**Cluster 1** {A(55,1), D(82,3)}: Age = (55+82)/2 = 68.5, Edu = (1+3)/2 = 2 → **New centroid 1 = (68.5, 2)**

**Cluster 2** {B(43,2), C(37,5), E(23,3.2), F(46,5)}: Age = (43+37+23+46)/4 = 37.25, Edu = (2+5+3.2+5)/4 = 3.8 → **New centroid 2 = (37.25, 3.8)**

Notice both centroids moved away from their original seed points (Andrew, Carolina) toward the center of mass of their assigned members — this is exactly what the "means" in k-means recomputes each iteration.
</details>

---

### &#128202; Q3. In R, how would you compute the distances, assign clusters, and plot the result with the recomputed centroids?

<details>
<summary><strong>Show answer</strong></summary>

```r
table_data <- data.frame(
  Name = c("Andrew","Bernhard","Carolina","Dennis","Eve","Fred"),
  Age  = c(55, 43, 37, 82, 23, 46),
  Edu  = c(1, 2, 5, 3, 3.2, 5))

centroid1 <- c(55, 1); centroid2 <- c(37, 5)
table_data$dist_to_A <- sqrt((table_data$Age-centroid1[1])^2 + (table_data$Edu-centroid1[2])^2)
table_data$dist_to_C <- sqrt((table_data$Age-centroid2[1])^2 + (table_data$Edu-centroid2[2])^2)
table_data$Cluster <- ifelse(table_data$dist_to_A < table_data$dist_to_C, 1, 2)

new_centroids <- aggregate(cbind(Age, Edu) ~ Cluster, data = table_data, FUN = mean)

plot(table_data$Age, table_data$Edu,
     col = ifelse(table_data$Cluster == 1, "blue", "red"), pch = 16,
     xlab = "Age", ylab = "Educational Level", main = "K-means: First Iteration")
text(table_data$Age, table_data$Edu, labels = table_data$Name, pos = 3)
points(new_centroids$Age, new_centroids$Edu, col = c("blue","red"), pch = 8, cex = 1)
```

A real run would repeat the distance/assign/recompute loop until the assignments stop changing (convergence) — this exercise only walks through iteration 1 by hand.
</details>

---

[📚 All Exercises](README.md)  ·  **Next:** [Chapter 06 — Frequent Pattern Mining](06-exercise.md) ➡️

<div align="center" markdown>

[All Exercises](README.md) &nbsp;|&nbsp; [Chapter 05 Notes](../01-notes/05-clustering.md) &nbsp;|&nbsp; <strong>Next:</strong> [06: Frequent Pattern Mining — Exercise](06-exercise.md)

</div>
