from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from uuid import UUID
from app.database import get_session
from app.models.user import User, UserRole
from app.crud.user import create_user, get_users
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.api.permissions import get_session, get_current_user, RoleChecker

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_new_user(
    user_in: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])) 
):
    return create_user(session, user_in)

@router.get("/", response_model=list[UserRead])
def read_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN]))
):
    return get_users(session)

@router.patch("/{user_id}", response_model=UserRead)
def update_user_status(
    user_id: UUID,
    user_in: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN]))
):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserRead)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return current_user