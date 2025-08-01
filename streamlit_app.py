import asyncio
import streamlit as st
from autogen_agentchat.ui import Console
from teams.outer_teams.outer_team_combining_with_inner_som_teams import (
    get_outer_team,
)
from models.azure_openai_client import get_model_client
from config.docker_util import (
    getDockerCommandLineExecutor,
    start_docker_container,
    stop_docker_container,
)

st.set_page_config(page_title="Agent Streaming UI", layout="wide")
st.title("🧠 UserProxyAgent Integration in SoM Teams")

# User input and trigger
default_task = (
    "Evaluate Q2 business performance and generate an executive report"
    " with analysis and recommendations. Data: Product A (1200 units),"
    " Product B (900), Product C (400). Revenue: A ($12K), B ($8K), C"
    " ($4K)."
)
task = st.text_area("📝 Task for Agent:", value=default_task, height=150)
run_button = st.button("🚀 Run Agent")


# Async logic
async def stream_to_streamlit(stream, output_placeholder):
    await Console(stream)
    full_output = ""
    async for chunk in stream:
        text_chunk = str(chunk)
        full_output += text_chunk
        output_placeholder.markdown(text_chunk, unsafe_allow_html=True)
    return full_output


async def run_agent(task: str):
    model_client = get_model_client()
    docker = getDockerCommandLineExecutor()
    outer_team = get_outer_team(model_client)

    await start_docker_container(docker)

    try:
        stream = outer_team.run_stream(task=task)

        output_placeholder = st.empty()
        final_output = await stream_to_streamlit(stream, output_placeholder)

        # Save final output to file
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(final_output)

        st.success("✅ Output saved to `output.txt`")
    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        await stop_docker_container(docker)


# Run task on button click
if run_button:
    asyncio.run(run_agent(task))
