import uuid
from uuid import UUID
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .record import FinancialRecord

class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"

class User(SQLModel, table=True):
    # We use uuid4 for random, non-sequential uniqueness
    id: UUID = Field(
        default_factory=uuid.uuid4, 
        primary_key=True,
        index=True,
        nullable=False
    )
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.VIEWER)
    is_active: bool = Field(default=True)
    
    records: List["FinancialRecord"] = Relationship(back_populates="creator")