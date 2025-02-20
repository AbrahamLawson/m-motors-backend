from sqlalchemy import Column, Integer, Enum, DateTime, func, ForeignKey, String
from sqlalchemy.orm import relationship
from ..database import Base

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    vehicule_id = Column(Integer, ForeignKey('vehicules.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum("in_progress", "accepted", "refused"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    repertory_name = Column(String(255), nullable=True)

    user = relationship("User", back_populates="reservations")
    vehicule = relationship("Vehicule", back_populates="reservations")

    def generate_repertory_name(self):
        date_str = self.start_date.strftime("%Y%m%d")
        user_name = f"{self.user.first_name}-{self.user.last_name}"
        return f"{date_str}_{user_name}_{self.vehicule_id}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'start_date' in kwargs and 'user' in kwargs and 'vehicule_id' in kwargs:
            try:
                self.user = kwargs['user']
                self.repertory_name = self.generate_repertory_name()
            except Exception as e:
                print(f"Error generating repertory_name: {e}")
                self.repertory_name = "default_repertory_name"
        else:
            self.repertory_name = "default_repertory_name"