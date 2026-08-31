"""
Preprocessing module containing functions for standardization, dataset cleaning, and split.
"""

import os
import numpy as np
import pandas as pd


class StandardScalerScratch:
    """
    StandardScaler implemented from scratch using NumPy.
    Standardizes features by removing the mean and scaling to unit variance:
    X_scaled = (X - mean) / std
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


def train_test_split_scratch(X, y, test_size=0.2, random_state=42):
    """
    Split arrays or matrices into random train and test subsets from scratch using NumPy.
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


def prepare_and_save_data(raw_path="data/raw/student_data.csv", processed_dir="data/processed"):
    """Load raw dataset, separate features/target, split, standardize, and save processed splits."""
    df = pd.read_csv(raw_path)
    X = df.drop(columns=["academic_success"]).values
    y = df["academic_success"].values

    X_train, X_test, y_train, y_test = train_test_split_scratch(X, y, test_size=0.2, random_state=42)

    scaler = StandardScalerScratch()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    os.makedirs(processed_dir, exist_ok=True)
    np.savez(
        os.path.join(processed_dir, "dataset.npz"),
        X_train=X_train,
        X_test=X_test,
        X_train_scaled=X_train_scaled,
        X_test_scaled=X_test_scaled,
        y_train=y_train,
        y_test=y_test,
        feature_names=np.array(df.drop(columns=["academic_success"]).columns, dtype=str)
    )
    print(f"Prepared and saved processed dataset to {processed_dir}/dataset.npz")
    return X_train_scaled, X_test_scaled, y_train, y_test


if __name__ == "__main__":
    prepare_and_save_data()
