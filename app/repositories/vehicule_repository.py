from sqlalchemy.orm import Session
from app.models import Vehicule

class VehiculeRepository:
    @staticmethod
    def save(db: Session, vehicule: Vehicule):
        db.add(vehicule)
        db.commit()
        db.refresh(vehicule)
        return vehicule
    
    @staticmethod
    def get_by_id(db: Session, vehicule_id: int):
        return db.query(Vehicule).filter(Vehicule.id == vehicule_id).first()
    
    @staticmethod
    def get_all(db: Session):
        return db.query(Vehicule).all()
    
    @staticmethod
    def delete(db: Session, vehicule: Vehicule):
        db.delete(vehicule)
        db.commit()