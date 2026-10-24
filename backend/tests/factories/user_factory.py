from app.models.user import User
from app.models.role import Role
from app.core.security import hash_password


def create_user(db, email="test@city.local", password="password", role_name="Гражданин"):
    user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name="Test User",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    role = db.query(Role).filter(Role.name == role_name).first()
    if role:
        user.roles.append(role)
        db.commit()
    return user