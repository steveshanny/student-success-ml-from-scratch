# Analyse Comparative et Sélection du Dataset

## 1. Contextualisation
Pour répondre aux exigences du projet de Mathématiques Appliquées / Machine Learning, la variable cible doit prédire la **réussite académique des étudiants** sous forme d'une classification binaire :
- `1` : Réussite académique (obtention du diplôme ou moyenne suffisante $\ge 10/20$).
- `0` : Non-réussite académique (échec ou abandon).

---

## 2. Comparaison des Datasets Candidats

| Critère | Candidat A : UCI Student Performance (Math) | Candidat B : UCI Higher Ed Dropout & Success | Candidat C : Synthetic Academic Toy Dataset |
| :--- | :--- | :--- | :--- |
| **Source** | UCI Machine Learning Repository (Cortez & Silva, 2008) | UCI ML Repository (Real Polytech Portugal) | Généré synthétiquement |
| **Nombre d'observations** | 395 étudiants | 4 424 étudiants | 500 étudiants |
| **Nombre de variables** | 33 attributs | 36 attributs | 10 attributs |
| **Types de variables** | Numériques (notes, absences, âge) & Catégorielles (éducation parents, soutien) | Numériques, démographiques & académiques | Numériques uniquement |
| **Valeurs manquantes** | 0 (Données propres) | 0 (Données propres) | 0 |
| **Cible originale** | Note finale $G3 \in [0, 20]$ | Catégorielle : `Graduate`, `Dropout`, `Enrolled` | Binaire (0/1) |
| **Transformation binaire** | $G3 \ge 10 \implies 1$, $G3 < 10 \implies 0$ | `Graduate` $\implies 1$, `Dropout` $\implies 0$ | Directe |
| **Facilité PCA / RegLog** | Excellent (forte corrélation inter-notes) | Bon (forte dimensionnalité) | Trivial |
| **Pertinence Académique** | Maximale (facteurs d'étude directes) | Élevée | Faible (artificiel) |
| **Coût de calcul CPU** | Très faible (< 0.1s) | Faible (< 0.5s) | Instantané |

---

## 3. Dataset Retenu : UCI Student Performance (Math & Académique)

Le dataset retenu est **UCI Student Performance**. 

### Raisons du choix :
1. **Origine réelle et publique :** Collecté dans des établissements scolaires secondaires et universitaires.
2. **Dimension idéale pour l'analyse matricielle :** 395 étudiants et 15 variables clés préservées après encodage.
3. **Parfaite adéquation avec l'ACP :** Les caractéristiques académiques (notes intermédiaires $G1, G2$, temps d'étude, absences, échecs passés) présentent des corrélations linéaires fortes se prêtant à la réduction de dimension spectrale.
4. **Binarisation scientifiquement justifiée :** En médecine et en éducation, le seuil de $10/20$ définit la validation de l'année académique.

---

## 4. Dictionnaire des Variables Sélectionnées

| Variable | Type | Description |
| :--- | :--- | :--- |
| `age` | Numérique | Âge de l'étudiant (15 à 22 ans) |
| `Medu` | Numérique | Niveau d'éducation de la mère (0 à 4) |
| `Fedu` | Numérique | Niveau d'éducation du père (0 à 4) |
| `traveltime` | Numérique | Temps de trajet domicile-école (1 à 4) |
| `studytime` | Numérique | Temps d'étude hebdomadaire (1 à 4) |
| `failures` | Numérique | Nombre d'échecs académiques passés (0 à 4) |
| `famrel` | Numérique | Qualité des relations familiales (1 à 5) |
| `freetime` | Numérique | Temps libre après les cours (1 à 5) |
| `goout` | Numérique | Sorties entre amis (1 à 5) |
| `Dalc` | Numérique | Consommation d'alcool en semaine (1 à 5) |
| `Walc` | Numérique | Consommation d'alcool le week-end (1 à 5) |
| `health` | Numérique | État de santé actuel (1 à 5) |
| `absences` | Numérique | Nombre d'absences scolaires (0 à 93) |
| `G1` | Numérique | Note du premier trimestre ($0 \le G1 \le 20$) |
| `G2` | Numérique | Note du deuxième trimestre ($0 \le G2 \le 20$) |
| **`academic_success`** | **Binaire (Cible)** | **$1$ si $G3 \ge 10$, $0$ sinon** |
