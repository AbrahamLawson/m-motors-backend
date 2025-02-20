import secrets
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.database import Base, engine
from app.models.user import User
from app.models.vehicule import Vehicule
from app.models.reservation import Reservation
from app.routes import user_routes, vehicules_routes, filter_routes, auth



app = FastAPI()

security = HTTPBasic()

#Base.metadata.drop_all(bind=engine)
# Create dataBase with the tables if it not exist
Base.metadata.create_all(bind=engine)

#Routes
app.include_router(user_routes.router)
app.include_router(vehicules_routes.router, prefix="/vehicules", tags=["Véhicules"])
app.include_router(filter_routes.router, prefix="/filters", tags=["filters"])
app.include_router(auth.router, tags=["Authentication"])

# Auth 
@app.get("/user/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {'username': credentials.username, 'password': credentials.password}




