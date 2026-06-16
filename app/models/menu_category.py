# ============================================================
# app/models/menu_category.py
# ============================================================
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
 
 
class MenuCategory(Base):
    __tablename__ = "menu_categories"
 
    id = Column(Integer, primary_key=True, index=True)
    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False)
    name = Column(String, nullable=False)
    sort_order = Column(Integer, default=0)
 
    cafe = relationship("Cafe", back_populates="categories")
    dishes = relationship("Dish", back_populates="category")
 