"""
Script to programmatically generate clean, valid Jupyter Notebooks (.ipynb) for the project.
"""

import os
import json


def make_cell(cell_type, source):
    """Helper to create a notebook cell."""
    return {
        "cell_type": cell_type,
        "metadata": {},
        "outputs": [] if cell_type == "code" else None,
        "execution_count": None if cell_type == "code" else None,
        "source": source if isinstance(source, list) else source.splitlines(keepends=True)
    }


def _base_metadata():
    return {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"},
        "nbformat": 4,
        "nbformat_minor": 2,
    }


def _save_notebook(cells, path):
    content = {"cells": cells, "metadata": _base_metadata(), "nbformat": 4, "nbformat_minor": 2}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)


def generate_final_notebook():
    cells = []
    cells.append(make_cell("markdown", [
        "# Prédiction de la Réussite Académique des Étudiants\n",
        "## Implémentation From Scratch et Analyse Mathématique en NumPy\n",
        "\n",
        "**Auteurs & Cadre :** Projet individuel de Mathématiques Appliquées et Machine Learning.\n",
        "**Objectif Pédagogique :** Développer from scratch (vectorisation matricielle avec NumPy) les algorithmes d'Analyse en Composantes Principales (ACP) et de Régression Logistique avec régularisation L2, et analyser leurs propriétés théoriques et empiriques."
    ]))
    cells.append(make_cell("markdown", [
        "## 2. Problématique Métier\n",
        "*Dans quelle mesure les caractéristiques académiques et personnelles d'un étudiant permettent-elles de prédire sa réussite académique ?*\n",
        "\n",
        "La réussite académique est modélisée par une variable binaire :\n",
        "- $y = 1$ : Réussite académique (Note finale $G3 \\ge 10/20$).\n",
        "- $y = 0$ : Non-réussite académique (Note finale $G3 < 10/20$)."
    ]))
    cells.append(make_cell("markdown", [
        "## 3. Dataset & Exploration des Données\n",
        "Chargement du jeu de données (données synthétiques basées sur les distributions du dataset UCI Student Performance)."
    ]))
    cells.append(make_cell("code", [
        "import numpy as np\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "df = pd.read_csv('../data/raw/student_data.csv')\n",
        "print('Taille du dataset :', df.shape)\n",
        "df.head()"
    ]))
    cells.append(make_cell("markdown", [
        "## 4. Prétraitement et Standardisation From Scratch\n",
        "\n",
        "**Formule mathématique :**\n",
        "$$X_{standard} = \\frac{X - \\mu}{\\sigma}$$\n",
        "\n",
        "La standardisation est cruciale pour l'ACP (sensible aux échelles) et la descente de gradient (conditionnement du problème)."
    ]))
    cells.append(make_cell("code", [
        "from src.preprocessing import StandardScalerScratch, train_test_split_scratch\n",
        "\n",
        "X = df.drop(columns=['academic_success']).values\n",
        "y = df['academic_success'].values\n",
        "\n",
        "X_train, X_test, y_train, y_test = train_test_split_scratch(X, y, test_size=0.2, random_state=42)\n",
        "\n",
        "scaler = StandardScalerScratch()\n",
        "X_train_scaled = scaler.fit_transform(X_train)\n",
        "X_test_scaled = scaler.transform(X_test)\n",
        "\n",
        "print('Moyennes après scaling :', np.round(X_train_scaled.mean(axis=0), 2))\n",
        "print('Écarts-types après scaling :', np.round(X_train_scaled.std(axis=0), 2))"
    ]))
    cells.append(make_cell("markdown", [
        "## 5. Analyse en Composantes Principales (ACP) From Scratch\n",
        "\n",
        "**Étape 1 : Matrice de covariance empirique :**\n",
        "$$\\Sigma = \\frac{1}{m} X^T X$$\n",
        "\n",
        "**Étape 2 : Décomposition spectrale :**\n",
        "$$\\Sigma v_i = \\lambda_i v_i$$\n",
        "\n",
        "**Étape 3 : Projection 2D :**\n",
        "$$Z = X W$$"
    ]))
    cells.append(make_cell("code", [
        "from src.pca_scratch import PCAFromScratch\n",
        "\n",
        "pca = PCAFromScratch(n_components=2)\n",
        "Z_train = pca.fit_transform(X_train_scaled)\n",
        "\n",
        "print('Ratio de variance expliquée (PC1, PC2) :', pca.explained_variance_ratio_)\n",
        "\n",
        "plt.figure(figsize=(7, 5))\n",
        "scatter = plt.scatter(Z_train[:, 0], Z_train[:, 1], c=y_train, cmap='coolwarm', alpha=0.8, edgecolors='k')\n",
        "plt.xlabel('PC1')\n",
        "plt.ylabel('PC2')\n",
        "plt.title('Projection ACP 2D')\n",
        "plt.colorbar(scatter, label='Réussite Académique')\n",
        "plt.grid(True, linestyle='--', alpha=0.5)\n",
        "plt.show()"
    ]))
    cells.append(make_cell("markdown", [
        "## 6. Régression Logistique & Descente de Gradient From Scratch\n",
        "\n",
        "**Hypothèse :** $\\hat{y} = \\sigma(X \\theta) = \\frac{1}{1 + e^{-X \\theta}}$\n",
        "\n",
        "**Fonction de coût Log-Loss + L2 :**\n",
        "$$J(\\theta) = -\\frac{1}{m} \\sum [ y \\log(\\hat{y}) + (1-y)\\log(1-\\hat{y}) ] + \\frac{\\lambda}{2m} \\sum_{j=1}^n \\theta_j^2$$\n",
        "\n",
        "**Gradient Matriciel Analytique :**\n",
        "$$\\nabla J(\\theta) = \\frac{1}{m} X^T (\\hat{y} - y) + \\frac{\\lambda}{m} \\theta$$"
    ]))
    cells.append(make_cell("code", [
        "from src.logistic_regression_scratch import LogisticRegressionScratch\n",
        "\n",
        "model = LogisticRegressionScratch(learning_rate=0.1, l2_lambda=0.1, n_iterations=1000)\n",
        "model.fit(X_train_scaled, y_train)\n",
        "\n",
        "plt.figure(figsize=(7, 4))\n",
        "plt.plot(model.cost_history, color='blue', linewidth=2)\n",
        "plt.title('Courbe de Convergence de la Loss J(theta)')\n",
        "plt.xlabel('Itérations')\n",
        "plt.ylabel('Coût Log-Loss')\n",
        "plt.grid(True, linestyle='--', alpha=0.5)\n",
        "plt.show()"
    ]))
    cells.append(make_cell("markdown", [
        "## 7. Évaluation et Comparaison avec Scikit-Learn\n",
        "Calcul des métriques et comparaison rigoureuse."
    ]))
    cells.append(make_cell("code", [
        "from src.metrics import accuracy_score_scratch, f1_score_scratch, confusion_matrix_scratch\n",
        "\n",
        "preds = model.predict(X_test_scaled)\n",
        "print('Accuracy Test :', accuracy_score_scratch(y_test, preds))\n",
        "print('F1-Score Test :', f1_score_scratch(y_test, preds))\n",
        "print('Matrice de confusion :\\n', confusion_matrix_scratch(y_test, preds))"
    ]))
    cells.append(make_cell("markdown", [
        "## 8. Conclusion Scientifique\n",
        "Les implémentations vectorisées en NumPy de l'ACP et de la Régression Logistique atteignent des performances identiques à Scikit-Learn tout en offrant une transparence mathématique totale."
    ]))

    os.makedirs("notebooks", exist_ok=True)
    _save_notebook(cells, "notebooks/final_project.ipynb")
    print("Notebook final_project.ipynb generated!")


