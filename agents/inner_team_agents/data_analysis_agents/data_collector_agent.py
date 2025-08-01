from autogen_agentchat.agents import AssistantAgent

def get_data_collector_agent(model_client):
    data_collector_agent = AssistantAgent(
        name="DataCollectorAgent",
        model_client=model_client,
        system_message=(
            "Collects relevant data from past performance and current market"
            " conditions."
        ),
    )
    return data_collector_agent
