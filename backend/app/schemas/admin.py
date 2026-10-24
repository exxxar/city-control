from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# --- Category & Priority (Справочники) ---
class CategoryRead(BaseModel):
    id: int
    name: str
    slug: str
    parent_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class PriorityRead(BaseModel):
    id: int
    name: str
    level: int
    color: str
    model_config = ConfigDict(from_attributes=True)

# --- Executor Organization ---
class ExecutorOrganizationRead(BaseModel):
    id: int
    name: str
    territory_id: Optional[int] = None
    email: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# --- Audit Log ---
class AuditLogRead(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    entity_type: str
    entity_id: Optional[int] = None
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Admin Settings (Пример) ---
class SystemSettingsUpdate(BaseModel):
    pusher_enabled: Optional[bool] = None
    email_notifications_enabled: Optional[bool] = None
    auto_blur_faces: Optional[bool] = None