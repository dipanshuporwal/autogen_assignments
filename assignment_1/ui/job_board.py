import streamlit as st
import os
from services.job_fetcher import fetch_jobs


def render_job_board():
    with st.expander(
        "🔍 Real-Time Job Board",
        expanded=not st.session_state.get("pipeline_completed", False),
    ):
        query = st.text_input("Enter job role", "Data Scientist")
        location = st.text_input("Enter location", "Bangalore")

        if st.button("Fetch Jobs"):
            with st.spinner("Fetching job listings..."):
                jobs = fetch_jobs(query, location)
                st.session_state.jobs = jobs

        if "jobs" in st.session_state:
            for job in st.session_state.jobs:
                st.subheader(job["job_title"])
                st.markdown(f"**Company:** {job['employer_name']}")
                st.markdown(
                    f"**Location:** {job['job_city']}, {job['job_country']}"
                )
                st.markdown(
                    "**Job"
                    f" Description:**\n\n{job['job_description'][:500]}..."
                )

                if st.button("Use this JD", key=job["job_id"]):
                    _save_selected_jd(job)


def _save_selected_jd(job):
    os.makedirs("input/test_jd", exist_ok=True)
    jd_path = f"input/test_jd/selected_job_{job['job_id']}.txt"
    with open(jd_path, "w", encoding="utf-8") as f:
        f.write(job["job_description"])
    st.session_state.selected_jd_path = jd_path
    st.session_state.jobs = []
    st.success("✅ Job description attached. Ready to run ATS pipeline.")
