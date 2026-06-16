
# ============================================================
# app/models/order.py
# ============================================================
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
 
 
class Order(Base):
    __tablename__ = "orders"
 
    id = Column(Integer, primary_key=True, index=True)
    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False)
 
    # Данные клиента (без регистрации)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)
 
    # Доставка
    delivery_address = Column(String, nullable=True)
    delivery_lat = Column(Float, nullable=True)
    delivery_lng = Column(Float, nullable=True)
    delivery_zone_id = Column(Integer, ForeignKey("delivery_zones.id"), nullable=True)
    delivery_price = Column(Float, default=0.0)
 
    # Суммы
    subtotal = Column(Float, nullable=False)        # сумма блюд
    total = Column(Float, nullable=False)           # subtotal + delivery
 
    # Статус
    # pending → paid → preparing → ready → delivering → delivered / cancelled
    status = Column(String, default="pending")
 
    # Stripe
    stripe_payment_intent_id = Column(String, nullable=True)
    stripe_checkout_session_id = Column(String, nullable=True)
 
    # QR подтверждение
    qr_code = Column(String, nullable=True)         # уникальный токен для QR на чеке
    is_confirmed = Column(Boolean, default=False)   # курьер отсканировал QR
 
    comment = Column(Text, nullable=True)
    language = Column(String, default="de")         # язык клиента при заказе
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
 
    cafe = relationship("Cafe", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    delivery_zone = relationship("DeliveryZone")
 