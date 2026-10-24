# backend/seed_users.py
from app.db.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def seed_users_and_roles():
    print("🔄 Подключение к базе данных для создания пользователей...")
    db = SessionLocal()

    try:
        # ==========================================
        # 1. Создаем роли (если их еще нет)
        # ==========================================
        roles_data = [
            {"name": "Пользователь", "description": "Базовая роль для граждан"},
            {"name": "Модератор", "description": "Модерация обращений и инициатив"},
            {"name": "Исполнитель", "description": "Сотрудник, выполняющий работы"},
            {"name": "Руководитель органа", "description": "Руководство подразделением"},
            {"name": "Системный администратор", "description": "Полный доступ ко всем функциям"}
        ]

        created_roles = {}
        for r_data in roles_data:
            role = db.query(Role).filter(Role.name == r_data["name"]).first()
            if not role:
                role = Role(**r_data)
                db.add(role)
                db.flush()
            created_roles[r_data["name"]] = role

        db.commit()
        print("✅ Роли проверены/созданы.")

        # ==========================================
        # 2. Создаем тестовых пользователей
        # ==========================================
        users_data = [
            {
                "full_name": "Системный Администратор",
                "email": "admin@city.local",
                "password": "admin123",
                "phone": "+7 (999) 000-00-00",
                "role_name": "Системный администратор"
            },
            {
                "full_name": "Модератор Петрова",
                "email": "moderator@city.local",
                "password": "mod123",
                "phone": "+7 (999) 234-56-78",
                "role_name": "Модератор"
            },
            {
                "full_name": "Козлова Мария Александровна",
                "email": "executor@city.local",
                "password": "exec123",
                "phone": "+7 (999) 456-78-90",
                "role_name": "Исполнитель"
            },
            {
                "full_name": "Волкова Елена Николаевна",
                "email": "manager@city.local",
                "password": "man123",
                "phone": "+7 (999) 678-90-12",
                "role_name": "Руководитель органа"
            },
            {
                "full_name": "Иванов Иван Иванович",
                "email": "user@city.local",
                "password": "user123",
                "phone": "+7 (999) 123-45-67",
                "role_name": "Пользователь"
            }
        ]

        for u_data in users_data:
            existing_user = db.query(User).filter(User.email == u_data["email"]).first()
            if not existing_user:
                role = created_roles[u_data["role_name"]]

                # Создаем пользователя с правильным именем поля
                new_user = User(
                    full_name=u_data["full_name"],
                    email=u_data["email"],
                    hashed_password=get_password_hash(u_data["password"]),  # ← ИСПРАВЛЕНО
                    phone=u_data["phone"],
                    is_active=True
                )

                # Добавляем пользователя в сессию
                db.add(new_user)
                db.flush()  # Получаем ID пользователя

                # Добавляем роль через many-to-many связь
                # Вариант 1: Если в модели есть relationship 'roles'
                if hasattr(new_user, 'roles'):
                    new_user.roles.append(role)
                else:
                    # Вариант 2: Прямая вставка в таблицу user_roles
                    from sqlalchemy import text
                    db.execute(
                        text("INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)"),
                        {"user_id": new_user.id, "role_id": role.id}
                    )

                print(f"  ✅ Создан пользователь: {u_data['email']} ({u_data['role_name']})")

        db.commit()
        print("\n🎉 Пользователи успешно добавлены в базу данных!")
        print("\n📋 Учетные данные для входа:")
        print("=" * 60)
        print(f"{'Email':<25} {'Пароль':<15} {'Роль'}")
        print("-" * 60)
        for u in users_data:
            print(f"{u['email']:<25} {u['password']:<15} {u['role_name']}")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка при заполнении пользователей: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_users_and_roles()