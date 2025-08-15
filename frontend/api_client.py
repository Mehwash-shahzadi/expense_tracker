import streamlit as st
import requests

# Read backend URL from environment variable
BASE_URL = st.secrets["general"]["BACKEND_URL"]
st.write(BASE_URL) 

def check_backend_status():
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
        r = requests.get(f"{BASE_URL}/expense")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        try:
            return r.json()
        except Exception:
            return {"error": str(e)}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def create_expense(data):
    try:
        r = requests.post(f"{BASE_URL}/expense", json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        try:
            """this will include budget error if backend returns it"""
            return r.json()  
        except Exception:
            return {"error": str(e)}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def update_expense(expense_id, data):
    try:
        r = requests.put(f"{BASE_URL}/expense/{expense_id}", json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        try:
            return r.json()
        except Exception:
            return {"error": str(e)}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def delete_expense(expense_id):
    try:
        r = requests.delete(f"{BASE_URL}/expense/{expense_id}")
        r.raise_for_status()
        return {"success": True}
    except requests.exceptions.HTTPError as e:
        try:
            return r.json()
        except Exception:
            return {"error": str(e)}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)} 
