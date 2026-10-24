from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.initiative import Initiative, InitiativeStatus
from app.models.initiative_support import InitiativeSupport
from app.models.user import User
from app.services.notification_service import NotificationService


class InitiativeService:
    def __init__(self, db: Session):
        self.db = db
        self.notification_service = NotificationService(db)

    def create_initiative(self, user: User, title: str, description: str, territory_id: int = None) -> Initiative:
        init = Initiative(
            title=title, description=description, territory_id=territory_id,
            created_by_id=user.id, status=InitiativeStatus.NEW
        )
        self.db.add(init)
        self.db.commit()
        self.db.refresh(init)
        return init

    def support_initiative(self, initiative_id: int, user: User) -> bool:
        """Пользователь поддерживает инициативу. Возвращает True, если поддержка засчитана."""
        init = self.db.get(Initiative, initiative_id)
        if not init: return False

        # Проверяем, не поддерживал ли уже
        exists = self.db.execute(select(InitiativeSupport).where(
            InitiativeSupport.initiative_id == initiative_id,
            InitiativeSupport.user_id == user.id
        )).scalar_one_or_none()

        if not exists:
            support = InitiativeSupport(initiative_id=initiative_id, user_id=user.id)
            self.db.add(support)
            init.support_count += 1
            self.db.commit()
            return True
        return False