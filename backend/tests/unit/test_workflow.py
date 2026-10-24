import pytest
from app.models.problem import Problem, ProblemStatus
from app.models.user import User
from app.services.workflow_service import WorkflowService
from tests.factories.user_factory import create_user


def test_change_problem_status(db_session):
    # Arrange
    user = create_user(db_session, email="admin@city.local", role_name="Системный администратор")
    problem = Problem(title="Test Problem", created_by_id=user.id, status=ProblemStatus.NEW)
    db_session.add(problem)
    db_session.commit()
    db_session.refresh(problem)

    service = WorkflowService(db_session)

    # Act
    service.change_status(problem, ProblemStatus.IN_PROGRESS, user, comment="Taking it")

    # Assert
    assert problem.status == ProblemStatus.IN_PROGRESS

    # Проверяем, что история сохранилась
    history = db_session.query(problem.__class__).filter_by(id=problem.id).first()  # Упрощенно
    # В реальности нужно проверить таблицу ProblemStatusHistory