import streamlit as st
from frontend import api_client

def render():
    st.header("Manage Categories")

# --- Fetch categories from backend ---
    categories = api_client.get_category()

    if not categories:
        st.info("No categories found.")
    else:
        st.subheader("Existing Categories")
        st.table(categories)

    st.markdown("---")

# --- Add new category ---
    st.subheader("Add Category")
    with st.form("add_category_form"):
        name = st.text_input("Name")
        description = st.text_input("Description (optional)")
        submit = st.form_submit_button("Add Category")

        if submit:
            if not name.strip():
                st.error("Name cannot be empty.")
            else:
                payload = {
                    "name": name,
                    "description": description
                }
                result = api_client.create_category(payload)
                if isinstance(result, dict) and "error" in result:
                    st.error(f"Failed to create category: {result['error']}")
                else:
                    st.success("Category created successfully.")
                    st.rerun()

    st.markdown("---")

# --- Edit category ---
    st.subheader("Edit Category")
    if categories:
        category_ids = [c["id"] for c in categories]
        with st.form("edit_category_form"):
            category_id = st.selectbox("Select Category to Edit", category_ids)
            new_name = st.text_input("New Name")
            new_description = st.text_input("New Description (optional)")
            edit_submit = st.form_submit_button("Update Category")

            if edit_submit:
                if not new_name.strip():
                    st.error("Name cannot be empty.")
                else:
                    payload = {
                        "name": new_name,
                        "description": new_description
                    }
                    result = api_client.update_category(category_id, payload)
                    if isinstance(result, dict) and "error" in result:
                        st.error(f"Failed to update category: {result['error']}")
                    else:
                        st.success("Category updated successfully.")
                        st.rerun()

    st.markdown("---")

# --- Delete category ---
    st.subheader("Delete Category")
    if categories:
        with st.form("delete_category_form"):
            delete_id = st.selectbox("Select Category to Delete", [c["id"] for c in categories])
            delete_submit = st.form_submit_button("Delete Category")

            if delete_submit:
                confirm = st.checkbox("I confirm I want to delete this category.")
                if confirm:
                    result = api_client.delete_category(delete_id)
                    if isinstance(result, dict) and "error" in result:
                        st.error(f"Failed to delete category: {result['error']}")
                    else:
                        st.success("Category deleted successfully.")
                        st.rerun()
                else:
                    st.warning("Please confirm deletion before submitting.")