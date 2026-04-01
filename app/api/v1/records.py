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
    current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.ANALYST])),
    type: Optional[str] = Query(None, pattern="^(income|expense)$"),
    category: Optional[str] = None,
    search: Optional[str] = None,
    offset: int = 0,
    limit: int = Query(default=100, le=100) # 'le=100' means less than or equal to 100
):
    """
    Fetch records with support for filtering, searching, and pagination.
    Available to: ADMIN, ANALYST
    """
    return get_financial_records(
        session, 
        type=type, 
        category=category, 
        search=search, 
        offset=offset, 
        limit=limit
    )

# Only ADMIN can delete
@router.delete("/{record_id}")
def remove_record(
    record_id: UUID, 
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN]))
):
    record = delete_financial_record(session, record_id)
    if not record:
        raise HTTPException(
            status_code=404, 
            detail=f"Financial record with ID {record_id} was not found."
        )
    
    return {"status": "success", "message": "Record successfully removed"}