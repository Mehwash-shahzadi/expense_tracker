# 💰 Expense Tracker API

A **FastAPI-based backend** for tracking expenses, managing budgets, and organizing categories — complete with an **automatic budget checker** to prevent overspending.  
Built with **Python, FastAPI, SQLModel, and PostgreSQL**, this API offers clean REST endpoints for financial tracking.

---

## 📖 Description

The Expense Tracker API helps users:

- Categorize expenses for better financial visibility
- Set budget limits per category
- Automatically prevent overspending through budget validation
- Perform CRUD operations for categories, budgets, and expenses

It’s designed for **personal finance apps** or **internal expense management systems** where simplicity, speed, and data integrity are priorities.

---

## ⚙️ Tech Stack

| Layer           | Technology    |
| --------------- | ------------- |
| Framework       | FastAPI       |
| ORM             | SQLModel      |
| Database        | PostgreSQL    |
| Config          | python-dotenv |
| Dependency Mgmt | Poetry        |
| Client GUI      | TablePlus     |
| Editor          | VS Code       |

---

## 📂 Project Structure

expense_tracker/
├── app/
│ ├── api/ # API route handlers
│ │ ├── budgets.py
│ │ ├── categories.py
│ │ └── expenses.py
│ ├── core/ # Configuration & DB connection
│ │ ├── config.py
│ │ └── db.py
│ ├── models/ # SQLModel ORM models
│ ├── schemas/ # Pydantic schemas for validation
│ ├── services/ # Business logic (budget checking)
│ └── main.py # FastAPI application entrypoint
├── tests/ # Unit tests
├── .env # Environment variables
├── .gitignore
├── pyproject.toml
└── requirements.txt

---

## ✨ Features

- **Categories**
  - Create, view, update, and delete categories
- **Budgets**
  - Create budgets linked to categories
  - View, update, and delete budgets
- **Expenses**
  - Add expenses under categories
  - Automatic budget limit validation
  - View, update, and delete expenses
- **Budget Check Service**
  - Prevents adding expenses that exceed the category budget

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Mehwash-shahzadi/expense_tracker.git
cd expense_tracker

2️⃣ Install Dependencies

Using Poetry:
poetry install

Or pip:
pip install -r requirements.txt

3️⃣ Configure Environment Variables

Create a .env file in the root:
DATABASE_URL=postgresql://postgres:route@localhost:5432/expense_db

4️⃣ Prepare Database

Ensure PostgreSQL is running and database exists:
createdb expense_db

5️⃣ Start Application

poetry run uvicorn app.main:app --reload

---


📌 API Endpoints

 📂 Categories
| Method | Endpoint           | Description             |
|--------|--------------------|-------------------------|
| POST   | `/category/`       | Create a new category   |
| GET    | `/category/`       | List all categories     |
| PUT    | `/category/{id}`   | Update a category by ID |
| DELETE | `/category/{id}`   | Delete a category by ID |

---

💵 Budgets
| Method | Endpoint         | Description           |
|--------|------------------|-----------------------|
| POST   | `/budget/`       | Create a new budget   |
| GET    | `/budget/`       | List all budgets      |
| PUT    | `/budget/{id}`   | Update a budget by ID |
| DELETE | `/budget/{id}`   | Delete a budget by ID |

---

🧾 Expenses
| Method | Endpoint          | Description                                         |
|--------|-------------------|-----------------------------------------------------|
| POST   | `/expense/`       | Create a new expense (**budget check applied**)     |
| GET    | `/expense/`       | List all expenses                                   |
| PUT    | `/expense/{id}`   | Update an expense by ID                             |
| DELETE | `/expense/{id}`   | Delete an expense by ID                             |
```
