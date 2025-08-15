from fastapi import HTTPException 
from sqlmodel import Session, select
from app.models.budget import Budget
from app.models.expense import Expense

def check_budget(db: Session, category_id: int, new_expense_amount: float, exclude_expense_id: int = None):
    """
    Check if adding/updating an expense exceeds the category budget.
    """

    # Find the budget for this category
    budget = db.exec(
        select(Budget).where(Budget.category_id == category_id)
    ).first()

    # If no budget exists, no check is needed
    if not budget:
        return

    # Calculate total expenses in this category, optionally excluding one expense
    expenses_query = select(Expense).where(Expense.category_id == category_id)
    if exclude_expense_id:
        expenses_query = expenses_query.where(Expense.id != exclude_expense_id)

    total_spent = db.exec(expenses_query).all()
    total_spent_amount = sum(exp.amount for exp in total_spent)

    # Check if adding the new expense would exceed the budget
    if total_spent_amount + new_expense_amount > budget.amount:
        remaining_budget = budget.amount - total_spent_amount
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Budget Exceeded",
                "message": (
                    f"You cannot add/update this expense of {new_expense_amount}. "
                    f"Your remaining budget for this category is {remaining_budget}."
                ),
                "budget_limit": budget.amount,
                "spent_so_far": total_spent_amount,
                "attempted_add": new_expense_amount,
                "remaining_budget": remaining_budget
            }
        )