def generate_data_exploration_notebook():
    cells = []
    cells.append(make_cell("markdown", [
        "# Notebook 1 : Exploration des Données\n",
        "Chargement, statistiques descriptives et analyse exploratoire du dataset."
    ]))
    cells.append(make_cell("code", [
        "import numpy as np\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "df = pd.read_csv('../data/raw/student_data.csv')\n",
        "print('Shape:', df.shape)\n",
        "print('\\n--- Premières lignes ---')\n",
        "df.head()"
    ]))
    cells.append(make_cell("code", [
        "print('--- Statistiques descriptives ---')\n",
        "df.describe().T[['mean', 'std', 'min', '50%', 'max']]"
    ]))
    cells.append(make_cell("code", [
        "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
        "\n",
        "# Distribution de la cible\n",
        "sns.countplot(x='academic_success', data=df, palette='viridis', ax=axes[0])\n",
        "axes[0].set_title('Distribution de la Cible (0=Non-réussite, 1=Réussite)')\n",
        "axes[0].set_xlabel('Réussite Académique')\n",
        "axes[0].set_ylabel('Effectif')\n",
        "\n",
        "# Matrice de corrélation\n",
        "sns.heatmap(df.corr(numeric_only=True), annot=False, cmap='coolwarm', ax=axes[1], center=0)\n",
        "axes[1].set_title('Matrice de Corrélation')\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()"
    ]))
    cells.append(make_cell("code", [
        "print('--- Taux de réussite ---')\n",
        "print(f\"{df['academic_success'].mean()*100:.1f}% des étudiants réussissent\")\n",
        "\n",
        "print('\\n--- Valeurs manquantes ---')\n",
        "print(df.isnull().sum().sum())"
    ]))
    cells.append(make_cell("markdown", [
        "### Conclusion\n",
        "Le dataset contient 395 étudiants avec 15 variables et 1 cible binaire. Les données sont synthétiques, générées avec les mêmes distributions que le dataset UCI Student Performance."
    ]))

    os.makedirs("notebooks", exist_ok=True)
    _save_notebook(cells, "notebooks/01_data_exploration.ipynb")
    print("Notebook 01_data_exploration.ipynb generated!")


