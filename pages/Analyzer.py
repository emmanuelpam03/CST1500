import streamlit as st
from app.data.incidents import get_all_incidents

st.title("All Incident Analyzer")

with st.spinner("Loading incidents..."):
	incidents = get_all_incidents()

if incidents.empty:
	st.error("No incidents found.")
else:
	st.selectbox(
		label="Select incident to analyze:",
		options=[f"{row['id']}: {row['incident_type']} - {row['severity']}" for _, row in incidents.iterrows()],
		placeholder="Select an option",
		key="dashboard_option"
	)

	st.subheader("🗒️ Incident Details")
	st.write("**Type:** Malware")
	st.write("**Severity:** High")
	st.write("**Description:** A malware attack was detected on the corporate network, affecting multiple systems and leading to data breaches.")
	st.write("**Status:** Under Investigation")