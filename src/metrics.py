"""
Classification performance metrics implemented from scratch using NumPy.
"""

import numpy as np


def confusion_matrix_scratch(y_true, y_pred):
    """
    Compute confusion matrix to evaluate classification accuracy.
    Returns array [[TN, FP], [FN, TP]]
    """
    y_true_arr = np.asarray(y_true).astype(int)
    y_pred_arr = np.asarray(y_pred).astype(int)

    tp = np.sum((y_true_arr == 1) & (y_pred_arr == 1))
    tn = np.sum((y_true_arr == 0) & (y_pred_arr == 0))
    fp = np.sum((y_true_arr == 0) & (y_pred_arr == 1))
    fn = np.sum((y_true_arr == 1) & (y_pred_arr == 0))

    return np.array([[tn, fp], [fn, tp]])


def accuracy_score_scratch(y_true, y_pred):
    """Compute Accuracy metric."""
    y_true_arr = np.asarray(y_true).astype(int)
    y_pred_arr = np.asarray(y_pred).astype(int)
    return np.mean(y_true_arr == y_pred_arr)


def precision_score_scratch(y_true, y_pred):
    """Compute Precision metric: TP / (TP + FP)."""
    cm = confusion_matrix_scratch(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    return tp / (tp + fp) if (tp + fp) > 0 else 0.0


def recall_score_scratch(y_true, y_pred):
    """Compute Recall / Sensitivity metric: TP / (TP + FN)."""
    cm = confusion_matrix_scratch(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    return tp / (tp + fn) if (tp + fn) > 0 else 0.0


def f1_score_scratch(y_true, y_pred):
    """Compute F1-score metric: 2 * (Precision * Recall) / (Precision + Recall)."""
    prec = precision_score_scratch(y_true, y_pred)
    rec = recall_score_scratch(y_true, y_pred)
    return 2.0 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
