# backend/app/repositories/user_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.core.security import hash_password

def get_user_by_email(db: Session, email: str) -> User | None:
    """Поиск пользователя по email."""
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Поиск пользователя по ID."""
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()

def create_user(
    db: Session,
    email: str,
    password: str,
    full_name: str,
    phone: str | None = None
) -> User:
    """Создание нового пользователя (пароль хэшируется здесь)."""
    hashed_password = hash_password(password)
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        phone=phone,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user