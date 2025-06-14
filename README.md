

# Mon Tableau de Bord Budgétaire Personnel 💰

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-red.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

Bienvenue sur votre tableau de bord financier personnel ! Cette application, construite avec Streamlit, est conçue pour vous aider à suivre, analyser et gérer vos finances personnelles en vous basant sur les principes de la gestion budgétaire saine, inspirés par la communauté `r/vosfinances`.

*(N'hésitez pas à ajouter une capture d'écran de votre tableau de bord ici !)*
`![App Screenshot](assets/screenshot_placeholder.png)`

## ✨ Fonctionnalités

L'application est organisée en quatre pages principales pour un flux de travail intuitif :

*   **💡 Conseils & Stratégie :** Un rappel constant de votre philosophie financière, avec la feuille de route visuelle et les principes clés pour rester sur la bonne voie.
*   **✍️ Saisie des Transactions :** Le cœur de l'application. Un formulaire simple pour ajouter de nouvelles dépenses, revenus ou virements, et un tableau interactif pour supprimer les erreurs.
*   **📊 Tableau de Bord :** Une vue d'ensemble mensuelle de votre situation financière avec des indicateurs clés (KPIs) et des graphiques visuels sur vos dépenses et la répartition de votre épargne.
*   **🔍 Analyse Détaillée :** Des outils puissants pour explorer vos données sur n'importe quelle période, avec des filtres par catégorie, compte et type de transaction.

## 📂 Structure du Projet

```
mon_budget_app/
├── Dockerfile              # Instructions pour construire l'image Docker
├── README.md               # Ce fichier
├── main_app.py             # Point d'entrée de l'application Streamlit
├── requirements.txt        # Dépendances Python
├── data/
│   └── transactions.csv    # Votre base de données ! Toutes les transactions sont ici.
├── pages/
│   ├── 1_📊_Tableau_de_Bord.py
│   ├── 2_✍️_Saisie_des_Transactions.py
│   ├── 3_🔍_Analyse_Détaillée.py
│   └── 4_💡_Conseils_&_Stratégie.py
└── assets/
    ├── flowchart.png       # L'organigramme de la stratégie financière
    └── screenshot_placeholder.png
```

## 🚀 Installation et Lancement

Vous avez deux options pour lancer l'application : localement avec un environnement Python, ou via Docker pour une portabilité maximale.

### Option 1 : Lancement Local

C'est la méthode la plus simple pour commencer si vous avez Python sur votre machine.

1.  **Clonez le projet (si ce n'est pas déjà fait) :**
    ```bash
    git clone <votre-url-de-repo>
    cd mon_budget_app
    ```

2.  **Créez un environnement virtuel et activez-le :**
    ```bash
    # Pour macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Pour Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Installez les dépendances :**
    ```bash
          
    pip install pip-tools
    pip-compile pyproject.toml -o requirements.txt

    ```

4.  **Lancez l'application Streamlit :**
    ```bash
    streamlit run main_app.py
    ```
    Votre navigateur devrait s'ouvrir automatiquement à l'adresse `http://localhost:8501`.

### Option 2 : Lancement avec Docker (Recommandé)

Cette méthode garantit que l'application fonctionne dans un environnement isolé et cohérent, et simplifie le déploiement.

1.  **Assurez-vous que Docker Desktop est installé et en cours d'exécution.**

2.  **Construisez l'image Docker :**
    Depuis la racine du projet, exécutez la commande suivante. Cela peut prendre quelques minutes la première fois.
    ```bash
    docker build -t mon-budget-app .
    ```

3.  **Lancez le conteneur Docker :**
    Cette commande lance l'application et, plus important encore, connecte le dossier `data` de votre machine au conteneur pour que vos données soient sauvegardées.

    ```bash
    docker run -p 8501:8501 -v "$(pwd)/data":/app/data --name my-budget-container mon-budget-app
    ```
    *   **Sur Windows (CMD) :** Remplacez `$(pwd)` par `%cd%`.
    *   **Sur Windows (PowerShell) :** Remplacez `$(pwd)` par `${pwd}`.

    Ouvrez votre navigateur à l'adresse `http://localhost:8501` pour utiliser l'application.

## 🛠️ Comment Utiliser l'Application

1.  **Commencez par la page `💡 Conseils & Stratégie`** pour vous remémorer vos objectifs.
2.  **Allez sur `✍️ Saisie des Transactions`** pour ajouter vos dépenses et revenus au fur et à mesure. Si vous faites une erreur, vous pouvez cocher la ou les lignes incorrectes et les supprimer avec le bouton dédié.
3.  **Consultez le `📊 Tableau de Bord`** régulièrement pour avoir une vue rapide de votre situation pour le mois en cours.
4.  **Utilisez `🔍 Analyse Détaillée`** pour des analyses plus poussées. Par exemple, pour voir combien vous avez dépensé en "Alimentaire" au cours des 6 derniers mois.

## 💾 Persistance des Données

**Important :** Toutes vos données financières sont stockées dans le fichier `data/transactions.csv`. L'application lit et écrit dans ce fichier.

*   **En mode local**, le fichier est directement modifié sur votre ordinateur.
*   **En mode Docker**, il est **crucial** d'utiliser l'option `-v` (volume) dans la commande `docker run`. Cela garantit que le fichier `transactions.csv` à l'intérieur du conteneur est en fait le fichier sur votre machine. Sans cela, toutes les transactions que vous ajoutez seraient perdues à chaque redémarrage du conteneur.

---
