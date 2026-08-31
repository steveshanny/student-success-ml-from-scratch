# Student Success ML From Scratch

> **Prédiction de la réussite académique des étudiants par Analyse en Composantes Principales (ACP) et Régression Logistique : implémentation et analyse mathématique from scratch.**

## 📌 Présentation du Projet
Ce projet universitaire de Mathématiques Appliquées et Machine Learning a pour objectif de comprendre la théorie sous-jacente des algorithmes d'Analyse en Composantes Principales (ACP) et de Régression Logistique (avec régularisation L2), et de les implémenter **exclusiverment from scratch en NumPy** (vectorisation matricielle complète).

## 🚀 Fonctionnalités Principales
- **Pipeline From Scratch :** Standardisation, Matrice de Covariance, Valeurs/Vecteurs Propres, Projection ACP, Sigmoïde, Log-Loss avec régularisation L2, Gradient matriciel et Descente de Gradient.
- **Démonstration Mathématique :** Justification de l'ACP (maximisation de variance) et dérivation du gradient de la Log-Loss.
- **Analyses Expérimentales :** Impact de la standardisation et influence du learning rate $\alpha$ sur la convergence.
- **Validation Externe :** Script de comparaison automatique avec Scikit-Learn.
- **Interface Streamlit :** Application web interactive pour l'exploration, l'entraînement et la prédiction de la réussite académique.

## 📁 Structure du Repository
```text
student-success-ml-from-scratch/
├── data/              # Données brutes et nettoyées
├── src/               # Code source Python (ACP, RegLog, Preprocessing, Métriques)
├── tests/             # Tests unitaires et script de comparaison avec Sklearn
├── notebooks/         # Notebooks Jupyter de démonstration scientifique
├── app/               # Application Streamlit
├── results/           # Graphiques et métriques exportés
├── docs/              # Cahier des charges, analyses théoriques et audit final
└── report/            # Rapport scientifique PDF (≥ 15 pages)
```

## 🛠️ Installation & Execution
```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancer la suite de tests
pytest

# Comparaison avec Scikit-Learn
python tests/compare_with_sklearn.py

# Lancer l'application Streamlit
streamlit run app/app.py
```
