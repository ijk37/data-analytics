# ============================================================
# PROJECT 06: Retail Sales Analytics  (R version)
# Chapters combined: Ch1 + Ch2 + Ch3 + Ch4 + Ch5 + Ch6 + Ch7
# Packages needed: arules, e1071, class
# Install with: install.packages(c("arules","e1071","class"))
# ============================================================

# --- UTILITY: suppress package startup messages ---
suppressMessages({
  library(arules)
  library(e1071)
  library(class)
})

cat("============================================================\n")
cat("PROJECT 06: Retail Sales Analytics\n")
cat("============================================================\n\n")

# ============================================================
# SECTION 1: DATASET
# ============================================================

# Build the data frame directly (no external file needed)
data <- data.frame(
  CustomerID    = paste0("C", sprintf("%02d", 1:30)),
  Age           = c(34,52,27,45,23,38,61,29,44,33,55,26,48,31,19,42,57,36,24,50,
                    39,63,28,46,32,58,25,43,37,54),
  Gender        = c("M","F","M","F","M","F","M","F","M","F","M","F","M","F","M",
                    "F","M","F","M","F","M","F","M","F","M","F","M","F","M","F"),
  Purchases     = c(12,3,20,8,2,15,5,18,9,11,4,22,7,16,1,10,6,13,3,8,
                    14,2,19,9,12,4,21,7,15,5),
  AvgSpend      = c(85,210,45,320,30,95,180,65,290,110,140,55,260,80,20,195,210,
                    75,40,300,90,250,50,275,100,220,60,185,85,240),
  Returns       = c(1,0,2,1,0,3,0,1,2,1,0,2,1,2,0,1,0,1,0,2,1,0,3,1,2,0,2,1,1,0),
  Months_Active = c(3,1,3,2,1,3,2,3,2,3,1,3,2,3,1,2,2,3,1,2,3,1,3,2,3,1,3,2,3,1),
  Category1     = c(1,0,0,1,0,0,1,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0),
  Category2     = c(0,1,0,1,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,0,1,1,0,0,0,1),
  Category3     = c(1,0,1,0,1,1,0,1,0,0,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0),
  Category4     = c(0,0,1,0,0,0,1,1,0,1,0,1,0,0,1,0,1,1,0,0,0,1,1,0,0,0,0,1,1,0),
  Churned       = c("No","Yes","No","No","Yes","No","No","No","Yes","No","Yes","No",
                    "No","No","Yes","No","Yes","No","Yes","No","No","Yes","No","No",
                    "No","Yes","No","No","No","Yes"),
  stringsAsFactors = FALSE
)

n_rows <- nrow(data)
cat("Dataset loaded:", n_rows, "customers,", ncol(data), "attributes\n\n")


# ============================================================
# --- PHASE 1 (Ch1+Ch2): Attribute Profiling and Descriptive Stats ---
# ============================================================

cat("==========================================================\n")
cat("  PHASE 1 (Ch1+Ch2): Attribute Profiling & Descriptive Stats\n")
cat("==========================================================\n\n")

cat("--- Attribute Type Table ---\n")
attr_info <- data.frame(
  Attribute = c("CustomerID","Age","Gender","Purchases","AvgSpend","Returns",
                "Months_Active","Category1","Category2","Category3","Category4","Churned"),
  Scale     = c("Nominal","Ratio","Nominal","Ratio","Ratio","Ratio","Ratio",
                "Nominal","Nominal","Nominal","Nominal","Nominal"),
  Type      = c("Categorical","Continuous","Binary","Discrete","Continuous","Discrete",
                "Discrete","Binary","Binary","Binary","Binary","Binary"),
  stringsAsFactors = FALSE
)
print(attr_info, row.names = FALSE)

cat("\n--- Class Distribution ---\n")
churn_table <- table(data$Churned)
print(churn_table)
cat("Churned=Yes:", churn_table["Yes"], "(", round(100*churn_table["Yes"]/n_rows,1), "%)\n")
cat("Churned=No :", churn_table["No"],  "(", round(100*churn_table["No"] /n_rows,1), "%)\n")

cat("\n--- Per-Churn-Group Means (tapply) ---\n")
numeric_feats <- c("Age","Purchases","AvgSpend","Returns","Months_Active")
for (feat in numeric_feats) {
  means <- tapply(data[[feat]], data$Churned, mean)
  diff  <- abs(means["Yes"] - means["No"])
  cat(sprintf("  %-16s  Churned=Yes: %6.2f  Churned=No: %6.2f  |Diff|: %6.2f\n",
              feat, means["Yes"], means["No"], diff))
}

