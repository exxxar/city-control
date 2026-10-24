from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# Инициализация Celery
celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.document_tasks",
        "app.tasks.email_tasks",
        "app.tasks.media_tasks",
        "app.tasks.sla_tasks",
        "app.tasks.cleanup_tasks",
    ]
)

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=30 * 60,  # Лимит 30 минут на задачу
    task_soft_time_limit=25 * 60,
    worker_send_task_events=True,
    task_send_sent_event=True,
    timezone="UTC",
    enable_utc=True,
)

# Настройка периодических задач (Celery Beat)
celery_app.conf.beat_schedule = {
    "check-sla-overdue-every-5-minutes": {
        "task": "app.tasks.sla_tasks.check_sla_overdue",
        "schedule": 300.0,  # Каждые 5 минут
    },
    "cleanup-temp-files-daily": {
        "task": "app.tasks.cleanup_tasks.cleanup_temp_files",
        "schedule": crontab(hour=3, minute=0),  # Каждый день в 03:00
    },
}