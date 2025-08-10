from datetime import date
from sqlmodel import SQLModel

class BudgetBase(SQLModel):
    """Base Budget model with common fields."""
    amount: float
    category_id: int


class BudgetCreate(BudgetBase):
    """Model for creating a new budget."""
    pass

class BudgetRead(BudgetBase):
    """Budget model with ID for reading."""
    id: int
