import streamlit as st
from ui.sidebar import render_sidebar
from ui.job_board import render_job_board
from pipeline.runner import process_pipeline
from ui.jd_summary import render_jd_summary
from ui.resume_summary import render_resume_summaries
from ui.visualization import render_visualization_summary

# 🖌️ Apply page style and layout
st.set_page_config(page_title="📄 ATS Resume Scoring System", layout="wide")
with open("ui/styles.css") as f:
    css = f"<style>{f.read()}</style>"
    st.markdown(css, unsafe_allow_html=True)


# 🏷️ Title and description
st.title("📄 ATS Resume Scoring & Improvement Suggestion App")
st.markdown(
    """
Upload multiple resumes and a job description, or select a job description directly from the real-time job dashboard.
Our intelligent AI agents will analyze and score each resume, provide personalized improvement suggestions, and generate rich visual insights to help you understand how well each resume aligns with the job description.
"""
)

# 🔍 Job board UI
render_job_board()


# 📁 Uploads & Run button
resume_files, jd_file, run_triggered = render_sidebar()

# 🚀 Run pipeline
if run_triggered:
    if not resume_files or not jd_file:
        st.warning(
            "⚠️ Please upload both resumes and a job description before"
            " running."
        )
    else:
        with st.spinner("⏳ Running pipeline. This may take a moment..."):
            result = process_pipeline(resume_files, jd_file)
            st.session_state["pipeline_result"] = result
            st.session_state["pipeline_completed"] = True
        st.success("🎉 Pipeline completed successfully!")

# 📊 Results
result = st.session_state.get("pipeline_result")
if result:
    render_jd_summary(result)
    render_resume_summaries(result)
    render_visualization_summary(result)
    st.balloons()

# import streamlit as st
# import uuid
# import os
# import json
# import asyncio
# import base64
# from io import BytesIO
# from datetime import datetime
# from main import run_pipeline
# import plotly.graph_objects as go
# from streamlit.components.v1 import html
# from services.job_fetcher import fetch_jobs

# st.set_page_config(page_title="📄 ATS Resume Scoring System", layout="wide")
# st.title("📄 ATS Resume Scoring & Improvement Suggestion App")

# # Custom Styles
# st.markdown(
#     """
# <style>
# .job-title { font-size: 22px; font-weight: 700; margin-top: 10px; }
# .highlight-box {
#     background-color: #f0f2f6;
#     padding: 12px;
#     border-radius: 10px;
#     color: #111;
#     font-weight: 600;
#     box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
# }
# .recommend-box {
#     background-color: #fffde7;
#     padding: 12px;
#     border-radius: 10px;
#     margin-bottom: 12px;
#     color: #333;
#     box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
# }
# .feedback-box {
#     background-color: #e3f2fd;
#     color: #000;
#     padding: 12px;
#     border-left: 6px solid #2196f3;
#     border-radius: 8px;
#     margin-bottom: 10px;
#     font-size: 15px;
#     font-weight: 500;
# }
# .stDownloadButton > button {
#         background-color: #1976d2;
#         color: white;
#         border-radius: 8px;
#         padding: 6px 12px;
#         font-weight: 600;
#         box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
#     }
#     .stDownloadButton > button:hover {
#         background-color: #125ea7;
#     }
# .job-title-value {
#     color: #ce93d8;
#     font-weight: 700;
# }
# .skill-box-container {
#         display: flex;
#         flex-wrap: wrap;
#         gap: 6px;
#         margin-top: 6px;
#     }
# .skill-box {
#     background-color: #f0f2f6;
#     border-radius: 6px;
#     padding: 6px 10px;
#     font-size: 0.85rem;
#     color: #8D6F64;
#     font-weight: bold;
#     border: 1px solid #ccc;
#     box-shadow: 1px 1px 2px rgba(0,0,0,0.05);
# }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# st.markdown(
#     """
# Upload multiple resumes and a job description.
# Our AI agents will process, **score**, **recommend improvements**, and generate **visual insights** comparing each resume to the job description.
# """
# )

# st.markdown("---")
# if "pipeline_completed" not in st.session_state:
#     st.session_state.run_clicked = False
# with st.expander(
#     "🔍 Real-Time Job Board",
#     expanded=not st.session_state.get("pipeline_completed", False),
# ):
#     query = st.text_input("Enter job role", "Data Scientist")
#     location = st.text_input("Enter location", "Bangalore")

