from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.models.role import Role
from app.core.security import hash_password

USERS_DATA = [
    {"email": "admin@city.local", "full_name": "Системный Администратор", "role": "Системный администратор",
     "password": "admin123"},
    {"email": "moderator@city.local", "full_name": "Иван Модераторов", "role": "Модератор", "password": "mod123"},
    {"email": "executor@city.local", "full_name": "Петр Исполнителев", "role": "Исполнитель", "password": "exec123"},
    {"email": "citizen@city.local", "full_name": "Сергей Гражданов", "role": "Гражданин", "password": "cit123"},
]


def seed_users(db: Session):
    print("Seeding users...")

    # Подтягиваем роли
    roles_stmt = select(Role)
    roles_in_db = {r.name: r for r in db.execute(roles_stmt).scalars().all()}

    for data in USERS_DATA:
        stmt = select(User).where(User.email == data["email"])
        if not db.execute(stmt).scalar_one_or_none():
            new_user = User(
                email=data["email"],
                hashed_password=hash_password(data["password"]),
                full_name=data["full_name"],
                phone="+79001234567",
                is_active=True
            )

            role_name = data["role"]
            if role_name in roles_in_db:
                new_user.roles.append(roles_in_db[role_name])
            else:
                print(f"Warning: Role '{role_name}' not found for user {data['email']}")

            db.add(new_user)

    db.commit()
    print("Users seeded.")