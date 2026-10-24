# backend/seed_initiatives.py
import random
from datetime import datetime, timedelta
from sqlalchemy import text
from app.db.session import SessionLocal
from app.models.user import User
from app.models.initiative import Initiative, InitiativeStatus


def seed_initiatives():
    print("🔄 Подключение к базе данных для создания инициатив...")
    db = SessionLocal()

    try:
        # 1. Получаем ID существующих пользователей
        users_emails = ["user1@city.local", "user2@city.local", "mod@city.local", "exec1@city.local"]
        users_map = {}
        for email in users_emails:
            user = db.query(User).filter(User.email == email).first()
            if user:
                users_map[email] = user.id

        if not users_map:
            print("⚠️ Пользователи не найдены. Сначала запустите seed_test_data.py или seed_users.py")
            return

        # 2. Получаем ID существующих категорий
        categories_names = ["Дороги и тротуары", "ЖКХ и коммунальные услуги", "Благоустройство", "Освещение"]
        categories_map = {}
        for cat_name in categories_names:
            result = db.execute(text("SELECT id FROM categories WHERE name = :name"), {"name": cat_name})
            row = result.fetchone()
            if row:
                categories_map[cat_name] = row[0]

        # 3. Данные для инициатив (18 разнообразных записей)
        initiatives_data = [
            {"title": "Установка воркаут-площадки в парке",
             "description": "Предлагаю установить турники, брусья и рукоход в центральной части парка для занятий спортом молодежи.",
             "category": "Благоустройство", "author": "user1@city.local", "status": InitiativeStatus.NEW,
             "support_count": 145},
            {"title": "Организация ярмарки выходного дня",
             "description": "Разрешить проведение ярмарки фермерских продуктов каждые выходные на центральной площади.",
             "category": "Благоустройство", "author": "user2@city.local", "status": InitiativeStatus.ACCEPTED,
             "support_count": 89},
            {"title": "Запрет на парковку у детской площадки",
             "description": "Установить знаки и бетонные столбики, чтобы машины не парковались на газоне у площадки.",
             "category": "Дороги и тротуары", "author": "user1@city.local", "status": InitiativeStatus.COMPLETED,
             "support_count": 210},
            {"title": "Создание клуба настольного тенниса",
             "description": "Выделить помещение в местном ДК для бесплатной секции настольного тенниса.",
             "category": "Благоустройство", "author": "user2@city.local", "status": InitiativeStatus.REJECTED,
             "support_count": 34},
            {"title": "Озеленение дворовых территорий",
             "description": "Массовая высадка деревьев и кустарников во дворах многоквартирных домов района.",
             "category": "Благоустройство", "author": "mod@city.local", "status": InitiativeStatus.UNDER_REVIEW,
             "support_count": 67},
            {"title": "Установка пандусов в подъездах",
             "description": "Оборудовать все подъезды домов на ул. Ленина съемными пандусами для маломобильных граждан.",
             "category": "ЖКХ и коммунальные услуги", "author": "user1@city.local",
             "status": InitiativeStatus.IN_PROGRESS, "support_count": 112},
            {"title": "Ремонт детской площадки 'Сказка'",
             "description": "Замена покрытия на безопасное, ремонт качелей и установка новой песочницы с крышкой.",
             "category": "Благоустройство", "author": "user2@city.local", "status": InitiativeStatus.COMPLETED,
             "support_count": 189},
            {"title": "Организация велодорожки вдоль набережной",
             "description": "Нанести разметку и установить ограждения для выделения безопасной велозоны.",
             "category": "Дороги и тротуары", "author": "exec1@city.local", "status": InitiativeStatus.NEW,
             "support_count": 340},
            {"title": "Замена старых лавочек в сквере",
             "description": "Демонтаж аварийных лавочек и установка новых, антивандальных, из металлокомпозита.",
             "category": "Благоустройство", "author": "user1@city.local", "status": InitiativeStatus.ACCEPTED,
             "support_count": 76},
            {"title": "Установка урн для раздельного сбора мусора",
             "description": "Замена обычных урн на двойные (пластик/бумага и смешанные отходы) во всех дворах.",
             "category": "ЖКХ и коммунальные услуги", "author": "user2@city.local",
             "status": InitiativeStatus.UNDER_REVIEW, "support_count": 55},
            {"title": "Освещение пешеходного перехода у школы №5",
             "description": "Установка дополнительного столба с ярким LED-освещением и мигающим светофором.",
             "category": "Освещение", "author": "mod@city.local", "status": InitiativeStatus.IN_PROGRESS,
             "support_count": 201},
            {"title": "Создание огороженной зоны для выгула собак",
             "description": "Установка забора, урн для экскрементов и тренажеров для собак в парке.",
             "category": "Благоустройство", "author": "user1@city.local", "status": InitiativeStatus.NEW,
             "support_count": 98},
            {"title": "Капитальный ремонт крыши дома №15",
             "description": "Устранение протечек и замена гидроизоляционного слоя на крыше.",
             "category": "ЖКХ и коммунальные услуги", "author": "user2@city.local", "status": InitiativeStatus.REJECTED,
             "support_count": 12},
            {"title": "Установка современных остановочных павильонов",
             "description": "Замена старых остановок на новые, с USB-зарядками, расписанием и обогревом.",
             "category": "Дороги и тротуары", "author": "exec1@city.local", "status": InitiativeStatus.ACCEPTED,
             "support_count": 134},
            {"title": "Праздничная иллюминация к Новому году",
             "description": "Украшение центральных улиц и парка гирляндами и световыми фигурами.",
             "category": "Освещение", "author": "user1@city.local", "status": InitiativeStatus.COMPLETED,
             "support_count": 412},
            {"title": "Обустройство площадки для воркаута",
             "description": "Дополнительное оборудование уже существующей спортзоны новыми тренажерами.",
             "category": "Благоустройство", "author": "user2@city.local", "status": InitiativeStatus.UNDER_REVIEW,
             "support_count": 88},
            {"title": "Высадка 'Аллеи памяти'",
             "description": "Посадка 50 молодых дубов в честь ветеранов в городском сквере.",
             "category": "Благоустройство", "author": "mod@city.local", "status": InitiativeStatus.NEW,
             "support_count": 156},
            {"title": "Установка камер видеонаблюдения во дворах",
             "description": "Интеграция дворовых камер в систему 'Безопасный город' для предотвращения вандализма.",
             "category": "ЖКХ и коммунальные услуги", "author": "user1@city.local",
             "status": InitiativeStatus.IN_PROGRESS, "support_count": 267},
        ]

        added_count = 0
        for i_data in initiatives_data:
            # Проверяем, нет ли уже такой инициативы
            exists = db.query(Initiative).filter(Initiative.title == i_data["title"]).first()
            if not exists:
                author_id = users_map.get(i_data["author"])
                # Если категория не найдена, берем первую попавшуюся или None
                cat_id = categories_map.get(i_data["category"], next(iter(categories_map.values()), None))

                # Генерируем случайную дату за последние 60 дней
                days_ago = random.randint(1, 60)
                created_at = datetime.utcnow() - timedelta(days=days_ago)

                new_initiative = Initiative(
                    title=i_data["title"],
                    description=i_data["description"],
                    status=i_data["status"],
                    category_id=cat_id,
                    created_by_id=author_id,
                    support_count=i_data["support_count"],
                    created_at=created_at
                )
                db.add(new_initiative)
                added_count += 1

        db.commit()

        if added_count > 0:
            print(f"✅ Успешно добавлено {added_count} новых инициатив.")
        else:
            print("ℹ️ Инициативы уже существуют, новые не добавлены.")

        print("\n🎉 Сидер инициатив успешно выполнен!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка при заполнении инициатив: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_initiatives()