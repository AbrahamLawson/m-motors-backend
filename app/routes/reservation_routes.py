from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..command.createReservationCommand.create_reservation import CreateReservationCommand
from ..command.handler.createReservationHandler.create_reservation_handler import CreateReservationHandler
from ..command.ReservationResponseCommand.reservation_response import ReservationResponse
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ReservationResponse)
async def create_reservation(command: CreateReservationCommand, db: Session = Depends(get_db)):
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
