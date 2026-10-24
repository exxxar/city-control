# backend/app/db/seed/initial_messages.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.problem import Problem
from app.models.problem_message import ProblemMessage
from app.models.user import User


def seed_messages(db: Session):
    print("Seeding problem messages...")

    if db.execute(select(ProblemMessage)).first():
        print("Messages already exist, skipping.")
        return

    problems = db.execute(select(Problem)).scalars().all()
    citizen = db.execute(select(User).where(User.email == "citizen@city.local")).scalar_one()
    executor = db.execute(select(User).where(User.email == "executor@city.local")).scalar_one()
    admin = db.execute(select(User).where(User.email == "admin@city.local")).scalar_one()

    for problem in problems:
        # Системное сообщение о создании
        sys_msg = ProblemMessage(
            problem_id=problem.id,
            content=f"Проблема создана пользователем {problem.created_by.full_name if problem.created_by else 'Неизвестно'}",
            is_system=True
        )
        db.add(sys_msg)

        # Сообщение от гражданина
        msg1 = ProblemMessage(
            problem_id=problem.id,
            user_id=citizen.id,
            content="Добрый день! Прошу обратить внимание на эту проблему."
        )
        db.add(msg1)

        # Сообщение от исполнителя (если назначен)
        if problem.assigned_to_id:
            msg2 = ProblemMessage(
                problem_id=problem.id,
                user_id=executor.id,
                content="Принял в работу. Приступим к устранению в ближайшее время."
            )
            db.add(msg2)

        # Ещё одно сообщение от гражданина
        msg3 = ProblemMessage(
            problem_id=problem.id,
            user_id=citizen.id,
            content="Спасибо! Жду результата."
        )
        db.add(msg3)

    db.commit()
    print("Problem messages seeded.")