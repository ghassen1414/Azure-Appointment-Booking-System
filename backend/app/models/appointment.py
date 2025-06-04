from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import datetime
import enum

class AppointmentStatus(enum.Enum):
    PENDING_CONFIRMATION = "pending_confirmation"
    CONFIRMED = "confirmed"
    CANCELLED_BY_USER = "cancelled_by_user"
    CANCELLED_BY_ADMIN = "cancelled_by_admin"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class Appointment(Base):
    __tablename__ = "appointments"  

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(255), index=True, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(SQLAlchemyEnum(AppointmentStatus), nullable=False, default=AppointmentStatus.PENDING_CONFIRMATION)
    notes = Column(String(500), nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    owner = relationship("User", back_populates="appointments")



