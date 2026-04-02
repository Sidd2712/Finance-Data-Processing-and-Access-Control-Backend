from uuid import UUID
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, col
from app.database import get_session
from app.models.record import FinancialRecord
from app.schemas.record import RecordCreate, RecordRead, RecordUpdate
from app.api.permissions import RoleChecker
from app.models.user import UserRole, User

router = APIRouter()

@router.get("/", response_model=List[RecordRead])
def read_records(
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.ANALYST])),
    category: Optional[str] = None,
    record_type: Optional[str] = Query(None, alias="type", pattern="^(income|expense)$"),
    search: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, le=100)
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
        
    if search:
        statement = statement.where(
            col(FinancialRecord.description).ilike(f"%{search}%") | 
            col(FinancialRecord.category).ilike(f"%{search}%")
        )
        
    statement = statement.order_by(FinancialRecord.date.desc()).offset(offset).limit(limit)
    
    return session.exec(statement).all()

@router.post("/", response_model=RecordRead, status_code=status.HTTP_201_CREATED)
def create_record(
    record_in: RecordCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN]))
):
    db_record = FinancialRecord.model_validate(record_in, update={"user_id": current_user.id})
    session.add(db_record)
    session.commit()
    session.refresh(db_record)
    return db_record

@router.patch("/{record_id}", response_model=RecordRead)
def update_record(
    record_id: UUID,
    record_in: RecordUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN]))
):
    db_record = session.get(FinancialRecord, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
        
    update_data = record_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
        
    session.add(db_record)
    session.commit()
    session.refresh(db_record)
    return db_record

@router.delete("/{record_id}")
def remove_record(
    record_id: UUID, 
    session: Session = Depends(get_session),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN]))
):
    db_record = session.get(FinancialRecord, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    session.delete(db_record)
    session.commit()
    return {"status": "success", "message": "Record successfully removed"}