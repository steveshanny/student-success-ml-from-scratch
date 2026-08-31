# Cahier des Charges Complet — Projet de Mathématiques Appliquées / Machine Learning

**Titre académique :** Prédiction de la réussite académique des étudiants par Analyse en Composantes Principales et Régression Logistique : implémentation et analyse mathématique from scratch  
**Nom du repository :** `student-success-ml-from-scratch`

---

## 1. Contexte & Objectifs Pédagogiques

### 1.1 Objectif Général
Comprendre les fondements mathématiques des algorithmes de Machine Learning et développer le cœur de ces algorithmes **from scratch** avec **NumPy**, sans dépendre des bibliothèques haut niveau (Scikit-Learn) pour l'implémentation principale.

### 1.2 Compétences Pédagogiques à Démontrer
- **Mathématiques :** Algèbre linéaire (matrice de covariance, valeurs/vecteurs propres, projection ACP), Calcul différentiel & Optimisation (fonctions de coût, gradient, descente de gradient, convergence, régularisation L2).
- **Programmation :** Python propre, modulaire, documenté, entièrement vectorisé avec NumPy (interdiction des boucles `for` sur les observations), avec suite de tests unitaires et intégrés.
- **Machine Learning :** Pipeline end-to-end : Nettoyage → Standardisation → ACP → Régression Logistique → Évaluation → Analyses expérimentales.

---

## 2. Définition du Problème & Contraintes

- **Domaine :** Prédiction de la réussite académique des étudiants.
- **Problématique :** *Dans quelle mesure les caractéristiques académiques et personnelles d'un étudiant permettent-elles de prédire sa réussite académique ?*
- **Variable cible :** Classification binaire ($y \in \{0, 1\}$) strictly ancrée dans le contexte académique ($0 =$ non-réussite académique, $1 =$ réussite académique).
- **Contraintes matérielles & de sobriété :** 
  - Exécution sur matériel léger (CPU basique).
  - Données tabulaires (quelques centaines/milliers de lignes, quelques variables).
  - Bibliothèques autorisées : `numpy`, `pandas`, `matplotlib`, `seaborn`, `streamlit`, `scipy` (pour validation).
  - Interdiction stricte : GPU, Deep Learning (TensorFlow, PyTorch, réseaux de neurones), modèles lourds.

---

## 3. Dataset Candidate Analysis

- Dataset réel, public, lié aux performances académiques.
- Analyse comparative obligatoire de plusieurs candidats selon :
  - Taille (lignes, colonnes), types de variables (numériques/catégorielles), valeurs manquantes.
  - Adéquation pour classification binaire, PCA et Régression Logistique.
  - Justification claire de la binarisation de la variable cible.

---

## 4. Spécifications Algorithmiques & Mathématiques

### 4.1 Phase 1 : ACP (PCA) From Scratch
1. **Standardisation :** $X_{standard} = \frac{X - \mu}{\sigma}$ (centrage-réduction).
2. **Matrice de Covariance :** $\Sigma = \frac{1}{m} X^T X$.
3. **Décomposition Spectrale :** Calcul des valeurs propres $\lambda_i$ et vecteurs propres $v_i$, triés par ordre décroissant.
4. **Projection :** Projection des données centrées-réduites sur les $k$ premières composantes : $Z = XW$.
5. **Variance Expliquée :** Ratio $\frac{\lambda_i}{\sum \lambda_j}$ et variance cumulée.
6. **Preuve Mathématique :** Démontrer pourquoi les vecteurs propres de la matrice de covariance correspondent aux directions de variance maximale projetée.
7. **Classe `PCAFromScratch` :** Implémenter les méthodes `fit()`, `transform()`, `fit_transform()`, `explained_variance_ratio()`.

### 4.2 Phase 2 : Régression Logistique & Optimisation From Scratch
1. **Fonction Sigmoïde :** $\sigma(z) = \frac{1}{1 + e^{-z}}$ avec protection contre le sous/sur-débit numérique (`np.clip`).
2. **Hypothèse & Prédiction :** $\hat{y} = \sigma(X\theta)$, classe prédite par seuillage ($\hat{y} \ge 0.5 \implies 1$).
3. **Fonction de Coût (Log-Loss + L2) :**
   $$J(\theta) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)}\log(\hat{y}^{(i)}) + (1 - y^{(i)})\log(1 - \hat{y}^{(i)}) \right] + \frac{\lambda}{2m} \sum_{j=1}^n \theta_j^2$$
   - Protection numérique contre $\log(0)$ (ex: $\epsilon = 10^{-15}$).
   - Exclusion (ou gestion documentée) du biais $\theta_0$ de la régularisation L2.
4. **Gradient Analytique Vectorisé :**
   $$\nabla J(\theta) = \frac{1}{m} X^T (\hat{y} - y) + \frac{\lambda}{m} \theta$$
   - Dérivation mathématique explicite incluse dans le notebook/rapport.
5. **Descente de Gradient :**
   $$\theta := \theta - \alpha \nabla J(\theta)$$
   - Enregistrement de l'historique des coûts pour analyse de convergence.
