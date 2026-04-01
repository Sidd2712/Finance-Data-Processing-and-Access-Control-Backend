from fastapi import APIRouter
from app.api.v1 import users, records, dashboard

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(records.router, prefix="/records", tags=["Records"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"]) # Add this!