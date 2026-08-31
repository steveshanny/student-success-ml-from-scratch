import numpy as np
from src.pca_scratch import PCAFromScratch


def test_pca_scratch():
    # Generate 2D correlated data
    np.random.seed(42)
    X = np.random.randn(100, 3)
    X[:, 1] = X[:, 0] * 2 + 0.5 * np.random.randn(100)

    # Standardize first
    X_centered = X - np.mean(X, axis=0)

    pca = PCAFromScratch(n_components=2)
    Z = pca.fit_transform(X_centered)

    assert Z.shape == (100, 2)
    assert len(pca.explained_variance_ratio_) == 2
    assert np.sum(pca.explained_variance_ratio_) <= 1.0
    assert pca.explained_variance_ratio_[0] >= pca.explained_variance_ratio_[1]
