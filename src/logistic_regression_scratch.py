"""
Logistic Regression with L2 regularization trained via gradient descent from scratch using NumPy.
"""

import os
import numpy as np
import matplotlib.pyplot as plt


def sigmoid(z):
    """
    Compute numerically stable sigmoid activation function.
    sigma(z) = 1 / (1 + exp(-z))
    """
    z_clipped = np.clip(z, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(-z_clipped))


class LogisticRegressionScratch:
    """
    Logistic Regression classifier with L2 regularization from scratch using NumPy.
    All mathematical operations (sigmoid, hypothesis, log loss, gradient, updates) are vectorized.
    """

    def __init__(self, learning_rate=0.1, l2_lambda=0.1, n_iterations=1000, threshold=0.5):
        self.learning_rate = learning_rate
        self.l2_lambda = l2_lambda
        self.n_iterations = n_iterations
        self.threshold = threshold
        self.theta = None
        self.cost_history = []

    def cost_function(self, X_b, y, theta):
        """
        Compute vectorized Log-Loss cost function with L2 regularization:
        J(theta) = - (1/m) * sum(y*log(y_hat) + (1-y)*log(1-y_hat)) + (lambda / 2m) * sum(theta_j^2) [j >= 1]
        """
        m = len(y)
        y_hat = sigmoid(np.dot(X_b, theta))

        # Protection against log(0)
        eps = 1e-15
        y_hat_clipped = np.clip(y_hat, eps, 1.0 - eps)

        # Vectorized Log Loss
        cost = - (1.0 / m) * np.sum(
            y * np.log(y_hat_clipped) + (1.0 - y) * np.log(1.0 - y_hat_clipped)
        )

        # L2 Regularization (excluding intercept theta_0)
        l2_cost = (self.l2_lambda / (2.0 * m)) * np.sum(theta[1:] ** 2)

        return cost + l2_cost

    def gradient(self, X_b, y, theta):
        """
        Compute vectorized analytical gradient of Log-Loss with L2 regularization:
        grad = (1/m) * X^T * (y_hat - y) + (lambda/m) * [0, theta_1, ..., theta_n]^T
        """
        m = len(y)
        y_hat = sigmoid(np.dot(X_b, theta))
        error = y_hat - y

        grad = (1.0 / m) * np.dot(X_b.T, error)

        # L2 penalty gradient (excluding intercept theta_0)
        reg_penalty = (self.l2_lambda / m) * theta
        reg_penalty[0] = 0.0

        return grad + reg_penalty

    def fit(self, X, y):
        """
        Train Logistic Regression model using vectorized Gradient Descent.
        """
        X_arr = np.asarray(X, dtype=np.float64)
        y_arr = np.asarray(y, dtype=np.float64).reshape(-1)

        # Add bias / intercept column
        m, n = X_arr.shape
        X_b = np.hstack([np.ones((m, 1)), X_arr])

        # Initialize parameters
        self.theta = np.zeros(n + 1, dtype=np.float64)
        self.cost_history = []

        # Vectorized gradient descent iterations
        for _ in range(self.n_iterations):
            cost = self.cost_function(X_b, y_arr, self.theta)
            grad = self.gradient(X_b, y_arr, self.theta)

            self.theta -= self.learning_rate * grad
            self.cost_history.append(cost)

        return self

    def decision_function(self, X):
        """Return confidence scores (logits) for X."""
        if self.theta is None:
            raise ValueError("Model is not fitted yet.")
        X_arr = np.asarray(X, dtype=np.float64)
        m = X_arr.shape[0]
        X_b = np.hstack([np.ones((m, 1)), X_arr])
        return np.dot(X_b, self.theta)

    def predict_proba(self, X):
        """Return estimated probabilities for positive class y=1."""
        return sigmoid(self.decision_function(X))

    def predict(self, X):
        """Predict binary class labels (0 or 1) based on classification threshold."""
        probas = self.predict_proba(X)
        return (probas >= self.threshold).astype(int)


def run_logistic_regression_pipeline(data_path="data/processed/dataset.npz", output_dir="results/figures"):
    """Fit logistic regression model on student dataset and plot convergence curve."""
    data = np.load(data_path)
    X_train_scaled = data["X_train_scaled"]
    y_train = data["y_train"]

    model = LogisticRegressionScratch(learning_rate=0.1, l2_lambda=0.1, n_iterations=1000)
    model.fit(X_train_scaled, y_train)

    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.plot(model.cost_history, color="blue", linewidth=2, label=r"Coût $J(\theta)$ ($\alpha=0.1, \lambda=0.1$)")
    plt.title("Courbe de Convergence de la Régression Logistique (Descente de Gradient)")
    plt.xlabel("Itérations")
    plt.ylabel("Coût Log-Loss + L2")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="upper right")
    plt.savefig(os.path.join(output_dir, "learning_curve_default.png"), bbox_inches="tight")
    plt.close()

    print(f"Logistic Regression pipeline finished. Initial Cost: {model.cost_history[0]:.4f} -> Final Cost: {model.cost_history[-1]:.4f}")
    return model


if __name__ == "__main__":
    run_logistic_regression_pipeline()
