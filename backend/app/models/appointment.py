from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import datetime

class Appointment(Base):
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(255), index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    notes = Column(String(500), nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id")) # Ensure 'users' is the tablename for User model
    # TODO: Add relationship back to user
    # owner = relationship("User", back_populates="appointments")

    # TODO: Add fields for status (e.g., confirmed, cancelled), provider_id if multiple providers