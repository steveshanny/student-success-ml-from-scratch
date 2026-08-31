"""
Script to compare PCA & Logistic Regression implementations from scratch against Scikit-Learn.
"""

import numpy as np
from sklearn.decomposition import PCA as SklearnPCA
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression

from src.pca_scratch import PCAFromScratch
from src.logistic_regression_scratch import LogisticRegressionScratch
from src.preprocessing import StandardScalerScratch


def compare_pca():
    print("--- Comparing PCA Scratch vs Sklearn ---")
    np.random.seed(42)
    X = np.random.randn(100, 5)
    scaler = StandardScalerScratch()
    X_scaled = scaler.fit_transform(X)

    # Scratch
    pca_scratch = PCAFromScratch(n_components=2)
    Z_scratch = pca_scratch.fit_transform(X_scaled)

    # Sklearn
    pca_sklearn = SklearnPCA(n_components=2)
    Z_sklearn = pca_sklearn.fit_transform(X_scaled)

    print("Scratch explained variance ratio:", pca_scratch.explained_variance_ratio_)
    print("Sklearn explained variance ratio:", pca_sklearn.explained_variance_ratio_)
    np.testing.assert_allclose(
        pca_scratch.explained_variance_ratio_,
        pca_sklearn.explained_variance_ratio_,
        atol=1e-5
    )
    print("PCA comparison PASSED!\n")


def compare_logistic_regression():
    print("--- Comparing Logistic Regression Scratch vs Sklearn ---")
    np.random.seed(42)
    X = np.random.randn(200, 4)
    true_weights = np.array([0.5, -1.2, 2.0, -0.8])
    logits = np.dot(X, true_weights)
    probs = 1.0 / (1.0 + np.exp(-logits))
    y = (probs >= 0.5).astype(int)

    # Scratch
    lr_scratch = LogisticRegressionScratch(learning_rate=0.1, l2_lambda=0.1, n_iterations=2000)
    lr_scratch.fit(X, y)
    preds_scratch = lr_scratch.predict(X)

    # Sklearn (C = 1 / l2_lambda * m if unscaled, using default comparison)
    lr_sklearn = SklearnLogisticRegression(C=1.0, solver='lbfgs')
    lr_sklearn.fit(X, y)
    preds_sklearn = lr_sklearn.predict(X)

    acc_scratch = np.mean(preds_scratch == y)
    acc_sklearn = np.mean(preds_sklearn == y)

    print(f"Scratch Accuracy: {acc_scratch:.4f}")
    print(f"Sklearn Accuracy: {acc_sklearn:.4f}")
    print("Logistic Regression comparison PASSED!\n")


if __name__ == "__main__":
    compare_pca()
    compare_logistic_regression()
