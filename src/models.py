from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


def create_logistic_regression():
    """Crée le modèle de régression logistique."""

    # Modèle simple utilisé comme référence
    return LogisticRegression(
        max_iter=1000,
        random_state=42
    )


def create_decision_tree():
    """Crée le modèle Decision Tree."""

    # Modèle basé sur une succession de règles de décision
    return DecisionTreeClassifier(
        random_state=42
    )


def create_random_forest():
    """Crée le modèle Random Forest."""

    # Ensemble de plusieurs arbres pour améliorer les prédictions
    return RandomForestClassifier(
        random_state=42,
        n_jobs=-1
    )