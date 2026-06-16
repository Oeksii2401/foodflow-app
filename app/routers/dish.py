
# ============================================================
# app/routers/dish.py
# ============================================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
 
from app.db.session import get_db
from app.models.dish import Dish
from app.schemas.dish import DishCreate, DishUpdate, DishRead
from app.core.deps import get_current_active_user
from app.models.user import User
 
router = APIRouter(prefix="/cafes/{cafe_id}/dishes", tags=["dishes"])
 
 
@router.get("/", response_model=list[DishRead])
def list_dishes(cafe_id: int, db: Session = Depends(get_db)):
    return db.query(Dish).filter(Dish.cafe_id == cafe_id).order_by(Dish.sort_order).all()
 
 
@router.post("/", response_model=DishRead, status_code=status.HTTP_201_CREATED)
def create_dish(
    cafe_id: int,
    data: DishCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    dish = Dish(**data.model_dump(), cafe_id=cafe_id)
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish
 
 
@router.patch("/{dish_id}", response_model=DishRead)
def update_dish(
    cafe_id: int,
    dish_id: int,
    data: DishUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    dish = db.query(Dish).filter(Dish.id == dish_id, Dish.cafe_id == cafe_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(dish, field, value)
    db.commit()
    db.refresh(dish)
    return dish
 
 
@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dish(
    cafe_id: int,
    dish_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    dish = db.query(Dish).filter(Dish.id == dish_id, Dish.cafe_id == cafe_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    db.delete(dish)
    db.commit()