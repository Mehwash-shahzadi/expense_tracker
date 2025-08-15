import streamlit as st
from frontend import api_client
from datetime import date

def handle_expense_response(result, success_msg="Operation successful."):
    
    """Process API response and display Streamlit messages."""

    if isinstance(result, dict):
        if "error" in result:
            st.error(f"Error: {result['error']}")
        elif "detail" in result:
            if isinstance(result["detail"], dict):
                st.error(f"Error: {result['detail'].get('message', 'Unknown error')}")
                st.info(f"Budget limit: {result['detail'].get('budget_limit')}, "
                        f"Spent so far: {result['detail'].get('spent_so_far')}, "
                        f"Attempted add: {result['detail'].get('attempted_add')}, "
                        f"Remaining: {result['detail'].get('remaining_budget')}")
            else:
                st.error(f"Error: {result['detail']}")
        else:
            st.success(success_msg)
            st.rerun()
    else:
        st.success(success_msg)
        st.rerun()

def render():
    st.header("Expenses")

    # --- Fetch data from backend ---
    categories = api_client.get_category() or []
    expenses = api_client.get_expense() or []

    if not categories:
        st.warning("No categories found. Please create categories first.")

    # ------Create Expense -----
    st.subheader("Add New Expense")
    with st.form("create_expense_form"):
        category_names = [cat["name"] for cat in categories]
        selected_category_name = st.selectbox("Select Category", category_names)

        expense_name = st.text_input("Expense Name")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        description = st.text_area("Description (optional)")
        expense_date = st.date_input("Expense Date", value=date.today())

        create_submit = st.form_submit_button("Add Expense")

    if create_submit:
        if not expense_name.strip():
            st.error("Expense name is required.")
        elif amount <= 0:
            st.error("Amount must be greater than zero.")
        else:
            selected_category_id = next((cat["id"] for cat in categories if cat["name"] == selected_category_name), None)
            if selected_category_id:
                payload = {
                    "name": expense_name.strip(),
                    "amount": amount,
                    "description": description if description else None,
                    "date": expense_date.isoformat(),
                    "category_id": selected_category_id
                }
                try:
                    result = api_client.create_expense(payload)
                    handle_expense_response(result, success_msg="Expense added successfully.")
                except Exception as e:
                    st.error(f"Request failed: {str(e)}")

    # ----- Update Expense -----
    if expenses:
        st.subheader("Update Expense")
        with st.form("update_expense_form"):
            expense_ids = [ex["id"] for ex in expenses]
            selected_expense_id = st.selectbox("Select Expense ID", expense_ids)
            selected_expense = next((ex for ex in expenses if ex["id"] == selected_expense_id), None)

            if selected_expense:
                expense_name = st.text_input("Expense Name", value=selected_expense["name"])
                amount = st.number_input("Amount", value=float(selected_expense["amount"]), min_value=0.0, step=0.01)
                description = st.text_area("Description (optional)", value=selected_expense.get("description", ""))
                expense_date = st.date_input("Expense Date", value=date.fromisoformat(selected_expense["date"]))

                category_names = [cat["name"] for cat in categories]
                category_index = next((i for i, cat in enumerate(categories) if cat["id"] == selected_expense["category_id"]), 0)
                selected_category_name = st.selectbox("Select Category", category_names, index=category_index)

            update_submit = st.form_submit_button("Update Expense")

        if update_submit and selected_expense:
            if not expense_name.strip():
                st.error("Expense name is required.")
            elif amount <= 0:
                st.error("Amount must be greater than zero.")
            else:
                selected_category_id = next((cat["id"] for cat in categories if cat["name"] == selected_category_name), None)
                if selected_category_id:
                    payload = {
                        "name": expense_name.strip(),
                        "amount": amount,
                        "description": description if description else None,
                        "date": expense_date.isoformat(),
                        "category_id": selected_category_id
                    }
                    try:
                        result = api_client.update_expense(selected_expense_id, payload)
                        handle_expense_response(result, success_msg="Expense updated successfully.")
                    except Exception as e:
                        st.error(f"Request failed: {str(e)}")

    # ----- Delete Expense----
    if expenses:
        st.subheader("Delete Expense")
        with st.form("delete_expense_form"):
            delete_ids = [ex["id"] for ex in expenses]
            selected_delete_id = st.selectbox("Select Expense ID to Delete", delete_ids)
            delete_confirm = st.checkbox("I confirm I want to delete this expense.")
            delete_submit = st.form_submit_button("Delete Expense")

        if delete_submit:
            if delete_confirm:
                try:
                    result = api_client.delete_expense(selected_delete_id)
                    handle_expense_response(result, success_msg="Expense deleted successfully.")
                except Exception as e:
                    st.error(f"Request failed: {str(e)}")
            else:
                st.warning("Please confirm deletion before submitting.")

    # -------Display Existing Expense ------
    st.subheader("Existing Expenses")
    if expenses:
        table_data = []
        for ex in expenses:
            category_name = next((cat["name"] for cat in categories if cat["id"] == ex["category_id"]), "Unknown")
            table_data.append({
                "ID": ex["id"],
                "Name": ex["name"],
                "Category": category_name,
                "Amount": ex["amount"],
                "Date": ex["date"],
                "Description": ex.get("description", "")
            })
        st.table(table_data)
