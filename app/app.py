"""
Streamlit Web Application — Student Success ML From Scratch.
PCA & Logistic Regression implemented from scratch with NumPy.
"""

import os
import sys
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.preprocessing import StandardScalerScratch
from src.pca_scratch import PCAFromScratch
from src.logistic_regression_scratch import LogisticRegressionScratch
from src.metrics import (
    accuracy_score_scratch,
    precision_score_scratch,
    recall_score_scratch,
    f1_score_scratch,
    confusion_matrix_scratch,
    roc_curve_scratch,
)

# Configuration
st.set_page_config(
    page_title="Student Success ML From Scratch",
    layout="wide",
)

st.title(" Prédiction de la Réussite Académique des Étudiants")
st.markdown(
    "**Analyse en Composantes Principales (ACP) & Régression Logistique avec régularisation L2 — Implémentation From Scratch en NumPy**"
)
st.caption("Données synthétiques inspirées du dataset UCI Student Performance — Projet pédagogique à visée d'apprentissage.")

# Data paths
RAW_DATA_PATH = "data/raw/student_data.csv"
PROCESSED_DATA_PATH = "data/processed/dataset.npz"

if not os.path.exists(RAW_DATA_PATH):
    with st.spinner("Génération du dataset..."):
        from src.data_loader import generate_uci_student_dataset
        generate_uci_student_dataset()

if not os.path.exists(PROCESSED_DATA_PATH):
    with st.spinner("Prétraitement des données..."):
        from src.preprocessing import prepare_and_save_data
        prepare_and_save_data()

df_raw = pd.read_csv(RAW_DATA_PATH)
data_processed = np.load(PROCESSED_DATA_PATH, allow_pickle=True)
X_train_scaled = data_processed["X_train_scaled"]
X_test_scaled = data_processed["X_test_scaled"]
y_train = data_processed["y_train"]
y_test = data_processed["y_test"]
feature_names = data_processed["feature_names"]


@st.cache_resource
def get_default_model():
    model = LogisticRegressionScratch(learning_rate=0.1, l2_lambda=0.1, n_iterations=1000)
    model.fit(X_train_scaled, y_train)
    return model


@st.cache_resource
def get_pca_model():
    pca = PCAFromScratch(n_components=2)
    pca.fit(X_train_scaled)
    return pca


@st.cache_resource
def get_full_pca_model():
    pca = PCAFromScratch(n_components=X_train_scaled.shape[1])
    pca.fit(X_train_scaled)
    return pca


@st.cache_resource
def get_scaler():
    scaler = StandardScalerScratch()
    scaler.fit(df_raw.drop(columns=["academic_success"]).values)
    return scaler


@st.cache_resource
def get_trained_model_on_all_data():
    scaler = get_scaler()
    X_raw_all = df_raw.drop(columns=["academic_success"]).values
    y_raw_all = df_raw["academic_success"].values
    X_scaled_all = scaler.transform(X_raw_all)
    model = LogisticRegressionScratch(learning_rate=0.1, l2_lambda=0.1, n_iterations=1000)
    model.fit(X_scaled_all, y_raw_all)
    return model, X_scaled_all


# Sidebar Navigation
st.sidebar.title("🎓 Student Success ML")
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Accéder aux sections :",
    ["Dashboard", "Dataset", "ACP (PCA)", "Entraînement", "Évaluation", "Prédiction Individuelle"],
)

# 1. DASHBOARD
if menu == "Dashboard":
    st.header("Tableau de Bord Général")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Étudiants Total", f"{len(df_raw)}")
    col2.metric("Variables (Features)", f"{len(feature_names)}")
    col3.metric("Taux de Réussite", f"{df_raw['academic_success'].mean() * 100:.1f}%")

    model_default = get_default_model()
    preds_test = model_default.predict(X_test_scaled)

    acc = accuracy_score_scratch(y_test, preds_test)
    f1 = f1_score_scratch(y_test, preds_test)

    col4.metric("Accuracy (Test)", f"{acc * 100:.1f}%")
    col5.metric("F1-Score (Test)", f"{f1 * 100:.1f}%")

    st.markdown("---")
    st.subheader("Objectif du Projet")
    st.info(
        "Ce projet démontre l'implémentation vectorisée from scratch des algorithmes d'Analyse en Composantes Principales (ACP) "
        "et de Régression Logistique (avec régularisation L2 et descente de gradient) en NumPy, appliqués à la prédiction de la réussite académique."
    )
    st.caption("Les données sont générées synthétiquement. Le but est de comprendre les mécanismes internes des algorithmes ML sans utiliser de bibliothèque ML prête-à-l'emploi.")

