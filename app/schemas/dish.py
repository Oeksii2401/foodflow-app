from pydantic import BaseModel
from typing import Optional


class DishBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool = True
    sort_order: int = 0
    category_id: Optional[int] = None
    calories: Optional[int] = None
    is_vegan: bool = False
    is_vegetarian: bool = False
    allergens: Optional[str] = None


class DishCreate(DishBase):
    pass


class DishUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    sort_order: Optional[int] = None
    category_id: Optional[int] = None
    calories: Optional[int] = None
    is_vegan: Optional[bool] = None
    is_vegetarian: Optional[bool] = None
    allergens: Optional[str] = None


class DishRead(DishBase):
    id: int
    cafe_id: int

    model_config = {"from_attributes": True}
