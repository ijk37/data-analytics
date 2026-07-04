// ── Chapter 01 — Data & Attribute Types ─────────────────────────────────────
QUESTIONS["01"] = [
  {
    q: "Which measurement scale applies to ZIP codes?",
    options: ["Nominal", "Ordinal", "Interval", "Ratio"],
    answer: 0,
    explain: "ZIP codes are just labels with no meaningful order, difference, or ratio between them — a classic nominal attribute (only = and != are valid operations).",
  },
  {
    q: "University letter grades (A, B, C, D, F) are an example of which scale?",
    options: ["Nominal", "Ordinal", "Interval", "Ratio"],
    answer: 1,
    explain: "Grades have a clear order but the 'distance' between grades isn't a defined numeric quantity, so they're ordinal, not interval or ratio.",
  },
  {
    q: "Temperature measured in Celsius is an example of which scale, and why?",
    options: [
      "Ratio — it has a true zero",
      "Interval — differences are meaningful but there's no true zero",
      "Ordinal — only the order matters",
      "Nominal — it's just a label",
    ],
    answer: 1,
    explain: "0°C doesn't mean 'no temperature' (it's just the freezing point of water), so ratios like '20°C is twice as hot as 10°C' are meaningless — but differences (20°C - 10°C = 10°C) are meaningful. That makes it interval, not ratio.",
  },
  {
    q: "Which of these is a ratio-scale attribute?",
    options: ["Eye color", "Class rank", "Temperature in Celsius", "Weight in kilograms"],
    answer: 3,
    explain: "Weight has a true zero (0 kg = no mass) and ratios are meaningful (20kg is twice 10kg) — the defining property of a ratio scale.",
  },
  {
    q: "Which location statistic is valid on ALL four measurement scales (nominal, ordinal, interval, ratio)?",
    options: ["Mean", "Median", "Mode", "Standard deviation"],
    answer: 2,
    explain: "Mode (the most frequent value) only requires counting matches, which works even on nominal data. Median needs order (ordinal+), and mean/std dev need meaningful arithmetic (interval+).",
  },
  {
    q: "A dataset of 14-friend records with Age, Weight, Gender columns is best described as which data structure?",
    options: ["Transaction data", "Graph data", "Record / data matrix", "Ordered data"],
    answer: 2,
    explain: "Fixed columns per row with (mostly) numeric attributes is the classic record / data-matrix structure — each row is a point in n-dimensional space.",
  },
  {
    q: "A shopping basket dataset, where each row lists a variable-length set of purchased items, is best described as which data structure?",
    options: ["Transaction data", "Data matrix", "Document data", "Graph data"],
    answer: 0,
    explain: "Transaction data has no fixed schema — each record is just a set of items, which is exactly the shopping-basket case (and the basis for association rule mining in Ch06).",
  },
  {
    q: "A social network dataset of users and their friendships is best described as which data structure?",
    options: ["Ordered data", "Graph data", "Record data", "Transaction data"],
    answer: 1,
    explain: "Objects (users) become nodes and relationships (friendships) become edges — the definition of graph data.",
  },
  {
    q: "Which type of analytics answers the question 'What will happen?'",
    options: ["Descriptive", "Diagnostic", "Predictive", "Prescriptive"],
    answer: 2,
    explain: "Predictive analytics builds a model (a generalization learned from data) that forecasts future or unseen outcomes. Descriptive = what happened, diagnostic = why, prescriptive = what should we do.",
  },
  {
    q: "In the KDD process, which mining functions map to 'Descriptive' analytics?",
    options: [
      "Classification and Regression",
      "Summarization and Clustering",
      "Regression only",
      "Prediction and Optimization",
    ],
    answer: 1,
    explain: "Summarization and clustering describe existing structure in the data (descriptive), while classification and regression predict outcomes for new data (predictive).",
  },
  {
    q: "How many phases does the CRISP-DM methodology have?",
    options: ["4", "5", "6", "9"],
    answer: 2,
    explain: "CRISP-DM has 6 phases: Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, and Deployment — and the cycle can loop back.",
  },
  {
    q: "Which of the following can be treated as a lower scale, but NOT the reverse?",
    options: [
      "A ratio attribute can be treated as ordinal, but an ordinal attribute cannot become ratio",
      "A nominal attribute can be treated as ratio",
      "An ordinal attribute can always compute a meaningful mean",
      "All four scales are interchangeable",
    ],
    answer: 0,
    explain: "You can always drop information (treat a ratio-scale weight as 'high/medium/low' ordinal categories), but you can't invent information that isn't there (turn nominal colors into a ratio scale).",
  },
  {
    q: "A model in predictive analytics is best described as...",
    options: [
      "A raw, uncleaned dataset",
      "A generalization learned from data that can predict outcomes for new, unseen instances",
      "A chart summarizing historical data only",
      "A database index",
    ],
    answer: 1,
    explain: "The model is the reusable, generalized function learned from training data — its value is that it extends to instances it has never seen before.",
  },
  {
    q: "Is a person's number of children discrete or continuous, and why?",
    options: [
      "Continuous — it can be any real number",
      "Discrete — it's a countable, integer value",
      "Neither — it's nominal",
      "Both, depending on the country",
    ],
    answer: 1,
    explain: "Discrete attributes take countable values (like whole-number counts); continuous attributes are real-valued and measured (like height or temperature).",
  },
  {
    q: "Which pair correctly matches an attribute to its Stevens' scale?",
    options: [
      "Class rank (1st, 2nd, 3rd) → Interval",
      "Calendar year (e.g., 2024) → Ratio",
      "Height in centimeters → Ratio",
      "Gender (Male/Female) → Ordinal",
    ],
    answer: 2,
    explain: "Height has a true zero and meaningful ratios, so it's ratio. Class rank is ordinal (order only, no equal intervals). Calendar year is interval (no true 'zero time'). Gender is nominal (no order).",
  },
];
