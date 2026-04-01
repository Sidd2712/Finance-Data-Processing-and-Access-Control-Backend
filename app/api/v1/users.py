from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.database import get_session
from app.models.user import User
from app.crud.user import create_user, get_users
from app.schemas.user import UserCreate, UserRead

router = APIRouter()

@router.post("/", response_model=UserRead)
def register_user(user_in: UserCreate, session: Session = Depends(get_session)):
    return create_user(session, user_in)

@router.get("/", response_model=List[UserRead])
def list_users(session: Session = Depends(get_session)):
    return get_users(session)