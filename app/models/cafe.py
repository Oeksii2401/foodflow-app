# app/models/cafe.py  — ОБНОВЛЁННАЯ ВЕРСИЯ (заменить существующий файл)
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base


class Cafe(Base):
    __tablename__ = "cafes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # Связи
    owner = relationship("User", back_populates="cafes")
    categories = relationship("MenuCategory", back_populates="cafe")
    dishes = relationship("Dish", back_populates="cafe")
    orders = relationship("Order", back_populates="cafe")
    delivery_zones = relationship("DeliveryZone", back_populates="cafe")
    stripe_account = relationship("StripeAccount", back_populates="cafe", uselist=False)