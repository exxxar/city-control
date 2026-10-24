# backend/app/schemas/auth.py
from pydantic import BaseModel, Field, field_validator
import re

class LoginRequest(BaseModel):
    email: str = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=6, description="Пароль")

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        # Простая проверка: что-то @ что-то . что-то
        # Это разрешает .local, .test и другие локальные домены
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Некорректный формат email')
        return v.lower().strip()

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: int | None = None # ID пользователя