#!/usr/bin/python3

import asyncio

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.base import TaskResult
from autogen_core import CancellationToken

from utils.constants import *
from tools.microsoft_tools import *
from models.azure_openai import *

soc_analyst_agent = AssistantAgent(
    description=("You are an advanced senior SOC analyst Agent. "
                 "Your responsibility is to analyze Microsoft Sentinel incidents including alerts. "
    ),
    name="soc_analyst",
    model_client=gpt_4o_client,
    tools=[tool_get_sentinel_incident_by_id, tool_get_sentinel_incident_alerts, tool_get_sentinel_incident_entities],
    system_message=("You should use tools to get incident, alert and entity data."),
    reflect_on_tool_use=True
)

async def assistant_run_stream(message_content) -> None:
    await Console(
        soc_analyst_agent.on_messages_stream(
            [TextMessage(content=message_content, source="user")],
            cancellation_token=CancellationToken(),
        ),
        output_stats=True,  # Enable stats printing.
    )

async def main():
    sentinel_incident_id = "148583a3-970f-4d1f-84dc-4da50b027695"

    message = (
        f"Retrieve the Microsoft Sentinel incident with incident id  '{sentinel_incident_id}', including all related alerts and entities." 
        "Give a summary of the incident, alerts and entities."
        "Create a detailed step by step analysis procedure including KQL queries that should be executed to conclude if the incident is a true positive or false positive."
    
    )

    await assistant_run_stream(message_content=message)

if __name__ == "__main__":
    asyncio.run(main())