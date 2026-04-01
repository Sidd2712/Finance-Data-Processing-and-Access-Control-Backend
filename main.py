import uvicorn
from fastapi import FastAPI
from app.database import init_db
from app.api.v1.api import api_router

app = FastAPI(
    title="Finance Dashboard API",
    description="A secure backend for managing financial records and dashboard analytics.",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "project": "Finance Data Processing & Access Control",
        "status": "online",
        "documentation": "/docs"
    }

# This block allows you to run 'python main.py'
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True  # Auto-restarts server when you save files
    )