from sqlalchemy import Column, Integer, String, VARCHAR, Enum, DateTime, func, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from ..database import Base

class Vehicule(Base):
    __tablename__ = "vehicules"
    id = Column(Integer, autoincrement=True, primary_key=True)
    model = Column(VARCHAR(50), nullable=False)
    color = Column(VARCHAR(50), nullable=False)
    picture = Column(VARCHAR(255), nullable=False)
    year = Column(Integer, nullable=False)
    kilometers = Column(Integer, nullable=False)
    location_price = Column(Integer, nullable=False)
    sell_price = Column(Integer, nullable=False)
    description = Column(TEXT, nullable=False)
    disponibilities = Column(BOOLEAN, default=True)
    options = Column(Enum(" camera_de_recul", "cartes_mains_libres", "siege_avant_chauffant", "retro_exterieur_rabattable_electriquement"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    reservations = relationship("Reservation", back_populates="vehicule")
