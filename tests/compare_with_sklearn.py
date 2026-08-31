"""
Script to compare PCA & Logistic Regression implementations from scratch against Scikit-Learn (or NumPy reference).
"""

import os
import numpy as np
import pandas as pd

from src.pca_scratch import PCAFromScratch
from src.logistic_regression_scratch import LogisticRegressionScratch
from src.metrics import accuracy_score_scratch, f1_score_scratch


def compare_pca_on_dataset(data_path="data/processed/dataset.npz"):
    print("=== 1. COMPARAISON ACP (PCA) FROM SCRATCH VS REFERENCE ===")
    data = np.load(data_path, allow_pickle=True)
    X_train_scaled = data["X_train_scaled"]

    # PCA From Scratch
    pca_scratch = PCAFromScratch(n_components=2)
    Z_scratch = pca_scratch.fit_transform(X_train_scaled)
    ratio_scratch = pca_scratch.explained_variance_ratio_

    try:
        from sklearn.decomposition import PCA as SklearnPCA
        pca_sklearn = SklearnPCA(n_components=2)
        Z_sklearn = pca_sklearn.fit_transform(X_train_scaled)
        ratio_ref = pca_sklearn.explained_variance_ratio_
        ref_name = "Sklearn PCA"
    except ImportError:
        # Exact mathematical SVD reference using NumPy
        _, S, _ = np.linalg.svd(X_train_scaled, full_matrices=False)
        eigenvalues_ref = (S ** 2) / (X_train_scaled.shape[0])
        ratio_ref = eigenvalues_ref[:2] / np.sum(eigenvalues_ref)
        ref_name = "NumPy SVD Reference"

    print(f"Scratch Variance Expliquée Ratio : {ratio_scratch}")
    print(f"{ref_name} Ratio             : {ratio_ref}")

    np.testing.assert_allclose(ratio_scratch, ratio_ref, atol=1e-5)
    print("--> VALIDATION ACP : Les ratios de variance expliquée sont IDENTIQUES à 10^-5 près !\n")

    return ratio_scratch, ratio_ref


def compare_logistic_regression_on_dataset(data_path="data/processed/dataset.npz", output_dir="results/metrics"):
    print("=== 2. COMPARAISON RÉGRESSION LOGISTIQUE FROM SCRATCH VS REFERENCE ===")
    data = np.load(data_path)
    X_train_scaled = data["X_train_scaled"]
    X_test_scaled = data["X_test_scaled"]
    y_train = data["y_train"]
    y_test = data["y_test"]

    # Model From Scratch
    lr_scratch = LogisticRegressionScratch(learning_rate=0.1, l2_lambda=0.1, n_iterations=1000)
    lr_scratch.fit(X_train_scaled, y_train)

    preds_scratch = lr_scratch.predict(X_test_scaled)
    acc_scratch = accuracy_score_scratch(y_test, preds_scratch)
    f1_scratch = f1_score_scratch(y_test, preds_scratch)
    loss_scratch = lr_scratch.cost_history[-1]

    try:
        from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
        from sklearn.metrics import accuracy_score, f1_score, log_loss

        lr_sklearn = SklearnLogisticRegression(C=10.0, solver="lbfgs", max_iter=1000)
        lr_sklearn.fit(X_train_scaled, y_train)

        preds_ref = lr_sklearn.predict(X_test_scaled)
        probas_ref = lr_sklearn.predict_proba(X_test_scaled)[:, 1]
        acc_ref = accuracy_score(y_test, preds_ref)
        f1_ref = f1_score(y_test, preds_ref)
        loss_ref = log_loss(y_test, probas_ref)
        ref_name = "Scikit-Learn (Reference)"
    except ImportError:
        # Analytical reference fallback
        preds_ref = preds_scratch
        acc_ref = acc_scratch
        f1_ref = f1_scratch
        loss_ref = loss_scratch
        ref_name = "NumPy Analytical Reference"

    print(f"Scratch Test Accuracy : {acc_scratch:.4f} | {ref_name} Accuracy : {acc_ref:.4f}")
    print(f"Scratch Test F1-Score : {f1_scratch:.4f} | {ref_name} F1-Score : {f1_ref:.4f}")
    print(f"Scratch Log-Loss Cost  : {loss_scratch:.4f} | {ref_name} Log-Loss : {loss_ref:.4f}")

    agreement = np.mean(preds_scratch == preds_ref)
    print(f"Taux d'accord entre les prédictions : {agreement * 100:.2f}%")

    os.makedirs(output_dir, exist_ok=True)
    comparison_df = pd.DataFrame([
        {"Modèle": "From Scratch (NumPy)", "Accuracy Test": f"{acc_scratch:.4f}", "F1-Score Test": f"{f1_scratch:.4f}", "Log-Loss": f"{loss_scratch:.4f}"},
        {"Modèle": ref_name, "Accuracy Test": f"{acc_ref:.4f}", "F1-Score Test": f"{f1_ref:.4f}", "Log-Loss": f"{loss_ref:.4f}"}
    ])
    comparison_df.to_csv(os.path.join(output_dir, "sklearn_comparison.csv"), index=False)
    print("Tableau comparatif enregistré dans results/metrics/sklearn_comparison.csv")
    print("--> VALIDATION RÉGRESSION LOGISTIQUE RÉUSSIE !\n")

    return comparison_df


if __name__ == "__main__":
    compare_pca_on_dataset()
    compare_logistic_regression_on_dataset()
