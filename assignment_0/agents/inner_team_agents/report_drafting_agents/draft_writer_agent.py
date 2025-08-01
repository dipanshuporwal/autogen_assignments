from autogen_agentchat.agents import AssistantAgent

def get_draft_writer_agent(model_client):
    draft_writer_agent = AssistantAgent(
        name="DraftWriterAgent",
        model_client=model_client,
        system_message=(
            "Writes the final report using insights provided by the analysis"
            " team."
        ),
    )
    return draft_writer_agent
