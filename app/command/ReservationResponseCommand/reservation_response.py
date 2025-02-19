from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class ReservationResponse(BaseModel):
    id: int 
    user_id: int
    vehicule_id: int
    start_date: datetime
    end_date: Optional[datetime] = None
    is_rental: Optional[bool] = None
    status: Optional[str] = None
    created_at: datetime
    repertory_name: Optional[str] = None
    documents: Optional[Dict[str, str]] = None
    total_price: Optional[float] = None

    class Config:
        from_attributes = True
