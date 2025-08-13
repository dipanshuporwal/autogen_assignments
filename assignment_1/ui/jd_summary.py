import streamlit as st
from datetime import datetime


def render_jd_summary(result: dict):
    jd_data = result.get("job_description", {})
    with st.expander("📌 Job Description Summary", expanded=True):
        jd_data = result.get("job_description", {})

        col_title, col_button = st.columns([4, 1])  # Responsive layout
        with col_title:
            st.markdown(
                f"""
                <div class='job-title'>
                    🧑‍💼 <span class='job-title'>Job Title:</span>
                    <span class='job-title-value'>{jd_data.get('job_title', 'N/A')}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_button:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacer for alignment
            st.download_button(
                label="📥 Download JD Summary",
                data=f"{jd_data}",
                file_name=f"job_description_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="text/plain",
                use_container_width=True,
            )

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📝 Overview",
                "✅ Skills",
                "🎓 Education & Certs",
                "📐 Matching Criteria",
            ]
        )

        with tab1:
            st.markdown("#### 📌 Experience Required")
            st.markdown(f"`{jd_data.get('experience_required', 'N/A')}`")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🎯 Responsibilities")
                st.markdown(
                    "\n".join(
                        f"- {r}" for r in jd_data.get("responsibilities") or []
                    )
                    or "_Not specified_"
                )

            with col2:
                st.markdown("#### 🏷️ Domain Keywords")
                st.markdown(
                    "\n".join(
                        f"- {kw}"
                        for kw in jd_data.get("domain_keywords") or []
                    )
                    or "_Not specified_"
                )

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### ✅ Required Skills")
                st.markdown(
                    "\n".join(
                        f"- {skill}"
                        for skill in jd_data.get("required_skills") or []
                    )
                    or "_Not specified_"
                )
            with col2:
                st.markdown("#### 🌟 Preferred Skills")
                st.markdown(
                    "\n".join(
                        f"- {skill}"
                        for skill in jd_data.get("preferred_skills") or []
                    )
                    or "_Not specified_"
                )

        with tab3:
            st.markdown("#### 🎓 Education Requirements")
            st.markdown(f"`{jd_data.get('education_requirements', 'N/A')}`")
            st.markdown("#### 📜 Certifications")
            st.markdown(
                "\n".join(
                    f"- {c}" for c in jd_data.get("certifications") or []
                )
                or "_Not specified_"
            )

        with tab4:
            st.markdown("#### 🧮 Matching Criteria")
            if jd_data.get("matching_criteria"):
                for crit in jd_data["matching_criteria"]:
                    st.markdown(
                        f"- `{crit.get('skill', '')}` (Weight:"
                        f" {crit.get('weight', 1)})"
                    )
            else:
                st.info("No matching criteria provided.")
