# &#9997; 03: Multivariate Analysis — Exercise

<div align="center" markdown>

![Data Analytics](../assets/banner.svg)

<img src="https://img.shields.io/badge/Chapter_03-Multivariate_Analysis-34526B?style=for-the-badge&labelColor=22384A" alt="Chapter 03: Multivariate Analysis"> <img src="https://img.shields.io/badge/8_questions-1E9E75?style=for-the-badge&labelColor=167A5A" alt="8 questions">

[![Home](https://img.shields.io/badge/⌂_Home-22384A?style=flat-square)](../index.md) [![Notes](https://img.shields.io/badge/Notes-22384A?style=flat-square)](../01-notes/03-descriptive-multivariate-analysis.md) [![All Exercises](https://img.shields.io/badge/All_Exercises-22384A?style=flat-square)](README.md) [![Quiz](https://img.shields.io/badge/▶_Quiz-1E9E75?style=flat-square&labelColor=167A5A)](../03-quiz/)

</div>

> [!TIP]
> **Practice —** try each question first, then expand the answer to check your reasoning. All answers use the built-in **Iris** dataset (150 flowers, 4 measurements, 3 species) in R.

---

### &#128200; Q1. How would you build a scatter plot of Sepal Length vs Sepal Width where the point *size* encodes Petal Length?

<details>
<summary><strong>Show answer</strong></summary>

```r
library(ggplot2)
ggplot(iris, aes(x = Sepal.Length, y = Sepal.Width, size = Petal.Length)) +
  geom_point(alpha = 0.7) +
  labs(title = "Sepal Length vs Sepal Width (size = Petal Length)")
```
Mapping a third numeric attribute to point **size** turns a 2D scatter into a pseudo-3D view without a 3D plot.
</details>

---

### &#127752; Q2. How would you show Species as both color and shape on a Sepal Length vs Sepal Width scatter plot?

<details>
<summary><strong>Show answer</strong></summary>

```r
ggplot(iris, aes(x = Sepal.Length, y = Sepal.Width, color = Species, shape = Species)) +
  geom_point(size = 3, alpha = 0.8)
```
Encoding a categorical attribute with **both** color and shape (rather than just one) keeps the plot readable for colorblind viewers and in grayscale print.
</details>

---

### &#127760; Q3. How do you build a 3D scatter plot of Sepal Length, Sepal Width, and Petal Length?

<details>
<summary><strong>Show answer</strong></summary>

```r
library(scatterplot3d)
scatterplot3d(iris$Sepal.Length, iris$Sepal.Width, iris$Petal.Length, pch = 16)
```
True 3D plots work for exactly 3 numeric attributes; beyond that you need parallel coordinates, star plots, or dimensionality reduction.
</details>

---

### &#128200; Q4. How do you build a parallel coordinates plot for all four numeric attributes, colored by Species?

<details>
<summary><strong>Show answer</strong></summary>

```r
library(MASS)
cols <- c(setosa = "red", versicolor = "blue", virginica = "darkgreen")
parcoord(iris[, 1:4], col = cols[iris$Species], lwd = 1.5)
```
Each vertical axis is one attribute; each line is one flower. Species that cluster tightly on the same path show up as bands of similar-colored lines.
</details>

---

### &#11088; Q5. How do you build a star plot for the first 20 Iris objects, and what is each object's mode?

<details>
<summary><strong>Show answer</strong></summary>

```r
stars(iris[1:20, 1:4], labels = paste0("Obj", 1:20))
```
Each object becomes a many-pointed "star" — one ray per attribute, ray length proportional to that attribute's value. Object shapes that look alike represent similar flowers.

For the **mode** of each attribute across the full 150-row dataset:

| Attribute | Min | Max | Mean | Mode |
| --- | --- | --- | --- | --- |
| Sepal Length | 4.3 | 7.9 | 5.843 | 5.0 |
| Sepal Width | 2.0 | 4.4 | 3.057 | 3.0 |
| Petal Length | 1.0 | 6.9 | 3.758 | 1.4 |
| Petal Width | 0.1 | 2.5 | 1.199 | 0.2 |
</details>

---

### &#128202; Q6. What are the amplitude (range), mean absolute deviation, and standard deviation of the four numeric attributes?

<details>
<summary><strong>Show answer</strong></summary>

| Attribute | Amplitude | Mean Abs. Deviation | Std. Deviation |
| --- | --- | --- | --- |
| Sepal Length | 3.6 | 0.688 | 0.828 |
| Sepal Width | 2.4 | 0.337 | 0.436 |
| Petal Length | 5.9 | 1.563 | 1.765 |
| Petal Width | 2.4 | 0.658 | 0.762 |

Amplitude = max − min. Mean absolute deviation averages |x − mean| across all rows (more robust to outliers than variance). Petal Length has both the widest range and highest spread — it's the most discriminating attribute between species.
</details>

---

### &#128512; Q7. What is a Chernoff face, and how would you generate one for the first 20 Iris objects?

<details>
<summary><strong>Show answer</strong></summary>

```r
library(aplpack)
faces(iris[1:20, 1:4], main = "Chernoff Faces: First 20 Iris Objects")
```
A Chernoff face maps each numeric attribute to a facial feature (face width, eye size, mouth curve, ...). Humans are very good at spotting subtle differences between faces, so this can reveal multivariate patterns that are hard to see in tables — at the cost of being somewhat subjective to read.
</details>

---

### &#128202; Q8. How do you build a scatter plot matrix with Pearson correlation coefficients, a correlogram, and a heatmap for the four numeric attributes?

<details>
<summary><strong>Show answer</strong></summary>

```r
library(GGally); library(corrplot); library(pheatmap)

# Scatter plot matrix + Pearson correlations
ggpairs(iris, columns = 1:4)

# Correlogram
corrplot(cor(iris[,1:4], method = "pearson"), method = "color",
         type = "upper", addCoef.col = "black")

# Heatmap (scaled so all attributes are comparable)
pheatmap(scale(iris[,1:4]), cluster_rows = TRUE, cluster_cols = TRUE)
```
`ggpairs` puts a scatter plot in the lower triangle and the correlation coefficient in the upper triangle for every attribute pair in one view. The correlogram color-codes the same correlation matrix; the heatmap additionally clusters similar rows/columns together via a dendrogram.
</details>

---

[📚 All Exercises](README.md)  ·  **Next:** [Chapter 04 — Data Quality & Preprocessing](04-exercise.md) ➡️

<div align="center" markdown>

[All Exercises](README.md) &nbsp;|&nbsp; [Chapter 03 Notes](../01-notes/03-descriptive-multivariate-analysis.md) &nbsp;|&nbsp; <strong>Next:</strong> [04: Data Quality & Preprocessing — Exercise](04-exercise.md)

</div>