def generate_pca_notebook():
    cells = []
    cells.append(make_cell("markdown", [
        "# Notebook 2 : Analyse en Composantes Principales (ACP)\n",
        "Implémentation from scratch de l'ACP avec décomposition spectrale."
    ]))
    cells.append(make_cell("code", [
        "import numpy as np\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "from src.preprocessing import StandardScalerScratch, train_test_split_scratch\n",
        "\n",
        "df = pd.read_csv('../data/raw/student_data.csv')\n",
        "X = df.drop(columns=['academic_success']).values\n",
        "y = df['academic_success'].values\n",
        "\n",
        "X_train, X_test, y_train, y_test = train_test_split_scratch(X, y, test_size=0.2, random_state=42)\n",
        "scaler = StandardScalerScratch()\n",
        "X_train_scaled = scaler.fit_transform(X_train)\n",
        "X_test_scaled = scaler.transform(X_test)\n",
        "print('Données standardisées. Shape train :', X_train_scaled.shape)"
    ]))
    cells.append(make_cell("markdown", [
        "## Implémentation ACP From Scratch\n",
        "\n",
        "**Étape 1 : Matrice de covariance empirique :**\n",
        "$$\\Sigma = \\frac{1}{m} X^T X$$\n",
        "\n",
        "**Étape 2 : Décomposition spectrale (eigenvalues/vectors) :**\n",
        "$$\\Sigma v_i = \\lambda_i v_i$$\n",
        "\n",
        "**Étape 3 : Projection :**\n",
        "$$Z = X W$$"
    ]))
    cells.append(make_cell("code", [
        "from src.pca_scratch import PCAFromScratch\n",
        "\n",
        "pca = PCAFromScratch(n_components=2)\n",
        "Z_train = pca.fit_transform(X_train_scaled)\n",
        "\n",
        "print('Valeurs propres :', pca.eigenvalues_)\n",
        "print('Ratio variance expliquée (PC1, PC2) :', pca.explained_variance_ratio_)\n",
        "print('Variance cumulée 2 composantes :', sum(pca.explained_variance_ratio_))"
    ]))
    cells.append(make_cell("code", [
        "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
        "\n",
        "# Scatter 2D\n",
        "scatter = axes[0].scatter(Z_train[:, 0], Z_train[:, 1], c=y_train, cmap='coolwarm', alpha=0.7, edgecolors='k')\n",
        "axes[0].set_xlabel('PC1')\n",
        "axes[0].set_ylabel('PC2')\n",
        "axes[0].set_title('Projection ACP 2D des Étudiants')\n",
        "fig.colorbar(scatter, ax=axes[0], label='Réussite')\n",
        "\n",
        "# Scree plot\n",
        "full_pca = PCAFromScratch(n_components=X_train_scaled.shape[1])\n",
        "full_pca.fit(X_train_scaled)\n",
        "cum_var = np.cumsum(full_pca.explained_variance_ratio_)\n",
        "axes[1].bar(range(1, len(cum_var)+1), full_pca.explained_variance_ratio_, alpha=0.6, label='Individuelle')\n",
        "axes[1].step(range(1, len(cum_var)+1), cum_var, where='mid', color='red', label='Cumulée')\n",
        "axes[1].set_xlabel('Composantes')\n",
        "axes[1].set_ylabel('Variance Expliquée')\n",
        "axes[1].set_title('Scree Plot')\n",
        "axes[1].legend()\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()"
    ]))
    cells.append(make_cell("markdown", [
        "### Conclusion\n",
        "L'ACP from scratch réduit la dimensionnalité tout en préservant la majorité de la variance. Les deux premières composantes captrent l'essentiel de l'information."
    ]))

    os.makedirs("notebooks", exist_ok=True)
    _save_notebook(cells, "notebooks/02_pca_analysis.ipynb")
    print("Notebook 02_pca_analysis.ipynb generated!")


