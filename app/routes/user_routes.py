from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.command.createUserCommand.create_user import CreateUserCommand
from app.command.handler.createUserHandler.create_user_handler import CreateUserHandler


router = APIRouter()

@router.post("/users/")
def create_user(user: CreateUserCommand, db: Session = Depends(get_db)):
    handler = CreateUserHandler(db)
    return handler.handle(user)
