from sqlmodel import Session, select, func
from app.models.record import FinancialRecord
from app.schemas.dashboard import DashboardSummary, CategoryTotal

def get_dashboard_data(session: Session) -> DashboardSummary:
    # 1. Calculate Total Income
    income_stmt = select(func.sum(FinancialRecord.amount)).where(FinancialRecord.type == "income")
    total_income = session.exec(income_stmt).first() or 0.0

    # 2. Calculate Total Expenses
    expense_stmt = select(func.sum(FinancialRecord.amount)).where(FinancialRecord.type == "expense")
    total_expenses = session.exec(expense_stmt).first() or 0.0

    # 3. Calculate Category-wise totals
    category_stmt = (
        select(FinancialRecord.category, func.sum(FinancialRecord.amount))
        .group_by(FinancialRecord.category)
    )
    category_results = session.exec(category_stmt).all()
    
    category_totals = [
        CategoryTotal(category=row[0], total=row[1]) for row in category_results
    ]

    return DashboardSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=total_income - total_expenses,
        category_totals=category_totals
    )