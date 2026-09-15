import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# CONFIGURATION
# ============================================================

# Configuration générale de l'application Streamlit :
# titre affiché dans l'onglet, icône et organisation de la page.
st.set_page_config(
    page_title="Telco Customer Churn",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# STYLE
# ============================================================

# Personnalisation de l'interface avec du CSS.
# L'objectif est d'avoir un dashboard cohérent et plus lisible
# qu'une interface Streamlit par défaut.
st.markdown(
    """
    <style>

    .stApp {
        background: #f6f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    [data-testid="stSidebar"] {
        background: #071A33;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .sidebar-title {
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .sidebar-subtitle {
        font-size: 13px;
        opacity: 0.7;
        margin-bottom: 25px;
    }

    .header-box {
        background: linear-gradient(135deg, #071A33 0%, #123C69 100%);
        border-radius: 18px;
        padding: 28px 32px;
        margin-bottom: 24px;
        color: white;
        box-shadow: 0 8px 25px rgba(7, 26, 51, 0.12);
    }

    .header-title {
        font-size: 34px;
        font-weight: 750;
        margin: 0;
        line-height: 1.15;
    }

    .header-subtitle {
        font-size: 15px;
        margin-top: 8px;
        opacity: 0.78;
    }

    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #e9edf3;
        box-shadow: 0 5px 18px rgba(7, 26, 51, 0.06);
        min-height: 125px;
    }

    .kpi-label {
        color: #6b7280;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #071A33;
        font-size: 28px;
        font-weight: 750;
        line-height: 1;
    }

    .kpi-description {
        color: #9ca3af;
        font-size: 12px;
        margin-top: 9px;
    }

    .section-title {
        color: #071A33;
        font-size: 21px;
        font-weight: 700;
        margin-top: 28px;
        margin-bottom: 14px;
    }

    .insight-box {
        background: #fff1f6;
        border-left: 5px solid #e83e8c;
        border-radius: 10px;
        padding: 15px 18px;
        margin-bottom: 10px;
        color: #273142;
        font-size: 14px;
    }

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 12px;
        padding-top: 35px;
        padding-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

# @st.cache_data évite de relire et retraiter le fichier
# à chaque interaction avec le dashboard.
@st.cache_data
def load_data():

    # Chemin vers le fichier de données utilisé par le dashboard.
    path = "data/raw/telco-customer-churn.csv"

    # Lecture du fichier CSV avec Pandas.
    df = pd.read_csv(path)

    # Certaines valeurs de TotalCharges sont vides.
    # Elles sont d'abord remplacées par des valeurs manquantes.
    df["TotalCharges"] = df["TotalCharges"].replace(
        r"^\s*$",
        pd.NA,
        regex=True
    )

    # Conversion de TotalCharges en variable numérique.
    # Les valeurs qui ne peuvent pas être converties deviennent NaN.
    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    # Pour les 11 clients concernés, TotalCharges est remplacé par 0.
    df["TotalCharges"] = df["TotalCharges"].fillna(0)

    return df


# Gestion du cas où le fichier de données n'est pas trouvé.
# Cela permet d'afficher un message clair au lieu de laisser
# l'application générer une erreur incompréhensible.
try:
    df = load_data()

except FileNotFoundError:

    st.error(
        "Le fichier data/raw/telco-customer-churn.csv est introuvable."
    )

    # Arrête l'exécution du dashboard si les données ne sont pas disponibles.
    st.stop()


# ============================================================
# VARIABLES
# ============================================================

# Création d'un libellé plus lisible pour l'affichage du statut client.
# La variable originale Churn est conservée pour les calculs.
df["Churn_Label"] = df["Churn"].map(
    {
        "Yes": "Churn",
        "No": "No Churn"
    }
)


# ============================================================
# SIDEBAR
# ============================================================

# Titre et sous-titre affichés dans la barre latérale.
st.sidebar.markdown(
    """
    <div class="sidebar-title">
        Telco Analytics
    </div>

    <div class="sidebar-subtitle">
        Customer Churn Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### Filtres")


# Récupération des différentes valeurs disponibles
# afin de les proposer dans les filtres.
contract_options = sorted(
    df["Contract"].dropna().unique().tolist()
)

internet_options = sorted(
    df["InternetService"].dropna().unique().tolist()
)

payment_options = sorted(
    df["PaymentMethod"].dropna().unique().tolist()
)


# Filtre sur le type de contrat.
# Toutes les valeurs sont sélectionnées par défaut.
selected_contract = st.sidebar.multiselect(
    "Contrat",
    options=contract_options,
    default=contract_options
)

# Filtre sur le service Internet.
selected_internet = st.sidebar.multiselect(
    "Service Internet",
    options=internet_options,
    default=internet_options
)

# Filtre sur le mode de paiement.
selected_payment = st.sidebar.multiselect(
    "Mode de paiement",
    options=payment_options,
    default=payment_options
)

# Filtre permettant de sélectionner tous les clients,
# uniquement les churners ou uniquement les non-churners.
selected_churn = st.sidebar.selectbox(
    "Statut client",
    options=[
        "Tous",
        "Churn",
        "No Churn"
    ]
)


# ============================================================
# FILTRAGE
# ============================================================

# Application des trois premiers filtres.
# .isin() permet de conserver uniquement les lignes
# correspondant aux valeurs sélectionnées.
filtered_df = df[
    df["Contract"].isin(selected_contract)
    & df["InternetService"].isin(selected_internet)
    & df["PaymentMethod"].isin(selected_payment)
].copy()


# Le filtre Churn est appliqué uniquement lorsque
# l'utilisateur ne souhaite pas afficher tous les clients.
if selected_churn != "Tous":

    filtered_df = filtered_df[
        filtered_df["Churn_Label"] == selected_churn
    ]


# ============================================================
# KPI
# ============================================================

# Nombre de clients correspondant aux filtres.
nb_clients = len(filtered_df)

# Nombre de clients ayant effectivement churné.
nb_churn = int(
    (filtered_df["Churn"] == "Yes").sum()
)


# Calcul des indicateurs uniquement si le dataframe
# contient au moins un client.
if nb_clients > 0:

    # Taux de churn parmi les clients actuellement filtrés.
    churn_rate = (
        nb_churn / nb_clients
    ) * 100

    # Ancienneté moyenne des clients.
    avg_tenure = filtered_df["tenure"].mean()

    # Montant moyen des charges mensuelles.
    avg_monthly = filtered_df["MonthlyCharges"].mean()

else:

    # Valeurs par défaut si aucun client ne correspond aux filtres.
    churn_rate = 0
    avg_tenure = 0
    avg_monthly = 0


# Mise en forme des valeurs avant leur affichage dans les KPI.
clients_display = f"{nb_clients:,}".replace(",", " ")
churn_display = f"{nb_churn:,}".replace(",", " ")

churn_rate_display = f"{churn_rate:.1f}%"
tenure_display = f"{avg_tenure:.1f}"
monthly_display = f"{avg_monthly:.2f} €"


# ============================================================
# HEADER
# ============================================================

# En-tête principal du dashboard.
st.html(
    """
    <div class="header-box">

        <div class="header-title">
            Telco Customer Churn
        </div>

        <div class="header-subtitle">
            Analyse interactive du comportement et du risque
            de résiliation des clients
        </div>

    </div>
    """
)


# ============================================================
# KPI CARDS
# ============================================================

# Création de cinq colonnes pour afficher les indicateurs
# principaux sur une seule ligne.
col1, col2, col3, col4, col5 = st.columns(5)


# Nombre total de clients après application des filtres.
with col1:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                CLIENTS
            </div>

            <div class="kpi-value">
                {clients_display}
            </div>

            <div class="kpi-description">
                Clients analysés
            </div>

        </div>
        """
    )


# Nombre de clients ayant churné.
with col2:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                CHURN
            </div>

            <div class="kpi-value">
                {churn_display}
            </div>

            <div class="kpi-description">
                Clients ayant résilié
            </div>

        </div>
        """
    )


# Taux de churn calculé sur les clients actuellement filtrés.
with col3:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                TAUX DE CHURN
            </div>

            <div class="kpi-value">
                {churn_rate_display}
            </div>

            <div class="kpi-description">
                Part des clients churn
            </div>

        </div>
        """
    )


# Ancienneté moyenne des clients sélectionnés.
with col4:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                ANCIENNETÉ MOYENNE
            </div>

            <div class="kpi-value">
                {tenure_display}
            </div>

            <div class="kpi-description">
                Mois en moyenne
            </div>

        </div>
        """
    )


