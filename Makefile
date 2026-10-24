.PHONY: up down logs migrate seed test

# Поднять все сервисы
up:
	docker-compose up -d

# Остановить все сервисы
down:
	docker-compose down

# Посмотреть логи
logs:
	docker-compose logs -f

# Применить миграции БД
migrate:
	docker-compose exec backend alembic upgrade head

# Заполнить БД начальными данными
seed:
	docker-compose exec backend python app/db/seed/run.py

# Запустить тесты
test:
	docker-compose exec backend pytest

# Создать новую миграцию
makemigrations:
	docker-compose exec backend alembic revision --autogenerate -m "update"