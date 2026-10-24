from sqlalchemy.orm import Session
from app.models.user import User

class PermissionService:
    def __init__(self, db: Session):
        self.db = db

    def can_user_manage_territory(self, user: User, territory_id: int) -> bool:
        """Проверяет, имеет ли пользователь право управлять конкретной территорией."""
        # Упрощенно: если есть admin.full_access, то может всё
        user_perms = {p.codename for role in user.roles for p in role.permissions}
        if "admin.full_access" in user_perms:
            return True
        # В реальности здесь должна быть проверка привязки пользователя к территории
        return "territory.manage" in user_perms