from autogen_agentchat.agents import SocietyOfMindAgent
from teams.inner_teams.report_drafting_inner_team import (
    get_report_drafting_team,
)


def get_report_society(model_client):

    report_drafting_inner_team = get_report_drafting_team(
        model_client
    )

    report_society = SocietyOfMindAgent(
        name="ReportSociety",
        team=report_drafting_inner_team,
        model_client=model_client,
        response_prompt="Return the finalized, polished report body.",
    )
    return report_society
