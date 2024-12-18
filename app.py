import streamlit as st
import pandas as pd
import sqlite3

# Fonction pour configurer la base de données SQLite
def init_db():
    conn = sqlite3.connect("pec_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS demandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            docteur_nom TEXT,
            docteur_prenom TEXT,
            docteur_telephone TEXT,
            docteur_mail TEXT,
            patient_nom TEXT,
            patient_prenom TEXT,
            patient_telephone TEXT,
            patient_traitement TEXT,
            patient_autres TEXT,
            date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Sauvegarder une demande
def save_demande(docteur_nom, docteur_prenom, docteur_telephone, docteur_mail,
                 patient_nom, patient_prenom, patient_telephone, patient_traitement, patient_autres):
    conn = sqlite3.connect("pec_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO demandes (docteur_nom, docteur_prenom, docteur_telephone, docteur_mail,
                              patient_nom, patient_prenom, patient_telephone, patient_traitement, patient_autres)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (docteur_nom, docteur_prenom, docteur_telephone, docteur_mail,
          patient_nom, patient_prenom, patient_telephone, patient_traitement, patient_autres))
    conn.commit()
    conn.close()

# Afficher les données dans un tableau de bord
def display_dashboard():
    conn = sqlite3.connect("pec_data.db")
    df = pd.read_sql_query("SELECT * FROM demandes", conn)
    conn.close()
    st.dataframe(df)

# Initialisation de la base de données
init_db()

# Authentification
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Entrez le mot de passe :", type="password")
    if password == "monmotdepasse":  # Changez ce mot de passe
        st.session_state.authenticated = True
        st.success("Authentifié avec succès !")
    else:
        st.error("Mot de passe incorrect.")
else:
    # Choix entre tableau de bord et formulaire
    page = st.sidebar.selectbox("Navigation", ["Formulaire", "Tableau de Bord"])

    if page == "Formulaire":
        # Formulaire pour les informations du docteur
        docteur_nom = st.text_input("Nom du Docteur 🧑🏻‍⚕️👩🏻‍⚕️")
        docteur_prenom = st.text_input("Prénom du Docteur")
        docteur_telephone = st.text_input("Téléphone du Docteur ☎️")
        docteur_mail = st.text_input("Email du Docteur 📧")

        # Formulaire pour les informations du patient
        patient_nom = st.text_input("Nom du Patient 🤒")
        patient_prenom = st.text_input("Prénom du Patient")
        patient_telephone = st.text_input("Téléphone du Patient ☎️")
        patient_traitement = st.text_area("Traitement 💊")
        patient_autres = st.text_area("Autre(s) (La voie d'abord, la durée,...) 🗒️")

        if st.button("Envoyer la prise en charge à l'équipe Bastide-Médical"):
            if not (docteur_nom and docteur_prenom and docteur_telephone and docteur_mail and patient_nom and patient_prenom and patient_telephone):
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                save_demande(docteur_nom, docteur_prenom, docteur_telephone, docteur_mail,
                             patient_nom, patient_prenom, patient_telephone, patient_traitement, patient_autres)
                st.success("Prise en charge sauvegardée et email envoyé !")
    elif page == "Tableau de Bord":
        st.title("Tableau de Bord des Prises en Charge")
        display_dashboard()
