// ── Chapter 03 — Descriptive Multivariate Analysis ──────────────────────────
QUESTIONS["03"] = [
  {
    q: "What distinguishes multivariate analysis from bivariate analysis?",
    options: [
      "Multivariate only works on nominal data",
      "Multivariate considers three or more attributes simultaneously",
      "Multivariate never uses visualization",
      "There is no real difference",
    ],
    answer: 1,
    explain: "Univariate = one attribute, bivariate = two, multivariate = three or more — but the underlying goals (location, spread, relationships) stay the same, just extended to every attribute pair at once.",
  },
  {
    q: "In a joint frequency table for Gender × Company (Bad/Good), what does each cell represent?",
    options: [
      "The count of one attribute alone, ignoring the other",
      "How often a specific combination of the two attribute values occurs together",
      "The correlation coefficient between the two attributes",
      "The mean of a third numeric attribute",
    ],
    answer: 1,
    explain: "A joint frequency table cross-tabulates two (or more) qualitative attributes, with each cell showing how often that exact combination appears — e.g., how many rows are Female AND Bad.",
  },
  {
    q: "In a bubble chart encoding 4 attributes, what does bubble SIZE typically represent?",
    options: ["The x-axis attribute", "The y-axis attribute", "A third quantitative attribute", "Nothing — size is only decorative"],
    answer: 2,
    explain: "A bubble chart maps 2 attributes to x/y position, a 3rd to bubble size, and often a 4th to bubble color — packing 4 dimensions into one 2D plot.",
  },
  {
    q: "What is a key limitation of parallel coordinates plots?",
    options: [
      "They cannot show more than 2 attributes",
      "The order of the axes matters — only adjacent axes visually 'connect'",
      "They require all attributes to be nominal",
      "They cannot be colored by class",
    ],
    answer: 1,
    explain: "Each object is a polyline crossing every axis in sequence, so relationships between adjacent axes are easy to see, but relationships between non-adjacent axes are much harder to spot — axis ORDER matters.",
  },
  {
    q: "In a star (radar) plot, what does the length of each spoke represent?",
    options: [
      "The object's ID number",
      "The (normalized) value of that attribute for the object",
      "The correlation with other objects",
      "Always a fixed length regardless of value",
    ],
    answer: 1,
    explain: "Each spoke radiates from the center at an equal angle, and its length is proportional to that attribute's (normalized) value — connecting the tips forms a unique polygon 'profile' per object.",
  },
  {
    q: "What is the main idea behind Chernoff faces?",
    options: [
      "Map each attribute to a facial feature, since humans are very sensitive to subtle face differences",
      "Draw a literal photograph of each object",
      "Only works for exactly 2 attributes",
      "Replace the need for any numeric data",
    ],
    answer: 0,
    explain: "Each attribute controls a facial feature (eye size, mouth curve, etc.); because people are so good at distinguishing faces, subtle multivariate patterns can become visually obvious — at the cost of the feature-to-attribute mapping being somewhat arbitrary.",
  },
  {
    q: "In a heatmap with dendrograms, why are rows and columns reordered?",
    options: [
      "To alphabetize the labels",
      "So hierarchical clustering groups similar objects and similar attributes next to each other",
      "It's purely cosmetic and has no analytical purpose",
      "To hide outliers",
    ],
    answer: 1,
    explain: "Reordering by the dendrogram's clustering puts similar rows (objects) and similar columns (attributes) adjacent to each other, making blocks of similar color jump out — revealing cluster structure at a glance.",
  },
  {
    q: "A scatter plot matrix (SPLOM) for p quantitative attributes shows...",
    options: [
      "One single scatter plot for the whole dataset",
      "A p × p grid of scatter plots, one for every attribute pair, often with the diagonal showing per-attribute summaries",
      "Only the two most correlated attributes",
      "A 3D rotating plot",
    ],
    answer: 1,
    explain: "Every off-diagonal cell (i,j) plots attribute i vs attribute j; the diagonal typically shows a histogram or density for that single attribute — giving a complete pairwise view in one grid.",
  },
  {
    q: "What is the covariance matrix's diagonal made up of?",
    options: ["Zeros", "Ones", "The variance of each attribute", "The mean of each attribute"],
    answer: 2,
    explain: "S[i][i] = cov(Xi, Xi), which reduces exactly to the sample variance of attribute i — so the diagonal is always the per-attribute variances.",
  },
  {
    q: "What is always true of the Pearson correlation matrix's diagonal?",
    options: ["It's always 0", "It's always 1.00 (every attribute is perfectly correlated with itself)", "It varies by dataset", "It equals the covariance"],
    answer: 1,
    explain: "R[i][i] = cov(Xi,Xi) / sqrt(S[i][i] * S[i][i]) = S[i][i]/S[i][i] = 1 — any attribute correlates perfectly with itself.",
  },
  {
    q: "If the Friends dataset shows Pearson r(Weight, Height) = 0.94, how should that be interpreted?",
    options: [
      "Negligible relationship",
      "Weak relationship",
      "Very strong positive relationship — taller friends tend to be heavier",
      "A perfect causal relationship",
    ],
    answer: 2,
    explain: "Using the |r| interpretation guide, 0.90-1.00 is 'very strong' — but note correlation still isn't causation, it just describes the strength/direction of the linear association.",
  },
  {
    q: "A correlogram is best described as...",
    options: [
      "A raw numeric correlation matrix with no visualization",
      "A visual (color- or shape-coded) version of the correlation matrix",
      "A type of scatter plot for only 2 variables",
      "A table of covariances only",
    ],
    answer: 1,
    explain: "A correlogram color-codes each cell of the correlation matrix (e.g., dark = high |r|, light = near zero), making the pattern of pairwise relationships visible at a glance instead of reading raw numbers.",
  },
  {
    q: "For which kind of attributes is a mosaic plot specifically designed?",
    options: [
      "Purely quantitative attributes",
      "Qualitative (categorical) attributes — typically up to 3",
      "Only continuous, normally-distributed data",
      "Time-series data",
    ],
    answer: 1,
    explain: "Mosaic plots draw tiles whose area is proportional to the joint frequency of category combinations — a visual version of a contingency table, and deviations from independence show up as unexpectedly large/small tiles.",
  },
  {
    q: "Which visualization technique can meaningfully encode the MOST attributes at once for a small number of objects?",
    options: ["A single scatter plot (2 attributes)", "A star/radar plot (many attributes per object)", "A bar chart (1 attribute)", "A box plot (1 attribute)"],
    answer: 1,
    explain: "Star plots use one spoke per attribute, so they scale to many attributes for a small set of objects — useful when you want to compare full multivariate 'profiles' rather than just one or two dimensions.",
  },
  {
    q: "In R, which function builds a scatter plot matrix annotated with Pearson correlations?",
    options: ["stars()", "parcoord()", "ggpairs() from the GGally package", "faces() from aplpack"],
    answer: 2,
    explain: "ggpairs() from GGally draws the full pairwise scatter plot matrix with correlation coefficients — parcoord() makes parallel coordinates, stars() makes star plots, and faces() draws Chernoff faces.",
  },
];
