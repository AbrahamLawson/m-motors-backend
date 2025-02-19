from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class CreateReservationCommand(BaseModel):
    user_id: int
    vehicule_id: int
    start_date: datetime
    end_date: Optional[datetime] = None
    documents: Optional[Dict[str, str]] = None  # Assure que c'est bien un mapping clé/URL

    class Config:
        from_attributes = True
