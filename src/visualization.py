"""
Visualization utilities for PCA, learning curves, and classification metrics.
"""

import matplotlib.pyplot as plt
import seaborn as sns


def plot_cost_history(cost_history, title="Cost History", save_path=None):
    """Plot gradient descent cost over iterations."""
    plt.figure(figsize=(8, 5))
    plt.plot(cost_history, color='blue', linewidth=2)
    plt.title(title)
    plt.xlabel("Iterations")
    plt.ylabel("Cost J(theta)")
    plt.grid(True, linestyle='--', alpha=0.6)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def plot_pca_2d(Z, y, title="PCA 2D Projection", save_path=None):
    """Plot 2D PCA projection of samples colored by target class."""
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(Z[:, 0], Z[:, 1], c=y, cmap='coolwarm', alpha=0.7, edgecolors='k')
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title(title)
    plt.colorbar(scatter, label="Academic Success")
    plt.grid(True, linestyle='--', alpha=0.6)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()
