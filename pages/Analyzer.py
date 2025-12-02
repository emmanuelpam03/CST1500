import streamlit as st
from app.data.incidents import get_all_incidents
from google import genai
from google.genai import types

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

	if st.button("Analyze with AI", type="primary"):
		with st.spinner("Analyzing incident..."):

			client = genai.Client(api_key="AIzaSyBzj3vg1oreBaQ8lhFCxTuyU7X-Q6QPlOw")
			model = "gemini-2.0-flash"

			analysis_prompt = f"""
				Analyze the following cyber incident and provide insights and recommendations:
				Incident ID: {selected_incident['id']}
				Type: {selected_incident['incident_type']}
				Severity: {selected_incident['severity']}
				Description: {selected_incident['description']}
				Status: {selected_incident['status']}

				Provide:
				1. Root cause analysis
				2. Immediate actions needed
				3. Long-term prevention measures
				4. Risk assessment
			"""

			response = client.models.generate_content_stream(
				model=model,
				contents=analysis_prompt,
			)

			st.subheader("AI Analysis Results")

			container = st.empty()
			full_reply = ""
			
			for chunk in response:
				if chunk.text:
					full_reply += chunk.text
					container.markdown(full_reply)
