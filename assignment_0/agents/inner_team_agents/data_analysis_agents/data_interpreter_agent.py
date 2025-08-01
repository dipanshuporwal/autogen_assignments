from autogen_agentchat.agents import AssistantAgent

def get_data_interpreter_agent(model_client):
    data_interpreter_agent = AssistantAgent(
        name="DataInterpreterAgent",
        model_client=model_client,
        system_message=(
            "Performs detailed interpretation of the collected data. Identify"
            " trends and anomalies."
        ),
    )
    return data_interpreter_agent
