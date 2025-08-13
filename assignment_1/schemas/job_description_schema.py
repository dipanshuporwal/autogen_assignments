from pydantic import BaseModel, Field
from typing import List, Optional


class MatchingCriterion(BaseModel):
    skill: str = Field(..., description="Skill or attribute to match")
    weight: Optional[int] = Field(
        1, description="Weight/importance of this criterion"
    )


class JobDescriptionData(BaseModel):
    job_title: Optional[str] = Field(
        "",
        description=(
            "The official title of the job position as stated in the job"
            " description."
        ),
    )

    responsibilities: Optional[List[str]] = Field(
        [],
        description=(
            "A list of key duties and responsibilities expected from the"
            " candidate."
        ),
    )

    required_skills: Optional[List[str]] = Field(
        [],
        description=(
            "A list of mandatory skills and competencies that the candidate"
            " must have."
        ),
    )

    preferred_skills: Optional[List[str]] = Field(
        [],
        description=(
            "A list of additional, nice-to-have skills that are not strictly"
            " required but preferred."
        ),
    )

    education_requirements: Optional[str] = Field(
        "",
        description=(
            "Minimum educational qualifications required, such as degrees or"
            " diplomas."
        ),
    )

    experience_required: Optional[str] = Field(
        "",
        description=(
            "The number of years or type of experience required for the"
            " position."
        ),
    )

    certifications: Optional[List[str]] = Field(
        [],
        description=(
            "Specific professional certifications that are required or"
            " desirable for the role."
        ),
    )

    domain_keywords: Optional[List[str]] = Field(
        [],
        description=(
            "Key industry-specific terms, tools, technologies, or"
            " methodologies mentioned in the job description."
        ),
    )

    matching_criteria: Optional[List[MatchingCriterion]] = Field(
        [],
        description=(
            "A list of criteria for resume matching, each with an associated"
            " skill and weight."
        ),
    )