# Montant moyen des charges mensuelles.
with col5:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                CHARGES MENSUELLES
            </div>

            <div class="kpi-value">
                {monthly_display}
            </div>

            <div class="kpi-description">
                Moyenne mensuelle
            </div>

        </div>
        """
    )


# ============================================================
# TABS
# ============================================================

# Organisation du dashboard en trois onglets :
# une vue globale, une analyse des profils et les données filtrées.
tab_overview, tab_profiles, tab_data = st.tabs(
    [
        "Vue d'ensemble",
        "Profils clients",
        "Données"
    ]
)


# ============================================================
# TAB 1 — VUE D'ENSEMBLE
# ============================================================

with tab_overview:

    st.html(
        """
        <div class="section-title">
            Analyse du churn
        </div>
        """
    )


    # ========================================================
    # CONTRAT + INTERNET
    # ========================================================

    # Deux graphiques sont affichés côte à côte.
    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # CONTRAT
    # --------------------------------------------------------

    with col1:

        # Pour chaque type de contrat, calcul du pourcentage
        # de clients ayant churné.
        contract_df = (
            filtered_df
            .groupby("Contract")["Churn"]
            .apply(
                lambda x: (x == "Yes").mean() * 100
            )
            .reset_index(name="Churn Rate")
        )


        # Création du graphique en barres avec Plotly Express.
        fig_contract = px.bar(
            contract_df,
            x="Contract",
            y="Churn Rate",
            title="Taux de churn par type de contrat",
            labels={
                "Contract": "Contrat",
                "Churn Rate": "Taux de churn (%)"
            },
            text_auto=".1f"
        )


        # Personnalisation de l'apparence du graphique.
        fig_contract.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            )
        )


        # Affichage du graphique dans Streamlit.
        st.plotly_chart(
            fig_contract,
            width="stretch"
        )


    # --------------------------------------------------------
    # INTERNET
    # --------------------------------------------------------

    with col2:

        # Calcul du taux de churn pour chaque type
        # de service Internet.
        internet_df = (
            filtered_df
            .groupby("InternetService")["Churn"]
            .apply(
                lambda x: (x == "Yes").mean() * 100
            )
            .reset_index(name="Churn Rate")
        )


        # Graphique du taux de churn selon le service Internet.
        fig_internet = px.bar(
            internet_df,
            x="InternetService",
            y="Churn Rate",
            title="Taux de churn par service Internet",
            labels={
                "InternetService": "Service Internet",
                "Churn Rate": "Taux de churn (%)"
            },
            text_auto=".1f"
        )


        fig_internet.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            )
        )


        st.plotly_chart(
            fig_internet,
            width="stretch"
        )


    # ========================================================
    # PAIEMENT + ANCIENNETÉ
    # ========================================================

    # Deux autres analyses sont placées côte à côte.
    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # PAIEMENT
    # --------------------------------------------------------

    with col1:

        # Calcul du taux de churn pour chaque mode de paiement.
        payment_df = (
            filtered_df
            .groupby("PaymentMethod")["Churn"]
            .apply(
                lambda x: (x == "Yes").mean() * 100
            )
            .reset_index(name="Churn Rate")
        )


        fig_payment = px.bar(
            payment_df,
            x="PaymentMethod",
            y="Churn Rate",
            title="Taux de churn par mode de paiement",
            labels={
                "PaymentMethod": "Mode de paiement",
                "Churn Rate": "Taux de churn (%)"
            },
            text_auto=".1f"
        )


        fig_payment.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            ),
            xaxis_tickangle=-30
        )


        st.plotly_chart(
            fig_payment,
            width="stretch"
        )


    # --------------------------------------------------------
    # ANCIENNETÉ
    # --------------------------------------------------------

    with col2:

        # Copie du dataframe filtré pour pouvoir créer
        # une nouvelle variable sans modifier directement
        # le dataframe principal.
        tenure_df = filtered_df.copy()


        # Création des intervalles d'ancienneté.
        bins = [
            0,
            12,
            24,
            48,
            72
        ]


        # Libellés associés aux intervalles.
        labels = [
            "0–12 mois",
            "13–24 mois",
            "25–48 mois",
            "49–72 mois"
        ]


        # Transformation de l'ancienneté numérique
        # en catégories d'ancienneté.
        tenure_df["TenureGroup"] = pd.cut(
            tenure_df["tenure"],
            bins=bins,
            labels=labels,
            include_lowest=True
        )


        # Calcul du taux de churn pour chaque tranche d'ancienneté.
        tenure_churn = (
            tenure_df
            .groupby(
                "TenureGroup",
                observed=False
            )["Churn"]
            .apply(
                lambda x: (x == "Yes").mean() * 100
            )
            .reset_index(name="Churn Rate")
        )


        # Visualisation du churn selon les tranches d'ancienneté.
        fig_tenure = px.bar(
            tenure_churn,
            x="TenureGroup",
            y="Churn Rate",
            title="Taux de churn selon l'ancienneté",
            labels={
                "TenureGroup": "Ancienneté",
                "Churn Rate": "Taux de churn (%)"
            },
            text_auto=".1f"
        )


        fig_tenure.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            )
        )


        st.plotly_chart(
            fig_tenure,
            width="stretch"
        )


# ============================================================
# TAB 2 — PROFILS CLIENTS
# ============================================================

with tab_profiles:

    st.html(
        """
        <div class="section-title">
            Profil des clients
        </div>
        """
    )


    # ========================================================
    # CHARGES + SENIOR
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # CHARGES MENSUELLES
    # --------------------------------------------------------

    with col1:

        # Histogramme permettant de comparer la distribution
        # des charges mensuelles entre churners et non-churners.
        fig_monthly = px.histogram(
            filtered_df,
            x="MonthlyCharges",
            color="Churn_Label",
            nbins=30,
            barmode="overlay",
            opacity=0.75,
            title="Distribution des charges mensuelles",
            labels={
                "MonthlyCharges": "Charges mensuelles (€)",
                "Churn_Label": "Statut"
            }
        )


        fig_monthly.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            )
        )


        st.plotly_chart(
            fig_monthly,
            width="stretch"
        )


    # --------------------------------------------------------
    # SENIOR
    # --------------------------------------------------------

    with col2:

        # Calcul du taux de churn pour les clients seniors
        # et non seniors.
        senior_df = (
            filtered_df
            .groupby("SeniorCitizen")["Churn"]
            .apply(
                lambda x: (x == "Yes").mean() * 100
            )
            .reset_index(name="Churn Rate")
        )


        # Remplacement des valeurs 0 et 1 par des libellés
        # plus compréhensibles pour le graphique.
        senior_df["SeniorCitizen"] = senior_df[
            "SeniorCitizen"
        ].map(
            {
                0: "Non senior",
                1: "Senior"
            }
        )


        fig_senior = px.bar(
            senior_df,
            x="SeniorCitizen",
            y="Churn Rate",
            title="Taux de churn selon le statut senior",
            labels={
                "SeniorCitizen": "Profil",
                "Churn Rate": "Taux de churn (%)"
            },
            text_auto=".1f"
        )


        fig_senior.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            )
        )


        st.plotly_chart(
            fig_senior,
            width="stretch"
        )


    # ========================================================
    # PARTENAIRE + SUPPORT
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # PARTENAIRE
    # --------------------------------------------------------

    with col1:

        # Calcul du taux de churn selon la présence
        # ou l'absence d'un partenaire.
        partner_df = (
            filtered_df
            .groupby("Partner")["Churn"]
            .apply(
                lambda x: (x == "Yes").mean() * 100
            )
            .reset_index(name="Churn Rate")
        )


        fig_partner = px.bar(
            partner_df,
            x="Partner",
            y="Churn Rate",
            title="Taux de churn selon la présence d'un partenaire",
            labels={
                "Partner": "Partenaire",
                "Churn Rate": "Taux de churn (%)"
            },
            text_auto=".1f"
        )


        fig_partner.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            )
        )


        st.plotly_chart(
            fig_partner,
            width="stretch"
        )


    # --------------------------------------------------------
    # SUPPORT TECHNIQUE
    # --------------------------------------------------------

    with col2:

        # Calcul du taux de churn selon l'utilisation
        # du support technique.
        support_df = (
            filtered_df
            .groupby("TechSupport")["Churn"]
            .apply(
                lambda x: (x == "Yes").mean() * 100
            )
            .reset_index(name="Churn Rate")
        )


        fig_support = px.bar(
            support_df,
            x="TechSupport",
            y="Churn Rate",
            title="Taux de churn selon le support technique",
            labels={
                "TechSupport": "Support technique",
                "Churn Rate": "Taux de churn (%)"
            },
            text_auto=".1f"
        )


        fig_support.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            )
        )


        st.plotly_chart(
            fig_support,
            width="stretch"
        )


# ============================================================
# TAB 3 — DONNÉES
# ============================================================

with tab_data:

    st.html(
        """
        <div class="section-title">
            Données filtrées
        </div>
        """
    )


    # Nombre de clients correspondant aux filtres actuels.
    number_display = f"{len(filtered_df):,}".replace(
        ",",
        " "
    )


    st.write(
        f"**{number_display}** clients correspondent aux filtres sélectionnés."
    )


    # Colonnes utiles pour afficher un aperçu des données.
    display_columns = [
        "customerID",
        "gender",
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "tenure",
        "InternetService",
        "Contract",
        "PaymentMethod",
        "MonthlyCharges",
        "TotalCharges",
        "Churn"
    ]


    # Vérification que les colonnes demandées existent bien
    # avant de les afficher.
    display_columns = [
        column
        for column in display_columns
        if column in filtered_df.columns
    ]


    # Affichage interactif du dataframe filtré.
    st.dataframe(
        filtered_df[display_columns],
        width="stretch",
        hide_index=True
    )


# ============================================================
# INSIGHTS
# ============================================================

# Section consacrée aux principales observations calculées
# automatiquement à partir des données filtrées.
st.html(
    """
    <div class="section-title">
        Insights clés
    </div>
    """
)


# Les insights sont calculés uniquement lorsqu'au moins
# un client correspond aux filtres.
if len(filtered_df) > 0:

    # Calcul du taux de churn pour chaque type de contrat.
    contract_churn = (
        filtered_df
        .groupby("Contract")["Churn"]
        .apply(
            lambda x: (x == "Yes").mean() * 100
        )
    )


    # Recherche du contrat présentant le taux de churn maximum.
    highest_contract = contract_churn.idxmax()
    highest_contract_rate = contract_churn.max()


    # Même principe pour les différents services Internet.
    internet_churn = (
        filtered_df
        .groupby("InternetService")["Churn"]
        .apply(
            lambda x: (x == "Yes").mean() * 100
        )
    )


    # Identification du service Internet avec le taux
    # de churn le plus élevé.
    highest_internet = internet_churn.idxmax()
    highest_internet_rate = internet_churn.max()


    # Affichage de l'insight concernant le contrat.
    st.html(
        f"""
        <div class="insight-box">

            <strong>Contrat :</strong>
            le taux de churn le plus élevé concerne les clients
            avec un contrat
            <strong>{highest_contract}</strong>
            ({highest_contract_rate:.1f} %).

        </div>
        """
    )


    # Affichage de l'insight concernant le service Internet.
    st.html(
        f"""
        <div class="insight-box">

            <strong>Internet :</strong>
            le service
            <strong>{highest_internet}</strong>
            présente le taux de churn le plus élevé
            ({highest_internet_rate:.1f} %).

        </div>
        """
    )


    # Insight général concernant l'ancienneté.
    st.html(
        """
        <div class="insight-box">

            <strong>Ancienneté :</strong>
            les clients ayant une ancienneté plus faible présentent
            généralement un risque de churn plus important.

        </div>
        """
    )


    # Résultat du modèle final affiché dans le dashboard.
    st.html(
        """
        <div class="insight-box">

            <strong>Modèle ML :</strong>
            le Random Forest optimisé atteint un ROC-AUC de
            <strong>84,38 %</strong> sur le jeu de test.

        </div>
        """
    )


else:

    # Message affiché lorsqu'aucune donnée ne correspond
    # aux filtres sélectionnés.
    st.html(
        """
        <div class="insight-box">

            Aucun client ne correspond aux filtres sélectionnés.

        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

# Pied de page de l'application.
st.html(
    """
    <div class="footer">

        Telco Customer Churn · Machine Learning Project
        · L'École Multimédia

    </div>
    """
)