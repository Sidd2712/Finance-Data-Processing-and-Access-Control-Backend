from sqlalchemy import text
from sqlmodel import Session, select, desc, func
from app.models.record import FinancialRecord
from app.schemas.dashboard import DashboardSummary, CategoryTotal, MonthlyTrend

def get_dashboard_data(session: Session) -> DashboardSummary:
    income = session.exec(select(func.sum(FinancialRecord.amount)).where(FinancialRecord.type == "income")).first() or 0.0
    expense = session.exec(select(func.sum(FinancialRecord.amount)).where(FinancialRecord.type == "expense")).first() or 0.0

    cat_query = session.exec(select(FinancialRecord.category, func.sum(FinancialRecord.amount)).group_by(FinancialRecord.category)).all()
    category_totals = [CategoryTotal(category=c, total=t) for c, t in cat_query]


    recent_activity = session.exec(select(FinancialRecord).order_by(desc(FinancialRecord.date)).limit(5)).all()

    trend_query = text("""
        SELECT 
            TO_CHAR(date, 'YYYY-MM') as month_alias, 
            type, 
            SUM(amount) as total 
        FROM financialrecord 
        GROUP BY TO_CHAR(date, 'YYYY-MM'), type 
        ORDER BY month_alias ASC
    """)
    
    try:
        trend_results = session.execute(trend_query).all()
    except Exception as e:
        print(f"Database Query Error: {e}")
        trend_results = []

    temp_trends = {}
    for month, r_type, total in trend_results:
        if month not in temp_trends:
            temp_trends[month] = {"month": month, "income": 0.0, "expense": 0.0}
        if r_type == 'income':
            temp_trends[month]['income'] = float(total or 0)
        elif r_type == 'expense':
            temp_trends[month]['expense'] = float(total or 0)
    
    return DashboardSummary(
        total_income=income,
        total_expenses=expense,
        net_balance=income - expense,
        category_totals=category_totals,
        recent_activity=recent_activity,
        monthly_trends=[MonthlyTrend(**v) for v in temp_trends.values()]
    )