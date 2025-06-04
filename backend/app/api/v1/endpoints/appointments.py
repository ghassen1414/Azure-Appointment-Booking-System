from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.appointment as appointment_schemas
import app.crud.crud_appointment as crud_appointment
from app.db.session import get_db
from app.deps import get_current_active_user
from app.models.user import User as UserModel
router = APIRouter()
@router.post("/", response_model=appointment_schemas.Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_in: appointment_schemas.AppointmentCreate,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Create a new appointment for the currently authenticated user.
    """
    # TODO: Add businness logic, check start time in the past, check overlapping appointments, etc.
    appointment= crud_appointment.create_appointment(
        db=db,
        appointment_in=appointment_in,
        owner_id=current_user.id
    )
    # Placeholder for sending notification
    # send_appointment_confirmation_email(current_user.email, appointment_schemas.Appointment.from_orm(appointment).dict())

    return appointment

@router.get("/", response_model=List[appointment_schemas.Appointment])
def read_user_appointments(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user),
) -> any:
    """
    Retrieve appointments for the currently authenticated user.
    """
    appointments = crud_appointment.get_appointments_by_owner(db=db, owner_id=current_user.id,skip=skip, limit=limit)
    # Check if appointments exist
    if not appointments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No appointments found")
    
    return appointments  

@router.get("/{appointment_id}", response_model=appointment_schemas.Appointment)
def read_single_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_id: int,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific appointment by ID
    Ensures the appointment belongs to the currently authenticated user.
    """
    appointment = crud_appointment.get_appointment(
        db=db,
        appointment_id=appointment_id,
        owner_id=current_user.id
    )
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment

@router.put("/{appointment_id}", response_model=appointment_schemas.Appointment)
def update_user_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_id: int,
    appointment_in: appointment_schemas.AppointmentUpdate,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Update an existing appointment for the currently authenticated user.
    """
    db_appointment = crud_appointment.get_appointment(
        db=db,
        appointment_id=appointment_id,
        owner_id=current_user.id
    )
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    # TODO: Add business logic validation here or in CRUD for updates:
    # - Check if new start_time is in the past (if start_time is being updated)
    # - Check for new overlapping appointments (if times are being updated)
    updated_appointment = crud_appointment.update_appointment(
        db=db,
        db_appointment=db_appointment,
        appointment_in=appointment_in
    )
    
    return updated_appointment
@router.delete("/{appointment_id}", response_model=appointment_schemas.Appointment)
def delete_user_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_id: int,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Delete an existing appointment for the currently authenticated user.
    """
    db_appointment = crud_appointment.get_appointment(
        db=db,
        appointment_id=appointment_id,
        owner_id=current_user.id
    )
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found or you don't have access")
    
    deleted_appointment = crud_appointment.delete_appointment(
        db=db,
        db_appointment=db_appointment
    )
    
    return deleted_appointment

