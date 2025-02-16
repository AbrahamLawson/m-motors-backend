from pydantic import BaseModel

class CreateUserCommand(BaseModel):
    civility: str
    last_name: str
    first_name: str
    email: str
    phone_number: str
    address: str
    zip_code: str
    password: str
    
    class Config:
        from_attributes = True # Permettre la conversion en un model sqlalchemy