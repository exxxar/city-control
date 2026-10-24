from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.permission import Permission

# Список всех прав в системе
PERMISSIONS_DATA = [
    # Проблемы (Problems)
    {"codename": "problem.view_public", "name": "Просмотр публичных проблем",
     "description": "Гости и граждане могут видеть карту проблем"},
    {"codename": "problem.create", "name": "Создание проблем", "description": "Возможность отправлять новые обращения"},
    {"codename": "problem.view_all", "name": "Просмотр всех проблем",
     "description": "Доступ ко всем проблемам, включая скрытые/черновики"},
    {"codename": "problem.moderate", "name": "Модерация проблем",
     "description": "Подтверждение, отклонение, запрос уточнений"},
    {"codename": "problem.assign", "name": "Назначение исполнителей",
     "description": "Передача проблемы ответственному органу/исполнителю"},
    {"codename": "problem.change_status", "name": "Изменение статусов",
     "description": "Полный доступ к изменению workflow статусов"},
    {"codename": "problem.delete", "name": "Удаление проблем",
     "description": "Физическое или логическое удаление обращений"},

    # Инициативы и Мероприятия (Initiatives & Events)
    {"codename": "initiative.create", "name": "Создание инициатив",
     "description": "Подача предложений по благоустройству"},
    {"codename": "initiative.moderate", "name": "Модерация инициатив",
     "description": "Рассмотрение и согласование инициатив"},
    {"codename": "event.create", "name": "Создание заявок на мероприятия", "description": "Подача заявок на события"},
    {"codename": "event.approve", "name": "Согласование мероприятий",
     "description": "Утверждение заявок на мероприятия"},

    # Гео-метки и Карты (GeoTags & Maps)
    {"codename": "geo_tag.view", "name": "Просмотр гео-меток", "description": "Доступ к данным гео-меток"},
    {"codename": "geo_tag.manage", "name": "Управление гео-метками",
     "description": "Создание, редактирование GPS, зон и QR-кодов"},
    {"codename": "indoor_map.manage", "name": "Управление внутренними картами",
     "description": "Загрузка планов зданий, создание этажей и зон"},

    # Территории и Объекты (Territories & Objects)
    {"codename": "territory.manage", "name": "Управление территориями",
     "description": "Редактирование иерархии муниципалитетов, районов, улиц"},
    {"codename": "object.manage", "name": "Управление объектами",
     "description": "Редактирование муниципальных объектов и зданий"},

    # Пользователи и Роли (Users & Roles)
    {"codename": "user.view", "name": "Просмотр пользователей", "description": "Доступ к списку пользователей"},
    {"codename": "user.manage", "name": "Управление пользователями",
     "description": "Блокировка, смена ролей, редактирование профилей"},
    {"codename": "role.manage", "name": "Управление ролями и правами",
     "description": "Создание ролей и назначение прав"},

    # SLA и Аналитика (SLA & Analytics)
    {"codename": "sla.manage", "name": "Управление SLA",
     "description": "Настройка политик SLA для категорий и приоритетов"},
    {"codename": "analytics.view", "name": "Просмотр аналитики",
     "description": "Доступ к дашбордам, тепловым картам и индексам"},

    # Системные (System)
    {"codename": "audit.view", "name": "Просмотр журнала аудита",
     "description": "Доступ к логам действий пользователей"},
    {"codename": "settings.manage", "name": "Управление настройками системы",
     "description": "Глобальные настройки, интеграции, email, pusher"},
    {"codename": "admin.full_access", "name": "Полный доступ администратора",
     "description": "Абсолютные права в системе (супер-админ)"},
]


def seed_permissions(db: Session):
    print("Seeding permissions...")
    for perm_data in PERMISSIONS_DATA:
        # Проверяем, существует ли уже такое право
        stmt = select(Permission).where(Permission.codename == perm_data["codename"])
        existing = db.execute(stmt).scalar_one_or_none()

        if not existing:
            new_perm = Permission(**perm_data)
            db.add(new_perm)

    db.commit()
    print(f"Permissions seeded successfully.")