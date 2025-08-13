from typing import List, Dict, Any
from autogen_agentchat.agents import AssistantAgent
from schemas.visualization_schema import VisualizationOutputData
from utils.prompt_loader import get_prompt_message_from_template
from models.azure_openai_client import get_model_client


class VisualizationAgent(AssistantAgent):
    def __init__(self):
        # Initialize the model client
        model_client = get_model_client()

        # Load system prompt template for visualization generation
        system_message = get_prompt_message_from_template(
            "sys_visualization_template.j2", prompt_type="sys"
        )

        super().__init__(
            name="VisualizationAgent",
            model_client=model_client,
            system_message=system_message,
            output_content_type=VisualizationOutputData,
        )

    async def generate_visualization(
        self,
        visualization_input: List[Dict[str,Any]],
    ) -> VisualizationOutputData:
        user_message = get_prompt_message_from_template(
            "usr_visualization_template.j2",
            prompt_type="usr",
            visualization_input=visualization_input,
        )

        response = await self.run(task=user_message)
        return response.messages[
            -1
        ].content  # Parsed as VisualizationOutputData
