from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models.expense import Expense
from app.models.category import Category
from app.schemas.expense import ExpenseCreate, ExpenseRead
from app.core.db import get_db
from app.services.budget_check import check_budget

router = APIRouter(
    prefix="/expense",
    tags=["Expense"]  
)

@router.post(
    "/",
    response_model=ExpenseRead,
    summary="Create a new expense",
    description="Create a new expense after checking the category exists and ensuring the budget is not exceeded."
)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    category = db.exec(
        select(Category).where(Category.id == expense.category_id)
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check budget for new expense
    check_budget(db, expense.category_id, expense.amount)

    new_expense = Expense(**expense.dict())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.put(
    "/{expense_id}",
    response_model=ExpenseRead,
    summary="Update an existing expense",
    description="Update the amount, description, and category of an expense by its ID."
)
def update_expense(expense_id: int, expense_data: ExpenseCreate, db: Session = Depends(get_db)):
    expense = db.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    # Check budget for updated expense, excluding the current expense from total
    check_budget(db, expense_data.category_id, expense_data.amount, exclude_expense_id=expense_id)

    # Update fields
    expense.amount = expense_data.amount
    expense.description = expense_data.description
    expense.category_id = expense_data.category_id

    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete(
    "/{expense_id}",
    summary="Delete an expense",
    description="Delete an expense record from the database by its ID."
)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}


@router.get(
    "/",
    response_model=List[ExpenseRead],
    summary="Get all expenses",
    description="Retrieve a list of all recorded expenses."
)
def read_all_expenses(db: Session = Depends(get_db)):
    expenses = db.exec(select(Expense)).all()
    return expenses

