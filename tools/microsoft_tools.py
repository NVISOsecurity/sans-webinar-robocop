from autogen_core.tools import FunctionTool

from utils.microsoft import *

tool_get_sentinel_incident_by_number = FunctionTool(
    name="get_sentinel_incident_by_id",
    description="Retrieve the Microsoft Sentinel incident with incident number.",
    func=get_incident_by_incident_number,
)

tool_get_sentinel_incident_alerts = FunctionTool(
    name="get_sentinel_incident_alerts",
    description="Retrieve the alerts associated with the Microsoft Sentinel incident.",
    func=get_incident_alerts,
)

tool_get_sentinel_incident_entities = FunctionTool(
    name="get_sentinel_incident_entities",
    description="Retrieve the entities associated with the Microsoft Sentinel incident.",
    func=get_incident_entities,
)

tool_get_sentinel_incident_by_id = FunctionTool(
    name="get_sentinel_incident_by_id",
    description="Retrieve the Microsoft Sentinel incident with incident id in human readable output.",
    func=get_incident_by_id,
)

tool_get_human_readable_sentinel_incident_alerts = FunctionTool(
    name="get_human_readable_sentinel_incident_alerts",
    description="Retrieve the alerts associated with the Microsoft Sentinel incident in human readable output.",
    func=get_human_readable_incident_alerts,
)

tool_get_human_readable_sentinel_incident_entities = FunctionTool(
    name="get_human_readable_sentinel_incident_entities",
    description="Retrieve the entities associated with the Microsoft Sentinel incident in human readable output.",
    func=get_human_readable_incident_entities,
)

tool_get_human_readable_sentinel_incident_by_id = FunctionTool(
    name="get_human_readable_sentinel_incident_by_id",
    description="Retrieve the Microsoft Sentinel incident with incident id.",
    func=get_human_readable_incident_by_id,
)

tool_execute_kql_sentinel_log_analytics_workspace = FunctionTool(
    name="execute_kql_sentinel_log_analytics_workspace",
    description="Execute a KQL query in the Microsoft Sentinel Log Analytics workspace.",
    func=query_sentinel_log_analytics_workspace,
)

tool_get_sentinel_tables_schema = FunctionTool(
    name="get_sentinel_tables_schema",
    description="Retrieve the tables with data larger than 1MB available in the Microsoft Sentinel Log Analytics workspace with their columns and field types.",
    func=get_sentinel_tables,
)
