import secrets
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.database import Base, engine
from app.models.user import User
from app.models.vehicule import Vehicule
from app.models.reservation import Reservation
from app.routes import user_routes, vehicules_routes, filter_routes


app = FastAPI()

security = HTTPBasic()

#Base.metadata.drop_all(bind=engine)
# Create dataBase with the tables if it not exist
Base.metadata.create_all(bind=engine)

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode('utf8')
    correct_username_bytes = b'username'
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode('utf8')    
    correct_password_bytes = b'password'
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
        
        return credentials.username

app.include_router(user_routes.router)
app.include_router(vehicules_routes.router, prefix="/vehicules", tags=["Véhicules"])
app.include_router(filter_routes.router, prefix="/filters", tags=["filters"])

# Auth 
@app.get("/user/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {'username': credentials.username, 'password': credentials.password}
