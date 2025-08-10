from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float 
    category_id: int = Field(foreign_key="category.id")

    
