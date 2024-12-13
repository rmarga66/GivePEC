import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import quote

# Configuration de l'email
def envoyer_email(destinataire, sujet, message):
    expediteur = "romainmargalet@gmail.com"  # Remplacez par votre adresse email
    mot_de_passe = "oipm xjxx lyab obeq"  # Remplacez par votre mot de passe

    try:
        msg = MIMEMultipart()
        msg['From'] = expediteur
        msg['To'] = destinataire
        msg['Subject'] = sujet

        msg.attach(MIMEText(message, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(expediteur, mot_de_passe)
            server.send_message(msg)

        st.success("Email envoyé avec succès!")
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de l'email: {e}")

# Interface principale de l'application
st.set_page_config(page_title="Prise en Charge Patient", page_icon="🩺", layout="centered")
st.title("Prise en Charge d'un Patient")
st.markdown("## Interface de demande de PEC")

# Formulaire pour les informations du docteur
docteur_nom = st.text_input("Nom du Docteur")
docteur_prenom = st.text_input("Prénom du Docteur")
docteur_telephone = st.text_input("Téléphone du Docteur")
docteur_mail = st.text_input("Email du Docteur")

# Formulaire pour les informations du patient
patient_nom = st.text_input("Nom du Patient")
patient_prenom = st.text_input("Prénom du Patient")
patient_telephone = st.text_input("Téléphone du Patient")
patient_traitement = st.text_area("Traitement")
patient_autres = st.text_area("Autre(s) Informations")

if st.button("Envoyer la demande de PEC"):
    if not (docteur_nom and docteur_prenom and docteur_telephone and docteur_mail and patient_nom and patient_prenom and patient_telephone):
        st.error("Veuillez remplir tous les champs obligatoires.")
    else:
        sujet = f"DEMANDE de PEC du DR {docteur_nom}"
        validation_link = f"mailto:{quote(docteur_mail)}?subject={quote('Réponse à votre demande de PEC')}&body={quote('Votre demande de PEC a été validée.')}"
        refusal_link = f"mailto:{quote(docteur_mail)}?subject={quote('Réponse à votre demande de PEC')}&body={quote('Votre demande de PEC a été refusée.')}"
        message = f"""
        <h3>Nouvelle demande de PEC</h3>
        <p><strong>Docteur :</strong> {docteur_nom} {docteur_prenom}</p>
        <p><strong>Téléphone :</strong> {docteur_telephone}</p>
        <p><strong>Email :</strong> {docteur_mail}</p>
        <hr>
        <p><strong>Patient :</strong> {patient_nom} {patient_prenom}</p>
        <p><strong>Téléphone :</strong> {patient_telephone}</p>
        <p><strong>Traitement :</strong> {patient_traitement}</p>
        <p><strong>Autres Informations :</strong> {patient_autres}</p>
        <hr>
        <p><a href='{validation_link}'>Valider la PEC</a></p>
        <p><a href='{refusal_link}'>Refuser la PEC</a></p>
        """
        envoyer_email("romain.margalet@bastide-medical.fr", sujet, message)

# Design coloré
def add_custom_css():
    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_custom_css()
