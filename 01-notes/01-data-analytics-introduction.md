# Chapter 1 — What Can We Do With Data?

---

## 1. What is Data Analytics?

- Core idea: **data → information → knowledge**
- **Analytics** = the science of analyzing raw data to extract useful, valid, human-understandable patterns

---

## 2. What Is Data?

| Term | Definition |
|------|-----------|
| **Instance** (object/row) | One example of the concept being studied |
| **Attribute** (feature/column) | A characteristic of an instance |
| **Attribute value** | The number or symbol assigned to an attribute for a specific object |

> A **measurement scale** is the rule (function) that maps an attribute to a value.

---

## 3. Four Types of Attributes (Stevens' Taxonomy)

| Type | Properties | Operations | Examples |
|------|-----------|-----------|---------|
| **Nominal** | Distinctness only (`=`, `≠`) | Mode, entropy, χ² | Eye color, zip code, ID |
| **Ordinal** | Distinctness + Order (`<`, `>`) | Median, percentiles, rank corr. | Grades, {good/better/best}, mineral hardness |
| **Interval** | + Meaningful differences (`+`, `−`) | Mean, std dev, Pearson's r | Temperature (°C/°F), calendar dates |
| **Ratio** | + Meaningful ratios (`×`, `÷`), true zero | Geometric/harmonic mean, % variation | Temperature (K), age, length, counts |


### Categorical vs. Numerical

```
Categorical (Qualitative)     Numerical (Quantitative)
├── Nominal                   ├── Interval
└── Ordinal                   └── Ratio
```

### Discrete vs. Continuous

- **Discrete** — finite or countably infinite values (integer variables, binary is a special case)  
  → Can be Nominal, Ordinal, Interval, or Ratio  
- **Continuous** — real-valued (floating-point); e.g., temperature, height, weight  
  → Interval or Ratio only

---

## 4. Data Structures

| Structure | Core idea | Example |
|-----------|-----------|---------|
| **Record** | Fixed attribute set per record; default tabular form | spreadsheet rows |
| **Data Matrix** | Record data where all attributes are numeric → *m × n* matrix, each row a point in n-D space | gene expression table |
| **Document** | Each doc → term-frequency vector (attributes = unique terms, values = counts) | bag-of-words corpus |
| **Transaction** | Each record = variable-length set of items; no fixed schema | shopping basket |
| **Graph** | Objects = nodes, relationships = edges | social network, molecule |
| **Ordered** | Sequential (item sets over time), Genomic (DNA over {A,T,C,G}), Spatio-Temporal (location + time) | clickstream, weather map |

---

## 5. Taxonomy of Analytics

| Type | Question Answered | Output |
|------|------------------|--------|
| **Descriptive** | "What happened?" | Summaries, patterns (applied directly to data) |
| **Diagnostic** | "Why did it happen?" | Root cause analysis |
| **Predictive** | "What will happen?" | **Model** — a generalization used for future predictions |
| **Prescriptive** | "What should we do?" | Recommended actions/strategies |

> A **model** in predictive analytics is a generalization learned from data that can generate predictions on new, unseen instances.

---

## 6. Data Analytics Methodologies

### CRISP-DM (Cross-Industry Standard Process for Data Mining) — 6 phases

```
Business Understanding → Data Understanding → Data Preparation
       ↑                                               ↓
   Deployment     ←      Evaluation      ←       Modeling
```

Each phase has sub-tasks (e.g., Data Preparation includes: Select, Clean, Construct, Integrate, Format data).

---

### KDD Process (Knowledge Discovery in Databases) — 9 steps

1. Learn application domain
2. Create target dataset
3. Clean & pre-process (missing values, noise, format)
4. Reduce & project (feature selection / engineering)
5. Choose mining function (clustering? classification? regression?)
6. Choose algorithm
7. Apply data mining
8. Interpret results → loop back if needed
9. Deploy discovered knowledge

**Mining function → analytics branch:**
- Summarization & Clustering → **Descriptive**
- Classification & Regression → **Predictive**

---

## 7. Quick-Reference: Key Distinctions

| Concept | Distinction |
|---------|------------|
| Tabular vs. Relational data | Relational uses foreign keys to express relationships *between* records across multiple tables |
| Attribute vs. Attribute Value | Same attribute can have different scales (feet vs. meters); same value set can represent different attributes |
| Algorithm vs. Method | Method = *what* to achieve; Algorithm = *how*, step-by-step, implementable in code |

---

## Apply the Chapter

Continue with the matching [Chapter 01 exercises](../02-exercises/01-exercise.md), take the [Chapter 01 quiz](../03-quiz/quiz.html?topic=01), or build one of these focused projects:

1. **[Attribute Auditor](../04-projects/01-project-01/README.md)** — infer each column's likely measurement scale, flag discrete vs. continuous values, and report missingness.
2. **[Dataset Type Explorer](../04-projects/01-project-02/README.md)** — classify a dataset as record, matrix, transaction, graph, or ordered data.
3. **[Attribute Scale Exercises](../04-projects/01-project-03/README.md)** — solve the measurement-scale examples in both Python and R.
