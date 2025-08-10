from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models.expense import Expense
from app.models.category import Category
from app.schemas.expense import ExpenseCreate, ExpenseRead
from app.core.db import get_db
from app.services.budget_check import check_budget  

router = APIRouter(prefix="/expense", tags=["expense"])

@router.post("/", response_model=ExpenseRead)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """ Check if category exists """
    category = db.exec(
        select(Category).where(Category.id == expense.category_id)
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    ''' Check if adding this expense would exceed budget'''
    check_budget(db, expense.category_id, expense.amount)

    '''If budget is fine, create expense'''
    new_expense = Expense(**expense.dict())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@router.get("/", response_model=List[ExpenseRead])
def read_all_expenses(db: Session = Depends(get_db)):
    expenses = db.exec(select(Expense)).all()
    return expenses
