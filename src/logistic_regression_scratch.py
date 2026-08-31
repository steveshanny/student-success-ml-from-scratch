"""
Logistic Regression with L2 regularization trained via gradient descent from scratch using NumPy.
"""

import numpy as np


def sigmoid(z):
    """
    Compute numerically stable sigmoid activation function.
    sigma(z) = 1 / (1 + exp(-z))
    """
    z_clipped = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z_clipped))


class LogisticRegressionScratch:
    """
    Logistic Regression classifier with L2 regularization from scratch using NumPy.
    """

    def __init__(self, learning_rate=0.01, l2_lambda=0.0, n_iterations=1000, threshold=0.5):
        self.learning_rate = learning_rate
        self.l2_lambda = l2_lambda
        self.n_iterations = n_iterations
        self.threshold = threshold
        self.theta = None
        self.cost_history = []

    def cost_function(self, X, y, theta):
        """
        Compute vectorized Log-Loss cost function with L2 regularization.
        """
        m = len(y)
        y_hat = sigmoid(np.dot(X, theta))
        
        # Clip y_hat to avoid log(0)
        eps = 1e-15
        y_hat_clipped = np.clip(y_hat, eps, 1.0 - eps)

        # Log Loss
        cost = - (1.0 / m) * np.sum(
            y * np.log(y_hat_clipped) + (1.0 - y) * np.log(1.0 - y_hat_clipped)
        )

        # L2 Regularization (excluding intercept theta_0)
        l2_cost = (self.l2_lambda / (2.0 * m)) * np.sum(theta[1:] ** 2)

        return cost + l2_cost

    def gradient(self, X, y, theta):
        """
        Compute vectorized gradient of Log-Loss with L2 regularization.
        """
        m = len(y)
        y_hat = sigmoid(np.dot(X, theta))
        error = y_hat - y

        grad = (1.0 / m) * np.dot(X.T, error)

        # L2 penalty gradient (excluding intercept theta_0)
        reg_penalty = (self.l2_lambda / m) * theta
        reg_penalty[0] = 0.0

        return grad + reg_penalty

    def fit(self, X, y):
        """
        Train Logistic Regression model using Gradient Descent.
        """
        X_arr = np.asarray(X, dtype=np.float64)
        y_arr = np.asarray(y, dtype=np.float64).reshape(-1)

        # Add bias / intercept column
        m, n = X_arr.shape
        X_b = np.hstack([np.ones((m, 1)), X_arr])

        # Initialize parameters
        self.theta = np.zeros(n + 1, dtype=np.float64)
        self.cost_history = []

        for _ in range(self.n_iterations):
            cost = self.cost_function(X_b, y_arr, self.theta)
            grad = self.gradient(X_b, y_arr, self.theta)

            self.theta -= self.learning_rate * grad
            self.cost_history.append(cost)

        return self

    def predict_proba(self, X):
        """Return probability estimates for positive class."""
        if self.theta is None:
            raise ValueError("Model is not fitted yet.")
        X_arr = np.asarray(X, dtype=np.float64)
        m = X_arr.shape[0]
        X_b = np.hstack([np.ones((m, 1)), X_arr])
        return sigmoid(np.dot(X_b, self.theta))

    def predict(self, X):
        """Predict class labels for X."""
        probas = self.predict_proba(X)
        return (probas >= self.threshold).astype(int)
