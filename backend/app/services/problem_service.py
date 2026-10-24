from typing import Optional
from sqlalchemy.orm import Session
from app.models.problem import Problem, ProblemStatus, ProblemType
from app.models.problem_fact import ProblemFact
from app.models.user import User
from app.repositories.problem_repository import ProblemRepository
from app.services.problem_matching_service import ProblemMatchingService
from app.services.notification_service import NotificationService
from app.services.audit_service import AuditService


class ProblemService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProblemRepository(db)
        self.matching_service = ProblemMatchingService(db)
        self.notification_service = NotificationService(db)
        self.audit_service = AuditService(db)

    def create_problem(
            self, user: User, title: str, description: Optional[str],
            category_id: Optional[int], territory_id: Optional[int],
            geo_tag_id: Optional[int], latitude: Optional[float] = None, longitude: Optional[float] = None
    ) -> Problem:
        # 1. Поиск похожих проблем (Матчинг)
        similar_problems = []
        if category_id and (latitude or longitude):
            similar_problems = self.matching_service.find_similar(
                category_id=category_id, territory_id=territory_id,
                latitude=latitude, longitude=longitude
            )
            # В реальном приложении фронтенд получит этот список и предложит пользователю:
            # "Найдены похожие проблемы. Хотите дополнить одну из них?"

        # 2. Создание проблемы
        problem = Problem(
            title=title, description=description, category_id=category_id,
            territory_id=territory_id, geo_tag_id=geo_tag_id,
            created_by_id=user.id, status=ProblemStatus.NEW, type=ProblemType.PROBLEM
        )
        problem = self.repo.create(problem)

        # 3. Уведомления (Модераторам о новой проблеме)
        self.notification_service.notify_new_problem(problem)

        # 4. Аудит
        self.audit_service.log_action(user.id, "create", "problem", problem.id, new_values={"title": title})

        return problem

    def add_fact_to_problem(self, problem_id: int, user: User, description: Optional[str] = None) -> ProblemFact:
        """Добавляет подтверждение (факт) к существующей проблеме."""
        problem = self.repo.get_by_id(problem_id)
        if not problem:
            raise ValueError("Problem not found")

        fact = ProblemFact(problem_id=problem_id, user_id=user.id, description=description, is_grouped=True)
        self.db.add(fact)

        # Увеличиваем счетчик и пересчитываем рейтинг (упрощенно)
        problem.confirmations_count += 1
        self.db.commit()

        self.notification_service.notify_problem_confirmed(problem, user)
        return fact