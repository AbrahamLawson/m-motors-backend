from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.command.createUserCommand.create_user import CreateUserCommand

class CreateUserHandler:
    def __init__(self, db: Session):
        self.db = db
        
    def handle(self, command: CreateUserCommand) -> UserRepository:
        user = User(
            civility=command.civility,
            last_name=command.last_name,
            first_name=command.first_name,
            email=command.email,
            phone_number=command.phone_number,
            address=command.address,
            zip_code=command.zip_code,
            password=command.password
        )
        user.set_password(command.password)
        
        return UserRepository.save(self.db, user)
