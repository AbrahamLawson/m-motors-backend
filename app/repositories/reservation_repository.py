from sqlalchemy.orm import Session
from app.models.reservation import Reservation

class ReservationRepository:
    @staticmethod
    def save(db: Session, reservation: Reservation):
        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return reservation
    
    @staticmethod
    def get_by_id(db: Session, reservation_id: int):
        return db.query(Reservation).filter(Reservation.id == reservation_id).first()
    
    @staticmethod
    def get_all(db: Session):
        return db.query(Reservation).all()
    
    @staticmethod
    def delete(db: Session, reservation: Reservation):
        db.delete(reservation)
        db.commit()