from sqlalchemy import text
from sqlmodel import Session, select, desc
from app.models.record import FinancialRecord

def get_recent_activity(session: Session, limit: int = 5):
    statement = select(FinancialRecord).order_code(desc(FinancialRecord.date)).limit(limit)
    return session.exec(statement).all()

def get_monthly_trends(session: Session):
    query = text("""
        SELECT 
            TO_CHAR(date, 'YYYY-MM') as month,
            type,
            SUM(amount) as total
        FROM financialrecord
        GROUP BY month, type
        ORDER BY month ASC
        LIMIT 12
    """)
    result = session.execute(query).all()
    
    trends = {}
    for month, r_type, total in result:
        if month not in trends:
            trends[month] = {"income": 0, "expense": 0}
        trends[month][r_type] = total
    return trends