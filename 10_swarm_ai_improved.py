#!/usr/bin/python3

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console

from utils.constants import *
from tools.microsoft_tools import *
from tools.file_tools import *
from tools.xsoar_tools import *
from models.azure_openai import *


soc_analyst = AssistantAgent(
    description=(
        "You are a senior SOC Analyst agent responsible for orchestrating the full investigation of security incidents. "
        "Your role is to guide the analysis process, delegate tasks to supporting agents, and synthesize findings. "
        "You begin by retrieving incident, alert, and entity data from Sentinel using the sentinel_info agent (only once). "
        "You then fetch corresponding incident data from XSOAR using the sentinel incident number via the xsoar_info agent. "
        "After all data is gathered, use the kql_sentinel_query agent to craft and execute KQL queries for log analysis. "
        "Always hand off tasks to a single agent at a time. Your final output must include a conclusive close reason and supporting close notes."
    ),
    name="soc_analyst",
    model_client=gpt_4o_client,
    handoffs=["sentinel_info", "xsoar_info", "kql_sentinel_query"],
    system_message=(
        "Your goal is to coordinate an end-to-end analysis of a Microsoft Sentinel incident. "
        "Use tools and agents only as needed. Do not write KQL queries yourself, use the kql_sentinel_query agent. "
        "Always retrieve the Sentinel incident first (via sentinel_info), then retrieve the XSOAR incident using the sentinel incident number. "
        "Use the KQL agent for any log data validation. "
        "Once your investigation is complete, return TERMINATE along with a clear close reason and detailed explanation."
    )
)

sentinel_info = AssistantAgent(
    name="sentinel_info",
    model_client=gpt_4o_mini_client,
    handoffs=["soc_analyst"],
    tools=[
        tool_get_human_readable_sentinel_incident_entities, 
        tool_get_human_readable_sentinel_incident_alerts, 
        tool_get_human_readable_sentinel_incident_by_id
    ],
    description=(
        "You are a Microsoft Sentinel incident data retrieval agent. "
        "Your role is to fetch the full incident, its related alerts, and involved entities from Microsoft Sentinel."
    ),
    system_message=(
        "Retrieve incident details, related alerts, and entities from Microsoft Sentinel. "
        "Do not perform any analysis or interpretation. Do not generate close reasons or notes. "
        "After completing your task, always hand off back to the soc_analyst agent."
    )
)

xsoar_info = AssistantAgent(
    name="xsoar_info",
    model_client=gpt_4o_mini_client,
    handoffs=["soc_analyst"],
    tools=[tool_get_xsoar_incident_by_sentinel_incident_number],
    description=(
        "You are a Cortex XSOAR data retrieval agent. "
        "You are responsible for fetching the incident details from XSOAR using the Sentinel incident number (not the GUID)."
    ),
    system_message=(
        "Retrieve the XSOAR incident using the Sentinel incident number. "
        "Do not perform any analysis. Do not determine close reasons or notes. "
        "Once data is retrieved, hand off back to the soc_analyst agent."
    )
)

kql_sentinel_query = AssistantAgent(
    description=(
        "You are a specialized agent for building and executing KQL queries in Microsoft Sentinel's Log Analytics workspace. "
        "You support investigations by fetching and analyzing log data to verify or refute hypotheses about incidents."
    ),
    name="kql_sentinel_query",
    tools=[
        tool_execute_kql_sentinel_log_analytics_workspace, 
        tool_get_sentinel_tables_schema
    ],
    handoffs=["soc_analyst"],
    model_client=gpt_4o_client,
    system_message=(
        "Always begin by retrieving the schema of the relevant Sentinel tables. "
        "Use this schema to build accurate KQL queries. Limit queries to a 3-day window around the time of the incident. "
        "Do not retrieve alerts or entities—only log data. Do not assign close reasons or write close notes. "
        "After reviewing the query result, reflect and then hand off back to the soc_analyst agent."
    ),
    reflect_on_tool_use=True
)


termination = TextMentionTermination("TERMINATE")

team = Swarm(
    participants=[soc_analyst, sentinel_info, kql_sentinel_query, xsoar_info], termination_condition=termination
)
async def main():
    sentinel_incident_id = "e4075c44-21c3-404e-a6a7-33ff041092a3"

    task = (
        f"Retrieve the Microsoft Sentinel incident with ID '{sentinel_incident_id}', "
        "including all associated alerts and entities. Perform a structured analysis of the incident by coordinating with supporting agents. "
        "Use KQL queries to validate your findings using log data. "
        "Based on your investigation, determine whether the incident is a 'True Positive', 'False Positive', 'Harmless', or 'Insufficient Information'. "
        "Provide a detailed explanation in the close notes justifying your assessment."
    )

    await Console(team.run_stream(task=task))


if __name__ == "__main__":
    asyncio.run(main())