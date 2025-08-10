from typing import Optional
from sqlmodel import SQLModel

class CategoryBase(SQLModel):
    """Base category model with common fields."""
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
      """Model for creating a new category."""
      pass

class CategoryRead(CategoryBase):
    """Category model with ID for reading."""
    id: int
