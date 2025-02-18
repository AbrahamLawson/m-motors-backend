from pydantic import BaseModel
from datetime import datetime
from typing import Optional


#Base commune pour tous les schémas
class VehiculeBase(BaseModel):
    brand: str
    model: str
    picture: str 
    kilometers: int
    year: int
    location_price: int
    sell_price: int
    description: str
    rear_view_camera: bool = False
    hands_free_card: bool = False
    heated_front_seats: bool = False
    electrically_folding_exterior_retro: bool = False

#Schéma pour la création d'un vehicule
class VehiculeCreate(VehiculeBase):
    pass

#Schéma pour la mise à jour d'un véhicule
class VehiculeUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    picture: Optional[str] = None
    kilometers: Optional[int] = None
    year: Optional[int] = None
    location_price: Optional[int] = None
    sell_price: Optional[int] = None
    description: Optional[str] = None
    rear_view_camera: Optional[bool] = False
    hands_free_card: Optional[bool] = False
    heated_front_seats: Optional[bool] = False
    electrically_folding_exterior_retro: Optional[bool] = False

#Schéma pour la supression d'un véhicule
class VehiculeOut(VehiculeBase):
    id: int
    created_at: datetime

    class Config:
         from_attributes = True
