# Prédiction du Churn Client avec des Modèles de Machine Learning

## Présentation du projet

Ce projet a pour objectif de développer un système de Machine Learning capable de prédire le **churn client**, c’est-à-dire la probabilité qu’un client résilie son abonnement auprès d'une entreprise de télécommunications.

Dans un contexte fortement concurrentiel, la fidélisation des clients représente un enjeu important pour les entreprises de télécommunications. Identifier suffisamment tôt les clients susceptibles de partir permet de mettre en place des actions de fidélisation ciblées et d'améliorer la prise de décision commerciale.

L'objectif est donc de construire un modèle capable d'identifier les clients présentant un risque de résiliation à partir de leurs caractéristiques et de leur historique.

Le projet couvre l'ensemble d'une démarche de Machine Learning :

* analyse et compréhension des données ;
* nettoyage et préparation des données ;
* analyse exploratoire des données (EDA) ;
* transformation des variables ;
* entraînement de plusieurs modèles ;
* comparaison des performances ;
* optimisation des hyperparamètres ;
* évaluation sur un jeu de test indépendant ;
* interprétation des résultats ;
* formulation de recommandations métier.

---

## Problématique

La problématique étudiée est la suivante :

> **Peut-on prédire si un client d'une entreprise de télécommunications va résilier son contrat à partir de ses caractéristiques et de son historique de consommation ?**

La variable cible est `Churn` :

* `No` : le client reste chez l'entreprise ;
* `Yes` : le client résilie son contrat.

Le problème est donc traité comme un problème de **classification binaire**.

---

## Dataset

Le projet utilise le dataset public **Telco Customer Churn**, disponible sur Kaggle.

Le dataset contient :

* **7 043 clients** ;
* **21 variables** ;
* une variable cible `Churn`.

Les variables décrivent notamment :

* les caractéristiques du client ;
* son ancienneté ;
* son contrat ;
* ses services ;
* son mode de paiement ;
* ses charges mensuelles ;
* ses charges totales.

### Principales variables

| Variable           | Description                    |
| ------------------ | ------------------------------ |
| `customerID`       | Identifiant unique du client   |
| `gender`           | Genre du client                |
| `SeniorCitizen`    | Indicateur de seniorité        |
| `Partner`          | Présence d'un partenaire       |
| `Dependents`       | Présence de personnes à charge |
| `tenure`           | Ancienneté du client           |
| `PhoneService`     | Service téléphonique           |
| `MultipleLines`    | Plusieurs lignes téléphoniques |
| `InternetService`  | Type de service Internet       |
| `OnlineSecurity`   | Service de sécurité en ligne   |
| `OnlineBackup`     | Service de sauvegarde en ligne |
| `DeviceProtection` | Protection des appareils       |
| `TechSupport`      | Support technique              |
| `StreamingTV`      | Service de streaming TV        |
| `StreamingMovies`  | Service de streaming vidéo     |
| `Contract`         | Type de contrat                |
| `PaperlessBilling` | Facturation sans papier        |
| `PaymentMethod`    | Mode de paiement               |
| `MonthlyCharges`   | Charges mensuelles             |
| `TotalCharges`     | Charges totales                |
| `Churn`            | Résiliation du client          |

---

# Méthodologie

Le projet est organisé en plusieurs étapes afin de suivre une démarche structurée de Data Science.

## 1. Analyse et préparation des données

La première étape consiste à charger le dataset et à analyser sa structure.

Les vérifications réalisées comprennent notamment :

* le nombre de lignes et de colonnes ;
* les types de données ;
* les valeurs manquantes ;
* les doublons ;
* les statistiques descriptives ;
* la distribution de la variable cible.

Une attention particulière a été portée à la variable `TotalCharges`, initialement considérée comme une variable textuelle.

Les valeurs vides ont été converties en valeurs manquantes, puis la variable a été transformée en numérique.

Les valeurs manquantes obtenues concernaient **11 observations**, correspondant à des clients ayant une ancienneté (`tenure`) égale à 0. Ces valeurs ont été remplacées par 0 afin de conserver ces observations dans le dataset.

La variable `customerID` n'a pas été utilisée pour l'apprentissage car il s'agit d'un identifiant unique qui n'apporte pas d'information prédictive pertinente.

---

## 2. Analyse exploratoire des données

Une analyse exploratoire a été réalisée afin d'identifier les principales caractéristiques associées au churn.

### Distribution du churn

Le dataset contient :

* **73,46 %** de clients n'ayant pas résilié ;
* **26,54 %** de clients ayant résilié.