#     if st.button("Fetch Jobs"):
#         with st.spinner("Fetching job listings..."):
#             jobs = fetch_jobs(query, location)
#             st.session_state.jobs = jobs

#     if "jobs" in st.session_state:
#         for idx, job in enumerate(st.session_state.jobs):
#             st.subheader(f"{idx + 1}. {job['job_title']}")
#             st.markdown(f"**Company:** {job['employer_name']}")
#             st.markdown(
#                 f"**Location:** {job['job_city']}, {job['job_country']}"
#             )
#             st.markdown(
#                 f"**Job Description:**\n\n{job['job_description'][:500]}..."
#             )

#             if st.button(f"Use this JD", key=f"use_jd_{job['job_id']}"):
#                 # Save selected JD to session
#                 st.session_state.selected_jd = job["job_description"]
#                 st.session_state.jobs = []  # Clear jobs from UI

#                 # Save JD to a text file
#                 os.makedirs("input/test_jd", exist_ok=True)
#                 jd_path = os.path.join(
#                     "input/test_jd", f"selected_job_{job['job_id']}.txt"
#                 )
#                 with open(jd_path, "w", encoding="utf-8") as f:
#                     f.write(job["job_description"])
#                 st.session_state.selected_jd_path = jd_path
#                 st.success(
#                     "✅ Job description attached. Ready to run ATS pipeline."
#                 )


# # Sidebar
# st.sidebar.markdown("### 📁 Upload Section")
# # jd_file = st.sidebar.file_uploader(
# #     "Upload Job Description",
# #     type=["pdf", "docx", "txt"],
# # )
# if "selected_jd_path" in st.session_state:
#     st.sidebar.success("📄 JD selected from job board.")
#     jd_file = st.session_state.selected_jd_path  # used later by pipeline
# else:
#     jd_file = st.sidebar.file_uploader(
#         "Upload Job Description", type=["pdf", "docx", "txt"]
#     )

# resume_folder = st.sidebar.file_uploader(
#     "Upload Resume(s)", type=["pdf", "docx", "txt"], accept_multiple_files=True
# )
# run_button = st.sidebar.button("🚀 Run ATS Pipeline")

# # File Saving
# os.makedirs(f"input/test_resume", exist_ok=True)
# os.makedirs(f"input/test_jd", exist_ok=True)


# async def save_uploaded_files(resume_files, jd_file):
#     for resume in resume_files:
#         with open(os.path.join("input/test_resume", resume.name), "wb") as f:
#             f.write(resume.read())
#     if jd_file:
#         if isinstance(jd_file, str):
#             # It's already a saved file path from the job board
#             dest_path = os.path.join(
#                 "input/test_jd", os.path.basename(jd_file)
#             )
#             if jd_file != dest_path:
#                 with open(jd_file, "rb") as src, open(dest_path, "wb") as dst:
#                     dst.write(src.read())
#         else:
#             with open(os.path.join("input/test_jd", jd_file.name), "wb") as f:
#                 f.write(jd_file.read())


# def render_chart(
#     data_dict: dict, title_prefix: str, selected_chart: str, zmax=100
# ):
#     labels = list(data_dict.keys())
#     values = list(data_dict.values())

#     if selected_chart == "Pie Chart":
#         pie_fig = go.Figure(
#             data=[
#                 go.Pie(
#                     labels=labels,
#                     values=values,
#                 )
#             ]
#         )
#         pie_fig.update_layout(title=f"{title_prefix} Score Distribution (Pie)")
#         st.plotly_chart(pie_fig, use_container_width=True)

#     elif selected_chart == "Bar Chart":
#         bar_fig = go.Figure(
#             data=[
#                 go.Bar(
#                     x=labels,
#                     y=values,
#                 )
#             ]
#         )
#         bar_fig.update_layout(title=f"{title_prefix} Score Distribution (Bar)")
#         st.plotly_chart(bar_fig, use_container_width=True)

#     elif selected_chart == "Radar Chart":
#         radar_fig = go.Figure(
#             data=go.Scatterpolar(
#                 r=values + [values[0]],
#                 theta=labels + [labels[0]],
#                 fill="toself",
#             )
#         )
#         radar_fig.update_layout(
#             title=f"{title_prefix} Score Distribution (Radar)",
#             polar=dict(radialaxis=dict(visible=True)),
#         )
#         st.plotly_chart(radar_fig, use_container_width=True)

