from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from config.constants import OPENAI_MODEL, OPENAI_API_VERSION 
import os
from dotenv import load_dotenv

load_dotenv()

def get_model_client():
    azure_client = AzureOpenAIChatCompletionClient(
        model=OPENAI_MODEL,
        api_version=OPENAI_API_VERSION,
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("API_KEY"),
    )

    return azure_client
