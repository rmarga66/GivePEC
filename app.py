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

        st.success("Email envoyé avec succès ! Merci pour votre confiance !")
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de l'email: {e}")

# Interface principale de l'application
st.set_page_config(page_title="Prise en Charge Patient", page_icon="🩺", layout="centered")

# Ajout du logo
st.image("logo.png", width=130)

st.markdown("<h3 style='text-align: center;'>Demande de Prise en Charge 🩺</h3>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: gray;'>fait par RM 💉</h6>", unsafe_allow_html=True)


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
        sujet = f"DEMANDE de PEC du DR {docteur_nom}"
        validation_link = f"mailto:{quote(docteur_mail)}?subject={quote('Réponse à votre demande de PEC')}&body={quote('Bonjour, Nous vous informons que votre demande de PEC a été validée')}"
        refusal_link = f"mailto:{quote(docteur_mail)}?subject={quote('Réponse à votre demande de PEC')}&body={quote('Bonjour, Nous vous informons que votre demande de PEC a été refusée pour le motif suivant :')}"
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
        <p><a href='{validation_link}' style='color: white; background-color: #007BFF; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>Valider la PEC</a></p>
        <p><a href='{refusal_link}' style='color: white; background-color: #FF5733; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>Refuser la PEC</a></p>
        """
        envoyer_email("romain.margalet@bastide-medical.fr", sujet, message)

# Design coloré
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f8ff;
            color: #333;
            font-family: Arial, sans-serif;
        }
        .stButton>button {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        .stTextInput>div>input {
            border: 2px solid #007BFF;
            padding: 8px;
            border-radius: 5px;
        }
        .stTextInput>div>input:focus {
            outline: none;
            border: 2px solid #0056b3;
        }
        textarea {
            border: 2px solid #007BFF;
            padding: 8px;
            border-radius: 5px;
        }
        textarea:focus {
            outline: none;
            border: 2px solid #0056b3;
        }
        .footer {
            position: centered;
            bottom: 10px;
            right: 10px;
            font-style: italic;
            color: #40E0D0; /* Bleu turquoise */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_custom_css()

# Ajouter une phrase en bas de la page
st.markdown("""
<div class="footer">
    Vous pouvez aussi joindre Romain MARGALET ☎️ 06.23.03.86.88
</div>
""", unsafe_allow_html=True)
