import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


# Variables numériques utilisées pour le modèle
NUMERIC_FEATURES = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]

# Variables catégorielles à transformer en variables numériques
CATEGORICAL_FEATURES = [
    "SeniorCitizen",
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod"
]


def clean_data(df):
    """Nettoie les données du dataset Telco Customer Churn."""

    # On travaille sur une copie pour ne pas modifier le dataset original
    df = df.copy()

    # Les valeurs vides de TotalCharges sont remplacées par des valeurs manquantes
    df["TotalCharges"] = df["TotalCharges"].replace(
        r"^\s*$", np.nan, regex=True
    )

    # Conversion de TotalCharges en variable numérique
    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    # Les valeurs manquantes restantes sont remplacées par 0
    df["TotalCharges"] = df["TotalCharges"].fillna(0)

    return df


def build_preprocessor():
    """Construit le pipeline de prétraitement des variables."""

    # Application d'un traitement différent selon le type de variable
    return ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),  # Standardisation des variables numériques
                NUMERIC_FEATURES
            ),
            (
                "cat",
                OneHotEncoder(
                    handle_unknown="ignore",  # Gère les catégories absentes du jeu d'entraînement
                    drop="first"              # Évite la redondance entre catégories
                ),
                CATEGORICAL_FEATURES
            )
        ]
    )