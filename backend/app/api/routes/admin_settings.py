from fastapi import APIRouter, Depends
from app.api.deps import require_permission
from pydantic import BaseModel

# Мок настроек (в реальности хранится в БД или Redis)
SETTINGS_STORE = {
    "pusher_enabled": True,
    "email_notifications_enabled": True,
    "auto_blur_faces": False
}

class SettingsUpdate(BaseModel):
    pusher_enabled: bool | None = None
    email_notifications_enabled: bool | None = None
    auto_blur_faces: bool | None = None

router = APIRouter()

@router.get("/", dependencies=[Depends(require_permission("settings.manage"))])
def get_settings():
    return SETTINGS_STORE

@router.patch("/", dependencies=[Depends(require_permission("settings.manage"))])
def update_settings(payload: SettingsUpdate):
    for key, value in payload.model_dump(exclude_unset=True).items():
        SETTINGS_STORE[key] = value
    return {"message": "Settings updated", "current": SETTINGS_STORE}