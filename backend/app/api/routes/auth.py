# backend/app/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import authenticate_user, register_user
from app.core.security import create_access_token

router = APIRouter()


@router.post("/login", response_model=Token, summary="Вход в систему")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Принимает email и пароль, возвращает JWT токен.
    """
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Генерируем JWT токен, где subject (sub) - это ID пользователя
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Регистрация")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Публичная регистрация нового гражданина.
    """
    return register_user(db, payload)