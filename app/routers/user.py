from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже существует"
        )
    
    # Создаём нового пользователя (пока без хэширования пароля)
    user = User(
        email=user_in.email,
        hashed_password=user_in.password,  # TODO: добавить хэширование позже
        full_name=user_in.full_name,
        role=user_in.role
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user