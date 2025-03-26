#!/usr/bin/python3

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
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
    tools=[tool_get_sentinel_incident_by_id, tool_get_sentinel_incident_alerts, tool_get_sentinel_incident_entities, tool_execute_kql_sentinel_log_analytics_workspace],
    system_message=("You should use tools to get incident, alert and entity data and perform queries to Microsoft Sentinel Log Analytics workspace or Microsoft Defender Advanced Hunting to verify your findings."),
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
        f"Retrieve the Microsoft Sentinel incident with incident id  '{sentinel_incident_id}', "
        "including all related alerts and entities, and analyze the security incident by performing additional KQL queries to the logs to verify your findings. "
        "Assign one of the following close reasons 'Impacted', 'Harmless', 'False Positive' or 'Insufficient Information' and "
        "provide close notes which explains summarizes the analysis and how you reached that conclusion."
    )

    await assistant_run_stream(message_content=message)

if __name__ == "__main__":
    asyncio.run(main())