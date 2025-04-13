from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..command.createReservationCommand.create_reservation import CreateReservationCommand
from ..command.handler.createReservationHandler.create_reservation_handler import CreateReservationHandler
from ..command.ReservationResponseCommand.reservation_response import ReservationResponse
from ..repositories.reservation_repository import ReservationRepository
from ..repositories.user_repository import UserRepository
from ..repositories.vehicule_repository import VehiculeRepository
from ..utils.email_service import send_reservation_notification
from typing import List
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ReservationResponse)
async def create_reservation(command: CreateReservationCommand, db: Session = Depends(get_db)):
    """
    Crée une nouvelle réservation en utilisant le pattern Command.
    """
    logging.info("POST /reservations/ called") 
    try:
        logging.info(f"Command: {command}")
        handler = CreateReservationHandler(db)
        result = handler.handle(command)
        logging.info(f"Réservation créée avec succès: {result}")
        return result
    except ValueError as ve:
        logging.error(f"Erreur de validation: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logging.error(f"Erreur lors de la création de la réservation: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Une erreur inattendue s'est produite: {str(e)}")

@router.get("/", response_model=List[ReservationResponse])
async def get_all_reservations(db: Session = Depends(get_db)):
    """
    Récupère toutes les réservations.
    """
    try:
        logging.info("GET /reservations/ called")
        reservations = ReservationRepository.get_all(db)
        return [ReservationResponse.model_validate(reservation) for reservation in reservations]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des réservations: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Récupère une réservation spécifique par son ID.
    """
    try:
        logging.info(f"GET /reservations/{reservation_id} called")
        reservation = ReservationRepository.get_by_id(db, reservation_id)
        if not reservation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Réservation non trouvée")
        return ReservationResponse.model_validate(reservation)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de la réservation: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/{reservation_id}/status", response_model=ReservationResponse)
async def update_reservation_status(reservation_id: int, status: str = Form(...), db: Session = Depends(get_db)):
    """
    Met à jour le statut d'une réservation et envoie une notification par email si nécessaire.
    """
    try:
        logging.info(f"PATCH /reservations/{reservation_id}/status called with status: {status}")
        
        if status not in ["accepted", "refused", "in_progress"]:
            raise ValueError("Statut invalide. Seuls 'accepted', 'refused' et 'in_progress' sont autorisés")

        reservation = ReservationRepository.get_by_id(db, reservation_id)
        if not reservation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Réservation non trouvée")

        # Vérification de l'existence de l'utilisateur et du véhicule
        user = UserRepository.get_by_id(db, reservation.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")

        vehicule = VehiculeRepository.get_by_id(db, reservation.vehicule_id)
        if not vehicule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Véhicule non trouvé")

        # Mise à jour du prix total si nécessaire
        if not reservation.total_price:
            reservation.total_price = reservation.calculate_total_price()

        reservation.status = status
        updated_reservation = ReservationRepository.save(db, reservation)
        
        try:
            if status in ["accepted", "refused"]:
                reservation_details = {
                    "vehicule_id": reservation.vehicule_id,
                    "start_date": reservation.start_date,
                    "end_date": reservation.end_date if reservation.end_date else reservation.start_date,
                    "total_price": reservation.total_price
                }
                
                await send_reservation_notification(
                    email=user.email,
                    reservation_type="location" if reservation.is_rental else "achat",
                    status=status,
                    reservation_details=reservation_details
                )
                logging.info(f"Email de notification envoyé à {user.email} pour la réservation {reservation_id}")
        except Exception as email_error:
            logging.error(f"Erreur lors de l'envoi de l'email: {str(email_error)}")
            # On continue car la mise à jour du statut a réussi
        
        return ReservationResponse.model_validate(updated_reservation)
        
    except ValueError as ve:
        logging.error(f"Erreur de validation: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour du statut: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
