import uuid
import secrets
import string

def generate_public_id() -> str:
    """Генерирует публичный ID (UUID4)."""
    return str(uuid.uuid4())

def generate_short_code(length: int = 8) -> str:
    """Генерирует короткий читаемый код (например, для номера обращения)."""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_secure_token(length: int = 32) -> str:
    """Генерирует криптографически стойкий токен."""
    return secrets.token_urlsafe(length)