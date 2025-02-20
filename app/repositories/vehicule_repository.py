from sqlalchemy.orm import Session
from sqlalchemy import and_, not_
from app.models import Vehicule
#from app.schema.vehicles_schema import VehiculeFilter
from app.models.reservation import Reservation
from typing import List, Optional
from datetime import datetime
from app.models.vehicule import ContractTypeEnum

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

def get_available_vehicles(
        self,
        start_date: datetime,
        end_date: datetime,
        brand: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        contract_type: Optional[ContractTypeEnum] = None
    ) -> List[Vehicule]:
        # Query de base
        query = self.db.query(Vehicule)
        
        # Filtre pour les véhicules non réservés pendant la période
        unavailable_vehicles = (
            self.db.query(Vehicule.id)
            .join(Vehicule.reservations)
            .filter(
                and_(
                    Reservation.start_date <= end_date,
                    Reservation.end_date >= start_date,
                    Reservation.status != "CANCELLED"
                )
            )
        )
        
        query = query.filter(not_(Vehicule.id.in_(unavailable_vehicles)))
        
        # Ajout des filtres optionnels
        if brand:
            query = query.filter(Vehicule.brand.ilike(f"%{brand}%"))
        
        if min_price:
            query = query.filter(
                (Vehicule.location_price >= min_price) |
                (Vehicule.sell_price >= min_price)
            )
        
        if max_price:
            query = query.filter(
                (Vehicule.location_price <= max_price) |
                (Vehicule.sell_price <= max_price)
            )
        
        if contract_type:
            query = query.filter(Vehicule.contract_type == contract_type)
        
        return query.all()
