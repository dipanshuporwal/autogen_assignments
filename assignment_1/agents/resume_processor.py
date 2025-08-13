from autogen_agentchat.agents import AssistantAgent
from schemas.resume_schema import ResumeData
from utils.prompt_loader import get_prompt_message_from_template
from utils.file_parser import parse_file
from models.azure_openai_client import get_model_client


class ResumeProcessorAgent(AssistantAgent):

    def __init__(self):
        # Get Azure OpenAI client
        model_client = get_model_client()

        # Load system message template
        system_message = get_prompt_message_from_template(
            "sys_resume_key_info_extarctor_template.j2", prompt_type="sys"
        )

        super().__init__(
            name="ResumeProcessorAgent",
            model_client=model_client,
            system_message=system_message,
            output_content_type=ResumeData,
        )

    async def process_resume_data(self, resume_path: str) -> ResumeData:
        # Parse the file to extract raw text
        resume_text = parse_file(resume_path)

        # Load user message template
        user_message = get_prompt_message_from_template(
            "usr_resume_key_info_extarctor_template.j2",
            prompt_type="usr",
            resume_text=resume_text,
        )

        response = await self.run(task=user_message)
        return response.messages[-1].content  # This will be of type ResumeData
