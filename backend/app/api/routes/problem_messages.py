# problem_messages.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.problem_message import ProblemMessage
from app.models.problem import Problem
from app.models.user import User
from app.api.deps import get_current_user
from pydantic import BaseModel

class MessageCreate(BaseModel):
    content: str

router = APIRouter()

@router.get("/{problem_id}/messages")
def get_messages(problem_id: int, db: Session = Depends(get_db)):
    msgs = db.execute(select(ProblemMessage).where(ProblemMessage.problem_id == problem_id)).scalars().all()
    return [{"id": m.id, "content": m.content, "user_id": m.user_id, "is_system": m.is_system} for m in msgs]

@router.post("/{problem_id}/messages", status_code=201)
def send_message(problem_id: int, payload: MessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.get(Problem, problem_id): raise HTTPException(404, "Problem not found")
    msg = ProblemMessage(problem_id=problem_id, user_id=current_user.id, content=payload.content)
    db.add(msg); db.commit(); db.refresh(msg)
    # TODO: Отправить Pusher event "problem.new_message"
    return {"id": msg.id, "content": msg.content}