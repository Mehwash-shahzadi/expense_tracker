from datetime import date
from typing import Optional
from sqlmodel import SQLModel

class ExpenseBase(SQLModel):
    """Base expense model with common fields."""
    name:str
    amount:float
    description: Optional[str] = None
    date: date
    category_id: int

class ExpenseCreate(ExpenseBase):
    """Model for creating a new expense."""
    pass

class ExpenseRead(ExpenseBase):
    """Expense model with ID for reading."""
    id: int
