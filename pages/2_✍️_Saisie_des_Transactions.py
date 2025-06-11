import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Saisie des Transactions",
    page_icon="✍️",
    layout="centered"
)

# --- FONCTIONS DE GESTION DES DONNÉES ---
# We use caching to prevent reloading the CSV on every interaction.
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/transactions.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Date', 'Description', 'Montant', 'Categorie', 'Compte', 'Type'])
    # Ensure data types are correct after loading
    df['Date'] = pd.to_datetime(df['Date'])
    df['Montant'] = pd.to_numeric(df['Montant'])
    return df

def save_data(df):
    # Sort by date before saving to keep the file organized
    df.sort_values(by="Date", ascending=False, inplace=True)
    df.to_csv('data/transactions.csv', index=False)
    # We need to clear the cache so the next load_data() call reads the new file
    st.cache_data.clear()

# --- DÉFINITIONS DES LISTES ---
CATEGORIES = [
    'Alimentaire', 'Assurances', 'Culture & Sport', 'Divers', 'Épargne',
    'Frais Bancaires', 'Impôts & Amendes', 'Logement & Charges', 'Revenus',
    'Santé & Bien-être', 'Vêtements', 'Voiture & Vélo', 'Voyages', 'Virement'
]
COMPTES = [
    'CIC', 'Caisse d\'Épargne', 'Livret A', 'Épargne Retraite',
    'Épargne Vie (Multi-supports)', 'Portefeuille', 'Espèces'
]
TYPES_TRANSACTION = ['Dépense', 'Revenu', 'Virement']

# --- INTERFACE DE SAISIE (UNCHANGED) ---
st.title("✍️ Ajouter une nouvelle transaction")
with st.form("transaction_form", clear_on_submit=True):
    st.subheader("Détails de la transaction")
    col1, col2 = st.columns(2)
    with col1:
        date_transaction = st.date_input("Date", datetime.date.today())
        montant = st.number_input("Montant (€)", format="%.2f", step=10.0)
        compte = st.selectbox("Compte", options=COMPTES)
    with col2:
        description = st.text_input("Description (ex: Courses, Salaire, ...)")
        categorie = st.selectbox("Catégorie", options=CATEGORIES)
        type_transaction = st.radio("Type", options=TYPES_TRANSACTION, horizontal=True)
    submitted = st.form_submit_button("✅ Ajouter la transaction")

# --- LOGIQUE DE TRAITEMENT DU FORMULAIRE (UNCHANGED) ---
if submitted:
    df = load_data()
    if type_transaction == 'Dépense' and montant > 0:
        montant = -montant
        st.info("Le montant a été automatiquement converti en négatif pour une dépense.")
    elif type_transaction == 'Revenu' and montant < 0:
        montant = abs(montant)
        st.info("Le montant a été automatiquement converti en positif pour un revenu.")

    new_transaction = pd.DataFrame([{
        'Date': pd.to_datetime(date_transaction),
        'Description': description,
        'Montant': montant,
        'Categorie': categorie,
        'Compte': compte,
        'Type': type_transaction
    }])
    df_updated = pd.concat([df, new_transaction], ignore_index=True)
    save_data(df_updated)
    st.success("Transaction ajoutée avec succès !")
    st.balloons()
    st.rerun() # Rerun the script to show the new transaction immediately

# --- SECTION DE GESTION DES TRANSACTIONS (NEW) ---
st.markdown("---")
st.header("Gérer les transactions existantes")

df_full = load_data()

if df_full.empty:
    st.info("Aucune transaction à afficher.")
else:
    # Create a view of the dataframe for display, sorted by most recent
    df_view = df_full.sort_values(by="Date", ascending=False).copy()
    
    # Reset index to make it look clean in the UI, but keep original index to delete rows
    df_view.reset_index(drop=True, inplace=True)

    st.markdown("Cochez les lignes que vous souhaitez supprimer, puis cliquez sur le bouton.")
    
    # Use st.data_editor to display the dataframe with checkboxes
    edited_df = st.data_editor(
        df_view,
        key="data_editor",
        num_rows="dynamic", # Allows adding/deleting rows in UI, but we'll handle delete ourselves
        hide_index=True,
        column_config={
            "Date": st.column_config.DateColumn(
                "Date",
                format="DD/MM/YYYY",
            ),
            "Montant": st.column_config.NumberColumn(
                "Montant (€)",
                format="%.2f €",
            ),
        },
        disabled=df_view.columns # Make all columns read-only
    )

    # Add a button to trigger the deletion
    if st.button("❌ Supprimer les transactions sélectionnées"):
        # Get the indices of the selected rows from the session state
        selected_indices = st.session_state["data_editor"]["edited_rows"]
        
        if not selected_indices:
            st.warning("Veuillez sélectionner au moins une transaction à supprimer.")
        else:
            # The keys of the dictionary are the indices of the rows to delete
            indices_to_drop = list(selected_indices.keys())
            
            # Map the view indices back to the original dataframe indices
            original_indices_to_drop = df_view.iloc[indices_to_drop].index
            
            # Drop the rows from the original full dataframe
            df_full.drop(original_indices_to_drop, inplace=True)
            
            # Save the modified dataframe
            save_data(df_full)
            
            st.success(f"{len(indices_to_drop)} transaction(s) supprimée(s) avec succès !")
            
            # Rerun the script to refresh the page and show the updated list
            st.rerun()