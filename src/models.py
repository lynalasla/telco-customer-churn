from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


def create_logistic_regression(**kwargs):
    """Crée le modèle de régression logistique."""

    # Modèle simple utilisé comme référence
    parameters = {
        "max_iter": 1000,
        "random_state": 42,
    }
    parameters.update(kwargs)
    return LogisticRegression(**parameters)


def create_decision_tree(**kwargs):
    """Crée le modèle Decision Tree."""

    # Modèle basé sur une succession de règles de décision
    parameters = {"random_state": 42}
    parameters.update(kwargs)
    return DecisionTreeClassifier(**parameters)


def create_random_forest(**kwargs):
    """Crée le modèle Random Forest."""

    # Ensemble de plusieurs arbres pour améliorer les prédictions
    parameters = {"random_state": 42, "n_jobs": -1}
    parameters.update(kwargs)
    return RandomForestClassifier(**parameters)
