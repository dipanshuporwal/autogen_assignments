from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv()


def get_model_client():
    azure_client = AzureOpenAIChatCompletionClient(
        model=os.getenv("MODEL"),
        api_version=os.getenv("API_VERSION"),
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("API_KEY"),
    )

    return azure_client
