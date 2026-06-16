# ============================================================
# app/schemas/menu_category.py
# ============================================================
from pydantic import BaseModel
from typing import Optional
 
 
class MenuCategoryBase(BaseModel):
    name: str
    sort_order: int = 0
 
 
class MenuCategoryCreate(MenuCategoryBase):
    pass
 
 
class MenuCategoryUpdate(BaseModel):
    name: Optional[str] = None
    sort_order: Optional[int] = None
 
 
class MenuCategoryRead(MenuCategoryBase):
    id: int
    cafe_id: int
 
    model_config = {"from_attributes": True}
 