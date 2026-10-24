import pusher
from app.core.config import settings

class PusherService:
    def __init__(self):
        self.client = pusher.Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET,
            cluster=settings.PUSHER_CLUSTER,
            ssl=True
        )

    def trigger(self, channel: str, event_name: str, data: dict):
        """Отправляет событие в канал Pusher."""
        try:
            self.client.trigger(channel, event_name, data)
        except Exception as e:
            print(f"Pusher error: {e}")

# Синглтон для использования в других сервисах
pusher_service = PusherService()