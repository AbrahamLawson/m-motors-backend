from sqlalchemy import Column, Integer, String, VARCHAR, Enum, DateTime, func
from sqlalchemy.orm import relationship
from ..database import Base
from passlib.context import CryptContext

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    civility = Column(VARCHAR(10), nullable=False)
    last_name = Column(VARCHAR(50), nullable=False)
    first_name = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(100), nullable=False, unique=True,)
    phone_number = Column(VARCHAR(15), nullable=False)
    address = Column(VARCHAR(200), nullable=False)
    zip_code = Column(VARCHAR(10), nullable=False)
    role = Column(Enum("admin", "user"), default="user")
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    reservations = relationship("Reservation", back_populates="user")

    def set_password(self, password: str):
        self.password = pwd_context.hash(password)
        
    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password)