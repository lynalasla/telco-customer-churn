import matplotlib.pyplot as plt

from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay
)


def plot_confusion_matrix(model, X_test, y_test):
    """Affiche la matrice de confusion."""

    # Génère la matrice à partir des prédictions du modèle
    ConfusionMatrixDisplay.from_estimator(
        model,
        X_test,
        y_test
    )

    # Ajoute le titre et ajuste l'affichage
    plt.title("Matrice de confusion")
    plt.tight_layout()
    plt.show()


def plot_roc_curve(model, X_test, y_test):
    """Affiche la courbe ROC."""

    # Génère la courbe ROC à partir des probabilités prédites
    RocCurveDisplay.from_estimator(
        model,
        X_test,
        y_test
    )

    # Ajoute le titre et ajuste l'affichage
    plt.title("Courbe ROC")
    plt.tight_layout()
    plt.show()