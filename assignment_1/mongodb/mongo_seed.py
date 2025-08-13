import re
from typing import List, Dict
from pymongo import MongoClient
from datetime import datetime

# --- MongoDB Configuration ---
MONGO_URI = "mongodb://localhost:27020/"
DB_NAME = "ats_resume_db"

# --- Connect to MongoDB ---
client = MongoClient(MONGO_URI)
db = client[DB_NAME]


# --- Collection Check and Seeding ---
def ensure_collections_exist():
    existing = db.list_collection_names()

    if "job_templates" not in existing:
        db.job_templates.insert_many(
            [
                {
                    "title": "Software Engineer",
                    "required_skills": ["Java", "Spring Boot", "REST APIs"],
                    "preferred_keywords": [
                        "microservices",
                        "distributed systems",
                    ],
                },
                {
                    "title": "Data Scientist",
                    "required_skills": [
                        "Python",
                        "Pandas",
                        "Machine Learning",
                    ],
                    "preferred_keywords": ["scikit-learn", "data analysis"],
                },
                {
                    "title": "AI Engineer",
                    "required_skills": [
                        "Python",
                        "Deep Learning",
                        "TensorFlow",
                        "PyTorch",
                    ],
                    "preferred_keywords": [
                        "transformers",
                        "neural networks",
                        "inference",
                    ],
                },
                {
                    "title": "Python Developer",
                    "required_skills": [
                        "Python",
                        "Flask",
                        "FastAPI",
                        "SQLAlchemy",
                    ],
                    "preferred_keywords": [
                        "async programming",
                        "data pipelines",
                        "RESTful APIs",
                    ],
                },
            ]
        )
        print("Seeded 'job_templates'")

    if "resume_feedback" not in existing:
        db.resume_feedback.insert_many(
            [
                {
                    "content": (
                        "Use consistent bullet formatting throughout"
                        " experience section."
                    ),
                    "tags": ["formatting"],
                },
                {
                    "content": (
                        "Mention quantifiable achievements using numbers"
                        " (e.g., 'improved latency by 40%')."
                    ),
                    "tags": ["content", "metrics"],
                },
                {
                    "content": (
                        "Group similar skills and tools to improve readability"
                        " (e.g., 'Java, Spring, Hibernate')."
                    ),
                    "tags": ["skills"],
                },
            ]
        )
        print("Seeded 'resume_feedback'")

    if "skill_chunks" not in existing:
        db.skill_chunks.insert_many(
            [
                # Existing examples
                {
                    "content": (
                        "Java is a high-level programming language used in"
                        " backend systems."
                    )
                },
                {
                    "content": (
                        "Spring Boot enables microservice architecture using"
                        " Java."
                    )
                },
                {
                    "content": (
                        "Best practices for resume formatting include clear"
                        " section headers and consistent font usage."
                    )
                },
                {
                    "content": (
                        "Microservices should be described with deployment or"
                        " scaling examples."
                    )
                },
                # AI and Python additions
                {
                    "content": (
                        "Python is a versatile language commonly used in"
                        " scripting, automation, and data science."
                    )
                },
                {
                    "content": (
                        "TensorFlow and PyTorch are popular frameworks for"
                        " building deep learning models."
                    )
                },
                {
                    "content": (
                        "AI Engineers should demonstrate experience with"
                        " model training, evaluation, and deployment."
                    )
                },
                {
                    "content": (
                        "Use of transformer models like BERT or GPT should be"
                        " backed by fine-tuning or inference examples."
                    )
                },
                {
                    "content": (
                        "FastAPI is a modern web framework for building"
                        " high-performance APIs in Python."
                    )
                },
                {
                    "content": (
                        "Explain asynchronous programming using 'async/await'"
                        " in Python for scalable applications."
                    )
                },
            ]
        )
        print("Seeded 'skill_chunks'")

    if "resumes" not in existing:
        db.resumes.insert_one(
            {
                "candidate_name": "example",
                "resume_json": "example json",
                "created_at": datetime.utcnow(),
            }
        )
    print("Seeded 'resumes'")

    if "job_description" not in existing:
        db.job_description.insert_one(
            {
                "file_name": "example",
                "jd_json": "example json",
                "created_at": datetime.utcnow(),
            }
        )
    print("Seeded 'job_description'")

    if "scoring_history" not in existing:
        db.scoring_history.insert_one(
            {
                "candidate_name": "example",
                "jd_title": "Software Engineer",
                "score": 85,
                "recommendations": ["Improve formatting"],
                "scored_at": datetime.utcnow(),
            }
        )
        print("Seeded 'scoring_history'")

    if "users" not in existing:
        db.users.insert_one(
            {"user_id": "user123", "name": "Dipanshu", "session_data": {}}
        )
        print("Seeded 'users'")

    if "open_jobs" not in existing:
        db.open_jobs.insert_many(
            [
                {
                    "title": "Backend Developer",
                    "description": "Looking for Python + FastAPI devs",
                    "required_skills": ["Python", "FastAPI"],
                    "location": "Remote",
                    "posted_at": datetime.utcnow(),
                },
                {
                    "title": "AI Engineer",
                    "description": "Experience in Transformers and ML",
                    "required_skills": ["Transformers", "PyTorch"],
                    "location": "Bangalore",
                    "posted_at": datetime.utcnow(),
                },
            ]
        )
        print("Seeded 'open_jobs'")


# --- MongoDB Fetch Utilities ---
def fetch_skill_chunks() -> List[str]:
    cursor = db.skill_chunks.find()
    return [doc["content"] for doc in cursor if "content" in doc]


def fetch_job_template_by_title(title: str) -> Dict:
    escaped_title = re.escape(title)
    return (
        db.job_templates.find_one(
            {"title": {"$regex": escaped_title, "$options": "i"}}
        )
        or {}
    )


def fetch_feedback_by_tag(tag: str) -> List[str]:
    escaped_tag = re.escape(tag)
    cursor = db.resume_feedback.find(
        {"tags": {"$regex": escaped_tag, "$options": "i"}}
    )
    # cursor = db.resume_feedback.find({"tags": tag})
    return [doc["content"] for doc in cursor]