#     elif selected_chart == "Donut Chart":
#         donut_fig = go.Figure(
#             data=[
#                 go.Pie(
#                     labels=labels,
#                     values=values,
#                     hole=0.4,
#                     textinfo="label+percent",
#                     insidetextorientation="radial",
#                 )
#             ]
#         )
#         donut_fig.update_layout(
#             title=f"{title_prefix} Score Distribution (Donut)"
#         )
#         st.plotly_chart(donut_fig, use_container_width=True)

#     elif selected_chart == "Heatmap":
#         sorted_data = sorted(
#             data_dict.items(),
#             key=lambda x: x[1],
#             reverse=True,
#         )
#         keys_sorted, values_sorted = zip(*sorted_data)
#         heatmap_fig = go.Figure(
#             data=go.Heatmap(
#                 z=[values_sorted],
#                 x=keys_sorted,
#                 y=["General Scores"],
#                 colorscale="YlGnBu",
#                 zmin=0,
#                 zmax=zmax,
#                 showscale=True,
#                 colorbar=dict(title="Score / 100"),
#                 hovertemplate="%{x}: %{z}<extra></extra>",
#             )
#         )
#         heatmap_fig.update_layout(
#             title=f"{title_prefix} Score Distribution (Heatmap)",
#             xaxis=dict(tickangle=-45),
#             margin=dict(l=40, r=20, t=40, b=80),
#             height=300,
#         )
#         st.plotly_chart(heatmap_fig, use_container_width=True)


# if run_button:
#     if not resume_folder or not jd_file:
#         st.warning(
#             "⚠️ Please upload both resumes and a job description before"
#             " running."
#         )
#     else:
#         with st.spinner("⏳ Running pipeline. This may take a moment..."):
#             asyncio.run(save_uploaded_files(resume_folder, jd_file))
#             result = asyncio.run(
#                 run_pipeline("input/test_resume", "input/test_jd")
#             )
#             st.session_state["pipeline_result"] = result  # 💾 save to session
#             st.session_state.pipeline_completed = True
#         st.success("🎉 Pipeline completed successfully!")

# result = st.session_state.get("pipeline_result")
# if result:
#     # Display JD Summary
#     with st.expander("📌 Job Description Summary", expanded=True):
#         jd_data = result.get("job_description", {})

#         col_title, col_button = st.columns([4, 1])  # Responsive layout
#         with col_title:
#             st.markdown(
#                 f"""
#                 <div class='job-title'>
#                     🧑‍💼 <span class='job-title'>Job Title:</span>
#                     <span class='job-title-value'>{jd_data.get('job_title', 'N/A')}</span>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )
#         with col_button:
#             st.markdown("<br>", unsafe_allow_html=True)  # Spacer for alignment
#             st.download_button(
#                 label="📥 Download JD Summary",
#                 data=f"{jd_data}",
#                 file_name=f"job_description_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
#                 mime="text/plain",
#                 use_container_width=True,
#             )

#         tab1, tab2, tab3, tab4 = st.tabs(
#             [
#                 "📝 Overview",
#                 "✅ Skills",
#                 "🎓 Education & Certs",
#                 "📐 Matching Criteria",
#             ]
#         )

#         with tab1:
#             st.markdown("#### 📌 Experience Required")
#             st.markdown(f"`{jd_data.get('experience_required', 'N/A')}`")
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown("#### 🎯 Responsibilities")
#                 st.markdown(
#                     "\n".join(
#                         f"- {r}" for r in jd_data.get("responsibilities") or []
#                     )
#                     or "_Not specified_"
#                 )

#             with col2:
#                 st.markdown("#### 🏷️ Domain Keywords")
#                 st.markdown(
#                     "\n".join(
#                         f"- {kw}"
#                         for kw in jd_data.get("domain_keywords") or []
#                     )
#                     or "_Not specified_"
#                 )

#         with tab2:
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown("#### ✅ Required Skills")
#                 st.markdown(
#                     "\n".join(
#                         f"- {skill}"
#                         for skill in jd_data.get("required_skills") or []
#                     )
#                     or "_Not specified_"
#                 )
#             with col2:
#                 st.markdown("#### 🌟 Preferred Skills")
#                 st.markdown(
#                     "\n".join(
#                         f"- {skill}"
#                         for skill in jd_data.get("preferred_skills") or []
#                     )
#                     or "_Not specified_"
#                 )

#         with tab3:
#             st.markdown("#### 🎓 Education Requirements")
#             st.markdown(f"`{jd_data.get('education_requirements', 'N/A')}`")
#             st.markdown("#### 📜 Certifications")
#             st.markdown(
#                 "\n".join(
#                     f"- {c}" for c in jd_data.get("certifications") or []
#                 )
#                 or "_Not specified_"
#             )

