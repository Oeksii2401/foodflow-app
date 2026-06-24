# ============================================================
# app/models/dish.py
# ============================================================
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("menu_categories.id"), nullable=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # AI-ассистент поля
    calories = Column(Integer, nullable=True)        # калорийность на порцию
    is_vegan = Column(Boolean, default=False)        # веган
    is_vegetarian = Column(Boolean, default=False)   # вегетарианец
    allergens = Column(String, nullable=True)        # "глютен, лактоза, орехи"
    is_halal = Column(Boolean, default=False)        # халяль
    is_kids = Column(Boolean, default=False)         # детское меню

    cafe = relationship("Cafe", back_populates="dishes")
    category = relationship("MenuCategory", back_populates="dishes")
