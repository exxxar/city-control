
import re
from typing import Optional

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


# Вложенная схема для роли (чтобы не тянуть все права в ответе пользователя)
class RoleShort(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


# Уберите импорт EmailStr, если он был:
# from pydantic import EmailStr

class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2)
    # ЗАМЕНЯЕМ EmailStr на str
    email: str = Field(..., description="Email пользователя")
    phone: Optional[str] = None

    # Добавляем мягкую валидацию, которая разрешает .local
    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Некорректный формат email')
        return v.lower().strip()

class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, description="ФИО пользователя")
    email: str = Field(..., description="Email пользователя")
    phone: Optional[str] = Field(None, description="Номер телефона")
    password: str = Field(..., min_length=6, description="Пароль")

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Некорректный формат email')
        return v.lower().strip()


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6)
    role_ids: Optional[List[int]] = None


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    roles: List[RoleShort] = []

    model_config = ConfigDict(from_attributes=True)


class UserReadShort(BaseModel):
    id: int
    full_name: str
    email: str  # <-- Должно быть str, а не EmailStr

    class Config:
        from_attributes = True
