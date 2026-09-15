# Prédiction du Churn Client avec des Modèles de Machine Learning

## Présentation du projet

Ce projet a pour objectif de prédire le **churn client**, c’est-à-dire la probabilité qu’un client résilie son abonnement à un service de télécommunication.

L’objectif est de construire et comparer plusieurs modèles de Machine Learning afin d’identifier les clients susceptibles de quitter l’entreprise, tout en mettant en place un pipeline complet allant de la préparation des données jusqu’à l’évaluation et à la visualisation des résultats.

**Projet réalisé dans le cadre de la formation Directeur de Projet en Intelligence Artificielle — AIA01.**

---

## Problématique

L’entreprise souhaite anticiper les départs de ses clients afin de pouvoir mettre en place des actions de fidélisation.

La problématique est donc la suivante :

> **Peut-on prédire quels clients sont susceptibles de résilier leur abonnement à partir de leurs caractéristiques et de leur historique d’utilisation ?**

Il s’agit d’un problème de **classification binaire** :

* `0` → No Churn : le client reste
* `1` → Churn : le client quitte l’entreprise

---

## Dataset

Le dataset utilisé est le **Telco Customer Churn**, disponible sur Kaggle.

Il contient :

* **7 043 clients**
* **21 variables**
* une variable cible : `Churn`

Les variables décrivent notamment :

* les caractéristiques du client ;
* son ancienneté ;
* son type de contrat ;
* ses services ;
* son mode de paiement ;
* ses dépenses mensuelles ;
* ses dépenses totales.

### Variable cible

La variable `Churn` indique si le client a quitté l'entreprise :

* `No` : client conservé
* `Yes` : client ayant résilié

La répartition de la cible est :

* **73,46 %** de clients sans churn
* **26,54 %** de clients ayant churné

---

## Analyse exploratoire

L'analyse exploratoire a permis d'identifier plusieurs associations avec le churn.

### Type de contrat

Le taux de churn est particulièrement élevé chez les clients ayant un contrat mensuel :

* Month-to-month : **42,71 %**
* One year : **11,27 %**
* Two year : **2,83 %**

### Ancienneté

L'ancienneté moyenne est différente selon le statut du client :

* Clients sans churn : **37,57 mois**
* Clients ayant churné : **17,98 mois**

Les clients ayant une ancienneté plus faible sont donc davantage représentés parmi les clients ayant quitté l'entreprise.

### Dépenses mensuelles

Les dépenses mensuelles moyennes sont également différentes :

* Clients sans churn : **61,27**
* Clients ayant churné : **74,44**

Ces résultats permettent d'identifier des profils associés au churn.

**Attention : ces observations montrent des associations dans les données et ne permettent pas de conclure à une relation de causalité.**

---

## Préparation des données

Plusieurs étapes de préparation ont été réalisées avant l'entraînement des modèles.

### Nettoyage

La variable `TotalCharges` contenait **11 valeurs manquantes**.

Ces valeurs correspondaient à des clients ayant une ancienneté de 0 mois.

Les valeurs ont été converties en valeurs numériques puis les valeurs manquantes ont été remplacées par `0`.

Aucun doublon n'a été détecté.

La variable `customerID` a été supprimée car elle constitue un identifiant et n'apporte pas d'information utile à la prédiction.

### Variables numériques

Les variables numériques utilisées sont :

* `tenure`
* `MonthlyCharges`
* `TotalCharges`

Elles sont standardisées avec **StandardScaler**.

### Variables catégorielles

Les variables catégorielles sont transformées avec **OneHotEncoder**.

Les paramètres utilisés sont :

* `handle_unknown="ignore"` afin de gérer les catégories éventuellement absentes du jeu d'entraînement ;
* `drop="first"` afin d'éviter une redondance entre les catégories.

Après transformation, le jeu de données contient **46 variables**.

---

## Séparation des données

Le dataset est séparé en deux parties :

* **80 % pour l'entraînement**
* **20 % pour le test**

La séparation est stratifiée afin de conserver une répartition similaire de la variable cible dans les deux ensembles.

Paramètres utilisés :

* `random_state=42`
* `stratify=y`

Résultat :

* Jeu d'entraînement : **5 634 clients**
* Jeu de test : **1 409 clients**

