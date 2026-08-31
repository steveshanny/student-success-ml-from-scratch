# Fondements Mathématiques de l'Analyse en Composantes Principales (ACP)

## 1. Formulation Propre du Problème

Soit $X \in \mathbb{R}^{m \times n}$ une matrice de données comportant $m$ observations et $n$ variables, préalablement centrée-réduite ($\mu = 0, \sigma = 1$).

La matrice de covariance empirique est définie par :
$$\Sigma = \frac{1}{m} X^T X \in \mathbb{R}^{n \times n}$$

L'objectif de l'ACP est de trouver un vecteur d'orientation $\|w\| = 1$ ($w^T w = 1$) tel que la projection des données sur $w$, notée $z = X w \in \mathbb{R}^m$, possède une **variance maximale**.

---

## 2. Démontrer la Maximisation de la Variance Projetée

La variance de la projection $z$ s'écrit :
$$\text{Var}(z) = \frac{1}{m} z^T z = \frac{1}{m} (Xw)^T (Xw) = \frac{1}{m} w^T X^T X w = w^T \left( \frac{1}{m} X^T X \right) w = w^T \Sigma w$$

Nous cherchons donc le vecteur $w$ qui résout le problème d'optimisation sous contrainte :
$$\max_{w} w^T \Sigma w \quad \text{sujet à} \quad w^T w = 1$$

---

## 3. Utilisation des Multiplicateurs de Lagrange

Définissons le Lagrangien :
$$\mathcal{L}(w, \lambda) = w^T \Sigma w - \lambda (w^T w - 1)$$

Prenons la dérivée partielle par rapport à $w$ et annulons-la :
$$\frac{\partial \mathcal{L}}{\partial w} = 2 \Sigma w - 2 \lambda w = 0 \implies \Sigma w = \lambda w$$

### Conclusion Majeure :
Cette équation est exactement la définition de l'**équation aux valeurs propres** de la matrice de covariance $\Sigma$.
- $w$ doit être un **vecteur propre** de $\Sigma$.
- $\lambda$ est la **valeur propre** associée.

---

## 4. Lien entre Valeur Propre et Variance Maximisée

Injectons $\Sigma w = \lambda w$ dans la formule de la variance projetée :
$$\text{Var}(z) = w^T \Sigma w = w^T (\lambda w) = \lambda (w^T w) = \lambda$$

Ainsi :
1. La variance des données projetées sur la direction du vecteur propre $w$ est **exactement égale à la valeur propre $\lambda$**.
2. Pour maximiser la variance projetée, il faut choisir le vecteur propre $w_1$ associé à la **plus grande valeur propre $\lambda_1$**.
3. Les vecteurs propres orthogonaux $w_2, w_3, \dots, w_k$ correspondent aux directions orthogonales successives de variance maximale restante.