La variable cible présente donc un déséquilibre modéré entre les deux classes.

### Type de contrat

Le type de contrat présente une différence importante dans les taux de churn.

| Type de contrat | Taux de churn |
| --------------- | ------------: |
| Month-to-month  |       42,71 % |
| One year        |       11,27 % |
| Two year        |        2,83 % |

Les clients disposant d'un contrat mensuel présentent donc un taux de résiliation nettement supérieur à celui observé pour les contrats d'un ou deux ans.

### Ancienneté

L'ancienneté moyenne diffère également entre les deux groupes :

* clients n'ayant pas résilié : **37,57 mois** ;
* clients ayant résilié : **17,98 mois**.

Les clients ayant une ancienneté plus faible sont davantage représentés parmi les clients ayant résilié leur contrat.

### Charges mensuelles

Les charges mensuelles moyennes sont :

* **61,27** pour les clients n'ayant pas résilié ;
* **74,44** pour les clients ayant résilié.

### Service Internet

Le taux de churn varie également selon le type de service Internet :

| Service Internet    | Taux de churn |
| ------------------- | ------------: |
| DSL                 |       18,96 % |
| Fiber optic         |       41,89 % |
| No internet service |        7,40 % |

### Mode de paiement

Le mode de paiement présente également des différences :

| Mode de paiement        | Taux de churn |
| ----------------------- | ------------: |
| Electronic check        |       45,29 % |
| Mailed check            |       19,11 % |
| Automatic bank transfer |       16,71 % |
| Automatic credit card   |       15,24 % |

Ces résultats permettent d'identifier des profils présentant des niveaux de churn différents.

**Attention : ces observations montrent des associations statistiques et ne permettent pas d'établir une relation de causalité.**

---

# Prétraitement des données

Avant l'entraînement des modèles, les données ont été séparées en variables numériques et catégorielles.

### Variables numériques

* `tenure`
* `MonthlyCharges`
* `TotalCharges`

Les variables numériques ont été standardisées avec `StandardScaler`.

### Variables catégorielles

Les variables catégorielles ont été transformées avec `OneHotEncoder`.

L'option `handle_unknown="ignore"` permet de gérer correctement d'éventuelles catégories inconnues lors de la transformation des données de test.

L'option `drop="first"` permet de supprimer une modalité de référence pour chaque variable catégorielle.

---

# Séparation des données

Les données ont été séparées en :

* **80 % pour l'entraînement** ;
* **20 % pour le test**.

La séparation a été réalisée avec une `random_state` fixée à `42` afin d'obtenir des résultats reproductibles.

Une **stratification sur la variable cible** a également été utilisée afin de conserver une proportion similaire de clients ayant résilié dans les ensembles d'entraînement et de test.

### Dimensions

| Ensemble     | Nombre d'observations |
| ------------ | --------------------: |
| Entraînement |                 5 634 |
| Test         |                 1 409 |

---

# Modèles de Machine Learning

Trois algorithmes de classification ont été étudiés.

## Régression Logistique

La Régression Logistique constitue un modèle de référence adapté aux problèmes de classification binaire.

Elle permet également d'obtenir un modèle relativement interprétable.

## Decision Tree

L'arbre de décision permet de représenter les règles de classification sous forme d'une structure arborescente.

Il peut capturer des relations non linéaires entre les variables.

## Random Forest

Le Random Forest repose sur un ensemble de plusieurs arbres de décision.

Cette approche permet généralement d'obtenir des modèles plus robustes qu'un arbre de décision unique et de mesurer l'importance des variables utilisées dans les prédictions.

---

# Métriques d'évaluation

Plusieurs métriques ont été utilisées afin d'obtenir une évaluation complète des modèles :

### Accuracy

Proportion globale de prédictions correctes.

### Precision

Parmi les clients prédits comme churners, proportion de clients qui ont réellement résilié.

### Recall

Parmi les clients ayant réellement résilié, proportion correctement détectée par le modèle.

### F1-score

Moyenne harmonique entre la précision et le recall.

### ROC-AUC

Mesure la capacité du modèle à distinguer les deux classes sur différents seuils de classification.

Une **matrice de confusion** et une **courbe ROC** ont également été utilisées pour compléter l'analyse.

---

# Résultats des modèles

## Modèles optimisés sur le jeu de test