---

## Pipeline de Machine Learning

Le pipeline général du projet est le suivant :

**Données brutes → Nettoyage → Prétraitement → Séparation Train/Test → Entraînement → Optimisation → Évaluation → Visualisation**

Le prétraitement et le modèle sont intégrés dans les pipelines afin d'éviter les fuites de données entre les différentes étapes.

---

## Modèles testés

Trois algorithmes de classification ont été étudiés :

### 1. Régression logistique

La régression logistique constitue un modèle de référence simple et interprétable.

Elle permet notamment d'obtenir des probabilités d'appartenance à la classe `Churn`.

### 2. Decision Tree

L'arbre de décision fonctionne à partir d'une succession de règles permettant de séparer les différentes classes.

Il est facilement interprétable mais peut être sensible au surapprentissage.

### 3. Random Forest

Random Forest est un ensemble de plusieurs arbres de décision.

L'objectif est de combiner leurs prédictions afin d'obtenir un modèle plus robuste qu'un arbre individuel.

---

## Métriques utilisées

Plusieurs métriques sont utilisées pour comparer les modèles :

### Accuracy

Proportion de prédictions correctement classées.

### Precision

Parmi les clients prédits comme churners, proportion de clients qui ont réellement churné.

### Recall

Parmi les clients ayant réellement churné, proportion de ceux correctement détectés.

### F1-score

Moyenne harmonique entre la précision et le recall.

### ROC-AUC

Mesure la capacité du modèle à distinguer les deux classes sur différents seuils de décision.

Le ROC-AUC est calculé à partir des probabilités prédites par les modèles.

---

# Résultats avant optimisation

Une première comparaison des modèles a été réalisée avant l'optimisation des hyperparamètres.

| Modèle              | Accuracy | Precision |  Recall | F1-score | ROC-AUC |
| ------------------- | -------: | --------: | ------: | -------: | ------: |
| Logistic Regression |  80,62 % |   65,93 % | 55,88 % |  60,49 % | 84,22 % |
| Decision Tree       |  73,03 % |   49,17 % | 47,59 % |  48,37 % | 64,86 % |
| Random Forest       |  79,49 % |   64,41 % | 50,80 % |  56,80 % | 82,56 % |

La **régression logistique** obtient les meilleurs résultats initiaux sur la majorité des métriques.

Cette première étape permet également de servir de référence avant l'optimisation des modèles.

---

# Optimisation des hyperparamètres

Afin d'améliorer les performances, une recherche des meilleurs hyperparamètres a été réalisée avec **GridSearchCV**.

La validation croisée permet de tester plusieurs configurations du modèle sur différentes partitions du jeu d'entraînement.

La métrique utilisée pour sélectionner les meilleurs paramètres est le **ROC-AUC**.

### Meilleurs paramètres

#### Logistic Regression

* `C = 10`
* `solver = lbfgs`
* ROC-AUC moyen en validation croisée : **0,8460**

#### Decision Tree

* `max_depth = 5`
* `min_samples_split = 2`
* `min_samples_leaf = 10`
* ROC-AUC moyen en validation croisée : **0,8184**

#### Random Forest

* `n_estimators = 200`
* `max_depth = 10`
* `min_samples_split = 2`
* `min_samples_leaf = 2`
* ROC-AUC moyen en validation croisée : **0,8435**

---

# Résultats après optimisation

Les modèles optimisés ont ensuite été évalués sur le jeu de test, qui n'a pas été utilisé pendant l'entraînement.

| Modèle              | Accuracy | Precision |  Recall | F1-score | ROC-AUC |
| ------------------- | -------: | --------: | ------: | -------: | ------: |
| Logistic Regression |  80,55 % |   65,72 % | 55,88 % |  60,40 % | 84,13 % |
| Decision Tree       |  79,56 % |   63,35 % | 54,55 % |  58,62 % | 82,70 % |
| Random Forest       |  80,41 % |   66,67 % | 52,41 % |  58,68 % | 84,38 % |

---

# Choix du modèle final

Le **Random Forest optimisé** a été retenu comme modèle final.

Il obtient le meilleur **ROC-AUC sur le jeu de test avec 84,38 %**, ainsi que la meilleure **Precision avec 66,67 %** parmi les modèles optimisés.

