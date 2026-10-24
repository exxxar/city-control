from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class AttachmentRead(BaseModel):
    id: int
    file_url: str
    file_name: str
    mime_type: str
    file_size: int
    linked_entity_type: str
    linked_entity_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)