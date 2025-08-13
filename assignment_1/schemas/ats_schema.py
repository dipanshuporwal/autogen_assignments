from typing import Dict, List, Optional, Union, Any

from pydantic import BaseModel, Field


class ATSScoringData(BaseModel):
    total_score: float = Field(
        ...,
        description=(
            "The overall ATS score calculated out of 100 based on the defined"
            " rubric."
        ),
    )
    score_breakdown: Optional[Dict[str, Union[float, Dict[str, float]]]] = (
        Field(
            {},
            description=(
                "A dictionary representing individual component scores. Keys"
                " include: 'skills', 'experience', 'education',"
                " 'certifications', 'communication', 'presentation'. For"
                " 'skills', the value is a nested dictionary with skill names"
                " as keys and their matching score (float) as values. For"
                " other keys, the value is a float score."
            ),
        )
    )
    feedback: Optional[List[str]] = Field(
        [],
        description=(
            "List of feedback comments explaining the strengths and weaknesses"
            " of the resume based on the scoring criteria."
        ),
    )
