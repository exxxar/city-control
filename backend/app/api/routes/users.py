from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.user import User, user_roles
from app.models.role import Role
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.api.deps import get_current_user, require_permission
from app.core.security import hash_password

router = APIRouter()


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=List[UserRead], dependencies=[Depends(require_permission("user.view"))])
def list_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.execute(select(User).offset(skip).limit(limit)).scalars().all()


@router.post("/", response_model=UserRead, status_code=201, dependencies=[Depends(require_permission("user.manage"))])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none():
        raise HTTPException(400, "Email already registered")

    user = User(email=payload.email, hashed_password=hash_password(payload.password), full_name=payload.full_name,
                phone=payload.phone)

    if payload.role_ids:
        roles = db.execute(select(Role).where(Role.id.in_(payload.role_ids))).scalars().all()
        user.roles = list(roles)
    else:
        citizen_role = db.execute(select(Role).where(Role.name == "Гражданин")).scalar_one_or_none()
        if citizen_role: user.roles = [citizen_role]

    db.add(user);
    db.commit();
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(require_permission("user.view"))])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead, dependencies=[Depends(require_permission("user.manage"))])
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    role_ids = update_data.pop("role_ids", None)
    for key, value in update_data.items():
        setattr(user, key, value)

    if role_ids is not None:
        roles = db.execute(select(Role).where(Role.id.in_(role_ids))).scalars().all()
        user.roles = list(roles)

    db.commit();
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204, dependencies=[Depends(require_permission("user.manage"))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    db.delete(user);
    db.commit()