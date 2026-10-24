# backend/seed_reports.py
import random
from datetime import datetime, timedelta
from sqlalchemy import text
from app.db.session import SessionLocal
from app.models.problem import Problem
from app.models.user import User
from app.models.report import Report, ReportStatus


def seed_reports():
    print("🔄 Подключение к базе данных для создания отчётов...")
    db = SessionLocal()

    try:
        # 0. Создаем таблицу reports, если её еще нет
        print("🔧 Проверка наличия таблицы 'reports'...")
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                problem_id INT NOT NULL,
                executor_id INT NOT NULL,
                work_description TEXT,
                work_date DATETIME,
                photos_before_count INT DEFAULT 0,
                photos_after_count INT DEFAULT 0,
                materials_used TEXT,
                cost FLOAT DEFAULT 0.0,
                status ENUM('pending', 'approved', 'rejected', 'revision') DEFAULT 'pending',
                reject_reason TEXT,
                revision_comment TEXT,
                submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE,
                FOREIGN KEY (executor_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """))
        db.commit()
        print("✅ Таблица 'reports' проверена/создана.")

        # 1. Находим проблемы, которые уже в работе или решены
        problems = db.query(Problem).filter(
            Problem.status.in_(["in_progress", "resolved"])
        ).limit(10).all()

        if not problems:
            print(
                "⚠️ Не найдено проблем со статусом 'in_progress' или 'resolved'. Запустите seed_test_data.py сначала.")
            return

        # 2. Находим пользователей-исполнителей
        try:
            executors = db.query(User).join(User.roles).filter(
                User.roles.any(name="Исполнитель")
            ).all()
        except Exception:
            executors = []

        if not executors:
            executors = db.query(User).filter(User.is_active == True).limit(3).all()

        if not executors:
            print("⚠️ Не найдено пользователей для назначения исполнителями.")
            return

        report_templates = [
            {
                "desc": "Выполнен полный комплекс работ по устранению неисправности. Проведена замена оборудования, тестирование системы показало нормальную работу.",
                "materials": "Кабель ВВГнг 3х1.5 — 15 м, Автоматический выключатель 16А — 2 шт., Изолента — 1 рулон",
                "cost_range": (1500, 5000)
            },
            {
                "desc": "Произведена очистка территории от мусора. Вывезено 2 контейнера ТБО. Проведена дезинфекция площадки.",
                "materials": "Мешки для мусора 120л — 20 шт., Средства дезинфекции — 5 л",
                "cost_range": (3000, 8000)
            },
            {
                "desc": "Выполнен ямочный ремонт дорожного покрытия. Произведена фрезеровка, обработка битумной эмульсией и укладка асфальтобетонной смеси с уплотнением.",
                "materials": "Асфальтобетонная смесь мелкозернистая — 0.5 т, Битумная эмульсия — 20 л",
                "cost_range": (15000, 35000)
            },
            {
                "desc": "Проведен ремонт детской площадки. Заменены деревянные настилы, укреплены опорные столбы, нанесено защитное лакокрасочное покрытие.",
                "materials": "Доска обрезная 40х150 мм — 10 шт., Антисептик для дерева — 5 л., Краска фасадная — 10 л.",
                "cost_range": (8000, 20000)
            }
        ]

        added_count = 0
        for problem in problems:
            # Проверяем, нет ли уже отчёта для этой проблемы
            exists = db.query(Report).filter(Report.problem_id == problem.id).first()
            if not exists:
                executor = random.choice(executors)
                template = random.choice(report_templates)

                # Статус отчёта зависит от статуса проблемы
                if problem.status == "resolved":
                    report_status = random.choice([ReportStatus.APPROVED, ReportStatus.APPROVED, ReportStatus.REVISION])
                else:
                    report_status = random.choice([ReportStatus.PENDING, ReportStatus.REVISION])

                # Дата выполнения на 1-5 дней раньше отправки отчёта
                days_ago_submit = random.randint(1, 15)
                submitted_at = datetime.utcnow() - timedelta(days=days_ago_submit)
                work_date = submitted_at - timedelta(days=random.randint(1, 5))

                new_report = Report(
                    problem_id=problem.id,
                    executor_id=executor.id,
                    work_description=template["desc"],
                    work_date=work_date,
                    photos_before_count=random.randint(1, 3),
                    photos_after_count=random.randint(2, 5),
                    materials_used=template["materials"],
                    cost=random.uniform(template["cost_range"][0], template["cost_range"][1]),
                    status=report_status,
                    submitted_at=submitted_at
                )

                if report_status == ReportStatus.REVISION:
                    new_report.revision_comment = "Необходимо предоставить фотофиксацию скрытых работ и уточнить сроки гарантии."
                elif report_status == ReportStatus.REJECTED:
                    new_report.reject_reason = "Отчёт не соответствует фактическому объему выполненных работ. Требуется переделка."

                db.add(new_report)
                added_count += 1

        db.commit()

        if added_count > 0:
            print(f"✅ Успешно создано {added_count} отчётов.")
        else:
            print("ℹ️ Отчёты уже существуют или нет подходящих проблем.")

        print("\n🎉 Сидер отчётов успешно выполнен!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка при заполнении отчётов: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_reports()