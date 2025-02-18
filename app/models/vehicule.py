from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from ..database import Base


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
    rear_view_camera = Column(Boolean, default=False)
    hands_free_card = Column(Boolean, default=False) 
    heated_front_seats = Column(Boolean, default=False)            
    electrically_folding_exterior_retro = Column(Boolean, default=False)                  
    disponibilities = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    reservations = relationship("Reservation", back_populates="vehicule")