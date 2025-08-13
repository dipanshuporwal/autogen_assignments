from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class VisualizationOutputData(BaseModel):
    chart_base64: str = Field(
        ...,
        description=(
            "A base64-encoded strings representing generated bar chart."
            " Useful for embedding directly into frontends or reports."
        ),
    )
    summary_insights: Optional[str] = Field(
        None,
        description=(
            "A concise textual summary of key insights or takeaways from the"
            " visualizations, useful for quick interpretation."
        ),
    )

    model_config = ConfigDict(extra="forbid")
