"""
Experiments module for learning rate analysis and standardization impact analysis.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from src.logistic_regression_scratch import LogisticRegressionScratch


def experiment_learning_rates(data_path="data/processed/dataset.npz", output_dir="results/figures"):
    """
    Compare gradient descent convergence across different learning rates alpha:
    - Alpha too small (0.001)
    - Alpha optimal (0.1)
    - Alpha too large (3.5)
    """
    data = np.load(data_path, allow_pickle=True)
    X_train_scaled = data["X_train_scaled"]
    y_train = data["y_train"]

    alphas = [0.001, 0.1, 3.5]
    n_iterations = 200

    plt.figure(figsize=(8, 5))

    for alpha in alphas:
        model = LogisticRegressionScratch(learning_rate=alpha, l2_lambda=0.01, n_iterations=n_iterations)
        model.fit(X_train_scaled, y_train)
        plt.plot(model.cost_history, label=f"alpha = {alpha}")

    plt.xlabel("Itérations")
    plt.ylabel("Coût J(theta)")
    plt.title("Impact du Pas d'Apprentissage (Learning Rate alpha) sur la Convergence")
    plt.ylim(0, 1.5)
    plt.legend(loc="upper right")
    plt.grid(True, linestyle="--", alpha=0.5)

    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "learning_rate_comparison.png"), bbox_inches="tight")
    plt.close()
    print("Saved learning rate comparison figure to results/figures/learning_rate_comparison.png")


def experiment_standardization(data_path="data/processed/dataset.npz", output_dir="results/figures"):
    """
    Compare convergence speed between scaled and unscaled feature representations.
    """
    data = np.load(data_path, allow_pickle=True)
    X_train_raw = data["X_train"]
    X_train_scaled = data["X_train_scaled"]
    y_train = data["y_train"]

    n_iterations = 300
    alpha = 0.01

    model_unscaled = LogisticRegressionScratch(learning_rate=alpha, l2_lambda=0.01, n_iterations=n_iterations)
    model_unscaled.fit(X_train_raw, y_train)

    model_scaled = LogisticRegressionScratch(learning_rate=alpha, l2_lambda=0.01, n_iterations=n_iterations)
    model_scaled.fit(X_train_scaled, y_train)

    plt.figure(figsize=(8, 5))
    plt.plot(model_unscaled.cost_history, color="red", linestyle="--", linewidth=2, label="Données NON Standardisées")
    plt.plot(model_scaled.cost_history, color="green", linewidth=2, label="Données Standardisées (StandardScaler)")
    plt.xlabel("Itérations")
    plt.ylabel("Coût J(theta)")
    plt.title("Impact de la Standardisation des Variables sur la Descente de Gradient")
    plt.legend(loc="upper right")
    plt.grid(True, linestyle="--", alpha=0.5)

    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "standardization_comparison.png"), bbox_inches="tight")
    plt.close()
    print("Saved standardization comparison figure to results/figures/standardization_comparison.png")


if __name__ == "__main__":
    experiment_learning_rates()
    experiment_standardization()
