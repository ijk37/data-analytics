// ── Chapter 06 — Frequent Pattern Mining ─────────────────────────────────────
QUESTIONS["06"] = [
  {
    q: "What is a 'k-itemset' in frequent pattern mining?",
    options: ["A set of exactly k transactions", "A set containing exactly k items", "A rule with k conditions", "A cluster of k objects"],
    answer: 1,
    explain: "An itemset is just a set of items (e.g., {milk, bread}); a k-itemset specifically contains exactly k items.",
  },
  {
    q: "What does the Apriori (anti-monotone) property state?",
    options: [
      "If an itemset is frequent, all its subsets are infrequent",
      "If an itemset is infrequent, ALL of its supersets are also infrequent",
      "Every itemset is automatically frequent",
      "Support always increases as itemsets grow larger",
    ],
    answer: 1,
    explain: "This is the key pruning rule: since adding an item to a set can only keep or reduce its support (never increase it), once a set is below the support threshold, every superset built from it is guaranteed to be too — so it never needs to be checked.",
  },
  {
    q: "In the Friends Cuisine dataset (10 transactions), FastFood has count = 2. If min_support = 3, is FastFood frequent?",
    options: ["Yes, because 2 is a positive count", "No — its support (2/10 = 20%) is below the min_support threshold", "Frequency doesn't apply to single items", "Only if it appears with Indian"],
    answer: 1,
    explain: "min_support=3 means an itemset needs a count of at least 3 (or 30%) to be frequent. FastFood's count of 2 falls short, so it's dropped before any 2-itemsets are even considered.",
  },
  {
    q: "For the rule {bread} → {milk}, how is confidence computed?",
    options: [
      "support({bread}) / support({milk})",
      "support({bread} ∪ {milk}) / support({bread})",
      "support({milk}) / support({bread} ∪ {milk})",
      "support({bread}) × support({milk})",
    ],
    answer: 1,
    explain: "Confidence(X→Y) = support(X∪Y) / support(X) = P(Y|X) — of the transactions containing bread, what fraction also contain milk.",
  },
  {
    q: "A rule has confidence 0.8 and lift 1.0. What does a lift of exactly 1 mean?",
    options: [
      "X and Y are perfectly correlated",
      "X and Y are statistically independent — knowing X gives no extra information about Y",
      "The rule is invalid",
      "Y always causes X",
    ],
    answer: 1,
    explain: "Lift = confidence(X→Y) / support(Y). Lift = 1 means P(Y|X) = P(Y) exactly, i.e., X occurring doesn't change the probability of Y at all — no real association, despite whatever confidence value the rule shows.",
  },
  {
    q: "A rule has lift = 454.75. What does this extremely high lift indicate?",
    options: [
      "The rule is definitely a data error",
      "X and Y co-occur far more often than random chance would predict — an unusually strong relationship",
      "Lift greater than 100 is mathematically impossible",
      "The confidence must also be exactly 1.0",
    ],
    answer: 1,
    explain: "Lift measures how much more likely Y is given X, compared to Y's baseline frequency. A lift over 400 means the co-occurrence is hundreds of times more common than chance — a very strong signal (e.g., two parts of the same multi-part document).",
  },
  {
    q: "In the Apriori algorithm, how are candidate k-itemsets (Ck) generated?",
    options: [
      "Randomly from the full dataset",
      "By joining pairs of frequent (k-1)-itemsets that share their first k-2 items",
      "By listing every possible combination of all items, with no filtering",
      "By copying the (k-1)-itemsets exactly",
    ],
    answer: 1,
    explain: "The join step builds Ck from L(k-1) by combining itemsets that agree on their first k-2 items — then the anti-monotone property prunes any candidate whose (k-1)-subsets aren't all already frequent.",
  },
  {
    q: "What is the main reason FP-Growth is generally faster than Apriori on large datasets?",
    options: [
      "FP-Growth requires more database scans",
      "FP-Growth compresses the data into an FP-tree and mines it without generating explicit candidate itemsets",
      "FP-Growth only works on numeric data",
      "FP-Growth doesn't need a minimum support threshold",
    ],
    answer: 1,
    explain: "Apriori needs 2 scans per level and can generate huge candidate sets; FP-Growth builds a compact prefix-tree in just 2 total scans and mines it recursively via conditional pattern bases, avoiding candidate generation entirely.",
  },
  {
    q: "What is a MAXIMAL frequent itemset?",
    options: [
      "A frequent itemset where no superset has the SAME support",
      "A frequent itemset where NO superset is frequent at all",
      "The single largest itemset in the dataset regardless of support",
      "Any itemset with support = 1.0",
    ],
    answer: 1,
    explain: "Maximal frequent itemsets sit at the boundary between frequent and infrequent — none of their supersets clear the min_support bar. (A CLOSED itemset is the stricter one: no superset shares the exact same support.)",
  },
  {
    q: "What is the relationship between maximal, closed, and (all) frequent itemsets?",
    options: [
      "Maximal ⊂ Closed ⊂ Frequent (maximal is the smallest, most compressed set)",
      "Frequent ⊂ Closed ⊂ Maximal",
      "They are always equal in size",
      "There is no relationship between them",
    ],
    answer: 0,
    explain: "Maximal itemsets are a subset of closed itemsets, which are a subset of all frequent itemsets — all frequent itemsets can be derived from the maximal/closed sets, which are much more compact to store.",
  },
  {
    q: "In the header table of an FP-tree, items are typically sorted by...",
    options: ["Alphabetical order", "Support (frequency), descending", "Random order", "Transaction ID"],
    answer: 1,
    explain: "Sorting frequent items by descending support before inserting each transaction maximizes path sharing in the tree (common frequent items end up near the root, shared across many transactions), keeping the tree compact.",
  },
  {
    q: "In the Epub dataset case study, raising the support threshold from 0.001 to 0.01 caused the itemset count to drop from 561 to 19. Why?",
    options: [
      "The dataset changed between runs",
      "The data is sparse — most itemsets are rare, so a higher support threshold prunes almost all of them via the anti-monotone property",
      "Higher support thresholds always find MORE itemsets",
      "It indicates a bug in the algorithm",
    ],
    answer: 1,
    explain: "With 15,729 sessions and 936 documents, most document combinations occur only rarely. Raising the minimum support bar prunes the long tail of rare combinations rapidly, leaving only the handful of itemsets that are genuinely common.",
  },
  {
    q: "A rule X → Y is generally considered 'interesting' when it has...",
    options: [
      "Low support and low confidence",
      "High support (appears often) AND high confidence (Y reliably follows X)",
      "Any support, regardless of confidence",
      "Confidence exactly equal to 0",
    ],
    answer: 1,
    explain: "A rule needs to be both common enough to matter (support) and reliable enough to trust (confidence) — lift then further filters for rules that reflect a genuine relationship rather than just Y's general popularity.",
  },
  {
    q: "For the Friends Cuisine dataset, {Indian, Mediterranean, Oriental} was found frequent (support=3) at min_support=3, while {Indian, Mediterranean, Arabic} was pruned. Why was the second one pruned without even counting it?",
    options: [
      "Because Arabic never appears in the dataset",
      "Because one of its 2-item subsets, {Indian, Arabic}, was already found infrequent (count=0)",
      "Because 3-itemsets are never allowed",
      "Because Mediterranean is infrequent",
    ],
    answer: 1,
    explain: "The Apriori candidate-pruning step rejects any candidate k-itemset if any of its (k-1)-subsets isn't already in the frequent set. Since {Indian, Arabic} had support 0 (never frequent), {Indian, Mediterranean, Arabic} is pruned immediately — no database scan needed.",
  },
];
