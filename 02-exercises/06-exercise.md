# &#9997; 06: Frequent Pattern Mining — Exercise

<div align="center" markdown>

![Data Analytics](../assets/banner.svg)

<img src="https://img.shields.io/badge/Chapter_06-Frequent_Pattern_Mining-34526B?style=for-the-badge&labelColor=22384A" alt="Chapter 06: Frequent Pattern Mining"> <img src="https://img.shields.io/badge/4_questions-1E9E75?style=for-the-badge&labelColor=167A5A" alt="4 questions">

[![Home](https://img.shields.io/badge/⌂_Home-22384A?style=flat-square)](../index.md) [![Notes](https://img.shields.io/badge/Notes-22384A?style=flat-square)](../01-notes/06-frequent-pattern-mining.md) [![All Exercises](https://img.shields.io/badge/All_Exercises-22384A?style=flat-square)](README.md) [![Quiz](https://img.shields.io/badge/▶_Quiz-1E9E75?style=flat-square&labelColor=167A5A)](../03-quiz/index.html)

</div>

> [!TIP]
> **Practice —** try each question first, then expand the answer to check your reasoning. This case study mines the **Epub** dataset (R's `arules` package): 15,729 sessions, 936 unique documents, each transaction being the set of documents downloaded in one session.

---

### &#128202; Q1. Mining at support thresholds 0.001, 0.005, and 0.01 produced 561, 67, and 19 frequent itemsets respectively. Why does raising the support threshold shrink the itemset count so quickly?

<details>
<summary><strong>Show answer</strong></summary>

Support = (transactions containing the itemset) / (total transactions). With 15,729 sessions and 936 documents, most document combinations are downloaded together only a handful of times — the dataset is **sparse**. Raising the minimum support threshold prunes out every itemset that doesn't clear that bar, and because popularity is so skewed (a few documents dominate, most are rare), even a small threshold increase eliminates the long tail of rare combinations. This matches the anti-monotone (downward-closure) property: if an itemset doesn't meet minimum support, none of its supersets can either.
</details>

---

### &#128279; Q2. Mining association rules at (support, confidence) = (0.001, 0.3), (0.001, 0.5), (0.001, 0.7), and at support 0.005 or 0.01 for any confidence, produced 30, 13, 4, 0, and 0 rules. What does this tell you about the relationship between confidence and rule count, and between support and rule count?

<details>
<summary><strong>Show answer</strong></summary>

- **Confidence vs. rule count** (support fixed at 0.001): 30 → 13 → 4 as confidence rises 0.3 → 0.5 → 0.7. Higher confidence is a stricter requirement (rule must hold true more often), so fewer rules survive — but the ones that do are more reliable.
- **Support vs. rule count**: at support 0.005 or 0.01, **zero** rules survive at any confidence. Association rule mining requires the underlying itemset to already be frequent enough to generate a rule from; since so few itemsets clear 0.005+ support (only 67 and 19 respectively, from Q1), there's little left to build multi-item rules from.

Together this shows a classic tradeoff: low support + low confidence = many rules (including noise); higher thresholds trade quantity for reliability, but too high a threshold here loses everything.
</details>

---

### &#128200; Q3. The strongest rules found were {doc_6e7, doc_6e8} → {doc_6e9} (confidence 0.81, lift 454.75), {doc_6e7, doc_6e9} → {doc_6e8} (confidence 0.85, lift 417.80), and {doc_6e8, doc_6e9} → {doc_6e7} (confidence 0.89, lift 402.09). Why does a lift over 400 matter more here than the confidence values?

<details>
<summary><strong>Show answer</strong></summary>

**Lift** = confidence / P(consequent) = how much more likely the consequent is *given* the antecedent, compared to its baseline popularity. A lift of ~400+ means these three documents co-occur **hundreds of times more often** than random chance would predict — an extremely strong, almost certainly non-coincidental relationship (e.g., a multi-part document or a tightly bundled reading set). Confidence alone (0.81–0.89) sounds good but doesn't rule out the possibility that the consequent is just a generally popular document; lift is what confirms the relationship is specific to that antecedent, not just general popularity.
</details>

---

### &#128161; Q4. In R, how would you generate frequent itemsets across three support thresholds and association rules across three support/confidence combinations, then find the top rules by lift?

<details>
<summary><strong>Show answer</strong></summary>

```r
library(arules)
data("Epub")

support_values <- c(0.001, 0.005, 0.01)
for (supp in support_values) {
  itemsets <- apriori(Epub, parameter = list(supp = supp, target = "frequent itemsets"))
  print(paste("Support:", supp, "-> itemsets:", length(itemsets)))
}

confidence_values <- c(0.3, 0.5, 0.7)
all_rules <- list()
for (supp in support_values) {
  for (conf in confidence_values) {
    rules <- apriori(Epub, parameter = list(supp = supp, conf = conf, minlen = 2))
    all_rules[[paste0("supp_", supp, "_conf_", conf)]] <- rules
  }
}

best <- all_rules[["supp_0.001_conf_0.3"]]
inspect(head(sort(best, by = "lift"), 10))
```

`apriori()` does the itemset search using the anti-monotone property to prune early; `sort(..., by = "lift")` re-ranks the resulting rules so the strongest relationships surface first, regardless of how they compare on raw confidence.
</details>

---

[📚 All Exercises](README.md)  ·  **Next:** [Chapter 07 — Classification](07-exercise.md) ➡️

<div align="center" markdown>

[All Exercises](README.md) &nbsp;|&nbsp; [Chapter 06 Notes](../01-notes/06-frequent-pattern-mining.md) &nbsp;|&nbsp; <strong>Next:</strong> [07: Classification — Exercise](07-exercise.md)

</div>
