from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.cafe import Cafe
from app.models.user import User
from app.schemas.cafe import CafeCreate, CafeRead
from app.core.deps import get_current_user

router = APIRouter(prefix="/cafes", tags=["cafes"])

@router.post("/", response_model=CafeRead, status_code=status.HTTP_201_CREATED)
def create_cafe(
    cafe_in: CafeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Создаём кафе для текущего пользователя
    cafe = Cafe(
        name=cafe_in.name,
        description=cafe_in.description,
        address=cafe_in.address,
        phone=cafe_in.phone,
        owner_id=current_user.id
    )
    
    db.add(cafe)
    db.commit()
    db.refresh(cafe)
    return cafe


@router.get("/my", response_model=list[CafeRead])
def get_my_cafes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cafes = db.query(Cafe).filter(Cafe.owner_id == current_user.id).all()
    return cafes