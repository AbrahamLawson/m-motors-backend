from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import Dict
import logging
from ....models.reservation import Reservation
from ....models.user import User
from ....models.vehicule import Vehicule
from ...createReservationCommand.create_reservation import CreateReservationCommand
from ....repositories.reservation_repository import ReservationRepository
from ....repositories.user_repository import UserRepository
from ....repositories.vehicule_repository import VehiculeRepository
from ....command.ReservationResponseCommand.reservation_response import ReservationResponse

logger = logging.getLogger(__name__)

class CreateReservationHandler:
    """
    Handler pour la création d'une réservation.
    Implémente le pattern Command pour gérer la logique de création.
    """
    
    def __init__(self, db: Session):
        """
        Initialise le handler avec une session de base de données.
        
        Args:
            db (Session): Session de base de données SQLAlchemy
        """
        self.db = db
        self.user_repository = UserRepository()
        self.vehicule_repository = VehiculeRepository()
        self.reservation_repository = ReservationRepository()

    def _calculate_total_price(self, vehicule: Vehicule, start_date: datetime, end_date: datetime = None, is_rental: bool = False) -> float:
        """
        Calcule le prix total de la réservation.
        
        Args:
            vehicule (Vehicule): Le véhicule concerné
            start_date (datetime): Date de début
            end_date (datetime, optional): Date de fin pour une location
            is_rental (bool): Si c'est une location ou un achat
            
        Returns:
            float: Le prix total calculé
        """
        if is_rental and end_date:
            duration_days = (end_date - start_date).days + 1  # +1 car on compte le jour de début
            return float(vehicule.location_price * duration_days)
        return float(vehicule.sell_price)

    def handle(self, command: CreateReservationCommand) -> Dict:
        """
        Traite la commande de création de réservation.
        
        Args:
            command (CreateReservationCommand): Commande contenant les données de la réservation
            
        Returns:
            Dict: Données de la réservation créée
            
        Raises:
            ValueError: Si l'utilisateur ou le véhicule n'existe pas
            SQLAlchemyError: En cas d'erreur de base de données
        """
        try:
            logger.info(f"Début de création de réservation pour user_id={command.user_id}, vehicule_id={command.vehicule_id}")
            
            # Récupération de l'utilisateur et du véhicule via les repositories
            user = self.user_repository.get_by_id(self.db, command.user_id)
            if not user:
                raise ValueError(f"Utilisateur avec ID {command.user_id} non trouvé")

            vehicule = self.vehicule_repository.get_by_id(self.db, command.vehicule_id)
            if not vehicule:
                raise ValueError(f"Véhicule avec ID {command.vehicule_id} non trouvé")

            # Détermination du type de contrat
            is_rental = vehicule.contract_type == 'LOCATION'
            
            # Calcul du prix total
            total_price = self._calculate_total_price(
                vehicule=vehicule,
                start_date=command.start_date,
                end_date=command.end_date,
                is_rental=is_rental
            )

            # Création de la réservation
            reservation = Reservation(
                user=user,
                vehicule=vehicule,
                vehicule_id=command.vehicule_id,
                start_date=command.start_date,
                end_date=command.end_date,
                is_rental=is_rental,
                documents=command.documents or {},
                total_price=total_price,
                repertory_name=f"reservation_{user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            )

            # Sauvegarde via le repository
            saved_reservation = self.reservation_repository.save(self.db, reservation)
            logger.info(f"Réservation créée avec succès, ID: {saved_reservation.id}")

            # Retourne la réponse formatée
            return ReservationResponse.model_validate(saved_reservation).model_dump()

        except ValueError as ve:
            logger.error(f"Erreur de validation: {str(ve)}")
            raise
        except SQLAlchemyError as e:
            logger.error(f"Erreur de base de données: {str(e)}")
            self.db.rollback()
            raise
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la création de la réservation: {str(e)}")
            self.db.rollback()
            raise ValueError(f"Erreur lors de la création de la réservation: {str(e)}")
