import streamlit as st

# Redirect to login if not authenticated
if not st.session_state.get("logged_in"):
    st.switch_page("pages/Login.py")

st.title("Dashboard")
st.write(f"Welcome, {st.session_state.get('username', 'User')}!")


if st.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.switch_page("pages/Login.py")
