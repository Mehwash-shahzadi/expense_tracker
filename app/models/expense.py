from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

class Expense(SQLModel, table=True):
    name:str
    amount: float
    id: Optional[int] = Field(default=None, primary_key=True)
    description: Optional[str] = None
    date: date
    category_id: int = Field(foreign_key="category.id")

