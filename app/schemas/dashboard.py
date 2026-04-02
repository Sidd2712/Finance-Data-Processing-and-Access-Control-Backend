from pydantic import BaseModel
from typing import List, Dict, Any
from app.schemas.record import RecordRead

class CategoryTotal(BaseModel):
    category: str
    total: float

class MonthlyTrend(BaseModel):
    month: str
    income: float
    expense: float

class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    category_totals: List[CategoryTotal]
    monthly_trends: List[MonthlyTrend]
    recent_activity: List[RecordRead]

