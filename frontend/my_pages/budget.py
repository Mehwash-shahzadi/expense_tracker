import streamlit as st
from frontend import api_client

def render():
    st.header("Manage Budgets")

# --- Get data from backend ---
    categories = api_client.get_category()
    budgets = api_client.get_budget()

    if not categories:
        st.warning("No categories found. Please create categories first.")
        categories = []

    if not budgets:
        budgets = []

    # --- Create budget ---
    st.subheader("Add New Budget")
    with st.form("create_budget_form"):
        category_names = []
        for cat in categories:
            category_names.append(cat["name"])
        selected_category_name = st.selectbox("Select Category", category_names)
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        create_submit = st.form_submit_button("Add Budget")

        if create_submit:
            selected_category_id = None
            for cat in categories:
                if cat["name"] == selected_category_name:
                    selected_category_id = cat["id"]
                    break

            if selected_category_id:
                result = api_client.create_budget({
                    "category_id": selected_category_id,
                    "amount": amount
                })
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("Budget added successfully.")
                    st.rerun()

# --- Update budget ---
    if budgets:
        st.subheader("Update Budget")
        with st.form("update_budget_form"):
            budget_ids = []
            for b in budgets:
                budget_ids.append(b["id"])
            selected_budget_id = st.selectbox("Select Budget ID", budget_ids)
            new_amount = st.number_input("New Amount", min_value=0.0, step=0.01, key="update_amount")
            update_submit = st.form_submit_button("Update Budget")

            if update_submit:
                category_id = None
                for b in budgets:
                    if b["id"] == selected_budget_id:
                        category_id = b["category_id"]
                        break

                if category_id:
                    result = api_client.update_budget(selected_budget_id, {
                        "category_id": category_id,
                        "amount": new_amount
                    })
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success("Budget updated successfully.")
                        st.rerun()
# --- Delete Budget ---
    if budgets:
        st.subheader("Delete Budget")
        with st.form("delete_budget_form"):
            delete_ids = []
            for b in budgets:
                delete_ids.append(b["id"])
            delete_budget_id = st.selectbox("Select Budget ID to Delete", delete_ids)
            delete_confirm = st.checkbox("I confirm I want to delete this budget.")
            delete_submit = st.form_submit_button("Delete Budget")

            if delete_submit:
                if delete_confirm:
                    result = api_client.delete_budget(delete_budget_id)
                    if isinstance(result, dict) and "error" in result:
                        st.error(f"Failed to delete budget: {result['error']}")
                    else:
                        st.success("Budget deleted successfully.")
                        st.rerun()
                else:
                    st.warning("Please confirm deletion before submitting.")

# --- Existing budget ---
    st.subheader("Existing Budgets")
    if budgets:
        table_data = []
        for b in budgets:
            category_name = "Unknown"
            for c in categories:
                if c["id"] == b["category_id"]:
                    category_name = c["name"]
                    break
            table_data.append({
                "ID": b["id"],
                "Category": category_name,
                "Amount": b["amount"]
            })
        st.table(table_data)
