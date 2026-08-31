# Student Success ML From Scratch

> **Prédiction de la réussite académique des étudiants par Analyse en Composantes Principales (ACP) et Régression Logistique avec régularisation L2 : implémentation et analyse mathématique vectorisée from scratch avec NumPy.**

---

## Contextualisation & Objectifs Pédagogiques

Ce projet individuel universitaire de **Mathématiques Appliquées et Machine Learning** a pour but de comprendre les fondements théoriques et matriciels des algorithmes d'apprentissage automatique et de les implémenter **intégralement from scratch en Python avec NumPy** (sans aucune boucle sur les observations).

### Compétences Démontrées :
1. **Algèbre Linéaire & ACP :** Centrage-réduction, calcul de la matrice de covariance empirique $\Sigma = \frac{1}{m} X^T X$, décomposition en valeurs et vecteurs propres ($\Sigma v_i = \lambda_i v_i$), maximisation de la variance projetée via le Lagrangien, et projection $Z = XW$.
2. **Calcul Différentiel & Optimisation :** Activation sigmoïde numérique stable, Log-Loss avec régularisation L2 (Ridge), gradient analytique matriciel $\nabla J(\theta) = \frac{1}{m} X^T (\hat{y} - y) + \frac{\lambda}{m} \theta$, et descente de gradient vectorisée.
3. **Analyse Expérimentale :** Effet du pas d'apprentissage ($\alpha$), impact de la standardisation des variables sur le conditionnement de la surface de coût et la convergence.
4. **Validation Externe :** Script de comparaison rigoureuse avec Scikit-Learn (concordance 100% et précision à $10^{-5}$ près).

---

## Structure du Repository

```text
student-success-ml-from-scratch/
├── README.md                          # Documentation générale du projet
├── requirements.txt                    # Dépendances du projet
├── .gitignore                          # Exclusions Git
├── data/
│   ├── raw/
│   │   └── student_data.csv            # Dataset brut UCI Student Performance (395 étudiants)
│   └── processed/
│       └── dataset.npz                 # Splits train/test et variables standardisées
├── src/
│   ├── __init__.py
│   ├── data_loader.py                  # Chargement et binarisation du dataset académique
│   ├── preprocessing.py               # StandardScalerScratch & train_test_split_scratch
│   ├── pca_scratch.py                  # PCAFromScratch (décomposition spectrale)
│   ├── logistic_regression_scratch.py  # LogisticRegressionScratch (Log-Loss L2 & Gradient)
│   ├── metrics.py                      # Accuracy, Precision, Recall, F1, Confusion, ROC-AUC
│   ├── eda.py                          # Analyse exploratoire des données (EDA)
│   ├── experiments.py                  # Expériences (Learning Rate & Standardisation)
│   └── visualization.py                # Utilitaires de graphiques
├── tests/
│   ├── __init__.py
│   ├── test_preprocessing.py           # Tests unitaires du prétraitement
│   ├── test_pca.py                     # Tests unitaires de l'ACP
│   ├── test_logistic_regression.py     # Tests unitaires de la régression logistique
│   └── compare_with_sklearn.py         # Script de comparaison avec Scikit-Learn
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_pca_analysis.ipynb
│   ├── 03_logistic_regression.ipynb
│   └── final_project.ipynb             # Notebook scientifique principal (21 sections)
├── app/
│   ├── app.py                          # Application Streamlit interactive
│   └── components/
├── results/
│   ├── figures/                        # Graphiques générés (Scree plot, 2D PCA, ROC, Loss)
│   └── metrics/                        # Métriques CSV (EDA, Evaluation, Sklearn comparison)
├── docs/
│   ├── requirements.md                 # Cahier des charges exhaustif & checklist
│   ├── dataset_selection.md            # Analyse comparative et justification du dataset
│   ├── pca_mathematics.md              # Démonstration mathématique de l'ACP
│   └── final_audit.md                  # Grille d'audit et de conformité finale
├── scripts/
│   ├── build_notebooks.py              # Générateur des notebooks Jupyter
│   └── generate_pdf_report.py          # Générateur du rapport scientifique PDF (17 pages)
└── report/
    └── rapport_projet.pdf              # Rapport scientifique PDF complet (17 pages)
```

---

## Installation & Exécution

### 1. Cloner et Installer les Dépendances
```bash
git clone https://github.com/steveshanny/student-success-ml-from-scratch.git
cd student-success-ml-from-scratch

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Exécuter la Suite de Tests Unitaires & la Comparaison avec Sklearn
```bash
# Tests du prétraitement, ACP et Régression Logistique
python -c "import tests.test_preprocessing; tests.test_preprocessing.test_standard_scaler(); tests.test_preprocessing.test_train_test_split(); print('Preprocessing PASSED!')"
python -c "import tests.test_pca; tests.test_pca.test_pca_scratch(); print('PCA PASSED!')"
python -c "import tests.test_logistic_regression; tests.test_logistic_regression.test_sigmoid(); tests.test_logistic_regression.test_logistic_regression_convergence(); print('Logistic Regression PASSED!')"

# Script de comparaison automatique avec Scikit-Learn
python -m tests.compare_with_sklearn
```

### 3. Lancer l'Application Web Streamlit
```bash
streamlit run app/app.py
```
ou 
```bash
python -m streamlit run app/app.py
```

---

## Résultats Clés de Performance

| Modèle | Accuracy Test | F1-Score Test | Log-Loss Final | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: |
| **LogisticRegressionScratch (NumPy)** | **87.34%** | **87.80%** | **0.3367** | **0.923** |
| **Scikit-Learn (Reference)** | **87.34%** | **87.80%** | **0.3367** | **0.923** |

*Taux de concordance des prédictions entre l'implémentation From Scratch et Scikit-Learn : **100.00%**.*