6. **Vectorisation Stricte :** Aucune boucle `for` sur les observations du dataset. Boucle autorisée uniquement pour l'itération des étapes d'optimisation.
7. **Classe `LogisticRegressionScratch` :** Implémenter `fit()`, `predict_proba()`, `predict()`, `cost_function()`, `gradient()`.

---

## 5. Expérimentations Pédagogiques & Analyse

1. **Courbe d'Apprentissage :** Graphique $J(\theta)$ en fonction des itérations pour valider la convergence.
2. **Analyse du Pas d'Apprentissage ($\alpha$) :**
   - Comparaison des régimes : $\alpha$ trop faible, $\alpha$ optimal, $\alpha$ trop élevé.
   - Explication mathématique des divergences/oscillations lorsque $\alpha$ est trop grand.
3. **Analyse de la Standardisation :**
   - Étude comparative : Données non-standardisées vs. Données standardisées.
   - Analyse de l'impact sur la forme de la fonction de coût, le conditionnement et la vitesse de convergence du gradient.
4. **Évaluation Complète :**
   - Accuracy, Précision, Rappel, F1-Score, Matrice de confusion, Courbe ROC-AUC.
   - Interprétation métier/académique détaillée des faux positifs et faux négatifs.
5. **Validation Externe (Scikit-Learn) :**
   - Script de test dédié `tests/compare_with_sklearn.py`.
   - Comparaison des poids $\theta$, probabilités, prédictions et métriques avec `sklearn.linear_model.LogisticRegression` et `sklearn.decomposition.PCA`.

---

## 6. Structure du Repository

```text
student-success-ml-from-scratch/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── pca_scratch.py
│   ├── logistic_regression_scratch.py
│   ├── metrics.py
│   └── visualization.py
├── tests/
│   ├── test_preprocessing.py
│   ├── test_pca.py
│   ├── test_logistic_regression.py
│   └── compare_with_sklearn.py
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_pca_analysis.ipynb
│   ├── 03_logistic_regression.ipynb
│   └── final_project.ipynb
├── app/
│   ├── app.py
│   └── components/
├── results/
│   ├── figures/
│   └── metrics/
├── docs/
│   ├── requirements.md
│   ├── dataset_selection.md
│   ├── pca_mathematics.md
│   └── final_audit.md
└── report/
    └── rapport_projet.pdf
```

---

## 7. Livrables Attendus

1. **Code Python & Suite de Tests :** Implémentations vectorisées, documentées et entièrement testées.
2. **Notebook Jupyter Principal (`notebooks/final_project.ipynb`) :** Démonstration scientifique combinant Formule → Signification → Dérivation → Algorithme → Code NumPy → Test → Résultat → Interprétation.
3. **Script de Comparaison (`tests/compare_with_sklearn.py`) :** Validation rigoureuse contre Scikit-Learn.
4. **Application Web Streamlit (`app/app.py`) :** Interface interactive avec Dashboard, Dataset, ACP 2D, Entraînement, Évaluation et Simulateur de prédiction individuelle avec clause de non-responsabilité.
5. **Rapport Scientifique PDF (`report/rapport_projet.pdf`) :** Document de $\ge 15$ pages structuré en 17 chapitres (du contexte aux biais et perspectives).
6. **Documentation & Audit Final (`docs/final_audit.md`) :** Grille de contrôle de toutes les exigences.

---

## 8. Checklist de Conformité & Audit

| Exigence | Validé |
| :--- | :---: |
| Dataset réel & public académique | 🟩 |
| Target binaire académique (0/1) bien justifiée | 🟩 |
| Standardisation des features from scratch | 🟩 |
| Calcul de la matrice de covariance $X^T X / m$ | 🟩 |
| Calcul des valeurs et vecteurs propres | 🟩 |
| Classe `PCAFromScratch` & projection 2D | 🟩 |
| Ratio & courbe de variance expliquée cumulée | 🟩 |
| Sigmoïde numérique stable | 🟩 |
| Log-Loss avec protection $\log(0)$ | 🟩 |
| Régularisation L2 (excluant $\theta_0$) | 🟩 |
| Gradient analytique matriciel de la Log-Loss L2 | 🟩 |
| Descente de gradient vectorisée | 🟩 |
| Strictement aucune boucle `for` sur les données | 🟩 |
| Courbe d'apprentissage et de convergence | 🟩 |
| Expérience & analyse théorique du learning rate ($\alpha$) | 🟩 |
| Expérience & analyse de l'impact de la standardisation | 🟩 |
| Métriques (Accuracy, Précision, Rappel, F1, Confusion, ROC-AUC) | 🟩 |
| Verification & comparaison automatique avec Scikit-Learn | 🟩 |
| Notebook Jupyter scientifique complet | 🟩 |
| Application Streamlit interactive | 🟩 |
| Rapport PDF $\ge 15$ pages | 🟩 |
| Git workflow rigoureux (Conventional Commits & tests validés) | 🟩 |

---

## 9. Workflow et Discipline de Développement

- Développement par étapes atomiques et progressives.
- Validation stricte des tests avant chaque commit Git.
- Format des commits : Conventional Commits (`chore:`, `docs:`, `feat:`, `test:`, `fix:`, `refactor:`).
- Interdiction d'inventer des métriques ou des résultats artificiels.