# 2. DATASET
elif menu == "Dataset":
    st.header("Exploration des Données Académiques")
    st.subheader("Aperçu du Dataset (synthétique, inspiré UCI Student Performance)")
    st.dataframe(df_raw.head(10), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Statistiques Descriptives")
        st.dataframe(df_raw.describe().T[["mean", "std", "min", "50%", "max"]], use_container_width=True)

    with col2:
        st.subheader("Distribution de la Cible (Réussite Académique)")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(x="academic_success", data=df_raw, palette="viridis", ax=ax)
        ax.set_title("Distribution de la Cible (0 = Non-Réussite, 1 = Réussite)")
        ax.set_xlabel("Réussite Académique (G3 >= 10)")
        ax.set_ylabel("Effectif")
        st.pyplot(fig)

# 3. ACP (PCA)
elif menu == "ACP (PCA)":
    st.header("Analyse en Composantes Principales (ACP) From Scratch")

    with st.spinner("Calcul de l'ACP..."):
        pca = get_pca_model()
        Z = pca.transform(X_train_scaled)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Projection 2D (PC1 vs PC2)")
        fig, ax = plt.subplots(figsize=(7, 5))
        scatter = ax.scatter(Z[:, 0], Z[:, 1], c=y_train, cmap="coolwarm", alpha=0.7, edgecolors="k")
        ax.set_xlabel("PC1 (Première Composante)")
        ax.set_ylabel("PC2 (Deuxième Composante)")
        ax.set_title("Projection 2D des Étudiants")
        fig.colorbar(scatter, ax=ax, label="Réussite Académique")
        st.pyplot(fig)

    with col2:
        st.subheader("Ratio de Variance Expliquée")
        full_pca = get_full_pca_model()
        cum_var = np.cumsum(full_pca.explained_variance_ratio_)

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(range(1, len(cum_var) + 1), full_pca.explained_variance_ratio_, alpha=0.6, label="Variance Individuelle")
        ax.step(range(1, len(cum_var) + 1), cum_var, where="mid", color="red", label="Variance Cumulée")
        ax.set_xlabel("Composantes Principales")
        ax.set_ylabel("Ratio de Variance")
        ax.set_title("Scree Plot — Variance Expliquée Cumulée")
        ax.legend()
        st.pyplot(fig)

    st.success(f"PC1 explique {pca.explained_variance_ratio_[0]*100:.2f}% de la variance et PC2 explique {pca.explained_variance_ratio_[1]*100:.2f}%.")

# 4. TRAINING
elif menu == "Entraînement":
    st.header("Entraînement et Analyse de Convergence")

    st.sidebar.subheader("Hyperparamètres du Modèle")
    lr = st.sidebar.slider("Pas d'apprentissage (alpha)", 0.001, 1.0, 0.1, step=0.01)
    l2_lambda = st.sidebar.slider("Régularisation L2 (lambda)", 0.0, 5.0, 0.1, step=0.1)
    n_iters = st.sidebar.slider("Nombre d'itérations", 50, 2000, 1000, step=50)

    with st.spinner(f"Entraînement en cours ({n_iters} itérations)..."):
        model = LogisticRegressionScratch(learning_rate=lr, l2_lambda=l2_lambda, n_iterations=n_iters)
        model.fit(X_train_scaled, y_train)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Courbe d'Apprentissage (Loss J(theta))")
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(model.cost_history, color="blue", linewidth=2)
        ax.set_xlabel("Itérations")
        ax.set_ylabel("Coût Log-Loss")
        ax.set_title(f"Convergence (Coût initial : {model.cost_history[0]:.4f} -> Final : {model.cost_history[-1]:.4f})")
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)

    with col2:
        st.subheader("Paramètres Optimisés theta")
        weights_df = pd.DataFrame({
            "Variable": ["Intercept (Bias)"] + list(feature_names),
            "Poids (theta)": model.theta
        })
        st.dataframe(weights_df, use_container_width=True)

