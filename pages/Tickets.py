import streamlit as st
import pandas as pd
from app.data.tickets import get_all_tickets, insert_ticket as create_ticket

st.title("Tickets Dashboard")

with st.spinner("Loading incidents..."):
	raw = get_all_tickets()

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

st.subheader("Tickets")
st.dataframe(df)


st.subheader("Tickets by Priority")

high_count = (df["priority"] == "High").sum()
total_count = len(df)

left, right = st.columns(2)
left.metric("High", high_count)
right.metric("Incidents", total_count)

counts = df["priority"].value_counts().reset_index()
counts.columns = ["priority", "count"]

counts = df["priority"].value_counts().reset_index()
counts.columns = ["priority", "count"]

st.bar_chart(counts.set_index("priority")["count"])

st.subheader("Create New Ticket")

with st.form("add_incident_form"):
	date = st.date_input("Date")
	incident_type = st.text_input("Incident Type")
	priority = st.selectbox("priority", ["Low", "Medium", "High"])
	status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
	description = st.text_area("Description")

	submitted = st.form_submit_button("Add Incident")

	if submitted:
		new_incident = {
			"date": date,
			"incident_type": incident_type,
			"priority": priority,
			"status": status,
			"description": description,
			"reported_by": st.session_state.get("username"),
		}

		create_incident(**new_incident)
		st.success("Incident added.")
		st.rerun()