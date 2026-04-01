from pydantic import BaseModel
from typing import List, Dict

class CategoryTotal(BaseModel):
    category: str
    total: float

class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    category_totals: List[CategoryTotal]