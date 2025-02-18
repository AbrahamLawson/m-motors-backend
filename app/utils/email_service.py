from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List, Dict
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fastmail = FastMail(conf)

def format_date(date: datetime) -> str:
    return date.strftime("%d/%m/%Y")

def get_email_content(reservation_type: str, status: str, details: Dict) -> tuple:
    templates = {
        ("achat", "accepted"): {
            "subject": "Votre demande d'achat a été acceptée !",
            "body": f"""
            Bonjour,
            
            Nous avons le plaisir de vous informer que votre demande d'achat du véhicule (ID: {details['vehicule_id']}) a été acceptée !
            
            Prochaines étapes :
            1. Notre équipe vous contactera dans les plus brefs délais pour organiser la finalisation de la vente
            2. Nous préparerons tous les documents nécessaires pour le transfert de propriété
            3. Un rendez-vous sera fixé pour la remise des clés
            
            Pour toute question, n'hésitez pas à nous contacter.
            
            Merci de votre confiance !
            L'équipe M-Motors
            """
        },
        ("achat", "refused"): {
            "subject": "Votre demande d'achat n'a pas pu être acceptée",
            "body": f"""
            Bonjour,
            
            Nous sommes au regret de vous informer que votre demande d'achat du véhicule (ID: {details['vehicule_id']}) n'a pas pu être acceptée.
            
            Si vous souhaitez plus d'informations sur les raisons de ce refus ou si vous désirez être conseillé sur d'autres véhicules,
            n'hésitez pas à nous contacter directement.
            
            Nous espérons avoir l'occasion de vous accompagner dans vos futurs projets.
            
            Cordialement,
            L'équipe M-Motors
            """
        },
        ("location", "accepted"): {
            "subject": "Votre réservation de location a été acceptée !",
            "body": f"""
            Bonjour,
            
            Nous avons le plaisir de vous informer que votre demande de location a été acceptée !
            
            Détails de votre location :
            - Véhicule ID: {details['vehicule_id']}
            - Date de début: {format_date(details['start_date'])}
            - Date de fin: {format_date(details['end_date'])}
            
            Informations importantes :
            1. Présentez-vous à notre agence le {format_date(details['start_date'])} avec :
               - Votre permis de conduire
               - Une pièce d'identité
               - Le moyen de paiement convenu
            2. Un état des lieux du véhicule sera effectué à la prise et au retour du véhicule
            
            Pour toute question, n'hésitez pas à nous contacter.
            
            Merci de votre confiance !
            L'équipe M-Motors
            """
        },
        ("location", "refused"): {
            "subject": "Votre demande de location n'a pas pu être acceptée",
            "body": f"""
            Bonjour,
            
            Nous sommes au regret de vous informer que votre demande de location pour la période du {format_date(details['start_date'])} au {format_date(details['end_date'])} 
            (Véhicule ID: {details['vehicule_id']}) n'a pas pu être acceptée.
            
            Si vous souhaitez plus d'informations sur les raisons de ce refus ou si vous désirez voir d'autres disponibilités,
            n'hésitez pas à nous contacter directement.
            
            Nous espérons avoir l'occasion de vous accompagner dans vos futurs projets.
            
            Cordialement,
            L'équipe M-Motors
            """
        }
    }
    
    template = templates.get((reservation_type, status))
    return template["subject"], template["body"]

async def send_reservation_notification(email: str, reservation_type: str, status: str, reservation_details: dict):
    subject, body = get_email_content(reservation_type, status, reservation_details)
    
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="plain"
    )

    await fastmail.send_message(message)
