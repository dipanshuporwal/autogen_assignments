from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.inner_team_agents.report_drafting_agents.draft_writer_agent import (
    get_draft_writer_agent,
)
from agents.inner_team_agents.report_drafting_agents.content_editor_agent import (
    get_content_editor_agent,
)

from agents.inner_team_agents.report_drafting_agents.format_specialist_agent import (
    get_format_specialist_agent,
)

from agents.inner_team_agents.report_drafting_agents.draft_supervisor_user_proxy_agent import (
    get_inner_draft_supervisor_agent,
)


def get_report_drafting_team(model_client):

    draft_writer_agent = get_draft_writer_agent(model_client)

    content_editor_agent = get_content_editor_agent(model_client)

    format_specialist_agent = get_format_specialist_agent(model_client)

    inner_draft_supervisor_agent = get_inner_draft_supervisor_agent()

    inner_termination = TextMentionTermination("APPROVED")
    inner_team = RoundRobinGroupChat(
        participants=[
            draft_writer_agent,
            content_editor_agent,
            format_specialist_agent,
            inner_draft_supervisor_agent,
        ],
        termination_condition=inner_termination,
        max_turns=10,
    )

    return inner_team
