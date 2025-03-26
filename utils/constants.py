import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

SENTINEL_API_VERSION = "2024-09-01"

SENTINEL_RESOURCE = "https://management.azure.com"
LAW_RESOURCE = "https://api.loganalytics.io"
ADVANCED_HUNTING_RESOURCE = "https://api.security.microsoft.com"

AZURE_OPENAI_GPT_4O_MINI_DEPLOYMENT= os.getenv("AZURE_OPENAI_GPT_4O_MINI_DEPLOYMENT")
AZURE_OPENAI_GPT_4O_DEPLOYMENT = os.getenv("AZURE_OPENAI_GPT_4O_DEPLOYMENT")
AZURE_OPENAI_API_VERSION= os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT= os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY= os.getenv("AZURE_OPENAI_API_KEY")

# Azure AD credentials
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Microsoft Sentinel details
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP")
WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")

# OAuth2 token endpoint
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"

SENTINEL_BASE_URL = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.OperationalInsights/workspaces/{WORKSPACE_NAME}/providers/Microsoft.SecurityInsights/"

SENTINEL_ACCESS_TOKEN = None
LAW_ACCESS_TOKEN = None
ADVANCED_HUNTING_ACCESS_TOKEN = None

XSOAR_URL = os.getenv("XSOAR_URL")
XSOAR_API_KEY = os.getenv("XSOAR_API_KEY")