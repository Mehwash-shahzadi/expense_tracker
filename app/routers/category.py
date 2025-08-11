from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryRead
from app.core.db import get_db

router = APIRouter(
    prefix="/category",
    tags=["Category"]  
)

@router.post(
    "/",
    response_model=CategoryRead,
    summary="Create a new category",
    description="Add a new category to the database."
)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.put(
    "/{category_id}",
    response_model=CategoryRead,
    summary="Update an existing category",
    description="Update the name of a category by its ID."
)
def update_category(category_id: int, category_data: CategoryCreate, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.name = category_data.name  
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.delete(
    "/{category_id}",
    summary="Delete a category",
    description="Delete a category from the database by its ID."
)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}


@router.get(
    "/",
    response_model=List[CategoryRead],
    summary="Get all categories",
    description="Retrieve a list of all categories from the database."
)
def read_all_categories(db: Session = Depends(get_db)):
    categories = db.exec(select(Category)).all()
    return categories
