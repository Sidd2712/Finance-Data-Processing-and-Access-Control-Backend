from uuid import UUID  # <--- Add this import
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.VIEWER
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: UUID  # <--- Change from int to UUID
    
    class Config:
        from_attributes = True