from fastapi import APIRouter, Depends
from sqlmodel import Session,select
from typing import List
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryRead
from app.core.db import get_db

router = APIRouter(prefix="/category", tags=["category"])

@router.post("/", response_model=CategoryRead)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=List[CategoryRead])
def read_all_categories(db: Session = Depends(get_db)):
    categories = db.exec(select(Category)).all()
    
    return categories
