from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.database import get_session
from app.models.user import User, UserRole
from app.crud.user import create_user, get_users
from app.schemas.user import UserCreate, UserRead
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