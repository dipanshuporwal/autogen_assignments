from autogen_agentchat.agents import AssistantAgent
from schemas.job_description_schema import JobDescriptionData
from utils.prompt_loader import get_prompt_message_from_template
from models.azure_openai_client import get_model_client
from utils.file_parser import parse_file


class JobDescriptionAnalysisAgent(AssistantAgent):

    def __init__(self):
        # Get Azure OpenAI client
        model_client = get_model_client()

        # Load system message for JD analysis
        system_message = get_prompt_message_from_template(
            "sys_jd_analysis_template.j2", prompt_type="sys"
        )

        super().__init__(
            name="JobDescriptionAnalysisAgent",
            model_client=model_client,
            system_message=system_message,
            output_content_type=JobDescriptionData,
        )

    async def analyze_job_description(
        self, jd_path: str
    ) -> JobDescriptionData:
        # Extract raw job description text
        jd_text = parse_file(jd_path)

        # Load user message prompt with JD text
        user_message = get_prompt_message_from_template(
            "usr_jd_analysis_template.j2",
            prompt_type="usr",
            jd_text=jd_text,
        )

        response = await self.run(task=user_message)
        return response.messages[
            -1
        ].content  # This will be of type JobDescriptionData
