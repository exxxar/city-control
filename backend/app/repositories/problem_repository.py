# backend/app/repositories/problem_repository.py
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, and_

from app.models.problem import Problem, ProblemStatus, ProblemType
from app.models.problem_fact import ProblemFact
from app.models.problem_status_history import ProblemStatusHistory
from app.models.problem_confirmation import ProblemConfirmation
from app.models.problem_message import ProblemMessage
from app.models.user import User


class ProblemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, problem_id: int) -> Optional[Problem]:
        return self.db.get(Problem, problem_id)

    def get_by_public_id(self, public_id: str) -> Optional[Problem]:
        stmt = select(Problem).where(Problem.public_id == public_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_problems(
            self,
            skip: int = 0,
            limit: int = 100,
            status: Optional[ProblemStatus] = None,
            category_id: Optional[int] = None,
            territory_id: Optional[int] = None,
            created_by_id: Optional[int] = None
    ) -> List[Problem]:
        stmt = select(Problem)
        if status: stmt = stmt.where(Problem.status == status)
        if category_id: stmt = stmt.where(Problem.category_id == category_id)
        if territory_id: stmt = stmt.where(Problem.territory_id == territory_id)
        if created_by_id: stmt = stmt.where(Problem.created_by_id == created_by_id)

        stmt = stmt.order_by(Problem.created_at.desc()).offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, problem: Problem) -> Problem:
        self.db.add(problem)
        self.db.commit()
        self.db.refresh(problem)
        return problem

    def update_status(self, problem: Problem, new_status: ProblemStatus, changed_by: User,
                      comment: Optional[str] = None):
        old_status = problem.status
        problem.status = new_status

        # Логируем историю
        history = ProblemStatusHistory(
            problem_id=problem.id,
            old_status=old_status,
            new_status=new_status,
            changed_by_id=changed_by.id,
            comment=comment
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(problem)
        return problem

    def add_confirmation(self, problem_id: int, user_id: int, is_verified: bool = False) -> ProblemConfirmation:
        conf = ProblemConfirmation(problem_id=problem_id, user_id=user_id, is_verified=is_verified)
        self.db.add(conf)

        # Увеличиваем счетчик подтверждений
        problem = self.get_by_id(problem_id)
        if problem:
            problem.confirmations_count += 1

        self.db.commit()
        return conf

    def find_similar_problems(
            self,
            latitude: float,
            longitude: float,
            category_id: Optional[int] = None,
            radius_km: float = 0.1  # 100 метров
    ) -> List[Problem]:
        """
        Упрощенный поиск похожих проблем по координатам и категории.
        В продакшене использовать PostGIS/MySQL Spatial или формулу Хаверсина.
        """
        # Для прототипа делаем простой фильтр по категории и статусу (не закрытые)
        stmt = select(Problem).where(
            Problem.category_id == category_id,
            Problem.status.notin_([ProblemStatus.RESOLVED, ProblemStatus.CLOSED, ProblemStatus.REJECTED])
        )
        # Фильтрация по координатам (если есть geo_tag)
        # Здесь можно добавить сложную логику, но для старта оставим так
        return list(self.db.execute(stmt.limit(10)).scalars().all())

    def add_message(self, problem_id: int, user_id: Optional[int], content: str,
                    is_system: bool = False) -> ProblemMessage:
        msg = ProblemMessage(
            problem_id=problem_id,
            user_id=user_id,
            content=content,
            is_system=is_system
        )
        self.db.add(msg)
        self.db.commit()
        return msg