| Modèle                |   Accuracy |  Precision |     Recall |   F1-score |    ROC-AUC |
| --------------------- | ---------: | ---------: | ---------: | ---------: | ---------: |
| Régression Logistique |     0.8055 |     0.6572 | **0.5588** | **0.6040** |     0.8413 |
| Decision Tree         |     0.7956 |     0.6335 |     0.5455 |     0.5862 |     0.8270 |
| Random Forest         | **0.8041** | **0.6667** |     0.5241 |     0.5868 | **0.8438** |

Les trois modèles présentent des performances relativement proches.

Le Random Forest obtient le meilleur ROC-AUC sur le jeu de test ainsi que la meilleure précision.

La Régression Logistique obtient cependant le meilleur recall et le meilleur F1-score.

---

# Optimisation des hyperparamètres

Une recherche par grille (`GridSearchCV`) a été réalisée afin d'identifier des configurations plus performantes.

### Random Forest

Les paramètres explorés comprenaient notamment :

* `n_estimators`
* `max_depth`
* `min_samples_split`
* `min_samples_leaf`

La meilleure configuration obtenue est :

```text
n_estimators = 200
max_depth = 10
min_samples_split = 2
min_samples_leaf = 2
```

Le meilleur ROC-AUC obtenu en validation croisée est de **0,8435**.

### Régression Logistique

Les paramètres `C` et `solver` ont été optimisés.

La meilleure configuration est :

```text
C = 10
solver = lbfgs
```

Le meilleur ROC-AUC obtenu en validation croisée est de **0,8460**.

### Decision Tree

Les paramètres liés à la profondeur et aux tailles minimales des feuilles et des divisions ont été optimisés.

La meilleure configuration est :

```text
max_depth = 5
min_samples_split = 2
min_samples_leaf = 10
```

Le meilleur ROC-AUC obtenu en validation croisée est de **0,8184**.

---

# Modèle final

Le **Random Forest optimisé** a été retenu comme modèle final.

Ses performances sur le jeu de test sont :

* Accuracy : **80,41 %**
* Precision : **66,67 %**
* Recall : **52,41 %**
* F1-score : **58,68 %**
* ROC-AUC : **84,38 %**

Le ROC-AUC de 0,8438 indique une bonne capacité du modèle à distinguer les clients susceptibles de résilier de ceux qui ne résilient pas.

Cependant, le recall de 52,41 % montre qu'une partie importante des clients réellement churners n'est pas détectée.

---

# Matrice de confusion

La matrice de confusion du modèle final est :

|            | Prédit : Non | Prédit : Oui |
| ---------- | -----------: | -----------: |
| Réel : Non |          937 |           98 |
| Réel : Oui |          178 |          196 |

Le modèle identifie correctement **196 clients parmi les 374 clients ayant réellement résilié**.

À l'inverse, **178 clients churners ne sont pas détectés** par le modèle.

Ce résultat constitue une limite importante si l'objectif principal de l'entreprise est de détecter le maximum de clients à risque.

---

# Importance des variables

L'analyse du Random Forest permet d'identifier les variables qui contribuent le plus aux prédictions.

Les dix variables les plus importantes sont :

| Variable                         | Importance |
| -------------------------------- | ---------: |
| `tenure`                         |    19,83 % |
| `TotalCharges`                   |    15,36 % |
| `MonthlyCharges`                 |    11,58 % |
| `InternetService_Fiber optic`    |     7,03 % |
| `PaymentMethod_Electronic check` |     6,56 % |
| `Contract_Two year`              |     5,95 % |
| `Contract_One year`              |     3,41 % |
| `OnlineSecurity_Yes`             |     3,39 % |
| `TechSupport_Yes`                |     2,53 % |
| `PaperlessBilling_Yes`           |     2,14 % |

L'ancienneté, les charges totales et les charges mensuelles sont les variables les plus contributives aux prédictions du modèle.

Ces importances permettent de mieux comprendre le fonctionnement du modèle, mais ne doivent pas être interprétées comme des relations causales.

---

# Recommandations métier

Les résultats obtenus peuvent être utilisés pour construire une stratégie de prévention du churn.

L'entreprise pourrait notamment :

1. **Identifier les clients à risque** à l'aide des probabilités produites par le modèle.

2. **Porter une attention particulière aux nouveaux clients**, notamment ceux présentant une faible ancienneté.

3. **Analyser les clients avec des contrats mensuels**, qui présentent un taux de churn nettement plus élevé.

4. **Mettre en place des actions de fidélisation ciblées**, telles que des offres personnalisées ou des avantages liés à l'engagement.

5. **Analyser les profils associés aux différents services Internet et modes de paiement** afin d'identifier d'éventuels segments présentant un risque plus important.

