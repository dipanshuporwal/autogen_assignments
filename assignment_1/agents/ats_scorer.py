from autogen_agentchat.agents import AssistantAgent
from schemas.ats_schema import ATSScoringData
from utils.prompt_loader import get_prompt_message_from_template
from models.azure_openai_client import get_model_client
from typing import Optional

class ATSScoringAgent(AssistantAgent):

    def __init__(self):
        # Get Azure OpenAI model client
        model_client = get_model_client()

        # Load system message that defines a consistent scoring strategy
        system_message = get_prompt_message_from_template(
            "sys_ats_scoring_template.j2", prompt_type="sys"
        )

        super().__init__(
            name="ATSScoringAgent",
            model_client=model_client,
            system_message=system_message,
            output_content_type=ATSScoringData,
        )

    async def score_resume_against_jd(
        self, resume_data: dict, job_description: dict, rag_context: Optional[str]=None
    ) -> ATSScoringData:
        """
        Compares extracted resume data with job description and returns detailed ATS scoring.
        Args:
            resume_data (dict): Extracted structured resume data
            job_description (str): Raw text of the JD
        Returns:
            ATSScoringData: Contains scores and breakdowns
        """

        user_message = get_prompt_message_from_template(
            "usr_ats_scoring_template.j2",
            prompt_type="usr",
            resume_data=resume_data,
            job_description=job_description,
            rag_context=rag_context,
        )

        response = await self.run(task=user_message)
        return response.messages[-1].content  # Structured ATSScoringData
