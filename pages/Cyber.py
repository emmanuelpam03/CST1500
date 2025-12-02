import streamlit as st
import pandas as pd
from app.data.incidents import get_all_incidents, insert_incident as create_incident

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

counts = df["severity"].value_counts().reset_index()
counts.columns = ["severity", "count"]

st.bar_chart(counts.set_index("severity")["count"])

st.subheader("Add New Incident")

with st.form("add_incident_form"):
	date = st.date_input("Date")
	incident_type = st.text_input("Incident Type")
	severity = st.selectbox("Severity", ["Low", "Medium", "High"])
	status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
	description = st.text_area("Description")

	submitted = st.form_submit_button("Add Incident")

	if submitted:
		new_incident = {
			"date": date,
			"incident_type": incident_type,
			"severity": severity,
			"status": status,
			"description": description,
			"reported_by": st.session_state.get("username"),
		}

		create_incident(**new_incident)
		st.success("Incident added.")
		st.rerun()