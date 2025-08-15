# frontend/api_client.py

import requests

BASE_URL = "http://localhost:8000"  

def check_backend_status():
    """Ping the backend to see if it's online."""
    try:
        r = requests.get(f"{BASE_URL}/health")
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False


# ---------- Categories ----------
def get_category():
    try:
        r = requests.get(f"{BASE_URL}/category")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def create_category(data):
    try:
        r = requests.post(f"{BASE_URL}/category", json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def update_category(category_id, data):
    try:
        r = requests.put(f"{BASE_URL}/category/{category_id}", json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def delete_category(category_id):
    try:
        r = requests.delete(f"{BASE_URL}/category/{category_id}")
        r.raise_for_status()
        return {"success": True}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# ---------- Budgets ----------
def get_budget():
    try:
        r = requests.get(f"{BASE_URL}/budget")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def create_budget(data):
    try:
        r = requests.post(f"{BASE_URL}/budget", json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def update_budget(budget_id, data):
    try:
        r = requests.put(f"{BASE_URL}/budget/{budget_id}", json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def delete_budget(budget_id):
    try:
        r = requests.delete(f"{BASE_URL}/budget/{budget_id}")
        r.raise_for_status()
        return {"success": True}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# ---------- Expenses ----------
def get_expense():
    try:
        r = requests.get(f"{BASE_URL}/expenses")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def create_expense(data):
    try:
        r = requests.post(f"{BASE_URL}/expense", json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def update_expense(expense_id, data):
    try:
        r = requests.put(f"{BASE_URL}/expense/{expense_id}", json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def delete_expense(expense_id):
    try:
        r = requests.delete(f"{BASE_URL}/expense/{expense_id}")
        r.raise_for_status()
        return {"success": True}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
