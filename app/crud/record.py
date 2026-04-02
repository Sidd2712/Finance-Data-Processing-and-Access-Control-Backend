from sqlmodel import Session, select, func, or_
from typing import List, Optional
from app.models.record import FinancialRecord
from app.schemas.record import RecordCreate

def create_financial_record(session: Session, record_in: RecordCreate, user_id: int):
    db_record = FinancialRecord(
        **record_in.model_dump(), 
        user_id=user_id
    )
    session.add(db_record)
    session.commit()
    session.refresh(db_record)
    return db_record

def get_financial_records(
    session: Session, 
    type: Optional[str] = None, 
    category: Optional[str] = None,
    search: Optional[str] = None,
    offset: int=0,
    limit: int=100
) -> List[FinancialRecord]:
    statement = select(FinancialRecord)
    if type:
        statement = statement.where(FinancialRecord.type == type)
    if category:
        statement = statement.where(FinancialRecord.category == category)
    if search:
        statement = statement.where(
            or_(
                FinancialRecord.description.contains(search),
                FinancialRecord.category.contains(search)
            )
        )
    statement = statement.offset(offset).limit(limit)
    
    return session.exec(statement).all()

def delete_financial_record(session: Session, record_id: int):
    record = session.get(FinancialRecord, record_id)
    if record:
        session.delete(record)
        session.commit()
    return record