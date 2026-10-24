import pusher
from app.core.config import settings
from loguru import logger

class PusherClient:
    def __init__(self):
        if settings.PUSHER_KEY and settings.PUSHER_SECRET:
            self.client = pusher.Pusher(
                app_id=settings.PUSHER_APP_ID,
                key=settings.PUSHER_KEY,
                secret=settings.PUSHER_SECRET,
                cluster=settings.PUSHER_CLUSTER,
                ssl=True
            )
        else:
            self.client = None

    def trigger(self, channel: str, event_name: str, data: dict):
        if self.client:
            try:
                self.client.trigger(channel, event_name, data)
            except Exception as e:
                logger.error(f"Pusher error: {e}")
        else:
            logger.debug(f"[PUSHER MOCK] Channel: {channel}, Event: {event_name}, Data: {data}")

pusher_client = PusherClient()