from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.crud.dashboard import get_dashboard_data
from app.schemas.dashboard import DashboardSummary
from app.api.permissions import RoleChecker, get_current_user
from app.models.user import UserRole, User

router = APIRouter()

@router.get("/", response_model=DashboardSummary)
def read_dashboard_summary(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return get_dashboard_data(session)