#         with tab4:
#             st.markdown("#### 🧮 Matching Criteria")
#             if jd_data.get("matching_criteria"):
#                 for crit in jd_data["matching_criteria"]:
#                     st.markdown(
#                         f"- `{crit.get('skill', '')}` (Weight:"
#                         f" {crit.get('weight', 1)})"
#                     )
#             else:
#                 st.info("No matching criteria provided.")

#     # Display Resume Results
#     st.markdown("---")
#     with st.expander("📝 Resume(s) Summary", expanded=True):
#         for score_item, job_item in zip(
#             result.get("scores_and_recommendations", []),
#             result.get("suggested_jobs", []),
#         ):
#             candidate_name = score_item.get("candidate_name", "Unknown")
#             with st.expander(f"📎 Resume: {candidate_name}", expanded=True):
#                 score = score_item.get("score", {})
#                 recs = score_item.get("recommendations", {})

#                 with st.expander("📈 Score Summary", expanded=True):
#                     score_breakdown = score.get("score_breakdown", {})
#                     if not score_breakdown:
#                         st.info("No score breakdown available.")
#                     else:
#                         # Separate out 'skills' if it's a nested dict
#                         skill_scores = score_breakdown.get("skills", {})
#                         general_scores = {
#                             k: v
#                             for k, v in score_breakdown.items()
#                             if k != "skills"
#                         }
#                         total_skill_score = (
#                             sum(skill_scores.values())
#                             if isinstance(skill_scores, dict)
#                             else skill_scores
#                         )
#                         general_scores["skill"] = total_skill_score

#                         chart_options = [
#                             "Pie Chart",
#                             "Bar Chart",
#                             "Radar Chart",
#                             "Donut Chart",
#                             "Heatmap",
#                         ]
#                         selected_chart = st.radio(
#                             f"Select chart for: {candidate_name}",
#                             options=chart_options,
#                             horizontal=True,
#                             key=f"chart_select_{candidate_name}",
#                         )

#                         col1, col2 = st.columns(2)

#                         with col1:
#                             st.markdown("**⭐ General Score Chart**")
#                             if general_scores:
#                                 render_chart(
#                                     general_scores,
#                                     "General",
#                                     selected_chart,
#                                     100,
#                                 )

#                             with col2:
#                                 # Skills Matching Breakdown
#                                 st.markdown("**🧠 Skill Score Chart**")
#                                 if (
#                                     isinstance(skill_scores, dict)
#                                     and skill_scores
#                                 ):
#                                     render_chart(
#                                         skill_scores,
#                                         "Skill",
#                                         selected_chart,
#                                         10,
#                                     )

#                         # Total score metric
#                         st.metric(
#                             "✅ Total ATS Score",
#                             f"{score.get('total_score', 0):.1f}/100",
#                         )

#                 # Feedback
#                 if score.get("feedback"):
#                     with st.expander("💬 Feedback", expanded=True):
#                         for fb in score["feedback"]:
#                             st.markdown(
#                                 f"<div class='feedback-box'>📝 {fb}</div>",
#                                 unsafe_allow_html=True,
#                             )

#                 # Recommendations Carousel
#                 with st.expander("🛠️ Recommendations", expanded=True):
#                     recommendations = recs.get("recommendations", [])
#                     if recommendations:
#                         cards_html = ""
#                         for idx, r in enumerate(recommendations):
#                             cards_html += f"""
#                                 <div class="carousel-card">
#                                     <h4>📍 {r['section']}</h4>
#                                     <p><strong>💡 Suggestion:</strong> {r['suggestion']}</p>
#                                     <p><strong>🔍 Reason:</strong> {r['reason']}</p>
#                                 </div>
#                             """

#                         carousel_html = f"""
#                         <style>
#                         .carousel-container {{
#                             position: relative;
#                             overflow: hidden;
#                             width: 100%;
#                         }}
#                         .carousel-track {{
#                             display: flex;
#                             overflow-x: auto;
#                             scroll-behavior: smooth;
#                             gap: 16px;
#                             padding: 10px;
#                         }}
#                         .carousel-card {{
#                             flex: 0 0 300px;
#                             background: #fffde7;
#                             padding: 15px;
#                             border-radius: 10px;
#                             box-shadow: 0 2px 6px rgba(0,0,0,0.1);
#                             min-height: 180px;
#                         }}
#                         .carousel-btn {{
#                             position: absolute;
#                             top: 45%;
#                             background-color: rgba(0,0,0,0.5);
#                             color: white;
#                             border: none;
#                             padding: 6px 10px;
#                             cursor: pointer;
#                             z-index: 2;
#                             border-radius: 50%;
#                         }}
#                         .carousel-btn.left {{ left: 0; transform: translateY(-50%); }}
#                         .carousel-btn.right {{ right: 0; transform: translateY(-50%); }}
#                         </style>