# 5. EVALUATION
elif menu == "Évaluation":
    st.header("Évaluation des Performances de Classification")

    with st.spinner("Entraînement du modèle d'évaluation..."):
        model = get_default_model()
        preds_test = model.predict(X_test_scaled)
        probs_test = model.predict_proba(X_test_scaled)

    acc = accuracy_score_scratch(y_test, preds_test)
    prec = precision_score_scratch(y_test, preds_test)
    rec = recall_score_scratch(y_test, preds_test)
    f1 = f1_score_scratch(y_test, preds_test)
    fprs, tprs, auc = roc_curve_scratch(y_test, probs_test)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Accuracy", f"{acc*100:.2f}%")
    col2.metric("Précision", f"{prec*100:.2f}%")
    col3.metric("Rappel", f"{rec*100:.2f}%")
    col4.metric("F1-Score", f"{f1*100:.2f}%")
    col5.metric("ROC-AUC", f"{auc:.3f}")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Matrice de Confusion")
        cm = confusion_matrix_scratch(y_test, preds_test)
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                    xticklabels=["Non-réussite (0)", "Réussite (1)"],
                    yticklabels=["Non-réussite (0)", "Réussite (1)"])
        ax.set_xlabel("Classe Prédite")
        ax.set_ylabel("Classe Réelle")
        st.pyplot(fig)

    with col_b:
        st.subheader("Courbe ROC")
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(fprs, tprs, color="darkorange", lw=2, label=f"AUC = {auc:.3f}")
        ax.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
        ax.set_xlabel("FPR")
        ax.set_ylabel("TPR")
        ax.set_title("Courbe ROC")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)

# 6. PREDICTION INDIVIDUELLE
elif menu == "Prédiction Individuelle":
    st.header("Simulation de Prédiction pour un Étudiant")
    st.markdown("Ajustez les caractéristiques de l'étudiant pour simuler son estimation de réussite académique :")

    with st.spinner("Chargement du modèle..."):
        model_full, _ = get_trained_model_on_all_data()
        scaler = get_scaler()

    col1, col2, col3 = st.columns(3)
    with col1:
        g1 = st.slider("Note 1er Trimestre (G1 / 20)", 0, 20, 12)
        g2 = st.slider("Note 2ème Trimestre (G2 / 20)", 0, 20, 13)
        studytime = st.selectbox("Temps d'étude (1: <2h, 2: 2-5h, 3: 5-10h, 4: >10h)", [1, 2, 3, 4], index=1)
        failures = st.selectbox("Nombre d'échecs passés", [0, 1, 2, 3], index=0)
        absences = st.slider("Absences scolaires", 0, 50, 4)

    with col2:
        age = st.slider("Âge de l'étudiant", 15, 22, 17)
        medu = st.selectbox("Éducation Mère (0: Aucune -> 4: Supérieur)", [0, 1, 2, 3, 4], index=2)
        fedu = st.selectbox("Éducation Père (0: Aucune -> 4: Supérieur)", [0, 1, 2, 3, 4], index=2)
        traveltime = st.selectbox("Temps de trajet (1: <15min -> 4: >1h)", [1, 2, 3, 4], index=0)

    with col3:
        famrel = st.slider("Relations familiales (1: Très mauvaises -> 5: Excellentes)", 1, 5, 4)
        freetime = st.slider("Temps libre (1: Très faible -> 5: Très élevé)", 1, 5, 3)
        goout = st.slider("Sorties entre amis (1: Très faible -> 5: Très élevé)", 1, 5, 3)
        dalc = st.slider("Alcool semaine (1: Très faible -> 5: Très élevé)", 1, 5, 1)
        walc = st.slider("Alcool week-end (1: Très faible -> 5: Très élevé)", 1, 5, 1)
        health = st.slider("État de santé (1: Très mauvais -> 5: Très bon)", 1, 5, 4)

    input_data = np.array([[age, medu, fedu, traveltime, studytime, failures, famrel, freetime, goout, dalc, walc, health, absences, g1, g2]])
    input_scaled = scaler.transform(input_data)

    proba = model_full.predict_proba(input_scaled)[0]
    pred_class = model_full.predict(input_scaled)[0]

    st.markdown("---")
    st.subheader("Résultat de la Prédiction Explicable")

    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("Probabilité Estimée de Réussite Académique", f"{proba * 100:.1f}%")

    with res_col2:
        if pred_class == 1:
            st.success("**Classe Prédite : Réussite Académique**")
        else:
            st.error("**Classe Prédite : Non-réussite Académique**")

    st.warning("**Avertissement :** Cette prédiction est issue d'un modèle expérimental à visée pédagogique (données synthétiques) et ne constitue en aucun cas une décision académique réelle ou un diagnostic d'orientation.")
