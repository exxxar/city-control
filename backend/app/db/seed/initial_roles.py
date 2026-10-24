from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.role import Role
from app.models.permission import Permission
from app.db.seed.initial_permissions import PERMISSIONS_DATA

# Маппинг ролей и их прав (по codename)
ROLES_DATA = [
    {
        "name": "Гость",
        "description": "Неавторизованный пользователь. Может просматривать публичную карту.",
        "permissions": ["problem.view_public", "geo_tag.view"]
    },
    {
        "name": "Гражданин",
        "description": "Зарегистрированный пользователь. Может создавать обращения и инициативы.",
        "permissions": ["problem.view_public", "problem.create", "initiative.create", "event.create", "geo_tag.view"]
    },
    {
        "name": "Модератор",
        "description": "Проверяет корректность обращений, фильтрует спам, запрашивает уточнения.",
        "permissions": ["problem.view_all", "problem.moderate", "initiative.moderate", "user.view"]
    },
    {
        "name": "Исполнитель",
        "description": "Сотрудник, который физически устраняет проблему или фиксирует результат.",
        "permissions": ["problem.view_public", "problem.change_status"]  # Статусы ограничены на уровне сервиса
    },
    {
        "name": "Руководитель органа",
        "description": "Контролирует работу подразделения, распределяет задачи, видит SLA.",
        "permissions": ["problem.view_all", "problem.assign", "sla.manage", "analytics.view"]
    },
    {
        "name": "Муниципальный администратор",
        "description": "Управляет территориями, объектами, гео-метками и пользователями своего муниципалитета.",
        "permissions": ["territory.manage", "object.manage", "geo_tag.manage", "indoor_map.manage", "user.manage"]
    },
    {
        "name": "Системный администратор",
        "description": "Полный доступ ко всем функциям, настройкам и аудиту системы.",
        "permissions": ["admin.full_access"]
    },
]


def seed_roles(db: Session):
    print("Seeding roles...")

    # Сначала подтягиваем все права из БД в словарь для быстрого доступа
    stmt = select(Permission)
    permissions_in_db = db.execute(stmt).scalars().all()
    perm_map = {p.codename: p for p in permissions_in_db}

    for role_data in ROLES_DATA:
        stmt = select(Role).where(Role.name == role_data["name"])
        existing_role = db.execute(stmt).scalar_one_or_none()

        if not existing_role:
            new_role = Role(
                name=role_data["name"],
                description=role_data["description"]
            )

            # Привязываем права
            for perm_codename in role_data["permissions"]:
                if perm_codename in perm_map:
                    new_role.permissions.append(perm_map[perm_codename])
                else:
                    print(f"Warning: Permission '{perm_codename}' not found in DB for role '{role_data['name']}'")

            db.add(new_role)

    db.commit()
    print("Roles seeded successfully.")