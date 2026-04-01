from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from app.database import get_session
from app.crud.record import create_financial_record, get_financial_records, delete_financial_record
from app.schemas.record import RecordCreate, RecordRead
from app.api.permissions import RoleChecker, get_current_user
from app.models.user import UserRole, User
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=RecordRead)
def create_record(
    record_in: RecordCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN]))
):
    # Notice we no longer ask for user_id in the body/query. 
    # We take it directly from the authenticated 'current_user'.
    return create_financial_record(session, record_in, current_user.id)

# ADMIN and ANALYST can view records
@router.get("/", response_model=List[RecordRead])
def read_records(
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.ANALYST]))
):
    return get_financial_records(session)

# Only ADMIN can delete
@router.delete("/{record_id}")
def remove_record(
    record_id: UUID, 
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN]))
):
    record = delete_financial_record(session, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}