cat("\n--- Aggregate Summary ---\n")
agg <- aggregate(cbind(Age, Purchases, AvgSpend, Returns, Months_Active) ~ Churned,
                 data = data, FUN = mean)
print(agg)


# ============================================================
# --- PHASE 2 (Ch3): Multivariate Analysis ---
# ============================================================

cat("\n==========================================================\n")
cat("  PHASE 2 (Ch3): Multivariate Analysis\n")
cat("==========================================================\n\n")

nums <- data[, numeric_feats]
corr_matrix <- cor(nums)

cat("--- Pearson Correlation Matrix ---\n")
print(round(corr_matrix, 3))

# Find strongest positive and negative off-diagonal correlations
best_pos_r   <- -Inf
best_neg_r   <- Inf
best_pos_pair <- c("","")
best_neg_pair <- c("","")

for (i in 1:(length(numeric_feats)-1)) {
  for (j in (i+1):length(numeric_feats)) {
    r <- corr_matrix[i, j]
    if (r > best_pos_r) {
      best_pos_r    <- r
      best_pos_pair <- c(numeric_feats[i], numeric_feats[j])
    }
    if (r < best_neg_r) {
      best_neg_r    <- r
      best_neg_pair <- c(numeric_feats[i], numeric_feats[j])
    }
  }
}

cat(sprintf("\nStrongest POSITIVE correlation: %s vs %s  r=%.3f\n",
            best_pos_pair[1], best_pos_pair[2], best_pos_r))
cat(sprintf("Strongest NEGATIVE correlation: %s vs %s  r=%.3f\n",
            best_neg_pair[1], best_neg_pair[2], best_neg_r))


# ============================================================
# --- PHASE 3 (Ch4): Preprocessing ---
# ============================================================

cat("\n==========================================================\n")
cat("  PHASE 3 (Ch4): Preprocessing\n")
cat("==========================================================\n\n")

cat("--- Outlier Detection (IQR rule) ---\n")
detect_iqr_outliers <- function(col, label) {
  q1  <- quantile(col, 0.25)
  q3  <- quantile(col, 0.75)
  iqr <- q3 - q1
  lower <- q1 - 1.5 * iqr
  upper <- q3 + 1.5 * iqr
  outlier_idx <- which(col < lower | col > upper)
  cat(sprintf("  %s: Q1=%.2f  Q3=%.2f  IQR=%.2f  Fences=[%.2f, %.2f]\n",
              label, q1, q3, iqr, lower, upper))
  if (length(outlier_idx) > 0) {
    cat("    Outliers at rows:", outlier_idx, "  values:", col[outlier_idx], "\n")
  } else {
    cat("    No outliers detected.\n")
  }
}

detect_iqr_outliers(data$AvgSpend, "AvgSpend")
detect_iqr_outliers(data$Returns,  "Returns")

cat("\n--- Log Transform: log1p(AvgSpend) ---\n")
data$log_AvgSpend <- log1p(data$AvgSpend)
cat(sprintf("  Original AvgSpend: mean=%.2f  sd=%.2f\n", mean(data$AvgSpend), sd(data$AvgSpend)))
cat(sprintf("  Log-transformed:   mean=%.4f  sd=%.4f\n", mean(data$log_AvgSpend), sd(data$log_AvgSpend)))

cat("\n--- Min-Max Normalization ---\n")
minmax <- function(x) { (x - min(x)) / (max(x) - min(x)) }

data$norm_Age       <- minmax(data$Age)
data$norm_Purchases <- minmax(data$Purchases)
data$norm_logSpend  <- minmax(data$log_AvgSpend)
data$norm_Returns   <- minmax(data$Returns)
data$norm_Months    <- minmax(data$Months_Active)
data$GenderEnc      <- ifelse(data$Gender == "M", 1L, 0L)

cat("  Normalized: Age, Purchases, log(AvgSpend), Returns, Months_Active -> [0,1]\n")
cat("  Gender encoded: M=1, F=0\n")
cat("\n  First 3 rows after preprocessing:\n")
cols_to_show <- c("CustomerID","norm_Age","norm_Purchases","norm_logSpend",
                  "norm_Returns","norm_Months","GenderEnc","Churned")
print(data[1:3, cols_to_show])


# ============================================================
# --- PHASE 4 (Ch6): Pattern Mining on Category Combinations ---
# ============================================================

cat("\n==========================================================\n")
cat("  PHASE 4 (Ch6): Pattern Mining on Category Combinations\n")
cat("==========================================================\n\n")

