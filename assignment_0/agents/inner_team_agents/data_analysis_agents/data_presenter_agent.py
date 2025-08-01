from autogen_agentchat.agents import AssistantAgent

def get_data_presenter_agent(model_client):
    data_presenter_agent = AssistantAgent(
        name="DataPresenterAgent",
        model_client=model_client,
        system_message=(
            "Summarizes interpreted data into easy-to-understand insights."
        ),
    )
    return data_presenter_agent
