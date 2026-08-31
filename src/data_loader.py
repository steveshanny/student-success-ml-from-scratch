"""
Data loader and dataset generator for UCI Student Performance dataset.
"""

import os
import numpy as np
import pandas as pd


def generate_uci_student_dataset(output_path="data/raw/student_data.csv", seed=42):
    """
    Generate realistic UCI Student Performance dataset (Math context).
    395 student records with realistic academic and demographic distributions.
    """
    np.random.seed(seed)
    n_samples = 395

    age = np.random.randint(15, 22, size=n_samples)
    Medu = np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.05, 0.25, 0.30, 0.20, 0.20])
    Fedu = np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.05, 0.30, 0.30, 0.20, 0.15])
    traveltime = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.65, 0.25, 0.07, 0.03])
    studytime = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.25, 0.50, 0.15, 0.10])
    failures = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.75, 0.15, 0.06, 0.04])

    famrel = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.02, 0.05, 0.18, 0.50, 0.25])
    freetime = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.05, 0.15, 0.40, 0.30, 0.10])
    goout = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.05, 0.20, 0.35, 0.25, 0.15])
    Dalc = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.70, 0.18, 0.07, 0.03, 0.02])
    Walc = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.40, 0.25, 0.20, 0.10, 0.05])
    health = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.10, 0.12, 0.23, 0.20, 0.35])
    absences = np.random.negative_binomial(1, 0.15, size=n_samples)
    absences = np.clip(absences, 0, 75)

    # Realistic correlated grades (G1, G2, G3 out of 20)
    base_ability = 10.0 + 0.8 * Medu + 0.7 * studytime - 1.5 * failures - 0.05 * absences + np.random.normal(0, 2.0, n_samples)
    G1 = np.clip(np.round(base_ability + np.random.normal(0, 1.2, n_samples)), 0, 20)
    G2 = np.clip(np.round(0.85 * G1 + np.random.normal(0, 1.5, n_samples)), 0, 20)
    G3 = np.clip(np.round(0.90 * G2 + np.random.normal(0, 1.5, n_samples)), 0, 20)

    # Target: academic success (1 if final grade G3 >= 10, else 0)
    academic_success = (G3 >= 10).astype(int)

    df = pd.DataFrame({
        "age": age,
        "Medu": Medu,
        "Fedu": Fedu,
        "traveltime": traveltime,
        "studytime": studytime,
        "failures": failures,
        "famrel": famrel,
        "freetime": freetime,
        "goout": goout,
        "Dalc": Dalc,
        "Walc": Walc,
        "health": health,
        "absences": absences,
        "G1": G1,
        "G2": G2,
        "academic_success": academic_success
    })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset generated at {output_path} ({len(df)} rows, {df.shape[1]} columns)")
    return df


if __name__ == "__main__":
    generate_uci_student_dataset()
