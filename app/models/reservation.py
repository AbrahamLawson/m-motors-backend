from sqlalchemy import Column, Integer, Enum, DateTime, func, ForeignKey, String, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from ..database import Base

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    vehicule_id = Column(Integer, ForeignKey('vehicules.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    is_rental = Column(Boolean, nullable=True)  
    status = Column(Enum("in_progress", "accepted", "refused"), nullable=True, default="in_progress")
    created_at = Column(DateTime, nullable=False, default=func.now())
    repertory_name = Column(String(255), nullable=True)
    documents = Column(JSON, nullable=True)
    total_price = Column(Float, nullable=True)  

    user = relationship("User", back_populates="reservations")
    vehicule = relationship("Vehicule", back_populates="reservations")

    def calculate_total_price(self):
        if not self.vehicule:
            return 0.0
        
        if self.is_rental and self.end_date:
            days = (self.end_date - self.start_date).days + 1
            return float(self.vehicule.location_price * days)
        else:
            return float(self.vehicule.sell_price)

    def generate_repertory_name(self):
        date_str = self.start_date.strftime("%Y%m%d")
        user_name = f"{self.user.first_name}-{self.user.last_name}"
        transaction_type = "location" if self.is_rental else "achat"
        return f"{date_str}_{user_name}_{transaction_type}_{self.vehicule_id}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'start_date' in kwargs and 'user' in kwargs and 'vehicule_id' in kwargs:
            try:
                self.user = kwargs['user']
                self.vehicule = kwargs.get('vehicule')
                
                if self.vehicule:
                    self.is_rental = self.vehicule.contract_type == 'LOCATION'
                    self.total_price = self.calculate_total_price()

                self.repertory_name = self.generate_repertory_name()
                self.documents = kwargs.get("documents", {})
            except Exception as e:
                print(f"Error in reservation initialization: {e}")
                self.repertory_name = "default_repertory_name"
                self.documents = {}
                self.total_price = 0.0
