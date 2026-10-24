# backend/app/services/auth_service.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.repositories.user_repository import get_user_by_email, create_user
from app.core.security import verify_password
from app.schemas.user import UserCreate
from app.models.user import User
from app.models.role import Role


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Проверяет email и пароль. Возвращает пользователя или None."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user


def register_user(db: Session, user_in: UserCreate) -> User:
    """Регистрирует нового пользователя. Если роли не указаны, выдает роль 'Гражданин'."""
    # 1. Проверка на уникальность email
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    # 2. Создание пользователя
    new_user = create_user(
        db=db,
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
        phone=user_in.phone
    )

    # 3. Назначение ролей
    if user_in.role_ids:
        # Если админ/модератор создает юзера и явно указал роли
        stmt_roles = select(Role).where(Role.id.in_(user_in.role_ids))
        roles_to_assign = db.execute(stmt_roles).scalars().all()
        new_user.roles.extend(roles_to_assign)
    else:
        # Если это публичная регистрация, выдаем базовую роль "Гражданин"
        stmt_citizen = select(Role).where(Role.name == "Гражданин")
        citizen_role = db.execute(stmt_citizen).scalar_one_or_none()
        if citizen_role:
            new_user.roles.append(citizen_role)

    db.commit()
    db.refresh(new_user)
    return new_user