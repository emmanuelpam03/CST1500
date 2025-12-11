import streamlit as st
import pandas as pd
from app.data.tickets import get_all_tickets, insert_ticket as create_ticket

# Redirect to login if not authenticated
if not st.session_state.get("logged_in"):
    st.switch_page("pages/Login.py")

st.title("Tickets Dashboard")

with st.spinner("Loading tickets..."):
	raw = get_all_tickets()

if isinstance(raw, pd.DataFrame):
	df = raw.copy()
else:
	df = pd.DataFrame(raw)

if "created_at" in df.columns:
	df = df.drop(columns=["created_at"])

df = df.fillna("None")

if df.empty:
	st.error("No tickets found.")
	st.stop()

st.subheader("Tickets")
st.dataframe(df)


st.subheader("Tickets by Priority")

high_count = (df["priority"] == "High").sum()
total_count = len(df)

left, right = st.columns(2)
left.metric("High Priority", high_count)
right.metric("Total Tickets", total_count)

counts = df["priority"].value_counts().reset_index()
counts.columns = ["priority", "count"]

st.bar_chart(counts.set_index("priority")["count"])

st.subheader("Create New Ticket")

with st.form("add_ticket_form", clear_on_submit=True):
	import uuid
	from datetime import datetime
	
	ticket_id = st.text_input("Ticket ID", value=f"TICKET-{uuid.uuid4().hex[:8].upper()}")
	priority = st.selectbox("Priority", ["Low", "Medium", "High"])
	status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
	category = st.text_input("Category")
	subject = st.text_input("Subject")
	description = st.text_area("Description")
	created_date = st.date_input("Created Date", value=datetime.now().date())
	assigned_to = st.text_input("Assigned To (optional)", value="")

	submitted = st.form_submit_button("Create Ticket")

	if submitted:
		if not ticket_id or not description:
			st.error("Ticket ID and Description are required!")
		else:
			try:
				create_ticket(
					ticket_id=ticket_id,
					priority=priority,
					status=status,
					category=category if category else None,
					subject=subject if subject else None,
					description=description,
					created_date=str(created_date),
					assigned_to=assigned_to if assigned_to else None
				)
				st.success("Ticket created successfully!")
				st.rerun()
			except Exception as e:
				st.error(f"Error creating ticket: {str(e)}")