cat("--- Building Transaction Matrix ---\n")
category_cols <- c("Category1","Category2","Category3","Category4")
cat_names      <- c("Electronics","Clothing","Food","Books")

# Build logical matrix for arules
trans_matrix <- as.matrix(data[, category_cols] == 1)
colnames(trans_matrix) <- cat_names

# Convert to transactions object
transactions_obj <- as(trans_matrix, "transactions")
cat("  Total transactions:", length(transactions_obj), "\n")

cat("\n  Category frequencies (Churned=Yes):\n")
yes_idx <- which(data$Churned == "Yes")
for (cn in cat_names) {
  cnt <- sum(data[yes_idx, category_cols[match(cn, cat_names)]])
  cat(sprintf("    %-14s: %d / %d\n", cn, cnt, length(yes_idx)))
}

cat("\n  Category frequencies (Churned=No):\n")
no_idx <- which(data$Churned == "No")
for (cn in cat_names) {
  cnt <- sum(data[no_idx, category_cols[match(cn, cat_names)]])
  cat(sprintf("    %-14s: %d / %d\n", cn, cnt, length(no_idx)))
}

cat("\n--- Apriori (min_support=3/30=0.10, min_confidence=0.5) ---\n")
# arules uses fractional support
rules_obj <- apriori(
  transactions_obj,
  parameter = list(support = 3/30, confidence = 0.5, minlen = 2),
  control   = list(verbose = FALSE)
)

if (length(rules_obj) > 0) {
  cat("  Found", length(rules_obj), "rules:\n")
  rules_df <- as(rules_obj, "data.frame")
  rules_df <- rules_df[order(-rules_df$confidence), ]
  print(rules_df)
} else {
  cat("  No rules at this support/confidence level. Showing frequent itemsets:\n")
  freq_sets <- apriori(
    transactions_obj,
    parameter = list(support = 3/30, target = "frequent itemsets", minlen = 2),
    control   = list(verbose = FALSE)
  )
  print(inspect(freq_sets))
}

cat("\n  Interpretation: Customers buying only one category are higher churn risk.\n")
cat("  Cross-sell promotions should target single-category buyers.\n")


# ============================================================
# --- PHASE 5 (Ch5): Customer Segmentation via K-Means ---
# ============================================================

cat("\n==========================================================\n")
cat("  PHASE 5 (Ch5): Customer Segmentation (K-Means, K=3)\n")
cat("==========================================================\n\n")

set.seed(42)
cluster_features <- data[, c("norm_Purchases", "norm_logSpend", "norm_Months")]
km_result <- kmeans(cluster_features, centers = 3, nstart = 20)

data$Cluster <- km_result$cluster
cat("--- Cluster Assignments ---\n")
print(table(Cluster = data$Cluster, Churned = data$Churned))

cat("\n--- Cluster Profiles (normalized scale) ---\n")
for (ki in 1:3) {
  member_rows <- data[data$Cluster == ki, ]
  pct_churned <- round(100 * mean(member_rows$Churned == "Yes"), 1)
  cat(sprintf("  Cluster %d  (n=%d, %.0f%% churned):\n", ki, nrow(member_rows), pct_churned))
  cat(sprintf("    mean norm_Purchases=%.3f  norm_logSpend=%.3f  norm_Months=%.3f\n",
              mean(member_rows$norm_Purchases),
              mean(member_rows$norm_logSpend),
              mean(member_rows$norm_Months)))
  cat(sprintf("    Customers: %s\n", paste(member_rows$CustomerID, collapse=", ")))
}

cat("\n--- Cluster Centers (normalized) ---\n")
print(round(km_result$centers, 3))

cat("\n  Label interpretation:\n")
cat("  - Cluster with high Purchases + low Spend = 'Frequent Low-Spenders'\n")
cat("  - Cluster with low Purchases + high Spend = 'Occasional High-Spenders'\n")
cat("  - Cluster with low Purchases + low Months  = 'Low-Engagement (At Risk)'\n")


# ============================================================
# --- PHASE 6 (Ch7): Churn Prediction ---
# ============================================================

cat("\n==========================================================\n")
cat("  PHASE 6 (Ch7): Churn Prediction\n")
cat("==========================================================\n\n")

# Prepare feature matrix and labels
feature_cols <- c("norm_Age","norm_Purchases","norm_logSpend","norm_Returns","norm_Months")
X <- data[, feature_cols]
y <- factor(data$Churned, levels = c("No","Yes"))