Cependant, la comparaison montre également que la régression logistique possède :

* un meilleur Recall : **55,88 % contre 52,41 %**
* un meilleur F1-score : **60,40 % contre 58,68 %**

Le choix du modèle dépend donc de l'objectif métier.

Dans ce projet, le Random Forest est retenu pour sa capacité de discrimination sur le jeu de test et sa possibilité d'analyser l'importance des variables.

---

# Validation du modèle final

Le modèle final est évalué sur un jeu de test indépendant afin d'estimer sa capacité de généralisation sur de nouvelles données.

La matrice de confusion du Random Forest est :

|               | Prédit No Churn | Prédit Churn |
| ------------- | --------------: | -----------: |
| Réel No Churn |             937 |           98 |
| Réel Churn    |             178 |          196 |

Le modèle détecte correctement **196 clients churners sur 374**, soit un Recall de **52,41 %**.

Cela signifie également que **178 clients ayant réellement churné ne sont pas détectés par le modèle**.

Ce résultat constitue une limite importante si l'objectif métier principal est de détecter un maximum de clients susceptibles de partir.

---

# Importance des variables

L'analyse de l'importance des variables du Random Forest montre notamment :

| Variable                       | Importance |
| ------------------------------ | ---------: |
| tenure                         |    19,83 % |
| TotalCharges                   |    15,36 % |
| MonthlyCharges                 |    11,58 % |
| InternetService_Fiber optic    |     7,03 % |
| PaymentMethod_Electronic check |     6,56 % |
| Contract_Two year              |     5,95 % |
| Contract_One year              |     3,41 % |
| OnlineSecurity_Yes             |     3,39 % |
| TechSupport_Yes                |     2,53 % |
| PaperlessBilling_Yes           |     2,14 % |

L'ancienneté (`tenure`) est la variable la plus importante selon le modèle.

Ces importances permettent d'identifier les variables utilisées fortement par le modèle dans ses décisions.

**Elles ne doivent cependant pas être interprétées comme des relations de causalité.**

---

# Dashboard

Une interface interactive a été développée avec **Streamlit** afin de faciliter l'exploration des données et des résultats.

Le dashboard permet notamment de :

* filtrer les clients ;
* analyser le churn selon le type de contrat ;
* analyser le churn selon le service Internet ;
* analyser le churn selon le moyen de paiement ;
* visualiser la relation entre ancienneté et churn ;
* analyser les dépenses mensuelles ;
* consulter plusieurs indicateurs clés ;
* afficher les données filtrées.

Les principaux indicateurs affichés sont notamment :

* nombre de clients ;
* nombre de clients churners ;
* taux de churn ;
* ancienneté moyenne ;
* dépenses mensuelles moyennes ;
* ROC-AUC du modèle final.

---

# Recommandations métier

Les résultats permettent d'identifier plusieurs profils particulièrement associés au churn.

Une attention particulière peut notamment être portée aux :

* clients avec un contrat `Month-to-month` ;
* clients ayant une faible ancienneté ;
* clients ayant des dépenses mensuelles élevées ;
* clients utilisant certains services ou moyens de paiement associés à un churn plus important.

Le modèle peut être utilisé comme outil d'aide à la décision afin de cibler des actions de fidélisation.

Par exemple :

* proposer des offres adaptées ;
* contacter les clients présentant un risque élevé ;
* proposer des changements de contrat ;
* améliorer l'accompagnement des nouveaux clients ;
* analyser les services associés aux départs.

Ces recommandations doivent être complétées par une analyse métier avant toute décision opérationnelle.

---

# Limites du projet

Plusieurs limites doivent être prises en compte.

### Déséquilibre de la cible

La classe `Churn` est minoritaire avec environ **26,54 %** des clients.

L'Accuracy seule ne suffit donc pas pour évaluer correctement le modèle.

### Recall encore limité

Le modèle final présente un Recall de **52,41 %**.

Une partie importante des clients churners n'est donc pas détectée.

### Dataset statique

Le dataset utilisé représente une situation donnée et ne constitue pas nécessairement une représentation complète des comportements futurs des clients.

### Interprétation des variables

Les importances des variables montrent des associations utilisées par le modèle mais ne permettent pas d'établir des relations causales.

