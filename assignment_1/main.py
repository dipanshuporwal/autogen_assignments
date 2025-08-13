import re
import os
import json
import asyncio
from typing import Dict, Any, List
from agents.resume_processor import ResumeProcessorAgent
from agents.jd_analyzer import JobDescriptionAnalysisAgent
from agents.ats_scorer import ATSScoringAgent
from agents.improvement_suggester import ImprovementRecommendationAgent
from agents.visualizer import VisualizationAgent
from utils.file_io import save_output_to_file
from rag.rag_retriever import get_augmented_context
from mongodb.mongo_writes import (
    save_resume_data,
    save_jd_data,
    save_scoring_history,
    suggest_relevant_jobs,
)
from config.docker_util import (
    getDockerCommandLineExecutor,
    start_docker_container,
    stop_docker_container,
)

os.environ["TOKENIZERS_PARALLELISM"] = "false"


async def run_resume_pipeline(resume_path: str) -> Dict[str, Any]:
    """Process a single resume file and return structured data."""
    try:
        r_agent = ResumeProcessorAgent()
        resume_data = await r_agent.process_resume_data(resume_path)
        resume_json = resume_data.model_dump()
        print(f"\n✅ Processed Resume: {resume_path}\n{resume_json}")

        # Save resume in DB
        candidate_name = sanitize_filename(resume_json.get("name", ""))
        save_resume_data(candidate_name, resume_json)

        # Save resume in local folder
        # resume_filename = os.path.splitext(os.path.basename(resume_path))[0]
        save_output_to_file(
            resume_json, f"{candidate_name}_output.json", subfolder="resumes"
        )

        return resume_json
    except Exception as e:
        print(f"\n❌ Error processing resume {resume_path}: {e}")
        return {"error": str(e), "path": resume_path}


async def run_jd_pipeline(jd_path: str) -> Dict[str, Any]:
    """Process a single job description file and return structured data."""
    try:
        jd_agent = JobDescriptionAnalysisAgent()
        jd_data = await jd_agent.analyze_job_description(jd_path)
        jd_json = jd_data.model_dump()
        print(f"\n✅ Processed JD: {jd_path}\n{jd_json}")

        jd_filename = os.path.splitext(os.path.basename(jd_path))[0]
        save_jd_data(jd_filename, jd_json)
        save_output_to_file(
            jd_json, f"{jd_filename}_output.json", subfolder="jds"
        )

        return jd_json
    except Exception as e:
        print(f"\n❌ Error processing JD {jd_path}: {e}")
        return {"error": str(e), "path": jd_path}


async def run_scoring_pipeline(
    resume_data: Dict[str, Any], jd_data: Dict[str, Any], candidate_name: str
) -> Dict[str, Any]:
    """Call ATS Scoring Agent and save results."""
    try:
        # Inject RAG context
        rag_context = get_augmented_context(
            resume_text=json.dumps(resume_data), jd_text=json.dumps(jd_data)
        )

        scoring_agent = ATSScoringAgent()
        scoring_result = await scoring_agent.score_resume_against_jd(
            resume_data, jd_data, rag_context
        )
        scoring_json = scoring_result.model_dump()
        print(f"\n✅ Scored Resume: {candidate_name}\n{scoring_json}")

        save_scoring_history(
            candidate_name,
            jd_data.get("title", "Unknown"),
            scoring_json,
        )
        save_output_to_file(
            scoring_json, f"{candidate_name}_score.json", subfolder="scores"
        )

        return scoring_json
    except Exception as e:
        print(f"\n❌ Error scoring resume {candidate_name}: {e}")
        return {"error": str(e), "resume": candidate_name}


async def run_improvement_pipeline(
    resume_data: Dict[str, Any], jd_data: Dict[str, Any], candidate_name: str
) -> Dict[str, Any]:
    try:
        # Inject RAG context
        rag_context = get_augmented_context(
            resume_text=json.dumps(resume_data), jd_text=json.dumps(jd_data)
        )

        improvement_agent = ImprovementRecommendationAgent()
        improvement_result = await improvement_agent.recommend_improvements(
            resume_data, jd_data, rag_context
        )
        improvement_json = improvement_result.model_dump()
        print(f"\n✅ Recommendations:\n{improvement_json}")

        save_output_to_file(
            improvement_json,
            f"{candidate_name}_recommendations.json",
            subfolder="recommendations",
        )

        return improvement_json
    except Exception as e:
        print(
            f"\n❌ Error generating recommendations for {candidate_name}: {e}"
        )
        return {"error": str(e), "resume": candidate_name}


