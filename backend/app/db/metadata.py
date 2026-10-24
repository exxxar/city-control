# backend/app/db/metadata.py
from app.db.base import Base

# Импортируем все модели из __init__.py, чтобы они зарегистрировались в Base.metadata
# Это гарантирует, что Alembic и скрипты инициализации увидят все таблицы.
from app.models import *

# Экспортируем сам объект metadata
metadata = Base.metadata