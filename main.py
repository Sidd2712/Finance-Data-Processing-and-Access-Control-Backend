import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: Connecting to Neon PostgreSQL...")
    try:
        init_db()
        print("Database tables synchronized!")
    except Exception as e:
        print(f"Database connection failed: {e}")
    
    yield

app = FastAPI(
    title="Finance Dashboard API",
    description="A secure backend for managing financial records and dashboard analytics.",
    version="1.0.0",
    lifespan=lifespan # Link the lifespan logic here
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "project": "Finance Data Processing & Access Control",
        "status": "online",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True 
    )