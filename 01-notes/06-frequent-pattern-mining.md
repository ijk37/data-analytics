# Chapter 6: Frequent Pattern Mining

## 1. Core Concepts

### What is an Itemset?
- An **itemset** is a set of items (e.g., {milk, bread, butter})
- A **k-itemset** contains exactly k items
- **Transaction data**: each row = one transaction (a basket of items bought together)

### Support
| Form | Formula | Meaning |
|------|---------|---------|
| Absolute support | count(X in transactions) | Number of transactions containing X |
| Relative support | count(X) / n_transactions | Fraction of all transactions containing X |

### Frequent Itemset
- An itemset X is **frequent** if support(X) >= min_support threshold
- min_support is a user-defined parameter (e.g., 3 transactions, or 30%)

### Apriori Property (Anti-Monotone)
> If an itemset X is infrequent, then ALL supersets of X are also infrequent.

This is the key pruning principle:
- If {A, B} is infrequent, we do not need to check {A, B, C}, {A, B, D}, etc.
- Allows massive reduction in the search space

---

## 2. Association Rules

Format: **X -> Y** where X = antecedent, Y = consequent, X and Y share no items

### Formulas

```
Support(X -> Y)    = support(X union Y) / n_transactions
                   = P(X and Y)

Confidence(X -> Y) = support(X union Y) / support(X)
                   = P(Y | X)

Lift(X -> Y)       = Confidence(X -> Y) / Support(Y)
                   = P(Y | X) / P(Y)
```

### Interpreting Lift
| Lift Value | Meaning |
|------------|---------|
| Lift > 1 | Positive correlation: X and Y appear together more than by chance |
| Lift = 1 | Independent: knowing X gives no info about Y |
| Lift < 1 | Negative correlation: X and Y tend to avoid each other |

### Interesting Rules
A rule is considered interesting when it has:
- **High support** (appears frequently in the data)
- **High confidence** (Y is reliably predicted by X)

---

## 3. Apriori Algorithm

### Goal
Find all frequent itemsets and generate association rules from them.

### Algorithm Pseudocode

```
INPUT:  transaction database D, min_support
OUTPUT: all frequent itemsets

Step 1: Find all frequent 1-itemsets
  L1 = {items with support >= min_support}

Step 2: For k = 2, 3, 4, ... until no new frequent itemsets:
  a) Candidate Generation (Join):
     Ck = generate all k-itemsets from pairs of (k-1)-itemsets in L(k-1)
     (Two itemsets join if they share the first k-2 items)

  b) Candidate Pruning (Apriori Property):
     Remove from Ck any itemset whose (k-1)-subsets are NOT all in L(k-1)

  c) Support Counting:
     Scan D once, count support of each candidate in Ck

  d) Filter:
     Lk = {c in Ck | support(c) >= min_support}

Step 3: Return union of all Lk

RULE GENERATION:
For each frequent itemset F:
  Try all bipartitions X -> (F minus X), X not empty, X not equal to F
  Keep rules with confidence >= min_confidence
```

### Worked Example (Cuisine Dataset, min_support = 3)

**Transactions:**
```
Andrew:   {Indian, Mediterranean}
Bernhard: {Indian, Oriental, FastFood}
Carolina: {Indian, Mediterranean, Oriental}
Dennis:   {Arabic, Mediterranean}
Eve:      {Oriental}
Fred:     {Indian, Mediterranean, Oriental}
Gwyneth:  {Arabic, Mediterranean}
Hayden:   {Indian, Oriental, FastFood}
Irene:    {Indian, Mediterranean, Oriental}
James:    {Arabic, Mediterranean}
```

**Step 1 - Frequent 1-itemsets (support >= 3):**
| Item | Count |
|------|-------|
| Indian | 6 |
| Mediterranean | 7 |
| Oriental | 6 |
| Arabic | 3 |
| FastFood | 2 |

FastFood (count=2) is infrequent -> dropped.

**Step 2 - Candidate 2-itemsets from frequent items:**
All pairs of {Indian, Mediterranean, Oriental, Arabic}

**Support counts for C2:**
| Itemset | Count |
|---------|-------|
| {Indian, Mediterranean} | 4 |
| {Indian, Oriental} | 5 |
| {Indian, Arabic} | 0 |
| {Mediterranean, Oriental} | 3 |
| {Mediterranean, Arabic} | 3 |
| {Oriental, Arabic} | 0 |

Frequent 2-itemsets (count >= 3): drop {Indian, Arabic} and {Oriental, Arabic}

