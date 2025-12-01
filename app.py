import streamlit as st
import sqlite3
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import migrate_users_from_file
from app.data.incidents import migrate_incidents_from_file

conn = connect_database()
create_all_tables(conn)
conn.close()

# Migrate users from file
migrate_users_from_file()

# Migrate incidents from file
migrate_incidents_from_file()

pg = st.navigation(
    [
        st.Page("pages/Dashboard.py"),
        st.Page("pages/Login.py"),
        st.Page("pages/Register.py"),
        st.Page("pages/Analyzer.py"),
    ]
)

st.sidebar.page_link("pages/Dashboard.py", label="Dashboard")
st.sidebar.page_link("pages/Analyzer.py", label="AI Incident Analyzer")


pg.run()
