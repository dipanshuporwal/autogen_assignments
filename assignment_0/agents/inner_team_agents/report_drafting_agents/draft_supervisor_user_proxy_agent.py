from autogen_agentchat.agents import UserProxyAgent


def get_inner_draft_supervisor_agent():
    inner_draft_supervisor_agent = UserProxyAgent(
        name="DraftSupervisorAgent",
        description="Human-in-the-loop for finalizing the report draft",
        input_func=input,
    )
    return inner_draft_supervisor_agent