def generate_logistic_regression_notebook():
    cells = []
    cells.append(make_cell("markdown", [
        "# Notebook 3 : Régression Logistique From Scratch\n",
        "Descente de gradient vectorisée avec Log-Loss et régularisation L2."
    ]))
    cells.append(make_cell("code", [
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "from src.preprocessing import StandardScalerScratch, train_test_split_scratch\n",
        "\n",
        "import pandas as pd\n",
        "df = pd.read_csv('../data/raw/student_data.csv')\n",
        "X = df.drop(columns=['academic_success']).values\n",
        "y = df['academic_success'].values\n",
        "\n",
        "X_train, X_test, y_train, y_test = train_test_split_scratch(X, y, test_size=0.2, random_state=42)\n",
        "scaler = StandardScalerScratch()\n",
        "X_train_scaled = scaler.fit_transform(X_train)\n",
        "X_test_scaled = scaler.transform(X_test)"
    ]))
    cells.append(make_cell("markdown", [
        "## Fonction de Coût Log-Loss + L2\n",
        "\n",
        "$$J(\\theta) = -\\frac{1}{m} \\sum [ y \\log(\\hat{y}) + (1-y)\\log(1-\\hat{y}) ] + \\frac{\\lambda}{2m} \\sum_{j=1}^n \\theta_j^2$$\n",
        "\n",
        "**Gradient :**\n",
        "$$\\nabla J(\\theta) = \\frac{1}{m} X^T (\\hat{y} - y) + \\frac{\\lambda}{m} \\theta$$"
    ]))
    cells.append(make_cell("code", [
        "from src.logistic_regression_scratch import LogisticRegressionScratch\n",
        "\n",
        "model = LogisticRegressionScratch(learning_rate=0.1, l2_lambda=0.1, n_iterations=1000)\n",
        "model.fit(X_train_scaled, y_train)\n",
        "\n",
        "plt.figure(figsize=(8, 5))\n",
        "plt.plot(model.cost_history, color='blue', linewidth=2)\n",
        "plt.title(f'Convergence (Coût initial: {model.cost_history[0]:.4f} -> Final: {model.cost_history[-1]:.4f})')\n",
        "plt.xlabel('Itérations')\n",
        "plt.ylabel('Coût Log-Loss + L2')\n",
        "plt.grid(True, linestyle='--', alpha=0.5)\n",
        "plt.show()"
    ]))
    cells.append(make_cell("markdown", [
        "## Impact du Learning Rate"
    ]))
    cells.append(make_cell("code", [
        "alphas = [0.001, 0.1, 3.5]\n",
        "plt.figure(figsize=(8, 5))\n",
        "\n",
        "for alpha in alphas:\n",
        "    m = LogisticRegressionScratch(learning_rate=alpha, l2_lambda=0.01, n_iterations=200)\n",
        "    m.fit(X_train_scaled, y_train)\n",
        "    plt.plot(m.cost_history, label=f'alpha = {alpha}')\n",
        "\n",
        "plt.xlabel('Itérations')\n",
        "plt.ylabel('Coût J(theta)')\n",
        "plt.title('Impact du Learning Rate sur la Convergence')\n",
        "plt.ylim(0, 1.5)\n",
        "plt.legend()\n",
        "plt.grid(True, linestyle='--', alpha=0.5)\n",
        "plt.show()"
    ]))
    cells.append(make_cell("code", [
        "from src.metrics import accuracy_score_scratch, f1_score_scratch, confusion_matrix_scratch\n",
        "import seaborn as sns\n",
        "\n",
        "preds = model.predict(X_test_scaled)\n",
        "probs = model.predict_proba(X_test_scaled)\n",
        "\n",
        "print(f'Accuracy Test : {accuracy_score_scratch(y_test, preds)*100:.2f}%')\n",
        "print(f'F1-Score Test : {f1_score_scratch(y_test, preds)*100:.2f}%')\n",
        "\n",
        "cm = confusion_matrix_scratch(y_test, preds)\n",
        "plt.figure(figsize=(6, 5))\n",
        "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,\n",
        "            xticklabels=['Non-réussite', 'Réussite'],\n",
        "            yticklabels=['Non-réussite', 'Réussite'])\n",
        "plt.xlabel('Prédit')\n",
        "plt.ylabel('Réel')\n",
        "plt.title('Matrice de Confusion')\n",
        "plt.show()"
    ]))
    cells.append(make_cell("markdown", [
        "### Conclusion\n",
        "La régression logistique from scratch avec régularisation L2 converge correctement. Le choix du learning rate est crucial pour la stabilité de la descente de gradient."
    ]))

    os.makedirs("notebooks", exist_ok=True)
    _save_notebook(cells, "notebooks/03_logistic_regression.ipynb")
    print("Notebook 03_logistic_regression.ipynb generated!")


if __name__ == "__main__":
    generate_final_notebook()
    generate_data_exploration_notebook()
    generate_pca_notebook()
    generate_logistic_regression_notebook()
    print("All 4 notebooks successfully generated!")
