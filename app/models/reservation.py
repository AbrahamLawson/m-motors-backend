from sqlalchemy import Column, Integer, Enum, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    vehicule_id = Column(Integer, ForeignKey('vehicules.id'), nullable=False)
    start_date = Column(DateTime, nullable=True)  # Nullable car pas nécessaire pour un achat
    end_date = Column(DateTime, nullable=True)    # Nullable car pas nécessaire pour un achat
    status = Column(Enum("in_progress", "accepted", "refused"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())

    user = relationship("User", back_populates="reservations")
    vehicule = relationship("Vehicule", back_populates="reservations")