6. Utiliser le modèle comme un **outil d'aide à la décision** plutôt que comme un système de décision automatique.

---

# Limites

Plusieurs limites doivent être prises en compte.

### Performance du recall

Le recall du modèle final est de **52,41 %**. Le modèle ne détecte donc qu'un peu plus de la moitié des clients ayant réellement résilié.

### Déséquilibre de la cible

Les clients n'ayant pas résilié représentent environ 73 % du dataset contre 27 % pour les churners. L'Accuracy seule ne permet donc pas d'évaluer correctement les performances du modèle.

### Données utilisées

Les résultats dépendent du dataset utilisé et de sa représentativité. Ils ne peuvent pas être automatiquement généralisés à toutes les entreprises de télécommunications.

### Évolution des comportements

Les comportements des clients peuvent évoluer avec le temps. Un modèle performant aujourd'hui pourrait donc perdre en efficacité si les données et les comportements changent.

---

# Perspectives d'amélioration

Plusieurs pistes pourraient être explorées dans une version future du projet :

* tester d'autres algorithmes de Machine Learning ;
* utiliser des techniques de gestion du déséquilibre des classes ;
* optimiser le seuil de classification afin d'améliorer le recall ;
* analyser plus précisément les faux négatifs ;
* utiliser des méthodes d'interprétabilité comme SHAP ;
* mettre en place un suivi des performances du modèle ;
* réentraîner régulièrement le modèle avec de nouvelles données ;
* développer un dashboard permettant aux équipes commerciales d'explorer les clients à risque ;
* déployer le modèle dans une application de prédiction.

---

# Structure du projet

```text
telco-customer-churn/
│
├── data/
│   ├── raw/
│   │   └── telco-customer-churn.csv
│   │
│   └── processed/
│
├── notebooks/
│   ├── 01_analyse_preparation.ipynb
│   ├── 02_modelisation_optimisation.ipynb
│   └── 03_validation_finale.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── models.py
│   ├── evaluation.py
│   └── visualization.py
│
├── models/
│
├── reports/
│   ├── figures/
│   └── conclusions.md
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

### Description des principaux dossiers

**`data/`**
Contient les données utilisées pour le projet.

**`notebooks/`**
Contient les notebooks correspondant aux différentes étapes de l'analyse.

**`src/`**
Contient les fonctions Python réutilisables liées au prétraitement, aux modèles, à l'évaluation et aux visualisations.

**`models/`**
Destiné aux modèles entraînés et sauvegardés.

**`reports/`**
Contient les conclusions et les figures produites pendant le projet.

---

# Installation

## 1. Cloner le projet

```bash
git clone <URL_DU_REPOSITORY>
cd telco-customer-churn
```

## 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# Exécution

L'analyse peut être exécutée dans l'ordre suivant :

### 1. Analyse et préparation

```text
notebooks/01_analyse_preparation.ipynb
```

Ce notebook contient l'analyse de la qualité des données, le nettoyage, les statistiques descriptives et l'analyse exploratoire.

### 2. Modélisation et optimisation

```text
notebooks/02_modelisation_optimisation.ipynb
```

Ce notebook contient l'entraînement des modèles, leur comparaison et l'optimisation des hyperparamètres.

### 3. Validation finale

```text
notebooks/03_validation_finale.ipynb
```

Ce notebook contient l'évaluation finale du modèle, la matrice de confusion, la courbe ROC et l'analyse de l'importance des variables.

---

# Technologies utilisées

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **Matplotlib**
* **Seaborn**
* **Jupyter Notebook**
* **Git / GitHub**

---

# Conclusion

Ce projet a permis de mettre en œuvre une démarche complète de Machine Learning appliquée à la prédiction du churn client.

L'analyse exploratoire a permis d'identifier plusieurs caractéristiques associées au départ des clients, notamment l'ancienneté, le type de contrat, les charges mensuelles, le type de service Internet et le mode de paiement.

Après comparaison et optimisation de plusieurs modèles, le Random Forest optimisé a obtenu un **ROC-AUC de 0,8438 sur le jeu de test**.

Le modèle constitue ainsi une base pertinente pour identifier les clients présentant un risque de résiliation. Toutefois, son recall de 52,41 % montre qu'une amélioration reste nécessaire avant une utilisation opérationnelle.

Dans un contexte réel, l'étape suivante consisterait notamment à optimiser le seuil de décision et à privilégier une stratégie permettant de détecter davantage de clients à risque, tout en maîtrisant le nombre de fausses alertes.