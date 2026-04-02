from uuid import UUID 
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole
from sqlmodel import SQLModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.VIEWER
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: UUID
    
    class Config:
        from_attributes = True

class UserUpdate(SQLModel):
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None