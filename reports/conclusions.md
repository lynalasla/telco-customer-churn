# Conclusion du projet

## 1. Objectif du projet

L'objectif de ce projet était de développer un modèle de Machine Learning capable de prédire le risque de résiliation d'un client dans le secteur des télécommunications.

Le projet a suivi une démarche complète de Data Science : analyse et préparation des données, exploration des variables, prétraitement, entraînement de plusieurs modèles, optimisation des hyperparamètres et évaluation finale sur un jeu de test indépendant.

## 2. Principaux enseignements de l'analyse

L'analyse exploratoire a permis d'identifier plusieurs variables associées au churn.

Le taux global de résiliation est de **26,54 %**, ce qui représente une proportion significative de clients susceptibles de quitter l'entreprise.

Le type de contrat présente notamment une association importante avec le churn : le taux de résiliation est beaucoup plus élevé pour les contrats mensuels que pour les contrats d'un ou deux ans.

Les clients ayant une ancienneté plus faible présentent également un taux de churn plus élevé. À l'inverse, les clients ayant une ancienneté importante sont globalement moins concernés par les résiliations.

Les charges mensuelles sont en moyenne plus élevées chez les clients ayant résilié leur contrat. Le type de service Internet et le mode de paiement présentent également des différences selon le statut de churn.

Ces observations constituent des **associations statistiques** et ne permettent pas d'établir de relations causales.

## 3. Comparaison des modèles

Trois algorithmes ont été étudiés :

* Régression Logistique
* Decision Tree
* Random Forest

Dans une première expérimentation, les modèles ont été comparés avant optimisation à partir de plusieurs indicateurs : Accuracy, Precision, Recall, F1-score et ROC-AUC.

La Régression Logistique obtient les meilleurs résultats de cette première comparaison, tandis que le Decision Tree présente les performances les plus faibles. Le Random Forest présente toutefois un potentiel intéressant qui justifie son optimisation.

Une recherche d'hyperparamètres avec GridSearchCV et validation croisée a ensuite été réalisée pour chaque modèle.

Après optimisation, les performances obtenues sur le jeu de test sont :

| Modèle                | Accuracy | Precision | Recall | F1-score | ROC-AUC |
| --------------------- | -------: | --------: | -----: | -------: | ------: |
| Régression Logistique |   0.8055 |    0.6572 | 0.5588 |   0.6040 |  0.8413 |
| Decision Tree         |   0.7956 |    0.6335 | 0.5455 |   0.5862 |  0.8270 |
| Random Forest         |   0.8041 |    0.6667 | 0.5241 |   0.5868 |  0.8438 |

La validation croisée réalisée pendant l'optimisation a donné les ROC-AUC suivants :

* Régression Logistique : **0,8460**
* Decision Tree : **0,8184**
* Random Forest : **0,8435**

Ces résultats montrent que les modèles présentent des performances proches après optimisation. Le choix du modèle final doit donc tenir compte de plusieurs métriques et du besoin métier.

## 4. Modèle final

Le **Random Forest optimisé** a été retenu comme modèle final principalement en raison de son meilleur ROC-AUC sur le jeu de test (**0,8438**) et de sa meilleure précision (**0,6667**) parmi les trois modèles optimisés.

Ses paramètres principaux sont :

* `n_estimators = 200`
* `max_depth = 10`
* `min_samples_split = 2`
* `min_samples_leaf = 2`

La matrice de confusion obtenue est :

|            | Prédit : Non | Prédit : Oui |
| ---------- | -----------: | -----------: |
| Réel : Non |          937 |           98 |
| Réel : Oui |          178 |          196 |

Le modèle identifie correctement **196 clients sur 374 ayant réellement résilié**, soit un recall de **52,41 %**.

Le ROC-AUC de **0,8438** indique une bonne capacité du modèle à distinguer les clients ayant résilié leur contrat des autres. Cependant, le recall de **52,41 %** montre qu'une partie importante des churners n'est pas détectée.

