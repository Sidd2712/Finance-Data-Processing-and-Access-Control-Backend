from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      
    pool_recycle=300,       
    connect_args={"sslmode": "require"}
)

def init_db():
    try:
        print("Checking cloud database connection...")
        SQLModel.metadata.create_all(engine)
        print("Neon Tables Synchronized!")
    except Exception as e:
        print(f"Error connecting to Neon: {e}")

def get_session():
    with Session(engine) as session:
        yield session