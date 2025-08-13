from typing import List, Dict
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from mongodb.mongo_seed import (
    fetch_skill_chunks,
    fetch_job_template_by_title,
    fetch_feedback_by_tag,
    ensure_collections_exist,
)

ensure_collections_exist()
skill_chunks = fetch_skill_chunks()
if not skill_chunks:
    raise ValueError(
        "No skill chunks found in MongoDB. Please seed the 'skill_chunks'"
        " collection."
    )

# Example embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
# Precompute and store embeddings (normally done offline)
skill_embeddings = embedding_model.encode(
    skill_chunks, convert_to_tensor=False
)
index = faiss.IndexFlatL2(len(skill_embeddings[0]))
index.add(np.array(skill_embeddings))

# Map index positions to text
index_to_text = {i: chunk for i, chunk in enumerate(skill_chunks)}


def retrieve_context(query: str, top_k: int = 3) -> List[str]:
    query_embedding = embedding_model.encode([query], convert_to_tensor=False)
    scores, indices = index.search(np.array(query_embedding), top_k)
    return [index_to_text[i] for i in indices[0]]


def get_augmented_context(
    resume_text: str, jd_text: str
) -> Dict[str, List[str]]:
    resume_context = retrieve_context(resume_text)
    jd_context = retrieve_context(jd_text)

    # Fetch structured data
    job_template = fetch_job_template_by_title(
        jd_text[:100]
    )  # crude title match from JD
    feedback_suggestions = fetch_feedback_by_tag(
        "formatting"
    )  # default tag for now

    return {
        "resume_context": resume_context,
        "jd_context": jd_context,
        "job_template": job_template,
        "feedback_suggestions": feedback_suggestions,
    }
