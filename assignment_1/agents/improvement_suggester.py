from autogen_agentchat.agents import AssistantAgent
from schemas.improvement_schema import ImprovementRecommendationData
from utils.prompt_loader import get_prompt_message_from_template
from models.azure_openai_client import get_model_client
from typing import Optional

class ImprovementRecommendationAgent(AssistantAgent):

    def __init__(self):
        # Get Azure OpenAI client
        model_client = get_model_client()

        # Load system prompt for improvement recommendation
        system_message = get_prompt_message_from_template(
            "sys_improvement_recommendation_template.j2", prompt_type="sys"
        )

        super().__init__(
            name="ImprovementRecommendationAgent",
            model_client=model_client,
            system_message=system_message,
            output_content_type=ImprovementRecommendationData,
        )

    async def recommend_improvements(
        self,
        resume_data: dict,
        job_description: dict,
        rag_context: Optional[str] = None,
    ) -> ImprovementRecommendationData:
        # Load user message with both resume and JD for comparison
        user_message = get_prompt_message_from_template(
            "usr_improvement_recommendation_template.j2",
            prompt_type="usr",
            resume_data=resume_data,
            job_description=job_description,
            rag_context=rag_context,
        )

        response = await self.run(task=user_message)
        return response.messages[
            -1
        ].content  # Parsed as ImprovementRecommendationData
