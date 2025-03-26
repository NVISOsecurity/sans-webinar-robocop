#!/usr/bin/python3

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console

from utils.constants import *
from tools.microsoft_tools import *
from tools.file_tools import *
from models.azure_openai import *


soc_analyst = AssistantAgent(
    description=("You are an advanced senior SOC analyst Agent. "
                 "Your responsibility is to analyze Microsoft Sentinel incidents including alerts."
                 "You should create a detailed step by step analysis procedure and coordinate the analysis by delagating to specialized agents:\n"
                "- Use sentinel_info agent only once to retrieve incidents, alerts and entities.\n"
                "- Use kql_sentinel_query agent to create and execute KQL queries in Microsoft Sentinel Log Analytics workspace.\n"
                "Always handoff to a single agent at a time."
    ),
    name="soc_analyst",
    model_client=gpt_4o_client,
    handoffs=["sentinel_info", "kql_sentinel_query"],
    system_message=(
        "You should use tools to get incident, alert and entity data and do KQL queries."
        "Do not create KQL queries yourself. Use the kql_sentinel_query agent for that."
        "Return TERMINATE when you have concluded your analysis."
    )
)

sentinel_info = AssistantAgent(
    name="sentinel_info",
    model_client=gpt_4o_mini_client,
    handoffs=["soc_analyst"],
    tools=[tool_get_human_readable_sentinel_incident_entities, tool_get_human_readable_sentinel_incident_alerts, tool_get_human_readable_sentinel_incident_by_id],
    description="You are a dedicated Microsoft Sentinel Incident Retrieval Agent. Your primary responsibility is to retrieve incidents, alerts, and related from Microsoft Sentinel.",
    system_message=(
        "Always handoff back to soc_analyst after retrieving incident, alert and entity data."
        "Do now analyze the data. That is the responsibility of the soc_analyst agent."
        "Do not define a close reason or close notes. That is the responsibility of the soc_analyst agent."                
    ),
)

kql_sentinel_query = AssistantAgent(
    description="You are a dedicated KQL Query Builder and Execution Agent. Your primary responsibility is to create KQL queries and execute them in Microsoft Sentinel Log Analytics workspace.",
    name="kql_sentinel_query",
    tools=[tool_execute_kql_sentinel_log_analytics_workspace, tool_get_sentinel_tables_schema],
    handoffs=["soc_analyst"],
    model_client=gpt_4o_client,
    system_message=(
        "Before executing a KQL query, get the schema of the tables in the Microsoft Sentinel Log Analytics workspace to know which tables and collumn names are available to create KQL queries."
        "Limit the timespan of the queries to a timespan of around the time of the incident."
        "Do not define a close reason or close notes. That is the responsibility of the soc_analyst agent."
        "Always handoff back to soc_analyst after reflecing on the data returned by executing the KQL query. "
        "Do not use KQL queries to get incident, alert and entity data. That is the responsibility of the sentinel_info agent."
    ),
)


termination = TextMentionTermination("TERMINATE")

team = Swarm(
    participants=[soc_analyst, sentinel_info, kql_sentinel_query], termination_condition=termination
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