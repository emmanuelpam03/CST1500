import streamlit as st
from app.data.incidents import get_all_incidents

st.title("All Incident Analyzer")

with st.spinner("Loading incidents..."):
    incidents = get_all_incidents()

if incidents.empty:
    st.error("No incidents found.")
else:
    labels = [
        f"{row['id']}: {row['incident_type']} - {row['severity']}"
        for _, row in incidents.iterrows()
    ]

    choice = st.selectbox(
        label="Select incident to analyze:",
        options=labels,
        placeholder="Select an option",
        key="dashboard_option",
    )

    selected_id = int(choice.split(":")[0])
    selected_incident = incidents.loc[incidents["id"] == selected_id].iloc[0]

    st.subheader("Incident Details")
    st.write(f"Type: {selected_incident['incident_type']}")
    st.write(f"Severity: {selected_incident['severity']}")
    st.write(f"Description: {selected_incident['description']}")
    st.write(f"Status: {selected_incident['status']}")