La Régression Logistique obtient par ailleurs un meilleur recall (**55,88 %**) et un meilleur F1-score (**60,40 %**) sur le jeu de test. Si l'objectif métier était de maximiser la détection des clients à risque, elle pourrait donc constituer une alternative pertinente.

## 5. Variables importantes

L'analyse de l'importance des variables du Random Forest montre que les variables les plus contributives aux prédictions sont :

1. `tenure`
2. `TotalCharges`
3. `MonthlyCharges`
4. `InternetService_Fiber optic`
5. `PaymentMethod_Electronic check`
6. `Contract_Two year`
7. `Contract_One year`
8. `OnlineSecurity_Yes`
9. `TechSupport_Yes`
10. `PaperlessBilling_Yes`

L'ancienneté, les charges totales et les charges mensuelles sont donc particulièrement importantes pour les prédictions du modèle.

Cette importance ne signifie toutefois pas qu'une variable est directement responsable du churn : elle indique uniquement qu'elle contribue fortement aux prédictions du modèle.

## 6. Recommandations métier

Les résultats peuvent être utilisés comme base pour mettre en place une stratégie de prévention du churn.

L'entreprise pourrait notamment :

* identifier régulièrement les clients présentant un risque élevé de résiliation ;
* porter une attention particulière aux clients avec une faible ancienneté ;
* analyser les profils associés aux contrats mensuels ;
* proposer des offres de fidélisation adaptées aux clients à risque ;
* étudier les différences de comportement selon le type de service Internet et le mode de paiement ;
* utiliser les probabilités prédites par le modèle pour prioriser les actions commerciales.

L'objectif ne serait pas de cibler automatiquement tous les clients prédits comme churners, mais de fournir aux équipes commerciales un outil d'aide à la décision.

## 7. Limites du projet

Le modèle présente plusieurs limites.

Tout d'abord, son recall de **52,41 %** montre qu'une partie importante des clients qui résilient leur contrat n'est pas détectée.

De plus, les performances dépendent de la qualité et de la représentativité du dataset utilisé. Les comportements des clients peuvent évoluer dans le temps, ce qui nécessite une surveillance régulière des performances du modèle.

Enfin, les résultats obtenus sur ce dataset ne peuvent pas être généralisés automatiquement à toutes les entreprises de télécommunications.

## 8. Perspectives d'amélioration

Plusieurs améliorations pourraient être envisagées :

* optimiser le seuil de classification afin d'améliorer le recall lorsque la détection des churners est prioritaire ;
* tester d'autres algorithmes de Machine Learning, notamment XGBoost ou LightGBM ;
* utiliser des techniques adaptées au déséquilibre des classes ;
* analyser plus précisément les erreurs de classification, notamment les faux négatifs ;
* étudier la calibration des probabilités prédites ;
* enrichir le dataset avec des données comportementales et temporelles ;
* mettre en place un suivi des performances du modèle dans le temps ;
* intégrer le modèle dans une application ou un dashboard opérationnel ;
* réentraîner régulièrement le modèle avec de nouvelles données clients.

## 9. Conclusion générale

Ce projet a permis de mettre en œuvre une chaîne complète de Machine Learning pour la prédiction du churn client, depuis la préparation des données jusqu'à l'évaluation finale du modèle.

L'analyse exploratoire a permis d'identifier plusieurs variables associées au départ des clients, notamment le type de contrat, l'ancienneté et les charges mensuelles.

La comparaison des modèles a montré que les performances varient selon la métrique considérée. Après optimisation, le **Random Forest** obtient le meilleur ROC-AUC sur le jeu de test avec **0,8438**, ainsi que la meilleure précision avec **0,6667**. La **Régression Logistique** conserve cependant un meilleur recall et un meilleur F1-score.

Le Random Forest retenu constitue donc une **base pertinente pour un outil d'aide à la décision**, mais son recall de **52,41 %** montre qu'une amélioration reste nécessaire avant une éventuelle utilisation opérationnelle.

L'étape suivante consisterait notamment à travailler sur le seuil de classification, l'équilibre entre précision et recall, ainsi que le suivi des performances du modèle dans le temps.