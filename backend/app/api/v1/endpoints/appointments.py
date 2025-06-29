from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.appointment as appointment_schemas
import app.crud.crud_appointment as crud_appointment
from app.db.session import get_db
from app.deps import get_current_active_user
from app.models.user import User as UserModel
import datetime

from app.services.notification_service import (
    send_appointment_created_email,
    send_appointment_updated_email,
    send_appointment_cancelled_email
)
import logging
logger = logging.getLogger(__name__)
router = APIRouter()
@router.post("/", response_model=appointment_schemas.Appointment, status_code=status.HTTP_201_CREATED)
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
    
    # --- Timezone Fix for Presentation Demo ---
    # The frontend sends UTC time from the user's local selection (e.g., 8am becomes 6am UTC for UTC+2).
    time_adjustment = datetime.timedelta(hours=2) 
    adjusted_appointment_in = appointment_in.model_copy(
        update={
            'start_time': appointment_in.start_time + time_adjustment,
            'end_time': appointment_in.end_time + time_adjustment,
        }
    )
    # --- End Timezone Fix ---


    # --- Past Time Check (using adjusted time) ---
    current_time_local = datetime.datetime.now()
    naive_adjusted_start_time = adjusted_appointment_in.start_time.replace(tzinfo=None)
    if naive_adjusted_start_time <= current_time_local:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment start time cannot be in the past.",
        )

    # --- Overlap Check (using adjusted time) ---
    overlapping = crud_appointment.get_overlapping_appointments(
        db=db,
        start_time=adjusted_appointment_in.start_time, # Use adjusted time
        end_time=adjusted_appointment_in.end_time      # Use adjusted time
    )
    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The requested time slot is already booked or overlaps with an existing appointment for this user.",
        )

    # If validations pass, use the ADJUSTED data to create the appointment
    appointment = crud_appointment.create_appointment(
        db=db, appointment_in=adjusted_appointment_in, owner_id=current_user.id # Use adjusted data
    )
    
    # --- Send Confirmation Email (uses the now-adjusted appointment object) ---
    if appointment: # Ensure appointment creation was successful
        # Prepare appointment details for the email
        email_payload = {
            "id": appointment.id,  # Include the ID for reference
            "service_name": appointment.service_name,
            "start_time": appointment.start_time, # This will be the adjusted time (e.g., 8am)
            "end_time": appointment.end_time,     # This will be the adjusted time
            "status": appointment.status,
            "notes": appointment.notes
        }

        email_sent = send_appointment_created_email(
            recipient_email=current_user.email,
            recipient_name=current_user.full_name,
            appointment_details=email_payload
        )
        if not email_sent:
            logger.warning(f"Appointment CREATED email failed to send to {current_user.email} for appointment ID {appointment.id}")
        else:
            logger.info(f"Appointment CREATED email initiated for {current_user.email} for appointment ID {appointment.id}")
            
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
    appointments = crud_appointment.get_appointments_by_owner(db=db, owner_id=current_user.id, skip=skip, limit=limit)
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
    Update an appointment owned by the currently authenticated user.
    """
    db_appointment = crud_appointment.get_appointment(
        db=db, appointment_id=appointment_id, owner_id=current_user.id
    )
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found or you don't have access")

    # --- Timezone Fix for Presentation Demo on Update ---
    time_adjustment = datetime.timedelta(hours=2) 

    # Create a copy of the incoming update data to modify
    update_data_dict = appointment_in.model_dump(exclude_unset=True)

    if 'start_time' in update_data_dict and update_data_dict['start_time']:
        # Pydantic has already converted the string to a datetime object
        original_start_time = update_data_dict['start_time']
        update_data_dict['start_time'] = original_start_time + time_adjustment
    
    if 'end_time' in update_data_dict and update_data_dict['end_time']:
        original_end_time = update_data_dict['end_time']
        update_data_dict['end_time'] = original_end_time + time_adjustment
    adjusted_appointment_in = appointment_schemas.AppointmentUpdate(**update_data_dict)
    # --- End Timezone Fix ---


    # --- Perform Validations using ADJUSTED times ---
    proposed_start_time = adjusted_appointment_in.start_time if adjusted_appointment_in.start_time is not None else db_appointment.start_time
    proposed_end_time = adjusted_appointment_in.end_time if adjusted_appointment_in.end_time is not None else db_appointment.end_time

    # --- Past Time Check (only if start_time is being updated) ---
    if adjusted_appointment_in.start_time is not None:
        current_time_local = datetime.datetime.now() # Naive local time
        
        # Make the proposed start_time naive for comparison
        naive_proposed_start_time = proposed_start_time.replace(tzinfo=None)

        if naive_proposed_start_time <= current_time_local:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment start time cannot be in the past.",
            )
    
    # --- End Time > Start Time Check ---
    if proposed_end_time <= proposed_start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, # Or 422
            detail="End time must be after start time."
        )

    # --- Overlap Check (only if times are changing) ---
    if adjusted_appointment_in.start_time is not None or adjusted_appointment_in.end_time is not None:
        overlapping = crud_appointment.get_overlapping_appointments(
            db=db,
            start_time=proposed_start_time,
            end_time=proposed_end_time,
            exclude_appointment_id=db_appointment.id # Exclude self
        )
        if overlapping:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The requested time slot is already booked or overlaps with an existing appointment for this user.",
            )

    # If validations pass, perform the update using the ADJUSTED data
    updated_appointment = crud_appointment.update_appointment(
        db=db, db_appointment=db_appointment, appointment_in=adjusted_appointment_in
    )

    # --- Send Update Email ---
    if updated_appointment:
        email_payload_updated = {
            "id": updated_appointment.id,  # Include the ID for reference
            "service_name": updated_appointment.service_name,
            "start_time": updated_appointment.start_time,
            "end_time": updated_appointment.end_time,
            "status": updated_appointment.status,
            "notes": updated_appointment.notes
        }

        email_sent = send_appointment_updated_email(
            recipient_email=current_user.email,
            recipient_name=current_user.full_name,
            appointment_details=email_payload_updated
        )
        if not email_sent:
            logger.warning(f"Appointment UPDATED email failed to send to {current_user.email} for appointment ID {updated_appointment.id}")
        else:
            logger.info(f"Appointment UPDATED email initiated for {current_user.email} for appointment ID {updated_appointment.id}")

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
    # Step 1: Fetch the appointment to ensure it exists and belongs to the user
    db_appointment_to_delete = crud_appointment.get_appointment(
        db=db,
        appointment_id=appointment_id,
        owner_id=current_user.id
    )
    if not db_appointment_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found or you don't have access")
    
    # Step 2: Capture necessary details for the email BEFORE the actual deletion
    email_payload_for_deleted = {
        "service_name": db_appointment_to_delete.service_name,
        "start_time": db_appointment_to_delete.start_time,
        "end_time": db_appointment_to_delete.end_time,
        "status": db_appointment_to_delete.status, # Original status before deletion
        "notes": db_appointment_to_delete.notes
        # "action": "cancelled" // This can be implicit by calling the specific email func
    }
    
    # Step 3: Perform the deletion
    deleted_appointment_data_for_response = crud_appointment.delete_appointment(
        db=db,
        db_appointment=db_appointment_to_delete # Pass the fetched object to be deleted
    )
    
    # Step 4: Send the Cancellation Email (AFTER successful deletion commit in CRUD)
    # We use the payload captured in Step 2.
    email_sent = send_appointment_cancelled_email( # Call the specific cancellation email function
        recipient_email=current_user.email,
        recipient_name=current_user.full_name,
        appointment_details=email_payload_for_deleted
    )
    if not email_sent:
        logger.warning(f"Appointment CANCELLED email failed to send to {current_user.email} for (now deleted) appointment ID {appointment_id}")
    else:
        logger.info(f"Appointment CANCELLED email initiated for {current_user.email} for (now deleted) appointment ID {appointment_id}")
    
    # Step 5: Return the data of the deleted appointment
    return deleted_appointment_data_for_response

