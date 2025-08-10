from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models.budget import Budget
from app.models.category import Category
from app.schemas.budget import BudgetCreate,BudgetRead
from app.core.db import get_db

router = APIRouter(prefix="/budget", tags=["budget"])

@router.post("/", response_model=BudgetRead)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    """ Check if category exists"""
    category = db.exec(select(Category).where(Category.id == budget.category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

 
    new_budget =Budget(**budget.dict())
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    return new_budget

@router.get("/", response_model=List[BudgetRead])
def read_all_expenses(db: Session = Depends(get_db)):
    budget = db.exec(select(Budget)).all()
    
    return budget