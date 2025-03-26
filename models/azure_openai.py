from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from utils.constants import *

gpt_4o_client = AzureOpenAIChatCompletionClient(
    azure_deployment=AZURE_OPENAI_GPT_4O_DEPLOYMENT,
    model="gpt-4o",
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,  # For key-based authentication.
)

gpt_4o_mini_client = AzureOpenAIChatCompletionClient(
    azure_deployment=AZURE_OPENAI_GPT_4O_MINI_DEPLOYMENT,
    model="gpt-4o-mini",
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,  # For key-based authentication.
)