import streamlit as st
from app.services.user_service import login_user

# Redirect if already logged in
if st.session_state.get("logged_in"):
    st.switch_page("pages/Dashboard.py")

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

st.page_link("pages/Register.py", label="Don't have an account? Register")
if st.button("Login"):
    success, message = login_user(username, password)
    if success:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.switch_page("pages/Dashboard.py")
    else:
        st.error(message)
