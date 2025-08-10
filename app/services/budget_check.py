from fastapi import HTTPException 
from sqlmodel import Session, select
from app.models.budget import Budget
from app.models.expense import Expense

def check_budget(db: Session, category_id: int, new_expense_amount: float):

    '''Find the budget for this category'''
    budget = db.exec(
        select(Budget).where(Budget.category_id == category_id)
    ).first()

    '''If no budget exists, no check is needed'''
    if not budget:
        return

    '''Calculate total expenses in this category'''
    total_spent = db.exec(
        select(Expense).where(Expense.category_id == category_id)
    ).all()

    total_spent_amount = 0
    for exp in total_spent:
        total_spent_amount += exp.amount

    '''Check if adding the new expense would exceed the budget'''
    if total_spent_amount + new_expense_amount > budget.amount:
        remaining_budget = budget.amount - total_spent_amount
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Budget Exceeded",
                "message": (
                    f"You cannot add this expense of {new_expense_amount}. "
                    f"Your remaining budget for this category is {remaining_budget}."
                ),
                "budget_limit": budget.amount,
                "spent_so_far": total_spent_amount,
                "attempted_add": new_expense_amount,
                "remaining_budget": remaining_budget
            }
        )
