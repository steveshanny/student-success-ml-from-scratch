"""
Principal Component Analysis (PCA) implemented from scratch using NumPy.
"""

import os
import numpy as np
import matplotlib.pyplot as plt


class PCAFromScratch:
    """
    PCA implemented from scratch using linear algebra spectral decomposition in NumPy.
    """

    def __init__(self, n_components=2):
        self.n_components = n_components
        self.components_ = None
        self.eigenvalues_ = None
        self.explained_variance_ratio_ = None

    def fit(self, X):
        """
        Fit the model with X by computing covariance matrix and spectral decomposition.
        Assumes X is centered/standardized.
        """
        X_arr = np.asarray(X, dtype=np.float64)
        if X_arr.ndim != 2:
            raise ValueError(f"X must be 2D, got {X_arr.ndim}D")
        if X_arr.shape[0] < 2:
            raise ValueError("X must have at least 2 samples for covariance computation")
        if self.n_components > X_arr.shape[1]:
            raise ValueError(f"n_components ({self.n_components}) cannot exceed n_features ({X_arr.shape[1]})")

        m = X_arr.shape[0]

        # Covariance matrix: Sigma = (1/m) * X^T * X
        cov_matrix = (1.0 / m) * np.dot(X_arr.T, X_arr)

        # Eigenvalue decomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        # Sort eigenvalues and eigenvectors in descending order
        idx = np.argsort(eigenvalues)[::-1]
        self.eigenvalues_ = eigenvalues[idx]
        sorted_vectors = eigenvectors[:, idx]

        # Select top n_components
        self.components_ = sorted_vectors[:, : self.n_components]

        # Explained variance ratio: lambda_i / sum(lambda_j)
        total_variance = np.sum(self.eigenvalues_)
        self.explained_variance_ratio_ = (
            self.eigenvalues_[: self.n_components] / total_variance
        )

        return self

    def transform(self, X):
        """Apply dimensionality reduction (projection Z = X * W)."""
        if self.components_ is None:
            raise ValueError("PCA instance is not fitted yet.")
        X_arr = np.asarray(X, dtype=np.float64)
        return np.dot(X_arr, self.components_)

    def fit_transform(self, X):
        """Fit the model with X and apply dimensionality reduction."""
        return self.fit(X).transform(X)


def run_pca_pipeline(data_path="data/processed/dataset.npz", output_dir="results/figures"):
    """Run PCA pipeline on dataset and save 2D projection and variance figures."""
    if not os.path.exists(data_path):
        from src.preprocessing import prepare_and_save_data
        prepare_and_save_data()

    data = np.load(data_path, allow_pickle=True)
    X_train_scaled = data["X_train_scaled"]
    y_train = data["y_train"]

    pca = PCAFromScratch(n_components=2)
    Z = pca.fit_transform(X_train_scaled)

    os.makedirs(output_dir, exist_ok=True)

    # 1. 2D Scatter Plot
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(Z[:, 0], Z[:, 1], c=y_train, cmap="coolwarm", alpha=0.7, edgecolors="k")
    plt.xlabel("Première Composante Principale (PC1)")
    plt.ylabel("Deuxième Composante Principale (PC2)")
    plt.title("Projection ACP 2D — Réussite Académique (0 = Non-réussite, 1 = Réussite)")
    plt.colorbar(scatter, label="Réussite Académique")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.savefig(os.path.join(output_dir, "pca_2d_projection.png"), bbox_inches="tight")
    plt.close()

    # 2. Explained Variance Scree Plot
    full_pca = PCAFromScratch(n_components=X_train_scaled.shape[1])
    full_pca.fit(X_train_scaled)
    cum_variance = np.cumsum(full_pca.explained_variance_ratio_)

    plt.figure(figsize=(8, 5))
    plt.bar(range(1, len(cum_variance) + 1), full_pca.explained_variance_ratio_, alpha=0.6, label="Variance Individuelle")
    plt.step(range(1, len(cum_variance) + 1), cum_variance, where="mid", color="red", label="Variance Cumulée")
    plt.xlabel("Composantes Principales")
    plt.ylabel("Ratio de Variance Expliquée")
    plt.title("Scree Plot — Variance Expliquée par les Composantes Principales")
    plt.legend(loc="best")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.savefig(os.path.join(output_dir, "pca_explained_variance.png"), bbox_inches="tight")
    plt.close()

    print(f"PCA Pipeline completed. PC1 & PC2 explained variance: {pca.explained_variance_ratio_ * 100}%")
    return pca, Z


if __name__ == "__main__":
    run_pca_pipeline()
