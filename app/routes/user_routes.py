from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.command.createUserCommand.create_user import CreateUserCommand
from app.command.handler.createUserHandler.create_user_handler import CreateUserHandler
from ..models.user import User
from ..dependencies import get_current_user


router = APIRouter()

@router.get("/user/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "created_at": current_user.created_at
    }

@router.post("/create/user/")
def create_user(user: CreateUserCommand, db: Session = Depends(get_db)):
    handler = CreateUserHandler(db)
    return handler.handle(user)
