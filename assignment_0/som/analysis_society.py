from autogen_agentchat.agents import SocietyOfMindAgent
from teams.inner_teams.data_analysis_inner_team import get_data_analysis_team


def get_analysis_society(model_client):

    data_analysis_inner_team = get_data_analysis_team(model_client)

    analysis_society = SocietyOfMindAgent(
        name="AnalysisSociety",
        team=data_analysis_inner_team,
        model_client=model_client,
        response_prompt=(
            "Summarize insights in business-friendly terms under 100 words."
        ),
    )
    return analysis_society
