from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


def evaluate_model(model, X_test, y_test):
    """Calcule les principales métriques de classification."""

    # Prédictions finales du modèle : 0 ou 1
    y_pred = model.predict(X_test)

    # Probabilité prédite pour la classe 1 (Churn = Yes)
    y_proba = model.predict_proba(X_test)[:, 1]

    # Calcul des différentes métriques
    return {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1-score": f1_score(y_test, y_pred),

        # Le ROC-AUC est calculé à partir des probabilités
        "ROC-AUC": roc_auc_score(y_test, y_proba)
    }