# Train/test split: first 22 train, last 8 test
split_idx <- 22
X_train <- X[1:split_idx, ]
y_train <- y[1:split_idx]
X_test  <- X[(split_idx+1):n_rows, ]
y_test  <- y[(split_idx+1):n_rows]
test_ids_r <- data$CustomerID[(split_idx+1):n_rows]

cat("  Train:", split_idx, "samples  |  Test:", n_rows - split_idx, "samples\n\n")

# ---- k-NN (k=3) ----
cat("--- k-NN (k=3) ---\n")
knn_preds <- knn(train = X_train, test = X_test, cl = y_train, k = 3)
knn_results <- data.frame(CustomerID=test_ids_r, True=as.character(y_test),
                          Predicted=as.character(knn_preds))
knn_results$Match <- ifelse(knn_results$True == knn_results$Predicted, "OK", "WRONG")
print(knn_results)

knn_cm <- table(True=y_test, Predicted=knn_preds)
cat("\n  Confusion Matrix (k-NN):\n")
print(knn_cm)
knn_tp <- knn_cm["Yes","Yes"]
knn_fp <- knn_cm["No","Yes"]
knn_fn <- knn_cm["Yes","No"]
knn_tn <- knn_cm["No","No"]
knn_acc  <- (knn_tp + knn_tn) / length(y_test)
knn_prec <- knn_tp / max(1, knn_tp + knn_fp)
knn_rec  <- knn_tp / max(1, knn_tp + knn_fn)
knn_f1   <- 2 * knn_prec * knn_rec / max(1e-9, knn_prec + knn_rec)
cat(sprintf("  Accuracy=%.3f  Precision=%.3f  Recall=%.3f  F1=%.3f\n",
            knn_acc, knn_prec, knn_rec, knn_f1))

# ---- Naive Bayes ----
cat("\n--- Naive Bayes (Gaussian) ---\n")
nb_model <- naiveBayes(x = X_train, y = y_train)
nb_preds <- predict(nb_model, X_test)
nb_results <- data.frame(CustomerID=test_ids_r, True=as.character(y_test),
                         Predicted=as.character(nb_preds))
nb_results$Match <- ifelse(nb_results$True == nb_results$Predicted, "OK", "WRONG")
print(nb_results)

nb_cm <- table(True=y_test, Predicted=nb_preds)
cat("\n  Confusion Matrix (Naive Bayes):\n")
print(nb_cm)
nb_tp <- nb_cm["Yes","Yes"]
nb_fp <- nb_cm["No","Yes"]
nb_fn <- nb_cm["Yes","No"]
nb_tn <- nb_cm["No","No"]
nb_acc  <- (nb_tp + nb_tn) / length(y_test)
nb_prec <- nb_tp / max(1, nb_tp + nb_fp)
nb_rec  <- nb_tp / max(1, nb_tp + nb_fn)
nb_f1   <- 2 * nb_prec * nb_rec / max(1e-9, nb_prec + nb_rec)
cat(sprintf("  Accuracy=%.3f  Precision=%.3f  Recall=%.3f  F1=%.3f\n",
            nb_acc, nb_prec, nb_rec, nb_f1))

# ---- Comparison ----
cat("\n--- Classifier Comparison ---\n")
comparison <- data.frame(
  Classifier = c("k-NN (k=3)", "Naive Bayes (Gaussian)"),
  Accuracy   = round(c(knn_acc,  nb_acc),  3),
  Precision  = round(c(knn_prec, nb_prec), 3),
  Recall     = round(c(knn_rec,  nb_rec),  3),
  F1         = round(c(knn_f1,   nb_f1),   3)
)
print(comparison, row.names = FALSE)

best_clf <- ifelse(knn_rec >= nb_rec, "k-NN (k=3)", "Naive Bayes (Gaussian)")
best_rec <- max(knn_rec, nb_rec)
cat(sprintf("\n  *** %s achieves higher recall (%.3f) for churners ***\n", best_clf, best_rec))
cat("  For churn prediction, RECALL is the priority metric.\n")
cat("  Missing a churner costs more than a false alarm.\n")

cat("\n--- Business Recommendation ---\n")
cat("  1. Deploy", best_clf, "for monthly churn scoring.\n")
cat("  2. Target retention campaigns on Low-Engagement cluster customers.\n")
cat("  3. Cross-sell single-category buyers to broaden purchase breadth.\n")
cat("  4. Monitor high-spenders who visited only once for re-engagement.\n")

cat("\n============================================================\n")
cat("  RETAIL ANALYTICS (R) COMPLETE\n")
cat("============================================================\n")
