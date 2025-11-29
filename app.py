import streamlit as st
import sqlite3
from app.data.db import connect_database
from app.data.schema import create_all_tables

conn = connect_database()
create_all_tables(conn)
conn.close()

pg = st.navigation(
    [
        st.Page("pages/Dashboard.py"),
        st.Page("pages/Login.py"),
        st.Page("pages/Register.py"),
    ]
)

pg.run()
