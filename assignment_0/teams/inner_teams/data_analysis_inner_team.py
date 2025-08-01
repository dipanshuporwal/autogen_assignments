from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.inner_team_agents.data_analysis_agents.data_collector_agent import (
    get_data_collector_agent,
)
from agents.inner_team_agents.data_analysis_agents.data_interpreter_agent import (
    get_data_interpreter_agent,
)

from agents.inner_team_agents.data_analysis_agents.data_presenter_agent import (
    get_data_presenter_agent,
)

from agents.inner_team_agents.data_analysis_agents.supervisor_user_proxy_agent import (
    get_inner_supervisor_agent,
)


def get_data_analysis_team(model_client):

    data_collector_agent = get_data_collector_agent(model_client)

    data_interpreter_agent = get_data_interpreter_agent(model_client)

    data_presenter_agent = get_data_presenter_agent(model_client)

    inner_user_proxy_agent = get_inner_supervisor_agent()

    inner_termination = TextMentionTermination("APPROVED")
    inner_team = RoundRobinGroupChat(
        participants=[
            data_collector_agent,
            data_interpreter_agent,
            data_presenter_agent,
            inner_user_proxy_agent,
        ],
        termination_condition=inner_termination,
        max_turns=10,
    )

    return inner_team
