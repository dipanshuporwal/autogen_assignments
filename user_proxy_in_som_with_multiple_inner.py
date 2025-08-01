import asyncio
import os
from dotenv import load_dotenv
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import (
    AssistantAgent,
    UserProxyAgent,
    SocietyOfMindAgent,
)
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from config.constants import OPENAI_MODEL, OPENAI_API_VERSION

# Load your environment variables
load_dotenv()

# Create Azure model client
model_client = AzureOpenAIChatCompletionClient(
    model=OPENAI_MODEL,
    api_version=OPENAI_API_VERSION,
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("API_KEY"),
)

# =====================================================
# PART A: Inner Team Integration
# =====================================================

# Human-in-the-loop agent for feedback, approvals, overrides
inner_user_proxy = UserProxyAgent(
    name="InnerSupervisor",
    description=(
        "Human-in-the-loop who supervises the inner team's analysis, providing"
        " feedback or approval."
    ),
    input_func=input,  # CLI-based feedback
)

# Specialized assistant agents for data analysis task
data_collector = AssistantAgent(
    name="DataCollector",
    model_client=model_client,
    system_message=(
        "Collects relevant data from past performance and current market"
        " conditions."
    ),
)

data_interpreter = AssistantAgent(
    name="DataInterpreter",
    model_client=model_client,
    system_message=(
        "Performs detailed interpretation of the collected data. Identify"
        " trends and anomalies."
    ),
)


data_presenter = AssistantAgent(
    name="DataPresenter",
    model_client=model_client,
    system_message=(
        "Summarizes interpreted data into easy-to-understand insights."
    ),
)

# Inner team group chat
inner_termination = TextMentionTermination("APPROVE")
inner_team = RoundRobinGroupChat(
    participants=[
        data_collector,
        data_interpreter,
        data_presenter,
        inner_user_proxy,
    ],
    termination_condition=inner_termination,
    max_turns=10,
)

# SocietyOfMindAgent that wraps the inner team
analysis_society = SocietyOfMindAgent(
    name="AnalysisTeam",
    team=inner_team,
    model_client=model_client,
    response_prompt=(
        "Summarize insights in business-friendly terms under 100 words."
    ),
)

# =====================================================
# PART B: Outer Team Integration
# =====================================================

# Additional inner team (e.g., report drafting)
draft_writer = AssistantAgent(
    name="DraftWriter",
    model_client=model_client,
    system_message=(
        "Writes the final report using insights provided by the analysis team."
    ),
)

content_editor = AssistantAgent(
    name="ContentEditor",
    model_client=model_client,
    system_message="Edits the draft for tone, clarity, and completeness.",
)

format_specialist = AssistantAgent(
    name="FormatSpecialist",
    model_client=model_client,
    system_message=(
        "Ensures the final report is visually formatted for business"
        " audiences."
    ),
)

outer_inner_user_proxy = UserProxyAgent(
    name="DraftSupervisor",
    description="Human-in-the-loop for finalizing the report draft",
    input_func=input,
)

drafting_team = RoundRobinGroupChat(
    participants=[
        draft_writer,
        content_editor,
        format_specialist,
        outer_inner_user_proxy,
    ],
    termination_condition=TextMentionTermination("APPROVED"),
    max_turns=5,
)

report_society = SocietyOfMindAgent(
    name="ReportTeam",
    team=drafting_team,
    model_client=model_client,
    response_prompt="Return the finalized, polished report body.",
)

# Top-level user proxy for inter-team coordination
outer_user_proxy = UserProxyAgent(
    name="Coordinator",
    description="Coordinates resources across teams, oversees final output",
    input_func=input,
)

# Outer team combining inner SoM teams
outer_termination = TextMentionTermination("FINALIZE")
outer_team = RoundRobinGroupChat(
    participants=[analysis_society, report_society, outer_user_proxy],
    termination_condition=outer_termination,
    max_turns=5,
)

# =====================================================
# MAIN EXECUTION
# =====================================================

stream = outer_team.run_stream(
    task=(
        "Evaluate Q2 business performance and generate an executive report"
        " with analysis and recommendations. Data: Product A (1200 units),"
        " Product B (900), Product C (400). Revenue: A ($12K), B ($8K), C"
        " ($4K)."
    )
)


async def main():
    await Console(stream)


if __name__ == "__main__":
    asyncio.run(main())
