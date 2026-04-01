from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core import security

def create_user(session: Session, user_in: UserCreate):
    # In a real app, we would hash the password here. 
    # For now, we'll store it (we can add hashing later).
    hashed_pas = security.get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pas,
        role=user_in.role,
        is_active=user_in.is_active
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_users(session: Session):
    return session.exec(select(User)).all()