from sqlalchemy.orm import Session
from datetime import datetime
from ....models.reservation import Reservation
from ....models.user import User
from ....models.vehicule import Vehicule
from ...createReservationCommand.create_reservation import CreateReservationCommand

class CreateReservationHandler:
    def __init__(self, db: Session):
        self.db = db

    def handle(self, command: CreateReservationCommand):
        try:
            user = self.db.query(User).filter(User.id == command.user_id).first()
            vehicule = self.db.query(Vehicule).filter(Vehicule.id == command.vehicule_id).first()

            if not user or not vehicule:
                raise ValueError("Utilisateur ou Véhicule non trouvé")

            is_rental = vehicule.contract_type == 'LOCATION'

            documents = command.documents if command.documents else {}

            total_price = 0.0
            if is_rental and command.end_date:
                duration_days = (command.end_date - command.start_date).days
                total_price = duration_days * vehicule.location_price
            else:
                total_price = vehicule.sell_price

            reservation = Reservation(
                user=user,
                vehicule=vehicule,
                vehicule_id=command.vehicule_id,
                start_date=command.start_date,
                end_date=command.end_date,
                is_rental=is_rental,
                documents=documents,  
                total_price=total_price,
                repertory_name=f"reservation_{user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            )

            self.db.add(reservation)
            self.db.commit()
            self.db.refresh(reservation)

            return {
                "id": reservation.id,
                "user_id": reservation.user_id,
                "vehicule_id": reservation.vehicule_id,
                "start_date": reservation.start_date,
                "end_date": reservation.end_date,
                "is_rental": reservation.is_rental,
                "status": reservation.status,
                "created_at": reservation.created_at,
                "repertory_name": reservation.repertory_name,
                "documents": reservation.documents,  
                "total_price": reservation.total_price
            }

        except Exception as e:
            self.db.rollback()
            raise Exception(f"Erreur lors de la création de la réservation: {str(e)}")
