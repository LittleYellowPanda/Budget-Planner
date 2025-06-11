import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Analyse Détaillée",
    page_icon="🔍",
    layout="wide"
)

# --- FONCTION POUR CHARGER LES DONNÉES ---
@st.cache_data # Use Streamlit's caching to load data only once
def load_data():
    try:
        df = pd.read_csv('data/transactions.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Montant'] = pd.to_numeric(df['Montant'])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Description', 'Montant', 'Categorie', 'Compte', 'Type'])

df = load_data()

# --- INTERFACE ---
st.title("🔍 Analyse Détaillée des Transactions")
st.markdown("Utilisez les filtres dans la barre latérale pour explorer vos données financières.")

# --- SIDEBAR AVEC LES FILTRES ---
st.sidebar.header("Filtres d'Analyse")

# Check if the dataframe is empty before creating filters
if df.empty:
    st.warning("Aucune transaction n'a été enregistrée. Veuillez en ajouter via la page 'Saisie des Transactions'.")
    st.stop()

# Filter by Date Range
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

date_range = st.sidebar.date_input(
    "Sélectionnez une plage de dates",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# We need to handle the case where the user selects a single day
start_date, end_date = date_range if len(date_range) == 2 else (date_range[0], date_range[0])

# Filter by Category, Account, and Type
# We use multiselect to allow choosing multiple options
all_categories = df['Categorie'].unique()
selected_categories = st.sidebar.multiselect("Catégories", options=all_categories, default=all_categories)

all_accounts = df['Compte'].unique()
selected_accounts = st.sidebar.multiselect("Comptes", options=all_accounts, default=all_accounts)

all_types = df['Type'].unique()
selected_types = st.sidebar.multiselect("Types de transaction", options=all_types, default=all_types)


# --- APPLICATION DES FILTRES ---
# We create a boolean mask for each filter and combine them
mask = (
    (df['Date'].dt.date >= start_date) &
    (df['Date'].dt.date <= end_date) &
    (df['Categorie'].isin(selected_categories)) &
    (df['Compte'].isin(selected_accounts)) &
    (df['Type'].isin(selected_types))
)
df_filtered = df[mask]

# --- AFFICHAGE DES RÉSULTATS ---
if df_filtered.empty:
    st.warning("Aucune transaction ne correspond aux filtres sélectionnés.")
else:
    # --- KPIs pour la période sélectionnée ---
    total_depenses = df_filtered[df_filtered['Type'] == 'Dépense']['Montant'].sum()
    total_revenus = df_filtered[df_filtered['Type'] == 'Revenu']['Montant'].sum()
    solde = total_revenus + total_depenses # Expenses are already negative

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenus", f"{total_revenus:,.2f} €")
    col2.metric("Total Dépenses", f"{total_depenses:,.2f} €")
    col3.metric("Solde", f"{solde:,.2f} €", delta=f"{solde:,.2f} €")

    st.markdown("---")

    # --- GRAPHIQUES ---
    col1, col2 = st.columns(2)

    with col1:
        # Treemap for expense breakdown
        st.subheader("Répartition des Dépenses")
        df_depenses = df_filtered[df_filtered['Type'] == 'Dépense'].copy()
        if not df_depenses.empty:
            df_depenses['Montant'] = df_depenses['Montant'].abs()
            fig_treemap = px.treemap(
                df_depenses,
                path=[px.Constant("Toutes les dépenses"), 'Categorie'],
                values='Montant',
                title="Dépenses par Catégorie",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig_treemap.update_layout(margin = dict(t=50, l=25, r=25, b=25))
            st.plotly_chart(fig_treemap, use_container_width=True)
        else:
            st.info("Aucune dépense dans la période sélectionnée.")

    with col2:
        # Line chart for cash flow over time
        st.subheader("Flux de Trésorerie")
        # Resample data by day to see daily net flow
        df_flow = df_filtered.set_index('Date').resample('D')['Montant'].sum().reset_index()
        fig_line = px.line(
            df_flow,
            x='Date',
            y='Montant',
            title="Solde Journalier (Revenus - Dépenses)"
        )
        fig_line.add_hline(y=0, line_dash="dot", line_color="red")
        st.plotly_chart(fig_line, use_container_width=True)

    # --- TABLEAU DE DONNÉES DÉTAILLÉ ---
    st.subheader("Détail des Transactions Filtrées")
    st.dataframe(
        df_filtered.sort_values(by="Date", ascending=False).style.format({
            'Date': '{:%d-%m-%Y}',
            'Montant': '{:,.2f} €'
        }),
        use_container_width=True
    )