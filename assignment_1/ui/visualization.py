import streamlit as st
import base64
from io import BytesIO
from datetime import datetime
import plotly.graph_objects as go
import json

def render_visualization_summary(result: dict):
    with st.expander("📊 Detailed Visualization Summary", expanded=True):
        visualization = result.get("visualization", {})
        bar_chart = visualization.get("chart_base64", "")
        insights = visualization.get("summary_insights", "")
        scores_data = result.get("scores_and_recommendations", [])
        # -- Download Button: Right above summary insights
        visualization_summary = {
            "chart_base64": bar_chart,
            "summary_insights": insights,
            "scores_and_recommendations": scores_data,
        }

        summary_json_str = json.dumps(visualization_summary, indent=2)
        summary_bytes = summary_json_str.encode("utf-8")
        summary_io = BytesIO(summary_bytes)

        col_d1, col_d2 = st.columns([5, 1])  # left space, right button
        with col_d2:
            st.download_button(
                label="📥 Download Summary",
                data=summary_io,
                file_name=f"visualization_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )

        with st.expander("📈 Job Fit Analysis Across Resumes", expanded=True):

            # -- Tabs for cleaner visualization UI
            tabs = st.tabs(
                [
                    "📈 Overall ATS Score",
                    "🧩 Score Breakdown",
                    "🧠 Skill Breakdown",
                ]
            )

            def render_fallback_chart():
                # st.warning(
                #     "⚠️ Base64 chart not available or failed to render. Showing"
                #     " fallback charts below."
                # )

                # Tab 1: Total ATS Score
                with tabs[0]:
                    st.subheader("✅ Total ATS Score Comparison")
                    total_scores = {
                        item.get("candidate_name", f"Resume {i+1}"): (
                            item.get("score", {}).get("total_score", 0)
                        )
                        for i, item in enumerate(scores_data)
                        if "score" in item
                    }

                    if total_scores:
                        fig = go.Figure()
                        for name, score in total_scores.items():
                            fig.add_trace(
                                go.Bar(name=name, x=[name], y=[score])
                            )
                        fig.update_layout(
                            title="Total ATS Score by Resume",
                            xaxis_title="Resume",
                            yaxis_title="Total Score",
                            yaxis=dict(range=[0, 100]),
                            barmode="group",
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No total scores available.")

                # Tab 2: Score Breakdown by Category
                with tabs[1]:
                    st.subheader("📊 Category-wise Score Breakdown")
                    breakdown_data = {}
                    all_categories = set()

                    for i, item in enumerate(scores_data):
                        name = item.get("candidate_name", f"Resume {i+1}")
                        breakdown = item.get("score", {}).get(
                            "score_breakdown", {}
                        )

                        score_dict = {}
                        for key, value in breakdown.items():
                            if key == "skills" and isinstance(value, dict):
                                score_dict["skills"] = sum(value.values())
                            elif isinstance(value, (int, float)):
                                score_dict[key] = value

                        breakdown_data[name] = score_dict
                        all_categories.update(score_dict.keys())

                    all_categories = sorted(list(all_categories))
                    fig = go.Figure()
                    for resume, cat_scores in breakdown_data.items():
                        y = [cat_scores.get(cat, 0) for cat in all_categories]
                        fig.add_trace(
                            go.Bar(name=resume, x=all_categories, y=y)
                        )

                    fig.update_layout(
                        barmode="group",
                        title="Score Breakdown by Category per Resume",
                        xaxis_title="Category",
                        yaxis_title="Score",
                        yaxis=dict(range=[0, 100]),
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # Tab 3: Skill Breakdown
                with tabs[2]:
                    st.subheader("🧠 Skill Breakdown by Resume")
                    skill_data = {}
                    all_skills = set()

                    for i, item in enumerate(scores_data):
                        name = item.get("candidate_name", f"Resume {i+1}")
                        skills = (
                            item.get("score", {})
                            .get("score_breakdown", {})
                            .get("skills", {})
                        )
                        if isinstance(skills, dict) and skills:
                            skill_data[name] = skills
                            all_skills.update(skills.keys())

                    all_skills = sorted(list(all_skills))
                    fig = go.Figure()
                    for resume, skills in skill_data.items():
                        y = [skills.get(skill, 0) for skill in all_skills]
                        fig.add_trace(go.Bar(name=resume, x=all_skills, y=y))

                    fig.update_layout(
                        barmode="group",
                        title="Skill Breakdown by Resume",
                        xaxis_title="Skill",
                        yaxis_title="Skill Score",
                        yaxis=dict(range=[0, 10]),
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # -- Try rendering Base64 image
            if bar_chart:
                try:
                    if bar_chart.startswith("data:image/png;base64,"):
                        b64_data = bar_chart.split(",")[1]
                    else:
                        b64_data = bar_chart.strip()

                    missing_padding = len(b64_data) % 4
                    if missing_padding:
                        b64_data += "=" * (4 - missing_padding)

                    image_bytes = base64.b64decode(b64_data)
                    st.image(BytesIO(image_bytes), use_container_width=True)
                except Exception as e:
                    render_fallback_chart()
            else:
                render_fallback_chart()

        # -- Summary Insights
        with st.expander("💡 Summary Insights", expanded=True):
            st.markdown("")
            if insights:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #e6f4ff;
                        color: #003366;
                        padding: 1rem;
                        border-radius: 10px;
                        border-left: 6px solid #2c91f0;
                        font-size: 16px;
                        line-height: 1.6;
                    ">
                        {insights}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
