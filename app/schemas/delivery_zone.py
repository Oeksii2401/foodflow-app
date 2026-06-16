
# ============================================================
# app/schemas/delivery_zone.py
# ============================================================
from pydantic import BaseModel
from typing import Optional
 
 
class DeliveryZoneBase(BaseModel):
    name: str
    min_order: float = 0.0
    delivery_price: float = 0.0
    delivery_time_min: int = 30
 
 
class DeliveryZoneCreate(DeliveryZoneBase):
    pass
 
 
class DeliveryZoneUpdate(BaseModel):
    name: Optional[str] = None
    min_order: Optional[float] = None
    delivery_price: Optional[float] = None
    delivery_time_min: Optional[int] = None
 
 
class DeliveryZoneRead(DeliveryZoneBase):
    id: int
    cafe_id: int
 
    model_config = {"from_attributes": True}
 