import streamlit as st
import pandas as pd
from app.data.users import get_user_by_username, list_users
from app.data.datasets import get_all_datasets_metadata
from app.services.user_service import register_user

# Redirect to login if not authenticated
if not st.session_state.get("logged_in"):
    st.switch_page("pages/Login.py")

st.title("Dashboard")
username = st.session_state.get("username", "User")
st.write(f"Welcome, {username}!")

# Get current user's role (from session state or database)
user_role = st.session_state.get("user_role")
if not user_role:
    current_user = get_user_by_username(username)
    user_role = current_user["role"] if current_user else "user"
    st.session_state["user_role"] = user_role

# Logout button
if st.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["user_role"] = None
    st.switch_page("pages/Login.py")

st.divider()

# Datasets Metadata Section
st.subheader("Datasets Metadata")
with st.spinner("Loading datasets metadata..."):
    datasets_df = get_all_datasets_metadata()

if datasets_df.empty:
    st.info("No datasets metadata found.")
else:
    # Drop created_at if it exists for display
    display_df = datasets_df.copy()
    if "created_at" in display_df.columns:
        display_df = display_df.drop(columns=["created_at"])
    display_df = display_df.fillna("N/A")
    st.dataframe(display_df, use_container_width=True)

st.divider()

# Users Management Section (Admin only)
if user_role == "admin":
    st.subheader("User Management")

    # Display users list
    st.write("**Users List**")
    users = list_users()
    if users:
        users_data = []
        for user in users:
            users_data.append(
                {
                    "ID": user["id"],
                    "Username": user["username"],
                    "Role": user["role"],
                    "Created At": user["created_at"],
                }
            )
        users_df = pd.DataFrame(users_data)
        st.dataframe(users_df, use_container_width=True)
    else:
        st.info("No users found.")

    # Create new user form
    st.write("**Create New User**")
    with st.form("create_user_form", clear_on_submit=True):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        new_role = st.selectbox("Role", ["user", "admin"], index=0)

        submitted = st.form_submit_button("Create User")

        if submitted:
            if not new_username or not new_password:
                st.error("Username and password are required!")
            else:
                success, message = register_user(new_username, new_password, new_role)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
else:
    st.info("User management is only available for administrators.")
