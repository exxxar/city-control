from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    stmt = select(User).where(User.id == int(user_id))
    user = db.execute(stmt).scalar_one_or_none()

    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_permission(permission_codename: str):
    """Фабрика зависимостей для проверки наличия конкретного права у пользователя."""

    def permission_checker(current_user: User = Depends(get_current_user)):
        # Собираем все права пользователя из его ролей
        user_permissions = {p.codename for role in current_user.roles for p in role.permissions}

        # Если есть полное право админа или нужное право - пропускаем
        if "admin.full_access" not in user_permissions and permission_codename not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission_codename}' required"
            )
        return current_user

    return permission_checker