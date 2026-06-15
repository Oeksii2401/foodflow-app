from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли уже пользователь
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже существует"
        )
    
    # Создаём пользователя с хэшированным паролем
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        role=user_in.role,
    )
    user.set_password(user_in.password)   # ← хэшируем пароль
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user