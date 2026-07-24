# &#128193; Learning Toolkit

<div align="center" markdown>

![Data Analytics](../assets/banner.svg)

[![View the live site — ijk37.com](https://img.shields.io/badge/%F0%9F%87%A7%F0%9F%87%A9_View_the_Live_Site-IJK37.COM-F42A41?style=for-the-badge&labelColor=006A4E)](https://ijk37.com/data-analytics/)

<img src="https://img.shields.io/badge/05_·_Toolkit-Setup_%26_Study_Guides-22384A?style=for-the-badge&labelColor=17252A" alt="Learning toolkit">

[Home](../index.md) | [Notes](../01-notes/README.md) | [Exercises](../02-exercises/README.md) | [Quiz Hub](../03-quiz/index.html) | [Projects](../04-projects/README.md)

</div>

Use this page to set up the project code, prepare a dataset, choose a reference, and turn a completed lab into a clear analytical write-up.

## Quick Reference Desk

| Need | Best starting point |
| --- | --- |
| A formula or method-selection reminder | [Course summary and decision guide](../01-notes/08-summary.md) |
| A worked problem | [Exercise dashboard](../02-exercises/README.md) |
| Fast recall practice | [Randomized Quiz Hub](../03-quiz/index.html) |
| A runnable example | [Project dashboard](../04-projects/README.md) |
| A complete applied workflow | [Module 08 capstones](../04-projects/README.md#module-08-final-projects-capstones) |

## Run the Project Code

### Python

The Python projects use the standard library, so Python 3 is enough for most labs.

```bash
# Run a project's built-in demonstration
python 04-projects/01-project-01/attribute_audit.py

# Pass a CSV file when the project supports file input
python 04-projects/01-project-01/attribute_audit.py your_data.csv
```

### R

Open a project in RStudio or run it from an R console:

```r
source("04-projects/05-project-02/kmeans_clustering.R")
```

Some visualization and modeling projects use packages such as `ggplot2`, `corrplot`, `pheatmap`, `arules`, `rpart`, `e1071`, `caret`, or `dbscan`. Each project README explains what its script needs.

### Excel

Selected exercises include formula walkthroughs for frequency tables, quartiles, correlation, covariance, and ranking. Use a copy of the data so you can compare formula results with the Python or R implementation.

## Prepare Your Own CSV

Before using a project with your data:

1. Keep a header row with short, descriptive, unique column names.
2. Use one row per observation and one column per attribute.
3. Store missing values consistently (`NA` or an empty field, not several different markers).
4. Remove totals, merged cells, footnotes, and presentation-only rows.
5. Save an untouched copy of the original data before cleaning.
6. Check the project README for its expected target column, numeric fields, or transaction format.

> [!WARNING]
> The scripts are educational implementations. Validate inferred types, cleaning choices, model assumptions, and outputs before using them for real decisions.

## Analytical Write-Up Checklist

A strong project is more than code. Document:

- **Question:** What decision or uncertainty is the analysis addressing?
- **Data:** What does one row represent, which fields are used, and what are the limitations?
- **Preparation:** What was removed, imputed, encoded, transformed, or scaled—and why?
- **Method:** Why is the chosen statistic or algorithm appropriate?
- **Evaluation:** Which checks or metrics support the result?
- **Interpretation:** What does the result mean in the original context?
- **Limits:** What cannot be concluded, and what data would improve the analysis?
- **Reproduction:** Which script, parameters, and environment recreate the result?

## Recommended Study Loop

```text
Read one concept
      ↓
Solve without looking
      ↓
Quiz from memory
      ↓
Run and modify a project
      ↓
Explain the result in plain language
```

## Source Material and Licensing

The repository owner's original lecture slides and assignment files remain local-only because they may contain copyrighted course material. They are not published or included in git. The public notes, exercises, quiz questions, and project explanations are the cleaned, structured learning materials intended for this site.

<div align="center" markdown>

[Course home](../index.md) · [Start with the notes](../01-notes/README.md)

</div>
