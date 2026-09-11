import pandas as pd
import streamlit as st
import plotly.express as px

# =========================
# Configuration
# =========================

st.set_page_config(
    page_title="Telco Customer Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# Chargement des données
# =========================

DATA_PATH = "data/processed/telco_customer_churn_clean.csv"

df = pd.read_csv(DATA_PATH)

# Conversion de la cible
df["Churn_numeric"] = df["Churn"].map({"No": 0, "Yes": 1})

# Groupes d'ancienneté
df["tenure_group"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 72],
    labels=["0–12 mois", "13–24 mois", "25–48 mois", "49–72 mois"]
)

# =========================
# Titre
# =========================

st.title("📊 Telco Customer Churn Dashboard")
st.markdown(
    "Dashboard interactif permettant d'explorer les caractéristiques "
    "associées au churn des clients."
)

# =========================
# Filtres
# =========================

st.sidebar.header("Filtres")

contract_options = sorted(df["Contract"].dropna().unique())
internet_options = sorted(df["InternetService"].dropna().unique())
payment_options = sorted(df["PaymentMethod"].dropna().unique())

selected_contract = st.sidebar.multiselect(
    "Contrat",
    contract_options,
    default=contract_options
)

selected_internet = st.sidebar.multiselect(
    "Service Internet",
    internet_options,
    default=internet_options
)

selected_payment = st.sidebar.multiselect(
    "Mode de paiement",
    payment_options,
    default=payment_options
)

filtered_df = df[
    df["Contract"].isin(selected_contract)
    & df["InternetService"].isin(selected_internet)
    & df["PaymentMethod"].isin(selected_payment)
].copy()

# =========================
# KPI
# =========================

total_customers = len(filtered_df)

churned_customers = int(
    (filtered_df["Churn"] == "Yes").sum()
)

churn_rate = (
    churned_customers / total_customers * 100
    if total_customers > 0
    else 0
)

average_tenure = (
    filtered_df["tenure"].mean()
    if total_customers > 0
    else 0
)

average_monthly_charges = (
    filtered_df["MonthlyCharges"].mean()
    if total_customers > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Clients",
    f"{total_customers:,}".replace(",", " ")
)

col2.metric(
    "Clients ayant churné",
    f"{churned_customers:,}".replace(",", " ")
)

col3.metric(
    "Taux de churn",
    f"{churn_rate:.1f}%"
)

col4.metric(
    "Charges mensuelles moyennes",
    f"{average_monthly_charges:.2f} €"
)

st.divider()

# =========================
# Graphiques
# =========================

if total_customers == 0:
    st.warning("Aucun client ne correspond aux filtres sélectionnés.")

else:

    # Churn par contrat
    churn_contract = (
        filtered_df.groupby("Contract", observed=True)["Churn_numeric"]
        .mean()
        .reset_index()
    )

    churn_contract["Churn Rate"] = (
        churn_contract["Churn_numeric"] * 100
    )

    fig_contract = px.bar(
        churn_contract,
        x="Contract",
        y="Churn Rate",
        title="Taux de churn selon le type de contrat",
        labels={
            "Contract": "Type de contrat",
            "Churn Rate": "Taux de churn (%)"
        },
        text_auto=".1f"
    )

    fig_contract.update_layout(yaxis_range=[0, 100])

    # Churn par service Internet
    churn_internet = (
        filtered_df.groupby("InternetService", observed=True)["Churn_numeric"]
        .mean()
        .reset_index()
    )

    churn_internet["Churn Rate"] = (
        churn_internet["Churn_numeric"] * 100
    )

    fig_internet = px.bar(
        churn_internet,
        x="InternetService",
        y="Churn Rate",
        title="Taux de churn selon le service Internet",
        labels={
            "InternetService": "Service Internet",
            "Churn Rate": "Taux de churn (%)"
        },
        text_auto=".1f"
    )

    fig_internet.update_layout(yaxis_range=[0, 100])

    # Churn par ancienneté
    churn_tenure = (
        filtered_df.groupby("tenure_group", observed=True)["Churn_numeric"]
        .mean()
        .reset_index()
    )

    churn_tenure["Churn Rate"] = (
        churn_tenure["Churn_numeric"] * 100
    )

    fig_tenure = px.bar(
        churn_tenure,
        x="tenure_group",
        y="Churn Rate",
        title="Taux de churn selon l'ancienneté",
        labels={
            "tenure_group": "Ancienneté",
            "Churn Rate": "Taux de churn (%)"
        },
        text_auto=".1f"
    )

    fig_tenure.update_layout(yaxis_range=[0, 100])

    # Distribution des charges mensuelles
    fig_charges = px.box(
        filtered_df,
        x="Churn",
        y="MonthlyCharges",
        title="Distribution des charges mensuelles selon le churn",
        labels={
            "Churn": "Churn",
            "MonthlyCharges": "Charges mensuelles (€)"
        }
    )

    # Affichage
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            fig_contract,
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            fig_internet,
            use_container_width=True
        )

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(
            fig_tenure,
            use_container_width=True
        )

    with col4:
        st.plotly_chart(
            fig_charges,
            use_container_width=True
        )

# =========================
# Tableau de données
# =========================

st.divider()

st.subheader("Données filtrées")

display_columns = [
    "customerID",
    "Contract",
    "InternetService",
    "PaymentMethod",
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
    "Churn"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)