from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

class AuditService:
    def __init__(self, db: Session):
        self.db = db

    def log_action(
        self, user_id: Optional[int], action: str, entity_type: str, entity_id: Optional[int],
        old_values: Optional[Dict[str, Any]] = None, new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None
    ):
        log = AuditLog(
            user_id=user_id, action=action, entity_type=entity_type, entity_id=entity_id,
            old_values=old_values, new_values=new_values, ip_address=ip_address
        )
        self.db.add(log)
        self.db.commit()