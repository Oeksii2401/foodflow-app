
# ============================================================
# app/schemas/order.py
# ============================================================
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
 
 
class OrderItemCreate(BaseModel):
    dish_id: int
    quantity: int = 1
 
 
class OrderItemRead(BaseModel):
    id: int
    dish_id: int
    dish_name: str
    dish_price: float
    quantity: int
    total: float
 
    model_config = {"from_attributes": True}
 
 
class OrderCreate(BaseModel):
    cafe_id: int
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_lat: Optional[float] = None
    delivery_lng: Optional[float] = None
    delivery_zone_id: Optional[int] = None
    comment: Optional[str] = None
    language: str = "de"
    items: List[OrderItemCreate]
 
 
class OrderRead(BaseModel):
    id: int
    cafe_id: int
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_price: float
    subtotal: float
    total: float
    status: str
    qr_code: Optional[str] = None
    is_confirmed: bool
    comment: Optional[str] = None
    language: str
    created_at: datetime
    items: List[OrderItemRead] = []
 
    model_config = {"from_attributes": True}
 
 
class OrderStatusUpdate(BaseModel):
    status: str  # pending, paid, preparing, ready, delivering, delivered, cancelled