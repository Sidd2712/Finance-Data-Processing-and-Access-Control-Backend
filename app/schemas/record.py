from uuid import UUID 
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel

class RecordBase(BaseModel):
    amount: float = Field(..., gt=0, description="The transaction amount must be positive")
    type: str = Field(pattern="^(income|expense)$")
    category: str
    date: datetime = Field(default_factory=datetime.utcnow)
    description: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

class RecordRead(RecordBase):
    id: UUID     
    user_id: UUID

    class Config:
        from_attributes = True