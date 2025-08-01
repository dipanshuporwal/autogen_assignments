from autogen_agentchat.agents import AssistantAgent

def get_format_specialist_agent(model_client):
    format_specialist_agent = AssistantAgent(
        name="FormatSpecialistAgent",
        model_client=model_client,
        system_message=(
            "Ensures the final report is visually formatted for business"
            " audiences."
        ),
    )
    return format_specialist_agent
