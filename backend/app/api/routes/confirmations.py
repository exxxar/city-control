# confirmations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.problem_confirmation import ProblemConfirmation
from app.models.problem import Problem
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/{problem_id}/confirmations", status_code=201)
def confirm_problem(problem_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    problem = db.get(Problem, problem_id)
    if not problem: raise HTTPException(404, "Problem not found")

    conf = ProblemConfirmation(problem_id=problem_id, user_id=current_user.id, is_verified=True)
    db.add(conf)

    problem.confirmations_count += 1
    # TODO: Пересчитать рейтинг проблемы (problem_rating_service)

    db.commit()
    return {"message": "Problem confirmed", "total_confirmations": problem.confirmations_count}