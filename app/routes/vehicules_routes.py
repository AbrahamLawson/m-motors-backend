from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schema.vehicles_schema import VehiculeCreate, VehiculeUpdate, VehiculeOut
from app.repositories.vehicule_repository import VehiculeRepository
from app.database import get_db
from app.models.vehicule import Vehicule


router = APIRouter()


# Créer un véhicule
@router.post("/", response_model=VehiculeOut)
def create(vehicule: VehiculeCreate, db: Session = Depends(get_db)):
    db_vehicule = Vehicule(**vehicule.model_dump())  
    return VehiculeRepository.save(db, db_vehicule)

# Lire tous les véhicules
@router.get("/", response_model=list[VehiculeOut])
def read_all(db: Session = Depends(get_db)):
    return VehiculeRepository.get_all(db)

# Lire un véhicule par ID
@router.get("/{vehicule_id}", response_model=VehiculeOut)
def read(vehicule_id: int, db: Session = Depends(get_db)):
    vehicule = VehiculeRepository.get_by_id(db, vehicule_id)
    if not vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    return vehicule

# Mettre à jour un véhicule
@router.put("/{vehicule_id}", response_model=VehiculeOut)
def update(vehicule_id: int, vehicule: VehiculeUpdate, db: Session = Depends(get_db)):
    db_vehicule = VehiculeRepository.get_by_id(db, vehicule_id)
    if not db_vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    
    # Mise à jour des champs
    for key, value in vehicule.model_dump(exclude_unset=True).items():
        setattr(db_vehicule, key, value)

    return VehiculeRepository.save(db, db_vehicule)

# Supprimer un véhicule
@router.delete("/{vehicule_id}")
def delete(vehicule_id: int, db: Session = Depends(get_db)):
    vehicule = VehiculeRepository.get_by_id(db, vehicule_id)
    if not vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    
    VehiculeRepository.delete(db, vehicule)
    return {"message": "Véhicule supprimé avec succès"}