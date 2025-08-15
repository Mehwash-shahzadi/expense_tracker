import streamlit as st
import requests

# ---------- Safe secret access ----------
BASE_URL = st.secrets.get("general", {}).get("BACKEND_URL", None)

if BASE_URL is None:
    st.error("BACKEND_URL is missing in st.secrets! Please add it in secrets.toml or Streamlit Cloud settings.")
    st.stop()  # stop the app if backend URL is missing

st.write(f"Using backend URL: {BASE_URL}")
st.write("Current secrets:", st.secrets)

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
