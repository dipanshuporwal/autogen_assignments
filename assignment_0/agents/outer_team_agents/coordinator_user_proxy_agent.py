from autogen_agentchat.agents import UserProxyAgent


def get_outer_coordinator_agent():
    outer_coordinator_agent = UserProxyAgent(
        name="OuterCoordinatorAgent",
        description=(
            "Coordinates resources across teams, oversees final output"
        ),
        input_func=input,
    )
    return outer_coordinator_agent
