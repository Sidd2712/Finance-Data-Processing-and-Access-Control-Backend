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
    category_totals: list[dict]
    monthly_trends: list[dict]
    recent_activity: list[RecordRead]

    @property
    def status(self) -> str:
        if self.net_balance > 0:
            return "surplus"
        elif self.net_balance < 0:
            return "deficit"
        return "balanced"