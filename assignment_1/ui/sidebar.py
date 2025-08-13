import streamlit as st


def render_sidebar():
    st.sidebar.markdown("### 📁 Upload Section")

    # jd_file = st.session_state.get(
    #     "selected_jd_path"
    # ) or st.sidebar.file_uploader(
    #     "Upload Job Description", type=["pdf", "docx", "txt"]
    # )

    # resume_files = st.sidebar.file_uploader(
    #     "Upload Resume(s)",
    #     type=["pdf", "docx", "txt"],
    #     accept_multiple_files=True,
    # )

    # run_triggered = st.sidebar.button("🚀 Run ATS Pipeline")
    # return resume_files, jd_file, run_triggered

    if "selected_jd_path" in st.session_state:
        st.sidebar.success("📄 JD selected from job board.")
        jd_file = st.session_state.selected_jd_path  # used later by pipeline
    else:
        jd_file = st.sidebar.file_uploader(
            "Upload Job Description", type=["pdf", "docx", "txt"]
        )

    resume_files = st.sidebar.file_uploader(
        "Upload Resume(s)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )
    run_triggered = st.sidebar.button("🚀 Run ATS Pipeline")
    return resume_files, jd_file, run_triggered
