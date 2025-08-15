from fastapi import FastAPI
from sqlmodel import SQLModel
from app.routers import category, expense, budget
from app.core.db import engine  
import os

print("DATABASE_URL =", os.getenv("DATABASE_URL"))  

app = FastAPI(title="Expense Tracker API")


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

app.include_router(category.router)
app.include_router(expense.router)
app.include_router(budget.router)

@app.get("/")
def root():
    return {"message": "Welcome to Expense Tracker API"}




