from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from app.database import get_session
from app.crud.record import create_financial_record, get_financial_records, delete_financial_record
from app.schemas.record import RecordCreate, RecordRead
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=RecordRead)
def create_record(
    record_in: RecordCreate, 
    user_id: UUID, # Temporary: we'll get this from Auth later
    session: Session = Depends(get_session)
):
    return create_financial_record(session, record_in, user_id)

@router.get("/", response_model=List[RecordRead])
def read_records(
    type: Optional[str] = Query(None, pattern="^(income|expense)$"),
    category: Optional[str] = None,
    session: Session = Depends(get_session)
):
    return get_financial_records(session, type=type, category=category)

@router.delete("/{record_id}")
def remove_record(record_id: int, session: Session = Depends(get_session)):
    record = delete_financial_record(session, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}