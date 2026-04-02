from pydantic import BaseModel, computed_field
from typing import List
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

    @computed_field
    @property
    def status(self) -> str:
        if self.net_balance > 0:
            return "surplus"
        elif self.net_balance < 0:
            return "deficit"
        return "balanced"

    class Config:
        from_attributes = True
