from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.vehicule_repository import VehiculeRepository
from app.database import get_db
from app.models.reservation import Reservation
from app.utils.email_service import send_reservation_notification
from typing import List
import os
from datetime import datetime

router = APIRouter()

# Lister toutes les réservations
@router.get("/", response_model=List[dict])
def list_reservations(db: Session = Depends(get_db)):
    try:
        reservations = ReservationRepository.get_all(db)
        return [
            {
                "id": reservation.id,
                "user_id": reservation.user_id,
                "vehicule_id": reservation.vehicule_id,
                "start_date": reservation.start_date,
                "end_date": reservation.end_date,
                "status": reservation.status,
                "created_at": reservation.created_at
            }
            for reservation in reservations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Consulter une réservation spécifique
@router.get("/{reservation_id}", response_model=dict)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = ReservationRepository.get_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    
    return {
        "id": reservation.id,
        "user_id": reservation.user_id,
        "vehicule_id": reservation.vehicule_id,
        "start_date": reservation.start_date,
        "end_date": reservation.end_date,
        "status": reservation.status,
        "created_at": reservation.created_at
    }

# Mettre à jour le statut d'une réservation
@router.patch("/{reservation_id}/status")
async def update_status(reservation_id: int, status: str = Form(...), db: Session = Depends(get_db)):
    reservation = ReservationRepository.get_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    
    if status not in ["accepted", "refused"]:
        raise HTTPException(status_code=400, detail="Statut invalide. Seuls 'accepted' et 'refused' sont autorisés")

    # Récupérer l'utilisateur pour obtenir son email
    user = UserRepository.get_by_id(db, reservation.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Récupérer le véhicule pour déterminer le type de réservation
    vehicule = VehiculeRepository.get_by_id(db, reservation.vehicule_id)
    if not vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")

    reservation.status = status
    updated_reservation = ReservationRepository.save(db, reservation)
    
    # Préparer les détails de la réservation pour l'email
    reservation_details = {
        "vehicule_id": reservation.vehicule_id,
        "start_date": reservation.start_date,
        "end_date": reservation.end_date
    }
    
    # Déterminer le type de réservation en fonction de disponibilities
    reservation_type = "location" if vehicule.disponibilities else "achat"
    
    # Envoyer l'email de notification avec le type approprié
    await send_reservation_notification(
        email=user.email,
        reservation_type=reservation_type,
        status=status,
        reservation_details=reservation_details
    )
    
    return {
        "message": "Statut mis à jour et notification envoyée",
        "nouveau_statut": updated_reservation.status,
        "type": reservation_type
    }
