# problem_subscriptions.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.db.session import get_db
from app.models.problem_subscription import ProblemSubscription
from app.models.problem import Problem
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/{problem_id}/subscribe", status_code=201)
def subscribe(problem_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.get(Problem, problem_id): raise HTTPException(404, "Problem not found")
    sub = ProblemSubscription(problem_id=problem_id, user_id=current_user.id)
    db.add(sub); db.commit()
    return {"message": "Subscribed"}

@router.delete("/{problem_id}/subscribe", status_code=204)
def unsubscribe(problem_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(delete(ProblemSubscription).where(
        ProblemSubscription.problem_id == problem_id,
        ProblemSubscription.user_id == current_user.id
    ))
    db.commit()