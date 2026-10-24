# backend/seed_test_data.py
import random
import re
from datetime import datetime, timedelta
from sqlalchemy import text
from app.db.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.problem import Problem  
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Простая функция для генерации slug из названия
def generate_slug(name: str) -> str:
    # Таблица транслитерации (базовая)
    cyrillic_to_latin = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        ' ': '-', '_': '-', 'А': 'a', 'Б': 'b', 'В': 'v', 'Г': 'g', 'Д': 'd',
        'Е': 'e', 'Ё': 'yo', 'Ж': 'zh', 'З': 'z', 'И': 'i', 'Й': 'y', 'К': 'k',
        'Л': 'l', 'М': 'm', 'Н': 'n', 'О': 'o', 'П': 'p', 'Р': 'r', 'С': 's',
        'Т': 't', 'У': 'u', 'Ф': 'f', 'Х': 'kh', 'Ц': 'ts', 'Ч': 'ch', 'Ш': 'sh',
        'Щ': 'shch', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'e', 'Ю': 'yu', 'Я': 'ya'
    }
    
    # Транслитерируем
    slug = ''.join(cyrillic_to_latin.get(c, c) for c in name)
    # Оставляем только буквы, цифры и дефисы
    slug = re.sub(r'[^a-z0-9\-]', '', slug.lower())
    # Убираем множественные дефисы
    slug = re.sub(r'-+', '-', slug)
    # Убираем дефисы по краям
    slug = slug.strip('-')
    
    return slug or 'category'

