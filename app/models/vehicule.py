from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from ..database import Base
from enum import Enum as PyEnum 
from sqlalchemy import Enum as SQLAlchemyEnum

class ContractTypeEnum(PyEnum):
    LOCATION = "location"
    ACHAT = "achat"
    LOA = "loa" 

class Vehicule(Base):
    __tablename__ = "vehicules"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), index=True)     
    model = Column(String(50), index=True) 
    picture = Column(String(255), index=True)  
    kilometers = Column(Integer)   
    year = Column(Integer)   
    location_price = Column(Integer)   
    sell_price = Column(Integer) 
    description = Column(String(255), index=True)   
    comprehensive_insurance = Column(Boolean, default=False)
    breakdown_assistance = Column(Boolean, default=False) 
    maintenance_and_ass = Column(Boolean, default=False)            
    technical_inspection = Column(Boolean, default=False)                  
    created_at = Column(DateTime, nullable=False, default=func.now())
    contract_type = Column(SQLAlchemyEnum(ContractTypeEnum), nullable=False, default=ContractTypeEnum.LOCATION)
    reservations = relationship("Reservation", back_populates="vehicule")
  
  
 
