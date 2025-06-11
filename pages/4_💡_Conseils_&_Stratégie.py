import streamlit as st
from PIL import Image

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Conseils & Stratégie",
    page_icon="💡",
    layout="wide"
)

# --- TITRE ---
st.title("💡 Stratégie Financière Personnelle")
st.markdown("Cette page résume la philosophie et les étapes clés de votre parcours financier, inspirées par `r/vosfinances`.")

st.markdown("---")

# --- AFFICHAGE DU FLOWCHART ---
st.header("Le Chemin vers la Sérénité Financière")
st.markdown("Suivez ces étapes dans l'ordre pour construire une base financière solide.")

# Load and display the flowchart image
try:
    image = Image.open('assets/flowchart.png')
    st.image(image, caption="Votre feuille de route financière, de l'épargne de précaution à l'investissement long terme.")
except FileNotFoundError:
    st.error("L'image `flowchart.png` est introuvable. Assurez-vous qu'elle se trouve dans le dossier `assets/`.")

st.markdown("---")

# --- CONSEILS DÉTAILLÉS ---
st.header("Principes et Pièges à Éviter")
st.markdown("Dépliez les sections ci-dessous pour revoir les conseils essentiels.")

# --- Section 1: Budget & Capacité d'Épargne ---
with st.expander("🎯 Construire son Budget et Définir sa Capacité d'Épargne"):
    st.subheader("Les 3 Piliers d'un Budget")
    st.markdown("""
    - **Revenus :** Salaires nets, aides, etc. C'est votre point de départ.
    - **Dépenses Obligatoires :** Loyer, crédits, factures, courses essentielles. Ce sont les dépenses non-négociables.
    - **Dépenses Discrétionnaires :** Loisirs, shopping, voyages. C'est ici que vous avez le plus de contrôle.
    """)
    st.subheader("Objectifs d'Épargne")
    st.success("""
    - **Correct :** Viser au moins **10%** de votre revenu net.
    - **Agressif :** Pousser jusqu'à **20%** ou plus si votre situation le permet.
    """)
    st.info("Un bon budget vous donne de la visibilité, pas de la frustration. Ajustez-le pour qu'il soit réaliste pour VOUS.")

# --- Section 2: Épargne de Précaution ---
with st.expander("🛡️ L'Importance de l'Épargne de Précaution"):
    st.subheader("Votre Coussin de Sécurité")
    st.markdown("""
    Le but est d'avoir de l'argent **facilement accessible** pour couvrir les imprévus (panne de voiture, problème de santé, etc.) sans avoir à s'endetter ou à vendre des investissements en panique.
    """)
    st.warning("""
    **Priorité absolue :** Avant tout investissement risqué, constituez cette épargne. L'objectif classique est de couvrir **3 à 6 mois de dépenses obligatoires**.
    """)

# --- Section 3: Investissements - Les Pièges à Éviter ---
with st.expander("🚫 Investissements : Les Pièges à Éviter"):
    st.subheader("Les Règles d'Or")
    st.markdown("""
    1.  **Méfiez-vous des "conseillers" bancaires :** Leurs objectifs ne sont pas toujours les vôtres. Ils vendent des produits avec des frais élevés.
    2.  **L'âge compte :** Une Assurance-Vie ou un PER n'est souvent pas pertinent pour un jeune de moins de 30 ans. Un PEA et des livrets suffisent.
    3.  **Les frais sont votre pire ennemi :** Des frais de gestion annuels de 2% peuvent dévorer près de la moitié de votre performance sur le long terme. Cherchez des frais bas (<1%).
    4.  **La défiscalisation n'est pas un objectif :** Ne choisissez pas un investissement (ex: Pinel) juste pour l'avantage fiscal. La rentabilité du sous-jacent prime.
    5.  **Simplicité > Complexité :** Inutile d'avoir 10 comptes différents. Un ou deux supports bien diversifiés (comme un ETF World sur PEA) sont plus efficaces.
    6.  **Pas de rendement élevé sans risque élevé :** Si on vous promet plus que le Livret A "sans risque", c'est soit un mensonge, soit un risque que vous ne voyez pas.
    """)

# --- Section 4: Objectifs d'Investissement ---
with st.expander("📈 Les Grands Objectifs d'Investissement"):
    st.subheader("Pourquoi Investir ?")
    st.markdown("""
    - **Apport pour Résidence Principale :** Viser 10% à 20% de la valeur du bien.
    - **Préparer la Retraite :** Compléter votre pension pour maintenir votre niveau de vie.
    - **Transmission :** Constituer un patrimoine à léguer à vos descendants.
    """)
    st.info("Chaque euro investi doit avoir un but. Définir vos objectifs vous aidera à choisir la bonne stratégie et à tenir le cap pendant les tempêtes.")