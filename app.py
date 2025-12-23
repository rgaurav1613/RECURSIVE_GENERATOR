import streamlit as st
from processor import process_incidents
import os

st.set_page_config(page_title="Incident Recurrence Tool", layout="wide")

st.title("📊 Weekly Recurrent Incident Analyzer")

current_file = st.file_uploader("Upload Current Week Excel", type=["xlsx"])
previous_file = st.file_uploader("Upload Previous Week Excel", type=["xlsx"])

if st.button("Generate Report"):
    if current_file and previous_file:
        os.makedirs("output", exist_ok=True)

        current_path = "output/current.xlsx"
        previous_path = "output/previous.xlsx"
        output_path = "output/Recurrent_Incident_Report.xlsx"

        with open(current_path, "wb") as f:
            f.write(current_file.getbuffer())

        with open(previous_path, "wb") as f:
            f.write(previous_file.getbuffer())

        process_incidents(current_path, previous_path, output_path)

        st.success("✅ Report Generated Successfully!")

        with open(output_path, "rb") as f:
            st.download_button(
                label="📥 Download Recurrent Incident Report",
                data=f,
                file_name="Recurrent_Incident_Report.xlsx"
            )
    else:
        st.warning("⚠ Please upload both Excel files")
