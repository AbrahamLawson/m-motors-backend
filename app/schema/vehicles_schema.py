from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from enum import Enum


class ContractTypeEnum(str, Enum):
    LOCATION = "location"
    ACHAT = "achat"
    LOA = "loa"  

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
    comprehensive_insurance: bool = False
    breakdown_assistance: bool = False
    maintenance_and_ass: bool = False
    technical_inspection: bool = False
    contract_type: ContractTypeEnum

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
    comprehensive_insurance: Optional[bool] = False
    breakdown_assistance: Optional[bool] = False
    maintenance_and_ass: Optional[bool] = False
    technical_inspection: Optional[bool] = False
    contract_type: Optional[ContractTypeEnum] = None

#Schéma pour la supression d'un véhicule
class VehiculeOut(VehiculeBase):
    id: int
    created_at: datetime

    model_config = {
    "from_attributes": True
}

#Schema pour le filtre 

class VehiculeFilter(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    contract_type: Optional[ContractTypeEnum] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    page: int = 1
    limit: int = 10
