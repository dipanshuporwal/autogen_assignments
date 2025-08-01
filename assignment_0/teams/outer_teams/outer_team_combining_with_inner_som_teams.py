from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from som.analysis_society import get_analysis_society
from som.report_society import get_report_society
from teams.inner_teams.report_drafting_inner_team import (
    get_report_drafting_team,
)
from agents.outer_team_agents.coordinator_user_proxy_agent import (
    get_outer_coordinator_agent,
)


def get_outer_team(model_client):

    analysis_society = get_analysis_society(model_client)

    report_society = get_report_society(model_client)

    outer_user_proxy_agent = get_outer_coordinator_agent()

    outer_termination = TextMentionTermination("FINALIZE")
    outer_team = RoundRobinGroupChat(
        participants=[
            analysis_society,
            report_society,
            outer_user_proxy_agent,
        ],
        termination_condition=outer_termination,
        max_turns=10,
    )

    return outer_team
