from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from app.database import get_session
from app.crud.record import create_financial_record, get_financial_records, delete_financial_record, FinancialRecord
from app.schemas.record import RecordCreate, RecordRead, RecordUpdate
from app.api.permissions import RoleChecker, get_current_user
from app.models.user import UserRole, User
from uuid import UUID
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=list[RecordRead])
def read_records(
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.ANALYST])),
    category: Optional[str] = None,
    record_type: Optional[str] = Query(None, alias="type"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    offset: int = 0,
    limit: int = 100
):
    statement = select(FinancialRecord)
    
    if record_type:
        statement = statement.where(FinancialRecord.type == record_type)
    if category:
        statement = statement.where(FinancialRecord.category == category)
    if start_date:
        statement = statement.where(FinancialRecord.date >= start_date)
    if end_date:
        statement = statement.where(FinancialRecord.date <= end_date)
        
    # Add Pagination (Requirement 6 Enhancement)
    statement = statement.offset(offset).limit(limit)
    
    return session.exec(statement).all()

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


@router.patch("/{record_id}", response_model=RecordRead)
def update_record(
    record_id: UUID,
    record_in: RecordUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN])) # Only Admin can update
):
    db_record = session.get(FinancialRecord, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
        
    # Update only the fields provided in the request
    update_data = record_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
        
    session.add(db_record)
    session.commit()
    session.refresh(db_record)
    return db_record