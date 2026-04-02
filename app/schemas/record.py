from uuid import UUID 
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel

class RecordBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: str
    category: str
    description: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(SQLModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None
    date: Optional[datetime] = None

class RecordRead(RecordBase):
    id: UUID     
    user_id: UUID
    date: datetime

    class Config:
        from_attributes = True