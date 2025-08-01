from autogen_agentchat.agents import AssistantAgent

def get_content_editor_agent(model_client):
    content_editor_agent = AssistantAgent(
        name="ContentEditorAgent",
        model_client=model_client,
        system_message="Edits the draft for tone, clarity, and completeness.",
    )
    return content_editor_agent
