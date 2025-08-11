from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models.budget import Budget
from app.models.category import Category
from app.schemas.budget import BudgetCreate, BudgetRead
from app.core.db import get_db

router = APIRouter(
    prefix="/budget",
    tags=["Budget"] 
)

@router.post(
    "/",
    response_model=BudgetRead,
    summary="Create a new budget",
    description="Create a new budget after verifying that the given category exists."
)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    category = db.exec(select(Category).where(Category.id == budget.category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_budget = Budget(**budget.dict())
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget


@router.put(
    "/{budget_id}",
    response_model=BudgetRead,
    summary="Update an existing budget",
    description="Update the amount and category of a budget by its ID."
)
def update_budget(budget_id: int, budget_data: BudgetCreate, db: Session = Depends(get_db)):
    budget = db.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    budget.amount = budget_data.amount
    budget.category_id = budget_data.category_id
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.delete(
    "/{budget_id}",
    summary="Delete a budget",
    description="Delete a budget record from the database by its ID."
)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully"}


@router.get(
    "/",
    response_model=List[BudgetRead],
    summary="Get all budgets",
    description="Retrieve a list of all budgets in the system."
)
def read_all_budgets(db: Session = Depends(get_db)):
    budgets = db.exec(select(Budget)).all()
    return budgets
