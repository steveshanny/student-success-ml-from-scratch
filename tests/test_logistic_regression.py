import numpy as np
from src.logistic_regression_scratch import sigmoid, LogisticRegressionScratch


def test_sigmoid():
    assert np.isclose(sigmoid(0), 0.5)
    assert sigmoid(100) > 0.999
    assert sigmoid(-100) < 0.001


def test_logistic_regression_convergence():
    # Simple linearly separable dataset
    X = np.array([[1.0, 2.0], [2.0, 3.0], [3.0, 1.0], [6.0, 7.0], [7.0, 8.0], [8.0, 6.0]])
    y = np.array([0, 0, 0, 1, 1, 1])

    model = LogisticRegressionScratch(learning_rate=0.1, n_iterations=500)
    model.fit(X, y)

    # Cost should decrease over iterations
    assert model.cost_history[0] > model.cost_history[-1]

    # Predictions should match y
    preds = model.predict(X)
    assert np.array_equal(preds, y)