**Step 3 - Candidate 3-itemsets:**
{Indian, Mediterranean, Oriental} - check all 2-subsets are in L2:
  {Indian, Mediterranean} -> YES
  {Indian, Oriental} -> YES
  {Mediterranean, Oriental} -> YES
Count: Carolina, Fred, Irene = 3 -> Frequent!

{Indian, Mediterranean, Arabic}: {Indian, Arabic} is infrequent -> PRUNED

Final frequent 3-itemsets: {{Indian, Mediterranean, Oriental}} with support 3

---

## 4. FP-Growth Algorithm

### Why FP-Growth?
- Apriori requires multiple database scans (once per level)
- FP-Growth compresses the database into an FP-tree and mines it without regenerating candidates

### FP-Tree Structure
- A prefix tree (trie) where each path represents a set of transactions
- Each node stores: item name, count, parent pointer, children, node link (to next node with same item)
- **Header table**: list of frequent items with their total support, sorted by support descending
- Each entry in header table has a pointer to the first node for that item in the tree

### Building the FP-Tree

```
Step 1: Scan database once -> find frequent 1-items, sort by support descending
Step 2: Scan database again:
  For each transaction:
    - Keep only frequent items, sort by header table order
    - Insert the sorted transaction into the tree:
      * Follow existing path as far as possible (increment counts)
      * Create new nodes for the remaining items
```

### Mining the FP-Tree (Recursive)

```
For each item i in header table (bottom to top):
  1. Find all paths from root to nodes labeled i (conditional pattern bases)
  2. Each prefix path has the count of the leaf node i
  3. Build a "conditional FP-tree" from these prefix paths
  4. If conditional FP-tree is non-empty: recurse
  5. All combinations of prefix items with i are frequent itemsets
```

### FP-Tree vs Apriori Comparison
| Aspect | Apriori | FP-Growth |
|--------|---------|-----------|
| Database scans | 2 per level (many) | 2 total |
| Candidate generation | Explicit (can be large) | None |
| Memory | Candidate sets | Compact tree |
| Speed | Slower for large data | Faster |
| Implementation | Simpler | More complex |

---

## 5. Maximal and Closed Itemsets

### Definitions

**Closed Frequent Itemset:**
> A frequent itemset X is closed if no superset of X has the same support as X.
> Adding any item to X would strictly decrease its support.

**Maximal Frequent Itemset:**
> A frequent itemset X is maximal if no superset of X is frequent.
> X is at the boundary of the frequent/infrequent space.

### Relationship
```
Maximal frequent itemsets  is a subset of  Closed frequent itemsets  is a subset of  All frequent itemsets
```

### Why Reduce?
- All frequent itemsets can be derived from the maximal/closed set
- Much smaller representation -> more efficient storage and mining

---

## 6. Key Formulas Summary

| Measure | Formula |
|---------|---------|
| Support(X) | count(X) / n |
| Confidence(X->Y) | Support(X union Y) / Support(X) |
| Lift(X->Y) | Confidence(X->Y) / Support(Y) |
| Frequent | Support(X) >= min_support |

---

## 7. Friends Cuisine Dataset Reference

```
TID       Items
Andrew    Indian, Mediterranean
Bernhard  Indian, Oriental, FastFood
Carolina  Indian, Mediterranean, Oriental
Dennis    Arabic, Mediterranean
Eve       Oriental
Fred      Indian, Mediterranean, Oriental
Gwyneth   Arabic, Mediterranean
Hayden    Indian, Oriental, FastFood
Irene     Indian, Mediterranean, Oriental
James     Arabic, Mediterranean
```

Total transactions: 10

1-item support counts:
- Indian: 6 (60%)
- Mediterranean: 7 (70%)
- Oriental: 6 (60%)
- Arabic: 3 (30%)
- FastFood: 2 (20%) <- infrequent if min_support >= 3

---

## 8. Summary Table

| Concept | Definition | Key Property |
|---------|-----------|--------------|
| Support | How often itemset appears | >= min_sup -> frequent |
| Confidence | Reliability of rule X->Y | P(Y|X) |
| Lift | Correlation strength | >1 = positive correlation |
| Apriori pruning | Anti-monotone | Infrequent X -> all supersets infrequent |
| Maximal | No frequent superset | Boundary of frequent space |
| Closed | No equal-support superset | Lossless compression |
| FP-Growth | Compressed tree mining | Avoids multiple DB scans |
