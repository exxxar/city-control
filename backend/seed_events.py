# backend/seed_events.py
import random
from datetime import datetime, timedelta, date
from sqlalchemy import text
from app.db.session import SessionLocal
from app.models.user import User
from app.models.event import Event, EventStatus


def seed_events():
    print("🔄 Подключение к базе данных для создания мероприятий...")
    db = SessionLocal()

    try:
        # 0. Создаем таблицу events, если её еще нет
        print("🔧 Проверка наличия таблицы 'events'...")
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                location VARCHAR(255),
                event_date DATE,
                organizer_name VARCHAR(255) NOT NULL,
                organizer_phone VARCHAR(50),
                target_audience VARCHAR(255),
                participants_count INT DEFAULT 0,
                status ENUM('pending', 'approved', 'rejected', 'completed', 'cancelled') DEFAULT 'pending',
                reject_reason TEXT,
                created_by_id INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """))
        db.commit()
        print("✅ Таблица 'events' проверена/создана.")

        # 1. Получаем пользователей
        users = db.query(User).limit(5).all()
        if not users:
            print("⚠️ Пользователи не найдены. Сначала запустите seed_test_data.py")
            return

        # 2. Данные для мероприятий
        events_data = [
            {
                "title": "Субботник в центральном парке",
                "description": "Массовая уборка территории парка от мусора и листвы. Инвентарь предоставляется.",
                "location": "Центральный парк",
                "organizer": "Иванов Иван Иванович",
                "phone": "+7 (999) 444-44-44",
                "audience": "Все желающие",
                "participants": 150,
                "status": EventStatus.PENDING,
                "days_offset": 5
            },
            {
                "title": "Ярмарка фермерских продуктов",
                "description": "Продажа свежих фермерских продуктов: молоко, мясо, овощи, мёд. Мастер-классы для детей.",
                "location": "пл. Ленина",
                "organizer": "Петрова Анна Сергеевна",
                "phone": "+7 (999) 555-55-55",
                "audience": "Семьи с детьми, пенсионеры",
                "participants": 300,
                "status": EventStatus.APPROVED,
                "days_offset": 8
            },
            {
                "title": "Концерт ко Дню города",
                "description": "Праздничный концерт с участием местных творческих коллективов. Фейерверк в завершении.",
                "location": "Городская площадь",
                "organizer": "Администрация города",
                "phone": "+7 (999) 000-00-00",
                "audience": "Все жители города",
                "participants": 2000,
                "status": EventStatus.COMPLETED,
                "days_offset": -15
            },
            {
                "title": "Турнир по дворовому футболу",
                "description": "Любительский турнир среди дворовых команд. Возраст 14-18 лет. Призы победителям.",
                "location": "Стадион 'Юность'",
                "organizer": "Иванов Иван Иванович",
                "phone": "+7 (999) 444-44-44",
                "audience": "Молодежь 14-18 лет",
                "participants": 120,
                "status": EventStatus.PENDING,
                "days_offset": 12
            },
            {
                "title": "Лекция по истории города",
                "description": "Известный краевед расскажет о малоизвестных фактах истории нашего города.",
                "location": "Городская библиотека",
                "organizer": "Петрова Анна Сергеевна",
                "phone": "+7 (999) 555-55-55",
                "audience": "Взрослые, студенты",
                "participants": 80,
                "status": EventStatus.APPROVED,
                "days_offset": 20
            },
            {
                "title": "Благотворительный забег",
                "description": "Забег на 5 км. Все собранные средства пойдут в детский хоспис.",
                "location": "Набережная реки",
                "organizer": "Иванов Иван Иванович",
                "phone": "+7 (999) 444-44-44",
                "audience": "Все желающие",
                "participants": 500,
                "status": EventStatus.REJECTED,
                "days_offset": 3,
                "reject_reason": "Не предоставлено разрешение от ГИБДД на перекрытие движения."
            },
            {
                "title": "Мастер-класс по рисованию",
                "description": "Бесплатный мастер-класс для детей 6-12 лет. Все материалы предоставляются.",
                "location": "Дом культуры",
                "organizer": "Петрова Анна Сергеевна",
                "phone": "+7 (999) 555-55-55",
                "audience": "Дети 6-12 лет",
                "participants": 30,
                "status": EventStatus.PENDING,
                "days_offset": 7
            },
            {
                "title": "Фестиваль уличной еды",
                "description": "Фестиваль с участием 20 фуд-траков. Живая музыка, конкурсы.",
                "location": "Центральный парк",
                "organizer": "Администрация города",
                "phone": "+7 (999) 000-00-00",
                "audience": "Все желающие",
                "participants": 1500,
                "status": EventStatus.APPROVED,
                "days_offset": 25
            }
        ]

        added_count = 0
        for e_data in events_data:
            exists = db.query(Event).filter(Event.title == e_data["title"]).first()
            if not exists:
                creator = random.choice(users)
                event_date = date.today() + timedelta(days=e_data["days_offset"])
                created_at = datetime.utcnow() - timedelta(days=random.randint(1, 30))

                new_event = Event(
                    title=e_data["title"],
                    description=e_data["description"],
                    location=e_data["location"],
                    event_date=event_date,
                    organizer_name=e_data["organizer"],
                    organizer_phone=e_data["phone"],
                    target_audience=e_data["audience"],
                    participants_count=e_data["participants"],
                    status=e_data["status"],
                    reject_reason=e_data.get("reject_reason"),
                    created_by_id=creator.id,
                    created_at=created_at
                )
                db.add(new_event)
                added_count += 1

        db.commit()

        if added_count > 0:
            print(f"✅ Успешно добавлено {added_count} мероприятий.")
        else:
            print("ℹ️ Мероприятия уже существуют.")

        print("\n🎉 Сидер мероприятий успешно выполнен!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка при заполнении мероприятий: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_events()