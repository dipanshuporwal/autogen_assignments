from pydantic import BaseModel, Field
from typing import List

class RecommendationItem(BaseModel):
    section: str = Field(
        ...,
        description="The specific section of the resume the recommendation applies to (e.g., 'Skills', 'Experience', 'Summary')."
    )
    suggestion: str = Field(
        ...,
        description="A concrete, actionable suggestion to improve the resume in the specified section."
    )
    reason: str = Field(
        ...,
        description="The rationale behind the suggestion, typically based on a comparison with the job description."
    )

class ImprovementRecommendationData(BaseModel):
    overall_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="The overall match score between the resume and job description, from 0 to 100."
    )
    recommendations: List[RecommendationItem] = Field(
        ...,
        description="A list of targeted recommendations for improving the resume to better align with the job description."
    )
