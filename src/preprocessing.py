"""
Preprocessing module containing functions for standardization and dataset split.
"""

import numpy as np


class StandardScalerScratch:
    """
    StandardScaler implemented from scratch using NumPy.
    Standardizes features by removing the mean and scaling to unit variance.
    """

    def __init__(self):
        self.mean_ = None
        self.scale_ = None

    def fit(self, X):
        """Compute the mean and std to be used for later scaling."""
        X_arr = np.asarray(X, dtype=np.float64)
        self.mean_ = np.mean(X_arr, axis=0)
        self.scale_ = np.std(X_arr, axis=0)
        # Avoid division by zero for constant features
        self.scale_[self.scale_ == 0.0] = 1.0
        return self

    def transform(self, X):
        """Perform standardization by centering and scaling."""
        if self.mean_ is None or self.scale_ is None:
            raise ValueError("StandardScaler instance is not fitted yet.")
        X_arr = np.asarray(X, dtype=np.float64)
        return (X_arr - self.mean_) / self.scale_

    def fit_transform(self, X):
        """Fit to data, then transform it."""
        return self.fit(X).transform(X)


def train_test_split_scratch(X, y, test_size=0.2, random_state=None):
    """
    Split arrays or matrices into random train and test subsets from scratch.
    """
    X_arr = np.asarray(X)
    y_arr = np.asarray(y)

    if len(X_arr) != len(y_arr):
        raise ValueError("X and y must have the same length.")

    n_samples = len(X_arr)
    n_test = int(n_samples * test_size)

    if random_state is not None:
        np.random.seed(random_state)

    indices = np.random.permutation(n_samples)
    test_idx = indices[:n_test]
    train_idx = indices[n_test:]

    return X_arr[train_idx], X_arr[test_idx], y_arr[train_idx], y_arr[test_idx]