def seed_test_data():
    print("🔄 Подключение к базе данных для создания тестовых данных...")
    db = SessionLocal()
    
    try:
        # 1. Создаем роли
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

        # 2. Создаем пользователей
        users_data = [
            {"full_name": "Администратор Системы", "email": "admin@city.local", "password": "admin123", "role_name": "Системный администратор", "phone": "+7 (999) 000-00-00"},
            {"full_name": "Модератор Петрова", "email": "mod@city.local", "password": "mod123", "role_name": "Модератор", "phone": "+7 (999) 111-11-11"},
            {"full_name": "Козлова Мария (ЖКХ)", "email": "exec1@city.local", "password": "exec123", "role_name": "Исполнитель", "phone": "+7 (999) 222-22-22"},
            {"full_name": "Смирнов Виктор (Дороги)", "email": "exec2@city.local", "password": "exec123", "role_name": "Исполнитель", "phone": "+7 (999) 333-33-33"},
            {"full_name": "Иванов Иван Иванович", "email": "user1@city.local", "password": "user123", "role_name": "Пользователь", "phone": "+7 (999) 444-44-44"},
            {"full_name": "Петрова Анна Сергеевна", "email": "user2@city.local", "password": "user123", "role_name": "Пользователь", "phone": "+7 (999) 555-55-55"},
        ]
        created_users = {}
        for u_data in users_data:
            user = db.query(User).filter(User.email == u_data["email"]).first()
            if not user:
                role = created_roles[u_data["role_name"]]
                new_user = User(
                    full_name=u_data["full_name"],
                    email=u_data["email"],
                    hashed_password=get_password_hash(u_data["password"]),
                    phone=u_data["phone"],
                    is_active=True
                )
                db.add(new_user)
                db.flush()
                db.execute(text("INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)"), 
                           {"user_id": new_user.id, "role_id": role.id})
            created_users[u_data["email"]] = db.query(User).filter(User.email == u_data["email"]).first()
        db.commit()
        print("✅ Пользователи созданы.")

        # 3. Создаем категории в таблице 'categories'
        # Теперь передаем и name, и slug
        categories_names = [
            "Дороги и тротуары",
            "ЖКХ и коммунальные услуги",
            "Благоустройство",
            "Освещение",
        ]
        created_category_ids = {}
        for cat_name in categories_names:
            result = db.execute(text("SELECT id FROM categories WHERE name = :name"), {"name": cat_name})
            row = result.fetchone()
            if row:
                created_category_ids[cat_name] = row[0]
            else:
                # Генерируем slug из названия
                slug = generate_slug(cat_name)
                
                # Проверяем, нет ли уже такого slug (на случай дублей)
                slug_check = db.execute(text("SELECT id FROM categories WHERE slug = :slug"), {"slug": slug})
                if slug_check.fetchone():
                    slug = f"{slug}-{random.randint(100, 999)}"
                
                # Вставляем с name и slug
                insert_result = db.execute(
                    text("INSERT INTO categories (name, slug) VALUES (:name, :slug)"),
                    {"name": cat_name, "slug": slug}
                )
                created_category_ids[cat_name] = insert_result.lastrowid
        db.commit()
        print("✅ Категории созданы в таблице 'categories'.")

        # 4. Создаем реалистичные проблемы (Обращения)
        problems_data = [
            {"title": "Огромная яма на проезжей части", "description": "Яма глубиной около 15 см, опасно для машин.\n\n📍 Адрес: ул. Ленина, д. 15, у подъезда 2", "category": "Дороги и тротуары", "author": "user1@city.local", "status": "new"},
            {"title": "Не горит фонарь уже неделю", "description": "Темно, страшно ходить вечером.\n\n📍 Адрес: Парк культуры, центральная аллея", "category": "Освещение", "author": "user2@city.local", "status": "approved"},
            {"title": "Мусорный бак переполнен", "description": "Мусор разбросан вокруг, неприятный запах.\n\n📍 Адрес: ул. Пушкина, д. 5, во дворе", "category": "Благоустройство", "author": "user1@city.local", "status": "in_progress"},
            {"title": "Прорыв трубы, течет вода", "description": "Затапливает подвал, вода идет по улице.\n\n📍 Адрес: ул. Гагарина, д. 22", "category": "ЖКХ и коммунальные услуги", "author": "user2@city.local", "status": "resolved"},
            {"title": "Сломанная лавочка в парке", "description": "Спинка оторвана, сидеть невозможно.\n\n📍 Адрес: Центральный парк, у пруда", "category": "Благоустройство", "author": "user1@city.local", "status": "rejected"},
            {"title": "Отсутствует дорожный знак", "description": "Снесли во время бури.\n\n📍 Адрес: ул. Советская, д. 8, перекресток", "category": "Дороги и тротуары", "author": "user2@city.local", "status": "new"},
            {"title": "Шумная стройка ночью", "description": "Работают после 23:00, невозможно спать.\n\n📍 Адрес: ул. Строителей, д. 1", "category": "Благоустройство", "author": "user1@city.local", "status": "in_progress"},
            {"title": "Детская горка ржавая", "description": "Ребенок поранился об острый край.\n\n📍 Адрес: ул. Мира, д. 10, двор", "category": "Благоустройство", "author": "user2@city.local", "status": "approved"},
            {"title": "Холодные батареи в квартире", "description": "Температура в комнате не превышает 16 градусов.\n\n📍 Адрес: ул. Кирова, д. 45, кв. 12", "category": "ЖКХ и коммунальные услуги", "author": "user1@city.local", "status": "resolved"},
            {"title": "Не работает лифт", "description": "Лифт не работает уже 3 дня.\n\n📍 Адрес: ул. Ленина, д. 15, подъезд 3", "category": "ЖКХ и коммунальные услуги", "author": "user2@city.local", "status": "in_progress"},
        ]

        for p_data in problems_data:
            exists = db.query(Problem).filter(Problem.title == p_data["title"]).first()
            if not exists:
                author_user = created_users[p_data["author"]]
                
                days_ago = random.randint(1, 30)
                created_at = datetime.utcnow() - timedelta(days=days_ago)

                new_problem = Problem(
                    title=p_data["title"],
                    description=p_data["description"],
                    status=p_data["status"],
                    category_id=created_category_ids[p_data["category"]],
                    created_by_id=author_user.id,
                    created_at=created_at
                )
                db.add(new_problem)
        
        db.commit()
        print("✅ Обращения созданы.")
        
        print("\n🎉 Тестовые данные успешно добавлены в базу данных!")
        print("\n📋 Учетные данные для входа в админку:")
        print("=" * 65)
        print(f"{'Email':<25} {'Пароль':<15} {'Роль'}")
        print("-" * 65)
        for u in users_data:
            print(f"{u['email']:<25} {u['password']:<15} {u['role_name']}")
        print("=" * 65)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка при заполнении данных: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_test_data()