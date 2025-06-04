from pydantic import BaseModel, field_validator, ValidationInfo
from typing import Optional
import datetime
from app.models.appointment import AppointmentStatus

class AppointmentBase(BaseModel):
    service_name: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    notes: Optional[str] = None

    @field_validator("end_time")
    def end_time_must_be_after_start_time(cls, v: datetime.datetime, info: ValidationInfo) -> datetime.datetime:
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError("end_time must be after start_time")
        return v
    

class AppointmentCreate(AppointmentBase):
    pass 
class AppointmentUpdate(BaseModel):
    service_name: Optional[str] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    notes: Optional[str] = None
    status: Optional[AppointmentStatus] = None

    @field_validator('end_time')
    def end_time_must_be_after_start_time_if_both_present(cls, v: Optional[datetime.datetime], info: ValidationInfo) -> Optional[datetime.datetime]:
        # If end_time isn't provided, no validation needed here
        if v is None:
            return v
        
        # Check if start_time is also being updated or exists
        if 'start_time' in info.data and info.data.get('start_time') is not None:
            start_time_to_check = info.data['start_time'] # <<< CORRECTED LINE
            if v <= start_time_to_check:
                 raise ValueError('End time must be after start time')
        return v



class Appointment(AppointmentBase):
    id: int
    owner_id: int
    status: AppointmentStatus

    class Config:
        from_attributes = True # Pydantic V2 compatibility