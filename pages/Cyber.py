import streamlit as st
import pandas as pd
from app.data.incidents import get_all_incidents, insert_incident as create_incident

# Redirect to login if not authenticated
if not st.session_state.get("logged_in"):
    st.switch_page("pages/Login.py")

st.title("Cyber Dashboard")

with st.spinner("Loading incidents..."):
    raw = get_all_incidents()

if isinstance(raw, pd.DataFrame):
    df = raw.copy()
else:
    df = pd.DataFrame(raw)

if "created_at" in df.columns:
    df = df.drop(columns=["created_at"])

df = df.fillna("None")

if df.empty:
    st.error("No incidents found.")
    st.stop()

st.subheader("Cyber Incidents")
st.dataframe(df)


st.subheader("Incidents by Type")

high_count = (df["severity"] == "High").sum()
total_count = len(df)

left, right = st.columns(2)
left.metric("High", high_count)
right.metric("Incidents", total_count)

counts = df["severity"].value_counts().reset_index()
counts.columns = ["severity", "count"]

st.bar_chart(counts.set_index("severity")["count"])

st.subheader("Add New Incident")

with st.form("add_incident_form", clear_on_submit=True):
    date = st.date_input("Date")
    incident_type = st.text_input("Incident Type")
    severity = st.selectbox("Severity", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
    description = st.text_area("Description")

    submitted = st.form_submit_button("Add Incident")

    if submitted:
        if not incident_type or not description:
            st.error("Incident Type and Description are required!")
        else:
            new_incident = {
                "date": str(date),
                "incident_type": incident_type,
                "severity": severity,
                "status": status,
                "description": description,
                "reported_by": st.session_state.get("username"),
            }

            try:
                create_incident(**new_incident)
                st.success("Incident added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