---

# Perspectives d'amélioration

Plusieurs améliorations pourraient être envisagées :

* tester d'autres algorithmes comme XGBoost, LightGBM ou SVM ;
* comparer différentes stratégies de gestion du déséquilibre des classes ;
* tester `class_weight="balanced"` ;
* utiliser du sur-échantillonnage comme SMOTE ;
* optimiser le seuil de classification afin d'améliorer le Recall ;
* utiliser des méthodes d'interprétabilité comme SHAP ;
* réaliser une validation plus approfondie ;
* intégrer de nouvelles données comportementales ;
* améliorer le suivi des performances du modèle dans le temps.

Une optimisation du seuil de décision pourrait notamment être intéressante si l'objectif métier est de détecter davantage de clients susceptibles de churner.

---

# Déploiement

Le projet peut être déployé sous la forme d'une application de scoring.

Une architecture possible serait :

**Utilisateur / Application métier → API de prédiction → Modèle Machine Learning → Résultat du scoring → Dashboard**

Le modèle pourrait être exposé via une API avec **Flask** ou **FastAPI**.

Le dashboard Streamlit constitue une première interface permettant d'explorer les résultats.

Le déploiement en production n'a pas été réalisé dans le cadre de ce projet ; cette architecture constitue une perspective d'évolution.

---

# Monitoring

Une fois déployé, le modèle pourrait être suivi à l'aide de plusieurs indicateurs :

* ROC-AUC ;
* Precision ;
* Recall ;
* F1-score ;
* taux de churn réel ;
* taux de prédictions positives ;
* évolution de la distribution des variables ;
* dérive des données ;
* temps de réponse de l'API ;
* taux d'erreurs.

Un système de monitoring permettrait de détecter une éventuelle dégradation des performances du modèle et d'identifier les besoins de réentraînement.

Le monitoring en production n'a pas été implémenté dans ce projet.

---

# Structure du projet

Le projet est organisé de la manière suivante :

```text
telco-customer-churn/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── notebooks/
│   ├── 01_analyse_preparation.ipynb
│   ├── 02_modelisation_optimisation.ipynb
│   └── 03_validation_finale.ipynb
│
├── reports/
│   ├── figures/
│   └── conclusions.md
│
├── src/
│   ├── preprocessing.py
│   ├── models.py
│   ├── evaluation.py
│   └── visualization.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

# Installation

Cloner le repository :

```bash
git clone https://github.com/lynalasla/telco-customer-churn.git
cd telco-customer-churn
```

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement virtuel.

Sous Windows :

```bash
.venv\Scripts\activate
```

Sous macOS/Linux :

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

# Exécution

Les notebooks peuvent être exécutés dans l'ordre suivant :

```text
01_analyse_preparation.ipynb
        ↓
02_modelisation_optimisation.ipynb
        ↓
03_validation_finale.ipynb
```

Pour lancer le dashboard Streamlit :

```bash
streamlit run dashboard/app.py
```

---

# Technologies utilisées

### Langage

* Python

### Analyse et traitement des données

* Pandas
* NumPy

### Machine Learning

* Scikit-learn

### Visualisation

* Matplotlib
* Seaborn
* Plotly

### Dashboard

* Streamlit

### Environnement

* Jupyter Notebook
* Git
* GitHub

---

# Conclusion

Ce projet a permis de mettre en place une chaîne complète de Machine Learning pour la prédiction du churn client.

Les principales étapes réalisées sont :

1. analyse et nettoyage des données ;
2. préparation des variables ;
3. séparation des données en train/test ;
4. entraînement de trois modèles ;
5. comparaison des performances ;
6. optimisation avec GridSearchCV ;
7. validation sur un jeu de test indépendant ;
8. analyse des variables importantes ;
9. création d'un dashboard interactif ;
10. réflexion sur le déploiement et le monitoring.

Le Random Forest optimisé atteint un **ROC-AUC de 84,38 %** sur le jeu de test.

Cependant, son Recall de **52,41 %** montre qu'une partie importante des clients churners reste difficile à détecter.

Le projet pourrait donc être amélioré en travaillant notamment sur le déséquilibre des classes, le choix du seuil de décision, l'interprétabilité et l'intégration de nouvelles données.
