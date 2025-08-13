from mongodb.mongo_seed import db
from datetime import datetime
from typing import Dict, Any


def save_resume_data(candidate_name: str, resume_json: Dict[str, Any]):
    db.resumes.insert_one(
        {
            "candidate_name": candidate_name,
            "resume_json": resume_json,
            "created_at": datetime.utcnow(),
        }
    )


def save_jd_data(file_name: str, jd_json: Dict[str, Any]):
    db.resumes.insert_one(
        {
            "file_name": file_name,
            "jd_json": jd_json,
            "created_at": datetime.utcnow(),
        }
    )


def save_scoring_history(
    candidate_name: str,
    jd_title: str,
    score: Dict[str, Any],
):
    db.scoring_history.insert_one(
        {
            "candidate_name": candidate_name,
            "jd_title": jd_title,
            "total_score": score["total_score"],
            "score_breakdown": score["score_breakdown"],
            "feedback": score["feedback"],
            "scored_at": datetime.utcnow(),
        }
    )


def suggest_relevant_jobs(resume_skills: list, top_k: int = 3):
    return list(
        db.open_jobs.find({"required_skills": {"$in": resume_skills}}).limit(
            top_k
        )
    )
