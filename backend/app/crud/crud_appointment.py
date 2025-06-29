from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.appointment import Appointment as AppointmentModel
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
import datetime
from app.models.appointment import AppointmentStatus

def create_appointment(
        db: Session, *, appointment_in: AppointmentCreate, owner_id: int
) -> AppointmentModel:
    """
    Create a new appointment in the database.
    Status defaults to PENDING_CONFIRMATION via the model's default.
    """
    db_appointment = AppointmentModel(**appointment_in.model_dump(), owner_id=owner_id)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointment(
        db: Session, *, appointment_id: int, owner_id: int
) -> Optional[AppointmentModel]:
    """
    Get a single appintment by its ID, ensuring it belongs to the specifiewed owner.
    """
    return db.query(AppointmentModel).filter(
        AppointmentModel.id == appointment_id,
        AppointmentModel.owner_id == owner_id
    ).first()

def get_appointments_by_owner(
        db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
) -> List[AppointmentModel]:
    """
    Get a list of appointments for a specific owner, with pagination.
    """
    return db.query(AppointmentModel).filter(
        AppointmentModel.owner_id == owner_id
    ).order_by(AppointmentModel.start_time.asc()).offset(skip).limit(limit).all() #sorting by start time

def update_appointment(
        db: Session,
        *,
        db_appointment: AppointmentModel,
        appointment_in: AppointmentUpdate
) -> AppointmentModel:
    """
    Update an existing appointment.
    'db_appointment' is the existing appointment object fetched from the database.
    """
    update_date = appointment_in.model_dump(exclude_unset=True)
    for field, value in update_date.items():
        setattr(db_appointment, field, value)

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def delete_appointment(
    db: Session, *, db_appointment: AppointmentModel 
) -> AppointmentModel: 
    """
    Delete an existing appointment.
    'db_appointment' is assumed to be the existing model instance fetched from the DB.
    """
    db.delete(db_appointment)
    db.commit()
    # db_appointment is now detached. If you need to return it, it's fine,
    # but accessing its relationships after deletion might be problematic.
    # Often, delete operations might just return a confirmation or None.
    # For consistency with other CRUDs returning the model, we return it here.
    return db_appointment

def get_overlapping_appointments(
    db: Session,
    *,
    #owner_id: int,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    exclude_appointment_id: Optional[int] = None # To exclude current appointment when updating
) -> List[AppointmentModel]:
    """
    Finds appointments FOR ANY USER that overlap with the given time slot.
    This assumes a single provider/resource system.
    """
    query = db.query(AppointmentModel).filter(
        #AppointmentModel.owner_id == owner_id,
        AppointmentModel.start_time < end_time,
        AppointmentModel.end_time > start_time,
        # Consider only appointments that are 'confirmed' or 'pending' as blocking a slot
        # Adjust statuses as per your business logic
        AppointmentModel.status.in_([AppointmentStatus.CONFIRMED, AppointmentStatus.PENDING_CONFIRMATION])
    )

    if exclude_appointment_id:
        query = query.filter(AppointmentModel.id != exclude_appointment_id)

    return query.all()

