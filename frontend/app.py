import streamlit as st
import api_client
from my_pages import category, budget, expense

#  ------Main title------
st.title("Expense Manager")

#  -------Backend health check------
if not api_client.check_backend_status():
    st.error("Backend offline — please try again later.")
    st.stop()

# ------- Sidebar navigation-----
with st.sidebar:
    st.header("Navigation")
    selected_page = st.radio("Go to:", ["Category", "Budget", "Expense"])

#  ----Routing-----
if selected_page == "Category":
    category.render()
elif selected_page == "Budget":
    budget.render()
elif selected_page == "Expense":
    expense.render()



