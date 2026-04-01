import uuid
from uuid import UUID
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User

class FinancialRecord(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid.uuid4, 
        primary_key=True,
        index=True,
        nullable=False
    )
    amount: float = Field(nullable=False)
    type: str = Field(index=True) 
    category: str = Field(index=True)
    date: datetime = Field(default_factory=datetime.utcnow)
    description: Optional[str] = None
    
    # Must match the User.id type exactly
    user_id: UUID = Field(foreign_key="user.id")
    creator: "User" = Relationship(back_populates="records")