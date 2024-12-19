import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import sqlite3

# Initialisation de la base de données SQLite
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

def display_dashboard():
    conn = sqlite3.connect("pec_data.db")
    df = pd.read_sql_query("SELECT * FROM demandes", conn)
    conn.close()
    st.dataframe(df)

# Initialiser la base de données
init_db()

# Configuration des utilisateurs
names = ["Margalet", "Romain"]
usernames = ["Margalet", "Romain"]
hashed_passwords = [
    "RMARGA66", 
]  # Remplacez par vos mots de passe hachés
cookie_name = "streamlit_auth_cookie"
key = "random_signature_key"

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "dashboard_cookie_name",  # Clé de cookie pour sessions persistantes
    "random_key_for_signature",  # Clé pour signer les cookies (sécurisez-la)
    cookie_expiry_days=1,
)

# Interface de connexion
name, authentication_status, username = authenticator.login("Connexion", "main")

if authentication_status:
    # Authentifié avec succès
    st.sidebar.title(f"Bienvenue, {name}")
    option = st.sidebar.radio("Navigation", ["Formulaire", "Tableau de Bord"])

    if option == "Formulaire":
        st.title("Demande de Prise en Charge 🩺")
        docteur_nom = st.text_input("Nom du Docteur 🧑🏻‍⚕️👩🏻‍⚕️")
        docteur_prenom = st.text_input("Prénom du Docteur")
        docteur_telephone = st.text_input("Téléphone du Docteur ☎️")
        docteur_mail = st.text_input("Email du Docteur 📧")
        patient_nom = st.text_input("Nom du Patient 🤒")
        patient_prenom = st.text_input("Prénom du Patient")
        patient_telephone = st.text_input("Téléphone du Patient ☎️")
        patient_traitement = st.text_area("Traitement 💊")
        patient_autres = st.text_area("Autre(s) (La voie d'abord, la durée,...) 🗒️")

        if st.button("Envoyer la prise en charge"):
            if not (docteur_nom and docteur_prenom and docteur_telephone and docteur_mail and patient_nom and patient_prenom and patient_telephone):
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                save_demande(docteur_nom, docteur_prenom, docteur_telephone, docteur_mail,
                             patient_nom, patient_prenom, patient_telephone, patient_traitement, patient_autres)
                st.success("Prise en charge enregistrée avec succès.")
    elif option == "Tableau de Bord":
        st.title("Tableau de Bord des Prises en Charge")
        display_dashboard()

    # Bouton de déconnexion
    authenticator.logout("Déconnexion", "sidebar")
elif authentication_status is False:
    st.error("Nom d'utilisateur ou mot de passe incorrect.")
elif authentication_status is None:
    st.warning("Veuillez entrer vos identifiants.")
