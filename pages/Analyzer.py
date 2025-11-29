import streamlit as st
from app.data.incidents import get_all_incidents

st.title("All Incident Analyzer")

incidents = get_all_incidents()
st.write(f"Total Incidents: {len(incidents)}")