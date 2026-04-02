from sqlalchemy import text
from sqlmodel import Session, select, desc, func
from app.models.record import FinancialRecord
from app.schemas.dashboard import DashboardSummary, CategoryTotal, MonthlyTrend

def get_dashboard_data(session: Session, user_id: str) -> DashboardSummary:
    income = session.exec(
        select(func.sum(FinancialRecord.amount))
        .where(FinancialRecord.user_id == user_id, FinancialRecord.type == "income")
    ).first() or 0.0
    
    expense = session.exec(
        select(func.sum(FinancialRecord.amount))
        .where(FinancialRecord.user_id == user_id, FinancialRecord.type == "expense")
    ).first() or 0.0

    cat_query = session.exec(
        select(FinancialRecord.category, func.sum(FinancialRecord.amount))
        .where(FinancialRecord.user_id == user_id)
        .group_by(FinancialRecord.category)
    ).all()
    category_totals = [CategoryTotal(category=c, total=t) for c, t in cat_query]

    recent_activity = session.exec(
        select(FinancialRecord)
        .where(FinancialRecord.user_id == user_id)
        .order_by(desc(FinancialRecord.date))
        .limit(5)
    ).all()

    trend_query = text("""
        SELECT TO_CHAR(date, 'YYYY-MM') as month, 
               type, 
               SUM(amount) as total 
        FROM financialrecord 
        WHERE user_id = :user_id
        GROUP BY month, type 
        ORDER BY month ASC
    """)
    trend_results = session.execute(trend_query, {"user_id": user_id}).all()
    
    temp_trends = {}
    for month, r_type, total in trend_results:
        if month not in temp_trends:
            temp_trends[month] = {"month": month, "income": 0, "expense": 0}
        
        if r_type in ['income', 'expense']:
            temp_trends[month][r_type] = total
    
    monthly_trends = [MonthlyTrend(**v) for v in temp_trends.values()]

    return DashboardSummary(
        total_income=income,
        total_expenses=expense,
        net_balance=income - expense,
        category_totals=category_totals,
        recent_activity=recent_activity,
        monthly_trends=monthly_trends
    )