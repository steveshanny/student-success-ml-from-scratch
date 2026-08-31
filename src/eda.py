"""
Exploratory Data Analysis module for Student Success Dataset.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def perform_eda(data_path="data/raw/student_data.csv", output_dir="results"):
    """Perform exploratory data analysis and save figures/metrics."""
    df = pd.read_csv(data_path)
    
    figures_dir = os.path.join(output_dir, "figures")
    metrics_dir = os.path.join(output_dir, "metrics")
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(metrics_dir, exist_ok=True)

    # 1. Summary Statistics
    stats = df.describe().T
    stats.to_csv(os.path.join(metrics_dir, "eda_summary.csv"))
    print("Summary statistics saved to results/metrics/eda_summary.csv")

    # 2. Target Distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(x="academic_success", data=df, palette="viridis")
    plt.title("Distribution de la Réussite Académique (0 = Échec, 1 = Réussite)")
    plt.xlabel("Réussite Académique")
    plt.ylabel("Nombre d'Étudiants")
    plt.savefig(os.path.join(figures_dir, "target_distribution.png"), bbox_inches="tight")
    plt.close()

    # 3. Correlation Matrix
    plt.figure(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True)
    plt.title("Matrice de Corrélation des Caractéristiques Académiques")
    plt.savefig(os.path.join(figures_dir, "correlation_matrix.png"), bbox_inches="tight")
    plt.close()

    print(f"EDA Completed: Target proportion = {df['academic_success'].mean():.2%}")
    return df


if __name__ == "__main__":
    perform_eda()
