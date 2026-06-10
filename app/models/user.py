from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="client")  # client, cafe_owner, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(String, default=func.now())

    # Связи
    # cafes = relationship("Cafe", back_populates="owner")  # позже