"""
Classification performance metrics implemented from scratch using NumPy.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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


def roc_curve_scratch(y_true, y_probs, n_thresholds=100):
    """
    Compute ROC curve True Positive Rate (TPR) and False Positive Rate (FPR) across thresholds.
    """
    thresholds = np.linspace(0.0, 1.0, n_thresholds)
    tprs = []
    fprs = []

    for t in thresholds:
        preds = (y_probs >= t).astype(int)
        cm = confusion_matrix_scratch(y_true, preds)
        tn, fp, fn, tp = cm.ravel()

        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

        tprs.append(tpr)
        fprs.append(fpr)

    # Sort by FPR
    sorted_indices = np.argsort(fprs)
    fprs = np.array(fprs)[sorted_indices]
    tprs = np.array(tprs)[sorted_indices]

    # Trapezoidal rule for AUC calculation
    if hasattr(np, 'trapezoid'):
        auc = np.trapezoid(tprs, fprs)
    else:
        auc = float(np.sum((fprs[1:] - fprs[:-1]) * (tprs[1:] + tprs[:-1]) / 2.0))
    return fprs, tprs, abs(auc)


def evaluate_model_pipeline(data_path="data/processed/dataset.npz", output_dir="results"):
    """Evaluate trained Logistic Regression model and save confusion matrix, ROC curve, and metrics table."""
    from src.logistic_regression_scratch import LogisticRegressionScratch

    data = np.load(data_path)
    X_train_scaled = data["X_train_scaled"]
    X_test_scaled = data["X_test_scaled"]
    y_train = data["y_train"]
    y_test = data["y_test"]

    model = LogisticRegressionScratch(learning_rate=0.1, l2_lambda=0.1, n_iterations=1000)
    model.fit(X_train_scaled, y_train)

    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    y_probs_test = model.predict_proba(X_test_scaled)

    acc_train = accuracy_score_scratch(y_train, y_pred_train)
    acc_test = accuracy_score_scratch(y_test, y_pred_test)
    prec_test = precision_score_scratch(y_test, y_pred_test)
    rec_test = recall_score_scratch(y_test, y_pred_test)
    f1_test = f1_score_scratch(y_test, y_pred_test)

    fprs, tprs, roc_auc = roc_curve_scratch(y_test, y_probs_test)

    # Save metrics table
    metrics_df = pd.DataFrame([{
        "Metric": "Accuracy (Train)", "Value": f"{acc_train:.4f}"
    }, {
        "Metric": "Accuracy (Test)", "Value": f"{acc_test:.4f}"
    }, {
        "Metric": "Precision (Test)", "Value": f"{prec_test:.4f}"
    }, {
        "Metric": "Recall (Test)", "Value": f"{rec_test:.4f}"
    }, {
        "Metric": "F1-Score (Test)", "Value": f"{f1_test:.4f}"
    }, {
        "Metric": "ROC-AUC (Test)", "Value": f"{roc_auc:.4f}"
    }])

    metrics_dir = os.path.join(output_dir, "metrics")
    figures_dir = os.path.join(output_dir, "figures")
    os.makedirs(metrics_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    metrics_df.to_csv(os.path.join(metrics_dir, "evaluation_metrics.csv"), index=False)

    # Save Confusion Matrix plot
    cm = confusion_matrix_scratch(y_test, y_pred_test)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Non-réussite (0)", "Réussite (1)"],
                yticklabels=["Non-réussite (0)", "Réussite (1)"])
    plt.xlabel("Classe Prédite")
    plt.ylabel("Classe Réelle")
    plt.title("Matrice de Confusion (Données de Test)")
    plt.savefig(os.path.join(figures_dir, "confusion_matrix.png"), bbox_inches="tight")
    plt.close()

    # Save ROC Curve plot
    plt.figure(figsize=(7, 5))
    plt.plot(fprs, tprs, color="darkorange", lw=2, label=f"Courbe ROC (AUC = {roc_auc:.3f})")
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--", label="Aléatoire (AUC = 0.500)")
    plt.xlabel("Taux de Faux Positifs (FPR)")
    plt.ylabel("Taux de Vrais Positifs (TPR / Rappel)")
    plt.title("Courbe ROC — Régression Logistique From Scratch")
    plt.legend(loc="lower right")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.savefig(os.path.join(figures_dir, "roc_curve.png"), bbox_inches="tight")
    plt.close()

    print(f"Evaluation finished: Accuracy Test = {acc_test:.2%}, F1 Test = {f1_test:.2%}, ROC-AUC = {roc_auc:.3f}")
    return metrics_df


if __name__ == "__main__":
    evaluate_model_pipeline()
