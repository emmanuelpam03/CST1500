import streamlit as st
import pandas as pd
from app.data.incidents import get_all_incidents

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
