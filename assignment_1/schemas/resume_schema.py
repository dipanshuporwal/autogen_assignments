from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import List, Optional


class Experience(BaseModel):
    job_title: str = Field(
        ..., description="Title or role held by the candidate."
    )
    company: str = Field(..., description="Company or organization name.")
    start_date: Optional[str] = Field(
        "", description="Start date in 'YYYY-MM' or 'YYYY' format."
    )
    end_date: Optional[str] = Field(
        "",
        description="End date in 'YYYY-MM' or 'YYYY' format, or 'Present'.",
    )
    duration_in_months: Optional[int] = Field(
        0,
        description=(
            "Duration of employment in months (auto-computed if missing)."
        ),
    )
    description: Optional[str] = Field(
        "",
        description=(
            "Brief summary of responsibilities and achievements in the role."
        ),
    )
    is_career_gap: Optional[bool] = Field(
        False,
        description=(
            "True if this entry represents a period of unemployment or gap."
        ),
    )


class Education(BaseModel):
    degree: str = Field(
        ..., description="Degree obtained, e.g., B.Tech, MBA, M.Sc."
    )
    institution: str = Field(
        ..., description="University or institution attended."
    )
    graduation_year: Optional[str] = Field(
        "", description="Year of graduation or completion."
    )
    grade: Optional[str] = Field(
        "", description="GPA, percentage, or division achieved (optional)."
    )


class Certification(BaseModel):
    name: str = Field(..., description="Name of the certification.")
    issuer: Optional[str] = Field(
        "",
        description="Issuing authority or organization (e.g., Coursera, AWS).",
    )
    date_issued: Optional[str] = Field(
        "", description="Date of certification issuance (YYYY or YYYY-MM)."
    )


class Project(BaseModel):
    title: str = Field(..., description="Name or title of the project.")
    description: Optional[str] = Field(
        "",
        description="Brief overview of the project objectives and outcomes.",
    )
    technologies_used: Optional[List[str]] = Field(
        [],
        description="Technologies, tools, or frameworks used in the project.",
    )


class ResumeData(BaseModel):
    # Contact and identity
    name: str = Field(..., description="Full name of the candidate.")
    email: Optional[EmailStr] = Field("", description="Primary email address.")
    phone: Optional[str] = Field(
        None, description="Phone number with country code."
    )
    # linkedin: Optional[HttpUrl] = Field(
    #     None, description="URL to the candidate's LinkedIn profile."
    # )
    # github: Optional[HttpUrl] = Field(
    #     None, description="URL to the candidate's GitHub profile."
    # )
    # personal_website: Optional[HttpUrl] = Field(
    #     None, description="URL to a portfolio or personal website."
    # )

    # Summary and core sections
    summary: Optional[str] = Field(
        "", description="Professional summary or objective statement."
    )
    skills: List[str] = Field(
        ..., description="List of relevant technical and soft skills."
    )
    languages: Optional[List[str]] = Field(
        [], description="Languages spoken by the candidate."
    )

    # Experience and education
    experience: List[Experience] = Field(
        ..., description="List of past jobs or professional experiences."
    )
    education: List[Education] = Field(
        ..., description="List of academic qualifications and institutions."
    )

    # Optional extras
    certifications: Optional[List[Certification]] = Field(
        [], description="List of certifications, licenses, or credentials."
    )
    projects: Optional[List[Project]] = Field(
        [], description="List of academic or professional projects."
    )

    # Meta/summary fields
    total_years_experience: Optional[float] = Field(
        0.0,
        description=(
            "Estimated total professional experience in years (can be"
            " computed)."
        ),
    )
    has_career_gap: Optional[bool] = Field(
        False, description="True if one or more career gaps were detected."
    )
