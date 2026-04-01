from sqlmodel import create_engine, Session, SQLModel
from .core.config import settings
from app.models.user import User
from app.models.record import FinancialRecord

# We'll define settings in the next step
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} # Needed for SQLite
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session