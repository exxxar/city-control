from sqlalchemy.orm import Session
from app.models.problem import Problem


class ProblemRatingService:
    def __init__(self, db: Session):
        self.db = db

    def recalculate_rating(self, problem: Problem):
        """
        Формула из концепта:
        Рейтинг = подтверждения × коэф. достоверности × коэф. критичности × коэф. актуальности
        """
        confirmations = problem.confirmations_count

        # Упрощенные коэффициенты
        credibility_factor = 1.0
        criticality_factor = 1.5 if problem.priority and problem.priority.level <= 2 else 1.0
        actuality_factor = 1.2 if problem.status.value in ["new", "in_progress"] else 0.8

        new_rating = confirmations * credibility_factor * criticality_factor * actuality_factor
        problem.rating = round(new_rating, 2)
        self.db.commit()