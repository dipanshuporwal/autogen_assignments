import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html


def render_chart(
    data_dict: dict, title_prefix: str, selected_chart: str, zmax=100
):
    labels = list(data_dict.keys())
    values = list(data_dict.values())

    if selected_chart == "Pie Chart":
        pie_fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                )
            ]
        )
        pie_fig.update_layout(title=f"{title_prefix} Score Distribution (Pie)")
        st.plotly_chart(pie_fig, use_container_width=True)

    elif selected_chart == "Bar Chart":
        bar_fig = go.Figure(
            data=[
                go.Bar(
                    x=labels,
                    y=values,
                )
            ]
        )
        bar_fig.update_layout(title=f"{title_prefix} Score Distribution (Bar)")
        st.plotly_chart(bar_fig, use_container_width=True)

    elif selected_chart == "Radar Chart":
        radar_fig = go.Figure(
            data=go.Scatterpolar(
                r=values + [values[0]],
                theta=labels + [labels[0]],
                fill="toself",
            )
        )
        radar_fig.update_layout(
            title=f"{title_prefix} Score Distribution (Radar)",
            polar=dict(radialaxis=dict(visible=True)),
        )
        st.plotly_chart(radar_fig, use_container_width=True)

    elif selected_chart == "Donut Chart":
        donut_fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    textinfo="label+percent",
                    insidetextorientation="radial",
                )
            ]
        )
        donut_fig.update_layout(
            title=f"{title_prefix} Score Distribution (Donut)"
        )
        st.plotly_chart(donut_fig, use_container_width=True)

    elif selected_chart == "Heatmap":
        sorted_data = sorted(
            data_dict.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        keys_sorted, values_sorted = zip(*sorted_data)
        heatmap_fig = go.Figure(
            data=go.Heatmap(
                z=[values_sorted],
                x=keys_sorted,
                y=["General Scores"],
                colorscale="YlGnBu",
                zmin=0,
                zmax=zmax,
                showscale=True,
                colorbar=dict(title="Score / 100"),
                hovertemplate="%{x}: %{z}<extra></extra>",
            )
        )
        heatmap_fig.update_layout(
            title=f"{title_prefix} Score Distribution (Heatmap)",
            xaxis=dict(tickangle=-45),
            margin=dict(l=40, r=20, t=40, b=80),
            height=300,
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)


def render_resume_summaries(result: dict):
    with st.expander("📝 Resume(s) Summary", expanded=True):
        for score_item, job_item in zip(
            result.get("scores_and_recommendations", []),
            result.get("suggested_jobs", []),
        ):
            candidate_name = score_item.get("candidate_name", "Unknown")
            with st.expander(f"📎 Resume: {candidate_name}", expanded=True):
                score = score_item.get("score", {})
                recs = score_item.get("recommendations", {})

                with st.expander("📈 Score Summary", expanded=True):
                    score_breakdown = score.get("score_breakdown", {})
                    if not score_breakdown:
                        st.info("No score breakdown available.")
                    else:
                        # Separate out 'skills' if it's a nested dict
                        skill_scores = score_breakdown.get("skills", {})
                        general_scores = {
                            k: v
                            for k, v in score_breakdown.items()
                            if k != "skills"
                        }
                        total_skill_score = (
                            sum(skill_scores.values())
                            if isinstance(skill_scores, dict)
                            else skill_scores
                        )
                        general_scores["skill"] = total_skill_score

                        chart_options = [
                            "Pie Chart",
                            "Bar Chart",
                            "Radar Chart",
                            "Donut Chart",
                            "Heatmap",
                        ]
                        selected_chart = st.radio(
                            f"Select chart for: {candidate_name}",
                            options=chart_options,
                            horizontal=True,
                            key=f"chart_select_{candidate_name}",
                        )

                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("**⭐ General Score Chart**")
                            if general_scores:
                                render_chart(
                                    general_scores,
                                    "General",
                                    selected_chart,
                                    100,
                                )

                            with col2:
                                # Skills Matching Breakdown
                                st.markdown("**🧠 Skill Score Chart**")
                                if (
                                    isinstance(skill_scores, dict)
                                    and skill_scores
                                ):
                                    render_chart(
                                        skill_scores,
                                        "Skill",
                                        selected_chart,
                                        10,
                                    )

                        # Total score metric
                        st.metric(
                            "✅ Total ATS Score",
                            f"{score.get('total_score', 0):.1f}/100",
                        )

                # Feedback
                if score.get("feedback"):
                    with st.expander("💬 Feedback", expanded=True):
                        for fb in score["feedback"]:
                            st.markdown(
                                f"<div class='feedback-box'>📝 {fb}</div>",
                                unsafe_allow_html=True,
                            )

                # Recommendations Carousel
                with st.expander("🛠️ Recommendations", expanded=True):
                    recommendations = recs.get("recommendations", [])
                    if recommendations:
                        cards_html = ""
                        for idx, r in enumerate(recommendations):
                            cards_html += f"""
                                <div class="carousel-card">
                                    <h4>📍 {r['section']}</h4>
                                    <p><strong>💡 Suggestion:</strong> {r['suggestion']}</p>
                                    <p><strong>🔍 Reason:</strong> {r['reason']}</p>
                                </div>
                            """

                        carousel_html = f"""
                        <style>
                        .carousel-container {{
                            position: relative;
                            overflow: hidden;
                            width: 100%;
                        }}
                        .carousel-track {{
                            display: flex;
                            overflow-x: auto;
                            scroll-behavior: smooth;
                            gap: 16px;
                            padding: 10px;
                        }}
                        .carousel-card {{
                            flex: 0 0 300px;
                            background: #fffde7;
                            padding: 15px;
                            border-radius: 10px;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                            min-height: 180px;
                        }}
                        .carousel-btn {{
                            position: absolute;
                            top: 45%;
                            background-color: rgba(0,0,0,0.5);
                            color: white;
                            border: none;
                            padding: 6px 10px;
                            cursor: pointer;
                            z-index: 2;
                            border-radius: 50%;
                        }}
                        .carousel-btn.left {{ left: 0; transform: translateY(-50%); }}
                        .carousel-btn.right {{ right: 0; transform: translateY(-50%); }}
                        </style>

                        <div class="carousel-container">
                            <button class="carousel-btn left" id="btn-left" onclick="scrollCarousel(-1)">◀</button>
                            <div id="carousel-track" class="carousel-track">
                                {cards_html}
                            </div>
                            <button class="carousel-btn right" id="btn-right" onclick="scrollCarousel(1)">▶</button>
                        </div>

                        <script>
                        const track = document.getElementById("carousel-track");
                        const cardWidth = 316; // 300 + 16 gap

                        function scrollCarousel(direction) {{
                            const maxScrollLeft = track.scrollWidth - track.clientWidth;
                            track.scrollLeft += direction * cardWidth;

                            // Optional: Disable arrows at ends
                            setTimeout(() => {{
                                document.getElementById("btn-left").disabled = track.scrollLeft <= 0;
                                document.getElementById("btn-right").disabled = track.scrollLeft >= maxScrollLeft - 5;
                            }}, 300);
                        }}

                        // Disable left button initially
                        setTimeout(() => {{
                            document.getElementById("btn-left").disabled = true;
                        }}, 100);
                        </script>
                        """

                        html(carousel_html, height=260)
                    else:
                        st.info("No recommendations available.")

                def render_skill_boxes(skills: list[str]) -> str:
                    if not skills:
                        return "<p>NA</p>"

                    boxes = "".join(
                        f"<span class='skill-box'>{skill}</span>"
                        for skill in skills
                    )
                    return f"<div class='skill-box-container'>{boxes}</div>"

                with st.expander("🎯 Suggested Open Jobs", expanded=True):
                    for job in job_item:
                        with st.container():
                            st.markdown("----")  # separator between jobs

                            st.markdown(
                                f"### 💼 {job.get('title', 'Untitled Job')}"
                            )

                            st.markdown(
                                "**📝 Description:**"
                                f" {job.get('description', 'NA')}"
                            )

                            st.markdown(
                                "**🛠 Required Skills:**"
                                f" {render_skill_boxes(job.get('required_skills', []))}",
                                unsafe_allow_html=True,
                            )
