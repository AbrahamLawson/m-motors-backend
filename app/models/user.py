from sqlalchemy import Column, Integer, String, VARCHAR, Enum, DateTime, func
from ..database import Base

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
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
