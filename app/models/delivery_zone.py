
# ============================================================
# app/models/delivery_zone.py
# ============================================================
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
 
 
class DeliveryZone(Base):
    __tablename__ = "delivery_zones"
 
    id = Column(Integer, primary_key=True, index=True)
    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False)
    name = Column(String, nullable=False)           # например "Центр", "Пригород"
    min_order = Column(Float, default=0.0)          # минимальная сумма заказа
    delivery_price = Column(Float, default=0.0)     # стоимость доставки
    delivery_time_min = Column(Integer, default=30) # время доставки в минутах
 
    cafe = relationship("Cafe", back_populates="delivery_zones")
 