import numpy as np
from src.preprocessing import StandardScalerScratch, train_test_split_scratch


def test_standard_scaler():
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    scaler = StandardScalerScratch()
    X_scaled = scaler.fit_transform(X)

    # Check mean is approx 0 and std is approx 1
    assert np.allclose(np.mean(X_scaled, axis=0), [0.0, 0.0])
    assert np.allclose(np.std(X_scaled, axis=0), [1.0, 1.0])


def test_train_test_split():
    X = np.arange(20).reshape(10, 2)
    y = np.arange(10)

    X_train, X_test, y_train, y_test = train_test_split_scratch(
        X, y, test_size=0.2, random_state=42
    )

    assert len(X_train) == 8
    assert len(X_test) == 2
    assert len(y_train) == 8
    assert len(y_test) == 2
