from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.api.deps import require_permission

router = APIRouter()

@router.get("/logs", dependencies=[Depends(require_permission("audit.view"))])
def list_audit_logs(db: Session = Depends(get_db)):
    logs = db.execute(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(100)).scalars().all()
    return [{"id": l.id, "action": l.action, "entity": l.entity_type, "user_id": l.user_id, "date": l.created_at.isoformat()} for l in logs]