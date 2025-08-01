import asyncio
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


async def main():

    model_client = get_model_client()
    docker = getDockerCommandLineExecutor()

    outer_team = get_outer_team(model_client)

    try:
        task = (
            "Evaluate Q2 business performance and generate an executive report"
            " with analysis and recommendations. Data: Product A (1200 units),"
            " Product B (900), Product C (400). Revenue: A ($12K), B ($8K), C"
            " ($4K)."
        )

        await start_docker_container(docker)

        stream = outer_team.run_stream(task=task)

        await Console(stream)

    except Exception as e:
        print(e)
    finally:
        await stop_docker_container(docker)


if __name__ == "__main__":
    asyncio.run(main())
