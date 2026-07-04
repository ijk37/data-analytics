# Project 07-03-03: Model Evaluation

## Overview

This project focuses on evaluating classification models rigorously using:
- **Confusion Matrix**: layout and interpretation of TP, TN, FP, FN
- **Evaluation Metrics**: accuracy, precision, recall, F1 score
- **k-Fold Cross-Validation**: splitting data into folds and rotating the test set

## Concepts Covered

- Confusion matrix construction from predicted vs actual labels
- Per-class precision and recall
- Macro-averaged F1 score
- k-fold cross-validation procedure step-by-step
- Majority-class baseline classifier
- ROC curve (R only, using pROC if available)

## Files

| File | Description |
|------|-------------|
| `model_evaluation.py` | Python implementation (pure stdlib) |
| `model_evaluation.R` | R implementation using caret and rpart |

## Formulas

```
Accuracy    = (TP + TN) / total
Precision   = TP / (TP + FP)
Recall      = TP / (TP + FN)
F1          = 2 * Precision * Recall / (Precision + Recall)
```

## How to Run

### Python
```bash
python model_evaluation.py
```

Requirements: Python 3.6+ with standard library only (no external packages).

### R
```r
source("model_evaluation.R")
```

Required packages: `caret`, `rpart`  
Optional: `pROC` for ROC curves  
Install with: `install.packages(c("caret", "rpart", "pROC"))`

## Expected Output

- ASCII confusion matrix with row/column headers
- Classification report with precision, recall, F1 per class
- 5-fold cross-validation step-by-step: which examples are in train vs test each fold
- Mean and per-fold accuracy
- R: caret confusionMatrix output, 5-fold CV with rpart on Iris dataset
