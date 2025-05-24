from pydantic import BaseModel
from typing import Optional
import datetime

class AppointmentBase(BaseModel):
    service_name: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass # No extra fields for creation beyond base

class AppointmentUpdate(AppointmentBase):
    # Allow partial updates by making fields optional
    service_name: Optional[str] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    notes: Optional[str] = None


class Appointment(AppointmentBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True # Pydantic V2 compatibility