async def run_visualization_pipeline(
    all_scores: List[Dict[str, Any]],
) -> Dict[str, Any]:
    try:
        visualization_agent = VisualizationAgent()

        # Combine all relevant data for visualization
        visualization_input = [
            {
                "candidate_name": entry["candidate_name"],
                "total_score": entry["score"]["total_score"],
                "score_breakdown": entry["score"]["score_breakdown"],
            }
            for entry in all_scores
            if "error" not in entry
        ]

        visualization_result = (
            await visualization_agent.generate_visualization(
                visualization_input=visualization_input
            )
        )

        visualization_json = visualization_result.model_dump()
        print(f"\n✅ Visualization Generated:\n{visualization_json}")

        save_output_to_file(
            visualization_json,
            "visualization_output.json",
            subfolder="visualizations",
        )

        return visualization_json
    except Exception as e:
        print(f"\n❌ Error generating visualizations: {e}")
        return {"error": str(e)}


async def run_pipeline(
    resume_folder_path: str, jd_folder_path: str
) -> Dict[str, Any]:
    """Main pipeline that processes resumes and a JD file."""
    # -------------------------
    # Collect Job Descriptions
    # -------------------------
    jd_files = [
        os.path.join(jd_folder_path, f)
        for f in os.listdir(jd_folder_path)
        if os.path.isfile(os.path.join(jd_folder_path, f))
    ]

    if not jd_files:
        print("⚠️ No job descriptions found in the folder.")
        return {}

    # Use first JD for now (future: support multiple)
    jd_path = jd_files[0]

    # -------------------------
    # Collect Resumes
    # -------------------------
    resume_files = [
        os.path.join(resume_folder_path, f)
        for f in os.listdir(resume_folder_path)
        if os.path.isfile(os.path.join(resume_folder_path, f))
    ]

    if not resume_files:
        print("⚠️ No resumes found in the folder.")
        return {}

    # -------------------------
    # Process All Resumes Concurrently
    # -------------------------
    resume_tasks = [
        run_resume_pipeline(resume_path) for resume_path in resume_files
    ]

    # Run all at once
    jd_data, all_resume_data = await asyncio.gather(
        run_jd_pipeline(jd_path), asyncio.gather(*resume_tasks)
    )

    # -------------------------
    # Score and improvement recommendation for each Resume in parallel
    # -------------------------
    scores_and_recommendations = await asyncio.gather(
        *[
            process_resume(resume_data, jd_data)
            for resume_data in all_resume_data
        ]
    )

    # -------------------------
    # Visulaization of Resumes Comparison
    # -------------------------
    visualization = await run_visualization_pipeline(
        scores_and_recommendations
    )

    print(f"all_resume_data:{all_resume_data}")
    suggested_jobs = [
        suggest_relevant_jobs(resume["skills"]) for resume in all_resume_data
    ]

    # -------------------------
    # Return Combined Result
    # -------------------------
    return {
        "job_description": jd_data,
        "resumes": all_resume_data,
        "scores_and_recommendations": scores_and_recommendations,
        "suggested_jobs": suggested_jobs,
        "visualization": visualization,
    }


async def process_resume(resume_data, jd_data):
    if "error" in resume_data:
        return resume_data

    candidate_name = sanitize_filename(resume_data.get("name", ""))

    # Run scoring and improvement in parallel for each resume
    score, improvements = await asyncio.gather(
        run_scoring_pipeline(resume_data, jd_data, candidate_name),
        run_improvement_pipeline(resume_data, jd_data, candidate_name),
    )

    return {
        "candidate_name": candidate_name,
        "score": score,
        "recommendations": improvements,
    }


def sanitize_filename(name: str) -> str:
    return re.sub(r"[^\w\-_.]", "_", name)


# ✅ Entry point wrapped with Docker lifecycle
async def main():
    resume_folder = "input/test_resume"
    jd_folder = "input/test_jd"

    docker = getDockerCommandLineExecutor()

    try:
        await start_docker_container(docker)

        final_output = await run_pipeline(resume_folder, jd_folder)

        with open("output/combined_data.json", "w") as f:
            json.dump(final_output, f, indent=2)

        print("\n🎯 Pipeline completed. Output saved to output.json.")

    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
    finally:
        await stop_docker_container(docker)


if __name__ == "__main__":
    asyncio.run(main())