#                         <div class="carousel-container">
#                             <button class="carousel-btn left" id="btn-left" onclick="scrollCarousel(-1)">◀</button>
#                             <div id="carousel-track" class="carousel-track">
#                                 {cards_html}
#                             </div>
#                             <button class="carousel-btn right" id="btn-right" onclick="scrollCarousel(1)">▶</button>
#                         </div>

#                         <script>
#                         const track = document.getElementById("carousel-track");
#                         const cardWidth = 316; // 300 + 16 gap

#                         function scrollCarousel(direction) {{
#                             const maxScrollLeft = track.scrollWidth - track.clientWidth;
#                             track.scrollLeft += direction * cardWidth;

#                             // Optional: Disable arrows at ends
#                             setTimeout(() => {{
#                                 document.getElementById("btn-left").disabled = track.scrollLeft <= 0;
#                                 document.getElementById("btn-right").disabled = track.scrollLeft >= maxScrollLeft - 5;
#                             }}, 300);
#                         }}

#                         // Disable left button initially
#                         setTimeout(() => {{
#                             document.getElementById("btn-left").disabled = true;
#                         }}, 100);
#                         </script>
#                         """

#                         html(carousel_html, height=260)
#                     else:
#                         st.info("No recommendations available.")

#                 def render_skill_boxes(skills: list[str]) -> str:
#                     if not skills:
#                         return "<p>NA</p>"

#                     boxes = "".join(
#                         f"<span class='skill-box'>{skill}</span>"
#                         for skill in skills
#                     )
#                     return f"<div class='skill-box-container'>{boxes}</div>"

#                 with st.expander("🎯 Suggested Open Jobs", expanded=True):
#                     for job in job_item:
#                         with st.container():
#                             st.markdown("----")  # separator between jobs

#                             st.markdown(
#                                 f"### 💼 {job.get('title', 'Untitled Job')}"
#                             )

#                             st.markdown(
#                                 "**📝 Description:**"
#                                 f" {job.get('description', 'NA')}"
#                             )

#                             st.markdown(
#                                 "**🛠 Required Skills:**"
#                                 f" {render_skill_boxes(job.get('required_skills', []))}",
#                                 unsafe_allow_html=True,
#                             )

#     # Display resume comparison visualization report
#     st.markdown("---")
#     with st.expander("📊 Detailed Visualization Summary", expanded=True):
#         visualization = result.get("visualization", {})
#         bar_chart = visualization.get("chart_base64", "")
#         insights = visualization.get("summary_insights", "")
#         scores_data = result.get("scores_and_recommendations", [])
#         # -- Download Button: Right above summary insights
#         visualization_summary = {
#             "chart_base64": bar_chart,
#             "summary_insights": insights,
#             "scores_and_recommendations": scores_data,
#         }

#         summary_json_str = json.dumps(visualization_summary, indent=2)
#         summary_bytes = summary_json_str.encode("utf-8")
#         summary_io = BytesIO(summary_bytes)

#         col_d1, col_d2 = st.columns([5, 1])  # left space, right button
#         with col_d2:
#             st.download_button(
#                 label="📥 Download Summary",
#                 data=summary_io,
#                 file_name=f"visualization_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
#                 mime="application/json",
#                 use_container_width=True,
#             )

#         with st.expander("📈 Job Fit Analysis Across Resumes", expanded=True):

#             # -- Tabs for cleaner visualization UI
#             tabs = st.tabs(
#                 [
#                     "📈 Overall ATS Score",
#                     "🧩 Score Breakdown",
#                     "🧠 Skill Breakdown",
#                 ]
#             )

#             def render_fallback_chart():
#                 # st.warning(
#                 #     "⚠️ Base64 chart not available or failed to render. Showing"
#                 #     " fallback charts below."
#                 # )

