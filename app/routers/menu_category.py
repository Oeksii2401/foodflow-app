# ============================================================
# app/routers/menu_category.py
# ============================================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
 
from app.db.session import get_db
from app.models.menu_category import MenuCategory
from app.schemas.menu_category import MenuCategoryCreate, MenuCategoryUpdate, MenuCategoryRead
from app.core.deps import get_current_active_user
from app.models.user import User
 
router = APIRouter(prefix="/cafes/{cafe_id}/categories", tags=["menu-categories"])
 
 
@router.get("/", response_model=list[MenuCategoryRead])
def list_categories(cafe_id: int, db: Session = Depends(get_db)):
    return db.query(MenuCategory).filter(MenuCategory.cafe_id == cafe_id).order_by(MenuCategory.sort_order).all()
 
 
@router.post("/", response_model=MenuCategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    cafe_id: int,
    data: MenuCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    category = MenuCategory(**data.model_dump(), cafe_id=cafe_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
 
 
@router.patch("/{category_id}", response_model=MenuCategoryRead)
def update_category(
    cafe_id: int,
    category_id: int,
    data: MenuCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    category = db.query(MenuCategory).filter(
        MenuCategory.id == category_id, MenuCategory.cafe_id == cafe_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category
 
 
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    cafe_id: int,
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    category = db.query(MenuCategory).filter(
        MenuCategory.id == category_id, MenuCategory.cafe_id == cafe_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()