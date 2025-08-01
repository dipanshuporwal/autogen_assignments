from autogen_agentchat.agents import UserProxyAgent


def get_inner_supervisor_agent():
    inner_supervisor_agent = UserProxyAgent(
        name="InnerSupervisorAgent",
        description=(
            "Human-in-the-loop who supervises the inner team's analysis,"
            " providing feedback or approval."
        ),
        input_func=input,
    )
    return inner_supervisor_agent