#                 # Tab 1: Total ATS Score
#                 with tabs[0]:
#                     st.subheader("✅ Total ATS Score Comparison")
#                     total_scores = {
#                         item.get("candidate_name", f"Resume {i+1}"): (
#                             item.get("score", {}).get("total_score", 0)
#                         )
#                         for i, item in enumerate(scores_data)
#                         if "score" in item
#                     }

#                     if total_scores:
#                         fig = go.Figure()
#                         for name, score in total_scores.items():
#                             fig.add_trace(
#                                 go.Bar(name=name, x=[name], y=[score])
#                             )
#                         fig.update_layout(
#                             title="Total ATS Score by Resume",
#                             xaxis_title="Resume",
#                             yaxis_title="Total Score",
#                             yaxis=dict(range=[0, 100]),
#                             barmode="group",
#                         )
#                         st.plotly_chart(fig, use_container_width=True)
#                     else:
#                         st.info("No total scores available.")

#                 # Tab 2: Score Breakdown by Category
#                 with tabs[1]:
#                     st.subheader("📊 Category-wise Score Breakdown")
#                     breakdown_data = {}
#                     all_categories = set()

#                     for i, item in enumerate(scores_data):
#                         name = item.get("candidate_name", f"Resume {i+1}")
#                         breakdown = item.get("score", {}).get(
#                             "score_breakdown", {}
#                         )

#                         score_dict = {}
#                         for key, value in breakdown.items():
#                             if key == "skills" and isinstance(value, dict):
#                                 score_dict["skills"] = sum(value.values())
#                             elif isinstance(value, (int, float)):
#                                 score_dict[key] = value

#                         breakdown_data[name] = score_dict
#                         all_categories.update(score_dict.keys())

#                     all_categories = sorted(list(all_categories))
#                     fig = go.Figure()
#                     for resume, cat_scores in breakdown_data.items():
#                         y = [cat_scores.get(cat, 0) for cat in all_categories]
#                         fig.add_trace(
#                             go.Bar(name=resume, x=all_categories, y=y)
#                         )

#                     fig.update_layout(
#                         barmode="group",
#                         title="Score Breakdown by Category per Resume",
#                         xaxis_title="Category",
#                         yaxis_title="Score",
#                         yaxis=dict(range=[0, 100]),
#                     )
#                     st.plotly_chart(fig, use_container_width=True)

#                 # Tab 3: Skill Breakdown
#                 with tabs[2]:
#                     st.subheader("🧠 Skill Breakdown by Resume")
#                     skill_data = {}
#                     all_skills = set()

#                     for i, item in enumerate(scores_data):
#                         name = item.get("candidate_name", f"Resume {i+1}")
#                         skills = (
#                             item.get("score", {})
#                             .get("score_breakdown", {})
#                             .get("skills", {})
#                         )
#                         if isinstance(skills, dict) and skills:
#                             skill_data[name] = skills
#                             all_skills.update(skills.keys())

#                     all_skills = sorted(list(all_skills))
#                     fig = go.Figure()
#                     for resume, skills in skill_data.items():
#                         y = [skills.get(skill, 0) for skill in all_skills]
#                         fig.add_trace(go.Bar(name=resume, x=all_skills, y=y))

#                     fig.update_layout(
#                         barmode="group",
#                         title="Skill Breakdown by Resume",
#                         xaxis_title="Skill",
#                         yaxis_title="Skill Score",
#                         yaxis=dict(range=[0, 10]),
#                     )
#                     st.plotly_chart(fig, use_container_width=True)

#             # -- Try rendering Base64 image
#             if bar_chart:
#                 try:
#                     if bar_chart.startswith("data:image/png;base64,"):
#                         b64_data = bar_chart.split(",")[1]
#                     else:
#                         b64_data = bar_chart.strip()

#                     missing_padding = len(b64_data) % 4
#                     if missing_padding:
#                         b64_data += "=" * (4 - missing_padding)

#                     image_bytes = base64.b64decode(b64_data)
#                     st.image(BytesIO(image_bytes), use_container_width=True)
#                 except Exception as e:
#                     render_fallback_chart()
#             else:
#                 render_fallback_chart()

#         # -- Summary Insights
#         with st.expander("💡 Summary Insights", expanded=True):
#             st.markdown("")
#             if insights:
#                 st.markdown(
#                     f"""
#                     <div style="
#                         background-color: #e6f4ff;
#                         color: #003366;
#                         padding: 1rem;
#                         border-radius: 10px;
#                         border-left: 6px solid #2c91f0;
#                         font-size: 16px;
#                         line-height: 1.6;
#                     ">
#                         {insights}
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )

#     st.balloons()
