# app/models/user.py  — ОБНОВЛЁННАЯ ВЕРСИЯ (заменить существующий файл)
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.core.security import get_password_hash


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="client")  # client, cafe_owner, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # исправлено

    def set_password(self, password: str):
        self.hashed_password = get_password_hash(password)

    cafes = relationship("Cafe", back_populates="owner")