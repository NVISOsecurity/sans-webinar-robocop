#!/usr/bin/python3

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

from utils.constants import *
from tools.microsoft_tools import *
from models.azure_openai import *


soc_analyst_agent = AssistantAgent(
    description=("You are an advanced senior SOC analyst Agent. "
                 "Your responsibility is to analyze Microsoft Sentinel incidents including alerts and entities. "
                 "You can do additional KQL queries to the Microsoft Sentinel Log Analytics workspace get additional information for your analysis."
    ),
    name="soc_analyst",
    model_client=gpt_4o_client,
    tools=[tool_get_sentinel_incident_by_id, tool_get_sentinel_incident_alerts, tool_get_sentinel_incident_entities, tool_execute_kql_sentinel_log_analytics_workspace],
    system_message=(
        "You should use tools to get incident, alert and entity data."
        "Return TERMINATE when you have concluded your analysis."
    ),
    reflect_on_tool_use=True
)

termination_condition = TextMentionTermination("TERMINATE")

team = RoundRobinGroupChat(
    [soc_analyst_agent],
    termination_condition=termination_condition,
)

async def main():
    sentinel_incident_id = "148583a3-970f-4d1f-84dc-4da50b027695"

    task = (
        f"Retrieve the Microsoft Sentinel incident with incident id  '{sentinel_incident_id}', "
        "including all related alerts and entities, and analyze the security incident by performing additional KQL queries to the logs to verify your findings. "
        "Assign one of the following close reasons 'Impacted', 'Harmless', 'False Positive' or 'Insufficient Information' and "
        "provide close notes which explains summarizes the analysis and how you reached that conclusion."
    )
    
    await Console(team.run_stream(task=task))


if __name__ == "__main__":
    asyncio.run(main())