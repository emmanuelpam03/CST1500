import streamlit as st
from app.services.user_service import register_user

# Redirect if already logged in
if st.session_state.get("logged_in"):
    st.switch_page("pages/Dashboard.py")

st.title("Sign Up")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

st.page_link("pages/Login.py", label="Already have an account? Login")

if st.button("Register"):
    success, message = register_user(username, password)
    if success:
        from app.data.users import get_user_by_username
        user = get_user_by_username(username)
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["user_role"] = user['role'] if user else 'user'
        st.switch_page("pages/Dashboard.py")
    else:
        st.error(message)
