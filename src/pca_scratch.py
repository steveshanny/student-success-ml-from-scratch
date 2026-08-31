"""
Principal Component Analysis (PCA) implemented from scratch using NumPy.
"""

import numpy as np


class PCAFromScratch:
    """
    PCA implemented from scratch using linear algebra operations in NumPy.
    """

    def __init__(self, n_components=2):
        self.n_components = n_components
        self.components_ = None
        self.eigenvalues_ = None
        self.explained_variance_ratio_ = None

    def fit(self, X):
        """
        Fit the model with X by computing covariance matrix and spectral decomposition.
        Assumes X is already centered/standardized.
        """
        X_arr = np.asarray(X, dtype=np.float64)
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

        # Explained variance ratio
        total_variance = np.sum(self.eigenvalues_)
        self.explained_variance_ratio_ = (
            self.eigenvalues_[: self.n_components] / total_variance
        )

        return self

    def transform(self, X):
        """Apply dimensionality reduction to X."""
        if self.components_ is None:
            raise ValueError("PCA instance is not fitted yet.")
        X_arr = np.asarray(X, dtype=np.float64)
        return np.dot(X_arr, self.components_)

    def fit_transform(self, X):
        """Fit the model with X and apply dimensionality reduction."""
        return self.fit(X).transform(X)
