from datetime import datetime, timezone, timedelta

def utc_now() -> datetime:
    """Возвращает текущее время в UTC."""
    return datetime.now(timezone.utc)

def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Форматирует datetime в строку."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime(fmt)

def add_minutes(dt: datetime, minutes: int) -> datetime:
    """Добавляет минуты к datetime."""
    return dt + timedelta(minutes=minutes)

def is_overdue(deadline: datetime) -> bool:
    """Проверяет, просрочен ли дедлайн."""
    return utc_now() > deadline