from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, aliased
from app.models.vehicule import Vehicule
from app.schema.vehicles_schema import VehiculeOut
from app.database import get_db
from typing import List
from app.models.vehicule import ContractTypeEnum
from app.models.reservation import Reservation
from datetime import date

router = APIRouter()

#filtre pour brand

@router.get("/vehicules/brand/{brand}", response_model=List[VehiculeOut])
def get_vehicles_by_brand(brand: str, db: Session = Depends(get_db)):
    vehicles = db.query(Vehicule).filter(Vehicule.brand == brand).all()
    if not vehicles:
        raise HTTPException(status_code=404, detail="Aucun véhicule trouvé pour cette marque")
    return vehicles

#filtre pour price

@router.get("/vehicules/price/", response_model=List[VehiculeOut])
def get_vehicles_by_price_range(
    price_min: float = Query(..., description="Prix minimum"),
    price_max: float = Query(..., description="Prix maximum"),
    db: Session = Depends(get_db)
):
    vehicles = db.query(Vehicule).filter(
        Vehicule.sell_price >= price_min,
        Vehicule.sell_price <= price_max
    ).all()
    if not vehicles:
        raise HTTPException(status_code=404, detail="Aucun véhicule trouvé dans cette gamme de prix")
    return vehicles

#filtre pour année
@router.get("/vehicules/filters/year/", response_model=List[VehiculeOut])
def get_vehicles_by_year(
    year: int = Query(..., description="Année du véhicule"),
    db: Session = Depends(get_db)
):
    vehicles = db.query(Vehicule).filter(Vehicule.year == year).all()
    if not vehicles:
        raise HTTPException(status_code=404, detail="Aucun véhicule trouvé pour cette année")
    return vehicles

#filtre pour modèle
@router.get("/vehicules/filters/model/", response_model=List[VehiculeOut])
def get_vehicles_by_model(
    model: str = Query(..., description="Modèle du véhicule"),
    db: Session = Depends(get_db)
):
    vehicles = db.query(Vehicule).filter(Vehicule.model.ilike(f"%{model}%")).all()
    if not vehicles:
        raise HTTPException(status_code=404, detail="Aucun véhicule trouvé pour ce modèle")
    return vehicles


#filtre pour contract type
@router.get("/vehicules/contract_type/{contract_type}", response_model=List[VehiculeOut])
def get_vehicles_by_contract_type(contract_type: ContractTypeEnum, db: Session = Depends(get_db)):
    vehicles = db.query(Vehicule).filter(Vehicule.contract_type == contract_type).all()
    if not vehicles:
        raise HTTPException(status_code=404, detail="Aucun véhicule trouvé pour ce type de contrat")
    return vehicles

#Filtre disponibility

@router.get("/vehicules/availability/", response_model=List[VehiculeOut])
def get_vehicles_by_availability(
    start_date: date = Query(..., description="Date de début"),
    end_date: date = Query(..., description="Date de fin"),
    db: Session = Depends(get_db)
):
    ReservationAlias = aliased(Reservation)
    subquery = db.query(ReservationAlias.vehicule_id).filter(
        ReservationAlias.start_date <= end_date,
        ReservationAlias.end_date >= start_date
    ).subquery()

    vehicles = db.query(Vehicule).filter(Vehicule.id.not_in(subquery)).all()
    if not vehicles:
        raise HTTPException(status_code=404, detail="Aucun véhicule disponible pour ces dates")
    return vehicles