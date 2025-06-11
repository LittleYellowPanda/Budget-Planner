import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Tableau de Bord Financier",
    page_icon="💰",
    layout="wide"
)

# --- CHARGEMENT DES DONNÉES ---
# We use a try-except block to handle the case where the file doesn't exist yet
try:
    df = pd.read_csv('data/transactions.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Montant'] = pd.to_numeric(df['Montant'])
except FileNotFoundError:
    st.error("Le fichier `transactions.csv` est introuvable. Veuillez le créer dans le dossier `data/`.")
    st.stop() # Stop the app if the data file is not found

# --- DÉFINITION DES COMPTES ---
# These values would ideally be calculated from transactions, but for now, we can use the spreadsheet values as a starting point.
# This is a simplified model. A real implementation would calculate these from the transaction history.
comptes_epargne = {
    'Livret A': 1006.32,
    'Épargne Retraite': 200.00,
    'Épargne Vie (Multi-supports)': 200.00
}
compte_courant_valeur = df[df['Compte'] == 'CIC']['Montant'].sum() # Simplified calculation
total_en_vrai = sum(comptes_epargne.values()) + compte_courant_valeur

# --- SIDEBAR ---
st.sidebar.header("Filtres")
selected_month = st.sidebar.selectbox(
    "Sélectionner un mois",
    options=sorted(df['Date'].dt.strftime('%Y-%m').unique(), reverse=True)
)

# Filter data for the selected month
df_filtered = df[df['Date'].dt.strftime('%Y-%m') == selected_month]

# --- TABLEAU DE BORD PRINCIPAL ---
st.title("💰 Tableau de Bord Financier")
st.markdown(f"### Vue d'ensemble pour : {selected_month}")

# --- KPIs ---
total_depenses = abs(df_filtered[df_filtered['Type'] == 'Dépense']['Montant'].sum())
total_revenus = df_filtered[df_filtered['Type'] == 'Revenu']['Montant'].sum()
epargne_du_mois = total_revenus - total_depenses

col1, col2, col3 = st.columns(3)
col1.metric("Revenus du Mois", f"{total_revenus:,.2f} €")
col2.metric("Dépenses du Mois", f"{total_depenses:,.2f} €")
col3.metric("Capacité d'Épargne", f"{epargne_du_mois:,.2f} €", delta=f"{epargne_du_mois - 0:,.2f} €")

st.markdown("---")

# --- GRAPHIQUES ---
col1, col2 = st.columns(2)

with col1:
    # Donut chart for Savings Allocation
    st.subheader("Répartition de l'Épargne")
    epargne_df = pd.DataFrame(list(comptes_epargne.items()), columns=['Compte', 'Valeur'])
    fig_donut = px.pie(
        epargne_df,
        names='Compte',
        values='Valeur',
        hole=0.5,
        title="Répartition de l'Épargne Totale"
    )
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_donut, use_container_width=True)

with col2:
    # Bar chart for Expenses by Category
    st.subheader("Dépenses par Catégorie")
    depenses_cat = df_filtered[df_filtered['Type'] == 'Dépense'].groupby('Categorie')['Montant'].sum().abs().sort_values(ascending=False)
    fig_bar = px.bar(
        depenses_cat,
        x=depenses_cat.index,
        y=depenses_cat.values,
        labels={'y': 'Montant (€)', 'x': 'Catégorie'},
        title=f"Dépenses pour {selected_month}"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- TABLEAU DES TRANSACTIONS RECENTES ---
st.subheader("Transactions Récentes du Mois")
st.dataframe(
    df_filtered[['Date', 'Description', 'Montant', 'Categorie', 'Compte']]
    .sort_values(by="Date", ascending=False)
    .style.format({'Date': '{:%d-%m-%Y}', 'Montant': '{:,.2f} €'})
)