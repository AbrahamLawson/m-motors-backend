from sqlalchemy.orm import Session
from app.models import User

class UserRepository:
    @staticmethod
    def save(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()