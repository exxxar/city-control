from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.document import DocumentType


class DocumentRead(BaseModel):
    id: int
    doc_type: DocumentType
    file_url: str
    file_name: str
    problem_id: Optional[int] = None
    generated_by_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)