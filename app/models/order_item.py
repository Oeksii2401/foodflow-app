
# ============================================================
# app/models/order_item.py
# ============================================================
from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.models.base import Base
 
 
class OrderItem(Base):
    __tablename__ = "order_items"
 
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("dishes.id"), nullable=False)
 
    # Снапшот цены и названия на момент заказа (цена может измениться)
    dish_name = Column(String, nullable=False)
    dish_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
 
    @property
    def total(self):
        return self.dish_price * self.quantity
 
    order = relationship("Order", back_populates="items")
    dish = relationship("Dish")
 